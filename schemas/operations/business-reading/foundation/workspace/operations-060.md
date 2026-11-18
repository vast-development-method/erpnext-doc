# Forms, reports and navigation · operations 60

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sidebar

[Record definition](../../../../data/record-types/sidebar.json)

<a id="op-fe9a354eddbfc6"></a>
### Validate item route

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_validate_item_route`

**Inputs** item.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only a Page item has a route inside it. {0} links a {1}.”.format(Platform.bold((item.get(“label”) or item.get(“link\_to”))), item.get(“link\_type”)) · validation helper — translated “{0} is not a path inside a page. Give a relative path, with no query or fragment.”.format(Platform.bold(route)).

**Local steps**

- Set item.route from ((item.get(“route”) or empty text).strip() or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item.get(“route”) or empty text).strip() → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“route”) → empty text.
- Set route from item.route.
- If not route.
  - Return no value.
- If item.get(“link\_type”) differs from “Page”.
  - Call the validation error handler Platform.throw(translated “Only a Page item has a route inside it. {0} links a {1}.”.format(Platform.bold((item.get(“label”) or item.get(“link\_to”))), item.get(“link\_type”)), title = translated “Route Not Allowed”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“label”) → item.get(“link\_to”).
- Set segments from route.split(“/”).
- If (route.startswith(“/”) or “:” belongs to segments at 0 or “..” belongs to segments or “?” belongs to route or “#” belongs to route).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in route.startswith(“/”) → “:” belongs to segments at 0 → “..” belongs to segments → “?” belongs to route → “#” belongs to route.
  - Call the validation error handler Platform.throw(translated “{0} is not a path inside a page. Give a relative path, with no query or fragment.”.format(Platform.bold(route)), title = translated “Invalid Route”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L756)

<a id="op-9983b409337636"></a>
### Item key

`operation_foundation_desk_record_definitions_sidebar_business_behavior_item_key`

**Inputs** item.

**Declared result** str.

**Explicit results** formatted text {key}\|{route} when route, otherwise key · (item.get(“key”) or unlinked\_key(item)).

**Local steps**

- If is\_linked(item).
  - Set tuple(expanded columns, route) from generator of (item.get(field) or empty text) for field drawn from LINKED\_IDENTITY\_FIELDS.
    - Draw field from LINKED\_IDENTITY\_FIELDS.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(field) → empty text.
  - Set key from “\|”.join(columns).
  - Return formatted text {key}\|{route} when route, otherwise key.
    - Value choice on route — true gives formatted text {key}\|{route}, false gives key.
- Return (item.get(“key”) or unlinked\_key(item)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“key”) → unlinked\_key(item).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L31) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1014)

<a id="op-140314b1e37279"></a>
### Unlinked key

`operation_foundation_desk_record_definitions_sidebar_business_behavior_unlinked_key`

**Inputs** item.

**Declared result** str.

**Explicit results** hashlib.sha1(identity.encode()).hexdigest() at slice no value to 10.

**Local steps**

- Set identity from formatted text {(item.get(“type”) or empty text)}\|{(item.get(“label”) or empty text)}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“type”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“label”) → empty text.
- Return hashlib.sha1(identity.encode()).hexdigest() at slice no value to 10.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L1974) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1046)

<a id="op-5f20cb6e442c07"></a>
### Majority module of

`operation_foundation_desk_record_definitions_sidebar_business_behavior_majority_module_of`

**Inputs** rows.

**Declared result** (str bitwise or no value).

**Record and data access** read “DocType” via exists · read row.link\_type via get\_value.

**Explicit results** counts.most\_common(1) at 0 at 0 when counts, otherwise no value.

**Local steps**

- Set modules from list().
- For each row in rows.
  - If (not row.get(“link\_to”) or row.get(“link\_type”) belongs to tuple(no value, empty text, “URL”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.get(“link\_to”) → row.get(“link\_type”) belongs to tuple(no value, empty text, “URL”).
    - Continue with the next iteration or loop test.
  - If not Platform.db.exists(“DocType”, row.link\_type).
    - Continue with the next iteration or loop test.
  - If module bound to Platform.db.get\_value(row.link\_type, row.link\_to, “module”).
    - Evaluate modules.append(module).
- Set counts from Counter(modules).
- Return counts.most\_common(1) at 0 at 0 when counts, otherwise no value.
  - Value choice on counts — true gives counts.most\_common(1) at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L2169) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1015)

<a id="op-c4443dac16b8aa"></a>
### Pick primary

`operation_foundation_desk_record_definitions_sidebar_business_behavior_pick_primary`

**Inputs** module, workspaces.

**Declared result** Platform.\_dict.

**Explicit results** workspace · sorted(workspaces, key = deferred anonymous expression) at 0.

**Local steps**

- For each workspace in workspaces.
  - If workspace.name equals module.
    - Return workspace.
- Return sorted(workspaces, key = deferred anonymous expression) at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L2533) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1022)

<a id="op-99f10751e200ec"></a>
### Display title

`operation_foundation_desk_record_definitions_sidebar_business_behavior_display_title`

**Inputs** module, primary, is\_merge.

**Declared result** str.

**Explicit results** module when is\_merge, otherwise (primary.title or primary.name).

**Local steps**

- Return module when is\_merge, otherwise (primary.title or primary.name).
  - Value choice on is\_merge — true gives module, false gives (primary.title or primary.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in primary.title → primary.name.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L2744) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L997)

<a id="op-c4cbfb35ba6446"></a>
### Merge items

`operation_foundation_desk_record_definitions_sidebar_business_behavior_merge_items`

**Inputs** primary, secondaries.

**Declared result** list at dict.

**Explicit results** merged.

**Local steps**

- Set merged from list().
- Set seen from set().
- Bind local operation take for subsequent calls.
- For each item in primary.rows.
  - Evaluate take(item).
- For each secondary in secondaries.
  - Set section from mapping(“type” → “Section Break”, “label” → (secondary.title or secondary.name), “collapsible” → 1, “keep\_closed” → 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in secondary.title → secondary.name.
  - Evaluate merged.append(section).
  - Evaluate seen.add(item\_key(section)).
  - For each item in secondary.rows.
    - Evaluate take(item, force\_child = true).
- Return merged.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L2843) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1018)

<a id="op-3c344b3c13f790"></a>
### Merge items.take

`operation_foundation_desk_record_definitions_sidebar_business_behavior_merge_items_take`

**Inputs** item, force\_child = false.

**Explicit results** no value.

**Local steps**

- Set key from item\_key(item).
- If key belongs to seen.
  - Return no value.
- Evaluate seen.add(key).
- Set row from mapping of field → item.get(field) for field drawn from SIDEBAR\_ITEM\_FIELDS.
  - Draw field from SIDEBAR\_ITEM\_FIELDS.
- If (force\_child and item.get(“type”) differs from “Section Break”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in force\_child → item.get(“type”) differs from “Section Break”.
  - Set row at “child” from 1.
- Evaluate merged.append(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L3471) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1019)

<a id="op-a6c1d550cb41e2"></a>
### Options as filters

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_options_as_filters`

