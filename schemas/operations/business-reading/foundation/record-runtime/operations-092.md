# Record lifecycle and persistence · operations 92

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Security settings

[Record definition](../../../../data/record-types/security_settings.json)

<a id="op-8ddddd7553dff8"></a>
### Check security txt expiry

`operation_foundation_core_record_definitions_security_settings_security_settings_alert_business_behavior_check_security_text_resource_expiry`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Security Settings” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set security\_settings from Platform.get\_doc(“Security Settings”).
- If not security\_settings.public\_expires.
  - Return no value.
- Set expires from security\_settings.public\_expires.
- If isinstance(expires, str).
  - Set expires from get\_datetime(expires).
- Set now from now\_datetime().
- Set days\_until\_expiry from (expires − now).days.
- Set alert\_days from list(30, 15, 7, 1).
- If days\_until\_expiry belongs to alert\_days.
  - Evaluate send\_expiry\_alert(Platform.local.site, expires, days\_until\_expiry).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L2819) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L510)

<a id="op-056e2a387f7d1b"></a>
### Send expiry alert

`operation_foundation_core_record_definitions_security_settings_security_settings_alert_business_behavior_send_expiry_alert`

**Inputs** site, expires, days\_until\_expiry.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set recipients from get\_users\_with\_role(“System Manager”).
- If not recipients.
  - Return no value.
- Set subject from get\_email\_subject(site, days\_until\_expiry).
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, template = “security\_txt\_expiry\_alert”, args = mapping(“site” → site, “expires” → expires, “days\_remaining” → days\_until\_expiry)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, template = “security\_txt\_expiry\_alert”, args = mapping(“site” → site, “expires” → expires, “days\_remaining” → days\_until\_expiry)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L3107) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L512)

<a id="op-bcd8c8f9982171"></a>
### Get email subject

`operation_foundation_core_record_definitions_security_settings_security_settings_alert_business_behavior_get_email_subject`

**Inputs** site, days\_until\_expiry.

**Declared result** str.

**Explicit results** formatted text &#91;URGENT&#93; Security.txt expires in 1 day - {site} · formatted text Security.txt expires in {days\_until\_expiry} days - {site}.

**Local steps**

- If days\_until\_expiry equals 1.
  - Return formatted text &#91;URGENT&#93; Security.txt expires in 1 day - {site}.
- Return formatted text Security.txt expires in {days\_until\_expiry} days - {site}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0104.json#L3330) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L511)

## Service · Sequence

<a id="op-30128a7e6769ef"></a>
### Create sequence

`operation_foundation_database_sequence_business_behavior_create_sequence`

**Inputs** doctype\_name, slug (named only, default “\_id\_seq”), temporary (named only, default false), check\_not\_exists (named only, default false), cycle (named only, default false), cache (named only, default SEQUENCE\_CACHE), start\_value (named only, default 0), increment\_by (named only, default 0), min\_value (named only, default 0), max\_value (named only, default 0).

**Declared result** str.

**Explicit results** sequence\_name.

**Local steps**

- Set query from “create sequence” when not temporary, otherwise “create temporary sequence”.
  - Value choice on not temporary — true gives “create sequence”, false gives “create temporary sequence”.
- Set sequence\_name from scrub((doctype\_name + slug)).
- If check\_not\_exists.
  - Update query using + “ if not exists”.
- Update query using + formatted text  {sequence\_name}.
- If increment\_by.
  - Update query using + formatted text  increment by {increment\_by}.
- If min\_value.
  - Update query using + formatted text  minvalue {min\_value}.
- If max\_value.
  - Update query using + formatted text  maxvalue {max\_value}.
- If start\_value.
  - Update query using + formatted text  start {start\_value}.
- If cache.
  - Update query using + formatted text  cache {cache}.
- Otherwise.
  - If db.db\_type equals “mariadb”.
    - Update query using + “ nocache”.
- If not cycle.
  - If db.db\_type equals “mariadb”.
    - Update query using + “ nocycle”.
- Otherwise.
  - Update query using + “ cycle”.
- Evaluate db.sql\_ddl(query).
- Return sequence\_name.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L7) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1451)

