# Web content and issued documents · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Network printer settings

[Record definition](../../../../data/record-types/network_printer_settings.json)

<a id="op-83af676e7e0df7"></a>
### Network Printer Settings.get printers list

`operation_foundation_printing_record_definitions_network_printer_settings_business_behavior_network_printer_settings_get_printers_list`

**Inputs** self, ip = “127.0.0.1”, port = 631.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · printer\_list.

**Explicit failure paths** validation helper — translated “This feature can not be used as dependencies are missing.\\n\\t\\t\\t\\tPlease contact your system manager to ena …” · validation helper — translated “Failed to connect to server”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set printer\_list from list().
- Attempt the following.
  - Bind dependencies cups.
- On failure (ImportError).
  - Call the validation error handler Platform.throw(translated “This feature can not be used as dependencies are missing.\\n\\t\\t\\t\\tPlease contact your system manager to ena …”).
  - Return no value.
- Attempt the following.
  - Evaluate cups.setServer(self.server\_ip).
  - Evaluate cups.setPort(self.port).
  - Set conn from cups.Connection().
  - Set printers from conn.getPrinters().
  - Evaluate printer\_list.extend(generator of mapping(“value” → printer\_id, “label” → printer at “printer-make-and-model”) for tuple(printer\_id, printer) drawn from printers.items()).
    - Draw tuple(printer\_id, printer) from printers.items().
- On failure (RuntimeError).
  - Call the validation error handler Platform.throw(translated “Failed to connect to server”).
- On failure (Platform.ValidationError).
  - Call the validation error handler Platform.throw(translated “Failed to connect to server”).
- Return printer\_list.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L47) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1735)

<a id="op-3f94472a7fe730"></a>
### Get network printer settings

`operation_foundation_printing_record_definitions_network_printer_settings_business_behavior_get_network_printer_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Network Printer Settings” via get\_list.

**Explicit results** Platform.db.get\_list(“Network Printer Settings”, pluck = “name”).

**Local steps**

- Return Platform.db.get\_list(“Network Printer Settings”, pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0313.json#L877) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1734)

## Service · Not found page

<a id="op-caf49d03f0e5ab"></a>
### Not Found Page.initialize

`operation_foundation_website_page_renderers_not_found_page_business_behavior_not_found_page_initialize`

**Inputs** self, path, http\_status\_code = no value.

**Local steps**

- Set self.request\_path from path.
- Set self.request\_url from Platform.local.request.url when hasattr(Platform.local, “request”), otherwise empty text.
  - Value choice on hasattr(Platform.local, “request”) — true gives Platform.local.request.url, false gives empty text.
- Set path from “404”.
- Set http\_status\_code from (http\_status\_code or 404).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in http\_status\_code → 404.
- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L4558) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1133)

<a id="op-75697d6724b193"></a>
### Not Found Page.can render

`operation_foundation_website_page_renderers_not_found_page_business_behavior_not_found_page_can_render`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L4763) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1132)

<a id="op-6174ea6bb84a68"></a>
### Not Found Page.render

`operation_foundation_website_page_renderers_not_found_page_business_behavior_not_found_page_render`

**Inputs** self.

**Explicit results** super().render().

**Local steps**

- If self.can\_cache\_404().
  - Evaluate Platform.cache.hset(“website\_404”, self.request\_url, true).
- Return super().render().

**Methods declared on this owner** [can cache 404](operations-005.md#op-990e27efed2fcf).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L4800) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1135)

<a id="op-990e27efed2fcf"></a>
### Not Found Page.can cache 404

`operation_foundation_website_page_renderers_not_found_page_business_behavior_not_found_page_can_cache_404`

**Inputs** self.

**Explicit results** (can\_cache() and self.request\_url and not self.is\_custom\_home\_page()).

**Local steps**

- Return (can\_cache() and self.request\_url and not self.is\_custom\_home\_page()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_cache() → self.request\_url → not self.is\_custom\_home\_page().

**Methods declared on this owner** [is custom home page](operations-005.md#op-cdca8cd72a3136).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L20) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1131)

<a id="op-cdca8cd72a3136"></a>
### Not Found Page.is custom home page

`operation_foundation_website_page_renderers_not_found_page_business_behavior_not_found_page_is_custom_home_page`

**Inputs** self.

**Explicit results** (request\_url belongs to HOMEPAGE\_PATHS and request\_path does not belong to HOMEPAGE\_PATHS).

**Local steps**

- Set url\_parts from urlparse(self.request\_url).
- Set request\_url from os.path.splitext(url\_parts.path) at 0.
- Set request\_path from os.path.splitext(self.request\_path) at 0.
- Return (request\_url belongs to HOMEPAGE\_PATHS and request\_path does not belong to HOMEPAGE\_PATHS).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in request\_url belongs to HOMEPAGE\_PATHS → request\_path does not belong to HOMEPAGE\_PATHS.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L5022) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1134)

## Service · Not permitted page

<a id="op-0ba53215a8ce48"></a>
### Not Permitted Page.initialize

`operation_foundation_website_page_renderers_not_permitted_page_business_behavior_not_permitted_page_initialize`

**Inputs** self, path = no value, http\_status\_code = no value, exception = empty text.

**Local steps**

- Set Platform.local.message from cstr(exception).
- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).
- Set self.http\_status\_code from 403.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L5466) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1137)

<a id="op-a6fa5cb23f456c"></a>
### Not Permitted Page.can render

`operation_foundation_website_page_renderers_not_permitted_page_business_behavior_not_permitted_page_can_render`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L5625) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1136)

<a id="op-21336a3644e0b2"></a>
### Not Permitted Page.render

`operation_foundation_website_page_renderers_not_permitted_page_business_behavior_not_permitted_page_render`

**Inputs** self.

**Explicit results** super().render().

**Local steps**

- Set action from formatted text /login?redirect-to={quote\_plus(Platform.request.path)}.
- If (Platform.request.path.startswith(“/desk/”) or Platform.request.path equals “/desk”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.request.path.startswith(“/desk/”) → Platform.request.path equals “/desk”.
  - Set action from “/login”.
- Set Platform.local.message\_title from translated “Not Permitted”.
- Set Platform.local.response at “context” from dict(indicator\_color = “red”, primary\_action = action, primary\_label = translated “Login”, fullpage = true).
- Evaluate self.set\_standard\_path(“message”).
- Return super().render().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L21) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1138)

## Service · Onboarding step

<a id="op-66acc043cae39f"></a>
### Extract

`operation_foundation_gettext_extractors_onboarding_step_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- If data.get(“doctype”) differs from “Onboarding Step”.
  - Return no value.
