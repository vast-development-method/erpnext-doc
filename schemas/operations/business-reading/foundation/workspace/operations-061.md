# Forms, reports and navigation · operations 61

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sidebar

[Record definition](../../../../data/record-types/sidebar.json)

<a id="op-306ef1d734cdd0"></a>
### Resolve private sidebar

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_resolve_private_sidebar`

**Inputs** shell, user, context, base.

**Declared result** ResolvedSidebar.

**Explicit results** ResolvedSidebar(name = shell, module = base.module, label = translated label, app = (base.app or get\_module\_placement(base.module)), …).

**Local steps**

- Bind dependencies merged\_arrangement.
- Set layers from list of layer for layer drawn from context.layers.get(PRIVATE\_MODULE, list()) where layer.user equals user.
  - Draw layer from context.layers.get(PRIVATE\_MODULE, list()), keep a combination only if (layer.user equals user).
- Set items from list().
- If layers.
  - Set tuple(items, \_hidden) from merged\_arrangement(list(), layers).
  - Set items from list of item for item drawn from items where allowed\_added\_item(item, context.perm\_ctx).
    - Draw item from items, keep a combination only if (allowed\_added\_item(item, context.perm\_ctx)).
- Set items from append\_derived\_items(items, all\_private\_rows(context.private\_rows), context.perm\_ctx).
- Set label from (base.title or shell).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in base.title → shell.
- Set header\_icon from PRIVATE\_HEADER\_ICON.
- For each layer in layers.
  - If layer.label.
    - Set label from layer.label.
  - If layer.header\_icon.
    - Set header\_icon from layer.header\_icon.
- Return ResolvedSidebar(name = shell, module = base.module, label = translated label, app = (base.app or get\_module\_placement(base.module)), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in base.app → get\_module\_placement(base.module).
  - Draw row from (context.private\_rows.get(PRIVATE\_MODULE) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.private\_rows.get(PRIVATE\_MODULE) → list().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L740)

<a id="op-26df661d8ff1ee"></a>
### All private rows

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_all_private_rows`

**Inputs** private\_rows.

**Declared result** list at Platform.\_dict.

**Explicit results** list of row for rows drawn from private\_rows.values(), then row drawn from rows.

**Local steps**

- Return list of row for rows drawn from private\_rows.values(), then row drawn from rows.
  - Draw rows from private\_rows.values().
  - Draw row from rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L734)

<a id="op-c478aa397c59b8"></a>
### Get navigable modules

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_navigable_modules`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** navigable.

**Local steps**

- Bind dependencies get\_code\_only\_modules, get\_visible\_modules.
- Set code\_only from get\_code\_only\_modules().
- Set modules from Platform.get\_all(“Module Def”, pluck = “name”, order\_by = “name asc”).
- Set visible from get\_visible\_modules(modules).
- Set navigable from list of module for module drawn from visible where module does not belong to code\_only.
  - Draw module from visible, keep a combination only if (module does not belong to code\_only).
- If (PRIVATE\_MODULE belongs to modules and PRIVATE\_MODULE does not belong to navigable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in PRIVATE\_MODULE belongs to modules → PRIVATE\_MODULE does not belong to navigable.
  - Set navigable from sorted(list(expanded navigable, PRIVATE\_MODULE)).
- Return navigable.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L29) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1008)

<a id="op-2bc26c7dc69ba7"></a>
### Get sidebar bases

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_sidebar_bases`

**Inputs** modules.

**Declared result** dict at tuple(str, Platform.\_dict).

**Record and data access** read “Sidebar” via get\_all.

**Explicit results** resolved.

**Local steps**

- Set documents from Platform.get\_all(“Sidebar”, filters = mapping(“module” → list(“in”, modules)), fields = list(“name”, “module”, “title”, “app”, …), order\_by = “name asc”).
- Set items\_by\_sidebar from get\_sidebar\_items(list of base.name for base drawn from documents).
  - Draw base from documents.
