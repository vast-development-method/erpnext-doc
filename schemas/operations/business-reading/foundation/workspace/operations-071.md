# Forms, reports and navigation · operations 71

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio page

<a id="op-1d919c1c2f452e"></a>
### Studio Page.after insert

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_after_insert`

**Inputs** self.

**Record and data access** read “Studio App” via get\_value.

**State and service calls** request set\_value on “Studio App”.

**Local steps**

- Set app\_home from Platform.db.get\_value(“Studio App”, self.studio\_app, “app\_home”).
- If not app\_home.
  - Evaluate Platform.db.set\_value(“Studio App”, self.studio\_app, “app\_home”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2079) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L56)

<a id="op-ae9c57c88a2a16"></a>
### Studio Page.before validate

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_before_validate`

**Inputs** self.

**Local steps**

- If isinstance(self.blocks, list).
  - Set self.blocks from Platform.as\_json(self.blocks, indent = no value).
- If isinstance(self.draft\_blocks, list).
  - Set self.draft\_blocks from Platform.as\_json(self.draft\_blocks, indent = no value).
- If not self.route.startswith(“/”).
  - Set self.route from formatted text /{self.route}.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2084) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L61)

<a id="op-0ad3fc7afd6d7d"></a>
### Studio Page.validate

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- Evaluate self.validate\_page\_title().
- If self.has\_value\_changed(“page\_title”).
  - Evaluate self.validate\_export\_stem\_is\_free().
- If self.has\_value\_changed(“route”).
  - Evaluate self.validate\_route\_is\_free().
