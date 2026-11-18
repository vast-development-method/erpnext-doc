# Forms, reports and navigation · operations 74

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · System console

[Record definition](../../../../data/record-types/system_console.json)

<a id="op-55bfb490989343"></a>
### Execute code

`operation_foundation_desk_record_definitions_system_console_business_behavior_execute_code`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L35) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1188)

<a id="op-e058b9e8d28036"></a>
### Show processlist

`operation_foundation_desk_record_definitions_system_console_business_behavior_show_processlist`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L717) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1189)

<a id="op-5ebaa2b38bd113"></a>
### Show processlist

`operation_foundation_desk_record_definitions_system_console_business_behavior_show_processlist_2`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a structured result, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L799) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1190)

## Record · System health report

[Record definition](../../../../data/record-types/system_health_report.json)

<a id="op-db70d020d54e38"></a>
### No wait

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_number_wait`

**Inputs** func.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Bind dependencies stop\_after\_attempt.
- Attempt the following.
  - Set original\_stop from func.retry.stop.
  - Set func.retry.stop from stop\_after\_attempt(1).
  - yield no value.
- On exit, including pending return or failure.
  - Set func.retry.stop from original\_stop.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L2044) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1201)

<a id="op-6d1c4b17fa9f83"></a>
### Health check

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_health_check`

**Inputs** step.

**Explicit results** suppress\_exception.

**Local steps**

- Require isinstance(step, str) or report “Invalid usage of decorator, Usage: @health\_check('step name')”.
- Bind local operation suppress\_exception for subsequent calls.
- Return suppress\_exception.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L2184) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1198)

<a id="op-759725297114d6"></a>
### Health check.suppress exception

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_health_check_suppress_exception`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L2533) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1199)

<a id="op-e6bddf2e6e6566"></a>
### Health check.suppress exception.wrapper

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_health_check_suppress_exception_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(func).

**State and service calls** msgprint with formatted text System Health check step {Platform.bold(step)} failed: {e}.

**Explicit results** func(expanded args, expanded names kwargs).

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Return func(expanded args, expanded names kwargs).
- On failure (Exception) bound to e.
  - If Platform.in\_test.
    - Propagate the active failure.
  - Evaluate Platform.log(Platform.get\_traceback()).
  - Evaluate Platform.msgprint(formatted text System Health check step {Platform.bold(step)} failed: {e}, alert = true, indicator = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L2825) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1200)

<a id="op-34a88261ceda55"></a>
### System Health Report.db insert

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L3291) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1202)

<a id="op-b0fe7750a16279"></a>
### System Health Report.load from db

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_load_from_database`

**Inputs** self.

**Local steps**

- Evaluate self.init\_from\_dict(mapping()).
- Evaluate Platform.only\_for(“System Manager”).
- Evaluate self.fetch\_background\_jobs().
- Evaluate self.fetch\_scheduler().
- Evaluate self.fetch\_email\_stats().
- Evaluate self.fetch\_errors().
- Evaluate self.fetch\_database\_details().
- Evaluate self.fetch\_cache\_details().
- Evaluate self.fetch\_storage\_details().
- Evaluate self.fetch\_user\_stats().

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch background jobs](operations-074.md#op-520956ad1eb129), [fetch scheduler](operations-074.md#op-2e4e5efd68f80e), [fetch email stats](operations-074.md#op-52464144168408), [fetch errors](operations-074.md#op-aa5383658fc0dc), [fetch database details](operations-074.md#op-29877faddf9b54), [fetch cache details](operations-074.md#op-251f68d322906f), [fetch storage details](operations-074.md#op-d68671fc3b1a44), [fetch user stats](operations-074.md#op-a449c81c62c5be).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L38) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1216)

<a id="op-520956ad1eb129"></a>
### System Health Report.fetch background jobs

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_background_jobs`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Background Jobs”), no\_wait(get\_redis\_conn).

**Record and data access** read “RQ Worker” via get\_all.

**State and service calls** enqueue with “Platform.ping”.

**Local steps**

- Set self.background\_jobs\_check from “failed”.
- Set self.test\_job\_id from Platform.enqueue(“Platform.ping”, at\_front = true).id.
- Set self.background\_jobs\_check from “queued”.
- Set workers from Platform.get\_all(“RQ Worker”).
- Set self.total\_background\_workers from len(workers).
- Set queue\_summary from defaultdict(list).
- For each worker in workers.
  - Evaluate queue\_summary at worker.queue\_type.append(worker).
- For each tuple(queue\_type, workers) in queue\_summary.items().
  - Evaluate self.append(“background\_workers”, mapping(“count” → len(workers), “queues” → queue\_type, “failed\_jobs” → sum(generator of w.failed\_job\_count for w drawn from workers), “utilization” → (sum(generator of w.u ….
    - Draw w from workers.
    - Draw w from workers.
- For each queue in get\_queue\_list().
  - Set q from get\_queue(queue).
  - Evaluate self.append(“queue\_status”, mapping(“queue” → queue, “pending\_jobs” → q.count)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.ping”, at\_front = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L3599) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1205)

<a id="op-2e4e5efd68f80e"></a>
### System Health Report.fetch scheduler

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_scheduler`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Scheduler”).

