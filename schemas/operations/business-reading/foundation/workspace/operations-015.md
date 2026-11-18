# Forms, reports and navigation · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Custom sidebar

[Record definition](../../../../data/record-types/custom_sidebar.json)

<a id="op-1dacbf96dcb494"></a>
### Settle references

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_settle_references`

**Inputs** module, rows, user.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set references from list of row for row drawn from rows where not row at “added”.
  - Draw row from rows, keep a combination only if (not row at “added”).
- If not references.
  - Return no value.
- Set tuple(resolved, \_hidden) from resolve\_arrangement(base\_items(module), layers\_below(module, user)).
- Set shown from mapping of item\_key(item) → item for item drawn from resolved.
  - Draw item from resolved.
- Evaluate anchor\_references(references, shown).
- Evaluate drop\_inherited\_values(references, shown).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L3498) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L471)

<a id="op-56c7e452d8c666"></a>
### Anchor references

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_anchor_references`

**Inputs** rows, shown.

**Declared result** no value.

**Local steps**

- For each row in rows.
  - Set item from shown.get(item\_key(row)).
  - If not item.
    - Continue with the next iteration or loop test.
  - Set row at “type” from item.get(“type”).
  - If is\_linked(item).
    - Evaluate row.update(mapping of field → item.get(field) for field drawn from LINKED\_IDENTITY\_FIELDS).
      - Draw field from LINKED\_IDENTITY\_FIELDS.
    - Set row at “key” from no value.
  - Otherwise.
    - Evaluate row.update(dict.fromkeys(tuple(“link\_type”, “link\_to”, “url”, “route”))).
    - Set row at “key” from item\_key(item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L107) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L437)

<a id="op-5588b2a52895a8"></a>
### Drop inherited values

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_drop_inherited_values`

**Inputs** rows, shown.

**Declared result** no value.

**Local steps**

- For each row in rows.
  - Set item from (shown.get(item\_key(row)) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in shown.get(item\_key(row)) → mapping().
  - For each field in REFERENCE\_FIELDS.
    - Set value from item.get(field).
    - If (row.get(field) and row at field belongs to tuple(value, translated value when value, otherwise no value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(field) → row at field belongs to tuple(value, translated value when value, otherwise no value).
      - Value choice on value — true gives translated value, false gives no value.
      - Set row at field from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L4227) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L450)

<a id="op-fd39b66443c2cd"></a>
### Layers below

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_layers_below`

**Inputs** module, user.

**Declared result** list at “CustomSidebar”.

**Explicit results** get\_layers(module, no value) when user, otherwise list().

**Local steps**

- Return get\_layers(module, no value) when user, otherwise list().
  - Value choice on user — true gives get\_layers(module, no value), false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L4520) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L459)

<a id="op-faa25557237985"></a>
### Base items

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_base_items`

**Inputs** module.

**Declared result** list at dict.

**Explicit results** list of dict(row) for row drawn from get\_module\_base(module).rows.

**Local steps**

- Bind dependencies get\_module\_base.
- Return list of dict(row) for row drawn from get\_module\_base(module).rows.
  - Draw row from get\_module\_base(module).rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L4626) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L439)

<a id="op-e0ac00031ad4bf"></a>
### Reset

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_reset`

**Inputs** module, user.

**State and service calls** request delete\_doc for “Custom Sidebar”.

**Explicit results** module\_payload().

**Local steps**

- Set doc from get\_customization(module, user).
- If doc.
  - Evaluate Platform.delete\_doc(“Custom Sidebar”, doc.name, ignore\_permissions = true, force = true).
- Return module\_payload().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L4737) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L463)

<a id="op-55490e53385f2e"></a>
### Has permission

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean true, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L4911) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L457)

<a id="op-8630cefd574435"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0157.json#L5113) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L454)

## Record · Custom workspace

[Record definition](../../../../data/record-types/custom_workspace.json)

<a id="op-3d66b7fc3d4eb9"></a>
### Custom Workspace.before validate

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_custom_workspace_before_validate`

**Inputs** self.

**Local steps**

- Bind dependencies sanitize\_content.
- Set self.content from sanitize\_content(self.content).
- Set self.widgets from sanitize\_content(self.widgets).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1039) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L37) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L560)

<a id="op-143037f4e417c6"></a>
### Custom Workspace.validate

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_custom_workspace_validate`

**Inputs** self.

**Record and data access** read “Workspace” via get\_value.

