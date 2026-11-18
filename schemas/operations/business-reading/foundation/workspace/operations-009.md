# Forms, reports and navigation · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Build

<a id="op-9038897be65f22"></a>
### Studio App Builder.write page sources

`operation_foundation_binding_foundation_studio_build_studioappbuilder_write_page_sources`

**Inputs** self.

**Explicit results** page\_sources.

**Local steps**

- Set page\_sources from tempfile.NamedTemporaryFile(“w”, suffix = “.txt”).
- Evaluate page\_sources.write(whitespace '\\n'.join(self.page\_sources)).
- Evaluate page\_sources.flush().
- Return page\_sources.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1921)

<a id="op-fd5a15be779992"></a>
### Studio App Builder.get app folder

`operation_foundation_binding_foundation_studio_build_studioappbuilder_get_app_folder`

**Inputs** self.

**Declared result** str.

**Explicit results** get\_export\_folder(self.Platform\_app, self.app\_name).

**Local steps**

- Return get\_export\_folder(self.Platform\_app, self.app\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1915)

<a id="op-418dbc74c6bf11"></a>
### Studio App Builder.validate components resolved

`operation_foundation_binding_foundation_studio_build_studioappbuilder_validate_components_resolved`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** StudioAppBuildError(formatted text Components used by '{self.app\_name}' are missing from its export: {names}, formatted text Looked under {self.app\_folder}. Export them with the app, or drop the blocks using them.).

**Local steps**

- If not self.missing\_components.
  - Return no value.
- Set names from “, ”.join(sorted(self.missing\_components)).
- Raise StudioAppBuildError(formatted text Components used by '{self.app\_name}' are missing from its export: {names}, formatted text Looked under {self.app\_folder}. Export them with the app, or drop the blocks using them.).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1920)

<a id="op-08abc1f8b5d8cf"></a>
### Studio App Builder.get page scripts from files

`operation_foundation_binding_foundation_studio_build_studioappbuilder_get_page_scripts_from_files`

**Inputs** self.

**Explicit results** no value · scripts.

**Local steps**

- Set page\_folder from os.path.join(self.app\_folder, “studio\_page”).
- If not os.path.isdir(page\_folder).
  - Return no value.
- Set scripts from list().
- For each entry in sorted(os.listdir(page\_folder)).
  - Set page\_dir from os.path.join(page\_folder, entry).
  - If not os.path.isdir(page\_dir).
    - Continue with the next iteration or loop test.
  - Set script\_path from find\_script\_file(page\_dir, entry).
  - Set json\_path from os.path.join(page\_dir, formatted text {entry}.json).
  - If not (os.path.exists(script\_path) and os.path.exists(json\_path)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(script\_path) → os.path.exists(json\_path).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Within open(json\_path) bound as f.
      - Set page\_data from json.load(f).
  - On failure (tuple(OSError, json.JSONDecodeError)).
    - Continue with the next iteration or loop test.
  - If (page\_data.get(“published”) and page\_data.get(“page\_name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in page\_data.get(“published”) → page\_data.get(“page\_name”).
    - Evaluate scripts.append(mapping(“page\_name” → page\_data at “page\_name”, “file\_path” → script\_path)).
- Set self.page\_scripts from scripts.
- Return scripts.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1916)

<a id="op-0919ec1e9c7df0"></a>
### Studio App Builder.run vite build

`operation_foundation_binding_foundation_studio_build_studioappbuilder_run_vite_build`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** no value.

**Locally raised failures** StudioAppBuildError.

**Local structure** 11 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1919)

<a id="op-0718e8fb8b335d"></a>
### Studio App Builder.get app components

`operation_foundation_binding_foundation_studio_build_studioappbuilder_get_app_components`

**Inputs** self.

**Declared result** set at str.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** set().

**Local steps**

- Set pages from Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.app\_name, “published” → 1, “blocks” → tuple(“is”, “set”)), fields = list(“blocks”, “script”)).
- If not pages.
  - Return set().
