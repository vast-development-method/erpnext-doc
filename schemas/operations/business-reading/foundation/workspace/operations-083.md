# Forms, reports and navigation · operations 83

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workspace

[Record definition](../../../../data/record-types/workspace.json)

<a id="op-9fc73fb6688947"></a>
### Make module workspace

`operation_foundation_desk_record_definitions_workspace_business_behavior_make_module_workspace`

**Inputs** module, icon = no value.

**Declared result** (str bitwise or no value).

**Record and data access** resolve a document from mapping(“doctype” → “Workspace”, “label” → module, “title” → module, “module” → module, …) via get\_doc.

**State and service calls** request set\_value on “Workspace” · call insert on page.

**Explicit results** no value · existing.name · page.name.

**Local steps**

- If existing bound to module\_page(module).
  - If existing.module differs from module.
    - Return no value.
  - If icon.
    - Evaluate Platform.db.set\_value(“Workspace”, existing.name, “icon”, icon).
  - Return existing.name.
- Set page from Platform.get\_doc(mapping(“doctype” → “Workspace”, “label” → module, “title” → module, “module” → module, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in icon → no value.
- Set page.flags.with\_module from true.
- Evaluate page.insert(ignore\_permissions = true).
- Return page.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L932) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1313)

<a id="op-0fab09791ecd8d"></a>
### Workspace payload

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_payload`

**Inputs** remaining named values extra.

**Explicit results** mapping(“workspace\_pages” → workspaces, “app\_data” → get\_app\_data(), “module\_sidebars” → module\_sidebars, “entity\_module” → build\_entity\_module\_map(module\_sidebars), …).

**Local steps**

- Bind dependencies build\_entity\_module\_map, get\_app\_data, get\_module\_sidebars.
- Set workspaces from get\_workspaces().
- Set module\_sidebars from get\_module\_sidebars().
- Return mapping(“workspace\_pages” → workspaces, “app\_data” → get\_app\_data(), “module\_sidebars” → module\_sidebars, “entity\_module” → build\_entity\_module\_map(module\_sidebars), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L1387) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1338)

<a id="op-1c858df7446607"></a>
### Can edit workspace

`operation_foundation_desk_record_definitions_workspace_business_behavior_can_edit_workspace`

**Inputs** doc.

**Explicit results** (is\_workspace\_manager() or (not doc.public and doc.for\_user equals Platform.session.user)).

**Local steps**

- Return (is\_workspace\_manager() or (not doc.public and doc.for\_user equals Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_workspace\_manager() → (not doc.public and doc.for\_user equals Platform.session.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.public → doc.for\_user equals Platform.session.user.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L1558) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1298)

<a id="op-254ce1b0a8ec49"></a>
### Get link type

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_link_type`

**Inputs** key.

**Explicit results** link\_type\_map at key · “DocType”.

**Local steps**

- Set key from key.lower().
- Set link\_type\_map from mapping(“doctype” → “DocType”, “page” → “Page”, “report” → “Report”).
- If key belongs to link\_type\_map.
  - Return link\_type\_map at key.
- Return “DocType”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L1657) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1305)

