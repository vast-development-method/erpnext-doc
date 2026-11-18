# Web content and issued documents · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Web form request

[Record definition](../../../../data/record-types/web_form_request.json)

<a id="op-9977ebe46cb79b"></a>
### Web Form Request.has reference

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_has_reference`

**Inputs** self, link\_name.

**Declared result** bool.

**Explicit results** any(generator of row.link\_name equals str(link\_name) for row drawn from self.references).

**Local steps**

- Return any(generator of row.link\_name equals str(link\_name) for row drawn from self.references).
  - Draw row from self.references.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5500) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1353)

<a id="op-3c90dd10ba4d75"></a>
### Web Form Request.find reference

`operation_foundation_website_record_definitions_web_form_request_business_behavior_web_form_request_find_reference`

**Inputs** self, link\_name.

**Explicit results** next(generator of row for row drawn from self.references where row.link\_name equals str(link\_name), no value).

**Local steps**

- Return next(generator of row for row drawn from self.references where row.link\_name equals str(link\_name), no value).
  - Draw row from self.references, keep a combination only if (row.link\_name equals str(link\_name)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5624) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1350)

<a id="op-1658845db31d66"></a>
### Get request web forms

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_get_request_web_forms`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, dict).

**Explicit results** mapping of d.name → d for d drawn from get\_published\_web\_forms() where (d.key\_required and d.allow\_edit).

**Local steps**

- Bind dependencies get\_published\_web\_forms.
- Return mapping of d.name → d for d drawn from get\_published\_web\_forms() where (d.key\_required and d.allow\_edit).
  - Draw d from get\_published\_web\_forms(), keep a combination only if ((d.key\_required and d.allow\_edit)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.key\_required → d.allow\_edit.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L66) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L459)

<a id="op-30e15eb37db058"></a>
### Get request forms by doctype

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_get_request_forms_by_doctype`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** mapping() · forms.

**Local steps**

- If not Platform.has\_permission(“Web Form Request”, “create”).
  - Return mapping().
- Set forms from mapping().
- For each tuple(name, form) in sorted(get\_request\_web\_forms().items()).
  - Evaluate forms.setdefault(form.doc\_type, list()).append(mapping(“value” → name, “label” → (form.title or name))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in form.title → name.
- Return forms.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Web Form Request”, “create”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L65) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L458)

<a id="op-a3d63aa582354f"></a>
### Get edit url

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_get_edit_url`

**Inputs** route, docname, key.

**Declared result** str.

**Explicit results** get\_url(formatted text /{route}/{name}/edit{get\_web\_form\_request\_query(key)}).

**Local steps**

- Set name from quote(str(docname), safe = empty text).
- Return get\_url(formatted text /{route}/{name}/edit{get\_web\_form\_request\_query(key)}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L64) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L457)

<a id="op-8a051b0164e233"></a>
### Is expired

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_is_expired`

**Inputs** expires\_on.

**Declared result** bool.

**Explicit results** (bool(expires\_on) and get\_datetime(expires\_on) &lt; now\_datetime()).

**Local steps**

- Return (bool(expires\_on) and get\_datetime(expires\_on) &lt; now\_datetime()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(expires\_on) → get\_datetime(expires\_on) &lt; now\_datetime().

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L69) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L462)

<a id="op-0b4e28d7200d53"></a>
### Get status

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_get_status`

**Inputs** request.

**Declared result** str.

**Explicit results** “Used” · “Expired” · “Not Used”.

**Local steps**

- If request.first\_used\_on.
  - Return “Used”.
- If is\_expired(request.expires\_on).
  - Return “Expired”.
- Return “Not Used”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L68) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L461)

