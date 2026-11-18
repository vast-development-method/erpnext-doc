# Forms, reports and navigation · operations 70

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Studio page

<a id="op-729227d0c1b1d1"></a>
### Duplicate page

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_duplicate_page`

**Inputs** page\_name, app\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** paste\_page((app\_name or page.studio\_app), mapping(expand page.get\_copy(blocks), “blocks” → blocks)).

**Local steps**

- Set page from Platform.get\_doc(“Studio Page”, page\_name).
- Evaluate page.check\_permission(“read”).
- Set blocks from (parse\_json((page.draft\_blocks or page.blocks)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json((page.draft\_blocks or page.blocks)) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.draft\_blocks → page.blocks.
- Return paste\_page((app\_name or page.studio\_app), mapping(expand page.get\_copy(blocks), “blocks” → blocks)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_name → page.studio\_app.

**Values supplied outside this operation** effective access from page.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L34)

<a id="op-0881a16b86d3d2"></a>
### Paste page

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_paste_page`

**Inputs** app\_name, page, target\_page = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Invalid page copy.”.

**Local steps**

- Set copy from Platform.parse\_json(page).
- If not isinstance(copy, dict).
  - Call the validation error handler Platform.throw(translated “Invalid page copy.”).
- Set app from get\_writable\_app(app\_name).
- Set blocks from parse\_dict\_list(copy.get(“blocks”), “blocks”).
- Set resources from parse\_dict\_list(copy.get(“resources”), “resources”).
- Set variables from parse\_dict\_list(copy.get(“variables”), “variables”).
- Evaluate validate\_page\_copy(copy).
- If target\_page.
  - Set doc from get\_writable\_page(target\_page, app.name).
- Otherwise.
  - Evaluate Platform.has\_permission(“Studio Page”, ptype = “create”, throw = true).
  - Set doc from new\_page\_from\_copy(app, copy).
- Evaluate install\_dependencies(app, copy.get(“components”), copy.get(“files”)).
- Set doc.draft\_blocks from blocks.
- Evaluate doc.set(“resources”, list of pick(row, PAGE\_RESOURCE\_FIELDS) for row drawn from resources).
  - Draw row from resources.
- Evaluate doc.set(“variables”, list of pick(row, PAGE\_VARIABLE\_FIELDS) for row drawn from variables).
  - Draw row from variables.
- Set doc.script from copy.get(“script”).
- Evaluate doc.save().
- If can\_export(doc).
  - Evaluate doc.write\_script\_file().
- Return doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “create”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2067) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L44)

<a id="op-a81e06cf0fc05f"></a>
### Create missing dependencies

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_create_missing_dependencies`

**Inputs** app\_name, components = no value, files = no value, page\_name = no value, resources = no value, variables = no value, overwrite\_conflicts = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** mapping(“conflicts” → conflicts, “modified” → page.modified when page, otherwise no value).

**Local steps**

- Set app from get\_writable\_app(app\_name).
- Set page from get\_writable\_page(page\_name, app.name) when page\_name, otherwise no value.
  - Value choice on page\_name — true gives get\_writable\_page(page\_name, app.name), false gives no value.
- Set resources from parse\_dict\_list(resources, “resources”).
- Set variables from parse\_dict\_list(variables, “variables”).
- Set conflicts from mapping(“components” → install\_dependencies(app, components, files, overwrite\_conflicts = overwrite\_conflicts)).
- If page\_name.
  - Evaluate conflicts.update(add\_page\_data(page, resources, variables, overwrite\_conflicts = overwrite\_conflicts)).
- Return mapping(“conflicts” → conflicts, “modified” → page.modified when page, otherwise no value).
  - Value choice on page — true gives page.modified, false gives no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L31)

<a id="op-8bfd58f6323203"></a>
### Paste data source

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_paste_data_source`

**Inputs** app\_name, page\_name, resource.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on page.

**Explicit results** mapping(“modified” → page.modified).

**Explicit failure paths** validation helper — translated “Invalid data source copy.” · validation helper — translated “Invalid data source name in copied content.” · validation helper — translated “Data source {0} already exists on this page.”.format(resource\_name).

**Local steps**

- Set app from get\_writable\_app(app\_name).
- Set page from get\_writable\_page(page\_name, app.name).
- Set resource from Platform.parse\_json(resource).
- If not isinstance(resource, dict).
  - Call the validation error handler Platform.throw(translated “Invalid data source copy.”).
