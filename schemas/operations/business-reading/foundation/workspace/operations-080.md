# Forms, reports and navigation · operations 80

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-5f6976aa5ab165"></a>
### Get export folder name

`operation_foundation_binding_foundation_studio_utils_get_export_folder_name`

**Inputs** app\_name.

**Declared result** str.

**Explicit results** Platform.scrub(app\_name).

**Local steps**

- Return Platform.scrub(app\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L22) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L92) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L180)

<a id="op-3086582fb5f982"></a>
### Get app file path

`operation_foundation_binding_foundation_studio_utils_get_app_file_path`

**Inputs** app\_folder.

**Declared result** str.

**Explicit results** os.path.join(app\_folder, formatted text {Platform.scrub(os.path.basename(app\_folder))}.json).

**Local steps**

- Return os.path.join(app\_folder, formatted text {Platform.scrub(os.path.basename(app\_folder))}.json).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L20) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L90) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L178)

<a id="op-bc4d6813c17518"></a>
### Script extension

`operation_foundation_binding_foundation_studio_utils_script_extension`

**Inputs** folder, stem, default = “ts”.

**Declared result** str.

**Explicit results** extension · default.

**Local steps**

- For each extension in tuple(“ts”, “js”).
  - If os.path.isfile(os.path.join(folder, formatted text {stem}.{extension})).
    - Return extension.
- Return default.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L29) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L99) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L187)

<a id="op-021de62e668071"></a>
### Validate one script file

`operation_foundation_binding_foundation_studio_utils_validate_one_script_file`

**Inputs** folder, filename, moved\_from = no value.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — Platform.\_(“{0} already has a {1} file. Keep only one script file.”).format(stem, companion).

**Local steps**

- Set tuple(stem, extension) from os.path.splitext(filename).
- Set companion from mapping(“.ts” → “.js”, “.js” → “.ts”).get(extension).
- If not companion.
  - Return no value.
- Set path from os.path.join(folder, (stem + companion)).
- If (path differs from moved\_from and os.path.isfile(path)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in path differs from moved\_from → os.path.isfile(path).
  - Call the validation error handler Platform.throw(Platform.\_(“{0} already has a {1} file. Keep only one script file.”).format(stem, companion), title = Platform.\_(“Ambiguous Script”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L33) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L191)

<a id="op-a6cc40ad27a4fe"></a>
### Find script file

`operation_foundation_binding_foundation_studio_utils_find_script_file`

**Inputs** folder, stem.

**Declared result** str.

**Explicit results** os.path.join(folder, formatted text {stem}.{script\_extension(folder, stem)}).

**Local steps**

- Return os.path.join(folder, formatted text {stem}.{script\_extension(folder, stem)}).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L19) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L89) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L177)

<a id="op-c48530a095701f"></a>
### Find component scripts

`operation_foundation_binding_foundation_studio_utils_find_component_scripts`

**Inputs** folder.

**Declared result** list at dict.

**Explicit results** list() · scripts.

**Local steps**

- If not os.path.isdir(folder).
  - Return list().
- Set scripts from list().
- For each file in sorted(os.listdir(folder)).
  - Set file\_path from find\_script\_file(folder, file.removesuffix(“.json”)).
  - If (not file.endswith(“.json”) or not os.path.exists(file\_path)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not file.endswith(“.json”) → not os.path.exists(file\_path).
    - Continue with the next iteration or loop test.
  - Set component\_id from Platform.parse\_json(Platform.read\_file(nested operand in the contract.path.join(folder, file))).get(“component\_id”).
  - If component\_id.
    - Evaluate scripts.append(mapping(“component\_id” → component\_id, “file\_path” → file\_path)).
- Return scripts.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L18) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L88) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L176)

<a id="op-e70dd379e6a10b"></a>
### Get exported app name

`operation_foundation_binding_foundation_studio_utils_get_exported_app_name`

**Inputs** app\_folder.

**Declared result** str.

**Explicit results** (name or os.path.basename(app\_folder)).

**Local steps**

