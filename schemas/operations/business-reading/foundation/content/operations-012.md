# Web content and issued documents · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Router

<a id="op-d7509117b4572c"></a>
### Setup source

`operation_foundation_website_router_business_behavior_setup_source`

**Inputs** page\_info.

**Local steps**

- Set jenv from Platform.get\_jenv().
- Set source from jenv.loader.get\_source(jenv, page\_info.template) at 0.
- Set html from empty text.
- If page\_info.template.endswith(tuple(“.md”, “.html”)).
  - Attempt the following.
    - Set res from get\_frontmatter(source).
    - If res at “attributes”.
      - Evaluate page\_info.update(res at “attributes”).
      - Set source from res at “body”.
  - On failure (Exception).
    - Take no action here.
  - If page\_info.template.endswith(“.md”).
    - Set source from Platform.utils.md\_to\_html(source).
    - Set page\_info.page\_toc\_html from source.toc\_html.
    - If not page\_info.show\_sidebar.
      - Set source from ((text in the contract + source) + “&lt;/div&gt;”).
- If not page\_info.base\_template.
  - Set page\_info.base\_template from get\_base\_template(page\_info.route).
- If (page\_info.template.endswith(tuple(“.html”, “.md”)) and “{%- extends” does not belong to source and “{% extends” does not belong to source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in page\_info.template.endswith(tuple(“.html”, “.md”)) → “{%- extends” does not belong to source → “{% extends” does not belong to source.
  - Set html from source.
- Set js\_path from os.path.join(page\_info.basepath, ((page\_info.basename or “index”) + “.js”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.basename → “index”.
- If (os.path.exists(js\_path) and “{% block script %}” does not belong to html).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(js\_path) → “{% block script %}” does not belong to html.
  - Within open(js\_path, encoding = “utf-8”) bound as f.
    - Set js from f.read().
    - Set page\_info.colocated\_js from js.
- Set css\_path from os.path.join(page\_info.basepath, ((page\_info.basename or “index”) + “.css”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.basename → “index”.
- If (os.path.exists(css\_path) and “{% block style %}” does not belong to html).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(css\_path) → “{% block style %}” does not belong to html.
  - Within open(css\_path, encoding = “utf-8”) bound as f.
    - Set css from f.read().
    - Set page\_info.colocated\_css from css.
- If html.
  - Set page\_info.source from html.
  - Set page\_info.base\_template from (page\_info.base\_template or “templates/web.html”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.base\_template → “templates/web.html”.
- Otherwise.
  - Set page\_info.source from empty text.
- Evaluate setup\_index(page\_info).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L1684) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1532)

<a id="op-12457067444809"></a>
### Get base template

`operation_foundation_website_router_business_behavior_get_base_template`

**Inputs** path = no value.

**Explicit results** templates at negative 1.

**Local steps**

- If not path.
  - Set path from Platform.local.request.path.
- Set base\_template\_map from (Platform.get\_hooks(“base\_template\_map”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“base\_template\_map”) → mapping().
- Set patterns from list(base\_template\_map.keys()).
- Set patterns\_desc from sorted(patterns, key = deferred anonymous expression, reverse = true).
- For each pattern in patterns\_desc.
  - If re.match(pattern, path).
    - Set templates from base\_template\_map at pattern.
    - Return templates at negative 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“base\_template\_map”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L2743) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1520)

<a id="op-e714893fdf2257"></a>
### Setup index

`operation_foundation_website_router_business_behavior_setup_index`

**Inputs** page\_info.

**Local steps**

- If page\_info.basename equals empty text.
  - Set index\_txt\_path from os.path.join(page\_info.basepath, “index.txt”).
  - If os.path.exists(index\_txt\_path).
    - Within open(index\_txt\_path) bound as f.
      - Set page\_info.index from f.read().splitlines().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L3045) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1531)

<a id="op-c242b021b4685f"></a>
### Load properties from controller

`operation_foundation_website_router_business_behavior_load_properties_from_controller`

**Inputs** page\_info.

**Explicit results** no value.

**Local steps**

- If not page\_info.controller.
  - Return no value.
- Set module from Platform.get\_module(page\_info.controller).
- If not module.
  - Return no value.
- For each prop in tuple(“base\_template\_path”, “template”, “no\_cache”, “sitemap”, …).
  - If hasattr(module, prop).
    - Set page\_info at prop from getattr(module, prop).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(module, prop).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L3242) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1530)

<a id="op-e03f0c843f30b8"></a>
### Get doctypes with web view

`operation_foundation_website_router_business_behavior_get_record_types_with_web_view`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.get\_value(“doctypes\_with\_web\_view”, \_get).

**Local steps**

- Bind local operation \_get for subsequent calls.
- Return Platform.cache.get\_value(“doctypes\_with\_web\_view”, \_get).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L59) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1527)

<a id="op-25155c07b005c9"></a>
### Get doctypes with web view.get

`operation_foundation_website_router_business_behavior_get_record_types_with_web_view_get`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**Explicit results** doctypes.

**Local steps**

- Set installed\_apps from Platform.get\_installed\_apps().
- Set doctypes from Platform.get\_hooks(“website\_generators”).
- Set doctypes\_with\_web\_view from Platform.get\_all(“DocType”, fields = list(“name”, “module”), filters = dict(has\_web\_view = 1)).
- Set module\_app\_map from Platform.local.module\_app.
- Set doctypes from (doctypes + list of d.name for d drawn from doctypes\_with\_web\_view where module\_app\_map.get(Platform.scrub(d.module)) belongs to installed\_apps).
  - Draw d from doctypes\_with\_web\_view, keep a combination only if (module\_app\_map.get(Platform.scrub(d.module)) belongs to installed\_apps).
- Return doctypes.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“website\_generators”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L60) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1528)

