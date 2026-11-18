# Forms, reports and navigation · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dashboard chart source

[Record definition](../../../../data/record-types/dashboard_chart_source.json)

<a id="op-641b6c6704c42a"></a>
### Dashboard Chart Source.on trash

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_dashboard_chart_source_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Deletion of this document is only permitted in developer mode.”.

**Local steps**

- If (not Platform.conf.developer\_mode and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_migrate.
  - Call the validation error handler Platform.throw(translated “Deletion of this document is only permitted in developer mode.”).
- Evaluate Platform.db.after\_commit.add(self.delete\_folder).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L6755) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L624)

<a id="op-5b9ecbb43884df"></a>
### Dashboard Chart Source.read config

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_dashboard_chart_source_read_configuration`

**Inputs** self.

**Declared result** str.

**Explicit results** config\_path.read\_text() when config\_path.exists(), otherwise empty text.

**Local steps**

- Set config\_path from (self.get\_folder\_path() ÷ formatted text {scrub(self.name)}.js).
- Return config\_path.read\_text() when config\_path.exists(), otherwise empty text.
  - Value choice on config\_path.exists() — true gives config\_path.read\_text(), false gives empty text.

**Methods declared on this owner** [get folder path](operations-019.md#op-fa1f7e2ca431fb).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L6905) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L626)

<a id="op-e7253e42ccf0b3"></a>
### Dashboard Chart Source.delete folder

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_dashboard_chart_source_delete_folder`

**Inputs** self.

**Local steps**

- Set path from self.get\_folder\_path().
- If path.exists().
  - Evaluate shutil.rmtree(path, ignore\_errors = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-019.md#op-fa1f7e2ca431fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L7049) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L99) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L622)

<a id="op-fa1f7e2ca431fb"></a>
### Dashboard Chart Source.get folder path

`operation_foundation_desk_record_definitions_dashboard_chart_source_business_behavior_dashboard_chart_source_get_folder_path`

**Inputs** self.

**Declared result** Path.

**Explicit results** ((Path(get\_module\_path(self.module)) ÷ FOLDER\_NAME) ÷ Platform.scrub(self.name)).

**Local steps**

- Return ((Path(get\_module\_path(self.module)) ÷ FOLDER\_NAME) ÷ Platform.scrub(self.name)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0164.json#L7161) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L623)

## Record · Dashboard settings

[Record definition](../../../../data/record-types/dashboard_settings.json)

<a id="op-e7200417e23109"></a>
### Create dashboard settings

`operation_foundation_desk_record_definitions_dashboard_settings_business_behavior_create_dashboard_settings`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Dashboard Settings” via exists.

**State and service calls** request new\_doc for “Dashboard Settings” · call insert on doc · commit.

**Explicit results** doc.

**Local steps**

- If not Platform.db.exists(“Dashboard Settings”, user).
  - Set doc from Platform.new\_doc(“Dashboard Settings”).
  - Set doc.name from user.
  - Evaluate doc.insert(ignore\_permissions = true).
  - Evaluate Platform.db.commit().
  - Return doc.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L643)

<a id="op-3b71975d9a9051"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_dashboard_settings_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L214) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L644)

<a id="op-05b0f0b8233b1e"></a>
### Has permission

`operation_foundation_desk_record_definitions_dashboard_settings_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L327) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L645)

<a id="op-4dd5b12b3c1e2f"></a>
### Save chart config

`operation_foundation_desk_record_definitions_dashboard_settings_business_behavior_save_chart_configuration`

**Inputs** reset, config, chart\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dashboard Settings” via get\_doc.

**State and service calls** request set\_value on “Dashboard Settings”.

**Local steps**

- Set reset from Platform.parse\_json(reset).
- Set doc from Platform.get\_doc(“Dashboard Settings”, Platform.session.user).
- Set chart\_config from (Platform.parse\_json(doc.chart\_config) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(doc.chart\_config) → mapping().
- If reset.
  - Set chart\_config at chart\_name from mapping().
- Otherwise.
  - Set config from Platform.parse\_json(config).
  - If chart\_name does not belong to chart\_config.
    - Set chart\_config at chart\_name from mapping().
  - Evaluate chart\_config at chart\_name.update(config).
- Evaluate Platform.db.set\_value(“Dashboard Settings”, Platform.session.user, “chart\_config”, json.dumps(chart\_config)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0165.json#L461) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L646)

## Service · Data

<a id="op-f997457a7b1d95"></a>
### Invalid filter message

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_invalid_filter_message`

