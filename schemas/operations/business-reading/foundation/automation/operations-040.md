# Workflow, automation and dispatch · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Runner

<a id="op-ac8ebec9033bcc"></a>
### Begin event wait

`operation_foundation_binding_foundation_automation_engine_runner_begin_event_wait`

**Inputs** step, context, pos.

**Explicit results** tuple(“Success”, \_simulated\_event\_wait(params), \_ms(started)) · tuple(“Waiting”, translated “Waiting for {0}”.format(subscription.event\_name), \_ms(started)).

**Local steps**

- Set started from time.monotonic().
- Set params from \_step\_params(step).
- If Platform.flags.get(“in\_automation\_trial”).
  - Return tuple(“Success”, \_simulated\_event\_wait(params), \_ms(started)).
- Set subscription from schedule\_event\_wait(context, params, step at “step\_key”, (pos + 1)).
- Return tuple(“Waiting”, translated “Waiting for {0}”.format(subscription.event\_name), \_ms(started)).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L463)

<a id="op-758a6a10c83b86"></a>
### Simulated event wait

`operation_foundation_binding_foundation_automation_engine_runner_simulated_event_wait`

**Inputs** params.

**Declared result** str.

**Explicit results** translated “Waited for {0} (simulated)”.format((params.get(“event\_name”) or translated “event”)).

**Local steps**

- Return translated “Waited for {0} (simulated)”.format((params.get(“event\_name”) or translated “event”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“event\_name”) → translated “event”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L499)

<a id="op-372c145ce2f6ad"></a>
### Wait seconds

`operation_foundation_binding_foundation_automation_engine_runner_wait_seconds`

**Inputs** params.

**Declared result** int.

**Explicit results** (cint(params.get(“value”)) × WAIT\_UNIT\_SECONDS.get(unit, 60)).

**Local steps**

- Set unit from (params.get(“unit”) or “Minutes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“unit”) → “Minutes”.
- Return (cint(params.get(“value”)) × WAIT\_UNIT\_SECONDS.get(unit, 60)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L512)

<a id="op-d9d4072398dbd2"></a>
### Schedule wait

`operation_foundation_binding_foundation_automation_engine_runner_schedule_wait`

**Inputs** context, seconds, resume\_from\_idx.

**Record and data access** resolve a document from resume\_row\_values(context, run\_after, resume\_from\_idx) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(resume\_row\_values(context, run\_after, resume\_from\_idx)).

**Local steps**

- Set run\_after from add\_to\_date(now(), seconds = seconds).
- Evaluate Platform.get\_doc(resume\_row\_values(context, run\_after, resume\_from\_idx)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L497)

<a id="op-db3715f5570f91"></a>
### Resume row values

`operation_foundation_binding_foundation_automation_engine_runner_resume_row_values`

**Inputs** context, run\_after, resume\_from\_idx.

**Declared result** dict.

**Explicit results** mapping(“doctype” → QUEUE, “automation” → row.automation, “ref\_doctype” → row.ref\_doctype, “ref\_name” → row.ref\_name, …).

**Local steps**

- Set row from context at “queue\_row”.
- Return mapping(“doctype” → QUEUE, “automation” → row.automation, “ref\_doctype” → row.ref\_doctype, “ref\_name” → row.ref\_name, …).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L488)

<a id="op-b188cbb86eefc1"></a>
### Run one

`operation_foundation_binding_foundation_automation_engine_runner_run_one`

**Inputs** registry, step, doc, context, idx.

**Explicit results** outcome · tuple(“Failed”, outcome at 1, outcome at 2).

**Local steps**

- Set started from time.monotonic().
- Set savepoint from formatted text auto\_step\_{idx}.
- Set handler from registry.get(step.get(“action\_type”)).
- Set params from \_step\_params(step).
- For each last\_attempt in tuple(false, true).
  - Set outcome from \_try\_action(handler, step, doc, context, …).
  - If outcome at 0 differs from “Retry”.
    - Return outcome.
  - If last\_attempt.
    - Return tuple(“Failed”, outcome at 1, outcome at 2).
  - If doc.
    - Evaluate doc.reload().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L490)

<a id="op-186e5d5eb2e843"></a>
### Try action

`operation_foundation_binding_foundation_automation_engine_runner_try_action`

