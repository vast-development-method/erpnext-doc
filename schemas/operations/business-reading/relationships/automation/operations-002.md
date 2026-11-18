# Relationship automation · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Events

<a id="op-3712b4ad62a9b8"></a>
### Emit overdue tasks

`operation_relationships_binding_crm_automation_events_emit_overdue_tasks`

**Inputs** no declared parameters.

**Record and data access** read “CRM Task” via get\_all.

**Explicit results** no value.

**Local steps**

- If not \_enabled().
  - Return no value.
- Set until from now().
- Set tasks from Platform.get\_all(“CRM Task”, filters = mapping(“status” → tuple(“not in”, OVERDUE\_STATUSES), “due\_date” → tuple(“between”, list(\_sweep\_start(until), until))), fields = list(“name”, “reference\_doctype”, “re ….
- For each task in tasks.
  - Evaluate \_emit\_overdue\_task(task).
- Evaluate Platform.db.set\_default(OVERDUE\_SWEEP\_KEY, until).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L91) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L247) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L228)

<a id="op-0bc6f883c4b515"></a>
### Sweep start

`operation_relationships_binding_crm_automation_events_sweep_start`

**Inputs** until.

**Explicit results** add\_to\_date(until, hours = negative 1) · max(get\_datetime(last), get\_datetime(floor)).

**Local steps**

- Set floor from add\_to\_date(until, hours = negative OVERDUE\_SWEEP\_MAX\_LOOKBACK\_HOURS).
- Set last from Platform.db.get\_default(OVERDUE\_SWEEP\_KEY).
- If not last.
  - Return add\_to\_date(until, hours = negative 1).
- Return max(get\_datetime(last), get\_datetime(floor)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L100) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L256) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L237)

<a id="op-c6dffa773015b7"></a>
### Emit overdue task

`operation_relationships_binding_crm_automation_events_emit_overdue_task`

**Inputs** task.

**Record and data access** resolve a document from “CRM Task” via get\_doc.

**Local steps**

- Set payload from mapping(“task” → task.name, “reference\_doctype” → task.reference\_doctype, “reference\_name” → task.reference\_docname, “due\_date” → str(task.due\_date)).
- Evaluate emit(“crm.task\_overdue”, doc = Platform.get\_doc(“CRM Task”, task.name), payload = payload, correlation\_key = task.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L90) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L246) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L227)

<a id="op-f28fc59b44a844"></a>
### Emit deal outcome

`operation_relationships_binding_crm_automation_events_emit_deal_outcome`

**Inputs** doc, payload.

**Record and data access** read “CRM Deal Status” via get\_cached\_value.

**Local steps**

- Set status\_type from Platform.get\_cached\_value(“CRM Deal Status”, doc.status, “type”) when doc.status, otherwise no value.
  - Value choice on doc.status — true gives Platform.get\_cached\_value(“CRM Deal Status”, doc.status, “type”), false gives no value.
- If status\_type equals “Won”.
  - Evaluate emit(“crm.deal\_won”, doc = doc, payload = payload, correlation\_key = doc.name).
- Otherwise.
  - If status\_type equals “Lost”.
    - Evaluate emit(“crm.deal\_lost”, doc = doc, payload = mapping(expand payload, “lost\_reason” → doc.lost\_reason), correlation\_key = doc.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“CRM Deal Status”, doc.status, “type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L88) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L244) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L225)

<a id="op-2165154f3974fa"></a>
### Emit correlated

`operation_relationships_binding_crm_automation_events_emit_correlated`

**Inputs** event, doc, payload, keys.

**Local steps**

- For each key in dict.fromkeys(generator of key for key drawn from keys where key).
  - Draw key from keys, keep a combination only if (key).
  - Evaluate emit(event, doc = doc, payload = payload, correlation\_key = key).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L87) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L243) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L224)

<a id="op-3c2ff20f2433bb"></a>
### Message payload

`operation_relationships_binding_crm_automation_events_message_payload`

**Inputs** doc, communication, channel, thread.

**Declared result** dict.

