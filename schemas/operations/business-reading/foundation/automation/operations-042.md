# Workflow, automation and dispatch · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Runner

<a id="op-89978a725a7e9a"></a>
### Traffic.count web

`operation_foundation_runner_business_behavior_traffic_count_web`

**Inputs** self, status.

**Declared result** no value.

**Local steps**

- Within self.\_lock.
  - Set self.last\_web\_request from time.monotonic().
  - If 200 ≤ status &lt; 300.
    - Compare adjacent operands in order, stopping at the first false comparison in 200 ≤ status &lt; 300.
    - Update self.counts at “web” using + 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4691) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L420)

<a id="op-7863140f363365"></a>
### Traffic.idle seconds

`operation_foundation_runner_business_behavior_traffic_idle_seconds`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** (time.monotonic() − self.last\_web\_request).

**Local steps**

- Return (time.monotonic() − self.last\_web\_request).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4835) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L421)

<a id="op-d752b7539f54c7"></a>
### Traffic.summary

`operation_foundation_runner_business_behavior_traffic_summary`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** “, ”.join(generator of formatted text {name} {count} for tuple(name, count) drawn from self.counts.items()).

**Local steps**

- Return “, ”.join(generator of formatted text {name} {count} for tuple(name, count) drawn from self.counts.items()).
  - Draw tuple(name, count) from self.counts.items().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L4903) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L429)

<a id="op-cce565b75900d9"></a>
### Background Jobs.initialize

`operation_foundation_runner_business_behavior_background_jobs_initialize`

**Inputs** self, config, traffic.

**Local steps**

- Set self.threads from list of JobThread(config, traffic, index) for index drawn from range(config.job\_threads).
  - Draw index from range(config.job\_threads).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5033) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L383)

<a id="op-a7b5c19d4d8ed5"></a>
### Background Jobs.start

`operation_foundation_runner_business_behavior_background_jobs_start`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each thread in self.threads.
  - Evaluate thread.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5159) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L384)

<a id="op-8ca7c341a05a2f"></a>
### Background Jobs.stop

`operation_foundation_runner_business_behavior_background_jobs_stop`

**Inputs** self.

**Declared result** no value.

**Local steps**

- For each thread in self.threads.
  - Evaluate thread.stop().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5227) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L385)

<a id="op-c27bd9f6d1b69a"></a>
### Background Jobs.wait

`operation_foundation_runner_business_behavior_background_jobs_wait`

**Inputs** self, timeout.

**Declared result** no value.

**Local steps**

- Set deadline from (time.monotonic() + timeout).
- For each thread in self.threads.
  - Evaluate thread.wait(max(0.0, (deadline − time.monotonic()))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5295) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L386)

<a id="op-cf845a0c0d38a7"></a>
### Job Thread.initialize

`operation_foundation_runner_business_behavior_job_thread_initialize`

**Inputs** self, config, traffic, index.

**Local steps**

- Set self.config from config.
- Set self.traffic from traffic.
- Set self.stopping from threading.Event().
- Set self.worker from no value.
- Set self.thread from threading.Thread(target = self.\_work, name = formatted text rq-worker-{index}, daemon = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5446) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L389)

<a id="op-22b964f44c8ebd"></a>
### Job Thread.start

`operation_foundation_runner_business_behavior_job_thread_start`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.thread.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5667) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L390)

<a id="op-e9612c725a6785"></a>
### Job Thread.stop

`operation_foundation_runner_business_behavior_job_thread_stop`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.stopping.set().
- If self.worker.
  - Evaluate self.worker.stop().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5720) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L391)

<a id="op-bfe0e88d69c2d1"></a>
### Job Thread.wait

`operation_foundation_runner_business_behavior_job_thread_wait`

**Inputs** self, timeout.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not self.thread.is\_alive().
  - Return no value.
- Evaluate self.thread.join(timeout).
- If self.thread.is\_alive().
  - Evaluate logger.warning(“the job continues after %.0fs: the runner stops without it”, timeout).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5809) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L392)

<a id="op-aba7e3f0f7a359"></a>
### Job Thread.work

`operation_foundation_runner_business_behavior_job_thread_work`

**Inputs** self.

**Declared result** no value.

**Local steps**

- While not self.stopping.is\_set().
  - Set queues from get\_queue\_list(self.config.queue\_names, build\_queue\_name = true).
  - Set self.worker from ThreadedWorker(queues, self.traffic, connection = get\_redis\_conn()).
  - Evaluate logger.info(“%s: jobs on %s”, self.thread.name, “, ”.join(generator of q.name for q drawn from self.worker.queues)).
    - Draw q from self.worker.queues.
  - Evaluate self.worker.work(logging\_level = “INFO” when self.config.verbose, otherwise “WARNING”).
    - Value choice on self.config.verbose — true gives “INFO”, false gives “WARNING”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L5965) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L393)

