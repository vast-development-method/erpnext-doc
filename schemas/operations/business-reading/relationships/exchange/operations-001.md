# Integrations and service calls · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Activities

<a id="op-d8e30bf4cd7d25"></a>
### Get activities

`operation_relationships_application_interface_activities_business_behavior_get_activities`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Deal” via exists · read “CRM Lead” via exists.

**Explicit results** get\_deal\_activities(name) · get\_lead\_activities(name).

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Document not found”.

**Local steps**

- If Platform.db.exists(“CRM Deal”, name).
  - Return get\_deal\_activities(name).
- Otherwise.
  - If Platform.db.exists(“CRM Lead”, name).
    - Return get\_lead\_activities(name).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Document not found”, Platform.DoesNotExistError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L3713) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L4) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L4)

<a id="op-24a4fbb5c3618f"></a>
### Get deal activities

`operation_relationships_application_interface_activities_business_behavior_get_deal_activities`

**Inputs** name.

**Record and data access** read “CRM Deal” via get\_values.

**Explicit results** tuple(activities, calls, notes, tasks, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Deal”, “read”, name).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Evaluate get\_docinfo(empty text, “CRM Deal”, name).
- Set docinfo from Platform.response at “docinfo”.
- Set deal\_meta from Platform.get\_meta(“CRM Deal”).
- Set deal\_fields from mapping of field.fieldname → mapping(“label” → field.label, “options” → field.options) for field drawn from deal\_meta.fields.
  - Draw field from deal\_meta.fields.
- Set avoid\_fields from list(“lead”, “response\_by”, “sla\_creation”, “sla”, …).
- Set doc from Platform.db.get\_values(“CRM Deal”, name, list(“creation”, “owner”, “lead”)) at 0.
- Set lead from doc at 2.
- Set activities from list().
- Set calls from list().
- Set notes from list().
- Set tasks from list().
- Set attachments from list().
- Set creation\_text from translated “created this deal”.
- If lead.
  - Set creation\_text from translated “converted the lead to this deal”.
  - If Platform.has\_permission(“CRM Lead”, “read”, lead).
    - Set tuple(activities, calls, notes, tasks, …) from get\_lead\_activities(lead).
    - Set activities from ungroup\_note\_activities(activities).
- Evaluate activities.append(mapping(“activity\_type” → “creation”, “creation” → doc at 0, “owner” → doc at 1, “data” → creation\_text, …)).
- Evaluate docinfo.versions.reverse().
- For each version in docinfo.versions.
  - Set data from json.loads(version.data).
  - If not data.get(“changed”).
    - Continue with the next iteration or loop test.
  - If change bound to data.get(“changed”) at 0.
    - Set field from deal\_fields.get(change at 0, no value).
    - If (not field or change at 0 belongs to avoid\_fields or (not change at 1 and not change at 2)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not field → change at 0 belongs to avoid\_fields → (not change at 1 and not change at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not change at 1 → not change at 2.
      - Continue with the next iteration or loop test.
    - Set field\_label from (field.get(“label”) or change at 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“label”) → change at 0.
    - Set field\_option from (field.get(“options”) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“options”) → no value.
    - Set activity\_type from “changed”.
    - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “old\_value” → change at 1, “value” → change at 2).
    - If (not change at 1 and change at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not change at 1 → change at 2.
      - Set activity\_type from “added”.
      - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “value” → change at 2).
    - Otherwise.
      - If (change at 1 and not change at 2).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in change at 1 → not change at 2.
        - Set activity\_type from “removed”.
        - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “value” → change at 1).
    - If (data.get(“value”) and field\_option and is\_translatable(field\_option)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“value”) → field\_option → is\_translatable(field\_option).
      - Set data at “value” from translated data at “value”.
      - If data.get(“old\_value”).
        - Set data at “old\_value” from translated data at “old\_value”.
  - Set activity from mapping(“activity\_type” → activity\_type, “creation” → version.creation, “owner” → version.owner, “data” → data, …).
  - Evaluate activities.append(activity).