- Set shells from mapping().
- For each base in documents.
  - Set base.rows from items\_by\_sidebar.get(base.name, list()).
  - Set base.computed from 0.
  - Evaluate shells.setdefault(base.module, list()).append(base).
- Set documented from set(shells).
- Set needs\_computing from list of module for module drawn from modules where module does not belong to documented.
  - Draw module from modules, keep a combination only if (module does not belong to documented).
- Update needs\_computing using + list of base.module for bases drawn from shells.values(), then base drawn from bases where not base.rows.
  - Draw bases from shells.values().
  - Draw base from bases, keep a combination only if (not base.rows).
- Set computed from get\_computed\_bases(sorted(set(needs\_computing))) when needs\_computing, otherwise mapping().
  - Value choice on needs\_computing — true gives get\_computed\_bases(sorted(set(needs\_computing))), false gives mapping().
- Set resolved from mapping().
- For each module in modules.
  - For each base in (shells.get(module) or list(computed at module)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in shells.get(module) → list(computed at module).
    - If not base.rows.
      - Set base.rows from computed at module.rows.
      - Set base.computed from 1.
    - Set resolved at (base.get(“name”) or module) from base.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in base.get(“name”) → module.
- Return resolved.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L1852) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1011)

<a id="op-9d0a9314504f95"></a>
### Module of shell

`operation_foundation_desk_record_definitions_sidebar_business_behavior_module_of_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** shell.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L2644) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1020)

<a id="op-694cda4fea0a10"></a>
### Get module base

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_module_base`

**Inputs** module, shell = no value.

**Declared result** Platform.\_dict.

**Explicit results** (bases.get(shell) or bases.get(module) or next(iter(bases.values()))).

**Local steps**

- Set bases from get\_sidebar\_bases(list(module)).
- Return (bases.get(shell) or bases.get(module) or next(iter(bases.values()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bases.get(shell) → bases.get(module) → next(iter(bases.values())).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L2838) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1003)

<a id="op-1bdca558bd844e"></a>
### Sidebar for module

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_for_module`

**Inputs** payload, module.

**Declared result** (dict bitwise or no value).

**Explicit results** payload at module · next(generator of entry for entry drawn from payload.values() where entry.get(“module”) equals module, no value).

**Local steps**

- If module belongs to payload.
  - Return payload at module.
- Return next(generator of entry for entry drawn from payload.values() where entry.get(“module”) equals module, no value).
  - Draw entry from payload.values(), keep a combination only if (entry.get(“module”) equals module).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L3019) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1036)

<a id="op-426e024fdf445e"></a>
### Get sidebar items

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_sidebar_items`

**Inputs** sidebar\_names.

**Record and data access** read “Sidebar Item” via get\_all.

**Explicit results** mapping() · items.

**Local steps**

- If not sidebar\_names.
  - Return mapping().
- Set items from mapping().
- For each item in Platform.get\_all(“Sidebar Item”, filters = mapping(“parenttype” → “Sidebar”, “parent” → list(“in”, sidebar\_names)), fields = list(“parent”, “idx”, “type”, “label”, …), order\_by = “idx asc”).
  - Evaluate items.setdefault(item.parent, list()).append(item).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L30) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1012)

<a id="op-da4533c0bf47ba"></a>
### Get module workspaces

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_module_workspaces`

**Inputs** no declared parameters.

**Record and data access** read “Workspace” via get\_all.

**Explicit results** workspaces.

**Local steps**

- Bind dependencies get\_workspaces.
- Set workspaces from mapping().
- Set allowed from set of p.name for p drawn from get\_workspaces() at “pages”.
  - Draw p from get\_workspaces() at “pages”.
- For each row in Platform.get\_all(“Workspace”, filters = mapping(“module” → list(“is”, “set”)), fields = list(“name”, “module”), order\_by = “sequence\_id asc, creation asc”).
  - If row.name belongs to allowed.
    - Evaluate workspaces.setdefault(row.module, list()).append(row.name).
- Return workspaces.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L3609) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1007)

<a id="op-1ad7939e1e4068"></a>
### Get private workspaces

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_private_workspaces`

