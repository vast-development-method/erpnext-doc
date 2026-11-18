# Forms, reports and navigation · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Event

[Record definition](../../../../data/record-types/event.json)

<a id="op-c97a50ba94dd05"></a>
### Send event digest

`operation_foundation_desk_record_definitions_event_business_behavior_send_event_digest`

**Inputs** no declared parameters.

**State and service calls** sendmail.

**Local steps**

- Set today from getdate().
- Set users from list of user for user drawn from get\_enabled\_system\_users() where is\_email\_enabled\_for\_feature(user.name, “enable\_email\_event\_reminders”).
  - Draw user from get\_enabled\_system\_users(), keep a combination only if (is\_email\_enabled\_for\_feature(user.name, “enable\_email\_event\_reminders”)).
- For each user in users.
  - Set events from get\_events(today, today, user.name, for\_reminder = true).
  - If events.
    - Evaluate Platform.set\_user\_lang(user.name, user.language).
    - For each e in events.
      - Set e.starts\_on from format\_datetime(e.starts\_on, “hh:mm a”).
      - If e.all\_day.
        - Set e.starts\_on from “All Day”.
    - Evaluate Platform.sendmail(recipients = user.email, subject = Platform.\_(“Upcoming Events for Today”), template = “upcoming\_events”, args = mapping(“events” → events), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = user.email, subject = Platform.\_(“Upcoming Events for Today”), template = “upcoming\_events”, args = mapping(“events” → events), …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L1068) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L754)

<a id="op-b0bc88a1e73fd8"></a>
### Get events

`operation_foundation_desk_record_definitions_event_business_behavior_get_events`

**Inputs** start, end, user = no value, for\_reminder = false, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = (5 × 60), stale\_while\_revalidate = (60 × 60)).

**Declared result** list at Platform.\_dict.

**Record and data access** execute query text (SELECT, Doc Share).format(tables = “, ”.join(tables), filter\_condition = filter\_condition, reminder\_condition = “AND ′tabEvent′.send\_reminder = 1” when for\_reminder, otherwise empty text).

**Explicit results** resolved\_events.

**Local steps**

- Set tuple(start, end) from tuple(getdate(start), getdate(end)).
- Set caller from Platform.session.user.
- Set target\_user from (user or caller).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → caller.
- If (user and user differs from caller).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user → user differs from caller.
  - Evaluate Platform.only\_for(“System Manager”).
- Bind the type alias EventLikeDict to (Event bitwise or Platform.\_dict).
- Set resolved\_events from list().
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set filter\_condition from get\_filters\_cond(“Event”, filters, list()).
- Set tables from list(“′tabEvent′”).
- If “′tabEvent Participants′” belongs to filter\_condition.
  - Evaluate tables.append(“′tabEvent Participants′”).
