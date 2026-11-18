# Workflow, automation and dispatch · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Automation flow

<a id="op-d6d73ac0a0c352"></a>
### Automation Flow.on trash

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_on_trash`

**Inputs** self.

**State and service calls** request delete on “Automation Trigger Queue”.

**Local steps**

- Evaluate clear\_automation\_cache(self.document\_type).
- Set queue from Platform.qb.DocType(“Automation Trigger Queue”).
- Set subscription from Platform.qb.DocType(“Automation Event Subscription”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(subscription.resume\_queue.isin(nested operand in the contract(nested operand in the contract).where(nested operand in the contr ….run().
- Evaluate Platform.db.delete(“Automation Trigger Queue”, mapping(“automation” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L266)

## Record · Automation run

<a id="op-61f7cb9813f517"></a>
### Automation Run.clear old logs

`operation_foundation_binding_foundation_automation_doctype_automation_run_automation_run_automationrun_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on step · request delete on run.

**Local steps**

- Set run from Platform.qb.DocType(“Automation Run”).
- Set old from (run.creation &lt; (Now() − Interval(days = days)) bitwise and run.status differs from “Waiting”).
- Set names from nested operand in the contract.qb.from\_(run).select(run.name).where(old).
- Set step from Platform.qb.DocType(“Automation Run Step”).
- Evaluate Platform.db.delete(step, filters = step.parent.isin(names)).
- Evaluate Platform.db.delete(run, filters = old).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L285)

<a id="op-1713bcfc0bc015"></a>
### On doctype update

`operation_foundation_binding_foundation_automation_doctype_automation_run_automation_run_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Automation Run”.

**Local steps**

- Evaluate Platform.db.add\_index(“Automation Run”, list(“automation”, “creation”)).
- Evaluate Platform.db.add\_index(“Automation Run”, list(“reference\_doctype”, “reference\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L286)

## Record · Automation trigger queue

<a id="op-05460f7c6ea50c"></a>
### On doctype update

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_on_doctype_update`

**Inputs** no declared parameters.

**Local steps**

- Evaluate ensure\_dedup\_indexes().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L290)

<a id="op-8a69b2a3192898"></a>
### Ensure dedup indexes

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_ensure_dedup_indexes`

**Inputs** no declared parameters.

**State and service calls** request add\_index on QUEUE.

**Local steps**

- If Platform.db.db\_type equals “mariadb”.
  - Evaluate \_ensure\_dedup\_column().
  - If not Platform.db.has\_index(TABLE, DEDUP\_INDEX).
    - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{TABLE}′ ADD UNIQUE INDEX ′{DEDUP\_INDEX}′ (′dedup\_key′)).
- Otherwise.
  - Evaluate \_ensure\_partial\_dedup\_index().
- Evaluate Platform.db.add\_index(QUEUE, list(“status”, “run\_after”, “triggered\_at”), “drain\_scan”).
- Evaluate Platform.db.add\_index(QUEUE, list(“automation”, “ref\_doctype”, “ref\_name”), LOOKUP\_INDEX).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L288)

<a id="op-eac86a26075c02"></a>
### Waiting states sql

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_waiting_states_sql`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** “, ”.join(generator of Platform.db.escape(state) for state drawn from WAITING\_STATES).

**Local steps**

- Return “, ”.join(generator of Platform.db.escape(state) for state drawn from WAITING\_STATES).
  - Draw state from WAITING\_STATES.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L292)

<a id="op-0a1fc5bb0b7b0e"></a>
### Ensure partial dedup index

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_ensure_partial_dedup_index`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.db.sql\_ddl(formatted text DROP INDEX IF EXISTS ′{DEDUP\_INDEX}′).
- Evaluate Platform.db.sql\_ddl(formatted text   CREATE UNIQUE INDEX ′{DEDUP\_INDEX}′ ON ′{TABLE}′ (′automation′, ′ref\_doctype′, ′ref\_name′)  WHERE ′status′ IN ({\_waiting\_states\_sql()}) AND ′resum).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L289)

<a id="op-9bfc93364afce8"></a>
### Ensure dedup column

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_ensure_dedup_column`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT).

