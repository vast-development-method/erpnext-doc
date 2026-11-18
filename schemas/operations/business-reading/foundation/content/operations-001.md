# Web content and issued documents · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · About us settings

[Record definition](../../../../data/record-types/about_us_settings.json)

<a id="op-6fd3e03ceb65ca"></a>
### About Us Settings.on update

`operation_foundation_website_record_definitions_about_us_settings_business_behavior_about_us_settings_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_cache.
- Evaluate clear\_cache(“about”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7507) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1191)

<a id="op-4d7c873ea7d66e"></a>
### Get args

`operation_foundation_website_record_definitions_about_us_settings_business_behavior_get_arguments`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “About Us Settings” via get\_doc.

**Explicit results** mapping(“obj” → obj).

**Local steps**

- Set obj from Platform.get\_doc(“About Us Settings”).
- Return mapping(“obj” → obj).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7572) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1192)

## Service · Base renderer

<a id="op-b9b8f889a3353e"></a>
### Base Renderer.initialize

`operation_foundation_website_page_renderers_base_renderer_business_behavior_base_renderer_initialize`

**Inputs** self, path = no value, http\_status\_code = no value.

**Local steps**

- Set self.headers from no value.
- Set self.http\_status\_code from (http\_status\_code or 200).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in http\_status\_code → 200.
- If not path.
  - Set path from Platform.local.request.path.
- Set self.path from path.strip(“/ ”).
- Set self.basepath from empty text.
- Set self.basename from empty text.
- Set self.name from empty text.
- Set self.route from empty text.
- Set self.file\_dir from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L7265) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1108)

<a id="op-6674eadd544802"></a>
### Base Renderer.can render

`operation_foundation_website_page_renderers_base_renderer_business_behavior_base_renderer_can_render`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0534.json#L7517) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1107)

<a id="op-79cf994754fd27"></a>
### Base Renderer.render

`operation_foundation_website_page_renderers_base_renderer_business_behavior_base_renderer_render`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1109)

<a id="op-1e33bfddb5b3b5"></a>
### Base Renderer.build response

`operation_foundation_website_page_renderers_base_renderer_business_behavior_base_renderer_build_response`

**Inputs** self, data, http\_status\_code = no value, headers = no value.

**Explicit results** build\_response(self.path, data, (http\_status\_code or self.http\_status\_code), (headers or self.headers)).

**Local steps**

- Return build\_response(self.path, data, (http\_status\_code or self.http\_status\_code), (headers or self.headers)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in http\_status\_code → self.http\_status\_code.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in headers → self.headers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L48) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1106)

## Service · Base template page

<a id="op-d20ec11ef8472c"></a>
### Base Template Page.initialize

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_initialize`

**Inputs** self, path, http\_status\_code = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(path = path, http\_status\_code = http\_status\_code).
- Set self.template\_path from empty text.
- Set self.source from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L171) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1111)

<a id="op-a73922900e3617"></a>
### Base Template Page.init context

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_initialize_context`

**Inputs** self.

**Local steps**

- Set self.context from Platform.\_dict().
- Evaluate self.context.update(get\_website\_settings()).
- Evaluate self.context.update((Platform.local.conf.get(“website\_context”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.get(“website\_context”) → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L297) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1112)

<a id="op-c1a31a9baa192b"></a>
### Base Template Page.add csrf token

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_add_cross_site_request_forgery_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, html.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L453) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1110)

<a id="op-bd237d38ccfae8"></a>
### Base Template Page.post process context

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_post_process_context`

**Inputs** self.

**Local steps**