<a id="op-f48322bda9234d"></a>
### Scheduler.initialize

`operation_foundation_runner_business_behavior_scheduler_initialize`

**Inputs** self.

**Local steps**

- Set self.thread from threading.Thread(target = start\_scheduler, name = “scheduler”, daemon = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6268) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L403)

<a id="op-909ca64e04e6fd"></a>
### Scheduler.start

`operation_foundation_runner_business_behavior_scheduler_start`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.thread.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6355) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L404)

<a id="op-b611420f687255"></a>
### Threaded Worker.initialize

`operation_foundation_runner_business_behavior_threaded_worker_initialize`

**Inputs** self, queues, traffic, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(queues, expanded names kwargs).
- Set self.traffic from traffic.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6408) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L413)

<a id="op-aa14a63ed268fb"></a>
### Threaded Worker.stop

`operation_foundation_runner_business_behavior_threaded_worker_stop`

**Inputs** self.

**Local steps**

- Set self.\_stop\_requested from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6519) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L417)

<a id="op-81f7945817d9b6"></a>
### Threaded Worker.execute job

`operation_foundation_runner_business_behavior_threaded_worker_execute_job`

**Inputs** self, job, queue.

**Local steps**

- Within self.traffic.busy().
  - Evaluate super().execute\_job(job, queue).
- Evaluate self.traffic.count(“jobs”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6566) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L412)

<a id="op-c8382427f06c10"></a>
### Threaded Worker.dequeue job and maintain ttl

`operation_foundation_runner_business_behavior_threaded_worker_dequeue_job_and_maintain_time_to_live`

**Inputs** self, timeout, max\_idle\_time = no value.

**Explicit results** job.

**Explicit failure paths** StopRequested.

**Local steps**

- While not self.\_stop\_requested.
  - Set job from super().dequeue\_job\_and\_maintain\_ttl(JOB\_POLL\_SECONDS, JOB\_POLL\_SECONDS).
  - If job.
    - Return job.
- Raise StopRequested.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6704) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L411)

<a id="op-6ccbf56b32d758"></a>
### Threaded Worker.kill horse

`operation_foundation_runner_business_behavior_threaded_worker_kill_horse`

**Inputs** self, sig = no value.

**Local steps**

- Evaluate logger.warning(“kill\_horse ignored: the jobs run on a thread, the job continues”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6839) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L415)

<a id="op-c8dedd83525e55"></a>
### Threaded Worker.start Platform scheduler

`operation_foundation_runner_business_behavior_threaded_worker_start_foundation_scheduler`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6903) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L416)

<a id="op-cd596b093acd88"></a>
### Threaded Worker.install signal handlers

`operation_foundation_runner_business_behavior_threaded_worker_install_signal_handlers`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6936) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L414)

<a id="op-6295a201bfbff6"></a>
### Systemd socket fd

`operation_foundation_binding_foundation_runner_systemd_socket_fd`

**Inputs** no declared parameters.

**Declared result** (int bitwise or no value).

**Explicit results** no value · 3.

**Local steps**

- If (os.environ.get(“LISTEN\_PID”) differs from str(os.getpid()) or os.environ.get(“LISTEN\_FDS”) differs from “1”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“LISTEN\_PID”) differs from str(os.getpid()) → os.environ.get(“LISTEN\_FDS”) differs from “1”.
  - Return no value.
- Return 3.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1708)

<a id="op-d77241b9dc782b"></a>
### Close inherited fds

`operation_foundation_binding_foundation_runner_close_inherited_fds`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- For each name in os.listdir(“/dev/fd”).
  - If (int(name) &gt; 2 and int(name) differs from systemd\_socket\_fd()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in int(name) &gt; 2 → int(name) differs from systemd\_socket\_fd().
    - Within suppress(OSError).
      - Evaluate os.set\_inheritable(int(name), false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1707)

<a id="op-09ac1f1e19f721"></a>
### Runner.initialize

`operation_foundation_runner_business_behavior_runner_initialize`

**Inputs** self, config.

**Local steps**

- Set self.config from config.
- Set self.traffic from Traffic().
- Set self.web from WebServer(config, self.traffic).
- Set self.jobs from BackgroundJobs(config, self.traffic).
- Set self.scheduler from Scheduler().
- Set self.draining from threading.Event().
- Set self.restarting from threading.Event().
- Set self.source from SourceWatch(self.draining) when config.dev, otherwise no value.
  - Value choice on config.dev — true gives SourceWatch(self.draining), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6969) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L401)
