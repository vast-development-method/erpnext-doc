# Web content and issued documents · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Print page

<a id="op-3171664b60bd23"></a>
### Print Page.can render

`operation_foundation_website_page_renderers_print_page_business_behavior_print_page_can_render`

**Inputs** self.

**Record and data access** read “DocType” via exists.

**Explicit results** false · true.

**Local steps**

- Set parts from self.path.split(“/”, 1).
- If (len(parts) differs from 2 or not Platform.db.exists(“DocType”, parts at 0, true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(parts) differs from 2 → not Platform.db.exists(“DocType”, parts at 0, true).
  - Return false.
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6188) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1139)

<a id="op-4cf153b22b62f8"></a>
### Print Page.render

`operation_foundation_website_page_renderers_print_page_business_behavior_print_page_render`

**Inputs** self.

**Explicit results** super().render().

**Local steps**

- Set parts from self.path.split(“/”, 1).
- Set Platform.form\_dict.doctype from parts at 0.
- Set Platform.form\_dict.name from parts at 1.
- Evaluate self.set\_standard\_path(“printview”).
- Return super().render().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6358) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1140)

## Record · Print settings

[Record definition](../../../../data/record-types/print_settings.json)

<a id="op-b5dae185b8db32"></a>
### Print Settings.validate

`operation_foundation_printing_record_definitions_print_settings_business_behavior_print_settings_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Page height and width cannot be zero”.

**Local steps**

- If (self.pdf\_page\_size equals “Custom” and not (self.pdf\_page\_height and self.pdf\_page\_width)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pdf\_page\_size equals “Custom” → not (self.pdf\_page\_height and self.pdf\_page\_width).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pdf\_page\_height → self.pdf\_page\_width.
  - Call the validation error handler Platform.throw(translated “Page height and width cannot be zero”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3013) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L20)

<a id="op-77a530ce2514b0"></a>
### Print Settings.onload

`operation_foundation_binding_foundation_printing_doctype_print_settings_print_settings_printsettings_onload`

**Inputs** self.

**Record and data access** read “Print Format” via count.

**Local steps**

- Evaluate self.set\_onload(“wkhtmltopdf\_print\_formats”, Platform.db.count(“Print Format”, mapping(“pdf\_generator” → “wkhtmltopdf”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1680)

<a id="op-c7277eeb0082af"></a>
### Print Settings.on update

`operation_foundation_printing_record_definitions_print_settings_business_behavior_print_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3141) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L19)

<a id="op-246cddcfa80d0c"></a>
### Is print server enabled

`operation_foundation_printing_record_definitions_print_settings_business_behavior_is_print_server_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Print Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Print Settings”, “enable\_print\_server”).

**Local steps**

- Return Platform.get\_single\_value(“Print Settings”, “enable\_print\_server”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Print Settings”, “enable\_print\_server”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3190) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L18)

<a id="op-263882ad1467f4"></a>
### Follow print settings pdf generator

`operation_foundation_binding_foundation_printing_doctype_print_settings_print_settings_follow_print_settings_pdf_generator`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Print Format” via count · read “Print Format” via get\_all.

**State and service calls** request set\_value on “Print Format”.

**Explicit results** count.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set filters from mapping(“pdf\_generator” → “wkhtmltopdf”).
- Set count from Platform.db.count(“Print Format”, filters).
- Set doctypes from Platform.get\_all(“Print Format”, mapping(expand filters, “doc\_type” → tuple(“is”, “set”)), pluck = “doc\_type”, distinct = true).
- Evaluate Platform.db.set\_value(“Print Format”, filters, “pdf\_generator”, empty text, update\_modified = false).
- For each doctype in doctypes.
  - Evaluate Platform.clear\_cache(doctype = doctype).
- Return count.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1679)

## Record · Print style

[Record definition](../../../../data/record-types/print_style.json)

<a id="op-722bbb95fa1bf7"></a>
### Print Style.validate

`operation_foundation_printing_record_definitions_print_style_business_behavior_print_style_validate`

**Inputs** self.

**Explicit failure paths** validation helper — Platform.\_(“Standard Print Style cannot be changed. Please duplicate to edit.”).

**Local steps**

- If (self.standard equals 1 and not Platform.local.conf.get(“developer\_mode”) and not Platform.flags.in\_import and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard equals 1 → not Platform.local.conf.get(“developer\_mode”) → not Platform.flags.in\_import → not Platform.in\_test.
  - Call the validation error handler Platform.throw(Platform.\_(“Standard Print Style cannot be changed. Please duplicate to edit.”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3269) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L23)

<a id="op-8c2e962d88150c"></a>
### Print Style.on update

`operation_foundation_printing_record_definitions_print_style_business_behavior_print_style_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export doc](operations-011.md#op-a4c44271b53ae3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3436) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L22)

<a id="op-a4c44271b53ae3"></a>
### Print Style.export doc

`operation_foundation_printing_record_definitions_print_style_business_behavior_print_style_export_record`

**Inputs** self.

**Local steps**

- Bind dependencies export\_module\_json.
- Evaluate export\_module\_json(self, self.standard equals 1, “Printing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L3487) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L21)

