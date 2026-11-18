# Forms, reports and navigation · operations 68

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio app

<a id="op-9f5e432d64f4e4"></a>
### Validate app name

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_validate_app_name`

**Inputs** name.

**Explicit failure paths** validation helper — translated “App Name must be lowercase, with hyphens instead of spaces or punctuation.”.

**Local steps**

- If (not name or name differs from cleanup\_page\_name(name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → name differs from cleanup\_page\_name(name).
  - Call the validation error handler Platform.throw(translated “App Name must be lowercase, with hyphens instead of spaces or punctuation.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1989)

<a id="op-acff3af1f742f3"></a>
### Move folder

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_move_folder`

**Inputs** source, destination.

**Explicit results** no value.

**Local steps**

- If (not os.path.exists(source) or os.path.exists(destination)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not os.path.exists(source) → os.path.exists(destination).
  - Return no value.
- Evaluate Platform.create\_folder(os.path.dirname(destination)).
- Evaluate shutil.move(source, destination).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1940)

<a id="op-67a3436fc116cf"></a>
### Resolve imports

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_resolve_imports`

**Inputs** source, from\_dir, read.

**Declared result** list at str.

**Explicit results** paths.

**Local steps**

- Set paths from list().
- For each spec in IMPORT\_RE.findall((source or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source → empty text.
  - Set base from spec at slice len(“@app/”) to no value when spec.startswith(“@app/”), otherwise os.path.join(from\_dir, spec).
    - Value choice on spec.startswith(“@app/”) — true gives spec at slice len(“@app/”) to no value, false gives os.path.join(from\_dir, spec).
  - If path bound to resolve\_module(os.path.normpath(base), read).
    - Evaluate paths.append(path).
- Return paths.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1941)

<a id="op-d8097825b8c230"></a>
### Resolve module

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_resolve_module`

**Inputs** base, read.

**Declared result** (str bitwise or no value).

**Explicit results** no value · next(generator of path for path drawn from candidates where read(path) is distinct from no value, no value).

**Local steps**

- If (os.path.isabs(base) or base equals “..” or base.startswith(formatted text ..{os.sep})).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.path.isabs(base) → base equals “..” → base.startswith(formatted text ..{os.sep}).
  - Return no value.
- Set candidates from list(base, expanded generator of (base + ext) for ext drawn from EXTENSIONS, expanded generator of os.path.join(base, formatted text index{ext}) for ext drawn from tuple(“.ts”, “.js”)).
  - Draw ext from EXTENSIONS.
  - Draw ext from tuple(“.ts”, “.js”).
- Return next(generator of path for path drawn from candidates where read(path) is distinct from no value, no value).
  - Draw path from candidates, keep a combination only if (read(path) is distinct from no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1942)

<a id="op-2767bf6a372c3d"></a>
### Custom vue component names

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_custom_vue_component_names`

**Inputs** blocks.

**Declared result** set at str.

**Explicit results** set of block at “componentName” for block drawn from walk\_blocks(blocks) where (block.get(“isCustomVueComponent”) and block.get(“componentName”)).

**Local steps**

- Return set of block at “componentName” for block drawn from walk\_blocks(blocks) where (block.get(“isCustomVueComponent”) and block.get(“componentName”)).
  - Draw block from walk\_blocks(blocks), keep a combination only if ((block.get(“isCustomVueComponent”) and block.get(“componentName”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in block.get(“isCustomVueComponent”) → block.get(“componentName”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1936)

<a id="op-46911f8b77c42a"></a>
### Get vite dev server port

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_get_vite_dev_server_port`

**Inputs** no declared parameters.

**Explicit results** (8080 + port\_offset).

**Local steps**

- Set port\_offset from (Platform.conf.webserver\_port − 8000).
- Return (8080 + port\_offset).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1939)

