# Record lifecycle and persistence · operations 89

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Scheduled job type

[Record definition](../../../../data/record-types/scheduled_job_type.json)

<a id="op-8511d105409ca8"></a>
### Scheduled Job Type.rq job id

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_background_queue_job_identifier`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** formatted text scheduled\_job\|\|{self.name}.

**Local steps**

- Return formatted text scheduled\_job\|\|{self.name}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L6494) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L476)

<a id="op-736ed4b9d82840"></a>
### Scheduled Job Type.next execution

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_next_execution`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.get\_next\_execution().

**Local steps**

- Return self.get\_next\_execution().

**Methods declared on this owner** [get next execution](operations-089.md#op-9261b694052885).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0102.json#L6558) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L484)

<a id="op-9261b694052885"></a>
### Scheduled Job Type.get next execution

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_get_next_execution`

**Inputs** self.

**Explicit results** next\_execution.

**Local steps**

- Set maintenance\_offset from (int(hashlib.sha1(nested operand in the contract.encode()).hexdigest(), 16) modulo or format 60).
- Set CRON\_MAP from mapping(“Yearly” → “0 0 1 1 \*”, “Annual” → “0 0 1 1 \*”, “Monthly” → “0 0 1 \* \*”, “Monthly Long” → “0 0 1 \* \*”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_conf().scheduler\_interval → 240.
- If not self.cron\_format.
  - Set self.cron\_format from CRON\_MAP.get(self.frequency).
- Set last\_execution from get\_datetime((self.last\_execution or self.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.last\_execution → self.creation.
- If self.frequency equals “Hourly Maintenance”.
  - Update last\_execution using − timedelta(minutes = maintenance\_offset).
- Set next\_execution from parse\_cron(self.cron\_format).get\_next(datetime, start\_time = last\_execution).
- If self.frequency belongs to tuple(“Hourly Maintenance”, “Daily Maintenance”).
  - Update next\_execution using + timedelta(minutes = maintenance\_offset).
- Return next\_execution.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L30) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L479)

<a id="op-6c63dbae1d698b"></a>
### Scheduled Job Type.execute

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_execute`

**Inputs** self.

**Record and data access** read “Server Script” via get\_value · resolve a document from “Server Script” via get\_doc.

**State and service calls** commit · rollback.

**Local steps**

- If Platform.job.
  - Set Platform.job.frequency from self.frequency.
  - Set Platform.job.cron\_format from self.cron\_format.
- Set self.scheduler\_log from no value.
- Attempt the following.
  - Evaluate self.log\_status(“Start”).
  - If self.server\_script.
    - Set script\_name from Platform.db.get\_value(“Server Script”, self.server\_script).
    - If script\_name.
      - Evaluate Platform.get\_doc(“Server Script”, script\_name).execute\_scheduled\_method().
  - Otherwise.
    - Evaluate Platform.get\_attr(self.method)().
  - Evaluate Platform.db.commit().
  - Evaluate self.log\_status(“Complete”).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate self.log\_status(“Failed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [log status](operations-089.md#op-18a8807e05f2cb).

**Values supplied outside this operation** selected callable from Platform.get\_attr(self.method).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L29) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L478)

<a id="op-18a8807e05f2cb"></a>
### Scheduled Job Type.log status

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_log_status`

**Inputs** self, status.

**Local steps**

- Evaluate Platform.logger(“scheduler”).info(formatted text Scheduled Job {status}: {self.method} for {Platform.local.site}).
- Evaluate self.update\_scheduler\_log(status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update scheduler log](operations-089.md#op-2012eb56785851).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L429) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L483)

<a id="op-2012eb56785851"></a>
### Scheduled Job Type.update scheduler log

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_update_scheduler_log`

**Inputs** self, status.

**Record and data access** resolve a document from “Scheduled Job Log” via get\_doc.

**State and service calls** call db\_set on self · commit · call insert on Platform.get\_doc(doctype = “Scheduled Job Log”, scheduled\_job\_type = self.name) · call db\_set on self.scheduler\_log.

**Explicit results** no value.

**Local steps**

- If not self.create\_log.
  - Evaluate self.db\_set(“last\_execution”, now\_datetime(), update\_modified = false).
  - Evaluate Platform.db.commit().
  - Return no value.
- If not self.scheduler\_log.
  - Set self.scheduler\_log from Platform.get\_doc(doctype = “Scheduled Job Log”, scheduled\_job\_type = self.name).insert(ignore\_permissions = true).
- Evaluate self.scheduler\_log.db\_set(“status”, status).
- If Platform.debug\_log.
  - Evaluate self.scheduler\_log.db\_set(“debug\_log”, whitespace '\\n'.join(Platform.debug\_log)).
- If status equals “Failed”.
  - Evaluate self.scheduler\_log.db\_set(“details”, Platform.get\_traceback(with\_context = true)).
- If status equals “Start”.
  - Evaluate self.db\_set(“last\_execution”, now\_datetime(), update\_modified = false).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L592) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L486)