<a id="op-91706f17575d55"></a>
### Get next val

`operation_foundation_database_sequence_business_behavior_get_next_val`

**Inputs** doctype\_name, slug = “\_id\_seq”.

**Declared result** int.

**Explicit results** db.sql(formatted text SELECT nextval({sequence\_name})) at 0 at 0.

**Explicit failure paths** db.SequenceGeneratorLimitExceeded.

**Local steps**

- Set sequence\_name from scrub(formatted text {doctype\_name}{slug}).
- If db.db\_type equals “postgres”.
  - Set sequence\_name from formatted text '"{sequence\_name}"'.
- Otherwise.
  - If db.db\_type equals “mariadb”.
    - Set sequence\_name from formatted text ′{sequence\_name}′.
- Attempt the following.
  - Return db.sql(formatted text SELECT nextval({sequence\_name})) at 0 at 0.
- On failure (IndexError).
  - Raise db.SequenceGeneratorLimitExceeded.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L8) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1453)

<a id="op-a9502af82c652b"></a>
### Set next val

`operation_foundation_database_sequence_business_behavior_set_next_val`

**Inputs** doctype\_name, next\_val, slug (named only, default “\_id\_seq”), is\_val\_used (named only, default false).

**Declared result** no value.

**Local steps**

- Set is\_val\_used from “false” when not is\_val\_used, otherwise “true”.
  - Value choice on not is\_val\_used — true gives “false”, false gives “true”.
- Evaluate db.multisql(mapping(“postgres” → formatted text SELECT SETVAL('"{scrub((doctype\_name + slug))}"', {next\_val}, {is\_val\_used}), “mariadb” → formatted text SELECT SETVAL(′{scrub((doctype\_name + slug))}′, {nex ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L9) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1454)

<a id="op-8c6426a5906e12"></a>
### Get existing sequences

`operation_foundation_database_sequence_business_behavior_get_existing_sequences`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** set of r at 0 for r drawn from rows.

**Local steps**

- If db.db\_type equals “postgres”.
  - Set rows from db.sql(query text (SELECT)).
- Otherwise.
  - Set rows from db.sql(query text (SELECT)).
- Return set of r at 0 for r drawn from rows.
  - Draw r from rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L4827) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1452)

<a id="op-79ff4a82801538"></a>
### Create missing sequences

`operation_foundation_database_sequence_business_behavior_create_missing_sequences`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “DocType” via get\_all.

**Explicit results** list() · created.

**Local steps**

- Bind dependencies Platform.
- Bind dependencies Max.
- If db.db\_type equals “sqlite”.
  - Return list().
- Set doctypes from Platform.get\_all(“DocType”, filters = mapping(“autoname” → “autoincrement”, “issingle” → 0, “is\_virtual” → 0), pluck = “name”).
- If not doctypes.
  - Return list().
- Set existing from \_get\_existing\_sequences().
- Set created from list().
- For each doctype in doctypes.
  - If scrub(formatted text {doctype}\_id\_seq) belongs to existing.
    - Continue with the next iteration or loop test.
  - Set table from Platform.qb.DocType(doctype).
  - Set max\_name from nested operand in the contract(nested operand in the contract).select(Max(nested operand in the contract at nested operand in the contract)).run() at 0 at 0.
  - Evaluate create\_sequence(doctype, check\_not\_exists = true, start\_value = (int(max\_name) + 1) when max\_name, otherwise 0).
    - Value choice on max\_name — true gives (int(max\_name) + 1), false gives 0.
  - Evaluate created.append(doctype).
- Return created.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0146.json#L3342) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1450)

## Record · Server script

[Record definition](../../../../data/record-types/server_script.json)