**Explicit results** no value.

**Local steps**

- Set expression from Platform.db.sql(query text (SELECT), TABLE).
- If (expression and all(generator of state belongs to (nested operand in the contract at nested operand in the contract at 0 or empty text) for state drawn from WAITING\_STATES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expression → all(generator of state belongs to (expression at 0 at 0 or empty text) for state drawn from WAITING\_STATES).
  - Draw state from WAITING\_STATES.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expression at 0 at 0 → empty text.
  - Return no value.
- Evaluate \_rebuild\_dedup\_column().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L287)

<a id="op-703c721ca4910a"></a>
### Rebuild dedup column

`operation_foundation_binding_foundation_automation_doctype_automation_trigger_queue_automation_trigger_queue_rebuild_dedup_column`

**Inputs** no declared parameters.

**Local steps**

- If Platform.db.has\_index(TABLE, DEDUP\_INDEX).
  - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{TABLE}′ DROP INDEX ′{DEDUP\_INDEX}′).
- If Platform.db.has\_column(QUEUE, “dedup\_key”).
  - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{TABLE}′ DROP COLUMN ′dedup\_key′).
  - Evaluate Platform.client\_cache.delete\_value(formatted text table\_columns::{TABLE}).
- Evaluate Platform.db.sql\_ddl(formatted text   ALTER TABLE ′{TABLE}′  ADD COLUMN ′dedup\_key′ VARCHAR(420)  AS (  CASE WHEN ′status′ IN ({\_waiting\_states\_sql()}) AND ′resume\_run′ IS NULL  T).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L291)

## Service · Base

<a id="op-e744a10cd4b5d1"></a>
### Render value

`operation_foundation_binding_foundation_automation_engine_actions_base_render_value`

**Inputs** value, doc, context = no value.

**Explicit results** Platform.render\_template(value, render\_context(doc, context)) · value.

**Local steps**