- If not hasattr(self, “\_skip\_validate”).
  - Evaluate self.validate\_variables().
  - Evaluate self.process\_resources().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate page title](operations-071.md#op-408d8171290bd7), [validate export stem is free](operations-072.md#op-e38fb11c6f7679), [validate route is free](operations-072.md#op-eb97fbb497f529), [validate variables](operations-071.md#op-f27e4a7b959026), [process resources](operations-071.md#op-5b6d25cc4aeae5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L199) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L6) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L94)

<a id="op-408d8171290bd7"></a>
### Studio Page.validate page title

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate_page_title`

**Inputs** self.

**Local steps**

- Evaluate validate\_file\_name(self.get\_export\_docname(), translated “Page Title cannot be empty or contain slashes.”, title = translated “Invalid Page Title”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L201) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L8) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L96)

<a id="op-a48992fe6e9912"></a>
### Studio Page.on update

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_page().
- Evaluate publish\_doc\_change(“Studio Page”, self.name, self.studio\_app).

If control reaches the end, it returns no value.

**Methods declared on this owner** [export page](operations-071.md#op-bc1e18e86b51aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L83)

<a id="op-bc1e18e86b51aa"></a>
### Studio Page.export page

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_export_page`

**Inputs** self.

**Local steps**

- If can\_export(self).
  - Evaluate Platform.create\_folder(self.get\_folder\_path()).
  - Evaluate write\_document\_file(self, folder = self.get\_folder\_path(), exclude\_fields = list(“script”)).
  - Evaluate self.relocate\_on\_retitle().
  - Evaluate self.export\_components().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-072.md#op-ea22ff6e7eb61a), [relocate on retitle](operations-071.md#op-d1cd6604d32daa), [export components](operations-072.md#op-5acab0732969d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2088) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L65)

<a id="op-ce11c258037c5b"></a>
### Studio Page.export script to file

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_export_script_to_file`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If not self.script.
  - Return no value.
- If os.path.exists(self.get\_script\_file\_path()).
  - Evaluate self.db\_set(“script”, no value, update\_modified = false).
- Otherwise.
  - Evaluate self.write\_script\_file(default\_extension = “js”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get script file path](operations-072.md#op-6c18d6264ab7ff), [write script file](operations-071.md#op-4f7780c4e12299).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2089) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L66)

<a id="op-4f7780c4e12299"></a>
### Studio Page.write script file

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_write_script_file`

**Inputs** self, default\_extension = “ts”.

**State and service calls** call db\_set on self.

**Local steps**

- If self.script.
  - Set folder from self.get\_folder\_path().
  - Set stem from self.get\_export\_docname().
  - Set extension from script\_extension(folder, stem, default\_extension).
  - Evaluate validate\_one\_script\_file(folder, formatted text {stem}.{extension}).
  - Evaluate Platform.create\_folder(folder).
  - Evaluate write\_code\_file(self, folder, code\_field = “script”, extension = extension, filename = stem).
- Otherwise.
  - Evaluate delete\_file(self.get\_script\_file\_path()).
- Evaluate self.db\_set(“script”, no value, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-072.md#op-ea22ff6e7eb61a), [get export docname](operations-072.md#op-8df8e34c595ac8), [get script file path](operations-072.md#op-6c18d6264ab7ff).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L205) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L12) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L100)

<a id="op-e089fe657e4ca8"></a>
### Studio Page.restore script from file

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_restore_script_from_file`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.has\_script\_file().
  - Evaluate self.db\_set(“script”, Platform.read\_file(self.get\_script\_file\_path()), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has script file](operations-071.md#op-febad913356d83), [get script file path](operations-072.md#op-6c18d6264ab7ff).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L88)

<a id="op-9b1298a80b53d7"></a>
### Studio Page.get copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_copy`

**Inputs** self, blocks = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(expand self.get\_dependencies(blocks, script), “page\_title” → self.page\_title, “tab\_title” → self.tab\_title, “allow\_guest” → self.allow\_guest, …).

**Local steps**

- Evaluate self.check\_permission(“read”).
- Set blocks from parse\_list(blocks when blocks is distinct from no value, otherwise (self.draft\_blocks or self.blocks), “blocks”).
  - Value choice on blocks is distinct from no value — true gives blocks, false gives (self.draft\_blocks or self.blocks).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.draft\_blocks → self.blocks.
- Set script from self.get\_script\_source().
- Return mapping(expand self.get\_dependencies(blocks, script), “page\_title” → self.page\_title, “tab\_title” → self.tab\_title, “allow\_guest” → self.allow\_guest, …).
  - Draw row from self.resources.
  - Draw row from self.variables.

**Methods declared on this owner** [get script source](operations-071.md#op-6584302c883016), [get dependencies](operations-071.md#op-c713e3a21ee111).

**Values supplied outside this operation** effective access from self.check\_permission(“read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2094) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L71)

<a id="op-c713e3a21ee111"></a>
### Studio Page.get dependencies

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_dependencies`

**Inputs** self, blocks, script = empty text.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“components” → get\_components\_for\_blocks(blocks, self.studio\_app), “files” → self.get\_app\_files(script, blocks), “resources” → list of pick(r, PAGE\_RESOURCE\_FIELDS) for r drawn from self.resources  ….

**Local steps**

- Evaluate self.check\_permission(“read”).
- Set blocks from parse\_list(blocks, “blocks”).
- Set text from Platform.as\_json(blocks).
- Bind local operation used for subsequent calls.
- Return mapping(“components” → get\_components\_for\_blocks(blocks, self.studio\_app), “files” → self.get\_app\_files(script, blocks), “resources” → list of pick(r, PAGE\_RESOURCE\_FIELDS) for r drawn from self.resources  ….
  - Draw r from self.resources, keep a combination only if (used(r.resource\_name)).
  - Draw v from self.variables, keep a combination only if (used(v.variable\_name)).

**Methods declared on this owner** [get app files](operations-071.md#op-4f74b006c0e25f).

**Values supplied outside this operation** effective access from self.check\_permission(“read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2095) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L72)

<a id="op-57537f7707dbb7"></a>
### Studio Page.get dependencies.used

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_dependencies_used`

**Inputs** name.

**Explicit results** (bool(name) and re.search(formatted text \\b{re.escape(name)}\\b, text)).

**Local steps**

- Return (bool(name) and re.search(formatted text \\b{re.escape(name)}\\b, text)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(name) → re.search(formatted text \\b{re.escape(name)}\\b, text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2096) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L73)

<a id="op-4f74b006c0e25f"></a>
### Studio Page.get app files

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_app_files`

**Inputs** self, script, blocks.

**Declared result** list at dict.

**Explicit results** app.collect\_files(script, script\_dir, blocks).

**Local steps**

- Set app from self.get\_app().
- Set script\_dir from formatted text studio\_page/{self.get\_export\_docname()}.
- Return app.collect\_files(script, script\_dir, blocks).

**Methods declared on this owner** [get app](operations-071.md#op-ca15ccea55473f), [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2091) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L68)

<a id="op-ca15ccea55473f"></a>
### Studio Page.get app

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_app`

**Inputs** self.

**Record and data access** resolve a document from “Studio App” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Studio App”, self.studio\_app).

**Local steps**

- Return Platform.get\_cached\_doc(“Studio App”, self.studio\_app).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Studio App”, self.studio\_app).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2090) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L67)