**Inputs** filters.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text FAILED: filter for '{field}' is a bare list {list(value)} — Platform reads a list as &#91;operator, value&#93;, so this crashes at fetch time. For multiple va · formatted text FAILED: filter for '{field}' has {len(value)} elements {list(value)} — a list filter is exactly &#91;operator, value&#93;. Pass &#91;"{value at 0}", &lt;one value&gt;&#93;,.

**Local steps**

- If not isinstance(filters, dict).
  - Return no value.
- For each tuple(field, value) in filters.items().
  - If not isinstance(value, (list bitwise or tuple)).
    - Continue with the next iteration or loop test.
  - Set operator from str(value at 0).casefold() when value, otherwise empty text.
    - Value choice on value — true gives str(value at 0).casefold(), false gives empty text.
  - If operator does not belong to FILTER\_OPERATORS.
    - Return formatted text FAILED: filter for '{field}' is a bare list {list(value)} — Platform reads a list as &#91;operator, value&#93;, so this crashes at fetch time. For multiple va.
  - If len(value) &gt; 2.
    - If operator belongs to MULTI\_VALUE\_OPERATORS.
      - Set filters at field from list(value at 0, list(value at slice 1 to no value)).
      - Continue with the next iteration or loop test.
    - Return formatted text FAILED: filter for '{field}' has {len(value)} elements {list(value)} — a list filter is exactly &#91;operator, value&#93;. Pass &#91;"{value at 0}", &lt;one value&gt;&#93;,.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1765)

<a id="op-dcb500c275afa4"></a>
### Run add data source

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_run_add_data_source`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “FAILED: data\_source\_name is required.” · formatted text FAILED: data\_source\_type must be one of {list(RESOURCE\_TYPES)}. · error · “FAILED: no page in context.” · formatted text FAILED: a data source named '{name}' already exists. Use update\_data\_source to change it. · 2 additional forms in the steps below.

**Local steps**

- Set name from text\_arg(args.get(“data\_source\_name”)).
- Set source\_type from text\_arg(args.get(“data\_source\_type”)).
- If not name.
  - Return “FAILED: data\_source\_name is required.”.
- If source\_type does not belong to RESOURCE\_TYPES.
  - Return formatted text FAILED: data\_source\_type must be one of {list(RESOURCE\_TYPES)}..
- If error bound to invalid\_filter\_message(args.get(“filters”)).
  - Return error.
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- If \_find\_resource(page, name).
  - Return formatted text FAILED: a data source named '{name}' already exists. Use update\_data\_source to change it..
- Evaluate page.append(“resources”, \_build\_row(name, source\_type, args)).
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Return formatted text Added {source\_type} data source '{name}'. Bind blocks to it with {{ {name}.data }}..

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1767)

<a id="op-5ff66d2c5e690a"></a>
### Run list data sources

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_run_list_data_sources`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “No page in context.” · “No data sources defined on this page yet.” · (formatted text {len(out)} data source(s):  + BlockCodec.to\_json(out)).

**Local steps**

- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “No page in context.”.
- If not page.resources.
  - Return “No data sources defined on this page yet.”.
- Set out from list of \_describe\_resource(r) for r drawn from page.resources.
  - Draw r from page.resources.
- Return (formatted text {len(out)} data source(s):  + BlockCodec.to\_json(out)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1769)