- Set step\_title from data.get(“title”).
- yield tuple(get\_line\_number(text, “title”, step\_title), “\_”, step\_title, list(“Title of an Onboarding Step”)).
- If action\_label bound to data.get(“action\_label”).
  - yield tuple(get\_line\_number(text, “action\_label”, action\_label), “\_”, action\_label, list(formatted text Label of an action in the Onboarding Step '{step\_title}')).
- If description bound to data.get(“description”).
  - yield tuple(get\_line\_number(text, “description”, description), “\_”, description, list(formatted text Description of the Onboarding Step '{step\_title}')).
- If report\_description bound to data.get(“report\_description”).
  - yield tuple(get\_line\_number(text, “report\_description”, report\_description), “\_”, report\_description, list(formatted text Description of a report in the Onboarding Step '{step\_title}')).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L121) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L360)

## Service · Path resolver

<a id="op-30c4a844493ce5"></a>
### Is Platform test fixture

`operation_foundation_website_path_resolver_business_behavior_is_foundation_test_fixture`

**Inputs** endpoint.

**Declared result** bool.

**Explicit results** false · any(generator of os.path.exists((target + suffix)) for suffix drawn from tuple(empty text, “.html”, “.md”, “/index.html”, …)).

**Local steps**

- If (endpoint differs from “\_test” and not endpoint.startswith(“\_test/”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in endpoint differs from “\_test” → not endpoint.startswith(“\_test/”).
  - Return false.
- Set www from os.path.join(Platform.get\_app\_path(“Platform”), “www”).
- Set target from os.path.normpath(os.path.join(www, endpoint)).
- If os.path.commonpath(tuple(www, target)) differs from www.
  - Return false.
- Return any(generator of os.path.exists((target + suffix)) for suffix drawn from tuple(empty text, “.html”, “.md”, “/index.html”, …)).
  - Draw suffix from tuple(empty text, “.html”, “.md”, “/index.html”, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L5874) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1181)

<a id="op-84eeb7c0400e62"></a>
### Path Resolver.initialize

`operation_foundation_website_path_resolver_business_behavior_path_resolver_initialize`

**Inputs** self, path, http\_status\_code = no value.

**Local steps**

- Set self.path from path.strip(“/ ”).
- Set self.http\_status\_code from http\_status\_code.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L6224) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1183)

