# Record lifecycle and persistence · operations 87

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Role permission for page and report

[Record definition](../../../../data/record-types/role_permission_for_page_and_report.json)

<a id="op-84c3b0ad11ae9d"></a>
### Role Permissionfor Pageand Report.update disable prepared report

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_update_disable_prepared_report`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4533) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L452)

<a id="op-cf9bb7ea0a7851"></a>
### Role Permissionfor Pageand Report.get args

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_get_arguments`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, row.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4666) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L445)

<a id="op-d919d96e02051c"></a>
### Role Permissionfor Pageand Report.get roles

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_get_roles`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4827) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L276) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L446)

<a id="op-b6d3e43e6ab99a"></a>
### Role Permissionfor Pageand Report.update status

`operation_foundation_core_record_definitions_role_permission_for_page_and_report_business_behavior_role_permissionfor_pageand_report_update_status`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4949) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L454)

## Record · Role profile

[Record definition](../../../../data/record-types/role_profile.json)

<a id="op-f64533c0d492d0"></a>
### Role Profile.autoname

`operation_foundation_core_record_definitions_role_profile_business_behavior_role_profile_autoname`

**Inputs** self.

**Local steps**

- Set self.name from self.role\_profile.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L4990) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L455)

<a id="op-cad972806aa7f2"></a>
### Role Profile.on update

`operation_foundation_core_record_definitions_role_profile_business_behavior_role_profile_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().
- Evaluate self.queue\_action(“update\_all\_users”, now = (Platform.in\_test or Platform.flags.in\_install), enqueue\_after\_commit = true, queue = “long”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.flags.in\_install.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L5043) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L457)

<a id="op-aa603346be1328"></a>
### Role Profile.update all users

`operation_foundation_core_record_definitions_role_profile_business_behavior_role_profile_update_all_users`

**Inputs** self.

**Record and data access** read “User Role Profile” via get\_all · resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set users from Platform.get\_all(“User Role Profile”, filters = mapping(“role\_profile” → self.name), pluck = “parent”).
- For each user in users.
  - Set user from Platform.get\_doc(“User”, user).
  - Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L5165) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L458)

<a id="op-612795b421c89e"></a>
### Role Profile.get permission log options

`operation_foundation_core_record_definitions_role_profile_business_behavior_role_profile_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0100.json#L5351) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L456)

## Record · Rq job

<a id="op-8547dc00c11df1"></a>
### Check permissions

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_check_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** method.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L517) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L89)

<a id="op-afa2a553983131"></a>
### Check permissions.wrapper

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_check_permissions_wrapper`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** args, kwargs.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L721) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L90)

<a id="op-74b00b3b9f5bfd"></a>
### RQJob.load from db

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_load_from_database`

**Inputs** self.

**Explicit failure paths** Platform.DoesNotExistError · Platform.PermissionError.

**Local steps**

- Attempt the following.
  - Set job from Job.fetch(self.name, connection = get\_redis\_conn()).
- On failure (NoSuchJobError).
  - Raise Platform.DoesNotExistError.
- If not for\_current\_site(job).
  - Raise Platform.PermissionError.
- Evaluate self.init\_from\_dict(serialize\_job(job)).
- Set self.\_job\_obj from job.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L103) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L87)

<a id="op-f1f47f908c345c"></a>
### RQJob.job

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_job`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.\_job\_obj.

**Local steps**

- Return self.\_job\_obj.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L1137) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L86)

<a id="op-d2717981d2335b"></a>
### RQJob.get list

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_get_list`

**Inputs** filters = no value, start = 0, page\_length = 20, order\_by = “creation desc”, fields = no value, as\_list = false, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of list of job.get(f) when isinstance(f, str), otherwise no value for f drawn from fields for job drawn from jobs · jobs.

**Local steps**

- Set matched\_job\_ids from RQJob.get\_matching\_job\_ids(filters = filters).
- Set conn from get\_redis\_conn().
- Set jobs from list of serialize\_job(job) for job drawn from Job.fetch\_many(job\_ids = matched\_job\_ids, connection = conn) where job.
  - Draw job from Job.fetch\_many(job\_ids = matched\_job\_ids, connection = conn), keep a combination only if (job).
- Set order\_desc from “desc” belongs to order\_by.
- Set jobs from sorted(jobs, key = deferred anonymous expression, reverse = order\_desc).
- Set jobs from jobs at slice start to (start + page\_length).
- If as\_list.
  - Set fields from (fields or list(“name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → list(“name”).
  - Return list of list of job.get(f) when isinstance(f, str), otherwise no value for f drawn from fields for job drawn from jobs.
    - Draw job from jobs.
    - Draw f from fields.
    - Value choice on isinstance(f, str) — true gives job.get(f), false gives no value.
- Return jobs.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L1183) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L83)

<a id="op-884771d75567d3"></a>
### RQJob.get matching job ids

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_get_matching_job_identifiers`

**Inputs** filters.

**Wrappers, in declaration order** staticmethod.

**Declared result** list at str.

**Explicit results** matched\_job\_ids at slice no value to MAX\_MATCHED\_JOBS.

**Local steps**

