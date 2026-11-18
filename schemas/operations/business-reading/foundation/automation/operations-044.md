# Workflow, automation and dispatch · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Safe exec

<a id="op-dbeeb16c415494"></a>
### Permissioned get single value

`operation_foundation_binding_foundation_flow_utils_safe_exec_permissioned_get_single_value`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, fieldname.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1439)

<a id="op-831dfb102793ca"></a>
### Permissioned exists

`operation_foundation_binding_foundation_flow_utils_safe_exec_permissioned_exists`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, filters.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1437)

<a id="op-a799fd1f23df95"></a>
### Permissioned count

`operation_foundation_binding_foundation_flow_utils_safe_exec_permissioned_count`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, filters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1436)

<a id="op-b976efbcc1cc1a"></a>
### Flow builtins

`operation_foundation_binding_foundation_flow_utils_safe_exec_flow_builtins`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** tool\_context.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1425)

<a id="op-389ab041bc877e"></a>
### Flow builtins.bind

`operation_foundation_binding_foundation_flow_utils_safe_exec_flow_builtins_bind`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** func.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1426)

<a id="op-550b464b29b1e2"></a>
### Flow builtins.bind.call

`operation_foundation_binding_foundation_flow_utils_safe_exec_flow_builtins_bind_call`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1427)

<a id="op-7b35dfe8e40c0e"></a>
### Stop

`operation_foundation_binding_foundation_flow_utils_safe_exec_stop`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** what, ctx, args, kwargs.

**Locally raised failures** stop.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1446)

<a id="op-07ff17ffe9a4e7"></a>
### Sandbox run action

`operation_foundation_binding_foundation_flow_utils_safe_exec_sandbox_run_action`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, names, action, args, ctx.

**Explicit result forms** the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1445)

<a id="op-eff4c316ea8042"></a>
### Sandbox call api

`operation_foundation_binding_foundation_flow_utils_safe_exec_sandbox_call_api`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** method, args, ctx.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1444)

<a id="op-9d445a0eca73c8"></a>
### Call read function

`operation_foundation_binding_foundation_flow_utils_safe_exec_call_read_function`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** ctx, function, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1424)

<a id="op-5fca67b6d27c01"></a>
### Get flow safe globals

`operation_foundation_binding_foundation_flow_utils_safe_exec_get_flow_safe_globals`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** tool\_context.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1435)

## Service · Scheduler

<a id="op-45f0a12b86fa08"></a>
### Process cron

`operation_foundation_binding_foundation_automation_engine_scheduler_process_cron`

**Inputs** now = no value.

**Explicit results** no value.

**Local steps**

- If not settings.is\_enabled().
  - Return no value.
- Set now from get\_datetime((now or now\_datetime())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in now → now\_datetime().
- Set queued from 0.
- For each rule in \_due\_scheduled\_rules(now).
  - Set fire\_at from \_latest\_fire(rule.cron\_expression, now).
  - If (fire\_at and fire\_at ≥ get\_datetime(rule.creation)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fire\_at → fire\_at ≥ get\_datetime(rule.creation).
    - Update queued using + \_queue\_rule(rule, fire\_at).
  - Evaluate set\_next\_run(rule.name, rule.cron\_expression, now).
- If queued.
  - Evaluate Platform.db.after\_commit.add(kick\_drainer).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L529)

<a id="op-1dc926720b1e23"></a>
### Due scheduled rules

`operation_foundation_binding_foundation_automation_engine_scheduler_due_scheduled_rules`

**Inputs** now.

**Declared result** list.

**Record and data access** read “Automation Flow” via get\_all.

**Explicit results** Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “trigger\_type” → “Scheduled”), or\_filters = list(list(“next\_run”, “is”, “not set”), list(“next\_run”, “&lt;=”, now)), fields = list(“name”,  ….

**Local steps**

- Return Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “trigger\_type” → “Scheduled”), or\_filters = list(list(“next\_run”, “is”, “not set”), list(“next\_run”, “&lt;=”, now)), fields = list(“name”,  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L521)

<a id="op-698eab260f122e"></a>
### Set next run

`operation_foundation_binding_foundation_automation_engine_scheduler_set_next_run`

**Inputs** automation, expression, after = no value.

**State and service calls** request set\_value on “Automation Flow”.

**Local steps**

- Evaluate Platform.db.set\_value(“Automation Flow”, automation, “next\_run”, next\_fire(expression, (after or now\_datetime())), update\_modified = false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in after → now\_datetime().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L534)

<a id="op-9d320486df172f"></a>
### Next fire

`operation_foundation_binding_foundation_automation_engine_scheduler_next_fire`

**Inputs** expression, after.

**Declared result** (datetime bitwise or no value).

**Explicit results** no value · parse\_cron(expression).get\_next(datetime, start\_time = after).

**Local steps**

- If not expression.
  - Return no value.
- Return parse\_cron(expression).get\_next(datetime, start\_time = after).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L526)

<a id="op-cd644404b10a2a"></a>
### Latest fire

`operation_foundation_binding_foundation_automation_engine_scheduler_latest_fire`

**Inputs** expression, now.

**Declared result** (datetime bitwise or no value).

**Explicit results** no value · parse\_cron(expression).get\_prev(datetime, start\_time = (now + timedelta(seconds = 1))).

**Local steps**

- If not expression.
  - Return no value.
- Return parse\_cron(expression).get\_prev(datetime, start\_time = (now + timedelta(seconds = 1))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L524)

<a id="op-ab43145ac3735c"></a>
### Handled names

`operation_foundation_binding_foundation_automation_engine_scheduler_handled_names`

**Inputs** automation, fire\_at.

**Declared result** set at (str bitwise or no value).

