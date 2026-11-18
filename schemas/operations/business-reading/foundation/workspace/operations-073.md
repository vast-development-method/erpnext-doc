# Forms, reports and navigation · operations 73

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio page

<a id="op-001a5a7d469cec"></a>
### Get app page

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_get_app_page`

**Inputs** app\_name, page\_name, cached = true.

**Declared result** “StudioPage”.

**Explicit results** page.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Page not found”.

**Local steps**

- Attempt the following.
  - Set get\_page\_doc from Platform.get\_cached\_doc when cached, otherwise Platform.get\_doc.
    - Value choice on cached — true gives Platform.get\_cached\_doc, false gives Platform.get\_doc.
  - Set page from get\_page\_doc(“Studio Page”, page\_name) when page\_name, otherwise no value.
    - Value choice on page\_name — true gives get\_page\_doc(“Studio Page”, page\_name), false gives no value.
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Set page from no value.
- If (not page or page.studio\_app differs from app\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not page → page.studio\_app differs from app\_name.
  - Call the validation error handler Platform.throw(translated “Page not found”, Platform.DoesNotExistError).
- Return page.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2073) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L50)

<a id="op-456ec9b9f54aff"></a>
### Get page

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_get_page`

**Inputs** app\_name, page\_name, preview = false.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“GET”)).

**Declared result** dict.

**Explicit results** mapping(“name” → page.name, “page\_title” → page.page\_title, “tab\_title” → page.tab\_title, “route” → page.route, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to preview this page” · validation helper with Platform.DoesNotExistError — translated “Page not found”.

**Local steps**

- Set page from get\_app\_page(app\_name, page\_name).
- Set is\_guest from Platform.session.user equals “Guest”.
- If preview.
  - If not Platform.has\_permission(“Studio Page”, ptype = “read”, doc = page).
    - Call the validation error handler Platform.throw(translated “You do not have permission to preview this page”, Platform.PermissionError).
  - Set blocks from (page.draft\_blocks or page.blocks).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.draft\_blocks → page.blocks.
- Otherwise.
  - If (not page.published or (is\_guest and not page.allow\_guest)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not page.published → (is\_guest and not page.allow\_guest).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_guest → not page.allow\_guest.
    - Call the validation error handler Platform.throw(translated “Page not found”, Platform.DoesNotExistError).
  - Set blocks from page.blocks.
- Return mapping(“name” → page.name, “page\_title” → page.page\_title, “tab\_title” → page.tab\_title, “route” → page.route, …).
  - Draw row from page.resources.
  - Draw field from PAGE\_RESOURCE\_FIELDS.
  - Draw row from page.variables.
  - Draw field from PAGE\_VARIABLE\_FIELDS.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “read”, doc = page).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2075) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L52)

## Service · Sync

<a id="op-b45467370f37e4"></a>
### After migrate

`operation_foundation_binding_foundation_studio_sync_after_migrate`

**Inputs** no declared parameters.

**Local steps**

- Evaluate \_patch\_mode(true).
- Evaluate sync\_studio\_apps().
- Evaluate remove\_orphaned\_apps\_and\_pages().
- Evaluate \_patch\_mode(false).
- Evaluate build\_custom\_apps().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L260) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L67) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L155)

<a id="op-7d4054de4122f4"></a>
### After app install

`operation_foundation_binding_foundation_studio_sync_after_app_install`

**Inputs** app\_name.

**Local steps**

- If importlib.util.find\_spec(app\_name).
  - Evaluate sync\_studio\_apps(app\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L259) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L66) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L154)

<a id="op-2d99bd49afd9c5"></a>
### Before app uninstall

`operation_foundation_binding_foundation_studio_sync_before_app_uninstall`

**Inputs** app\_name.

**Record and data access** read “Studio App” via get\_all.

**State and service calls** request delete\_doc for “Studio App”.

**Local steps**

- Set apps from Platform.get\_all(“Studio App”, filters = mapping(“Platform\_app” → app\_name), pluck = “name”).
- For each studio\_app in apps.
  - Evaluate print(formatted text Deleting Studio App {studio\_app} for {app\_name}).
  - Evaluate Platform.delete\_doc(“Studio App”, studio\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L261) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L68) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L156)

<a id="op-e4a50893d042e2"></a>
### Sync studio apps

`operation_foundation_binding_foundation_studio_sync_sync_studio_apps`

**Inputs** app\_name = no value.

**Local steps**

