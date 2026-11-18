# Forms, reports and navigation · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Address template

[Record definition](../../../../data/record-types/address_template.json)

<a id="op-4e4ae449076497"></a>
### Get default address template

`operation_foundation_contacts_record_definitions_address_template_business_behavior_get_default_address_template`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** (Path(\_\_file\_\_).parent ÷ “address\_template.jinja”).read\_text().

**Local steps**

- Bind dependencies Path.
- Return (Path(\_\_file\_\_).parent ÷ “address\_template.jinja”).read\_text().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L7381) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L823)

## Report · Addresses and contacts

<a id="op-985855f58bad4c"></a>
### Execute

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(get\_columns(filters), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L418) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L875)

<a id="op-c45ffd79610e73"></a>
### Get columns

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(formatted text {translated reference\_doctype}:Link/{reference\_doctype}, translated “Address Line 1”, translated “Address Line 2”, translated “City”, …).

**Local steps**

- Set reference\_doctype from filters.get(“reference\_doctype”).
- Return list(formatted text {translated reference\_doctype}:Link/{reference\_doctype}, translated “Address Line 1”, translated “Address Line 2”, translated “City”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L155) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L876)

<a id="op-6bc172c75f8696"></a>
### Get data

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_get_data`

**Inputs** filters.

**Explicit results** get\_reference\_addresses\_and\_contact(reference\_doctype, reference\_name).

**Local steps**

- Set reference\_doctype from filters.get(“reference\_doctype”).
- Set reference\_name from filters.get(“reference\_name”).
- Return get\_reference\_addresses\_and\_contact(reference\_doctype, reference\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L909) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L877)

<a id="op-dccd1a3642f08f"></a>
### Get reference addresses and contact

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_get_reference_addresses_and_contact`

**Inputs** reference\_doctype, reference\_name.

**Record and data access** read reference\_doctype via get\_list.

**Explicit results** list() · data.

**Local steps**

- Set data from list().
- Set filters from no value.
- Set reference\_details from Platform.\_dict().
- If not reference\_doctype.
  - Return list().
- If reference\_name.
  - Set filters from mapping(“name” → reference\_name).
- Set reference\_list from list of d at 0 for d drawn from Platform.get\_list(reference\_doctype, filters = filters, fields = list(“name”), as\_list = true).
  - Draw d from Platform.get\_list(reference\_doctype, filters = filters, fields = list(“name”), as\_list = true).
- For each d in reference\_list.
  - Evaluate reference\_details.setdefault(d, Platform.\_dict()).
- Set reference\_details from get\_reference\_details(reference\_doctype, “Address”, reference\_list, reference\_details).
- Set reference\_details from get\_reference\_details(reference\_doctype, “Contact”, reference\_list, reference\_details).
- For each tuple(reference\_name, details) in reference\_details.items().
  - Set addresses from details.get(“address”, list()).
  - Set contacts from details.get(“contact”, list()).
  - If not any(list(addresses, contacts)).
    - Set result from list(reference\_name).
    - Evaluate result.extend(add\_blank\_columns\_for(“Address”)).
    - Evaluate result.extend(add\_blank\_columns\_for(“Contact”)).
    - Evaluate data.append(result).
  - Otherwise.
    - Set addresses from list(map(list, addresses)).
    - Set contacts from list(map(list, contacts)).
    - Set max\_length from max(len(addresses), len(contacts)).
    - For each idx in range(0, max\_length).
      - Set result from list(reference\_name).
      - Evaluate result.extend(addresses at idx when idx &lt; len(addresses), otherwise add\_blank\_columns\_for(“Address”)).
        - Value choice on idx &lt; len(addresses) — true gives addresses at idx, false gives add\_blank\_columns\_for(“Address”).
      - Evaluate result.extend(contacts at idx when idx &lt; len(contacts), otherwise add\_blank\_columns\_for(“Contact”)).
        - Value choice on idx &lt; len(contacts) — true gives contacts at idx, false gives add\_blank\_columns\_for(“Contact”).
      - Evaluate data.append(result).
- Return data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L1033) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L878)

