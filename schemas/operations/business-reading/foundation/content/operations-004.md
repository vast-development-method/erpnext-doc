# Web content and issued documents · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Letter head

[Record definition](../../../../data/record-types/letter_head.json)

<a id="op-a9050abcf7a391"></a>
### Letter Head.validate

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_image().
- Evaluate self.validate\_disabled\_and\_default().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set image](operations-004.md#op-290a65ced6fef3), [validate disabled and default](operations-004.md#op-47b19668251903).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L45) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1731)

<a id="op-47b19668251903"></a>
### Letter Head.validate disabled and default

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_validate_disabled_and_default`

**Inputs** self.

**Record and data access** read “Letter Head” via exists.

**Explicit failure paths** validation helper — translated “Letter Head cannot be both disabled and default”.

**Local steps**

- If (self.disabled and self.is\_default).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.disabled → self.is\_default.
  - Call the validation error handler Platform.throw(translated “Letter Head cannot be both disabled and default”).
- If (self.is\_new() and not self.is\_default and not self.disabled and not Platform.flags.in\_migrate and not Platform.flags.in\_install).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.is\_default → not self.disabled → not Platform.flags.in\_migrate → not Platform.flags.in\_install.
  - If not Platform.db.exists(“Letter Head”, dict(is\_default = 1)).
    - Set self.is\_default from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L46) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1732)

<a id="op-290a65ced6fef3"></a>
### Letter Head.set image

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_set_image`

**Inputs** self.

**Local steps**

- If self.source equals “Image”.
  - Evaluate self.set\_image\_as\_html(field = “image”, width = “image\_width”, height = “image\_height”, align = “align”, …).
- If self.footer\_source equals “Image”.
  - Evaluate self.set\_image\_as\_html(field = “footer\_image”, width = “footer\_image\_width”, height = “footer\_image\_height”, align = “footer\_align”, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set image as html](operations-004.md#op-526b68b1128776).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L4888) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1729)

<a id="op-526b68b1128776"></a>
### Letter Head.set image as html

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_set_image_as_document_markup`

**Inputs** self, field, width, height, dimension\_prefix, align, html\_field, success\_msg, failure\_msg.

**State and service calls** msgprint with failure\_msg · msgprint with success\_msg.

**Explicit results** no value.

**Local steps**

- If (not self.get(field) or not is\_image(self.get(field))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(field) → not is\_image(self.get(field)).
  - Evaluate Platform.msgprint(failure\_msg, alert = true, indicator = “orange”).
  - Return no value.
- Evaluate self.set(width, flt(self.get(width))).
- Evaluate self.set(height, flt(self.get(height))).
- Set dimension from “width” when self.get(width) &gt; self.get(height), otherwise “height”.
  - Value choice on self.get(width) &gt; self.get(height) — true gives “width”, false gives “height”.
- Set dimension\_value from self.get(formatted text {dimension\_prefix}{dimension}).
- If not dimension\_value.
  - Set dimension\_value from empty text.
- Evaluate self.set(html\_field, formatted text &lt;div style="text-align: {self.get(align, empty text).lower()};"&gt; &lt;img src="{self.get(field)}" alt="{self.get(“name”)}" {dimension}="{dimension\_value}").
- Evaluate Platform.msgprint(success\_msg, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L5315) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1730)

<a id="op-064223d83089e5"></a>
### Letter Head.on update

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.set\_as\_default().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set as default](operations-004.md#op-beceee7e5c8e47).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L43) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1727)

<a id="op-beceee7e5c8e47"></a>
### Letter Head.set as default

`operation_foundation_printing_record_definitions_letter_head_business_behavior_letter_head_set_as_default`

**Inputs** self.

**State and service calls** request set\_value on “Letter Head”.

**Local steps**

- Bind dependencies set\_default.
- If self.is\_default.
  - Evaluate Platform.db.set\_value(“Letter Head”, mapping(“name” → list(“!=”, self.name)), “is\_default”, 0, update\_modified = false).
  - Evaluate set\_default(“letter\_head”, self.name).
  - Evaluate Platform.db.set\_default(“default\_letter\_head\_content”, self.content).
- Otherwise.
  - Evaluate Platform.defaults.clear\_default(“letter\_head”, self.name).
  - Evaluate Platform.defaults.clear\_default(“default\_letter\_head\_content”, self.content).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L44) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1728)

## Service · List filter

<a id="op-37741885e5a4a2"></a>
### Extract

`operation_foundation_binding_foundation_gettext_extractors_list_filter_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If (not isinstance(data, dict) or data.get(“doctype”) differs from “List Filter”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(data, dict) → data.get(“doctype”) differs from “List Filter”.
  - Return no value.
- If filter\_name bound to data.get(“filter\_name”).
  - yield tuple(get\_line\_number(text, “filter\_name”, filter\_name), “\_”, filter\_name, list(formatted text Name of a list layout for {data.get(“reference\_doctype”)})).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1456)

## Service · List renderer

<a id="op-56669a6657de77"></a>
### List Page.can render

`operation_foundation_website_page_renderers_list_renderer_business_behavior_list_page_can_render`

**Inputs** self.

**Explicit results** false · true · hasattr(module, “get\_list\_context”).

**Local steps**

- Set doctype from self.path.
- If (not doctype or doctype equals “Web Page”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → doctype equals “Web Page”.
  - Return false.
- Attempt the following.
  - Set meta from Platform.get\_meta(doctype).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return false.
- If meta.has\_web\_view.
  - Return true.
- If meta.custom.
  - Return false.
- Set module from load\_doctype\_module(doctype).
- Return hasattr(module, “get\_list\_context”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0535.json#L4164) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L181) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1129)

<a id="op-f39458d2096b1d"></a>
### List Page.render

`operation_foundation_website_page_renderers_list_renderer_business_behavior_list_page_render`

**Inputs** self.

**Explicit results** super().render().

**Local steps**

- Set Platform.form\_dict.doctype from self.path.
- Evaluate self.set\_standard\_path(“portal”).
- Return super().render().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L19) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1130)

## Service · Locale

<a id="op-9db5c908a45e89"></a>
### Get number format

`operation_foundation_locale_business_behavior_get_number_format`

**Inputs** language = no value.

**Declared result** NumberFormat.

**Explicit results** NumberFormat.from\_string(number\_format).

**Local steps**

- Set number\_format from (get\_locale\_value(“number\_format”, language) or “#,###.##”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_locale\_value(“number\_format”, language) → “#,###.##”.
- Return NumberFormat.from\_string(number\_format).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L2603) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L890)

<a id="op-141bd3991f6d0b"></a>
### Get date format

`operation_foundation_locale_business_behavior_get_date_format`

**Inputs** language = no value.

**Declared result** str.

**Explicit results** (get\_locale\_value(“date\_format”, language) or “yyyy-mm-dd”).

**Local steps**

- Return (get\_locale\_value(“date\_format”, language) or “yyyy-mm-dd”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_locale\_value(“date\_format”, language) → “yyyy-mm-dd”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L2722) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L887)

