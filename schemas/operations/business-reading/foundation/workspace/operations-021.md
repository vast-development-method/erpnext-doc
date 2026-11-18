# Forms, reports and navigation · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Desktop

<a id="op-ca9a78311f3478"></a>
### Workspace.get cached

`operation_foundation_desk_desktop_business_behavior_workspace_get_cached`

**Inputs** self, cache\_key, fallback\_fn.

**Explicit results** value.

**Local steps**

- Set value from Platform.cache.get\_value(cache\_key, user = Platform.session.user).
- If value is distinct from no value.
  - Return value.
- Set value from fallback\_fn().
- Evaluate Platform.cache.set\_value(cache\_key, value, Platform.session.user, 21600).
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L105)

<a id="op-90f4e95161528c"></a>
### Workspace.get can read items

`operation_foundation_desk_desktop_business_behavior_workspace_get_can_read_items`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L204) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L106)

<a id="op-f4daaab4413ce8"></a>
### Workspace.get allowed modules

`operation_foundation_desk_desktop_business_behavior_workspace_get_allowed_modules`

**Inputs** self.

**Explicit results** self.user.allow\_modules.

**Local steps**

- If not self.user.allow\_modules.
  - Evaluate self.user.build\_permissions().
- Return self.user.allow\_modules.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L294) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L104)

<a id="op-e08149177cdcfc"></a>
### Workspace.get onboarding doc

`operation_foundation_desk_desktop_business_behavior_workspace_get_onboarding_record`

**Inputs** self, onboarding.

**Record and data access** read “Module Onboarding” via get\_value · resolve a document from “Module Onboarding” via get\_doc.

**Explicit results** no value · doc.

**Local steps**

- If not Platform.get\_system\_settings(“enable\_onboarding”).
  - Return no value.
- Set is\_complete from Platform.db.get\_value(“Module Onboarding”, onboarding, “is\_complete”).
- If (is\_complete is identical to no value or is\_complete).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_complete is identical to no value → is\_complete.
  - Return no value.
- Set doc from Platform.get\_doc(“Module Onboarding”, onboarding).
- Set allowed\_roles from set(doc.get\_allowed\_roles()).
- Set user\_roles from set(Platform.get\_roles()).
- If not (allowed\_roles bitwise and user\_roles).
  - Return no value.
- If doc.check\_completion().
  - Return no value.
- Return doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_onboarding”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L44) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L111)

<a id="op-f759684f34dc30"></a>
### Workspace.get onboardings

`operation_foundation_binding_foundation_desk_desktop_workspace_get_onboardings`

**Inputs** self.

**Explicit results** onboardings.

**Local steps**

- Bind dependencies get\_step\_details.
- Set onboardings from list().
- For each name in self.onboarding\_list.
  - Set doc from self.get\_onboarding\_doc(name).
  - If doc.
    - Evaluate onboardings.append(mapping(“label” → name, “title” → translated doc.title, “items” → list of get\_step\_details(row.step, row.is\_optional) for row drawn from doc.steps)).
      - Draw row from doc.steps.
- Return onboardings.

