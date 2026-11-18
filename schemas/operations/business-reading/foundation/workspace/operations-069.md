# Forms, reports and navigation · operations 69

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio component

<a id="op-a015886e60bb69"></a>
### Studio Component.rename references

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_rename_references`

**Inputs** self, old\_id, new\_id.

**Record and data access** resolve a document from “Studio Component” via get\_doc · resolve a document from “Studio Page” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- For each component in self.get\_referencing\_docs(“Studio Component”, old\_id).
  - Set doc from Platform.get\_doc(“Studio Component”, component.name).
  - Set block from parse\_json(doc.block).
  - If not rename\_component\_in\_blocks(block, old\_id, new\_id).
    - Continue with the next iteration or loop test.
  - Set doc.block from block.
  - Evaluate doc.save().
  - For each folder in doc.get\_export\_folders().
    - Evaluate doc.export\_to\_folder(folder).
- For each page in self.get\_referencing\_docs(“Studio Page”, old\_id).
  - Set doc from Platform.get\_doc(“Studio Page”, page.name).
  - Set trees from mapping of field → parse\_json(doc.get(field)) for field drawn from tuple(“blocks”, “draft\_blocks”).
    - Draw field from tuple(“blocks”, “draft\_blocks”).
  - If not any(list of rename\_component\_in\_blocks(tree, old\_id, new\_id) for tree drawn from trees.values()).
    - Draw tree from trees.values().
    - Continue with the next iteration or loop test.
  - For each tuple(field, tree) in trees.items().
    - If tree.
      - Evaluate doc.set(field, Platform.as\_json(tree, indent = no value)).
  - Set doc.\_skip\_validate from true.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get referencing docs](operations-069.md#op-bf1cf937a71246).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L19)

<a id="op-bf1cf937a71246"></a>
### Studio Component.get referencing docs

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_get_referencing_docs`

**Inputs** self, doctype, old\_id, fields = no value.

**Declared result** list at dict.

**Record and data access** read doctype via get\_all · read “Studio Component” via get\_all.

**Explicit results** Platform.get\_all(doctype, filters = mapping(“studio\_app” → self.studio\_app), fields = fields) · list of doc for doc drawn from docs where doc.studio\_app does not belong to apps\_with\_their\_own.

**Local steps**