- Set self.tags from MetaTags(self.path, self.context).tags.
- Set self.context.metatags from self.tags.
- Evaluate self.set\_base\_template\_if\_missing().
- Evaluate self.set\_title\_with\_prefix().
- Evaluate self.update\_website\_context().
- Set self.template\_path from (self.context.template or self.template\_path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.template → self.template\_path.
- Set self.context.\_context\_dict from self.context.
- Evaluate self.set\_missing\_values().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set base template if missing](operations-001.md#op-579dc364b626e5), [set title with prefix](operations-001.md#op-93b2913e8b5cea), [update website context](operations-001.md#op-95c11865c5c25c), [set missing values](operations-001.md#op-73af73ecc791ab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L639) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1113)

<a id="op-579dc364b626e5"></a>
### Base Template Page.set base template if missing

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_set_base_template_if_missing`

**Inputs** self.

**Local steps**

- If not self.context.base\_template\_path.
  - Set app\_base from Platform.get\_hooks(“base\_template”).
  - Set self.context.base\_template\_path from app\_base at negative 1 when app\_base, otherwise “templates/base.html”.
    - Value choice on app\_base — true gives app\_base at negative 1, false gives “templates/base.html”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“base\_template”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L885) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1114)

<a id="op-93b2913e8b5cea"></a>
### Base Template Page.set title with prefix

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_set_title_with_prefix`

**Inputs** self.

**Local steps**

- If (self.context.title\_prefix and self.context.title and not self.context.title.startswith(self.context.title\_prefix)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.context.title\_prefix → self.context.title → not self.context.title.startswith(self.context.title\_prefix).
  - Set self.context.title from formatted text {self.context.title\_prefix} - {self.context.title}.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L1012) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1116)

<a id="op-73af73ecc791ab"></a>
### Base Template Page.set missing values

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_set_missing_values`

**Inputs** self.

**Local steps**

- If (hasattr(Platform.local, “response”) and Platform.local.response.get(“context”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “response”) → Platform.local.response.get(“context”).
  - Evaluate self.context.update(Platform.local.response.context).
- Set self.context.canonical from Platform.utils.get\_url(Platform.utils.escape\_html(self.path)).
- If “url\_prefix” does not belong to self.context.
  - Set self.context.url\_prefix from empty text.
- If (self.context.url\_prefix and self.context.url\_prefix at negative 1 differs from “/”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.context.url\_prefix → self.context.url\_prefix at negative 1 differs from “/”.
  - Update self.context.url\_prefix using + “/”.
- Set self.context.path from self.path.
- Set self.context.pathname from getattr(Platform.local, “path”, no value) when hasattr(Platform, “local”), otherwise self.path.
  - Value choice on hasattr(Platform, “local”) — true gives getattr(Platform.local, “path”, no value), false gives self.path.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “path”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L1183) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1115)

<a id="op-95c11865c5c25c"></a>
### Base Template Page.update website context

`operation_foundation_website_page_renderers_base_template_page_business_behavior_base_template_page_update_website_context`

**Inputs** self.

**Local steps**

- Set update\_website\_context from Platform.get\_hooks(“update\_website\_context”).
- For each method in update\_website\_context.
  - Set values from Platform.get\_attr(method)(self.context).
  - If values.
    - Evaluate self.context.update(values).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“update\_website\_context”), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L1627) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1117)

## Service · Comments

<a id="op-a6d9c97d923619"></a>
### Get limit

`operation_foundation_templates_includes_comments_business_behavior_get_limit`

**Inputs** no declared parameters.

**Explicit results** 5 · limit.

**Local steps**

- Set method from Platform.get\_hooks(“comment\_rate\_limit”).
- If not method.
  - Return 5.
- Otherwise.
  - Set limit from Platform.call(method at 0).
  - Return limit.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“comment\_rate\_limit”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L596)

<a id="op-a0b6db361ff354"></a>
### Add comment

`operation_foundation_templates_includes_comments_business_behavior_add_comment`

**Inputs** comment, comment\_email, comment\_by, reference\_doctype, reference\_name, route, web\_form = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(limit = get\_limit, seconds = (60 × 60)).

**Record and data access** read “User” via get\_value · resolve a document from reference\_doctype via get\_doc.

**State and service calls** msgprint with translated “The comment cannot be empty” · msgprint with translated “Comments cannot have links or email addresses” · call db\_set on comment.

**Explicit results** no value · false · template.render(mapping(“comment” → comment.as\_dict())).

**Explicit failure paths** validation helper with Platform.AuthenticationError — translated “Please login to post a comment.” · Platform.AuthenticationError · Platform.PermissionError.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set allowed\_doctypes from list(“Web Page”).
  - Set comments\_permission\_config from Platform.get\_hooks(“has\_comment\_permission”).
  - Set guest\_allowed from false.
  - If len(comments\_permission\_config).
    - If comments\_permission\_config at “doctype”.
      - Evaluate allowed\_doctypes.append(comments\_permission\_config at “doctype” at 0).
      - Set check\_permission\_method from comments\_permission\_config at “method”.
      - Set guest\_allowed from Platform.call(check\_permission\_method at 0, ref\_doctype = reference\_doctype).
  - If reference\_doctype does not belong to allowed\_doctypes.
    - Return no value.
  - If not guest\_allowed.
    - Call the validation error handler Platform.throw(translated “Please login to post a comment.”, exc = Platform.AuthenticationError).
- Otherwise.
  - Set comment\_email from Platform.session.user.
  - Set comment\_by from Platform.get\_value(“User”, Platform.session.user, “full\_name”).
- If not comment.strip().
  - Evaluate Platform.msgprint(translated “The comment cannot be empty”).
  - Return false.
- If (URLS\_COMMENT\_PATTERN.search(comment) or EMAIL\_PATTERN.search(comment)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in URLS\_COMMENT\_PATTERN.search(comment) → EMAIL\_PATTERN.search(comment).
  - Evaluate Platform.msgprint(translated “Comments cannot have links or email addresses”).
  - Return false.
- Set perm\_flag from true.
- Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
- If web\_form.
  - Set web\_form from Platform.get\_lazy\_doc(“Web Form”, web\_form).
  - Set perm\_flag from (web\_form.doc\_type equals reference\_doctype and web\_form.has\_web\_form\_permission(reference\_doctype, reference\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in web\_form.doc\_type equals reference\_doctype → web\_form.has\_web\_form\_permission(reference\_doctype, reference\_name).
- Otherwise.
  - If not (Platform.session.user equals “Guest” and guest\_allowed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user equals “Guest” → guest\_allowed.
    - Set perm\_flag from doc.has\_permission().
- If not perm\_flag.
  - If Platform.session.user equals “Guest”.
    - Raise Platform.AuthenticationError.
  - Raise Platform.PermissionError.
- Set comment from doc.add\_comment(text = clean\_html(comment), comment\_email = comment\_email, comment\_by = comment\_by).
- Evaluate comment.db\_set(“published”, 1).
- If route.
  - Evaluate clear\_cache(route).
- Set template from Platform.get\_template(“templates/includes/comments/comment.html”).
- Return template.render(mapping(“comment” → comment.as\_dict())).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“has\_comment\_permission”) · effective access from doc.has\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L127) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L595)

## Record · Contact us settings

[Record definition](../../../../data/record-types/contact_us_settings.json)

<a id="op-1452069040d5cb"></a>
### Contact Us Settings.on update

`operation_foundation_website_record_definitions_contact_us_settings_business_behavior_contact_us_settings_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_cache.
- Evaluate clear\_cache(“contact”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7648) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1193)

