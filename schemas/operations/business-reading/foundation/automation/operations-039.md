# Workflow, automation and dispatch · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Retriever

<a id="op-c8fd38d5df14a3"></a>
### Source titles

`operation_foundation_binding_foundation_flow_knowledge_retriever_source_titles`

**Inputs** names.

**Declared result** dict at tuple(str, str).

**Record and data access** read SOURCE\_DOCTYPE via get\_all.

**Explicit results** mapping of row at “name” → row at “title” for row drawn from rows.

**Local steps**

- Set rows from Platform.get\_all(SOURCE\_DOCTYPE, filters = mapping(“name” → list(“in”, list(names))), fields = list(“name”, “title”)).
- Return mapping of row at “name” → row at “title” for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L238) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1216)

## Service · Runner

<a id="op-3e7e1fa775d96a"></a>
### Execute automation

`operation_foundation_binding_foundation_automation_engine_runner_execute_automation`

**Inputs** queue\_name.

**Record and data access** resolve a document from QUEUE via get\_doc · resolve a document from “Automation Flow” via get\_cached\_doc.

**Explicit results** \_finalize(run, rule, row, “Skipped”, error = “Target document not found”, …) · \_finalize(run, rule, row, “Skipped”, error = “Rule no longer matches”, …).

**Local steps**

- Set row from Platform.get\_doc(QUEUE, queue\_name).
- Set event from get\_wait\_outcome(row) when row.resume\_run, otherwise no value.
  - Value choice on row.resume\_run — true gives get\_wait\_outcome(row), false gives no value.
- Set rule from Platform.get\_cached\_doc(“Automation Flow”, row.automation).
- Set doc from \_load\_target(row).
- Set tuple(run, steps, snapshot) from \_run\_state(rule, row, doc).
- If (doc is identical to no value and row.ref\_doctype and row.ref\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc is identical to no value → row.ref\_doctype → row.ref\_name.
  - Return \_finalize(run, rule, row, “Skipped”, error = “Target document not found”, …).
- If (rule.revalidate\_on\_run and doc and not matches\_rule(rule, doc)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.revalidate\_on\_run → doc → not matches\_rule(rule, doc).
  - Return \_finalize(run, rule, row, “Skipped”, error = “Rule no longer matches”, …).
- Set tuple(status, context) from \_execute\_plan(rule, row, run, doc, …).
- Evaluate \_finalize(run, rule, row, status, context = context, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Automation Flow”, row.automation).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L472)

<a id="op-17f0d5d6431aa5"></a>
### Execute plan

`operation_foundation_binding_foundation_automation_engine_runner_execute_plan`

**Inputs** rule, row, run, doc, steps, snapshot, event.

**Explicit results** tuple(status, context) · tuple(“Failed”, context).

**Local steps**

- Set previous\_depth from Platform.flags.get(“automation\_depth”, 0).
- Set previous\_run from Platform.flags.get(“in\_automation\_run”).
- Set Platform.flags.automation\_depth from cint(row.depth).
- Set Platform.flags.in\_automation\_run from true.
- Set context from no value.
- Attempt the following.
  - Within \_execution\_identity(rule, row, doc).
    - Evaluate \_ensure\_trigger\_access(doc).
    - Set context from \_context(row, run, rule, doc, …).
    - Set status from \_run\_plan(steps, rule, doc, context, …).
  - Return tuple(status, context).
- On failure (Exception).
  - Evaluate \_append\_step(steps, mapping(“step\_key” → “setup”), len(steps), “Failed”, …).
  - Return tuple(“Failed”, context).
- On exit, including pending return or failure.
  - Set Platform.flags.automation\_depth from previous\_depth.
  - Set Platform.flags.in\_automation\_run from previous\_run.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L473)

<a id="op-25a8aec95cd8dd"></a>
### Run state

`operation_foundation_binding_foundation_automation_engine_runner_run_state`

**Inputs** rule, row, doc.

**Explicit results** \_resumed\_run\_state(row) · tuple(\_create\_run(rule, row, snapshot, doc), list(), snapshot).

**Local steps**

- If row.resume\_run.
  - Return \_resumed\_run\_state(row).
- Set snapshot from list of \_action\_snapshot(action) for action drawn from rule.actions.
  - Draw action from rule.actions.
- Return tuple(\_create\_run(rule, row, snapshot, doc), list(), snapshot).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L493)

<a id="op-0ddf7957866d53"></a>
### Resumed run state

`operation_foundation_binding_foundation_automation_engine_runner_resumed_run_state`

**Inputs** row.

**Record and data access** resolve a document from RUN via get\_doc.

