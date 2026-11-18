# Shared value and file services · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Background jobs

<a id="op-7a9019bc197a4e"></a>
### Get running jobs in queue

`operation_foundation_utils_background_jobs_business_behavior_get_running_jobs_in_queue`

**Inputs** queue.

**Explicit results** jobs.

**Local steps**

- Set jobs from list().
- Set workers from get\_workers(queue).
- For each worker in workers.
  - Set current\_job from worker.get\_current\_job().
  - If current\_job.
    - Evaluate jobs.append(current\_job).
- Return jobs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L349) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1485)

<a id="op-86703da85b50b0"></a>
### Get queue args

`operation_foundation_binding_foundation_utils_background_jobs_get_queue_args`

**Inputs** job.

**Declared result** dict.

**Explicit results** job.kwargs · mapping().

**Local steps**

- Attempt the following.
  - Return job.kwargs.
- On failure (DeserializationError).
  - Return mapping().

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L52) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L210)

<a id="op-f9201303cb39e1"></a>
### Get queue

`operation_foundation_utils_background_jobs_business_behavior_get_queue`

**Inputs** qtype, is\_async = true.

**Declared result** Queue.

**Explicit results** Queue(generate\_qname(qtype), connection = get\_redis\_conn(), is\_async = is\_async).

**Local steps**

- Evaluate validate\_queue(qtype).
- Return Queue(generate\_qname(qtype), connection = get\_redis\_conn(), is\_async = is\_async).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L500) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1481)

<a id="op-29836e47bfbbf5"></a>
### Validate queue

`operation_foundation_utils_background_jobs_business_behavior_validate_queue`

**Inputs** queue, default\_queue\_list = no value.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Queue should be one of {0}”.format(“, ”.join(default\_queue\_list)).

**Local steps**

- If not default\_queue\_list.
  - Set default\_queue\_list from list(get\_queues\_timeout()).
- If queue does not belong to default\_queue\_list.
  - Call the validation error handler Platform.throw(translated “Queue should be one of {0}”.format(“, ”.join(default\_queue\_list))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L637) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1498)

<a id="op-b9f454ff119890"></a>
### Get redis conn

`operation_foundation_utils_background_jobs_business_behavior_get_cache_service_conn`

**Inputs** username = no value, password = no value.

**Wrappers, in declaration order** retry(retry = retry\_if\_exception\_type(tuple(BusyLoadingError, ConnectionError)), stop = stop\_after\_attempt(5), wait = wait\_fixed(1), reraise = true).

**Explicit results** get\_redis\_connection\_without\_auth() · RedisQueue.get\_connection(expanded names cred).

**Explicit failure paths** Exception(“redis\_queue missing in common\_site\_config.json”) · propagate active failure.

**Local steps**

- Set conf from Platform.get\_conf().
- If not conf.redis\_queue.
  - Raise Exception(“redis\_queue missing in common\_site\_config.json”).
- Use module bindings \_redis\_queue\_conn.
- Set cred from Platform.\_dict().
- If conf.get(“use\_rq\_auth”).
  - If username.
    - Set cred at “username” from username.
    - Set cred at “password” from password.
  - Otherwise.
    - Set cred at “username” from (conf.rq\_username or get\_bench\_id()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.rq\_username → get\_bench\_id().
    - Set cred at “password” from conf.rq\_password.
- Otherwise.
  - If os.environ.get(“RQ\_ADMIN\_PASWORD”).
    - Set cred at “username” from “default”.
    - Set cred at “password” from os.environ.get(“RQ\_ADMIN\_PASWORD”).
- Attempt the following.
  - If not cred.
    - Return get\_redis\_connection\_without\_auth().
  - Otherwise.
    - Return RedisQueue.get\_connection(expanded names cred).
- On failure (redis.exceptions.AuthenticationError).
  - Evaluate log(formatted text Wrong credentials used for {(cred.username or “default user”)}. You can reset credentials using ′bench create-rq-users′ CLI and restart the server, colour = “red”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cred.username → “default user”.
  - Propagate the active failure.
- On failure (Exception) bound to e.
  - Evaluate log(formatted text Please make sure that Redis Queue runs @ {Platform.get\_conf().redis\_queue}. Redis reported error: {e}, colour = “red”).
  - Propagate the active failure.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L836) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1475)

<a id="op-f7a47a14fe1d8c"></a>
### Get redis connection without auth

`operation_foundation_utils_background_jobs_business_behavior_get_cache_service_connection_without_authentication`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L1601) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1476)

<a id="op-a15cf7d3f8c793"></a>
### Get queues

`operation_foundation_utils_background_jobs_business_behavior_get_queues`

**Inputs** connection = no value.

