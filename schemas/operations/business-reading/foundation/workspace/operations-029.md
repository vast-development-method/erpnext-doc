# Forms, reports and navigation · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Files

<a id="op-698dca5f09dd8b"></a>
### Page script owner

`operation_foundation_binding_foundation_studio_files_page_script_owner`

**Inputs** studio\_app, file\_path.

**Declared result** (str bitwise or no value).

**Explicit results** page\_script\_paths(studio\_app).get(path) when is\_page\_script\_path(path), otherwise no value.

**Local steps**

- Set path from normalize\_path(file\_path).
- Return page\_script\_paths(studio\_app).get(path) when is\_page\_script\_path(path), otherwise no value.
  - Value choice on is\_page\_script\_path(path) — true gives page\_script\_paths(studio\_app).get(path), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L238) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L45) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L133)

<a id="op-dbf8666de05533"></a>
### Page script paths

`operation_foundation_binding_foundation_studio_files_page_script_paths`

**Inputs** studio\_app.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** mapping of formatted text studio\_page/{stem bound to Platform.scrub(page.page\_title)}/{stem}.js → page.name for page drawn from pages.

**Local steps**

- Set pages from Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → studio\_app, “page\_title” → tuple(“is”, “set”)), fields = list(“name”, “page\_title”)).
- Return mapping of formatted text studio\_page/{stem bound to Platform.scrub(page.page\_title)}/{stem}.js → page.name for page drawn from pages.
  - Draw page from pages.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L239) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L46) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L134)

<a id="op-2dae27d2fc9ecf"></a>
### Is component script path

`operation_foundation_binding_foundation_studio_files_is_component_script_path`

**Inputs** path.

**Declared result** bool.

**Explicit results** bool(re.fullmatch(“studio\_components/&#91;^/&#93;+\\.(js\|ts)”, path)).

**Local steps**

- Return bool(re.fullmatch(“studio\_components/&#91;^/&#93;+\\.(js\|ts)”, path)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L229) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L36) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L124)

<a id="op-defb28f4210e93"></a>
### Component script owner

`operation_foundation_binding_foundation_studio_files_component_script_owner`

**Inputs** studio\_app, file\_path.

**Declared result** (str bitwise or no value).

**Explicit results** no value · find\_component(posixpath.basename(path).removesuffix(“.js”), studio\_app).

**Local steps**

- Bind dependencies find\_component.
- Set path from normalize\_path(file\_path).
- If (not is\_component\_script\_path(path) or not path.endswith(“.js”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_component\_script\_path(path) → not path.endswith(“.js”).
  - Return no value.
- Return find\_component(posixpath.basename(path).removesuffix(“.js”), studio\_app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L217) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L24) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L112)

<a id="op-92556da358de0a"></a>
### Component script paths

`operation_foundation_binding_foundation_studio_files_component_script_paths`

**Inputs** studio\_app.

**Declared result** set at str.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** set of formatted text studio\_components/{component.component\_id}.js for component drawn from get\_components\_for\_blocks(blocks, studio\_app) where component.script.

**Local steps**

- Bind dependencies get\_components\_for\_blocks.
- Set pages from Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → studio\_app), fields = list(“blocks”, “draft\_blocks”)).
- Set blocks from list of block for page drawn from pages, then tree drawn from tuple(page.blocks, page.draft\_blocks), then block drawn from parse\_blocks(tree).
  - Draw page from pages.
  - Draw tree from tuple(page.blocks, page.draft\_blocks).
  - Draw block from parse\_blocks(tree).
- Return set of formatted text studio\_components/{component.component\_id}.js for component drawn from get\_components\_for\_blocks(blocks, studio\_app) where component.script.
  - Draw component from get\_components\_for\_blocks(blocks, studio\_app), keep a combination only if (component.script).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L218) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L25) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L113)

<a id="op-01cbe6f1598090"></a>
### Parse blocks

`operation_foundation_binding_foundation_studio_files_parse_blocks`

**Inputs** blocks.

**Declared result** list at dict.

**Explicit results** Platform.parse\_json(blocks) when blocks, otherwise list().

**Local steps**

- Return Platform.parse\_json(blocks) when blocks, otherwise list().
  - Value choice on blocks — true gives Platform.parse\_json(blocks), false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L240) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L47) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L135)

