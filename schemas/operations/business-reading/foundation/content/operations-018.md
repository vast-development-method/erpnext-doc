# Web content and issued documents · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-fa79b4930274d9"></a>
### Get sidebar items

`operation_foundation_website_utils_business_behavior_get_sidebar_items`

**Inputs** parent\_sidebar, basepath = no value.

**Record and data access** read “Website Sidebar Item” via get\_all.

**Explicit results** sidebar\_items.

**Local steps**

- Bind dependencies Platform.www.list.
- Set sidebar\_items from list().
- Set hooks from Platform.get\_hooks(“look\_for\_sidebar\_json”).
- Set look\_for\_sidebar\_json from hooks at 0 when hooks, otherwise Platform.flags.look\_for\_sidebar.
  - Value choice on hooks — true gives hooks at 0, false gives Platform.flags.look\_for\_sidebar.
- If (basepath and look\_for\_sidebar\_json).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in basepath → look\_for\_sidebar\_json.
  - Set sidebar\_items from get\_sidebar\_items\_from\_sidebar\_file(basepath, look\_for\_sidebar\_json).
- If (not sidebar\_items and parent\_sidebar).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sidebar\_items → parent\_sidebar.
  - Set sidebar\_items from Platform.get\_all(“Website Sidebar Item”, filters = dict(parent = parent\_sidebar), fields = list(“title”, “route”, “′group′”), order\_by = “idx asc”).
- If not sidebar\_items.
  - Set sidebar\_items from get\_portal\_sidebar\_items().
- Return sidebar\_items.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“look\_for\_sidebar\_json”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L4619) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1564)

<a id="op-defe4f3d558112"></a>
### Get portal sidebar items

`operation_foundation_website_utils_business_behavior_get_portal_sidebar_items`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Portal Settings” via get\_doc.

**Explicit results** sidebar\_items.

**Local steps**

- Set sidebar\_items from Platform.cache.hget(“portal\_menu\_items”, Platform.session.user).
- If sidebar\_items is identical to no value.
  - Set sidebar\_items from list().
  - Set roles from Platform.get\_roles().
  - Set portal\_settings from Platform.get\_doc(“Portal Settings”, “Portal Settings”).
  - Bind local operation add\_items for subsequent calls.
  - If not portal\_settings.hide\_standard\_menu.
    - Evaluate add\_items(sidebar\_items, portal\_settings.get(“menu”)).
  - If portal\_settings.custom\_menu.
    - Evaluate add\_items(sidebar\_items, portal\_settings.get(“custom\_menu”)).
  - Set items\_via\_hooks from Platform.get\_hooks(“portal\_menu\_items”).
  - If items\_via\_hooks.
    - For each i in items\_via\_hooks.
      - Set i at “enabled” from 1.
    - Evaluate add\_items(sidebar\_items, items\_via\_hooks).
  - Evaluate Platform.cache.hset(“portal\_menu\_items”, Platform.session.user, sidebar\_items).
- Return sidebar\_items.

**Values supplied outside this operation** effective access from Platform.get\_roles() · selected callable from Platform.get\_hooks(“portal\_menu\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L65) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1562)

<a id="op-69051276f76617"></a>
### Get portal sidebar items.add items

`operation_foundation_website_utils_business_behavior_get_portal_sidebar_items_add_items`

**Inputs** sidebar\_items, items.

**Local steps**

- For each d in items.
  - If (d.get(“enabled”) and (not d.get(“role”) or d.get(“role”) belongs to roles)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“enabled”) → (not d.get(“role”) or d.get(“role”) belongs to roles).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.get(“role”) → d.get(“role”) belongs to roles.
    - Evaluate sidebar\_items.append(d.as\_dict() when isinstance(d, Document), otherwise d).
      - Value choice on isinstance(d, Document) — true gives d.as\_dict(), false gives d.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L66) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1563)

<a id="op-b06217771bcfbd"></a>
### Get sidebar items from sidebar file

`operation_foundation_website_utils_business_behavior_get_sidebar_items_from_sidebar_file`

**Inputs** basepath, look\_for\_sidebar\_json.

**Explicit results** sidebar\_items.

