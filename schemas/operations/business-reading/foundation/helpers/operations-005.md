# Shared value and file services · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Boilerplate

<a id="op-47966062ebedf1"></a>
### Get license text

`operation_foundation_utils_boilerplate_business_behavior_get_license_text`

**Inputs** license\_name.

**Declared result** str.

**Explicit results** “No license text found” · res.get(“body”) · license\_name.

**Local steps**

- Set url from formatted command or address in the contract.
- Attempt the following.
  - Set res from requests.get(url = url).
- On failure (requests.exceptions.RequestException).
  - Return “No license text found”.
- If res.status\_code equals 200.
  - Set res from res.json().
  - Return res.get(“body”).
- Return license\_name.

**Values supplied outside this operation** service or queued work from requests.get(url = url).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L7165) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1550)

<a id="op-743f3e9f79b3dc"></a>
### Copy from Platform

`operation_foundation_utils_boilerplate_business_behavior_copy_from_foundation`

**Inputs** rel\_path, new\_app\_path.

**Local steps**

- Set src from (Path(Platform.get\_app\_path(“Platform”, “..”)) ÷ rel\_path).
- Set target from (Path(new\_app\_path) ÷ rel\_path).
- Evaluate Path(target).write\_text(Path(src).read\_text()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0464.json#L7397) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1546)

<a id="op-97337c752cdd60"></a>
### Create app boilerplate

`operation_foundation_utils_boilerplate_business_behavior_create_application_boilerplate`

**Inputs** dest, hooks, no\_git = false.

**Local steps**

- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, Platform.scrub(hooks.app\_title)), with\_init = true).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “templates”), with\_init = true).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “www”)).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “templates”, …), with\_init = true).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “templates”, …)).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “config”), with\_init = true).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “public”, …)).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “public”, …)).
- Evaluate Platform.create\_folder(os.path.join(dest, hooks.app\_name, hooks.app\_name, “patches”), with\_init = true).
- Within open(os.path.join(dest, hooks.app\_name, hooks.app\_name, “public”, …), “w”) bound as f.
  - Evaluate f.write(empty text).