<a id="op-72fd0d2e44c329"></a>
### Scheduled Job Type.get queue name

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_get_queue_name`

**Inputs** self.

**Explicit results** “long” when (“Long” belongs to self.frequency or “Maintenance” belongs to self.frequency), otherwise “default”.

**Local steps**

- Return “long” when (“Long” belongs to self.frequency or “Maintenance” belongs to self.frequency), otherwise “default”.
  - Value choice on (“Long” belongs to self.frequency or “Maintenance” belongs to self.frequency) — true gives “long”, false gives “default”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “Long” belongs to self.frequency → “Maintenance” belongs to self.frequency.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L31) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L480)

<a id="op-8766d899068446"></a>
### Scheduled Job Type.on trash

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_scheduled_job_type_on_trash`

**Inputs** self.

**State and service calls** request delete on “Scheduled Job Log”.

**Local steps**

- Evaluate Platform.db.delete(“Scheduled Job Log”, mapping(“scheduled\_job\_type” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L1220) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L485)

<a id="op-04659d735f4b59"></a>
### Execute event

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_execute_event`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**Explicit results** doc.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set doc from json.loads(doc).
- Evaluate Platform.get\_doc(“Scheduled Job Type”, doc.get(“name”)).enqueue(force = true).
- Return doc.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L27) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L469)

<a id="op-a3bc0245ea1584"></a>
### Skip next execution

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_skip_next_execution`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.save().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set doc from json.loads(doc).
- Set doc from Platform.get\_doc(“Scheduled Job Type”, doc.get(“name”)).
- Set doc.last\_execution from doc.next\_execution.
- Return doc.save().

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L33) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L488)

<a id="op-299c32addd0eb9"></a>
### Run scheduled job

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_run_scheduled_job`

**Inputs** scheduled\_job\_type, job\_type = no value.

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**Explicit failure paths** Platform.InReadOnlyMode(“Scheduled jobs can't run in maintenance mode.”).

**Local steps**

- If Platform.conf.maintenance\_mode.
  - Raise Platform.InReadOnlyMode(“Scheduled jobs can't run in maintenance mode.”).
- Attempt the following.
  - Evaluate Platform.get\_doc(“Scheduled Job Type”, scheduled\_job\_type).execute().
- On failure (Exception).
  - Evaluate print(Platform.get\_traceback()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L1782) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L475)

<a id="op-f002a221827b1e"></a>
### Sync jobs

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_sync_jobs`

**Inputs** hooks = no value.

**Local steps**

- Evaluate Platform.reload\_doc(“core”, “doctype”, “scheduled\_job\_type”).
- Set scheduler\_events from (hooks or Platform.get\_hooks(“scheduler\_events”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks → Platform.get\_hooks(“scheduler\_events”).
- Evaluate insert\_events(scheduler\_events).
- Evaluate clear\_events(scheduler\_events).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“scheduler\_events”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L34) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L489)

<a id="op-8f520cd6a03de0"></a>
### Insert events

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_insert_events`

**Inputs** scheduler\_events.

**Declared result** list.

**Explicit results** (cron\_jobs + event\_jobs).

**Local steps**

- Set tuple(cron\_jobs, event\_jobs) from tuple(list(), list()).
- For each event\_type in scheduler\_events.
  - Set events from scheduler\_events.get(event\_type).
  - If isinstance(events, dict).
    - Update cron\_jobs using + insert\_cron\_jobs(events).
  - Otherwise.
    - Update event\_jobs using + insert\_event\_jobs(events, event\_type).
- Return (cron\_jobs + event\_jobs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L2372) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L471)

<a id="op-c23d1de28e09ee"></a>
### Insert cron jobs

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_insert_schedule_jobs`

