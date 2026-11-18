# Forms, reports and navigation · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Desk views

<a id="op-3e76b83322a33a"></a>
### Desk Views.build entities

`operation_foundation_desk_desk_views_business_behavior_desk_views_build_entities`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Bind dependencies get\_workspaces.
- Set self.pages from self.get\_allowed\_pages().
- Set self.reports from self.get\_allowed\_reports().
- Set self.workspaces from get\_workspaces().
- Set self.dashboards from self.get\_allowed\_dashboards(cache = true).
- Return self.

**Methods declared on this owner** [get allowed pages](operations-020.md#op-a0870b86efdc4e), [get allowed reports](operations-020.md#op-42f1bdff9d4209), [get allowed dashboards](operations-020.md#op-1a5fda66c41a19).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L507) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L75)

<a id="op-b1ee8dae7ae134"></a>
### Desk Views.add to boot

`operation_foundation_desk_desk_views_business_behavior_desk_views_add_to_boot`

**Inputs** self, bootinfo.

**Local steps**

- Set bootinfo.page\_info from self.pages.
- Set bootinfo.allowed\_reports from self.reports.
- Set bootinfo.workspaces from self.workspaces.
- Set bootinfo.dashboards from self.dashboards.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L681) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L69)

<a id="op-b41fe9b151c968"></a>
### Desk Views.allowed pages

`operation_foundation_desk_desk_views_business_behavior_desk_views_allowed_pages`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** self.get\_allowed\_pages(cache = true).

**Local steps**

- Return self.get\_allowed\_pages(cache = true).

**Methods declared on this owner** [get allowed pages](operations-020.md#op-a0870b86efdc4e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L802) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L72)

<a id="op-a616b9a1531766"></a>
### Desk Views.allowed reports

`operation_foundation_desk_desk_views_business_behavior_desk_views_allowed_reports`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** self.get\_allowed\_reports(cache = true).

**Local steps**

- Return self.get\_allowed\_reports(cache = true).

**Methods declared on this owner** [get allowed reports](operations-020.md#op-42f1bdff9d4209).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L869) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L73)

<a id="op-100448a479d040"></a>
### Desk Views.allowed dashboards

`operation_foundation_desk_desk_views_business_behavior_desk_views_allowed_dashboards`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** set of d at “name” for d drawn from self.get\_allowed\_dashboards(cache = true).

**Local steps**

- Return set of d at “name” for d drawn from self.get\_allowed\_dashboards(cache = true).
  - Draw d from self.get\_allowed\_dashboards(cache = true).

**Methods declared on this owner** [get allowed dashboards](operations-020.md#op-1a5fda66c41a19).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L936) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L70)

<a id="op-e31af60d284635"></a>
### Desk Views.restricted doctypes

`operation_foundation_desk_desk_views_business_behavior_desk_views_restricted_record_types`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** (Platform.cache.get\_value(“domain\_restricted\_doctypes”) or build\_domain\_restricted\_doctype\_cache()).

**Local steps**

- Bind dependencies build\_domain\_restricted\_doctype\_cache.
- Return (Platform.cache.get\_value(“domain\_restricted\_doctypes”) or build\_domain\_restricted\_doctype\_cache()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(“domain\_restricted\_doctypes”) → build\_domain\_restricted\_doctype\_cache().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1033) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L87)

<a id="op-59cb5897124a06"></a>
### Desk Views.restricted pages

`operation_foundation_desk_desk_views_business_behavior_desk_views_restricted_pages`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** (Platform.cache.get\_value(“domain\_restricted\_pages”) or build\_domain\_restricted\_page\_cache()).

**Local steps**

- Bind dependencies build\_domain\_restricted\_page\_cache.
- Return (Platform.cache.get\_value(“domain\_restricted\_pages”) or build\_domain\_restricted\_page\_cache()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(“domain\_restricted\_pages”) → build\_domain\_restricted\_page\_cache().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1123) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L86)

<a id="op-e32b20149c3eb0"></a>
### Desk Views.can read

`operation_foundation_desk_desk_views_business_behavior_desk_views_can_read`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1213) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L78)

<a id="op-d24923c80413c4"></a>
### Desk Views.allowed workspaces

`operation_foundation_desk_desk_views_business_behavior_desk_views_allowed_workspaces`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** list of page.name for page drawn from get\_workspaces() at “pages”.

**Local steps**

- Bind dependencies get\_workspaces.
- Return list of page.name for page drawn from get\_workspaces() at “pages”.
  - Draw page from get\_workspaces() at “pages”.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1323) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L74)

