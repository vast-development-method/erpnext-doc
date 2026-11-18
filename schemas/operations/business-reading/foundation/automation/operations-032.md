# Workflow, automation and dispatch · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Lifecycle

<a id="op-dab1ca1d524037"></a>
### Start

`operation_foundation_binding_foundation_flow_daemon_lifecycle_start`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If supervised().
  - Evaluate \_wait\_for\_supervisor().
  - Return no value.
- Within filelock(LOCK, is\_global = true).
  - Evaluate \_start().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L955)

<a id="op-3cd6b0815cdd98"></a>
### Serve

`operation_foundation_binding_foundation_flow_daemon_lifecycle_serve`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit failure paths** RuntimeError(“set flow\_server\_manager to supervisor in common\_site\_config.json before serving”).

**Local steps**

- If not supervised().
  - If os.environ.get(“FLOW\_SERVER\_MANAGER”) differs from “supervisor”.
    - Raise RuntimeError(“set flow\_server\_manager to supervisor in common\_site\_config.json before serving”).
  - Evaluate update\_site\_config(“flow\_server\_manager”, “supervisor”, site\_config\_path = str((\_sites\_dir() ÷ “common\_site\_config.json”))).
- Evaluate runtime\_dir().mkdir(parents = true, exist\_ok = true).
- Within filelock(LOCK, is\_global = true).
  - Evaluate \_stop().
  - Set tuple(command, env) from \_prepare().
  - Evaluate pid\_file().write\_text(str(os.getpid())).
- Evaluate os.chdir(runtime\_dir()).
- Evaluate os.umask(UMASK).
- Evaluate os.execve(command at 0, command, env).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L949)

<a id="op-7fae53e8cfc0c3"></a>
### Stop

`operation_foundation_binding_foundation_flow_daemon_lifecycle_stop`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Within filelock(LOCK, is\_global = true).
  - Evaluate \_stop().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L234) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L959)

<a id="op-d35a00f2341421"></a>
### Restart

`operation_foundation_binding_foundation_flow_daemon_lifecycle_restart_e3b9eef7fa6d`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate \_stop().
- Evaluate \_start().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L945)

<a id="op-2c7ad8f9513914"></a>
### Start

`operation_foundation_binding_foundation_flow_daemon_lifecycle_start_fcd84b7b1c72`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Locally raised failures** RuntimeError, active or constructed exception.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L956)

<a id="op-99c8bcd7caa09b"></a>
### Prepare

`operation_foundation_binding_foundation_flow_daemon_lifecycle_prepare`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(list at str, dict at tuple(str, str)).

**Explicit results** tuple(command, env).

**Explicit failure paths** RuntimeError(“flow server is missing from the bench environment; reinstall the Flow app”) · RuntimeError(formatted text a flow server already answers on {socket\_path()}; stop it by hand).

**Local steps**

- If not \_flow\_bin().exists().
  - Raise RuntimeError(“flow server is missing from the bench environment; reinstall the Flow app”).
- If healthy().
  - Raise RuntimeError(formatted text a flow server already answers on {socket\_path()}; stop it by hand).
- Evaluate runtime\_dir().mkdir(parents = true, exist\_ok = true).
- Set env from mapping of name → os.environ at name for name drawn from INHERITED\_ENV where name belongs to os.environ.
  - Draw name from INHERITED\_ENV, keep a combination only if (name belongs to os.environ).
- Set env at “FLOW\_TENANTS” from json.dumps(tenant\_template()).
- Set env at “FLOW\_POLICY” from json.dumps(mapping(“tool\_allowlist” → list(“read”, “grep”, “subagent”, “web\_fetch”, …))).
- If redis\_url bound to \_redis\_url().
  - Set env at “FLOW\_REDIS\_URL” from redis\_url.
- Set command from list(str(\_flow\_bin()), “serve”, expanded tuple(“--uds”, str(socket\_path())), expanded tuple(“--data-dir”, str((state\_dir() ÷ “data”))), …).
- Return tuple(command, env).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L941)

<a id="op-235b70cc83ecaa"></a>
### Tenant template

