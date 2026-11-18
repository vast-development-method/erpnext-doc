# Web content and issued documents · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Web form

[Record definition](../../../../data/record-types/web_form.json)

<a id="op-b0da0aa6c96c5e"></a>
### Delete multiple

`operation_foundation_website_record_definitions_web_form_business_behavior_delete_multiple`

**Inputs** web\_form\_name, docnames.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “DELETE”)), rate\_limit(key = “web\_form\_name”, limit = 999, seconds = 60).

**Record and data access** read web\_form.doc\_type via get\_value.

**State and service calls** request delete\_doc for web\_form.doc\_type.

**Explicit failure paths** Platform.PermissionError((“You do not have permisssion to delete ” + “, ”.join(restricted\_docnames))).

**Local steps**

- Set web\_form from Platform.get\_lazy\_doc(“Web Form”, web\_form\_name).
- Evaluate web\_form.raise\_if\_unpublished().
- Set docnames from json.loads(docnames).
- Set allowed\_docnames from list().
- Set restricted\_docnames from list().
- For each docname in docnames.
  - Require isinstance(docname, (str bitwise or int)) or raise an assertion failure.
  - Set owner from Platform.db.get\_value(web\_form.doc\_type, docname, “owner”).
  - If (Platform.session.user equals owner and web\_form.allow\_delete).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals owner → web\_form.allow\_delete.
    - Evaluate allowed\_docnames.append(docname).
  - Otherwise.
    - Evaluate restricted\_docnames.append(docname).
- For each docname in allowed\_docnames.
  - Evaluate Platform.delete\_doc(web\_form.doc\_type, docname, ignore\_permissions = true).
- If restricted\_docnames.
  - Raise Platform.PermissionError((“You do not have permisssion to delete ” + “, ”.join(restricted\_docnames))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L34) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1304)

<a id="op-0c1e8044bbfe49"></a>
### Check webform perm

`operation_foundation_website_record_definitions_web_form_business_behavior_check_webform_permission`

**Inputs** doctype, name.

**Explicit results** true.

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name).
- If hasattr(doc, “has\_webform\_permission”).
  - If doc.has\_webform\_permission().
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L5857) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1302)

<a id="op-92f4940bf3aacd"></a>
### Get web form filters

`operation_foundation_website_record_definitions_web_form_business_behavior_get_web_form_filters`

**Inputs** web\_form\_name.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), Platform.read\_only().

**Record and data access** resolve a document from “Web Form” via get\_doc.

**Explicit results** list of field for field drawn from web\_form.web\_form\_fields where field.show\_in\_filter.

**Local steps**

- Set web\_form from Platform.get\_doc(“Web Form”, web\_form\_name).
- Evaluate web\_form.raise\_if\_unpublished().
- Return list of field for field drawn from web\_form.web\_form\_fields where field.show\_in\_filter.
  - Draw field from web\_form.web\_form\_fields, keep a combination only if (field.show\_in\_filter).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L5982) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1311)

<a id="op-5c0ffb036ca079"></a>
### Get web form list

`operation_foundation_website_record_definitions_web_form_business_behavior_get_web_form_list`

**Inputs** web\_form, web\_form\_request\_key, limit\_start = 0, limit = 20, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(key = “web\_form”, limit = 10, seconds = 60), Platform.read\_only().

**Declared result** list at dict.

**Record and data access** read web\_form\_doc.doc\_type via get\_list.