<a id="op-39ce2ba929be7c"></a>
### Run update data source

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_run_update_data_source`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** error · “FAILED: no page in context.” · formatted text FAILED: no data source named '{name}'. Call list\_data\_sources to see the current set. · “Nothing to update — pass the fields you want to change.” · formatted text FAILED: {error} · 1 additional forms in the steps below.

**Local steps**

- Set name from text\_arg(args.get(“data\_source\_name”)).
- If error bound to invalid\_filter\_message(args.get(“filters”)).
  - Return error.
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Set row from \_find\_resource(page, name).
- If row is identical to no value.
  - Return formatted text FAILED: no data source named '{name}'. Call list\_data\_sources to see the current set..
- Set changed from \_apply\_changes(row, args).
- If not changed.
  - Return “Nothing to update — pass the fields you want to change.”.
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Return formatted text Updated data source '{name}' ({“, ”.join(changed)})..

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1770)

<a id="op-ae230676f008c0"></a>
### Run delete data source

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_run_delete_data_source`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “FAILED: no page in context.” · formatted text FAILED: no data source named '{name}'. · formatted text FAILED: {error} · (formatted text Deleted data source '{name}'. + formatted text  {warning} when warning, otherwise empty text).

**Local steps**

- Set name from text\_arg(args.get(“data\_source\_name”)).
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Set row from \_find\_resource(page, name).
- If row is identical to no value.
  - Return formatted text FAILED: no data source named '{name}'..
- Evaluate page.resources.remove(row).
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Set warning from dangling\_binding\_warning(ctx, name).
- Return (formatted text Deleted data source '{name}'. + formatted text  {warning} when warning, otherwise empty text).
  - Value choice on warning — true gives formatted text  {warning}, false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1768)

<a id="op-84e059e4f8df93"></a>
### Build row

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_build_row`

**Inputs** name, source\_type, args.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set row from mapping(“resource\_name” → name, “resource\_type” → source\_type).
- For each field in \_RESOURCE\_FIELDS.
  - If args.get(field) is distinct from no value.
    - Set row at field from args at field.
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1762)

<a id="op-86b551440daabf"></a>
### Apply changes

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_apply_changes`

**Inputs** row, args.

**Declared result** list at str.

**Explicit results** changed.

**Local steps**

- Set changed from list().
- For each field in \_RESOURCE\_FIELDS.
  - If args.get(field) is distinct from no value.
    - Evaluate setattr(row, field, args at field).
    - Evaluate changed.append(field).
- Return changed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1761)

<a id="op-0a85836b9aab60"></a>
### Find resource

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_find_resource`

**Inputs** page, name.

**Explicit results** no value · next(generator of r for r drawn from page.resources where r.resource\_name equals name, no value).

**Local steps**

- If not name.
  - Return no value.
- Return next(generator of r for r drawn from page.resources where r.resource\_name equals name, no value).
  - Draw r from page.resources, keep a combination only if (r.resource\_name equals name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1764)

<a id="op-4da1f05caa6846"></a>
### Reload

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_reload`

**Inputs** ctx, page.

**Declared result** no value.

**Local steps**

- Evaluate ctx.emit(“reload”, resources = true, modified = page.modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1766)

<a id="op-fa9954117c7b18"></a>
### Describe resource

`operation_foundation_binding_foundation_studio_ai_agent_tools_data_describe_resource`

**Inputs** r.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping(“name” → r.resource\_name, “type” → r.resource\_type).
- For each field in tuple(“document\_type”, “document\_name”, “fields”, “filters”, …).
  - If value bound to r.get(field).
    - Set out at field from value.
- For each field in tuple(“transform”, “on\_success”, “on\_error”).
  - If value bound to r.get(field).
    - Set out at field from value.
- Set out at “auto” from bool(r.get(“auto”)).
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1763)

## Service · Desk

<a id="op-d5e87517c67f90"></a>
### Get session boot failed error

`operation_foundation_public_pages_desk_business_behavior_get_session_boot_failed_error`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** e.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L4008) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L32)

<a id="op-6b5e477b8a4cc1"></a>
### Is schema out of date

`operation_foundation_public_pages_desk_business_behavior_is_schema_out_of_date`

**Inputs** e.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set seen from set().
- While (e is distinct from no value and id(e) does not belong to seen).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in e is distinct from no value → id(e) does not belong to seen.
  - Evaluate seen.add(id(e)).
  - If Platform.db.is\_missing\_table\_or\_column(e).
    - Return true.
  - Set e from (e.\_\_cause\_\_ or e.\_\_context\_\_).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in e.\_\_cause\_\_ → e.\_\_context\_\_.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L4211) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L33)