**Explicit results** tuple(run, run\_steps(run), (Platform.parse\_json(run.actions\_snapshot) or list())).

**Local steps**

- Set run from Platform.get\_doc(RUN, row.resume\_run).
- Return tuple(run, run\_steps(run), (Platform.parse\_json(run.actions\_snapshot) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(run.actions\_snapshot) → list().

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L489)

<a id="op-631d77bc9c6727"></a>
### Run steps

`operation_foundation_binding_foundation_automation_engine_runner_run_steps`

**Inputs** run.

**Declared result** list at dict.

**Explicit results** steps.

**Local steps**

- Set steps from list().
- For each row in run.steps.
  - Set step from mapping of field → row.get(field) for field drawn from STEP\_FIELDS.
    - Draw field from STEP\_FIELDS.
  - For each field in STEP\_JSON\_FIELDS.
    - Set step at field from Platform.parse\_json(step at field) when step at field, otherwise no value.
      - Value choice on step at field — true gives Platform.parse\_json(step at field), false gives no value.
  - Evaluate steps.append(step).
- Return steps.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L494)

<a id="op-2fc74c8d5e499b"></a>
### Load target

`operation_foundation_binding_foundation_automation_engine_runner_load_target`

**Inputs** row.

**Record and data access** resolve a document from row.ref\_doctype via get\_doc.

**Explicit results** no value · Platform.get\_doc(row.ref\_doctype, row.ref\_name).

**Local steps**

- If not (row.ref\_doctype and row.ref\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.ref\_doctype → row.ref\_name.
  - Return no value.
- Attempt the following.
  - Return Platform.get\_doc(row.ref\_doctype, row.ref\_name).
- On failure (Platform.DoesNotExistError).
  - Return no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L481)

<a id="op-2f1febf4b4cb22"></a>
### Create run

`operation_foundation_binding_foundation_automation_engine_runner_create_run`

**Inputs** rule, row, snapshot, doc.

**State and service calls** request new\_doc for RUN · call insert on run.

**Explicit results** run.insert(ignore\_permissions = true).

**Local steps**

- Set run from Platform.new\_doc(RUN).
- Evaluate run.update(\_run\_start\_values(rule, row, snapshot, doc)).
- Set run.flags.ignore\_links from true.
- Return run.insert(ignore\_permissions = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L468)

<a id="op-12ce84867eafff"></a>
### Run start values

`operation_foundation_binding_foundation_automation_engine_runner_run_start_values`

**Inputs** rule, row, snapshot, doc.

**Declared result** dict.

**Explicit results** mapping(“automation” → rule.name, “automation\_title” → rule.title, “status” → “Running”, “reference\_doctype” → row.ref\_doctype, …).

**Local steps**

- Return mapping(“automation” → rule.name, “automation\_title” → rule.title, “status” → “Running”, “reference\_doctype” → row.ref\_doctype, …).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L492)

<a id="op-756683203409ea"></a>
### Action snapshot

`operation_foundation_binding_foundation_automation_engine_runner_action_snapshot`

**Inputs** action.

**Declared result** dict.

**Explicit results** mapping(“idx” → cint(action.idx), “step\_type” → (action.step\_type or “Action”), “action\_type” → action.action\_type, “params” → action.params, …).

**Local steps**

- Return mapping(“idx” → cint(action.idx), “step\_type” → (action.step\_type or “Action”), “action\_type” → action.action\_type, “params” → action.params, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in action.step\_type → “Action”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in action.step\_key → formatted text step\_{action.idx}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in action.target → “trigger”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in action.branch → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L461)

<a id="op-ca15f0d214614a"></a>
### Context

`operation_foundation_binding_foundation_automation_engine_runner_context`

**Inputs** row, run, rule, doc, event = no value.

**Declared result** dict.

**Explicit results** mapping(“payload” → Platform.parse\_json(row.event\_payload) when row.event\_payload, otherwise mapping(), “event” → (event or mapping()), “queue\_row” → row, “run” → run, …).

**Local steps**

- Set state from Platform.parse\_json(run.run\_state) when run.run\_state, otherwise mapping().
  - Value choice on run.run\_state — true gives Platform.parse\_json(run.run\_state), false gives mapping().
