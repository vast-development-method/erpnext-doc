# Web content and issued documents · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Web form

[Record definition](../../../../data/record-types/web_form.json)

<a id="op-ae55dc179c129f"></a>
### Web Form.on update

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_on_update`

**Inputs** self.

**Local steps**

- Set path from export\_module\_json(self, self.is\_standard, self.module).
- If path.
  - If not os.path.exists((path + “.js”)).
    - Within open((path + “.js”), “w”) bound as f.
      - Evaluate f.write(“Platform.ready(function () {\\n\\t// bind events here\\n});\\n”).
  - If not os.path.exists((path + “.py”)).
    - Within open((path + “.py”), “w”) bound as f.
      - Evaluate f.write(multiline text in the contract).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L43) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1330)

<a id="op-8928c154e781df"></a>
### Web Form.clear cache

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_webform_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate Platform.cache.delete\_key(“bootinfo”).
- Evaluate Platform.db.after\_commit.add(deferred anonymous expression).
- Evaluate Platform.db.after\_rollback.add(deferred anonymous expression).
- Return super().clear\_cache().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L73) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L466)

<a id="op-5478e12e04a8dc"></a>
### Web Form.get context

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_get_context`

**Inputs** self, context.

**Record and data access** read self.doc\_type via exists · read self.doc\_type via get\_all.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be logged in to access this {0}.”.format(self.doc\_type) · Platform.PageDoesNotExistError() · validation helper with Platform.PermissionError — translated “You don't have the permissions to access this document”.

**Local steps**

- Set context.in\_edit\_mode from false.
- Set context.in\_view\_mode from false.
- If Platform.form\_dict.is\_list.
  - Set context.template from “website/doctype/web\_form/templates/web\_list.html”.
- Otherwise.
  - Set context.template from “website/doctype/web\_form/templates/web\_form.html”.