<a id="op-08e26527e62d32"></a>
### Get report type

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_report_type`

**Inputs** report.

**Record and data access** read “Report” via get\_value.

**Explicit results** report\_type belongs to list(“Query Report”, “Script Report”, “Custom Report”).

**Local steps**

- Set report\_type from Platform.get\_value(“Report”, report, “report\_type”).
- Return report\_type belongs to list(“Query Report”, “Script Report”, “Custom Report”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L1837) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1308)

<a id="op-2ab13b1b44a426"></a>
### New page

`operation_foundation_desk_record_definitions_workspace_business_behavior_new_page`

**Inputs** new\_page.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Workspace” · call save on doc.

**Explicit results** no value · workspace\_payload().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to create a workspace others can see.” · validation helper with Platform.PermissionError — translated “Cannot create private workspace of other users” · Platform.PermissionError.

**Local steps**

- Set page from Platform.parse\_json(new\_page).
- If not page.
  - Return no value.
- If (page.get(“public”) and not is\_workspace\_manager()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in page.get(“public”) → not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to create a workspace others can see.”, Platform.PermissionError).
- Otherwise.
  - If (not page.get(“public”) and page.get(“for\_user”) differs from Platform.session.user and not is\_workspace\_manager()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not page.get(“public”) → page.get(“for\_user”) differs from Platform.session.user → not is\_workspace\_manager().
    - Call the validation error handler Platform.throw(translated “Cannot create private workspace of other users”, Platform.PermissionError).
  - Otherwise.
    - If not Platform.has\_permission(doctype = “Workspace”, ptype = “create”).
      - Set Platform.flags.error\_message from translated “User {0} does not have the permission to create a Workspace.”.format(Platform.bold(Platform.session.user)).
      - Raise Platform.PermissionError.
- Set doc from Platform.new\_doc(“Workspace”).
- Set doc.title from page.get(“title”).
- Set doc.icon from (page.get(“icon”) or “grid”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.get(“icon”) → “grid”.
- Set doc.content from page.get(“content”).
- Set doc.parent\_page from page.get(“parent\_page”).
- Set doc.label from page.get(“label”).
- Set doc.for\_user from page.get(“for\_user”).
- Set doc.public from page.get(“public”).
- For each role in (page.get(“roles”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.get(“roles”) → list().
  - If role.get(“role”).
    - Evaluate doc.append(“roles”, mapping(“role” → role.get(“role”))).
- Set doc.module from (page.get(“module”) or first\_module\_of\_app(page.get(“app”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.get(“module”) → first\_module\_of\_app(page.get(“app”)).
- Set doc.type from page.get(“type”).
- Set doc.link\_to from page.get(“link\_to”).
- Set doc.link\_type from page.get(“link\_type”).
- Set doc.external\_link from page.get(“external\_link”).
- Set doc.sequence\_id from (last\_sequence\_id(doc) + 1).
- Evaluate doc.save(ignore\_permissions = true).
- If doc.public.
  - Evaluate add\_to\_sidebar(doc).
- Return workspace\_payload().

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype = “Workspace”, ptype = “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L41) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1316)

<a id="op-c21e6f22404297"></a>
### Ensure module

`operation_foundation_desk_record_definitions_workspace_business_behavior_ensure_module`

**Inputs** module.

**Declared result** no value.

**Record and data access** read “Module Def” via exists · resolve a document from mapping(“doctype” → “Module Def”, “module\_name” → module, “custom” → 1) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Module Def”, “module\_name” → module, “custom” → 1)).

**Explicit results** no value.

**Local steps**

- If Platform.db.exists(“Module Def”, module).
  - Return no value.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Module Def”, “module\_name” → module, “custom” → 1)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L3232) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1302)

<a id="op-da566d7008d654"></a>
### Triage module

`operation_foundation_desk_record_definitions_workspace_business_behavior_triage_module`

**Inputs** for\_user = no value.

**Declared result** str.

**Explicit results** module.

**Local steps**

- Set module from PRIVATE\_MODULE when for\_user, otherwise CUSTOM\_MODULE.
  - Value choice on for\_user — true gives PRIVATE\_MODULE, false gives CUSTOM\_MODULE.
- Evaluate ensure\_module(module).
- Return module.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L3411) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1321)

<a id="op-80da4c13170670"></a>
### Get workspace app

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_workspace_application`

**Inputs** doc.

**Declared result** (str bitwise or no value).

**Record and data access** read “Module Def” via get\_value.

**Explicit results** no value · Platform.db.get\_value(“Module Def”, doc.module, “app\_name”).

**Local steps**

- If not doc.module.
  - Return no value.
- Return Platform.db.get\_value(“Module Def”, doc.module, “app\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L3512) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1309)

<a id="op-6699040624561d"></a>
### First module of app

`operation_foundation_desk_record_definitions_workspace_business_behavior_first_module_of_application`

**Inputs** app.

**Declared result** (str bitwise or no value).

**Explicit results** no value · modules at 0 when modules, otherwise no value.

**Local steps**

- If not app.
  - Return no value.
