# Forms, reports and navigation · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dock

[Record definition](../../../../data/record-types/dock.json)

<a id="op-4f5393a40c7399"></a>
### Apps screen sort key.sequence

`operation_foundation_desk_record_definitions_dock_business_behavior_apps_screen_sort_key_sequence`

**Inputs** app.

**Declared result** float.

**Explicit results** ((declared and declared at 0.get(“sequence\_id”)) or DEFAULT\_APP\_SEQUENCE\_ID).

**Local steps**

- Set declared from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app).
- Return ((declared and declared at 0.get(“sequence\_id”)) or DEFAULT\_APP\_SEQUENCE\_ID).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (declared and declared at 0.get(“sequence\_id”)) → DEFAULT\_APP\_SEQUENCE\_ID.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in declared → declared at 0.get(“sequence\_id”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L1892) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L677)

<a id="op-ed68d7c574407f"></a>
### Get site dock

`operation_foundation_desk_record_definitions_dock_business_behavior_get_site_dock`

**Inputs** app.

**Declared result** list at dict.

**Explicit results** dock\_rows(get\_dock(app)).

**Local steps**

- Return dock\_rows(get\_dock(app)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L2028) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L710)

<a id="op-d4b09083ab2910"></a>
### Get user dock

`operation_foundation_desk_record_definitions_dock_business_behavior_get_user_dock`

**Inputs** app, user = no value.

**Declared result** list at dict.

**Explicit results** dock\_rows(get\_dock(app, user = (user or Platform.session.user))).

**Local steps**

- Return dock\_rows(get\_dock(app, user = (user or Platform.session.user))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L2111) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L712)

<a id="op-e0b42b90e1bb43"></a>
### Resolve dock

`operation_foundation_desk_record_definitions_dock_business_behavior_resolve_dock`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** resolved.

**Local steps**

- Set resolved from mapping().
- For each app in docked\_apps().
  - Set rail from resolve\_app\_dock(app).
  - If rail.
    - Set resolved at app from rail.
- Return resolved.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L2246) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L727)

<a id="op-ebff5e53c35b63"></a>
### Docked apps

`operation_foundation_desk_record_definitions_dock_business_behavior_docked_apps`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** sorted(apps, key = apps\_screen\_sort\_key()).

**Local steps**

- Set installed from set(Platform.get\_installed\_apps()).
- Set mounted from mounted\_apps().
- Set apps from (set of row at “app” for row drawn from dock\_records() where row at “app” belongs to installed − set(mounted)).
  - Draw row from dock\_records(), keep a combination only if (row at “app” belongs to installed).
- Return sorted(apps, key = apps\_screen\_sort\_key()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L127) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L699)

<a id="op-9981de5c985c3e"></a>
### Resolve app dock

`operation_foundation_desk_record_definitions_dock_business_behavior_resolve_application_dock`

**Inputs** app, upto = “user”, gated = true.

**Declared result** list at dict.

**Explicit results** list of mapping(expand rail\_entry(entry), “hidden” → int(hidden.get(dock\_key(entry), 0))) for entry drawn from resolved where (not gated or is\_reachable(entry)).

**Local steps**

- Set layers from list().
- If upto belongs to tuple(“site”, “user”).
  - Evaluate layers.append(get\_site\_dock(app)).
- If upto equals “user”.
  - Evaluate layers.append(get\_user\_dock(app)).
- Set tuple(resolved, hidden) from resolve\_layers(get\_app\_base(app), layers, key = dock\_key, apply\_row = apply\_dock\_row, keep\_unnamed = false).
- Return list of mapping(expand rail\_entry(entry), “hidden” → int(hidden.get(dock\_key(entry), 0))) for entry drawn from resolved where (not gated or is\_reachable(entry)).
  - Draw entry from resolved, keep a combination only if ((not gated or is\_reachable(entry))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not gated → is\_reachable(entry).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L2629) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L726)

