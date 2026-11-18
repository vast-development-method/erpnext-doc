# Workflow, automation and dispatch · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Realtime

<a id="op-1cc4c99904e92e"></a>
### Publish to doc

`operation_foundation_realtime_initialize_business_behavior_publish_to_record`

**Inputs** doctype, docname, event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, doctype = doctype, docname = docname, after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, doctype = doctype, docname = docname, after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7276) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L290)

<a id="op-5920de38f37ca7"></a>
### Publish to doctype

`operation_foundation_realtime_initialize_business_behavior_publish_to_record_type`

**Inputs** doctype, event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, room = get\_doctype\_room(doctype), after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, room = get\_doctype\_room(doctype), after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7426) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L291)

<a id="op-eb8c9686753626"></a>
### Publish task progress

`operation_foundation_realtime_initialize_business_behavior_publish_task_progress`

**Inputs** task\_id, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(message = message, task\_id = task\_id, after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(message = message, task\_id = task\_id, after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7568) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L288)

<a id="op-7a48e3f1b9d042"></a>
### Publish to website

`operation_foundation_realtime_initialize_business_behavior_publish_to_website`

**Inputs** event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, room = get\_website\_room(), after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, room = get\_website\_room(), after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7685) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L294)

<a id="op-6640876c45caff"></a>
### Publish to all

`operation_foundation_realtime_initialize_business_behavior_publish_to_all`

**Inputs** event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, room = get\_site\_room(), after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, room = get\_site\_room(), after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L7810) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L289)

<a id="op-1b464e45dea846"></a>
### Publish to room

`operation_foundation_realtime_initialize_business_behavior_publish_to_room`

**Inputs** room, event, message = no value, after\_commit (named only, default false).

**Local steps**

- Evaluate publish\_realtime(event, message, room = room, after\_commit = after\_commit).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from publish\_realtime(event, message, room = room, after\_commit = after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L292)

<a id="op-5b249f477006bc"></a>
### Getattr

`operation_foundation_realtime_initialize_business_behavior_getattr`

**Inputs** name.

**Declared result** object.

**Explicit results** realtime · Socket.

**Explicit failure paths** AttributeError(formatted text module {\_\_name\_\_} has no attribute {name}).

**Local steps**

- If name equals “realtime”.
  - Bind dependencies realtime.
  - Return realtime.
- If name equals “Socket”.
  - Bind dependencies Socket.
  - Return Socket.
- Raise AttributeError(formatted text module {\_\_name\_\_} has no attribute {name}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L134) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L284)

## Service · Registry

<a id="op-3ffc1612808a78"></a>
### Get automations for

`operation_foundation_binding_foundation_automation_engine_registry_get_automations_for`

**Inputs** doctype.

**Declared result** list.

**Explicit results** Platform.client\_cache.get\_value(REGISTRY\_KEY.format(doctype), generator = deferred anonymous expression).

**Local steps**

- Return Platform.client\_cache.get\_value(REGISTRY\_KEY.format(doctype), generator = deferred anonymous expression).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L432)

<a id="op-aa50677bfb1671"></a>
### Build automations for

`operation_foundation_binding_foundation_automation_engine_registry_build_automations_for`

**Inputs** doctype.

**Declared result** list.

**Record and data access** read “Automation Flow” via get\_all.

**Explicit results** Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “document\_type” → doctype, “trigger\_type” → tuple(“in”, DOC\_TRIGGER\_TYPES)), fields = RULE\_FIELDS) · list().

**Local steps**

- Attempt the following.
  - Return Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “document\_type” → doctype, “trigger\_type” → tuple(“in”, DOC\_TRIGGER\_TYPES)), fields = RULE\_FIELDS).
- On failure (tuple(Platform.DoesNotExistError, Platform.db.TableMissingError)).
  - Return list().

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L428)

<a id="op-af3354479c9041"></a>
### Get custom event map