- Set modules from Platform.get\_module\_list(app).
- Return modules at 0 when modules, otherwise no value.
  - Value choice on modules — true gives modules at 0, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L3626) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1303)

<a id="op-bbe3bbbabd5d8c"></a>
### Add to sidebar

`operation_foundation_desk_record_definitions_workspace_business_behavior_add_to_sidebar`

**Inputs** workspace.

**Record and data access** read “Sidebar” via get\_all · resolve a document from “Sidebar” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies add\_site\_sidebar\_item.
- If (workspace.type and workspace.type differs from “Workspace”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in workspace.type → workspace.type differs from “Workspace”.
  - Return no value.
- If not workspace.public.
  - Evaluate add\_private\_to\_sidebar(workspace).
  - Return no value.
- If not workspace.module.
  - Return no value.
- Set shells from Platform.get\_all(“Sidebar”, filters = mapping(“module” → workspace.module), pluck = “name”).
- If not shells.
  - Return no value.
- For each shell in shells.
  - Set sidebar from Platform.get\_cached\_doc(“Sidebar”, shell).
  - If any(generator of (item.link\_type equals “Workspace” and item.link\_to equals workspace.name) for item drawn from sidebar.items).
    - Draw item from sidebar.items.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.link\_type equals “Workspace” → item.link\_to equals workspace.name.
    - Return no value.
- Evaluate add\_site\_sidebar\_item(workspace.module, mapping(“type” → “Link”, “label” → workspace.title, “link\_type” → “Workspace”, “link\_to” → workspace.name, …)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Sidebar”, shell).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L40) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1297)

