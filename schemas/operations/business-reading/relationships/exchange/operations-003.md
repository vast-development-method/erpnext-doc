# Integrations and service calls · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-4ee50a6f339f1d"></a>
### Update call log

`operation_relationships_integrations_twilio_application_interface_business_behavior_update_call_log`

**Inputs** call\_sid, status = no value.

**Record and data access** read “CRM Call Log” via exists · resolve a document from “CRM Call Log” via get\_doc.

**State and service calls** call save on call\_log · commit.

**Explicit results** no value · call\_log.

**Local steps**

- Set twilio from Twilio.connect().
- If not (twilio and Platform.db.exists(“CRM Call Log”, call\_sid)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in twilio → Platform.db.exists(“CRM Call Log”, call\_sid).
  - Return no value.
- Attempt the following.
  - Set call\_details from twilio.get\_call\_info(call\_sid).
  - Set call\_log from Platform.get\_doc(“CRM Call Log”, call\_sid).
  - Set call\_log.status from TwilioCallDetails.get\_call\_status((status or call\_details.status)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in status → call\_details.status.
  - Set call\_log.duration from call\_details.duration.
  - Set call\_log.start\_time from get\_datetime\_from\_timestamp(call\_details.start\_time).
  - Set call\_log.end\_time from get\_datetime\_from\_timestamp(call\_details.end\_time).
  - Evaluate call\_log.save(ignore\_permissions = true).
  - Evaluate Platform.db.commit().
  - Return call\_log.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Error while updating call record”).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L5402) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1352) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1328)

<a id="op-018581a19336f3"></a>
### Get twilio settings

`operation_relationships_integrations_twilio_application_interface_business_behavior_get_twilio_settings`

**Inputs** no declared parameters.

**Record and data access** read “CRM Twilio Settings” via get\_single.

**Explicit results** Platform.get\_single(“CRM Twilio Settings”).

**Local steps**

- Return Platform.get\_single(“CRM Twilio Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L5857) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1348) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1324)

<a id="op-3f145b77564120"></a>
### Update recording info

`operation_relationships_integrations_twilio_application_interface_business_behavior_update_recording_info`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**State and service calls** request set\_value on “CRM Call Log” · commit.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Call log not found” · exc.

**Local steps**

- Set args from Platform.\_dict(kwargs).
- Evaluate validate\_twilio\_request(args).
- Set recording\_url from args.RecordingUrl.
- Set call\_sid from args.CallSid.
- Set call\_log from update\_call\_log(call\_sid).
- If not call\_log.
  - Call the validation error handler Platform.throw(translated “Call log not found”, Platform.DoesNotExistError).
- Attempt the following.
  - Evaluate Platform.db.set\_value(“CRM Call Log”, call\_sid, “recording\_url”, recording\_url).
  - Evaluate Platform.db.commit().
- On failure (Exception) bound to exc.
  - Evaluate Platform.log\_error(title = translated “Failed to capture Twilio recording”).
  - Raise exc.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L5908) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1354) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1330)

<a id="op-191f5b119fafac"></a>
### Update call status info

`operation_relationships_integrations_twilio_application_interface_business_behavior_update_call_status_info`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Call log not found” · exc.

**Local steps**

- Set args from Platform.\_dict(kwargs).
- Evaluate validate\_twilio\_request(args).
- Set parent\_call\_sid from args.ParentCallSid.
- Set call\_log from update\_call\_log(parent\_call\_sid, status = args.CallStatus).
- If not call\_log.
  - Call the validation error handler Platform.throw(translated “Call log not found”, Platform.DoesNotExistError).
- Set call\_info from mapping(“ParentCallSid” → args.ParentCallSid, “CallSid” → args.CallSid, “CallStatus” → args.CallStatus, “CallDuration” → args.CallDuration, …).
- Attempt the following.
  - Set client from Twilio.get\_twilio\_client().
  - Evaluate client.calls(args.ParentCallSid).user\_defined\_messages.create(content = json.dumps(call\_info)).
- On failure (Exception) bound to exc.
  - Evaluate Platform.log\_error(title = translated “Failed to update Twilio call status”).
  - Raise exc.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L6283) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1353) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1329)

<a id="op-8a6b0d3d5198df"></a>
### Get datetime from timestamp

`operation_relationships_integrations_twilio_application_interface_business_behavior_get_datetime_from_timestamp`

**Inputs** timestamp.

**Explicit results** no value · Platform.utils.format\_datetime(converted\_datetime, “yyyy-MM-dd HH:mm:ss”).

**Local steps**

- Bind dependencies datetime.
- Bind dependencies ZoneInfo.
- If not timestamp.
  - Return no value.
