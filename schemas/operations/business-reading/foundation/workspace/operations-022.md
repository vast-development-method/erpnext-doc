# Forms, reports and navigation · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Desktop

<a id="op-98bea89d4b17a0"></a>
### Clean up

`operation_foundation_desk_desktop_business_behavior_clean_up`

**Inputs** original\_page, blocks.

**Local steps**

- Set page\_widgets from mapping().
- For each wid in list(“shortcut”, “card”, “chart”, “quick\_list”, …).
  - Set page\_widgets at wid from list of x at “data” at (wid + “\_name”) for x drawn from loads(blocks) where x at “type” equals wid.
    - Draw x from loads(blocks), keep a combination only if (x at “type” equals wid).
- For each wid in list(“shortcut”, “chart”, “quick\_list”, “number\_card”, …).
  - Set updated\_widgets from list().
  - Evaluate original\_page.get((wid + “s”)).reverse().
  - For each w in original\_page.get((wid + “s”)).
    - If (w.label belongs to page\_widgets at wid and w.label does not belong to list of x.label for x drawn from updated\_widgets).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in w.label belongs to page\_widgets at wid → w.label does not belong to list of x.label for x drawn from updated\_widgets.
      - Draw x from updated\_widgets.
      - Evaluate updated\_widgets.append(w).
  - Evaluate original\_page.set((wid + “s”), updated\_widgets).
- For each tuple(i, v) in enumerate(original\_page.links).
  - If (v.type equals “Card Break” and v.label does not belong to page\_widgets at “card”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in v.type equals “Card Break” → v.label does not belong to page\_widgets at “card”.
    - Remove original\_page.links at slice i to ((i + v.link\_count) + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L1214) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L88)

<a id="op-63f5ecd6002db9"></a>
### New widget

`operation_foundation_desk_desktop_business_behavior_new_widget`

**Inputs** config, doctype, parentfield.

**State and service calls** request new\_doc for doctype.

**Explicit results** list() · prepare\_widget\_list.

**Local steps**

- If not config.
  - Return list().
- Set prepare\_widget\_list from list().
- For each tuple(idx, widget) in enumerate(config).
  - Evaluate widget.pop(“name”, no value).
  - Set doc from Platform.new\_doc(doctype).
  - Evaluate doc.update(widget).
  - Set doc.idx from (idx + 1).
  - Set doc.parentfield from parentfield.
  - Evaluate prepare\_widget\_list.append(doc).
- Return prepare\_widget\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L1853) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L98)

<a id="op-fbd32a1c15d2e4"></a>
### Prepare widget

`operation_foundation_desk_desktop_business_behavior_prepare_widget`

**Inputs** config, doctype, parentfield.

**State and service calls** request new\_doc for doctype.

**Explicit results** list() · prepare\_widget\_list.

**Local steps**

- If not config.
  - Return list().
- Set order from config.get(“order”).
- Set widgets from config.get(“widgets”).
- Set prepare\_widget\_list from list().
- For each tuple(idx, name) in enumerate(order).
  - Set wid\_config from widgets at name.copy().
  - Evaluate wid\_config.pop(“name”, no value).
  - Set doc from Platform.new\_doc(doctype).
  - Evaluate doc.update(wid\_config).
  - Set doc.idx from (idx + 1).
  - Set doc.parentfield from parentfield.
  - Evaluate prepare\_widget\_list.append(doc).
- Return prepare\_widget\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L2127) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L100)

<a id="op-f15d04d1b3a764"></a>
### Update onboarding step

`operation_foundation_desk_desktop_business_behavior_update_onboarding_step`

**Inputs** name, field, value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Onboarding Step” via get\_doc.

**State and service calls** request set\_value on “Onboarding Step”.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to update this onboarding step”.

**Local steps**

- Bind dependencies can\_update\_step, capture\_step\_update, update\_completion.
- Set allowed\_fields from list(“is\_skipped”, “is\_complete”).
- If field does not belong to allowed\_fields.
  - Return no value.
- If not can\_update\_step(name).
  - Call the validation error handler Platform.throw(translated “You are not allowed to update this onboarding step”, Platform.PermissionError).