<a id="op-4d4cc9013f3af8"></a>
### Add private to sidebar

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_add_private_to_sidebar`

**Inputs** workspace.

**Explicit results** no value.

**Local steps**

- Bind dependencies add\_user\_sidebar\_item.
- If (not workspace.for\_user or not workspace.module).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not workspace.for\_user → not workspace.module.
  - Return no value.
- Evaluate ensure\_module(PRIVATE\_MODULE).
- Set row from mapping(“type” → “Link”, “label” → workspace.title, “link\_type” → “Workspace”, “link\_to” → workspace.name, …).
- For each module in dict.fromkeys(list(PRIVATE\_MODULE, workspace.module)).
  - Evaluate add\_user\_sidebar\_item(module, workspace.for\_user, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L757)

<a id="op-e6930be45dd09f"></a>
### Save page

`operation_foundation_desk_record_definitions_workspace_business_behavior_save_page`

**Inputs** name, public, new\_widgets, blocks.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_doc.

**Explicit results** mapping(“name” → name, “public” → public, “label” → doc.label).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to edit this workspace.”.

**Local steps**

- Set public from Platform.parse\_json(public).
- Set doc from Platform.get\_doc(“Workspace”, name).
- Set can\_edit from can\_edit\_workspace(doc).
- If not can\_edit.
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to edit this workspace.”, Platform.PermissionError).
- If (doc.standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard → not Platform.conf.developer\_mode.
  - Bind dependencies upsert\_content\_customization.
  - Evaluate upsert\_content\_customization(name, Platform.parse\_json(blocks), Platform.parse\_json((new\_widgets or “{}”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_widgets → “{}”.
  - Return mapping(“name” → name, “public” → public, “label” → doc.label).
- If not doc.type.
  - Set doc.type from “Workspace”.
- Set doc.content from blocks.
- Evaluate save\_new\_widget(doc, name, blocks, new\_widgets).
- Return mapping(“name” → name, “public” → public, “label” → doc.label).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L42) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1319)

<a id="op-50ed3ca74cccf7"></a>
### Update page

`operation_foundation_desk_record_definitions_workspace_business_behavior_update_page`

**Inputs** name, title, icon, indicator\_color, parent, public.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_doc · read “Workspace” via get\_all · read “Workspace” via count.

**State and service calls** call save on doc · call save on child\_doc.

**Explicit results** mapping(“name” → doc.title, “public” → doc.public, “label” → doc.label) · mapping(“name” → title, “public” → public, “label” → new\_name).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Need Workspace Manager role to edit public workspaces.” · validation helper with Platform.PermissionError — translated “Need Workspace Manager role to edit private workspace of other users.”.

**Local steps**

- Set public from Platform.parse\_json(public).
- Set doc from Platform.get\_doc(“Workspace”, name).
- If (doc.get(“public”) and not is\_workspace\_manager()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“public”) → not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(translated “Need Workspace Manager role to edit public workspaces.”, Platform.PermissionError).
- Otherwise.
  - If (not doc.get(“public”) and doc.get(“for\_user”) differs from Platform.session.user and not is\_workspace\_manager()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.get(“public”) → doc.get(“for\_user”) differs from Platform.session.user → not is\_workspace\_manager().
    - Call the validation error handler Platform.throw(translated “Need Workspace Manager role to edit private workspace of other users.”, Platform.PermissionError).
- If (doc.standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard → not Platform.conf.developer\_mode.
  - Bind dependencies upsert\_property\_customization.
  - Evaluate upsert\_property\_customization(name, icon = icon, indicator\_color = indicator\_color).
  - Return mapping(“name” → doc.title, “public” → doc.public, “label” → doc.label).
- If doc.
  - Set child\_docs from Platform.get\_all(“Workspace”, filters = mapping(“parent\_page” → doc.title, “public” → doc.public)).
  - Set doc.title from title.
  - Set doc.icon from icon.
  - Set doc.indicator\_color from indicator\_color.
  - Set doc.parent\_page from parent.
  - If doc.public differs from public.
    - Set doc.sequence\_id from Platform.db.count(“Workspace”, mapping(“public” → public), cache = true).
    - Set doc.public from public.
  - Set doc.for\_user from empty text when public, otherwise (doc.for\_user or Platform.session.user).
    - Value choice on public — true gives empty text, false gives (doc.for\_user or Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.for\_user → Platform.session.user.
  - Set doc.label, new\_name from formatted text {title}-{doc.for\_user} when doc.for\_user, otherwise title.
    - Value choice on doc.for\_user — true gives formatted text {title}-{doc.for\_user}, false gives title.
  - Evaluate doc.save(ignore\_permissions = true).
  - If name differs from new\_name.
    - Evaluate rename\_doc(“Workspace”, name, new\_name, force = true, ignore\_permissions = true).
  - If child\_docs.
    - For each child in child\_docs.
      - Set child\_doc from Platform.get\_doc(“Workspace”, child.name).
      - Set child\_doc.parent\_page from doc.title.
      - If child\_doc.public differs from public.
        - Set child\_doc.public from public.
      - Set child\_doc.for\_user from empty text when public, otherwise (child\_doc.for\_user or Platform.session.user).
        - Value choice on public — true gives empty text, false gives (child\_doc.for\_user or Platform.session.user).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_doc.for\_user → Platform.session.user.
      - Set child\_doc.label, new\_child\_name from formatted text {child\_doc.title}-{child\_doc.for\_user} when child\_doc.for\_user, otherwise child\_doc.title.
        - Value choice on child\_doc.for\_user — true gives formatted text {child\_doc.title}-{child\_doc.for\_user}, false gives child\_doc.title.
      - Evaluate child\_doc.save(ignore\_permissions = true).
      - If child.name differs from new\_child\_name.
        - Evaluate rename\_doc(“Workspace”, child.name, new\_child\_name, force = true, ignore\_permissions = true).
  - Evaluate add\_to\_sidebar(Platform.get\_doc(“Workspace”, new\_name)).
- Return mapping(“name” → title, “public” → public, “label” → new\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L43) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1322)

<a id="op-6b95636d4974d3"></a>
### Get manageable workspaces

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_manageable_workspaces`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Workspace” via get\_all.

**Explicit results** Platform.get\_all(“Workspace”, fields = fields, filters = filters, order\_by = “public desc, sequence\_id asc”, ignore\_permissions = true).

**Local steps**

- Set fields from list(“name”, “title”, “icon”, “public”, …).
- If is\_workspace\_manager().
  - Set filters from mapping().