- Set name from json.loads(Platform.read\_file(get\_app\_file\_path(app\_folder))).get(“name”).
- Return (name or os.path.basename(app\_folder)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → os.path.basename(app\_folder).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L24) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L94) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L182)

<a id="op-7e3776e2571765"></a>
### Validate installed app

`operation_foundation_binding_foundation_studio_utils_validate_installed_app`

**Inputs** app\_name.

**Declared result** no value.

**Explicit failure paths** validation helper — Platform.\_(“App {0} is not installed on this site.”).format(app\_name).

**Local steps**

- If app\_name does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(Platform.\_(“App {0} is not installed on this site.”).format(app\_name), title = Platform.\_(“Invalid App”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L32) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L190)

<a id="op-bb3610b9b5db36"></a>
### Validate file name

`operation_foundation_binding_foundation_studio_utils_validate_file_name`

**Inputs** value, message, title = no value.

**Declared result** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If (not value or value belongs to tuple(“.”, “..”) or “/” belongs to value or “\\” belongs to value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value → value belongs to tuple(“.”, “..”) → “/” belongs to value → “\\” belongs to value.
  - Call the validation error handler Platform.throw(message, title = title).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L31) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L189)

<a id="op-9d78cbca48941e"></a>
### Get exported app folders

`operation_foundation_binding_foundation_studio_utils_get_exported_app_folders`

**Inputs** studio\_folder.

**Declared result** list at str.

**Explicit results** list() · list of folder for folder drawn from folders where os.path.isfile(get\_app\_file\_path(folder)).

**Local steps**

- If not os.path.isdir(studio\_folder).
  - Return list().
- Set folders from list of os.path.join(studio\_folder, entry) for entry drawn from sorted(os.listdir(studio\_folder)).
  - Draw entry from sorted(os.listdir(studio\_folder)).
- Return list of folder for folder drawn from folders where os.path.isfile(get\_app\_file\_path(folder)).
  - Draw folder from folders, keep a combination only if (os.path.isfile(get\_app\_file\_path(folder))).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L23) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L93) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L181)

## Service · Variables

<a id="op-6c8ada68f96af2"></a>
### Run add variable

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_run_add_variable`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** formatted text FAILED: variable\_type must be one of {list(VARIABLE\_TYPES)}. · “FAILED: no page in context.” · formatted text FAILED: {error} · formatted text Added {var\_type} variable '{name}'. Bind blocks to it with {{ {name} }}..

**Local steps**

- Set name from text\_arg(args.get(“variable\_name”)).
- Set var\_type from (text\_arg(args.get(“variable\_type”)) or “String”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text\_arg(args.get(“variable\_type”)) → “String”.
- If var\_type does not belong to VARIABLE\_TYPES.
  - Return formatted text FAILED: variable\_type must be one of {list(VARIABLE\_TYPES)}..
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Evaluate page.append(“variables”, mapping(“variable\_name” → name, “variable\_type” → var\_type, “initial\_value” → \_encode\_initial\_value(var\_type, args.get(“initial\_value”)))).
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Return formatted text Added {var\_type} variable '{name}'. Bind blocks to it with {{ {name} }}..

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1798)

<a id="op-3e2c27f2064a47"></a>
### Run list variables

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_run_list_variables`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “No page in context.” · “No variables defined on this page yet.” · (formatted text {len(out)} variable(s):  + BlockCodec.to\_json(out)).

**Local steps**

- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “No page in context.”.
- If not page.variables.
  - Return “No variables defined on this page yet.”.
- Set out from list of mapping(“name” → v.variable\_name, “type” → v.variable\_type, “initial\_value” → v.initial\_value) for v drawn from page.variables.
  - Draw v from page.variables.
- Return (formatted text {len(out)} variable(s):  + BlockCodec.to\_json(out)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1800)

