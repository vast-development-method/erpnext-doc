# Forms, reports and navigation · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-1c61cd1d1820d5"></a>
### Get studio component

`operation_foundation_binding_foundation_studio_api_get_studio_component`

**Inputs** component\_id, studio\_app = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**Explicit results** doc.as\_dict().

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Component {0} not found”.format(component\_id).

**Local steps**

- Set name from find\_component(component\_id, studio\_app).
- If not name.
  - Call the validation error handler Platform.throw(translated “Component {0} not found”.format(component\_id), Platform.DoesNotExistError).
- Set doc from Platform.get\_doc(“Studio Component”, name).
- Evaluate doc.check\_permission(“read”).
- Return doc.as\_dict().

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L219) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1882)

<a id="op-050979efeea8c0"></a>
### Get studio component scripts

`operation_foundation_binding_foundation_studio_api_get_studio_component_scripts`

**Inputs** Platform\_app, studio\_app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list() · find\_component\_scripts(os.path.join(app\_folder, COMPONENT\_FOLDER)).

**Local steps**

- Evaluate Platform.has\_permission(“Studio Page”, ptype = “read”, throw = true).
- Evaluate validate\_installed\_app(Platform\_app).
- Set app\_folder from get\_export\_folder(Platform\_app, studio\_app).
- If app\_folder does not belong to get\_exported\_app\_folders(get\_studio\_folder(Platform\_app)).
  - Return list().
- Return find\_component\_scripts(os.path.join(app\_folder, COMPONENT\_FOLDER)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1883)

<a id="op-25ba795688c153"></a>
### List studio files

`operation_foundation_binding_foundation_studio_api_list_studio_files`

**Inputs** Platform\_app, studio\_app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list\_db\_file\_tree(studio\_app) · list() · \_build\_studio\_file\_tree(root, root).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(on\_disk = false).
  - Return list\_db\_file\_tree(studio\_app).
- Evaluate \_validate\_studio\_file\_access().
- Set root from \_studio\_app\_root(Platform\_app, studio\_app).
- If not os.path.isdir(root).
  - Return list().
- Return \_build\_studio\_file\_tree(root, root).

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L223) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1886)

<a id="op-1967813d9bba4c"></a>
### Read studio file

`operation_foundation_binding_foundation_studio_api_read_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path, ignore\_missing = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“path” → file\_path, “content” → no value, “hash” → no value) · mapping(“path” → file\_path, “content” → content, “hash” → file\_hash(content)).

**Explicit failure paths** validation helper — translated “File not found: {0}”.format(file\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(on\_disk = false).
  - Evaluate validate\_allowed\_extension(file\_path, ALLOWED\_DB\_FILE\_EXTENSIONS).
  - Set content from read\_db\_file(studio\_app, file\_path).
- Otherwise.
  - Evaluate \_validate\_studio\_file\_access().
  - Evaluate validate\_allowed\_extension(file\_path).
  - Set target from \_resolve\_studio\_file(Platform\_app, studio\_app, file\_path).
  - Set content from no value.
  - If os.path.isfile(target).
    - Within open(target, encoding = “utf-8”) bound as f.
      - Set content from f.read().
- If content is identical to no value.
  - If sbool(ignore\_missing).
    - Return mapping(“path” → file\_path, “content” → no value, “hash” → no value).
  - Call the validation error handler Platform.throw(translated “File not found: {0}”.format(file\_path)).
- Return mapping(“path” → file\_path, “content” → content, “hash” → file\_hash(content)).

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1887)

<a id="op-7246fb90db1f26"></a>
### Write studio file

`operation_foundation_binding_foundation_studio_api_write_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path, content, known\_hash = no value.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** dict.

**Explicit results** mapping(“path” → file\_path, “hash” → file\_hash(content)).