<a id="op-a0870b86efdc4e"></a>
### Desk Views.get allowed pages

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_allowed_pages`

**Inputs** cls, cache = false, user = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.get\_user\_pages\_or\_reports(“Page”, cache = cache, user = user).

**Local steps**

- Return cls.get\_user\_pages\_or\_reports(“Page”, cache = cache, user = user).

**Methods declared on this owner** [get user pages or reports](operations-020.md#op-082216f31b4df4).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1414) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L81)

<a id="op-42f1bdff9d4209"></a>
### Desk Views.get allowed reports

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_allowed_reports`

**Inputs** cls, cache = false, user = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.get\_user\_pages\_or\_reports(“Report”, cache = cache, user = user).

**Local steps**

- Return cls.get\_user\_pages\_or\_reports(“Report”, cache = cache, user = user).

**Methods declared on this owner** [get user pages or reports](operations-020.md#op-082216f31b4df4).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1535) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L83)

<a id="op-892d0e9ef921e8"></a>
### Desk Views.get allowed report names

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_allowed_report_names`

**Inputs** cls, cache = false, user = no value.

**Wrappers, in declaration order** classmethod.

**Declared result** set at str.

**Explicit results** set of cstr(report) for report drawn from cls.get\_allowed\_reports(cache = cache, user = user).keys() where report.

**Local steps**

- Return set of cstr(report) for report drawn from cls.get\_allowed\_reports(cache = cache, user = user).keys() where report.
  - Draw report from cls.get\_allowed\_reports(cache = cache, user = user).keys(), keep a combination only if (report).

**Methods declared on this owner** [get allowed reports](operations-020.md#op-42f1bdff9d4209).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1656) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L82)

<a id="op-1a38d38292551e"></a>
### Desk Views.get cached allowed report names

`operation_foundation_binding_foundation_desk_desk_views_deskviews_get_cached_allowed_report_names`

**Inputs** cls, user.

**Wrappers, in declaration order** classmethod, Platform.request\_cache.

**Declared result** set at str.

**Explicit results** cls.get\_allowed\_report\_names(user = user).

**Local steps**

- Return cls.get\_allowed\_report\_names(user = user).

**Methods declared on this owner** [get allowed report names](operations-020.md#op-892d0e9ef921e8).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L667)

<a id="op-1a5fda66c41a19"></a>
### Desk Views.get allowed dashboards

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_allowed_dashboards`

**Inputs** cls, cache = false.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.\_allowed\_entity\_cache(“allowed\_dashboards”, Platform.session.user, build, cache = cache).

**Local steps**

- Bind dependencies get\_permitted\_cards, get\_permitted\_charts.
- Bind local operation build for subsequent calls.
- Return cls.\_allowed\_entity\_cache(“allowed\_dashboards”, Platform.session.user, build, cache = cache).

**Methods declared on this owner** [allowed entity cache](operations-020.md#op-bab8d8851338fd).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L1828) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L79)

<a id="op-d71d9363fca3e5"></a>
### Desk Views.get allowed dashboards.build

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_allowed_dashboards_build`

**Inputs** no declared parameters.

**Record and data access** read “Dashboard” via get\_list · read child via get\_all.

**Explicit results** list() · list of mapping(“name” → d.name, “module” → d.module) for d drawn from dashboards where (d.name does not belong to filled or get\_permitted\_charts(d.name) or get\_permitted\_cards(d.name)).

**Local steps**

- Attempt the following.
  - Set dashboards from Platform.get\_list(“Dashboard”, fields = list(“name”, “module”)).
- On failure (Platform.PermissionError).
  - Evaluate Platform.clear\_last\_message().
  - Return list().
- If not dashboards.
  - Return list().
- Set filled from set().
- For each child in tuple(“Dashboard Chart Link”, “Number Card Link”).
  - Evaluate filled.update(Platform.get\_all(child, filters = mapping(“parenttype” → “Dashboard”, “parent” → tuple(“in”, list of d.name for d drawn from dashboards)), pluck = “parent”)).
    - Draw d from dashboards.
- Return list of mapping(“name” → d.name, “module” → d.module) for d drawn from dashboards where (d.name does not belong to filled or get\_permitted\_charts(d.name) or get\_permitted\_cards(d.name)).
  - Draw d from dashboards, keep a combination only if ((d.name does not belong to filled or get\_permitted\_charts(d.name) or get\_permitted\_cards(d.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.name does not belong to filled → get\_permitted\_charts(d.name) → get\_permitted\_cards(d.name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L2419) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L80)

<a id="op-bab8d8851338fd"></a>
### Desk Views.allowed entity cache

`operation_foundation_desk_desk_views_business_behavior_desk_views_allowed_entity_cache`

**Inputs** cls, key, user, builder, cache = false.

**Wrappers, in declaration order** classmethod.

**Explicit results** cached · value.

**Local steps**

- If cache.
  - Set cached from Platform.cache.get\_value(key, user = user).
  - If cached is distinct from no value.
    - Return cached.
- Set value from builder().
- Evaluate Platform.cache.set\_value(key, value, user, cls.CACHE\_EXPIRY).
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L2911) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L71)

<a id="op-082216f31b4df4"></a>
### Desk Views.get user pages or reports

`operation_foundation_desk_desk_views_business_behavior_desk_views_get_user_pages_or_reports`

**Inputs** cls, parent, cache = false, user = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.\_allowed\_entity\_cache((“has\_role:” + parent), user, deferred anonymous expression, cache = cache).

**Local steps**

- If user is identical to no value.
  - Set user from Platform.session.user.
- Return cls.\_allowed\_entity\_cache((“has\_role:” + parent), user, deferred anonymous expression, cache = cache).

**Methods declared on this owner** [allowed entity cache](operations-020.md#op-bab8d8851338fd).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L3130) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L84)

<a id="op-8fdd16f477de50"></a>
### Desk Views.build user pages or reports

`operation_foundation_desk_desk_views_business_behavior_desk_views_build_user_pages_or_reports`

**Inputs** cls, parent, user.

**Wrappers, in declaration order** classmethod.

**Record and data access** read “Report” via get\_list.

**Explicit results** mapping() · has\_role.

**Local steps**

- Set roles from Platform.get\_roles(user).
- Set has\_role from mapping().
- Set page from DocType(“Page”).
- Set report from DocType(“Report”).
- Set is\_report from parent equals “Report”.
- If is\_report.
  - Set columns from tuple(report.name.as\_(“title”), report.ref\_doctype, report.report\_type, report.module).
- Otherwise.
  - Set columns from tuple(page.title.as\_(“title”), page.module, page.system\_page, page.shared\_page).
- Set customRole from DocType(“Custom Role”).
- Set hasRole from DocType(“Has Role”).
- Set parentTable from DocType(parent).
- Bind local operation shell\_flags for subsequent calls.
- Bind local operation exclude\_disabled\_reports for subsequent calls.
- Set pages\_with\_custom\_roles from exclude\_disabled\_reports(nested operand in the contract.select(nested operand in the contract(nested operand in the contract), nested operand in the contract.modified, nested operand in the contract.ref\_do ….
- For each p in pages\_with\_custom\_roles.
  - Set has\_role at p.name from mapping(“modified” → p.modified, “title” → p.title, “ref\_doctype” → p.ref\_doctype, “module” → p.module, …).
- Set subq from nested operand in the contract.qb.from\_(customRole).select(customRole at parent.lower()).where(customRole at parent.lower().isnotnull()).
- Set pages\_with\_standard\_roles from exclude\_disabled\_reports(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).distinct()).run(as\_dict = true).
- For each p in pages\_with\_standard\_roles.
  - If p.name does not belong to has\_role.
    - Set has\_role at p.name from mapping(“modified” → p.modified, “title” → p.title, “module” → p.module, expand shell\_flags(p)).
    - If parent equals “Report”.
      - Evaluate has\_role at p.name.update(mapping(“ref\_doctype” → p.ref\_doctype)).
- Set no\_of\_roles from SubQuery(nested operand in the contract.from\_(hasRole).select(Count(“\*”)).where(hasRole.parent equals parentTable.name)).
- Set rows\_with\_no\_roles from exclude\_disabled\_reports(nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.modified, expanded nested operand in the contract).where(no\_of\_roles equal ….
- For each r in rows\_with\_no\_roles.
  - If r.name does not belong to has\_role.
    - Set has\_role at r.name from mapping(“modified” → r.modified, “title” → r.title, “module” → r.module, expand shell\_flags(r)).
    - If is\_report.
      - Update has\_role at r.name using bitwise or mapping(“ref\_doctype” → r.ref\_doctype).
- If is\_report.
  - If not has\_permission(“Report”, user = user, print\_logs = false).
    - Return mapping().
  - Set reports from Platform.get\_list(“Report”, fields = list(“name”, “report\_type”), filters = mapping(“name” → tuple(“in”, has\_role.keys())), ignore\_ifnull = true, user = user).
  - For each report in reports.
    - Set has\_role at report.name at “report\_type” from report.report\_type.
  - Set non\_permitted\_reports from (set(has\_role.keys()) − set of r.name for r drawn from reports).
    - Draw r from reports.
  - For each r in non\_permitted\_reports.
    - Evaluate has\_role.pop(r, no value).
- Return has\_role.

**Values supplied outside this operation** effective access from Platform.get\_roles(user), has\_permission(“Report”, user = user, print\_logs = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L38) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L76)

<a id="op-94feb34854ccf6"></a>
### Desk Views.build user pages or reports.shell flags

`operation_foundation_binding_foundation_desk_desk_views_deskviews_build_user_pages_or_reports_shell_flags`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** row.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L666)

<a id="op-83a2b09f9a22dc"></a>
### Desk Views.build user pages or reports.exclude disabled reports

`operation_foundation_desk_desk_views_business_behavior_desk_views_build_user_pages_or_reports_exclude_disabled_reports`

**Inputs** query.

**Explicit results** query.where(report.disabled equals 0) when is\_report, otherwise query.

**Local steps**

- Return query.where(report.disabled equals 0) when is\_report, otherwise query.
  - Value choice on is\_report — true gives query.where(report.disabled equals 0), false gives query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L5963) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L77)

## Service · Desktop

<a id="op-16b16238ae1546"></a>
### Handle not exist

`operation_foundation_desk_desktop_business_behavior_handle_not_exist`

**Inputs** fn.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L6044) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L96)

<a id="op-64c49eb1f477e9"></a>
### Handle not exist.wrapper

`operation_foundation_desk_desktop_business_behavior_handle_not_exist_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs) · list().

**Local steps**

- Attempt the following.
  - Return fn(expanded args, expanded names kwargs).
- On failure (DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return list().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L6198) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L97)