**Explicit results** mapping(“reference\_doctype” → doc.reference\_doctype, “reference\_name” → doc.reference\_name, “communication” → communication, “channel” → channel, …).

**Local steps**

- Return mapping(“reference\_doctype” → doc.reference\_doctype, “reference\_name” → doc.reference\_name, “communication” → communication, “channel” → channel, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L94) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L250) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L231)

<a id="op-8a7b4a6a4d54bb"></a>
### Email thread key

`operation_relationships_binding_crm_automation_events_email_thread_key`

**Inputs** doc.

**Declared result** (str bitwise or no value).

**Record and data access** read “Communication” via get\_value.

**Explicit results** (\_message\_key(doc.message\_id) or doc.name) · no value · (\_message\_key(parent) or doc.in\_reply\_to).

**Local steps**

- If doc.sent\_or\_received equals “Sent”.
  - Return (\_message\_key(doc.message\_id) or doc.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_message\_key(doc.message\_id) → doc.name.
- If not doc.in\_reply\_to.
  - Return no value.
- Set parent from Platform.db.get\_value(“Communication”, doc.in\_reply\_to, “message\_id”).
- Return (\_message\_key(parent) or doc.in\_reply\_to).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_message\_key(parent) → doc.in\_reply\_to.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L86) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L242) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L223)

<a id="op-aba41300f8c89d"></a>
### Message key

`operation_relationships_binding_crm_automation_events_message_key`

**Inputs** message\_id.

**Declared result** (str bitwise or no value).

**Explicit results** message\_id.strip(“&lt;&gt;”).strip() when message\_id, otherwise no value.

**Local steps**

- Return message\_id.strip(“&lt;&gt;”).strip() when message\_id, otherwise no value.
  - Value choice on message\_id — true gives message\_id.strip(“&lt;&gt;”).strip(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L93) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L249) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L230)

<a id="op-7cbbe038e55053"></a>
### Record key

`operation_relationships_binding_crm_automation_events_record_key`

**Inputs** doc.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text {doc.reference\_doctype}:{doc.reference\_name}.

**Local steps**

- If not (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return no value.
- Return formatted text {doc.reference\_doctype}:{doc.reference\_name}.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L99) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L255) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L236)

<a id="op-5d555131370a32"></a>
### Enabled

`operation_relationships_binding_crm_automation_events_enabled`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** (HAS\_AUTOMATION\_ENGINE and is\_enabled() and not Platform.flags.in\_install and not Platform.flags.in\_migrate).

**Local steps**

- Return (HAS\_AUTOMATION\_ENGINE and is\_enabled() and not Platform.flags.in\_install and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in HAS\_AUTOMATION\_ENGINE → is\_enabled() → not Platform.flags.in\_install → not Platform.flags.in\_migrate.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L92) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L248) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L229)

## Service · Reference flows

<a id="op-aa439d7375c5c6"></a>
### Install

`operation_relationships_binding_crm_automation_reference_flows_install`

**Inputs** enable = 0.

**Local steps**

- Evaluate ensure\_email\_templates().
- For each build in builders().
  - Set flow from build().
  - Set flow at “enabled” from Platform.utils.cint(enable).
  - Evaluate print(“installed:”, replace\_flow(flow)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L117) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L273) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L254)

<a id="op-4c12300054586a"></a>
### Uninstall

`operation_relationships_binding_crm_automation_reference_flows_uninstall`

**Inputs** no declared parameters.

**Record and data access** read “Automation Flow” via get\_value.

**State and service calls** request delete\_doc for “Automation Flow”.

**Local steps**

- For each title in list of build() at “title” for build drawn from builders().
  - Draw build from builders().
  - Set name from Platform.db.get\_value(“Automation Flow”, mapping(“title” → title), “name”).
  - If not name.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.delete\_doc(“Automation Flow”, name, force = true, ignore\_permissions = true).
  - Evaluate print(“removed:”, title).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L135) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L291) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L272)

<a id="op-af97063934694d"></a>
### Builders

`operation_relationships_binding_crm_automation_reference_flows_builders`