## Service · Custom field

<a id="op-a99578b0adac8c"></a>
### Extract

`operation_foundation_gettext_extractors_custom_field_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If not isinstance(data, list).
  - Return no value.
- Set messages from list().
- For each custom\_field in data.
  - Set doctype from custom\_field.get(“dt”).
  - Evaluate messages.extend(extract\_messages\_from\_docfield(doctype, custom\_field, text)).
- yield values from generator of tuple(lineno, “\_”, message, list(comment)) for tuple(lineno, message, comment) drawn from messages.
  - Draw tuple(lineno, message, comment) from messages.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L117) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L352)

## Service · Customization

<a id="op-665da83f9b6224"></a>
### Extract

`operation_foundation_gettext_extractors_customization_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- Set doctype from data.get(“doctype”).
- Set messages from list().
- For each field in data.get(“custom\_fields”, list()).
  - Evaluate messages.extend(extract\_messages\_from\_docfield(doctype, field, text)).
- Evaluate messages.extend(extract\_messages\_from\_links(doctype, data.get(“links”, list()), text)).
- For each property\_setter in data.get(“property\_setters”, list()).
  - If property\_setter.get(“doctype\_or\_field”) differs from “DocField”.
    - Continue with the next iteration or loop test.
  - Set property\_name from property\_setter.get(“property”).
  - Set fieldname from property\_setter.get(“field\_name”).
  - Set value from property\_setter.get(“value”).
  - Set lineno from get\_line\_number(text, “value”, value).
  - If (property\_name equals “options” and fieldname does not belong to EXCLUDE\_SELECT\_OPTIONS).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in property\_name equals “options” → fieldname does not belong to EXCLUDE\_SELECT\_OPTIONS.
    - Set select\_options from list of option for option drawn from value.split(whitespace '\\n') where (option and not option.isdigit()).
      - Draw option from value.split(whitespace '\\n'), keep a combination only if ((option and not option.isdigit())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in option → not option.isdigit().
    - If (select\_options and “icon” belongs to select\_options at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in select\_options → “icon” belongs to select\_options at 0.
      - Continue with the next iteration or loop test.
    - Evaluate messages.extend(generator of tuple(lineno, option, formatted text Option for the '{fieldname}' (Select) field in DocType '{doctype}') for option drawn from select\_options).
      - Draw option from select\_options.
  - If property\_name equals “label”.
    - Evaluate messages.append(tuple(lineno, value, formatted text Label of the '{fieldname}' field in DocType '{doctype}')).
  - If property\_name equals “description”.
    - Evaluate messages.append(tuple(lineno, value, formatted text Description of the '{fieldname}' field in DocType '{doctype}')).
- yield values from generator of tuple(lineno, “\_”, message, list(comment)) for tuple(lineno, message, comment) drawn from messages.
  - Draw tuple(lineno, message, comment) from messages.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L118) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L353)

