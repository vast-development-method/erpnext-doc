# Shared value and file services · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Safe exec

<a id="op-6c11e1432e3b45"></a>
### Validate attribute read

`operation_foundation_utils_safe_exec_business_behavior_validate_attribute_read`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** object, name.

**Locally raised failures** AttributeError, SyntaxError.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L892) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L612)

<a id="op-080478e90cef85"></a>
### Write

`operation_foundation_utils_safe_exec_business_behavior_write`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** obj.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** SyntaxError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L1196) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L616)

<a id="op-627659429b7f44"></a>
### Get module properties

`operation_foundation_utils_safe_exec_business_behavior_get_module_properties`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** module, filter\_method.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L1411) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L567)

## Service · Sbom

<a id="op-a1b76e36e9a6d5"></a>
### Generate sbom

`operation_foundation_binding_foundation_utils_sbom_init_generate_sbom`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with build\_and\_attach\_sbom · msgprint with translated “SBOM generation is already in progress. You will get a notification when it is ready.” · msgprint with translated “SBOM generation started. You will get a notification when it is ready.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set job from Platform.enqueue(build\_and\_attach\_sbom, queue = “long”, job\_id = “generate\_sbom”, deduplicate = true).
- If job is identical to no value.
  - Evaluate Platform.msgprint(translated “SBOM generation is already in progress. You will get a notification when it is ready.”).
- Otherwise.
  - Evaluate Platform.msgprint(translated “SBOM generation started. You will get a notification when it is ready.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · service or queued work from Platform.enqueue(build\_and\_attach\_sbom, queue = “long”, job\_id = “generate\_sbom”, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L234) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L392)

<a id="op-73781ff71a6177"></a>
### Build and attach sbom

`operation_foundation_binding_foundation_utils_sbom_init_build_and_attach_sbom`

**Inputs** no declared parameters.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “attached\_to\_doctype” → ATTACH\_TO, “attached\_to\_name” → ATTACH\_TO, “file\_name” → formatted text sbom-{Platform.local.site}-{now\_datetime()}.spdx.json, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → ATTACH\_TO, “attached\_to\_name” → ATTACH\_TO, “file\_name” → formatted text sbom-{Platform.local.site}-{now\_datetime()}.spdx.json, …)) · rollback · commit.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set document from to\_spdx(collect(Platform.get\_installed\_apps(\_ensure\_on\_bench = true)), Platform.local.site).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → ATTACH\_TO, “attached\_to\_name” → ATTACH\_TO, “file\_name” → formatted text sbom-{nested operand in the contract.local.site}-{now\_datetime() ….
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = translated “SBOM generation failed”).
  - Evaluate \_notify(translated “SBOM generation failed”).
  - Evaluate Platform.db.commit().
  - Return no value.
- Evaluate \_notify(translated “SBOM is ready”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L233) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L391)

<a id="op-b846a6b9183356"></a>
### Notify

`operation_foundation_binding_foundation_utils_sbom_init_notify`

**Inputs** subject.

**Record and data access** read “User” via get\_value.

**Local steps**

- Evaluate make\_notification\_logs(mapping(“type” → “Alert”, “document\_type” → ATTACH\_TO, “document\_name” → ATTACH\_TO, “subject” → subject), list(Platform.db.get\_value(“User”, Platform.session.user, “email”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L235) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L393)

## Service · Scheduler

<a id="op-67a5aea85352d8"></a>
### Cprint

`operation_foundation_utils_scheduler_business_behavior_cprint`

**Inputs** remaining positional values args, remaining named values kwargs.

**Local steps**

- Attempt the following.
  - Evaluate os.get\_terminal\_size().
  - Evaluate print(expanded args, expanded names kwargs).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L1579) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L618)

<a id="op-18d3f498961e5e"></a>
### Start scheduler

`operation_foundation_utils_scheduler_business_behavior_start_scheduler`

**Inputs** no declared parameters.

**Declared result** NoReturn.

**Explicit results** no value.

**Local steps**

- Bind dependencies FileLock, Timeout.
- Set tick from get\_scheduler\_tick().
- Evaluate set\_niceness().
- Set lock\_path from \_get\_scheduler\_lock\_file().
- Attempt the following.
  - Set lock from FileLock(lock\_path).
  - Evaluate lock.acquire(blocking = false).
- On failure (Timeout).
  - Evaluate Platform.logger(“scheduler”).debug(“Scheduler already running”).
  - Return no value.
- While true.
  - Evaluate time.sleep(sleep\_duration(tick)).
  - Evaluate enqueue\_events\_for\_all\_sites().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L72) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L634)

<a id="op-8c6efb2f67c9dc"></a>
### Get scheduler lock file

`operation_foundation_utils_scheduler_business_behavior_get_scheduler_dependency_lock_file`

**Inputs** no declared parameters.

**Declared result** true.

**Explicit results** os.path.abspath(os.path.join(get\_bench\_path(), “config”, “scheduler\_process”)).