## Service · Python

<a id="op-ffe66cd724ece5"></a>
### Extract

`operation_foundation_gettext_extractors_expression_runtime_business_behavior_extract`

**Inputs** remaining positional values args, remaining named values kwargs.

**Local steps**

- For each tuple(lineno, funcname, messages, comments) in extract\_python(expanded args, expanded names kwargs).
  - If (funcname equals “\_” and isinstance(messages, tuple) and len(messages) &gt; 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in funcname equals “\_” → isinstance(messages, tuple) → len(messages) &gt; 1.
    - Set funcname from “pgettext”.
    - Set messages from tuple(messages at negative 1, messages at 0).
  - yield tuple(lineno, funcname, messages, comments).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L4687) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L355)

## Service · Redirect page

<a id="op-8b85d082bc3d2c"></a>
### Redirect Page.initialize

`operation_foundation_website_page_renderers_redirect_page_business_behavior_redirect_page_initialize`

**Inputs** self, path, http\_status\_code = 301.

**Local steps**

- Set self.path from path.
- Set self.http\_status\_code from http\_status\_code.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6532) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1142)

<a id="op-8de73c7f351547"></a>
### Redirect Page.can render

`operation_foundation_website_page_renderers_redirect_page_business_behavior_redirect_page_can_render`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6614) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1141)

<a id="op-d8504497ab825a"></a>
### Redirect Page.render

`operation_foundation_website_page_renderers_redirect_page_business_behavior_redirect_page_render`

**Inputs** self.

**Explicit results** build\_response(self.path, empty text, self.http\_status\_code, mapping(“Location” → (Platform.flags.redirect\_location or (nested operand in the contract.response or mapping()).get(“location”)))).

**Local steps**

- Return build\_response(self.path, empty text, self.http\_status\_code, mapping(“Location” → (Platform.flags.redirect\_location or (nested operand in the contract.response or mapping()).get(“location”)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.redirect\_location → (Platform.local.response or mapping()).get(“location”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.response → mapping().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6651) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1143)

## Service · Report

<a id="op-3c4336dd42ba64"></a>
### Extract

`operation_foundation_gettext_extractors_report_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- If data.get(“doctype”) differs from “Report”.
  - Return no value.
- Set report\_name from data.get(“report\_name”).
- yield tuple(get\_line\_number(text, “report\_name”, report\_name), “\_”, report\_name, list(“Name of a report”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L4) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L365)

## Service · Request data

<a id="op-7d99f844747dd9"></a>
### Get context

`operation_foundation_website_web_form_request_data_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1805) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1571)

## Service · Request to delete data

<a id="op-9431a78ece4456"></a>
### Get context