**Inputs** user.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** rows.

**Local steps**

- Bind dependencies get\_workspaces.
- Set rows from mapping().
- For each page in get\_workspaces() at “pages”.
  - If (page.public or not page.module or page.for\_user differs from user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.public → not page.module → page.for\_user differs from user.
    - Continue with the next iteration or loop test.
  - If (page.type and page.type differs from “Workspace”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in page.type → page.type differs from “Workspace”.
    - Continue with the next iteration or loop test.
  - Evaluate rows.setdefault(page.module, list()).append(Platform.\_dict(mapping(“type” → “Link”, “link\_type” → “Workspace”, “link\_to” → page.name, “label” → page.title, …))).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L3906) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1009)

<a id="op-15cb1ed87ddd5b"></a>
### Filter sidebar items

`operation_foundation_desk_record_definitions_sidebar_business_behavior_filter_sidebar_items`

**Inputs** items, perm\_ctx, check\_permission = true.

**Explicit results** filtered.

**Local steps**

- Set filtered from list().
- Set seen from set().
- For each item in items.
  - Set key from item\_key(item).
  - If key belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(key).
  - If (check\_permission and item.type does not belong to tuple(“Section Break”, “Spacer”) and not is\_item\_allowed(item.link\_to, item.link\_type, perm\_ctx)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in check\_permission → item.type does not belong to tuple(“Section Break”, “Spacer”) → not is\_item\_allowed(item.link\_to, item.link\_type, perm\_ctx).
    - Continue with the next iteration or loop test.
  - Set entry from mapping(“key” → key, “label” → translated item.label, “link\_to” → item.link\_to, “link\_type” → item.link\_type, …).
  - If item.hidden.
    - Set entry at “hidden” from 1.
  - Evaluate attach\_report(entry, item.link\_type, item.link\_to).
  - Evaluate filtered.append(entry).
- Return filtered.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L27) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L998)

<a id="op-d9d10067804a51"></a>
### Attach report

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_attach_report`

**Inputs** entry, link\_type, link\_to.

**Declared result** dict.

**Record and data access** read “Report” via get\_value.

**Explicit results** entry.

**Local steps**

- If (link\_type differs from “Report” or not link\_to).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_type differs from “Report” → not link\_to.
  - Return entry.
- Set report from Platform.db.get\_value(“Report”, link\_to, list(“report\_type”, “ref\_doctype”, “disabled”), as\_dict = true, cache = true).
- If (report and not report.disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in report → not report.disabled.
  - Set entry at “report” from mapping(“report\_type” → report.report\_type, “ref\_doctype” → report.ref\_doctype).
- Return entry.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L736)

<a id="op-d8559ab0527bfb"></a>
### Allowed added item

`operation_foundation_desk_record_definitions_sidebar_business_behavior_allowed_added_item`

**Inputs** item, perm\_ctx.

**Declared result** bool.

**Explicit results** true · is\_item\_allowed(item.get(“link\_to”), item.get(“link\_type”), perm\_ctx).

**Local steps**

- If (not item.get(“added”) or not is\_linked(item)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“added”) → not is\_linked(item).
  - Return true.
- Return is\_item\_allowed(item.get(“link\_to”), item.get(“link\_type”), perm\_ctx).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L5213) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L985)

<a id="op-04cfacda512333"></a>
### Append derived items

`operation_foundation_desk_record_definitions_sidebar_business_behavior_append_derived_items`

**Inputs** items, rows, perm\_ctx, hidden = tuple().

**Explicit results** items.

**Local steps**

- If not rows.
  - Return items.
- Set seen from (set of item at “key” for item drawn from items bitwise or set(hidden)).
  - Draw item from items.
- For each entry in filter\_sidebar\_items(rows, perm\_ctx).
  - If entry at “key” belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(entry at “key”).
  - Set entry at “derived” from 1.
  - Evaluate items.append(entry).
- Return items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L26) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L986)

<a id="op-91150746496fc6"></a>
### Get module landing route

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_module_landing_route`