<a id="op-dc61ea010f64b2"></a>
### Create for document

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_create_for_document`

**Inputs** web\_form, docname, expires\_on = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** resolve a document from form.doc\_type via get\_doc · resolve a document from mapping(“doctype” → “Web Form Request”, “web\_form” → web\_form, “expires\_on” → expires\_on, “references” → list(mapping(“link\_doctype” → form.doc\_type, “link\_name” → docname))) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Web Form Request”, “web\_form” → web\_form, “expires\_on” → expires\_on, “references” → list(mapping(“link\_doctype” → form.doc\_type, “link\_name” → docname)))).

**Explicit results** get\_edit\_url(form.route, docname, request.key).

**Explicit failure paths** validation helper — translated “Web Form {0} must be published, require a key and allow editing”.format(web\_form).

**Local steps**

- Evaluate Platform.has\_permission(“Web Form Request”, “create”, throw = true).
- Set form from get\_request\_web\_forms().get(web\_form).
- If not form.
  - Call the validation error handler Platform.throw(translated “Web Form {0} must be published, require a key and allow editing”.format(web\_form), title = translated “Web Form Not Allowed”).
- Evaluate Platform.get\_doc(form.doc\_type, docname).check\_permission(“write”).
- Set request from Platform.get\_doc(mapping(“doctype” → “Web Form Request”, “web\_form” → web\_form, “expires\_on” → expires\_on, “references” → list(mapping(“link\_doctype” → nested operand in the contract.doc\_type, “link\_name”  ….
- Return get\_edit\_url(form.route, docname, request.key).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Web Form Request”, “create”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L63) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L456)

<a id="op-a22b78888dc111"></a>
### Get requests for document

`operation_foundation_binding_foundation_website_doctype_web_form_request_web_form_request_get_requests_for_document`

**Inputs** doctype, docname, start = 0, page\_length = 20.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list at dict.

**Record and data access** read “Web Form Request” via get\_list.

**Explicit results** requests.

**Local steps**

- Evaluate Platform.has\_permission(doctype, “write”, docname, throw = true).
- Set forms from get\_request\_web\_forms().
- Set requests from Platform.get\_list(“Web Form Request”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, docname)), fields = list(“name”, “web\_form”, “key”, “expires\_ ….
- For each row in requests.
  - Set row.status from get\_status(row).
  - Set key from row.pop(“key”).
  - Set form from forms.get(row.web\_form).
  - If (form and not is\_expired(row.expires\_on)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in form → not is\_expired(row.expires\_on).
    - Set row.url from get\_edit\_url(form.route, docname, key).
- Return requests.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “write”, docname, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L67) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L460)

<a id="op-b3ba3e81de8550"></a>
### Parse json object

`operation_foundation_website_record_definitions_web_form_request_business_behavior_parse_structured_data_object`

**Inputs** json\_string.

**Explicit results** mapping() · values.

**Explicit failure paths** validation helper — translated “Invalid JSON” · validation helper — translated “JSON value must be an object”.

**Local steps**

- If not json\_string.
  - Return mapping().
- Attempt the following.
  - Set values from json.loads(json\_string).
- On failure (json.JSONDecodeError).
  - Call the validation error handler Platform.throw(translated “Invalid JSON”).
- If not isinstance(values, dict).
  - Call the validation error handler Platform.throw(translated “JSON value must be an object”).
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5754) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1344)

<a id="op-f9d4a4d84a3424"></a>
### Validate json object

`operation_foundation_website_record_definitions_web_form_request_business_behavior_validate_structured_data_object`

**Inputs** json\_string.

**Local steps**

- Evaluate parse\_json\_object(json\_string).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L5986) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1346)

<a id="op-25760996b84132"></a>
### Validate web form values

`operation_foundation_website_record_definitions_web_form_request_business_behavior_validate_web_form_values`

**Inputs** web\_form, values.

**Local steps**

- Set valid\_fields from set of field.fieldname for field drawn from web\_form.web\_form\_fields where field.fieldname.
  - Draw field from web\_form.web\_form\_fields, keep a combination only if (field.fieldname).
- Evaluate validate\_value\_fields(values, valid\_fields, translated “Web Form Values”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L6043) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1348)

<a id="op-0966233ffda896"></a>
### Validate doc values

`operation_foundation_website_record_definitions_web_form_request_business_behavior_validate_record_values`

**Inputs** doctype, values.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set valid\_fields from set of field.fieldname for field drawn from meta.fields where field.fieldname.
  - Draw field from meta.fields, keep a combination only if (field.fieldname).
- Evaluate validate\_value\_fields(values, valid\_fields, translated “Doc Values”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L6177) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1345)

<a id="op-6d152a359276e2"></a>
### Validate value fields

`operation_foundation_website_record_definitions_web_form_request_business_behavior_validate_value_fields`

**Inputs** values, valid\_fields, label.

**Explicit failure paths** validation helper with InvalidFieldsInValuesError(msg, invalid\_fields = tuple(invalid\_fields)) — msg.

**Local steps**

- Set invalid\_fields from sorted((set(values) − valid\_fields)).
- If invalid\_fields.
  - Set msg from translated “{0} contains invalid field(s): {1}”.format(label, “, ”.join(invalid\_fields)).
  - Call the validation error handler Platform.throw(msg, InvalidFieldsInValuesError(msg, invalid\_fields = tuple(invalid\_fields))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L6346) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1347)

<a id="op-588d3481c3b701"></a>
### Get web form request query

`operation_foundation_website_record_definitions_web_form_request_business_behavior_get_web_form_request_query`

**Inputs** key = no value.

**Declared result** str.

**Explicit results** empty text · formatted text ?web\_form\_request\_key={quote(str(key), safe = empty text)}.

**Local steps**

- Set key from (key or Platform.form\_dict.get(“web\_form\_request\_key”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in key → Platform.form\_dict.get(“web\_form\_request\_key”).
- If not key.
  - Return empty text.
- Return formatted text ?web\_form\_request\_key={quote(str(key), safe = empty text)}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L6598) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1342)

<a id="op-c2f6054679dd26"></a>
### Get web form request

`operation_foundation_website_record_definitions_web_form_request_business_behavior_get_web_form_request`

**Inputs** web\_form, key, for\_update (named only, default false), required (named only, default false), allow\_used (named only, default false).

**Declared result** (WebFormRequest bitwise or no value).

**Record and data access** read “Web Form Request” via get\_value · resolve a document from “Web Form Request” via get\_doc.

**Explicit results** no value · web\_form\_request.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Web Form Request key is required” · validation helper with Platform.PermissionError — translated “Invalid Web Form Request”.

**Local steps**

- If not key.
  - If required.
    - Call the validation error handler Platform.throw(translated “Web Form Request key is required”, Platform.PermissionError).
  - Return no value.
- If not isinstance(key, str).
  - Call the validation error handler Platform.throw(translated “Invalid Web Form Request”, Platform.PermissionError).
- Set request\_name from Platform.db.get\_value(“Web Form Request”, mapping(“web\_form” → web\_form, “key” → key), “name”).
- If not request\_name.
  - If required.
    - Call the validation error handler Platform.throw(translated “Invalid Web Form Request”, Platform.PermissionError).
  - Return no value.
- Set web\_form\_request from Platform.get\_doc(“Web Form Request”, request\_name, for\_update = for\_update).
- Evaluate web\_form\_request.validate\_key(allow\_used = allow\_used).
- Return web\_form\_request.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0531.json#L6768) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1341)

## Record · Web page

[Record definition](../../../../data/record-types/web_page.json)

<a id="op-4f97a27c14a82f"></a>
### Web Page.validate

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.set\_route().
- If not self.dynamic\_route.
  - Set self.route from quoted(self.route).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-022.md#op-3903b79380d112).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L794) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1428)

<a id="op-be54117b09cdd4"></a>
### Web Page.get context

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_get_context`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, context.