- If (field equals “is\_complete” and cint(value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals “is\_complete” → cint(value).
  - Evaluate Platform.get\_doc(“Onboarding Step”, name).throw\_if\_unfinished().
- Evaluate Platform.db.set\_value(“Onboarding Step”, name, field, cint(value)).
- Evaluate capture\_step\_update(name, field, cint(value)).
- Evaluate update\_completion(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L42) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L102)

<a id="op-4049121717eed8"></a>
### Get installed apps

`operation_foundation_desk_desktop_business_behavior_get_installed_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.get\_installed\_apps().

**Local steps**

- Return Platform.get\_installed\_apps().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L40) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L93)

## Workspace · Desktop

<a id="op-bc207d0c77454f"></a>
### Get context

`operation_foundation_desk_page_desktop_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “Navbar Settings” via get\_single\_value · read “User” via get\_cached\_value · resolve a document from “Desktop Layout” via get\_doc.

**Explicit results** context.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set Platform.local.flags.redirect\_location from “/app”.
  - Raise Platform.Redirect.
- Set brand\_logo from no value.
- Set brand\_logo from Platform.get\_single\_value(“Navbar Settings”, “app\_logo”).
- If not brand\_logo.
  - Set brand\_logo from Platform.get\_hooks(“app\_logo\_url”, app\_name = “Platform”) at 0.
- Set context.brand\_logo from brand\_logo.
- Set context.show\_search\_bar from Platform.get\_cached\_value(“User”, Platform.session.user, “search\_bar”).
- If is\_desktop\_icons\_page().
  - Attempt the following.
    - Set context.desktop\_layout from (Platform.get\_doc(“Desktop Layout”, Platform.session.user).layout or mapping()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_doc(“Desktop Layout”, Platform.session.user).layout → mapping().
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Set context.desktop\_layout from mapping().
- Return context.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Navbar Settings”, “app\_logo”), Platform.get\_cached\_value(“User”, Platform.session.user, “search\_bar”) · selected callable from Platform.get\_hooks(“app\_logo\_url”, app\_name = “Platform”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L1125) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L333)

## Record · Desktop icon

[Record definition](../../../../data/record-types/desktop_icon.json)

<a id="op-be56f0bacd4fe9"></a>
### Desktop Icon.validate

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_validate`

**Inputs** self.

**Local steps**

- If not self.label.
  - Set self.label from self.module\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L906) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L661)

<a id="op-0329c751880a40"></a>
### Desktop Icon.on trash

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_on_trash`

**Inputs** self.

**Local steps**

- Evaluate clear\_every\_users\_desktop\_icons().
- If (Platform.conf.developer\_mode and self.standard and self.app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.standard → self.app.
  - Evaluate delete\_desktop\_icon\_file(self.app, self.label).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L120) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L659)

<a id="op-a1559ebb84da44"></a>
### Desktop Icon.check for restrict removal

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_check_for_restrict_removal`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot delete Desktop Icon '{0}' as it is restricted”.format(self.label).

**Local steps**

- If self.restrict\_removal.
  - Call the validation error handler Platform.throw(translated “Cannot delete Desktop Icon '{0}' as it is restricted”.format(self.label)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L1099) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L656)

<a id="op-5fc205e960094c"></a>
### Desktop Icon.on update

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_desktop\_icon().
- Evaluate clear\_every\_users\_desktop\_icons().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export desktop icon](operations-022.md#op-44b28e7daeef8a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L121) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L660)

<a id="op-f9af6c9870d2e3"></a>
### Desktop Icon.after rename

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_after_rename`

**Inputs** self, old, new, merge.

**Local steps**

- Evaluate delete\_desktop\_icon\_file(self.app, old).
- Evaluate self.export\_desktop\_icon().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export desktop icon](operations-022.md#op-44b28e7daeef8a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L1355) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L655)

<a id="op-44b28e7daeef8a"></a>
### Desktop Icon.export desktop icon

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_export_desktop_icon`

**Inputs** self.

**Local steps**

- Set allow\_export from (self.standard and self.app and not Platform.flags.in\_import and Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard → self.app → not Platform.flags.in\_import → Platform.conf.developer\_mode.
- If allow\_export.
  - Set folder\_path from create\_directory\_on\_app\_path(“desktop\_icon”, self.app).
  - Set file\_path from os.path.join(folder\_path, formatted text {Platform.scrub(self.label)}.json).
  - Set doc\_export from self.as\_dict(no\_nulls = true, no\_private\_properties = true).
  - Evaluate strip\_default\_fields(self, doc\_export).
  - Within open(file\_path, “w+”) bound as icon\_file\_doc.
    - Evaluate icon\_file\_doc.write((Platform.as\_json(doc\_export) + whitespace '\\n')).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L1458) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L658)

<a id="op-b1de09ecf427f9"></a>
### Desktop Icon.delete desktop icon file

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_desktop_icon_delete_desktop_icon_file`

**Inputs** self.

**Local steps**

- Set folder\_path from create\_directory\_on\_app\_path(“desktop\_icon”, self.app).
- Set file\_path from os.path.join(folder\_path, formatted text {Platform.scrub(self.label)}.json).
- If os.path.exists(file\_path).
  - Evaluate os.remove(file\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L1824) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L657)

