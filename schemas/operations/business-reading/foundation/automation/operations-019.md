# Workflow, automation and dispatch · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Drainer

<a id="op-750288e55094e4"></a>
### Has due pending

`operation_foundation_binding_foundation_automation_engine_drainer_has_due_pending`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(nested operand in the contract.where((nested operand in the contract bitwise or nested operand in the contract)).limit(1).run()).

**Local steps**

- Set queue from Platform.qb.DocType(QUEUE).
- Return bool(nested operand in the contract.where((nested operand in the contract bitwise or nested operand in the contract)).limit(1).run()).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L394)

<a id="op-27bed9317691c9"></a>
### Drain due

`operation_foundation_binding_foundation_automation_engine_drainer_drain_due`

**Inputs** no declared parameters.

**Local steps**

- Evaluate requeue\_stale\_running().
- Evaluate drain().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L386)

<a id="op-21e224e0f038d8"></a>
### Requeue stale running

`operation_foundation_binding_foundation_automation_engine_drainer_requeue_stale_running`

**Inputs** no declared parameters.

**Local steps**

- Set cutoff from add\_to\_date(now(), minutes = negative cint(settings.get(“stale\_running\_minutes”))).
- Set queue from Platform.qb.DocType(QUEUE).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.status equals “Running”).where(queue.modified &lt; cutoff).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L399)

<a id="op-9639e3521336f6"></a>
### Purge queue

`operation_foundation_binding_foundation_automation_engine_drainer_purge_queue`

**Inputs** no declared parameters.

**State and service calls** request delete on QUEUE · request delete on “Automation Event Subscription”.

**Local steps**

- Set cutoff from add\_days(now(), negative cint(settings.get(“queue\_retention\_days”))).
- Evaluate Platform.db.delete(QUEUE, mapping(“status” → tuple(“in”, tuple(“Failed”, “Skipped”)), “modified” → tuple(“&lt;”, cutoff))).
- Evaluate Platform.db.delete(“Automation Event Subscription”, mapping(“status” → tuple(“in”, tuple(“Matched”, “Timed Out”, “Cancelled”)), “modified” → tuple(“&lt;”, cutoff))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L397)

## Service · Embedder

<a id="op-fb4d9024624db3"></a>
### Embed texts

`operation_foundation_binding_foundation_flow_knowledge_embedder_embed_texts`

**Inputs** texts.

**Declared result** list at list at float.

**Explicit results** list() · vectors.

**Local steps**

- If not texts.
  - Return list().
- Set config from \_embedding\_config().
- Set vectors from list().
- For each start in range(0, len(texts), BATCH\_SIZE).
  - Evaluate vectors.extend(\_embed\_batch(texts at slice start to (start + BATCH\_SIZE), config, timeout = EMBED\_TIMEOUT)).
- Return vectors.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1153)

<a id="op-9c82e109871e68"></a>
### Probe dimension

`operation_foundation_binding_foundation_flow_knowledge_embedder_probe_dimension`

**Inputs** model.

**Declared result** int.

**Explicit results** len(vector).

**Local steps**

- Set config from \_model\_config(model).
- Set tuple(vector) from \_embed\_batch(list(“dimension probe”), config, timeout = PROBE\_TIMEOUT).
- Return len(vector).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1157)

<a id="op-58ecfe5788c494"></a>
### Embedding config

`operation_foundation_binding_foundation_flow_knowledge_embedder_embedding_config`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from “Flow Knowledge Settings” via get\_cached\_doc.

**Explicit results** \_model\_config(settings.embedding\_model).

**Explicit failure paths** validation helper — translated “Set an embedding model in Flow Knowledge Settings first.”.

**Local steps**

- Set settings from Platform.get\_cached\_doc(“Flow Knowledge Settings”).
- If not settings.embedding\_model.
  - Call the validation error handler Platform.throw(translated “Set an embedding model in Flow Knowledge Settings first.”, title = translated “Knowledge Not Configured”).
- Return \_model\_config(settings.embedding\_model).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Flow Knowledge Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1154)