- Set apps from list(app\_name) when app\_name, otherwise Platform.get\_installed\_apps().
  - Value choice on app\_name — true gives list(app\_name), false gives Platform.get\_installed\_apps().
- For each app in apps.
  - For each app\_folder in get\_exported\_app\_folders(get\_studio\_folder(app)).
    - Evaluate print(formatted text Syncing Studio App {get\_exported\_app\_name(app\_folder)} for {app}).
    - Evaluate import\_file\_by\_path(get\_app\_file\_path(app\_folder)).
    - Evaluate sync\_pages(app\_folder).
    - Evaluate sync\_components(app\_folder).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L16) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L86) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L174)

<a id="op-940edcbf77f5fb"></a>
### Remove orphaned apps and pages

`operation_foundation_binding_foundation_studio_sync_remove_orphaned_apps_and_pages`

**Inputs** no declared parameters.

**Record and data access** read “Studio App” via get\_all · read “Studio Page” via get\_all.

**State and service calls** request delete\_doc for “Studio App” · request delete\_doc for “Studio Page”.

**Local steps**

- Set tuple(apps, pages) from get\_exported\_docnames().
- Set standard from mapping(“is\_standard” → 1, “Platform\_app” → tuple(“in”, Platform.get\_installed\_apps())).
- For each app in Platform.get\_all(“Studio App”, filters = standard, pluck = “name”).
  - If app does not belong to apps.
    - Evaluate print(formatted text Removing orphan Studio App {app}).
    - Evaluate Platform.delete\_doc(“Studio App”, app, force = true).
- For each page in Platform.get\_all(“Studio Page”, filters = standard, fields = list(“name”, “page\_title”)).
  - If page.name does not belong to pages.
    - Evaluate print(formatted text Removing orphan Studio Page {page.page\_title}).
    - Evaluate Platform.delete\_doc(“Studio Page”, page.name, force = true, ignore\_missing = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L13) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L83) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L171)

<a id="op-9cb83712d981a9"></a>
### Get exported docnames

`operation_foundation_binding_foundation_studio_sync_get_exported_docnames`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(set at str, set at str).

**Explicit results** tuple(apps, pages).

**Local steps**

- Set tuple(apps, pages) from tuple(set(), set()).
- For each app in Platform.get\_installed\_apps().
  - For each app\_folder in get\_exported\_app\_folders(get\_studio\_folder(app)).
    - Evaluate apps.add(get\_exported\_app\_name(app\_folder)).
    - Evaluate pages.update(generator of read\_json\_file(path).get(“page\_name”) for path drawn from get\_page\_file\_paths(app\_folder)).
      - Draw path from get\_page\_file\_paths(app\_folder).
- Return tuple(apps, pages).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L262) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L69) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L157)

<a id="op-8f372adbc3b78d"></a>
### Sync pages

`operation_foundation_binding_foundation_studio_sync_sync_pages`

**Inputs** app\_folder.

**Local steps**

- For each page\_path in get\_page\_file\_paths(app\_folder).
  - Evaluate import\_file\_by\_path(page\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L15) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L85) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L173)

<a id="op-5fa60993f864f9"></a>
### Sync components

`operation_foundation_binding_foundation_studio_sync_sync_components`

**Inputs** app\_folder.

**Explicit results** no value.

**Local steps**

- Set studio\_component\_folder from os.path.join(app\_folder, “studio\_components”).
- If not os.path.exists(studio\_component\_folder).
  - Return no value.
- Set names from list().
- For each component in os.listdir(studio\_component\_folder).
  - If component.endswith(“.json”).
    - Set component\_path from os.path.join(studio\_component\_folder, component).
    - Evaluate import\_file\_by\_path(component\_path).
    - Evaluate import\_script\_file(component\_path).
    - Evaluate names.append(get\_exported\_component\_name(component\_path)).
- Evaluate mark\_components\_standard(names).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L14) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L84) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L172)

<a id="op-e03d6239889002"></a>
### Get page file paths

`operation_foundation_binding_foundation_studio_sync_get_page_file_paths`

**Inputs** app\_folder.

**Declared result** list at str.

**Explicit results** list() · paths.

**Local steps**

- Set studio\_page\_folder from os.path.join(app\_folder, “studio\_page”).
- If not os.path.exists(studio\_page\_folder).
  - Return list().
- Set paths from list().
- For each entry in os.listdir(studio\_page\_folder).
  - Set page\_path from os.path.join(studio\_page\_folder, entry, formatted text {entry}.json).
  - If os.path.isfile(page\_path).
    - Evaluate paths.append(page\_path).