- Set event\_candidates from Platform.db.sql(query text (SELECT, Doc Share).format(tables = “, ”.join(tables), filter\_condition = filter\_condition, reminder\_condition = “AND ′tabEvent′.send\_reminder = 1” when for\_reminder, otherwise e ….
  - Value choice on for\_reminder — true gives “AND ′tabEvent′.send\_reminder = 1”, false gives empty text.
- Bind local operation resolve\_event for subsequent calls.
- For each e in event\_candidates.
  - If not e.repeat\_this\_event.
    - Evaluate resolved\_events.append(e).
    - Continue with the next iteration or loop test.
  - If (e.repeat\_till and e.repeat\_till &lt; start).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.repeat\_till → e.repeat\_till &lt; start.
    - Continue with the next iteration or loop test.
  - Set repeat\_till from getdate((e.repeat\_till or “3000-01-01”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in e.repeat\_till → “3000-01-01”.
  - If e.repeat\_on equals “Daily”.
    - Set target\_date from start.
    - While target\_date ≤ end.
      - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
      - Set target\_date from add\_days(target\_date, 1).
  - Otherwise.
    - If e.repeat\_on equals “Weekly”.
      - Set target\_date from start.
      - While target\_date ≤ end.
        - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
        - Set target\_date from add\_days(target\_date, 1).
    - Otherwise.
      - If e.repeat\_on equals “Monthly”.
        - Set first\_occurence\_in\_range from e.starts\_on.date().
        - Set jump\_ahead from (month\_diff(start, first\_occurence\_in\_range) − 1).
        - Set target\_date from add\_months(first\_occurence\_in\_range, jump\_ahead).
        - While target\_date ≤ end.
          - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
          - Set target\_date from add\_months(target\_date, 1).
      - Otherwise.
        - If e.repeat\_on equals “Quarterly”.
          - Set first\_occurence\_in\_range from e.starts\_on.date().
          - Set jump\_ahead from (month\_diff(start, first\_occurence\_in\_range) floor divide 3).
          - Set target\_date from add\_months(first\_occurence\_in\_range, (3 × jump\_ahead)).
          - While target\_date ≤ end.
            - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
            - Set target\_date from add\_months(target\_date, 3).
        - Otherwise.
          - If e.repeat\_on equals “Yearly”.
            - Set first\_occurence\_in\_range from e.starts\_on.date().
            - Set jump\_ahead from (month\_diff(start, first\_occurence\_in\_range) floor divide 12).
            - Set target\_date from add\_years(first\_occurence\_in\_range, jump\_ahead).
            - While target\_date ≤ end.
              - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
              - Set target\_date from add\_years(target\_date, 1).
          - Otherwise.
            - If e.repeat\_on equals “Half Yearly”.
              - Set first\_occurence\_in\_range from e.starts\_on.date().
              - Set jump\_ahead from (month\_diff(start, first\_occurence\_in\_range) floor divide 6).
              - Set target\_date from add\_months(first\_occurence\_in\_range, (6 × jump\_ahead)).
              - While target\_date ≤ end.
                - Evaluate resolve\_event(e, target\_date = target\_date, repeat\_till = repeat\_till).
                - Set target\_date from add\_months(target\_date, 6).
- For each event in resolved\_events.
  - For each fieldname in weekdays.
    - Evaluate event.pop(fieldname, no value).
- Return resolved\_events.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L2) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L750)

<a id="op-d7e2e885514b1c"></a>
### Get events.resolve event

`operation_foundation_desk_record_definitions_event_business_behavior_get_events_resolve_event`

**Inputs** e, target\_date, repeat\_till.

**Explicit results** no value.

**Local steps**

- If (e.repeat\_on equals “Weekly” and not e at weekdays at target\_date.weekday()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.repeat\_on equals “Weekly” → not e at weekdays at target\_date.weekday().
  - Return no value.
- If not (e.starts\_on.date() ≤ target\_date and target\_date ≥ start and target\_date ≤ end and target\_date ≤ repeat\_till).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e.starts\_on.date() ≤ target\_date → target\_date ≥ start → target\_date ≤ end → target\_date ≤ repeat\_till.
  - Return no value.
- Set ends\_on\_date from add\_days(target\_date, (e.ends\_on − e.starts\_on).days) when e.ends\_on, otherwise no value.
  - Value choice on e.ends\_on — true gives add\_days(target\_date, (e.ends\_on − e.starts\_on).days), false gives no value.
- If (ends\_on\_date and e.repeat\_till and (ends\_on\_date &gt; e.repeat\_till or ends\_on\_date &lt; start)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ends\_on\_date → e.repeat\_till → (ends\_on\_date &gt; e.repeat\_till or ends\_on\_date &lt; start).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ends\_on\_date &gt; e.repeat\_till → ends\_on\_date &lt; start.
  - Return no value.
- Set new\_event from e.copy().
- Set new\_event.original\_starts\_on from new\_event.starts\_on.
- Set new\_event.original\_ends\_on from new\_event.ends\_on.
- Set new\_event.starts\_on from datetime.combine(target\_date, e.starts\_on.time()).
- Set new\_event.ends\_on from datetime.combine(ends\_on\_date, e.ends\_on.time()) when ends\_on\_date, otherwise no value.
  - Value choice on ends\_on\_date — true gives datetime.combine(ends\_on\_date, e.ends\_on.time()), false gives no value.
- Evaluate resolved\_events.append(new\_event).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L4894) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L751)

<a id="op-b2e6bc48de6105"></a>
### Delete events

`operation_foundation_desk_record_definitions_event_business_behavior_delete_events`

**Inputs** ref\_type, ref\_name, delete\_event = false.

**Record and data access** read “Event Participants” via get\_all.

**State and service calls** request delete\_doc for “Event” · request delete on “Event” · request delete on “Event Participants”.

**Local steps**

- Set participations from Platform.get\_all(“Event Participants”, filters = mapping(“reference\_doctype” → ref\_type, “reference\_docname” → ref\_name, “parenttype” → “Event”), fields = list(“parent”, “name”)).
- If participations.
  - For each participation in participations.
    - If delete\_event.
      - Evaluate Platform.delete\_doc(“Event”, participation.parent, for\_reload = true).
    - Otherwise.
      - Set total\_participants from Platform.get\_all(“Event Participants”, filters = mapping(“parenttype” → “Event”, “parent” → participation.parent)).
      - If len(total\_participants) ≤ 1.
        - Evaluate Platform.db.delete(“Event”, mapping(“name” → participation.parent)).
        - Evaluate Platform.db.delete(“Event Participants”, mapping(“name” → participation.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L5472) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L738)

<a id="op-adc4119bdac6b8"></a>
### Set status of events

`operation_foundation_desk_record_definitions_event_business_behavior_set_status_of_events`

**Inputs** no declared parameters.

**Record and data access** read “Event” via get\_list.

**State and service calls** request set\_value on “Event”.

**Local steps**

- Set events from Platform.get\_list(“Event”, filters = mapping(“status” → “Open”), fields = list(“name”, “ends\_on”, “repeat\_till”)).
- For each event in events.
  - If ((event.ends\_on and getdate(event.ends\_on) &lt; getdate(nowdate())) or (event.repeat\_till and getdate(event.repeat\_till) &lt; getdate(nowdate()))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (event.ends\_on and getdate(event.ends\_on) &lt; getdate(nowdate())) → (event.repeat\_till and getdate(event.repeat\_till) &lt; getdate(nowdate())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in event.ends\_on → getdate(event.ends\_on) &lt; getdate(nowdate()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in event.repeat\_till → getdate(event.repeat\_till) &lt; getdate(nowdate()).
    - Evaluate Platform.db.set\_value(“Event”, event.name, “status”, “Closed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L5969) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L755)

## Service · Export

<a id="op-8688fa4945a5dc"></a>
### Write document file

`operation_foundation_binding_foundation_studio_export_write_document_file`

**Inputs** doc, folder = no value, exclude\_fields = no value, filename = no value.

**Explicit failure paths** validation helper — translated “Invalid export path: {0}”.format(Path(path).as\_posix()).

**Local steps**

- Set doc\_export from doc.as\_dict(no\_nulls = true).
- Evaluate doc.run\_method(“before\_export”, doc\_export).
- Set doc\_export from strip\_default\_fields(doc, doc\_export).
- Evaluate remove\_empty\_values(doc\_export).
- For each field in (exclude\_fields or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in exclude\_fields → list().
  - Evaluate doc\_export.pop(field, no value).
- For each field in doc.meta.get(“fields”, mapping(“is\_virtual” → 1)).
  - Evaluate doc\_export.pop(field.fieldname, no value).
- Set fname from (filename or scrub(doc\_export.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename → scrub(doc\_export.name).
- Set path from os.path.join(folder, formatted text {fname}.json).
- If Path(path).resolve().is\_relative\_to(Path(Platform.get\_site\_path()).resolve()).
  - Call the validation error handler Platform.throw(translated “Invalid export path: {0}”.format(Path(path).as\_posix())).
- Within open(path, “w+”) bound as txtfile.
  - Evaluate txtfile.write((Platform.as\_json(doc\_export) + whitespace '\\n')).
- Evaluate cache\_synced\_file\_hash(path).
- Evaluate print(formatted text Wrote document file for {doc.doctype} {doc.name} at {path}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“before\_export”, doc\_export).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L215) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L22) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L110)

<a id="op-34e6e9489da741"></a>
### Write code file

`operation_foundation_binding_foundation_studio_export_write_code_file`

**Inputs** doc, folder, code\_field, extension, filename = no value.

**Explicit failure paths** validation helper — translated “Invalid export path: {0}”.format(Path(path).as\_posix()).

**Local steps**

- Set fname from (filename or scrub(doc.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename → scrub(doc.name).
- Set path from os.path.join(folder, formatted text {fname}.{extension}).
- If Path(path).resolve().is\_relative\_to(Path(Platform.get\_site\_path()).resolve()).
  - Call the validation error handler Platform.throw(translated “Invalid export path: {0}”.format(Path(path).as\_posix())).
- Within open(path, “w+”) bound as codefile.
  - Evaluate codefile.write((doc.get(code\_field) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(code\_field) → empty text.
- Evaluate print(formatted text Wrote {extension} file for {doc.doctype} {doc.name} at {path}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L214) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L21) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L109)

<a id="op-d201c9f9c93566"></a>
### Delete folder

`operation_foundation_binding_foundation_studio_export_delete_folder`

**Inputs** path = no value.

**Local steps**

- If (path and os.path.exists(path)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in path → os.path.exists(path).
  - Evaluate shutil.rmtree(path, ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L208) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L15) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L103)

<a id="op-5d203bff77b4a8"></a>
### Delete file

`operation_foundation_binding_foundation_studio_export_delete_file`

**Inputs** path, remaining positional values joins.

**Explicit results** no value.

**Local steps**

- If not path.
  - Return no value.
- Set path from os.path.join(path, expanded joins).
- If os.path.exists(path).
  - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L207) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L14) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L102)

<a id="op-2bf1a5f1b41ba1"></a>
### Can export

`operation_foundation_binding_foundation_studio_export_can_export`

**Inputs** doc.

**Declared result** bool.

**Explicit results** (doc.is\_standard and Platform.conf.developer\_mode and not Platform.flags.in\_install and not Platform.flags.in\_uninstall and not Platform.flags.in\_import).

**Local steps**

- Return (doc.is\_standard and Platform.conf.developer\_mode and not Platform.flags.in\_install and not Platform.flags.in\_uninstall and not Platform.flags.in\_import).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_standard → Platform.conf.developer\_mode → not Platform.flags.in\_install → not Platform.flags.in\_uninstall → not Platform.flags.in\_import.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L206) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L13) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L101)