**Explicit results** list() · Platform.get\_list(web\_form\_doc.doc\_type, fields = fields, filters = filters, limit\_start = cint(limit\_start), limit\_page\_length = min(cint(limit), 100), …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You must login to use this form” · validation helper with Platform.PermissionError — translated “Not permitted” · validation helper with Platform.PermissionError — translated “Invalid Web Form Request”.

**Local steps**

- Set web\_form\_doc from Platform.get\_lazy\_doc(“Web Form”, web\_form).
- Evaluate web\_form\_doc.raise\_if\_unpublished().
- If (web\_form\_doc.login\_required and Platform.session.user equals “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form\_doc.login\_required → Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “You must login to use this form”, Platform.PermissionError).
- If not web\_form\_doc.show\_list.
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set web\_form\_request from web\_form\_doc.get\_web\_form\_request(web\_form\_request\_key, allow\_used = true).
- If not web\_form\_request.
  - Call the validation error handler Platform.throw(translated “Invalid Web Form Request”, Platform.PermissionError).
- Set reference\_names from list of row.link\_name for row drawn from web\_form\_request.references.
  - Draw row from web\_form\_request.references.
- If not reference\_names.
  - Return list().
- Set meta from Platform.get\_meta(web\_form\_doc.doc\_type).
- Set filters from mapping().
- For each tuple(fieldname, raw\_value) in kwargs.items().
  - If not meta.has\_field(fieldname).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set filters at fieldname from json.loads(raw\_value).
  - On failure (tuple(TypeError, ValueError)).
    - Set filters at fieldname from raw\_value.
- Set filters at “name” from list(“in”, reference\_names).
- Set fields from get\_web\_form\_list\_fields(web\_form\_doc, web\_form\_request\_key).
- Return Platform.get\_list(web\_form\_doc.doc\_type, fields = fields, filters = filters, limit\_start = cint(limit\_start), limit\_page\_length = min(cint(limit), 100), …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L6159) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1312)

<a id="op-ba516c680b7f2d"></a>
### Get form data

`operation_foundation_website_record_definitions_web_form_business_behavior_get_form_data`

**Inputs** doctype, docname = no value, web\_form\_name = no value, web\_form\_request\_key = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), Platform.read\_only().

**Record and data access** resolve a document from “Web Form” via get\_doc · read doctype via get\_value · resolve a document from doctype via get\_doc.

**Explicit results** out.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted” · validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set web\_form from Platform.get\_doc(“Web Form”, web\_form\_name).
- Evaluate web\_form.raise\_if\_unpublished().
- If (web\_form.login\_required and Platform.session.user equals “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.login\_required → Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- If getattr(web\_form, “key\_required”, false).
  - Evaluate web\_form.get\_web\_form\_request(web\_form\_request\_key, docname = docname, allow\_used = true).
- Set out from Platform.\_dict().
- Set out.web\_form from web\_form.
- If (Platform.session.user differs from “Guest” and not docname and not web\_form.allow\_multiple).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from “Guest” → not docname → not web\_form.allow\_multiple.
  - Set docname from Platform.db.get\_value(doctype, mapping(“owner” → Platform.session.user), “name”).
- If docname.
  - Set doc from Platform.get\_doc(doctype, docname).
  - If web\_form.has\_web\_form\_permission(doctype, docname, ptype = “read”).
    - Set out.doc from doc.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- For each field in out.web\_form.web\_form\_fields.
  - If field.fieldtype equals “Table”.
    - Set field.fields from get\_in\_list\_view\_fields(field.options, web\_form\_name, web\_form\_request\_key, docname, allow\_read\_on\_all\_link\_options = field.allow\_read\_on\_all\_link\_options, apply\_user\_permissions = field.apply\_user\_permissions).
    - Evaluate out.update(mapping(field.fieldname → field.fields)).
  - If field.fieldtype equals “Table MultiSelect”.
    - Set field.fields from get\_table\_multiselect\_fields(field.options, web\_form\_name, web\_form\_request\_key, docname, …).
  - If field.fieldtype equals “Link”.
    - Evaluate process\_link\_field(field, web\_form\_name, web\_form\_request\_key, docname, allow\_read\_on\_all\_link\_options = field.allow\_read\_on\_all\_link\_options, apply\_user\_permissions = field.apply\_user\_permissions).
- Return out.

**Values supplied outside this operation** selected callable from getattr(web\_form, “key\_required”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L35) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1306)