**Record and data access** read “Scheduled Job Type” via get\_all · resolve a document from “Scheduled Job Type” via get\_doc.

**Local steps**

- Set scheduler\_enabled from get\_scheduler\_status().get(“status”) equals “active”.
- If not is\_schduler\_process\_running().
  - Set self.scheduler\_status from “Process Not Found”.
- Otherwise.
  - If is\_dormant().
    - Set self.scheduler\_status from “Dormant”.
  - Otherwise.
    - If scheduler\_enabled.
      - Set self.scheduler\_status from “Active”.
    - Otherwise.
      - Set self.scheduler\_status from “Inactive”.
- Set lower\_threshold from add\_to\_date(no value, days = negative 7, as\_datetime = true).
- Set upper\_threshold from add\_to\_date(no value, minutes = negative 30, as\_datetime = true).
- Set query from query text (SELECT, Scheduled Job Log).
- Set postgres\_query from query text (SELECT, Scheduled Job Log).
- Set failing\_jobs from Platform.db.multisql(mapping(“postgres” → postgres\_query, “\*” → query), mapping(“lower\_threshold” → lower\_threshold, “upper\_threshold” → upper\_threshold), as\_dict = true).
- For each job in failing\_jobs.
  - Evaluate self.append(“failing\_scheduled\_jobs”, job).
- Set threshold from add\_to\_date(no value, seconds = (negative 30 × get\_scheduler\_tick()), as\_datetime = true).
- For each job\_type in Platform.get\_all(“Scheduled Job Type”, filters = mapping(“stopped” → 0, “last\_execution” → tuple(“&lt;”, threshold)), fields = “\*”, order\_by = “last\_execution asc”).
  - Set job\_type from Platform.get\_doc(doctype = “Scheduled Job Type”, expanded names job\_type).
  - If job\_type.is\_event\_due().
    - Set self.oldest\_unscheduled\_job from job\_type.name.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L37) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1210)

<a id="op-52464144168408"></a>
### System Health Report.fetch email stats

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_email_stats`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Emails”).

**Record and data access** read “Email Queue” via count · read “Unhandled Email” via count · read “Communication” via count.

**Local steps**

- Set threshold from add\_to\_date(no value, days = negative 7, as\_datetime = true).
- Set filters from mapping(“creation” → tuple(“&gt;”, threshold), “modified” → tuple(“&gt;”, threshold)).
- Set self.total\_outgoing\_emails from Platform.db.count(“Email Queue”, filters).
- Set self.pending\_emails from Platform.db.count(“Email Queue”, mapping(“status” → “Not Sent”, expand filters)).
- Set self.failed\_emails from Platform.db.count(“Email Queue”, mapping(“status” → “Error”, expand filters)).
- Set self.unhandled\_emails from Platform.db.count(“Unhandled Email”, filters).
- Set self.handled\_emails from Platform.db.count(“Communication”, mapping(“sent\_or\_received” → “Received”, “communication\_type” → “Communication”, expand filters)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L5241) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1208)

<a id="op-aa5383658fc0dc"></a>
### System Health Report.fetch errors

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_errors`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Errors”).

**Record and data access** read “Error Log” via count · execute query text (SELECT, Error Log).

**Local steps**

- Set threshold from add\_to\_date(no value, days = negative 1, as\_datetime = true).
- Set filters from mapping(“creation” → tuple(“&gt;”, threshold), “modified” → tuple(“&gt;”, threshold)).
- Set self.total\_errors from Platform.db.count(“Error Log”, filters).
- Set top\_errors from Platform.db.sql(query text (SELECT, Error Log), mapping(“threshold” → threshold), as\_dict = true).
- For each row in top\_errors.
  - Evaluate self.append(“top\_errors”, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L5731) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1209)