<a id="op-83de542b571d5d"></a>
### Validate standard app change

`operation_foundation_binding_foundation_studio_export_validate_standard_app_change`

**Inputs** doc.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Standard apps can only be edited in developer mode.”.

**Local steps**

- If Platform.conf.developer\_mode.
  - Return no value.
- Set previous from doc.get\_doc\_before\_save().
- If not (doc.is\_standard or (previous and previous.is\_standard)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_standard → (previous and previous.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.is\_standard.
  - Return no value.
- If any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS).
  - Draw flag from SYNC\_FLAGS.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Standard apps can only be edited in developer mode.”, Platform.PermissionError, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L213) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L20) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L108)

<a id="op-2fd937823c43ca"></a>
### Validate Platform app

`operation_foundation_binding_foundation_studio_export_validate_foundation_app`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If (not doc.Platform\_app or any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.Platform\_app → any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS).
  - Draw flag from SYNC\_FLAGS.
  - Return no value.
- Evaluate validate\_installed\_app(doc.Platform\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L212) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L19) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L107)

<a id="op-b3c10834e73d19"></a>
### Parse json

`operation_foundation_binding_foundation_studio_export_parse_json`

**Inputs** field.

**Explicit results** Platform.parse\_json(field) · no value.

**Local steps**

- If (field and isinstance(field, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field → isinstance(field, str).
  - Return Platform.parse\_json(field).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L209) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L16) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L104)