**Record and data access** read QUEUE via get\_all.

**Explicit results** set(expanded active, expanded completed).

**Local steps**

- Set active from Platform.get\_all(QUEUE, filters = mapping(“automation” → automation, “status” → tuple(“in”, tuple(expanded WAITING\_STATES, “Running”))), pluck = “ref\_name”).
- Set completed from \_completed\_names(automation, fire\_at).
- Return set(expanded active, expanded completed).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L523)

<a id="op-dea4fcbc41f9b6"></a>
### Completed names

`operation_foundation_binding_foundation_automation_engine_scheduler_completed_names`

**Inputs** automation, fire\_at.

**Declared result** list at (str bitwise or no value).

**Record and data access** read RUN via get\_all.

**Explicit results** Platform.get\_all(RUN, filters = mapping(“automation” → automation, “creation” → tuple(“&gt;=”, fire\_at)), pluck = “reference\_name”).

**Local steps**

- Return Platform.get\_all(RUN, filters = mapping(“automation” → automation, “creation” → tuple(“&gt;=”, fire\_at)), pluck = “reference\_name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L514)

<a id="op-295b9ca18438b9"></a>
### Queue rule

`operation_foundation_binding_foundation_automation_engine_scheduler_queue_rule`

**Inputs** rule, fire\_at.

**Declared result** int.

**Explicit results** \_queue\_matching\_docs(rule, fire\_at) · 0 · 1.

**Local steps**

- If rule.document\_type.
  - Return \_queue\_matching\_docs(rule, fire\_at).
- If no value belongs to \_handled\_names(rule.name, fire\_at).
  - Return 0.
- Evaluate queue\_trigger(rule.name, no value, no value, payload = \_payload(fire\_at)).
- Return 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L533)

<a id="op-acb463da18edcd"></a>
### Queue matching docs

`operation_foundation_binding_foundation_automation_engine_scheduler_queue_matching_docs`

**Inputs** rule, fire\_at.

**Declared result** int.

**Explicit results** 0 · queued.

**Local steps**

- Set names from \_matching\_names(rule).
- If not names.
  - Return 0.
- Set handled from \_handled\_names(rule.name, fire\_at).
- Set queued from 0.
- For each name in names.
  - If name belongs to handled.
    - Continue with the next iteration or loop test.
  - Evaluate queue\_trigger(rule.name, rule.document\_type, name, payload = \_payload(fire\_at)).
  - Update queued using + 1.
- Return queued.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L532)

<a id="op-3638e8b8d8a881"></a>
### Matching names

`operation_foundation_binding_foundation_automation_engine_scheduler_matching_names`

**Inputs** rule.

**Declared result** list at str.

**Record and data access** read rule.document\_type via get\_all.

**Explicit results** \_condition\_filtered(rule, names).

**Local steps**

- Set filters from Platform.parse\_json(rule.filters) when rule.filters, otherwise no value.
  - Value choice on rule.filters — true gives Platform.parse\_json(rule.filters), false gives no value.
- Set names from Platform.get\_all(rule.document\_type, filters = filters, pluck = “name”).
- Return \_condition\_filtered(rule, names).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L525)

<a id="op-24a9a4dda73b32"></a>
### Condition filtered

`operation_foundation_binding_foundation_automation_engine_scheduler_condition_filtered`

**Inputs** rule, names.

**Declared result** list at str.

**Record and data access** resolve a document from rule.document\_type via get\_doc.

**Explicit results** names · list of name for name drawn from names where matches\_rule(rule, Platform.get\_doc(rule.document\_type, name)) · list of row.name for row drawn from \_condition\_rows(rule, names, fields) where matches\_rule(rule, row).

**Local steps**

- If not rule.condition.
  - Return names.
- Set fields from \_condition\_columns(rule).
- If fields is identical to no value.
  - Return list of name for name drawn from names where matches\_rule(rule, Platform.get\_doc(rule.document\_type, name)).
    - Draw name from names, keep a combination only if (matches\_rule(rule, Platform.get\_doc(rule.document\_type, name))).
- Return list of row.name for row drawn from \_condition\_rows(rule, names, fields) where matches\_rule(rule, row).
  - Draw row from \_condition\_rows(rule, names, fields), keep a combination only if (matches\_rule(rule, row)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L516)

<a id="op-718a729ec838d1"></a>
### Condition rows

`operation_foundation_binding_foundation_automation_engine_scheduler_condition_rows`

**Inputs** rule, names, fields.

**Declared result** list.

**Record and data access** read rule.document\_type via get\_all.

**Explicit results** list() · rows.

**Local steps**

- If not names.
  - Return list().
- Set rows from Platform.get\_all(rule.document\_type, filters = list(list(“name”, “in”, names)), fields = list(“name”, expanded sorted(fields))).
- For each row in rows.
  - Set row.doctype from rule.document\_type.
- Return rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L517)

<a id="op-3d770db22d74d4"></a>
### Condition columns

`operation_foundation_binding_foundation_automation_engine_scheduler_condition_columns`

**Inputs** rule.

**Declared result** (set at str bitwise or no value).

**Explicit results** no value · names when names ≤ valid, otherwise no value.

**Local steps**

- Set names from condition\_fieldnames(rule.condition).
- If names is identical to no value.
  - Return no value.
- Update names using bitwise or \_filter\_fieldnames(Platform.parse\_json(rule.filters) when rule.filters, otherwise no value).
  - Value choice on rule.filters — true gives Platform.parse\_json(rule.filters), false gives no value.
- Set valid from set(Platform.get\_meta(rule.document\_type).get\_valid\_columns()).
- Return names when names ≤ valid, otherwise no value.
  - Value choice on names ≤ valid — true gives names, false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L515)