**Inputs** handler, step, doc, context, params, savepoint, idx, started.

**State and service calls** savepoint savepoint · rollback.

**Explicit results** tuple(“Success”, handler.execute(target, params, context), \_ms(started)) · tuple(“Waiting”, (str(error) or translated “Automation paused”), \_ms(started)) · tuple(“Retry”, Platform.get\_traceback(), \_ms(started)) · tuple(“Failed”, \_failure\_detail(error, messages\_before), \_ms(started)).

**Explicit failure paths** ValueError(formatted text Unknown action type: {step.get(“action\_type”)}).

**Local steps**

- Evaluate Platform.db.savepoint(savepoint).
- Set messages\_before from len(Platform.local.message\_log).
- Attempt the following.
  - Set target from \_target\_doc(step, doc, context, permission\_type = “write”).
  - If not handler.
    - Raise ValueError(formatted text Unknown action type: {step.get(“action\_type”)}).
  - Evaluate handler.validate(params, target.doctype when target, otherwise no value).
    - Value choice on target — true gives target.doctype, false gives no value.
  - If not handler.transactional.
    - Evaluate mark\_effects\_delivered(context at “queue\_row”.name).
  - Return tuple(“Success”, handler.execute(target, params, context), \_ms(started)).
- On failure (StopAutomation) bound to error.
  - Evaluate schedule\_wait(context, error.resume\_after, (idx + 1)).
  - Return tuple(“Waiting”, (str(error) or translated “Automation paused”), \_ms(started)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(error) → translated “Automation paused”.
- On failure (Platform.TimestampMismatchError).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Return tuple(“Retry”, Platform.get\_traceback(), \_ms(started)).
- On failure (Exception) bound to error.
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Return tuple(“Failed”, \_failure\_detail(error, messages\_before), \_ms(started)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L510)

<a id="op-18f6aa43cc6430"></a>
### Skip detail

`operation_foundation_binding_foundation_automation_engine_runner_skip_detail`

**Inputs** step, doc, context.

**Declared result** dict.

**Explicit results** mapping(“note” → true, “detail” → translated “Step condition did not match”, “condition” → (condition or step.get(“related\_condition”) or empty text), “condition\_values” → condition\_values(condition, mappi ….

**Local steps**

- Set condition from (step.get(“step\_condition”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“step\_condition”) → empty text.
- Set target from \_target\_doc(step, doc, context, permission\_type = “read”) when condition, otherwise no value.
  - Value choice on condition — true gives \_target\_doc(step, doc, context, permission\_type = “read”), false gives no value.
- Return mapping(“note” → true, “detail” → translated “Step condition did not match”, “condition” → (condition or step.get(“related\_condition”) or empty text), “condition\_values” → condition\_values(condition, mappi ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition → step.get(“related\_condition”) → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L501)

<a id="op-491c14fbdc83b8"></a>
### Failure detail

`operation_foundation_binding_foundation_automation_engine_runner_failure_detail`

**Inputs** error, messages\_before.

**Declared result** dict.

**Explicit results** mapping(“note” → true, “detail” → traceback, “traceback” → traceback, “message” → \_thrown\_message(error, messages\_before), …).

**Local steps**

- Set traceback from Platform.get\_traceback().
- Return mapping(“note” → true, “detail” → traceback, “traceback” → traceback, “message” → \_thrown\_message(error, messages\_before), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L476)

<a id="op-8ddbdc9870ac6b"></a>
### Thrown message

`operation_foundation_binding_foundation_automation_engine_runner_thrown_message`

**Inputs** error, messages\_before.

**Declared result** str.

**Explicit results** whitespace '\\n'.join(messages) when messages, otherwise str(error).

**Local steps**

- Set thrown from Platform.local.message\_log at slice messages\_before to no value.
- Set messages from list of message.get(“message”) for message drawn from thrown where message.get(“message”).
  - Draw message from thrown, keep a combination only if (message.get(“message”)).
- Return whitespace '\\n'.join(messages) when messages, otherwise str(error).
  - Value choice on messages — true gives whitespace '\\n'.join(messages), false gives str(error).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L507)

<a id="op-30d6ef98b600c1"></a>
### Step params

`operation_foundation_binding_foundation_automation_engine_runner_step_params`

**Inputs** step.

**Declared result** dict.

**Explicit results** (Platform.parse\_json(params) when isinstance(params, str), otherwise params or mapping()).

**Local steps**

- Set params from step.get(“params”).
- Return (Platform.parse\_json(params) when isinstance(params, str), otherwise params or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(params) when isinstance(params, str), otherwise params → mapping().
  - Value choice on isinstance(params, str) — true gives Platform.parse\_json(params), false gives params.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L504)

<a id="op-2f6bc2498961d7"></a>
### Step condition matches

`operation_foundation_binding_foundation_automation_engine_runner_step_condition_matches`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** step, doc, context.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L502)

<a id="op-eb3ab3e796c25f"></a>
### Append step

`operation_foundation_binding_foundation_automation_engine_runner_append_step`

**Inputs** steps, step, idx, status, detail, duration.

**Explicit results** entry.

**Local steps**

- Set note from detail when (isinstance(detail, dict) and detail.get(“note”)), otherwise mapping().
  - Value choice on (isinstance(detail, dict) and detail.get(“note”)) — true gives detail, false gives mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(detail, dict) → detail.get(“note”).
- Set tuple(detail, output) from tuple(note at “detail”, no value) when note, otherwise \_action\_result(detail).
  - Value choice on note — true gives tuple(note at “detail”, no value), false gives \_action\_result(detail).
- Set entry from mapping(“step\_idx” → idx, “step\_key” → (step.get(“step\_key”) or formatted text step\_{(idx + 1)}), “action\_type” → (step.get(“action\_type”) or step.get(“step\_type”) or “Action”), “status” → status, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“step\_key”) → formatted text step\_{(idx + 1)}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“action\_type”) → step.get(“step\_type”) → “Action”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in detail → empty text.
- Evaluate steps.append(entry).
- Return entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L462)

<a id="op-778a7f06394c1d"></a>
### Trim

`operation_foundation_binding_foundation_automation_engine_runner_trim`

**Inputs** value.

**Explicit results** value at slice no value to 5000 when value, otherwise no value.

**Local steps**

- Return value at slice no value to 5000 when value, otherwise no value.
  - Value choice on value — true gives value at slice no value to 5000, false gives no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L508)

