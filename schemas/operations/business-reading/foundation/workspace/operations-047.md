# Forms, reports and navigation · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Onboarding step

[Record definition](../../../../data/record-types/onboarding_step.json)

<a id="op-a21a37b0881cda"></a>
### Onboarding Step.get record filters

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_onboardingstep_get_record_filters`

**Inputs** self, meta.

**Declared result** dict.

**Explicit results** mapping() · mapping of key → value for tuple(key, value) drawn from options.items() where (meta.has\_field(key) and isinstance(value, ((str bitwise or int) bitwise or float))).

**Local steps**

- Set options from Platform.parse\_json(self.route\_options) when self.route\_options, otherwise no value.
  - Value choice on self.route\_options — true gives Platform.parse\_json(self.route\_options), false gives no value.
- If not isinstance(options, dict).
  - Return mapping().
- Return mapping of key → value for tuple(key, value) drawn from options.items() where (meta.has\_field(key) and isinstance(value, ((str bitwise or int) bitwise or float))).
  - Draw tuple(key, value) from options.items(), keep a combination only if ((meta.has\_field(key) and isinstance(value, ((str bitwise or int) bitwise or float)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.has\_field(key) → isinstance(value, ((str bitwise or int) bitwise or float)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L728)

<a id="op-83fb3244aaf33e"></a>
### Onboarding Step.throw if unfinished

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_onboardingstep_throw_if_unfinished`

**Inputs** self.

**Record and data access** read “Module Onboarding” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Finish {0} to finish this step.”.format(translated title) · validation helper — translated “Set {0} in {1} to finish this step.”.format(label, doctype) · validation helper — translated “Submit a {0} to finish this step.”.format(doctype) · validation helper — translated “Create a {0} to finish this step.”.format(doctype).

**Local steps**

- If self.is\_work\_done() is distinct from false.
  - Return no value.
- If self.action equals “Complete Onboarding”.
  - Set title from Platform.db.get\_value(“Module Onboarding”, self.module\_onboarding, “title”).
  - Call the validation error handler Platform.throw(translated “Finish {0} to finish this step.”.format(translated title)).
- Set doctype from translated self.reference\_document.
- If self.action equals “Update Settings”.
  - Set label from translated Platform.get\_meta(self.reference\_document).get\_label(self.field).
  - Call the validation error handler Platform.throw(translated “Set {0} in {1} to finish this step.”.format(label, doctype)).
- Otherwise.
  - If Platform.get\_meta(self.reference\_document).is\_submittable.
    - Call the validation error handler Platform.throw(translated “Submit a {0} to finish this step.”.format(doctype)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Create a {0} to finish this step.”.format(doctype)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is work done](operations-046.md#op-70469febe62770).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L732)

<a id="op-3d467d01ebb181"></a>
### Get onboarding steps

`operation_foundation_desk_record_definitions_onboarding_step_business_behavior_get_onboarding_steps`

**Inputs** ob\_steps.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list of get\_step\_details(s.get(“step”), s.get(“is\_optional”)) for s drawn from steps.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to see this onboarding step”.

**Local steps**

- Bind dependencies can\_update\_step.
- Set steps from Platform.parse\_json(ob\_steps).
- For each step in steps.
  - If not can\_update\_step(step.get(“step”)).
    - Call the validation error handler Platform.throw(translated “You are not allowed to see this onboarding step”, Platform.PermissionError).
- Return list of get\_step\_details(s.get(“step”), s.get(“is\_optional”)) for s drawn from steps.
  - Draw s from steps.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L24) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L979)