<a id="op-9d9767ef54ac38"></a>
### Remove empty values

`operation_foundation_binding_foundation_studio_export_remove_empty_values`

**Inputs** docdict.

**Local steps**

- Set to\_remove from list().
- For each tuple(attr, value) in docdict.items().
  - If (attr equals “componentSlots” and isinstance(value, dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in attr equals “componentSlots” → isinstance(value, dict).
    - Evaluate remove\_empty\_values\_from\_slots(value).
  - If attr belongs to PRESERVED\_EMPTY\_PROPERTIES.
    - Continue with the next iteration or loop test.
  - If isinstance(value, list).
    - For each item in value.
      - If isinstance(item, dict).
        - Evaluate remove\_empty\_values(item).
    - If not value.
      - Evaluate to\_remove.append(attr).
  - Otherwise.
    - If isinstance(value, dict).
      - If not value.
        - Evaluate to\_remove.append(attr).
    - Otherwise.
      - If (value is identical to no value or value equals empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → value equals empty text.
        - Evaluate to\_remove.append(attr).
- For each attr in to\_remove.
  - Remove docdict at attr.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L210) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L17) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L105)

<a id="op-1e493a4f78c06f"></a>
### Remove empty values from slots

`operation_foundation_binding_foundation_studio_export_remove_empty_values_from_slots`