<a id="op-db3de2b596406e"></a>
### Get time format

`operation_foundation_locale_business_behavior_get_time_format`

**Inputs** language = no value.

**Declared result** str.

**Explicit results** (get\_locale\_value(“time\_format”, language) or “HH:mm:ss”).

**Local steps**

- Return (get\_locale\_value(“time\_format”, language) or “HH:mm:ss”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_locale\_value(“time\_format”, language) → “HH:mm:ss”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L2811) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L891)

<a id="op-8cb8dd87cef871"></a>
### Get first day of the week

`operation_foundation_locale_business_behavior_get_first_day_of_the_week`

**Inputs** language = no value.

**Declared result** str.

**Explicit results** (get\_locale\_value(“first\_day\_of\_the\_week”, language) or “Sunday”).

**Local steps**

- Return (get\_locale\_value(“first\_day\_of\_the\_week”, language) or “Sunday”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_locale\_value(“first\_day\_of\_the\_week”, language) → “Sunday”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L2900) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L888)

<a id="op-329ac3afdcb8d6"></a>
### Get locale value

`operation_foundation_locale_business_behavior_get_locale_value`

**Inputs** key, language = no value.

**Declared result** (str bitwise or no value).

**Explicit results** (value or Platform.db.get\_default(key)).

**Local steps**