<a id="op-34ed82a2dcb5ac"></a>
### Get start folders

`operation_foundation_website_router_business_behavior_get_start_folders`

**Inputs** no declared parameters.

**Explicit results** (Platform.local.flags.web\_pages\_folders or tuple(“www”, “templates/pages”)).

**Local steps**

- Return (Platform.local.flags.web\_pages\_folders or tuple(“www”, “templates/pages”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.web\_pages\_folders → tuple(“www”, “templates/pages”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L4071) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1529)

<a id="op-e00bbc92bf90b0"></a>
### Clear routing cache

`operation_foundation_website_router_business_behavior_clear_routing_cache`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies get\_published\_web\_forms.
- Bind dependencies get\_dynamic\_web\_pages.
- Bind dependencies \_find\_matching\_document\_webview.
- Bind dependencies get\_public\_pages\_from\_doctypes.
- Evaluate \_find\_matching\_document\_webview.clear\_cache().
- Evaluate get\_dynamic\_web\_pages.clear\_cache().
- Evaluate get\_published\_web\_forms.clear\_cache().
- Evaluate get\_public\_pages\_from\_doctypes.clear\_cache().
- Evaluate Platform.cache.delete\_value(“home\_page”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L4131) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1518)

## Service · Serve

<a id="op-f38fc1d5c49f06"></a>
### Get response

`operation_foundation_website_serve_business_behavior_get_response`

**Inputs** path = no value, http\_status\_code = 200.

**Declared result** Response.

**Explicit results** renderer\_instance.render() · handle\_exception(e, endpoint, path, http\_status\_code).

**Local steps**

- Set path from (path or Platform.local.request.path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → Platform.local.request.path.
- Set endpoint from path.
- Attempt the following.
  - Set path\_resolver from PathResolver(path, http\_status\_code).
  - Set tuple(endpoint, renderer\_instance) from path\_resolver.resolve().
  - Return renderer\_instance.render().
- On failure (Exception) bound to e.
  - Return handle\_exception(e, endpoint, path, http\_status\_code).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L4298) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1533)

<a id="op-f764807ea9904e"></a>
### Handle exception

`operation_foundation_website_serve_business_behavior_handle_exception`

**Inputs** e, endpoint, path, http\_status\_code.

**Wrappers, in declaration order** handle\_does\_not\_exist\_error.

**Explicit results** RedirectPage((endpoint or path), e.http\_status\_code).render() · NotPermittedPage(endpoint, http\_status\_code, exception = e).render() · NotFoundPage(endpoint).render() · ErrorPage(exception = e).render().

**Local steps**

- If isinstance(e, Platform.Redirect).
  - Return RedirectPage((endpoint or path), e.http\_status\_code).render().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in endpoint → path.
- If isinstance(e, Platform.PermissionError).
  - Return NotPermittedPage(endpoint, http\_status\_code, exception = e).render().
- If isinstance(e, Platform.PageDoesNotExistError).
  - Return NotFoundPage(endpoint).render().
- Return ErrorPage(exception = e).render().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L61) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1536)