- Set context.has\_delete\_permission from false.
- Set web\_form\_request from self.get\_web\_form\_request(Platform.form\_dict.web\_form\_request\_key, docname = Platform.form\_dict.name, allow\_used = (bool(Platform.form\_dict.name) or bool(self.allow\_multiple) or bool(Platform.form\_dict.is\_list))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bool(Platform.form\_dict.name) → bool(self.allow\_multiple) → bool(Platform.form\_dict.is\_list).
- If Platform.form\_dict.name.
  - Require isinstance(Platform.form\_dict.name, (str bitwise or int)) or raise an assertion failure.
  - If (Platform.session.user equals “Guest” and (not web\_form\_request or self.login\_required)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → (not web\_form\_request or self.login\_required).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not web\_form\_request → self.login\_required.
    - Call the validation error handler Platform.throw(translated “You need to be logged in to access this {0}.”.format(self.doc\_type), Platform.PermissionError).
  - If not Platform.db.exists(self.doc\_type, Platform.form\_dict.name).
    - Evaluate check\_doctype\_permission(self.doc\_type).
    - Raise Platform.PageDoesNotExistError().
  - If (not web\_form\_request and not self.has\_web\_form\_permission(self.doc\_type, Platform.form\_dict.name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not web\_form\_request → not self.has\_web\_form\_permission(self.doc\_type, Platform.form\_dict.name).
    - Evaluate check\_doctype\_permission(self.doc\_type).
    - Call the validation error handler Platform.throw(translated “You don't have the permissions to access this document”, Platform.PermissionError).
  - Set context.has\_delete\_permission from (self.allow\_delete and (bool(web\_form\_request) or Platform.has\_permission(self.doc\_type, “delete”, Platform.form\_dict.name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.allow\_delete → (bool(web\_form\_request) or Platform.has\_permission(self.doc\_type, “delete”, Platform.form\_dict.name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bool(web\_form\_request) → Platform.has\_permission(self.doc\_type, “delete”, Platform.form\_dict.name).
- If Platform.local.path equals self.route.
  - Set path from formatted text /{self.route}/list when self.show\_list, otherwise formatted text /{self.route}/new.
    - Value choice on self.show\_list — true gives formatted text /{self.route}/list, false gives formatted text /{self.route}/new.
  - Evaluate self.redirect\_to(path).
- If (Platform.form\_dict.is\_list and not self.show\_list).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.form\_dict.is\_list → not self.show\_list.
  - Evaluate self.redirect\_to(formatted text /{self.route}/new).
- If (Platform.form\_dict.is\_edit and not self.allow\_edit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.form\_dict.is\_edit → not self.allow\_edit.
  - Set context.in\_view\_mode from true.
  - Evaluate self.redirect\_to(formatted text /{self.route}/{Platform.form\_dict.name}).
- If Platform.form\_dict.is\_edit.
  - Set context.in\_edit\_mode from true.
- If Platform.form\_dict.is\_read.
  - Set context.in\_view\_mode from true.
- Set context.allows\_public\_access from not (self.login\_required or self.key\_required).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.login\_required → self.key\_required.
- If (not Platform.form\_dict.is\_edit and not Platform.form\_dict.is\_read and self.allow\_edit and Platform.form\_dict.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.form\_dict.is\_edit → not Platform.form\_dict.is\_read → self.allow\_edit → Platform.form\_dict.name.
  - Set context.in\_edit\_mode from true.
  - Evaluate self.redirect\_to(formatted text /{Platform.local.path}/edit).
- If (Platform.session.user differs from “Guest” and self.login\_required and not self.allow\_multiple and not Platform.form\_dict.name and not Platform.form\_dict.is\_list and not web\_form\_request).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from “Guest” → self.login\_required → not self.allow\_multiple → not Platform.form\_dict.name → not Platform.form\_dict.is\_list → not web\_form\_request.
  - Set condition\_json from json.loads(self.condition\_json) when self.condition\_json, otherwise list().
    - Value choice on self.condition\_json — true gives json.loads(self.condition\_json), false gives list().
  - Evaluate condition\_json.append(list(“owner”, “=”, Platform.session.user)).
  - Set names from Platform.get\_all(self.doc\_type, filters = condition\_json, pluck = “name”).
  - If names.
    - Set context.in\_view\_mode from true.
    - Evaluate self.redirect\_to(formatted text /{self.route}/{names at 0}).
- Set route\_to\_new from (Platform.session.user equals “Guest” or not self.login\_required).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.session.user equals “Guest” → not self.login\_required.
- If (not Platform.form\_dict.is\_new and route\_to\_new and not web\_form\_request).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.form\_dict.is\_new → route\_to\_new → not web\_form\_request.
  - Evaluate self.redirect\_to(formatted text /{self.route}/new).
- Evaluate self.reset\_field\_parent().
- Evaluate context.update(dict\_with\_keys(Platform.form\_dict, list(“is\_list”, “is\_new”, “is\_edit”, “is\_read”))).
- For each df in self.web\_form\_fields.
  - If df.fieldtype equals “Column Break”.
    - Set context.has\_column\_break from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set context.web\_form\_doc from self.as\_dict(no\_nulls = true).
- Evaluate context.web\_form\_doc.update(dict\_with\_keys(context, list(“is\_list”, “is\_new”, “in\_edit\_mode”, “in\_view\_mode”))).
- If web\_form\_request.
  - Set context.is\_web\_form\_request from true.
  - Set context.web\_form\_request\_key from web\_form\_request.key.
  - Set context.web\_form\_doc.is\_web\_form\_request from true.
  - Set context.web\_form\_doc.web\_form\_request\_key from web\_form\_request.key.
- If (self.show\_sidebar and self.website\_sidebar).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.show\_sidebar → self.website\_sidebar.
  - Set context.sidebar\_items from get\_sidebar\_items(self.website\_sidebar).
- If Platform.form\_dict.is\_list.
  - Evaluate self.load\_list\_data(context).
- Otherwise.
  - Evaluate self.load\_form\_data(context, web\_form\_request).
- Evaluate self.add\_custom\_context\_and\_script(context).
- Evaluate self.load\_translations(context).
- Evaluate self.add\_metatags(context).
- Set context.boot from get\_boot\_data().
- Set context.boot at “link\_title\_doctypes” from Platform.boot.get\_link\_title\_doctypes().
- Set context.webform\_banner\_image from (context.get(“banner\_image”) or self.banner\_image).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.get(“banner\_image”) → self.banner\_image.
- Evaluate context.pop(“banner\_image”, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get web form request](operations-019.md#op-3d3fe6e90770a6), [has web form permission](operations-019.md#op-8348e23aaa543c), [redirect to](operations-019.md#op-8db4cd47df6d9f), [reset field parent](operations-018.md#op-995a5ebddee13c), [load list data](operations-019.md#op-2bcb1b884ea5c9), [load form data](operations-019.md#op-619ab40781aa9f), [add custom context and script](operations-019.md#op-4ba7771d94424b), [load translations](operations-019.md#op-e5a1832187da44), [add metatags](operations-019.md#op-64d71dc302ed81).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doc\_type, “delete”, Platform.form\_dict.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L349) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1321)

<a id="op-64d71dc302ed81"></a>
### Web Form.add metatags

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_add_metatags`

**Inputs** self, context.

**Local steps**

- Set description from self.meta\_description.
- If (not description and self.introduction\_text).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not description → self.introduction\_text.
  - Set description from self.introduction\_text at slice no value to 140.
- Set context.metatags from mapping(“title” → (self.meta\_title or self.title), “description” → description, “image” → self.meta\_image).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta\_title → self.title.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L2924) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1319)

<a id="op-e5a1832187da44"></a>
### Web Form.load translations

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_load_translations`

**Inputs** self, context.

**Local steps**

- Set messages from list(“{0} if you are not redirected within {1} seconds”, “← Back to upload files”, “Are you sure you want to delete this record?”, “Are you sure you want to discard the changes?”, …).
- For each field in self.web\_form\_fields.
  - Evaluate messages.extend(list(field.label, field.description)).
  - If (field.fieldtype equals “Select” and field.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Select” → field.options.
    - Evaluate messages.extend(field.options.split(whitespace '\\n')).
- If any(generator of field.fieldtype equals “Table” for field drawn from self.web\_form\_fields).
  - Draw field from self.web\_form\_fields.
  - Evaluate messages.extend(tuple(“Move”, “Insert Above”, “Insert Below”, “Duplicate”, …)).
- If any(generator of field.fieldtype equals “Phone” for field drawn from self.web\_form\_fields).
  - Draw field from self.web\_form\_fields.
  - Evaluate messages.append(“Search for countries...”).
- If any(generator of field.fieldtype equals “Date” for field drawn from self.web\_form\_fields).
  - Draw field from self.web\_form\_fields.
  - Evaluate messages.extend(tuple(“Now”, “Today”, “Date {0} must be in format: {1}”, “{0} to {1}”)).
- If any(generator of field.fieldtype equals “Time” for field drawn from self.web\_form\_fields).
  - Draw field from self.web\_form\_fields.
  - Evaluate messages.append(“Now”).
- Evaluate messages.extend(generator of col.get(“label”) when col, otherwise empty text for col drawn from self.list\_columns).
  - Draw col from self.list\_columns.
  - Value choice on col — true gives col.get(“label”), false gives empty text.
- Set translation\_dict from mapping().
- For each key in messages.
  - If not key.
    - Continue with the next iteration or loop test.
  - If isinstance(key, tuple).
    - Set tuple(msg, ctx) from key.
    - Set translation\_dict at formatted text {msg}:{ctx} from \_(msg, context = ctx).
  - Otherwise.
    - Set translation\_dict at key from translated key.
- Set context.translated\_messages from Platform.as\_json(translation\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L3127) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1329)

<a id="op-2bcb1b884ea5c9"></a>
### Web Form.load list data

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_load_list_data`

**Inputs** self, context.

**Local steps**

- If not self.list\_columns.
  - Set self.list\_columns from get\_in\_list\_view\_fields(self.doc\_type, self.name, web\_form\_request\_key = context.get(“web\_form\_request\_key”)).
  - Set context.web\_form\_doc.list\_columns from self.list\_columns.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L4520) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1328)

<a id="op-8db4cd47df6d9f"></a>
### Web Form.redirect to

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_redirect_to`

**Inputs** self, path.

**Local steps**

- Evaluate Platform.redirect((path + get\_web\_form\_request\_query())).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L4674) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1332)

<a id="op-3d3fe6e90770a6"></a>
### Web Form.get web form request

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_get_web_form_request`

**Inputs** self, key, docname (named only, default no value), for\_update (named only, default false), allow\_used (named only, default false).

**Declared result** “WebFormRequest \| None”.

**Explicit results** no value · web\_form\_request.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid Web Form Request”.

**Local steps**

- If (key and not getattr(self, “key\_required”, false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key → not getattr(self, “key\_required”, false).
  - Return no value.
- Set web\_form\_request from get\_web\_form\_request(self.name, key, for\_update = for\_update, required = getattr(self, “key\_required”, false), allow\_used = allow\_used).
- If (web\_form\_request and docname and not web\_form\_request.has\_reference(docname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form\_request → docname → not web\_form\_request.has\_reference(docname).
  - Call the validation error handler Platform.throw(translated “Invalid Web Form Request”, Platform.PermissionError).
- Return web\_form\_request.

**Values supplied outside this operation** selected callable from getattr(self, “key\_required”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L4759) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1323)

<a id="op-619ab40781aa9f"></a>
### Web Form.load form data

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_load_form_data`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, context, web\_form\_request.

**Observed service boundaries** record lookup.

**Local structure** 15 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L42) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1327)

<a id="op-4ba7771d94424b"></a>
### Web Form.add custom context and script

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_add_custom_context_and_script`

**Inputs** self, context.

**Local steps**

- If self.is\_standard.
  - Set web\_form\_module from get\_web\_form\_module(self).
  - Set new\_context from web\_form\_module.get\_context(context).
  - If new\_context.
    - Evaluate context.update(new\_context).
  - Set js\_path from os.path.join(os.path.dirname(web\_form\_module.\_\_file\_\_), (scrub(self.name) + “.js”)).
  - If os.path.exists(js\_path).
    - Set script from Platform.render\_template(open(js\_path).read(), context).
    - For each path in (get\_code\_files\_via\_hooks(“webform\_include\_js”, context.doc\_type) + get\_code\_files\_via\_hooks(“webform\_include\_js”, “\*”)).
      - Set custom\_js from Platform.render\_template(open(path).read(), context).
      - Set script from whitespace '\\n\\n'.join(list(script, custom\_js)).
    - Set context.script from script.
  - Set css\_path from os.path.join(os.path.dirname(web\_form\_module.\_\_file\_\_), (scrub(self.name) + “.css”)).
  - If os.path.exists(css\_path).
    - Set style from open(css\_path).read().
    - For each path in get\_code\_files\_via\_hooks(“webform\_include\_css”, context.doc\_type).
      - Set custom\_css from open(path).read().
      - Set style from whitespace '\\n\\n'.join(list(style, custom\_css)).
    - Set context.style from style.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L6652) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1318)

<a id="op-592d19f2355c73"></a>
### Web Form.get parents

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_get_parents`

**Inputs** self, context.

**Explicit results** parents.

**Local steps**

- Set parents from no value.
- If (context.is\_list and not context.parents).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.is\_list → not context.parents.
  - Set parents from list(mapping(“title” → translated “My Account”, “name” → “me”)).
- Otherwise.
  - If context.parents.
    - Set parents from context.parents.
- Return parents.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0529.json#L7416) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1322)

<a id="op-50ad27989e19fe"></a>
### Web Form.validate submission

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_submission`

**Inputs** self, doc, uploaded\_fields = no value.

**Local steps**

- If not self.allow\_incomplete.
  - Evaluate self.validate\_mandatory(doc, uploaded\_fields).
- Evaluate self.validate\_data\_field\_options(doc).
- Evaluate self.validate\_user\_permitted\_links(doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory](operations-019.md#op-ea1ef63f3886d6), [validate data field options](operations-019.md#op-e9116250ac8bf9), [validate user permitted links](operations-019.md#op-8c8052bdcc4cbe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L46) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1340)

<a id="op-8c8052bdcc4cbe"></a>
### Web Form.validate user permitted links

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_webform_validate_user_permitted_links`

**Inputs** self, doc.

**Local steps**

- Set meta from Platform.get\_meta(self.doc\_type).
- For each field in self.web\_form\_fields.
  - If not field.apply\_user\_permissions.
    - Continue with the next iteration or loop test.
  - If field.fieldtype equals “Link”.
    - Set df from meta.get\_field(field.fieldname).
    - Evaluate self.check\_permitted\_link(field.options, field.fieldname, (df and df.ignore\_user\_permissions), list(doc)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.ignore\_user\_permissions.
  - Otherwise.
    - If field.fieldtype belongs to tuple(“Table”, “Table MultiSelect”).
      - Set rows from (doc.get(field.fieldname) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(field.fieldname) → list().
      - For each df in Platform.get\_meta(field.options).get\_link\_fields().
        - Evaluate self.check\_permitted\_link(df.options, df.fieldname, df.ignore\_user\_permissions, rows).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check permitted link](operations-019.md#op-1be4c413c70198).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L75) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L468)

<a id="op-1be4c413c70198"></a>
### Web Form.check permitted link

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_webform_check_permitted_link`

**Inputs** self, link\_doctype, fieldname, ignore\_user\_permissions, rows.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to select {0} {1}”.format(translated link\_doctype, Platform.bold(value)).

**Local steps**

- If (ignore\_user\_permissions or not allowed bound to set(get\_permitted\_link\_values(self, link\_doctype))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_user\_permissions → not allowed bound to set(get\_permitted\_link\_values(self, link\_doctype)).
  - Return no value.
- For each row in rows.
  - Set value from row.get(fieldname).
  - If (value and value does not belong to allowed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → value does not belong to allowed.
    - Call the validation error handler Platform.throw(translated “You are not allowed to select {0} {1}”.format(translated link\_doctype, Platform.bold(value)), Platform.PermissionError, title = translated “Not Permitted”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L72) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L465)

<a id="op-ea1ef63f3886d6"></a>
### Web Form.validate mandatory

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_mandatory`

**Inputs** self, doc, uploaded\_fields = no value.

**Explicit failure paths** validation helper — ((translated “Mandatory Information missing:” + text in the contract) + text in the contract.join(generator of formatted text {d.label} ({d.fieldtype}) for d drawn from missing)).

**Local steps**

- Set uploaded\_fields from (uploaded\_fields or set()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uploaded\_fields → set().
- Set missing from list of f for f drawn from self.web\_form\_fields where (f.reqd and f.fieldname does not belong to uploaded\_fields and doc.get(f.fieldname) belongs to tuple(no value, list(), empty text)).
  - Draw f from self.web\_form\_fields, keep a combination only if ((f.reqd and f.fieldname does not belong to uploaded\_fields and doc.get(f.fieldname) belongs to tuple(no value, list(), empty text))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.reqd → f.fieldname does not belong to uploaded\_fields → doc.get(f.fieldname) belongs to tuple(no value, list(), empty text).
- If missing.
  - Call the validation error handler Platform.throw(((translated “Mandatory Information missing:” + text in the contract) + text in the contract.join(generator of formatted text {d.label} ({d.fieldtype}) for d drawn from missing))).
    - Draw d from missing.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1339)

<a id="op-e9116250ac8bf9"></a>
### Web Form.validate data field options

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_data_field_options`

**Inputs** self, doc.

**Local steps**

- Bind dependencies split\_emails, validate\_email\_address, validate\_name, validate\_phone\_number, validate\_phone\_number\_with\_country\_code, validate\_url.
- Set meta from Platform.get\_meta(self.doc\_type).
- For each field in self.web\_form\_fields.
  - Set value from doc.get(field.fieldname).
  - If not value.
    - Continue with the next iteration or loop test.
  - Set df from meta.get\_field(field.fieldname).
  - If field.fieldtype equals “Phone”.
    - If not (df and df.fieldtype equals “Phone”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Phone”.
      - Evaluate validate\_phone\_number\_with\_country\_code(value, field.fieldname, translated field.label).
    - Continue with the next iteration or loop test.
  - If (field.fieldtype differs from “Data” or not field.options).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldtype differs from “Data” → not field.options.
    - Continue with the next iteration or loop test.
  - If (df and df.fieldtype equals “Data” and df.options equals field.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Data” → df.options equals field.options.
    - Continue with the next iteration or loop test.
  - If field.options equals “Email”.
    - For each email\_address in split\_emails(value).
      - Evaluate validate\_email\_address(email\_address, throw = true).
  - Otherwise.
    - If field.options equals “Name”.
      - Evaluate validate\_name(value, throw = true).
    - Otherwise.
      - If field.options equals “Phone”.
        - Evaluate validate\_phone\_number(value, throw = true).
      - Otherwise.
        - If field.options equals “URL”.
          - Evaluate validate\_url(value, throw = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L45) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1335)

<a id="op-9d3f39e73cc31d"></a>
### Web Form.allow website search indexing

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_allow_website_search_indexing`

**Inputs** self.

**Explicit results** false.

**Local steps**

- Return false.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L1002) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1320)

<a id="op-8348e23aaa543c"></a>
### Web Form.has web form permission

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_has_web_form_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, doctype, name, ptype.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L1039) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1326)

<a id="op-3bf0a69829d465"></a>
### Web Form.get webform attachments

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_get_webform_attachments`

**Inputs** self, context.

**Record and data access** read “File” via get\_all.

**Explicit results** permitted\_attachments.

**Local steps**

- Bind dependencies has\_file\_permission.
- Bind local operation \_add\_attachment for subsequent calls.
- Set attachments from Platform.get\_all(“File”, filters = mapping(“attached\_to\_name” → context.reference\_name, “attached\_to\_doctype” → context.reference\_doctype), fields = list(“is\_private”, “file\_name”, “file\_url”, “file\_size”, …)).
- Set permitted\_attachments from list().
- For each attachment in attachments.
  - If not attachment.is\_private.
    - Evaluate permitted\_attachments.append(\_add\_attachment(attachment)).
    - Continue with the next iteration or loop test.
  - If has\_file\_permission(attachment, “read”).
    - Evaluate permitted\_attachments.append(\_add\_attachment(attachment)).
- Return permitted\_attachments.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L1372) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1324)

<a id="op-61025cfbdbac86"></a>
### Web Form.get webform attachments.add attachment

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_get_webform_attachments_add_attachment`

**Inputs** attachment.

**Explicit results** mapping(“file\_name” → attachment.file\_name, “file\_url” → attachment.file\_url, “file\_size” → attachment.file\_size).

**Local steps**

- Return mapping(“file\_name” → attachment.file\_name, “file\_url” → attachment.file\_url, “file\_size” → attachment.file\_size).

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L1825) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1325)

<a id="op-ecb298926290dd"></a>
### Process link field

`operation_foundation_website_record_definitions_web_form_business_behavior_process_link_field`

**Inputs** field, web\_form\_name, web\_form\_request\_key = no value, docname = no value, allow\_read\_on\_all\_link\_options = false, apply\_user\_permissions = false.

**Record and data access** resolve a document from “Web Form” via get\_cached\_doc.

**Explicit results** field.

**Local steps**

- Set ignore\_user\_permissions from field.get(“ignore\_user\_permissions”).
- If field.get(“doctype”) equals “Web Form Field”.
  - Set web\_form\_doctype from Platform.get\_cached\_doc(“Web Form”, web\_form\_name).doc\_type.
  - Set docfield from Platform.get\_meta(web\_form\_doctype).get\_field(field.fieldname).
  - Set ignore\_user\_permissions from docfield.ignore\_user\_permissions when docfield, otherwise no value.
    - Value choice on docfield — true gives docfield.ignore\_user\_permissions, false gives no value.
- Set field.fieldtype from “Autocomplete”.
- Set field.options from get\_link\_options(web\_form\_name, field.options, allow\_read\_on\_all\_link\_options, web\_form\_request\_key = web\_form\_request\_key, docname = docname, apply\_user\_permissions = apply\_user\_permissions, ignore\_user\_p ….
- Return field.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Web Form”, web\_form\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L41) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1317)

<a id="op-165120efec2e17"></a>
### Get web form module

`operation_foundation_website_record_definitions_web_form_business_behavior_get_web_form_module`

**Inputs** doc.

**Explicit results** get\_doc\_module(doc.module, doc.doctype, doc.name).

**Local steps**

- If doc.is\_standard.
  - Return get\_doc\_module(doc.module, doc.doctype, doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L2095) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1314)

<a id="op-4d6ae0738660d4"></a>
### Accept

`operation_foundation_website_record_definitions_web_form_business_behavior_accept`

**Inputs** web\_form, data, web\_form\_request\_key = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”), allow\_guest = true), rate\_limit(key = “web\_form”, limit = 10, seconds = 60).

**Record and data access** resolve a document from doctype via get\_doc · resolve a document from mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → doc.name, …) via get\_doc.

**State and service calls** request new\_doc for doctype · call save on doc · call save on web\_form\_request · call insert on doc · call save on \_file.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “You must login to use this form” · validation helper — translated “You are not allowed to update this Web Form Document”.

**Local steps**

- Set data from Platform.\_dict(json.loads(data)).
- Set files from list().
- Set files\_to\_delete from list().
- Set web\_form from Platform.get\_lazy\_doc(“Web Form”, web\_form).
- Evaluate web\_form.raise\_if\_unpublished().
- Set doctype from web\_form.doc\_type.
- Set user from Platform.session.user.
- Set web\_form\_request from web\_form.get\_web\_form\_request(web\_form\_request\_key, docname = data.name, for\_update = true, allow\_used = (bool(data.name) or bool(web\_form.allow\_multiple))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bool(data.name) → bool(web\_form.allow\_multiple).
- If (web\_form.login\_required and Platform.session.user equals “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.login\_required → Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “You must login to use this form”).
- If (web\_form.anonymous and Platform.session.user differs from “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.anonymous → Platform.session.user differs from “Guest”.
  - Set Platform.session.user from “Guest”.
- If (data.name and not web\_form.allow\_edit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.name → not web\_form.allow\_edit.
  - Call the validation error handler Platform.throw(translated “You are not allowed to update this Web Form Document”).
- Set Platform.flags.in\_web\_form from true.
- Set meta from Platform.get\_meta(doctype).
- If data.name.
  - Set doc from Platform.get\_doc(doctype, data.name).
- Otherwise.
  - Set doc from Platform.new\_doc(doctype).
- If web\_form.allow\_incomplete.
  - Set doc.flags.ignore\_mandatory from true.
- For each field in web\_form.web\_form\_fields.
  - Set fieldname from field.fieldname.
  - Set df from meta.get\_field(fieldname).
  - Set value from data.get(fieldname, empty text).
  - If (df and df.fieldtype belongs to tuple(“Attach”, “Attach Image”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype belongs to tuple(“Attach”, “Attach Image”).
    - If (value and “data:” and “base64” belongs to value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → “data:” → “base64” belongs to value.
      - Evaluate files.append(tuple(fieldname, value)).
      - If not doc.name.
        - Evaluate doc.set(fieldname, empty text).
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If (not value and doc.get(fieldname)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not value → doc.get(fieldname).
        - Evaluate files\_to\_delete.append(doc.get(fieldname)).
  - Evaluate doc.set(fieldname, value).
- If web\_form\_request.
  - For each tuple(fieldname, value) in web\_form\_request.get\_doc\_values().items().
    - If meta.has\_field(fieldname).
      - Evaluate doc.set(fieldname, value).
- Evaluate web\_form.validate\_submission(doc, uploaded\_fields = set of fieldname for tuple(fieldname, \_) drawn from files).
  - Draw tuple(fieldname, \_) from files.
- If doc.name.
  - If web\_form\_request.
    - Evaluate doc.save(ignore\_permissions = true).
    - If not web\_form\_request.first\_used\_on.
      - Set web\_form\_request.first\_used\_on from now\_datetime().
      - Evaluate web\_form\_request.save(ignore\_permissions = true).
  - Otherwise.
    - If web\_form.has\_web\_form\_permission(doctype, doc.name, “write”).
      - Evaluate doc.save(ignore\_permissions = true).
    - Otherwise.
      - Evaluate doc.save().
- Otherwise.
  - Set ignore\_mandatory from true when (files or web\_form.allow\_incomplete), otherwise false.
    - Value choice on (files or web\_form.allow\_incomplete) — true gives true, false gives false.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in files → web\_form.allow\_incomplete.
  - Evaluate doc.insert(ignore\_permissions = true, ignore\_mandatory = ignore\_mandatory).
  - If web\_form\_request.
    - Evaluate web\_form\_request.append(“references”, mapping(“link\_doctype” → doctype, “link\_name” → doc.name)).
    - If not web\_form\_request.first\_used\_on.
      - Set web\_form\_request.first\_used\_on from now\_datetime().
    - Evaluate web\_form\_request.save(ignore\_permissions = true).
- If files.
  - For each f in files.
    - Set tuple(fieldname, filedata) from f.
    - If doc.get(fieldname).
      - Evaluate remove\_file\_by\_url(doc.get(fieldname), doctype = doctype, name = doc.name).
    - Set tuple(filename, dataurl) from filedata.split(“,”, 1).
    - Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → doc.name, …)).
    - Evaluate \_file.save().
    - Evaluate doc.set(fieldname, \_file.file\_url).
  - Evaluate doc.save(ignore\_permissions = true).
- If files\_to\_delete.
  - For each f in files\_to\_delete.
    - If f.
      - Evaluate remove\_file\_by\_url(f, doctype = doctype, name = doc.name).
- If (web\_form.anonymous and Platform.session.user equals “Guest” and user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.anonymous → Platform.session.user equals “Guest” → user.
  - Set Platform.session.user from user.
- Set Platform.flags.web\_form\_doc from doc.
- Return doc.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L33) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1301)

<a id="op-89c72b40bc68fd"></a>
### Delete

`operation_foundation_website_record_definitions_web_form_business_behavior_delete`

**Inputs** web\_form\_name, docname, web\_form\_request\_key = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “DELETE”), allow\_guest = true), rate\_limit(key = “web\_form\_name”, limit = 999, seconds = 60).

**Record and data access** read web\_form.doc\_type via get\_value.

**State and service calls** call save on web\_form\_request · request delete\_doc for web\_form.doc\_type.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Allowed”.

**Local steps**

- Set web\_form from Platform.get\_lazy\_doc(“Web Form”, web\_form\_name).
- Evaluate web\_form.raise\_if\_unpublished().
- Set web\_form\_request from web\_form.get\_web\_form\_request(web\_form\_request\_key, docname = docname, for\_update = true, allow\_used = true).
- If (not web\_form.allow\_delete or (Platform.session.user equals “Guest” and web\_form.login\_required) or (Platform.session.user equals “Guest” and not web\_form\_request)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not web\_form.allow\_delete → (Platform.session.user equals “Guest” and web\_form.login\_required) → (Platform.session.user equals “Guest” and not web\_form\_request).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → web\_form.login\_required.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → not web\_form\_request.
  - Call the validation error handler Platform.throw(translated “Not Allowed”, Platform.PermissionError).
- Set owner from Platform.db.get\_value(web\_form.doc\_type, docname, “owner”).
- If (web\_form\_request or Platform.session.user equals owner).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in web\_form\_request → Platform.session.user equals owner.
  - If web\_form\_request.
    - Evaluate web\_form\_request.remove(web\_form\_request.find\_reference(docname)).
    - If not web\_form\_request.first\_used\_on.
      - Set web\_form\_request.first\_used\_on from now\_datetime().
    - Evaluate web\_form\_request.save(ignore\_permissions = true).
  - Evaluate Platform.delete\_doc(web\_form.doc\_type, docname, ignore\_permissions = true).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Not Allowed”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0530.json#L4558) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1303)