<a id="op-9f3368b96af843"></a>
### Workspace.initialize

`operation_foundation_desk_desktop_business_behavior_workspace_initialize`

**Inputs** self, page, minimal = false.

**Record and data access** resolve a document from “Workspace” via get\_doc · resolve a document from “Workspace” via get\_cached\_doc.

**Local steps**

- Set self.page\_name from page.get(“name”).
- Set self.page\_title from page.get(“title”).
- Set self.public\_page from page.get(“public”).
- Set self.workspace\_manager from “Workspace Manager” belongs to Platform.get\_roles().
- Set self.user from Platform.get\_user().
- Set customization from get\_customization(self.page\_name).
- If customization.
  - Set self.doc from Platform.get\_doc(“Workspace”, self.page\_name).
  - Evaluate apply\_customization(self.doc, customization).
- Otherwise.
  - Set self.doc from Platform.get\_cached\_doc(“Workspace”, self.page\_name).
- Set self.can\_read from self.get\_cached(“user\_perm\_can\_read”, self.get\_can\_read\_items).
- Set self.onboarding\_list from list().
- Set self.allowed\_pages from DeskViews.get\_allowed\_pages(cache = true).
- Set self.allowed\_reports from DeskViews.get\_allowed\_reports(cache = true).
- If not minimal.
  - If self.doc.content.
    - Set self.onboarding\_list from list of x at “data” at “onboarding\_name” for x drawn from loads(self.doc.content) where x at “type” equals “onboarding”.
      - Draw x from loads(self.doc.content), keep a combination only if (x at “type” equals “onboarding”).
  - Set self.table\_counts from get\_table\_with\_counts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get cached](operations-021.md#op-ca9a78311f3478).

**Values supplied outside this operation** effective access from Platform.get\_roles() · configured or stored value from Platform.get\_cached\_doc(“Workspace”, self.page\_name).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L45) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L115)

<a id="op-a8dd59ac81562f"></a>
### Workspace.is permitted

`operation_foundation_desk_desktop_business_behavior_workspace_is_permitted`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Bind dependencies has\_common.
- Bind dependencies is\_module\_visible.
- If (self.doc.for\_user and self.doc.for\_user equals Platform.session.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.for\_user → self.doc.for\_user equals Platform.session.user.
  - Return true.
- If not is\_module\_visible(self.doc.module).
  - Return false.
- Set allowed from list of d.role for d drawn from self.doc.roles.
  - Draw d from self.doc.roles.
- Evaluate allowed.extend(get\_custom\_allowed\_roles(“page”, self.doc.name)).
- If not allowed.
  - Return true.
- If has\_common(Platform.get\_roles(), allowed).
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L46) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L117)
