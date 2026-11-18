# Forms, reports and navigation · operations 84

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workspace

[Record definition](../../../../data/record-types/workspace.json)

<a id="op-338cb6aebd33bd"></a>
### Check workspace manager

`operation_foundation_desk_record_definitions_workspace_business_behavior_check_workspace_manager`

**Inputs** message.

**Declared result** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — message.

**Local steps**

- If not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(message, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3621) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1299)

## Workspace · Workspace restore

<a id="op-56caf209bc74eb"></a>
### Get restorable workspaces

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_get_restorable_workspaces`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Workspace” via get\_all · resolve a document from “Workspace” via get\_cached\_doc.

**Explicit results** list() · rows.

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need the Workspace Manager role to see pre-upgrade workspace edits.”).
- If Platform.conf.developer\_mode.
  - Return list().
- Set workspaces from mapping of ws.name → ws for ws drawn from Platform.get\_all(“Workspace”, filters = mapping(“standard” → 1), fields = list(“name”, “title”, “module”, “content”)).
  - Draw ws from Platform.get\_all(“Workspace”, filters = mapping(“standard” → 1), fields = list(“name”, “title”, “module”, “content”)).
- If not workspaces.
  - Return list().
- Set rows from list().
- For each tuple(name, versions) in get\_versions(list(workspaces)).items().
  - Set replay from replay\_versions(versions, Platform.get\_cached\_doc(“Workspace”, name)).
  - If replay.content is identical to no value.
    - Continue with the next iteration or loop test.
  - Set workspace from workspaces at name.
  - Set last from versions at negative 1.
  - Evaluate rows.append(mapping(“workspace” → name, “title” → workspace.title, “module” → workspace.module, “last\_edited\_on” → last.creation, …)).
- Evaluate rows.sort(key = deferred anonymous expression, reverse = true).
- Return rows.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workspace”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L803)

<a id="op-c4e60436cfa756"></a>
### Restore workspace edits

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_restore_workspace_edits`

**Inputs** workspace.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** read “Workspace” via get\_value · resolve a document from “Workspace” via get\_doc.

**State and service calls** call save on customization.

**Explicit results** workspace\_payload(warnings = replay.warnings).

**Explicit failure paths** validation helper — translated “In developer mode a standard workspace's edits belong to the app's JSON, not to a customization.” · validation helper — translated “{0} is not a standard workspace.”.format(bold(workspace)) · validation helper — translated “No pre-upgrade layout edit is recorded for {0}.”.format(bold(workspace)).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need the Workspace Manager role to restore workspace edits.”).
- If Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “In developer mode a standard workspace's edits belong to the app's JSON, not to a customization.”).
- If not Platform.db.get\_value(“Workspace”, workspace, “standard”).
  - Call the validation error handler Platform.throw(translated “{0} is not a standard workspace.”.format(bold(workspace))).
- Set base from Platform.get\_doc(“Workspace”, workspace).
- Set replay from replay\_versions(get\_versions(list(workspace)).get(workspace, list()), base).
- If replay.content is identical to no value.
  - Call the validation error handler Platform.throw(translated “No pre-upgrade layout edit is recorded for {0}.”.format(bold(workspace))).
- Set customization from \_get\_or\_new(workspace).
- Set customization.content from dumps(replay.content).
- Set customization.widgets from dumps(replay.widgets).
- Evaluate customization.set(“added\_roles”, list of mapping(“role” → role) for role drawn from replay.added\_roles).
  - Draw role from replay.added\_roles.
- Evaluate customization.set(“removed\_roles”, list of mapping(“role” → role) for role drawn from replay.removed\_roles).
  - Draw role from replay.removed\_roles.
- For each tuple(field, default) in CUSTOMIZATION\_PROPERTIES.items().
  - Evaluate customization.set(field, replay.properties.get(field, default)).
- Evaluate customization.save().
- Return workspace\_payload(warnings = replay.warnings).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L811)

