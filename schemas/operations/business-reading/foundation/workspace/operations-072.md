# Forms, reports and navigation · operations 72

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio page

<a id="op-acf32b7fe76910"></a>
### Studio Page.before export

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_before_export`

**Inputs** self, doc.

**Local steps**

- Set doc.name from self.get\_export\_docname().
- Set doc.blocks from parse\_json(doc.blocks).
- Set doc.draft\_blocks from parse\_json(doc.draft\_blocks).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2081) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L58)

<a id="op-24ebca0fc47f6d"></a>
### Studio Page.before import

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_before_import`

**Inputs** self.

**Local steps**

- Set self.name from self.page\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2082) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L59)

<a id="op-8df8e34c595ac8"></a>
### Studio Page.get export docname

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_export_docname`

**Inputs** self.

**Explicit results** Platform.scrub(self.page\_title).

**Local steps**

- Return Platform.scrub(self.page\_title).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L74)

<a id="op-26e4ef92f254cd"></a>
### Studio Page.save draft

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_save_draft`

**Inputs** self, draft\_blocks, known\_modified = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** self.modified.

**Local steps**

- Evaluate self.reject\_if\_stale(known\_modified).
- Set self.draft\_blocks from draft\_blocks.
- Set self.\_skip\_validate from true.
- Evaluate self.save().
- Return self.modified.