`operation_foundation_binding_foundation_flow_daemon_lifecycle_tenant_template`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“token\_file” → str((site ÷ “site\_config.json”)), “token\_key” → “flow\_server\_secret”, “allowed\_roots” → list(str(((site ÷ “public”) ÷ “files”)), str((nested operand in the contract(nested operand in ….

**Local steps**

- Set site from (\_sites\_dir() ÷ “{site}”).
- Return mapping(“token\_file” → str((site ÷ “site\_config.json”)), “token\_key” → “flow\_server\_secret”, “allowed\_roots” → list(str(((site ÷ “public”) ÷ “files”)), str((nested operand in the contract(nested operand in ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L237) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L962)

<a id="op-4497edc899aebd"></a>
### Wait for supervisor

`operation_foundation_binding_foundation_flow_daemon_lifecycle_wait_for_supervisor`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit failure paths** RuntimeError(“flow server did not become ready under supervisor; check its status and log”).

**Local steps**

- If not \_wait\_until\_healthy().
  - Raise RuntimeError(“flow server did not become ready under supervisor; check its status and log”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L239) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L964)

<a id="op-ed2afe3b048422"></a>
### Wait until healthy

`operation_foundation_binding_foundation_flow_daemon_lifecycle_wait_until_healthy`

**Inputs** process = no value.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set deadline from (time.monotonic() + START\_TIMEOUT).
- While (time.monotonic() &lt; deadline and (process is identical to no value or process.poll() is identical to no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in time.monotonic() &lt; deadline → (process is identical to no value or process.poll() is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in process is identical to no value → process.poll() is identical to no value.
  - If healthy().
    - Return true.
  - Evaluate time.sleep(0.2).
- Return false.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L240) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L965)

<a id="op-c6cfcd6e7fd123"></a>
### Stop

`operation_foundation_binding_foundation_flow_daemon_lifecycle_stop_9a1209df90c1`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set pid from pid\_file().
- Attempt the following.
  - Set process\_id from int(pid.read\_text()).
- On failure (tuple(OSError, ValueError)).
  - Return no value.
- If \_is\_daemon(process\_id).
  - Evaluate os.kill(process\_id, signal.SIGTERM).
  - Set deadline from (time.monotonic() + STOP\_TIMEOUT).
  - While (\_alive(process\_id) and time.monotonic() &lt; deadline).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_alive(process\_id) → time.monotonic() &lt; deadline.
    - Evaluate time.sleep(0.1).
  - If \_alive(process\_id).
    - Evaluate os.kill(process\_id, signal.SIGKILL).
- Evaluate pid.unlink(missing\_ok = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, file state, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L235) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L960)

<a id="op-fd1ab289fc15f9"></a>
### Terminate process

`operation_foundation_binding_foundation_flow_daemon_lifecycle_terminate_process`

**Inputs** process.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If process.poll() is distinct from no value.
  - Return no value.
- Evaluate process.terminate().
- Attempt the following.
  - Evaluate process.wait(timeout = STOP\_TIMEOUT).
- On failure (subprocess.TimeoutExpired).
  - Evaluate process.kill().
  - Evaluate process.wait(timeout = STOP\_TIMEOUT).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L238) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L963)

<a id="op-9c28c9b253f485"></a>
### Status

`operation_foundation_binding_foundation_flow_daemon_lifecycle_status`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** formatted text flow server {state} · sites: {sites}.

**Local steps**

- Set state from formatted text running on {socket\_path()} when healthy(), otherwise “not running”.
  - Value choice on healthy() — true gives formatted text running on {socket\_path()}, false gives “not running”.
- Set sites from (“, ”.join(flow\_sites()) or “none”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(flow\_sites()) → “none”.
- Return formatted text flow server {state} · sites: {sites}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L233) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L958)

<a id="op-23b1be1fbbe88b"></a>
### Flow sites

`operation_foundation_binding_foundation_flow_daemon_lifecycle_flow_sites`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** sites.

**Local steps**

- Set sites from list().
- For each config in sorted(\_sites\_dir().glob(“\*/site\_config.json”)).
  - Attempt the following.
    - If json.loads(config.read\_text(encoding = “utf-8”)).get(“flow\_server\_secret”).
      - Evaluate sites.append(config.parent.name).
  - On failure (tuple(OSError, ValueError)).
    - Continue with the next iteration or loop test.
- Return sites.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L935)

<a id="op-03de48696565cb"></a>
### Healthy

`operation_foundation_binding_foundation_flow_daemon_lifecycle_healthy`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Attempt the following.
  - Within DaemonClient(str(socket\_path())) bound as client.
    - Evaluate client.healthz().
- On failure (DaemonError).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L936)

<a id="op-e81072955eef4e"></a>
### Supervised

`operation_foundation_binding_foundation_flow_daemon_lifecycle_supervised`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** manager equals “supervisor”.

**Explicit failure paths** RuntimeError(“flow\_server\_manager must be local or supervisor in common\_site\_config.json”).

**Local steps**

- Set manager from Platform.get\_common\_site\_config().get(“flow\_server\_manager”, “local”).
- If manager does not belong to tuple(“local”, “supervisor”).
  - Raise RuntimeError(“flow\_server\_manager must be local or supervisor in common\_site\_config.json”).
- Return manager equals “supervisor”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L236) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L961)