`operation_foundation_binding_foundation_automation_engine_registry_get_custom_event_map`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** Platform.client\_cache.get\_value(EVENTS\_KEY, generator = \_build\_custom\_event\_map).

**Local steps**

- Return Platform.client\_cache.get\_value(EVENTS\_KEY, generator = \_build\_custom\_event\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L433)

<a id="op-e3b89388dbd327"></a>
### Build custom event map

`operation_foundation_binding_foundation_automation_engine_registry_build_custom_event_map`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “Automation Flow” via get\_all.

**Explicit results** mapping() · event\_map.

**Local steps**

- Attempt the following.
  - Set rules from Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “trigger\_type” → “Custom Event”), fields = tuple(expanded RULE\_FIELDS, “custom\_event”, “document\_type”)).
- On failure (tuple(Platform.DoesNotExistError, Platform.db.TableMissingError)).
  - Return mapping().
- Set event\_map from mapping().
- For each rule in rules.
  - Evaluate event\_map.setdefault(rule.custom\_event, list()).append(rule).
- Return event\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L429)

<a id="op-8b9f028d670438"></a>
### Clear automation cache

`operation_foundation_binding_foundation_automation_engine_registry_clear_automation_cache`

**Inputs** doctype = no value.

**Local steps**

- If doctype.
  - Evaluate Platform.client\_cache.delete\_value(REGISTRY\_KEY.format(doctype)).
  - Evaluate Platform.client\_cache.delete\_value(EVENTS\_KEY).
- Otherwise.
  - Evaluate Platform.client\_cache.delete\_keys(REGISTRY\_KEY.format(empty text)).
- Evaluate \_clear\_request\_caches().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L430)

<a id="op-87ac67e0513946"></a>
### Clear request caches

`operation_foundation_binding_foundation_automation_engine_registry_clear_request_caches`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies \_providers.
- Bind dependencies \_ignored, derived\_definitions.
- Set cache from getattr(Platform.local, “request\_cache”, no value).
- For each func in tuple(\_providers, derived\_definitions, \_ignored).
  - If cache is distinct from no value.
    - Evaluate cache.pop(getattr(func, “\_\_wrapped\_\_”, func), no value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request\_cache”, no value), getattr(func, “\_\_wrapped\_\_”, func).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L431)

<a id="op-33538ef0162794"></a>
### Is async callable

`operation_foundation_realtime_registry_business_behavior_is_async_callable`

**Inputs** fn.

**Declared result** bool.

**Explicit results** true · (call is distinct from no value and inspect.iscoroutinefunction(call)).

**Local steps**

- If inspect.iscoroutinefunction(fn).
  - Return true.
- Set call from getattr(fn, “\_\_call\_\_”, no value).
- Return (call is distinct from no value and inspect.iscoroutinefunction(call)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in call is distinct from no value → inspect.iscoroutinefunction(call).

**Values supplied outside this operation** selected callable from getattr(fn, “\_\_call\_\_”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L5354) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L296)

<a id="op-38f8a3e74e887c"></a>
### Registry.initialize

`operation_foundation_realtime_registry_business_behavior_registry_initialize`

**Inputs** self.

**Local steps**

- Set self.\_handlers from mapping().
- Set self.\_current\_app from CORE\_APP.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L5500) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L300)

<a id="op-e1c487b86573de"></a>
### Registry.on

`operation_foundation_realtime_registry_business_behavior_registry_on`

**Inputs** self, event, Platform\_context (named only, default false), allow\_guest (named only, default false).

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L5564) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L301)

<a id="op-fa35bc30f09825"></a>
### Registry.on.decorator

`operation_foundation_realtime_registry_business_behavior_registry_on_decorator`

**Inputs** fn.

**Declared result** Callable.

**Explicit results** fn.

**Explicit failure paths** TypeError(formatted text {getattr(fn, “\_\_name\_\_”, fn)}: Platform\_context runs in a worker thread, so the handler must be a plain function, not 'async def'.).