- Set lang from (language or Platform.local.lang).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in language → Platform.local.lang.
- If lang.
  - Set value from Platform.client\_cache.get\_doc(“Language”, lang).get(key).
- Return (value or Platform.db.get\_default(key)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → Platform.db.get\_default(key).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L65) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L889)

## Service · Metatags

<a id="op-c30ae3e6f280b4"></a>
### Meta Tags.initialize

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_initialize`

**Inputs** self, path, context.

**Local steps**

- Set self.path from path.
- Set self.context from context.
- Set self.tags from Platform.\_dict((self.context.get(“metatags”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.context.get(“metatags”) → mapping().
- Evaluate self.init\_metatags\_from\_context().
- Evaluate self.set\_opengraph\_tags().
- Evaluate self.set\_twitter\_tags().
- Evaluate self.set\_meta\_published\_on().
- Evaluate self.set\_metatags\_from\_website\_route\_meta().

If control reaches the end, it returns no value.

**Methods declared on this owner** [init metatags from context](operations-004.md#op-c268ed55d072b5), [set opengraph tags](operations-004.md#op-d39254b800ac27), [set twitter tags](operations-004.md#op-ff100d1099486b), [set meta published on](operations-004.md#op-719abc4348c7b7), [set metatags from website route meta](operations-004.md#op-650c989fff25be).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1871) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1574)

<a id="op-c268ed55d072b5"></a>
### Meta Tags.init metatags from context

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_initialize_metatags_from_context`

**Inputs** self.

**Local steps**

- For each key in METATAGS.
  - If (not self.tags.get(key) and self.context.get(key)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.tags.get(key) → self.context.get(key).
    - Set self.tags at key from self.context at key.
- If not self.tags.get(“title”).
  - Set self.tags at “title” from self.context.get(“name”).
- If self.tags.get(“image”).
  - Set self.tags at “image” from Platform.utils.get\_url(self.tags at “image”).
- Set self.tags at “language” from (Platform.local.lang or “en”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L2114) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1575)

<a id="op-d39254b800ac27"></a>
### Meta Tags.set opengraph tags

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_set_opengraph_tags`

**Inputs** self.

**Local steps**

- If “og:type” does not belong to self.tags.
  - Set self.tags at “og:type” from “article”.
- For each key in METATAGS.
  - If self.tags.get(key).
    - Set self.tags at (“og:” + key) from self.tags.get(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L2499) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1578)

<a id="op-ff100d1099486b"></a>
### Meta Tags.set twitter tags

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_set_twitter_tags`

**Inputs** self.

**Local steps**

- For each key in METATAGS.
  - If self.tags.get(key).
    - Set self.tags at (“twitter:” + key) from self.tags.get(key).
- If self.tags.get(“image”).
  - Set self.tags at “twitter:card” from “summary\_large\_image”.
- Otherwise.
  - Set self.tags at “twitter:card” from “summary”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L2676) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1579)