**Inputs** events.

**Declared result** list.

**Explicit results** cron\_jobs.

**Local steps**

- Set cron\_jobs from list().
- For each cron\_format in events.
  - For each event in events.get(cron\_format).
    - Evaluate cron\_jobs.append(event).
    - Evaluate insert\_single\_event(“Cron”, event, cron\_format).
- Return cron\_jobs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L2584) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L472)

<a id="op-85cb67a7dc3e5e"></a>
### Insert event jobs

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_insert_event_jobs`

**Inputs** events, event\_type.

**Declared result** list.

**Explicit results** event\_jobs.

**Local steps**

- Set event\_jobs from list().
- For each event in events.
  - Evaluate event\_jobs.append(event).
  - Set frequency from event\_type.replace(“\_”, one space).title().
  - Evaluate insert\_single\_event(frequency, event).
- Return event\_jobs.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L2741) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L470)

<a id="op-b9182dc6cea50c"></a>
### Insert single event

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_insert_single_event`

**Inputs** frequency, event, cron\_format = empty text.

**Record and data access** read “Scheduled Job Type” via exists · resolve a document from “Scheduled Job Type” via get\_doc · resolve a document from mapping(“doctype” → “Scheduled Job Type”, “method” → event, “cron\_format” → cron\_format, “frequency” → frequency) via get\_doc.

**State and service calls** call save on doc · savepoint savepoint · call insert on doc · rollback.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Evaluate Platform.get\_attr(event).
- On failure (Exception) bound to e.
  - Evaluate click.secho(formatted text {event} is not a valid method: {e}, fg = “yellow”).
  - Return no value.
- If job\_name bound to Platform.db.exists(“Scheduled Job Type”, mapping(“method” → event)).
  - Set doc from Platform.get\_doc(“Scheduled Job Type”, job\_name).
  - If (doc.frequency differs from frequency or doc.cron\_format differs from cron\_format).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.frequency differs from frequency → doc.cron\_format differs from cron\_format.
    - Set doc.cron\_format from cron\_format.
    - Set doc.frequency from frequency.
    - Evaluate doc.save().
- Otherwise.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “method” → event, “cron\_format” → cron\_format, “frequency” → frequency)).
  - Set savepoint from “scheduled\_job\_type\_creation”.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Evaluate doc.insert().
  - On failure (Platform.UniqueValidationError).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate doc.delete().
    - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(event).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L2919) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L473)

<a id="op-eca0974c7f6344"></a>
### Clear events

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_clear_events`

**Inputs** scheduler\_events.

**Record and data access** read “Scheduled Job Type” via get\_all.

**State and service calls** request delete\_doc for “Scheduled Job Type”.

**Local steps**

- Bind local operation event\_exists for subsequent calls.
- For each event in Platform.get\_all(“Scheduled Job Type”, fields = list(“\*”)).
  - If not event\_exists(event).
    - Evaluate Platform.delete\_doc(“Scheduled Job Type”, event.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L3570) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L467)

<a id="op-0a22e640d86c5f"></a>
### Clear events.event exists

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_clear_events_event_exists`

**Inputs** event.

**Declared result** bool.

**Explicit results** true · event.method belongs to scheduler\_events.get(freq, mapping()).get(event.cron\_format, list()) · event.method belongs to scheduler\_events.get(freq, list()).

**Local steps**

- If event.server\_script.
  - Return true.
- If event.scheduler\_event.
  - Return true.
- Set freq from Platform.scrub(event.frequency).
- If freq equals “cron”.
  - Return event.method belongs to scheduler\_events.get(freq, mapping()).get(event.cron\_format, list()).
- Otherwise.
  - Return event.method belongs to scheduler\_events.get(freq, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L3956) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L468)

<a id="op-3ab05418c07091"></a>
### On doctype update

`operation_foundation_core_record_definitions_scheduled_job_type_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Scheduled Job Type”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Scheduled Job Type”, list(“frequency”, “cron\_format”, “method”), constraint\_name = “unique\_scheduled\_job”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0103.json#L4532) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L474)

## Service · Schema

<a id="op-587688700aeb31"></a>
### Duck DBColumn.get definition

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_column_get_definition`