**Explicit result forms** a value selected from the current context.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L917) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1422)

<a id="op-e523bba8c1d591"></a>
### Web Page.render dynamic

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_render_dynamic`

**Inputs** self, context.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set is\_jinja from (context.dynamic\_template or “&lt;!-- jinja --&gt;” belongs to context.main\_section or “{{” belongs to context.main\_section).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.dynamic\_template → “&lt;!-- jinja --&gt;” belongs to context.main\_section → “{{” belongs to context.main\_section.
- If is\_jinja.
  - Set Platform.flags.web\_block\_scripts from mapping().
  - Set Platform.flags.web\_block\_styles from mapping().
  - Attempt the following.
    - Set context at “main\_section” from render\_template(context.main\_section, context, restrict\_globals = true).
    - If “&lt;!-- static --&gt;” does not belong to context.main\_section.
      - Set context at “no\_cache” from 1.
  - On failure (TemplateSyntaxError).
    - Propagate the active failure.
  - On exit, including pending return or failure.
    - Set Platform.flags.web\_block\_scripts from mapping().
    - Set Platform.flags.web\_block\_styles from mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L1673) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1423)

<a id="op-deacbf81e190c9"></a>
### Web Page.set breadcrumbs

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_set_breadcrumbs`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L2004) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1424)

