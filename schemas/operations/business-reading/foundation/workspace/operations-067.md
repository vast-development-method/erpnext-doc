# Forms, reports and navigation · operations 67

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio app

<a id="op-92327e4f5188ea"></a>
### Studio App.delete app build

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_delete_app_build`

**Inputs** self.

**Local steps**

- If path bound to self.get\_build\_path().
  - Evaluate delete\_folder(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get build path](operations-067.md#op-b0485c1603437f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1951)

<a id="op-b0485c1603437f"></a>
### Studio App.get build path

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_build_path`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** os.path.abspath(get\_files\_path(“app\_builds”, self.name)) · no value · Platform.get\_app\_path(self.Platform\_app, “public”, “app\_builds”, self.name).

**Local steps**

- If not self.is\_standard.
  - Return os.path.abspath(get\_files\_path(“app\_builds”, self.name)).
- If not self.Platform\_app.
  - Return no value.
- Return Platform.get\_app\_path(self.Platform\_app, “public”, “app\_builds”, self.name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1962)

<a id="op-07ee31e5029037"></a>
### Studio App.before rename

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit failure paths** validation helper — translated “Exported apps can only be renamed in developer mode.” · validation helper — translated “Folder {0} already exists.”.format(self.get\_folder\_path(new)).

**Local steps**

- Evaluate validate\_app\_name(new).
- If (self.is\_standard and not can\_export(self)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → not can\_export(self).
  - Call the validation error handler Platform.throw(translated “Exported apps can only be renamed in developer mode.”).
- Set moves\_folder from Platform.scrub(old) differs from Platform.scrub(new).
- If (can\_export(self) and moves\_folder and os.path.exists(self.get\_folder\_path(new))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_export(self) → moves\_folder → os.path.exists(self.get\_folder\_path(new)).
  - Call the validation error handler Platform.throw(translated “Folder {0} already exists.”.format(self.get\_folder\_path(new))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1946)

<a id="op-aaff11ae23c194"></a>
### Studio App.after rename

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_after_rename`

**Inputs** self, old, new, merge = false.

**Record and data access** read “Studio Component” via get\_all · resolve a document from “Studio Component” via get\_doc.

**State and service calls** request rename\_doc for “Studio Component”.

**Explicit results** no value.

**Local steps**

- For each component in Platform.get\_all(“Studio Component”, filters = mapping(“studio\_app” → new), fields = list(“name”, “component\_id”)).
  - Evaluate Platform.rename\_doc(“Studio Component”, component.name, get\_component\_name(component.component\_id, new), force = true).
- If not can\_export(self).
  - Return no value.
- Evaluate move\_folder(self.get\_folder\_path(old), self.get\_folder\_path()).
- Set old\_file from os.path.join(self.get\_folder\_path(), formatted text {Platform.scrub(old)}.json).
- If os.path.exists(old\_file).
  - Evaluate os.replace(old\_file, get\_app\_file\_path(self.get\_folder\_path())).
- Evaluate self.export\_app().
- For each component in self.components.
  - Set doc from Platform.get\_doc(“Studio Component”, component).
  - For each folder in doc.get\_export\_folders().
    - Evaluate doc.export\_to\_folder(folder).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937), [export app](operations-067.md#op-5ca56915cdf791).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1943)

<a id="op-ff3ad5596f474a"></a>
### Studio App.move export to

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_move_export_to`

**Inputs** self, target\_app.

**Explicit failure paths** validation helper — translated “Folder {0} already exists.”.format(new\_path).

**Local steps**

- Set old\_path from self.get\_folder\_path().
- Set new\_path from self.get\_folder\_path(Platform\_app = target\_app).
- If os.path.exists(new\_path).
  - Call the validation error handler Platform.throw(translated “Folder {0} already exists.”.format(new\_path)).
- Evaluate move\_folder(old\_path, new\_path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1969)

<a id="op-c4c09bdc97e57a"></a>
### Studio App.generate app build

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_generate_app_build`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“build\_error” → no value) · mapping(“build\_error” → mapping(“error\_log” → error\_log.name)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to generate the app build”.

**Local steps**

- If not Platform.has\_permission(“Studio App”, ptype = “write”).
  - Call the validation error handler Platform.throw(translated “You do not have permission to generate the app build”, Platform.PermissionError).
- Attempt the following.
  - Evaluate self.build\_app\_bundle().
  - Return mapping(“build\_error” → no value).
- On failure (Exception) bound to e.
  - Set error\_log from Platform.log\_error(title = formatted text Studio app build failed: {self.name}, message = (getattr(e, “output”, no value) or Platform.get\_traceback())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(e, “output”, no value) → Platform.get\_traceback().
  - Return mapping(“build\_error” → mapping(“error\_log” → error\_log.name)).

**Methods declared on this owner** [build app bundle](operations-067.md#op-c551036fc0bcec).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio App”, ptype = “write”) · selected callable from getattr(e, “output”, no value).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1959)

<a id="op-c551036fc0bcec"></a>
### Studio App.build app bundle

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_build_app_bundle`

**Inputs** self.

**Local steps**

- Bind dependencies StudioAppBuilder.
- Evaluate StudioAppBuilder(studio\_app = self.name, is\_standard = self.is\_standard, Platform\_app = self.Platform\_app).build().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1947)

<a id="op-b3ec88504e2e9a"></a>
### Studio App.publish app

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_publish_app`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** mapping(“published\_pages” → len(pages), “unresolved\_variants” → unresolved\_variants, expand self.generate\_app\_build()).

**Local steps**

- Set pages from self.pages.
- Set unresolved\_variants from list().
- For each page in pages.
  - Set page\_doc from Platform.get\_doc(“Studio Page”, page).
  - Update unresolved\_variants using + page\_doc.publish() at “unresolved\_variants”.
- Return mapping(“published\_pages” → len(pages), “unresolved\_variants” → unresolved\_variants, expand self.generate\_app\_build()).

**Methods declared on this owner** [generate app build](operations-067.md#op-c4c09bdc97e57a).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1973)

<a id="op-93699c34670ce5"></a>
### Studio App.unpublish app

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_unpublish_app`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Local steps**

- For each page in self.pages.
  - Set page\_doc from Platform.get\_doc(“Studio Page”, page).
  - Evaluate page\_doc.unpublish().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1977)