- For each comment in docinfo.comments.
  - Set activity from mapping(“name” → comment.name, “activity\_type” → “comment”, “creation” → comment.creation, “owner” → comment.owner, …).
  - Evaluate activities.append(activity).
- For each communication in (docinfo.communications + docinfo.automated\_messages).
  - Set activity from mapping(“activity\_type” → “communication”, “name” → communication.name, “communication\_type” → communication.communication\_type, “communication\_date” → (communication.communication\_date or communication.cr ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.communication\_date → communication.creation.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.communication\_date → communication.creation.
  - Evaluate activities.append(activity).
- For each attachment\_log in docinfo.attachment\_logs.
  - Set activity from mapping(“name” → attachment\_log.name, “activity\_type” → “attachment\_log”, “creation” → attachment\_log.creation, “owner” → attachment\_log.owner, …).
  - Evaluate activities.append(activity).
- Set linked\_calls from get\_linked\_calls(name).
- Set calls from (calls + linked\_calls.get(“calls”, list())).
- Set lead\_notes from set of n.get(“name”) for n drawn from notes.
  - Draw n from notes.
- Set deal\_notes from list of n for n drawn from (get\_linked\_notes(name) + linked\_calls.get(“notes”, list())) where n.get(“name”) does not belong to lead\_notes.
  - Draw n from (get\_linked\_notes(name) + linked\_calls.get(“notes”, list())), keep a combination only if (n.get(“name”) does not belong to lead\_notes).
- Set notes from (notes + deal\_notes).
- Set tasks from ((tasks + get\_linked\_tasks(name)) + linked\_calls.get(“tasks”, list())).
- Set attachments from (attachments + get\_attachments(“CRM Deal”, name)).
- Update activities using + get\_note\_activities(deal\_notes, is\_lead = false).
- Evaluate activities.sort(key = deferred anonymous expression, reverse = true).
- Set activities from handle\_multiple\_versions(activities).
- Set activities from group\_note\_activities(activities).
- Return tuple(activities, calls, notes, tasks, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “read”, name), Platform.has\_permission(“CRM Lead”, “read”, lead).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L2) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L6) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L6)

<a id="op-6d891ff94ec8a1"></a>
### Get lead activities

`operation_relationships_application_interface_activities_business_behavior_get_lead_activities`

**Inputs** name.

**Record and data access** read “CRM Lead” via get\_values.

**Explicit results** tuple(activities, calls, notes, tasks, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Lead”, “read”, name).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Evaluate get\_docinfo(empty text, “CRM Lead”, name).
- Set docinfo from Platform.response at “docinfo”.
- Set lead\_meta from Platform.get\_meta(“CRM Lead”).
- Set lead\_fields from mapping of field.fieldname → mapping(“label” → field.label, “options” → field.options) for field drawn from lead\_meta.fields.
  - Draw field from lead\_meta.fields.