<a id="op-3ccaa62bee3798"></a>
### Get versions

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_get_versions`

**Inputs** names.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Record and data access** read “Version” via get\_all.

**Explicit results** by\_workspace.

**Local steps**

- Set rows from Platform.get\_all(“Version”, filters = mapping(“ref\_doctype” → “Workspace”, “docname” → list(“in”, names)), fields = list(“name”, “docname”, “owner”, “creation”, …), order\_by = “creation asc, name asc”).
- Set by\_workspace from mapping().
- For each row in rows.
  - Set row.diff from loads(row.data).
  - Evaluate row.pop(“data”).
  - Evaluate by\_workspace.setdefault(row.docname, list()).append(row).
- Return by\_workspace.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L805)

<a id="op-da2f59f60a2b75"></a>
### Replay versions

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_replay_versions`

**Inputs** versions, base.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(content = content, widgets = widgets, added\_roles = added\_roles, removed\_roles = removed\_roles, …).

**Local steps**

- Set content from no value.
- Set added from mapping().
- Set role\_events from mapping().
- Set changed from mapping().
- Set warnings from list().
- Set moved from false.
- For each version in versions.
  - Set diff from version.diff.
  - If not any(generator of diff.get(key) for key drawn from tuple(“changed”, “added”, “removed”, “row\_changed”)).
    - Draw key from tuple(“changed”, “added”, “removed”, “row\_changed”).
    - Continue with the next iteration or loop test.
  - For each tuple(field, \_old, new) in diff.get(“changed”, list()).
    - If field equals “content”.
      - Set decoded from decode\_content(new).
      - If decoded is identical to no value.
        - Evaluate warnings.append(translated “A layout saved on {0} could not be read and was skipped.”.format(version.creation)).
      - Otherwise.
        - Set content from decoded.
    - Otherwise.
      - If field belongs to PROPERTY\_FIELDS.
        - Set changed at field from new.
      - Otherwise.
        - If field equals “sequence\_id”.
          - Set moved from true.
        - Otherwise.
          - If field does not belong to SILENT\_FIELDS.
            - Evaluate warnings.append(translated “The change to {0} cannot be carried by a customization.”.format(field\_label(base, field))).
  - For each tuple(parentfield, row) in diff.get(“removed”, list()).
    - If parentfield equals “roles”.
      - Set role\_events at row at “role” from “remove”.
    - Otherwise.
      - If parentfield belongs to PARENTFIELD\_WIDGET.
        - Evaluate added.get(parentfield, mapping()).pop(row.get(“label”), no value).
  - Set link\_rows from list().
  - For each tuple(parentfield, row) in diff.get(“added”, list()).
    - If parentfield equals “roles”.
      - Set role\_events at row at “role” from “add”.
    - Otherwise.
      - If parentfield equals “links”.
        - Evaluate link\_rows.append(row).
      - Otherwise.
        - If parentfield belongs to PARENTFIELD\_WIDGET.
          - Set added.setdefault(parentfield, mapping()) at row.get(“label”) from strip\_row(row).
  - For each card in cards\_from\_link\_rows(link\_rows, warnings).
    - Set added.setdefault(“links”, mapping()) at card at “label” from card.
  - For each tuple(parentfield, \_index, \_row\_name, \_changes) in diff.get(“row\_changed”, list()).
    - Evaluate warnings.append(translated “An edit to a shipped row in {0} cannot be carried by a customization.”.format(field\_label(base, parentfield))).
