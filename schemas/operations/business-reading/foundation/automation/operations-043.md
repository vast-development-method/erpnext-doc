# Workflow, automation and dispatch · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Runner

<a id="op-8e909a4643a4f7"></a>
### Runner.run

`operation_foundation_runner_business_behavior_runner_run`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each sig in tuple(signal.SIGHUP, signal.SIGINT, signal.SIGTERM).
  - Evaluate signal.signal(sig, self.drain).
- If self.config.has\_restart\_limit.
  - Evaluate RestartWatch(self.config, self.traffic, self.draining).start().
- If self.source.
  - Evaluate self.source.start().
- Evaluate self.jobs.start().
- Evaluate self.scheduler.start().
- Evaluate self.web.serve(self.drain).
- Evaluate self.jobs.stop().
- Evaluate self.jobs.wait(self.config.job\_drain\_seconds).
- If self.restarting.is\_set().
  - Evaluate logger.info(“re-exec”).
  - Evaluate close\_inherited\_fds().
  - Evaluate os.execv(sys.executable, sys.orig\_argv).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L11) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L402)

<a id="op-e20d3f14e5824c"></a>
### Runner.drain

`operation_foundation_runner_business_behavior_runner_drain`

**Inputs** self, sig, frame = no value.

**Declared result** no value.

**Local steps**

- If sig differs from signal.SIGHUP.
  - Evaluate self.restarting.clear().
- Otherwise.
  - If not self.draining.is\_set().
    - Evaluate self.restarting.set().
- If not self.draining.is\_set().
  - Evaluate self.draining.set().
  - Evaluate logger.info(“%s: shutdown starts (%s)”, signal.Signals(sig).name, self.traffic.summary).
  - Evaluate self.jobs.stop().
  - Evaluate self.web.close\_realtime().
- Evaluate self.web.stop(sig, frame).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L7674) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L400)

<a id="op-85cd1958811004"></a>
### Restart Watch.initialize

`operation_foundation_runner_business_behavior_restart_watch_initialize`

**Inputs** self, config, traffic, draining.

**Local steps**

- Set self.config from config.
- Set self.traffic from traffic.
- Set self.draining from draining.
- Set self.thread from threading.Thread(target = self.\_watch, name = “restart-watch”, daemon = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L395)

<a id="op-754e9cc4492e7d"></a>
### Restart Watch.start

`operation_foundation_runner_business_behavior_restart_watch_start`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.thread.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L184) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L398)

<a id="op-95822724db48c3"></a>
### Restart Watch.is limit reached

`operation_foundation_runner_business_behavior_restart_watch_is_limit_reached`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** (bool((config.restart\_after\_requests and counts at “web” ≥ config.restart\_after\_requests)) or bool((config.restart\_after\_jobs and counts at “jobs” ≥ config.restart\_after\_jobs))).

**Local steps**

- Set counts from self.traffic.counts.
- Set config from self.config.
- Return (bool((config.restart\_after\_requests and counts at “web” ≥ config.restart\_after\_requests)) or bool((config.restart\_after\_jobs and counts at “jobs” ≥ config.restart\_after\_jobs))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bool((config.restart\_after\_requests and counts at “web” ≥ config.restart\_after\_requests)) → bool((config.restart\_after\_jobs and counts at “jobs” ≥ config.restart\_after\_jobs)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in config.restart\_after\_requests → counts at “web” ≥ config.restart\_after\_requests.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in config.restart\_after\_jobs → counts at “jobs” ≥ config.restart\_after\_jobs.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L237) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L397)

<a id="op-3a7a2a3540fdaf"></a>
### Restart Watch.is idle

`operation_foundation_runner_business_behavior_restart_watch_is_idle`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** bool.

**Explicit results** bool((self.config.restart\_idle\_seconds and any(nested operand in the contract.traffic.counts.values()) and self.traffic.idle\_seconds ≥ self.config.restart\_idle\_seconds)).

**Local steps**

- Return bool((self.config.restart\_idle\_seconds and any(nested operand in the contract.traffic.counts.values()) and self.traffic.idle\_seconds ≥ self.config.restart\_idle\_seconds)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.config.restart\_idle\_seconds → any(self.traffic.counts.values()) → self.traffic.idle\_seconds ≥ self.config.restart\_idle\_seconds.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L427) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L396)

<a id="op-cf32a98f4aebf3"></a>
### Restart Watch.watch

`operation_foundation_runner_business_behavior_restart_watch_watch`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- While not self.draining.wait(RESTART\_CHECK\_SECONDS).
  - If self.traffic.in\_flight.
    - Continue with the next iteration or loop test.
  - If (self.is\_limit\_reached or self.is\_idle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_limit\_reached → self.is\_idle.
    - Evaluate logger.info(“restart (%s), idle %.0fs”, self.traffic.summary, self.traffic.idle\_seconds).
    - Evaluate os.kill(os.getpid(), signal.SIGHUP).
    - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L565) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L399)

<a id="op-97e42b6080c7fd"></a>
### Source Watch.initialize

`operation_foundation_runner_business_behavior_source_watch_initialize`

**Inputs** self, draining.

**Local steps**

- Set self.draining from draining.
- Set self.fired from threading.Event().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L774) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L406)

<a id="op-7e47ec0b4baefd"></a>
### Source Watch.start

`operation_foundation_runner_business_behavior_source_watch_start`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** SystemExit(“--dev needs watchdog: pip install 'Platform&#91;dev&#93;'”).

**Local steps**

- Attempt the following.
  - Bind dependencies Observer.
- On failure (ImportError) bound to e.
  - Raise SystemExit(“--dev needs watchdog: pip install 'Platform&#91;dev&#93;'”) with cause e.