<a id="op-3209635ac4d5af"></a>
### Path Resolver.resolve

`operation_foundation_website_path_resolver_business_behavior_path_resolver_resolve`

**Inputs** self.

**Explicit results** tuple(“desk”, TemplatePage(“desk”, self.http\_status\_code)) · tuple(self.path, NotFoundPage(self.path)) · tuple(Platform.flags.redirect\_location, RedirectPage(self.path, e.http\_status\_code)) · tuple(Platform.flags.redirect\_location, RedirectPage(e.new\_url, e.code)) · tuple(endpoint, NotFoundPage(endpoint)) · 1 additional forms in the steps below.

**Local steps**

- Set request from Platform.\_dict().
- If hasattr(Platform.local, “request”).
  - Set request from (Platform.local.request or request).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.request → request.
- If (self.path equals “desk” or self.path.startswith(“desk/”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.path equals “desk” → self.path.startswith(“desk/”).
  - Return tuple(“desk”, TemplatePage(“desk”, self.http\_status\_code)).
- If (request.url and can\_cache() and Platform.cache.hget(“website\_404”, request.url)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in request.url → can\_cache() → Platform.cache.hget(“website\_404”, request.url).
  - Return tuple(self.path, NotFoundPage(self.path)).
- Attempt the following.
  - Evaluate resolve\_redirect(self.path, request.query\_string).
- On failure (Platform.Redirect) bound to e.
  - Return tuple(Platform.flags.redirect\_location, RedirectPage(self.path, e.http\_status\_code)).
- If Platform.get\_hooks(“website\_path\_resolver”).
  - For each handler in Platform.get\_hooks(“website\_path\_resolver”).
    - Set endpoint from Platform.get\_attr(handler)(self.path).
- Otherwise.
  - Attempt the following.
    - Set endpoint from resolve\_path(self.path).
  - On failure (werkzeug.routing.exceptions.RequestRedirect) bound to e.
    - Set Platform.flags.redirect\_location from e.new\_url.
    - Return tuple(Platform.flags.redirect\_location, RedirectPage(e.new\_url, e.code)).
- If (not (Platform.conf.developer\_mode or Platform.conf.allow\_tests) and \_is\_Platform\_test\_fixture(endpoint)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (Platform.conf.developer\_mode or Platform.conf.allow\_tests) → \_is\_Platform\_test\_fixture(endpoint).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.conf.allow\_tests.
  - Return tuple(endpoint, NotFoundPage(endpoint)).
- Set custom\_renderers from self.get\_custom\_page\_renderers().
- Set renderers from list(expanded custom\_renderers, StaticPage, WebFormPage, DocumentPage, …).
- For each renderer in renderers.
  - Set renderer\_instance from renderer(endpoint, self.http\_status\_code).
  - If renderer\_instance.can\_render().
    - Return tuple(endpoint, renderer\_instance).
- Return tuple(endpoint, NotFoundPage(endpoint)).

**Methods declared on this owner** [get custom page renderers](operations-005.md#op-eacc26db608f40).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“website\_path\_resolver”), Platform.get\_attr(handler).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L26) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1185)

<a id="op-6743a960ee5e9e"></a>
### Path Resolver.is valid path

`operation_foundation_website_path_resolver_business_behavior_path_resolver_is_valid_path`

**Inputs** self.

**Explicit results** not isinstance(renderer\_instance, NotFoundPage).

**Local steps**

- Set tuple(\_endpoint, renderer\_instance) from self.resolve().
- Return not isinstance(renderer\_instance, NotFoundPage).

**Methods declared on this owner** [resolve](operations-005.md#op-3209635ac4d5af).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L7242) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1184)

<a id="op-eacc26db608f40"></a>
### Path Resolver.get custom page renderers

`operation_foundation_website_path_resolver_business_behavior_path_resolver_get_custom_page_renderers`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** custom\_renderers.

**Local steps**

- Bind dependencies click.
- Set custom\_renderers from list().
- For each renderer\_path in (Platform.get\_hooks(“page\_renderer”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“page\_renderer”) → list().
  - Attempt the following.
    - Set renderer from Platform.get\_attr(renderer\_path).
    - If not hasattr(renderer, “can\_render”).
      - Evaluate click.echo(formatted text {renderer.\_\_name\_\_} does not have can\_render method).
      - Continue with the next iteration or loop test.
    - If not hasattr(renderer, “render”).
      - Evaluate click.echo(formatted text {renderer.\_\_name\_\_} does not have render method).
      - Continue with the next iteration or loop test.
    - Evaluate custom\_renderers.append(renderer).
  - On failure (Exception).
    - Evaluate click.echo(formatted text Failed to load page renderer. Import path: {renderer\_path}).
- Return custom\_renderers.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“page\_renderer”), Platform.get\_attr(renderer\_path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0536.json#L7336) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1182)

<a id="op-192094a3e11737"></a>
### Resolve redirect

`operation_foundation_website_path_resolver_business_behavior_resolve_redirect`

**Inputs** path, query\_string = no value.

**Explicit results** no value.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- Bind local operation raise\_redirect for subsequent calls.
- Set redirects from Platform.get\_hooks(“website\_redirects”).
- Set use\_cache from not (query\_string and any(generator of rule.get(“match\_with\_query\_string”) for rule drawn from redirects)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query\_string → any(generator of rule.get(“match\_with\_query\_string”) for rule drawn from redirects).
  - Draw rule from redirects.
- Set redirect\_to from Platform.cache.hget(“website\_redirects”, (path or “/”)) when use\_cache, otherwise no value.
  - Value choice on use\_cache — true gives Platform.cache.hget(“website\_redirects”, (path or “/”)), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → “/”.
- If redirect\_to.
  - If isinstance(redirect\_to, dict).
    - Evaluate raise\_redirect(redirect\_to at “path”, redirect\_to.get(“status\_code”, 301), redirect\_to.get(“forward\_query\_parameters”, false)).
  - Set Platform.flags.redirect\_location from redirect\_to.
  - Raise Platform.Redirect.
- If redirect\_to is identical to false.
  - Return no value.
- Set redirects from (redirects + list of mapping(“source” → r.source, “target” → r.target, “redirect\_http\_status” → r.redirect\_http\_status, “forward\_query\_parameters” → r.get(“forward\_query\_parameters”)) for r drawn from (Pla ….
  - Draw r from (Platform.get\_website\_settings(“route\_redirects”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_website\_settings(“route\_redirects”) → list().
- If not redirects.
  - Return no value.
- For each rule in redirects.
  - Set pattern from (rule at “source”.strip(“/ ”) + “$”).
  - Set path\_to\_match from path.
  - If (query\_string and rule.get(“match\_with\_query\_string”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in query\_string → rule.get(“match\_with\_query\_string”).
    - Set path\_to\_match from ((path + “?”) + Platform.safe\_decode(query\_string)).
  - Attempt the following.
    - Set match from re.match(pattern, path\_to\_match).
  - On failure (re.error).
    - Evaluate Platform.log\_error((“Broken Redirect: ” + pattern)).
  - If match.
    - Set redirect\_to from re.sub(pattern, rule at “target”, path\_to\_match).
    - Set status\_code from (rule.get(“redirect\_http\_status”) or 301).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.get(“redirect\_http\_status”) → 301.
    - If use\_cache.
      - Evaluate Platform.cache.hset(“website\_redirects”, (path or “/”), mapping(“path” → redirect\_to, “status\_code” → status\_code, “forward\_query\_parameters” → rule.get(“forward\_query\_parameters”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → “/”.
    - Evaluate raise\_redirect(redirect\_to, status\_code, rule.get(“forward\_query\_parameters”)).
- If use\_cache.
  - Evaluate Platform.cache.hset(“website\_redirects”, (path or “/”), false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in path → “/”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“website\_redirects”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L27) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1188)

<a id="op-917c8ce5094337"></a>
### Resolve redirect.raise redirect

`operation_foundation_website_path_resolver_business_behavior_resolve_redirect_raise_redirect`

**Inputs** redirect\_location, status\_code = 301, forward\_query\_params = false.

**Explicit failure paths** Platform.Redirect(status\_code).

**Local steps**

- If (forward\_query\_params and query\_string).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in forward\_query\_params → query\_string.
  - Set separator from “&amp;” when “?” belongs to redirect\_location, otherwise “?”.
    - Value choice on “?” belongs to redirect\_location — true gives “&amp;”, false gives “?”.
  - Update redirect\_location using + (separator + Platform.safe\_decode(query\_string)).
- Set Platform.flags.redirect\_location from redirect\_location.
- Raise Platform.Redirect(status\_code).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L1227) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1189)

<a id="op-6ff7764c580ef7"></a>
### Resolve path

`operation_foundation_website_path_resolver_business_behavior_resolve_path`

**Inputs** path.

**Explicit results** path.

**Local steps**

- If not path.
  - Set path from “index”.
- If path.endswith(“.html”).
  - Set path from path at slice no value to negative 5.
- If path equals “index”.
  - Set path from get\_home\_page().
- Set Platform.local.path from path.
- If path differs from “index”.
  - Set path from resolve\_from\_map(path).
- Return path.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L1424) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1187)

<a id="op-ce3f860a503fa3"></a>
### Resolve from map

`operation_foundation_website_path_resolver_business_behavior_resolve_from_map`

**Inputs** path.

**Explicit results** (evaluate\_dynamic\_routes(rules, path) or path).

**Local steps**

- Set rules from list of Rule(r at “from\_route”, endpoint = r at “to\_route”, defaults = r.get(“defaults”)) for r drawn from get\_website\_rules().
  - Draw r from get\_website\_rules().
- Return (evaluate\_dynamic\_routes(rules, path) or path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in evaluate\_dynamic\_routes(rules, path) → path.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L1678) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1186)

<a id="op-671f1b2ca3f11a"></a>
### Get website rules

`operation_foundation_website_path_resolver_business_behavior_get_website_rules`

**Inputs** no declared parameters.

**Explicit results** \_get() · Platform.cache.get\_value(“website\_route\_rules”, \_get).

**Local steps**

- Bind local operation \_get for subsequent calls.
- If Platform.\_dev\_server.
  - Return \_get().
- Return Platform.cache.get\_value(“website\_route\_rules”, \_get).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L24) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1179)

<a id="op-89ff4eb440c67c"></a>
### Get website rules.get

`operation_foundation_website_path_resolver_business_behavior_get_website_rules_get`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**Explicit results** rules.

**Local steps**

- Set rules from list(Platform.get\_hooks(“website\_route\_rules”)).
- For each d in Platform.get\_all(“DocType”, “name, route”, dict(has\_web\_view = 1)).
  - If d.route.
    - Evaluate rules.append(dict(from\_route = (“/” + d.route.strip(“/”)), to\_route = d.name)).
- Return rules.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“website\_route\_rules”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L25) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1180)

<a id="op-7ab7c93b9b6449"></a>
### Validate path

`operation_foundation_website_path_resolver_business_behavior_validate_path`

**Inputs** path.

**Explicit failure paths** validation helper — Platform.\_(“Path {0} it not a valid path”).format(Platform.bold(path)).

**Local steps**

- If not PathResolver(path).is\_valid\_path().
  - Call the validation error handler Platform.throw(Platform.\_(“Path {0} it not a valid path”).format(Platform.bold(path))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L2363) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1190)

## Record · Personal data deletion request

[Record definition](../../../../data/record-types/personal_data_deletion_request.json)

<a id="op-c693caad232e06"></a>
### Personal Data Deletion Request.initialize

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.user\_data\_fields from Platform.get\_hooks(“user\_data\_fields”).
- Set self.full\_match\_privacy\_docs from list of x for x drawn from self.user\_data\_fields where x.get(“redact\_fields”).
  - Draw x from self.user\_data\_fields, keep a combination only if (x.get(“redact\_fields”)).
- Set self.partial\_privacy\_docs from list of x for x drawn from self.user\_data\_fields where (x.get(“partial”) or not x.get(“redact\_fields”)).
  - Draw x from self.user\_data\_fields, keep a combination only if ((x.get(“partial”) or not x.get(“redact\_fields”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in x.get(“partial”) → not x.get(“redact\_fields”).
- Set self.anonymization\_value\_map from mapping(“Code” → “&#91;REDACTED&#93;: Removed due to Personal Data Deletion Request”, “Data” → “&#91;REDACTED&#93;”, “Date” → “1111-01-01”, “Int” → 0, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“user\_data\_fields”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6378) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1237)