- Within open(os.path.join(dest, hooks.app\_name, hooks.app\_name, “\_\_init\_\_.py”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(init\_template)).
- Within open(os.path.join(dest, hooks.app\_name, “pyproject.toml”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(pyproject\_template.format(expanded names hooks))).
- Within open(os.path.join(dest, hooks.app\_name, “.pre-commit-config.yaml”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(precommit\_template.format(expanded names hooks))).
- Set license\_body from get\_license\_text(license\_name = hooks.app\_license).
- Within open(os.path.join(dest, hooks.app\_name, “license.txt”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(license\_body)).
- Within open(os.path.join(dest, hooks.app\_name, hooks.app\_name, Platform.scrub(hooks.app\_title), …), “w”) bound as f.
  - Evaluate f.write(empty text).
- Bind dependencies boilerplate\_modules\_txt.
- Evaluate boilerplate\_modules\_txt(dest, hooks.app\_name, hooks.app\_title).
- For each key in tuple(“app\_publisher”, “app\_description”, “app\_license”).
  - Set hooks at key from nested operand in the contract at nested operand in the contract.replace(“\\”, “\\\\”).replace(“'”, “\\'”).replace(“"”, “\\"”).
- Within open(os.path.join(dest, hooks.app\_name, hooks.app\_name, “hooks.py”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(hooks\_template.format(expanded names hooks))).
- Within open(os.path.join(dest, hooks.app\_name, hooks.app\_name, “patches.txt”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(patches\_template.format(expanded names hooks))).
- Set app\_directory from os.path.join(dest, hooks.app\_name).
- Evaluate copy\_from\_Platform(“.editorconfig”, app\_directory).
- Evaluate copy\_from\_Platform(“.eslintrc”, app\_directory).
- If hooks.create\_github\_workflow.
  - Evaluate \_create\_github\_workflow\_files(dest, hooks).
  - Set hooks.readme\_ci\_section from readme\_ci\_section.
- Otherwise.
  - Set hooks.readme\_ci\_section from empty text.
- Within open(os.path.join(dest, hooks.app\_name, “README.md”), “w”) bound as f.
  - Evaluate f.write(Platform.as\_unicode(readme\_template.format(expanded names hooks))).
- If not no\_git.
  - Within open(os.path.join(dest, hooks.app\_name, “.gitignore”), “w”) bound as f.
    - Evaluate f.write(Platform.as\_unicode(gitignore\_template.format(app\_name = hooks.app\_name))).
  - Set app\_repo from git.Repo.init(app\_directory, initial\_branch = hooks.branch\_name).
  - Evaluate app\_repo.git.add(A = true).
  - Evaluate app\_repo.index.commit(“feat: Initialize App”).
- Evaluate print(formatted text '{hooks.app\_name}' created at {app\_directory}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1547)

<a id="op-377b9ab64b4834"></a>
### Create github workflow files

`operation_foundation_utils_boilerplate_business_behavior_create_github_workflow_files`

**Inputs** dest, hooks.

**Local steps**

- Set workflows\_path from (((pathlib.Path(dest) ÷ hooks.app\_name) ÷ “.github”) ÷ “workflows”).
- Evaluate workflows\_path.mkdir(parents = true, exist\_ok = true).
- Set ci\_workflow from (workflows\_path ÷ “ci.yml”).
- Within open(ci\_workflow, “w”) bound as f.
  - Evaluate f.write(github\_workflow\_template.format(expanded names hooks)).
- Set linter\_workflow from (workflows\_path ÷ “linter.yml”).
- Within open(linter\_workflow, “w”) bound as f.
  - Evaluate f.write(linter\_workflow\_template).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L2519) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1548)

<a id="op-1249fec8cf184d"></a>
### Patch Creator.initialize

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_initialize`

**Inputs** self.

**Local steps**

- Set self.all\_apps from Platform.get\_all\_apps(sites\_path = “.”, with\_internal\_apps = false).
- Set self.app from no value.
- Set self.app\_dir from no value.
- Set self.patch\_dir from no value.
- Set self.filename from no value.
- Set self.docstring from no value.
- Set self.patch\_file from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L2827) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1563)

<a id="op-6d7f8bceb088b5"></a>
### Patch Creator.fetch user inputs

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_fetch_user_inputs`

**Inputs** self.

**Local steps**

- Evaluate self.\_ask\_app\_name().
- Evaluate self.\_ask\_doctype\_name().
- Evaluate self.\_ask\_patch\_meta\_info().

If control reaches the end, it returns no value.

**Methods declared on this owner** [ask app name](operations-005.md#op-00f90584eea28f), [ask doctype name](operations-005.md#op-f0d1775717ab1d), [ask patch meta info](operations-005.md#op-d59497a13b3653).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L3003) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1562)

<a id="op-00f90584eea28f"></a>
### Patch Creator.ask app name

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_ask_application_name`

**Inputs** self.

**Local steps**

- Set self.app from click.prompt(“Select app for new patch”, type = click.Choice(self.all\_apps)).
- Set self.app\_dir from pathlib.Path(Platform.get\_app\_path(self.app)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L3094) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1555)

<a id="op-f0d1775717ab1d"></a>
### Patch Creator.ask doctype name

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_ask_record_type_name`

**Inputs** self.

**Local steps**

- Bind local operation \_doctype\_name for subsequent calls.
- Set doctype\_files from list(glob.glob(formatted text {self.app\_dir}/\*\*/doctype/\*\*/\*.json)).
- Set doctype\_map from mapping of \_doctype\_name(file) → file for file drawn from doctype\_files.
  - Draw file from doctype\_files.
- Evaluate doctype\_map.pop(no value, no value).
- Set doctype from click.prompt(“Provide DocType name on which this patch will apply”, type = click.Choice(doctype\_map.keys()), show\_choices = false).
- Set self.patch\_dir from (pathlib.Path(doctype\_map at doctype).parents at 0 ÷ “patches”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L3245) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1558)

<a id="op-edfadb7e60b76e"></a>
### Patch Creator.ask doctype name.doctype name

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_ask_record_type_name_record_type_name`

**Inputs** filename.

**Explicit results** json.load(f).get(“name”).

**Local steps**

- Within contextlib.suppress(Exception).
  - Within open(filename) bound as f.
    - Return json.load(f).get(“name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L3670) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1559)

<a id="op-d59497a13b3653"></a>
### Patch Creator.ask patch meta info

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_ask_patch_meta_info`

**Inputs** self.

**Local steps**

- Set self.docstring from click.prompt(“Describe what this patch does”, type = str).
- Set default\_filename from (Platform.scrub(self.docstring) + “.py”).
- Bind local operation \_valid\_filename for subsequent calls.
- While not \_valid\_filename(self.filename).
  - Set self.filename from click.prompt(“Provide filename for this patch”, type = str, default = default\_filename).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L3808) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1556)

<a id="op-750a772da77231"></a>
### Patch Creator.ask patch meta info.valid filename

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_ask_patch_meta_info_valid_filename`

**Inputs** name.

**Explicit results** no value · true.

**Local steps**

- If not name.
  - Return no value.
- Select the first matching pattern against name.partition(“.”).
  - Pattern sequence filename, “.”, “py” with guard filename.isidentifier().
    - Return true.
  - Pattern any value.
    - Evaluate click.echo(formatted text {name} is not a valid python file name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L4178) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1557)

<a id="op-81440f197d6006"></a>
### Patch Creator.create patch file

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_create_patch_file`

**Inputs** self.

**Explicit failure paths** Exception(formatted text Patch {self.patch\_file} already exists) · Exception(formatted text Patch {dotted\_path} is already present in patches.txt).

**Local steps**

- Evaluate self.\_create\_parent\_folder\_if\_not\_exists().
- Set self.patch\_file from (self.patch\_dir ÷ self.filename).
- If self.patch\_file.exists().
  - Raise Exception(formatted text Patch {self.patch\_file} already exists).
- Set tuple(expanded path, \_filename) from self.patch\_file.relative\_to(self.app\_dir.parents at 0).parts.
- Set dotted\_path from “.”.join(list(expanded path, self.patch\_file.stem)).
- Set patches\_txt from (self.app\_dir ÷ “patches.txt”).
- Set existing\_patches from patches\_txt.read\_text().
- If dotted\_path belongs to existing\_patches.
  - Raise Exception(formatted text Patch {dotted\_path} is already present in patches.txt).
- Evaluate self.patch\_file.write\_text(PATCH\_TEMPLATE.format(docstring = self.docstring)).
- Within open(patches\_txt, “a+”) bound as f.
  - If not existing\_patches.endswith(whitespace '\\n').
    - Evaluate f.write(whitespace '\\n').
  - Evaluate f.write((dotted\_path + whitespace '\\n')).
- Evaluate click.echo(formatted text Created {self.patch\_file} and updated patches.txt).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create parent folder if not exists](operations-005.md#op-4e5be3bdeae197).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L4361) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1561)

<a id="op-4e5be3bdeae197"></a>
### Patch Creator.create parent folder if not exists

`operation_foundation_utils_boilerplate_business_behavior_patch_creator_create_parent_folder_if_not_exists`

**Inputs** self.

**Local steps**

- If not self.patch\_dir.exists().
  - Evaluate click.confirm(formatted text Patch folder '{self.patch\_dir}' doesn't exist, create it?, abort = true, default = true).
  - Evaluate self.patch\_dir.mkdir().
- Set init\_py from (self.patch\_dir ÷ “\_\_init\_\_.py”).
- Evaluate init\_py.touch().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L4962) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1560)

## Service · Browser

<a id="op-9a82b395e134d8"></a>
### Browser.initialize

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_initialize`

**Inputs** self, generator, print\_format, html, options.

**Record and data access** read “Print Format” via get\_cached\_value.

**Local steps**

- Set self.print\_format from print\_format.
- Set self.is\_print\_designer from Platform.get\_cached\_value(“Print Format”, print\_format, “print\_designer”).
- Set self.debug\_mode from (Platform.conf.developer\_mode and bool(Platform.form\_dict.get(“pdf\_debug”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → bool(Platform.form\_dict.get(“pdf\_debug”)).
- Set self.browserID from Platform.utils.random\_string(10).
- Evaluate generator.add\_browser(self.browserID).
- Attempt the following.
  - Evaluate self.set\_html(html).
  - Evaluate self.set\_options(options).
  - Evaluate self.open(generator).
  - Evaluate self.prepare\_header\_footer().
  - Evaluate self.setup\_body\_page().
  - Evaluate self.prepare\_options\_for\_pdf().
  - Evaluate self.update\_header\_footer\_page\_pd().
  - Evaluate self.try\_async\_header\_footer\_pdf().
  - Evaluate self.body\_page.wait\_for\_set\_content().
  - Evaluate self.fit\_body\_height().
  - Set self.body\_pdf from self.body\_page.generate\_pdf(raw = (not self.header\_page and not self.footer\_page)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.header\_page → not self.footer\_page.
  - Evaluate self.update\_header\_footer\_page().
  - If self.header\_page.
    - If not self.is\_header\_dynamic.
      - Set self.header\_pdf from self.header\_page.get\_pdf\_from\_stream(self.header\_page.get\_pdf\_stream\_id()).
    - Otherwise.
      - Set self.header\_pdf from self.header\_page.generate\_pdf().
  - If self.footer\_page.
    - If not self.is\_footer\_dynamic.
      - Set self.footer\_pdf from self.footer\_page.get\_pdf\_from\_stream(self.footer\_page.get\_pdf\_stream\_id()).
    - Otherwise.
      - Set self.footer\_pdf from self.footer\_page.generate\_pdf().
- On exit, including pending return or failure.
  - If not self.debug\_mode.
    - For each attr in tuple(“body\_page”, “header\_page”, “footer\_page”).
      - Set page from getattr(self, attr, no value).
      - If page.
        - Attempt the following.
          - Evaluate page.close().
        - On failure (Exception).
          - Evaluate Platform.log\_error(formatted text Failed to close {attr} in Chrome).
    - If getattr(self, “session”, no value).
      - Attempt the following.
        - Evaluate self.close().
      - On failure (Exception).
        - Evaluate Platform.log\_error(“Failed to disconnect CDP session”).
  - Evaluate generator.remove\_browser(self.browserID).
- If self.debug\_mode.
  - Evaluate generator.detach\_debug\_browser().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set html](operations-005.md#op-6f9cca88165fdc), [set options](operations-005.md#op-dc1bcca3fc5d67), [open](operations-005.md#op-00c96f7111aa0e), [prepare header footer](operations-005.md#op-7b5cd6846f5cec), [setup body page](operations-005.md#op-a9d8e7e0a9b93e), [prepare options for pdf](operations-006.md#op-e6a174fc3e1c1f), [update header footer page pd](operations-006.md#op-a95bcb4e31315b), [try async header footer pdf](operations-006.md#op-ebc279e6ef01ea), [fit body height](operations-005.md#op-656596e7eef910), [update header footer page](operations-006.md#op-05574c829719e6), [close](operations-006.md#op-59b383349f8a3c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Print Format”, print\_format, “print\_designer”) · selected callable from getattr(self, attr, no value), getattr(self, “session”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L17) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L447)

<a id="op-00c96f7111aa0e"></a>
### Browser.open

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_open`

**Inputs** self, generator.

**Local steps**

- Bind dependencies CDPSocketClient.
- If not generator.\_devtools\_url.
  - Evaluate generator.\_set\_devtools\_url().
- Set self.session from CDPSocketClient(generator.\_devtools\_url).
- Evaluate self.session.connect().
- Evaluate self.create\_browser\_context().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create browser context](operations-005.md#op-f679ea157ae218).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L19) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L451)

<a id="op-f679ea157ae218"></a>
### Browser.create browser context

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_create_browser_context`

**Inputs** self.

**Local steps**

- Set tuple(result, error) from self.session.send(“Target.createBrowserContext”, mapping(“disposeOnDetach” → true)).
- If error.
  - Evaluate Platform.log\_error(title = “Error creating browser context:”, message = formatted text {error}).
- Set self.browser\_context\_id from result at “browserContextId”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L6613) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L444)

<a id="op-6f9cca88165fdc"></a>
### Browser.set html

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_set_document_markup`

**Inputs** self, html.

**Local steps**

- Set self.soup from BeautifulSoup(html, “html5lib”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L6785) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L457)