**Inputs** no declared parameters.

**Declared result** tuple.

**Explicit results** tuple(welcome\_sequence, reply\_temperature, profile\_scoring, assign\_on\_outreach, …).

**Local steps**

- Return tuple(welcome\_sequence, reply\_temperature, profile\_scoring, assign\_on\_outreach, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L105) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L261) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L242)

<a id="op-a594c30b898d66"></a>
### Replace flow

`operation_relationships_binding_crm_automation_reference_flows_replace_flow`

**Inputs** payload.

**Declared result** str.

**Record and data access** read “Automation Flow” via get\_value · resolve a document from payload via get\_doc.

**State and service calls** request delete\_doc for “Automation Flow” · call insert on Platform.get\_doc(payload).

**Explicit results** Platform.get\_doc(payload).insert(ignore\_permissions = true).title.

**Local steps**

- Set existing from Platform.db.get\_value(“Automation Flow”, mapping(“title” → payload at “title”), “name”).
- If existing.
  - Evaluate Platform.delete\_doc(“Automation Flow”, existing, force = true, ignore\_permissions = true).
- Return Platform.get\_doc(payload).insert(ignore\_permissions = true).title.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L126) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L282) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L263)

<a id="op-6f4a56d728cb03"></a>
### Ensure email templates

`operation_relationships_binding_crm_automation_reference_flows_ensure_email_templates`

**Inputs** no declared parameters.

**Record and data access** read “Email Template” via exists · resolve a document from mapping(“doctype” → “Email Template”, “name” → name, “subject” → subject, “response” → response, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Template”, “name” → name, “subject” → subject, “response” → response, …)).

**Local steps**

- For each tuple(name, tuple(subject, response)) in TEMPLATES.items().
  - If Platform.db.exists(“Email Template”, name).
    - Continue with the next iteration or loop test.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Template”, “name” → name, “subject” → subject, “response” → response, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L112) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L268) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L249)

<a id="op-1a121dddd572f3"></a>
### Welcome sequence

`operation_relationships_binding_crm_automation_reference_flows_welcome_sequence`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Welcome sequence by lead source”, “CRM Lead”, “Doc Created”), “actions” → list(step(1, “by\_source”, “If”, condition = “doc.source == "Website"”), email\_step(2, “welcome\_web”, “CRM Web  ….

**Local steps**

- Return mapping(expand flow(“Welcome sequence by lead source”, “CRM Lead”, “Doc Created”), “actions” → list(step(1, “by\_source”, “If”, condition = “doc.source == "Website"”), email\_step(2, “welcome\_web”, “CRM Web  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L136) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L292) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L273)

<a id="op-9f40d197cca320"></a>
### Reply temperature

`operation_relationships_binding_crm_automation_reference_flows_reply_temperature`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Lead temperature from reply”, “Communication”, “Doc Created”), “filters” → Platform.as\_json(list(list(“communication\_type”, “=”, “Communication”), list(“sent\_or\_received”, “=”, “Sent”) ….

**Local steps**

- Return mapping(expand flow(“Lead temperature from reply”, “Communication”, “Doc Created”), “filters” → Platform.as\_json(list(list(“communication\_type”, “=”, “Communication”), list(“sent\_or\_received”, “=”, “Sent”) ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L127) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L283) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L264)

<a id="op-d17988937443bd"></a>
### Title is senior

`operation_relationships_binding_crm_automation_reference_flows_title_is_senior`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** “ or ”.join(generator of formatted text "{word}" in (doc.job\_title or "").lower() for word drawn from SENIOR\_TITLES).

**Local steps**

- Return “ or ”.join(generator of formatted text "{word}" in (doc.job\_title or "").lower() for word drawn from SENIOR\_TITLES).
  - Draw word from SENIOR\_TITLES.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L133) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L289) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L270)

<a id="op-e3c649439ff9b4"></a>
### Profile scoring

`operation_relationships_binding_crm_automation_reference_flows_profile_scoring`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Lead scoring from the profile”, “CRM Lead”, “Doc Created”), “actions” → rows).