<a id="op-2ca98d45b886d7"></a>
### Get vite dev server host

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_get_vite_dev_server_host`

**Inputs** no declared parameters.

**Explicit results** formatted text {Platform.local.site}:{get\_vite\_dev\_server\_port()}.

**Local steps**

- Return formatted text {Platform.local.site}:{get\_vite\_dev\_server\_port()}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1938)

## Record · Studio app file

<a id="op-912ba92c331b1e"></a>
### Studio App File.validate

`operation_foundation_binding_foundation_studio_doctype_studio_app_file_studio_app_file_studioappfile_validate`

**Inputs** self.

**Local steps**

- Set self.file\_path from normalize\_path(self.file\_path).
- Evaluate validate\_allowed\_extension(self.file\_path, ALLOWED\_DB\_FILE\_EXTENSIONS).
- Evaluate validate\_folder\_names(self.file\_path).
- Evaluate validate\_editable(self.studio\_app, self.file\_path).
- Evaluate self.validate\_unique\_path().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate unique path](operations-068.md#op-19041e1f8db055).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1934)

<a id="op-19041e1f8db055"></a>
### Studio App File.validate unique path

`operation_foundation_binding_foundation_studio_doctype_studio_app_file_studio_app_file_studioappfile_validate_unique_path`

**Inputs** self.

**Record and data access** read “Studio App File” via exists.

**Explicit failure paths** validation helper — translated “{0} already exists in app {1}.”.format(self.file\_path, self.studio\_app).

**Local steps**

- Set duplicate from Platform.db.exists(“Studio App File”, mapping(“studio\_app” → self.studio\_app, “file\_path” → self.file\_path, “name” → list(“!=”, self.name))).
- If duplicate.
  - Call the validation error handler Platform.throw(translated “{0} already exists in app {1}.”.format(self.file\_path, self.studio\_app)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1935)

<a id="op-b55052254dc90e"></a>
### Studio App File.on update

`operation_foundation_binding_foundation_studio_doctype_studio_app_file_studio_app_file_studioappfile_on_update`

**Inputs** self.

**Local steps**

- Evaluate publish\_doc\_change(“Studio App File”, self.file\_path, self.studio\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1933)

<a id="op-a0b104aad49314"></a>
### Studio App File.after delete

`operation_foundation_binding_foundation_studio_doctype_studio_app_file_studio_app_file_studioappfile_after_delete`

**Inputs** self.

**Local steps**

- Evaluate publish\_doc\_change(“Studio App File”, self.file\_path, self.studio\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1932)

<a id="op-8118a55cc2a2f7"></a>
### On doctype update

`operation_foundation_binding_foundation_studio_doctype_studio_app_file_studio_app_file_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Studio App File”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Studio App File”, tuple(“studio\_app”, “file\_path”), constraint\_name = “unique\_app\_file\_path”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1931)

## Record · Studio component

<a id="op-445be0c3d090e9"></a>
### Studio Component.autoname

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_autoname`

**Inputs** self.

**Local steps**

- If not self.component\_id.
  - Set self.component\_id from append\_number\_if\_name\_exists(“Studio Component”, Platform.scrub(self.component\_name), fieldname = “component\_id”, separator = “\_”, filters = mapping(“studio\_app” → (self.studio\_app or tuple(“is”, “not set”)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.studio\_app → tuple(“is”, “not set”).
- Evaluate validate\_component\_id(self.component\_id).
- Set self.name from get\_component\_name(self.component\_id, self.studio\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L5)

<a id="op-ffea1bcf9db737"></a>
### Studio Component.before export

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_before_export`

**Inputs** self, doc.

**Local steps**

- Set doc.block from parse\_json(doc.block).
- If doc.block.
  - Evaluate remove\_empty\_values(doc.block).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L6)

<a id="op-b891cecff0dd17"></a>
### Studio Component.before validate

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_before_validate`

**Inputs** self.

**Local steps**

- If isinstance(self.block, dict).
  - Set self.block from Platform.as\_json(self.block, indent = no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L8)

<a id="op-f59a88300a5b4b"></a>
### Studio Component.validate

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- Set self.component\_id from get\_component\_id(self.name).
- If not self.studio\_app.
  - Evaluate self.validate\_no\_app\_dependencies().
- Evaluate self.validate\_legacy\_inputs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate no app dependencies](operations-068.md#op-ebd2417f54d83d), [validate legacy inputs](operations-068.md#op-19361778d09ab8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L21)

<a id="op-19361778d09ab8"></a>
### Studio Component.validate legacy inputs

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_validate_legacy_inputs`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You cannot add or edit input rows. Define props in the component's script instead.”.

**Local steps**

- If (self.flags.is\_moved or any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.is\_moved → any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS).
  - Draw flag from SYNC\_FLAGS.
  - Return no value.
- Set before from self.get\_doc\_before\_save().
- Set saved\_rows from list of get\_input\_values(row) for row drawn from before.inputs when before, otherwise list().
  - Value choice on before — true gives list of get\_input\_values(row) for row drawn from before.inputs, false gives list().
  - Draw row from before.inputs.