**Explicit failure paths** validation helper — translated “Only standard (app-shipped) workspaces can be customized.”.

**Local steps**

- If not Platform.db.get\_value(“Workspace”, self.workspace, “standard”).
  - Call the validation error handler Platform.throw(translated “Only standard (app-shipped) workspaces can be customized.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1145) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L41) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L564)

<a id="op-efbf6ea9f8dea5"></a>
### Custom Workspace.on update

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_custom_workspace_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-015.md#op-9dec114a5b0aa3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1272) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L40) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L563)

<a id="op-e0a74ba1afd510"></a>
### Custom Workspace.on trash

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_custom_workspace_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-015.md#op-9dec114a5b0aa3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1323) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L39) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L562)

<a id="op-9dec114a5b0aa3"></a>
### Custom Workspace.clear cache

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_custom_workspace_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- Evaluate Platform.cache.delete\_key(“bootinfo”).
- Evaluate Platform.cache.delete\_value(CUSTOMIZED\_NAMES\_CACHE\_KEY).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1374) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L38) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L561)

<a id="op-f5e69afaf85e0c"></a>
### Get customized workspace names

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_get_customized_workspace_names`

**Inputs** no declared parameters.

**Declared result** set at str.

**Record and data access** read “Custom Workspace” via get\_all.

**Explicit results** set(names).

**Local steps**

- Set names from Platform.cache.get\_value(CUSTOMIZED\_NAMES\_CACHE\_KEY).
- If names is identical to no value.
  - Set names from Platform.get\_all(“Custom Workspace”, pluck = “workspace”).
  - Evaluate Platform.cache.set\_value(CUSTOMIZED\_NAMES\_CACHE\_KEY, names).
- Return set(names).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1484) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L44) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L567)

<a id="op-bd1e1b1cfd5e99"></a>
### Get customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_get_customization`

**Inputs** workspace.

**Declared result** “CustomWorkspace \| None”.

**Record and data access** resolve a document from “Custom Workspace” via get\_cached\_doc.

**Explicit results** no value · Platform.get\_cached\_doc(“Custom Workspace”, workspace).

**Local steps**

- If workspace does not belong to get\_customized\_workspace\_names().
  - Return no value.
- Attempt the following.
  - Return Platform.get\_cached\_doc(“Custom Workspace”, workspace).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Custom Workspace”, workspace).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1675) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L43) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L566)

<a id="op-845c21097ed77f"></a>
### Effective roles

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_effective_roles`

**Inputs** base\_roles, customization.

**Declared result** list at str.

**Explicit results** list(roles).

**Local steps**

- Set removed from set of r.role for r drawn from customization.removed\_roles.
  - Draw r from customization.removed\_roles.
- Set roles from set of r for r drawn from base\_roles where r does not belong to removed.
  - Draw r from base\_roles, keep a combination only if (r does not belong to removed).
- Evaluate roles.update(generator of r.role for r drawn from customization.added\_roles).
  - Draw r from customization.added\_roles.
- Return list(roles).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L1844) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L42) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L565)

<a id="op-5a21f089756e6b"></a>
### Apply customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_apply_customization`

**Inputs** doc, customization.

**Declared result** no value.

**Local steps**

- Evaluate \_apply\_roles(doc, customization).
- Evaluate \_apply\_properties(doc, customization).
- Evaluate \_apply\_content(doc, customization).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L2072) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L34) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L557)

<a id="op-e358573cb8aa51"></a>
### Apply roles

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_apply_roles`

**Inputs** doc, customization.

**Declared result** no value.

**Local steps**

- Set new\_roles from effective\_roles(list of r.role for r drawn from doc.roles, customization).
  - Draw r from doc.roles.
- Evaluate doc.set(“roles”, list()).
- For each role in new\_roles.
  - Evaluate doc.append(“roles”, mapping(“role” → role)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L2193) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L36) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L559)

<a id="op-b42a014b17ed4a"></a>
### Apply properties

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_apply_properties`

**Inputs** doc, customization.

**Declared result** no value.

**Local steps**

- If customization.visibility equals “Hidden”.
  - Set doc.is\_hidden from 1.
- Otherwise.
  - If customization.visibility equals “Visible”.
    - Set doc.is\_hidden from 0.
- If customization.icon.
  - Set doc.icon from customization.icon.
- If customization.indicator\_color.
  - Set doc.indicator\_color from customization.indicator\_color.