- Set avoid\_fields from list(“converted”, “response\_by”, “sla\_creation”, “sla”, …).
- Set doc from Platform.db.get\_values(“CRM Lead”, name, list(“creation”, “owner”)) at 0.
- Set activities from list(mapping(“activity\_type” → “creation”, “creation” → doc at 0, “owner” → doc at 1, “data” → translated “created this lead”, …)).
- Evaluate docinfo.versions.reverse().
- For each version in docinfo.versions.
  - Set data from json.loads(version.data).
  - If not data.get(“changed”).
    - Continue with the next iteration or loop test.
  - If change bound to data.get(“changed”) at 0.
    - Set field from lead\_fields.get(change at 0, no value).
    - If (not field or change at 0 belongs to avoid\_fields or (not change at 1 and not change at 2)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not field → change at 0 belongs to avoid\_fields → (not change at 1 and not change at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not change at 1 → not change at 2.
      - Continue with the next iteration or loop test.
    - Set field\_label from (field.get(“label”) or change at 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“label”) → change at 0.
    - Set field\_option from (field.get(“options”) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“options”) → no value.
    - Set activity\_type from “changed”.
    - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “old\_value” → change at 1, “value” → change at 2).
    - If (not change at 1 and change at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not change at 1 → change at 2.
      - Set activity\_type from “added”.
      - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “value” → change at 2).
    - Otherwise.
      - If (change at 1 and not change at 2).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in change at 1 → not change at 2.
        - Set activity\_type from “removed”.
        - Set data from mapping(“field” → change at 0, “field\_label” → field\_label, “value” → change at 1).
    - If (data.get(“value”) and field\_option and is\_translatable(field\_option)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“value”) → field\_option → is\_translatable(field\_option).
      - Set data at “value” from translated data at “value”.
      - If data.get(“old\_value”).
        - Set data at “old\_value” from translated data at “old\_value”.
  - Set activity from mapping(“activity\_type” → activity\_type, “creation” → version.creation, “owner” → version.owner, “data” → data, …).
  - Evaluate activities.append(activity).
- For each comment in docinfo.comments.
  - Set activity from mapping(“name” → comment.name, “activity\_type” → “comment”, “creation” → comment.creation, “owner” → comment.owner, …).
  - Evaluate activities.append(activity).
- For each communication in (docinfo.communications + docinfo.automated\_messages).
  - Set activity from mapping(“activity\_type” → “communication”, “name” → communication.name, “communication\_type” → communication.communication\_type, “communication\_date” → (communication.communication\_date or communication.cr ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.communication\_date → communication.creation.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.communication\_date → communication.creation.
  - Evaluate activities.append(activity).
- For each attachment\_log in docinfo.attachment\_logs.
  - Set activity from mapping(“name” → attachment\_log.name, “activity\_type” → “attachment\_log”, “creation” → attachment\_log.creation, “owner” → attachment\_log.owner, …).
  - Evaluate activities.append(activity).
- Set calls from get\_linked\_calls(name).get(“calls”, list()).
- Set notes from (get\_linked\_notes(name) + get\_linked\_calls(name).get(“notes”, list())).
- Set tasks from (get\_linked\_tasks(name) + get\_linked\_calls(name).get(“tasks”, list())).
- Set attachments from get\_attachments(“CRM Lead”, name).
- Update activities using + get\_note\_activities(notes, is\_lead = true).
- Evaluate activities.sort(key = deferred anonymous expression, reverse = true).
- Set activities from handle\_multiple\_versions(activities).
- Set activities from group\_note\_activities(activities).
- Return tuple(activities, calls, notes, tasks, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Lead”, “read”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L3) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L7) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L7)

<a id="op-75a31336d2e6ef"></a>
### Get attachments

`operation_relationships_application_interface_activities_business_behavior_get_attachments`

**Inputs** doctype, name.

**Record and data access** read “File” via get\_all.

**Explicit results** (Platform.db.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → name), fields = list(“name”, “file\_name”, “file\_type”, “file\_url”, …)) or list()).

**Local steps**

- Return (Platform.db.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → name), fields = list(“name”, “file\_name”, “file\_type”, “file\_url”, …)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → name), fields = list(“name”, “file\_name”, “file\_type”, “file\_url”, …)) → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L2905) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L5) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L5)

<a id="op-f21781d43d6438"></a>
### Get send after

`operation_relationships_binding_crm_api_activities_get_send_after`

**Inputs** communication.

**Declared result** (str bitwise or no value).

**Record and data access** read “Communication” via get\_value.

**Explicit results** no value · Platform.db.get\_value(“Communication”, communication.name, “send\_after”).

**Local steps**

- If communication.delivery\_status differs from “Scheduled”.
  - Return no value.
- Return Platform.db.get\_value(“Communication”, communication.name, “send\_after”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L21) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L177) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L158)