**Local steps**

- If (Platform\_context and is\_async\_callable(fn)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform\_context → is\_async\_callable(fn).
  - Raise TypeError(formatted text {getattr(fn, “\_\_name\_\_”, fn)}: Platform\_context runs in a worker thread, so the handler must be a plain function, not 'async def'.).
- Set handler from Handler(event = event, fn = fn, Platform\_context = Platform\_context, allow\_guest = allow\_guest, …).
- Evaluate self.\_handlers.setdefault(event, list()).append(handler).
- Return fn.

**Values supplied outside this operation** selected callable from getattr(fn, “\_\_name\_\_”, fn).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L5877) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L302)

<a id="op-7e96ccd0e5f108"></a>
### Registry.importing app

`operation_foundation_realtime_registry_business_behavior_registry_importing_application`

**Inputs** self, app.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous from self.\_current\_app.
- Set self.\_current\_app from app.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Set self.\_current\_app from previous.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6134) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L299)

<a id="op-4d7b8a703ee162"></a>
### Registry.handlers for

`operation_foundation_realtime_registry_business_behavior_registry_handlers_for`

**Inputs** self, event.

**Declared result** list at Handler.

**Explicit results** self.\_handlers.get(event, list()).

**Local steps**

- Return self.\_handlers.get(event, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6251) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L298)

<a id="op-26ad826200419f"></a>
### Registry.events

`operation_foundation_realtime_registry_business_behavior_registry_events`

**Inputs** self.

**Declared result** Iterable at str.

**Explicit results** self.\_handlers.keys().

**Local steps**

- Return self.\_handlers.keys().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6337) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L297)

<a id="op-58d036afe6f7c8"></a>
### Discover app handlers

`operation_foundation_realtime_registry_business_behavior_discover_application_handlers`

**Inputs** sites\_path = no value.

**Declared result** no value.

**Local steps**

- Bind dependencies importlib.
- Bind dependencies importlib.util.
- Bind dependencies Platform.
- Set sites\_path from (sites\_path or getattr(Platform.local, “sites\_path”, no value) or “sites”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sites\_path → getattr(Platform.local, “sites\_path”, no value) → “sites”.
- For each app in Platform.get\_all\_apps(with\_internal\_apps = false, sites\_path = sites\_path).
  - If app equals CORE\_APP.
    - Continue with the next iteration or loop test.
  - Set module from formatted text {app}.realtime.handlers.
  - Attempt the following.
    - Set spec from importlib.util.find\_spec(module).
  - On failure (ModuleNotFoundError).
    - Set spec from no value.
  - If spec is identical to no value.
    - Continue with the next iteration or loop test.
  - Within realtime.importing\_app(app).
    - Evaluate importlib.import\_module(module).
  - Evaluate logger.info(“loaded realtime handlers from %s”, module).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “sites\_path”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6402) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L295)

## Service · Relationships

<a id="op-08778760055684"></a>
### Automation Relationship Provider.get definitions

`operation_foundation_binding_foundation_automation_engine_relationships_automationrelationshipprovider_get_definitions`

**Inputs** self, source\_doctype.

**Declared result** list at dict.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L435)

<a id="op-351f79b6aa26e2"></a>
### Automation Relationship Provider.resolve

`operation_foundation_binding_foundation_automation_engine_relationships_automationrelationshipprovider_resolve`

**Inputs** self, source\_doc, relationship, params.

**Declared result** list at dict.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L437)

<a id="op-ad89b8de4b5297"></a>
### Automation Relationship Provider.query

`operation_foundation_binding_foundation_automation_engine_relationships_automationrelationshipprovider_query`

**Inputs** self, source\_doc, relationship, filters, limit.

**Declared result** list at dict.

**Explicit results** \_query\_resolved(self, source\_doc, relationship, filters, …).

**Local steps**

- Return \_query\_resolved(self, source\_doc, relationship, filters, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L436)