- If moved.
  - Evaluate warnings.append(translated “The workspace's place in the sidebar is not restored.”).
- Set widgets from mapping of PARENTFIELD\_WIDGET at pf → list(rows.values()) for tuple(pf, rows) drawn from added.items() where rows.
  - Draw tuple(pf, rows) from added.items(), keep a combination only if (rows).
- If content is distinct from no value.
  - Set widgets from \_prune\_widgets(widgets, content).
  - Evaluate drop\_shadowed\_widgets(widgets, base, warnings).
  - Evaluate recover\_dropped\_widgets(content, widgets, base, versions at negative 1.creation).
  - Evaluate warn\_about\_missing\_widgets(content, widgets, base, warnings).
- Set base\_roles from set of r.role for r drawn from base.roles.
  - Draw r from base.roles.
- Set added\_roles from sorted(generator of role for tuple(role, event) drawn from role\_events.items() where (event equals “add” and role does not belong to base\_roles)).
  - Draw tuple(role, event) from role\_events.items(), keep a combination only if ((event equals “add” and role does not belong to base\_roles)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in event equals “add” → role does not belong to base\_roles.
- Set removed\_roles from sorted(generator of role for tuple(role, event) drawn from role\_events.items() where (event equals “remove” and role belongs to base\_roles)).
  - Draw tuple(role, event) from role\_events.items(), keep a combination only if ((event equals “remove” and role belongs to base\_roles)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in event equals “remove” → role belongs to base\_roles.
- Return Platform.\_dict(content = content, widgets = widgets, added\_roles = added\_roles, removed\_roles = removed\_roles, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L809)

<a id="op-a3a0c5c4439771"></a>
### Decode content

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_decode_content`

**Inputs** value.

**Declared result** (list bitwise or no value).

**Explicit results** no value · decoded.

**Local steps**

- If not value.
  - Return no value.
- For each candidate in tuple(value, value.replace(text in the contract, whitespace '\\n')).
  - Attempt the following.
    - Set decoded from loads(candidate).
  - On failure (tuple(JSONDecodeError, TypeError)).
    - Continue with the next iteration or loop test.
  - If isinstance(decoded, list).
    - Return decoded.
- Return no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L799)

<a id="op-b4cae154fadc75"></a>
### Strip row

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_strip_row`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from row.items() where (key does not belong to BOOKKEEPING\_KEYS and not key.startswith(“\_”)).

**Local steps**

- Return mapping of key → value for tuple(key, value) drawn from row.items() where (key does not belong to BOOKKEEPING\_KEYS and not key.startswith(“\_”)).
  - Draw tuple(key, value) from row.items(), keep a combination only if ((key does not belong to BOOKKEEPING\_KEYS and not key.startswith(“\_”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key does not belong to BOOKKEEPING\_KEYS → not key.startswith(“\_”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L812)

<a id="op-cc73140dd00c54"></a>
### Cards from link rows

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_cards_from_link_rows`

**Inputs** rows, warnings.

**Declared result** list at dict.

**Explicit results** cards.

**Local steps**

- Set cards from list().
- Set current from no value.
- For each row in sorted(rows, key = deferred anonymous expression).
  - If row.get(“type”) equals “Card Break”.
    - Set current from mapping(“label” → row.get(“label”), “icon” → row.get(“icon”), “description” → row.get(“description”), “hidden” → (row.get(“hidden”) or 0), …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“hidden”) → 0.
    - Evaluate cards.append(current).
  - Otherwise.
    - If current is distinct from no value.
      - Evaluate current at “links”.append(mapping of key → row.get(key) for key drawn from LINK\_KEYS).
        - Draw key from LINK\_KEYS.
    - Otherwise.
      - Evaluate warnings.append(translated “The link {0} was added to a shipped card and cannot be carried by a customization.”.format(bold(row.get(“label”)))).
- For each card in cards.
  - Set card at “link\_count” from len(card at “links”).
  - Set card at “links” from dumps(card at “links”).
- Return cards.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L798)

<a id="op-7777e9c267a00d"></a>
### Drop shadowed widgets

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_drop_shadowed_widgets`

**Inputs** widgets, base, warnings.

**Declared result** no value.

**Local steps**

- For each widget\_type in list(widgets).
  - If widget\_type equals “card”.
    - Continue with the next iteration or loop test.
  - Set base\_labels from set of row.label for row drawn from base.get(WIDGET\_PARENTFIELD at widget\_type).
    - Draw row from base.get(WIDGET\_PARENTFIELD at widget\_type).
  - Set kept from list().
  - For each item in widgets at widget\_type.
    - If item.get(“label”) belongs to base\_labels.
      - Evaluate warnings.append(translated “{0} is a shipped {1} edited in place; the app's version is shown.”.format(bold(item.get(“label”)), widget\_label(widget\_type))).
    - Otherwise.
      - Evaluate kept.append(item).
  - If kept.
    - Set widgets at widget\_type from kept.
  - Otherwise.
    - Evaluate widgets.pop(widget\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L801)

<a id="op-f39797279c5c4a"></a>
### Missing widgets

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_missing_widgets`

**Inputs** content, widgets, base.

**Declared result** list at tuple at tuple(str, str).

**Explicit results** missing.

**Local steps**

- Set missing from list().
- For each block in content.
  - Set widget\_type from block.get(“type”).
  - If widget\_type does not belong to WIDGET\_PARENTFIELD.
    - Continue with the next iteration or loop test.
  - Set label from (block.get(“data”) or mapping()).get(formatted text {widget\_type}\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“data”) → mapping().
  - If label belongs to set of item.get(“label”) for item drawn from widgets.get(widget\_type, list()).
    - Draw item from widgets.get(widget\_type, list()).
    - Continue with the next iteration or loop test.
  - If label belongs to set of row.label for row drawn from base.get(WIDGET\_PARENTFIELD at widget\_type).
    - Draw row from base.get(WIDGET\_PARENTFIELD at widget\_type).
    - Continue with the next iteration or loop test.
  - Evaluate missing.append(tuple(widget\_type, label)).
- Return missing.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L807)

<a id="op-c9ecb5d0e0eab1"></a>
### Recover dropped widgets

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_recover_dropped_widgets`

**Inputs** content, widgets, base, last\_edit.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set missing from missing\_widgets(content, widgets, base).
- If not missing.
  - Return no value.
- Set copy from deleted\_copy(base.name, last\_edit).
- If not copy.
  - Return no value.
- For each tuple(widget\_type, label) in missing.
  - Set rows from (copy.get(WIDGET\_PARENTFIELD at widget\_type) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in copy.get(WIDGET\_PARENTFIELD at widget\_type) → list().
  - If widget\_type equals “card”.
    - Set card from card\_from\_rows(rows, label).
    - If card.
      - Evaluate widgets.setdefault(“card”, list()).append(card).
  - Otherwise.
    - Set row from next(generator of r for r drawn from rows where r.get(“label”) equals label, no value).
      - Draw r from rows, keep a combination only if (r.get(“label”) equals label).
    - If row.
      - Evaluate widgets.setdefault(widget\_type, list()).append(strip\_row(row)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L808)

<a id="op-fd86f5f0654017"></a>
### Deleted copy

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_deleted_copy`

**Inputs** workspace, last\_edit.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Deleted Document” via get\_value.

**Explicit results** loads(data) when data, otherwise no value.

**Local steps**

- Set data from Platform.db.get\_value(“Deleted Document”, mapping(“deleted\_doctype” → “Workspace”, “deleted\_name” → workspace, “creation” → tuple(“&gt;”, last\_edit)), “data”, order\_by = “creation asc”).
- Return loads(data) when data, otherwise no value.
  - Value choice on data — true gives loads(data), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L800)

<a id="op-a506180165ec34"></a>
### Card from rows

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_card_from_rows`

**Inputs** rows, label.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · cards at 0 when cards, otherwise no value.

**Local steps**

- Set start from next(generator of i for tuple(i, row) drawn from enumerate(rows) where (row.get(“type”) equals “Card Break” and row.get(“label”) equals label), no value).
  - Draw tuple(i, row) from enumerate(rows), keep a combination only if ((row.get(“type”) equals “Card Break” and row.get(“label”) equals label)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“type”) equals “Card Break” → row.get(“label”) equals label.
- If start is identical to no value.
  - Return no value.
- Set end from next(generator of i for i drawn from range((start + 1), len(rows)) where rows at i.get(“type”) equals “Card Break”, len(rows)).
  - Draw i from range((start + 1), len(rows)), keep a combination only if (rows at i.get(“type”) equals “Card Break”).
- Set cards from cards\_from\_link\_rows(rows at slice start to end, list()).
- Return cards at 0 when cards, otherwise no value.
  - Value choice on cards — true gives cards at 0, false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L797)

<a id="op-ffc2836b385403"></a>
### Warn about missing widgets

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_warn_about_missing_widgets`

**Inputs** content, widgets, base, warnings.

**Declared result** no value.

**Local steps**

- For each tuple(widget\_type, label) in missing\_widgets(content, widgets, base).
  - Evaluate warnings.append(translated “The block {0} points at a {1} this version of the app no longer ships.”.format(bold(label), widget\_label(widget\_type))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L814)

<a id="op-80d9196c962c49"></a>
### Restorable properties

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_restorable_properties`

**Inputs** changed, base, warnings.

**Declared result** dict.

**Explicit results** properties.

**Local steps**

- Set properties from mapping().
- If (“icon” belongs to changed and changed at “icon” differs from base.icon).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “icon” belongs to changed → changed at “icon” differs from base.icon.
  - Set properties at “icon” from changed at “icon”.
- If “indicator\_color” belongs to changed.
  - Set options from Platform.get\_meta(“Custom Workspace”).get\_options(“indicator\_color”).split(whitespace '\\n').
  - Set by\_translation from mapping of \_(option, context = “Custom Workspace”) → option for option drawn from options where option.
    - Draw option from options, keep a combination only if (option).
  - Set value from changed at “indicator\_color”.
  - Set color from value when value belongs to options, otherwise by\_translation.get(value).
    - Value choice on value belongs to options — true gives value, false gives by\_translation.get(value).
  - If color is identical to no value.
    - Evaluate warnings.append(translated “The colour {0} is not one the desk offers and was skipped.”.format(bold(value))).
  - Otherwise.
    - If color differs from base.indicator\_color.
      - Set properties at “indicator\_color” from color.
- If “is\_hidden” belongs to changed.
  - Set hidden from cint(changed at “is\_hidden”).
  - If hidden differs from cint(base.is\_hidden).
    - Set properties at “visibility” from “Hidden” when hidden, otherwise “Visible”.
      - Value choice on hidden — true gives “Hidden”, false gives “Visible”.
- Return properties.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L810)

<a id="op-be3df6a5b4eb86"></a>
### Get state

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_get_state`

**Inputs** workspace, replay.

**Declared result** str.

**Explicit results** “Restored” when holds\_replay(customization, replay), otherwise “Customized since” · “Not yet overwritten” · “Overwritten”.

**Local steps**

- Set customization from get\_customization(workspace.name).
- If customization.
  - Return “Restored” when holds\_replay(customization, replay), otherwise “Customized since”.
    - Value choice on holds\_replay(customization, replay) — true gives “Restored”, false gives “Customized since”.
- If loads((workspace.content or “&#91;&#93;”)) equals replay.content.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in workspace.content → “&#91;&#93;”.
  - Return “Not yet overwritten”.
- Return “Overwritten”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L804)

<a id="op-5fe45893de3435"></a>
### Holds replay

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_holds_replay`

**Inputs** customization, replay.

**Declared result** bool.

**Explicit results** (loads((customization.content or “&#91;&#93;”)) equals replay.content and loads((customization.widgets or “{}”)) equals replay.widgets and sorted(generator of r.role for r drawn from customization.added\_roles) equ ….

**Local steps**

- Return (loads((customization.content or “&#91;&#93;”)) equals replay.content and loads((customization.widgets or “{}”)) equals replay.widgets and sorted(generator of r.role for r drawn from customization.added\_roles) equ ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in loads((customization.content or “&#91;&#93;”)) equals replay.content → loads((customization.widgets or “{}”)) equals replay.widgets → sorted(generator of r.role for r drawn from customization.added\_roles) equals replay.added\_roles → sorted(generator of r.role for r drawn from customization.removed\_roles) equals replay.removed\_roles → all(generator of (customization.get(field) or default) equals replay.properties.get(field, default) for tuple(field, default) drawn from CUSTOMIZATION\_PROPERTIES.items()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.content → “&#91;&#93;”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.widgets → “{}”.
  - Draw r from customization.added\_roles.
  - Draw r from customization.removed\_roles.
  - Draw tuple(field, default) from CUSTOMIZATION\_PROPERTIES.items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in customization.get(field) → default.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L806)

<a id="op-f33e991279de45"></a>
### Summarize

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_summarize`

**Inputs** replay.

**Declared result** dict.

**Explicit results** mapping(“blocks” → len(replay.content), “widgets” → mapping of widget\_label(widget\_type) → len(items) for tuple(widget\_type, items) drawn from replay.widgets.items(), “roles” → (len(replay.added\_roles) + l ….

**Local steps**

- Return mapping(“blocks” → len(replay.content), “widgets” → mapping of widget\_label(widget\_type) → len(items) for tuple(widget\_type, items) drawn from replay.widgets.items(), “roles” → (len(replay.added\_roles) + l ….
  - Draw tuple(widget\_type, items) from replay.widgets.items().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L813)

<a id="op-a4c235fcc33757"></a>
### Field label

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_field_label`

**Inputs** base, fieldname.

**Declared result** str.

**Explicit results** translated field.label when (field and field.label), otherwise fieldname.

**Local steps**

- Set field from base.meta.get\_field(fieldname).
- Return translated field.label when (field and field.label), otherwise fieldname.
  - Value choice on (field and field.label) — true gives translated field.label, false gives fieldname.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field → field.label.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L802)

<a id="op-aff777b374866c"></a>
### Widget label

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_widget_label`

**Inputs** widget\_type.

**Declared result** str.

**Explicit results** translated widget\_type.replace(“\_”, one space).

**Local steps**

- Return translated widget\_type.replace(“\_”, one space).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L815)

<a id="op-a955d42d05a8ba"></a>
### Bold

`operation_foundation_binding_foundation_desk_page_workspace_restore_workspace_restore_bold`

**Inputs** text.

**Declared result** str.

**Explicit results** Platform.bold(escape\_html(text)).

**Local steps**

- Return Platform.bold(escape\_html(text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L796)

## Record · Workspace sidebar

[Record definition](../../../../data/record-types/workspace_sidebar.json)

<a id="op-302fd004458d5a"></a>
### Workspace Sidebar.validate

`operation_foundation_desk_record_definitions_workspace_sidebar_business_behavior_workspace_sidebar_validate`

**Inputs** self.

**Local steps**

- Evaluate self.refuse\_new\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [refuse new rows](operations-084.md#op-19888f50adcc6c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3713) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1344)

<a id="op-19888f50adcc6c"></a>
### Workspace Sidebar.refuse new rows

`operation_foundation_desk_record_definitions_workspace_sidebar_business_behavior_workspace_sidebar_refuse_new_rows`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is an archive of the previous navigation and can no longer be edited. Customize the module's sidebar instead.”.format(Platform.bold((self.name or self.\_DOCTYPE\_NAME))).

**Local steps**

- If (Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_patch → Platform.flags.in\_install.
  - Return no value.
- Call the validation error handler Platform.throw(translated “{0} is an archive of the previous navigation and can no longer be edited. Customize the module's sidebar instead.”.format(Platform.bold((self.name or self.\_DOCTYPE\_NAME))), title ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → self.\_DOCTYPE\_NAME.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3764) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1343)