<a id="op-621fff1c044c64"></a>
### Get web form list fields

`operation_foundation_website_record_definitions_web_form_business_behavior_get_web_form_list_fields`

**Inputs** web\_form\_doc, web\_form\_request\_key = no value.

**Declared result** list at str.

**State and service calls** call insert on fields.

**Explicit results** fields.

**Local steps**

- If web\_form\_doc.list\_columns.
  - Set fields from list of col.fieldname for col drawn from web\_form\_doc.list\_columns.
    - Draw col from web\_form\_doc.list\_columns.
- Otherwise.
  - Set fields from list of col at “fieldname” for col drawn from get\_in\_list\_view\_fields(web\_form\_doc.doc\_type, web\_form\_doc.name, web\_form\_request\_key).
    - Draw col from get\_in\_list\_view\_fields(web\_form\_doc.doc\_type, web\_form\_doc.name, web\_form\_request\_key).
- If “name” does not belong to fields.
  - Evaluate fields.insert(0, “name”).
- Return fields.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L905) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1313)

<a id="op-34b294a4f26581"></a>
### Get in list view fields

`operation_foundation_website_record_definitions_web_form_business_behavior_get_in_list_view_fields`

**Inputs** doctype, web\_form\_name = no value, web\_form\_request\_key = no value, docname = no value, allow\_read\_on\_all\_link\_options = false, apply\_user\_permissions = false.

**Explicit results** list of get\_field\_df(f) for f drawn from fields.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set fields from list().
- If meta.title\_field.
  - Evaluate fields.append(meta.title\_field).
- Otherwise.
  - Evaluate fields.append(“name”).
- If meta.has\_field(“status”).
  - Evaluate fields.append(“status”).
- Update fields using + list of df.fieldname for df drawn from meta.fields where (df.in\_list\_view and df.fieldname does not belong to fields).
  - Draw df from meta.fields, keep a combination only if ((df.in\_list\_view and df.fieldname does not belong to fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.in\_list\_view → df.fieldname does not belong to fields.
- Bind local operation get\_field\_df for subsequent calls.
- Return list of get\_field\_df(f) for f drawn from fields.
  - Draw f from fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L36) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1307)

<a id="op-2485e6838af41f"></a>
### Get in list view fields.get field df

`operation_foundation_website_record_definitions_web_form_business_behavior_get_in_list_view_fields_get_field_df`

**Inputs** fieldname.

**Explicit results** mapping(“label” → “Name”, “fieldname” → “name”, “fieldtype” → “Data”, “hidden” → 1) · df.

**Local steps**

- If fieldname equals “name”.
  - Return mapping(“label” → “Name”, “fieldname” → “name”, “fieldtype” → “Data”, “hidden” → 1).
- Set df from meta.get\_field(fieldname).as\_dict().
- If (df.get(“options”) and df.get(“fieldtype”) equals “Link”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“options”) → df.get(“fieldtype”) equals “Link”.
  - Evaluate process\_link\_field(df, web\_form\_name, web\_form\_request\_key, docname, allow\_read\_on\_all\_link\_options = allow\_read\_on\_all\_link\_options, apply\_user\_permissions = apply\_user\_permissions).
- Return df.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L37) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1308)