<a id="op-b16a51868dc34f"></a>
### Get step details

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_get_step_details`

**Inputs** name, is\_optional = 0.

**Declared result** dict.

**Record and data access** resolve a document from “Onboarding Step” via get\_doc · read “DocType” via get\_value · read “Module Onboarding” via get\_value.

**Explicit results** step.

**Local steps**

- Set doc from Platform.get\_doc(“Onboarding Step”, name).
- Set step from doc.as\_dict().copy().
- Set step.is\_optional from int(bool(is\_optional)).
- Set step.label from translated doc.title.
- Set step.title from translated doc.title.
- Set step.description from translated doc.description when doc.description, otherwise no value.
  - Value choice on doc.description — true gives translated doc.description, false gives no value.
- Set step.action\_label from translated doc.action\_label when doc.action\_label, otherwise no value.
  - Value choice on doc.action\_label — true gives translated doc.action\_label, false gives no value.
- Set step.is\_complete from int(bool((doc.is\_complete or doc.is\_work\_done()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_complete → doc.is\_work\_done().
- If step.action equals “Create Entry”.
  - Set step.is\_submittable from Platform.db.get\_value(“DocType”, step.reference\_document, “is\_submittable”, cache = true).
  - Set step.can\_import from can\_import(step.reference\_document, step.is\_submittable).
- Otherwise.
  - If step.action equals “Complete Onboarding”.
    - Set step.module from Platform.db.get\_value(“Module Onboarding”, step.module\_onboarding, “module”).
- Return step.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L727)

<a id="op-5d6608f7bfaa04"></a>
### Can import

`operation_foundation_binding_foundation_desk_doctype_onboarding_step_onboarding_step_can_import`

**Inputs** doctype, is\_submittable.

**Declared result** bool.

**Explicit results** bool((not is\_submittable and Platform.get\_meta(doctype).allow\_import and Platform.has\_permission(doctype, “import”))).

**Local steps**

- Return bool((not is\_submittable and Platform.get\_meta(doctype).allow\_import and Platform.has\_permission(doctype, “import”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_submittable → Platform.get\_meta(doctype).allow\_import → Platform.has\_permission(doctype, “import”).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “import”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L268) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L726)

## Service · Page

<a id="op-04d4f94cb48f8d"></a>
### Text arg

`operation_foundation_binding_foundation_studio_ai_agent_tools_page_text_arg`

**Inputs** value.

**Declared result** str.

**Explicit results** value.strip() when isinstance(value, str), otherwise empty text.

**Local steps**

- Return value.strip() when isinstance(value, str), otherwise empty text.
  - Value choice on isinstance(value, str) — true gives value.strip(), false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1788)

<a id="op-fbbc134caedab2"></a>
### Load page

`operation_foundation_binding_foundation_studio_ai_agent_tools_page_load_page`

**Inputs** ctx.

**Record and data access** resolve a document from “Studio Page” via get\_doc.

**Explicit results** Platform.get\_doc(“Studio Page”, ctx.page\_id) when ctx.page\_id, otherwise no value.

**Local steps**

- Return Platform.get\_doc(“Studio Page”, ctx.page\_id) when ctx.page\_id, otherwise no value.
  - Value choice on ctx.page\_id — true gives Platform.get\_doc(“Studio Page”, ctx.page\_id), false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1786)

<a id="op-bf937f64d83dca"></a>
### Save page

`operation_foundation_binding_foundation_studio_ai_agent_tools_page_save_page`

**Inputs** page.

**Declared result** (str bitwise or no value).

**State and service calls** call save on page · commit · rollback.

**Explicit results** no value · str(e) · “could not save the change (see error log).”.

**Local steps**

- Attempt the following.
  - Evaluate page.save().
  - Evaluate Platform.db.commit().
  - Return no value.
- On failure (Platform.ValidationError) bound to e.
  - Evaluate Platform.db.rollback().
  - Return str(e).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(“Studio AI page child-table write failed”, Platform.get\_traceback(with\_context = true)).
  - Return “could not save the change (see error log).”.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1787)

<a id="op-2b098e71ecc171"></a>
### Dangling binding warning

`operation_foundation_binding_foundation_studio_ai_agent_tools_page_dangling_binding_warning`

**Inputs** ctx, name.

**Declared result** str.

**Explicit results** empty text · formatted text WARNING: these blocks still bind '{name}' and now resolve to nothing — rebind or remove them: {hits}..

**Local steps**

- Set root from ctx.\_page\_root().
- If not root.
  - Return empty text.
- Set pattern from re.compile(((“\\{\\{&#91;^}&#93;\*\\b” + re.escape(name)) + “\\b&#91;^}&#93;\*\\}\\}”)).
- Set hits from list().
- For each tuple(block, \_depth) in walk\_blocks(root).
  - For each value in (block.get(“componentProps”) or mapping()).values().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentProps”) → mapping().
    - If (isinstance(value, str) and pattern.search(value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → pattern.search(value).
      - Evaluate hits.append(block.get(“componentId”)).
      - Leave the innermost loop without its normal-exhaustion alternative.
- If not hits.
  - Return empty text.
- Return formatted text WARNING: these blocks still bind '{name}' and now resolve to nothing — rebind or remove them: {hits}..

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1785)

## Service · Permissions

<a id="op-82a1b438e0ddd0"></a>
### Has session permission

`operation_foundation_binding_foundation_studio_permissions_has_session_permission`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L255) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L62) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L150)

<a id="op-4eb320792dc082"></a>
### Session query conditions

`operation_foundation_binding_foundation_studio_permissions_session_query_conditions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L257) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L64) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L152)

