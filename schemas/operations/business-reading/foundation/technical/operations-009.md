# Site operations and diagnostics · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Monitor

<a id="op-0549a3ba36e4dc"></a>
### Monitor.initialize

`operation_foundation_monitor_business_behavior_monitor_initialize`

**Inputs** self, transaction\_type, method, kwargs.

**Local steps**

- Attempt the following.
  - Set self.data from Platform.\_dict(mapping(“site” → Platform.local.site, “timestamp” → datetime.datetime.now(datetime.UTC), “transaction\_type” → transaction\_type, “uuid” → str(uuid.uuid4()))).
  - If transaction\_type equals “request”.
    - Evaluate self.collect\_request\_meta().
  - Otherwise.
    - Evaluate self.collect\_job\_meta(method, kwargs).
- On failure (Exception).
  - Evaluate traceback.print\_exc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [collect request meta](operations-009.md#op-61f5b939c6dc3f), [collect job meta](operations-009.md#op-8683e1a9de45be).

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(datetime.UTC), uuid.uuid4().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L3254) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1436)

<a id="op-61f5b939c6dc3f"></a>
### Monitor.collect request meta

`operation_foundation_monitor_business_behavior_monitor_collect_request_meta`

**Inputs** self.

**Local steps**

- Set self.data.request from Platform.\_dict(mapping(“ip” → Platform.local.request\_ip, “method” → Platform.request.method, “path” → Platform.request.path)).
- If (request\_id bound to Platform.request.headers.get(“X-Platform-Request-Id”) and TRACE\_ID\_PATTERN.fullmatch(request\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in request\_id bound to Platform.request.headers.get(“X-Platform-Request-Id”) → TRACE\_ID\_PATTERN.fullmatch(request\_id).
  - Set self.data.uuid from request\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L3560) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1434)

<a id="op-8683e1a9de45be"></a>
### Monitor.collect job meta

`operation_foundation_monitor_business_behavior_monitor_collect_job_meta`

**Inputs** self, method, kwargs.

**Local steps**

- Bind dependencies rq.
- Set self.data.job from Platform.\_dict(mapping(“method” → method, “scheduled” → false, “wait” → 0)).
- If “run\_scheduled\_job” belongs to method.
  - Set self.data.job.method from kwargs at “job\_type”.
  - Set self.data.job.scheduled from true.
- If job bound to rq.get\_current\_job().
  - Set self.data.job\_id from job.id.
  - Set waitdiff from (self.data.timestamp − job.enqueued\_at.replace(tzinfo = datetime.UTC)).
  - Set self.data.job.wait from int((waitdiff.total\_seconds() × 1000000)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L3784) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1433)

<a id="op-309abeb33cdcec"></a>
### Monitor.add custom data

`operation_foundation_monitor_business_behavior_monitor_add_custom_data`

**Inputs** self, remaining named values kwargs.

**Local steps**

- If self.data.
  - Evaluate self.data.update(kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L4161) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1432)

<a id="op-9203184bc09148"></a>
### Monitor.dump

`operation_foundation_monitor_business_behavior_monitor_dump`

**Inputs** self, response = no value.

**Local steps**

- Attempt the following.
  - Set timediff from (datetime.datetime.now(datetime.UTC) − self.data.timestamp).
  - Set self.data.duration from int((timediff.total\_seconds() × 1000000)).
  - If self.data.transaction\_type equals “request”.
    - If response.
      - Set self.data.request.status\_code from response.status\_code.
      - Set self.data.request.response\_length from int(response.headers.get(“Content-Length”, 0)).
    - Otherwise.
      - Set self.data.request.status\_code from 500.
    - If hasattr(Platform.local, “rate\_limiter”).
      - Set limiter from Platform.local.rate\_limiter.
      - Set self.data.request.counter from limiter.counter.
      - If limiter.rejected.
        - Set self.data.request.reset from limiter.reset.
  - Evaluate self.store().
- On failure (Exception).
  - Evaluate traceback.print\_exc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [store](operations-009.md#op-254733e3cb6c1d).

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(datetime.UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L4238) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1435)

<a id="op-254733e3cb6c1d"></a>
### Monitor.store

`operation_foundation_monitor_business_behavior_monitor_store`

**Inputs** self.

**Local steps**