**Local steps**

- Set tuple(rows, idx) from tuple(list(), 1).
- For each tuple(key, label, condition, points) in SIGNALS.
  - Evaluate rows.append(step(idx, key, “If”, condition = condition)).
  - Evaluate rows.append(score((idx + 1), \_points\_key(key), points, label, parent = idx, branch = “If”)).
  - Update idx using + 2.
- Update rows using + \_source\_signal(idx).
- Update rows using + \_banding((idx + 3)).
- Return mapping(expand flow(“Lead scoring from the profile”, “CRM Lead”, “Doc Created”), “actions” → rows).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L122) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L278) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L259)

<a id="op-e672945a8204d2"></a>
### Source signal

`operation_relationships_binding_crm_automation_reference_flows_source_signal`

**Inputs** idx.

**Declared result** list at dict.

**Explicit results** list(step(idx, “inbound\_source”, “If”, condition = formatted text doc.source in {INBOUND\_SOURCES}), score((idx + 1), \_points\_key(“inbound\_source”), 20, “Inbound lead”, parent = idx, branch = “If”), score(( ….

**Local steps**

- Return list(step(idx, “inbound\_source”, “If”, condition = formatted text doc.source in {INBOUND\_SOURCES}), score((idx + 1), \_points\_key(“inbound\_source”), 20, “Inbound lead”, parent = idx, branch = “If”), score(( ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L129) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L285) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L266)

<a id="op-fad0c391a26fe6"></a>
### Banding

`operation_relationships_binding_crm_automation_reference_flows_banding`

**Inputs** idx.

**Declared result** list at dict.

**Explicit results** list(step(idx, “is\_hot”, “If”, condition = \_total\_at\_least(HOT\_AT)), temperature((idx + 1), “mark\_hot”, “Hot”, target = “trigger”, parent = idx, branch = “If”), step((idx + 2), “is\_warm”, “If”, condition = ….

**Local steps**

- Return list(step(idx, “is\_hot”, “If”, condition = \_total\_at\_least(HOT\_AT)), temperature((idx + 1), “mark\_hot”, “Hot”, target = “trigger”, parent = idx, branch = “If”), step((idx + 2), “is\_warm”, “If”, condition = ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L104) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L260) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L241)

<a id="op-967ec44195ef23"></a>
### Points key

`operation_relationships_binding_crm_automation_reference_flows_points_key`

**Inputs** key.

**Declared result** str.

**Explicit results** formatted text {key}\_points.

**Local steps**

- Return formatted text {key}\_points.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L121) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L277) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L258)

<a id="op-f80221a4d1cba4"></a>
### Total at least

`operation_relationships_binding_crm_automation_reference_flows_total_at_least`

**Inputs** threshold.

**Declared result** str.

**Explicit results** formatted text ({awarded}) &gt;= {threshold}.

**Local steps**

- Set keys from list of \_points\_key(signal at 0) for signal drawn from SIGNALS.
  - Draw signal from SIGNALS.
- Update keys using + list(\_points\_key(“inbound\_source”), \_points\_key(“outbound\_source”)).
- Set awarded from “ + ”.join(generator of formatted text context&#91;"steps"&#93;.get("{key}", {}).get("delta", 0) for key drawn from keys).
  - Draw key from keys.
- Return formatted text ({awarded}) &gt;= {threshold}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L134) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L290) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L271)

<a id="op-c15d87600cbce8"></a>
### Assign on outreach

`operation_relationships_binding_crm_automation_reference_flows_assign_on_outreach`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Assign the lead when we email it”, “Communication”, “Doc Created”), “filters” → Platform.as\_json(list(list(“communication\_type”, “=”, “Communication”), list(“sent\_or\_received”, “=”, “S ….

**Local steps**

- Return mapping(expand flow(“Assign the lead when we email it”, “Communication”, “Doc Created”), “filters” → Platform.as\_json(list(list(“communication\_type”, “=”, “Communication”), list(“sent\_or\_received”, “=”, “S ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L102) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L258) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L239)