**Inputs** row.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (row.get(“filters”) or not row.get(“route\_options”) or row.get(“link\_type”) belongs to tuple(“Page”, “URL”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“filters”) → not row.get(“route\_options”) → row.get(“link\_type”) belongs to tuple(“Page”, “URL”).
  - Return no value.
- Attempt the following.
  - Set options from json.loads(row.route\_options).
- On failure (ValueError).
  - Return no value.
- If (not isinstance(options, dict) or not options).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(options, dict) → not options.
  - Return no value.
- Set row.filters from json.dumps(list of list(row.link\_to, field, expanded value) when (isinstance(value, list) and len(value) equals 2), otherwise list(row.link\_to, field, “=”, value) for tuple(field, value) drawn from options.items()).
  - Draw tuple(field, value) from options.items().
  - Value choice on (isinstance(value, list) and len(value) equals 2) — true gives list(row.link\_to, field, expanded value), false gives list(row.link\_to, field, “=”, value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, list) → len(value) equals 2.
- Set row.route\_options from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L739)

<a id="op-9d01237a73d9f2"></a>
### Build sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_build_sidebar`

**Inputs** module, workspaces.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(mapping(“module” → module, “title” → display\_title(module, primary, bool(secondaries)), “header\_icon” → primary.icon, “app” → get\_module\_placement(module), …)).

**Local steps**