<a id="op-d7228f4daa9ae9"></a>
### Handle multiple versions

`operation_relationships_application_interface_activities_business_behavior_handle_multiple_versions`

**Inputs** versions.

**Explicit results** activities.

**Local steps**

- Set activities from list().
- Set grouped\_versions from list().
- Set old\_version from no value.
- For each version in versions.
  - Set is\_version from version at “activity\_type” belongs to list(“changed”, “added”, “removed”).
  - If not is\_version.
    - Evaluate activities.append(version).
  - If not old\_version.
    - Set old\_version from version.
    - If is\_version.
      - Evaluate grouped\_versions.append(version).
    - Continue with the next iteration or loop test.
  - If (is\_version and old\_version.get(“owner”) and version at “owner” equals old\_version at “owner”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_version → old\_version.get(“owner”) → version at “owner” equals old\_version at “owner”.
    - Evaluate grouped\_versions.append(version).
  - Otherwise.
    - If grouped\_versions.
      - Evaluate activities.append(parse\_grouped\_versions(grouped\_versions)).
    - Set grouped\_versions from list().
    - If is\_version.
      - Evaluate grouped\_versions.append(version).
  - Set old\_version from version.
  - If (version equals versions at negative 1 and grouped\_versions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in version equals versions at negative 1 → grouped\_versions.
    - Evaluate activities.append(parse\_grouped\_versions(grouped\_versions)).
- Return activities.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L3129) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L12) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L11)

<a id="op-7fa6981a07f656"></a>
### Group note activities

`operation_relationships_binding_crm_api_activities_group_note_activities`

**Inputs** activities.

**Explicit results** grouped.

**Local steps**

- Set grouped from list().
- For each activity in activities.
  - Set previous from grouped at negative 1 when grouped, otherwise no value.
    - Value choice on grouped — true gives grouped at negative 1, false gives no value.
  - If (activity at “activity\_type” equals “note” and previous and previous at “activity\_type” equals “note” and previous at “owner” equals activity at “owner”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in activity at “activity\_type” equals “note” → previous → previous at “activity\_type” equals “note” → previous at “owner” equals activity at “owner”.
    - Evaluate previous.setdefault(“other\_notes”, list()).append(activity).
  - Otherwise.
    - Evaluate grouped.append(activity).
- Return grouped.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L22) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L178) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L159)

<a id="op-d2f5271974d78d"></a>
### Ungroup note activities

`operation_relationships_binding_crm_api_activities_ungroup_note_activities`

**Inputs** activities.

**Explicit results** ungrouped.

**Local steps**

- Set ungrouped from list().
- For each activity in activities.
  - Evaluate ungrouped.append(activity).
  - Evaluate ungrouped.extend(activity.pop(“other\_notes”, list())).
- Return ungrouped.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L23) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L179) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L160)

<a id="op-08352bdfc06f6f"></a>
### Parse grouped versions

`operation_relationships_application_interface_activities_business_behavior_parse_grouped_versions`

**Inputs** versions.

**Explicit results** version.

**Local steps**

- Set version from versions at 0.
- If len(versions) equals 1.
  - Return version.
- Set other\_versions from versions at slice 1 to no value.
- Set version at “other\_versions” from other\_versions.
- Return version.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L3667) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L15) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L14)

<a id="op-4f09117c594ce9"></a>
### Get linked calls

`operation_relationships_application_interface_activities_business_behavior_get_linked_calls`

**Inputs** name.

**Record and data access** read “CRM Call Log” via get\_all · read “Dynamic Link” via get\_all · read “FCRM Note” via get\_all · read “CRM Task” via get\_all.

**Explicit results** mapping(“calls” → calls, “notes” → notes, “tasks” → tasks).

**Local steps**

