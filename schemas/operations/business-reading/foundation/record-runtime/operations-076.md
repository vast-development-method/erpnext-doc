# Record lifecycle and persistence · operations 76

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platformclient

<a id="op-f60031ea397b90"></a>
### Platform OAuth2 Client.initialize

`operation_foundation_frappeclient_business_behavior_foundation_o_authentication_2_client_initialize`

**Inputs** self, url, access\_token, verify = true.

**Local steps**

- Bind dependencies requests.
- Set self.access\_token from access\_token.
- Set self.headers from mapping(“Authorization” → (“Bearer ” + access\_token), “content-type” → “application/x-www-form-urlencoded”).
- Set self.verify from verify.
- Set self.session from requests.session().
- Set self.url from url.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.session().

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L1699) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L336)

## Service · Platformdict

<a id="op-409d3964c85abc"></a>
### Dict.getstate

`operation_foundation_types_frappedict_business_behavior_mapping_getstate`

**Inputs** self.

**Wrappers, in declaration order** override.

**Declared result** Self.

**Explicit results** self.

**Local steps**

- Return self.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3811) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1445)

<a id="op-7f274ed7d21758"></a>
### Dict.update

`operation_foundation_types_frappedict_business_behavior_mapping_update`

**Inputs** self (positional only), m (positional only), remaining named values kwargs.

**Wrappers, in declaration order** overload.

**Declared result** Self.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3855) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1446)

<a id="op-2f7532f057f97d"></a>
### Dict.update

`operation_foundation_types_frappedict_business_behavior_mapping_update_2`

**Inputs** self (positional only), m (positional only), remaining named values kwargs.

**Wrappers, in declaration order** overload.

**Declared result** Self.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3930) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1447)

<a id="op-f1ae7548f2fabd"></a>
### Dict.update

`operation_foundation_types_frappedict_business_behavior_mapping_update_3`

**Inputs** self (positional only), remaining named values kwargs.

**Wrappers, in declaration order** overload.

**Declared result** Self.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4015) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1448)

<a id="op-346c0fb083c1b7"></a>
### Dict.update

`operation_foundation_types_frappedict_business_behavior_mapping_update_4`

**Inputs** self (positional only), m (positional only) = no value, remaining named values kwargs.

**Wrappers, in declaration order** override.

**Declared result** Self.

**Explicit results** self.

**Local steps**

- If m.
  - Evaluate super().update(m, expanded names kwargs).
- Otherwise.
  - Evaluate super().update(expanded names kwargs).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4063) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1449)

<a id="op-c718d910931e27"></a>
### Dict.copy

`operation_foundation_types_frappedict_business_behavior_mapping_copy`

**Inputs** self.

**Wrappers, in declaration order** override.

**Declared result** “\_dict&#91;\_KT, \_VT&#93;”.

**Explicit results** \_dict(self).

**Local steps**

- Return \_dict(self).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4268) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1444)

## Record · Prepared report

[Record definition](../../../../data/record-types/prepared_report.json)

<a id="op-cd754b72230145"></a>
### Prepared Report.queued by

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_queued_by`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.owner.

**Local steps**

- Return self.owner.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L2998) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L66)

<a id="op-c57f2aad556a5d"></a>
### Prepared Report.queued at

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_queued_at`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.creation.

**Local steps**

- Return self.creation.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L3044) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L65)

<a id="op-5560d8654aeba6"></a>
### Prepared Report.clear old logs

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “Prepared Report” via get\_all.

**Local steps**

- Set prepared\_reports\_to\_delete from Platform.get\_all(“Prepared Report”, filters = mapping(“creation” → list(“&lt;”, Platform.utils.add\_days(nested operand in the contract.utils.now(), negative days)))).
- For each batch in Platform.utils.create\_batch(prepared\_reports\_to\_delete, 100).
  - Evaluate enqueue(method = delete\_prepared\_reports, reports = batch).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now() · service or queued work from enqueue(method = delete\_prepared\_reports, reports = batch).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L3092) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L62)

<a id="op-101a74a057ca9a"></a>
### Prepared Report.before insert

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_before_insert`

**Inputs** self.

**Local steps**

- Set self.status from “Queued”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L3328) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L61)

<a id="op-5407a08fa6c6dd"></a>
### Prepared Report.on trash

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_on_trash`