- Set primary from pick\_primary(module, workspaces).
- Set secondaries from list of ws for ws drawn from workspaces where ws.name differs from primary.name.
  - Draw ws from workspaces, keep a combination only if (ws.name differs from primary.name).
- Return Platform.\_dict(mapping(“module” → module, “title” → display\_title(module, primary, bool(secondaries)), “header\_icon” → primary.icon, “app” → get\_module\_placement(module), …)).
  - Draw ws from workspaces.
  - Draw ws from secondaries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L3743) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L991)

<a id="op-b418757f8bb8db"></a>
### Get module contents

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_module_contents`

**Inputs** modules.

**Declared result** dict at tuple(str, dict at tuple(str, list)).

**Record and data access** read entity via get\_all.

**Explicit results** mapping of module → arrange\_contents(held) for tuple(module, held) drawn from contents.items().

**Local steps**

- Set contents from mapping of module → mapping of entity → list() for entity drawn from MODULE\_CONTENT\_ENTITIES for module drawn from modules.
  - Draw module from modules.
  - Draw entity from MODULE\_CONTENT\_ENTITIES.
- For each entity in MODULE\_CONTENT\_ENTITIES.
  - Set filters from mapping(“module” → list(“in”, modules)).
  - Set fields from list(“name”, “module”).
  - If entity equals “DocType”.
    - Set filters at “istable” from 0.
  - If entity equals “Workspace”.
    - Set filters at “public” from 1.
    - Evaluate fields.append(“icon”).
  - If entity equals “Page”.
    - Evaluate fields.append(“title”).
  - For each row in Platform.get\_all(entity, filters = filters, fields = fields, order\_by = “creation asc”).
    - If bucket bound to contents.get(row.module).
      - Evaluate bucket at entity.append(row).
- Return mapping of module → arrange\_contents(held) for tuple(module, held) drawn from contents.items().
  - Draw tuple(module, held) from contents.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L4193) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1004)

<a id="op-b835272d95312d"></a>
### Arrange contents

`operation_foundation_desk_record_definitions_sidebar_business_behavior_arrange_contents`

**Inputs** held.

**Declared result** dict at tuple(str, list).

**Explicit results** held.

**Local steps**

- Set dropped from max(0, (len(held at “DocType”) − COMPUTED\_DOCTYPE\_LIMIT)).
- Set held at “DocType” from held at “DocType” at slice no value to COMPUTED\_DOCTYPE\_LIMIT.
- If not held at “Workspace”.
  - Set held from mapping(“DocType” → held at “DocType”, expand held).
- If dropped.
  - Set held at OVERFLOW\_KEY from dropped.
- Return held.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L4792) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L989)

<a id="op-7d2eef4f320c21"></a>
### Generate items

`operation_foundation_desk_record_definitions_sidebar_business_behavior_generate_items`

**Inputs** held, module = no value.

**Declared result** list at dict.

**Explicit results** items.

**Local steps**

- Set items from list().
- Set sections from mapping(“Report” → “Reports”, “Dashboard” → “Dashboards”, “Page” → “Pages”).
- Set icons from mapping(“Report” → “table”, “Page” → “panel-top”, “Workspace” → “wallpaper”).
- For each tuple(entity, rows) in held.items().
  - If (entity equals OVERFLOW\_KEY or not rows).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entity equals OVERFLOW\_KEY → not rows.
    - Continue with the next iteration or loop test.
  - Set sectioned from (entity belongs to sections and (entity equals “Report” or len(rows) &gt; 1)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entity belongs to sections → (entity equals “Report” or len(rows) &gt; 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entity equals “Report” → len(rows) &gt; 1.
  - If sectioned.
    - Evaluate items.append(mapping(“type” → “Section Break”, “label” → sections at entity, “indent” → 1, “collapsible” → 1)).
  - For each row in rows.
    - Set item from mapping(“type” → “Link”, “link\_type” → entity, “link\_to” → row.name, “label” → row.title when entity equals “Page”, otherwise row.name, …).
      - Value choice on entity equals “Page” — true gives row.title, false gives row.name.
    - If (entity equals “Workspace” and module and row.name equals module).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entity equals “Workspace” → module → row.name equals module.
      - Set item at “label” from translated “Home”.
    - If (entity equals “DocType” and “settings” belongs to row.name.lower()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entity equals “DocType” → “settings” belongs to row.name.lower().
      - Set item at “icon” from “settings”.
    - If (entity equals “Report” or sectioned).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entity equals “Report” → sectioned.
      - Set item at “child” from 1.
    - Evaluate items.append(item).
  - If (entity equals “DocType” and held.get(OVERFLOW\_KEY)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entity equals “DocType” → held.get(OVERFLOW\_KEY).
    - Evaluate items.append(mapping(“type” → “Link”, “link\_type” → “DocType”, “link\_to” → “DocType”, “label” → translated “{0} more not shown”.format(held at OVERFLOW\_KEY), …)).
      - Value choice on module — true gives json.dumps(list(list(“DocType”, “module”, “=”, module))), false gives no value.
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L5089) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L999)

<a id="op-40296796749424"></a>
### Get computed bases

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_computed_bases`