- Set resource\_name from resource.get(“resource\_name”).
- If (not isinstance(resource\_name, str) or not resource\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(resource\_name, str) → not resource\_name.
  - Call the validation error handler Platform.throw(translated “Invalid data source name in copied content.”).
- If any(generator of row.resource\_name equals resource\_name for row drawn from page.resources).
  - Draw row from page.resources.
  - Call the validation error handler Platform.throw(translated “Data source {0} already exists on this page.”.format(resource\_name)).
- Evaluate page.append(“resources”, pick(resource, PAGE\_RESOURCE\_FIELDS)).
- Evaluate page.save().
- Return mapping(“modified” → page.modified).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2066) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L43)

<a id="op-795488b7f9bfa6"></a>
### Get writable app

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_get_writable_app`

**Inputs** app\_name.

**Record and data access** resolve a document from “Studio App” via get\_doc.

**Explicit results** app.

**Explicit failure paths** validation helper — translated “Invalid Studio App.”.

**Local steps**

- If (not isinstance(app\_name, str) or not app\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(app\_name, str) → not app\_name.
  - Call the validation error handler Platform.throw(translated “Invalid Studio App.”).
- Set app from Platform.get\_doc(“Studio App”, app\_name).
- Evaluate app.check\_permission(“write”).
- Return app.

**Values supplied outside this operation** effective access from app.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2059) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L36)

<a id="op-370bc8d2eb388c"></a>
### Get writable page

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_get_writable_page`

**Inputs** page\_name, app\_name.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** page.

**Explicit failure paths** validation helper — translated “Invalid Studio Page.” · validation helper with Platform.PermissionError — translated “The target page does not belong to the selected app.”.

**Local steps**

- If (not isinstance(page\_name, str) or not page\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(page\_name, str) → not page\_name.
  - Call the validation error handler Platform.throw(translated “Invalid Studio Page.”).
- Set page from Platform.get\_doc(“Studio Page”, page\_name).
- Evaluate page.check\_permission(“read”).
- Evaluate page.check\_permission(“write”).
- If page.studio\_app differs from app\_name.
  - Call the validation error handler Platform.throw(translated “The target page does not belong to the selected app.”, Platform.PermissionError).
- Return page.

**Values supplied outside this operation** effective access from page.check\_permission(“read”), page.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2060) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L37)

<a id="op-0b719b5344f2be"></a>
### Install dependencies

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_install_dependencies`

**Inputs** app, components, files, overwrite\_conflicts (named only, default false).

**Explicit results** conflicts.

**Local steps**

- Set conflicts from create\_missing\_components(parse\_dict\_list(components, “components”), app.name, overwrite\_conflicts = overwrite\_conflicts).
- Evaluate app.write\_files(parse\_dict\_list(files, “files”)).
- Return conflicts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2061) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L38)

<a id="op-bd759963af34a8"></a>
### Parse list

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_parse_list`

**Inputs** value, label.

**Declared result** list.

**Explicit results** list() · value.

**Explicit failure paths** validation helper — translated “Invalid {0} in copied content.”.format(label).

**Local steps**

- Set value from Platform.parse\_json(value).
- If value is identical to no value.
  - Return list().
- If not isinstance(value, list).
  - Call the validation error handler Platform.throw(translated “Invalid {0} in copied content.”.format(label)).
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2065) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L42)

<a id="op-08ea59ac2f1271"></a>
### Parse dict list

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_parse_dict_list`

**Inputs** value, label.

**Declared result** list at dict.

**Explicit results** rows.

**Explicit failure paths** validation helper — translated “Invalid {0} in copied content.”.format(label).

**Local steps**

- Set rows from parse\_list(value, label).
- If not all(generator of isinstance(row, dict) for row drawn from rows).
  - Draw row from rows.
  - Call the validation error handler Platform.throw(translated “Invalid {0} in copied content.”.format(label)).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2064) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L41)

<a id="op-5586572ffa245c"></a>
### Validate page copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_validate_page_copy`

**Inputs** copy.

**Explicit failure paths** validation helper — translated “Invalid page title in copied content.” · validation helper — translated “Invalid tab title in copied content.” · validation helper — translated “Invalid script in copied content.” · validation helper — translated “Invalid guest access setting in copied content.”.

**Local steps**