<a id="op-21c9fa93d4f357"></a>
### Get table multiselect fields

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_get_table_multiselect_fields`

**Inputs** child\_doctype, web\_form\_name = no value, web\_form\_request\_key = no value, docname = no value, allow\_read\_on\_all = false.

**Explicit results** list() · list(df).

**Local steps**

- Attempt the following.
  - Set meta from Platform.get\_meta(child\_doctype).
- On failure (Platform.DoesNotExistError).
  - Return list().
- Set link\_field from next(generator of df for df drawn from meta.fields where df.fieldtype equals “Link”, no value).
  - Draw df from meta.fields, keep a combination only if (df.fieldtype equals “Link”).
- If not link\_field.
  - Return list().
- Set df from link\_field.as\_dict().
- If web\_form\_name.
  - Set df.link\_options from get\_link\_options(web\_form\_name, df.options, allow\_read\_on\_all, web\_form\_request\_key, …).
- Return list(df).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L71) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L464)

<a id="op-90236a63df3dc1"></a>
### Is guest key web form

`operation_foundation_website_record_definitions_web_form_business_behavior_is_guest_key_web_form`

**Inputs** web\_form.

**Explicit results** (cint(web\_form.key\_required) and not cint(web\_form.login\_required)).

**Local steps**

- Return (cint(web\_form.key\_required) and not cint(web\_form.login\_required)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(web\_form.key\_required) → not cint(web\_form.login\_required).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L2049) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1316)

<a id="op-66b704726bd464"></a>
### Ensure guest key link doctype allowed

`operation_foundation_website_record_definitions_web_form_business_behavior_ensure_guest_key_link_record_type_allowed`

**Inputs** web\_form, link\_doctype.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You don't have permission to access the {0} DocType.”.format(link\_doctype).

**Local steps**

- If not is\_guest\_key\_web\_form(web\_form).
  - Return no value.
- If not Platform.has\_permission(link\_doctype, “read”, user = “Guest”).
  - Call the validation error handler Platform.throw(translated “You don't have permission to access the {0} DocType.”.format(link\_doctype), Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(link\_doctype, “read”, user = “Guest”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L2136) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1305)

<a id="op-e4719622097dc1"></a>
### Has link option

`operation_foundation_website_record_definitions_web_form_business_behavior_has_link_option`

**Inputs** fields, doctype.

**Explicit results** true · false.

**Local steps**

- For each f in fields.
  - If f.options equals doctype.
    - Return true.
  - If (f.fieldtype belongs to tuple(“Table”, “Table MultiSelect”) and f.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.fieldtype belongs to tuple(“Table”, “Table MultiSelect”) → f.options.
    - Set child\_doctype from f.options.
    - If (not isinstance(child\_doctype, str) or not child\_doctype.strip()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(child\_doctype, str) → not child\_doctype.strip().
      - Continue with the next iteration or loop test.
    - Attempt the following.
      - Set child\_table\_fields from Platform.get\_meta(child\_doctype).fields.
    - On failure (Exception).
      - Continue with the next iteration or loop test.
    - For each child\_field in child\_table\_fields.
      - If getattr(child\_field, “options”, no value) equals doctype.
        - Return true.
- Return false.

**Values supplied outside this operation** selected callable from getattr(child\_field, “options”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L40) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1315)

<a id="op-6e726b6ec0ecba"></a>
### Get link options

`operation_foundation_website_record_definitions_web_form_business_behavior_get_link_options`

**Inputs** web\_form\_name, doctype, allow\_read\_on\_all\_link\_options = false, web\_form\_request\_key = no value, docname = no value, apply\_user\_permissions = false, ignore\_user\_permissions = false.

**Record and data access** resolve a document from “Web Form” via get\_cached\_doc · read doctype via get\_all.

**Explicit results** json.dumps(link\_options, default = str) · list of mapping(“value” → row.value, “label” → translated row.value) for row drawn from link\_options · whitespace '\\n'.join(list of doc.value for doc drawn from link\_options).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You must be logged in to use this form.” · validation helper with Platform.PermissionError — translated “You don't have permission to access the {0} DocType.”.format(doctype).

**Local steps**

- Set web\_form from Platform.get\_cached\_doc(“Web Form”, web\_form\_name).
- If (web\_form.login\_required and Platform.session.user equals “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.login\_required → Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “You must be logged in to use this form.”, Platform.PermissionError).
- If getattr(web\_form, “key\_required”, false).
  - Evaluate get\_web\_form\_request(web\_form.name, web\_form\_request\_key, required = true, allow\_used = true).
- Evaluate ensure\_guest\_key\_link\_doctype\_allowed(web\_form, doctype).
- If (not web\_form.published or not has\_link\_option(web\_form.web\_form\_fields, doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not web\_form.published → not has\_link\_option(web\_form.web\_form\_fields, doctype).
  - Call the validation error handler Platform.throw(translated “You don't have permission to access the {0} DocType.”.format(doctype), Platform.PermissionError).
- Set tuple(link\_options, filters) from tuple(list(), list()).
- If (web\_form.login\_required and not allow\_read\_on\_all\_link\_options).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.login\_required → not allow\_read\_on\_all\_link\_options.
  - Evaluate filters.append(list(“owner”, “=”, Platform.session.user)).
- If (apply\_user\_permissions and not ignore\_user\_permissions and allowed\_docs bound to get\_permitted\_link\_values(web\_form, doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in apply\_user\_permissions → not ignore\_user\_permissions → allowed\_docs bound to get\_permitted\_link\_values(web\_form, doctype).
  - Evaluate filters.append(list(“name”, “in”, allowed\_docs)).
- Set fields from list(“name as value”).
- Set meta from Platform.get\_meta(doctype).
- Set show\_title\_field from (meta.title\_field and meta.show\_title\_field\_in\_link).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.title\_field → meta.show\_title\_field\_in\_link.
- If show\_title\_field.
  - Evaluate fields.append(formatted text {meta.title\_field} as label).
- Set link\_options from Platform.get\_all(doctype, filters = filters, fields = fields).
- For each row in link\_options.
  - Set row.value from cstr(row.value).
  - If show\_title\_field.
    - Set row.label from cstr(row.label).
- If show\_title\_field.
  - If meta.translated\_doctype.
    - Set link\_options from list of mapping(“value” → row.value, “label” → translated row.label) for row drawn from link\_options.
      - Draw row from link\_options.
  - Return json.dumps(link\_options, default = str).
- Otherwise.
  - If meta.translated\_doctype.
    - Return list of mapping(“value” → row.value, “label” → translated row.value) for row drawn from link\_options.
      - Draw row from link\_options.
  - Return whitespace '\\n'.join(list of doc.value for doc drawn from link\_options).
    - Draw doc from link\_options.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Web Form”, web\_form\_name) · selected callable from getattr(web\_form, “key\_required”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L38) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1309)

<a id="op-15c4004e3fbb5e"></a>
### Get permitted link values

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_get_permitted_link_values`