<a id="op-dc1bcca3fc5d67"></a>
### Browser.set options

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_set_options`

**Inputs** self, options.

**Local steps**

- Set self.options from options.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L6856) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L458)

<a id="op-0400f737887f81"></a>
### Browser.new page

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_new_page`

**Inputs** self, page\_type.

**Explicit results** page.

**Local steps**

- Bind dependencies Page.
- Set page from Page(self.session, self.browser\_context\_id, page\_type).
- Set page.is\_print\_designer from self.is\_print\_designer.
- Return page.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L18) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L450)

<a id="op-a9d8e7e0a9b93e"></a>
### Browser.setup body page

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_setup_body_page`

**Inputs** self.

**Local steps**

- Set self.body\_page from self.new\_page(“body”).
- Evaluate self.body\_page.set\_tab\_url(get\_host\_url()).
- Evaluate self.body\_page.wait\_for\_navigate().
- Evaluate self.body\_page.set\_content(str(self.soup)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [new page](operations-005.md#op-0400f737887f81).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L7027) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L459)

<a id="op-656596e7eef910"></a>
### Browser.fit body height

`operation_foundation_binding_foundation_utils_pdf_generator_browser_browser_fit_body_height`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.options.get(“fit-height”).
  - Return no value.
- Set options from self.body\_page.options.
- Set printable from (96 × ((options at “paperWidth” − options.get(“marginLeft”, 0)) − options.get(“marginRight”, 0))).
- Evaluate self.body\_page.set\_device\_metrics(width = int(printable), height = 1).
- Set height from (((self.body\_page.get\_content\_height() + 2) × options.get(“scale”, 1)) ÷ 96).
- Set options at “paperHeight” from ((height + options.get(“marginTop”, 0)) + options.get(“marginBottom”, 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L65) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L223)

<a id="op-eadc6f02ac5dd7"></a>
### Browser.close page

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_close_page`