- Set calls from Platform.db.get\_all(“CRM Call Log”, filters = mapping(“reference\_docname” → name), fields = list(“name”, “caller”, “receiver”, “from”, …)).
- Set linked\_calls from Platform.db.get\_all(“Dynamic Link”, filters = mapping(“link\_name” → name, “parenttype” → “CRM Call Log”), pluck = “parent”).
- Set notes from list().
- Set tasks from list().
- If linked\_calls.
  - Set CallLog from Platform.qb.DocType(“CRM Call Log”).
  - Set Link from Platform.qb.DocType(“Dynamic Link”).
  - Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).join(Link, JoinType.inner).on(Link.parent e ….
  - Set \_calls from query.run(as\_dict = true).
  - For each call in \_calls.
    - If call.get(“link\_doctype”) equals “FCRM Note”.
      - Evaluate notes.append(call.link\_name).
    - Otherwise.
      - If call.get(“link\_doctype”) equals “CRM Task”.
        - Evaluate tasks.append(call.link\_name).
  - Set \_calls from list of call for call drawn from \_calls where call.get(“link\_doctype”) does not belong to list(“FCRM Note”, “CRM Task”).
    - Draw call from \_calls, keep a combination only if (call.get(“link\_doctype”) does not belong to list(“FCRM Note”, “CRM Task”)).
  - If \_calls.
    - Set calls from (calls + \_calls).
- If notes.
  - Set notes from Platform.db.get\_all(“FCRM Note”, filters = mapping(“name” → tuple(“in”, notes)), fields = list(“name”, “title”, “content”, “pinned”, …)).
- If tasks.
  - Set tasks from Platform.db.get\_all(“CRM Task”, filters = mapping(“name” → tuple(“in”, tasks)), fields = list(“name”, “title”, “description”, “assigned\_to”, …)).
- Set calls from list of parse\_call\_log(call) for call drawn from calls when calls, otherwise list().
  - Value choice on calls — true gives list of parse\_call\_log(call) for call drawn from calls, false gives list().
  - Draw call from calls.
- Return mapping(“calls” → calls, “notes” → notes, “tasks” → tasks).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L4) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L8) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L8)

<a id="op-4d0227d8eb7781"></a>
### Get linked notes

`operation_relationships_application_interface_activities_business_behavior_get_linked_notes`

**Inputs** name.

**Record and data access** read “FCRM Note” via get\_all.

**Explicit results** (notes or list()).

**Local steps**

- Set notes from Platform.db.get\_all(“FCRM Note”, filters = mapping(“reference\_docname” → name), fields = list(“name”, “title”, “content”, “pinned”, …)).
- Return (notes or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in notes → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L5) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L9) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L9)

<a id="op-4983fe36ccd24d"></a>
### Get note activities

`operation_relationships_binding_crm_api_activities_get_note_activities`

**Inputs** notes, is\_lead.

**Record and data access** read “Version” via get\_all.

**Explicit results** list() · activities.

**Local steps**

- Set notes from list of n for n drawn from notes where n.get(“name”).
  - Draw n from notes, keep a combination only if (n.get(“name”)).
- If not notes.
  - Return list().
- Set titles from mapping of n.get(“name”) → n.get(“title”) for n drawn from notes.
  - Draw n from notes.
- Set activities from list of mapping(“name” → note.get(“name”), “activity\_type” → “note”, “creation” → note.get(“creation”), “owner” → note.get(“owner”), …) for note drawn from notes.
  - Draw note from notes.
- Set versions from Platform.get\_all(“Version”, filters = mapping(“ref\_doctype” → “FCRM Note”, “docname” → list(“in”, list(titles)), “data” → list(“like”, “%"pinned"%”)), fields = list(“name”, “docname”, “owner”, “creation”, …)).
- For each version in versions.
  - Set changed from json.loads(version.data).get(“changed”, list()).
  - Set pinned from next(generator of c at 2 for c drawn from changed where c at 0 equals “pinned”, no value).
    - Draw c from changed, keep a combination only if (c at 0 equals “pinned”).
  - If pinned is identical to no value.
    - Continue with the next iteration or loop test.
  - Evaluate activities.append(mapping(“name” → version.name, “activity\_type” → “note”, “creation” → version.creation, “owner” → version.owner, …)).
    - Value choice on int(pinned) — true gives “pinned”, false gives “unpinned”.