**Inputs** web\_form, link\_doctype.

**Explicit results** get\_allowed\_docs\_for\_doctype(get\_user\_permissions(Platform.session.user).get(link\_doctype, list()), web\_form.doc\_type).

**Local steps**

- Return get\_allowed\_docs\_for\_doctype(get\_user\_permissions(Platform.session.user).get(link\_doctype, list()), web\_form.doc\_type).

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L70) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L463)

<a id="op-039e03511907a1"></a>
### Get published web forms

`operation_foundation_website_record_definitions_web_form_business_behavior_get_published_web_forms`

**Inputs** no declared parameters.

**Wrappers, in declaration order** redis\_cache(ttl = (60 × 60)).

**Declared result** list at dict.

**Record and data access** read “Web Form” via get\_all.

**Explicit results** Platform.get\_all(“Web Form”, list(“name”, “title”, “route”, “modified”, …), mapping(“published” → 1)).

**Local steps**

- Return Platform.get\_all(“Web Form”, list(“name”, “title”, “route”, “modified”, …), mapping(“published” → 1)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L39) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1310)

## Service · Web form

<a id="op-9c626772de4313"></a>
### Extract

`operation_foundation_gettext_extractors_web_form_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- If data.get(“doctype”) differs from “Web Form”.
  - Return no value.
- Set web\_form\_name from data.get(“name”).
- If title bound to data.get(“title”).
  - yield tuple(get\_line\_number(text, “title”, title), “\_”, title, list(formatted text Title of the {web\_form\_name} Web Form)).
- If introduction\_text bound to data.get(“introduction\_text”).
  - yield tuple(get\_line\_number(text, “introduction\_text”, introduction\_text), “\_”, introduction\_text, list(formatted text Introduction text of the {web\_form\_name} Web Form)).
- If success\_message bound to data.get(“success\_message”).
  - yield tuple(get\_line\_number(text, “success\_message”, success\_message), “\_”, success\_message, list(formatted text Success message of the {web\_form\_name} Web Form)).
- If success\_title bound to data.get(“success\_title”).
  - yield tuple(get\_line\_number(text, “success\_title”, success\_title), “\_”, success\_title, list(formatted text Success title of the {web\_form\_name} Web Form)).
- If list\_title bound to data.get(“list\_title”).
  - yield tuple(get\_line\_number(text, “list\_title”, list\_title), “\_”, list\_title, list(formatted text List title of the {web\_form\_name} Web Form)).
- If button\_label bound to data.get(“button\_label”).
  - yield tuple(get\_line\_number(text, “button\_label”, button\_label), “\_”, button\_label, list(formatted text Button label of the {web\_form\_name} Web Form)).
- If meta\_title bound to data.get(“meta\_title”).
  - yield tuple(get\_line\_number(text, “meta\_title”, meta\_title), “\_”, meta\_title, list(formatted text Meta title of the {web\_form\_name} Web Form)).
- If meta\_description bound to data.get(“meta\_description”).
  - yield tuple(get\_line\_number(text, “meta\_description”, meta\_description), “\_”, meta\_description, list(formatted text Meta description of the {web\_form\_name} Web Form)).
- For each field in data.get(“web\_form\_fields”, list()).
  - If label bound to field.get(“label”).
    - yield tuple(get\_line\_number(text, “label”, label), “\_”, label, list(formatted text Label of a field in the {web\_form\_name} Web Form)).
  - If description bound to field.get(“description”).
    - yield tuple(get\_line\_number(text, “description”, description), “\_”, description, list(formatted text Description of a field in the {web\_form\_name} Web Form)).
  - If (field.get(“fieldtype”) equals “Select” and options bound to field.get(“options”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.get(“fieldtype”) equals “Select” → options bound to field.get(“options”).
    - Set skip\_options from (web\_form\_name equals “edit-profile” and field.get(“fieldname”) equals “time\_zone”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form\_name equals “edit-profile” → field.get(“fieldname”) equals “time\_zone”.
    - If (isinstance(options, str) and not skip\_options).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(options, str) → not skip\_options.
      - Set option\_list from options.split(whitespace '\\n') when whitespace '\\n' belongs to options, otherwise list(options).
        - Value choice on whitespace '\\n' belongs to options — true gives options.split(whitespace '\\n'), false gives list(options).
      - For each option in option\_list.
        - If option.strip().
          - yield tuple(get\_line\_number(text, “options”, options), “\_”, option.strip(), list(formatted text Option in a Select field in the {web\_form\_name} Web Form)).
- For each column in data.get(“list\_columns”, list()).
  - If (isinstance(column, dict) and label bound to column.get(“label”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(column, dict) → label bound to column.get(“label”).
    - yield tuple(get\_line\_number(text, “label”, label), “\_”, label, list(formatted text Label of a list column in the {web\_form\_name} Web Form)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L8) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L376)

<a id="op-d0e89825e2ca7f"></a>
### Web Form Page.can render

`operation_foundation_website_page_renderers_web_form_business_behavior_web_form_page_can_render`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Set web\_form from get\_page\_info\_from\_web\_form(self.path).
- If web\_form.
  - Set self.doctype from “Web Form”.
  - Set self.docname from web\_form.name.
  - Evaluate self.set\_headers().
  - Return true.
- Otherwise.
  - Return false.

**Methods declared on this owner** [set headers](operations-020.md#op-a1aef305f410fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5545) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1177)

<a id="op-a1aef305f410fb"></a>
### Web Form Page.set headers

`operation_foundation_website_page_renderers_web_form_business_behavior_web_form_page_set_headers`

**Inputs** self.

**Record and data access** resolve a document from self.doctype via get\_cached\_doc.

**Local steps**

- Set doc from Platform.get\_cached\_doc(self.doctype, self.docname).
- Set allowed\_embedding\_domains from doc.allowed\_embedding\_domains.
- If allowed\_embedding\_domains.
  - Set allowed\_embedding\_domains from allowed\_embedding\_domains.replace(whitespace '\\n', one space).
  - Set self.headers from mapping(“Content-Security-Policy” → formatted text frame-ancestors 'self' {allowed\_embedding\_domains}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.doctype, self.docname).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5697) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1178)

## Record · Web form request

[Record definition](../../../../data/record-types/web_form_request.json)

<a id="op-8db7b82996dc09"></a>
### Invalid Fields In Values Error.initialize

`operation_foundation_website_record_definitions_web_form_request_business_behavior_invalid_fields_in_values_error_initialize`

**Inputs** self, message, invalid\_fields (named only).

**Local steps**

- Evaluate super().\_\_init\_\_(message).
- Set self.invalid\_fields from invalid\_fields.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L4734) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1343)

<a id="op-5194130e1ebf44"></a>
### Web Form Request.before insert

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_before_insert`

