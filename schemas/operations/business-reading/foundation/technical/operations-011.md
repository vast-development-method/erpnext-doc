# Site operations and diagnostics · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Patch handler

<a id="op-4031bce8881be9"></a>
### Should never skip

`operation_foundation_binding_foundation_modules_patch_handler_should_never_skip`

**Inputs** patchmodule, never\_skip.

**Declared result** bool.

**Explicit results** true · false · patchmodule.split(maxsplit = 1) at 0 belongs to never\_skip.

**Local steps**

- Set patchmodule from patchmodule.replace(“finally:”, empty text).
- If patchmodule belongs to never\_skip.
  - Return true.
- If patchmodule.startswith(“execute:”).
  - Return false.
- Return patchmodule.split(maxsplit = 1) at 0 belongs to never\_skip.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1643)

<a id="op-1716c9c17b0082"></a>
### Update patch log

`operation_foundation_modules_patch_handler_business_behavior_update_patch_log`

**Inputs** patchmodule, skipped = false.

**Record and data access** resolve a document from mapping(“doctype” → “Patch Log”, “patch” → patchmodule) via get\_doc.

**State and service calls** call insert on patch.

**Local steps**

- Set patch from Platform.get\_doc(mapping(“doctype” → “Patch Log”, “patch” → patchmodule)).
- If skipped.
  - Set traceback from Platform.get\_traceback(with\_context = true).
  - Set patch.skipped from 1.
  - Set patch.traceback from traceback.
  - Evaluate print(traceback, end = whitespace '\\n\\n').
- Evaluate patch.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L4567) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1404)

<a id="op-b7d94184e33a28"></a>
### Executed

`operation_foundation_modules_patch_handler_business_behavior_executed`

**Inputs** patchmodule.

**Record and data access** read “Patch Log” via get\_value.

**Explicit results** Platform.db.get\_value(“Patch Log”, mapping(“patch” → patchmodule, “skipped” → 0)).

**Local steps**

- If patchmodule.startswith(“finally:”).
  - Set patchmodule from patchmodule.replace(“finally:”, empty text).
- Return Platform.db.get\_value(“Patch Log”, mapping(“patch” → patchmodule, “skipped” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L4811) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1395)

<a id="op-7e3ef2eb3a484b"></a>
### Patch mode

`operation_foundation_modules_patch_handler_business_behavior_patch_mode`

**Inputs** enable.

**State and service calls** commit.

**Local steps**

- Set Platform.local.flags.in\_patch from enable.
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L4980) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1399)

## Service · Recorder

<a id="op-da67ad6815cf87"></a>
### Recorder Config.post init

`operation_foundation_recorder_business_behavior_recorder_configuration_post_initialize`

**Inputs** self.

**Explicit failure paths** validation helper — “You must record one of jobs or requests”.

**Local steps**

- If not (self.record\_jobs or self.record\_requests).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.record\_jobs → self.record\_requests.
  - Call the validation error handler Platform.throw(“You must record one of jobs or requests”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L4620) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L370)

<a id="op-b80284de37d466"></a>
### Recorder Config.store

`operation_foundation_recorder_business_behavior_recorder_configuration_store`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.set\_value(RECORDER\_CONFIG\_FLAG, self, expires\_in\_sec = RECORDER\_AUTO\_DISABLE).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L4708) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L372)

<a id="op-c17179548189f1"></a>
### Recorder Config.retrieve

`operation_foundation_recorder_business_behavior_recorder_configuration_retrieve`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** (Platform.cache.get\_value(RECORDER\_CONFIG\_FLAG) or cls()).

**Local steps**

- Return (Platform.cache.get\_value(RECORDER\_CONFIG\_FLAG) or cls()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(RECORDER\_CONFIG\_FLAG) → cls().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L4780) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L371)

<a id="op-8c5feec8a2f54f"></a>
### Recorder Config.delete

`operation_foundation_recorder_business_behavior_recorder_configuration_delete`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Evaluate Platform.cache.delete\_value(RECORDER\_CONFIG\_FLAG).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L4860) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L369)

<a id="op-bd87371daaf1a7"></a>
### Record sql

`operation_foundation_recorder_business_behavior_record_database_query`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** result.

**Local steps**