**Inputs** modules.

**Declared result** dict at tuple(str, Platform.\_dict).

**Explicit results** bases.

**Local steps**

- Set bases from mapping().
- Set missing from list().
- For each module in modules.
  - Set cached from Platform.cache.hget(COMPUTED\_BASE\_CACHE\_KEY, module).
  - If cached is identical to no value.
    - Evaluate missing.append(module).
  - Otherwise.
    - Set bases at module from copy\_of(cached).
- If missing.
  - Set contents from get\_module\_contents(missing).
  - For each module in missing.
    - Set base from build\_computed\_base(module, contents at module).
    - Evaluate Platform.cache.hset(COMPUTED\_BASE\_CACHE\_KEY, module, base).
    - Set bases at module from copy\_of(base).
- Return bases.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L6318) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1002)

<a id="op-e1918d790d5aff"></a>
### Copy of

`operation_foundation_desk_record_definitions_sidebar_business_behavior_copy_of`

**Inputs** base.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(mapping(expand base, “rows” → list(base.rows))).

**Local steps**

- Return Platform.\_dict(mapping(expand base, “rows” → list(base.rows))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L6704) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L996)

<a id="op-a6218c4bcf0230"></a>
### Get computed base

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_computed_base`

**Inputs** module.

**Declared result** Platform.\_dict.

**Explicit results** get\_computed\_bases(list(module)) at module.

**Local steps**

- Return get\_computed\_bases(list(module)) at module.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L6808) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1001)

<a id="op-5c6c9238becd76"></a>
### Build computed base

`operation_foundation_desk_record_definitions_sidebar_business_behavior_build_computed_base`

**Inputs** module, held.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(mapping(“module” → module, “title” → module, “app” → get\_module\_placement(module), “header\_icon” → (own\_page\_icon(module, held) or DEFAULT\_HEADER\_ICON), …)).

**Local steps**

- Return Platform.\_dict(mapping(“module” → module, “title” → module, “app” → get\_module\_placement(module), “header\_icon” → (own\_page\_icon(module, held) or DEFAULT\_HEADER\_ICON), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in own\_page\_icon(module, held) → DEFAULT\_HEADER\_ICON.
  - Draw item from generate\_items(held, module).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L6879) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L990)

<a id="op-c1cab6f121691b"></a>
### Own page icon

`operation_foundation_desk_record_definitions_sidebar_business_behavior_own_page_icon`

**Inputs** module, held.

**Declared result** (str bitwise or no value).

**Explicit results** row.get(“icon”) · no value.

**Local steps**

- For each row in held.get(“Workspace”, list()).
  - If row.name equals module.
    - Return row.get(“icon”).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L7142) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1021)

<a id="op-90917f0e66d683"></a>
### Clear computed base cache

`operation_foundation_desk_record_definitions_sidebar_business_behavior_clear_computed_base_cache`

**Inputs** module.

**Declared result** no value.

**Local steps**

- Evaluate Platform.cache.hdel(COMPUTED\_BASE\_CACHE\_KEY, module).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L7317) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L994)

<a id="op-f3b73a8961a68f"></a>
### Clear computed base for

`operation_foundation_desk_record_definitions_sidebar_business_behavior_clear_computed_base_for`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- Set modules from set(doc.get(“module”)).
- If previous bound to doc.get\_doc\_before\_save().
  - Evaluate modules.add(previous.get(“module”)).
- For each module in modules.
  - If module.
    - Evaluate clear\_computed\_base\_cache(module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L7384) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L995)

<a id="op-04ca8363e52187"></a>
### Sidebar Context.for modules

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_context_for_modules`