<a id="op-0a3ed8998eaf53"></a>
### Dock key

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_key`

**Inputs** entry.

**Declared result** str.

**Explicit results** “\|”.join(generator of (entry.get(field) or empty text) for field drawn from DESTINATION\_FIELDS).

**Local steps**

- Return “\|”.join(generator of (entry.get(field) or empty text) for field drawn from DESTINATION\_FIELDS).
  - Draw field from DESTINATION\_FIELDS.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(field) → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L3094) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L689)

<a id="op-da54c68ab9921f"></a>
### Apply dock row

`operation_foundation_desk_record_definitions_dock_business_behavior_apply_dock_row`

**Inputs** row, entry.

**Declared result** (dict bitwise or no value).

**Explicit results** rail\_entry(row) · no value · mapping(expand entry, expand overrides(row)).

**Local steps**

- If row.get(“added”).
  - Return rail\_entry(row).
- If entry is identical to no value.
  - Return no value.
- Return mapping(expand entry, expand overrides(row)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L3194) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L675)

<a id="op-51b1f72d68ea7b"></a>
### Rail entry

`operation_foundation_desk_record_definitions_dock_business_behavior_rail_entry`

**Inputs** entry.

**Declared result** dict.

**Explicit results** mapping(expand mapping of field → entry.get(field) for field drawn from DESTINATION\_FIELDS, expand mapping of field → entry.get(field) for field drawn from REFERENCE\_FIELDS, “title” → translated entry at “ ….

**Local steps**

- Return mapping(expand mapping of field → entry.get(field) for field drawn from DESTINATION\_FIELDS, expand mapping of field → entry.get(field) for field drawn from REFERENCE\_FIELDS, “title” → translated entry at “ ….
  - Draw field from DESTINATION\_FIELDS.
  - Draw field from REFERENCE\_FIELDS.
  - Value choice on entry.get(“title”) — true gives translated entry at “title”, false gives entry.get(“title”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L131) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L722)

<a id="op-af26b1da069721"></a>
### Overrides

`operation_foundation_desk_record_definitions_dock_business_behavior_overrides`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping of field → row.get(field) for field drawn from REFERENCE\_FIELDS where row.get(field).

**Local steps**

- Return mapping of field → row.get(field) for field drawn from REFERENCE\_FIELDS where row.get(field).
  - Draw field from REFERENCE\_FIELDS, keep a combination only if (row.get(field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L3513) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L719)

<a id="op-a0ce59beebcb3b"></a>
### Entry exists

`operation_foundation_desk_record_definitions_dock_business_behavior_entry_exists`

**Inputs** entry.

**Declared result** bool.

**Record and data access** read “Workspace” via exists.

**Explicit results** shell\_exists(entry.get(“link\_to”)) · bool(Platform.db.exists(“Workspace”, entry.get(“link\_to”), cache = true)) · true.

**Local steps**

- If entry.get(“link\_type”) equals “Sidebar”.
  - Return shell\_exists(entry.get(“link\_to”)).
- If entry.get(“link\_type”) equals “Workspace”.
  - Return bool(Platform.db.exists(“Workspace”, entry.get(“link\_to”), cache = true)).
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L3611) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L702)

<a id="op-c56510b1fdbb8c"></a>
### Shell exists

`operation_foundation_desk_record_definitions_dock_business_behavior_shell_exists`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** shell.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L3866) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L734)

<a id="op-60b91125685877"></a>
### Is reachable

`operation_foundation_desk_record_definitions_dock_business_behavior_is_reachable`

**Inputs** entry.

**Declared result** bool.

**Explicit results** false · (not module or is\_module\_visible(module)) · entry.get(“link\_to”) belongs to permitted\_workspaces() · true.

**Local steps**

- Bind dependencies module\_of\_shell.
- Bind dependencies is\_module\_visible.
- If entry.get(“link\_type”) equals “Sidebar”.
  - Set shell from entry.get(“link\_to”).
  - If not shell\_exists(shell).
    - Return false.
  - Set module from module\_of\_shell(shell).
  - Return (not module or is\_module\_visible(module)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not module → is\_module\_visible(module).
- If entry.get(“link\_type”) equals “Workspace”.
  - Return entry.get(“link\_to”) belongs to permitted\_workspaces().
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L4010) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L715)

<a id="op-253ff89a622743"></a>
### Permitted workspaces

`operation_foundation_desk_record_definitions_dock_business_behavior_permitted_workspaces`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** set of page.name for page drawn from get\_workspaces() at “pages”.

**Local steps**

- Bind dependencies get\_workspaces.
- Return set of page.name for page drawn from get\_workspaces() at “pages”.
  - Draw page from get\_workspaces() at “pages”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L4340) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L720)

<a id="op-3273f98b9922a2"></a>
### Shape dock rows

`operation_foundation_desk_record_definitions_dock_business_behavior_shape_dock_rows`

**Inputs** items, require\_visible, below.

**Declared result** list at dict.

**Explicit results** shaped.

**Local steps**

- Set shown from below.
- Set tuple(shaped, seen) from tuple(list(), set()).
- For each row in (Platform.parse\_json(items) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(items) → list().
  - If not isinstance(row, dict).
    - Continue with the next iteration or loop test.
  - Set entry from stored\_row(row).
  - If any(generator of (value is distinct from no value and not isinstance(value, str)) for value drawn from destination(entry).values()).
    - Draw value from destination(entry).values().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → not isinstance(value, str).
    - Continue with the next iteration or loop test.
  - If (entry at “link\_type” and entry at “link\_type” does not belong to DOCK\_LINK\_TYPES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry at “link\_type” → entry at “link\_type” does not belong to DOCK\_LINK\_TYPES.
    - Continue with the next iteration or loop test.
  - If not points\_somewhere(entry).
    - Continue with the next iteration or loop test.
  - If not entry\_exists(entry).
    - Continue with the next iteration or loop test.
  - Set key from dock\_key(entry).
  - If key belongs to seen.
    - Continue with the next iteration or loop test.
  - If (require\_visible and not is\_reachable(entry)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in require\_visible → not is\_reachable(entry).
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(key).
  - Evaluate shaped.append(settle\_reference(entry, shown.get(key))).
- Return shaped.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L4430) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L733)

<a id="op-48ea0f775214ff"></a>
### Settle reference

`operation_foundation_desk_record_definitions_dock_business_behavior_settle_reference`

**Inputs** entry, below.

**Declared result** dict.

**Explicit results** mapping(expand entry, “added” → 1) · settled.

**Local steps**

- If below is identical to no value.
  - Return mapping(expand entry, “added” → 1).
- Set settled from mapping(expand entry, “added” → 0).
- For each field in REFERENCE\_FIELDS.
  - Set inherited from below.get(field).
  - If (settled.get(field) and settled at field belongs to tuple(inherited, translated inherited when inherited, otherwise no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in settled.get(field) → settled at field belongs to tuple(inherited, translated inherited when inherited, otherwise no value).
    - Value choice on inherited — true gives translated inherited, false gives no value.
    - Set settled at field from no value.
- Return settled.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L5089) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L732)

<a id="op-60ad17d78de7f9"></a>
### Entries below

`operation_foundation_desk_record_definitions_dock_business_behavior_entries_below`

**Inputs** app, user.

**Declared result** dict at tuple(str, dict).

**Explicit results** mapping of dock\_key(entry) → entry for entry drawn from below.

**Local steps**

- Set below from resolve\_app\_dock(app, upto = “site” when user, otherwise “app”, gated = false).
  - Value choice on user — true gives “site”, false gives “app”.
- Return mapping of dock\_key(entry) → entry for entry drawn from below.
  - Draw entry from below.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L128) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L701)

<a id="op-2748bc6afd440b"></a>
### Destination

`operation_foundation_desk_record_definitions_dock_business_behavior_destination`

**Inputs** entry.

**Declared result** dict.

**Explicit results** mapping of field → entry.get(field) for field drawn from DESTINATION\_FIELDS.

**Local steps**

- Return mapping of field → entry.get(field) for field drawn from DESTINATION\_FIELDS.
  - Draw field from DESTINATION\_FIELDS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L5581) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L681)

<a id="op-ac2f6ebbf6365a"></a>
### Save user dock

`operation_foundation_desk_record_definitions_dock_business_behavior_save_user_dock`

**Inputs** app, items.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_save\_layer(app, items, user = Platform.session.user, require\_visible = true).

**Local steps**

- Return \_save\_layer(app, items, user = Platform.session.user, require\_visible = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L5659) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L731)

<a id="op-efee05969c67fe"></a>
### Save site dock

`operation_foundation_desk_record_definitions_dock_business_behavior_save_site_dock`

**Inputs** app, items.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_save\_layer(app, items, user = no value, require\_visible = false).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to change the dock for everyone.”).
- Return \_save\_layer(app, items, user = no value, require\_visible = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L5789) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L730)

<a id="op-eb38e5bcf3f3e5"></a>
### Save layer

`operation_foundation_desk_record_definitions_dock_business_behavior_save_layer`

**Inputs** app, items, user, require\_visible.

**Record and data access** resolve a document from “Dock” via get\_doc.

**State and service calls** request new\_doc for “Dock” · call save on doc.

**Explicit results** resolve\_app\_dock(app).

**Local steps**

- Set app from check\_docked\_app(app).
- Set doc from get\_dock(app, user = user).
- If doc.
  - Set doc from Platform.get\_doc(“Dock”, doc.name).
- Otherwise.
  - Set doc from Platform.new\_doc(“Dock”).
  - Set doc.app from app.
  - Set doc.user from (user or SITE\_LAYER).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → SITE\_LAYER.
- Evaluate doc.set(“items”, list()).
- For each row in shape\_dock\_rows(items, require\_visible = require\_visible, below = entries\_below(app, user)).
  - Evaluate doc.append(“items”, mapping of field → row at field for field drawn from DOCK\_ITEM\_FIELDS).
    - Draw field from DOCK\_ITEM\_FIELDS.
- Evaluate doc.save(ignore\_permissions = true).
- Return resolve\_app\_dock(app).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L5945) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L729)

<a id="op-1e5bc0e34929fd"></a>
### Check docked app

`operation_foundation_desk_record_definitions_dock_business_behavior_check_docked_application`

**Inputs** app.

**Declared result** str.

**Explicit results** app.

**Explicit failure paths** validation helper — translated “{0} is not an app on this site.”.format(Platform.bold((app or “-”))).

**Local steps**

- Set app from (app or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app → empty text.
- If (not app or app does not belong to Platform.get\_installed\_apps()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not app → app does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(translated “{0} is not an app on this site.”.format(Platform.bold((app or “-”)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app → “-”.
- Return app.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L126) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L680)

<a id="op-c90e05db8a8a08"></a>
### Get user dock layer

`operation_foundation_desk_record_definitions_dock_business_behavior_get_user_dock_layer`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_user\_dock(check\_docked\_app(app)).

**Local steps**

- Return get\_user\_dock(check\_docked\_app(app)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L6664) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L713)

<a id="op-830cc1f2c088d3"></a>
### Get site dock layer

`operation_foundation_desk_record_definitions_dock_business_behavior_get_site_dock_layer`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_site\_dock(check\_docked\_app(app)).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to see the dock's site layer.”).
- Return get\_site\_dock(check\_docked\_app(app)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L6765) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L711)