**Inputs** self.

**Local steps**

- Set self.key from (self.key or token\_urlsafe()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.key → token\_urlsafe().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L4831) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1349)

<a id="op-c257f5e0efd797"></a>
### Web Form Request.validate

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_validate`

**Inputs** self.

**Record and data access** resolve a document from “Web Form” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Expires On must be in the future”.

**Local steps**

- If not self.web\_form.
  - Return no value.
- Set web\_form from Platform.get\_doc(“Web Form”, self.web\_form).
- For each row in self.references.
  - Set row.link\_doctype from web\_form.doc\_type.
- If (self.has\_value\_changed(“expires\_on”) and is\_expired(self.expires\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“expires\_on”) → is\_expired(self.expires\_on).
  - Call the validation error handler Platform.throw(translated “Expires On must be in the future”, title = translated “Invalid Expiry”).
- If self.web\_form\_values.
  - Evaluate validate\_web\_form\_values(web\_form, parse\_json\_object(self.web\_form\_values)).
- If self.doc\_values.
  - Evaluate validate\_doc\_values(web\_form.doc\_type, parse\_json\_object(self.doc\_values)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L47) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1354)

<a id="op-9a855783b5dbfa"></a>
### Web Form Request.validate key

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_validate_key`

**Inputs** self, allow\_used (named only, default false).

**Explicit failure paths** validation helper with Platform.exceptions.LinkExpired — translated “This Web Form Request has already been used” · validation helper with Platform.exceptions.LinkExpired — translated “This Web Form Request has expired”.

**Local steps**

- If (self.first\_used\_on and not allow\_used).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.first\_used\_on → not allow\_used.
  - Call the validation error handler Platform.throw(translated “This Web Form Request has already been used”, Platform.exceptions.LinkExpired).
- If is\_expired(self.expires\_on).
  - Call the validation error handler Platform.throw(translated “This Web Form Request has expired”, Platform.exceptions.LinkExpired).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L48) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1355)

<a id="op-ae467496ba75fb"></a>
### Web Form Request.get web form values

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_get_web_form_values`

**Inputs** self.

**Explicit results** parse\_json\_object(self.web\_form\_values).

**Local steps**

- Return parse\_json\_object(self.web\_form\_values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5388) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1352)

<a id="op-915bc76b557e33"></a>
### Web Form Request.get doc values

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_get_record_values`

**Inputs** self.

**Explicit results** parse\_json\_object(self.doc\_values).

**Local steps**

- Return parse\_json\_object(self.doc\_values).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5444) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1351)