<a id="op-9d9ea0f3cfbbff"></a>
### Target doc

`operation_foundation_binding_foundation_automation_engine_runner_target_doc`

**Inputs** step, trigger\_doc, context, permission\_type = no value.

**Explicit results** trigger\_doc · load\_record(context at “records”.get(target), permission\_type = permission\_type).

**Local steps**

- Set target from (step.get(“target”) or “trigger”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“target”) → “trigger”.
- If target equals “trigger”.
  - If (trigger\_doc and permission\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in trigger\_doc → permission\_type.
    - Evaluate trigger\_doc.check\_permission(permission\_type).
  - Return trigger\_doc.
- Return load\_record(context at “records”.get(target), permission\_type = permission\_type).

**Values supplied outside this operation** effective access from trigger\_doc.check\_permission(permission\_type).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L506)

<a id="op-1b42e4a47c1d31"></a>
### Update context

`operation_foundation_binding_foundation_automation_engine_runner_update_context`

**Inputs** context, step, entry.

**Local steps**

- Set output from (entry.get(“output”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“output”) → mapping().
- If not \_within\_output\_limit(output).
  - Set entry at “output”, output from mapping(“truncated” → true).
- Set context at “steps” at entry at “step\_key” from output.
- Set alias from step.get(“output\_alias”).
- If (alias and output.get(“destination\_reference”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in alias → output.get(“destination\_reference”).
  - Set context at “records” at alias from output at “destination\_reference”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L511)

<a id="op-38ebda841c4999"></a>
### Within output limit

`operation_foundation_binding_foundation_automation_engine_runner_within_output_limit`

**Inputs** output.

**Declared result** bool.

**Explicit results** len(Platform.as\_json(output).encode()) ≤ settings.get(“step\_output\_limit”).

**Local steps**

- Return len(Platform.as\_json(output).encode()) ≤ settings.get(“step\_output\_limit”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L513)

<a id="op-4416d0f8b7ff21"></a>
### Action result

`operation_foundation_binding_foundation_automation_engine_runner_action_result`

**Inputs** result.

**Explicit results** tuple(result, no value) · tuple(str(detail), result).

**Local steps**

- If not isinstance(result, dict).
  - Return tuple(result, no value).
- Set detail from (result.get(“detail”) or result.get(“destination\_reference”) or translated “Action completed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.get(“detail”) → result.get(“destination\_reference”) → translated “Action completed”.
- Return tuple(str(detail), result).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L460)

<a id="op-34202657ccba77"></a>
### Ms

`operation_foundation_binding_foundation_automation_engine_runner_ms`

**Inputs** started.

**Declared result** int.

**Explicit results** int(((time.monotonic() − started) × 1000)).

**Local steps**

- Return int(((time.monotonic() − started) × 1000)).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L482)

<a id="op-2668e501c7716c"></a>
### Finalize

`operation_foundation_binding_foundation_automation_engine_runner_finalize`

**Inputs** run, rule, row, status, steps, error = no value, context = no value.

**State and service calls** call save on run.

**Explicit results** no value.

**Local steps**

- Set error\_summary from (error or \_error\_summary(status, steps)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in error → \_error\_summary(status, steps).
- Evaluate run.update(\_run\_values(status, steps, error\_summary, context)).
- Set run.flags.ignore\_links from true.
- Evaluate run.save(ignore\_permissions = true).
- Evaluate \_settle\_queue\_row(row, status).
- If Platform.flags.get(“in\_automation\_trial”).
  - Evaluate clear\_effects(row.name).
  - Return no value.
- If status equals “Failed”.
  - Evaluate \_record\_failure(rule).
- Otherwise.
  - If status equals “Success”.
    - Evaluate \_reset\_failures(rule).
- Evaluate \_publish\_update(run, rule, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L478)

<a id="op-5e87e4547fb7f7"></a>
### Publish update

`operation_foundation_binding_foundation_automation_engine_runner_publish_update`

**Inputs** run, rule, status.

**State and service calls** publish realtime with “automation\_run\_update”.

**Local steps**

- Evaluate Platform.publish\_realtime(“automation\_run\_update”, mapping(“automation” → rule.name, “run” → run.name, “status” → status), doctype = run.reference\_doctype, docname = run.reference\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“automation\_run\_update”, mapping(“automation” → rule.name, “run” → run.name, “status” → status), doctype = run.reference\_doctype, docname = run.reference\_name).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L484)

<a id="op-3506de2efa03f4"></a>
### Run values

`operation_foundation_binding_foundation_automation_engine_runner_run_values`

**Inputs** status, steps, error\_summary, context = no value.

**Declared result** dict.

**Explicit results** values.

**Local steps**

- Set values from mapping(“status” → status, “error\_summary” → error\_summary, “steps” → \_step\_rows(steps)).
- If context.
  - Set values at “run\_state” from Platform.as\_json(mapping(“step\_outputs” → context at “steps”, “records” → context at “records”, “branches” → context at “branches”)).
- If status differs from “Waiting”.
  - Set values at “ended\_at” from now().
- Return values.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L495)