## Service · Dashboard fixtures

<a id="op-1b55002ba4e5c8"></a>
### Get data

`operation_foundation_website_dashboard_fixtures_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“dashboards” → get\_dashboards(), “charts” → get\_charts(), “number\_cards” → no value)).

**Local steps**

- Return Platform.\_dict(mapping(“dashboards” → get\_dashboards(), “charts” → get\_charts(), “number\_cards” → no value)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L6993) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1105)

<a id="op-d373fcf32a6941"></a>
### Get dashboards

`operation_foundation_website_dashboard_fixtures_business_behavior_get_dashboards`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“name” → “Website”, “dashboard\_name” → “Website”, “charts” → list(mapping(“chart” → “Website Analytics”, “width” → “Full”)))).

**Local steps**

- Return list(mapping(“name” → “Website”, “dashboard\_name” → “Website”, “charts” → list(mapping(“chart” → “Website Analytics”, “width” → “Full”)))).

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7101) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1104)

<a id="op-16a44ae55496e6"></a>
### Get charts

`operation_foundation_website_dashboard_fixtures_business_behavior_get_charts`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“chart\_name” → “Website Analytics”, “chart\_type” → “Report”, “custom\_options” → “{"type": "line", "lineOptions": {"regionFill": 1}, "axisOptions": {"shortenYAxisNumbers": 1}, "tooltipOptions": {}}” …).

**Local steps**

- Return list(mapping(“chart\_name” → “Website Analytics”, “chart\_type” → “Report”, “custom\_options” → “{"type": "line", "lineOptions": {"regionFill": 1}, "axisOptions": {"shortenYAxisNumbers": 1}, "tooltipOptions": {}}” …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7222) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1103)

## Service · Desktop icon

<a id="op-494c0d154cdcec"></a>
### Extract

`operation_foundation_gettext_extractors_desktop_icon_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- Set label from data.get(“label”).
- If label.
  - yield tuple(get\_line\_number(text, “label”, label), “\_”, label, list(“Label of a Desktop Icon”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L119) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L354)

## Record · Discussion reply

[Record definition](../../../../data/record-types/discussion_reply.json)

<a id="op-7d96579f013b71"></a>
### Discussion Reply.on update

`operation_foundation_website_record_definitions_discussion_reply_business_behavior_discussion_reply_on_update`

**Inputs** self.

**State and service calls** publish realtime.

**Local steps**

- Bind dependencies sanitize\_html.
- Evaluate Platform.publish\_realtime(event = “update\_message”, room = get\_website\_room(), message = mapping(“reply” → sanitize\_html(Platform.utils.md\_to\_html(self.reply)), “reply\_name” → self.name), after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event = “update\_message”, room = get\_website\_room(), message = mapping(“reply” → sanitize\_html(Platform.utils.md\_to\_html(self.reply)), “reply\_name” → self.name), after\_commit = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0521.json#L7713) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1197)