<a id="op-6f3b512b3986f2"></a>
### Get response content

`operation_foundation_website_serve_business_behavior_get_response_content`

**Inputs** path = no value, http\_status\_code = 200.

**Declared result** str.

**Explicit results** str(response.data, “utf-8”).

**Local steps**

- Set response from get\_response(path, http\_status\_code).
- Return str(response.data, “utf-8”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L4830) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1534)

<a id="op-9403ed2750ebae"></a>
### Get response without exception handling

`operation_foundation_website_serve_business_behavior_get_response_without_exception_handling`

**Inputs** path = no value, http\_status\_code = 200.

**Declared result** Response.

**Explicit results** renderer\_instance.render().

**Local steps**

- Set path from (path or Platform.local.request.path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → Platform.local.request.path.
- Set path\_resolver from PathResolver(path, http\_status\_code).
- Set tuple(\_endpoint, renderer\_instance) from path\_resolver.resolve().
- Return renderer\_instance.render().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L4936) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1535)

## Service · Sidebar

<a id="op-01f34fb20e0ed0"></a>
### Extract

`operation_foundation_gettext_extractors_sidebar_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- Set title from data.get(“title”).
- If title.
  - yield tuple(get\_line\_number(text, “title”, title), “\_”, title, list(“Title of a Sidebar”)).
- Set items from data.get(“items”, list()).
- If isinstance(items, list).
  - For each item in items.
    - Set label from item.get(“label”).
    - If label.
      - yield tuple(get\_line\_number(text, “label”, label), “\_”, label, list(“Label of a Sidebar Item”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L5) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L366)

## Service · Static page

<a id="op-bad0bde7378f1f"></a>
### Static Page.initialize

`operation_foundation_website_page_renderers_static_page_business_behavior_static_page_initialize`

**Inputs** self, path, http\_status\_code = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).
- Evaluate self.set\_file\_path().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set file path](operations-012.md#op-4f3e1486ee2d7f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6798) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1145)

<a id="op-4f3e1486ee2d7f"></a>
### Static Page.set file path

`operation_foundation_website_page_renderers_static_page_business_behavior_static_page_set_file_path`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.file\_path from empty text.
- If not self.is\_valid\_file\_path().
  - Return no value.
- For each app in Platform.get\_installed\_apps().
  - Set app\_path from Path(Platform.get\_app\_path(app, “www”)).
  - Set requested\_path from (app\_path ÷ self.path).resolve().
  - If (requested\_path.is\_relative\_to(app\_path) and requested\_path.is\_file() and is\_binary\_file(requested\_path)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in requested\_path.is\_relative\_to(app\_path) → requested\_path.is\_file() → is\_binary\_file(requested\_path).
    - Set self.file\_path from requested\_path.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is valid file path](operations-012.md#op-2fe7f1a10c704a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L22) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1148)

<a id="op-d98005202aea48"></a>
### Static Page.can render

`operation_foundation_website_page_renderers_static_page_business_behavior_static_page_can_render`

**Inputs** self.

**Explicit results** (self.is\_valid\_file\_path() and self.file\_path).

**Local steps**

- Return (self.is\_valid\_file\_path() and self.file\_path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_valid\_file\_path() → self.file\_path.

**Methods declared on this owner** [is valid file path](operations-012.md#op-2fe7f1a10c704a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L7185) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1144)

<a id="op-2fe7f1a10c704a"></a>
### Static Page.is valid file path

`operation_foundation_website_page_renderers_static_page_business_behavior_static_page_is_valid_file_path`

**Inputs** self.

**Explicit results** false · true.

**Local steps**

- Set extension from self.path.rsplit(“.”, 1) at negative 1 when “.” belongs to self.path, otherwise empty text.
  - Value choice on “.” belongs to self.path — true gives self.path.rsplit(“.”, 1) at negative 1, false gives empty text.
- If extension belongs to UNSUPPORTED\_STATIC\_PAGE\_TYPES.
  - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L7250) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1146)

<a id="op-31b798daa2e09d"></a>
### Static Page.render

`operation_foundation_website_page_renderers_static_page_business_behavior_static_page_render`

**Inputs** self.

**Explicit results** response.

**Local steps**

- Set f from open(self.file\_path, “rb”).
- Set response from Response(wrap\_file(Platform.local.request.environ, f), direct\_passthrough = true).
- Set response.mimetype from (mimetypes.guess\_type(self.file\_path) at 0 or “application/octet-stream”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in mimetypes.guess\_type(self.file\_path) at 0 → “application/octet-stream”.
- Return response.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L7392) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1147)

## Service · Template page

<a id="op-946e06ceba9e47"></a>
### Template Page.initialize

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_initialize`