- Return paths.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L263) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L70) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L158)

<a id="op-753e84032b786d"></a>
### Read json file

`operation_foundation_binding_foundation_studio_sync_read_json_file`

**Inputs** path.

**Declared result** dict.

**Explicit results** Platform.parse\_json(Platform.read\_file(path)).

**Local steps**

- Return Platform.parse\_json(Platform.read\_file(path)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L12) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L82) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L170)

## Service · Sync json

<a id="op-a836d4232a9b74"></a>
### Sync file

`operation_foundation_binding_foundation_studio_sync_json_sync_file`

**Inputs** path.

**Declared result** (dict bitwise or no value).

**Explicit results** sync\_component\_script(component\_path) · no value · synced\_doc\_identity(path, doctype).

**Local steps**

- If component\_path bound to get\_component\_path\_from\_script(path).
  - Return sync\_component\_script(component\_path).
- Set doctype from get\_doctype\_from\_path(path).
- If (not doctype or not os.path.exists(path) or is\_in\_sync(path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not os.path.exists(path) → is\_in\_sync(path).
  - Return no value.
- If not import\_file\_by\_path(path, force = true).
  - Return no value.
- If doctype equals “Studio Component”.
  - Evaluate import\_script\_file(path).
- Evaluate cache\_synced\_file\_hash(path).
- Return synced\_doc\_identity(path, doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L10) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L80) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L168)

<a id="op-9e572f27236293"></a>
### Sync component script

`operation_foundation_binding_foundation_studio_sync_json_sync_component_script`

**Inputs** component\_path.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · identity.

**Local steps**

- If (not os.path.exists(component\_path) or not import\_script\_file(component\_path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not os.path.exists(component\_path) → not import\_script\_file(component\_path).
  - Return no value.
- Set identity from synced\_doc\_identity(component\_path, “Studio Component”).
- Evaluate publish\_doc\_change(“Studio Component”, identity at “name”, source = “disk”).
- Return identity.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L9) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L79) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L167)

<a id="op-85684fceb9d4ba"></a>
### Import script file

`operation_foundation_binding_foundation_studio_sync_json_import_script_file`

**Inputs** component\_path.

**Declared result** bool.

**Record and data access** read “Studio Component” via exists · read “Studio Component” via get\_value.

**State and service calls** request set\_value on “Studio Component”.

**Explicit results** false · true.

**Local steps**

- Set tuple(folder, file\_name) from os.path.split(component\_path).
- Set name from get\_exported\_component\_name(component\_path).
- Set script from (Platform.read\_file(find\_script\_file(folder, file\_name.removesuffix(“.json”))) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.read\_file(find\_script\_file(folder, file\_name.removesuffix(“.json”))) → no value.
- If not Platform.db.exists(“Studio Component”, name).
  - Return false.
- If Platform.db.get\_value(“Studio Component”, name, “script”) equals script.
  - Return false.
- Evaluate Platform.db.set\_value(“Studio Component”, name, “script”, script, update\_modified = false).
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L7) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L77) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L165)

<a id="op-5ec0812e410d3d"></a>
### Get exported component name

`operation_foundation_binding_foundation_studio_sync_json_get_exported_component_name`

**Inputs** component\_path.

**Declared result** str.

**Explicit results** get\_component\_name((data.get(“component\_id”) or data.get(“name”)), data.get(“studio\_app”)).

**Local steps**

- Bind dependencies get\_component\_name.
- Set data from Platform.parse\_json(Platform.read\_file(component\_path)).
- Return get\_component\_name((data.get(“component\_id”) or data.get(“name”)), data.get(“studio\_app”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.get(“component\_id”) → data.get(“name”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L4) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L74) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L162)

<a id="op-a04180ec1950ec"></a>
### Get component path from script

`operation_foundation_binding_foundation_studio_sync_json_get_component_path_from_script`

**Inputs** path.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text {stem}.json.

**Local steps**

- Set tuple(stem, extension) from os.path.splitext(path).
- Set parts from get\_studio\_relative\_parts(path).
- If (extension does not belong to tuple(“.js”, “.ts”) or not parts or len(parts) differs from 3 or parts at 1 differs from COMPONENT\_FOLDER).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extension does not belong to tuple(“.js”, “.ts”) → not parts → len(parts) differs from 3 → parts at 1 differs from COMPONENT\_FOLDER.
  - Return no value.
- Return formatted text {stem}.json.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L2) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L72) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L160)

<a id="op-b5638310b40af6"></a>
### Synced doc identity