**Methods declared on this owner** [get onboarding doc](operations-021.md#op-e08149177cdcfc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L668)

<a id="op-29981f8eecbc7d"></a>
### Workspace.build workspace

`operation_foundation_desk_desktop_business_behavior_workspace_build_workspace`

**Inputs** self.

**Local steps**

- Set self.cards from mapping(“items” → self.get\_links()).
- Set self.charts from mapping(“items” → self.get\_charts()).
- Set self.shortcuts from mapping(“items” → self.get\_shortcuts()).
- Set self.onboardings from mapping(“items” → self.get\_onboardings()).
- Set self.quick\_lists from mapping(“items” → self.get\_quick\_lists()).
- Set self.number\_cards from mapping(“items” → self.get\_number\_cards()).
- Set self.custom\_blocks from mapping(“items” → self.get\_custom\_blocks()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get links](operations-021.md#op-7fcd1e08c50e2e), [get charts](operations-021.md#op-fb918db1a5bc75), [get shortcuts](operations-021.md#op-84de1f3c37ea82), [get onboardings](operations-021.md#op-f759684f34dc30), [get quick lists](operations-021.md#op-3ed6024346d267), [get number cards](operations-021.md#op-2d56aeabff03e3), [get custom blocks](operations-021.md#op-45dc5ba9ecd35e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L43) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L103)

<a id="op-bb21bc770c75c2"></a>
### Workspace.doctype contains a record

`operation_foundation_desk_desktop_business_behavior_workspace_record_type_contains_a_record`

**Inputs** self, name.

**Record and data access** read name via exists · read “DocType” via get\_value · read name via get\_all.

**Explicit results** exists.

**Local steps**

- Set exists from self.table\_counts.get(name, false).
- If (not exists and Platform.db.exists(name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not exists → Platform.db.exists(name).
  - If not Platform.db.get\_value(“DocType”, name, “issingle”).
    - Set exists from bool(Platform.get\_all(name, limit = 1)).
  - Otherwise.
    - Set exists from true.
  - Set self.table\_counts at name from exists.
- Return exists.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L1062) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L119)

<a id="op-e6caf0dcd859cb"></a>
### Workspace.prepare item

`operation_foundation_desk_desktop_business_behavior_workspace_prepare_item`

**Inputs** self, item.

**Explicit results** item.

**Local steps**

- If item.dependencies.
  - Set dependencies from list of dep.strip() for dep drawn from item.dependencies.split(“,”).
    - Draw dep from item.dependencies.split(“,”).
  - Set incomplete\_dependencies from list of d for d drawn from dependencies where not self.\_doctype\_contains\_a\_record(d).
    - Draw d from dependencies, keep a combination only if (not self.\_doctype\_contains\_a\_record(d)).
  - If len(incomplete\_dependencies).
    - Set item.incomplete\_dependencies from incomplete\_dependencies.
  - Otherwise.
    - Set item.incomplete\_dependencies from empty text.
- If item.onboard.
  - If item.get(“type”) equals “doctype”.
    - Set name from item.get(“name”).
    - Set count from self.\_doctype\_contains\_a\_record(name).
    - Set item at “count” from count.
- If item.get(“link\_type”) equals “DocType”.
  - Set item at “description” from Platform.get\_meta(item.link\_to).description.
- Set item at “label” from translated item.label when item.label, otherwise translated item.name.
  - Value choice on item.label — true gives translated item.label, false gives translated item.name.
- Return item.

**Methods declared on this owner** [doctype contains a record](operations-021.md#op-bb21bc770c75c2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L1332) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L118)

<a id="op-71d5386eab4b3d"></a>
### Workspace.is custom block permitted

`operation_foundation_desk_desktop_business_behavior_workspace_is_custom_block_permitted`

**Inputs** self, custom\_block\_name.

**Record and data access** read “Has Role” via get\_all.

**Explicit results** true · false.

**Local steps**

- Bind dependencies has\_common.
- Set allowed from list of d.role for d drawn from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → custom\_block\_name)).
  - Draw d from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → custom\_block\_name)).
- If not allowed.
  - Return true.
- Set roles from Platform.get\_roles().
- If has\_common(roles, allowed).
  - Return true.
- Return false.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L1892) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L116)

<a id="op-7fcd1e08c50e2e"></a>
### Workspace.get links

`operation_foundation_desk_desktop_business_behavior_workspace_get_links`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** new\_data.

**Local steps**

- Set cards from self.doc.get\_link\_groups().
- If not self.doc.hide\_custom.
  - Set cards from (cards + get\_custom\_reports\_and\_doctypes(self.doc.module)).