- Set datetime\_utc\_tz\_str from timestamp.strftime(“%Y-%m-%d %H:%M:%S%z”).
- Set datetime\_utc\_tz from datetime.strptime(datetime\_utc\_tz\_str, “%Y-%m-%d %H:%M:%S%z”).
- Set system\_timezone from Platform.utils.get\_system\_timezone().
- Set converted\_datetime from datetime\_utc\_tz.astimezone(ZoneInfo(system\_timezone)).
- Return Platform.utils.format\_datetime(converted\_datetime, “yyyy-MM-dd HH:mm:ss”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0053.json#L6781) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1347) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1323)

## Service · Assignment rule

<a id="op-2539f22d2331e1"></a>
### Get assignment rules list

`operation_relationships_application_interface_assignment_rule_business_behavior_get_assignment_rules_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Assignment Rule” via get\_all · read “Assignment Rule” via get\_value · read “Assignment Rule User” via exists.

**Explicit results** assignment\_rules.

**Local steps**

- Set assignment\_rules from list().
- For each docname in Platform.get\_all(“Assignment Rule”, filters = mapping(“document\_type” → list(“in”, list(“CRM Lead”, “CRM Deal”)))).
  - Set doc from Platform.get\_value(“Assignment Rule”, docname, fieldname = list(“name”, “description”, “disabled”, “priority”), as\_dict = true).
  - Set users\_exists from bool(Platform.db.exists(“Assignment Rule User”, mapping(“parent” → docname.name))).
  - Evaluate assignment\_rules.append(mapping(expand doc, “users\_exists” → users\_exists)).
- Return assignment\_rules.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L6113) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L17) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L16)

<a id="op-f84c6102d6d276"></a>
### Duplicate assignment rule

`operation_relationships_application_interface_assignment_rule_business_behavior_duplicate_assignment_rule`

**Inputs** docname, new\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Assignment Rule” via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.get\_doc(“Assignment Rule”, docname).
- Set doc.name from new\_name.
- Set doc.assignment\_rule\_name from new\_name.
- Evaluate doc.insert().
- Return doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L6486) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L16) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L15)

## Service · Auth

<a id="op-543a0ab972156c"></a>
### Oauth providers

`operation_relationships_application_interface_auth_business_behavior_delegated_authorization_providers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L6652) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L18) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L17)

## Service · Availability

<a id="op-8dbe956c348565"></a>
### Validate user

`operation_relationships_binding_crm_api_availability_validate_user`

**Inputs** doc, method = no value.

**Record and data access** read “CRM Availability Status” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is not an enabled availability status.”.format(doc.crm\_availability).

**Local steps**

- If (doc.is\_new() or not doc.has\_value\_changed(“crm\_availability”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → not doc.has\_value\_changed(“crm\_availability”).
  - Return no value.
- If (doc.crm\_availability and not Platform.db.get\_value(“CRM Availability Status”, doc.crm\_availability, “enabled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.crm\_availability → not Platform.db.get\_value(“CRM Availability Status”, doc.crm\_availability, “enabled”).
  - Call the validation error handler Platform.throw(translated “{0} is not an enabled availability status.”.format(doc.crm\_availability)).
- Set doc.crm\_availability\_changed\_on from Platform.utils.now().
- Set doc.crm\_availability\_changed\_by from Platform.session.user.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L28) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L184) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L165)

<a id="op-aa33b2026fa40b"></a>
### On user update

`operation_relationships_binding_crm_api_availability_on_user_update`

**Inputs** doc, method = no value.

**Local steps**

- If (doc.get\_doc\_before\_save() and doc.has\_value\_changed(“crm\_availability”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get\_doc\_before\_save() → doc.has\_value\_changed(“crm\_availability”).
  - Evaluate publish\_availability(doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L25) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L181) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L162)

<a id="op-7122e4ae4a6126"></a>
### Publish availability

`operation_relationships_binding_crm_api_availability_publish_availability`

**Inputs** user.

**Record and data access** read “User” via get\_value.

**State and service calls** publish realtime with “crm\_availability\_updated”.

**Local steps**

- Set values from Platform.db.get\_value(“User”, user, list(“crm\_availability”, “crm\_availability\_changed\_on”, “crm\_availability\_changed\_by”), as\_dict = true).
- Evaluate Platform.publish\_realtime(“crm\_availability\_updated”, mapping(“user” → user, expand values), room = get\_site\_room(), after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_availability\_updated”, mapping(“user” → user, expand values), room = get\_site\_room(), after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L26) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L182) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L163)

<a id="op-c873ad2f8ab158"></a>
### Publish statuses updated