- Set start\_time from time.monotonic().
- Set result from Platform.db.\_sql(expanded args, expanded names kwargs).
- Set end\_time from time.monotonic().
- Set query from getattr(Platform.db, “last\_query”, no value).
- If (not query or isinstance(result, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not query → isinstance(result, str).
  - Return result.
- Set stack from list().
- If Platform.local.\_recorder.config.capture\_stack.
  - Set stack from list(get\_current\_stack\_frames()).
- Set data from mapping(“query” → str(query), “stack” → stack, “explain\_result” → list(), “time” → start\_time, …).
- Evaluate Platform.local.\_recorder.register(data).
- Return result.

**Values supplied outside this operation** clock or generated value from time.monotonic() · selected callable from getattr(Platform.db, “last\_query”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L4915) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L364)

<a id="op-99b53ae58c461e"></a>
### Get current stack frames

`operation_foundation_recorder_business_behavior_get_current_stack_frames`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies SERVER\_SCRIPT\_FILE\_PREFIX.
- Attempt the following.
  - Set current from inspect.currentframe().
  - Set frames from inspect.getouterframes(current, context = 10).
  - For each tuple(frame, filename, lineno, function, …) in list(reversed(frames)) at slice no value to negative 2.
    - If (“/apps/” belongs to filename or SERVER\_SCRIPT\_FILE\_PREFIX belongs to filename).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “/apps/” belongs to filename → SERVER\_SCRIPT\_FILE\_PREFIX belongs to filename.
      - yield mapping(“filename” → TRACEBACK\_PATH\_PATTERN.sub(empty text, filename), “lineno” → lineno, “function” → function).
- On failure (Exception).
  - Take no action here.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L5388) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L356)

<a id="op-9ecada157a7d75"></a>
### Doc event contributors

`operation_foundation_recorder_business_behavior_record_event_contributors`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, method, doc.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 4 statement loops and 3 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0324.json#L5709) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L365)

<a id="op-ba9119c3b4754d"></a>
### Install run method tracer

`operation_foundation_recorder_business_behavior_install_run_method_tracer`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Use module bindings \_run\_method\_traced.
- If \_run\_method\_traced.
  - Return no value.
- Bind dependencies Document.
- Set original\_run\_method from Document.run\_method.
- Bind local operation run\_method for subsequent calls.
- Set Document.run\_method from run\_method.
- Set \_run\_method\_traced from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L358)

<a id="op-26a764e0e3ac82"></a>
### Install run method tracer.run method

`operation_foundation_recorder_business_behavior_install_run_method_tracer_run_method`

**Inputs** doc, method, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(original\_run\_method).

**Explicit results** original\_run\_method(doc, method, expanded args, expanded names kwargs).

**Local steps**

- Set recorder from getattr(Platform.local, “\_recorder”, no value).
- If (recorder is identical to no value or not getattr(recorder, “\_recording”, false) or not recorder.config.capture\_doc\_events or method.startswith(“\_\_”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in recorder is identical to no value → not getattr(recorder, “\_recording”, false) → not recorder.config.capture\_doc\_events → method.startswith(“\_\_”).
  - Return original\_run\_method(doc, method, expanded args, expanded names kwargs).
- Set seq from recorder.\_seq.
- Set depth from recorder.\_depth.
- Update recorder.\_seq using + 1.
- Update recorder.\_depth using + 1.
- Set queries\_before from len(recorder.calls).
- Set start\_time from time.monotonic().
- Attempt the following.
  - Return original\_run\_method(doc, method, expanded args, expanded names kwargs).
- On exit, including pending return or failure.
  - Update recorder.\_depth using − 1.
  - Set duration from float(formatted text {((time.monotonic() − start\_time) × 1000)}).
  - Set queries from (len(recorder.calls) − queries\_before).
  - Set tuple(apps, handlers) from \_doc\_event\_contributors(doc.doctype, method, doc = doc).
  - Evaluate recorder.register\_event(mapping(“seq” → seq, “depth” → depth, “method” → method, “ref\_doctype” → doc.doctype, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.name → empty text.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_recorder”, no value), getattr(recorder, “\_recording”, false) · clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L7) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L359)

<a id="op-7413a5977b7350"></a>
### Post process

`operation_foundation_recorder_business_behavior_post_process`

**Inputs** no declared parameters.

**State and service calls** rollback · execute a supplied database query.

**Local steps**

- Evaluate Platform.db.rollback().
- Evaluate Platform.db.begin(read\_only = true).
- Set config from RecorderConfig.retrieve().
- Set result from list(Platform.cache.hgetall(RECORDER\_REQUEST\_HASH).values()).
- For each request in result.
  - For each call in request at “calls”.
    - Set formatted\_query from sqlparse.format(call at “query”.strip(), keyword\_case = “upper”, reindent = true, strip\_comments = true).
    - Set call at “query” from formatted\_query.
    - If (config.explain and is\_query\_type(formatted\_query, tuple(“select”, “update”, “delete”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in config.explain → is\_query\_type(formatted\_query, tuple(“select”, “update”, “delete”)).
      - Attempt the following.
        - Set call at “explain\_result” from Platform.db.sql(formatted text EXPLAIN {formatted\_query}, as\_dict = true).
      - On failure (Exception).
        - Take no action here.
  - Evaluate mark\_duplicates(request).
  - Evaluate Platform.cache.hset(RECORDER\_REQUEST\_HASH, request at “uuid”, request).
- Evaluate config.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L3436) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L362)

<a id="op-d2b31b547443e0"></a>
### Mark duplicates

`operation_foundation_recorder_business_behavior_mark_duplicates`

**Inputs** request.

**Local steps**

- Set exact\_duplicates from Counter(list of call at “query” for call drawn from request at “calls”).
  - Draw call from request at “calls”.
- For each sql\_call in request at “calls”.
  - Set sql\_call at “normalized\_query” from normalize\_query(sql\_call at “query”).
- Set normalized\_duplicates from Counter(list of call at “normalized\_query” for call drawn from request at “calls”).
  - Draw call from request at “calls”.
- For each tuple(index, call) in enumerate(request at “calls”).
  - Set call at “index” from index.
  - Set call at “exact\_copies” from exact\_duplicates at call at “query”.
  - Set call at “normalized\_copies” from normalized\_duplicates at call at “normalized\_query”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L3983) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L360)