- If any(generator of get\_input\_values(row) does not belong to saved\_rows for row drawn from self.inputs).
  - Draw row from self.inputs.
  - Call the validation error handler Platform.throw(translated “You cannot add or edit input rows. Define props in the component's script instead.”, title = translated “Input rows are deprecated”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L22)

<a id="op-ebd2417f54d83d"></a>
### Studio Component.validate no app dependencies

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_validate_no_app_dependencies`

**Inputs** self.

**State and service calls** msgprint with translated “This global component will not work in other apps. It uses {0} from this app. To keep it local to this app,  …”.format(“, ”.join(app\_components)).

**Explicit failure paths** validation helper — translated “A global component cannot import a file of one app: {0}. Import only libraries such as "vue", or edit the co …”.format(“, ”.join(imports)).

**Local steps**

- If imports bound to IMPORT\_RE.findall((self.script or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.script → empty text.
  - Call the validation error handler Platform.throw(translated “A global component cannot import a file of one app: {0}. Import only libraries such as "vue", or edit the co …”.format(“, ”.join(imports)), title = translated “Script not saved”).
- Set is\_edit from (self.has\_value\_changed(“block”) and not any(generator of nested operand in the contract.flags.get(flag) for flag drawn from SYNC\_FLAGS)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“block”) → not any(generator of Platform.flags.get(flag) for flag drawn from SYNC\_FLAGS).
  - Draw flag from SYNC\_FLAGS.
- If (is\_edit and app\_components bound to get\_app\_vue\_components(self.block)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_edit → app\_components bound to get\_app\_vue\_components(self.block).
  - Evaluate Platform.msgprint(translated “This global component will not work in other apps. It uses {0} from this app. To keep it local to this app,  …”.format(“, ”.join(app\_components)), title = translated “Global c ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L23)

<a id="op-a636c5b220fd66"></a>
### Studio Component.set app

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_set_app`

**Inputs** self, studio\_app = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Studio Component” via exists.

**State and service calls** request copy\_doc for self · call insert on moved.

**Explicit results** mapping(“name” → self.name, “is\_global\_kept” → false) · mapping(“name” → moved.name, “is\_global\_kept” → is\_global\_kept).

**Explicit failure paths** validation helper — translated “A global component with the ID {0} already exists.”.format(self.component\_id).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set studio\_app from (studio\_app or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in studio\_app → no value.
- If studio\_app equals (self.studio\_app or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.studio\_app → no value.
  - Return mapping(“name” → self.name, “is\_global\_kept” → false).
- If studio\_app.
  - Evaluate Platform.has\_permission(“Studio App”, ptype = “write”, doc = studio\_app, throw = true).
- Otherwise.
  - If Platform.db.exists(“Studio Component”, self.component\_id).
    - Call the validation error handler Platform.throw(translated “A global component with the ID {0} already exists.”.format(self.component\_id)).
- Set folders from self.get\_export\_folders().
- Set moved from Platform.copy\_doc(self).
- Set moved.studio\_app from studio\_app.
- Set moved.flags.is\_moved from true.
- Evaluate moved.insert().
- Set is\_global\_kept from (bool(studio\_app) and bool(self.get\_usages())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(studio\_app) → bool(self.get\_usages()).
- If not is\_global\_kept.
  - Set self.flags.is\_moved from true.
  - Evaluate self.delete().
- For each folder in folders when not studio\_app, otherwise moved.get\_export\_folders().
  - Value choice on not studio\_app — true gives folders, false gives moved.get\_export\_folders().
  - Evaluate moved.export\_to\_folder(folder).
- Return mapping(“name” → moved.name, “is\_global\_kept” → is\_global\_kept).

**Methods declared on this owner** [get export folders](operations-069.md#op-703c84698ad92d), [get usages](operations-068.md#op-3f5ef0ed6e9d5e).

**Values supplied outside this operation** effective access from self.check\_permission(“write”), Platform.has\_permission(“Studio App”, ptype = “write”, doc = studio\_app, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L20)

<a id="op-3f5ef0ed6e9d5e"></a>
### Studio Component.get usages

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_get_usages`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at (str bitwise or no value).

**Explicit results** usages.

**Local steps**

- Evaluate self.check\_permission(“read”).
- Set usages from list().
- For each tuple(doctype, title\_field, tree\_fields, label) in tuple(tuple(“Studio Component”, “component\_name”, list(“block”), translated “{0} (component)”), tuple(“Studio Page”, “page\_title”, list(“blocks”, “draft\_blocks”), translated “{0} (page)”)).
  - For each doc in self.get\_referencing\_docs(doctype, self.component\_id, list(title\_field, expanded tree\_fields)).
    - If any(generator of self.is\_in\_blocks(doc at field) for field drawn from tree\_fields).
      - Draw field from tree\_fields.
      - Set can\_read from Platform.has\_permission(doctype, “read”, doc = doc.name).
      - Evaluate usages.append(label.format(doc at title\_field) when can\_read, otherwise no value).
        - Value choice on can\_read — true gives label.format(doc at title\_field), false gives no value.
- Return usages.

**Methods declared on this owner** [get referencing docs](operations-069.md#op-bf1cf937a71246), [is in blocks](operations-068.md#op-a453e9b55bba4a).

**Values supplied outside this operation** effective access from self.check\_permission(“read”), Platform.has\_permission(doctype, “read”, doc = doc.name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L15)

<a id="op-a453e9b55bba4a"></a>
### Studio Component.is in blocks

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_is_in_blocks`

**Inputs** self, tree.

**Declared result** bool.

**Explicit results** (bool(tree) and self.component\_id belongs to extract\_component\_names(tree)).

**Local steps**

- Return (bool(tree) and self.component\_id belongs to extract\_component\_names(tree)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(tree) → self.component\_id belongs to extract\_component\_names(tree).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L16)

<a id="op-aebb23c28c7bd1"></a>
### Studio Component.validate not used

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_validate_not_used`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.LinkExistsError — translated “{0} is used in: {1}. Remove it from there first.”.format(self.component\_name, “, ”.join(titles)).

**Local steps**

- Set usages from self.get\_usages().
- Set titles from list of title for title drawn from usages where title.
  - Draw title from usages, keep a combination only if (title).
- If hidden bound to (len(usages) − len(titles)).
  - If titles.
    - Set text from translated “and {0} more that you cannot access”.
  - Otherwise.
    - If hidden equals 1.
      - Set text from translated “{0} place that you cannot access”.
    - Otherwise.
      - Set text from translated “{0} places that you cannot access”.
  - Evaluate titles.append(text.format(hidden)).
- If usages.
  - Call the validation error handler Platform.throw(translated “{0} is used in: {1}. Remove it from there first.”.format(self.component\_name, “, ”.join(titles)), title = translated “Component not deleted”, exc = Platform.LinkExistsError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get usages](operations-068.md#op-3f5ef0ed6e9d5e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L24)

<a id="op-021ff3c6dae83f"></a>
### Studio Component.before rename

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit results** mapping(“new” → get\_component\_name(component\_id, self.studio\_app)).

**Explicit failure paths** validation helper — translated “Components cannot be merged.” · validation helper — translated “A component cannot move to another app.”.

**Local steps**

- If merge.
  - Call the validation error handler Platform.throw(translated “Components cannot be merged.”).
- Evaluate validate\_standard\_app\_change(self).
- Set tuple(owner, \_separator, component\_id) from new.rpartition(“/”).
- If (owner and owner differs from self.studio\_app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in owner → owner differs from self.studio\_app.
  - Call the validation error handler Platform.throw(translated “A component cannot move to another app.”).
- Evaluate validate\_component\_id(component\_id).
- Return mapping(“new” → get\_component\_name(component\_id, self.studio\_app)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L7)

<a id="op-b3a3552c4baa95"></a>
### Studio Component.after rename

`operation_foundation_binding_foundation_studio_doctype_studio_component_studio_component_studiocomponent_after_rename`

**Inputs** self, old, new, merge = false.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- Set tuple(old\_id, new\_id) from tuple(get\_component\_id(old), get\_component\_id(new)).
- If old\_id equals new\_id.
  - Return no value.
- Set self.component\_id from old\_id.
- Set folders from self.get\_export\_folders().
- For each folder in folders.
  - Evaluate rename\_component\_files(folder, Platform.scrub(old\_id), Platform.scrub(new\_id)).
- Evaluate self.db\_set(“component\_id”, new\_id, update\_modified = false).
- For each folder in folders.
  - Evaluate self.export\_to\_folder(folder).
- Evaluate self.rename\_references(old\_id, new\_id).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export folders](operations-069.md#op-703c84698ad92d), [export to folder](operations-069.md#op-c8ae1aaecb186a), [rename references](operations-069.md#op-a015886e60bb69).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L4)