- Set serialized from json.dumps(self.data, sort\_keys = true, default = str, separators = tuple(“,”, “:”)).
- Set length from Platform.cache.rpush(MONITOR\_REDIS\_KEY, serialized).
- If cint(length) &gt; MONITOR\_MAX\_ENTRIES.
  - Evaluate Platform.cache.ltrim(MONITOR\_REDIS\_KEY, 1, negative 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L4721) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1437)

<a id="op-4352e79944d1bf"></a>
### Flush

`operation_foundation_monitor_business_behavior_flush`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set logs from Platform.cache.lrange(MONITOR\_REDIS\_KEY, 0, negative 1).
- If not logs.
  - Return no value.
- Set logs from list(map(Platform.safe\_decode, logs)).
- Within filelock(“monitor\_flush”, is\_global = true, timeout = 5).
  - Within open(log\_file(), “a”) bound as f.
    - Evaluate f.write(whitespace '\\n'.join(logs)).
    - Evaluate f.write(whitespace '\\n').
- Evaluate Platform.cache.ltrim(MONITOR\_REDIS\_KEY, len(logs), negative 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L4935) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1429)

## Service · Optimizations

<a id="op-3d4526ef55431c"></a>
### Optimize all

`operation_foundation_optimizations_business_behavior_optimize_all`

**Inputs** no declared parameters.

**Local steps**

- Evaluate optimize\_regex\_cache().
- Evaluate optimize\_gc\_parameters().
- Evaluate optimize\_gc\_for\_copy\_on\_write().
- Evaluate optimize\_for\_gil\_contention().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L35) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1443)

<a id="op-44cbadd4025674"></a>
### Optimize gc parameters

`operation_foundation_optimizations_business_behavior_optimize_garbage_collection_parameters`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Bind dependencies sbool.
- If not bool(sbool(os.environ.get(“Platform\_TUNE\_GC”, true))).
  - Return no value.
- Set tuple(g0, g1, g2) from gc.get\_threshold().
- Evaluate gc.set\_threshold((g0 × 10), (g1 × 2), (g2 × 2)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L2301) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1445)

<a id="op-46180a872f3808"></a>
### Optimize regex cache