<a id="op-61e3282707b0e1"></a>
### Normalize query

`operation_foundation_recorder_business_behavior_normalize_query`

**Inputs** query.

**Declared result** str.

**Explicit results** q · query.

**Local steps**

- Attempt the following.
  - Set q from sqlparse.parse(query) at 0.
  - For each token in q.flatten().
    - If “Token.Literal” belongs to str(token.ttype).
      - Set token.value from “?”.
  - Set q from re.sub(“( IN )\\(\\?&#91;\\s\\n\\?\\,&#93;\*\\)”, “\\1(?)”, str(q), flags = re.IGNORECASE).
  - Return q.
- On failure (Exception) bound to e.
  - Evaluate print(“Failed to normalize query ”, e).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L4367) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L361)

<a id="op-c698e3d16f1eaa"></a>
### Record

`operation_foundation_recorder_business_behavior_record`

**Inputs** force = false.

**Explicit results** Platform.local.\_recorder.

**Local steps**

- Set flag\_value from Platform.client\_cache.get\_value(RECORDER\_INTERCEPT\_FLAG).
- If (flag\_value or force).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flag\_value → force.
  - Set Platform.local.\_recorder from Recorder(force = force).
  - Return Platform.local.\_recorder.
- Otherwise.
  - If flag\_value is identical to no value.
    - Evaluate Platform.client\_cache.set\_value(RECORDER\_INTERCEPT\_FLAG, false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L4641) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L363)

<a id="op-25e649a338165a"></a>
### Dump

`operation_foundation_recorder_business_behavior_dump`

**Inputs** no declared parameters.

**Local steps**

- If hasattr(Platform.local, “\_recorder”).
  - Evaluate Platform.local.\_recorder.dump().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L4835) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L353)

<a id="op-a8d6d2b268058d"></a>
### Recorder.initialize

`operation_foundation_recorder_business_behavior_recorder_initialize`

**Inputs** self, force = false.

**Explicit results** no value.

**Local steps**