<a id="op-56a86645043a74"></a>
### Studio App.get assets from manifest

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_assets_from_manifest`

**Inputs** self.

**Explicit results** no value · result.

**Local steps**

- Attempt the following.
  - If self.is\_standard.
    - Set base\_path from formatted text /assets/{self.Platform\_app}/app\_builds/{self.name}/.
  - Otherwise.
    - Set base\_path from formatted text /files/app\_builds/{self.name}/.
  - Set build\_path from self.get\_build\_path().
  - If not build\_path.
    - Return no value.
  - Set manifest\_path from os.path.join(build\_path, “.vite”, “manifest.json”).
  - If not os.path.exists(manifest\_path).
    - Return no value.
  - Within open(manifest\_path) bound as f.
    - Set manifest from json.load(f).
  - Set entry\_key from formatted text renderer-{self.name}.js.
  - Set entry\_key from next(generator of key for key drawn from manifest where key.endswith(entry\_key), entry\_key).
    - Draw key from manifest, keep a combination only if (key.endswith(entry\_key)).
  - Set entry from manifest at entry\_key.
  - Set result from mapping(“script” → formatted text {base\_path}{entry at “file”}, “stylesheets” → list of formatted text {base\_path}{css\_file} for css\_file drawn from entry.get(“css”, list())).
    - Draw css\_file from entry.get(“css”, list()).
  - For each tuple(chunk\_key, chunk\_data) in manifest.items().
    - If (chunk\_key differs from entry\_key and “css” belongs to chunk\_data).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in chunk\_key differs from entry\_key → “css” belongs to chunk\_data.
      - Evaluate result at “stylesheets”.extend(generator of formatted text {base\_path}{css\_file} for css\_file drawn from chunk\_data at “css”).
        - Draw css\_file from chunk\_data at “css”.
  - Return result.
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(formatted text Error reading manifest for app {self.name}: {e}).
  - Return no value.

**Methods declared on this owner** [get build path](operations-067.md#op-b0485c1603437f).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1960)

<a id="op-80c3a5e25dc294"></a>
### Studio App.enable app export

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_enable_app_export`