<a id="op-29877faddf9b54"></a>
### System Health Report.fetch database details

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_database_details`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Database”).

**State and service calls** execute a supplied database query.

**Local steps**

- Bind dependencies db\_report.
- Set tuple(\_cols, data) from db\_report().
- Set self.database from Platform.db.db\_type.
- Set self.db\_storage\_usage from sum(generator of (table.size or 0.0) for table drawn from data).
  - Draw table from data.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in table.size → 0.0.
- For each row in data at slice no value to 5.
  - Evaluate self.append(“top\_db\_tables”, row).
- If Platform.db.db\_type equals “sqlite”.
  - Set self.database\_version from Platform.db.sql(“select sqlite\_version()”) at 0 at 0.
- Otherwise.
  - Set self.database\_version from Platform.db.sql(“select version()”) at 0 at 0.
- If Platform.db.db\_type equals “mariadb”.
  - Set self.bufferpool\_size from Platform.db.sql(“show variables like 'innodb\_buffer\_pool\_size'”) at 0 at 1.
  - Set self.binary\_logging from Platform.db.sql(“show variables like 'log\_bin'”) at 0 at 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L6148) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1207)

<a id="op-251f68d322906f"></a>
### System Health Report.fetch cache details

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_cache_details`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Cache”).

**Local steps**

- Set self.cache\_keys from len(Platform.cache.get\_keys(empty text)).
- Set self.cache\_memory\_usage from Platform.cache.execute\_command(“INFO”, “MEMORY”).get(“used\_memory\_human”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L6651) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1206)

<a id="op-d68671fc3b1a44"></a>
### System Health Report.fetch storage details

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_storage_details`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Storage”).

**Local steps**

- Bind dependencies get\_context.
- Set self.backups\_size from (get\_directory\_size(“private”, “backups”) ÷ (1024 × 1024)).
- Set self.private\_files\_size from (get\_directory\_size(“private”, “files”) ÷ (1024 × 1024)).
- Set self.public\_files\_size from (get\_directory\_size(“public”, “files”) ÷ (1024 × 1024)).
- Set self.onsite\_backups from len(get\_context(Platform.\_dict()).get(“files”, list())).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L6808) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1211)

<a id="op-a449c81c62c5be"></a>
### System Health Report.fetch user stats

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_fetch_user_stats`

**Inputs** self.

**Wrappers, in declaration order** health\_check(“Users”).

**Record and data access** read “User” via count · read “Activity Log” via count · read “Sessions” via count · read “User” via get\_all.

**Local steps**

- Set threshold from add\_to\_date(no value, days = negative 30, as\_datetime = true).
- Set self.total\_users from Platform.db.count(“User”, mapping(“enabled” → 1)).
- Set self.new\_users from Platform.db.count(“User”, mapping(“enabled” → 1, “creation” → tuple(“&gt;”, threshold))).
- Set self.failed\_logins from Platform.db.count(“Activity Log”, mapping(“operation” → “login”, “status” → “Failed”, “creation” → tuple(“&gt;”, threshold), “modified” → tuple(“&gt;”, threshold))).
- Set self.active\_sessions from Platform.db.count(“Sessions”).
- Set self.last\_10\_active\_users from whitespace '\\n'.join(Platform.get\_all(“User”, mapping(“enabled” → 1), order\_by = “last\_active desc”, limit = 10, pluck = “name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L7107) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1212)

<a id="op-707c7c0274481e"></a>
### System Health Report.db update

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_database_update`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L7629) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1203)

<a id="op-ab33e679feb5fb"></a>
### System Health Report.delete

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_delete`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L7671) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1204)

<a id="op-1646317fc5cb7b"></a>
### System Health Report.get list

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_get_list`

**Inputs** filters = no value, page\_length = 20, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0189.json#L7713) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1214)

<a id="op-1f084a6d217ddb"></a>
### System Health Report.get count

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_get_count`

**Inputs** filters = no value, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1213)

<a id="op-3ae0574b81350c"></a>
### System Health Report.get stats

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_system_health_report_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L61) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1215)

<a id="op-f5d748141edfe7"></a>
### Get job status

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_get_job_status`

**Inputs** job\_id = no value.

**Wrappers, in declaration order** Platform.whitelist(), no\_wait(get\_redis\_conn).

**Record and data access** resolve a document from “RQ Job” via get\_doc.

**Explicit results** Platform.get\_doc(“RQ Job”, job\_id).status.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Attempt the following.
  - Return Platform.get\_doc(“RQ Job”, job\_id).status.
- On failure (Exception).
  - Evaluate Platform.clear\_messages().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1197)

<a id="op-1cddac027a0b68"></a>
### Get directory size

`operation_foundation_desk_record_definitions_system_health_report_business_behavior_get_directory_size`

**Inputs** remaining positional values path.

**Wrappers, in declaration order** redis\_cache(ttl = (5 × 60)).

**Explicit results** \_get\_directory\_size(expanded path).

**Local steps**

- Return \_get\_directory\_size(expanded path).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L291) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1195)
