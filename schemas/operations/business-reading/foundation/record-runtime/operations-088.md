# Record lifecycle and persistence · operations 88

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Rq job

<a id="op-9ddaf22349457a"></a>
### Eval filters

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_evaluate_filters`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** filter, values.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4061) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L91)

<a id="op-65536fb85754d7"></a>
### Has filter value

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_has_filter_value`

**Inputs** field\_filter.

**Explicit results** field\_filter · no value.

**Local steps**

- If (field\_filter and field\_filter at 1 does not belong to tuple(no value, empty text)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field\_filter → field\_filter at 1 does not belong to tuple(no value, empty text).
  - Return field\_filter.
- Return no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4217) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L100)

<a id="op-5447457a228486"></a>
### Get job name

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_get_job_name`

**Inputs** job.

**Declared result** str.

**Explicit results** serialize\_job(job).job\_name.

**Local steps**

- Return serialize\_job(job).job\_name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4307) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L98)

<a id="op-45782006156d76"></a>
### Get job status

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_get_job_status`

**Inputs** job.

**Declared result** (str bitwise or no value).

**Explicit results** job.get\_status(refresh = true) · no value.

**Local steps**

- Attempt the following.
  - Return job.get\_status(refresh = true).
- On failure (InvalidJobOperation).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4370) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L99)

<a id="op-19b7c4e47c2cd0"></a>
### Filter job ids by field

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_filter_job_identifiers_by_field`

**Inputs** job\_ids, field\_filter, get\_field\_value.

**Declared result** list at str.

**Explicit results** matched\_ids.

**Local steps**

- Set tuple(operator, operand) from field\_filter.
- Set conn from get\_redis\_conn().
- Set matched\_ids from list().
- For each job in Job.fetch\_many(job\_ids = job\_ids, connection = conn).
  - If not job.
    - Continue with the next iteration or loop test.
  - Set value from get\_field\_value(job).
  - If (value is distinct from no value and compare(value, operator, operand)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → compare(value, operator, operand).
    - Evaluate matched\_ids.append(job.id).
- Return matched\_ids.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4470) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L94)

<a id="op-68c5dc3358d04a"></a>
### Fetch job ids

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_fetch_job_identifiers`

**Inputs** queue, status.

**Declared result** list at str.

**Explicit results** list of j for j drawn from job\_ids where j · list().

**Local steps**

- Set registry\_map from mapping(“queued” → queue, “started” → queue.started\_job\_registry, “finished” → queue.finished\_job\_registry, “failed” → queue.failed\_job\_registry, …).
- Set registry from registry\_map.get(status).
- If registry is distinct from no value.
  - If isinstance(registry, Queue).
    - Set job\_ids from registry.get\_job\_ids().
  - Otherwise.
    - Set job\_ids from registry.get\_job\_ids(cleanup = false).
  - Return list of j for j drawn from job\_ids where j.
    - Draw j from job\_ids, keep a combination only if (j).
- Return list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L4774) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L92)

<a id="op-4ebad0646e8540"></a>
### Remove failed jobs

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_remove_failed_jobs`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- For each queue in get\_queues().
  - Set fail\_registry from queue.failed\_job\_registry.
  - Set failed\_jobs from filter\_current\_site\_jobs(fail\_registry.get\_job\_ids(cleanup = false)).
  - Set conn from get\_redis\_conn().
  - For each job\_ids in create\_batch(failed\_jobs, 100).
    - For each job in Job.fetch\_many(job\_ids = job\_ids, connection = conn).
      - Evaluate (job and fail\_registry.remove(job, delete\_job = true)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in job → fail\_registry.remove(job, delete\_job = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L5125) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L101)

<a id="op-be821d69352354"></a>
### Get all queued jobs

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_get_all_queued_jobs`

**Inputs** no declared parameters.

**Explicit results** list of job for job drawn from jobs where for\_current\_site(job).

**Local steps**

- Set jobs from list().
- For each q in get\_queues().
  - Evaluate jobs.extend(q.get\_jobs()).
