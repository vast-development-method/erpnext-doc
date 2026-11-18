# Forms, reports and navigation · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Desktop icon

[Record definition](../../../../data/record-types/desktop_icon.json)

<a id="op-31237f9266fb1f"></a>
### Clear every users desktop icons

`operation_foundation_binding_foundation_desk_doctype_desktop_icon_desktop_icon_clear_every_users_desktop_icons`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_key(“desktop\_icons”).
- Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L683)

<a id="op-73fa101e34ce3e"></a>
### Create desktop icons from workspace

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_create_desktop_icons_from_workspace`

**Inputs** no declared parameters.

**Record and data access** read “Workspace” via get\_all · read “Module Def” via get\_value · read “Desktop Icon” via exists · read “Desktop Icon” via get\_value.

**State and service calls** request new\_doc for “Desktop Icon” · call insert on icon.

**Local steps**

- Set workspaces from Platform.get\_all(“Workspace”, filters = mapping(“public” → 1), fields = list(“name”, “icon”, “module”)).
- For each w in workspaces.
  - Set icon from Platform.new\_doc(“Desktop Icon”).
  - Set icon.link\_type from “Workspace Sidebar”.
  - Set icon.label from w.name.
  - Set icon.icon\_type from “Link”.
  - Set icon.link\_to from w.name.
  - Set icon.icon from w.icon.
  - If w.module.
    - Set app\_name from Platform.db.get\_value(“Module Def”, w.module, “app\_name”).
    - If app\_name belongs to Platform.get\_installed\_apps().
      - Set icon.app from app\_name.
      - Set app\_title from (Platform.get\_hooks(“app\_title”, app\_name = app\_name) or list(no value)) at 0.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app\_name) → list(no value).
      - Set app\_icon from Platform.db.exists(“Desktop Icon”, mapping(“icon\_type” → “App”, “app” → app\_name)).
      - If app\_icon.
        - Set icon.parent\_icon from app\_icon.
      - Set app\_link from Platform.db.get\_value(“Desktop Icon”, app\_icon, “link”) when app\_icon, otherwise no value.
        - Value choice on app\_icon — true gives Platform.db.get\_value(“Desktop Icon”, app\_icon, “link”), false gives no value.
      - If (app\_link and not is\_desk\_link(app\_link)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in app\_link → not is\_desk\_link(app\_link).
        - Set icon.hidden from 1.
        - Set icon.parent\_icon from no value.
      - If (icon.label equals app\_title and is\_desk\_link(app\_link)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon.label equals app\_title → is\_desk\_link(app\_link).
        - Set icon.hidden from 1.
        - Set icon.parent\_icon from no value.
      - Attempt the following.
        - If not Platform.db.exists(“Desktop Icon”, list(mapping(“label” → icon.label, “icon\_type” → icon.icon\_type))).
          - Evaluate icon.insert(ignore\_if\_duplicate = true, ignore\_links = true).
      - On failure (Exception).
        - Evaluate Platform.log\_error(“Creation of Desktop Icon Failed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = app\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L119) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L652)

<a id="op-ec4dc0ce808357"></a>
### Create desktop icons from installed apps

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_create_desktop_icons_from_installed_apps`

**Inputs** no declared parameters.

**Record and data access** read “Desktop Icon” via exists.

**State and service calls** request new\_doc for “Desktop Icon” · call save on icon.

**Local steps**

- Set apps from Platform.get\_installed\_apps().
- Set index from 0.
- For each a in apps.
  - Set app\_title from (Platform.get\_hooks(“app\_title”, app\_name = a) or list(no value)) at 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = a) → list(no value).
  - If not app\_title.
    - Continue with the next iteration or loop test.
  - Set app\_details from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = a).
  - If not Platform.db.exists(“Desktop Icon”, list(mapping(“icon\_type” → “App”), mapping(“app” → a))).
    - If len(app\_details) differs from 0.
      - Set icon from Platform.new\_doc(“Desktop Icon”).
      - Set icon.label from app\_title.
      - Set icon.link\_type from “External”.
      - Set icon.idx from index.
      - Set icon.icon\_type from “App”.
      - Set icon.app from a.
      - Set icon.link from app\_details at 0 at “route”.
      - Set icon.logo\_url from app\_details at 0 at “logo”.
      - If not Platform.db.exists(“Desktop Icon”, icon.label).
        - Evaluate icon.save().
      - Update index using + 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = a), Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L118) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L651)