<a id="op-dee0ec6303b638"></a>
### Delete desktop icon file

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_delete_desktop_icon_file`

**Inputs** app, label.

**Local steps**

- Set folder\_path from create\_directory\_on\_app\_path(“desktop\_icon”, app).
- Set file\_path from os.path.join(folder\_path, formatted text {Platform.scrub(label)}.json).
- If os.path.exists(file\_path).
  - Evaluate os.remove(file\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L2068) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L654)

<a id="op-995e0ac2e0431c"></a>
### Get workspace names

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_get_workspace_names`

**Inputs** workspaces.

**Explicit results** workspace\_list.

**Local steps**

- Set workspace\_list from list().
- For each w in workspaces at “pages”.
  - Evaluate workspace\_list.append(w at “name”).
- Return workspace\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L2262) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L665)

<a id="op-e1147f94b90178"></a>
### Is icon permitted

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_is_icon_permitted`

**Inputs** icon, bootinfo, roles, icon\_module.

**Declared result** bool.

**Explicit results** false · true · \_has\_app\_permission(icon) · bool(sidebar).

**Local steps**

- Bind dependencies sidebar\_for\_module.
- Bind dependencies is\_module\_visible.
- If (icon\_module and not is\_module\_visible(icon\_module)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon\_module → not is\_module\_visible(icon\_module).
  - Return false.
- If (roles and not set(roles).intersection(Platform.get\_roles())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in roles → not set(roles).intersection(Platform.get\_roles()).
  - Return false.
- If icon.icon\_type equals “Folder”.
  - Return true.
- Otherwise.
  - If icon.icon\_type equals “App”.
    - Return \_has\_app\_permission(icon).
  - Otherwise.
    - Set sidebar from sidebar\_for\_module((bootinfo.module\_sidebars or mapping()), (icon\_module or icon.label)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in bootinfo.module\_sidebars → mapping().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in icon\_module → icon.label.
    - Return bool(sidebar).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L2370) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L668)

<a id="op-42e768c4676ccd"></a>
### Has app permission

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_has_application_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** icon.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L123) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L666)

<a id="op-69d6dc17e9b653"></a>
### Get roles by icon

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_get_roles_by_icon`

**Inputs** icons.

**Declared result** dict at tuple(str, list at str).

**Record and data access** read “Has Role” via get\_all.

**Explicit results** mapping() · roles\_by\_icon.

**Local steps**

- If not icons.
  - Return mapping().
- Set roles\_by\_icon from mapping().
- For each row in Platform.get\_all(“Has Role”, filters = mapping(“parenttype” → “Desktop Icon”, “parent” → tuple(“in”, list of icon.name for icon drawn from icons)), fields = list(“parent”, “role”)).
  - Draw icon from icons.
  - Evaluate roles\_by\_icon.setdefault(row.parent, list()).append(row.role).
- Return roles\_by\_icon.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L3100) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L664)