- Otherwise.
  - Set filters from mapping(“public” → 0, “for\_user” → Platform.session.user).
- Return Platform.get\_all(“Workspace”, fields = fields, filters = filters, order\_by = “public desc, sequence\_id asc”, ignore\_permissions = true).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L6411) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1306)

<a id="op-b8b4d68d4f6e41"></a>
### Get workspace settings

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_workspace_settings`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_cached\_doc.

**Explicit results** mapping(“name” → doc.name, “title” → doc.title, “icon” → icon, “indicator\_color” → indicator\_color, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to manage this workspace.”.

**Local steps**

- Bind dependencies effective\_roles, get\_customization.
- Set doc from Platform.get\_cached\_doc(“Workspace”, name).
- Set can\_edit from can\_edit\_workspace(doc).
- If not can\_edit.
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to manage this workspace.”, Platform.PermissionError).
- Set is\_standard from (bool(doc.standard) and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(doc.standard) → not Platform.conf.developer\_mode.
- Set roles from list of r.role for r drawn from doc.roles.
  - Draw r from doc.roles.
- Set icon from doc.icon.
- Set indicator\_color from doc.indicator\_color.
- If (is\_standard and customization bound to get\_customization(name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_standard → customization bound to get\_customization(name).
  - Set roles from effective\_roles(list of r.role for r drawn from doc.roles, customization).
    - Draw r from doc.roles.
  - Set icon from (customization.icon or icon).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.icon → icon.
  - Set indicator\_color from (customization.indicator\_color or indicator\_color).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.indicator\_color → indicator\_color.
- If not doc.public.
  - Set access from “private”.
- Otherwise.
  - If roles.
    - Set access from “group”.
  - Otherwise.
    - Set access from “public”.
- Return mapping(“name” → doc.name, “title” → doc.title, “icon” → icon, “indicator\_color” → indicator\_color, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workspace”, name).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L6683) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1310)

<a id="op-44f134c65aa82d"></a>
### Update workspace settings

`operation_foundation_desk_record_definitions_workspace_business_behavior_update_workspace_settings`

**Inputs** name, title = no value, icon = no value, indicator\_color = no value, access = no value, roles = no value, module = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_doc · read “Workspace” via get\_all · read “Workspace” via count.

**State and service calls** call save on doc · call save on child\_doc.

**Explicit results** workspace\_payload(name = name) · workspace\_payload(name = new\_name).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to edit this workspace.” · validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to make a workspace public.”.

**Local steps**

- Set doc from Platform.get\_doc(“Workspace”, name).
- Set can\_edit from can\_edit\_workspace(doc).
- If not can\_edit.
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to edit this workspace.”, Platform.PermissionError).
- Set role\_list from Platform.parse\_json(roles) when isinstance(roles, str), otherwise (roles or list()).
  - Value choice on isinstance(roles, str) — true gives Platform.parse\_json(roles), false gives (roles or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in roles → list().
- Set role\_names from sorted(set of r.get(“role”) when isinstance(r, dict), otherwise r for r drawn from role\_list where r).
  - Draw r from role\_list, keep a combination only if (r).
  - Value choice on isinstance(r, dict) — true gives r.get(“role”), false gives r.
- If access differs from “group”.
  - Set role\_names from list().
- Set is\_standard from (bool(doc.standard) and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(doc.standard) → not Platform.conf.developer\_mode.
- If is\_standard.
  - Bind dependencies upsert\_settings\_customization.
  - Evaluate upsert\_settings\_customization(name, icon = icon, indicator\_color = indicator\_color, roles = role\_names).
  - Return workspace\_payload(name = name).
- Set make\_public from 0 when access equals “private”, otherwise 1.
  - Value choice on access equals “private” — true gives 0, false gives 1.
- If (make\_public and not is\_workspace\_manager()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in make\_public → not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to make a workspace public.”, Platform.PermissionError).
- Set child\_docs from Platform.get\_all(“Workspace”, filters = mapping(“parent\_page” → doc.title, “public” → doc.public)).
- If title.
  - Set doc.title from strip\_html(title).
- If icon.
  - Set doc.icon from icon.
- If indicator\_color is distinct from no value.
  - Set doc.indicator\_color from indicator\_color.
- If module.
  - Evaluate validate\_assignable\_module(module).
  - Set doc.module from module.
- Evaluate doc.set(“roles”, list of mapping(“role” → r) for r drawn from role\_names).
  - Draw r from role\_names.
- If doc.public differs from make\_public.
  - Set doc.sequence\_id from Platform.db.count(“Workspace”, mapping(“public” → make\_public), cache = true).
  - Set doc.public from make\_public.
- Set doc.for\_user from empty text when make\_public, otherwise (doc.for\_user or Platform.session.user).
  - Value choice on make\_public — true gives empty text, false gives (doc.for\_user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.for\_user → Platform.session.user.
- Set doc.label, new\_name from formatted text {doc.title}-{doc.for\_user} when doc.for\_user, otherwise doc.title.
  - Value choice on doc.for\_user — true gives formatted text {doc.title}-{doc.for\_user}, false gives doc.title.
- Evaluate doc.save(ignore\_permissions = true).
- If name differs from new\_name.
  - Evaluate rename\_doc(“Workspace”, name, new\_name, force = true, ignore\_permissions = true).
- For each child in child\_docs.
  - Set child\_doc from Platform.get\_doc(“Workspace”, child.name).
  - Set child\_doc.parent\_page from doc.title.
  - If child\_doc.public differs from make\_public.
    - Set child\_doc.public from make\_public.
  - Set child\_doc.for\_user from empty text when make\_public, otherwise (child\_doc.for\_user or Platform.session.user).
    - Value choice on make\_public — true gives empty text, false gives (child\_doc.for\_user or Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_doc.for\_user → Platform.session.user.
  - Set child\_doc.label, new\_child\_name from formatted text {child\_doc.title}-{child\_doc.for\_user} when child\_doc.for\_user, otherwise child\_doc.title.
    - Value choice on child\_doc.for\_user — true gives formatted text {child\_doc.title}-{child\_doc.for\_user}, false gives child\_doc.title.
  - Evaluate child\_doc.save(ignore\_permissions = true).
  - If child.name differs from new\_child\_name.
    - Evaluate rename\_doc(“Workspace”, child.name, new\_child\_name, force = true, ignore\_permissions = true).
- Evaluate add\_to\_sidebar(Platform.get\_doc(“Workspace”, new\_name)).
- Return workspace\_payload(name = new\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1323)

<a id="op-fda9d3e82c356d"></a>
### Delete page

`operation_foundation_desk_record_definitions_workspace_business_behavior_delete_page`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_doc.

**State and service calls** request delete\_doc for “Workspace”.

**Explicit results** workspace\_payload().

**Explicit failure paths** validation helper — translated “Standard workspaces cannot be deleted. Reset to standard instead.” · validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to delete this workspace.”.

**Local steps**

- Set doc from Platform.get\_doc(“Workspace”, name).
- If (doc.standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Standard workspaces cannot be deleted. Reset to standard instead.”).
- Set can\_edit from can\_edit\_workspace(doc).
- If not can\_edit.
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to delete this workspace.”, Platform.PermissionError).
- Evaluate Platform.delete\_doc(“Workspace”, name, ignore\_permissions = true).
- Return workspace\_payload().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L1886) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1300)

<a id="op-3c111da6671b75"></a>
### Get assignable modules

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_assignable_modules`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Module Def” via get\_all.