**Declared result** list at Queue.

**Explicit results** list of q for q drawn from queues where is\_queue\_accessible(q).

**Local steps**

- Set queues from Queue.all(connection = (connection or get\_redis\_conn())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in connection → get\_redis\_conn().
- Return list of q for q drawn from queues where is\_queue\_accessible(q).
  - Draw q from queues, keep a combination only if (is\_queue\_accessible(q)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L1676) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1483)

<a id="op-1b67910ed87aaa"></a>
### Generate qname

`operation_foundation_utils_background_jobs_business_behavior_generate_qname`

**Inputs** qtype.

**Declared result** str.

**Explicit results** formatted text {get\_bench\_id()}:{qtype}.

**Local steps**

- If isinstance(qtype, list).
  - Set qtype from “,”.join(qtype).
- Return formatted text {get\_bench\_id()}:{qtype}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L1820) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1474)

<a id="op-5b2026502a69b1"></a>
### Is queue accessible

`operation_foundation_utils_background_jobs_business_behavior_is_queue_accessible`

**Inputs** qobj.

**Declared result** bool.

**Explicit results** qobj.name belongs to accessible\_queues.

**Local steps**

- Set accessible\_queues from list of generate\_qname(q) for q drawn from list(get\_queues\_timeout()).
  - Draw q from list(get\_queues\_timeout()).
- Return qobj.name belongs to accessible\_queues.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L1957) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1489)

<a id="op-038e6b6a2fd2ed"></a>
### Enqueue test job

`operation_foundation_utils_background_jobs_business_behavior_enqueue_test_job`

**Inputs** no declared parameters.

**Local steps**

- Evaluate enqueue(“Platform.utils.background\_jobs.test\_job”, s = 100).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(“Platform.utils.background\_jobs.test\_job”, s = 100).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2087) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1463)

<a id="op-414af23f01a62c"></a>
### Test job

`operation_foundation_utils_background_jobs_business_behavior_test_job`

**Inputs** s.

**Local steps**

- Bind dependencies time.
- Evaluate print(“sleeping...”).
- Evaluate time.sleep(s).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2186) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1496)

<a id="op-555aa7e3d6df86"></a>
### Create job id

`operation_foundation_utils_background_jobs_business_behavior_create_job_identifier`

**Inputs** job\_id = no value.

**Declared result** str.

**Explicit results** formatted text {Platform.local.site}\|\|{job\_id}.

**Local steps**

- If not job\_id.
  - Set job\_id from str(uuid4()).
- Otherwise.
  - Set job\_id from job\_id.replace(“:”, “\|”).
- Return formatted text {Platform.local.site}\|\|{job\_id}.

**Values supplied outside this operation** clock or generated value from uuid4().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L62) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1459)

<a id="op-a03e67b69c988f"></a>
### Is job enqueued

`operation_foundation_utils_background_jobs_business_behavior_is_job_enqueued`

**Inputs** job\_id.

**Declared result** bool.

**Explicit results** get\_job\_status(job\_id) belongs to tuple(JobStatus.QUEUED, JobStatus.STARTED).

**Local steps**

- Return get\_job\_status(job\_id) belongs to tuple(JobStatus.QUEUED, JobStatus.STARTED).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2514) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1488)

<a id="op-fbe290fb714abb"></a>
### Get job status

`operation_foundation_utils_background_jobs_business_behavior_get_job_status`

**Inputs** job\_id.

**Declared result** (JobStatus bitwise or no value).

**Explicit results** job.get\_status(refresh = false).

**Local steps**

- If job bound to get\_job(job\_id).
  - Return job.get\_status(refresh = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2602) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1478)

<a id="op-aeef01dc163209"></a>
### Get job

`operation_foundation_utils_background_jobs_business_behavior_get_job`

**Inputs** job\_id.

**Declared result** (Job bitwise or no value).

**Explicit results** Job.fetch(create\_job\_id(job\_id), connection = get\_redis\_conn()) · no value.

**Local steps**

- Attempt the following.
  - Return Job.fetch(create\_job\_id(job\_id), connection = get\_redis\_conn()).
- On failure (tuple(NoSuchJobError, InvalidJobOperation)).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2708) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1477)

<a id="op-46e926bebc3a99"></a>
### Set niceness

`operation_foundation_utils_background_jobs_business_behavior_set_niceness`

**Inputs** no declared parameters.

**Local steps**

- Set conf from Platform.get\_conf().
- Set nice\_increment from BACKGROUND\_PROCESS\_NICENESS.
- Set configured\_niceness from conf.get(“background\_process\_niceness”).
- If configured\_niceness is distinct from no value.
  - Set nice\_increment from cint(configured\_niceness).