**Inputs** self, for\_modification = false.

**Explicit results** column\_def.

**Local steps**

- Set column\_def from get\_definition(self.fieldtype, precision = self.precision, length = self.length, options = self.options, duckdb = true).
- If not column\_def.
  - Return column\_def.
- Set null from true.
- Set default from no value.
- Set unique from false.
- If self.fieldtype belongs to NOT\_NULL\_TYPES.
  - Set null from false.
- If self.fieldtype belongs to tuple(“Check”, “Int”).
  - Set default from cint(self.default).
- Otherwise.
  - If self.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
    - Set default from flt(self.default).
  - Otherwise.
    - If (self.default and self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS and not cstr(self.default).startswith(“:”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default → self.default does not belong to Platform.db.DEFAULT\_SHORTCUTS → not cstr(self.default).startswith(“:”).
      - Set default from Platform.db.escape(self.default).
- If (self.not\_nullable and null).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.not\_nullable → null.
  - If default is identical to no value.
    - Set default from get\_not\_null\_defaults(self.fieldtype).
    - If isinstance(default, str).
      - Set default from Platform.db.escape(default).
  - Set null from false.
- If (self.unique and not for\_modification and column\_def does not belong to tuple(“text”, “longtext”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.unique → not for\_modification → column\_def does not belong to tuple(“text”, “longtext”).
  - Set unique from true.
- If not null.
  - Update column\_def using + “ NOT NULL”.
- If default is distinct from no value.
  - Update column\_def using + formatted text  DEFAULT {default}.
- If unique.
  - Update column\_def using + “ UNIQUE”.
- Return column\_def.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L4432) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1135)

<a id="op-1c9af7dc400d67"></a>
### Duck DBTable.is new

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_is_new`

**Inputs** self, conn.

**Explicit results** self.table\_name does not belong to tables.

**Local steps**

- Set tables from list of x at 0 for x drawn from conn.sql(“show tables”).fetchall().
  - Draw x from conn.sql(“show tables”).fetchall().
- Return self.table\_name does not belong to tables.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L5242) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1143)

<a id="op-8f71f3fbb51f29"></a>
### Duck DBTable.sync

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_sync`

**Inputs** self, conn.

**Explicit results** no value.

**Local steps**

- If self.meta.get(“is\_virtual”).
  - Return no value.
- If self.is\_new(conn).
  - Evaluate self.create(conn).
- Otherwise.
  - Return no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-089.md#op-1c9af7dc400d67), [create](operations-090.md#op-34f23fa39924a0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L5368) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1144)

<a id="op-15d1e09be6af15"></a>
### Duck DBTable.get column definitions

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_column_definitions`

**Inputs** self.

**Explicit results** ret.

**Local steps**

- Set column\_list from list(expanded Platform.db.DEFAULT\_COLUMNS).
- Set ret from list().
- For each k in list(self.columns).
  - If k does not belong to column\_list.
    - Set d from self.columns at k.get\_definition().
    - If d.
      - Evaluate ret.append((((“"” + k) + “" ”) + d)).
      - Evaluate column\_list.append(k).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L5508) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1140)

<a id="op-8aa644e3032fad"></a>
### Duck DBTable.get all column definitions

`operation_foundation_database_duckdb_schema_business_behavior_duck_database_table_get_all_column_definitions`

**Inputs** self.

**Explicit results** fields.

**Local steps**

- Set fields from list().
- Set varchar\_len from Platform.db.VARCHAR\_LEN.
- Evaluate fields.extend(list(formatted text "name" varchar({varchar\_len}), “"creation" datetime(6)”, “"modified" datetime(6)”, formatted text "modified\_by" varchar({varchar\_len}), …)).
- Evaluate fields.extend(self.get\_column\_definitions()).
- If self.meta.get(“istable”, default = 0).
  - Evaluate fields.extend(list(formatted text "parent" varchar({varchar\_len}), formatted text "parentfield" varchar({varchar\_len}), formatted text "parenttype" varchar({varchar\_len}))).
- Return fields.

**Methods declared on this owner** [get column definitions](operations-089.md#op-15d1e09be6af15).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L5756) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1137)
