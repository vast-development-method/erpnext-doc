# Forms, reports and navigation · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Custom sidebar

[Record definition](../../../../data/record-types/custom_sidebar.json)

<a id="op-e603f490ba9ea2"></a>
### Merge layers

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_merge_layers`

**Inputs** items, layers.

**Declared result** list at dict.

**Explicit results** merged\_arrangement(items, layers) at 0.

**Local steps**

- Return merged\_arrangement(items, layers) at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L460)

<a id="op-dd0a0c7966c1e3"></a>
### Merged arrangement

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_merged_arrangement`

**Inputs** items, layers.

**Declared result** tuple at tuple(list at dict, set at str).

**Explicit results** tuple(kept, set of key for tuple(key, is\_hidden) drawn from hidden.items() where is\_hidden).

**Local steps**

- Set tuple(resolved, hidden) from resolve\_arrangement(items, layers).
- Set kept from list().
- For each item in resolved.
  - If hidden.get(item\_key(item)).
    - Continue with the next iteration or loop test.
  - Evaluate item.pop(“hidden”, no value).
  - Evaluate kept.append(item).
- Return tuple(kept, set of key for tuple(key, is\_hidden) drawn from hidden.items() where is\_hidden).
  - Draw tuple(key, is\_hidden) from hidden.items(), keep a combination only if (is\_hidden).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L675)

<a id="op-726478a35cc874"></a>
### Apply sidebar row

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_apply_sidebar_row`

**Inputs** row, item.

**Declared result** (dict bitwise or no value).

**Explicit results** shape\_added\_item(row) · no value · mapping(expand item, expand overrides(row), “child” → int((row.child or 0))).

**Local steps**

- If row.added.
  - Return shape\_added\_item(row).
- If item is identical to no value.
  - Return no value.
- Return mapping(expand item, expand overrides(row), “child” → int((row.child or 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.child → 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L7033) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L438)

<a id="op-6a269c9a378d17"></a>
### Overrides

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_overrides`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping of field → row.get(field) for field drawn from REFERENCE\_FIELDS where row.get(field).

**Local steps**

- Return mapping of field → row.get(field) for field drawn from REFERENCE\_FIELDS where row.get(field).
  - Draw field from REFERENCE\_FIELDS, keep a combination only if (row.get(field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L7241) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L462)

<a id="op-eb590174b6f2a8"></a>
### Shape added item

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_shape_added_item`

**Inputs** row.

**Declared result** dict.

**Explicit results** item.

**Local steps**

- Bind dependencies attach\_report.
- Set item from mapping of field → row.get(field) for field drawn from ADDED\_ITEM\_FIELDS.
  - Draw field from ADDED\_ITEM\_FIELDS.
- Evaluate item.update(mapping(“key” → item\_key(row), “label” → translated row.label, “tab” → row.navigate\_to\_tab, “added” → 1)).
- Evaluate attach\_report(item, row.link\_type, row.link\_to).
- Return item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L112) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L472)

<a id="op-730607e0eff1ed"></a>
### Layer arrangement

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_layer_arrangement`

**Inputs** module, user.

**Declared result** list at dict.

**State and service calls** request new\_doc for “Workspace”.

**Explicit results** (arrangement + unstored\_private\_items(module, user, arrangement, perm\_ctx)).

**Local steps**

- Bind dependencies PRIVATE\_MODULE, filter\_sidebar\_items, get\_module\_base.
- Evaluate check\_module(module).
- Set perm\_ctx from Platform.new\_doc(“Workspace”).
- If module equals PRIVATE\_MODULE.
  - Set items from list().
- Otherwise.
  - Set base from get\_module\_base(module).
  - Set items from filter\_sidebar\_items(base.rows, perm\_ctx, check\_permission = bool(user)).
- Set tuple(resolved, hidden) from resolve\_arrangement(items, get\_layers(module, user)).
- Set own from get\_customization(module, user).
- Set own\_added from set of item\_key(row) for row drawn from own.sidebar\_items where row.added when own, otherwise set().
  - Value choice on own — true gives set of item\_key(row) for row drawn from own.sidebar\_items where row.added, false gives set().
  - Draw row from own.sidebar\_items, keep a combination only if (row.added).
- Set arrangement from list of mapping(expand item, “hidden” → int(hidden.get(item\_key(item), 0)), “added” → int(item\_key(item) belongs to own\_added)) for item drawn from resolved.
  - Draw item from resolved.