<a id="op-1587b29f81a571"></a>
### Has message permission

`operation_foundation_binding_foundation_studio_permissions_has_message_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L254) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L61) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L149)

<a id="op-a5222be84e725e"></a>
### Message query conditions

`operation_foundation_binding_foundation_studio_permissions_message_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L256) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L63) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L151)

## Service · Portal

<a id="op-7ad4708c7e1bd7"></a>
### Get context

`operation_foundation_public_pages_portal_business_behavior_get_context`

**Inputs** context, remaining named values dict\_params.

**Explicit results** context.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Login to view”.

**Local steps**

- Evaluate Platform.local.form\_dict.update(dict\_params).
- Set context.show\_sidebar from true.
- Set doctype from Platform.local.form\_dict.doctype.
- If doctype.
  - Set meta from Platform.get\_meta(doctype).
  - If (Platform.session.user equals “Guest” and not meta.allow\_guest\_to\_view).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → not meta.allow\_guest\_to\_view.
    - Call the validation error handler Platform.throw(translated “Login to view”, Platform.PermissionError).
  - Set context.meta from meta.
  - Set list\_context from get\_list\_context(Platform.\_dict(), doctype, Platform.local.form\_dict.web\_form\_name).
  - Evaluate context.update(list\_context).
  - Evaluate context.update(get(list\_context, expanded names Platform.local.form\_dict)).
  - Set context.home\_page from “/portal”.
  - Set context.doctype from Platform.local.form\_dict.doctype.
- Return context.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L7076) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L53)

<a id="op-8cd1d36890e248"></a>
### Set route

`operation_foundation_public_pages_portal_business_behavior_set_route`

**Inputs** context.

**Local steps**

- If context.web\_form\_name.
  - Set context.route from formatted text {context.pathname}?name={quote(cstr(context.doc.name), safe = empty text)}.