**Local steps**

- Return os.path.abspath(os.path.join(get\_bench\_path(), “config”, “scheduler\_process”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L1966) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L626)

<a id="op-5ca85e664c2cef"></a>
### Is schduler process running

`operation_foundation_binding_foundation_utils_scheduler_is_schduler_process_running`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Bind dependencies FileLock, Timeout.
- Attempt the following.
  - Set lock from FileLock(\_get\_scheduler\_lock\_file()).
  - Evaluate lock.acquire(blocking = false).
  - Evaluate lock.release().
  - Return false.
- On failure (Timeout).
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L16) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L409)

<a id="op-902a5f9c3e931b"></a>
### Sleep duration

`operation_foundation_utils_scheduler_business_behavior_sleep_duration`

**Inputs** tick.

**Explicit results** tick · (next\_execution − now).total\_seconds().

**Local steps**

- If tick differs from DEFAULT\_SCHEDULER\_TICK.
  - Return tick.
- Set minutes from (tick floor divide 60).
- Set now from datetime.datetime.now(datetime.UTC).
- Set left\_minutes from (minutes − (now.minute modulo or format minutes)).
- Set next\_execution from (now.replace(second = 0) + datetime.timedelta(minutes = left\_minutes)).
- Return (next\_execution − now).total\_seconds().

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(datetime.UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L71) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L633)

<a id="op-1ab61f20a2a081"></a>
### Enqueue events for all sites

`operation_foundation_utils_scheduler_business_behavior_enqueue_events_for_all_sites`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Within Platform.init\_site().
  - Set sites from get\_sites().
- Evaluate random.shuffle(sites).
- For each site in sites.
  - Attempt the following.
    - Evaluate enqueue\_events\_for\_site(site = site).
  - On failure (Exception).
    - Evaluate Platform.logger(“scheduler”).debug(formatted text Failed to enqueue events for site: {site}, exc\_info = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L70) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L622)

<a id="op-59fc3021b94aa0"></a>
### Enqueue events for site

`operation_foundation_utils_scheduler_business_behavior_enqueue_events_for_site`

**Inputs** site.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Bind local operation log\_exc for subsequent calls.
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - If is\_scheduler\_inactive().
    - Return no value.
  - Evaluate enqueue\_events().
  - Evaluate Platform.logger(“scheduler”).debug(formatted text Queued events for site {site}).
- On failure (Exception) bound to e.
  - If Platform.db.is\_access\_denied(e).
    - Evaluate Platform.logger(“scheduler”).debug(formatted text Access denied for site {site}).
  - Evaluate log\_exc().
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L3062) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L623)

<a id="op-a7cd31282db38c"></a>
### Enqueue events for site.log exc

`operation_foundation_utils_scheduler_business_behavior_enqueue_events_for_site_log_exception`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.logger(“scheduler”).error(formatted text Exception in Enqueue Events for Site {site}, exc\_info = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L3459) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L624)

<a id="op-714e86dc1e3e00"></a>
### Enqueue events

`operation_foundation_utils_scheduler_business_behavior_enqueue_events`

**Inputs** no declared parameters.

**Declared result** (list at str bitwise or no value).

**Record and data access** read “Scheduled Job Type” via get\_all · resolve a document from “Scheduled Job Type” via get\_doc.

**Explicit results** enqueued\_jobs.

**Local steps**

- If schedule\_jobs\_based\_on\_activity().
  - Bind dependencies CroniterBadCronError.
  - Set enqueued\_jobs from list().
  - Set all\_jobs from Platform.get\_all(“Scheduled Job Type”, filters = mapping(“stopped” → 0), fields = “\*”).
  - Evaluate random.shuffle(all\_jobs).
  - For each job\_type in all\_jobs.
    - Set job\_type from Platform.get\_doc(doctype = “Scheduled Job Type”, expanded names job\_type).
    - Attempt the following.
      - If job\_type.enqueue().
        - Evaluate enqueued\_jobs.append(job\_type.method).
    - On failure (CroniterBadCronError).
      - Evaluate Platform.logger(“scheduler”).error(formatted text Invalid Job on {Platform.local.site} - {job\_type.name}, exc\_info = true).
  - Return enqueued\_jobs.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from job\_type.enqueue().

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L69) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L621)

<a id="op-632542438e84ec"></a>
### Is scheduler inactive

`operation_foundation_utils_scheduler_business_behavior_is_scheduler_inactive`

**Inputs** verbose = true.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If Platform.local.conf.maintenance\_mode.
  - If verbose.
    - Evaluate cprint(formatted text {Platform.local.site}: Maintenance mode is ON).
  - Return true.
- If Platform.local.conf.pause\_scheduler.
  - If verbose.
    - Evaluate cprint(formatted text {Platform.local.site}: Platform.conf.pause\_scheduler is SET).
  - Return true.
- If is\_scheduler\_disabled(verbose = verbose).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L3987) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L631)