**Inputs** slots.

**Local steps**

- For each slot in slots.values().
  - If (isinstance(slot, dict) and isinstance(slot.get(“slotContent”), list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(slot, dict) → isinstance(slot.get(“slotContent”), list).
    - For each block in slot at “slotContent”.
      - If isinstance(block, dict).
        - Evaluate remove\_empty\_values(block).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L211) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L18) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L106)

## Service · Files

<a id="op-c90e4320c96bc6"></a>
### Run list app files

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_run_list_app_files`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** ref · formatted text FAILED: {error} · formatted text The app has no editable files yet. Create them with write\_app\_file (e.g. stores/notes.{extension}). · (“App files (paths are relative to the app root, imported as '@app/&lt;path&gt;'):\\n” + whitespace '\\n'.join(paths)).

**Local steps**

- Set ref from \_app\_ref(ctx).
- If isinstance(ref, str).
  - Return ref.
- Bind dependencies api, files.
- Attempt the following.
  - Set tree from api.list\_studio\_files(expanded ref).
- On failure (Exception) bound to error.
  - Return formatted text FAILED: {error}.
- Set paths from \_flatten(tree).
- If not paths.
  - Set extension from “js” when files.is\_db\_app(ref at 1), otherwise “ts”.
    - Value choice on files.is\_db\_app(ref at 1) — true gives “js”, false gives “ts”.
  - Return formatted text The app has no editable files yet. Create them with write\_app\_file (e.g. stores/notes.{extension})..
- Return (“App files (paths are relative to the app root, imported as '@app/&lt;path&gt;'):\\n” + whitespace '\\n'.join(paths)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1774)

<a id="op-21843fea86f298"></a>
### Run read app file

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_run_read_app_file`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** ref · “FAILED: file\_path is required.” · formatted text FAILED: {error} · formatted text {path}: {result at “content”}.

**Local steps**

- Set ref from \_app\_ref(ctx).
- If isinstance(ref, str).
  - Return ref.
- Set path from text\_arg(args.get(“file\_path”)).
- If not path.
  - Return “FAILED: file\_path is required.”.
- Bind dependencies api.
- Attempt the following.
  - Set result from api.read\_studio\_file(expanded ref, path).
- On failure (Exception) bound to error.
  - Return formatted text FAILED: {error}.
- Return formatted text {path}: {result at “content”}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1775)

<a id="op-8d1b1d3f0c6690"></a>
### Run write app file

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_run_write_app_file`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** ref · “FAILED: file\_path is required.” · “FAILED: content is required (the full file text).” · formatted text FAILED: {error} · formatted text Wrote {path}. Import it from a page script via '@app/{path.rsplit(“.”, 1) at 0}'. {reaches\_app}.

**Local steps**

- Set ref from \_app\_ref(ctx).
- If isinstance(ref, str).
  - Return ref.
- Set path from text\_arg(args.get(“file\_path”)).
- Set content from args.get(“content”).
- If not path.
  - Return “FAILED: file\_path is required.”.
- If not isinstance(content, str).
  - Return “FAILED: content is required (the full file text).”.
- Bind dependencies api, files.
- Attempt the following.
  - Evaluate api.write\_studio\_file(expanded ref, path, content).
- On failure (Exception) bound to error.
  - Return formatted text FAILED: {error}.
- Set reaches\_app from “It compiles in the browser, so there is no build to wait for.” when files.is\_db\_app(ref at 1), otherwise “Run trigger\_app\_build once your files are ready so the running app picks them up.”.
  - Value choice on files.is\_db\_app(ref at 1) — true gives “It compiles in the browser, so there is no build to wait for.”, false gives “Run trigger\_app\_build once your files are ready so the running app picks them up.”.
- Return formatted text Wrote {path}. Import it from a page script via '@app/{path.rsplit(“.”, 1) at 0}'. {reaches\_app}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1777)

<a id="op-f32e51b6ab6352"></a>
### Run delete app file

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_run_delete_app_file`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** ref · “FAILED: file\_path is required.” · formatted text FAILED: {error} · formatted text Deleted {path}..