- Return (arrangement + unstored\_private\_items(module, user, arrangement, perm\_ctx)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L110) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L458)

<a id="op-0731aee5d95cdc"></a>
### Unstored private items

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_unstored_private_items`

**Inputs** module, user, arrangement, perm\_ctx.

**Declared result** list at dict.

**Explicit results** list() · list of mapping(expand item, “hidden” → 0, “added” → 1) for item drawn from filter\_sidebar\_items(rows, perm\_ctx) where item\_key(item) does not belong to seen.

**Local steps**

- Bind dependencies PRIVATE\_MODULE, all\_private\_rows, filter\_sidebar\_items, get\_private\_workspaces.
- If not user.
  - Return list().
- Set by\_module from get\_private\_workspaces(user).
- Set rows from all\_private\_rows(by\_module) when module equals PRIVATE\_MODULE, otherwise by\_module.get(module).
  - Value choice on module equals PRIVATE\_MODULE — true gives all\_private\_rows(by\_module), false gives by\_module.get(module).
- If not rows.
  - Return list().
- Set seen from set of item\_key(item) for item drawn from arrangement.
  - Draw item from arrangement.
- Return list of mapping(expand item, “hidden” → 0, “added” → 1) for item drawn from filter\_sidebar\_items(rows, perm\_ctx) where item\_key(item) does not belong to seen.
  - Draw item from filter\_sidebar\_items(rows, perm\_ctx), keep a combination only if (item\_key(item) does not belong to seen).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L678)

<a id="op-083afcd26ba205"></a>
### Get user sidebar layer

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_user_sidebar_layer`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** layer\_arrangement(module, Platform.session.user).

**Local steps**

- Return layer\_arrangement(module, Platform.session.user).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L736) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L456)

<a id="op-d0316b86354577"></a>
### Get site sidebar layer

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_site_sidebar_layer`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** layer\_arrangement(module, no value).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to see the sidebar's site layer.”).
- Return layer\_arrangement(module, no value).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L835) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L455)

<a id="op-0e631698093359"></a>
### Module payload

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_module_payload`

**Inputs** remaining named values extra.

**Declared result** dict.

**Explicit results** mapping(“module\_sidebars” → module\_sidebars, “entity\_module” → build\_entity\_module\_map(module\_sidebars), expand extra).

**Local steps**

- Bind dependencies build\_entity\_module\_map, get\_module\_sidebars.
- Set module\_sidebars from get\_module\_sidebars().
- Return mapping(“module\_sidebars” → module\_sidebars, “entity\_module” → build\_entity\_module\_map(module\_sidebars), expand extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L960) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L461)

<a id="op-f42c1f64bb5aa6"></a>
### Save sidebar customization

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_save_sidebar_customization`

**Inputs** module, items = no value, label = no value, header\_icon = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_save\_customization(module, items, user = Platform.session.user, label = label, header\_icon = header\_icon).

**Local steps**

- Return \_save\_customization(module, items, user = Platform.session.user, label = label, header\_icon = header\_icon).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1077) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L469)

<a id="op-8fc64bd1dcaf89"></a>
### Save site sidebar

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_save_site_sidebar`

**Inputs** module, items = no value, label = no value, header\_icon = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_save\_customization(module, items, user = no value, label = label, header\_icon = header\_icon).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to change this for everyone.”).
- Return \_save\_customization(module, items, user = no value, label = label, header\_icon = header\_icon).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1274) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L470)

<a id="op-b020cd35592c32"></a>
### Reset user sidebar

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_reset_user_sidebar`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_reset(module, Platform.session.user).

**Local steps**

- Return \_reset(module, Platform.session.user).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1497) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L466)

<a id="op-28ef9701806467"></a>
### Reset site sidebar

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_reset_site_sidebar`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_reset(module, no value).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to reset this for everyone.”).
- Return \_reset(module, no value).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1584) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L464)

<a id="op-49501b77020893"></a>
### Reset to standard

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_reset_to_standard`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Custom Sidebar” via get\_all.

**State and service calls** request delete\_doc for “Custom Sidebar”.

**Explicit results** module\_payload().

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to reset this for everyone.”).
- Evaluate check\_module(module).
- For each name in Platform.get\_all(“Custom Sidebar”, filters = mapping(“module” → module), pluck = “name”).
  - Evaluate Platform.delete\_doc(“Custom Sidebar”, name, ignore\_permissions = true, force = true).
- Return module\_payload().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1697) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L465)

<a id="op-1192fdc841ebef"></a>
### Add user sidebar item

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_add_user_sidebar_item`