<a id="op-781b78c9c399d6"></a>
### Run update variable

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_run_update_variable`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “FAILED: no page in context.” · formatted text FAILED: no variable named '{name}'. Call list\_variables to see the current set. · formatted text FAILED: variable\_type must be one of {list(VARIABLE\_TYPES)}. · “Nothing to update — pass variable\_type and/or initial\_value.” · formatted text FAILED: {error} · 1 additional forms in the steps below.

**Local steps**

- Set name from text\_arg(args.get(“variable\_name”)).
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Set row from \_find\_variable(page, name).
- If row is identical to no value.
  - Return formatted text FAILED: no variable named '{name}'. Call list\_variables to see the current set..
- Set changed from list().
- If var\_type bound to text\_arg(args.get(“variable\_type”)).
  - If var\_type does not belong to VARIABLE\_TYPES.
    - Return formatted text FAILED: variable\_type must be one of {list(VARIABLE\_TYPES)}..
  - Set row.variable\_type from var\_type.
  - Evaluate changed.append(“variable\_type”).
- If args.get(“initial\_value”) is distinct from no value.
  - Set row.initial\_value from \_encode\_initial\_value(row.variable\_type, args at “initial\_value”).
  - Evaluate changed.append(“initial\_value”).
- If not changed.
  - Return “Nothing to update — pass variable\_type and/or initial\_value.”.
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Return formatted text Updated variable '{name}' ({“, ”.join(changed)})..

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1801)

<a id="op-535d350ce27a42"></a>
### Run delete variable

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_run_delete_variable`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “FAILED: no page in context.” · formatted text FAILED: no variable named '{name}'. · formatted text FAILED: {error} · (formatted text Deleted variable '{name}'. + formatted text  {warning} when warning, otherwise empty text).

**Local steps**

- Set name from text\_arg(args.get(“variable\_name”)).
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- Set row from \_find\_variable(page, name).
- If row is identical to no value.
  - Return formatted text FAILED: no variable named '{name}'..
- Evaluate page.variables.remove(row).
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate \_reload(ctx, page).
- Set warning from dangling\_binding\_warning(ctx, name).
- Return (formatted text Deleted variable '{name}'. + formatted text  {warning} when warning, otherwise empty text).
  - Value choice on warning — true gives formatted text  {warning}, false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1799)

<a id="op-2a818b962bfc85"></a>
### Find variable

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_find_variable`

**Inputs** page, name.

**Explicit results** no value · next(generator of v for v drawn from page.variables where v.variable\_name equals name, no value).

**Local steps**

- If not name.
  - Return no value.
- Return next(generator of v for v drawn from page.variables where v.variable\_name equals name, no value).
  - Draw v from page.variables, keep a combination only if (v.variable\_name equals name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1796)

<a id="op-01633542e44a2d"></a>
### Encode initial value

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_encode_initial_value`

**Inputs** variable\_type, value.

**Declared result** str.

**Explicit results** str(int(num)) when num equals int(num), otherwise str(num) · “0” · “true” when truthy, otherwise “false” · Platform.as\_json(value, indent = no value) · value · 3 additional forms in the steps below.

**Local steps**

- If variable\_type equals “Number”.
  - Attempt the following.
    - Set num from float(value).
    - Return str(int(num)) when num equals int(num), otherwise str(num).
      - Value choice on num equals int(num) — true gives str(int(num)), false gives str(num).
  - On failure (tuple(TypeError, ValueError)).
    - Return “0”.
- If variable\_type equals “Boolean”.
  - Set truthy from value when isinstance(value, bool), otherwise nested operand in the contract(nested operand in the contract).strip().lower() belongs to tuple(“true”, “1”, “yes”).
    - Value choice on isinstance(value, bool) — true gives value, false gives str(value).strip().lower() belongs to tuple(“true”, “1”, “yes”).
  - Return “true” when truthy, otherwise “false”.
    - Value choice on truthy — true gives “true”, false gives “false”.
- If variable\_type equals “Object”.
  - If isinstance(value, (dict bitwise or list)).
    - Return Platform.as\_json(value, indent = no value).
  - Attempt the following.
    - Evaluate json.loads(value).
    - Return value.
  - On failure (tuple(TypeError, ValueError)).
    - Return “{}”.
- If value is identical to no value.
  - Return “""”.
