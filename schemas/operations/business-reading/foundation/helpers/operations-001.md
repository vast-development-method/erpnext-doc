# Shared value and file services · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · App heartbeat event

<a id="op-681416c2612e74"></a>
### Capture app heartbeat

`operation_foundation_utils_telemetry_pulse_app_heartbeat_event_business_behavior_capture_application_heartbeat`

**Inputs** app.

**Explicit results** no value.

**Local steps**

- If not should\_capture().
  - Return no value.
- If (app and app differs from “Platform”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in app → app differs from “Platform”.
  - Evaluate capture(event\_name = “app\_heartbeat”, app = app, properties = mapping(“app\_version” → get\_app\_version(app), “Platform\_version” → get\_Platform\_version()), interval = “6h”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L6685) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L726)

<a id="op-baab599b21e744"></a>
### Should capture

`operation_foundation_utils_telemetry_pulse_app_heartbeat_event_business_behavior_should_capture`

**Inputs** no declared parameters.

**Explicit results** false · true.

**Local steps**

- If (not is\_enabled() or Platform.session.user belongs to Platform.STANDARD\_USERS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_enabled() → Platform.session.user belongs to Platform.STANDARD\_USERS.
  - Return false.
- Set status\_code from (Platform.response.http\_status\_code or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.response.http\_status\_code → 0.
- If (status\_code and not 200 ≤ status\_code &lt; 300).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status\_code → not 200 ≤ status\_code &lt; 300.
  - Compare adjacent operands in order, stopping at the first false comparison in 200 ≤ status\_code &lt; 300.
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L6885) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L727)

## Service · Background jobs

<a id="op-3d4402abedcffe"></a>
### Get queues timeout

`operation_foundation_utils_background_jobs_business_behavior_get_queues_timeout`

**Inputs** no declared parameters.

**Wrappers, in declaration order** lru\_cache.

**Declared result** dict at tuple(str, int).

**Explicit results** mapping(“short” → default\_timeout, “default” → default\_timeout, “long” → 1500, expand mapping of worker → config.get(“timeout”, default\_timeout) for tuple(worker, config) drawn from custom\_workers\_config.items()).

**Local steps**

- Set common\_site\_config from Platform.get\_conf().
- Set custom\_workers\_config from common\_site\_config.get(“workers”, mapping()).
- Set default\_timeout from 300.
- Return mapping(“short” → default\_timeout, “default” → default\_timeout, “long” → 1500, expand mapping of worker → config.get(“timeout”, default\_timeout) for tuple(worker, config) drawn from custom\_workers\_config.items()).
  - Draw tuple(worker, config) from custom\_workers\_config.items().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L66) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1484)

<a id="op-7812cadd94f87e"></a>
### Enqueue

`operation_foundation_utils_background_jobs_business_behavior_enqueue`

**Inputs** method, queue = “default”, timeout = no value, event = no value, is\_async = true, job\_name = no value, now = false, enqueue\_after\_commit = false, on\_success (named only, default no value), on\_failure (named only, default no value), at\_front (named only, default false), job\_id (named only, default no value), deduplicate (named only, default false), at\_front\_when\_starved (named only, default false), remaining named values kwargs.

**Declared result** (Job bitwise or Any).

**Explicit results** no value · Platform.call(method, expanded names kwargs) · enqueue\_call().

**Explicit failure paths** validation helper — translated “′job\_id′ paramater is required for deduplication.” · propagate active failure.

**Local steps**