<a id="op-ab84d69712a706"></a>
### List db file tree

`operation_foundation_binding_foundation_studio_files_list_db_file_tree`

**Inputs** studio\_app.

**Declared result** list at dict.

**Record and data access** read “Studio App File” via get\_all.

**Explicit results** build\_tree(empty text, folders, files).

**Local steps**

- Set paths from Platform.get\_all(“Studio App File”, filters = mapping(“studio\_app” → studio\_app), pluck = “file\_path”).
- Set files from ((set(paths) bitwise or page\_script\_paths(studio\_app).keys()) bitwise or component\_script\_paths(studio\_app)).
- Set folders from set().
- For each path in files.
  - Set folder from posixpath.dirname(path).
  - While folder.
    - Evaluate folders.add(folder).
    - Set folder from posixpath.dirname(folder).
- Return build\_tree(empty text, folders, files).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L236) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L43) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L131)

<a id="op-090d766a211367"></a>
### Build tree

`operation_foundation_binding_foundation_studio_files_build_tree`

**Inputs** parent, folders, files.

**Declared result** list at dict.

**Explicit results** nodes.

**Local steps**

- Set nodes from list of mapping(“label” → posixpath.basename(path), “path” → path, “is\_folder” → true, “children” → build\_tree(path, folders, files)) for path drawn from folders where posixpath.dirname(path) equals parent.
  - Draw path from folders, keep a combination only if (posixpath.dirname(path) equals parent).
- Update nodes using + list of mapping(“label” → posixpath.basename(path), “path” → path, “is\_folder” → false, “children” → list()) for path drawn from files where posixpath.dirname(path) equals parent.
  - Draw path from files, keep a combination only if (posixpath.dirname(path) equals parent).
- Evaluate nodes.sort(key = deferred anonymous expression).
- Return nodes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L216) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L23) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L111)

<a id="op-46379593dc78d8"></a>
### Get db files

`operation_foundation_binding_foundation_studio_files_get_db_files`

**Inputs** studio\_app.

**Declared result** list at dict.

**Record and data access** read “Studio App File” via get\_all.

**Explicit results** list of mapping(“path” → row.file\_path, “content” → (row.content or empty text)) for row drawn from rows.

**Local steps**

- Set rows from Platform.get\_all(“Studio App File”, filters = mapping(“studio\_app” → studio\_app), fields = list(“file\_path”, “content”), order\_by = “file\_path”).
- Return list of mapping(“path” → row.file\_path, “content” → (row.content or empty text)) for row drawn from rows.
  - Draw row from rows.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L227) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L34) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L122)

<a id="op-b4b26f4f0b6ea0"></a>
### Write db files

`operation_foundation_binding_foundation_studio_files_write_db_files`

**Inputs** studio\_app, files.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Invalid copied file.” · validation helper — translated “Unsupported copied file: {0}”.format(path) · validation helper — translated “The copy contains conflicting versions of {0}.”.format(path) · validation helper — translated “{0} already exists with different content. Rename it before pasting.”.format(path).

**Local steps**

- Set existing from mapping of file at “path” → file at “content” for file drawn from get\_db\_files(studio\_app).
  - Draw file from get\_db\_files(studio\_app).