<a id="op-dadfe057ca6afd"></a>
### Server Script.validate

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_validate`

**Inputs** self.

**Local steps**

- Evaluate Platform.only\_for(“Script Manager”, true).
- Evaluate self.check\_if\_compilable\_in\_restricted\_context().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if compilable in restricted context](operations-092.md#op-3fca34dca3a870).

**Values supplied outside this operation** effective access from Platform.only\_for(“Script Manager”, true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L591) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L556)

<a id="op-89022ecd132afd"></a>
### Server Script.on update

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.sync\_scheduled\_job\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync scheduled job type](operations-092.md#op-451521d0a34ac0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L671) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L552)

<a id="op-275bb64abe195d"></a>
### Server Script.clear cache

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate Platform.client\_cache.delete\_value(“server\_script\_map”).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L722) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L544)

<a id="op-99a37034dbd715"></a>
### Server Script.on trash

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_on_trash`

**Inputs** self.

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**State and service calls** call save on scheduled\_job\_type.

**Local steps**

- Evaluate Platform.client\_cache.delete\_value(“server\_script\_map”).
- If self.script\_type equals “Scheduler Event”.
  - For each job in self.scheduled\_jobs.
    - Set scheduled\_job\_type from Platform.get\_doc(“Scheduled Job Type”, job.name).
    - Set scheduled\_job\_type.stopped from true.
    - Set scheduled\_job\_type.server\_script from no value.
    - Evaluate scheduled\_job\_type.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L805) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L551)

<a id="op-4a5e14e4c9c0c0"></a>
### Server Script.get code fields

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_get_code_fields`

**Inputs** self.

**Explicit results** mapping(“script” → “py”).

**Local steps**

- Return mapping(“script” → “py”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L1008) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L549)

<a id="op-3c28bbc290c1de"></a>
### Server Script.scheduled jobs

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_scheduled_jobs`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at dict at tuple(str, str).

**Record and data access** read “Scheduled Job Type” via get\_all.

**Explicit results** Platform.get\_all(“Scheduled Job Type”, filters = mapping(“server\_script” → self.name), fields = list(“name”, “stopped”)).

**Local steps**

- Return Platform.get\_all(“Scheduled Job Type”, filters = mapping(“server\_script” → self.name), fields = list(“name”, “stopped”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L1062) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L553)

<a id="op-451521d0a34ac0"></a>
### Server Script.sync scheduled job type

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_sync_scheduled_job_type`

**Inputs** self.

**State and service calls** call save on get\_scheduled\_job().update(mapping(“stopped” → 1)) · call save on get\_scheduled\_job().update(mapping(“method” → Platform.scrub(formatted text {self.name}-{self.event\_frequency}), “frequency” → self.event\_frequency, “cron\_format” → self.cron\_format when self.event\_frequen … · msgprint with translated “Scheduled execution for script {0} has updated”.format(self.name).

**Explicit results** no value.

**Local steps**

- Bind local operation get\_scheduled\_job for subsequent calls.
- Set previous\_script\_type from self.get\_value\_before\_save(“script\_type”).
- If (previous\_script\_type differs from self.script\_type and previous\_script\_type equals “Scheduler Event”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_script\_type differs from self.script\_type → previous\_script\_type equals “Scheduler Event”.
  - Evaluate get\_scheduled\_job().update(mapping(“stopped” → 1)).save().
  - Return no value.
- If (self.script\_type differs from “Scheduler Event” or not (self.has\_value\_changed(“event\_frequency”) or self.has\_value\_changed(“cron\_format”) or self.has\_value\_changed(“disabled”) or self.has\_value\_changed(“ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.script\_type differs from “Scheduler Event” → not (self.has\_value\_changed(“event\_frequency”) or self.has\_value\_changed(“cron\_format”) or self.has\_value\_changed(“disabled”) or self.has\_value\_changed(“script\_type”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“event\_frequency”) → self.has\_value\_changed(“cron\_format”) → self.has\_value\_changed(“disabled”) → self.has\_value\_changed(“script\_type”).
  - Return no value.
- Evaluate get\_scheduled\_job().update(mapping(“method” → Platform.scrub(formatted text {nested operand in the contract.name}-{nested operand in the contract.event\_frequency}), “frequency” → self.event\_frequency, “cro ….save().
  - Value choice on self.event\_frequency equals “Cron” — true gives self.cron\_format, false gives empty text.
- Evaluate Platform.msgprint(translated “Scheduled execution for script {0} has updated”.format(self.name), alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L35) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L554)

<a id="op-897d2c444a7662"></a>
### Server Script.sync scheduled job type.get scheduled job

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_sync_scheduled_job_type_get_scheduled_job`