<a id="op-d6f33a9a452ea0"></a>
### Step rows

`operation_foundation_binding_foundation_automation_engine_runner_step_rows`

**Inputs** steps.

**Declared result** list at dict.

**Explicit results** list of mapping(expand step, expand mapping of field → Platform.as\_json(step at field) for field drawn from STEP\_JSON\_FIELDS where step.get(field)) for step drawn from steps.

**Local steps**

- Return list of mapping(expand step, expand mapping of field → Platform.as\_json(step at field) for field drawn from STEP\_JSON\_FIELDS where step.get(field)) for step drawn from steps.
  - Draw step from steps.
  - Draw field from STEP\_JSON\_FIELDS, keep a combination only if (step.get(field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L505)

<a id="op-4bb11465ebd9ce"></a>
### Settle queue row

`operation_foundation_binding_foundation_automation_engine_runner_settle_queue_row`

**Inputs** row, status.

**State and service calls** request delete on QUEUE · request set\_value on QUEUE.

**Local steps**

- If status belongs to tuple(“Success”, “Partially Failed”, “Waiting”).
  - Evaluate Platform.db.delete(QUEUE, mapping(“name” → row.name)).
- Otherwise.
  - Evaluate Platform.db.set\_value(QUEUE, row.name, “status”, status, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L498)