**Inputs** self.

**Record and data access** resolve a document from “RQ Job” via get\_doc.

**Explicit results** no value.

**Local steps**

- If self.status does not belong to tuple(“Started”, “Queued”).
  - Return no value.
- Within suppress(Exception).
  - Set job from Platform.get\_doc(“RQ Job”, self.job\_id).
  - Evaluate job.stop\_job() when self.status equals “Started”, otherwise job.delete().
    - Value choice on self.status equals “Started” — true gives job.stop\_job(), false gives job.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L3375) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L64)

<a id="op-16098a099b2e3d"></a>
### Prepared Report.after insert

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_after_insert`

**Inputs** self.

**Record and data access** read “Report” via get\_value.

**Local steps**

- Set timeout from Platform.get\_value(“Report”, self.report\_name, “timeout”).
- Evaluate enqueue(generate\_report, queue = “long”, prepared\_report = self.name, timeout = (timeout or REPORT\_TIMEOUT), enqueue\_after\_commit = true, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in timeout → REPORT\_TIMEOUT.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(generate\_report, queue = “long”, prepared\_report = self.name, timeout = (timeout or REPORT\_TIMEOUT), enqueue\_after\_commit = true, …).

**Boundaries to resolve** stored data, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L3574) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L60)

<a id="op-78357f601a1534"></a>
### Prepared Report.get prepared data

`operation_foundation_core_record_definitions_prepared_report_business_behavior_prepared_report_get_prepared_data`

**Inputs** self, with\_file\_name = false.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** tuple(gzip.decompress(attached\_file.get\_content()), attachment.file\_name) · gzip.decompress(attached\_file.get\_content()).

**Explicit failure paths** validation helper — translated “No attachment found for the prepared report”.

**Local steps**

- Set attachments from get\_attachments(self.doctype, self.name).
- If not attachments.
  - Call the validation error handler Platform.throw(translated “No attachment found for the prepared report”, title = translated “Attachment Not Found”).
- Set attachment from no value.
- For each f in (attachments or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in attachments → list().
  - If f.file\_url.endswith(“.gz”).
    - Set attachment from f.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set attached\_file from Platform.get\_doc(“File”, attachment.name).
- If with\_file\_name.
  - Return tuple(gzip.decompress(attached\_file.get\_content()), attachment.file\_name).
- Return gzip.decompress(attached\_file.get\_content()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L99) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L63)

<a id="op-de5e231861e2f8"></a>
### Generate report

`operation_foundation_core_record_definitions_prepared_report_business_behavior_generate_report`

**Inputs** prepared\_report.

**Record and data access** resolve a document from “Prepared Report” via get\_doc · resolve a document from “Report” via get\_doc.

**State and service calls** call save on instance.

**Explicit results** no value.

**Local steps**

- Evaluate update\_job\_id(prepared\_report).
- Set instance from Platform.get\_doc(“Prepared Report”, prepared\_report).
- Set report from Platform.get\_doc(“Report”, instance.report\_name).
- Evaluate add\_data\_to\_monitor(report = instance.report\_name).
- Attempt the following.
  - Set report.custom\_columns from list().
  - If report.report\_type equals “Custom Report”.
    - Set custom\_report\_doc from report.
    - Set reference\_report from custom\_report\_doc.reference\_report.
    - Set report from Platform.get\_doc(“Report”, reference\_report).
    - If custom\_report\_doc.json.
      - Set data from json.loads(custom\_report\_doc.json).
      - If data.
        - Set report.custom\_columns from data at “columns”.
  - Set result from generate\_report\_result(report = report, filters = instance.filters, user = instance.owner).
  - Evaluate create\_json\_gz\_file(result, instance.doctype, instance.name, instance.report\_name).
  - Set instance.status from “Completed”.
- On failure (Exception).
  - Evaluate \_save\_error(instance, error = Platform.get\_traceback(with\_context = true)).
  - Evaluate notify\_report\_status(instance).
  - Return no value.
- Evaluate instance.reload().
- Set instance.status from “Completed”.
- Set instance.report\_end\_time from Platform.utils.now().
- Set instance.peak\_memory\_usage from resource.getrusage(resource.RUSAGE\_SELF).ru\_maxrss.
- Evaluate add\_data\_to\_monitor(peak\_memory\_usage = instance.peak\_memory\_usage).
- Evaluate instance.save(ignore\_permissions = true).
- Evaluate notify\_report\_status(instance).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L96) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L55)

<a id="op-2e50c8100af158"></a>
### Notify report status

`operation_foundation_binding_foundation_core_doctype_prepared_report_prepared_report_notify_report_status`

**Inputs** instance.

**Record and data access** resolve a document from mapping(“doctype” → “Notification Log”, “subject” → subject, “for\_user” → instance.owner, “document\_type” → “Report”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Notification Log”, “subject” → subject, “for\_user” → instance.owner, “document\_type” → “Report”, …)) · publish realtime with “report\_processed”.

**Explicit results** no value.

**Local steps**

- If instance.status does not belong to tuple(“Completed”, “Error”).
  - Return no value.
- If instance.status equals “Completed”.
  - Set subject from translated “Report {0} is ready.”.format(Platform.bold(instance.report\_name)).
- Otherwise.
  - Set subject from translated “Report {0} failed to generate.”.format(Platform.bold(instance.report\_name)).
  - If error bound to get\_user\_facing\_error(instance.error\_message).
    - Set subject from \_(“{0} Error: {1}”, context = “Prepared Report Notification”).format(subject, error).
- Set link from get\_url\_to\_report\_with\_filters(instance.report\_name, formatted text prepared\_report\_name={instance.name}).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Notification Log”, “subject” → subject, “for\_user” → instance.owner, “document\_type” → “Report”, …)).insert(ignore\_permissions = true).
- Evaluate Platform.publish\_realtime(“report\_processed”, mapping(“report\_name” → instance.report\_name, “name” → instance.name), user = instance.owner, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“report\_processed”, mapping(“report\_name” → instance.report\_name, “name” → instance.name), user = instance.owner, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L637)

<a id="op-575f26cae9b32e"></a>
### Save error

`operation_foundation_core_record_definitions_prepared_report_business_behavior_save_error`

**Inputs** instance, error.

**Wrappers, in declaration order** dangerously\_reconnect\_on\_connection\_abort.

**State and service calls** call save on instance.

**Local steps**

- Evaluate instance.reload().
- Set instance.status from “Error”.
- Set instance.error\_message from error.
- Set instance.report\_end\_time from Platform.utils.now().
- Evaluate instance.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L100) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L68)

<a id="op-45a48c73b0092a"></a>
### Update job id

`operation_foundation_core_record_definitions_prepared_report_business_behavior_update_job_identifier`

**Inputs** prepared\_report.

**State and service calls** request set\_value on “Prepared Report” · commit.

**Local steps**

- Set job from get\_current\_job().
- Evaluate Platform.db.set\_value(“Prepared Report”, prepared\_report, mapping(“job\_id” → (job and job.id), “status” → “Started”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job → job.id.
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L5694) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L70)

<a id="op-a597c139438fe6"></a>
### Make prepared report

`operation_foundation_core_record_definitions_prepared_report_business_behavior_make_prepared_report`

**Inputs** report\_name, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “Prepared Report”, “report\_name” → report\_name, “filters” → process\_filters\_for\_prepared\_report(filters)) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Prepared Report”, “report\_name” → report\_name, “filters” → process\_filters\_for\_prepared\_report(filters))).

**Explicit results** mapping(“name” → prepared\_report.name).

**Local steps**

- Bind dependencies validate\_report\_permission.
- Evaluate validate\_report\_permission(report\_name).
- Set prepared\_report from Platform.get\_doc(mapping(“doctype” → “Prepared Report”, “report\_name” → report\_name, “filters” → process\_filters\_for\_prepared\_report(filters))).insert(ignore\_permissions = true).
- Return mapping(“name” → prepared\_report.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L98) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L59)

<a id="op-5020dc99da352c"></a>
### Stop prepared report

`operation_foundation_core_record_definitions_prepared_report_business_behavior_stop_prepared_report`

**Inputs** report\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Prepared Report” via get\_doc.

**State and service calls** request set\_value on “Prepared Report” · msgprint with translated “Job stopped successfully” · msgprint with translated “Job is not running.”.

**Explicit failure paths** validation helper — formatted text Invalid job\_id: must start with {Platform.local.site}.

**Local steps**

- Set prepared\_report from Platform.get\_doc(“Prepared Report”, report\_name).
- Evaluate prepared\_report.check\_permission(“write”).
- Set job\_id from prepared\_report.job\_id.
- If not job\_id.startswith(formatted text {Platform.local.site}\|\|).
  - Call the validation error handler Platform.throw(formatted text Invalid job\_id: must start with {Platform.local.site}).
- Attempt the following.
  - Evaluate send\_stop\_job\_command(connection = get\_redis\_conn(), job\_id = job\_id).
  - Evaluate Platform.db.set\_value(“Prepared Report”, prepared\_report.name, mapping(“status” → “Cancelled”)).
  - Evaluate Platform.msgprint(translated “Job stopped successfully”, alert = true, indicator = “green”).
- On failure (InvalidJobOperation).
  - Evaluate Platform.msgprint(translated “Job is not running.”, title = translated “Invalid Operation”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from prepared\_report.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L101) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L69)

<a id="op-296724d094d9fc"></a>
### Process filters for prepared report

`operation_foundation_core_record_definitions_prepared_report_business_behavior_process_filters_for_prepared_report`

**Inputs** filters.

**Declared result** str.

**Explicit results** Platform.as\_json(filters, indent = no value, separators = tuple(“,”, “:”)).

**Local steps**

- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Return Platform.as\_json(filters, indent = no value, separators = tuple(“,”, “:”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L6615) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L67)

<a id="op-5132cc85b50f0b"></a>
### Get reports in queued state

`operation_foundation_core_record_definitions_prepared_report_business_behavior_get_reports_in_queued_state`

**Inputs** report\_name, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Prepared Report” via get\_all.

**Explicit results** Platform.get\_all(“Prepared Report”, filters = mapping(“report\_name” → report\_name, “filters” → process\_filters\_for\_prepared\_report(filters), “status” → tuple(“in”, tuple(“Queued”, “Started”)), “owner” → Pl ….

**Local steps**

- Return Platform.get\_all(“Prepared Report”, filters = mapping(“report\_name” → report\_name, “filters” → process\_filters\_for\_prepared\_report(filters), “status” → tuple(“in”, tuple(“Queued”, “Started”)), “owner” → Pl ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L6788) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L57)

<a id="op-c3a3deab9c7873"></a>
### Get last processed prepared report

`operation_foundation_binding_foundation_core_doctype_prepared_report_prepared_report_get_last_processed_prepared_report`

**Inputs** filters, user, report\_name.

**Record and data access** read “Prepared Report” via get\_value.

**Explicit results** Platform.db.get\_value(“Prepared Report”, filters = mapping(“status” → tuple(“in”, tuple(“Completed”, “Error”)), “filters” → process\_filters\_for\_prepared\_report(filters), “owner” → user, “report\_name” → rep ….

**Local steps**

- Return Platform.db.get\_value(“Prepared Report”, filters = mapping(“status” → tuple(“in”, tuple(“Completed”, “Error”)), “filters” → process\_filters\_for\_prepared\_report(filters), “owner” → user, “report\_name” → rep ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L636)

<a id="op-0ce559cf89c019"></a>
### Expire stalled report

`operation_foundation_core_record_definitions_prepared_report_business_behavior_expire_stalled_report`

**Inputs** no declared parameters.

**Record and data access** read “Prepared Report” via get\_all.

**State and service calls** request set\_value on “Prepared Report”.

**Explicit results** no value.

**Local steps**

- Set stalled\_reports from Platform.get\_all(“Prepared Report”, filters = mapping(“status” → “Started”, “creation” → tuple(“&lt;”, add\_to\_date(now(), seconds = negative FAILURE\_THRESHOLD, as\_datetime = true))), fields = list(“name”, “re ….
- If not stalled\_reports.
  - Return no value.
- Set status from “Error”.
- Set error\_message from translated “Report timed out.”.
- Evaluate Platform.db.set\_value(“Prepared Report”, mapping(“name” → tuple(“in”, list of instance.name for instance drawn from stalled\_reports)), mapping(“status” → status, “error\_message” → error\_message, “report\_en ….
  - Draw instance from stalled\_reports.
- For each instance in stalled\_reports.
  - Set instance.status from status.
  - Set instance.error\_message from error\_message.
  - Evaluate notify\_report\_status(instance).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L95) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L54)