<a id="op-ea9e1900b3ad45"></a>
### Get reference details

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_get_reference_details`

**Inputs** reference\_doctype, doctype, reference\_list, reference\_details.

**Record and data access** read doctype via get\_list.

**Explicit results** reference\_details.

**Explicit failure paths** validation helper — translated “No records present in {0}”.format(reference\_doctype).

**Local steps**

- Set filters from list(list(“Dynamic Link”, “link\_doctype”, “=”, reference\_doctype), list(“Dynamic Link”, “link\_name”, “in”, reference\_list)).
- Set fields from list(“′tabDynamic Link′.link\_name”, expanded field\_map.get(doctype, list())).
- Set records from Platform.get\_list(doctype, filters = filters, fields = fields, as\_list = true).
- Set temp\_records from list of d at slice 1 to no value for d drawn from records.
  - Draw d from records.
- If not reference\_list.
  - Call the validation error handler Platform.throw(translated “No records present in {0}”.format(reference\_doctype)).
- Set reference\_details at reference\_list at 0 at Platform.scrub(doctype) from temp\_records.
- Return reference\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L2056) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L879)

<a id="op-304f034003b107"></a>
### Add blank columns for

`operation_foundation_contacts_report_addresses_and_contacts_business_behavior_add_blank_columns_for`

**Inputs** doctype.

**Explicit results** list of empty text for field drawn from field\_map.get(doctype, list()).

**Local steps**

- Return list of empty text for field drawn from field\_map.get(doctype, list()).
  - Draw field from field\_map.get(doctype, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L2464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L874)

## Service · Api

<a id="op-c9099c042fe6a3"></a>
### Run

`operation_foundation_binding_foundation_studio_ai_api_run`

**Inputs** prompt, page\_context, page\_id, model = no value, selected\_block\_ids = no value, image\_data = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)), has\_page\_write\_perm().

**State and service calls** enqueue with run\_agent\_job.

**Explicit results** mapping(“status” → “busy”, “message” → translated “Another AI request is still processing. Please wait.”) · mapping(“status” → “accepted”, “session\_id” → session.name).

**Explicit failure paths** validation helper — translated “Invalid page context JSON” · validation helper — translated “OpenRouter API key is not configured. Please set it in Studio Settings.”.

**Local steps**

- Evaluate logger.info(formatted text run: page\_id={page\_id}, model={model}).
- Attempt the following.
  - Evaluate json.loads(page\_context).
- On failure (tuple(json.JSONDecodeError, TypeError)).
  - Call the validation error handler Platform.throw(translated “Invalid page context JSON”).
- Set resolved\_model from (model or ModelRegistry.DEFAULT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in model → ModelRegistry.DEFAULT.
- Set api\_key from llm.get\_api\_key().
- If not api\_key.
  - Call the validation error handler Platform.throw(translated “OpenRouter API key is not configured. Please set it in Studio Settings.”).
- Set image\_url from BlockCodec.validate\_image\_data(image\_data) when image\_data, otherwise no value.
  - Value choice on image\_data — true gives BlockCodec.validate\_image\_data(image\_data), false gives no value.
- Set session from AISession.get\_or\_create(page\_id, resolved\_model).
- Set job\_id from formatted text studio-ai-{session.name}.
- If (AISession.is\_session\_running(session.name) or is\_job\_enqueued(job\_id)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in AISession.is\_session\_running(session.name) → is\_job\_enqueued(job\_id).
  - Set Platform.local.response.http\_status\_code from 429.
  - Return mapping(“status” → “busy”, “message” → translated “Another AI request is still processing. Please wait.”).
- Set msg\_meta from mapping(“attachedImageUrl” → image\_url) when image\_url, otherwise no value.
  - Value choice on image\_url — true gives mapping(“attachedImageUrl” → image\_url), false gives no value.
- Evaluate session.append\_message(“user”, prompt, message\_type = “chat”, task\_type = “agent”, metadata = msg\_meta).
- Evaluate Platform.enqueue(run\_agent\_job, queue = “long”, timeout = 600, job\_id = job\_id, deduplicate = true, …).
- Set Platform.local.response.http\_status\_code from 202.
- Return mapping(“status” → “accepted”, “session\_id” → session.name).

**Values supplied outside this operation** service or queued work from Platform.enqueue(run\_agent\_job, queue = “long”, timeout = 600, job\_id = job\_id, deduplicate = true, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1821)

<a id="op-8b0244facbcb36"></a>
### Cancel

`operation_foundation_binding_foundation_studio_ai_api_cancel`

**Inputs** session\_id.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Explicit results** mapping(“status” → “ok”).

**Local steps**

- If session\_id.
  - Evaluate Platform.cache.set\_value(formatted text studio\_ai\_cancel:{session\_id}, “1”, expires\_in\_sec = 300).
- Return mapping(“status” → “ok”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1817)

<a id="op-d0e0fb8afcea13"></a>
### Get ai session

`operation_foundation_binding_foundation_studio_ai_api_get_ai_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** page\_id, model.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1819)

<a id="op-b6c4205d0307d4"></a>
### Clear ai session