<a id="op-10b8ca55b955d5"></a>
### Model config

`operation_foundation_binding_foundation_flow_knowledge_embedder_model_config`

**Inputs** model.

**Declared result** dict at tuple(str, Any).

**Record and data access** resolve a document from “Flow Model” via get\_doc.

**Explicit results** config.

**Explicit failure paths** validation helper — translated “Flow Model {0} is disabled.”.format(model).

**Local steps**

- Bind dependencies litellm\_route, resolve\_provider\_credentials.
- Set doc from Platform.get\_doc(“Flow Model”, model).
- If not doc.enabled.
  - Call the validation error handler Platform.throw(translated “Flow Model {0} is disabled.”.format(model), title = translated “Model Disabled”).
- Set provider\_creds from resolve\_provider\_credentials(doc.model\_id, doc.provider).
- Set tuple(model\_id, base\_url) from litellm\_route(doc.model\_id, (doc.base\_url or provider\_creds.get(“base\_url”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.base\_url → provider\_creds.get(“base\_url”).
- Set config from mapping(expand doc.model\_params(), “model” → model\_id, “api\_key” → (doc.get\_password(“api\_key”, raise\_exception = false) or provider\_creds.get(“api\_key”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_password(“api\_key”, raise\_exception = false) → provider\_creds.get(“api\_key”) → empty text.
- If base\_url.
  - Set config at “api\_base” from base\_url.
- Return config.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1156)

<a id="op-a734f30c4b016b"></a>
### Embed batch

`operation_foundation_binding_foundation_flow_knowledge_embedder_embed_batch`

**Inputs** texts, config, timeout (named only).

**Declared result** list at list at float.

**Explicit results** vectors.

**Explicit failure paths** validation helper — (str(e) at slice no value to 500 or type(e).\_\_name\_\_) · validation helper — translated “Embedding provider returned {0} vectors for {1} inputs.”.format(len(vectors), len(texts)).

**Local steps**

- Bind dependencies litellm.
- Attempt the following.
  - Set response from litellm.embedding(input = texts, timeout = timeout, expanded names config).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw((str(e) at slice no value to 500 or type(e).\_\_name\_\_), title = translated “Embedding Failed”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(e) at slice no value to 500 → type(e).\_\_name\_\_.
- Set entries from sorted(response.data, key = deferred anonymous expression).
- Set vectors from list of list of float(value) for value drawn from \_get(entry, “embedding”) for entry drawn from entries.
  - Draw entry from entries.
  - Draw value from \_get(entry, “embedding”).
- If len(vectors) differs from len(texts).
  - Call the validation error handler Platform.throw(translated “Embedding provider returned {0} vectors for {1} inputs.”.format(len(vectors), len(texts)), title = translated “Embedding Failed”).
- Return vectors.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1152)

<a id="op-5221975face60d"></a>
### Get

`operation_foundation_binding_foundation_flow_knowledge_embedder_get`

**Inputs** entry, key.

**Declared result** Any.

**Explicit results** entry.get(key) when isinstance(entry, dict), otherwise getattr(entry, key, no value).

**Local steps**

- Return entry.get(key) when isinstance(entry, dict), otherwise getattr(entry, key, no value).
  - Value choice on isinstance(entry, dict) — true gives entry.get(key), false gives getattr(entry, key, no value).

**Values supplied outside this operation** selected callable from getattr(entry, key, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1155)

## Service · Events

<a id="op-17595633a23ce6"></a>
### Emit

`operation_foundation_binding_foundation_automation_engine_events_emit`

**Inputs** event, doc = no value, payload = no value, correlation\_key = no value.

**Declared result** dict.

**Explicit results** mapping(“queued” → queued, “resumed” → resumed).

**Local steps**

- Evaluate validate\_event(event).
- Set payload from mapping(expand (payload or mapping()), “event\_name” → event).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payload → mapping().
- Evaluate \_validate\_payload\_size(payload).
- Set queued from \_queue\_event\_flows(event, doc, payload).
- Set resumed from \_claim\_subscriptions(event, correlation\_key, payload).
- If (queued or resumed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in queued → resumed.
  - Evaluate Platform.db.after\_commit.add(kick\_drainer).
- Return mapping(“queued” → queued, “resumed” → resumed).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L406)

<a id="op-36294c9684e454"></a>
### Schedule event wait

`operation_foundation_binding_foundation_automation_engine_events_schedule_event_wait`

**Inputs** context, params, step\_key, resume\_from\_idx.

**Record and data access** resolve a document from resume\_row\_values(context, expires\_at, resume\_from\_idx) via get\_doc · resolve a document from mapping(“doctype” → SUBSCRIPTION, “event\_name” → params at “event\_name”, “correlation\_key” → correlation, “run” → context at “run”.name, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(resume\_row\_values(context, expires\_at, resume\_from\_idx)) · call insert on Platform.get\_doc(mapping(“doctype” → SUBSCRIPTION, “event\_name” → params at “event\_name”, “correlation\_key” → correlation, “run” → context at “run”.name, …)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → SUBSCRIPTION, “event\_name” → params at “event\_name”, “correlation\_key” → correlation, “run” → context at “run”.name, …)).insert(ignore\_permissions = true).

**Explicit failure paths** validation helper — translated “Wait for Event correlation key rendered empty”.

**Local steps**

- Bind dependencies resume\_row\_values.
- Evaluate validate\_wait\_params(params).
- Set correlation from \_render(params at “correlation\_key”, context).
- If not correlation.
  - Call the validation error handler Platform.throw(translated “Wait for Event correlation key rendered empty”).
- Set expires\_at from add\_to\_date(now(), seconds = \_timeout\_seconds(params)).
- Set queue from Platform.get\_doc(resume\_row\_values(context, expires\_at, resume\_from\_idx)).insert(ignore\_permissions = true).
- Return Platform.get\_doc(mapping(“doctype” → SUBSCRIPTION, “event\_name” → params at “event\_name”, “correlation\_key” → correlation, “run” → context at “run”.name, …)).insert(ignore\_permissions = true).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L416)

<a id="op-07c15903f06fa1"></a>
### Get wait outcome

`operation_foundation_binding_foundation_automation_engine_events_get_wait_outcome`

**Inputs** row.

**Declared result** (dict bitwise or no value).

**Record and data access** read SUBSCRIPTION via get\_value.

**State and service calls** call db\_set on subscription.

**Explicit results** no value · mapping(“outcome” → subscription.status, “event\_name” → subscription.event\_name, “payload” → Platform.parse\_json(subscription.event\_payload) when subscription.event\_payload, otherwise mapping()).

**Local steps**

- Set name from Platform.db.get\_value(SUBSCRIPTION, mapping(“resume\_queue” → row.name), “name”).
- If not name.
  - Return no value.
- Set subscription from \_lock\_subscription(name).
- If subscription.status equals “Waiting”.
  - Evaluate subscription.db\_set(“status”, “Timed Out”, update\_modified = false).
- Return mapping(“outcome” → subscription.status, “event\_name” → subscription.event\_name, “payload” → Platform.parse\_json(subscription.event\_payload) when subscription.event\_payload, otherwise mapping()).
  - Value choice on subscription.event\_payload — true gives Platform.parse\_json(subscription.event\_payload), false gives mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L409)

<a id="op-56865d1db31b02"></a>
### Registered events

`operation_foundation_binding_foundation_automation_engine_events_registered_events`

**Inputs** doctype = no value.

**Declared result** list at dict.

**Explicit results** options · list of option for option drawn from options where doctype belongs to option at “subject\_doctypes”.

**Local steps**

- Set options from list of \_event\_option(name, schema) for tuple(name, schema) drawn from sorted(\_registered\_events().items()).
  - Draw tuple(name, schema) from sorted(\_registered\_events().items()).
- If not doctype.
  - Return options.
- Return list of option for option drawn from options where doctype belongs to option at “subject\_doctypes”.
  - Draw option from options, keep a combination only if (doctype belongs to option at “subject\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L413)

<a id="op-1b3f4942bb46b0"></a>
### Event option

`operation_foundation_binding_foundation_automation_engine_events_event_option`

**Inputs** name, schema.

**Declared result** dict.

**Explicit results** mapping(“value” → name, “label” → (schema.get(“label”) or \_prettify(name)), “description” → (schema.get(“description”) or empty text), “correlation\_options” → (schema.get(“correlation\_options”) or list()), …).

**Local steps**

- Set schema from schema when isinstance(schema, dict), otherwise mapping().
  - Value choice on isinstance(schema, dict) — true gives schema, false gives mapping().
- Return mapping(“value” → name, “label” → (schema.get(“label”) or \_prettify(name)), “description” → (schema.get(“description”) or empty text), “correlation\_options” → (schema.get(“correlation\_options”) or list()), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema.get(“label”) → \_prettify(name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema.get(“description”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in schema.get(“correlation\_options”) → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L407)

<a id="op-7e2af6497b9647"></a>
### Subject doctypes

`operation_foundation_binding_foundation_automation_engine_events_subject_doctypes`

**Inputs** subject.

**Declared result** list at str.

**Explicit results** list() · list(subject at “doctype”) · list((subject.get(“doctypes”) or list())).

**Local steps**

- If not isinstance(subject, dict).
  - Return list().
- If subject.get(“doctype”).
  - Return list(subject at “doctype”).
- Return list((subject.get(“doctypes”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in subject.get(“doctypes”) → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L417)

<a id="op-e7359459d04f37"></a>
### Event subject

`operation_foundation_binding_foundation_automation_engine_events_event_subject`

**Inputs** event, payload.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“doctype” → doctype, “name” → name).

**Local steps**

- Set subject from (\_registered\_events().get(event) or mapping()).get(“subject”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_registered\_events().get(event) → mapping().
- If not isinstance(subject, dict).
  - Return no value.
- Set doctype from (subject.get(“doctype”) or (payload or mapping()).get((subject.get(“doctype\_key”) or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in subject.get(“doctype”) → (payload or mapping()).get((subject.get(“doctype\_key”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payload → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in subject.get(“doctype\_key”) → empty text.
- Set name from (payload or mapping()).get((subject.get(“name\_key”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payload → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in subject.get(“name\_key”) → empty text.
- If (not doctype or not name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not name.
  - Return no value.
- Set allowed from \_subject\_doctypes(subject).
- If (allowed and doctype does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed → doctype does not belong to allowed.
  - Return no value.
- Return mapping(“doctype” → doctype, “name” → name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L408)

<a id="op-01cfd33604188b"></a>
### Prettify

`operation_foundation_binding_foundation_automation_engine_events_prettify`

**Inputs** name.

**Declared result** str.

**Explicit results** nested operand in the contract.split(“.”) at negative 1.replace(“\_”, one space).capitalize().

**Local steps**

- Return nested operand in the contract.split(“.”) at negative 1.replace(“\_”, one space).capitalize().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L411)

<a id="op-76b1a92369dc58"></a>
### Validate event

`operation_foundation_binding_foundation_automation_engine_events_validate_event`

**Inputs** event.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unregistered automation event: {0}”.format(event).

**Local steps**

- If event belongs to \_registered\_events().
  - Return no value.
- If settings.get(“allow\_unregistered\_events”).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Unregistered automation event: {0}”.format(event)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L420)

<a id="op-d4b8bb50260010"></a>
### Validate wait params

`operation_foundation_binding_foundation_automation_engine_events_validate_wait_params`

**Inputs** params.

**Explicit failure paths** validation helper — translated “Wait for Event requires a correlation key” · validation helper — translated “Wait for Event requires a timeout” · validation helper — translated “Wait for Event timeout unit must be one of {0}”.format(“, ”.join(TIMEOUT\_UNITS)).

**Local steps**

- Evaluate validate\_event(params.get(“event\_name”)).
- If not params.get(“correlation\_key”).
  - Call the validation error handler Platform.throw(translated “Wait for Event requires a correlation key”).
- If not cint(params.get(“timeout\_value”)).
  - Call the validation error handler Platform.throw(translated “Wait for Event requires a timeout”).
- If params.get(“timeout\_unit”) does not belong to TIMEOUT\_UNITS.
  - Call the validation error handler Platform.throw(translated “Wait for Event timeout unit must be one of {0}”.format(“, ”.join(TIMEOUT\_UNITS))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L422)

<a id="op-1e6729192dfd1a"></a>
### Registered events

`operation_foundation_binding_foundation_automation_engine_events_registered_events_81d0a86361f3`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** events.

**Local steps**

- Set events from mapping().
- For each value in Platform.get\_hooks(“automation\_events”).
  - If isinstance(value, str).
    - Evaluate events.setdefault(value, mapping()).
  - Otherwise.
    - Evaluate events.update(value).
- Return events.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“automation\_events”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L414)

<a id="op-4d581bcb50dd47"></a>
### Queue event flows

`operation_foundation_binding_foundation_automation_engine_events_queue_event_flows`

**Inputs** event, doc, payload.

**Declared result** int.

**Explicit results** queued.

**Local steps**

- Set queued from 0.
- Set occurrence from Platform.generate\_hash(length = 20).
- Set subject\_doc from \_subject\_document(event, payload).
- For each rule in get\_custom\_event\_map().get(event, list()).
  - Set target from subject\_doc when (subject\_doc and rule.document\_type equals subject\_doc.doctype), otherwise doc.
    - Value choice on (subject\_doc and rule.document\_type equals subject\_doc.doctype) — true gives subject\_doc, false gives doc.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in subject\_doc → rule.document\_type equals subject\_doc.doctype.
  - If (rule.document\_type and (not target or target.doctype differs from rule.document\_type)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.document\_type → (not target or target.doctype differs from rule.document\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not target → target.doctype differs from rule.document\_type.
    - Continue with the next iteration or loop test.
  - If (target and not matches\_rule(rule, target)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in target → not matches\_rule(rule, target).
    - Continue with the next iteration or loop test.
  - Evaluate queue\_trigger(rule.name, target.doctype when target, otherwise no value, target.name when target, otherwise occurrence, payload = payload).
    - Value choice on target — true gives target.doctype, false gives no value.
    - Value choice on target — true gives target.name, false gives occurrence.
  - Update queued using + 1.
- Return queued.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 20).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L412)

<a id="op-403e1fc79ae59a"></a>
### Subject document

`operation_foundation_binding_foundation_automation_engine_events_subject_document`

**Inputs** event, payload.

**Record and data access** read reference at “doctype” via exists · resolve a document from reference at “doctype” via get\_doc.

**Explicit results** no value · Platform.get\_doc(reference at “doctype”, reference at “name”).

**Local steps**

- Set reference from event\_subject(event, payload).
- If not reference.
  - Return no value.
- If not Platform.db.exists(reference at “doctype”, reference at “name”).
  - Return no value.
- Return Platform.get\_doc(reference at “doctype”, reference at “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L418)

<a id="op-74c9c49d667c97"></a>
### Claim subscriptions

`operation_foundation_binding_foundation_automation_engine_events_claim_subscriptions`

**Inputs** event, correlation\_key, payload.

**Declared result** int.

**Record and data access** read SUBSCRIPTION via get\_all.

**Explicit results** 0 · sum(generator of \_claim\_subscription(name, payload) for name drawn from names).

**Local steps**

- If not correlation\_key.
  - Return 0.
- Set names from Platform.get\_all(SUBSCRIPTION, filters = mapping(“event\_name” → event, “correlation\_key” → correlation\_key, “status” → “Waiting”), pluck = “name”).
- Return sum(generator of \_claim\_subscription(name, payload) for name drawn from names).
  - Draw name from names.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L405)