- Set is\_async from kwargs.pop(“async”, is\_async).
- If deduplicate.
  - If not job\_id.
    - Call the validation error handler Platform.throw(translated “′job\_id′ paramater is required for deduplication.”).
  - Set job from get\_job(job\_id).
  - If (job and job.get\_status(refresh = false) belongs to tuple(JobStatus.QUEUED, JobStatus.STARTED)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in job → job.get\_status(refresh = false) belongs to tuple(JobStatus.QUEUED, JobStatus.STARTED).
    - Evaluate Platform.logger().error(formatted text Not queueing job {job.id} because it is in queue already).
    - Return no value.
  - Otherwise.
    - If job.
      - Evaluate job.delete().
- Set job\_id from create\_job\_id(job\_id).
- If job\_name.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
- If (not is\_async and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_async → not Platform.in\_test.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
- Set call\_directly from (now or (not is\_async and not Platform.in\_test)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in now → (not is\_async and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_async → not Platform.in\_test.
- If call\_directly.
  - Return Platform.call(method, expanded names kwargs).
- Attempt the following.
  - Set q from get\_queue(queue, is\_async = is\_async).
- On failure (ConnectionError).
  - If Platform.local.flags.in\_migrate.
    - Evaluate print(formatted text Redis queue is unreachable: Executing {method} synchronously).
    - Return Platform.call(method, expanded names kwargs).
  - Propagate the active failure.
- Evaluate \_check\_queue\_size(q).
- If not timeout.
  - Set timeout from (get\_queues\_timeout().get(queue) or 300).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_queues\_timeout().get(queue) → 300.
- If isinstance(method, Callable).
  - Set method\_name from formatted text {method.\_\_module\_\_}.{method.\_\_qualname\_\_}.
- Otherwise.
  - Set method\_name from method.
- Set queue\_args from mapping(“site” → Platform.local.site, “user” → Platform.session.user, “method” → method, “event” → event, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_name → method\_name.
- Set on\_failure from (on\_failure or truncate\_failed\_registry).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in on\_failure → truncate\_failed\_registry.
- If (at\_front\_when\_starved and q.count &gt; QUEUE\_STARVATION\_THRESHOLD).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in at\_front\_when\_starved → q.count &gt; QUEUE\_STARVATION\_THRESHOLD.
  - Set at\_front from true.
- Bind local operation enqueue\_call for subsequent calls.
- If enqueue\_after\_commit.
  - Evaluate Platform.db.after\_commit.add(enqueue\_call).
  - Return no value.
- Return enqueue\_call().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L63) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1460)

<a id="op-8969d96be8f045"></a>
### Enqueue.enqueue call

`operation_foundation_utils_background_jobs_business_behavior_enqueue_enqueue_call`

**Inputs** no declared parameters.

**Explicit results** q.enqueue\_call(“Platform.utils.background\_jobs.execute\_job”, on\_success = Callback(func = on\_success) when on\_success, otherwise no value, on\_failure = Callback(func = on\_failure), timeout = timeout, kwarg ….

**Local steps**

- Return q.enqueue\_call(“Platform.utils.background\_jobs.execute\_job”, on\_success = Callback(func = on\_success) when on\_success, otherwise no value, on\_failure = Callback(func = on\_failure), timeout = timeout, kwarg ….
  - Value choice on on\_success — true gives Callback(func = on\_success), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“rq\_job\_failure\_ttl”) → RQ\_JOB\_FAILURE\_TTL.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“rq\_results\_ttl”) → RQ\_RESULTS\_TTL.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L64) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1461)

<a id="op-0e8ca8fefc8aa2"></a>
### Enqueue doc

`operation_foundation_utils_background_jobs_business_behavior_enqueue_record`

**Inputs** doctype, name = no value, method = no value, queue = “default”, timeout = 300, now = false, remaining named values kwargs.

**Explicit results** enqueue(“Platform.utils.background\_jobs.run\_doc\_method”, doctype = doctype, name = name, doc\_method = method, queue = queue, …).

**Local steps**

- Return enqueue(“Platform.utils.background\_jobs.run\_doc\_method”, doctype = doctype, name = name, doc\_method = method, queue = queue, …).

**Values supplied outside this operation** service or queued work from enqueue(“Platform.utils.background\_jobs.run\_doc\_method”, doctype = doctype, name = name, doc\_method = method, queue = queue, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L3014) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1462)

<a id="op-dec486db0b1eb2"></a>
### Run doc method

`operation_foundation_utils_background_jobs_business_behavior_run_record_method`

**Inputs** doctype, name, doc\_method, remaining named values kwargs.

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Evaluate getattr(Platform.get\_doc(doctype, name), doc\_method)(expanded names kwargs).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.get\_doc(doctype, name), doc\_method).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L3240) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1490)

<a id="op-5424d960298d99"></a>
### Execute job

`operation_foundation_utils_background_jobs_business_behavior_execute_job`

**Inputs** site, method, event, job\_name, kwargs, user = no value, is\_async = true, retry = 0.

**State and service calls** rollback · commit.

**Explicit results** execute\_job(site, method, event, job\_name, is\_async = is\_async, retry = (retry + 1), …) · retval.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set retval from no value.
- If is\_async.
  - Evaluate Platform.init(site, force = true, is\_job = true).
  - Evaluate Platform.connect().
  - If os.environ.get(“CI”).
    - Bind dependencies toggle\_test\_mode.
    - Evaluate toggle\_test\_mode(true).
  - If user.
    - Evaluate Platform.set\_user(user).