- Evaluate os.nice(nice\_increment).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L2846) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1491)

<a id="op-f38b3eafb9ff97"></a>
### Truncate failed registry

`operation_foundation_utils_background_jobs_business_behavior_truncate_failed_registry`

**Inputs** job, connection, type, value, traceback.

**Local steps**

- Bind dependencies create\_batch.
- Set conf from Platform.conf when Platform.conf, otherwise Platform.get\_conf(site = get\_queue\_args(job).get(“site”)).
  - Value choice on Platform.conf — true gives Platform.conf, false gives Platform.get\_conf(site = get\_queue\_args(job).get(“site”)).
- Set limit from ((conf.get(“rq\_failed\_jobs\_limit”) or RQ\_FAILED\_JOBS\_LIMIT) − 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“rq\_failed\_jobs\_limit”) → RQ\_FAILED\_JOBS\_LIMIT.
- For each queue in get\_queues(connection = connection).
  - Set fail\_registry from queue.failed\_job\_registry.
  - Set failed\_jobs from fail\_registry.get\_job\_ids() at slice limit to no value.
  - For each job\_ids in create\_batch(failed\_jobs, 100).
    - For each job\_obj in Job.fetch\_many(job\_ids = job\_ids, connection = connection).
      - Evaluate (job\_obj and fail\_registry.remove(job\_obj, delete\_job = true)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_obj → fail\_registry.remove(job\_obj, delete\_job = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L68) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1497)

<a id="op-c2e6f9922b44a6"></a>
### Check queue size

`operation_foundation_utils_background_jobs_business_behavior_check_queue_size`

**Inputs** q.

**Explicit failure paths** validation helper with Platform.QueueOverloaded — translated “Too many queued background jobs ({0}). Please retry after some time.”.format(max\_jobs).

**Local steps**

- Set max\_jobs from (cint(Platform.conf.max\_queued\_jobs) or MAX\_QUEUED\_JOBS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.max\_queued\_jobs) → MAX\_QUEUED\_JOBS.
- Update max\_jobs using + (\_site\_count() × 50).
- If cint(q.count) ≥ max\_jobs.
  - Set primary\_action from mapping(“label” → “Monitor System Health”, “client\_action” → “Platform.set\_route”, “args” → list(“Form”, “System Health Report”)).
  - Call the validation error handler Platform.throw(translated “Too many queued background jobs ({0}). Please retry after some time.”.format(max\_jobs), title = translated “Queue Overloaded”, exc = Platform.QueueOverloaded, primary\_action = pr ….
    - Value choice on Platform.has\_permission(“System Health Report”) — true gives primary\_action, false gives no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“System Health Report”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L3408) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1458)

<a id="op-198d4c392384e8"></a>
### Site count