`operation_foundation_binding_foundation_studio_ai_api_clear_ai_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** page\_id.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1818)

<a id="op-a3e7936f008c55"></a>
### Parse block ids

`operation_foundation_binding_foundation_studio_ai_api_parse_block_ids`

**Inputs** selected\_block\_ids.

**Declared result** list at str.

**Explicit results** list() · selected\_block\_ids when isinstance(selected\_block\_ids, list), otherwise list().

**Local steps**

- If isinstance(selected\_block\_ids, str).
  - Attempt the following.
    - Set selected\_block\_ids from json.loads(selected\_block\_ids).
  - On failure (tuple(json.JSONDecodeError, TypeError)).
    - Return list().
- Return selected\_block\_ids when isinstance(selected\_block\_ids, list), otherwise list().
  - Value choice on isinstance(selected\_block\_ids, list) — true gives selected\_block\_ids, false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1820)

<a id="op-b8d3ba27e803e1"></a>
### Get app boot

`operation_foundation_binding_foundation_studio_api_get_app_boot`

**Inputs** app\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Studio App” via get\_doc.

**Explicit results** app.get\_boot().

**Local steps**

- Set app from Platform.get\_doc(“Studio App”, app\_name).
- Evaluate app.check\_permission(“read”).
- Return app.get\_boot().

**Values supplied outside this operation** effective access from app.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L210) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1873)

<a id="op-621a2d405e12a9"></a>
### Get doctype fields

`operation_foundation_binding_foundation_studio_api_get_doctype_fields`

**Inputs** doctype, with\_standard\_fields = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** fields.

**Local steps**

- Evaluate Platform.has\_permission(doctype, ptype = “read”, throw = true).
- Set excluded\_fieldtypes from ((set(no\_value\_fields) bitwise or set(display\_fieldtypes)) − set(table\_fields)).
- Set fields from list of field for field drawn from Platform.get\_meta(doctype).fields where field.fieldtype does not belong to excluded\_fieldtypes.
  - Draw field from Platform.get\_meta(doctype).fields, keep a combination only if (field.fieldtype does not belong to excluded\_fieldtypes).
- Set standard\_fields from list(Platform.\_dict(fieldname = “name”, fieldtype = “Data”, label = “ID”)).
- If sbool(with\_standard\_fields).
  - Update standard\_fields using + get\_meta\_fields(doctype).
- Set existing\_fieldnames from set of field.fieldname for field drawn from fields.
  - Draw field from fields.
- Update fields using + list of field for field drawn from standard\_fields where field.fieldname does not belong to existing\_fieldnames.
  - Draw field from standard\_fields, keep a combination only if (field.fieldname does not belong to existing\_fieldnames).
- Return fields.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype = “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L216) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1879)

<a id="op-e4c73c2f991d91"></a>
### Get meta fields

`operation_foundation_binding_foundation_studio_api_get_meta_fields`

**Inputs** doctype.

**Declared result** list at Platform.\_dict.

**Explicit results** fields.

**Local steps**

- Set fields from list of Platform.\_dict(field) for field drawn from std\_fields where field at “fieldname” differs from “name”.
  - Draw field from std\_fields, keep a combination only if (field at “fieldname” differs from “name”).
- If Platform.get\_meta(doctype).istable.
  - Update fields using + list of Platform.\_dict(fieldname = fieldname, fieldtype = “Data”) for fieldname drawn from child\_table\_fields.
    - Draw fieldname from child\_table\_fields.
- Return fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L217) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1880)

<a id="op-980f9e3bb8bed1"></a>
### Get whitelisted methods

`operation_foundation_binding_foundation_studio_api_get_whitelisted_methods`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1885)

<a id="op-2f8641ce04adf1"></a>
### Get sort fields

`operation_foundation_binding_foundation_studio_api_get_sort_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** fields.

**Local steps**

- Evaluate Platform.has\_permission(doctype, ptype = “read”, throw = true).
- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where field.fieldtype does not belong to no\_value\_fields.
  - Draw field from fields, keep a combination only if (field.fieldtype does not belong to no\_value\_fields).