- Set self.config from RecorderConfig.retrieve().
- Set self.calls from list().
- Set self.profiler from no value.
- Set self.\_recording from true.
- Set self.force from force.
- Set self.cmd from no value.
- Set self.method from no value.
- Set self.headers from no value.
- Set self.form\_dict from no value.
- Set self.patched\_databases from list().
- Set self.events from list().
- Set self.\_depth from 0.
- Set self.\_seq from 0.
- If (self.config.record\_requests and Platform.request and self.config.request\_filter belongs to Platform.request.path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.config.record\_requests → Platform.request → self.config.request\_filter belongs to Platform.request.path.
  - Set self.path from Platform.request.path.
  - Set self.cmd from (Platform.local.form\_dict.cmd or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.form\_dict.cmd → empty text.
  - Set self.method from Platform.request.method.
  - Set self.headers from dict(Platform.local.request.headers).
  - Set self.form\_dict from Platform.local.form\_dict.
  - Set self.event\_type from “HTTP Request”.
- Otherwise.
  - If (self.config.record\_jobs and Platform.job and self.config.jobs\_filter belongs to Platform.job.method).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.config.record\_jobs → Platform.job → self.config.jobs\_filter belongs to Platform.job.method.
    - Set self.event\_type from “Background Job”.
    - Set self.path from Platform.job.method.
    - Set self.cmd from no value.
    - Set self.method from no value.
    - Set self.headers from no value.
    - Set self.form\_dict from no value.
  - Otherwise.
    - If not self.force.
      - Set self.\_recording from false.
      - Return no value.
    - Otherwise.
      - Set self.event\_type from “Function Call”.
- Set self.uuid from Platform.generate\_hash(length = 10).
- Set self.time from now\_datetime().
- Evaluate self.\_patch\_sql(Platform.db).
- If self.config.capture\_doc\_events.
  - Evaluate \_install\_run\_method\_tracer().
- If self.config.profile.
  - Bind dependencies cProfile.
  - Set self.profiler from cProfile.Profile().
  - Evaluate self.profiler.enable().

If control reaches the end, it returns no value.

**Methods declared on this owner** [patch sql](operations-012.md#op-034cd6c2df3c0b).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10), now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L9) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L374)

<a id="op-98e9b850d447ef"></a>
### Recorder.register

`operation_foundation_recorder_business_behavior_recorder_register`

**Inputs** self, data.

**Local steps**

- Evaluate self.calls.append(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L5951) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L377)

<a id="op-f9500d740c1db7"></a>
### Recorder.register event

`operation_foundation_recorder_business_behavior_recorder_register_event`

**Inputs** self, data.

**Local steps**

- Evaluate self.events.append(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L6016) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L378)

<a id="op-fd304d4336e621"></a>
### Recorder.cleanup

`operation_foundation_recorder_business_behavior_recorder_cleanup`

**Inputs** self.

**Local steps**

- If self.profiler.
  - Evaluate self.profiler.disable().
- Evaluate self.\_unpatch\_sql().

If control reaches the end, it returns no value.

**Methods declared on this owner** [unpatch sql](operations-012.md#op-d4acf84e1ae9b9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L6081) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L368)

<a id="op-bde2c7a047da68"></a>
### Recorder.process profiler

`operation_foundation_recorder_business_behavior_recorder_process_profiler`

**Inputs** self.

**Explicit results** profile.

**Local steps**

- If (self.config.profile or self.profiler).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.config.profile → self.profiler.
  - Bind dependencies pstats.
  - Evaluate self.profiler.disable().
  - Set profiler\_output from io.StringIO().
  - Evaluate pstats.Stats(self.profiler, stream = profiler\_output).sort\_stats(“cumulative”).print\_stats(200).
  - Set profile from profiler\_output.getvalue().
  - Evaluate profiler\_output.close().
  - Return profile.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L6169) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L376)

<a id="op-444b6e5eaef877"></a>
### Recorder.dump

`operation_foundation_recorder_business_behavior_recorder_dump`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.\_recording.
  - Return no value.
- Set profiler\_output from self.process\_profiler().
- Set request\_data from mapping(“uuid” → self.uuid, “path” → self.path, “cmd” → self.cmd, “time” → self.time, …).
  - Draw call from self.calls.
  - Draw event from self.events.
  - Draw app from event at “apps”.
- Evaluate Platform.cache.hset(RECORDER\_REQUEST\_SPARSE\_HASH, self.uuid, request\_data).
- Set request\_data at “calls” from self.calls.
- Set request\_data at “events” from sorted(self.events, key = deferred anonymous expression).
- Set request\_data at “headers” from self.headers.
- Set request\_data at “form\_dict” from self.form\_dict.
- Set request\_data at “profile” from profiler\_output.
- Evaluate Platform.cache.hset(RECORDER\_REQUEST\_HASH, self.uuid, request\_data).
- Evaluate self.\_unpatch\_sql().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process profiler](operations-011.md#op-bde2c7a047da68), [unpatch sql](operations-012.md#op-d4acf84e1ae9b9).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L8) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L373)