- Return list of job for job drawn from jobs where for\_current\_site(job).
  - Draw job from jobs, keep a combination only if (for\_current\_site(job)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L5424) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L96)

<a id="op-63ad8857bc08be"></a>
### Stop job

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_stop_job`

**Inputs** job\_id.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “RQ Job” via get\_doc.

**Local steps**

- Evaluate Platform.get\_doc(“RQ Job”, job\_id).stop\_job().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L5563) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L103)

<a id="op-444d21dff4b9a8"></a>
### Get custom queues

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_get_custom_queues`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list((Platform.conf.workers or mapping()).keys()).

**Local steps**

- Evaluate Platform.has\_permission(“RQ Job”, throw = true).
- Return list((Platform.conf.workers or mapping()).keys()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.workers → mapping().

**Values supplied outside this operation** effective access from Platform.has\_permission(“RQ Job”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L5661) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L97)

## Record · Rq worker

<a id="op-91174092ac420b"></a>
### RQWorker.load from db

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_load_from_database`

**Inputs** self.

**Explicit failure paths** Platform.DoesNotExistError.

**Local steps**

- Set all\_workers from get\_workers().
- Set workers from list of w for w drawn from all\_workers where w.name equals self.name.
  - Draw w from all\_workers, keep a combination only if (w.name equals self.name).
- If not workers.
  - Raise Platform.DoesNotExistError.
- Set d from serialize\_worker(workers at 0).
- Evaluate self.init\_from\_dict(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L107) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L128)

<a id="op-948e357b15d257"></a>
### RQWorker.get list

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_get_list`

**Inputs** start = 0, page\_length = 0.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of serialize\_worker(worker) for worker drawn from valid\_workers.

**Local steps**

- Set workers from get\_workers().
- Set valid\_workers from list of w for w drawn from workers where w.pid.
  - Draw w from workers, keep a combination only if (w.pid).
- If page\_length.
  - Set valid\_workers from valid\_workers at slice start to (start + page\_length).
- Otherwise.
  - Set valid\_workers from valid\_workers at slice start to no value.
- Return list of serialize\_worker(worker) for worker drawn from valid\_workers.
  - Draw worker from valid\_workers.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L3922) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L126)

<a id="op-3f596ac080aa64"></a>
### RQWorker.get count

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_get_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Declared result** int.

**Explicit results** len(get\_workers()).

**Local steps**

- Return len(get\_workers()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4154) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L125)

<a id="op-9fb11c58a8a7a7"></a>
### RQWorker.get stats

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_get_stats`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping().

**Local steps**

- Return mapping().

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4213) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L127)

<a id="op-f1d6bec159853f"></a>
### RQWorker.db insert

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4247) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L122)

<a id="op-4faccfb1d50a39"></a>
### RQWorker.db update

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4290) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L123)

<a id="op-18f14b574de168"></a>
### RQWorker.delete

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_background_queue_worker_delete`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4333) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L124)