- Set filters from make\_filter\_dict((filters or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Set queues from \_eval\_filters(filters.get(“queue”), (QUEUES + get\_custom\_queues())).
- Set status\_filter from has\_filter\_value(filters.get(“status”)).
- Set job\_name\_filter from has\_filter\_value(filters.get(“job\_name”)).
- Set name\_filter from has\_filter\_value(filters.get(“name”)).
- Set matched\_job\_ids from list().
- For each queue in get\_queues().
  - If not queue.name.endswith(tuple(queues)).
    - Continue with the next iteration or loop test.
  - For each status in JOB\_STATUSES.
    - Evaluate matched\_job\_ids.extend(fetch\_job\_ids(queue, status)).
- Set matched\_job\_ids from list(dict.fromkeys(filter\_current\_site\_jobs(matched\_job\_ids))).
- Set matched\_job\_ids from \_eval\_filters(name\_filter, matched\_job\_ids).
- If job\_name\_filter.
  - Set matched\_job\_ids from filter\_job\_ids\_by\_field(matched\_job\_ids, job\_name\_filter, get\_job\_name).
- If status\_filter.
  - Set matched\_job\_ids from filter\_job\_ids\_by\_field(matched\_job\_ids, status\_filter, get\_job\_status).
- Return matched\_job\_ids at slice no value to MAX\_MATCHED\_JOBS.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L102) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L84)

<a id="op-930b429d8a10ca"></a>
### RQJob.delete

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_delete`

**Inputs** self.

**Wrappers, in declaration order** check\_permissions.

**Local steps**

- Evaluate self.job.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2327) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L81)

<a id="op-b971687417a979"></a>
### RQJob.stop job

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_stop_job`

**Inputs** self.

**Wrappers, in declaration order** check\_permissions.

**State and service calls** msgprint with translated “Job is not running.”.

**Local steps**

- Attempt the following.
  - Evaluate send\_stop\_job\_command(connection = get\_redis\_conn(), job\_id = self.job\_id).
- On failure (InvalidJobOperation).
  - Evaluate Platform.msgprint(translated “Job is not running.”, title = translated “Invalid Operation”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2385) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L88)

<a id="op-6f9b24a1440f5b"></a>
### RQJob.cancel

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_cancel`

**Inputs** self.

**Wrappers, in declaration order** check\_permissions.

**State and service calls** call cancel on self.job · msgprint with translated “Job is in {0} state and can't be cancelled”.format(self.status).

**Local steps**

- If self.status equals “queued”.
  - Evaluate self.job.cancel().
- Otherwise.
  - Evaluate Platform.msgprint(translated “Job is in {0} state and can't be cancelled”.format(self.status), title = translated “Invalid Operation”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2551) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L78)

<a id="op-ccfd8674f40782"></a>
### RQJob.get count

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_get_count`

**Inputs** filters = no value.

**Wrappers, in declaration order** staticmethod.

**Declared result** int.

**Explicit results** len(RQJob.get\_matching\_job\_ids(filters)).

**Local steps**

- Return len(RQJob.get\_matching\_job\_ids(filters)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2720) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L82)

<a id="op-19d7a14e4f3128"></a>
### RQJob.get stats

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_get_stats`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping().

**Local steps**

- Return mapping().

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2799) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L85)

<a id="op-a9f50ec4c0c551"></a>
### RQJob.db insert

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2833) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L79)

<a id="op-12d9bcfa38d257"></a>
### RQJob.db update

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_background_queue_job_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0101.json#L2876) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L80)

<a id="op-42eb78d09eea77"></a>
### Serialize job

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_serialize_job`

**Inputs** job.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(name = job.id, job\_id = job.id, queue = job.origin.rsplit(“:”, 1) at 1, job\_name = job\_name, …).

**Local steps**

- Set modified from (job.last\_heartbeat or job.ended\_at or job.started\_at or job.created\_at).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job.last\_heartbeat → job.ended\_at → job.started\_at → job.created\_at.
- Set queue\_args from get\_queue\_args(job).
- Set job\_kwargs from queue\_args.get(“kwargs”, mapping()).
- Set job\_name from (job\_kwargs.get(“job\_type”) or str(queue\_args.get(“job\_name”, job.description))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_kwargs.get(“job\_type”) → str(queue\_args.get(“job\_name”, job.description)).
- If job\_name equals “Platform.utils.background\_jobs.run\_doc\_method”.
  - Set doctype from job\_kwargs.get(“doctype”).
  - Set doc\_method from job\_kwargs.get(“doc\_method”).
  - If (doctype and doc\_method).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → doc\_method.
    - Set job\_name from formatted text {doctype}.{doc\_method}.
- If matches bound to re.match(text in the contract, job\_name).
  - Set job\_name from matches.group(“func\_name”).
- Set exc\_info from no value.
- If job\_result bound to job.latest\_result().
  - Set exc\_info from job\_result.exc\_string.
- Return Platform.\_dict(name = job.id, job\_id = job.id, queue = job.origin.rsplit(“:”, 1) at 1, job\_name = job\_name, …).
  - Value choice on job.started\_at — true gives convert\_utc\_to\_system\_timezone(job.started\_at), false gives empty text.
  - Value choice on job.ended\_at — true gives convert\_utc\_to\_system\_timezone(job.ended\_at), false gives empty text.
  - Value choice on job.ended\_at — true gives (job.ended\_at − job.started\_at).total\_seconds(), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L106) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L102)

<a id="op-be3bf47d5faae4"></a>
### For current site

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_for_current_site`

**Inputs** job.

**Declared result** bool.

**Explicit results** job.id.startswith(formatted text {Platform.local.site}\|\|).

**Local steps**

- Return job.id.startswith(formatted text {Platform.local.site}\|\|).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L105) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L95)

<a id="op-54cb02081ef15b"></a>
### Filter current site jobs

`operation_foundation_core_record_definitions_queued_work_job_business_behavior_filter_current_site_jobs`

**Inputs** job\_ids.

**Declared result** list at str.

**Explicit results** list of j for j drawn from job\_ids where j.startswith(formatted text {site}\|\|).

**Local steps**

- Set site from Platform.local.site.
- Return list of j for j drawn from job\_ids where j.startswith(formatted text {site}\|\|).
  - Draw j from job\_ids, keep a combination only if (j.startswith(formatted text {site}\|\|)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L104) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L93)