`operation_foundation_binding_foundation_studio_sync_json_synced_doc_identity`

**Inputs** path, doctype.

**Declared result** dict.

**Explicit results** mapping(“doctype” → doctype, “name” → get\_exported\_component\_name(path) when is\_component, otherwise data.get(DOCNAME\_FIELD at doctype), “studio\_app” → get\_studio\_relative\_parts(path) at 0).

**Local steps**

- Set data from Platform.parse\_json(Platform.read\_file(path)).
- Set is\_component from doctype equals “Studio Component”.
- Return mapping(“doctype” → doctype, “name” → get\_exported\_component\_name(path) when is\_component, otherwise data.get(DOCNAME\_FIELD at doctype), “studio\_app” → get\_studio\_relative\_parts(path) at 0).
  - Value choice on is\_component — true gives get\_exported\_component\_name(path), false gives data.get(DOCNAME\_FIELD at doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L11) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L81) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L169)

<a id="op-6bd759748d5543"></a>
### Cache synced file hash

`operation_foundation_binding_foundation_studio_sync_json_cache_synced_file_hash`

**Inputs** path.

**Local steps**

- Evaluate Platform.cache.hset(SYNCED\_HASHES\_KEY, path, calculate\_hash(path)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L264) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L71) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L159)

<a id="op-de39edf910105f"></a>
### Is in sync

`operation_foundation_binding_foundation_studio_sync_json_is_in_sync`

**Inputs** path.

**Declared result** bool.

**Explicit results** (bool(synced\_hash) and synced\_hash equals calculate\_hash(path)).

**Local steps**

- Set synced\_hash from Platform.cache.hget(SYNCED\_HASHES\_KEY, path).
- Return (bool(synced\_hash) and synced\_hash equals calculate\_hash(path)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(synced\_hash) → synced\_hash equals calculate\_hash(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L8) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L78) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L166)

<a id="op-d7d59c887b8f57"></a>
### Get doctype from path

`operation_foundation_binding_foundation_studio_sync_json_get_doctype_from_path`

**Inputs** path.

**Declared result** (str bitwise or no value).

**Explicit results** no value · “Studio App” · “Studio Page” · “Studio Component”.

**Local steps**

- Set parts from get\_studio\_relative\_parts(path).
- If (not parts or not parts at negative 1.endswith(“.json”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parts → not parts at negative 1.endswith(“.json”).
  - Return no value.
- Set tuple(studio\_app, expanded rest) from parts.
- If rest equals list(formatted text {Platform.scrub(studio\_app)}.json).
  - Return “Studio App”.
- If (len(rest) equals 3 and rest at 0 equals PAGE\_FOLDER and rest at 1 equals rest at 2.removesuffix(“.json”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(rest) equals 3 → rest at 0 equals PAGE\_FOLDER → rest at 1 equals rest at 2.removesuffix(“.json”).
  - Return “Studio Page”.
- If (len(rest) equals 2 and rest at 0 equals COMPONENT\_FOLDER).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(rest) equals 2 → rest at 0 equals COMPONENT\_FOLDER.
  - Return “Studio Component”.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L3) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L73) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L161)

<a id="op-05f8886cbf9334"></a>
### Get studio relative parts

`operation_foundation_binding_foundation_studio_sync_json_get_studio_relative_parts`

**Inputs** path.

**Declared result** (list at str bitwise or no value).

**Explicit results** path at slice (len(folder) + 1) to no value.split(os.sep) · no value.

**Local steps**

- Set path from os.path.realpath(path).
- For each folder in get\_studio\_folders().
  - Set folder from os.path.realpath(folder).
  - If path.startswith((folder + os.sep)).
    - Return path at slice (len(folder) + 1) to no value.split(os.sep).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L76) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L164)

<a id="op-4c8be379eb5aaa"></a>
### Get studio folders

`operation_foundation_binding_foundation_studio_sync_json_get_studio_folders`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** folders.

**Local steps**

- Set folders from list().
- For each app in Platform.get\_installed\_apps().
  - Set path from get\_studio\_folder(app).
  - If os.path.exists(path).
    - Evaluate folders.append(os.path.abspath(path)).
- Return folders.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L5) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L75) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L163)

## Record · System console

[Record definition](../../../../data/record-types/system_console.json)

<a id="op-25b527a8c33308"></a>
### System Console.run

`operation_foundation_desk_record_definitions_system_console_business_behavior_system_console_run`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup, transaction control.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L36) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1191)