- If (isinstance(value, str) and “{{” belongs to value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → “{{” belongs to value.
  - Return Platform.render\_template(value, render\_context(doc, context)).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L305)

<a id="op-d895de16adce87"></a>
### Render context

`operation_foundation_binding_foundation_automation_engine_actions_base_render_context`

**Inputs** doc, context = no value.

**Explicit results** mapping(“doc” → doc, “target” → doc, “trigger” → (context.get(“trigger\_doc”) or doc), “payload” → (context.get(“payload”) or mapping()), …).

**Local steps**

- Set context from (context or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → mapping().
- Return mapping(“doc” → doc, “target” → doc, “trigger” → (context.get(“trigger\_doc”) or doc), “payload” → (context.get(“payload”) or mapping()), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.get(“trigger\_doc”) → doc.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.get(“payload”) → mapping().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L304)

<a id="op-42d9203bc65993"></a>
### Automation Param Error.initialize

`operation_foundation_binding_foundation_automation_engine_actions_base_automationparamerror_init`

**Inputs** self, message, fieldname = no value.

**Local steps**

- Set self.fieldname from fieldname.
- Evaluate super().\_\_init\_\_(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L300)

<a id="op-4d548513cf2878"></a>
### Stop Automation.initialize

`operation_foundation_binding_foundation_automation_engine_actions_base_stopautomation_init`

**Inputs** self, message = empty text, resume\_after = 60.

**Local steps**

- Set self.resume\_after from resume\_after.
- Evaluate super().\_\_init\_\_(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L306)

<a id="op-e98fa782ca220f"></a>
### Automation Action.validate

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_validate`

**Inputs** self, params, doctype.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L299)

<a id="op-ad5954d4d5993a"></a>
### Automation Action.output doctype

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_output_doctype`

**Inputs** self, params.

**Declared result** (str bitwise or no value).

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L297)

<a id="op-1af20f44c701a0"></a>
### Automation Action.output targets

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_output_targets`

**Inputs** self, params, output\_alias.

**Declared result** dict.

**Explicit results** mapping(output\_alias → self.output\_doctype(params)) when output\_alias, otherwise mapping().

**Local steps**

- Return mapping(output\_alias → self.output\_doctype(params)) when output\_alias, otherwise mapping().
  - Value choice on output\_alias — true gives mapping(output\_alias → self.output\_doctype(params)), false gives mapping().

**Methods declared on this owner** [output doctype](operations-009.md#op-ad5954d4d5993a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L298)

<a id="op-c3050abe55545e"></a>
### Automation Action.execute

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_execute`

**Inputs** self, doc, params, context.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L296)

<a id="op-b4eb87a84b384d"></a>
### Automation Action.app

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_app`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** type(self).\_\_module\_\_.split(“.”) at 0.

**Local steps**

- Return type(self).\_\_module\_\_.split(“.”) at 0.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L294)

<a id="op-55299027b5f4ee"></a>
### Automation Action.as dict

`operation_foundation_binding_foundation_automation_engine_actions_base_automationaction_as_dict`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“action\_type” → self.action\_type, “label” → self.label, “app” → self.app, “app\_title” → \_app\_title(self.app), …).

**Local steps**

- Return mapping(“action\_type” → self.action\_type, “label” → self.label, “app” → self.app, “app\_title” → \_app\_title(self.app), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L295)

<a id="op-12de43d7461984"></a>
### App title

`operation_foundation_binding_foundation_automation_engine_actions_base_app_title`

**Inputs** app.

**Declared result** str.

**Explicit results** (Platform.get\_hooks(“app\_title”, app\_name = app) or list(app)) at 0.

**Local steps**

- Return (Platform.get\_hooks(“app\_title”, app\_name = app) or list(app)) at 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app) → list(app).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L293)

<a id="op-9e41919bd99c18"></a>
### Get action registry

`operation_foundation_binding_foundation_automation_engine_actions_base_get_action_registry`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** Platform.local.automation\_actions · registry.

**Explicit failure paths** validation helper — translated “Duplicate automation action\_type: {0}”.format(action.action\_type).

**Local steps**

- If getattr(Platform.local, “automation\_actions”, no value) is distinct from no value.
  - Return Platform.local.automation\_actions.
- Set registry from mapping().
- For each cls in \_iter\_action\_classes().
  - Set action from cls().
  - If action.action\_type belongs to registry.
    - Call the validation error handler Platform.throw(translated “Duplicate automation action\_type: {0}”.format(action.action\_type)).
  - Set registry at action.action\_type from action.
- Set Platform.local.automation\_actions from registry.
- Return registry.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “automation\_actions”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L302)

<a id="op-f3650a499c35b4"></a>
### Get action

`operation_foundation_binding_foundation_automation_engine_actions_base_get_action`

**Inputs** action\_type.

**Declared result** AutomationAction.

**Explicit results** action.

**Explicit failure paths** validation helper — translated “Unknown automation action: {0}”.format(action\_type).

**Local steps**

- Set action from get\_action\_registry().get(action\_type).
- If not action.
  - Call the validation error handler Platform.throw(translated “Unknown automation action: {0}”.format(action\_type)).
- Return action.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L301)

<a id="op-67acdcfb1f952f"></a>
### Iter action classes

`operation_foundation_binding_foundation_automation_engine_actions_base_iter_action_classes`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies CORE\_ACTIONS.
- yield values from CORE\_ACTIONS.
- For each path in Platform.get\_hooks(“automation\_actions”).
  - yield Platform.get\_attr(path).

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“automation\_actions”), Platform.get\_attr(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L303)

## Service · Boot

<a id="op-d0542d564c8974"></a>
### Boot session

`operation_foundation_binding_foundation_flow_boot_boot_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** bootinfo.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L873)