- Set default\_country from Platform.db.get\_default(“country”).
- Set new\_data from list().
- For each card in cards.
  - Set new\_items from list().
  - Set card from \_dict(card).
  - Set links from card.get(“links”, list()).
  - For each item in links.
    - Set item from \_dict(item).
    - If (item.country and item.country differs from default\_country).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.country → item.country differs from default\_country.
      - Continue with the next iteration or loop test.
    - If is\_item\_allowed(item.link\_to, item.link\_type, self).
      - Set prepared\_item from self.\_prepare\_item(item).
      - Evaluate new\_items.append(prepared\_item).
  - If new\_items.
    - If isinstance(card, \_dict).
      - Set new\_card from card.copy().
    - Otherwise.
      - Set new\_card from card.as\_dict().copy().
    - Set new\_card at “links” from new\_items.
    - Set new\_card at “label” from translated new\_card at “label”.
    - Evaluate new\_data.append(new\_card).
- Return new\_data.

**Methods declared on this owner** [prepare item](operations-021.md#op-e6caf0dcd859cb).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L2132) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L109)

<a id="op-fb918db1a5bc75"></a>
### Workspace.get charts

`operation_foundation_desk_desktop_business_behavior_workspace_get_charts`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** all\_charts.

**Local steps**

- Set all\_charts from list().
- If Platform.has\_permission(“Dashboard Chart”, throw = false).
  - Set charts from self.doc.charts.
  - For each chart in charts.
    - If Platform.has\_permission(“Dashboard Chart”, doc = chart.chart\_name).
      - Set chart.label from translated chart.label when chart.label, otherwise translated chart.chart\_name.
        - Value choice on chart.label — true gives translated chart.label, false gives translated chart.chart\_name.
      - Evaluate all\_charts.append(chart).
- Return all\_charts.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Dashboard Chart”, throw = false), Platform.has\_permission(“Dashboard Chart”, doc = chart.chart\_name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L2782) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L107)

<a id="op-84de1f3c37ea82"></a>
### Workspace.get shortcuts

`operation_foundation_desk_desktop_business_behavior_workspace_get_shortcuts`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** items.

**Local steps**

- Bind local operation \_in\_active\_domains for subsequent calls.
- Set items from list().
- Set shortcuts from self.doc.shortcuts.
- For each item in shortcuts.
  - Set new\_item from item.as\_dict().copy().
  - If (is\_item\_allowed(item.link\_to, item.type, self) and \_in\_active\_domains(item)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_item\_allowed(item.link\_to, item.type, self) → \_in\_active\_domains(item).
    - If item.type equals “Report”.
      - Set report from self.allowed\_reports.get(item.link\_to, mapping()).
      - If report.get(“report\_type”) belongs to list(“Query Report”, “Script Report”, “Custom Report”).
        - Set new\_item at “is\_query\_report” from 1.
      - Otherwise.
        - Set new\_item at “ref\_doctype” from report.get(“ref\_doctype”).
    - Set new\_item at “label” from translated item.label when item.label, otherwise translated item.link\_to.
      - Value choice on item.label — true gives translated item.label, false gives translated item.link\_to.
    - Evaluate items.append(new\_item).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L3056) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L113)

<a id="op-524e64a71f0853"></a>
### Workspace.get shortcuts.in active domains

`operation_foundation_desk_desktop_business_behavior_workspace_get_shortcuts_in_active_domains`

**Inputs** item.

**Explicit results** true · item.restrict\_to\_domain belongs to Platform.get\_active\_domains().

**Local steps**

- If not item.restrict\_to\_domain.
  - Return true.
- Otherwise.
  - Return item.restrict\_to\_domain belongs to Platform.get\_active\_domains().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L3624) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L114)

<a id="op-3ed6024346d267"></a>
### Workspace.get quick lists

`operation_foundation_desk_desktop_business_behavior_workspace_get_quick_lists`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** items.

**Local steps**

- Set items from list().
- Set quick\_lists from self.doc.quick\_lists.
- For each item in quick\_lists.
  - If is\_item\_allowed(item.document\_type, “doctype”, self).
    - Set new\_item from item.as\_dict().copy().
    - Set new\_item at “label” from translated item.label when item.label, otherwise translated item.document\_type.
      - Value choice on item.label — true gives translated item.label, false gives translated item.document\_type.
    - Evaluate items.append(new\_item).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L3717) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L112)

<a id="op-2d56aeabff03e3"></a>
### Workspace.get number cards