`operation_foundation_utils_background_jobs_business_behavior_site_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** site\_cache(ttl = (10 × 60)).

**Declared result** int.

**Explicit results** len(get\_sites()).

**Local steps**

- Return len(get\_sites()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L3782) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1492)

<a id="op-f6dede54e0ef33"></a>
### Start sentry

`operation_foundation_utils_background_jobs_business_behavior_start_sentry`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set sentry\_dsn from os.getenv(“Platform\_SENTRY\_DSN”).
- If not sentry\_dsn.
  - Return no value.
- Bind dependencies sentry\_sdk.
- Bind dependencies ArgvIntegration.
- Bind dependencies AtexitIntegration.
- Bind dependencies DedupeIntegration.
- Bind dependencies ExcepthookIntegration.
- Bind dependencies ModulesIntegration.
- Bind dependencies PlatformIntegration, before\_send.
- Set integrations from list(AtexitIntegration(), ExcepthookIntegration(), DedupeIntegration(), ModulesIntegration(), …).
- Set experiments from mapping().
- Set kwargs from mapping().
- If os.getenv(“ENABLE\_SENTRY\_DB\_MONITORING”).
  - Evaluate integrations.append(PlatformIntegration()).
  - Set experiments at “record\_sql\_params” from true.
- If tracing\_sample\_rate bound to os.getenv(“SENTRY\_TRACING\_SAMPLE\_RATE”).
  - Set kwargs at “traces\_sample\_rate” from float(tracing\_sample\_rate).
- If profiling\_sample\_rate bound to os.getenv(“SENTRY\_PROFILING\_SAMPLE\_RATE”).
  - Set kwargs at “profiles\_sample\_rate” from float(profiling\_sample\_rate).
- Evaluate sentry\_sdk.init(dsn = sentry\_dsn, before\_send = before\_send, attach\_stacktrace = true, release = Platform.\_\_version\_\_, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L67) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1493)

## Service · Backups

<a id="op-66b20ec45d7bb1"></a>
### Backup Generator.initialize

`operation_foundation_utils_backups_business_behavior_backup_generator_initialize`

**Inputs** self, db\_name, user, password, backup\_path = no value, backup\_path\_db = no value, backup\_path\_files = no value, backup\_path\_private\_files = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_type = no value, backup\_path\_conf = no value, ignore\_conf = false, compress\_files = false, include\_doctypes = empty text, exclude\_doctypes = empty text, verbose = false, old\_backup\_metadata = false, rollback\_callback = no value.

**Local steps**

- Use module bindings \_verbose.
- Set self.compress\_files from (compress\_files or compress).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in compress\_files → compress.
- Set self.db\_socket from db\_socket.
- Set self.db\_host from db\_host.
- Set self.db\_port from db\_port.
- Set self.db\_name from db\_name.
- Set self.db\_type from db\_type.
- Set self.user from user.
- Set self.password from password.
- Set self.backup\_path from backup\_path.
- Set self.backup\_path\_conf from backup\_path\_conf.
- Set self.backup\_path\_db from backup\_path\_db.
- Set self.backup\_path\_files from backup\_path\_files.
- Set self.backup\_path\_private\_files from backup\_path\_private\_files.
- Set self.ignore\_conf from ignore\_conf.
- Set self.include\_doctypes from include\_doctypes.
- Set self.exclude\_doctypes from exclude\_doctypes.
- Set self.partial from false.
- Set self.old\_backup\_metadata from old\_backup\_metadata.
- Set self.rollback\_callback from rollback\_callback.
- Set site from (Platform.local.site or Platform.generate\_hash(length = 8)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.site → Platform.generate\_hash(length = 8).
- Set self.site\_slug from site.replace(“.”, “\_”).
- Set self.verbose from verbose.
- Evaluate self.setup\_backup\_directory().
- Evaluate self.setup\_backup\_tables().
- Set \_verbose from verbose.

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup backup directory](operations-002.md#op-c122c2b214fad8), [setup backup tables](operations-002.md#op-b1e01f3f61b394).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 8).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L5164) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1511)

<a id="op-c122c2b214fad8"></a>
### Backup Generator.setup backup directory

`operation_foundation_utils_backups_business_behavior_backup_generator_setup_backup_directory`

**Inputs** self.

**Local steps**

- Set specified from (self.backup\_path or self.backup\_path\_db or self.backup\_path\_files or self.backup\_path\_private\_files or self.backup\_path\_conf).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.backup\_path → self.backup\_path\_db → self.backup\_path\_files → self.backup\_path\_private\_files → self.backup\_path\_conf.
- If not specified.
  - Set backups\_folder from get\_backup\_path().
  - If not os.path.exists(backups\_folder).
    - Evaluate os.makedirs(backups\_folder, exist\_ok = true).
- Otherwise.
  - If self.backup\_path.
    - Evaluate os.makedirs(self.backup\_path, exist\_ok = true).
  - For each file\_path in set(self.backup\_path\_files, self.backup\_path\_db, self.backup\_path\_private\_files, self.backup\_path\_conf).
    - If file\_path.
      - Set dir from os.path.dirname(file\_path).
      - Evaluate os.makedirs(dir, exist\_ok = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L5882) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1517)

<a id="op-32ad6fc863aefc"></a>
### Backup Generator.set existing tables

`operation_foundation_utils_backups_business_behavior_backup_generator_set_existing_tables`

**Inputs** self.

**Local steps**

- If not hasattr(self, “\_existing\_tables”).
  - Set self.\_existing\_tables from Platform.db.get\_tables().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L6246) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1516)

<a id="op-b1e01f3f61b394"></a>
### Backup Generator.setup backup tables

`operation_foundation_utils_backups_business_behavior_backup_generator_setup_backup_tables`

**Inputs** self.

**Local steps**

- Evaluate self.\_set\_existing\_tables().
- Set self.backup\_includes from \_get\_tables(self.include\_doctypes.strip().split(“,”), self.\_existing\_tables).
- Set self.backup\_excludes from \_get\_tables(self.exclude\_doctypes.strip().split(“,”), self.\_existing\_tables).
- Evaluate self.set\_backup\_tables\_from\_config().
- Set self.partial from ((self.backup\_includes or self.backup\_excludes) and not self.ignore\_conf).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.backup\_includes or self.backup\_excludes) → not self.ignore\_conf.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.backup\_includes → self.backup\_excludes.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set existing tables](operations-002.md#op-32ad6fc863aefc), [set backup tables from config](operations-003.md#op-2d77169fb4b560).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0462.json#L6339) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1518)