- Set fields from list of mapping(“label” → translated field.label, “value” → field.fieldname, “fieldname” → field.fieldname) for field drawn from fields where (field.label and field.fieldname).
  - Draw field from fields, keep a combination only if ((field.label and field.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.label → field.fieldname.
- Set standard\_fields from list(mapping(“label” → “Created On”, “fieldname” → “creation”), mapping(“label” → “Last Modified”, “fieldname” → “modified”), mapping(“label” → “Modified By”, “fieldname” → “modified\_by”), mapping(“label”  ….
- For each field in standard\_fields.
  - Set field at “label” from translated field at “label”.
  - Set field at “value” from field at “fieldname”.
  - Evaluate fields.append(field).
- Return fields.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype = “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1881)

<a id="op-8f6fd06029b73d"></a>
### Get component definition

`operation_foundation_binding_foundation_studio_api_get_component_definition`

**Inputs** component.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Declared result** dict.

**Explicit results** components.get\_component\_definition(component).

**Local steps**

- Return components.get\_component\_definition(component).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L212) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1875)

<a id="op-fca4eec41f787a"></a>
### Can use flow

`operation_foundation_binding_foundation_studio_api_can_use_flow`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Explicit results** bool(Platform.has\_permission(“Flow Session”, “read”)).

**Local steps**

- Return bool(Platform.has\_permission(“Flow Session”, “read”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Session”, “read”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1868)

<a id="op-96a8989301ce51"></a>
### Check app permission

`operation_foundation_binding_foundation_studio_api_check_app_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1869)

<a id="op-aa2ea782f53cfd"></a>
### Get custom vue components

`operation_foundation_binding_foundation_studio_api_get_custom_vue_components`

**Inputs** Platform\_app, studio\_app.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list at dict.

**Explicit results** list() · components.

**Local steps**

- Evaluate Platform.has\_permission(“Studio Page”, ptype = “read”, throw = true).
- Evaluate validate\_installed\_app(Platform\_app).
- Set components from list().
- Set seen\_names from set().
- Set app\_folder from get\_export\_folder(Platform\_app, studio\_app).
- If app\_folder does not belong to get\_exported\_app\_folders(get\_studio\_folder(Platform\_app)).
  - Return list().
- Bind local operation has\_reserved\_name for subsequent calls.
- Bind local operation has\_conflicting\_name for subsequent calls.
- For each tuple(dirpath, \_dirnames, filenames) in os.walk(app\_folder).
  - For each filename in sorted(filenames).
    - If not filename.endswith(“.vue”).
      - Continue with the next iteration or loop test.
    - Set component\_name from filename at slice no value to negative 4.
    - If (has\_reserved\_name(component\_name) or has\_conflicting\_name(component\_name)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_reserved\_name(component\_name) → has\_conflicting\_name(component\_name).
      - Continue with the next iteration or loop test.
    - Evaluate seen\_names.add(component\_name).
    - Set file\_path from os.path.join(dirpath, filename).
    - Evaluate components.append(mapping(“component\_name” → component\_name, “studio\_app” → studio\_app, “file\_path” → file\_path, “studio\_file\_path” → os.path.relpath(file\_path, app\_folder))).
- Return components.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1876)

<a id="op-40cfee52e3949c"></a>
### Get custom vue components.has reserved name

`operation_foundation_binding_foundation_studio_api_get_custom_vue_components_has_reserved_name`

**Inputs** name.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If name belongs to STANDARD\_COMPONENT\_NAMES.
  - Evaluate Platform.log\_error(title = “Studio: Custom component name conflict”, message = formatted text Custom component '{component\_name}' in {Platform\_app}/{studio\_app} conflicts with a standard component. Skipping.).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L215) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1878)

<a id="op-eac520f4015817"></a>
### Get custom vue components.has conflicting name

`operation_foundation_binding_foundation_studio_api_get_custom_vue_components_has_conflicting_name`

**Inputs** name.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If name belongs to seen\_names.
  - Evaluate Platform.log\_error(title = “Studio: Duplicate custom component”, message = formatted text Custom component '{component\_name}' in {Platform\_app}/{studio\_app} conflicts with another component. Skipping.).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L214) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1877)

<a id="op-dd0539ad74cf93"></a>
### Get studio page scripts

`operation_foundation_binding_foundation_studio_api_get_studio_page_scripts`

**Inputs** Platform\_app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list() · scripts.

**Local steps**

- Evaluate validate\_installed\_app(Platform\_app).
- Set scripts from list().
- Set studio\_folder from get\_studio\_folder(Platform\_app).
- If not os.path.exists(studio\_folder).
  - Return list().
- For each studio\_app in sorted(os.listdir(studio\_folder)).
  - Set page\_folder from os.path.join(studio\_folder, studio\_app, “studio\_page”).
  - If not os.path.isdir(page\_folder).
    - Continue with the next iteration or loop test.
  - For each entry in sorted(os.listdir(page\_folder)).
    - Set page\_dir from os.path.join(page\_folder, entry).
    - If not os.path.isdir(page\_dir).
      - Continue with the next iteration or loop test.
    - Set file\_path from find\_script\_file(page\_dir, entry).
    - Set json\_path from os.path.join(page\_dir, formatted text {entry}.json).
    - If not (os.path.exists(file\_path) and os.path.exists(json\_path)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(file\_path) → os.path.exists(json\_path).
      - Continue with the next iteration or loop test.
    - Set page\_name from Platform.parse\_json(Platform.read\_file(json\_path)).get(“page\_name”).
    - If page\_name.
      - Evaluate scripts.append(mapping(“page\_name” → page\_name, “Platform\_app” → Platform\_app, “studio\_app” → studio\_app, “file\_path” → file\_path)).
- Return scripts.

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1884)