**Explicit failure paths** validation helper — (“Invalid Sidebar JSON at ” + sidebar\_json\_path).

**Local steps**

- Set sidebar\_items from list().
- Set sidebar\_json\_path from get\_sidebar\_json\_path(basepath, look\_for\_sidebar\_json).
- If not sidebar\_json\_path.
  - Return sidebar\_items.
- Within open(sidebar\_json\_path) bound as sidebarfile.
  - Attempt the following.
    - Set sidebar\_json from sidebarfile.read().
    - Set sidebar\_items from json.loads(sidebar\_json).
  - On failure (json.decoder.JSONDecodeError).
    - Call the validation error handler Platform.throw((“Invalid Sidebar JSON at ” + sidebar\_json\_path)).
- Return sidebar\_items.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L5695) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1565)

<a id="op-1b24fdabfd06b4"></a>
### Get sidebar json path

`operation_foundation_website_utils_business_behavior_get_sidebar_structured_data_path`

**Inputs** path, look\_for = false.

**Explicit results** empty text · sidebar\_json\_path · get\_sidebar\_json\_path(os.path.split(path) at 0, look\_for).

**Local steps**

- If (os.path.split(path) at 1 equals “www” or path equals “/” or not path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.path.split(path) at 1 equals “www” → path equals “/” → not path.
  - Return empty text.
- Set sidebar\_json\_path from os.path.join(path, “\_sidebar.json”).
- If os.path.exists(sidebar\_json\_path).
  - Return sidebar\_json\_path.
- Otherwise.
  - If look\_for.
    - Return get\_sidebar\_json\_path(os.path.split(path) at 0, look\_for).
  - Otherwise.
    - Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L5950) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1566)

<a id="op-6c83c8ecac2aa7"></a>
### Cache html

`operation_foundation_website_utils_business_behavior_cache_document_markup`

**Inputs** func.

**Explicit results** cache\_html\_decorator.

**Local steps**

- Bind local operation cache\_html\_decorator for subsequent calls.
- Return cache\_html\_decorator.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L6223) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1540)

<a id="op-3a2e0baef22f09"></a>
### Cache html.cache html decorator

`operation_foundation_website_utils_business_behavior_cache_document_markup_cache_document_markup_decorator`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** html.

**Local steps**

- Set cache\_key from formatted text {WEBSITE\_PAGE\_CACHE\_PREFIX}{args at 0.path}.
- Set cache\_headers from mapping(“Cache-Control” → “private,max-age=300,stale-while-revalidate=10800”).
- Set no\_cache from (Platform.request and Platform.request.cache\_control.no\_cache).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → Platform.request.cache\_control.no\_cache.
- If can\_cache(no\_cache).
  - Set html from no value.
  - Set page\_cache from Platform.cache.get\_value(cache\_key).
  - If (page\_cache and Platform.local.lang belongs to page\_cache).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in page\_cache → Platform.local.lang belongs to page\_cache.
    - Set html from page\_cache at Platform.local.lang.
  - If html.
    - Set Platform.local.response.from\_cache from true.
    - Evaluate Platform.local.response\_headers.update(cache\_headers).
    - Return html.
- Set html from func(expanded args, expanded names kwargs).
- Set context from args at 0.context.
- If can\_cache(context.no\_cache).
  - Set page\_cache from (Platform.cache.get\_value(cache\_key) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(cache\_key) → mapping().
  - Set page\_cache at Platform.local.lang from html.
  - Evaluate Platform.cache.set\_value(cache\_key, page\_cache, expires\_in\_sec = (30 × 60)).
  - Evaluate Platform.local.response\_headers.update(cache\_headers).
- Return html.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L6864) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1541)

<a id="op-fbdba5ef3a754a"></a>
### Build response

`operation_foundation_website_utils_business_behavior_build_response`

**Inputs** path, data, http\_status\_code, headers = no value.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.data from set\_content\_type(response, data, path).
- Set response.status\_code from http\_status\_code.
- Set response.headers at “X-Page-Name” from cstr(cstr(path).encode(“ascii”, errors = “xmlcharrefreplace”)).
- Set response.headers at “X-From-Cache” from (Platform.local.response.from\_cache or false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.response.from\_cache → false.
- If http\_status\_code differs from 404.
  - Evaluate add\_preload\_for\_bundled\_assets(response).
- If headers.
  - For each tuple(key, val) in headers.items().
    - Set response.headers at key from cstr(cstr(val).encode(“utf-8”, errors = “xmlcharrefreplace”)).
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1539)