**Local steps**

- Set ref from \_app\_ref(ctx).
- If isinstance(ref, str).
  - Return ref.
- Set path from text\_arg(args.get(“file\_path”)).
- If not path.
  - Return “FAILED: file\_path is required.”.
- Bind dependencies api.
- Attempt the following.
  - Evaluate api.delete\_studio\_file(expanded ref, path).
- On failure (Exception) bound to error.
  - Return formatted text FAILED: {error}.
- Return formatted text Deleted {path}..

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1773)

<a id="op-3cb5717bef5376"></a>
### Run trigger app build

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_run_trigger_app_build`

**Inputs** ctx, args.

**Declared result** str.

**State and service calls** enqueue doc with “Studio App”.

**Explicit results** ref · “Started an app rebuild. The file changes appear in the running app only after it finishes — tell the user to …”.

**Local steps**

- Set ref from \_app\_ref(ctx).
- If isinstance(ref, str).
  - Return ref.
- Set tuple(\_, studio\_app) from ref.
- Evaluate Platform.enqueue\_doc(“Studio App”, studio\_app, “build\_app\_bundle”, queue = “long”, timeout = 1200).
- Return “Started an app rebuild. The file changes appear in the running app only after it finishes — tell the user to …”.

**Values supplied outside this operation** service or queued work from Platform.enqueue\_doc(“Studio App”, studio\_app, “build\_app\_bundle”, queue = “long”, timeout = 1200).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1776)

<a id="op-cfa3b2451b4952"></a>
### App ref

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_app_ref`

**Inputs** ctx.

**Declared result** (tuple at tuple(str, str) bitwise or str).

**Explicit results** “FAILED: no page in context.” · tuple((page.Platform\_app or empty text), page.studio\_app).

**Local steps**

- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Return tuple((page.Platform\_app or empty text), page.studio\_app).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.Platform\_app → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1771)

<a id="op-75a184fcc4f9b9"></a>
### Flatten

`operation_foundation_binding_foundation_studio_ai_agent_tools_files_flatten`

**Inputs** nodes.

**Declared result** list at str.

**Explicit results** paths.

**Local steps**

- Set paths from list().
- For each node in nodes.
  - Evaluate paths.append((node at “path” + “/” when node at “is\_folder”, otherwise empty text)).
    - Value choice on node at “is\_folder” — true gives “/”, false gives empty text.
  - If node at “is\_folder”.
    - Evaluate paths.extend(\_flatten(node at “children”)).
- Return paths.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1772)

<a id="op-ac225b7c7b20c2"></a>
### Is db app

`operation_foundation_binding_foundation_studio_files_is_db_app`

**Inputs** studio\_app.

**Declared result** bool.

**Record and data access** read “Studio App” via get\_value.

**Explicit results** Platform.db.get\_value(“Studio App”, studio\_app, “is\_standard”) equals 0.

**Local steps**

- Return Platform.db.get\_value(“Studio App”, studio\_app, “is\_standard”) equals 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L230) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L37) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L125)

<a id="op-c6b19c7ded6204"></a>
### Is page script path

`operation_foundation_binding_foundation_studio_files_is_page_script_path`

**Inputs** path.

**Declared result** bool.

**Explicit results** bool(re.fullmatch(“studio\_page/(&#91;^/&#93;+)/\\1\\.(js\|ts)”, path)).

**Local steps**

- Return bool(re.fullmatch(“studio\_page/(&#91;^/&#93;+)/\\1\\.(js\|ts)”, path)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L234) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L41) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L129)