**Inputs** no declared parameters.

**Declared result** “ScheduledJobType”.

**Record and data access** read “Scheduled Job Type” via get\_value · resolve a document from “Scheduled Job Type” via get\_doc · resolve a document from mapping(“doctype” → “Scheduled Job Type”, “server\_script” → self.name, “create\_log” → should\_create\_log) via get\_doc.

**Explicit results** Platform.get\_doc(“Scheduled Job Type”, scheduled\_script) · Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “server\_script” → self.name, “create\_log” → should\_create\_log)).

**Local steps**

- If scheduled\_script bound to Platform.db.get\_value(“Scheduled Job Type”, mapping(“server\_script” → self.name)).
  - Return Platform.get\_doc(“Scheduled Job Type”, scheduled\_script).
- Otherwise.
  - Set should\_create\_log from self.event\_frequency does not belong to tuple(“All”, “Cron”).
  - Return Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “server\_script” → self.name, “create\_log” → should\_create\_log)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L2099) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L555)

<a id="op-3fca34dca3a870"></a>
### Server Script.check if compilable in restricted context

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_check_if_compilable_in_restricted_context`

**Inputs** self.

**State and service calls** msgprint with str(e).

**Local steps**

- Bind dependencies compile\_restricted.
- Attempt the following.
  - Evaluate compile\_restricted(self.script, policy = PlatformTransformer).
- On failure (Exception) bound to e.
  - Evaluate Platform.msgprint(str(e), title = translated “Compilation warning”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L2349) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L543)

<a id="op-84686a52eb03f9"></a>
### Server Script.execute method

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_execute_method`

**Inputs** self.

**Declared result** dict.

**Explicit results** rate\_limit(limit = limit, seconds = seconds, endpoint = formatted text server\_script:{self.name})(\_fn)() · execute\_api\_server\_script(self).

**Local steps**

- If self.enable\_rate\_limit.
  - Set limit from (self.rate\_limit\_count or 5).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rate\_limit\_count → 5.
  - Set seconds from (self.rate\_limit\_seconds or ((24 × 60) × 60)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rate\_limit\_seconds → ((24 × 60) × 60).
  - Set \_fn from partial(execute\_api\_server\_script, script = self).
  - Return rate\_limit(limit = limit, seconds = seconds, endpoint = formatted text server\_script:{self.name})(\_fn)().
- Otherwise.
  - Return execute\_api\_server\_script(self).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L2506) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L545)

<a id="op-e5623b8c2881f3"></a>
### Server Script.execute doc

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_execute_record`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, doc.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L2768) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L546)

<a id="op-3c37d477013e39"></a>
### Server Script.execute scheduled method

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_execute_scheduled_method`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Locally raised failures** DoesNotExistError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L2885) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L547)

<a id="op-5df25cce076353"></a>
### Server Script.get permission query conditions

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, user, active\_child\_tables.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3005) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L550)

<a id="op-ebc8d837d10027"></a>
### Server Script.execute workflow task

`operation_foundation_core_record_definitions_server_script_business_behavior_server_script_execute_workflow_task`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, doc.

**Locally raised failures** DoesNotExistError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3227) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L548)

<a id="op-fdb5293643594e"></a>
### Get autocompletion items

`operation_foundation_core_record_definitions_server_script_business_behavior_get_autocompletion_items`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = (10 × 60), stale\_while\_revalidate = ((6 × 60) × 60)).

**Explicit results** Platform.cache.get\_value(“server\_script\_autocompletion\_items”, generator = deferred anonymous expression).

**Local steps**

- Return Platform.cache.get\_value(“server\_script\_autocompletion\_items”, generator = deferred anonymous expression).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3376) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L542)

<a id="op-a13e841b678c31"></a>
### Execute api server script

`operation_foundation_core_record_definitions_server_script_business_behavior_execute_application_programming_interface_server_script`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script, args, kwargs.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** DoesNotExistError, PermissionError.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0105.json#L3619) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L541)