- Set fields from list(“name”, “studio\_app”, expanded (fields or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → list().
- If self.studio\_app.
  - Return Platform.get\_all(doctype, filters = mapping(“studio\_app” → self.studio\_app), fields = fields).
- Set apps\_with\_their\_own from Platform.get\_all(“Studio Component”, filters = mapping(“component\_id” → old\_id, “studio\_app” → tuple(“is”, “set”)), pluck = “studio\_app”).
- Set docs from Platform.get\_all(doctype, fields = fields).
- Return list of doc for doc drawn from docs where doc.studio\_app does not belong to apps\_with\_their\_own.
  - Draw doc from docs, keep a combination only if (doc.studio\_app does not belong to apps\_with\_their\_own).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L13)

<a id="op-08efdad596b67f"></a>
### Studio Component.on update

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_on_update`

**Inputs** self.

**Local steps**

- If (can\_export(self) and self.has\_value\_changed(“script”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_export(self) → self.has\_value\_changed(“script”).
  - For each folder in self.get\_export\_folders().
    - Evaluate self.write\_script\_file(folder).
- Evaluate publish\_doc\_change(“Studio Component”, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export folders](operations-069.md#op-703c84698ad92d), [write script file](operations-069.md#op-718ea02391e867).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L18)

<a id="op-36a98d4d99800f"></a>
### Studio Component.on trash

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_on_trash`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- If self.flags.is\_moved.
  - Return no value.
- If not self.flags.is\_app\_deleted.
  - Evaluate self.validate\_not\_used().
- If Platform.conf.developer\_mode.
  - Evaluate self.delete\_files().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not used](operations-068.md#op-aebb23c28c7bd1), [delete files](operations-069.md#op-2fbe301784b2ac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L17)

<a id="op-c8ae1aaecb186a"></a>
### Studio Component.export to folder

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_export_to_folder`

**Inputs** self, folder.

**Local steps**

- Evaluate write\_document\_file(self, folder = folder, exclude\_fields = list(“script”), filename = self.get\_file\_stem()).
- If (self.script and not os.path.exists(self.get\_script\_file\_path(folder))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.script → not os.path.exists(self.get\_script\_file\_path(folder)).
  - Evaluate self.write\_script\_file(folder).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get file stem](operations-069.md#op-ecb316ad66f9d4), [get script file path](operations-069.md#op-c0d11c07acf71a), [write script file](operations-069.md#op-718ea02391e867).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L115) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L10)

<a id="op-718ea02391e867"></a>
### Studio Component.write script file

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_write_script_file`

**Inputs** self, folder.

**Local steps**

- Set stem from self.get\_file\_stem().
- If self.script.
  - Set extension from script\_extension(folder, stem, default = “js”).
  - Evaluate write\_code\_file(self, folder, code\_field = “script”, extension = extension, filename = stem).
- Otherwise.
  - Evaluate delete\_file(self.get\_script\_file\_path(folder)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get file stem](operations-069.md#op-ecb316ad66f9d4), [get script file path](operations-069.md#op-c0d11c07acf71a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L25)

<a id="op-c0d11c07acf71a"></a>
### Studio Component.get script file path

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_get_script_file_path`

**Inputs** self, folder.

**Declared result** str.

**Explicit results** find\_script\_file(folder, self.get\_file\_stem()).

**Local steps**

- Return find\_script\_file(folder, self.get\_file\_stem()).

**Methods declared on this owner** [get file stem](operations-069.md#op-ecb316ad66f9d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L14)

<a id="op-ecb316ad66f9d4"></a>
### Studio Component.get file stem

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_get_file_stem`

**Inputs** self.

**Declared result** str.

**Explicit results** Platform.scrub(self.component\_id).

**Local steps**

- Return Platform.scrub(self.component\_id).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L12)

<a id="op-703c84698ad92d"></a>
### Studio Component.get export folders

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_get_export_folders`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Studio App” via get\_value · read “Studio Component” via exists.

**Explicit results** list of folder for folder drawn from generator of os.path.join(app\_folder, COMPONENT\_FOLDER) for app\_folder drawn from folders where os.path.exists(os.path.join(folder, formatted text {self.get\_file\_stem()}.json)).

**Local steps**

- If self.studio\_app.
  - Set Platform\_app from Platform.db.get\_value(“Studio App”, self.studio\_app, “Platform\_app”).
  - Set folders from list(get\_export\_folder(Platform\_app, self.studio\_app)) when Platform\_app, otherwise list().
    - Value choice on Platform\_app — true gives list(get\_export\_folder(Platform\_app, self.studio\_app)), false gives list().
- Otherwise.
  - Set folders from list of app\_folder for studio\_folder drawn from get\_studio\_folders(), then app\_folder drawn from get\_exported\_app\_folders(studio\_folder) where not Platform.db.exists(“Studio Component”, get\_component\_name( ….
    - Draw studio\_folder from get\_studio\_folders().
    - Draw app\_folder from get\_exported\_app\_folders(studio\_folder), keep a combination only if (not Platform.db.exists(“Studio Component”, get\_component\_name(self.component\_id, get\_exported\_app\_name(app\_folder)))).
- Return list of folder for folder drawn from generator of os.path.join(app\_folder, COMPONENT\_FOLDER) for app\_folder drawn from folders where os.path.exists(os.path.join(folder, formatted text {self.get\_file\_stem()}.json)).
  - Draw folder from generator of os.path.join(app\_folder, COMPONENT\_FOLDER) for app\_folder drawn from folders, keep a combination only if (os.path.exists(os.path.join(folder, formatted text {self.get\_file\_stem()}.json))).
  - Draw app\_folder from folders.

**Methods declared on this owner** [get file stem](operations-069.md#op-ecb316ad66f9d4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L11)

<a id="op-2fbe301784b2ac"></a>
### Studio Component.delete files

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_delete_files`

**Inputs** self.

**Local steps**

- For each folder in self.get\_export\_folders().
  - Evaluate delete\_component\_files(folder, self.get\_file\_stem()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export folders](operations-069.md#op-703c84698ad92d), [get file stem](operations-069.md#op-ecb316ad66f9d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L114) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2032) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L9)

<a id="op-03c9689885fdf6"></a>
### Rename component files

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_rename_component_files`

**Inputs** folder, old\_stem, new\_stem.

**Local steps**

- Set old\_script from find\_script\_file(folder, old\_stem).
- If os.path.exists(old\_script).
  - Evaluate os.replace(old\_script, os.path.join(folder, (new\_stem + nested operand in the contract.path.splitext(old\_script) at 1))).
- Evaluate os.replace(os.path.join(folder, formatted text {old\_stem}.json), os.path.join(folder, formatted text {new\_stem}.json)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L2)

<a id="op-1fedafa1da51fa"></a>
### Rename component in blocks

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_rename_component_in_blocks`

**Inputs** blocks, old\_id, new\_id.

**Declared result** bool.

**Explicit results** renamed.

**Local steps**

- Set renamed from false.
- For each block in walk\_blocks(blocks).
  - If (block.get(“isStudioComponent”) and block.get(“componentName”) equals old\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in block.get(“isStudioComponent”) → block.get(“componentName”) equals old\_id.
    - Set block at “componentName” from new\_id.
    - Set renamed from true.
- Return renamed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L108) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L3)

<a id="op-9734cc77d34be0"></a>
### Get app vue components

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_app_vue_components`

**Inputs** blocks.

**Declared result** list at str.

**Explicit results** sorted(generator of name for name drawn from names where name).

**Local steps**

- Set names from set of block.get(“componentName”) for block drawn from walk\_blocks(blocks) where block.get(“isCustomVueComponent”).
  - Draw block from walk\_blocks(blocks), keep a combination only if (block.get(“isCustomVueComponent”)).
- Return sorted(generator of name for name drawn from names where name).
  - Draw name from names, keep a combination only if (name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1994)

<a id="op-4b465f67d3a95b"></a>
### Validate component id

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_validate_component_id`

**Inputs** component\_id.

**Local steps**

- Evaluate validate\_file\_name(component\_id, translated “Component ID cannot be empty or contain slashes.”, title = translated “Invalid Component ID”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L26)

<a id="op-54c9f0ef80ce82"></a>
### Delete component files

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_delete_component_files`

**Inputs** folder, stem.

**Local steps**

- Evaluate delete\_file(find\_script\_file(folder, stem)).
- Evaluate delete\_file(folder, formatted text {stem}.json).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1990)

<a id="op-6dd11e89966777"></a>
### Mark components standard

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_mark_components_standard`

**Inputs** names.

**State and service calls** request set\_value on “Studio Component”.

**Local steps**

- Evaluate Platform.db.set\_value(“Studio Component”, mapping(“name” → list(“in”, names), “is\_standard” → 0), “is\_standard”, 1, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L106) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L2000)