<a id="op-6584302c883016"></a>
### Studio Page.get script source

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_script_source`

**Inputs** self.

**Declared result** str.

**Explicit results** Platform.read\_file(self.get\_script\_file\_path()) · (self.script or empty text).

**Local steps**

- If self.has\_script\_file().
  - Return Platform.read\_file(self.get\_script\_file\_path()).
- Return (self.script or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.script → empty text.

**Methods declared on this owner** [has script file](operations-071.md#op-febad913356d83), [get script file path](operations-072.md#op-6c18d6264ab7ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L78)

<a id="op-febad913356d83"></a>
### Studio Page.has script file

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_has_script_file`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((self.is\_standard and self.Platform\_app and os.path.exists(self.get\_script\_file\_path()))).

**Local steps**

- Return bool((self.is\_standard and self.Platform\_app and os.path.exists(self.get\_script\_file\_path()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.Platform\_app → os.path.exists(self.get\_script\_file\_path()).

**Methods declared on this owner** [get script file path](operations-072.md#op-6c18d6264ab7ff).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L81)

<a id="op-d1cd6604d32daa"></a>
### Studio Page.relocate on retitle

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_relocate_on_retitle`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_value\_changed(“page\_title”).
  - Return no value.
- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- Set old\_stem from Platform.scrub(doc\_before\_save.page\_title).
- Set old\_folder from os.path.join(get\_export\_folder(self.Platform\_app, self.studio\_app), “studio\_page”, old\_stem).
- If old\_folder equals self.get\_folder\_path().
  - Return no value.
- Set old\_page\_script from find\_script\_file(old\_folder, old\_stem).
- If os.path.exists(old\_page\_script).
  - Set extension from os.path.splitext(old\_page\_script) at 1.
  - Set new\_name from (self.get\_export\_docname() + extension).
  - Evaluate os.rename(old\_page\_script, os.path.join(self.get\_folder\_path(), new\_name)).
- Evaluate delete\_folder(old\_folder).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-072.md#op-ea22ff6e7eb61a), [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L87)

<a id="op-98793a9d8b596d"></a>
### Studio Page.has blocks

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_has_blocks`

**Inputs** self, check\_draft = false.

**Explicit results** true · false.

**Local steps**

- If check\_draft.
  - If (self.draft\_blocks and self.draft\_blocks differs from “&#91;&#93;”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.draft\_blocks → self.draft\_blocks differs from “&#91;&#93;”.
    - Return true.
- Otherwise.
  - If (self.blocks and self.blocks differs from “&#91;&#93;”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.blocks → self.blocks differs from “&#91;&#93;”.
    - Return true.
- Return false.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L80)

<a id="op-95154c313403ec"></a>
### Studio Page.on trash

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_on_trash`

**Inputs** self.

**Local steps**

- Evaluate validate\_standard\_app\_change(self).
- Evaluate self.delete\_ai\_sessions().
- If can\_export(self).
  - Evaluate delete\_folder(self.get\_folder\_path()).
  - Evaluate self.delete\_unused\_component\_files(deleting = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete ai sessions](operations-071.md#op-ef7231474a6102), [get folder path](operations-072.md#op-ea22ff6e7eb61a), [delete unused component files](operations-072.md#op-2d712e2359e9c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L82)

<a id="op-ef7231474a6102"></a>
### Studio Page.delete ai sessions

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_delete_ai_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2085) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L62)

<a id="op-f27e4a7b959026"></a>
### Studio Page.validate variables

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate_variables`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Duplicate variable name: {0}”.format(“, ”.join(duplicate\_variable\_names)) · validation helper — translated “Invalid variable name '{0}' — use letters, digits and underscores, starting with a letter.”.format(variable.variable\_name).

**Local steps**

- Set variable\_names from list of variable.variable\_name for variable drawn from self.variables.
  - Draw variable from self.variables.
- Set duplicate\_variable\_names from set(generator of x for x drawn from variable\_names where variable\_names.count(x) &gt; 1).
  - Draw x from variable\_names, keep a combination only if (variable\_names.count(x) &gt; 1).
- If duplicate\_variable\_names.
  - Call the validation error handler Platform.throw(translated “Duplicate variable name: {0}”.format(“, ”.join(duplicate\_variable\_names))).
- For each variable in self.variables.
  - If not VARIABLE\_NAME\_REGEX.match((variable.variable\_name or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in variable.variable\_name → empty text.
    - Call the validation error handler Platform.throw(translated “Invalid variable name '{0}' — use letters, digits and underscores, starting with a letter.”.format(variable.variable\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L204) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L11) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L99)

<a id="op-5b6d25cc4aeae5"></a>
### Studio Page.process resources

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_process_resources`

**Inputs** self.

**Local steps**

- For each resource in self.resources.
  - Evaluate self.validate\_resources(resource).
  - Evaluate self.set\_resource\_json\_fields(resource).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate resources](operations-071.md#op-eb2e37271b26fd), [set resource json fields](operations-071.md#op-1bb35215631fd0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L84)

<a id="op-eb2e37271b26fd"></a>
### Studio Page.validate resources

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate_resources`

**Inputs** self, resource.

**Explicit failure paths** validation helper — translated “Please set API URL for Data Source {0}”.format(resource.name) · validation helper — translated “Please set Document Type for Data Source {0}”.format(resource.name) · validation helper — translated “Please set fields to fetch for Data Source {0}”.format(resource.name) · validation helper — translated “Please set filters to fetch the Data Source {0}”.format(resource.name) · validation helper — translated “Please set the document name to fetch the Data Source {0}”.format(resource.name).

**Local steps**

- If (resource.resource\_type equals “API Resource” and not resource.url).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in resource.resource\_type equals “API Resource” → not resource.url.
  - Call the validation error handler Platform.throw(translated “Please set API URL for Data Source {0}”.format(resource.name)).
- Otherwise.
  - If (resource.resource\_type belongs to list(“Document”, “Document List”) and not resource.document\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in resource.resource\_type belongs to list(“Document”, “Document List”) → not resource.document\_type.
    - Call the validation error handler Platform.throw(translated “Please set Document Type for Data Source {0}”.format(resource.name)).
  - If (resource.resource\_type equals “Document List” and not resource.fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in resource.resource\_type equals “Document List” → not resource.fields.
    - Call the validation error handler Platform.throw(translated “Please set fields to fetch for Data Source {0}”.format(resource.name)).
  - If resource.resource\_type equals “Document”.
    - If resource.fetch\_document\_using\_filters.
      - If not resource.filters.
        - Call the validation error handler Platform.throw(translated “Please set filters to fetch the Data Source {0}”.format(resource.name)).
      - Set resource.document\_name from empty text.
    - Otherwise.
      - If not resource.document\_name.
        - Call the validation error handler Platform.throw(translated “Please set the document name to fetch the Data Source {0}”.format(resource.name)).
      - Set resource.filters from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L202) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L9) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L97)

<a id="op-1bb35215631fd0"></a>
### Studio Page.set resource json fields

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_set_resource_json_fields`

**Inputs** self, resource.

**Local steps**

- If isinstance(resource.fields, list).
  - Set resource.fields from Platform.as\_json(resource.fields, indent = no value).
- If isinstance(resource.filters, list).
  - Set resource.filters from Platform.as\_json(resource.filters, indent = no value).
- If isinstance(resource.whitelisted\_methods, list).
  - Set resource.whitelisted\_methods from Platform.as\_json(resource.whitelisted\_methods, indent = no value).
- If isinstance(resource.params, list).
  - Set resource.params from Platform.as\_json(resource.params, indent = no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L197) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L4) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L92)