`operation_foundation_desk_desktop_business_behavior_workspace_get_number_cards`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** all\_number\_cards.

**Local steps**

- Set all\_number\_cards from list().
- If Platform.has\_permission(“Number Card”, throw = false).
  - Set number\_cards from self.doc.number\_cards.
  - For each number\_card in number\_cards.
    - If Platform.has\_permission(“Number Card”, doc = number\_card.number\_card\_name).
      - Set number\_card.label from translated number\_card.label when number\_card.label, otherwise translated number\_card.number\_card\_name.
        - Value choice on number\_card.label — true gives translated number\_card.label, false gives translated number\_card.number\_card\_name.
      - Evaluate all\_number\_cards.append(number\_card).
- Return all\_number\_cards.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Number Card”, throw = false), Platform.has\_permission(“Number Card”, doc = number\_card.number\_card\_name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L3984) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L110)

<a id="op-45dc5ba9ecd35e"></a>
### Workspace.get custom blocks

`operation_foundation_desk_desktop_business_behavior_workspace_get_custom_blocks`

**Inputs** self.

**Wrappers, in declaration order** handle\_not\_exist.

**Explicit results** all\_custom\_blocks.

**Local steps**

- Set all\_custom\_blocks from list().
- If Platform.has\_permission(“Custom HTML Block”, throw = false).
  - Set custom\_blocks from self.doc.custom\_blocks.
  - For each custom\_block in custom\_blocks.
    - If Platform.has\_permission(“Custom HTML Block”, doc = custom\_block.custom\_block\_name).
      - If not self.is\_custom\_block\_permitted(custom\_block.custom\_block\_name).
        - Continue with the next iteration or loop test.
      - Set custom\_block.label from translated custom\_block.label when custom\_block.label, otherwise translated custom\_block.custom\_block\_name.
        - Value choice on custom\_block.label — true gives translated custom\_block.label, false gives translated custom\_block.custom\_block\_name.
      - Evaluate all\_custom\_blocks.append(custom\_block).
- Return all\_custom\_blocks.

**Methods declared on this owner** [is custom block permitted](operations-021.md#op-71d5386eab4b3d).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Custom HTML Block”, throw = false), Platform.has\_permission(“Custom HTML Block”, doc = custom\_block.custom\_block\_name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L4258) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L108)

<a id="op-a4fd89a564a626"></a>
### Get desktop page

`operation_foundation_desk_desktop_business_behavior_get_desktop_page`

**Inputs** page.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Explicit results** mapping(“charts” → workspace.charts, “shortcuts” → workspace.shortcuts, “cards” → workspace.cards, “onboardings” → workspace.onboardings, …) · mapping().

**Local steps**

- Attempt the following.
  - Set workspace from Workspace(loads(page)).
  - Evaluate workspace.build\_workspace().
  - Return mapping(“charts” → workspace.charts, “shortcuts” → workspace.shortcuts, “cards” → workspace.cards, “onboardings” → workspace.onboardings, …).
- On failure (DoesNotExistError).
  - Evaluate Platform.log\_error(“Workspace Missing”).
  - Return mapping().

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L39) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L92)

<a id="op-0dd4156ce1f90e"></a>
### Overlay customization properties

`operation_foundation_desk_desktop_business_behavior_overlay_customization_properties`

**Inputs** pages.

**Declared result** bool.

**Explicit results** resequenced.

**Local steps**

- Set resequenced from false.
- For each page in pages.
  - Set customization from get\_customization(page.name).
  - If not customization.
    - Continue with the next iteration or loop test.
  - Set page at “is\_customized” from true.
  - If customization.content.
    - Set page at “content” from customization.content.
    - Set page at “is\_layout\_customized” from 1.
  - If customization.visibility equals “Hidden”.
    - Set page at “is\_hidden” from 1.
  - Otherwise.
    - If customization.visibility equals “Visible”.
      - Set page at “is\_hidden” from 0.
  - If customization.icon.
    - Set page at “icon” from customization.icon.
  - If customization.indicator\_color.
    - Set page at “indicator\_color” from customization.indicator\_color.
  - If customization.override\_sequence.
    - Set page at “sequence\_id” from customization.sequence\_id.
    - Set resequenced from true.