<a id="op-b50a520f6c309a"></a>
### Get linked workspace modules

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_get_linked_workspace_modules`

**Inputs** icons.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Workspace” via get\_all.

**Explicit results** mapping() · mapping of name → modules.get(workspace) for tuple(name, workspace) drawn from linked.items().

**Local steps**

- Set linked from mapping of icon.name → icon.link\_to for icon drawn from icons where (icon.icon\_type equals “Link” and icon.link\_to).
  - Draw icon from icons, keep a combination only if ((icon.icon\_type equals “Link” and icon.link\_to)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon.icon\_type equals “Link” → icon.link\_to.
- If not linked.
  - Return mapping().
- Set modules from dict(Platform.get\_all(“Workspace”, filters = mapping(“name” → tuple(“in”, list(set(nested operand in the contract())))), fields = list(“name”, “module”), as\_list = true)).
- Return mapping of name → modules.get(workspace) for tuple(name, workspace) drawn from linked.items().
  - Draw tuple(name, workspace) from linked.items().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L3415) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L663)

<a id="op-0128830e9edf6c"></a>
### Is shared icon

`operation_foundation_binding_foundation_desk_doctype_desktop_icon_desktop_icon_is_shared_icon`

**Inputs** icon, private\_workspaces.

**Declared result** bool.

**Explicit results** (icon.icon\_type equals “Link” and icon.link\_to does not belong to private\_workspaces).

**Local steps**

- Return (icon.icon\_type equals “Link” and icon.link\_to does not belong to private\_workspaces).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon.icon\_type equals “Link” → icon.link\_to does not belong to private\_workspaces.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L686)

<a id="op-5c796de42c2df2"></a>
### Get private workspaces

`operation_foundation_binding_foundation_desk_doctype_desktop_icon_desktop_icon_get_private_workspaces`

**Inputs** icons.

**Declared result** set at str.

**Record and data access** read “Workspace” via get\_all.

**Explicit results** set() · set(Platform.get\_all(“Workspace”, filters = mapping(“name” → tuple(“in”, list(linked)), “public” → 0), pluck = “name”)).

**Local steps**

- Set linked from set of icon.link\_to for icon drawn from icons where (icon.icon\_type equals “Link” and icon.link\_to).
  - Draw icon from icons, keep a combination only if ((icon.icon\_type equals “Link” and icon.link\_to)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon.icon\_type equals “Link” → icon.link\_to.
- If not linked.
  - Return set().
- Return set(Platform.get\_all(“Workspace”, filters = mapping(“name” → tuple(“in”, list(linked)), “public” → 0), pluck = “name”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L684)

<a id="op-598849d078049a"></a>
### Get desktop icons

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_get_desktop_icons`

**Inputs** user = no value, bootinfo = no value.

**Record and data access** read “Desktop Icon” via get\_all.

**Explicit results** user\_icons.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Set user\_icons from Platform.cache.hget(“desktop\_icons”, user).
- If not user\_icons.
  - Set fields from list(“label”, “bg\_color”, “link”, “link\_type”, …).
  - Set rows from Platform.get\_all(“Desktop Icon”, fields = list(expanded fields, “owner”)).
  - Set private\_workspaces from get\_private\_workspaces(rows).
  - Set user\_icons from list of row for row drawn from rows where (row.standard or row.owner belongs to tuple(“Administrator”, user) or is\_shared\_icon(row, private\_workspaces)).
    - Draw row from rows, keep a combination only if ((row.standard or row.owner belongs to tuple(“Administrator”, user) or is\_shared\_icon(row, private\_workspaces))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.standard → row.owner belongs to tuple(“Administrator”, user) → is\_shared\_icon(row, private\_workspaces).
  - For each row in user\_icons.
    - Remove row at “owner”.
  - Evaluate user\_icons.sort(key = deferred anonymous expression).
  - Set permitted\_icons from list().
  - Set permitted\_parent\_labels from set().
  - If bootinfo.
    - Set roles\_by\_icon from get\_roles\_by\_icon(user\_icons).
    - Set modules\_by\_icon from get\_linked\_workspace\_modules(user\_icons).
    - For each s in user\_icons.
      - Set icon\_module from modules\_by\_icon.get(s.name).
      - If is\_icon\_permitted(s, bootinfo, roles = roles\_by\_icon.get(s.name, list()), icon\_module = icon\_module).
        - Set s.module from icon\_module.
        - Evaluate permitted\_icons.append(s).
        - If not s.parent\_icon.
          - Evaluate permitted\_parent\_labels.add(s.label).
  - Set user\_icons from list of s for s drawn from permitted\_icons where (not s.parent\_icon or s.parent\_icon belongs to permitted\_parent\_labels).
    - Draw s from permitted\_icons, keep a combination only if ((not s.parent\_icon or s.parent\_icon belongs to permitted\_parent\_labels)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not s.parent\_icon → s.parent\_icon belongs to permitted\_parent\_labels.
  - Evaluate Platform.cache.hset(“desktop\_icons”, user, user\_icons).
- Return user\_icons.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L122) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L662)

<a id="op-8e226681891d35"></a>
### Clear desktop icons cache

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_clear_desktop_icons_cache`

**Inputs** user = no value.

**Local steps**

- Evaluate Platform.cache.hdel(“desktop\_icons”, (user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Evaluate Platform.cache.hdel(“bootinfo”, (user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L4780) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L649)

<a id="op-bb0993eb6551f3"></a>
### Is desk link

`operation_foundation_binding_foundation_desk_doctype_desktop_icon_desktop_icon_is_desk_link`

**Inputs** link.

**Declared result** bool.

**Explicit results** bool((link and DESK\_LINK\_PATTERN.match(link))).

**Local steps**

- Return bool((link and DESK\_LINK\_PATTERN.match(link))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in link → DESK\_LINK\_PATTERN.match(link).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L685)