<a id="op-713951c6cfee69"></a>
### Create desktop icons

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_create_desktop_icons`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not is\_desktop\_icons\_page().
  - Return no value.
- Evaluate create\_desktop\_icons\_from\_installed\_apps().
- Evaluate create\_desktop\_icons\_from\_workspace().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L6505) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L650)

<a id="op-4049cf7867ab40"></a>
### Import desktop icon fixtures

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_import_desktop_icon_fixtures`

**Inputs** app = no value, force = false.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If not is\_desktop\_icons\_page().
  - Return no value.
- For each app\_name in list(app) when app, otherwise Platform.get\_installed\_apps().
  - Value choice on app — true gives list(app), false gives Platform.get\_installed\_apps().
  - For each doc\_path in get\_app\_level\_files(“desktop\_icon”, app\_name).
    - If import\_file\_by\_path(doc\_path, force = force, ignore\_version = true).
      - Evaluate Platform.db.commit(chain = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L6589) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L667)

<a id="op-7ea23865f28938"></a>
### Create user icons

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_create_user_icons`

**Inputs** user, data.

**State and service calls** request new\_doc for “Desktop Icon” · call save on desktop\_icon.

**Explicit results** json.dumps(user\_settings) · data.

**Local steps**

- Set user\_settings from json.loads(data).
- Set new\_icons from user\_settings.get(“icons\_to\_create”).
- If new\_icons.
  - Set new\_icons from json.loads(user\_settings.get(“icons\_to\_create”)).
  - If new\_icons.
    - For each icon in new\_icons.
      - Attempt the following.
        - Set desktop\_icon from Platform.new\_doc(“Desktop Icon”).
        - Evaluate desktop\_icon.update(icon).
        - Set desktop\_icon.owner from user.
        - Evaluate desktop\_icon.save().
      - On failure (Exception) bound to e.
        - Evaluate Platform.log\_error(“Error in syncing icons”, e).
    - Evaluate user\_settings.pop(“icons\_to\_create”, no value).
    - Evaluate Platform.cache.hset(“\_user\_settings”, formatted text {“Desktop Icon”}::{user}, json.dumps(user\_settings)).
    - Return json.dumps(user\_settings).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L6834) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L653)

<a id="op-8ca18191076f80"></a>
### Add workspace to desktop

`operation_foundation_desk_record_definitions_desktop_icon_business_behavior_add_workspace_to_desktop`

**Inputs** workspace.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Desktop Icon” · call insert on new\_icon.

**Explicit results** mapping(“icon” → new\_icon.as\_dict()).

**Local steps**

- Set new\_icon from Platform.new\_doc(“Desktop Icon”).
- Set new\_icon.label from workspace.
- Set new\_icon.icon\_type from “Link”.
- Set new\_icon.link\_to from workspace.
- Set new\_icon.link\_type from “Workspace Sidebar”.
- Evaluate new\_icon.insert(ignore\_links = true).
- Return mapping(“icon” → new\_icon.as\_dict()).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L648)

## Record · Desktop layout

[Record definition](../../../../data/record-types/desktop_layout.json)

<a id="op-6d70d156505ab9"></a>
### Save layout

`operation_foundation_desk_record_definitions_desktop_layout_business_behavior_save_layout`

**Inputs** user, layout, new\_icons = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Desktop Layout” via get\_doc.

**State and service calls** request new\_doc for “Desktop Layout” · call save on desktop\_layout · request new\_doc for “Workspace” · call save on new\_workspace · request new\_doc for “Desktop Icon” · 1 additional forms in the steps below.

**Explicit results** mapping(“layout” → layout, “workspace\_modules” → workspace\_modules).

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Set layout from json.loads(layout).
- Set desktop\_layout from no value.
- Attempt the following.
  - Set desktop\_layout from Platform.get\_doc(“Desktop Layout”, Platform.session.user).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Set desktop\_layout from Platform.new\_doc(“Desktop Layout”).
  - Set desktop\_layout.user from Platform.session.user.
- If layout.
  - Set desktop\_layout.layout from json.dumps(layout).
  - Evaluate desktop\_layout.save().
- Set workspace\_modules from mapping().
- If new\_icons.
  - Set new\_icons from json.loads(new\_icons).
  - For each icon in new\_icons.
    - Set workspace from icon.get(“workspace”).
    - If workspace.
      - Set new\_workspace from Platform.new\_doc(“Workspace”).
      - Evaluate new\_workspace.update(workspace).
      - Set new\_workspace.title from new\_workspace.label.
      - If not new\_workspace.module.
        - Set new\_workspace.module from triage\_module(new\_workspace.for\_user).
      - Evaluate new\_workspace.save().
      - Evaluate add\_workspace\_to\_desktop(new\_workspace.name).
      - Set workspace\_modules at new\_workspace.name from new\_workspace.module.
      - Continue with the next iteration or loop test.
    - Set desktop\_icon from Platform.new\_doc(“Desktop Icon”).
    - Evaluate desktop\_icon.update(icon).
    - Set desktop\_icon.owner from Platform.session.user.
    - Evaluate desktop\_icon.save().
- Return mapping(“layout” → layout, “workspace\_modules” → workspace\_modules).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L124) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L670)

<a id="op-e4045a8bc7ad42"></a>
### Delete layout

`operation_foundation_desk_record_definitions_desktop_layout_business_behavior_delete_layout`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.delete\_doc\_if\_exists(“Desktop Layout”, Platform.session.user).

**Local steps**

- Return Platform.delete\_doc\_if\_exists(“Desktop Layout”, Platform.session.user).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1005) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L669)

## Record · Desktop settings

[Record definition](../../../../data/record-types/desktop_settings.json)

<a id="op-67d43249d6aba6"></a>
### Desktop Settings.on update

`operation_foundation_desk_record_definitions_desktop_settings_business_behavior_desktop_settings_on_update`

**Inputs** self.

**State and service calls** enqueue with seed\_desktop\_icons.

**Explicit results** no value.

**Local steps**

- If not self.has\_value\_changed(“desktop\_page”).
  - Return no value.
- Evaluate Platform.clear\_cache().
- If self.desktop\_page equals DESKTOP\_ICONS.
  - Evaluate Platform.enqueue(seed\_desktop\_icons, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(seed\_desktop\_icons, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1087) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L671)

<a id="op-75fe47552da9a3"></a>
### Seed desktop icons

`operation_foundation_desk_record_definitions_desktop_settings_business_behavior_seed_desktop_icons`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies create\_desktop\_icons, import\_desktop\_icon\_fixtures.
- Evaluate create\_desktop\_icons().
- Evaluate import\_desktop\_icon\_fixtures().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1236) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L674)

<a id="op-7dc3410656f640"></a>
### Get desktop page

`operation_foundation_desk_record_definitions_desktop_settings_business_behavior_get_desktop_page`

**Inputs** no declared parameters.

**Declared result** str.

**Record and data access** read DesktopSettings.\_DOCTYPE\_NAME via get\_single\_value.

**Explicit results** APPS · page when page belongs to tuple(APPS, DESKTOP\_ICONS), otherwise APPS.

**Local steps**

- Attempt the following.
  - Set has\_field from Platform.get\_meta(DesktopSettings.\_DOCTYPE\_NAME).has\_field(“desktop\_page”).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return APPS.
- If not has\_field.
  - Return APPS.
- Set page from Platform.db.get\_single\_value(DesktopSettings.\_DOCTYPE\_NAME, “desktop\_page”).
- Return page when page belongs to tuple(APPS, DESKTOP\_ICONS), otherwise APPS.
  - Value choice on page belongs to tuple(APPS, DESKTOP\_ICONS) — true gives page, false gives APPS.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(DesktopSettings.\_DOCTYPE\_NAME, “desktop\_page”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1319) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L672)

<a id="op-c815b788ec7e41"></a>
### Is desktop icons page

`operation_foundation_desk_record_definitions_desktop_settings_business_behavior_is_desktop_icons_page`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** get\_desktop\_page() equals DESKTOP\_ICONS.

**Local steps**

- Return get\_desktop\_page() equals DESKTOP\_ICONS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1556) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L673)

## Service · Doc preview

<a id="op-821d5d84527d98"></a>
### Get preview

`operation_foundation_binding_foundation_desk_doc_preview_get_preview`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** mapping(“doc” → doc.as\_dict(), “permlevels” → doc.get\_permlevel\_access(“read”)).

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Evaluate set\_link\_titles(doc).
- Return mapping(“doc” → doc.as\_dict(), “permlevels” → doc.get\_permlevel\_access(“read”)).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L669)

## Record · Dock

[Record definition](../../../../data/record-types/dock.json)

<a id="op-73d72bfba1de47"></a>
### Dock.autoname

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_autoname`