**Inputs** self, type.

**Local steps**

- Set page from getattr(self, formatted text {type}\_page).
- Evaluate page.close().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, formatted text {type}\_page).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L7200) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L443)

<a id="op-f801a6277697b1"></a>
### Browser.is page no used

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_is_page_number_used`

**Inputs** self, soup.

**Explicit results** true · false.

**Local steps**

- Set classes\_to\_check from list(“page”, “frompage”, “topage”, “page\_info\_page”, …).
- For each class\_name in classes\_to\_check.
  - If soup.find(class\_ = class\_name).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L7301) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L449)

<a id="op-7b5cd6846f5cec"></a>
### Browser.prepare header footer

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_prepare_header_footer`

**Inputs** self.

**Local steps**

- Set soup from self.soup.
- Evaluate self.\_add\_page\_number(soup).
- Evaluate self.\_open\_header\_footer\_pages().
- Evaluate self.\_inject\_page\_no\_script(soup).
- Set head from soup.find(“head”).contents.
- Set styles from soup.find\_all(“style”).
- If self.header\_page.
  - Evaluate self.header\_page.wait\_for\_navigate().
  - Evaluate self.header\_page.set\_content(self.get\_rendered\_header\_footer(self.header\_content, “header”, head, styles, css = list())).
- If self.footer\_page.
  - Evaluate self.footer\_page.wait\_for\_navigate().
  - Evaluate self.footer\_page.set\_content(self.get\_rendered\_header\_footer(self.footer\_content, “footer”, head, styles, css = list())).