**Inputs** self, path, http\_status\_code = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).
- Evaluate self.set\_template\_path().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set template path](operations-012.md#op-778862dcb884dc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L7580) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1159)

<a id="op-778862dcb884dc"></a>
### Template Page.set template path

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_set_template_path`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set folders from get\_start\_folders().
- For each app in reversed(Platform.get\_installed\_apps()).
  - Set app\_path from Platform.get\_app\_path(app).
  - For each dirname in folders.
    - Set search\_path from os.path.join(app\_path, dirname, self.path).
    - For each file\_path in self.get\_index\_path\_options(search\_path).
      - If (os.path.isfile(file\_path) and not is\_binary\_file(file\_path)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isfile(file\_path) → not is\_binary\_file(file\_path).
        - Set self.app from app.
        - Set self.app\_path from app\_path.
        - Set self.file\_dir from dirname.
        - Set self.basename from os.path.splitext(file\_path) at 0.
        - Set self.template\_path from os.path.relpath(file\_path, self.app\_path).
        - Set self.basepath from os.path.dirname(file\_path).
        - Set self.filename from os.path.basename(file\_path).
        - Set self.name from os.path.splitext(self.filename) at 0.
        - Return no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index path options](operations-012.md#op-180408858fc72f).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L23) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1172)

<a id="op-2636335fe25a83"></a>
### Template Page.can render

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_can_render`

**Inputs** self.

**Explicit results** (hasattr(self, “template\_path”) and self.template\_path and not self.template\_path.endswith(PY\_LOADER\_SUFFIXES)).

**Local steps**

- Return (hasattr(self, “template\_path”) and self.template\_path and not self.template\_path.endswith(PY\_LOADER\_SUFFIXES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “template\_path”) → self.template\_path → not self.template\_path.endswith(PY\_LOADER\_SUFFIXES).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L549) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1151)

<a id="op-180408858fc72f"></a>
### Template Page.get index path options

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_get_index_path_options`

**Inputs** search\_path.

**Wrappers, in declaration order** staticmethod.

**Explicit results** generator of Platform.as\_unicode(formatted text {search\_path}{d}) for d drawn from tuple(empty text, “.html”, “.md”, “/index.html”, …).

**Local steps**

- Return generator of Platform.as\_unicode(formatted text {search\_path}{d}) for d drawn from tuple(empty text, “.html”, “.md”, “/index.html”, …).
  - Draw d from tuple(empty text, “.html”, “.md”, “/index.html”, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L645) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1157)

<a id="op-39cd6490ff9770"></a>
### Template Page.render

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_render`

**Inputs** self.

**Explicit results** self.build\_response(html).

**Local steps**

- Set html from self.get\_html().
- Set html from self.add\_csrf\_token(html).
- Return self.build\_response(html).

**Methods declared on this owner** [get html](operations-012.md#op-f2c88195bf3b42).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L768) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1162)

<a id="op-f2c88195bf3b42"></a>
### Template Page.get html

`operation_foundation_website_page_renderers_template_page_business_behavior_template_page_get_document_markup`

**Inputs** self.

**Wrappers, in declaration order** cache\_html.

**Explicit results** html.

**Local steps**

- Evaluate self.init\_context().
- Evaluate self.set\_pymodule().
- Evaluate self.update\_context().
- Evaluate self.setup\_template\_source().
- Evaluate self.load\_colocated\_files().
- Evaluate self.set\_properties\_from\_source().
- Evaluate self.post\_process\_context().
- Set html from self.render\_template().
- Set html from self.update\_toc(html).
- Return html.

**Methods declared on this owner** [set pymodule](operations-013.md#op-88178654755576), [update context](operations-013.md#op-e9c1de74c5707e), [setup template source](operations-013.md#op-49f9b8968522fb), [load colocated files](operations-013.md#op-d82e35840cc43a), [set properties from source](operations-013.md#op-5ed7085339bf3a), [post process context](operations-013.md#op-ea924c88c79509), [render template](operations-013.md#op-7a8709e6640ce6), [update toc](operations-013.md#op-2ecb28b6b6b922).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L878) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1156)