**Methods declared on this owner** [reject if stale](operations-072.md#op-1d1502538c4448).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L195) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L90)

<a id="op-91c3156231c161"></a>
### Studio Page.save page field

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_save_page_field`

**Inputs** self, fieldname, value = no value, known\_modified = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** self.modified.

**Explicit failure paths** validation helper — translated “Field {0} is not editable outside the Studio editor”.format(field).

**Local steps**

- Set FIELDS from list(“page\_title”, “tab\_title”, “route”, “script”, …).
- Set values from fieldname when isinstance(fieldname, dict), otherwise mapping(fieldname → value).
  - Value choice on isinstance(fieldname, dict) — true gives fieldname, false gives mapping(fieldname → value).
- For each field in values.
  - If field does not belong to FIELDS.
    - Call the validation error handler Platform.throw(translated “Field {0} is not editable outside the Studio editor”.format(field)).
- Evaluate self.reject\_if\_stale(known\_modified).
- Evaluate self.update(values).
- Set self.\_skip\_validate from true.
- Evaluate self.save().
- Return self.modified.

**Methods declared on this owner** [reject if stale](operations-072.md#op-1d1502538c4448).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L196) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L3) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L91)

<a id="op-1d1502538c4448"></a>
### Studio Page.reject if stale

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_reject_if_stale`

**Inputs** self, known\_modified.

**Explicit failure paths** validation helper with TimestampMismatchError — translated “This page was changed outside the editor. Refresh to load the latest version before editing.”.

**Local steps**

- If (known\_modified and get\_datetime(known\_modified) differs from get\_datetime(self.modified)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in known\_modified → get\_datetime(known\_modified) differs from get\_datetime(self.modified).
  - Call the validation error handler Platform.throw(translated “This page was changed outside the editor. Refresh to load the latest version before editing.”, exc = TimestampMismatchError, title = translated “Page changed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L86)

<a id="op-0bbe083a252b31"></a>
### Studio Page.publish

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_publish`

**Inputs** self, known\_modified = no value, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** mapping(“unresolved\_variants” → self.get\_unresolved\_variants()).

**Local steps**

- Evaluate self.reject\_if\_stale(known\_modified).
- Evaluate Platform.form\_dict.update(kwargs).
- Set self.published from 1.
- If self.draft\_blocks.
  - Set self.blocks from self.draft\_blocks.
  - Set self.draft\_blocks from no value.
- Evaluate self.save().
- Return mapping(“unresolved\_variants” → self.get\_unresolved\_variants()).

**Methods declared on this owner** [reject if stale](operations-072.md#op-1d1502538c4448), [get unresolved variants](operations-072.md#op-1f74b29370ff9e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L85)

<a id="op-1f74b29370ff9e"></a>
### Studio Page.get unresolved variants

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_unresolved_variants`

**Inputs** self.

**Declared result** list at str.

**Explicit results** list() · list of ((nested operand in the contract.get(“componentProps”) or mapping()).get(“name”) or “Variant”) for tree drawn from trees, then block drawn from walk\_blocks(tree) where block.get(“componentName”) eq ….

**Local steps**

- Set blocks from (parse\_json(self.blocks) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(self.blocks) → list().
- If not blocks.
  - Return list().
- Set trees from list(blocks, expanded generator of parse\_json(component at “block”) for component drawn from self.get\_components(blocks)).
  - Draw component from self.get\_components(blocks).
- Return list of ((nested operand in the contract.get(“componentProps”) or mapping()).get(“name”) or “Variant”) for tree drawn from trees, then block drawn from walk\_blocks(tree) where block.get(“componentName”) eq ….
  - Draw tree from trees.
  - Draw block from walk\_blocks(tree), keep a combination only if (block.get(“componentName”) equals “Variants”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (block.get(“componentProps”) or mapping()).get(“name”) → “Variant”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentProps”) → mapping().

**Methods declared on this owner** [get components](operations-072.md#op-a494a3ca85416e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L79)

<a id="op-20b2a0036d7e1c"></a>
### Studio Page.unpublish

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_unpublish`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Local steps**

- Set self.published from 0.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L198) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L5) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L93)

<a id="op-3f6556a6849dfa"></a>
### Studio Page.revert

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_revert`

**Inputs** self, known\_modified = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** self.modified.

**Local steps**

- Evaluate self.reject\_if\_stale(known\_modified).
- Set self.draft\_blocks from no value.
- Set self.\_skip\_validate from true.
- Evaluate self.save().
- Return self.modified.

**Methods declared on this owner** [reject if stale](operations-072.md#op-1d1502538c4448).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L89)

<a id="op-e38fb11c6f7679"></a>
### Studio Page.validate export stem is free

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate_export_stem_is_free`

**Inputs** self.

**Record and data access** read “Studio Page” via get\_all.

**Explicit failure paths** validation helper — translated “Page titles "{0}" and "{1}" both become "{2}". Rename one of the pages.”.format(self.page\_title, page\_title, stem).

**Local steps**

- Set stem from self.get\_export\_docname().
- For each page\_title in Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.studio\_app, “name” → list(“!=”, self.name)), pluck = “page\_title”).
  - If Platform.scrub(page\_title) equals stem.
    - Call the validation error handler Platform.throw(translated “Page titles "{0}" and "{1}" both become "{2}". Rename one of the pages.”.format(self.page\_title, page\_title, stem), title = translated “Conflicting Page Titles”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L200) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L7) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L95)

<a id="op-eb97fbb497f529"></a>
### Studio Page.validate route is free

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_validate_route_is_free`

**Inputs** self.

**Record and data access** read “Studio Page” via get\_all.

**Explicit failure paths** validation helper — translated “Route {0} is already used by: {1}”.format(self.route, “, ”.join(other\_pages)).

**Local steps**

- Set other\_pages from Platform.get\_all(“Studio Page”, filters = mapping(“studio\_app” → self.studio\_app, “name” → list(“!=”, self.name), “route” → self.route), pluck = “page\_title”).
- If other\_pages.
  - Call the validation error handler Platform.throw(translated “Route {0} is already used by: {1}”.format(self.route, “, ”.join(other\_pages))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L203) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L10) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L98)

<a id="op-ea22ff6e7eb61a"></a>
### Studio Page.get folder path

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_folder_path`

**Inputs** self, with\_filename = false.

**Declared result** str.

**Explicit results** os.path.join(expanded path).

**Local steps**

- Set path from list(get\_export\_folder(self.Platform\_app, self.studio\_app), “studio\_page”, self.get\_export\_docname()).
- If with\_filename.
  - Evaluate path.append(self.get\_file\_name()).
- Return os.path.join(expanded path).

**Methods declared on this owner** [get export docname](operations-072.md#op-8df8e34c595ac8), [get file name](operations-072.md#op-60329a01342176).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2099) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L76)

<a id="op-5acab0732969d4"></a>
### Studio Page.export components

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_export_components`

**Inputs** self.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**Local steps**

- Set components from self.get\_components(get\_blocks(self)).
- If components.
  - Evaluate Platform.create\_folder(self.get\_component\_folder\_path()).
  - Evaluate mark\_components\_standard(list of component.name for component drawn from components).
    - Draw component from components.
- For each component in components.
  - Evaluate Platform.get\_doc(“Studio Component”, component.name).export\_to\_folder(self.get\_component\_folder\_path()).
- Evaluate self.delete\_unused\_component\_files().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get components](operations-072.md#op-a494a3ca85416e), [get component folder path](operations-072.md#op-438eb1416340cd), [delete unused component files](operations-072.md#op-2d712e2359e9c0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2087) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L64)

<a id="op-2d712e2359e9c0"></a>
### Studio Page.delete unused component files

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_delete_unused_component_files`

**Inputs** self, deleting = false.

**Record and data access** read “Studio Page” via get\_all.

**Explicit results** no value.

**Local steps**

- Set folder from self.get\_component\_folder\_path().
- If not os.path.isdir(folder).
  - Return no value.
- Set filters from mapping(“studio\_app” → self.studio\_app).
- If deleting.
  - Set filters at “name” from list(“!=”, self.name).
- Set pages from Platform.get\_all(“Studio Page”, filters = filters, fields = list(“blocks”, “draft\_blocks”)).
- Set blocks from list of block for page drawn from pages, then block drawn from get\_blocks(page).
  - Draw page from pages.
  - Draw block from get\_blocks(page).
- Set used from set of Platform.scrub(component.component\_id) for component drawn from self.get\_components(blocks).
  - Draw component from self.get\_components(blocks).
- For each file in os.listdir(folder).
  - If (file.endswith(“.json”) and file.removesuffix(“.json”) does not belong to used).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in file.endswith(“.json”) → file.removesuffix(“.json”) does not belong to used.
    - Evaluate delete\_component\_files(folder, file.removesuffix(“.json”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component folder path](operations-072.md#op-438eb1416340cd), [get components](operations-072.md#op-a494a3ca85416e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2086) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L63)

<a id="op-a494a3ca85416e"></a>
### Studio Page.get components

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_components`

**Inputs** self, blocks.

**Declared result** list at dict.

**Explicit results** get\_components\_for\_blocks(blocks, self.studio\_app).

**Local steps**

- Return get\_components\_for\_blocks(blocks, self.studio\_app).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2093) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L70)

<a id="op-438eb1416340cd"></a>
### Studio Page.get component folder path

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_component_folder_path`

**Inputs** self.

**Declared result** str.

**Explicit results** os.path.join(get\_export\_folder(self.Platform\_app, self.studio\_app), “studio\_components”).

**Local steps**

- Return os.path.join(get\_export\_folder(self.Platform\_app, self.studio\_app), “studio\_components”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2092) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L69)

<a id="op-60329a01342176"></a>
### Studio Page.get file name

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_file_name`

**Inputs** self.

**Explicit results** formatted text {self.get\_export\_docname()}.json.

**Local steps**

- Return formatted text {self.get\_export\_docname()}.json.

**Methods declared on this owner** [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L75)

<a id="op-6c18d6264ab7ff"></a>
### Studio Page.get script file path

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_get_script_file_path`

**Inputs** self.

**Declared result** str.

**Explicit results** find\_script\_file(self.get\_folder\_path(), self.get\_export\_docname()).

**Local steps**

- Return find\_script\_file(self.get\_folder\_path(), self.get\_export\_docname()).

**Methods declared on this owner** [get folder path](operations-072.md#op-ea22ff6e7eb61a), [get export docname](operations-072.md#op-8df8e34c595ac8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L77)

<a id="op-00006812da081f"></a>
### Get blocks

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_get_blocks`

**Inputs** page.

**Declared result** list at dict.

**Explicit results** list(expanded (parse\_json(page.blocks) or list()), expanded (parse\_json(page.draft\_blocks) or list())).

**Local steps**

- Return list(expanded (parse\_json(page.blocks) or list()), expanded (parse\_json(page.draft\_blocks) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(page.blocks) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(page.draft\_blocks) → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2074) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L51)

<a id="op-3dc29612957459"></a>
### Keep variant

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_keep_variant`

**Inputs** app\_name, page\_name, block\_id, option\_name.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** no value.

**State and service calls** call save on page.

**Explicit failure paths** validation helper — translated “Could not keep option "{0}" of variants block {1}. Reload the page and try again.”.format(option\_name, block\_id).

**Local steps**

- Set page from get\_app\_page(app\_name, page\_name, cached = false).
- Set option\_name from str(option\_name).
- Set kept from false.
- For each field in tuple(“draft\_blocks”, “blocks”).
  - Set blocks from (parse\_json(page.get(field)) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(page.get(field)) → list().
  - If (blocks and replace\_variants\_block(blocks, str(block\_id), option\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in blocks → replace\_variants\_block(blocks, str(block\_id), option\_name).
    - Evaluate page.set(field, Platform.as\_json(blocks, indent = no value)).
    - Set kept from true.
- If kept.
  - Set page.\_skip\_validate from true.
  - Evaluate page.save().
- Otherwise.
  - If not keep\_component\_variant(page, str(block\_id), option\_name).
    - Call the validation error handler Platform.throw(translated “Could not keep option "{0}" of variants block {1}. Reload the page and try again.”.format(option\_name, block\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2077) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L54)

<a id="op-9889dee1889272"></a>
### Keep component variant

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_keep_component_variant`

**Inputs** page, block\_id, option\_name.

**Declared result** bool.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**State and service calls** call save on component\_doc.

**Explicit results** true · false.

**Local steps**

- For each component in page.get\_components(get\_blocks(page)).
  - Set block from parse\_json(component at “block”).
  - If (not block or not replace\_variants\_block(block, block\_id, option\_name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not block → not replace\_variants\_block(block, block\_id, option\_name).
    - Continue with the next iteration or loop test.
  - Set component\_doc from Platform.get\_doc(“Studio Component”, component at “name”).
  - Set component\_doc.block from Platform.as\_json(block, indent = no value).
  - Evaluate component\_doc.save().
  - If page.is\_standard.
    - Evaluate page.export\_components().
  - Return true.
- Return false.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2076) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L53)

<a id="op-5f7f65e27ed995"></a>
### Replace variants block

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_replace_variants_block`

**Inputs** blocks, block\_id, option\_name.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- For each parent in walk\_blocks(blocks).
  - For each children in child\_lists(parent).
    - For each tuple(index, child) in enumerate(children).
      - If (not isinstance(child, dict) or child.get(“componentId”) differs from block\_id).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(child, dict) → child.get(“componentId”) differs from block\_id.
        - Continue with the next iteration or loop test.
      - If child.get(“componentName”) differs from “Variants”.
        - Continue with the next iteration or loop test.
      - Set options from (child.get(“children”) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in child.get(“children”) → list().
      - Set matches from list of option for tuple(position, option) drawn from enumerate(options) where (isinstance(option, dict) and (option.get(“variantOptionName”) or formatted text Option {(position + 1)}) equals option\_name).
        - Draw tuple(position, option) from enumerate(options), keep a combination only if ((isinstance(option, dict) and (option.get(“variantOptionName”) or formatted text Option {(position + 1)}) equals option\_name)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(option, dict) → (option.get(“variantOptionName”) or formatted text Option {(position + 1)}) equals option\_name.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in option.get(“variantOptionName”) → formatted text Option {(position + 1)}.
      - If len(matches) differs from 1.
        - Return false.
      - Set kept from matches at 0.
      - Evaluate kept.pop(“variantOptionName”, no value).
      - Set children at index from kept.
      - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2078) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L55)

<a id="op-fac096799c1616"></a>
### Child lists

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_child_lists`

**Inputs** block.

**Local steps**

- If isinstance(block.get(“children”), list).
  - yield block at “children”.
- For each slot in (block.get(“componentSlots”) or mapping()).values().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentSlots”) → mapping().
  - If (isinstance(slot, dict) and isinstance(slot.get(“slotContent”), list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(slot, dict) → isinstance(slot.get(“slotContent”), list).
    - yield slot at “slotContent”.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2072) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L49)