**Inputs** self, target\_app.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**State and service calls** request set\_value on “Studio Page” · call save on self.

**Local steps**

- Evaluate Platform.has\_permission(self.doctype, “write”, self.name, throw = true).
- Evaluate validate\_installed\_app(target\_app).
- If (self.is\_standard and self.Platform\_app and self.Platform\_app differs from target\_app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.Platform\_app → self.Platform\_app differs from target\_app.
  - Evaluate self.move\_export\_to(target\_app).
- Evaluate Platform.db.set\_value(“Studio Page”, mapping(“studio\_app” → self.name), mapping(“is\_standard” → 1, “Platform\_app” → target\_app)).
- Set self.is\_standard from 1.
- Set self.Platform\_app from target\_app.
- Evaluate self.save().
- For each page\_name in self.standard\_pages.
  - Evaluate Platform.get\_doc(“Studio Page”, page\_name).export\_script\_to\_file().
- Evaluate export\_db\_files\_to\_disk(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [move export to](operations-067.md#op-ff3ad5596f474a).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, self.name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1954)

<a id="op-4f6231821aacb4"></a>
### Studio App.get discarded export files

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_discarded_export_files`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** discarded\_export\_files(self).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Return discarded\_export\_files(self).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1964)

<a id="op-b9b957c7143763"></a>
### Studio App.disable app export

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_disable_app_export`

**Inputs** self, confirm\_discarded = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**State and service calls** request set\_value on “Studio Page” · call save on self.

**Explicit failure paths** validation helper — translated “The database cannot store these files, so they would be deleted with {0}: {1}”.format(self.get\_folder\_path(), “, ”.join(discarded)).

**Local steps**

- Set discarded from discarded\_export\_files(self).
- If (discarded and not sbool(confirm\_discarded)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in discarded → not sbool(confirm\_discarded).
  - Call the validation error handler Platform.throw(translated “The database cannot store these files, so they would be deleted with {0}: {1}”.format(self.get\_folder\_path(), “, ”.join(discarded))).
- For each page\_name in self.standard\_pages.
  - Evaluate Platform.get\_doc(“Studio Page”, page\_name).restore\_script\_from\_file().
- Evaluate restore\_db\_files\_from\_disk(self).
- Evaluate Platform.db.set\_value(“Studio Page”, mapping(“studio\_app” → self.name), “is\_standard”, 0).
- Set self.is\_standard from 0.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1953)

<a id="op-5ca56915cdf791"></a>
### Studio App.export app

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_export_app`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Platform App must be set to export the Studio App.”.

**Local steps**

- If not can\_export(self).
  - Return no value.
- If not self.Platform\_app.
  - Call the validation error handler Platform.throw(translated “Platform App must be set to export the Studio App.”).
- Set app\_path from self.create\_app\_folder().
- Evaluate self.export\_studio\_pages(app\_path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create app folder](operations-067.md#op-132e09314b2855), [export studio pages](operations-067.md#op-8ded7e86c03e8b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1955)

<a id="op-132e09314b2855"></a>
### Studio App.create app folder

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_create_app_folder`

**Inputs** self.

**Declared result** str.

**Explicit results** app\_path.

**Explicit failure paths** validation helper — translated “Folder {0} exists and is not a Studio app.”.format(app\_path).

**Local steps**

- Set app\_path from self.get\_folder\_path().
- If (os.path.isdir(app\_path) and not os.path.isfile(get\_app\_file\_path(app\_path))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isdir(app\_path) → not os.path.isfile(get\_app\_file\_path(app\_path)).
  - Call the validation error handler Platform.throw(translated “Folder {0} exists and is not a Studio app.”.format(app\_path)).
- Evaluate Platform.create\_folder(app\_path).
- Evaluate write\_document\_file(self, folder = app\_path).
- Evaluate self.write\_tsconfig(app\_path).
- Return app\_path.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937), [write tsconfig](operations-067.md#op-b0ee3cdf856beb).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1950)

<a id="op-b0ee3cdf856beb"></a>
### Studio App.write tsconfig

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_write_tsconfig`

**Inputs** self, app\_path.

**Declared result** no value.

**Local steps**

- Set tsconfig from mapping(“compilerOptions” → mapping(“baseUrl” → “.”, “paths” → mapping(“@app/\*” → list(“./\*”)), “allowJs” → true, “module” → “esnext”, …)).
- Within open(os.path.join(app\_path, “tsconfig.json”), “w”) bound as f.
  - Evaluate f.write(json.dumps(tsconfig, indent = whitespace '\\t')).
  - Evaluate f.write(whitespace '\\n').

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1981)

<a id="op-8ded7e86c03e8b"></a>
### Studio App.export studio pages

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_export_studio_pages`

**Inputs** self, app\_path.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Local steps**

- Set page\_folder\_path from os.path.join(app\_path, “studio\_page”).
- Evaluate Platform.create\_folder(page\_folder\_path).
- For each page in self.pages.
  - Set page\_doc from Platform.get\_doc(“Studio Page”, page).
  - Evaluate page\_doc.export\_page().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1956)

<a id="op-a34343c1d60dd2"></a>
### Studio App.collect files

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_collect_files`

**Inputs** self, script, script\_dir, blocks.

**Declared result** list at dict.

**Explicit results** list of mapping(“path” → path, “content” → files at path) for path drawn from sorted(files).

**Local steps**

- If self.is\_standard.
  - Set read from self.read\_exported\_file.
  - Set pending from list of path for name drawn from custom\_vue\_component\_names(blocks) where path bound to self.find\_vue\_component(name).
    - Draw name from custom\_vue\_component\_names(blocks), keep a combination only if (path bound to self.find\_vue\_component(name)).
- Otherwise.
  - Set stored from mapping of file at “path” → file at “content” for file drawn from get\_db\_files(self.name).
    - Draw file from get\_db\_files(self.name).
  - Set read from stored.get.
  - Set pending from list().
- Set files from mapping().
- Update pending using + resolve\_imports(script, script\_dir, read).
- While pending.
  - Set path from pending.pop().
  - If path belongs to files.
    - Continue with the next iteration or loop test.
  - Set files at path from read(path).
  - Update pending using + resolve\_imports(files at path, os.path.dirname(path), read).
- Return list of mapping(“path” → path, “content” → files at path) for path drawn from sorted(files).
  - Draw path from sorted(files).

**Methods declared on this owner** [find vue component](operations-067.md#op-47fe0c60d99482).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1948)

<a id="op-d675ecfca5b475"></a>
### Studio App.read exported file

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_read_exported_file`

**Inputs** self, path.

**Declared result** (str bitwise or no value).

**Explicit results** no value · f.read().

**Local steps**

- Set target from self.resolve\_file\_path(path).
- If not os.path.isfile(target).
  - Return no value.
- Within open(target, encoding = “utf-8”) bound as f.
  - Return f.read().

If control reaches the end, it returns no value.

**Methods declared on this owner** [resolve file path](operations-067.md#op-170100cb46deb9).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L80) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1974)

<a id="op-3747bbb7c6eea3"></a>
### Studio App.write files

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_write_files`

**Inputs** self, files.

**Local steps**

- If not self.is\_standard.
  - Evaluate write\_db\_files(self.name, files).
- Otherwise.
  - If can\_export(self).
    - Evaluate self.write\_exported\_files(files).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write exported files](operations-067.md#op-e1cba30887b00f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1980)

<a id="op-e1cba30887b00f"></a>
### Studio App.write exported files

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_write_exported_files`

**Inputs** self, files.

**Explicit failure paths** validation helper — translated “Invalid copied file.” · validation helper — translated “Unsupported copied file: {0}”.format(path) · validation helper — translated “The copy contains conflicting versions of {0}.”.format(path) · validation helper — translated “{0} already exists with different content. Rename it before pasting.”.format(file at “path”).

**Local steps**

- Set targets from mapping().
- For each file in files.
  - If (not isinstance(file, dict) or not isinstance(file.get(“path”), str) or not isinstance(file.get(“content”), str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(file, dict) → not isinstance(file.get(“path”), str) → not isinstance(file.get(“content”), str).
    - Call the validation error handler Platform.throw(translated “Invalid copied file.”).
  - Set path from file at “path”.
  - Set target from self.resolve\_file\_path(path).
  - If not target.lower().endswith(EXTENSIONS).
    - Call the validation error handler Platform.throw(translated “Unsupported copied file: {0}”.format(path)).
  - If (target belongs to targets and targets at target at “content” differs from file at “content”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in target belongs to targets → targets at target at “content” differs from file at “content”.
    - Call the validation error handler Platform.throw(translated “The copy contains conflicting versions of {0}.”.format(path)).
  - Set targets at target from file.
- For each tuple(target, file) in targets.items().
  - If not os.path.exists(target).
    - Continue with the next iteration or loop test.
  - If (os.path.isfile(target) and Platform.read\_file(target) equals file at “content”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isfile(target) → Platform.read\_file(target) equals file at “content”.
    - Continue with the next iteration or loop test.
  - Call the validation error handler Platform.throw(translated “{0} already exists with different content. Rename it before pasting.”.format(file at “path”), title = translated “File conflict”).
- For each tuple(target, file) in targets.items().
  - If os.path.exists(target).
    - Continue with the next iteration or loop test.
  - Evaluate os.makedirs(os.path.dirname(target), exist\_ok = true).
  - Within open(target, “x”, encoding = “utf-8”) bound as f.
    - Evaluate f.write(file at “content”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [resolve file path](operations-067.md#op-170100cb46deb9).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L85) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1979)

<a id="op-47fe0c60d99482"></a>
### Studio App.find vue component

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_find_vue_component`

**Inputs** self, name.

**Declared result** (str bitwise or no value).

**Explicit results** matches at 0 when matches, otherwise no value.

**Explicit failure paths** validation helper — translated “Custom component {0} is ambiguous: {1}”.format(name, “, ”.join(sorted(matches))).

**Local steps**

- Set matches from list().
- For each tuple(dirpath, \_dirnames, filenames) in os.walk(self.get\_folder\_path()).
  - If formatted text {name}.vue belongs to filenames.
    - Evaluate matches.append(os.path.relpath(os.path.join(dirpath, formatted text {name}.vue), self.get\_folder\_path())).
- If len(matches) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Custom component {0} is ambiguous: {1}”.format(name, “, ”.join(sorted(matches))), title = translated “Duplicate component name”).
- Return matches at 0 when matches, otherwise no value.
  - Value choice on matches — true gives matches at 0, false gives no value.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1957)

<a id="op-170100cb46deb9"></a>
### Studio App.resolve file path

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_resolve_file_path`

**Inputs** self, path.

**Declared result** str.

**Explicit results** target.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid file path: {0}”.format(path).

**Local steps**

- Set root from os.path.realpath(self.get\_folder\_path()).
- Set target from os.path.realpath(os.path.join(root, path)).
- If (target equals root or not target.startswith((root + os.sep))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target equals root → not target.startswith((root + os.sep)).
  - Call the validation error handler Platform.throw(translated “Invalid file path: {0}”.format(path), Platform.PermissionError).
- Return target.

**Methods declared on this owner** [get folder path](operations-067.md#op-ca6b619b68c937).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L81) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1975)

<a id="op-ca6b619b68c937"></a>
### Studio App.get folder path

`operation_foundation_binding_foundation_studio_doctype_studio_app_studio_app_studioapp_get_folder_path`

**Inputs** self, name = no value, Platform\_app = no value.

**Explicit results** get\_export\_folder((Platform\_app or self.Platform\_app), (name or self.name)).

**Local steps**

- Return get\_export\_folder((Platform\_app or self.Platform\_app), (name or self.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform\_app → self.Platform\_app.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → self.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1965)