- If self.header\_page.
  - Evaluate self.header\_page.wait\_for\_set\_content().
  - Set self.header\_height from self.header\_page.get\_element\_height().
  - Set self.is\_header\_dynamic from self.is\_page\_no\_used(self.header\_content).
  - Remove self.header\_content.
  - If not self.header\_height.
    - Evaluate self.header\_page.close().
    - Set self.header\_page from no value.
- If self.footer\_page.
  - Evaluate self.footer\_page.wait\_for\_set\_content().
  - Set self.footer\_height from self.footer\_page.get\_element\_height().
  - Set self.is\_footer\_dynamic from self.is\_page\_no\_used(self.footer\_content).
  - Remove self.footer\_content.
  - If not self.footer\_height.
    - Evaluate self.footer\_page.close().
    - Set self.footer\_page from no value.
- For each html\_id in list(“header-html”, “footer-html”).
  - For each tag in soup.find\_all(id = html\_id).
    - Evaluate tag.extract().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add page number](operations-006.md#op-bf34c0f00c8496), [open header footer pages](operations-006.md#op-e75af8d3916ead), [inject page no script](operations-006.md#op-222b6faad2bd79), [get rendered header footer](operations-006.md#op-d6ac8c05ddfa5b), [is page no used](operations-005.md#op-f801a6277697b1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L21) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L454)