- Return resequenced.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L4905) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L99)

<a id="op-901f3af6824e7e"></a>
### Get workspaces

`operation_foundation_desk_desktop_business_behavior_get_workspaces`

**Inputs** no declared parameters.

**Wrappers, in declaration order** request\_cache.

**Record and data access** read “Workspace” via get\_all · read “Report” via get\_value.

**Explicit results** mapping(“pages” → pages, “has\_access” → has\_access, “has\_create\_access” → Platform.has\_permission(doctype = “Workspace”, ptype = “create”)).

**Local steps**

- Bind dependencies get\_module\_placement.
- Set has\_access from “Workspace Manager” belongs to Platform.get\_roles().
- Set allowed\_domains from list(no value, expanded Platform.get\_active\_domains()).
- Set filters from mapping(“restrict\_to\_domain” → list(“in”, allowed\_domains)).
- If has\_access.
  - Set filters from list().
- Set order\_by from “sequence\_id asc”.
- Set fields from list(“name”, “title”, “for\_user”, “parent\_page”, …).
- Set all\_pages from Platform.get\_all(“Workspace”, fields = fields, filters = filters, order\_by = order\_by, ignore\_permissions = true).
- If \_overlay\_customization\_properties(all\_pages).
  - Evaluate all\_pages.sort(key = deferred anonymous expression).
- Set pages from list().
- Set private\_pages from list().
- For each page in all\_pages.
  - Attempt the following.
    - Set workspace from Workspace(page, true).
    - If (has\_access or workspace.is\_permitted()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_access → workspace.is\_permitted().
      - If (page.public and (has\_access or not page.is\_hidden)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in page.public → (has\_access or not page.is\_hidden).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_access → not page.is\_hidden.
        - Evaluate pages.append(page).
      - Otherwise.
        - If page.for\_user equals Platform.session.user.
          - Evaluate private\_pages.append(page).
        - Otherwise.
          - If (not page.public and not page.for\_user).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in not page.public → not page.for\_user.
            - Evaluate pages.append(page).
      - Set page at “label” from translated page.get(“name”).
    - Set page at “app” from get\_module\_placement(page at “module”) when page at “module”, otherwise no value.
      - Value choice on page at “module” — true gives get\_module\_placement(page at “module”), false gives no value.
    - If page at “link\_type” equals “Report”.
      - Set tuple(report\_type, ref\_doctype) from Platform.db.get\_value(“Report”, page at “link\_to”, list(“report\_type”, “ref\_doctype”)).
      - Set page at “report” from mapping(“report\_type” → report\_type, “ref\_doctype” → ref\_doctype).
  - On failure (Platform.PermissionError).
    - Take no action here.
- If private\_pages.
  - Evaluate pages.extend(private\_pages).
- Return mapping(“pages” → pages, “has\_access” → has\_access, “has\_create\_access” → Platform.has\_permission(doctype = “Workspace”, ptype = “create”)).

**Values supplied outside this operation** effective access from Platform.get\_roles(), Platform.has\_permission(doctype = “Workspace”, ptype = “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L41) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L95)

<a id="op-3922356b818702"></a>
### Get table with counts

`operation_foundation_desk_desktop_business_behavior_get_table_with_counts`

**Inputs** no declared parameters.

**Explicit results** counts.

**Local steps**

- Set counts from Platform.cache.get\_value(“information\_schema:counts”).
- If not counts.
  - Set counts from build\_table\_count\_cache().
- Return counts.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L6690) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L94)

<a id="op-157ebc501f827a"></a>
### Get custom reports and doctypes

`operation_foundation_desk_desktop_business_behavior_get_custom_reports_and_record_types`

**Inputs** module.

**Explicit results** list(\_dict(mapping(“label” → translated “Custom Documents”, “links” → get\_custom\_doctype\_list(module))), \_dict(mapping(“label” → translated “Custom Reports”, “links” → get\_custom\_report\_list(module)))).