- If customization.override\_sequence.
  - Set doc.sequence\_id from customization.sequence\_id.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L2385) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L35) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L558)

<a id="op-d9f3e77defc4ad"></a>
### Apply content

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_apply_content`

**Inputs** doc, customization.

**Declared result** no value.

**Local steps**

- If customization.content.
  - Set doc.content from customization.content.
- Set widgets from loads((customization.widgets or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.widgets → “{}”.
- If widgets.
  - Evaluate \_append\_widgets(doc, widgets).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L2614) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L556)

<a id="op-98c204141b21a7"></a>
### Append widgets

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_append_widgets`

**Inputs** doc, widgets.

**Declared result** no value.

**Local steps**

- Bind dependencies new\_widget.
- If widgets.get(“chart”).
  - Evaluate doc.charts.extend(new\_widget(widgets at “chart”, “Workspace Chart”, “charts”)).
- If widgets.get(“shortcut”).
  - Evaluate doc.shortcuts.extend(new\_widget(widgets at “shortcut”, “Workspace Shortcut”, “shortcuts”)).
- If widgets.get(“quick\_list”).
  - Evaluate doc.quick\_lists.extend(new\_widget(widgets at “quick\_list”, “Workspace Quick List”, “quick\_lists”)).
- If widgets.get(“custom\_block”).
  - Evaluate doc.custom\_blocks.extend(new\_widget(widgets at “custom\_block”, “Workspace Custom Block”, “custom\_blocks”)).
- If widgets.get(“number\_card”).
  - Evaluate doc.number\_cards.extend(new\_widget(widgets at “number\_card”, “Workspace Number Card”, “number\_cards”)).
- If widgets.get(“card”).
  - Evaluate doc.build\_links\_table\_from\_card(widgets at “card”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L2762) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L32) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L555)

<a id="op-f061b4ecaefdcb"></a>
### Upsert content customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_upsert_content_customization`

**Inputs** workspace, edited\_content, new\_widgets.

**Declared result** no value.

**State and service calls** call save on customization.

**Local steps**

- Set customization from \_get\_or\_new(workspace).
- Set widgets from loads((customization.widgets or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.widgets → “{}”.
- For each tuple(widget\_type, items) in (new\_widgets or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_widgets → mapping().
  - If items.
    - Evaluate widgets.setdefault(widget\_type, list()).extend(items).
- Set widgets from \_prune\_widgets(widgets, edited\_content).
- Set customization.content from dumps(edited\_content).
- Set customization.widgets from dumps(widgets).
- Evaluate customization.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L3332) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L48) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L571)

<a id="op-852a97e9a304c5"></a>
### Prune widgets

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_prune_widgets`

**Inputs** widgets, content.

**Declared result** dict.

**Explicit results** pruned.

**Local steps**

- Set referenced from mapping().
- For each block in content.
  - Set block\_type from block.get(“type”).
  - If block\_type belongs to WIDGET\_PARENTFIELD.
    - Set name from (block.get(“data”) or mapping()).get(formatted text {block\_type}\_name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“data”) → mapping().
    - Evaluate referenced.setdefault(block\_type, set()).add(name).
- Set pruned from mapping().
- For each tuple(widget\_type, items) in widgets.items().
  - Set kept from mapping().
  - For each item in items.
    - If item.get(“label”) belongs to referenced.get(widget\_type, set()).
      - Set kept at item.get(“label”) from item.
  - If kept.
    - Set pruned at widget\_type from list(kept.values()).
- Return pruned.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L3673) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L46) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L569)

<a id="op-de2d1353435caa"></a>
### Upsert property customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_upsert_property_customization`

**Inputs** workspace, icon (named only, default no value), indicator\_color (named only, default no value), visibility (named only, default no value), override\_sequence (named only, default no value), sequence\_id (named only, default no value).

**Declared result** no value.

**State and service calls** call save on customization.

**Local steps**

- Set customization from \_get\_or\_new(workspace).
- If icon is distinct from no value.
  - Set customization.icon from icon.
- If indicator\_color is distinct from no value.
  - Set customization.indicator\_color from indicator\_color.
- If visibility is distinct from no value.
  - Set customization.visibility from visibility.
- If override\_sequence is distinct from no value.
  - Set customization.override\_sequence from override\_sequence.
- If sequence\_id is distinct from no value.
  - Set customization.sequence\_id from sequence\_id.
- Evaluate customization.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L4182) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L49) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L572)