**Explicit failure paths** validation helper — translated “{0} changed on disk since you opened it.”.format(file\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(“write”, on\_disk = false).
  - Evaluate write\_db\_file(studio\_app, file\_path, content, known\_hash).
  - Return mapping(“path” → file\_path, “hash” → file\_hash(content)).
- Evaluate \_validate\_studio\_file\_access(“write”).
- Evaluate validate\_allowed\_extension(file\_path).
- Evaluate validate\_editable(studio\_app, file\_path).
- Set target from \_resolve\_studio\_file(Platform\_app, studio\_app, file\_path).
- Evaluate validate\_one\_script\_file(os.path.dirname(target), os.path.basename(file\_path)).
- If (known\_hash and os.path.isfile(target)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in known\_hash → os.path.isfile(target).
  - Within open(target, encoding = “utf-8”) bound as f.
    - If file\_hash(f.read()) differs from known\_hash.
      - Call the validation error handler Platform.throw(translated “{0} changed on disk since you opened it.”.format(file\_path)).
- Evaluate os.makedirs(os.path.dirname(target), exist\_ok = true).
- Within open(target, “w”, encoding = “utf-8”) bound as f.
  - Evaluate f.write(content).
- Evaluate \_sync\_component\_script(file\_path, target).
- Return mapping(“path” → file\_path, “hash” → file\_hash(content)).

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1893)

<a id="op-619649cdefad50"></a>
### Create studio file

`operation_foundation_binding_foundation_studio_api_create_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** dict.

**Explicit results** mapping(“path” → file\_path, “hash” → file\_hash(empty text)).

**Explicit failure paths** validation helper — translated “{0} already exists.”.format(file\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(“write”, on\_disk = false).
  - Evaluate create\_db\_file(studio\_app, file\_path).
  - Return mapping(“path” → file\_path, “hash” → file\_hash(empty text)).
- Evaluate \_validate\_studio\_file\_access(“write”).
- Evaluate validate\_allowed\_extension(file\_path).
- Evaluate validate\_editable(studio\_app, file\_path).
- Set target from \_resolve\_studio\_file(Platform\_app, studio\_app, file\_path).
- If os.path.exists(target).
  - Call the validation error handler Platform.throw(translated “{0} already exists.”.format(file\_path)).
- Evaluate validate\_one\_script\_file(os.path.dirname(target), os.path.basename(file\_path)).
- Evaluate os.makedirs(os.path.dirname(target), exist\_ok = true).
- Evaluate touch\_file(target).
- Return mapping(“path” → file\_path, “hash” → file\_hash(empty text)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1870)

<a id="op-206a001e87d101"></a>
### Create studio folder

`operation_foundation_binding_foundation_studio_api_create_studio_folder`

**Inputs** Platform\_app, studio\_app, folder\_path.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** dict.

**Explicit results** mapping(“path” → folder\_path).

**Explicit failure paths** validation helper — translated “A folder appears when you create a file in it.” · validation helper — translated “{0} already exists.”.format(folder\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Call the validation error handler Platform.throw(translated “A folder appears when you create a file in it.”).
- Evaluate \_validate\_studio\_file\_access(“write”).
- Set target from \_resolve\_studio\_file(Platform\_app, studio\_app, folder\_path).
- If os.path.exists(target).
  - Call the validation error handler Platform.throw(translated “{0} already exists.”.format(folder\_path)).
- Evaluate os.makedirs(target).
- Return mapping(“path” → folder\_path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1871)

<a id="op-23cfa9cecfec9a"></a>
### Rename studio file

`operation_foundation_binding_foundation_studio_api_rename_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path, new\_path.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** dict.

**Explicit results** mapping(“path” → new\_path).

**Explicit failure paths** validation helper — translated “Not found: {0}”.format(file\_path) · validation helper — translated “{0} already exists.”.format(new\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(“write”, on\_disk = false).
  - Evaluate rename\_db\_path(studio\_app, file\_path, new\_path).
  - Return mapping(“path” → new\_path).
- Evaluate \_validate\_studio\_file\_access(“write”).
- Set source from \_resolve\_studio\_file(Platform\_app, studio\_app, file\_path).
- Set destination from \_resolve\_studio\_file(Platform\_app, studio\_app, new\_path).
- If not os.path.exists(source).
  - Call the validation error handler Platform.throw(translated “Not found: {0}”.format(file\_path)).
- If os.path.exists(destination).
  - Call the validation error handler Platform.throw(translated “{0} already exists.”.format(new\_path)).
- If os.path.isfile(source).
  - Evaluate validate\_allowed\_extension(file\_path).
  - Evaluate validate\_allowed\_extension(new\_path).
  - Evaluate validate\_editable(studio\_app, file\_path).
  - Evaluate validate\_editable(studio\_app, new\_path).
  - Evaluate validate\_one\_script\_file(os.path.dirname(destination), os.path.basename(new\_path), moved\_from = source).
- Otherwise.
  - Evaluate validate\_folder\_removable(file\_path).
- Evaluate os.makedirs(os.path.dirname(destination), exist\_ok = true).
- Evaluate os.rename(source, destination).
- Evaluate \_sync\_component\_script(file\_path, source).
- Evaluate \_sync\_component\_script(new\_path, destination).
- Return mapping(“path” → new\_path).

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1888)

<a id="op-5e03f91966915a"></a>
### Delete studio file

`operation_foundation_binding_foundation_studio_api_delete_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Not found: {0}”.format(file\_path).

**Local steps**

- If is\_db\_app(studio\_app).
  - Evaluate \_validate\_studio\_file\_access(“write”, on\_disk = false).
  - Evaluate delete\_db\_path(studio\_app, file\_path).
  - Return no value.
- Evaluate \_validate\_studio\_file\_access(“write”).
- Set target from \_resolve\_studio\_file(Platform\_app, studio\_app, file\_path).
- If os.path.isdir(target).
  - Evaluate validate\_folder\_removable(file\_path).
  - Evaluate shutil.rmtree(target).
  - Return no value.
- Evaluate validate\_allowed\_extension(file\_path).
- Evaluate validate\_editable(studio\_app, file\_path).
- If not os.path.isfile(target).
  - Call the validation error handler Platform.throw(translated “Not found: {0}”.format(file\_path)).
- Evaluate os.remove(target).
- Evaluate \_sync\_component\_script(file\_path, target).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L209) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1872)

<a id="op-6385e07c7ba907"></a>
### Get app files

`operation_foundation_binding_foundation_studio_api_get_app_files`

**Inputs** app\_name.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“GET”)).

**Declared result** list at dict.

**Explicit results** list() · get\_db\_files(app\_name).

**Explicit failure paths** validation helper — translated “Invalid app name.”.

**Local steps**

- If not isinstance(app\_name, str).
  - Call the validation error handler Platform.throw(translated “Invalid app name.”).
- Evaluate validate\_app\_viewer\_access(app\_name).
- If not is\_db\_app(app\_name).
  - Return list().
- Return get\_db\_files(app\_name).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L211) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1874)

<a id="op-9a87bc2936d513"></a>
### Sync component script

`operation_foundation_binding_foundation_studio_api_sync_component_script`

**Inputs** file\_path, target.

**Declared result** no value.

**Local steps**

- If is\_component\_script\_path(file\_path.strip(“/”)).
  - Evaluate sync\_component\_script((os.path.splitext(target) at 0 + “.json”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1891)

<a id="op-2455489e5eb8eb"></a>
### Validate studio file access

`operation_foundation_binding_foundation_studio_api_validate_studio_file_access`

**Inputs** permission\_type = “read”, on\_disk = true.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Editing Studio code files is only allowed in developer mode.”.

**Local steps**

- If (on\_disk and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in on\_disk → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Editing Studio code files is only allowed in developer mode.”).
- Evaluate Platform.has\_permission(“Studio App”, ptype = permission\_type, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio App”, ptype = permission\_type, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1892)

<a id="op-93fd93f662f970"></a>
### Studio app root

`operation_foundation_binding_foundation_studio_api_studio_app_root`

**Inputs** Platform\_app, studio\_app.

**Declared result** str.

**Record and data access** read “Studio App” via get\_value.

**Explicit results** os.path.realpath(get\_export\_folder(Platform\_app, studio\_app)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Studio App {0} is not exported to {1}.”.format(studio\_app, Platform\_app).

**Local steps**

- If Platform.db.get\_value(“Studio App”, studio\_app, “Platform\_app”) differs from Platform\_app.
  - Call the validation error handler Platform.throw(translated “Studio App {0} is not exported to {1}.”.format(studio\_app, Platform\_app), Platform.PermissionError).
- Return os.path.realpath(get\_export\_folder(Platform\_app, studio\_app)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1890)

<a id="op-0bff7410ebbf74"></a>
### Resolve studio file

`operation_foundation_binding_foundation_studio_api_resolve_studio_file`

**Inputs** Platform\_app, studio\_app, file\_path.

**Declared result** str.

**Explicit results** target.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid file path: {0}”.format(file\_path).

**Local steps**

- Set root from \_studio\_app\_root(Platform\_app, studio\_app).
- Set target from os.path.realpath(os.path.join(root, file\_path)).
- If (target differs from root and not target.startswith((root + os.sep))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target differs from root → not target.startswith((root + os.sep)).
  - Call the validation error handler Platform.throw(translated “Invalid file path: {0}”.format(file\_path), Platform.PermissionError).
- Return target.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1889)

<a id="op-597e4f6468c3c0"></a>
### Build studio file tree

`operation_foundation_binding_foundation_studio_api_build_studio_file_tree`

**Inputs** directory, root.

**Declared result** list at dict.

**Explicit results** nodes.

**Local steps**

- Set nodes from list().
- For each name in sorted(os.listdir(directory)).
  - If (name.startswith(“.”) or name belongs to tuple(“\_\_pycache\_\_”, “node\_modules”, “tsconfig.json”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.startswith(“.”) → name belongs to tuple(“\_\_pycache\_\_”, “node\_modules”, “tsconfig.json”).
    - Continue with the next iteration or loop test.
  - Set absolute\_path from os.path.join(directory, name).
  - Set relative\_path from os.path.relpath(absolute\_path, root).
  - If os.path.isdir(absolute\_path).
    - Set children from \_build\_studio\_file\_tree(absolute\_path, root).
    - Evaluate nodes.append(mapping(“label” → name, “path” → relative\_path, “is\_folder” → true, “children” → children)).
  - Otherwise.
    - If nested operand in the contract.path.splitext(name) at 1.lower() belongs to ALLOWED\_STUDIO\_FILE\_EXTENSIONS.
      - Evaluate nodes.append(mapping(“label” → name, “path” → relative\_path, “is\_folder” → false, “children” → list())).
- Evaluate nodes.sort(key = deferred anonymous expression).
- Return nodes.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1867)

## Service · Artifact

<a id="op-5b83b16ce77584"></a>
### Generate page json

`operation_foundation_binding_foundation_studio_ai_agent_artifact_generate_page_json`

**Inputs** ctx, args.

**Declared result** list at dict.

**Explicit results** list() · list(mapping(“tool\_name” → “generate\_page”, “args” → mapping(“block” → block))).

**Explicit failure paths** CancelledError.

**Local steps**

- Set brief from (args.get(“brief”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“brief”) → empty text.
- Set messages from list(mapping(“role” → “system”, “content” → get\_generation\_prompt(), “cache\_control” → mapping(“type” → “ephemeral”))).
- Evaluate messages.extend(AISession.build\_context\_messages\_from\_id(ctx.session\_id)).
- If data\_note bound to \_available\_data\_note(ctx).
  - Evaluate messages.append(mapping(“role” → “user”, “content” → data\_note)).
- Evaluate messages.append(\_build\_message(ctx, brief)).
- Evaluate ctx.emit(“progress”, message = “Building the page…”).
- Set content from empty text.
- Set finish\_reason from no value.
- Set stream from llm.complete(ctx.model, messages, llm.TASK\_PARAMS at “complex”, stream = true, api\_key = ctx.api\_key).
- For each chunk in stream.
  - If ctx.is\_cancelled().
    - Attempt the following.
      - Evaluate stream.close().
    - On failure (Exception).
      - Take no action here.
    - Bind dependencies CancelledError.
    - Raise CancelledError.
  - If not chunk.choices.
    - Continue with the next iteration or loop test.
  - If fr bound to chunk.choices at 0.finish\_reason.
    - Set finish\_reason from fr.
  - Set delta from chunk.choices at 0.delta.content.
  - If delta.
    - Update content using + delta.
    - Evaluate ctx.emit(“stream”, chunk = delta, kind = “page\_json”).
- If finish\_reason equals “length”.
  - Evaluate logger.warning(“generate\_page hit max\_tokens — the page may be truncated”).
- Attempt the following.
  - Set block from BlockCodec.parse\_blocks(content).
- On failure (Exception) bound to e.
  - Evaluate logger.warning(“generate\_page\_json: could not parse model output (model=%s): %s”, ctx.model, e).
  - Return list().
- Return list(mapping(“tool\_name” → “generate\_page”, “args” → mapping(“block” → block))).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1719)

<a id="op-0bdf353a0e83b6"></a>
### Build message

`operation_foundation_binding_foundation_studio_ai_agent_artifact_build_message`

**Inputs** ctx, brief.

**Declared result** dict.

**Explicit results** mapping(“role” → “user”, “content” → text) · mapping(“role” → “user”, “content” → list(mapping(“type” → “text”, “text” → text), mapping(“type” → “image\_url”, “image\_url” → mapping(“url” → image\_url)))).

**Local steps**

- Set text from formatted text Build this page now: {brief} when brief, otherwise “Build the page now.”.
  - Value choice on brief — true gives formatted text Build this page now: {brief}, false gives “Build the page now.”.
- Set image\_url from getattr(ctx, “image\_url”, no value).
- If (not image\_url or not ModelRegistry.is\_vision\_capable(ctx.model)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not image\_url → not ModelRegistry.is\_vision\_capable(ctx.model).
  - Return mapping(“role” → “user”, “content” → text).
- Update text using + multiline text in the contract.
- Return mapping(“role” → “user”, “content” → list(mapping(“type” → “text”, “text” → text), mapping(“type” → “image\_url”, “image\_url” → mapping(“url” → image\_url)))).

**Values supplied outside this operation** selected callable from getattr(ctx, “image\_url”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1718)

<a id="op-da30c4ea20d002"></a>
### Available data note

`operation_foundation_binding_foundation_studio_ai_agent_artifact_available_data_note`

**Inputs** ctx.

**Declared result** str.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** empty text · (“Data sources and variables already created on this page — bind the layout to THESE (and only these), per the …” + BlockCodec.to\_json(state)).

**Local steps**

- Set page from Platform.get\_doc(“Studio Page”, ctx.page\_id) when ctx.page\_id, otherwise no value.
  - Value choice on ctx.page\_id — true gives Platform.get\_doc(“Studio Page”, ctx.page\_id), false gives no value.
- If page is identical to no value.
  - Return empty text.
- Set state from describe\_page\_data(page).
- If (not state at “data\_sources” and not state at “variables”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not state at “data\_sources” → not state at “variables”.
  - Return empty text.
- Return (“Data sources and variables already created on this page — bind the layout to THESE (and only these), per the …” + BlockCodec.to\_json(state)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1717)

## Service · Assign to

<a id="op-0779f69901b6df"></a>
### Get

`operation_foundation_desk_form_assign_to_business_behavior_get`

**Inputs** args = no value.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** Platform.get\_all(“ToDo”, fields = list(“allocated\_to as owner”, “name”), filters = mapping(“reference\_type” → args.get(“doctype”), “reference\_name” → args.get(“name”), “status” → tuple(“not in”, tuple(“Can ….

**Local steps**

- If not args.
  - Set args from Platform.local.form\_dict.
- Return Platform.get\_all(“ToDo”, fields = list(“allocated\_to as owner”, “name”), filters = mapping(“reference\_type” → args.get(“doctype”), “reference\_name” → args.get(“name”), “status” → tuple(“not in”, tuple(“Can ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L4475) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L157)

<a id="op-248bd130c5c410"></a>
### Add

`operation_foundation_desk_form_assign_to_business_behavior_add`

**Inputs** args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_add(args, ignore\_permissions = false, validate\_assignees = is\_endpoint\_call(“Platform.desk.form.assign\_to.add”)).

**Local steps**

- Return \_add(args, ignore\_permissions = false, validate\_assignees = is\_endpoint\_call(“Platform.desk.form.assign\_to.add”)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L48) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L150)

<a id="op-eccd17edfd8b12"></a>
### Is endpoint call

`operation_foundation_binding_foundation_desk_form_assign_to_is_endpoint_call`

**Inputs** method.

**Declared result** bool.

**Explicit results** (bool(request) and method belongs to set(nested operand in the contract(nested operand in the contract).rpartition(“/”) at 2, Platform.form\_dict.cmd)).

**Local steps**

- Set request from getattr(Platform.local, “request”, no value).
- Return (bool(request) and method belongs to set(nested operand in the contract(nested operand in the contract).rpartition(“/”) at 2, Platform.form\_dict.cmd)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(request) → method belongs to set(nested operand in the contract.removesuffix(“/”).rpartition(“/”) at 2, Platform.form\_dict.cmd).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L766)

<a id="op-acc25d64918303"></a>
### Add

`operation_foundation_desk_form_assign_to_business_behavior_add_2`

**Inputs** args = no value, ignore\_permissions (named only, default false), validate\_assignees (named only, default false).

**Record and data access** resolve a document from args at “doctype” via get\_doc · read “ToDo” via get\_all · resolve a document from mapping(“doctype” → “ToDo”, “allocated\_to” → assign\_to, “reference\_type” → args at “doctype”, “reference\_name” → str(args at “name”), …) via get\_doc · read “User” via get\_cached\_value.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “ToDo”, “allocated\_to” → assign\_to, “reference\_type” → args at “doctype”, “reference\_name” → str(args at “name”), …)) · request set\_value on args at “doctype” · msgprint with translated “Shared with the following Users with Read access:{0}”.format(user\_list, alert = true) · msgprint with translated “Already in the following Users ToDo list:{0}”.format(user\_list, alert = true).

**Explicit results** get(args).

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not args.
  - Set args from Platform.local.form\_dict.
- Set users\_with\_duplicate\_todo from list().
- Set shared\_with\_users from list().
- For each assign\_to in Platform.parse\_json(args.get(“assign\_to”)).
  - Set filters from mapping(“reference\_type” → args at “doctype”, “reference\_name” → args at “name”, “status” → “Open”, “allocated\_to” → assign\_to).
  - If not ignore\_permissions.
    - Evaluate Platform.get\_doc(args at “doctype”, args at “name”).check\_permission().
  - If validate\_assignees.
    - Evaluate Platform.share.validate\_user\_access(assign\_to, translated “Allocated To”).
  - If Platform.get\_all(“ToDo”, filters = filters).
    - Evaluate users\_with\_duplicate\_todo.append(assign\_to).
  - Otherwise.
    - Bind dependencies nowdate.
    - Set description from (args.get(“description”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“description”) → empty text.
    - Set has\_content from (strip\_html(description) or “&lt;img” belongs to description).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in strip\_html(description) → “&lt;img” belongs to description.
    - If not has\_content.
      - Set args at “description” from translated “Assignment for {0} {1}”.format(args at “doctype”, args at “name”).
    - Set d from Platform.get\_doc(mapping(“doctype” → “ToDo”, “allocated\_to” → assign\_to, “reference\_type” → args at “doctype”, “reference\_name” → str(args at “name”), …)).insert(ignore\_permissions = true).
    - If Platform.get\_meta(args at “doctype”).get\_field(“assigned\_to”).
      - Evaluate Platform.db.set\_value(args at “doctype”, args at “name”, “assigned\_to”, assign\_to).
    - Set doc from Platform.get\_doc(args at “doctype”, args at “name”).
    - If not Platform.has\_permission(doc = doc, user = assign\_to).
      - If Platform.get\_system\_settings(“disable\_document\_sharing”).
        - Set msg from translated “User {0} is not permitted to access this document.”.format(Platform.bold(assign\_to)).
        - Update msg using + (text in the contract + translated “As document sharing is disabled, please give them the required permissions before assigning.”).
        - Call the validation error handler Platform.throw(msg, title = translated “Missing Permission”).
      - Otherwise.
        - Evaluate Platform.share.add\_docshare(doc.doctype, str(doc.name), assign\_to).
        - Evaluate shared\_with\_users.append(assign\_to).
    - If Platform.get\_cached\_value(“User”, assign\_to, “follow\_assigned\_documents”).
      - Evaluate \_follow\_document(args at “doctype”, args at “name”, assign\_to).
    - Evaluate notify\_assignment(d.assigned\_by, d.allocated\_to, d.reference\_type, d.reference\_name, action = “ASSIGN”, description = args.get(“description”)).
- If shared\_with\_users.
  - Set user\_list from format\_message\_for\_assign\_to(shared\_with\_users).
  - Evaluate Platform.msgprint(translated “Shared with the following Users with Read access:{0}”.format(user\_list, alert = true)).
- If users\_with\_duplicate\_todo.
  - Set user\_list from format\_message\_for\_assign\_to(users\_with\_duplicate\_todo).
  - Evaluate Platform.msgprint(translated “Already in the following Users ToDo list:{0}”.format(user\_list, alert = true)).
- Return get(args).

**Values supplied outside this operation** clock or generated value from nowdate() · effective access from Platform.has\_permission(doc = doc, user = assign\_to) · configured or stored value from Platform.get\_system\_settings(“disable\_document\_sharing”), Platform.get\_cached\_value(“User”, assign\_to, “follow\_assigned\_documents”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L49) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L151)

<a id="op-07c9438cd704e3"></a>
### Add multiple

`operation_foundation_desk_form_assign_to_business_behavior_add_multiple`

**Inputs** args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If not args.
  - Set args from Platform.local.form\_dict.
- Set docname\_list from json.loads(args at “name”).
- For each docname in docname\_list.
  - Evaluate args.update(mapping(“name” → docname)).
  - Evaluate \_add(args, ignore\_permissions = false, validate\_assignees = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L50) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L152)

<a id="op-6de71b5abbfb24"></a>
### Close all assignments

`operation_foundation_desk_form_assign_to_business_behavior_close_all_assignments`

**Inputs** doctype, name, ignore\_permissions = false.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** false · true.

**Local steps**

- Set assignments from Platform.get\_all(“ToDo”, fields = list(“allocated\_to”, “name”), filters = dict(reference\_type = doctype, reference\_name = name, status = tuple(“not in”, list(“Cancelled”, “Closed”)))).
- If not assignments.
  - Return false.
- For each assign\_to in assignments.
  - Evaluate set\_status(doctype, name, todo = assign\_to.name, assign\_to = assign\_to.allocated\_to, status = “Closed”, ignore\_permissions = ignore\_permissions).
- Return true.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L6995) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L155)