**Explicit results** modules.

**Local steps**

- Bind dependencies is\_module\_visible.
- Set modules from list().
- For each row in Platform.get\_all(“Module Def”, fields = list(“name”, “app\_name”), order\_by = “app\_name asc, name asc”).
  - Attempt the following.
    - If not is\_module\_visible(row.name).
      - Continue with the next iteration or loop test.
    - Set app\_title from (Platform.get\_hooks(“app\_title”, app\_name = row.app\_name) or list(row.app\_name)) at 0 when row.app\_name, otherwise no value.
      - Value choice on row.app\_name — true gives (Platform.get\_hooks(“app\_title”, app\_name = row.app\_name) or list(row.app\_name)) at 0, false gives no value.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = row.app\_name) → list(row.app\_name).
    - Evaluate modules.append(mapping(“module” → row.name, “label” → row.name, “app\_name” → row.app\_name, “app\_title” → app\_title)).
  - On failure (Exception).
    - Evaluate Platform.log\_error(formatted text Module {row.name} left out of the assignable list).
    - Continue with the next iteration or loop test.
- Return modules.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = row.app\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L2201) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1304)

<a id="op-61d241cfdfb059"></a>
### Validate assignable module

`operation_foundation_desk_record_definitions_workspace_business_behavior_validate_assignable_module`