- For each page in pages.
  - Evaluate self.\_add\_icons(page.script).
  - Evaluate self.\_add\_page\_source(page.script).
  - Evaluate self.\_add\_page\_source(page.blocks).
  - Set blocks from page.blocks.
  - If not blocks.
    - Continue with the next iteration or loop test.
  - Evaluate self.\_add\_icons(blocks when isinstance(blocks, str), otherwise no value).
    - Value choice on isinstance(blocks, str) — true gives blocks, false gives no value.
  - If isinstance(blocks, str).
    - Evaluate self.\_add\_h\_function\_components(blocks).
    - Set blocks from Platform.parse\_json(blocks).
  - If not blocks.
    - Continue with the next iteration or loop test.
  - Set root\_block from blocks at 0.
  - Evaluate self.\_add\_block\_components(root\_block).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add icons](operations-009.md#op-1321388cd708ac), [add page source](operations-009.md#op-087eb128ecfc20), [add h function components](operations-009.md#op-4b0ffd103907fa), [add block components](operations-009.md#op-58d65897072e2c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1913)

<a id="op-655d16b224411a"></a>
### Studio App Builder.get app components from files

`operation_foundation_binding_foundation_studio_build_studioappbuilder_get_app_components_from_files`

**Inputs** self.

**Explicit results** self.components.

**Local steps**

- Set app\_folder, self.app\_folder from (self.app\_folder or self.get\_app\_folder()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.app\_folder → self.get\_app\_folder().
- Set page\_folder from os.path.join(app\_folder, “studio\_page”).
- If not os.path.exists(page\_folder).
  - Return self.components.
- Evaluate self.\_load\_studio\_components\_from\_files(app\_folder).
- For each entry in os.listdir(page\_folder).
  - Set page\_dir from os.path.join(page\_folder, entry).
  - If not os.path.isdir(page\_dir).
    - Continue with the next iteration or loop test.
  - Set page\_path from os.path.join(page\_dir, formatted text {entry}.json).
  - If not os.path.exists(page\_path).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Within open(page\_path) bound as f.
      - Set page\_text from f.read().
    - Set page\_data from json.loads(page\_text).
  - On failure (tuple(json.JSONDecodeError, OSError)) bound to e.
    - Evaluate click.secho(formatted text Warning: Could not read {page\_path}: {e}, fg = “yellow”).
    - Continue with the next iteration or loop test.
  - If not page\_data.get(“published”).
    - Continue with the next iteration or loop test.
  - Evaluate self.\_add\_icons(page\_text).
  - Evaluate self.\_add\_h\_function\_components(page\_text).
  - Set blocks from page\_data.get(“blocks”).
  - If not blocks.
    - Continue with the next iteration or loop test.
  - If isinstance(blocks, str).
    - Set blocks from json.loads(blocks).
  - If (isinstance(blocks, list) and blocks).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(blocks, list) → blocks.
    - Evaluate self.\_add\_block\_components(blocks at 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get app folder](operations-009.md#op-fd5a15be779992), [load studio components from files](operations-009.md#op-16558d999325f4), [add icons](operations-009.md#op-1321388cd708ac), [add h function components](operations-009.md#op-4b0ffd103907fa), [add block components](operations-009.md#op-58d65897072e2c).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1914)

<a id="op-1321388cd708ac"></a>
### Studio App Builder.add icons

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_icons`

**Inputs** self, text.

**Declared result** no value.

**Local steps**

- Evaluate self.icons.update(LUCIDE\_ICON\_REGEX.findall((text or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1909)

<a id="op-4b0ffd103907fa"></a>
### Studio App Builder.add h function components

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_h_function_components`

**Inputs** self, text.

**Declared result** no value.

**Local steps**

- Set pattern from “\\bh\\(\\s\*(&#91;A-Z&#93;&#91;a-zA-Z0-9\_&#93;\*)”.
- Set matches from re.findall(pattern, text).
- For each match in matches.
  - Evaluate self.components.add(match).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1908)

<a id="op-58d65897072e2c"></a>
### Studio App Builder.add block components

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_block_components`

**Inputs** self, blocks.

**Declared result** no value.

**Local steps**

- For each block in walk\_blocks(blocks).
  - If block.get(“isStudioComponent”).
    - Evaluate self.\_add\_studio\_components(block).
  - Otherwise.
    - If block.get(“isCustomVueComponent”).
      - Evaluate self.\_add\_custom\_vue\_component(block.get(“componentName”)).
    - Otherwise.
      - If is\_vue\_component(block.get(“componentName”)).
        - Evaluate self.components.add(block.get(“componentName”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add studio components](operations-009.md#op-5a34022ec35c64), [add custom vue component](operations-009.md#op-7dcc08a9c5c912).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1905)

<a id="op-5a34022ec35c64"></a>
### Studio App Builder.add studio components

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_studio_components`

**Inputs** self, block.

**Record and data access** read “Studio Component” via get\_value.

**Local steps**

- If self.is\_standard.
  - Set comp\_name from block.get(“componentName”).
  - If (comp\_name and comp\_name belongs to self.studio\_component\_blocks).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in comp\_name → comp\_name belongs to self.studio\_component\_blocks.
    - Evaluate self.\_add\_block\_components(self.studio\_component\_blocks at comp\_name).
  - Otherwise.
    - If comp\_name.
      - Evaluate self.missing\_components.add(comp\_name).
- Otherwise.
  - Set name from block.get(“componentName”).
  - Set tuple(component\_block, script) from (Platform.db.get\_value(“Studio Component”, find\_component(name, self.app\_name), list(“block”, “script”)) or tuple(no value, no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Studio Component”, find\_component(name, self.app\_name), list(“block”, “script”)) → tuple(no value, no value).
  - Evaluate self.\_add\_icons(component\_block when isinstance(component\_block, str), otherwise no value).
    - Value choice on isinstance(component\_block, str) — true gives component\_block, false gives no value.
  - Evaluate self.\_add\_page\_source(component\_block).
  - Evaluate self.\_add\_component\_script(name, script).
  - If isinstance(component\_block, str).
    - Set component\_block from Platform.parse\_json(component\_block).
  - Evaluate self.\_add\_block\_components(component\_block).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add block components](operations-009.md#op-58d65897072e2c), [add icons](operations-009.md#op-1321388cd708ac), [add page source](operations-009.md#op-087eb128ecfc20), [add component script](operations-009.md#op-17aabffde65879).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1911)

<a id="op-17aabffde65879"></a>
### Studio App Builder.add component script

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_component_script`

**Inputs** self, name, script.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (not script or name belongs to self.component\_scripts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not script → name belongs to self.component\_scripts.
  - Return no value.
- Set path from os.path.join(self.app\_folder, “studio\_components”, formatted text {name}.js).
- Evaluate write\_build\_file(path, script).
- Set self.component\_scripts at name from path.
- Evaluate self.\_add\_icons(script).
- Evaluate self.\_add\_page\_source(script).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add icons](operations-009.md#op-1321388cd708ac), [add page source](operations-009.md#op-087eb128ecfc20).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1906)

<a id="op-087eb128ecfc20"></a>
### Studio App Builder.add page source

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_page_source`

**Inputs** self, source.

**Declared result** no value.

**Local steps**

- If source.
  - Evaluate self.page\_sources.append(source when isinstance(source, str), otherwise json.dumps(source)).
    - Value choice on isinstance(source, str) — true gives source, false gives json.dumps(source).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1910)

<a id="op-16558d999325f4"></a>
### Studio App Builder.load studio components from files

`operation_foundation_binding_foundation_studio_build_studioappbuilder_load_studio_components_from_files`

**Inputs** self, app\_folder.

**Explicit results** self.studio\_component\_blocks.

**Local steps**

- Set self.studio\_component\_blocks from mapping().
- Set components\_folder from os.path.join(app\_folder, “studio\_components”).
- If not os.path.exists(components\_folder).
  - Return self.studio\_component\_blocks.
- For each file in os.listdir(components\_folder).
  - If not file.endswith(“.json”).
    - Continue with the next iteration or loop test.
  - Set component\_file\_path from os.path.join(components\_folder, file).
  - Attempt the following.
    - Within open(component\_file\_path) bound as f.
      - Set component\_text from f.read().
    - Set component from json.loads(component\_text).
    - Evaluate self.\_add\_icons(component\_text).
    - Set component\_name from (component.get(“component\_id”) or component.get(“name”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“component\_id”) → component.get(“name”).
    - Set block from component.get(“block”).
    - If (component\_name and block).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in component\_name → block.
      - If isinstance(block, str).
        - Set block from json.loads(block).
      - Set self.studio\_component\_blocks at component\_name from block.
  - On failure (tuple(json.JSONDecodeError, OSError)).
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add icons](operations-009.md#op-1321388cd708ac).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1918)

<a id="op-7dcc08a9c5c912"></a>
### Studio App Builder.add custom vue component

`operation_foundation_binding_foundation_studio_build_studioappbuilder_add_custom_vue_component`

**Inputs** self, componentName.

**Explicit results** no value.

**Local steps**

- If (not componentName or not self.app\_folder).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not componentName → not self.app\_folder.
  - Return no value.
- For each tuple(dirpath, \_dirnames, filenames) in os.walk(self.app\_folder).
  - If formatted text {componentName}.vue belongs to filenames.
    - Set self.custom\_vue\_components at componentName from os.path.join(dirpath, formatted text {componentName}.vue).
    - Return no value.
- Evaluate self.missing\_components.add(componentName).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1907)

<a id="op-e8f6712a198726"></a>
### Build standard apps

`operation_foundation_binding_foundation_studio_build_build_standard_apps`

**Inputs** apps = no value.

**Declared result** no value.

**Explicit failure paths** RuntimeError(formatted text Studio app builds failed: {“, ”.join(failed\_apps)}).

**Local steps**

- Set failed\_apps from list().
- For each Platform\_app in (apps or Platform.get\_all\_apps()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in apps → Platform.get\_all\_apps().
  - For each app\_folder in get\_exported\_app\_folders(get\_studio\_folder(Platform\_app)).
    - Set studio\_app from get\_exported\_app\_name(app\_folder).
    - Evaluate click.echo(formatted text  Building Studio App: {studio\_app} (from {Platform\_app})).
    - Attempt the following.
      - Evaluate StudioAppBuilder(studio\_app, is\_standard = true, Platform\_app = Platform\_app).build().
      - Evaluate click.echo((click.style(“✔”, fg = “green”) + formatted text  Built {studio\_app})).
    - On failure (Exception).
      - Evaluate traceback.print\_exc().
      - Evaluate click.echo((click.style(“✖”, fg = “red”) + formatted text  Build failed for {studio\_app})).
      - Evaluate failed\_apps.append(studio\_app).
- If failed\_apps.
  - Raise RuntimeError(formatted text Studio app builds failed: {“, ”.join(failed\_apps)}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1896)

<a id="op-2fb49e8a5cecf0"></a>
### Build custom apps

`operation_foundation_binding_foundation_studio_build_build_custom_apps`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Set custom\_apps from get\_published\_custom\_apps().
- For each app\_name in custom\_apps.
  - Evaluate click.echo(formatted text  Building Custom Studio App: {app\_name}).
  - Attempt the following.
    - Evaluate StudioAppBuilder(app\_name, is\_standard = false).build().
  - On failure (Exception) bound to e.
    - Evaluate click.secho(formatted text Failed to build {app\_name}: {e}, fg = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L232) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1895)

<a id="op-b4ac4af41a220c"></a>
### Get published custom apps

`operation_foundation_binding_foundation_studio_build_get_published_custom_apps`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** custom\_apps.

**Local steps**

- Set StudioApp from Platform.qb.DocType(“Studio App”).
- Set StudioPage from Platform.qb.DocType(“Studio Page”).
- Set custom\_apps from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.published equals 1).distinct().run(pluck = true).
- Return custom\_apps.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1901)

<a id="op-0a9faafaed0c4d"></a>
### Get router file

`operation_foundation_binding_foundation_studio_build_get_router_file`

**Inputs** Platform\_app, studio\_app.

**Declared result** (str bitwise or no value).

**Explicit results** find\_router\_file(get\_export\_folder(Platform\_app, studio\_app)).

**Local steps**

- Return find\_router\_file(get\_export\_folder(Platform\_app, studio\_app)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1902)

<a id="op-bd393a32e4b22b"></a>
### Find router file

`operation_foundation_binding_foundation_studio_build_find_router_file`

**Inputs** app\_folder.

**Declared result** (str bitwise or no value).

**Explicit results** path when os.path.exists(path), otherwise no value.

**Local steps**

- Set path from find\_script\_file(app\_folder, “router”).
- Return path when os.path.exists(path), otherwise no value.
  - Value choice on os.path.exists(path) — true gives path, false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1898)

<a id="op-4d4271e3814883"></a>
### Write db files to folder

`operation_foundation_binding_foundation_studio_build_write_db_files_to_folder`

**Inputs** studio\_app, app\_folder.

**Declared result** list at dict.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** page\_scripts.

**Local steps**

- Bind dependencies get\_db\_files.
- Evaluate Platform.create\_folder(app\_folder).
- For each file in get\_db\_files(studio\_app).
  - Evaluate write\_build\_file(os.path.join(app\_folder, file at “path”), file at “content”).
- Set pages from Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → studio\_app, “published” → 1, “script” → tuple(“is”, “set”)), fields = list(“name”, “page\_title”, “script”)).
- Set page\_scripts from list().
- For each page in pages.
  - Set stem from Platform.scrub(page.page\_title).
  - Set path from os.path.join(app\_folder, “studio\_page”, stem, formatted text {stem}.js).
  - Evaluate write\_build\_file(path, page.script).
  - Evaluate page\_scripts.append(mapping(“page\_name” → page.name, “file\_path” → path)).