**Local steps**

- Return list(\_dict(mapping(“label” → translated “Custom Documents”, “links” → get\_custom\_doctype\_list(module))), \_dict(mapping(“label” → translated “Custom Reports”, “links” → get\_custom\_report\_list(module)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L6790) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L91)

<a id="op-2addb4f1ed8f81"></a>
### Get custom doctype list

`operation_foundation_desk_desktop_business_behavior_get_custom_record_type_list`

**Inputs** module.

**Record and data access** read “DocType” via get\_all.

**Explicit results** list of mapping(“type” → “Link”, “link\_type” → “doctype”, “link\_to” → d.name, “label” → translated d.name) for d drawn from doctypes.

**Local steps**

- Set doctypes from Platform.get\_all(“DocType”, fields = list(“name”), filters = mapping(“custom” → 1, “istable” → 0, “module” → module), order\_by = “name”).
- Return list of mapping(“type” → “Link”, “link\_type” → “doctype”, “link\_to” → d.name, “label” → translated d.name) for d drawn from doctypes.
  - Draw d from doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0154.json#L6982) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L89)

<a id="op-4ad0d5fc65d5ef"></a>
### Get custom report list

`operation_foundation_desk_desktop_business_behavior_get_custom_report_list`

**Inputs** module.

**Record and data access** read “Report” via get\_all.

**Explicit results** list of mapping(“type” → “Link”, “link\_type” → “report”, “doctype” → r.ref\_doctype, “dependencies” → r.ref\_doctype, …) for r drawn from reports.

**Local steps**

- Set reports from Platform.get\_all(“Report”, fields = list(“name”, “ref\_doctype”, “report\_type”), filters = mapping(“is\_standard” → “No”, “disabled” → 0, “module” → module), order\_by = “name”).
- Return list of mapping(“type” → “Link”, “link\_type” → “report”, “doctype” → r.ref\_doctype, “dependencies” → r.ref\_doctype, …) for r drawn from reports.
  - Draw r from reports.
  - Value choice on r.report\_type belongs to tuple(“Query Report”, “Script Report”, “Custom Report”) — true gives 1, false gives 0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L90)

<a id="op-b869662a5d4f86"></a>
### Save new widget

`operation_foundation_desk_desktop_business_behavior_save_new_widget`

**Inputs** doc, page, blocks, new\_widgets.

**State and service calls** call save on doc.

**Explicit results** true.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set widgets from \_dict().
- If new\_widgets.
  - Set widgets from \_dict(Platform.parse\_json(new\_widgets)).
  - If widgets.chart.
    - Evaluate doc.charts.extend(new\_widget(widgets.chart, “Workspace Chart”, “charts”)).
  - If widgets.shortcut.
    - Evaluate doc.shortcuts.extend(new\_widget(widgets.shortcut, “Workspace Shortcut”, “shortcuts”)).
  - If widgets.quick\_list.
    - Evaluate doc.quick\_lists.extend(new\_widget(widgets.quick\_list, “Workspace Quick List”, “quick\_lists”)).
  - If widgets.custom\_block.
    - Evaluate doc.custom\_blocks.extend(new\_widget(widgets.custom\_block, “Workspace Custom Block”, “custom\_blocks”)).
  - If widgets.number\_card.
    - Evaluate doc.number\_cards.extend(new\_widget(widgets.number\_card, “Workspace Number Card”, “number\_cards”)).
  - If widgets.card.
    - Evaluate doc.build\_links\_table\_from\_card(widgets.card).
- Evaluate clean\_up(doc, blocks).
- Attempt the following.
  - Evaluate doc.save(ignore\_permissions = true).
- On failure (tuple(ValidationError, TypeError)) bound to e.
  - Set json\_config from (widgets and dumps(widgets, sort\_keys = true, indent = 4)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in widgets → dumps(widgets, sort\_keys = true, indent = 4).
  - Set log from formatted text   page: {page}  config: {json\_config}  exception: {e}.
  - Evaluate doc.log\_error(“Could not save customization”, log).
  - Propagate the active failure.
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L420) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L101)