**Inputs** module.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} is not a module you can assign a workspace to.”.format(Platform.bold(module)).

**Local steps**

- If module does not belong to set of row at “module” for row drawn from get\_assignable\_modules().
  - Draw row from get\_assignable\_modules().
  - Call the validation error handler Platform.throw(translated “{0} is not a module you can assign a workspace to.”.format(Platform.bold(module))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L2649) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1324)

<a id="op-a5b17546eb431a"></a>
### Set workspace module

`operation_foundation_desk_record_definitions_workspace_business_behavior_set_workspace_module`

**Inputs** name, module.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Workspace” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** workspace\_payload(name = doc.name).

**Explicit failure paths** validation helper — translated “A standard workspace belongs to the module that ships it.” · validation helper with Platform.PermissionError — translated “You need the Workspace Manager role to move this workspace.”.

**Local steps**

- Set doc from Platform.get\_doc(“Workspace”, name).
- If (doc.standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “A standard workspace belongs to the module that ships it.”).
- If not can\_edit\_workspace(doc).
  - Call the validation error handler Platform.throw(translated “You need the Workspace Manager role to move this workspace.”, Platform.PermissionError).
- Evaluate validate\_assignable\_module(module).
- Set doc.module from module.
- Evaluate doc.save(ignore\_permissions = true).
- Return workspace\_payload(name = doc.name).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L2820) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1320)

<a id="op-c1b5e03abc54e5"></a>
### Last sequence id

`operation_foundation_desk_record_definitions_workspace_business_behavior_last_sequence_identifier`

**Inputs** doc.

**Record and data access** read mapping(“doctype” → “Workspace”, “public” → doc.public, “for\_user” → doc.for\_user) via exists · read “Workspace” via get\_all.

**Explicit results** 0 · Platform.get\_all(“Workspace”, fields = list(“sequence\_id”), filters = mapping(“public” → doc.public, “for\_user” → doc.for\_user), order\_by = “sequence\_id desc”) at 0.sequence\_id.

**Local steps**

- Set doc\_exists from Platform.db.exists(mapping(“doctype” → “Workspace”, “public” → doc.public, “for\_user” → doc.for\_user)).
- If not doc\_exists.
  - Return 0.
- Return Platform.get\_all(“Workspace”, fields = list(“sequence\_id”), filters = mapping(“public” → doc.public, “for\_user” → doc.for\_user), order\_by = “sequence\_id desc”) at 0.sequence\_id.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3171) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1312)

<a id="op-7875fbe038bccf"></a>
### Get page list

`operation_foundation_desk_record_definitions_workspace_business_behavior_get_page_list`

**Inputs** fields, filters.

**Record and data access** read “Workspace” via get\_all.

**Explicit results** Platform.get\_all(“Workspace”, fields = fields, filters = filters, order\_by = “sequence\_id asc”).

**Local steps**

- Return Platform.get\_all(“Workspace”, fields = fields, filters = filters, order\_by = “sequence\_id asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3439) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1307)

<a id="op-bc6270e0060de1"></a>
### Is workspace manager

`operation_foundation_desk_record_definitions_workspace_business_behavior_is_workspace_manager`

**Inputs** user = no value.

**Declared result** bool.

**Explicit results** “Workspace Manager” belongs to Platform.get\_roles(user).

**Local steps**

- Return “Workspace Manager” belongs to Platform.get\_roles(user).

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3535) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1311)