- Return page\_scripts.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1924)

<a id="op-b181e079bacf03"></a>
### Write build file

`operation_foundation_binding_foundation_studio_build_write_build_file`

**Inputs** path, content.

**Declared result** no value.

**Local steps**

- Evaluate Platform.create\_folder(os.path.dirname(path)).
- Within open(path, “w”, encoding = “utf-8”) bound as f.
  - Evaluate f.write(content).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1923)

<a id="op-7db4c5bbde4db5"></a>
### Get tailwind content

`operation_foundation_binding_foundation_studio_build_get_tailwind_content`

**Inputs** folder.

**Declared result** list at str.

**Explicit results** list(os.path.join(folder, “\*\*”, “\*.{vue,js,ts,jsx,tsx,json}”), (“!” + os.path.join(folder, “\*\*”, “node\_modules”, “\*\*”))).

**Local steps**

- Return list(os.path.join(folder, “\*\*”, “\*.{vue,js,ts,jsx,tsx,json}”), (“!” + os.path.join(folder, “\*\*”, “node\_modules”, “\*\*”))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1903)

<a id="op-cd6227b1b94c5d"></a>
### Is vue component

`operation_foundation_binding_foundation_studio_build_is_vue_component`

**Inputs** component\_name.

**Declared result** bool.

**Explicit results** (bool(component\_name) and component\_name at 0.isupper()).

**Local steps**

- Return (bool(component\_name) and component\_name at 0.isupper()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(component\_name) → component\_name at 0.isupper().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1904)