<a id="op-205f6591578d17"></a>
### Set content type

`operation_foundation_website_utils_business_behavior_set_content_type`

**Inputs** response, data, path.

**Explicit results** data.

**Local steps**

- If isinstance(data, dict).
  - Set response.mimetype from “application/json”.
  - Set data from json.dumps(data).
  - Return data.
- Set response.mimetype from “text/html”.
- If (“.” belongs to path and not path.endswith(“.com”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “.” belongs to path → not path.endswith(“.com”).
  - Set tuple(content\_type, encoding) from mimetypes.guess\_type(path).
  - If content\_type.
    - Set response.mimetype from content\_type.
    - If encoding.
      - Set response.charset from encoding.
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L444) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1570)

<a id="op-33e7cb42df984e"></a>
### Add preload for bundled assets

`operation_foundation_website_utils_business_behavior_add_preload_for_bundled_assets`

**Inputs** response.

**Local steps**

- Set links from list of formatted text &lt;{css}&gt;; rel=preload; as=style for css drawn from Platform.local.preload\_assets at “style”.
  - Draw css from Platform.local.preload\_assets at “style”.
- Evaluate links.extend(generator of formatted text &lt;{js}&gt;; rel=preload; as=script for js drawn from Platform.local.preload\_assets at “script”).
  - Draw js from Platform.local.preload\_assets at “script”.
- Set version from get\_build\_version().
- Evaluate links.extend(generator of formatted text &lt;{svg}?v={version}&gt;; rel=preload; as=fetch; crossorigin for svg drawn from Platform.local.preload\_assets at “icons”).
  - Draw svg from Platform.local.preload\_assets at “icons”.
- Set MAX\_LINK\_HEADER\_BYTES from 1000.
- If links.
  - Set trimmed from \_fit\_links\_within\_limit(links, MAX\_LINK\_HEADER\_BYTES).
  - If trimmed.
    - Set response.headers at “Link” from “,”.join(trimmed).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L736) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1538)

<a id="op-fd7d01dad58f2d"></a>
### Fit links within limit

`operation_foundation_website_utils_business_behavior_fit_links_within_limit`

**Inputs** links, byte\_limit.

**Declared result** list at str.

**Explicit results** result.

**Local steps**

- Set result from list().
- Set total from 0.
- For each link in links.
  - Set link\_size from len(link.encode(“utf-8”)).
  - Set needed\_size from (link\_size + 1 when result, otherwise 0).
    - Value choice on result — true gives 1, false gives 0.
  - If (total + needed\_size) &gt; byte\_limit.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate result.append(link).
  - Update total using + needed\_size.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1136) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1551)

<a id="op-ba40ab6f54b182"></a>
### Is binary file

`operation_foundation_website_utils_business_behavior_is_binary_file`

**Inputs** path.

**Wrappers, in declaration order** lru\_cache.

**Explicit results** bool(content.translate(no value, textchars)).

**Local steps**

- Set textchars from bytearray((set(7, 8, 9, 10, …) bitwise or (set(range(32, 256)) − set(127)))).
- Within open(path, “rb”) bound as f.
  - Set content from f.read(1024).
  - Return bool(content.translate(no value, textchars)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1395) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1568)

<a id="op-633f76e3283cdf"></a>
### Check if webform exists

`operation_foundation_website_utils_business_behavior_check_if_webform_exists`

**Inputs** route.

**Record and data access** read “Web Form” via exists.

**Explicit results** (Platform.db.exists(“Web Form”, mapping(“name” → route.strip(“/”))) or Platform.db.exists(“Web Form”, mapping(“route” → route.strip(“/”)))).

**Local steps**