- If (copy.get(“page\_title”) is distinct from no value and not isinstance(copy at “page\_title”, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in copy.get(“page\_title”) is distinct from no value → not isinstance(copy at “page\_title”, str).
  - Call the validation error handler Platform.throw(translated “Invalid page title in copied content.”).
- If (copy.get(“tab\_title”) is distinct from no value and not isinstance(copy at “tab\_title”, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in copy.get(“tab\_title”) is distinct from no value → not isinstance(copy at “tab\_title”, str).
  - Call the validation error handler Platform.throw(translated “Invalid tab title in copied content.”).
- If (copy.get(“script”) is distinct from no value and not isinstance(copy at “script”, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in copy.get(“script”) is distinct from no value → not isinstance(copy at “script”, str).
  - Call the validation error handler Platform.throw(translated “Invalid script in copied content.”).
- If copy.get(“allow\_guest”) does not belong to tuple(no value, 0, 1, false, …).
  - Call the validation error handler Platform.throw(translated “Invalid guest access setting in copied content.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2071) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L48)

<a id="op-dfcb8bde4a2463"></a>
### Add page data

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_add_page_data`

**Inputs** page, resources, variables, overwrite\_conflicts (named only, default false).

**State and service calls** call save on page.

**Explicit results** conflicts.

**Local steps**

- Set conflicts from mapping().
- Set tuple(conflicts at “resources”, resources\_changed) from append\_missing\_rows(page, “resources”, resources, “resource\_name”, int\_fields = PAGE\_RESOURCE\_INT\_FIELDS, json\_fields = PAGE\_RESOURCE\_JSON\_FIELDS, overwrite\_conflicts = overwrite\_conflicts, …).
- Set tuple(conflicts at “variables”, variables\_changed) from append\_missing\_rows(page, “variables”, variables, “variable\_name”, overwrite\_conflicts = overwrite\_conflicts, …).
- If (resources\_changed or variables\_changed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in resources\_changed → variables\_changed.
  - Evaluate page.save().
- Return conflicts.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L27)

<a id="op-932a05ac91b0ed"></a>
### Append missing rows

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_append_missing_rows`

**Inputs** page, table\_field, rows, key\_field, fields, int\_fields (named only, default tuple()), json\_fields (named only, default tuple()), overwrite\_conflicts (named only, default false).

**Explicit results** tuple(conflicts, changed).

**Explicit failure paths** validation helper — translated “Invalid {0} in copied content.”.format(key\_field.replace(“\_”, one space)).

**Local steps**

- Set existing from mapping of row.get(key\_field) → row for row drawn from page.get(table\_field).
  - Draw row from page.get(table\_field).
- Set conflicts from list().
- Set changed from false.
- For each row in rows.
  - If (not isinstance(row, dict) or not isinstance(row.get(key\_field), str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(row, dict) → not isinstance(row.get(key\_field), str).
    - Call the validation error handler Platform.throw(translated “Invalid {0} in copied content.”.format(key\_field.replace(“\_”, one space))).
  - Set key from row at key\_field.
  - If key belongs to existing.
    - If dependency\_signature(existing at key, fields, int\_fields, json\_fields) differs from dependency\_signature(row, fields, int\_fields, json\_fields).
      - Evaluate conflicts.append(mapping(“name” → key, “existing” → pick(existing at key, fields), “copied” → pick(row, fields))).
      - If overwrite\_conflicts.
        - Evaluate existing at key.update(pick(row, fields)).
        - Set changed from true.
    - Continue with the next iteration or loop test.
  - Set existing at key from page.append(table\_field, pick(row, fields)).
  - Set changed from true.
- Return tuple(conflicts, changed).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L28)

<a id="op-19cd7302ec8b50"></a>
### Dependency signature

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_dependency_signature`

**Inputs** row, fields, int\_fields = tuple(), json\_fields = tuple().

**Explicit results** mapping of field → normalize(field) for field drawn from fields.

**Local steps**

- Bind local operation normalize for subsequent calls.
- Return mapping of field → normalize(field) for field drawn from fields.
  - Draw field from fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L32)

<a id="op-fc066b2cae141f"></a>
### Dependency signature.normalize

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_dependency_signature_normalize`

**Inputs** field.

**Explicit results** cint(value) · Platform.parse\_json(value) when value, otherwise no value · value when value does not belong to tuple(no value, empty text), otherwise no value.

**Local steps**

- Set value from row.get(field).
- If field belongs to int\_fields.
  - Return cint(value).
- If field belongs to json\_fields.
  - Return Platform.parse\_json(value) when value, otherwise no value.
    - Value choice on value — true gives Platform.parse\_json(value), false gives no value.
- Return value when value does not belong to tuple(no value, empty text), otherwise no value.
  - Value choice on value does not belong to tuple(no value, empty text) — true gives value, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L33)

<a id="op-77fc67ad7ca657"></a>
### Pick

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_pick`

**Inputs** row, fields.

**Declared result** dict.

**Explicit results** mapping of field → row.get(field) for field drawn from fields.

**Local steps**

- Return mapping of field → row.get(field) for field drawn from fields.
  - Draw field from fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2068) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L45)

<a id="op-cbf564eec3879a"></a>
### Create missing components

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_create_missing_components`

**Inputs** components, studio\_app, overwrite\_conflicts (named only, default false).

**Record and data access** read “Studio Component” via exists · resolve a document from “Studio Component” via get\_doc.

**State and service calls** call insert on new\_component\_from\_copy(component, owner) · call save on update\_component\_from\_copy(existing, component).

**Explicit results** list() · conflicts.

**Local steps**

- For each component in components.
  - Evaluate validate\_component\_copy(component).
- If not components.
  - Return list().
- Evaluate Platform.has\_permission(“Studio Component”, ptype = “read”, throw = true).
- Set conflicts from list().
- For each component in components.
  - Set owner from studio\_app when component.get(“studio\_app”), otherwise no value.
    - Value choice on component.get(“studio\_app”) — true gives studio\_app, false gives no value.
  - Set name from get\_component\_name(component at “component\_id”, owner).
  - If not Platform.db.exists(“Studio Component”, name).
    - Evaluate new\_component\_from\_copy(component, owner).insert().
    - Continue with the next iteration or loop test.
  - Set existing from Platform.get\_doc(“Studio Component”, name).
  - If component\_signature(existing) equals component\_signature(component).
    - Continue with the next iteration or loop test.
  - Evaluate conflicts.append(mapping(“name” → component at “component\_name”, “existing” → get\_component\_copy(existing), “copied” → get\_component\_copy(component))).
  - If overwrite\_conflicts.
    - Evaluate update\_component\_from\_copy(existing, component).save().
- Return conflicts.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Component”, ptype = “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L30)

<a id="op-f0b218c86f4a93"></a>
### Component signature

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_component_signature`

**Inputs** component.

**Explicit results** mapping(“component\_name” → component.get(“component\_name”), “block” → Platform.parse\_json(component.get(“block”)), “script” → (component.get(“script”) or empty text), “is\_disabled” → cint(component.get(“is ….

**Local steps**

- Return mapping(“component\_name” → component.get(“component\_name”), “block” → Platform.parse\_json(component.get(“block”)), “script” → (component.get(“script”) or empty text), “is\_disabled” → cint(component.get(“is ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“script”) → empty text.
  - Draw row from (component.get(“inputs”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“inputs”) → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L29)

<a id="op-edb5672d91ebd5"></a>
### Get component copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_get_component_copy`

**Inputs** component.

**Explicit results** mapping(“name” → component.get(“name”), “component\_id” → component.get(“component\_id”), “studio\_app” → component.get(“studio\_app”), “component\_name” → component.get(“component\_name”), …).

**Local steps**

- Return mapping(“name” → component.get(“name”), “component\_id” → component.get(“component\_id”), “studio\_app” → component.get(“studio\_app”), “component\_name” → component.get(“component\_name”), …).
  - Draw row from (component.get(“inputs”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“inputs”) → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L35)

<a id="op-668bd4945fb98f"></a>
### Validate component copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_validate_component_copy`

**Inputs** component.

**Explicit failure paths** validation helper — translated “Invalid component in copied content.” · validation helper — translated “Invalid component definition in copied content.” · validation helper — translated “Invalid component script in copied content.” · validation helper — translated “Invalid component inputs in copied content.”.

**Local steps**

- If not isinstance(component, dict).
  - Call the validation error handler Platform.throw(translated “Invalid component in copied content.”).
- Evaluate validate\_file\_name(component.get(“component\_id”), translated “Invalid component ID in copied content.”).
- If (not isinstance(component.get(“component\_name”), str) or not isinstance(component.get(“block”), (str bitwise or dict))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(component.get(“component\_name”), str) → not isinstance(component.get(“block”), (str bitwise or dict)).
  - Call the validation error handler Platform.throw(translated “Invalid component definition in copied content.”).
- If not isinstance((component.get(“script”) or empty text), str).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“script”) → empty text.
  - Call the validation error handler Platform.throw(translated “Invalid component script in copied content.”).
- If (not isinstance((component.get(“inputs”) or list()), list) or not all(generator of isinstance(row, dict) for row drawn from (nested operand in the contract.get(“inputs”) or list()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance((component.get(“inputs”) or list()), list) → not all(generator of isinstance(row, dict) for row drawn from (component.get(“inputs”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“inputs”) → list().
  - Draw row from (component.get(“inputs”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“inputs”) → list().
  - Call the validation error handler Platform.throw(translated “Invalid component inputs in copied content.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2070) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L47)

<a id="op-933d5ab5b99ca8"></a>
### New component from copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_new_component_from_copy`

**Inputs** component, studio\_app = no value.

**Record and data access** resolve a document from “Studio Component” via get\_doc.

**Explicit results** update\_component\_from\_copy(Platform.get\_doc(doctype = “Studio Component”, component\_id = component at “component\_id”, studio\_app = studio\_app), component).

**Local steps**

- Return update\_component\_from\_copy(Platform.get\_doc(doctype = “Studio Component”, component\_id = component at “component\_id”, studio\_app = studio\_app), component).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2062) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L39)

<a id="op-2519385d4a4f2e"></a>
### Update component from copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_update_component_from_copy`

**Inputs** doc, component.

**Explicit results** doc.

**Local steps**

- Set doc.component\_name from component at “component\_name”.
- Set doc.block from component at “block”.
- Set doc.script from component.get(“script”).
- Set doc.is\_disabled from component.get(“is\_disabled”).
- Evaluate doc.set(“inputs”, list of mapping(expand pick(row, COMPONENT\_INPUT\_FIELDS), “name” → no value) for row drawn from (component.get(“inputs”) or list())).
  - Draw row from (component.get(“inputs”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in component.get(“inputs”) → list().
- Return doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2069) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L46)

<a id="op-d24df8ee63a6ec"></a>
### New page from copy

`operation_foundation_binding_foundation_studio_doctype_studio_page_copy_paste_handler_new_page_from_copy`

**Inputs** app, copy.

**Record and data access** read “Studio Page” via exists · resolve a document from “Studio Page” via get\_doc.

**Explicit results** Platform.get\_doc(doctype = “Studio Page”, studio\_app = app.name, page\_title = title, tab\_title = copy.get(“tab\_title”), …).

**Local steps**

- Set title from copy.get(“page\_title”).
- If (title and Platform.db.exists(“Studio Page”, mapping(“studio\_app” → app.name, “page\_title” → title))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in title → Platform.db.exists(“Studio Page”, mapping(“studio\_app” → app.name, “page\_title” → title)).
  - Set title from append\_number\_if\_name\_exists(“Studio Page”, formatted text {title} Copy, fieldname = “page\_title”, separator = one space, filters = mapping(“studio\_app” → app.name)).
- Return Platform.get\_doc(doctype = “Studio Page”, studio\_app = app.name, page\_title = title, tab\_title = copy.get(“tab\_title”), …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2063) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L40)

<a id="op-a4909efdc846a0"></a>
### Studio Page.autoname

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_autoname`

**Inputs** self.

**Local steps**

- If not self.name.
  - Set self.name from formatted text page-{Platform.generate\_hash(length = 8)}.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 8).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2080) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L57)

<a id="op-d2b07a22602433"></a>
### Studio Page.before insert

`operation_foundation_binding_foundation_studio_doctype_studio_page_studio_page_studiopage_before_insert`

**Inputs** self.

**Local steps**

- If not self.blocks.
  - Set self.blocks from “&#91;&#93;”.
- If not self.page\_title.
  - Set self.page\_title from “My Page”.
  - Set self.page\_title from append\_number\_if\_name\_exists(“Studio Page”, self.page\_title, fieldname = “page\_title”, filters = mapping(“studio\_app” → self.studio\_app)).
- If not self.route.
  - Set self.route from formatted text {camel\_case\_to\_kebab\_case(self.page\_title, true)}-{Platform.generate\_hash(length = 4)}.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 4).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L2083) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L60)