**Inputs** module, user, item.

**Declared result** no value.

**Record and data access** resolve a document from “Custom Sidebar” via get\_doc.

**State and service calls** request new\_doc for “Custom Sidebar” · call save on doc.

**Explicit results** no value.

**Local steps**

- Set existing from get\_customization(module, user).
- Set doc from Platform.get\_doc(“Custom Sidebar”, existing.name) when existing, otherwise Platform.new\_doc(“Custom Sidebar”).update(mapping(“module” → module, “user” → user)).
  - Value choice on existing — true gives Platform.get\_doc(“Custom Sidebar”, existing.name), false gives Platform.new\_doc(“Custom Sidebar”).update(mapping(“module” → module, “user” → user)).
- If any(generator of item\_key(row) equals item\_key(item) for row drawn from doc.sidebar\_items).
  - Draw row from doc.sidebar\_items.
  - Return no value.
- Evaluate doc.append(“sidebar\_items”, mapping(expand item, “added” → 1)).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L670)

<a id="op-53d5fff6d4950e"></a>
### Layers holding

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_layers_holding`

**Inputs** link\_to, user = no value, added\_only = false, not\_labelled = no value.

**Declared result** list at Platform.\_dict.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set item from Platform.qb.DocType(“Sidebar Item”).
- Set layer from Platform.qb.DocType(“Custom Sidebar”).
- Set query from nested operand in the contract(nested operand in the contract).select(layer.name, layer.user).distinct().where(((item.parenttype equals “Custom Sidebar” bitwise and item.link\_type equals “Workspace”) bitwi ….
- If user.
  - Set query from query.where(layer.user equals user).
- If added\_only.
  - Set query from query.where(item.added equals 1).
- If not\_labelled is distinct from no value.
  - Set query from query.where((item.label differs from not\_labelled bitwise or item.label.isnull())).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L674)

<a id="op-e590f9282cd257"></a>
### Forget layers

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_forget_layers`

**Inputs** layers.

**Declared result** no value.

**Local steps**

- For each layer in layers.
  - Evaluate Platform.clear\_document\_cache(“Custom Sidebar”, layer.name).
  - If layer.user.
    - Evaluate Platform.cache.hdel(“bootinfo”, layer.user).
  - Otherwise.
    - Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L673)

<a id="op-bddd344e184dcb"></a>
### Remove workspace rows

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_remove_workspace_rows`

**Inputs** link\_to, owner = no value.

**Declared result** no value.

**State and service calls** request delete on “Sidebar Item”.

**Explicit results** no value.

**Local steps**

- Set layers from layers\_holding(link\_to).
- If not layers.
  - Return no value.
- Set names from list of layer.name for layer drawn from layers.
  - Draw layer from layers.
- Evaluate Platform.db.delete(“Sidebar Item”, mapping(“parenttype” → “Custom Sidebar”, “link\_type” → “Workspace”, “link\_to” → link\_to, “parent” → list(“in”, names))).
- If owner.
  - Evaluate drop\_layers\_saying\_nothing(list of layer.name for layer drawn from layers where layer.user equals owner).
    - Draw layer from layers, keep a combination only if (layer.user equals owner).
- Evaluate forget\_layers(layers).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L677)

<a id="op-eda90b64428dc3"></a>
### Drop layers saying nothing

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_drop_layers_saying_nothing`

**Inputs** names.

**Declared result** no value.

**Record and data access** read “Custom Sidebar” via get\_all · read “Sidebar Item” via get\_all.

**State and service calls** request delete\_doc for “Custom Sidebar”.

**Explicit results** no value.

**Local steps**

- Set unopinionated from Platform.get\_all(“Custom Sidebar”, filters = mapping(“name” → list(“in”, names), “label” → list(“in”, list(empty text, no value)), “header\_icon” → list(“in”, list(empty text, no value))), pluck = “name”).
- If not unopinionated.
  - Return no value.
- Set still\_holding from set(Platform.get\_all(“Sidebar Item”, filters = mapping(“parenttype” → “Custom Sidebar”, “parent” → list(“in”, unopinionated)), pluck = “parent”, distinct = true)).
- Set empty from list of name for name drawn from unopinionated where name does not belong to still\_holding.
  - Draw name from unopinionated, keep a combination only if (name does not belong to still\_holding).
- If empty.
  - Evaluate Platform.delete\_doc(“Custom Sidebar”, empty, ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L672)