- Otherwise.
  - If (context.doc and getattr(context.doc, “route”, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in context.doc → getattr(context.doc, “route”, no value).
    - Set context.route from context.doc.route.
  - Otherwise.
    - Set context.route from formatted text {(context.pathname or quoted(context.doc.doctype))}/{quote(cstr(context.doc.name), safe = empty text)}.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.pathname → quoted(context.doc.doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(context.doc, “route”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L68) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L54)

<a id="op-6f3bf401fe4b39"></a>
### Get

`operation_foundation_public_pages_portal_business_behavior_get`

**Inputs** list\_context (positional only) = no value, doctype = no value, txt = no value, limit\_start = 0, limit = 20, pathname = no value, remaining named values kwargs.

**Record and data access** resolve a document from doc.doctype via get\_doc.

**Explicit results** mapping(“result” → list(), “txt” → txt) · mapping(“raw\_result” → json.dumps(raw\_result, default = json\_handler), “result” → result, “show\_more” → show\_more, “next\_start” → (limit\_start + limit), …).

**Local steps**

- Set limit\_start from cint(limit\_start).
- If list\_context is identical to no value.
  - Set list\_context from get\_list\_context(Platform.\_dict(), doctype, kwargs.get(“web\_form\_name”)).
- Set raw\_result from get\_list\_data\_for\_context(list\_context, doctype, txt, limit\_start, limit = (limit + 1), expanded names kwargs).
- Set show\_more from len(raw\_result) &gt; limit.
- If show\_more.
  - Set raw\_result from raw\_result at slice no value to negative 1.
- Set meta from Platform.get\_meta(doctype).
- If not raw\_result.
  - Return mapping(“result” → list(), “txt” → txt).
- If txt.
  - Set list\_context.default\_subtitle from translated “Filtered by "{0}"”.format(txt).
- Set result from list().
- Set row\_template from (list\_context.row\_template or “templates/includes/list/row\_template.html”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list\_context.row\_template → “templates/includes/list/row\_template.html”.
- Set list\_view\_fields from list of df for df drawn from meta.fields where df.in\_list\_view at slice no value to 4.
  - Draw df from meta.fields, keep a combination only if (df.in\_list\_view).
- For each doc in raw\_result.
  - Set doc.doctype from doctype.
  - Set new\_context from Platform.\_dict(doc = doc, meta = meta, list\_view\_fields = list\_view\_fields).
  - If (not list\_context.get\_list and not isinstance(new\_context.doc, Document)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not list\_context.get\_list → not isinstance(new\_context.doc, Document).
    - Set new\_context.doc from Platform.get\_doc(doc.doctype, doc.name).
    - Evaluate new\_context.update(new\_context.doc.as\_dict()).
  - If not Platform.in\_test.
    - Set pathname from (pathname or Platform.local.request.path).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in pathname → Platform.local.request.path.
    - Set new\_context at “pathname” from pathname.strip(“/ ”).
  - Evaluate new\_context.update(list\_context).
  - Evaluate set\_route(new\_context).
  - Set rendered\_row from Platform.render\_template(row\_template, new\_context, is\_path = true).
  - Evaluate result.append(rendered\_row).
- Bind dependencies json\_handler.
- Return mapping(“raw\_result” → json.dumps(raw\_result, default = json\_handler), “result” → result, “show\_more” → show\_more, “next\_start” → (limit\_start + limit), …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0546.json#L305) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L52)

## Service · Printpreview

<a id="op-962fce750beee3"></a>
### Get context

`operation_foundation_public_pages_printpreview_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Bind dependencies Platform.
- Bind dependencies uses\_legacy\_weasyprint.
- Bind dependencies is\_rtl.
- Bind dependencies get\_print\_filename, get\_print\_style, get\_rendered\_template, resolve\_print\_format, set\_link\_titles.
- Set doctype from Platform.form\_dict.doctype.
- Set docname from Platform.form\_dict.name.
- Set letterhead from Platform.form\_dict.get(“letterhead”).
- Set settings from Platform.parse\_json(Platform.form\_dict.get(“settings”)).
- Set doc from Platform.get\_doc(doctype, docname).
- Set tuple(pf, is\_beta) from resolve\_print\_format(Platform.form\_dict.print\_format, doc.meta).
- If uses\_legacy\_weasyprint(pf).
  - Bind dependencies get\_html.
  - Set context.body from get\_html(doctype, docname, pf, letterhead).
- Otherwise.
  - If is\_beta.
    - Bind dependencies get\_html.
    - Set context.body from get\_html(doctype, docname, pf, letterhead, settings = settings).
  - Otherwise.
    - Evaluate set\_link\_titles(doc).
    - Set body from get\_rendered\_template(doc, print\_format = pf, meta = doc.meta, letterhead = letterhead, settings = settings).
    - Set context.body from Platform.render\_template(“www/printview.html”, mapping(“standalone” → false, “no\_action\_banner” → true, “body” → body, “print\_style” → get\_print\_style(print\_format = pf), …)).
      - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_title() → doc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L69) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L55)

## Service · Printview

<a id="op-eb1fc8190944b6"></a>
### Get context

`operation_foundation_public_pages_printview_business_behavior_get_context`

**Inputs** context.

**Declared result** PrintContext.

**Explicit results** PrintContext(print\_style = empty text, comment = empty text, title = “Error”, lang = “en”, …) · context.

**Local steps**

- If not ((Platform.form\_dict.doctype and Platform.form\_dict.name) or Platform.form\_dict.doc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (Platform.form\_dict.doctype and Platform.form\_dict.name) → Platform.form\_dict.doc.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.form\_dict.doctype → Platform.form\_dict.name.
  - Return PrintContext(print\_style = empty text, comment = empty text, title = “Error”, lang = “en”, …).
- If Platform.form\_dict.doc.
  - Set doc from Platform.form\_dict.doc.
- Otherwise.
  - Set doc from Platform.get\_lazy\_doc(Platform.form\_dict.doctype, Platform.form\_dict.name).
- Evaluate set\_link\_titles(doc).
- Set settings from Platform.parse\_json(Platform.form\_dict.settings).
- Set letterhead from (Platform.form\_dict.letterhead or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.letterhead → no value.
- Set meta from Platform.get\_meta(doc.doctype).
- Set tuple(print\_format, standalone) from resolve\_print\_format(no value, meta).
- Set legacy\_weasyprint from uses\_legacy\_weasyprint(print\_format).
- If legacy\_weasyprint.
  - Set standalone from false.
- Set print\_format\_name from getattr(print\_format, “name”, “Standard”).
- Set pdf\_generator from Platform.form\_dict.get(“pdf\_generator”, getattr(print\_format, “pdf\_generator”, “wkhtmltopdf”)).
- Set context from mapping(“standalone” → standalone, “comment” → Platform.session.user, “title” → Platform.utils.strip\_html(cstr((doc.get\_title() or doc.name))), “print\_filename” → get\_print\_filename(doc), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_title() → doc.name.
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
  - Value choice on settings — true gives Platform.as\_json(settings, indent = no value), false gives no value.
- If legacy\_weasyprint.
  - Bind dependencies get\_html.
  - Set body from get\_html(doctype = Platform.form\_dict.doctype, name = Platform.form\_dict.name, print\_format = print\_format, letterhead = letterhead).
  - Update body using + trigger\_print\_script.
- Otherwise.
  - If standalone.
    - Bind dependencies get\_html.
    - Set body from get\_html(doctype = Platform.form\_dict.doctype, name = Platform.form\_dict.name, doc = doc, print\_format = print\_format, …).
  - Otherwise.
    - Set body from get\_rendered\_template(doc, print\_format = print\_format, meta = meta, trigger\_print = Platform.form\_dict.trigger\_print, no\_letterhead = Platform.form\_dict.no\_letterhead, …).
- Evaluate make\_access\_log(doctype = Platform.form\_dict.doctype, document = Platform.form\_dict.name, file\_type = “PDF”, method = “Print”, …).
- Evaluate context.update(mapping(“body” → body, “print\_style” → empty text when standalone, otherwise get\_print\_style(Platform.form\_dict.style, print\_format, overrides = get\_allowed\_print\_settings\_override(doc, settings)))).
  - Value choice on standalone — true gives empty text, false gives get\_print\_style(Platform.form\_dict.style, print\_format, overrides = get\_allowed\_print\_settings\_override(doc, settings)).
- Return context.

**Values supplied outside this operation** selected callable from getattr(print\_format, “name”, “Standard”), getattr(print\_format, “pdf\_generator”, “wkhtmltopdf”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L71) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L59)

<a id="op-e659378330b1c3"></a>
### Cast client values

`operation_foundation_binding_foundation_www_printview_cast_client_values`

**Inputs** document.

**Local steps**

- Bind dependencies table\_fields.
- Bind dependencies cast.
- Set rows from list(document).
- For each df in document.meta.get\_table\_fields().
  - Evaluate rows.extend((document.get(df.fieldname) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in document.get(df.fieldname) → list().
- For each row in rows.
  - For each df in row.meta.fields.
    - Set value from row.get(df.fieldname).
    - If (value belongs to tuple(no value, empty text) or df.fieldtype belongs to table\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value belongs to tuple(no value, empty text) → df.fieldtype belongs to table\_fields.
      - Continue with the next iteration or loop test.
    - Set messages from len(Platform.local.message\_log).
    - Attempt the following.
      - Evaluate row.set(df.fieldname, cast(df.fieldtype, value)).
    - On failure (Platform.ValidationError).
      - Remove Platform.local.message\_log at slice messages to no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L79) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L472)

<a id="op-6b6448db4c5e36"></a>
### Get print format doc

`operation_foundation_public_pages_printview_business_behavior_get_print_format_record`

**Inputs** print\_format\_name, meta.

**Declared result** (“PrintFormat” bitwise or no value).

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Explicit results** no value · Platform.get\_doc(“Print Format”, print\_format\_name).

**Local steps**

- If not print\_format\_name.
  - Set print\_format\_name from (Platform.form\_dict.format or meta.default\_print\_format or “Standard”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.format → meta.default\_print\_format → “Standard”.
- If print\_format\_name equals “Standard”.
  - Return no value.
- Otherwise.
  - Attempt the following.
    - Return Platform.get\_doc(“Print Format”, print\_format\_name).
  - On failure (Platform.DoesNotExistError).
    - Return no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L74) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L64)

<a id="op-01566894bf3b2d"></a>
### Resolve print format

`operation_foundation_public_pages_printview_business_behavior_resolve_print_format`

**Inputs** print\_format\_name, meta.

**Declared result** tuple at tuple(“PrintFormat \| None”, bool).

**Explicit results** tuple(print\_format, uses\_beta\_renderer(print\_format)).

**Local steps**

- Set print\_format from get\_print\_format\_doc(print\_format\_name, meta = meta).
- Return tuple(print\_format, uses\_beta\_renderer(print\_format)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L79) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L75)

<a id="op-763588cbd81712"></a>
### Get print filename

`operation_foundation_binding_foundation_www_printview_get_print_filename`

**Inputs** doc.

**Declared result** str.

**Explicit results** get\_safe\_file\_name(cstr(doc.name)).

**Local steps**

- Bind dependencies get\_safe\_file\_name.
- Return get\_safe\_file\_name(cstr(doc.name)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L86) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L479)

<a id="op-9e49138aac0117"></a>
### Get rendered template

`operation_foundation_public_pages_printview_business_behavior_get_rendered_template`

**Inputs** doc, print\_format = no value, meta = no value, no\_letterhead = no value, letterhead = no value, trigger\_print = false, settings = no value.

**Declared result** str.

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc.

**Explicit results** html.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to print draft documents” · validation helper with Platform.PermissionError — translated “Not allowed to print cancelled documents”.

**Local steps**

- If not Platform.flags.ignore\_print\_permissions.
  - Evaluate validate\_print\_permission(doc).
- Set print\_settings from Platform.get\_cached\_doc(“Print Settings”).as\_dict().
- Evaluate print\_settings.update((settings or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings → mapping().
- If isinstance(no\_letterhead, str).
  - Set no\_letterhead from cint(no\_letterhead).
- Otherwise.
  - If no\_letterhead is identical to no value.
    - Set no\_letterhead from not cint(print\_settings.with\_letterhead).
- Set doc.flags.in\_print from true.
- Set doc.flags.print\_settings from print\_settings.
- If doc.meta.is\_submittable.
  - If (doc.docstatus.is\_draft() and not cint(print\_settings.allow\_print\_for\_draft)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_draft() → not cint(print\_settings.allow\_print\_for\_draft).
    - Call the validation error handler Platform.throw(translated “Not allowed to print draft documents”, Platform.PermissionError).
  - If (doc.docstatus.is\_cancelled() and not cint(print\_settings.allow\_print\_for\_cancelled)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_cancelled() → not cint(print\_settings.allow\_print\_for\_cancelled).
    - Call the validation error handler Platform.throw(translated “Not allowed to print cancelled documents”, Platform.PermissionError).
- Evaluate doc.run\_method(“before\_print”, print\_settings).
- If not hasattr(doc, “print\_heading”).
  - Set doc.print\_heading from no value.
- If not hasattr(doc, “sub\_heading”).
  - Set doc.sub\_heading from no value.
- If not meta.
  - Set meta from Platform.get\_meta(doc.doctype).
- Set jenv from Platform.get\_jenv().
- Set tuple(format\_data, format\_data\_map) from tuple(list(), mapping()).
- If print\_format.
  - Set doc.print\_section\_headings from print\_format.show\_section\_headings.
  - Set doc.print\_line\_breaks from print\_format.line\_breaks.
  - Set doc.align\_labels\_right from print\_format.align\_labels\_right.
  - Set doc.absolute\_value from print\_format.absolute\_value.
  - Bind local operation get\_template\_from\_string for subsequent calls.
  - Set template from no value.
  - If hook\_func bound to Platform.get\_hooks(“get\_print\_format\_template”).
    - Set template from Platform.call(hook\_func at negative 1, jenv = jenv, print\_format = print\_format).
  - If template.
    - Take no action here.
  - Otherwise.
    - If print\_format.custom\_format.
      - Set template from get\_template\_from\_string().
    - Otherwise.
      - If is\_classic\_layout(print\_format.format\_data).
        - Set format\_data from json.loads(print\_format.format\_data).
        - For each df in format\_data.
          - Set format\_data\_map at df.get(“fieldname”) from df.
          - If “visible\_columns” belongs to df.
            - For each \_df in df.get(“visible\_columns”).
              - Set format\_data\_map at \_df.get(“fieldname”) from \_df.
        - Set doc.format\_data\_map from format\_data\_map.
        - Set template from “standard”.
      - Otherwise.
        - If print\_format.standard equals “Yes”.
          - Set template from get\_template\_from\_string().
        - Otherwise.
          - Set template from “standard”.
- Otherwise.
  - Set template from “standard”.
- If template equals “standard”.
  - Set template from jenv.get\_template(standard\_format).
- Set letter\_head from Platform.\_dict((get\_letter\_head(doc, no\_letterhead, letterhead) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_letter\_head(doc, no\_letterhead, letterhead) → mapping().
- If letter\_head.content.
  - Set letter\_head.content from Platform.utils.jinja.render\_template(letter\_head.content, mapping(“doc” → doc.as\_dict())).
  - If letter\_head.custom\_css.
    - Update letter\_head.content using + formatted text   &lt;style&gt;  {letter\_head.custom\_css}  &lt;/style&gt;.
  - If letter\_head.header\_script.
    - Update letter\_head.content using + formatted text   &lt;script&gt;  {letter\_head.header\_script}  &lt;/script&gt;.
- If letter\_head.footer.
  - Set letter\_head.footer from Platform.utils.jinja.render\_template(letter\_head.footer, mapping(“doc” → doc.as\_dict())).
  - If letter\_head.footer\_script.
    - Update letter\_head.footer using + formatted text   &lt;script&gt;  {letter\_head.footer\_script}  &lt;/script&gt;.
- Evaluate convert\_markdown(doc).
- Set args from mapping().
- If (format\_data and format\_data at 0.get(“fieldname”) equals “print\_heading\_template”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in format\_data → format\_data at 0.get(“fieldname”) equals “print\_heading\_template”.
  - Set args at “print\_heading\_template” from format\_data.pop(0).get(“options”).
- Evaluate args.update(mapping(“doc” → doc, “meta” → Platform.get\_meta(doc.doctype), “layout” → make\_layout(doc, meta, format\_data), “no\_letterhead” → no\_letterhead, …)).
- Set hook\_func from Platform.get\_hooks(“pdf\_body\_html”).
- Set html from Platform.get\_attr(hook\_func at negative 1)(jenv = jenv, template = template, print\_format = print\_format, args = args).
- If cint(trigger\_print).
  - Update html using + trigger\_print\_script.
- Return html.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Settings”) · selected callable from doc.run\_method(“before\_print”, print\_settings), Platform.get\_hooks(“get\_print\_format\_template”) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L77) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L67)

<a id="op-2ec37d0d252c6e"></a>
### Get rendered template.get template from string

`operation_foundation_binding_foundation_www_printview_get_rendered_template_get_template_from_string`

**Inputs** no declared parameters.

**Explicit results** jenv.from\_string(get\_print\_format(doc.doctype, print\_format)).

**Local steps**

- Return jenv.from\_string(get\_print\_format(doc.doctype, print\_format)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L87) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L480)