- Set targets from mapping().
- For each file in files.
  - If (not isinstance(file, dict) or not isinstance(file.get(“path”), str) or not isinstance(file.get(“content”), str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(file, dict) → not isinstance(file.get(“path”), str) → not isinstance(file.get(“content”), str).
    - Call the validation error handler Platform.throw(translated “Invalid copied file.”).
  - Set path from normalize\_path(file at “path”).
  - Evaluate validate\_allowed\_extension(path, ALLOWED\_DB\_FILE\_EXTENSIONS).
  - Evaluate validate\_folder\_names(path).
  - If not is\_db\_file\_allowed(studio\_app, path).
    - Call the validation error handler Platform.throw(translated “Unsupported copied file: {0}”.format(path)).
  - If (path belongs to targets and targets at path differs from file at “content”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in path belongs to targets → targets at path differs from file at “content”.
    - Call the validation error handler Platform.throw(translated “The copy contains conflicting versions of {0}.”.format(path)).
  - If (path belongs to existing and existing at path differs from file at “content”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in path belongs to existing → existing at path differs from file at “content”.
    - Call the validation error handler Platform.throw(translated “{0} already exists with different content. Rename it before pasting.”.format(path), title = translated “File conflict”).
  - Set targets at path from file at “content”.
- For each tuple(path, content) in targets.items().
  - If path does not belong to existing.
    - Evaluate write\_db\_file(studio\_app, path, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L252) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L59) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L147)

<a id="op-32de2a33e17f2a"></a>
### Read db file

`operation_foundation_binding_foundation_studio_files_read_db_file`

**Inputs** studio\_app, file\_path.

**Declared result** (str bitwise or no value).

**Record and data access** read “Studio Page” via get\_value · read “Studio Component” via get\_value.

**Explicit results** (Platform.db.get\_value(“Studio Page”, page, “script”) or empty text) · (Platform.db.get\_value(“Studio Component”, component, “script”) or empty text) · no value · (row.content or empty text).

**Local steps**

- Set page from page\_script\_owner(studio\_app, file\_path).
- If page.
  - Return (Platform.db.get\_value(“Studio Page”, page, “script”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Studio Page”, page, “script”) → empty text.
- Set component from component\_script\_owner(studio\_app, file\_path).
- If component.
  - Evaluate Platform.has\_permission(“Studio Component”, ptype = “read”, doc = component, throw = true).
  - Return (Platform.db.get\_value(“Studio Component”, component, “script”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Studio Component”, component, “script”) → empty text.
- Set row from get\_db\_file\_row(studio\_app, file\_path).
- If not row.
  - Return no value.
- Return (row.content or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → empty text.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Component”, ptype = “read”, doc = component, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L241) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L48) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L136)

<a id="op-205ae3cbbbcdeb"></a>
### Write db file

`operation_foundation_binding_foundation_studio_files_write_db_file`

**Inputs** studio\_app, file\_path, content, known\_hash = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Studio App File” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** write\_page\_script(page, content, known\_hash) · write\_component\_script(component, content, known\_hash) · no value.

**Explicit failure paths** validation helper — translated “Invalid file content.” · validation helper — translated “{0} changed since you opened it.”.format(file\_path).

**Local steps**

- If not isinstance(content, str).
  - Call the validation error handler Platform.throw(translated “Invalid file content.”).
- Set page from page\_script\_owner(studio\_app, file\_path).
- If page.
  - Return write\_page\_script(page, content, known\_hash).
- Set component from component\_script\_owner(studio\_app, file\_path).
- If component.
  - Return write\_component\_script(component, content, known\_hash).
- Set row from get\_db\_file\_row(studio\_app, file\_path).
- If not row.
  - Evaluate insert\_db\_file\_row(studio\_app, file\_path, content).
  - Return no value.
- If (known\_hash and file\_hash((row.content or empty text)) differs from known\_hash).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in known\_hash → file\_hash((row.content or empty text)) differs from known\_hash.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.content → empty text.
  - Call the validation error handler Platform.throw(translated “{0} changed since you opened it.”.format(file\_path)).
- Set doc from Platform.get\_doc(“Studio App File”, row.name).
- Set doc.content from content.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L251) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L58) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L146)

<a id="op-eb1563a9a81789"></a>
### Write page script

`operation_foundation_binding_foundation_studio_files_write_page_script`

**Inputs** page, content, known\_hash = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper — translated “{0} changed since you opened it.”.format(doc.page\_title).

**Local steps**

- Set doc from Platform.get\_doc(“Studio Page”, page).
- If (known\_hash and file\_hash((doc.script or empty text)) differs from known\_hash).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in known\_hash → file\_hash((doc.script or empty text)) differs from known\_hash.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.script → empty text.
  - Call the validation error handler Platform.throw(translated “{0} changed since you opened it.”.format(doc.page\_title)).
- Set doc.script from content.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L253) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L60) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L148)

<a id="op-deda8db9673ed3"></a>
### Write component script

`operation_foundation_binding_foundation_studio_files_write_component_script`

**Inputs** component, content, known\_hash = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper — translated “{0} changed since you opened it.”.format(doc.component\_name).

**Local steps**