`operation_foundation_optimizations_business_behavior_optimize_regular_expression_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate os.register\_at\_fork(before = re.purge).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L2494) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1446)

<a id="op-25f75c07dfb46e"></a>
### Preload modules

`operation_foundation_optimizations_business_behavior_preload_modules`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If nested operand in the contract.get(“Platform\_PRELOAD\_MODULES”, “1”).strip().lower() belongs to tuple(“0”, “false”).
  - Return no value.
- Bind dependencies gettext.
- Bind dependencies babel.
- Bind dependencies babel.dates.
- Bind dependencies bs4.
- Bind dependencies nh3.
- Bind dependencies num2words.
- Bind dependencies pydantic.
- Bind dependencies Platform.boot.
- Bind dependencies Platform.client.
- Bind dependencies Platform.core.doctype.file.file.
- Bind dependencies Platform.core.doctype.user.user.
- Bind dependencies Platform.database.query.
- Bind dependencies Platform.desk.desktop.
- Bind dependencies Platform.desk.form.save.
- Bind dependencies Platform.model.db\_query.
- Bind dependencies Platform.query\_builder.
- Bind dependencies Platform.utils.background\_jobs.
- Bind dependencies Platform.utils.data.
- Bind dependencies Platform.utils.jinja.
- Bind dependencies Platform.utils.jinja\_globals.
- Bind dependencies Platform.utils.redis\_wrapper.
- Bind dependencies Platform.utils.safe\_exec.
- Bind dependencies Platform.utils.typing\_validations.
- Bind dependencies Platform.website.path\_resolver.
- Bind dependencies Platform.website.router.
- Bind dependencies Platform.website.website\_generator.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L2549) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1448)

<a id="op-65e537953c1eaf"></a>
### Preload database drivers

`operation_foundation_optimizations_business_behavior_preload_database_drivers`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set value from (nested operand in the contract.get(“Platform\_PRELOAD\_DATABASE\_DRIVERS”, empty text).strip().lower() or “mariadb”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract.environ.get(“Platform\_PRELOAD\_DATABASE\_DRIVERS”, empty text).strip().lower() → “mariadb”.
- If value equals “none”.
  - Return no value.
- Set drivers from set of driver.strip() for driver drawn from value.split(“,”) where driver.strip().
  - Draw driver from value.split(“,”), keep a combination only if (driver.strip()).
- If “mariadb” belongs to drivers.
  - Bind dependencies Platform.database.mariadb.mysqlclient.
- If “postgres” belongs to drivers.
  - Bind dependencies Platform.database.postgres.database.
- If “sqlite” belongs to drivers.
  - Bind dependencies Platform.database.sqlite.database.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L2915) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1447)

<a id="op-b7ae73f5f08e8a"></a>
### Register fault handler

`operation_foundation_optimizations_business_behavior_register_fault_handler`

**Inputs** no declared parameters.

**Local steps**

- If isinstance(sys.\_\_stderr\_\_, io.TextIOWrapper).
  - Evaluate faulthandler.enable().
  - Evaluate faulthandler.register(signal.SIGUSR1, file = sys.\_\_stderr\_\_).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L3204) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1449)

<a id="op-2c0a4eb85b7e11"></a>
### Optimize gc for copy on write

`operation_foundation_optimizations_business_behavior_optimize_garbage_collection_for_copy_on_write`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Bind dependencies sbool.
- If not bool(sbool(os.environ.get(“Platform\_TUNE\_GC”, true))).
  - Return no value.
- Evaluate os.register\_at\_fork(before = freeze\_gc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L3320) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1444)

<a id="op-6f63d92373e523"></a>
### Freeze gc

`operation_foundation_optimizations_business_behavior_freeze_garbage_collection`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Use module bindings \_gc\_frozen.
- If \_gc\_frozen.
  - Return no value.
- Evaluate gc.collect().
- Evaluate gc.freeze().
- Set \_gc\_frozen from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L3449) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1442)

<a id="op-dd9d7d078e4fd7"></a>
### Optimize for gil contention

`operation_foundation_binding_foundation_optimizations_optimize_for_gil_contention`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not os.environ.get(“Platform\_PERF\_PIN\_WORKERS”).
  - Return no value.
- If “gunicorn” does not belong to str(sys.argv at 0).
  - Return no value.
- If os.environ.get(“Platform\_PERF\_PIN\_WORKERS\_DETERMINISTIC”).
  - Use module bindings worker\_num.
  - Set worker\_num from 0.
- If not psutil.LINUX.
  - Return no value.
- Set \_ from parse\_thread\_siblings().
- Evaluate os.register\_at\_fork(after\_in\_parent = increment\_worker\_count, after\_in\_child = pin\_web\_worker\_to\_one\_core).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1646)

<a id="op-fa851f4e3fe598"></a>
### Increment worker count

`operation_foundation_binding_foundation_optimizations_increment_worker_count`

**Inputs** no declared parameters.

**Local steps**

- Use module bindings worker\_num.
- Update worker\_num using + 1.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1645)

<a id="op-96abe136d8d17b"></a>
### Assign core

`operation_foundation_binding_foundation_optimizations_assign_core`

**Inputs** pid, physical\_cpu\_count, logical\_cpu\_count, current\_affinity, thread\_siblings.

**Declared result** (int bitwise or no value).

**Explicit results** current\_affinity at 0 · physical\_core · no value · logical\_core.

**Local steps**

- If len(current\_affinity) equals 1.
  - Return current\_affinity at 0.
- If (sorted(current\_affinity) equals list(range(physical\_cpu\_count)) and physical\_cpu\_count equals logical\_cpu\_count).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sorted(current\_affinity) equals list(range(physical\_cpu\_count)) → physical\_cpu\_count equals logical\_cpu\_count.
  - Set physical\_core from current\_affinity at (pid modulo or format physical\_cpu\_count).
  - Return physical\_core.
- If not thread\_siblings.
  - Return no value.
- Set thread\_bucket from thread\_siblings at (pid modulo or format len(thread\_siblings)).
- Set logical\_core from thread\_bucket at ((pid modulo or format (len(thread\_siblings) × len(thread\_bucket))) floor divide len(thread\_siblings)).
- Return logical\_core.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1644)

<a id="op-785b4d1d90d08b"></a>
### Pin web worker to one core

`operation_foundation_binding_foundation_optimizations_pin_web_worker_to_one_core`

**Inputs** no declared parameters.

**Local steps**

- Set core from assign\_core(pid = worker\_num, physical\_cpu\_count = psutil.cpu\_count(logical = false), logical\_cpu\_count = psutil.cpu\_count(logical = true), current\_affinity = sorted(os.sched\_getaffinity(0)), …).
- If core is distinct from no value.
  - Evaluate psutil.Process().cpu\_affinity(list(core)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1648)

<a id="op-96e6253ad8d080"></a>
### Parse thread siblings

`operation_foundation_binding_foundation_optimizations_parse_thread_siblings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** lru\_cache(maxsize = 1).