**Inputs** items.

**Declared result** (str bitwise or no value).

**Record and data access** read “Workspace” via get\_value.

**Explicit results** no value · (“/desk/” + Platform.utils.slug(item at “link\_to”)) · (“/desk/private/” + Platform.utils.slug(page.title)) · doctype\_landing\_route(item).

**Local steps**

- Set item from next(generator of item for item drawn from (items or list()) where item.get(“type”) equals “Link”, no value).
  - Draw item from (items or list()), keep a combination only if (item.get(“type”) equals “Link”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items → list().
- If (not item or not item.get(“link\_to”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item → not item.get(“link\_to”).
  - Return no value.
- If item.get(“link\_type”) equals “Workspace”.
  - Set page from Platform.db.get\_value(“Workspace”, item at “link\_to”, list(“public”, “title”), as\_dict = true).
  - If not page.
    - Return no value.
  - If page.public.
    - Return (“/desk/” + Platform.utils.slug(item at “link\_to”)).
  - Return (“/desk/private/” + Platform.utils.slug(page.title)).
- If item.get(“link\_type”) equals “DocType”.
  - Return doctype\_landing\_route(item).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L28) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1005)

<a id="op-8d1dd8f4dd0c09"></a>
### Doctype landing route

`operation_foundation_desk_record_definitions_sidebar_business_behavior_record_type_landing_route`

**Inputs** item.

**Declared result** (str bitwise or no value).

**Record and data access** read “DocType” via exists.

**Explicit results** no value · route.

**Local steps**

- Set meta from Platform.get\_meta(item at “link\_to”) when Platform.db.exists(“DocType”, item at “link\_to”), otherwise no value.
  - Value choice on Platform.db.exists(“DocType”, item at “link\_to”) — true gives Platform.get\_meta(item at “link\_to”), false gives no value.
- If (not meta or meta.istable).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta → meta.istable.
  - Return no value.
- Set slug from Platform.utils.slug(item at “link\_to”).
- Set route from formatted text /desk/{slug}/{item at “link\_to”} when meta.issingle, otherwise formatted text /desk/{slug}.
  - Value choice on meta.issingle — true gives formatted text /desk/{slug}/{item at “link\_to”}, false gives formatted text /desk/{slug}.
- If item.get(“tab”).
  - Update route using + formatted text #{item at “tab”}.
- Return route.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0183.json#L6152) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1023)

<a id="op-d0e34dfe9df19d"></a>
### Build canonical shells

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_build_canonical_shells`

**Inputs** module\_sidebars, entity\_module, perm\_ctx, default\_workspace = no value.

**Declared result** tuple at tuple(dict, (str bitwise or no value)).

**Explicit results** tuple(canonical, home).

**Local steps**

- Set shells from ShellIndex(module\_sidebars).
- Set canonical from mapping of kind → mapping() for kind drawn from ROUTABLE\_ENTITY\_KINDS.
  - Draw kind from ROUTABLE\_ENTITY\_KINDS.
- Set homeless from list().
- For each tuple(kind, entities) in routable\_entities(perm\_ctx).items().
  - For each tuple(name, module) in entities.items().
    - Set shell from entity\_module.get(name) when entity\_module.get(name) belongs to shells.all, otherwise no value.
      - Value choice on entity\_module.get(name) belongs to shells.all — true gives entity\_module.get(name), false gives no value.
    - Set shell from (shell or shells.resolve(kind, name, module)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in shell → shells.resolve(kind, name, module).
    - If shell.
      - Set canonical at kind at name from shell.
    - Otherwise.
      - Evaluate homeless.append(tuple(kind, name, module)).
- Set home from home\_shell(module\_sidebars, canonical, dict(shells.workspace\_owners()), default\_workspace).
- For each tuple(kind, name, module) in homeless.
  - Set shell from (shells.shell\_of\_app(app\_of\_module(module)) or home).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in shells.shell\_of\_app(app\_of\_module(module)) → home.
  - If shell.
    - Set canonical at kind at name from shell.
- Return tuple(canonical, home).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L737)

<a id="op-14533ecd28be1f"></a>
### Home shell

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_home_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** module\_sidebars, canonical, workspace\_shells, default\_workspace.

**Explicit result forms** a value selected from the current context, no value, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L738)

<a id="op-7419b29cd5eeb2"></a>
### App of module

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_app_of_module`

**Inputs** module.

**Declared result** (str bitwise or no value).

**Explicit results** no value · (Platform.local.module\_app or mapping()).get(Platform.scrub(module)).

**Local steps**

- If not module.
  - Return no value.
- Return (Platform.local.module\_app or mapping()).get(Platform.scrub(module)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.module\_app → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L735)

<a id="op-5aadc9a0c2a890"></a>
### Shell Index.initialize

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_init`

**Inputs** self, module\_sidebars.

**Local steps**

- Set self.all from module\_sidebars.
- Set self.listing from mapping().
- Set self.of\_module from mapping().
- Set self.of\_workspace from mapping().
- Set self.of\_app from mapping().
- Set self.computed from set of shell for tuple(shell, sidebar) drawn from module\_sidebars.items() where sidebar.get(“computed”).
  - Draw tuple(shell, sidebar) from module\_sidebars.items(), keep a combination only if (sidebar.get(“computed”)).
- For each tuple(shell, sidebar) in module\_sidebars.items().
  - For each item in sidebar at “items”.
    - Set tuple(kind, entity) from tuple(item.get(“link\_type”), item.get(“link\_to”)).
    - If (kind and entity).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in kind → entity.
      - Evaluate self.listing.setdefault(tuple(kind, entity), list()).append(shell).
  - Set module from sidebar.get(“module”).
  - If module.
    - Evaluate self.of\_module.setdefault(module, shell).
  - If sidebar.get(“app”).
    - Evaluate self.of\_app.setdefault(sidebar at “app”, shell).
  - For each workspace in (sidebar.get(“workspaces”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sidebar.get(“workspaces”) → list().
    - Evaluate self.of\_workspace.setdefault(workspace, shell).
- Set self.heirs from mapping of module → list of shell for heir drawn from heirs where shell bound to self.shell\_of(heir) for tuple(module, heirs) drawn from get\_code\_only\_module\_heirs().items().
  - Draw tuple(module, heirs) from get\_code\_only\_module\_heirs().items().
  - Draw heir from heirs, keep a combination only if (shell bound to self.shell\_of(heir)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [shell of](operations-061.md#op-c1d989bf0e2886).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L745)

<a id="op-91befe45591309"></a>
### Shell Index.workspace owners

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_workspace_owners`

**Inputs** self.

**Explicit results** self.of\_workspace.items().

**Local steps**

- Return self.of\_workspace.items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L750)

<a id="op-c1d989bf0e2886"></a>
### Shell Index.shell of

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_shell_of`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, module.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L748)

<a id="op-a7eb89685a2c1f"></a>
### Shell Index.shell of app

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_shell_of_app`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, app.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L749)

<a id="op-bb63836d421930"></a>
### Shell Index.listed in

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_listed_in`

**Inputs** self, kind, entity.

**Declared result** list at str.

**Explicit results** self.listing.get(tuple(kind, entity), list()).

**Local steps**

- Return self.listing.get(tuple(kind, entity), list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L746)