- Return mapping(“payload” → Platform.parse\_json(row.event\_payload) when row.event\_payload, otherwise mapping(), “event” → (event or mapping()), “queue\_row” → row, “run” → run, …).
  - Value choice on row.event\_payload — true gives Platform.parse\_json(row.event\_payload), false gives mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in event → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in state.get(“step\_outputs”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in state.get(“records”) → resolve\_relationships(doc, Platform.parse\_json(run.relationships)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in state.get(“branches”) → mapping().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L467)

<a id="op-1d514bb1d5c8eb"></a>
### Execution identity

`operation_foundation_binding_foundation_automation_engine_runner_execution_identity`

**Inputs** rule, row, doc.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous from Platform.\_dict(Platform.session).
- Evaluate Platform.set\_user(\_execution\_user(rule, row, doc)).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(previous.user).
  - Evaluate Platform.local.session.update(previous).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L474)

<a id="op-e364847acf68c1"></a>
### Execution user

`operation_foundation_binding_foundation_automation_engine_runner_execution_user`

**Inputs** rule, row, doc.

**Explicit results** (row.triggered\_by or rule.owner) · doc.owner · (rule.automation\_user or “Administrator”).

**Local steps**

- If rule.run\_as equals “Triggering User”.
  - Return (row.triggered\_by or rule.owner).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.triggered\_by → rule.owner.
- If (rule.run\_as equals “Document Owner” and doc).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.run\_as equals “Document Owner” → doc.
  - Return doc.owner.
- Return (rule.automation\_user or “Administrator”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.automation\_user → “Administrator”.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L475)

<a id="op-7d8f3ab8014c4a"></a>
### Ensure trigger access

`operation_foundation_binding_foundation_automation_engine_runner_ensure_trigger_access`

**Inputs** doc.

**Local steps**

- If doc.
  - Evaluate doc.check\_permission(“read”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L469)

<a id="op-feba81f11189cd"></a>
### Run plan

`operation_foundation_binding_foundation_automation_engine_runner_run_plan`

**Inputs** steps, rule, doc, context, snapshot, start\_idx = 0.

**Declared result** str.

**Explicit results** “Waiting” · “Failed” · overall.

**Local steps**

- Set registry from get\_action\_registry().
- Set taken from context at “branches”.
- Set overall from “Success”.
- For each tuple(pos, step) in enumerate(snapshot).
  - Set tuple(status, detail, duration) from \_safe\_step\_outcome(registry, step, doc, context, …).
  - If status is identical to no value.
    - Continue with the next iteration or loop test.
  - Set entry from \_append\_step(steps, step, pos, status, …).
  - Evaluate \_update\_context(context, step, entry).
  - If status equals “Waiting”.
    - Return “Waiting”.
  - If status equals “Failed”.
    - Set overall from “Partially Failed”.
    - If rule.stop\_on\_error.
      - Return “Failed”.
- Return overall.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L491)

<a id="op-22e5cf1d32335e"></a>
### Safe step outcome

`operation_foundation_binding_foundation_automation_engine_runner_safe_step_outcome`

**Inputs** registry, step, doc, context, pos, start\_idx, taken.

**Explicit results** \_step\_outcome(registry, step, doc, context, …) · tuple(“Failed”, Platform.get\_traceback(), 0).

**Local steps**

- Attempt the following.
  - Return \_step\_outcome(registry, step, doc, context, …).
- On failure (Exception).
  - Return tuple(“Failed”, Platform.get\_traceback(), 0).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L496)

<a id="op-143e57a6ddbf8a"></a>
### Step outcome

`operation_foundation_binding_foundation_automation_engine_runner_step_outcome`

**Inputs** registry, step, doc, context, pos, start\_idx, taken.

**Explicit results** tuple(no value, no value, no value) · \_resolve\_if(step, doc, context, pos, …) · tuple(“Skipped”, \_skip\_detail(step, doc, context), 0) · \_begin\_wait(step, context, pos) · \_begin\_event\_wait(step, context, pos) · 1 additional forms in the steps below.

**Local steps**

- If not \_branch\_active(step, taken).
  - Return tuple(no value, no value, no value).
- Set step\_type from (step.get(“step\_type”) or “Action”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“step\_type”) → “Action”.
- If step\_type equals “If”.
  - Return \_resolve\_if(step, doc, context, pos, …).
- If pos &lt; start\_idx.
  - Return tuple(no value, no value, no value).
- If not \_step\_condition\_matches(step, doc, context).
  - Return tuple(“Skipped”, \_skip\_detail(step, doc, context), 0).
- If step\_type equals “Wait”.
  - Return \_begin\_wait(step, context, pos).
- If step\_type equals “WaitForEvent”.
  - Return \_begin\_event\_wait(step, context, pos).
- Return \_run\_one(registry, step, doc, context, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L503)

<a id="op-05f8b05ec98a26"></a>
### Branch active

`operation_foundation_binding_foundation_automation_engine_runner_branch_active`

**Inputs** step, taken.