- If isinstance(method, str).
  - Set method\_name from method.
  - Set method from Platform.get\_attr(method).
- Otherwise.
  - Set method\_name from formatted text {method.\_\_module\_\_}.{method.\_\_qualname\_\_}.
- Set Platform.local.job from Platform.\_dict(site = site, method = method\_name, job\_name = job\_name, kwargs = kwargs, …).
- For each before\_job\_task in Platform.get\_hooks(“before\_job”).
  - Evaluate Platform.call(before\_job\_task, method = method\_name, kwargs = kwargs, transaction\_type = “job”).
- Attempt the following.
  - Set retval from method(expanded names kwargs).
- On failure (tuple(Platform.db.InternalError, Platform.RetryBackgroundJobError)) bound to e.
  - Evaluate Platform.db.rollback(chain = true).
  - If (retry &lt; 5 and (isinstance(e, Platform.RetryBackgroundJobError) or (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in retry &lt; 5 → (isinstance(e, Platform.RetryBackgroundJobError) or (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(e, Platform.RetryBackgroundJobError) → (Platform.db.is\_deadlocked(e) or Platform.db.is\_timedout(e)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.is\_deadlocked(e) → Platform.db.is\_timedout(e).
    - Evaluate Platform.job.after\_job.reset().
    - Evaluate Platform.destroy().
    - Evaluate time.sleep((retry + 1)).
    - Return execute\_job(site, method, event, job\_name, is\_async = is\_async, retry = (retry + 1), …).
  - Otherwise.
    - Evaluate Platform.log\_error(title = method\_name).
    - Propagate the active failure.
- On failure (Exception) bound to e.
  - Evaluate Platform.db.rollback(chain = true).
  - Evaluate Platform.log\_error(title = method\_name).
  - Evaluate Platform.monitor.add\_data\_to\_monitor(exception = e.\_\_class\_\_.\_\_name\_\_).
  - Evaluate Platform.db.commit(chain = true).
  - Evaluate print(Platform.get\_traceback()).
  - Propagate the active failure.
- When the protected block completes normally.
  - Evaluate Platform.db.commit(chain = true).
  - Return retval.
- On exit, including pending return or failure.
  - If not hasattr(Platform.local, “site”).
    - Evaluate Platform.init(site, force = true, is\_job = true).
    - Evaluate Platform.connect().
  - For each after\_job\_task in Platform.get\_hooks(“after\_job”).
    - Evaluate Platform.call(after\_job\_task, method = method\_name, kwargs = kwargs, result = retval).
  - Evaluate Platform.local.job.after\_job.run().
  - If is\_async.
    - Evaluate Platform.destroy().

**Values supplied outside this operation** selected callable from Platform.get\_attr(method), Platform.get\_hooks(“before\_job”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L3349) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1464)

<a id="op-213316b956f843"></a>
### Start worker

`operation_foundation_utils_background_jobs_business_behavior_start_worker`

**Inputs** queue = no value, quiet = false, rq\_username = no value, rq\_password = no value, burst = false, strategy = DequeueStrategy.DEFAULT.

**Declared result** NoReturn.

**Local steps**

- If not strategy.
  - Set strategy from DequeueStrategy.DEFAULT.
- Evaluate \_start\_sentry().
- Set redis\_connection from get\_redis\_conn(username = rq\_username, password = rq\_password).
- If queue.
  - Set queue from list of q.strip() for q drawn from queue.split(“,”).
    - Draw q from queue.split(“,”).
- Set queues from get\_queue\_list(queue, build\_queue\_name = true).
- If os.environ.get(“CI”).
  - Evaluate setup\_loghandlers(“ERROR”).
- Evaluate set\_niceness().
- Set logging\_level from “INFO”.
- If quiet.
  - Set logging\_level from “WARNING”.
- Set worker from Worker(queues, connection = redis\_connection).
- Evaluate worker.work(logging\_level = logging\_level, burst = burst, date\_format = “%Y-%m-%d %H:%M:%S”, log\_format = “%(asctime)s,%(msecs)03d %(message)s”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L4752) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1494)

<a id="op-73f58c78234de4"></a>
### Platform Worker.work

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_work`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** super().work(expanded args, expanded names kwargs).

**Local steps**

- Evaluate self.start\_Platform\_scheduler().
- Set kwargs at “with\_scheduler” from false.
- Return super().work(expanded args, expanded names kwargs).

**Methods declared on this owner** [start Platform scheduler](operations-001.md#op-eff1728419209d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5313) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1473)

<a id="op-abca4c8e79678a"></a>
### Platform Worker.run maintenance tasks

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_run_maintenance_tasks`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** super().run\_maintenance\_tasks(expanded args, expanded names kwargs).

**Local steps**

- Evaluate self.start\_Platform\_scheduler().
- Return super().run\_maintenance\_tasks(expanded args, expanded names kwargs).

**Methods declared on this owner** [start Platform scheduler](operations-001.md#op-eff1728419209d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5437) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1471)

<a id="op-eff1728419209d"></a>
### Platform Worker.start Platform scheduler

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_start_foundation_scheduler`

**Inputs** self.

**Local steps**

- Bind dependencies start\_scheduler.
- Evaluate Thread(target = start\_scheduler, daemon = true).start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5541) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1472)

<a id="op-33faf39e27b3ec"></a>
### Platform Worker No Fork.initialize

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Evaluate self.push\_exc\_handler(self.no\_fork\_exception\_handler).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5626) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1467)

<a id="op-63ebf5cd68204f"></a>
### Platform Worker No Fork.work

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_work`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** super().work(expanded args, expanded names kwargs).

**Local steps**

- Set kwargs at “max\_jobs” from (RQ\_MAX\_JOBS + random.randint(0, RQ\_MAX\_JOBS\_JITTER)).
- Return super().work(expanded args, expanded names kwargs).

**Values supplied outside this operation** clock or generated value from random.randint(0, RQ\_MAX\_JOBS\_JITTER).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5736) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1470)

<a id="op-edc67a504cb4d1"></a>
### Platform Worker No Fork.execute job

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_execute_job`

**Inputs** self, job, queue.

**Local steps**

- Evaluate self.prepare\_execution(job).
- Evaluate self.perform\_job(job, queue).
- Evaluate self.set\_state(WorkerStatus.IDLE).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L5867) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1465)

<a id="op-e79b5d657bc6a8"></a>
### Platform Worker No Fork.no fork exception handler

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_number_fork_exception_handler`

**Inputs** self, job, exc\_type, exc\_value, traceback.

**Explicit failure paths** StopRequested.

**Local steps**

- If isinstance(exc\_value, JobTimeoutException).
  - Raise StopRequested.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L6005) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1469)

<a id="op-5e049d8fd4dbf0"></a>
### Platform Worker No Fork.get heartbeat ttl

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_get_heartbeat_time_to_live`

**Inputs** self, job.

**Declared result** int.

**Explicit results** DEFAULT\_WORKER\_TTL · (int((job.timeout or DEFAULT\_WORKER\_TTL)) + 60).

**Local steps**

- If job.timeout equals negative 1.
  - Return DEFAULT\_WORKER\_TTL.
- Otherwise.
  - Return (int((job.timeout or DEFAULT\_WORKER\_TTL)) + 60).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in job.timeout → DEFAULT\_WORKER\_TTL.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L6102) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1466)

<a id="op-39702a47419da3"></a>
### Platform Worker No Fork.kill horse

`operation_foundation_utils_background_jobs_business_behavior_foundation_worker_number_fork_kill_horse`

**Inputs** self, sig = signal.SIGKILL.

**Local steps**

- Evaluate os.kill(os.getpid(), sig).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L6229) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1468)

<a id="op-b756e3dbbe70a2"></a>
### Start worker pool

`operation_foundation_utils_background_jobs_business_behavior_start_worker_pool`

**Inputs** queue = no value, num\_workers = 1, quiet = false, burst = false.

**Declared result** NoReturn.

**Local steps**

- Evaluate \_start\_sentry().
- Bind dependencies filelock.
- Bind dependencies Platform.database.query.
- Bind dependencies Platform.query\_builder.
- Bind dependencies Platform.utils.
- Bind dependencies Platform.utils.safe\_exec.
- Bind dependencies Platform.utils.scheduler.
- Bind dependencies Platform.utils.typing\_validations.
- Bind dependencies Platform.website.path\_resolver.
- Set redis\_connection from get\_redis\_conn().
- If queue.
  - Set queue from list of q.strip() for q drawn from queue.split(“,”).
    - Draw q from queue.split(“,”).
- Set queues from get\_queue\_list(queue, build\_queue\_name = true).
- If os.environ.get(“CI”).
  - Evaluate setup\_loghandlers(“ERROR”).
- Evaluate set\_niceness().
- Set logging\_level from “INFO”.
- If quiet.
  - Set logging\_level from “WARNING”.
- If sbool(os.environ.get(“Platform\_BACKGROUND\_WORKERS\_NOFORK”, false)).
  - Set worker\_klass from PlatformWorkerNoFork.
- Otherwise.
  - Bind dependencies multiprocessing.
  - Evaluate multiprocessing.set\_start\_method(“fork”, force = true).
  - Set worker\_klass from PlatformWorker.
- Set pool from WorkerPool(queues = queues, connection = redis\_connection, num\_workers = num\_workers, worker\_class = worker\_klass).
- Evaluate pool.start(logging\_level = logging\_level, burst = burst).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L6313) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1495)

<a id="op-035783f2fc720d"></a>
### Get worker name

`operation_foundation_utils_background_jobs_business_behavior_get_worker_name`

**Inputs** queue.

**Explicit results** name.

**Local steps**

- Set name from no value.
- If queue.
  - Set name from formatted text {uuid4().hex}.{socket.gethostname()}.{os.getpid()}.{queue}.
- Return name.

**Values supplied outside this operation** clock or generated value from uuid4() · service or queued work from socket.gethostname().

**Boundaries to resolve** external or queued work, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L6947) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1486)

<a id="op-00238b6a030454"></a>
### Get jobs

`operation_foundation_utils_background_jobs_business_behavior_get_jobs`

**Inputs** site = no value, queue = no value, key = “method”.

**Explicit results** jobs\_per\_site.

**Local steps**

- Set jobs\_per\_site from defaultdict(list).
- Bind local operation add\_to\_dict for subsequent calls.
- For each \_queue in get\_queue\_list(queue).
  - Set q from get\_queue(\_queue).
  - Set jobs from (q.jobs + get\_running\_jobs\_in\_queue(q)).
  - For each job in jobs.
    - If not queue\_args bound to get\_queue\_args(job).
      - Continue with the next iteration or loop test.
    - If queue\_args.get(“site”).
      - If (job.kwargs at “site” equals site or site is identical to no value).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in job.kwargs at “site” equals site → site is identical to no value.
        - Evaluate add\_to\_dict(job).
    - Otherwise.
      - Evaluate print(“No site found in job”, job.\_\_dict\_\_).
- Return jobs\_per\_site.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L65) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1479)

<a id="op-8c91b3ac9df7fe"></a>
### Get jobs.add to dict

`operation_foundation_utils_background_jobs_business_behavior_get_jobs_add_to_mapping`

**Inputs** job.

**Local steps**

- If key belongs to job.kwargs.
  - Evaluate jobs\_per\_site at job.kwargs at “site”.append(job.kwargs at key).
- Otherwise.
  - If key belongs to job.kwargs.get(“kwargs”, mapping()).
    - Evaluate jobs\_per\_site at job.kwargs at “site”.append(job.kwargs at “kwargs” at key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0461.json#L7645) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1480)

<a id="op-99754ff6f67f67"></a>
### Get queue list

`operation_foundation_utils_background_jobs_business_behavior_get_queue_list`

**Inputs** queue\_list = no value, build\_queue\_name = false.

**Explicit results** list of generate\_qname(qtype) for qtype drawn from queue\_list when build\_queue\_name, otherwise queue\_list.

**Local steps**

- Set default\_queue\_list from list(get\_queues\_timeout()).
- If queue\_list.
  - If isinstance(queue\_list, str).
    - Set queue\_list from list(queue\_list).
  - For each queue in queue\_list.
    - Evaluate validate\_queue(queue, default\_queue\_list).
- Otherwise.
  - Set queue\_list from default\_queue\_list.
- Return list of generate\_qname(qtype) for qtype drawn from queue\_list when build\_queue\_name, otherwise queue\_list.
  - Value choice on build\_queue\_name — true gives list of generate\_qname(qtype) for qtype drawn from queue\_list, false gives queue\_list.
  - Draw qtype from queue\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1482)

<a id="op-bbc833ca17dd7d"></a>
### Get workers

`operation_foundation_utils_background_jobs_business_behavior_get_workers`

**Inputs** queue = no value.

**Explicit results** Worker.all(queue = queue) · Worker.all(get\_redis\_conn()).

**Local steps**

- If queue.
  - Return Worker.all(queue = queue).
- Otherwise.
  - Return Worker.all(get\_redis\_conn()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L244) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1487)