`operation_relationships_binding_crm_api_availability_publish_statuses_updated`

**Inputs** no declared parameters.

**State and service calls** publish realtime with “crm\_availability\_statuses\_updated”.

**Local steps**

- Evaluate Platform.publish\_realtime(“crm\_availability\_statuses\_updated”, room = get\_site\_room(), after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_availability\_statuses\_updated”, room = get\_site\_room(), after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L27) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L183) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L164)

<a id="op-312ac47f84b464"></a>
### Get user categories

`operation_relationships_binding_crm_api_availability_get_user_categories`

**Inputs** users.

**Record and data access** read “CRM Availability Status” via get\_all · read “User” via get\_all.

**Explicit results** mapping of user → (categories.get(statuses.get(user)) or “Active”) for user drawn from users.

**Local steps**

- Set categories from dict(Platform.get\_all(“CRM Availability Status”, fields = list(“name”, “category”), as\_list = true)).
- Set statuses from dict(Platform.get\_all(“User”, mapping(“name” → list(“in”, users)), list(“name”, “crm\_availability”), as\_list = true)).
- Return mapping of user → (categories.get(statuses.get(user)) or “Active”) for user drawn from users.
  - Draw user from users.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in categories.get(statuses.get(user)) → “Active”.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L24) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L180) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L161)

## Service · Command palette

<a id="op-cee5a7441e08a7"></a>
### Search

`operation_relationships_binding_crm_api_command_palette_search`

**Inputs** query = empty text, recent\_names = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“matches” → \_search\_all(query) when len(query) ≥ 2, otherwise list(), “activity” → \_search\_activity(query) when len(query) ≥ 2, otherwise list(), “recent” → \_get\_recent(recent) when not query, othe ….

**Local steps**

- Set query from (query or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query → empty text.
- Set recent from \_parse\_recent(recent\_names).
- Return mapping(“matches” → \_search\_all(query) when len(query) ≥ 2, otherwise list(), “activity” → \_search\_activity(query) when len(query) ≥ 2, otherwise list(), “recent” → \_get\_recent(recent) when not query, othe ….
  - Value choice on len(query) ≥ 2 — true gives \_search\_all(query), false gives list().
  - Value choice on len(query) ≥ 2 — true gives \_search\_activity(query), false gives list().
  - Value choice on not query — true gives \_get\_recent(recent), false gives list().
  - Value choice on not query — true gives \_get\_upcoming(), false gives list().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L41) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L197) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L178)

<a id="op-cfaa4be69c133e"></a>
### Get upcoming

`operation_relationships_binding_crm_api_command_palette_get_upcoming`

**Inputs** no declared parameters.

**Explicit results** items at slice no value to UPCOMING\_LIMIT.

**Local steps**

- Set items from (\_upcoming\_tasks() + \_upcoming\_slas()).
- Evaluate items.sort(key = deferred anonymous expression).
- Return items at slice no value to UPCOMING\_LIMIT.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L33) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L189) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L170)

<a id="op-467d2ef0a0ae36"></a>
### Upcoming tasks

`operation_relationships_binding_crm_api_command_palette_upcoming_tasks`

**Inputs** no declared parameters.

**Record and data access** read “CRM Task” via get\_list.

**Explicit results** list() · list of \_upcoming\_task(row) for row drawn from rows.

**Local steps**

- If not Platform.has\_permission(“CRM Task”, “read”).
  - Return list().
- Set rows from Platform.get\_list(“CRM Task”, fields = list(“name”, “title”, “due\_date”, “reference\_doctype”, …), filters = mapping(“status” → list(“not in”, OPEN\_TASK\_STATUSES), “assigned\_to” → Platform.session.user, “du ….
- Return list of \_upcoming\_task(row) for row drawn from rows.
  - Draw row from rows.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Task”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L48) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L204) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L185)

<a id="op-11021c3f20c329"></a>
### Upcoming task

`operation_relationships_binding_crm_api_command_palette_upcoming_task`

**Inputs** row.

**Explicit results** mapping(“kind” → “task”, “name” → row.name, “title” → row.title, “label” → “Task”, …).

**Local steps**

- Set reference from SEARCH\_TYPES.get(row.reference\_doctype).
- Return mapping(“kind” → “task”, “name” → row.name, “title” → row.title, “label” → “Task”, …).
  - Value choice on (reference and row.reference\_docname) — true gives reference at 0, false gives “Tasks”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference → row.reference\_docname.
  - Value choice on reference — true gives row.reference\_docname, false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L47) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L203) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L184)

<a id="op-19028d63042c58"></a>
### Window

`operation_relationships_binding_crm_api_command_palette_window`