<a id="op-1496998c34f756"></a>
### Get input values

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_input_values`

**Inputs** row.

**Declared result** list at str.

**Explicit results** list of Platform.utils.cstr((row.get(field) or empty text)) for field drawn from fields.

**Local steps**

- Set fields from tuple(“input\_name”, “type”, “description”, “options”, …).
- Return list of Platform.utils.cstr((row.get(field) or empty text)) for field drawn from fields.
  - Draw field from fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(field) → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1998)

<a id="op-e96e38c97f7cfe"></a>
### Get component name

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_component_name`

**Inputs** component\_id, studio\_app = no value.

**Declared result** str.

**Explicit results** formatted text {studio\_app}/{component\_id} when studio\_app, otherwise component\_id.

**Local steps**

- Return formatted text {studio\_app}/{component\_id} when studio\_app, otherwise component\_id.
  - Value choice on studio\_app — true gives formatted text {studio\_app}/{component\_id}, false gives component\_id.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1996)

<a id="op-1fc89c5a4300e0"></a>
### Get component id

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_component_id`

**Inputs** name.

**Declared result** str.

**Explicit results** name.rpartition(“/”) at 2.

**Local steps**

- Return name.rpartition(“/”) at 2.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1995)

<a id="op-dd2ff151ceb340"></a>
### Find component

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_find_component`