**Inputs** cls, modules, user.

**Wrappers, in declaration order** classmethod.

**Declared result** “SidebarContext”.

**State and service calls** request new\_doc for “Workspace”.

**Explicit results** cls(user = user, bases = get\_sidebar\_bases(modules), workspaces = get\_module\_workspaces(), private\_rows = get\_private\_workspaces(user), …).

**Local steps**

- Bind dependencies get\_layers\_for.
- Bind dependencies get\_permitted\_onboardings.
- Return cls(user = user, bases = get\_sidebar\_bases(modules), workspaces = get\_module\_workspaces(), private\_rows = get\_private\_workspaces(user), …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1033)

<a id="op-60924f5de77e9b"></a>
### Resolved Sidebar.landing

`operation_foundation_desk_record_definitions_sidebar_business_behavior_resolved_sidebar_landing`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** (str bitwise or no value).

**Explicit results** get\_module\_landing\_route(self.items).

**Local steps**

- Return get\_module\_landing\_route(self.items).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L261) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1027)

<a id="op-91a17883ab9b8d"></a>
### Resolved Sidebar.as boot entry

`operation_foundation_desk_record_definitions_sidebar_business_behavior_resolved_sidebar_as_boot_entry`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“name” → self.name, “module” → self.module, “label” → self.label, “app” → self.app, …).

**Local steps**

- Return mapping(“name” → self.name, “module” → self.module, “label” → self.label, “app” → self.app, …).
  - Value choice on self.customized — true gives 1, false gives 0.
  - Value choice on self.computed — true gives 1, false gives 0.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L332) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1026)

<a id="op-2759dc264fb997"></a>
### Resolve sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_resolve_sidebar`

**Inputs** shell, user, context = no value.

**Declared result** (ResolvedSidebar bitwise or no value).

**Explicit results** resolve\_private\_sidebar(shell, user, context, base) · no value · ResolvedSidebar(name = shell, module = base.module, label = translated label, app = (base.app or get\_module\_placement(base.module)), …).

**Explicit failure paths** ValueError(formatted text sidebar context is {context.user}'s, and cannot answer for {user}).

**Local steps**

- Bind dependencies merged\_arrangement.
- If context is identical to no value.
  - Set context from SidebarContext.for\_modules(list((module\_of\_shell(shell) or shell)), user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in module\_of\_shell(shell) → shell.
- Otherwise.
  - If context.user differs from user.
    - Raise ValueError(formatted text sidebar context is {context.user}'s, and cannot answer for {user}).
- Set base from context.bases at shell.
- If base.module equals PRIVATE\_MODULE.
  - Return resolve\_private\_sidebar(shell, user, context, base).
- Set filtered from filter\_sidebar\_items(base.rows, context.perm\_ctx).
- Set layers from context.layers.get(base.module, list()).
- Set hidden from set().
- If layers.
  - Set tuple(filtered, hidden) from merged\_arrangement(filtered, layers).
  - Set filtered from list of item for item drawn from filtered where allowed\_added\_item(item, context.perm\_ctx).
    - Draw item from filtered, keep a combination only if (allowed\_added\_item(item, context.perm\_ctx)).
- Otherwise.
  - Set filtered from list of item for item drawn from filtered where not item.get(“hidden”).
    - Draw item from filtered, keep a combination only if (not item.get(“hidden”)).
- Set filtered from append\_derived\_items(filtered, context.private\_rows.get(base.module), context.perm\_ctx, hidden = hidden).
- If not any(generator of row.get(“type”) does not belong to tuple(“Section Break”, “Spacer”) for row drawn from filtered).
  - Draw row from filtered.
  - Return no value.
- Set label from (base.title or shell).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in base.title → shell.
- Set header\_icon from base.header\_icon.
- For each layer in layers.
  - If layer.label.
    - Set label from layer.label.
  - If layer.header\_icon.
    - Set header\_icon from layer.header\_icon.
- Return ResolvedSidebar(name = shell, module = base.module, label = translated label, app = (base.app or get\_module\_placement(base.module)), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in base.app → get\_module\_placement(base.module).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L32) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1025)