<a id="op-719abc4348c7b7"></a>
### Meta Tags.set meta published on

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_set_meta_published_on`

**Inputs** self.

**Local steps**

- If “published\_on” belongs to self.tags.
  - Set self.tags at “datePublished” from self.tags at “published\_on”.
  - Remove self.tags at “published\_on”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L2891) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1576)

<a id="op-650c989fff25be"></a>
### Meta Tags.set metatags from website route meta

`operation_foundation_website_website_components_metatags_business_behavior_meta_tags_set_metatags_from_website_route_meta`

**Inputs** self.

**Record and data access** resolve a document from “Website Route Meta” via get\_doc.

**Local steps**

- Set route from self.path.
- If route equals empty text.
  - Set route from Platform.get\_website\_settings(“home\_page”).
- Set route\_exists from (route and not route.endswith(tuple(“.js”, “.css”)) and has\_meta\_tags(route)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in route → not route.endswith(tuple(“.js”, “.css”)) → has\_meta\_tags(route).
- If route\_exists.
  - Set website\_route\_meta from Platform.get\_doc(“Website Route Meta”, route).
  - For each meta\_tag in website\_route\_meta.meta\_tags.
    - Set d from meta\_tag.get\_meta\_dict().
    - Evaluate self.tags.update(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3002) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1577)

<a id="op-461971294cec21"></a>
### Has meta tags

`operation_foundation_website_website_components_metatags_business_behavior_has_meta_tags`

**Inputs** route.

**Wrappers, in declaration order** site\_cache(ttl = (10 × 60), maxsize = 16).

**Record and data access** read “Website Route Meta” via exists.

**Explicit results** bool(Platform.db.exists(“Website Route Meta”, route)).

**Local steps**

- Return bool(Platform.db.exists(“Website Route Meta”, route)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L3297) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1573)

## Service · Module onboarding

<a id="op-436a5adca1e385"></a>
### Extract

`operation_foundation_gettext_extractors_module_onboarding_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set text from fileobj.read().decode().
- Set data from json.loads(text).
- If isinstance(data, list).
  - Return no value.
- If data.get(“doctype”) differs from “Module Onboarding”.
  - Return no value.
- Set onboarding\_name from data.get(“name”).
- If title bound to data.get(“title”).
  - yield tuple(get\_line\_number(text, “title”, title), “\_”, title, list(formatted text Title of the Module Onboarding '{onboarding\_name}')).
- If subtitle bound to data.get(“subtitle”).
  - yield tuple(get\_line\_number(text, “subtitle”, subtitle), “\_”, subtitle, list(formatted text Subtitle of the Module Onboarding '{onboarding\_name}')).
- If success\_message bound to data.get(“success\_message”).
  - yield tuple(get\_line\_number(text, “success\_message”, success\_message), “\_”, success\_message, list(formatted text Success message of the Module Onboarding '{onboarding\_name}')).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L120) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L357)

## Service · Navbar

<a id="op-a6a728d86024d2"></a>
### Extract

`operation_foundation_gettext_extractors_navbar_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set module from get\_module(fileobj.name).
- If hasattr(module, “standard\_navbar\_items”).
  - Set standard\_navbar\_items from module.standard\_navbar\_items.
  - For each nav\_item in standard\_navbar\_items.
    - If label bound to nav\_item.get(“item\_label”).
      - Set item\_type from nav\_item.get(“item\_type”).
      - yield tuple(no value, “\_”, label, list(“Label of a standard navbar item”, formatted text Type: {item\_type})).
- If hasattr(module, “standard\_help\_items”).
  - Set standard\_help\_items from module.standard\_help\_items.
  - For each help\_item in standard\_help\_items.
    - If label bound to help\_item.get(“item\_label”).
      - Set item\_type from help\_item.get(“item\_type”).
      - yield tuple(no value, “\_”, label, list(“Label of a standard help item”, formatted text Type: {item\_type})).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L3586) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L358)

<a id="op-0f546d469d5119"></a>
### Get module

`operation_foundation_gettext_extractors_navbar_business_behavior_get_module`

**Inputs** path.

**Explicit results** importlib.import\_module(import\_path).

**Local steps**

- Set \_path from Path(path).
- Set rel\_path from \_path.relative\_to(get\_bench\_path()).
- Set import\_path from “.”.join(rel\_path.parts at slice 2 to no value).rstrip(“.py”).
- Return importlib.import\_module(import\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L4020) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L359)