**Inputs** self.

**Local steps**

- If self.standard.
  - Set self.name from self.app.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1609) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L683)

<a id="op-13a981411603d6"></a>
### Dock.validate

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_validate`

**Inputs** self.

**Local steps**

- Set self.user from (self.user or SITE\_LAYER).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.user → SITE\_LAYER.
- Evaluate self.validate\_app\_content().
- Evaluate self.validate\_standard().
- Evaluate self.blank\_the\_mount().
- Evaluate self.anchor\_the\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate app content](operations-023.md#op-f7c73622122139), [validate standard](operations-023.md#op-61994d74fa3f6a), [blank the mount](operations-023.md#op-1070032e92301e), [anchor the items](operations-023.md#op-e71843039f3164).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1678) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L694)

<a id="op-1070032e92301e"></a>
### Dock.blank the mount

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_blank_the_mount`

**Inputs** self.

**Local steps**

- If not self.standard.
  - Set self.mount\_on from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1820) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L684)

<a id="op-f7c73622122139"></a>
### Dock.validate app content

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_validate_application_content`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0}'s dock belongs to its app and can only be authored in developer mode. Arrange the dock instead to change …”.format(Platform.bold(self.app)).

**Local steps**

- If not (self.standard or (not self.is\_new() and self.has\_value\_changed(“standard”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.standard → (not self.is\_new() and self.has\_value\_changed(“standard”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“standard”).
  - Return no value.
- If Platform.conf.developer\_mode.
  - Return no value.
- If any(generator of Platform.flags.get(flag) for flag drawn from SYSTEM\_WRITE\_FLAGS).
  - Draw flag from SYSTEM\_WRITE\_FLAGS.
  - Return no value.
- Call the validation error handler Platform.throw(translated “{0}'s dock belongs to its app and can only be authored in developer mode. Arrange the dock instead to change …”.format(Platform.bold(self.app)), title = translated “Not Editable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L1884) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L696)

<a id="op-61994d74fa3f6a"></a>
### Dock.validate standard

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_validate_standard`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “App {0} is not installed, so a standard dock cannot be written to it.”.format(Platform.bold(self.app)).