<a id="op-c69f1df0efd108"></a>
### Get context

`operation_foundation_public_pages_desk_business_behavior_get_context`

**Inputs** context.

**State and service calls** msgprint with translated “Log in to access this page.”.

**Explicit results** context.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to access this page.” · get\_session\_boot\_failed\_error(e).

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set Platform.response at “status\_code” from 403.
  - Evaluate Platform.msgprint(translated “Log in to access this page.”).
  - Evaluate Platform.redirect(formatted text /login?{urlencode(mapping(“redirect-to” → Platform.request.path))}).
- Otherwise.
  - If Platform.session.data.user\_type equals “Website User”.
    - Call the validation error handler Platform.throw(translated “You are not permitted to access this page.”, Platform.PermissionError).
- Attempt the following.
  - Set boot from Platform.sessions.get().
- On failure (Exception) bound to e.
  - Raise get\_session\_boot\_failed\_error(e) with cause e.
- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Set hooks from Platform.get\_hooks().
- Set app\_include\_js from (hooks.get(“app\_include\_js”, list()) + Platform.conf.get(“app\_include\_js”, list())).
- Set app\_include\_css from (hooks.get(“app\_include\_css”, list()) + Platform.conf.get(“app\_include\_css”, list())).
- Set app\_include\_icons from hooks.get(“app\_include\_icons”, list()).
- If (Platform.get\_system\_settings(“enable\_telemetry”) and os.getenv(“Platform\_SENTRY\_DSN”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_system\_settings(“enable\_telemetry”) → os.getenv(“Platform\_SENTRY\_DSN”).
  - Evaluate app\_include\_js.append(“sentry.bundle.js”).
- Evaluate context.update(mapping(“no\_cache” → 1, “build\_version” → Platform.utils.get\_build\_version(), “app\_include\_js” → app\_include\_js, “app\_include\_css” → app\_include\_css, …)).
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boot.get(“desk\_theme”) → “Light”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_website\_settings(“app\_name”) → Platform.get\_system\_settings(“app\_name”) → “Platform”.
- Return context.

**Values supplied outside this operation** selected callable from Platform.get\_hooks() · configured or stored value from Platform.get\_system\_settings(“enable\_telemetry”), Platform.get\_system\_settings(“app\_name”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L4433) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L31)

## Service · Desk page

<a id="op-ce094742bb023f"></a>
### Get

`operation_foundation_desk_desk_page_business_behavior_get`

**Inputs** name.

**Record and data access** resolve a document from “Page” via get\_doc.

**Explicit results** docs.

**Explicit failure paths** Platform.PermissionError((“No read permission for Page %s” modulo or format (page.title or name))).

**Local steps**

- Set page from Platform.get\_doc(“Page”, name).
- If page.is\_permitted().
  - Evaluate page.load\_assets().
  - Set docs from Platform.\_dict(page.as\_dict()).
  - If getattr(page, “\_dynamic\_page”, no value).
    - Set docs at “\_dynamic\_page” from 1.
  - Return docs.
- Otherwise.
  - Set Platform.response at “403” from 1.
  - Raise Platform.PermissionError((“No read permission for Page %s” modulo or format (page.title or name))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.title → name.

**Values supplied outside this operation** selected callable from getattr(page, “\_dynamic\_page”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L67)

<a id="op-c779197b257a00"></a>
### Getpage

`operation_foundation_desk_desk_page_business_behavior_getpage`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Local steps**

- Set doc from get(name).
- Evaluate Platform.response.docs.append(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L285) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L68)

## Service · Desk views

<a id="op-19f72a516bf5be"></a>
### Desk Views.initialize

`operation_foundation_desk_desk_views_business_behavior_desk_views_initialize`

**Inputs** self.

**Local steps**

- Set self.pages from mapping().
- Set self.reports from mapping().
- Set self.workspaces from mapping().
- Set self.dashboards from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0153.json#L409) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L85)