- Set doc from Platform.get\_doc(“Studio Component”, component).
- If (known\_hash and file\_hash((doc.script or empty text)) differs from known\_hash).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in known\_hash → file\_hash((doc.script or empty text)) differs from known\_hash.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.script → empty text.
  - Call the validation error handler Platform.throw(translated “{0} changed since you opened it.”.format(doc.component\_name)).
- Set doc.script from content.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L250) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L57) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L145)

<a id="op-5609fd5f6e3aca"></a>
### Create db file

`operation_foundation_binding_foundation_studio_files_create_db_file`

**Inputs** studio\_app, file\_path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} already exists.”.format(file\_path).

**Local steps**

- If db\_path\_exists(studio\_app, file\_path).
  - Call the validation error handler Platform.throw(translated “{0} already exists.”.format(file\_path)).
- Evaluate insert\_db\_file\_row(studio\_app, file\_path, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L219) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L26) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L114)

<a id="op-cfb0dfb4f507ee"></a>
### Rename db path

`operation_foundation_binding_foundation_studio_files_rename_db_path`

**Inputs** studio\_app, file\_path, new\_path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “A page script is named after its page. Rename the page instead.” · validation helper — translated “A component script is named after its component.” · validation helper — translated “Not found: {0}”.format(file\_path) · validation helper — translated “{0} already exists.”.format(new\_path).

**Local steps**

- Set old from normalize\_path(file\_path).
- Set new from normalize\_path(new\_path).
- If (page\_script\_owner(studio\_app, old) or page\_script\_owner(studio\_app, new)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_script\_owner(studio\_app, old) → page\_script\_owner(studio\_app, new).
  - Call the validation error handler Platform.throw(translated “A page script is named after its page. Rename the page instead.”).
- If (component\_script\_owner(studio\_app, old) or component\_script\_owner(studio\_app, new)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component\_script\_owner(studio\_app, old) → component\_script\_owner(studio\_app, new).
  - Call the validation error handler Platform.throw(translated “A component script is named after its component.”).
- Set row from get\_db\_file\_row(studio\_app, old).
- Set children from get\_db\_file\_rows\_under(studio\_app, old).
- If (not row and not children).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row → not children.
  - Call the validation error handler Platform.throw(translated “Not found: {0}”.format(file\_path)).
- If db\_path\_exists(studio\_app, new).
  - Call the validation error handler Platform.throw(translated “{0} already exists.”.format(new\_path)).
- For each child in children.
  - Evaluate rename\_db\_file\_row(child.name, (new + child.file\_path at slice len(old) to no value)).
- If row.
  - Evaluate rename\_db\_file\_row(row.name, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L243) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L50) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L138)

<a id="op-d66e20535f0ae3"></a>
### Rename db file row

`operation_foundation_binding_foundation_studio_files_rename_db_file_row`

**Inputs** name, new\_path.

**Declared result** no value.

**Record and data access** resolve a document from “Studio App File” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Studio App File”, name).
- Set doc.file\_path from new\_path.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L242) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L49) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L137)

<a id="op-16415b4e5b7c57"></a>
### Delete db path

`operation_foundation_binding_foundation_studio_files_delete_db_path`

**Inputs** studio\_app, file\_path.

**Declared result** no value.

**State and service calls** request delete\_doc for “Studio App File”.

**Explicit results** write\_page\_script(page, empty text) · write\_component\_script(component, empty text).

**Explicit failure paths** validation helper — translated “Not found: {0}”.format(file\_path).

**Local steps**

- Set path from normalize\_path(file\_path).
- Set page from page\_script\_owner(studio\_app, path).
- If page.
  - Return write\_page\_script(page, empty text).
- Set component from component\_script\_owner(studio\_app, path).
- If component.
  - Return write\_component\_script(component, empty text).
- Set row from get\_db\_file\_row(studio\_app, path).
- Set children from get\_db\_file\_rows\_under(studio\_app, path).
- If (not row and not children).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row → not children.
  - Call the validation error handler Platform.throw(translated “Not found: {0}”.format(file\_path)).
- For each child in children.
  - Evaluate Platform.delete\_doc(“Studio App File”, child.name).
- If row.
  - Evaluate Platform.delete\_doc(“Studio App File”, row.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L221) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L28) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L116)