**Declared result** (list at tuple at tuple(int, int) bitwise or no value).

**Explicit results** sorted(threads\_list).

**Local steps**

- Attempt the following.
  - Set threads\_list from set().
  - Set siblings\_pattern from “/sys/devices/system/cpu/cpu&#91;0-9&#93;\*/topology/core\_cpus\_list”.
  - For each path in glob.glob(siblings\_pattern).
    - Evaluate threads\_list.add(tuple(generator of int(cpu) for cpu drawn from nested operand in the contract.replace(“-”, “,”).split(“,”))).
      - Draw cpu from nested operand in the contract(nested operand in the contract).read\_text().replace(“-”, “,”).split(“,”).
  - Return sorted(threads\_list).
- On failure (Exception) bound to e.
  - Bind dependencies Platform.
  - Set logger from Platform.logger(with\_more\_info = true).
  - Evaluate logger.error(formatted text failed to parse thread siblings: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1647)

## Service · Parallel test runner

<a id="op-ae17cb8c3dd06b"></a>
### Parallel Test Runner.initialize

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_initialize`

**Inputs** self, app, site, build\_number = 1, total\_builds = 1, dry\_run = false, lightmode = false.

**Local steps**

- Set self.app from app.
- Set self.site from site.
- Set self.build\_number from (Platform.utils.cint(build\_number) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.cint(build\_number) → 1.
- Set self.total\_builds from Platform.utils.cint(total\_builds).
- Set self.dry\_run from dry\_run.
- Set self.lightmode from lightmode.
- Set self.test\_file\_list from list().
- Set self.total\_test\_weight from 0.
- Set self.test\_result from no value.
- Evaluate self.setup\_test\_file\_list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup test file list](operations-010.md#op-a842e3d3b733e8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L36) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1455)

<a id="op-f7ec61c6827e7e"></a>
### Parallel Test Runner.setup and run

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_setup_and_run`

**Inputs** self.

**Local steps**

- Evaluate self.setup\_test\_site().
- Evaluate self.run\_tests().
- Evaluate self.print\_result().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup test site](operations-009.md#op-f84c2e94b22cbc), [run tests](operations-010.md#op-bde15359a06a99), [print result](operations-010.md#op-73591ee3afe4a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L350) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1459)

<a id="op-f84c2e94b22cbc"></a>
### Parallel Test Runner.setup test site

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_setup_test_site`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.init(self.site).
- If not Platform.db.
  - Evaluate Platform.connect().
- If self.dry\_run.
  - Return no value.
- Evaluate toggle\_test\_mode(true).
- Evaluate Platform.clear\_cache().
- Evaluate Platform.utils.scheduler.disable\_scheduler().
- If not self.lightmode.
  - Evaluate \_decorate\_all\_methods\_and\_functions\_with\_type\_checker().
  - Evaluate self.before\_test\_setup().

If control reaches the end, it returns no value.

**Methods declared on this owner** [before test setup](operations-009.md#op-5eee937803a091).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L38) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1461)

<a id="op-5eee937803a091"></a>
### Parallel Test Runner.before test setup

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_before_test_setup`

**Inputs** self.

**Local steps**

- Set start\_time from time.monotonic().
- For each fn in Platform.get\_hooks(“before\_tests”, app\_name = self.app).
  - Evaluate Platform.get\_attr(fn)().
- Set test\_module from Platform.get\_module(formatted text {self.app}.tests).
- If hasattr(test\_module, “global\_test\_dependencies”).
  - For each doctype in test\_module.global\_test\_dependencies.
    - Evaluate make\_test\_records(doctype, commit = true).
- Set elapsed from (time.monotonic() − start\_time).
- Set elapsed from click.style(formatted text  ({elapsed}s), fg = “red”).
- Evaluate click.echo(formatted text Before Test {elapsed}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic() · selected callable from Platform.get\_hooks(“before\_tests”, app\_name = self.app), Platform.get\_attr(fn).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L665) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1451)