- Return activities.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L20) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L176) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L157)

<a id="op-8dbb4426ab326d"></a>
### Get linked tasks

`operation_relationships_application_interface_activities_business_behavior_get_linked_tasks`

**Inputs** name.

**Record and data access** read “CRM Task” via get\_all.

**Explicit results** (tasks or list()).

**Local steps**

- Set tasks from Platform.db.get\_all(“CRM Task”, filters = mapping(“reference\_docname” → name), fields = list(“name”, “title”, “description”, “assigned\_to”, …)).
- Return (tasks or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tasks → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L5447) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L10) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L10)

<a id="op-d9a2b318c9ddc8"></a>
### Parse attachment log

`operation_relationships_application_interface_activities_business_behavior_parse_attachment_log`

**Inputs** html, type.

**Explicit results** mapping(“type” → type, “file\_name” → html.replace(“Removed ”, empty text), “file\_url” → empty text, “is\_private” → false) · mapping(“type” → type, “file\_name” → a\_tag.text, “file\_url” → a\_tag at “href”, “is\_private” → is\_private).

**Local steps**

- Set soup from BeautifulSoup(html, “html.parser”).
- Set a\_tag from soup.find(“a”).
- Set type from “added” when type equals “Attachment”, otherwise “removed”.
  - Value choice on type equals “Attachment” — true gives “added”, false gives “removed”.
- If not a\_tag.
  - Return mapping(“type” → type, “file\_name” → html.replace(“Removed ”, empty text), “file\_url” → empty text, “is\_private” → false).
- Set is\_private from false.
- If “private/files” belongs to a\_tag at “href”.
  - Set is\_private from true.
- Return mapping(“type” → type, “file\_name” → a\_tag.text, “file\_url” → a\_tag at “href”, “is\_private” → is\_private).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L5656) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L14) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L13)

<a id="op-87799c63966b85"></a>
### Is translatable

`operation_relationships_application_interface_activities_business_behavior_is_translatable`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** doctype belongs to get\_translated\_doctypes().

**Local steps**

- Return doctype belongs to get\_translated\_doctypes().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0002.json#L6047) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L13) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L12)

## Service · Api

<a id="op-68d78c56fb42f2"></a>
### Get translations

`operation_relationships_application_interface_initialize_business_behavior_get_translations`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** read “User” via get\_value · read “System Settings” via get\_single\_value.

**Explicit results** get\_all\_translations(language).

**Local steps**

- If Platform.session.user differs from “Guest”.
  - Set language from Platform.db.get\_value(“User”, Platform.session.user, “language”).
- Otherwise.
  - Set language from Platform.db.get\_single\_value(“System Settings”, “language”).
- Return get\_all\_translations(language).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “language”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L485) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L109) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L91)

<a id="op-81d6e3aa6046d6"></a>
### Get user signature

`operation_relationships_application_interface_initialize_business_behavior_get_user_signature`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value · read “Email Account” via get\_value.

**Explicit results** no value · content.

**Local steps**

- Set user from Platform.session.user.
- Set user\_email\_signature from Platform.db.get\_value(“User”, user, “email\_signature”) when user, otherwise no value.
  - Value choice on user — true gives Platform.db.get\_value(“User”, user, “email\_signature”), false gives no value.