- Return (Platform.db.exists(“Web Form”, mapping(“name” → route.strip(“/”))) or Platform.db.exists(“Web Form”, mapping(“route” → route.strip(“/”)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“Web Form”, mapping(“name” → route.strip(“/”))) → Platform.db.exists(“Web Form”, mapping(“route” → route.strip(“/”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L1635) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1543)

## Record · Utm campaign

<a id="op-ca514bc911fd6c"></a>
### UTMCampaign.before save

`operation_foundation_website_record_definitions_utm_campaign_business_behavior_campaign_tracking_campaign_before_save`

**Inputs** self.

**Local steps**

- If self.slug.
  - Set self.slug from Platform.utils.slug(self.slug).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0525.json#L1793) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1298)

## Record · Utm medium

<a id="op-0ef15252c0f030"></a>
### UTMMedium.before save

`operation_foundation_website_record_definitions_utm_medium_business_behavior_campaign_tracking_medium_before_save`

**Inputs** self.

**Local steps**

- If self.slug.
  - Set self.slug from Platform.utils.slug(self.slug).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0525.json#L1881) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1299)

## Record · Utm source

<a id="op-6af669e845be34"></a>
### UTMSource.before save

`operation_foundation_website_record_definitions_utm_source_business_behavior_campaign_tracking_source_before_save`

**Inputs** self.

**Local steps**

- If self.slug.
  - Set self.slug from Platform.utils.slug(self.slug).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0525.json#L1969) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1300)

## Record · Web form

[Record definition](../../../../data/record-types/web_form.json)

<a id="op-051889a2db9822"></a>
### Web Form.validate

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate`

**Inputs** self.

**Record and data access** read “DocType” via get\_value.

**Explicit failure paths** validation helper — translated “You need to be in developer mode to edit a Standard Web Form”.

**Local steps**

- Evaluate super().validate().
- If not self.module.
  - Set self.module from Platform.db.get\_value(“DocType”, self.doc\_type, “module”).
- Set in\_user\_env from not (Platform.flags.in\_install or Platform.flags.in\_patch or Platform.in\_test or Platform.flags.in\_fixtures).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_patch → Platform.in\_test → Platform.flags.in\_fixtures.
- If (in\_user\_env and self.is\_standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_user\_env → self.is\_standard → not Platform.conf.developer\_mode.
  - If self.has\_value\_changed(“published”).
    - Set published\_value from self.published.
    - Evaluate self.reload().
    - Set self.published from published\_value.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “You need to be in developer mode to edit a Standard Web Form”).
- If not Platform.flags.in\_import.
  - Evaluate self.validate\_fields().
  - Evaluate self.warn\_about\_empty\_pages().
- Evaluate self.validate\_hidden\_and\_mandatory().
- Evaluate self.validate\_guest\_key\_link\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fields](operations-018.md#op-003ce13a46225e), [warn about empty pages](operations-018.md#op-aff04bab4cbd1a), [validate hidden and mandatory](operations-018.md#op-b3d67e8ca98048), [validate guest key link fields](operations-018.md#op-c651eb79e65c5c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L44) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1334)

<a id="op-c651eb79e65c5c"></a>
### Web Form.validate guest key link fields

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_guest_key_link_fields`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0}: Link field cannot reference DocType {1} without Guest read permission”.format(field.label, field.options).

**Local steps**

- If not is\_guest\_key\_web\_form(self).
  - Return no value.
- For each field in self.web\_form\_fields.
  - If (field.fieldtype differs from “Link” or not field.options).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldtype differs from “Link” → not field.options.
    - Continue with the next iteration or loop test.
  - If not Platform.has\_permission(field.options, “read”, user = “Guest”).
    - Call the validation error handler Platform.throw(translated “{0}: Link field cannot reference DocType {1} without Guest read permission”.format(field.label, field.options)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(field.options, “read”, user = “Guest”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0528.json#L6468) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1337)

<a id="op-003ce13a46225e"></a>
### Web Form.validate fields

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_fields`

**Inputs** self.

**Explicit failure paths** validation helper — ((translated “Following fields are missing:” + text in the contract) + text in the contract.join(missing)).

**Local steps**

- Bind dependencies no\_value\_fields.
- Set meta from Platform.get\_meta(self.doc\_type).
- Set missing from list of df.fieldname for df drawn from self.web\_form\_fields where (df.fieldname and (df.fieldtype does not belong to no\_value\_fields and not meta.has\_field(df.fieldname))).
  - Draw df from self.web\_form\_fields, keep a combination only if ((df.fieldname and (df.fieldtype does not belong to no\_value\_fields and not meta.has\_field(df.fieldname)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldname → (df.fieldtype does not belong to no\_value\_fields and not meta.has\_field(df.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → not meta.has\_field(df.fieldname).
- If missing.
  - Call the validation error handler Platform.throw(((translated “Following fields are missing:” + text in the contract) + text in the contract.join(missing))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0528.json#L6723) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1336)

<a id="op-aff04bab4cbd1a"></a>
### Web Form.warn about empty pages

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_webform_warn_about_empty_pages`

**Inputs** self.

**State and service calls** msgprint with ((translated “The web form skips these pages, because they have no visible fields: {0}”.format(“, ”.join(generator of nested operand in the contract.bold(nested operand in the contract(nested operand in th ….

**Local steps**

- If empty\_pages bound to self.get\_empty\_pages().
  - Evaluate Platform.msgprint(((translated “The web form skips these pages, because they have no visible fields: {0}”.format(“, ”.join(generator of nested operand in the contract(nested operand in the contract) for la ….
    - Draw label from empty\_pages.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get empty pages](operations-018.md#op-8c6ee2973fd180).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L76) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L469)

<a id="op-8c6ee2973fd180"></a>
### Web Form.get empty pages

`operation_foundation_binding_foundation_website_doctype_web_form_web_form_webform_get_empty_pages`

**Inputs** self.

**Explicit results** list of (page at “label” or translated “Page {0}”.format((i + 2))) for tuple(i, page) drawn from enumerate(pages) where not page at “has\_fields”.

**Local steps**

- Set pages from list().
- For each df in self.web\_form\_fields at slice 1 to no value.
  - If df.fieldtype equals “Page Break”.
    - Evaluate pages.append(mapping(“label” → df.label, “has\_fields” → false)).
  - Otherwise.
    - If (pages and not df.hidden and df.fieldtype does not belong to tuple(“Section Break”, “Column Break”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pages → not df.hidden → df.fieldtype does not belong to tuple(“Section Break”, “Column Break”).
      - Set pages at negative 1 at “has\_fields” from true.
- Return list of (page at “label” or translated “Page {0}”.format((i + 2))) for tuple(i, page) drawn from enumerate(pages) where not page at “has\_fields”.
  - Draw tuple(i, page) from enumerate(pages), keep a combination only if (not page at “has\_fields”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page at “label” → translated “Page {0}”.format((i + 2)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L74) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L467)

<a id="op-b3d67e8ca98048"></a>
### Web Form.validate hidden and mandatory

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_validate_hidden_and_mandatory`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with HiddenAndMandatoryWithoutDefaultError — translated “{0}: Field {1} in row {2} cannot be hidden and mandatory without default”.format(self.name, d.label, d.idx).

**Local steps**

- If self.allow\_incomplete.
  - Return no value.
- For each d in self.web\_form\_fields.
  - If ((d.hidden and d.reqd) and not (d.default or Platform.flags.in\_migrate)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (d.hidden and d.reqd) → not (d.default or Platform.flags.in\_migrate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.hidden → d.reqd.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.default → Platform.flags.in\_migrate.
    - Call the validation error handler Platform.throw(translated “{0}: Field {1} in row {2} cannot be hidden and mandatory without default”.format(self.name, d.label, d.idx), HiddenAndMandatoryWithoutDefaultError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0528.json#L6987) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1338)

<a id="op-1f0fe72c9744b9"></a>
### Web Form.raise if unpublished

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_raise_if_unpublished`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not self.published.
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0528.json#L7207) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1331)

<a id="op-995a5ebddee13c"></a>
### Web Form.reset field parent

`operation_foundation_website_record_definitions_web_form_business_behavior_web_form_reset_field_parent`

**Inputs** self.

**Local steps**

- For each df in self.web\_form\_fields.
  - Set df.parent from self.doc\_type.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0528.json#L7303) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1333)