<a id="op-00104ec09750f3"></a>
### Db path exists

`operation_foundation_binding_foundation_studio_files_db_path_exists`

**Inputs** studio\_app, path.

**Declared result** bool.

**Explicit results** true · bool((get\_db\_file\_row(studio\_app, path) or get\_db\_file\_rows\_under(studio\_app, path))).

**Local steps**

- If (page\_script\_owner(studio\_app, path) or component\_script\_owner(studio\_app, path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_script\_owner(studio\_app, path) → component\_script\_owner(studio\_app, path).
  - Return true.
- Return bool((get\_db\_file\_row(studio\_app, path) or get\_db\_file\_rows\_under(studio\_app, path))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_db\_file\_row(studio\_app, path) → get\_db\_file\_rows\_under(studio\_app, path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L220) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L27) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L115)

<a id="op-7773172d477169"></a>
### Get db file row

`operation_foundation_binding_foundation_studio_files_get_db_file_row`

**Inputs** studio\_app, file\_path.

**Record and data access** read “Studio App File” via get\_value.

**Explicit results** Platform.db.get\_value(“Studio App File”, mapping(“studio\_app” → studio\_app, “file\_path” → normalize\_path(file\_path)), list(“name”, “file\_path”, “content”), as\_dict = true).

**Local steps**

- Return Platform.db.get\_value(“Studio App File”, mapping(“studio\_app” → studio\_app, “file\_path” → normalize\_path(file\_path)), list(“name”, “file\_path”, “content”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L225) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L32) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L120)

<a id="op-642d0dd3397e8d"></a>
### Get db file rows under

`operation_foundation_binding_foundation_studio_files_get_db_file_rows_under`

**Inputs** studio\_app, folder\_path.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Studio App File” via get\_all.

**Explicit results** list of row for row drawn from rows where row.file\_path.startswith(prefix).

**Local steps**

- Set prefix from (normalize\_path(folder\_path) + “/”).
- Set rows from Platform.get\_all(“Studio App File”, filters = mapping(“studio\_app” → studio\_app), fields = list(“name”, “file\_path”)).
- Return list of row for row drawn from rows where row.file\_path.startswith(prefix).
  - Draw row from rows, keep a combination only if (row.file\_path.startswith(prefix)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L226) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L121)

<a id="op-62ec91973e83cd"></a>
### Insert db file row

`operation_foundation_binding_foundation_studio_files_insert_db_file_row`

**Inputs** studio\_app, file\_path, content.

**Declared result** no value.

**Record and data access** resolve a document from “Studio App File” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “Studio App File”, studio\_app = studio\_app, file\_path = file\_path, content = content).

**Local steps**

- Evaluate Platform.get\_doc(doctype = “Studio App File”, studio\_app = studio\_app, file\_path = file\_path, content = content).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L228) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L35) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L123)

<a id="op-91a931b83fc6cf"></a>
### Export db files to disk

`operation_foundation_binding_foundation_studio_files_export_db_files_to_disk`

**Inputs** app.

**Declared result** no value.

**State and service calls** request delete on “Studio App File”.

**Local steps**

- If files bound to get\_db\_files(app.name).
  - Evaluate app.write\_exported\_files(files).
  - Evaluate Platform.db.delete(“Studio App File”, mapping(“studio\_app” → app.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L223) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L30) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L118)

<a id="op-f17be6db62b7c3"></a>
### Restore db files from disk

`operation_foundation_binding_foundation_studio_files_restore_db_files_from_disk`

**Inputs** app.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set root from app.get\_folder\_path().
- If not os.path.isdir(root).
  - Return no value.
- For each tuple(dirpath, filenames, folder) in walk\_export\_folder(root).
  - For each filename in filenames.
    - Set path from formatted text {folder}/{filename} when folder, otherwise filename.
      - Value choice on folder — true gives formatted text {folder}/{filename}, false gives filename.
    - If not is\_db\_file\_allowed(app.name, path).
      - Continue with the next iteration or loop test.
    - Evaluate write\_db\_file(app.name, path, (Platform.read\_file(os.path.join(dirpath, filename)) or empty text)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.read\_file(os.path.join(dirpath, filename)) → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L244) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L51) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L139)