**Inputs** hours.

**Explicit results** list(add\_days(now, negative OVERDUE\_GRACE\_DAYS), add\_to\_date(now, hours = hours)).

**Local steps**

- Set now from now\_datetime().
- Return list(add\_days(now, negative OVERDUE\_GRACE\_DAYS), add\_to\_date(now, hours = hours)).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L49) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L205) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L186)

<a id="op-bf8328dde01ebf"></a>
### Upcoming slas

`operation_relationships_binding_crm_api_command_palette_upcoming_slas`

**Inputs** no declared parameters.

**Explicit results** items.

**Local steps**

- Set items from list().
- For each tuple(doctype, tuple(route, title\_field, \_fields)) in SEARCH\_TYPES.items().
  - If (doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) or not Platform.has\_permission(doctype, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) → not Platform.has\_permission(doctype, “read”).
    - Continue with the next iteration or loop test.
  - Evaluate items.extend(\_upcoming\_sla(doctype, route, title\_field)).
- Return items.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L46) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L202) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L183)

<a id="op-d47d22405fc810"></a>
### Upcoming sla

`operation_relationships_binding_crm_api_command_palette_upcoming_sla`

**Inputs** doctype, route, title\_field.

**Record and data access** read doctype via get\_list.

**Explicit results** list of mapping(“kind” → “sla”, “name” → row.name, “title” → (row.get(title\_field) or row.name), “label” → “Response due”, …) for row drawn from rows.

**Local steps**

- Set rows from Platform.get\_list(doctype, fields = list(“name”, title\_field, “response\_by”), filters = mapping(“sla\_status” → list(“in”, SLA\_DUE\_STATUSES), “response\_by” → list(“between”, \_window(UPCOMING\_SLA\_HOURS)), “\_ ….
- Return list of mapping(“kind” → “sla”, “name” → row.name, “title” → (row.get(title\_field) or row.name), “label” → “Response due”, …) for row drawn from rows.
  - Draw row from rows.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(title\_field) → row.name.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L45) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L201) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L182)

<a id="op-236d10e240a9ac"></a>
### Parse recent

`operation_relationships_binding_crm_api_command_palette_parse_recent`

**Inputs** value.

**Explicit results** mapping() · recent when isinstance(recent, dict), otherwise mapping().

**Local steps**

- Attempt the following.
  - Set recent from Platform.parse\_json((value or “{}”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → “{}”.
- On failure (tuple(TypeError, ValueError)).
  - Return mapping().
- Return recent when isinstance(recent, dict), otherwise mapping().
  - Value choice on isinstance(recent, dict) — true gives recent, false gives mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L36) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L192) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L173)

<a id="op-df19a61b287377"></a>
### Search all

`operation_relationships_binding_crm_api_command_palette_search_all`

**Inputs** query.

**Explicit results** results.

**Local steps**

- Set results from list().
- For each tuple(doctype, config) in SEARCH\_TYPES.items().
  - If Platform.has\_permission(doctype, “read”).
    - Evaluate results.extend(\_search\_doctype(doctype, config, query)).
- Return results.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L43) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L199) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L180)

<a id="op-771e826637a115"></a>
### Search doctype

`operation_relationships_binding_crm_api_command_palette_search_doctype`

**Inputs** doctype, config, query.

**Record and data access** read doctype via get\_list.

**Explicit results** list of mapping(expand \_record(row, doctype, route, title\_field), “keywords” → \_keywords(row, search\_fields)) for row drawn from rows.

**Local steps**

- Set tuple(route, title\_field, search\_fields) from config.
- Set fields from list(“name”, title\_field, expanded search\_fields).
- Set rows from Platform.get\_list(doctype, fields = list(dict.fromkeys(fields)), or\_filters = list of list(field, “like”, formatted text %{query}%) for field drawn from list(“name”, expanded search\_fields), order\_by = “mo ….
  - Draw field from list(“name”, expanded search\_fields).
- Return list of mapping(expand \_record(row, doctype, route, title\_field), “keywords” → \_keywords(row, search\_fields)) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L44) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L200) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L181)

<a id="op-f95e9a2f690f3a"></a>
### Keywords

`operation_relationships_binding_crm_api_command_palette_keywords`

**Inputs** row, search\_fields.

**Explicit results** one space.join(generator of str(row.get(field)) for field drawn from list(“name”, expanded search\_fields) where row.get(field)).

**Local steps**

- Return one space.join(generator of str(row.get(field)) for field drawn from list(“name”, expanded search\_fields) where row.get(field)).
  - Draw field from list(“name”, expanded search\_fields), keep a combination only if (row.get(field)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L34) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L190) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L171)