<a id="op-997ad9ff763727"></a>
### Relabel workspace rows

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_relabel_workspace_rows`

**Inputs** link\_to, label.

**Declared result** no value.

**State and service calls** request set\_value on “Sidebar Item”.

**Explicit results** no value.

**Local steps**

- Set layers from layers\_holding(link\_to, added\_only = true, not\_labelled = label).
- If not layers.
  - Return no value.
- Evaluate Platform.db.set\_value(“Sidebar Item”, mapping(“parenttype” → “Custom Sidebar”, “link\_type” → “Workspace”, “link\_to” → link\_to, “added” → 1, …), “label”, label, update\_modified = false).
  - Draw layer from layers.
- Evaluate forget\_layers(layers).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L676)

<a id="op-9ac28708d6465e"></a>
### Add site sidebar item

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_add_site_sidebar_item`

**Inputs** module, item.

**Declared result** no value.

**Record and data access** resolve a document from “Custom Sidebar” via get\_doc.

**State and service calls** request new\_doc for “Custom Sidebar” · call save on doc.

**Explicit results** no value.

**Local steps**

- Set existing from get\_customization(module, no value).
- Set doc from Platform.get\_doc(“Custom Sidebar”, existing.name) when existing, otherwise Platform.new\_doc(“Custom Sidebar”).update(mapping(“module” → module, “user” → SITE\_LAYER)).
  - Value choice on existing — true gives Platform.get\_doc(“Custom Sidebar”, existing.name), false gives Platform.new\_doc(“Custom Sidebar”).update(mapping(“module” → module, “user” → SITE\_LAYER)).
- If any(generator of item\_key(row) equals item\_key(item) for row drawn from doc.sidebar\_items).
  - Draw row from doc.sidebar\_items.
  - Return no value.
- Evaluate doc.append(“sidebar\_items”, mapping(expand item, “added” → 1)).
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L1957) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L436)

<a id="op-56c31514916999"></a>
### Save customization

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_save_customization`

**Inputs** module, items, user, label = no value, header\_icon = no value.

**Record and data access** resolve a document from “Custom Sidebar” via get\_doc.

**State and service calls** request new\_doc for “Custom Sidebar” · call save on doc.

**Explicit results** module\_payload().

**Local steps**

- Evaluate check\_module(module).
- Set doc from get\_customization(module, user).
- If doc.
  - Set doc from Platform.get\_doc(“Custom Sidebar”, doc.name).
- Otherwise.
  - Set doc from Platform.new\_doc(“Custom Sidebar”).
  - Set doc.module from module.
  - Set doc.user from (user or SITE\_LAYER).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → SITE\_LAYER.
- If label is distinct from no value.
  - Set doc.label from label.
- If header\_icon is distinct from no value.
  - Set doc.header\_icon from header\_icon.
- If items is distinct from no value.
  - Set rows from list of shape\_row(row) for row drawn from (Platform.parse\_json(items) or list()).
    - Draw row from (Platform.parse\_json(items) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(items) → list().
  - Evaluate settle\_references(module, rows, user).
  - Evaluate doc.set(“sidebar\_items”, list()).
  - For each row in rows.
    - Evaluate doc.append(“sidebar\_items”, row).
- Evaluate doc.save(ignore\_permissions = true).
- Return module\_payload().

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L2337) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L468)

<a id="op-e54c71b161af91"></a>
### Shape row

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_shape_row`

**Inputs** row.

**Declared result** dict.

**Explicit results** shaped.

**Local steps**

- Set shaped from mapping(expand mapping of field → row.get(field) for field drawn from LINKED\_IDENTITY\_FIELDS, “key” → row.get(“key”), “hidden” → int((row.get(“hidden”) or 0)), “added” → int((row.get(“added”) or 0)), …).
  - Draw field from LINKED\_IDENTITY\_FIELDS.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“hidden”) → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“added”) → 0.
  - Draw field from REFERENCE\_FIELDS.
- If shaped at “added”.
  - Evaluate shaped.update(mapping of field → row.get(field) for field drawn from ADDED\_ITEM\_FIELDS).
    - Draw field from ADDED\_ITEM\_FIELDS.
  - Set shaped at “navigate\_to\_tab” from (row.get(“navigate\_to\_tab”) or row.get(“tab”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“navigate\_to\_tab”) → row.get(“tab”).
- Set shaped at “child” from int((row.get(“child”) or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“child”) → 0.
- Return shaped.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L2975) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L473)