<a id="op-bf72619709c1db"></a>
### Is scheduler disabled

`operation_foundation_utils_scheduler_business_behavior_is_scheduler_disabled`

**Inputs** verbose = true.

**Declared result** bool.

**Explicit results** true · scheduler\_disabled.

**Local steps**

- If Platform.conf.disable\_scheduler.
  - If verbose.
    - Evaluate cprint(formatted text {Platform.local.site}: Platform.conf.disable\_scheduler is SET).
  - Return true.
- Set scheduler\_disabled from not Platform.get\_system\_settings(“enable\_scheduler”).
- If scheduler\_disabled.
  - If verbose.
    - Evaluate cprint(formatted text {Platform.local.site}: SystemSettings.enable\_scheduler is UNSET).
- Return scheduler\_disabled.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_scheduler”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4240) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L630)

<a id="op-fe9ba2008ec4d9"></a>
### Toggle scheduler

`operation_foundation_utils_scheduler_business_behavior_toggle_scheduler`

**Inputs** enable.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- Evaluate Platform.db.set\_single\_value(“System Settings”, “enable\_scheduler”, int(enable)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4472) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L635)

<a id="op-c0548b62cdbf45"></a>
### Enable scheduler

`operation_foundation_utils_scheduler_business_behavior_enable_scheduler`

**Inputs** no declared parameters.

**Local steps**

- Evaluate toggle\_scheduler(true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4560) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L620)

<a id="op-78716d3030bf6f"></a>
### Disable scheduler

`operation_foundation_utils_scheduler_business_behavior_disable_scheduler`

**Inputs** no declared parameters.

**Local steps**

- Evaluate toggle\_scheduler(false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4604) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L619)

<a id="op-760ab93e101ed7"></a>
### Schedule jobs based on activity

`operation_foundation_utils_scheduler_business_behavior_schedule_jobs_based_on_activity`

**Inputs** check\_time = no value.

**Wrappers, in declaration order** redis\_cache(ttl = (60 × 60)).

**Explicit results** true · false.

**Local steps**

- If is\_dormant(check\_time = check\_time).
  - Set last\_job\_timestamp from \_get\_last\_creation\_timestamp(“Scheduled Job Log”).
  - If not last\_job\_timestamp.
    - Return true.
  - Otherwise.
    - If ((check\_time or now\_datetime()) − last\_job\_timestamp).total\_seconds() ≥ 86400.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in check\_time → now\_datetime().
      - Return true.
    - Otherwise.
      - Return false.
- Otherwise.
  - Return true.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4648) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L632)

<a id="op-64a3854a9eefcc"></a>
### Is dormant

`operation_foundation_utils_scheduler_business_behavior_is_dormant`

**Inputs** check\_time = no value.

**Wrappers, in declaration order** redis\_cache(ttl = (60 × 60)).

**Record and data access** read “User” via get\_value.

**Explicit results** false · true.

**Local steps**

- Bind dependencies on\_Platformcloud.
- If (Platform.conf.developer\_mode or not on\_Platformcloud()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → not on\_Platformcloud().
  - Return false.
- Set threshold from (cint(Platform.get\_system\_settings(“dormant\_days”)) × 86400).
- If not threshold.
  - Return false.
- Set last\_activity from Platform.db.get\_value(“User”, filters = mapping(), fieldname = “last\_active”, order\_by = “last\_active desc”).
- If not last\_activity.
  - Return true.
- If ((check\_time or now\_datetime()) − last\_activity).total\_seconds() ≥ threshold.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in check\_time → now\_datetime().
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“dormant\_days”) · clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L4883) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L629)

<a id="op-e4a6834892182c"></a>
### Get last creation timestamp

`operation_foundation_utils_scheduler_business_behavior_get_last_creation_timestamp`

**Inputs** doctype.

**Record and data access** read doctype via get\_value.

**Explicit results** get\_datetime(timestamp).

**Local steps**

- Set timestamp from Platform.db.get\_value(doctype, filters = mapping(), fieldname = “creation”, order\_by = “creation desc”).
- If timestamp.
  - Return get\_datetime(timestamp).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L5250) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L625)

<a id="op-f0b1a3c0ad63c9"></a>
### Activate scheduler

`operation_foundation_utils_scheduler_business_behavior_activate_scheduler`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — Platform.\_(“Scheduler can not be re-enabled when maintenance mode is active.”).

**Local steps**

- Bind dependencies update\_site\_config.
- Evaluate Platform.only\_for(“Administrator”).
- If Platform.local.conf.maintenance\_mode.
  - Call the validation error handler Platform.throw(Platform.\_(“Scheduler can not be re-enabled when maintenance mode is active.”)).
- If is\_scheduler\_disabled().
  - Evaluate enable\_scheduler().
- If Platform.conf.pause\_scheduler.
  - Evaluate update\_site\_config(“pause\_scheduler”, 0).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“Administrator”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L5379) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L617)