<a id="op-b3f6415d9a588a"></a>
### Serialize worker

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_serialize_worker`

**Inputs** worker.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(name = worker.name, queue = queue, queue\_type = queue\_types, worker\_name = worker.name, …).

**Local steps**

- Set queue\_names from worker.queue\_names().
- Set queue from “, ”.join(queue\_names).
- Set queue\_types from “,”.join(generator of q.rsplit(“:”, 1) at 1 for q drawn from queue\_names).
  - Draw q from queue\_names.
- Set current\_job from worker.get\_current\_job\_id().
- If (current\_job and not current\_job.startswith(formatted text {Platform.local.site}\|\|)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_job → not current\_job.startswith(formatted text {Platform.local.site}\|\|).
  - Set current\_job from no value.
- Return Platform.\_dict(name = worker.name, queue = queue, queue\_type = queue\_types, worker\_name = worker.name, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L108) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L130)

<a id="op-1b71fa85f6e0d6"></a>
### Compute utilization

`operation_foundation_core_record_definitions_queued_work_worker_business_behavior_compute_utilization`

**Inputs** worker.

**Declared result** float.

**Explicit results** ((worker.total\_working\_time ÷ total\_time) × 100).

**Local steps**

- Within suppress(Exception).
  - Set total\_time from (datetime.datetime.now(datetime.UTC) − worker.birth\_date.replace(tzinfo = datetime.UTC)).total\_seconds().
  - Return ((worker.total\_working\_time ÷ total\_time) × 100).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(datetime.UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L4902) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L129)

## Record · Scheduled job log

[Record definition](../../../../data/record-types/scheduled_job_log.json)

<a id="op-9dd733d10b28f2"></a>
### Scheduled Job Log.clear old logs

`operation_foundation_core_record_definitions_scheduled_job_log_business_behavior_scheduled_job_log_clear_old_logs`

**Inputs** days = 90.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Set table from Platform.qb.DocType(“Scheduled Job Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L5344) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L466)

## Record · Scheduled job type

[Record definition](../../../../data/record-types/scheduled_job_type.json)

<a id="op-a7391a505191a2"></a>
### Scheduled Job Type.validate

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cron format is required for job types with Cron frequency.” · validation helper — translated “{0} is not a valid Cron expression.”.format(formatted text &lt;code&gt;{self.cron\_format}&lt;/code&gt;).

**Local steps**

- If self.frequency does not belong to tuple(“All”, “Cron”).
  - Set self.create\_log from 1.
- If self.frequency equals “Cron”.
  - If not self.cron\_format.
    - Call the validation error handler Platform.throw(translated “Cron format is required for job types with Cron frequency.”).
  - Attempt the following.
    - Evaluate croniter(self.cron\_format).
  - On failure (CroniterBadCronError).
    - Call the validation error handler Platform.throw(translated “{0} is not a valid Cron expression.”.format(formatted text &lt;code&gt;{self.cron\_format}&lt;/code&gt;), title = translated “Bad Cron Expression”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L32) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L487)

<a id="op-3cfb0a96c4e950"></a>
### Scheduled Job Type.enqueue

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_enqueue`

**Inputs** self, force = false.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If (self.is\_event\_due() or force).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_event\_due() → force.
  - If not self.is\_job\_in\_queue().
    - Evaluate enqueue(“Platform.core.doctype.scheduled\_job\_type.scheduled\_job\_type.run\_scheduled\_job”, queue = self.get\_queue\_name(), job\_type = self.method, job\_id = self.rq\_job\_id, scheduled\_job\_type = self.name).
    - Return true.
  - Otherwise.
    - Evaluate Platform.logger(“scheduler”).error(formatted text Skipped queueing {self.method} because it was found in queue for {Platform.local.site}).
- Return false.

**Methods declared on this owner** [is event due](operations-088.md#op-fb3fdbb9758e2a), [is job in queue](operations-088.md#op-b097e2089e3566), [get queue name](operations-089.md#op-72fd0d2e44c329).

**Values supplied outside this operation** service or queued work from enqueue(“Platform.core.doctype.scheduled\_job\_type.scheduled\_job\_type.run\_scheduled\_job”, queue = self.get\_queue\_name(), job\_type = self.method, job\_id = self.rq\_job\_id, scheduled\_job\_type = self.name).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L28) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L477)

<a id="op-fb3fdbb9758e2a"></a>
### Scheduled Job Type.is event due

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_is_event_due`

**Inputs** self, current\_time = no value.

**Explicit results** self.get\_next\_execution() ≤ (current\_time or now\_datetime()).

**Local steps**

- Return self.get\_next\_execution() ≤ (current\_time or now\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_time → now\_datetime().

**Methods declared on this owner** [get next execution](operations-089.md#op-9261b694052885).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L6344) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L481)

<a id="op-b097e2089e3566"></a>
### Scheduled Job Type.is job in queue

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_is_job_in_queue`

**Inputs** self.

**Declared result** bool.

**Explicit results** is\_job\_enqueued(self.rq\_job\_id).

**Local steps**

- Return is\_job\_enqueued(self.rq\_job\_id).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L6436) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L482)