- Set paths from list().
- For each app in Platform.get\_all\_apps().
  - Within suppress(ImportError).
    - Evaluate paths.append(Platform.get\_app\_path(app)).
- Set observer from Observer().
- Set observer.daemon from true.
- For each path in paths.
  - Evaluate observer.schedule(self, path, recursive = true).
- Evaluate observer.start().
- Evaluate logger.info(“dev: watching %s”, “, ”.join(paths)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L862) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L408)

<a id="op-889e29355f8b4a"></a>
### Source Watch.dispatch

`operation_foundation_runner_business_behavior_source_watch_dispatch`

**Inputs** self, event.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set path from (getattr(event, “dest\_path”, empty text) or event.src\_path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(event, “dest\_path”, empty text) → event.src\_path.
- If (event.is\_directory or event.event\_type does not belong to self.CHANGES or not path.endswith(“.py”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in event.is\_directory → event.event\_type does not belong to self.CHANGES → not path.endswith(“.py”).
  - Return no value.
- If (self.draining.is\_set() or self.fired.is\_set()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.draining.is\_set() → self.fired.is\_set().
  - Return no value.
- Evaluate self.fired.set().
- Evaluate logger.info(“dev: %s changed, reloading”, path).
- Evaluate threading.Timer(SOURCE\_QUIET\_SECONDS, self.reload).start().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(event, “dest\_path”, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L1205) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L405)

<a id="op-aa39c90f55d946"></a>
### Source Watch.reload

`operation_foundation_runner_business_behavior_source_watch_reload`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If not self.draining.is\_set().
  - Evaluate os.kill(os.getpid(), signal.SIGHUP).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L1511) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L407)

<a id="op-bb0f3085036f9f"></a>
### Main

`operation_foundation_runner_business_behavior_main`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Set parser from argparse.ArgumentParser(description = \_\_doc\_\_, formatter\_class = HelpFormatter).
- Evaluate parser.add\_argument(“--host”, default = “127.0.0.1”, help = “address to listen on”).
- Evaluate parser.add\_argument(“--port”, type = int, default = 8000, help = “port to listen on”).
- Evaluate parser.add\_argument(“--queue”, help = “comma separated queues; unset means all of them”).
- Evaluate parser.add\_argument(“--verbose”, action = “store\_true”, help = “log each job and each realtime packet”).
- Evaluate parser.add\_argument(“--dev”, action = “store\_true”, help = “reload on a change of a python file, and send the assets”).
- Evaluate parser.add\_argument(“--web-threads”, type = int, default = 0, help = “concurrent web requests (0 = the default of Platform.asgi)”).
- Evaluate parser.add\_argument(“--job-threads”, type = int, default = 1, help = “concurrent background jobs”).
- Evaluate parser.add\_argument(“--restart-after-requests”, type = int, default = 5000, help = “web requests before a restart (0 = never)”).
- Evaluate parser.add\_argument(“--restart-after-jobs”, type = int, default = 500, help = “jobs before a restart (0 = never)”).
- Evaluate parser.add\_argument(“--restart-idle-seconds”, type = float, default = 300, help = “time without a web request before a restart (0 = never)”).
- Evaluate parser.add\_argument(“--request-drain-seconds”, type = float, default = 60, help = “how long to wait for the open requests”).
- Evaluate parser.add\_argument(“--job-drain-seconds”, type = float, default = 600, help = “how long to wait for a job in progress”).
- Set config from Config(expanded names vars(parser.parse\_args())).
- Evaluate logging.basicConfig(level = logging.INFO, format = “%(asctime)s %(levelname)s %(name)s %(message)s”).
- If config.verbose.
  - Evaluate logging.getLogger(“Platform.realtime.packets”).setLevel(logging.INFO).
- Evaluate Runner(config).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L1613) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L394)

## Service · Safe exec

<a id="op-ca3512641c0160"></a>
### Safe exec

`operation_foundation_binding_foundation_flow_utils_safe_exec_safe_exec`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script, \_globals, \_locals, script\_filename, tool\_context.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1443)

<a id="op-64cd2c417399c2"></a>
### Gated get doc

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_get_doc`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1430)

<a id="op-ec26463366c9f4"></a>
### Gated get last doc

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_get_last_doc`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, filters, order\_by, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1431)

<a id="op-4295fe05f00107"></a>
### Readable name

`operation_foundation_binding_foundation_flow_utils_safe_exec_readable_name`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, filters, order\_by.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** DoesNotExistError.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1442)

<a id="op-d84e67f7d849f8"></a>
### Gated get meta

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_get_meta`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, cached.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1432)

<a id="op-60f702d89e5164"></a>
### Gated get print

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_get_print`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, name, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1433)

<a id="op-29f3e4cbf50e2a"></a>
### Gated attach print

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_attach_print`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, name, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1428)

<a id="op-aea6e142e09aed"></a>
### Gated enqueue

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_enqueue`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** function, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1429)

<a id="op-b429ad18b7b7e7"></a>
### Gated sendmail

`operation_foundation_binding_foundation_flow_utils_safe_exec_gated_sendmail`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup, notification or queued-work request, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1434)

<a id="op-37592d082a64db"></a>
### Readable attachment

`operation_foundation_binding_foundation_flow_utils_safe_exec_readable_attachment`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** attachment.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1441)

<a id="op-4d55484bef0d6e"></a>
### Permissioned get list

`operation_foundation_binding_foundation_flow_utils_safe_exec_permissioned_get_list`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1438)

<a id="op-53d24ba90a1f47"></a>
### Permissioned get value

`operation_foundation_binding_foundation_flow_utils_safe_exec_permissioned_get_value`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, filters, fieldname, as\_dict.

**Explicit result forms** a structured result, a value selected from the current context, no value, the result of a delegated call.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1440)