**Local steps**

- If not self.standard.
  - Return no value.
- If (not self.has\_value\_changed(“standard”) and not self.has\_value\_changed(“app”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_value\_changed(“standard”) → not self.has\_value\_changed(“app”).
  - Return no value.
- If not any(generator of Platform.flags.get(flag) for flag drawn from SYSTEM\_WRITE\_FLAGS).
  - Draw flag from SYSTEM\_WRITE\_FLAGS.
  - Evaluate check\_developer\_mode().
- If self.app does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(translated “App {0} is not installed, so a standard dock cannot be written to it.”.format(Platform.bold(self.app))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L2189) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L698)

<a id="op-e71843039f3164"></a>
### Dock.anchor the items

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_anchor_the_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: a dock entry opens a Sidebar, a Workspace or a web address, not a {1}.”.format(row.idx, row.link\_type).

**Local steps**

- For each row in self.items.
  - If (row.link\_type and row.link\_type does not belong to DOCK\_LINK\_TYPES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.link\_type → row.link\_type does not belong to DOCK\_LINK\_TYPES.
    - Call the validation error handler Platform.throw(translated “Row #{0}: a dock entry opens a Sidebar, a Workspace or a web address, not a {1}.”.format(row.idx, row.link\_type)).
- Evaluate self.set(“items”, list of row for row drawn from self.items where points\_somewhere(stored\_row(row))).
  - Draw row from self.items, keep a combination only if (points\_somewhere(stored\_row(row))).
- Evaluate self.validate\_added\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate added rows](operations-023.md#op-f811c93dc4df2b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L2518) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L682)

<a id="op-f811c93dc4df2b"></a>
### Dock.validate added rows

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_validate_added_rows`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: an entry on this dock needs an icon and a title of its own.”.format(row.idx).

**Local steps**

- For each row in self.items.
  - If ((self.standard or row.added) and not (row.icon and row.title)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.standard or row.added) → not (row.icon and row.title).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.standard → row.added.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.icon → row.title.
    - Call the validation error handler Platform.throw(translated “Row #{0}: an entry on this dock needs an icon and a title of its own.”.format(row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L2785) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L695)

<a id="op-ccf4789dc47f94"></a>
### Dock.validate links

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_validate_links`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L2957) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L697)

<a id="op-2ebb9cc6102bdc"></a>
### Dock.on update

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_dock\_cache().
- Evaluate self.export\_dock().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear dock cache](operations-024.md#op-0e7f6a7de52399), [export dock](operations-024.md#op-62ea64b3e87add).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L2993) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L691)

<a id="op-41a722847eb135"></a>
### Dock.on trash

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_dock\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear dock cache](operations-024.md#op-0e7f6a7de52399).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3064) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L690)