`operation_foundation_website_web_form_request_to_delete_data_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1838) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1572)

## Service · Router

<a id="op-c0b72ec298208f"></a>
### Get page info from web page with dynamic routes

`operation_foundation_website_router_business_behavior_get_page_info_from_web_page_with_dynamic_routes`

**Inputs** path.

**Explicit results** page\_info at end\_point.

**Local steps**

- Bind dependencies get\_dynamic\_web\_pages.
- Set tuple(rules, page\_info) from tuple(list(), mapping()).
- For each d in get\_dynamic\_web\_pages().
  - Evaluate rules.append(Rule(formatted text /{d.route}, endpoint = d.name)).
  - Set d.doctype from (d.doctype or “Web Page”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.doctype → “Web Page”.
  - Set page\_info at d.name from d.
- Set end\_point from evaluate\_dynamic\_routes(rules, path).
- If end\_point.
  - Return page\_info at end\_point.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L5895) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1523)

<a id="op-0a9e63e7d788be"></a>
### Get page info from web form

`operation_foundation_website_router_business_behavior_get_page_info_from_web_form`

**Inputs** path.

**Explicit results** d.

**Local steps**

- Bind dependencies get\_published\_web\_forms.
- For each d in get\_published\_web\_forms().
  - If not (path.startswith(formatted text {d.route}) or path.startswith(formatted text /{d.route})).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in path.startswith(formatted text {d.route}) → path.startswith(formatted text /{d.route}).
    - Continue with the next iteration or loop test.
  - Set rules from list().
  - Evaluate rules.append(Rule(formatted text /{d.route}, endpoint = d.name)).
  - Evaluate rules.append(Rule(formatted text /{d.route}/list, endpoint = d.name)).
  - Evaluate rules.append(Rule(formatted text /{d.route}/new, endpoint = d.name)).
  - Evaluate rules.append(Rule(formatted text /{d.route}/&lt;name&gt;, endpoint = d.name)).
  - Evaluate rules.append(Rule(formatted text /{d.route}/&lt;name&gt;/edit, endpoint = d.name)).
  - Set d.doctype from “Web Form”.
  - Set end\_point from evaluate\_dynamic\_routes(rules, path).
  - If end\_point.
    - If path.endswith(“/list”).
      - Set Platform.form\_dict.is\_list from true.
    - Otherwise.
      - If path.endswith(“/new”).
        - Set Platform.form\_dict.is\_new from true.
      - Otherwise.
        - If path.endswith(“/edit”).
          - Set Platform.form\_dict.is\_edit from true.
        - Otherwise.
          - Set Platform.form\_dict.is\_read from true.
    - Return d.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L56) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1522)

<a id="op-96d69d64601d9c"></a>
### Evaluate dynamic routes

`operation_foundation_website_router_business_behavior_evaluate_dynamic_routes`

**Inputs** rules, path.

**Explicit results** endpoint.

**Local steps**

- Set route\_map from Map(rules).
- Set endpoint from no value.
- If (hasattr(Platform.local, “request”) and Platform.local.request.environ).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “request”) → Platform.local.request.environ.
  - Set urls from route\_map.bind\_to\_environ(Platform.local.request.environ).
  - Attempt the following.
    - Set tuple(endpoint, args) from urls.match((“/” + path)).
    - If args.
      - Set Platform.local.no\_cache from 1.
      - Evaluate Platform.local.form\_dict.update(args).
  - On failure (NotFound).
    - Take no action here.
- Return endpoint.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L7004) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1519)

<a id="op-428c8b8d972c12"></a>
### Get pages

`operation_foundation_website_router_business_behavior_get_pages`

**Inputs** app = no value.

**Explicit results** Platform.cache.get\_value(“website\_pages”, deferred anonymous expression).

**Local steps**

- Bind local operation \_build for subsequent calls.
- Return Platform.cache.get\_value(“website\_pages”, deferred anonymous expression).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L57) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1524)

<a id="op-1d22b85696291f"></a>
### Get pages.build

`operation_foundation_website_router_business_behavior_get_pages_build`

**Inputs** app.

**Explicit results** pages.

**Local steps**

- Set pages from mapping().
- If app.
  - Set apps from list(app).
- Otherwise.
  - Set apps from Platform.get\_installed\_apps().
- For each app in apps.
  - Set app\_path from Platform.get\_app\_path(app).
  - For each start in get\_start\_folders().
    - Evaluate pages.update(get\_pages\_from\_path(start, app, app\_path)).
- Return pages.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L58) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1525)

<a id="op-f2d86480ba0069"></a>
### Get pages from path

`operation_foundation_website_router_business_behavior_get_pages_from_path`

**Inputs** start, app, app\_path.

**Explicit results** pages.

**Local steps**

- Set pages from mapping().
- Set start\_path from os.path.join(app\_path, start).
- If os.path.exists(start\_path).
  - For each tuple(basepath, folders, files) in os.walk(start\_path).
    - For each fname in files.
      - Set fname from Platform.utils.cstr(fname).
      - If “.” does not belong to fname.
        - Continue with the next iteration or loop test.
      - Set tuple(page\_name, extn) from fname.rsplit(“.”, 1).
      - If (extn belongs to tuple(“js”, “css”) and os.path.exists(os.path.join(basepath, (page\_name + “.html”)))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in extn belongs to tuple(“js”, “css”) → os.path.exists(os.path.join(basepath, (page\_name + “.html”))).
        - Continue with the next iteration or loop test.
      - If extn belongs to tuple(“html”, “xml”, “js”, “css”, …).
        - Set page\_info from get\_page\_info(os.path.join(basepath, fname), app, start, basepath, …).
        - Set pages at page\_info.route from page\_info.
- Return pages.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1526)

<a id="op-a892491c7de482"></a>
### Get page info

`operation_foundation_website_router_business_behavior_get_page_info`

**Inputs** path, app, start, basepath = no value, app\_path = no value, fname = no value.

**Explicit results** page\_info.

**Local steps**

- If fname is identical to no value.
  - Set fname from os.path.basename(path).
- If app\_path is identical to no value.
  - Set app\_path from Platform.get\_app\_path(app).
- If basepath is identical to no value.
  - Set basepath from os.path.dirname(path).
- Set tuple(page\_name, extn) from os.path.splitext(fname).
- Set page\_info from Platform.\_dict().
- Set page\_info.basename from page\_name when extn belongs to tuple(“html”, “md”), otherwise fname.
  - Value choice on extn belongs to tuple(“html”, “md”) — true gives page\_name, false gives fname.
- Set page\_info.basepath from basepath.
- Set page\_info.page\_or\_generator from “Page”.
- Set page\_info.template from os.path.relpath(os.path.join(basepath, fname), app\_path).
- If page\_info.basename equals “index”.
  - Set page\_info.basename from empty text.
- Set page\_info.route from page\_info.template.replace(start, empty text).strip(“/”).
- If os.path.basename(page\_info.route) belongs to tuple(“index.html”, “index.md”).
  - Set page\_info.route from os.path.dirname(page\_info.route).
- If (page\_info.route.endswith(“.md”) or page\_info.route.endswith(“.html”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.route.endswith(“.md”) → page\_info.route.endswith(“.html”).
  - Set page\_info.route from page\_info.route.rsplit(“.”, 1) at 0.
- Set page\_info.name, page\_info.page\_name from page\_info.route.
- Set page\_info.controller\_path from os.path.join(basepath, (page\_name.replace(“-”, “\_”) + “.py”)).
- If os.path.exists(page\_info.controller\_path).
  - Set controller from ((app + “.”) + nested operand in the contract.path.relpath(page\_info.controller\_path, app\_path).replace(os.path.sep, “.”) at slice no value to negative 3).
  - Set page\_info.controller from controller.
- Evaluate setup\_source(page\_info).
- If not page\_info.title.
  - Set page\_info.title from extract\_title(page\_info.source, page\_info.route).
- Evaluate load\_properties\_from\_controller(page\_info).
- Return page\_info.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L556) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1521)