**Inputs** component\_id, studio\_app = no value.

**Declared result** (str bitwise or no value).

**Record and data access** read “Studio Component” via exists.

**Explicit results** next(generator of name for name drawn from names where Platform.db.exists(“Studio Component”, name), no value).

**Local steps**

- Set names from list(get\_component\_name(component\_id, studio\_app), component\_id).
- Return next(generator of name for name drawn from names where Platform.db.exists(“Studio Component”, name), no value).
  - Draw name from names, keep a combination only if (Platform.db.exists(“Studio Component”, name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1993)

<a id="op-9c9a0f9d88819b"></a>
### Get components for blocks

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_components_for_blocks`

**Inputs** blocks, studio\_app = no value.

**Declared result** list at dict.

**Explicit results** components.

**Local steps**

- Set components from list().
- Set requested\_components from set().
- Set to\_fetch from extract\_component\_names(blocks).
- While to\_fetch.
  - Evaluate requested\_components.update(to\_fetch).
  - Set batch from fetch\_component\_batch(to\_fetch, studio\_app).
  - Evaluate components.extend(batch).
  - Set to\_fetch from (get\_nested\_component\_names(batch) − requested\_components).
- Return components.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1997)

<a id="op-1728a84165d836"></a>
### Extract component names

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_extract_component_names`

**Inputs** blocks.

**Declared result** set at str.

**Explicit results** set of block at “componentName” for block drawn from walk\_blocks(blocks) where (block.get(“isStudioComponent”) and block.get(“componentName”)).

**Local steps**

- Return set of block at “componentName” for block drawn from walk\_blocks(blocks) where (block.get(“isStudioComponent”) and block.get(“componentName”)).
  - Draw block from walk\_blocks(blocks), keep a combination only if ((block.get(“isStudioComponent”) and block.get(“componentName”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in block.get(“isStudioComponent”) → block.get(“componentName”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1991)

<a id="op-a9b3fa9e36220d"></a>
### Get nested component names

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_get_nested_component_names`

**Inputs** components.

**Declared result** set at str.

**Explicit results** names.

**Local steps**

- Set names from set().
- For each component in components.
  - Evaluate names.update(extract\_component\_names(component at “block”)).
- Return names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1999)

<a id="op-bd9f5bed26c551"></a>
### Fetch component batch

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_fetch_component_batch`

**Inputs** component\_ids, studio\_app = no value.

**Declared result** list at dict.

**Record and data access** read “Studio Component” via get\_all · read “Studio Component Input” via get\_all.

**Explicit results** list() · components.

**Local steps**

- Set names from list of get\_component\_name(component\_id, studio\_app) for component\_id drawn from component\_ids.
  - Draw component\_id from component\_ids.
- Set found from Platform.get\_all(“Studio Component”, filters = mapping(“name” → list(“in”, list(expanded names, expanded component\_ids))), fields = list(“name”, “component\_name”, “component\_id”, “studio\_app”, …), order\_by ….
- Set components from list(mapping of component.component\_id → component for component drawn from reversed(found).values()).
  - Draw component from reversed(found).
- If not components.
  - Return list().
- Set inputs\_by\_component from mapping().
- Set input\_rows from Platform.get\_all(“Studio Component Input”, filters = mapping(“parenttype” → “Studio Component”, “parent” → list(“in”, list of c.name for c drawn from components)), fields = list(“name”, “parent”, “input\_na ….
  - Draw c from components.
- For each row in input\_rows.
  - Evaluate inputs\_by\_component.setdefault(row.pop(“parent”), list()).append(row).
- For each component in components.
  - Set component at “inputs” from inputs\_by\_component.get(component.name, list()).
- Return components.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1992)