<a id="op-2fae57de42b196"></a>
### Web Page.set title and header

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_set_title_and_header`

**Inputs** self, context.

**Local steps**

- If “no\_header” does not belong to context.
  - If “&lt;!-- no-header --&gt;” belongs to context.main\_section.
    - Set context.no\_header from 1.
- If not context.title.
  - Set context.title from extract\_title(context.main\_section, context.path\_name).
- If (context.no\_header and “header” belongs to context).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.no\_header → “header” belongs to context.
  - Set context.header from empty text.
- If not context.no\_header.
  - If (not context.header and “&lt;h1” does not belong to context.main\_section).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not context.header → “&lt;h1” does not belong to context.main\_section.
    - Set context.header from context.title.
  - If (context.get(“header”) and not H\_TAG\_PATTERN.findall(context.header)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.get(“header”) → not H\_TAG\_PATTERN.findall(context.header).
    - Set context.header from ((text in the contract + context.header) + “&lt;/h1&gt;”).
- If (not context.title and context.header).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not context.title → context.header.
  - Set context.title from strip\_html(context.header).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L2174) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1427)

<a id="op-d6cd5371b7b2d2"></a>
### Web Page.set page blocks

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_set_page_blocks`

**Inputs** self, context.

**Explicit results** no value.

**Local steps**

- If self.content\_type differs from “Page Builder”.
  - Return no value.
- Set out from get\_web\_blocks\_html(self.page\_blocks).
- Set context.page\_builder\_html from out.html.
- Set context.page\_builder\_scripts from out.scripts.
- Set context.page\_builder\_styles from out.styles.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L2649) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1426)

<a id="op-17a8cced6341f3"></a>
### Web Page.add hero

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_add_hero`

**Inputs** self, context.

**Local steps**

- Set context.hero from empty text.
- If “&lt;!-- start-hero --&gt;” belongs to context.main\_section.
  - Set parts1 from context.main\_section.split(“&lt;!-- start-hero --&gt;”).
  - Set parts2 from parts1 at 1.split(“&lt;!-- end-hero --&gt;”).
  - Set context.main\_section from (parts1 at 0 + parts2 at 1).
  - Set context.hero from parts2 at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L2815) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1420)

<a id="op-d29a05f831884c"></a>
### Web Page.check for redirect

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_check_for_redirect`

**Inputs** self, context.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- If “&lt;!-- redirect:” belongs to context.main\_section.
  - Set Platform.local.flags.redirect\_location from nested operand in the contract(nested operand in the contract, nested operand in the contract) at 1.split(“--&gt;”, 1) at 0.strip().
  - Raise Platform.Redirect.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L3028) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1421)