**Declared result** bool.

**Explicit results** true · false · (step.get(“branch”) or “If”) equals arm.

**Local steps**

- Set parent from cint(step.get(“parent\_step”)).
- If not parent.
  - Return true.
- Set arm from taken.get(\_branch\_key(parent)).
- If arm is identical to no value.
  - Return false.
- Return (step.get(“branch”) or “If”) equals arm.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“branch”) → “If”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L465)

<a id="op-4a00f256f33bad"></a>
### Branch key

`operation_foundation_binding_foundation_automation_engine_runner_branch_key`

**Inputs** idx.

**Declared result** str.

**Explicit results** str(cint(idx)).

**Local steps**

- Return str(cint(idx)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L466)

<a id="op-cea0d10b9353ac"></a>
### Resolve if

`operation_foundation_binding_foundation_automation_engine_runner_resolve_if`

**Inputs** step, doc, context, pos, start\_idx, taken.

**Explicit results** tuple(no value, no value, no value) · tuple(“Success”, translated “Forced the {0} branch”.format(arm), 0) · tuple(“Success”, translated “Condition took the {0} branch”.format(arm), 0).

**Local steps**

- Set key from \_branch\_key(step.get(“idx”)).
- Set forced from \_forced\_arm(key).
- If pos &lt; start\_idx.
  - If key belongs to taken.
    - Return tuple(no value, no value, no value).
  - Set taken at key from (forced or \_evaluated\_arm(step, doc, context)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in forced → \_evaluated\_arm(step, doc, context).
  - Return tuple(no value, no value, no value).
- Set taken at key, arm from (forced or \_evaluated\_arm(step, doc, context)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in forced → \_evaluated\_arm(step, doc, context).
- If forced.
  - Return tuple(“Success”, translated “Forced the {0} branch”.format(arm), 0).
- Return tuple(“Success”, translated “Condition took the {0} branch”.format(arm), 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L487)

<a id="op-bf8e36e50192bb"></a>
### Evaluated arm

`operation_foundation_binding_foundation_automation_engine_runner_evaluated_arm`

**Inputs** step, doc, context.

**Declared result** str.

**Explicit results** “If” when \_step\_condition\_matches(step, doc, context), otherwise “Else”.

**Local steps**

- Return “If” when \_step\_condition\_matches(step, doc, context), otherwise “Else”.
  - Value choice on \_step\_condition\_matches(step, doc, context) — true gives “If”, false gives “Else”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L471)

<a id="op-bd21a9ce741c36"></a>
### Forced arm

`operation_foundation_binding_foundation_automation_engine_runner_forced_arm`

**Inputs** key.

**Declared result** (str bitwise or no value).

**Explicit results** no value · arm when arm belongs to tuple(“If”, “Else”), otherwise no value.

**Local steps**

- If not Platform.flags.get(“in\_automation\_trial”).
  - Return no value.
- Set arm from (Platform.flags.get(“automation\_branch\_overrides”) or mapping()).get(key).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.get(“automation\_branch\_overrides”) → mapping().
- Return arm when arm belongs to tuple(“If”, “Else”), otherwise no value.
  - Value choice on arm belongs to tuple(“If”, “Else”) — true gives arm, false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L480)

<a id="op-7be25b2f0fc7da"></a>
### Begin wait

`operation_foundation_binding_foundation_automation_engine_runner_begin_wait`

**Inputs** step, context, pos.

**Explicit results** tuple(“Success”, \_simulated\_wait(params), \_ms(started)) · tuple(“Waiting”, translated “Waiting {0} seconds”.format(seconds), \_ms(started)).

**Local steps**

- Set started from time.monotonic().
- Set params from \_step\_params(step).
- If Platform.flags.get(“in\_automation\_trial”).
  - Return tuple(“Success”, \_simulated\_wait(params), \_ms(started)).
- Set seconds from \_wait\_seconds(params).
- Evaluate schedule\_wait(context, seconds, (pos + 1)).
- Return tuple(“Waiting”, translated “Waiting {0} seconds”.format(seconds), \_ms(started)).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L464)

<a id="op-caa95b682fef86"></a>
### Simulated wait

`operation_foundation_binding_foundation_automation_engine_runner_simulated_wait`

**Inputs** params.

**Declared result** str.

**Explicit results** translated “Waited {0} {1} (simulated)”.format(cint(params.get(“value”)), (params.get(“unit”) or “Minutes”)).

**Local steps**

- Return translated “Waited {0} {1} (simulated)”.format(cint(params.get(“value”)), (params.get(“unit”) or “Minutes”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“unit”) → “Minutes”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L500)