- Return Platform.as\_json(value when isinstance(value, str), otherwise str(value)).
  - Value choice on isinstance(value, str) — true gives value, false gives str(value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1795)

<a id="op-ee0f7110b4668a"></a>
### Reload

`operation_foundation_binding_foundation_studio_ai_agent_tools_variables_reload`

**Inputs** ctx, page.

**Declared result** no value.

**Local steps**

- Evaluate ctx.emit(“reload”, variables = true, modified = page.modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1797)

## Service · Watch

<a id="op-4e7abad9d5cc17"></a>
### Watch

`operation_foundation_binding_foundation_studio_watch_watch`

**Inputs** site.

**Explicit results** no value.

**Local steps**

- Set observer from start\_watcher(site).
- If not observer.
  - Return no value.
- Attempt the following.
  - While observer.is\_alive().
    - Evaluate observer.join(1).
- On failure (KeyboardInterrupt).
  - Evaluate observer.stop().
- Evaluate observer.join().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L46) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L204)

<a id="op-46db8fcd5389d6"></a>
### Start watcher

`operation_foundation_binding_foundation_studio_watch_start_watcher`

**Inputs** site.

**Explicit results** no value · observer.

**Local steps**

- If not WATCHDOG\_AVAILABLE.
  - Evaluate print(“&#91;watch-studio&#93; watchdog not installed — run ′bench setup requirements --dev studio′”).
  - Return no value.
- Set folders from get\_studio\_folders().
- If not folders.
  - Evaluate print(“&#91;watch-studio&#93; no studio folder found in any installed app”).
  - Return no value.
- Set observer from Observer().
- Set observer.daemon from true.
- Set handler from StudioSyncHandler(site).
- For each folder in folders.
  - Evaluate observer.schedule(handler, folder, recursive = true).
- Evaluate observer.start().
- Evaluate print(formatted text &#91;watch-studio&#93; watching {len(folders)} studio folder(s) for {site}).
- Return observer.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L36) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L194)

<a id="op-40b8b4abc16279"></a>
### Studio Sync Handler.initialize

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_init`

**Inputs** self, site.

**Local steps**

- Evaluate super().\_\_init\_\_().
- Set self.site from site.
- Set self.pending from set().
- Set self.lock from threading.Lock().
- Set self.timer from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L38) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L196)

<a id="op-c8c382bec332d1"></a>
### Studio Sync Handler.on created

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_on_created`

**Inputs** self, event.

**Local steps**

- Evaluate self.queue(event.src\_path, event.is\_directory).

If control reaches the end, it returns no value.

**Methods declared on this owner** [queue](operations-080.md#op-88a8582d0bd3e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L39) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L197)

<a id="op-7e594185fd8b72"></a>
### Studio Sync Handler.on modified

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_on_modified`

**Inputs** self, event.

**Local steps**

- Evaluate self.queue(event.src\_path, event.is\_directory).

If control reaches the end, it returns no value.

**Methods declared on this owner** [queue](operations-080.md#op-88a8582d0bd3e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L40) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L198)

<a id="op-6e60d537e3b45f"></a>
### Studio Sync Handler.on moved

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_on_moved`

**Inputs** self, event.

**Local steps**

- Evaluate self.queue(event.dest\_path, event.is\_directory).

If control reaches the end, it returns no value.

**Methods declared on this owner** [queue](operations-080.md#op-88a8582d0bd3e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L41) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L199)

<a id="op-88a8582d0bd3e7"></a>
### Studio Sync Handler.queue

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_queue`

**Inputs** self, path, is\_directory.

**Explicit results** no value.

**Local steps**

- If (is\_directory or not (path.endswith(“.json”) or get\_component\_path\_from\_script(path))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_directory → not (path.endswith(“.json”) or get\_component\_path\_from\_script(path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path.endswith(“.json”) → get\_component\_path\_from\_script(path).
  - Return no value.
- Within self.lock.
  - Evaluate self.pending.add(path).
  - Evaluate self.restart\_timer().

If control reaches the end, it returns no value.

**Methods declared on this owner** [restart timer](operations-081.md#op-f3015fcb9f549b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L42) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L200)