- Set signature from (user\_email\_signature or Platform.db.get\_value(“Email Account”, mapping(“default\_outgoing” → 1, “add\_signature” → 1), “signature”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_email\_signature → Platform.db.get\_value(“Email Account”, mapping(“default\_outgoing” → 1, “add\_signature” → 1), “signature”).
- If not signature.
  - Return no value.
- Set soup from BeautifulSoup(signature, “html.parser”).
- Set html\_signature from soup.find(“div”, mapping(“class” → “ql-editor read-mode”)).
- Set \_signature from no value.
- If html\_signature.
  - Set \_signature from html\_signature.renderContents().
- Set content from empty text.
- If (cstr(\_signature) or signature).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(\_signature) → signature.
  - Set content from formatted text &lt;br&gt;&lt;p class="signature"&gt;{signature}&lt;/p&gt;.
- Return content.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L696) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L110) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L92)

<a id="op-09ca79b0fa4892"></a>
### Get unsubscribed emails

`operation_relationships_binding_crm_api_init_get_unsubscribed_emails`

**Inputs** emails, doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** list() · nested operand in the contract().where(nested operand in the contract.isin(emails)).where((EmailUnsubscribe.global\_unsubscribe equals 1 bitwise or (nested operand in the contract.reference\_doctype equals d ….

**Local steps**

- Evaluate Platform.has\_permission(doctype, “read”, name, throw = true).
- If not emails.
  - Return list().
- Set EmailUnsubscribe from Platform.qb.DocType(“Email Unsubscribe”).
- Return nested operand in the contract().where(nested operand in the contract.isin(emails)).where((EmailUnsubscribe.global\_unsubscribe equals 1 bitwise or (nested operand in the contract.reference\_doctype equals d ….

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L59) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L215) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L196)

<a id="op-250e5b9930d5c0"></a>
### Check app permission

`operation_relationships_application_interface_initialize_business_behavior_check_application_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L1145) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L106) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L88)

<a id="op-4e4df6a885ebf4"></a>
### Accept invitation

`operation_relationships_application_interface_initialize_business_behavior_accept_invitation`

**Inputs** key = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(limit = 10, seconds = (60 × 60)).

**Record and data access** read “CRM Invitation” via get\_all · resolve a document from “CRM Invitation” via get\_doc · resolve a document from “User” via get\_doc.

**Explicit failure paths** validation helper — translated “Invalid or expired key”.

**Local steps**

- If not key.
  - Call the validation error handler Platform.throw(translated “Invalid or expired key”).
- Set result from Platform.db.get\_all(“CRM Invitation”, filters = mapping(“key” → key), pluck = “name”).
- If not result.
  - Call the validation error handler Platform.throw(translated “Invalid or expired key”).
- Set invitation from Platform.get\_doc(“CRM Invitation”, result at 0).
- Set is\_new\_user from invitation.accept().
- Evaluate invitation.reload().
- Set Platform.local.flags.commit from true.
- If invitation.status equals “Accepted”.
  - Set Platform.local.response at “type” from “redirect”.
  - If is\_new\_user.
    - Set user from Platform.get\_doc(“User”, invitation.email).
    - Set Platform.local.response at “location” from user.\_reset\_password().
  - Otherwise.
    - Evaluate Platform.local.login\_manager.login\_as(invitation.email).
    - Set Platform.local.response at “location” from “/crm”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L1513) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L105) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L87)

<a id="op-7857e5e4310677"></a>
### Invite by email

`operation_relationships_application_interface_initialize_business_behavior_invite_by_email`

**Inputs** emails, role.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_all · read “CRM Invitation” via get\_all · resolve a document from “CRM Invitation” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “CRM Invitation”, email = email, role = role).

**Explicit results** no value · mapping(“existing\_members” → existing\_members, “existing\_invites” → existing\_invites, “to\_invite” → to\_invite).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to invite System Managers” · validation helper with Platform.PermissionError — translated “You are not allowed to invite Sales Managers” · validation helper with Platform.PermissionError — translated “Cannot invite for this role”.

**Local steps**

- Evaluate Platform.only\_for(list(“Sales Manager”, “System Manager”), true).
- Set user\_roles from Platform.get\_roles(Platform.session.user).
- If (role equals “System Manager” and “System Manager” does not belong to user\_roles).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in role equals “System Manager” → “System Manager” does not belong to user\_roles.
  - Call the validation error handler Platform.throw(translated “You are not allowed to invite System Managers”, Platform.PermissionError).
- If (role equals “Sales Manager” and “System Manager” does not belong to user\_roles).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in role equals “Sales Manager” → “System Manager” does not belong to user\_roles.
  - Call the validation error handler Platform.throw(translated “You are not allowed to invite Sales Managers”, Platform.PermissionError).
- If role does not belong to list(“System Manager”, “Sales Manager”, “Sales User”).
  - Call the validation error handler Platform.throw(translated “Cannot invite for this role”, Platform.PermissionError).
- If not emails.
  - Return no value.
- Set email\_string from validate\_email\_address(emails, throw = false).
- Set email\_list from split\_emails(email\_string).
- If not email\_list.
  - Return no value.
- Set existing\_members from Platform.db.get\_all(“User”, filters = mapping(“email” → list(“in”, email\_list)), pluck = “email”).
- Set existing\_invites from Platform.db.get\_all(“CRM Invitation”, filters = mapping(“email” → list(“in”, email\_list), “role” → list(“in”, list(“System Manager”, “Sales Manager”, “Sales User”))), pluck = “email”).
- Set to\_invite from list(((set(email\_list) − set(existing\_members)) − set(existing\_invites))).
- For each email in to\_invite.
  - Evaluate Platform.get\_doc(doctype = “CRM Invitation”, email = email, role = role).insert(ignore\_permissions = true).
- Return mapping(“existing\_members” → existing\_members, “existing\_invites” → existing\_invites, “to\_invite” → to\_invite).

**Values supplied outside this operation** effective access from Platform.only\_for(list(“Sales Manager”, “System Manager”), true), Platform.get\_roles(Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L2150) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L111) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L93)

<a id="op-6e1cdd0534145b"></a>
### Delete attachment

`operation_relationships_application_interface_initialize_business_behavior_delete_attachment`

**Inputs** doctype, docname, file\_url.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“DELETE”, “POST”)).

**Record and data access** read “File” via get\_value.

**State and service calls** request delete\_doc for “File”.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You don't have permission to delete this attachment”.

**Local steps**

- If not Platform.has\_permission(doctype, doc = docname, ptype = “write”).
  - Call the validation error handler Platform.throw(translated “You don't have permission to delete this attachment”, Platform.PermissionError).
- Set file\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → file\_url, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname), “name”).
- If file\_name.
  - Evaluate Platform.delete\_doc(“File”, file\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = docname, ptype = “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L3075) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L107) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L89)

<a id="op-bb8523f8b6d049"></a>
### Get file uploader defaults

`operation_relationships_application_interface_initialize_business_behavior_get_file_uploader_defaults`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“allowed\_file\_types” → Platform.get\_system\_settings(“allowed\_file\_extensions”), “max\_file\_size” → get\_max\_file\_size(), “max\_number\_of\_files” → max\_number\_of\_files, “make\_attachments\_public” → bool( ….

**Local steps**

- Set max\_number\_of\_files from no value.
- Set make\_attachments\_public from false.
- If doctype.
  - Set meta from Platform.get\_meta(doctype).
  - Set max\_number\_of\_files from meta.get(“max\_attachments”).
  - Set make\_attachments\_public from meta.get(“make\_attachments\_public”).
- Return mapping(“allowed\_file\_types” → Platform.get\_system\_settings(“allowed\_file\_extensions”), “max\_file\_size” → get\_max\_file\_size(), “max\_number\_of\_files” → max\_number\_of\_files, “make\_attachments\_public” → bool( ….

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“allowed\_file\_extensions”).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0001.json#L3423) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L108) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L90)

<a id="op-7f732e626c8421"></a>
### Get recording credentials

`operation_relationships_integrations_application_interface_business_behavior_get_recording_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** telephony\_medium.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0049.json#L6846) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1265) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1241)