<a id="op-c83ed0e0558bab"></a>
### Redis url

`operation_foundation_binding_foundation_flow_daemon_lifecycle_redis_url`

**Inputs** no declared parameters.

**Declared result** (str bitwise or no value).

**Explicit results** (conf.flow\_redis\_url or conf.redis\_queue).

**Local steps**

- Set conf from Platform.get\_common\_site\_config().
- Return (conf.flow\_redis\_url or conf.redis\_queue).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.flow\_redis\_url → conf.redis\_queue.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L943)

<a id="op-0dff5237b2c99c"></a>
### Extension tools

`operation_foundation_binding_foundation_flow_daemon_lifecycle_extension_tools`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** folders.

**Explicit result forms** a structured result, a value selected from the current context.

**Locally raised failures** RuntimeError.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L933)

<a id="op-b974d074d2c91c"></a>
### Is daemon

`operation_foundation_binding_foundation_flow_daemon_lifecycle_is_daemon`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** pid.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L937)

<a id="op-dae619aa908609"></a>
### Alive

`operation_foundation_binding_foundation_flow_daemon_lifecycle_alive`

**Inputs** pid.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Attempt the following.
  - Evaluate os.waitpid(pid, os.WNOHANG).
- On failure (ChildProcessError).
  - Take no action here.
- Attempt the following.
  - Evaluate os.kill(pid, 0).
- On failure (ProcessLookupError).
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L927)

<a id="op-3867092e740154"></a>
### Log tail

`operation_foundation_binding_foundation_flow_daemon_lifecycle_log_tail`

**Inputs** log, chars = 2000.

**Declared result** str.

**Explicit results** log.read\_text() at slice negative chars to no value · empty text.

**Local steps**

- Attempt the following.
  - Return log.read\_text() at slice negative chars to no value.
- On failure (OSError).
  - Return empty text.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L939)

<a id="op-c191c818cd4d3c"></a>
### Socket path

`operation_foundation_binding_foundation_flow_daemon_lifecycle_socket_path`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** (runtime\_dir() ÷ “flow.sock”).

**Local steps**

- Return (runtime\_dir() ÷ “flow.sock”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L954)

<a id="op-edd6d37ff52878"></a>
### Pid file

`operation_foundation_binding_foundation_flow_daemon_lifecycle_pid_file`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** (runtime\_dir() ÷ “daemon.pid”).

**Local steps**

- Return (runtime\_dir() ÷ “daemon.pid”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L940)

<a id="op-8b6aabbe5d1935"></a>
### Log path

`operation_foundation_binding_foundation_flow_daemon_lifecycle_log_path`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** ((Path(get\_bench\_path()) ÷ “logs”) ÷ “flow-server.log”).

**Local steps**

- Return ((Path(get\_bench\_path()) ÷ “logs”) ÷ “flow-server.log”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L938)

<a id="op-28a1c1aa63ff6d"></a>
### Sites dir

`operation_foundation_binding_foundation_flow_daemon_lifecycle_sites_dir`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** Path(get\_bench\_path(), “sites”).resolve().

**Local steps**

- Return Path(get\_bench\_path(), “sites”).resolve().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L953)
