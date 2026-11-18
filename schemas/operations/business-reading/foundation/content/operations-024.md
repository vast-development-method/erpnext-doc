# Web content and issued documents · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Website generator

<a id="op-7f922c446941bd"></a>
### Website Generator.get condition field

`operation_foundation_website_website_generator_business_behavior_website_generator_get_condition_field`

**Inputs** self.

**Explicit results** condition\_field.

**Local steps**

- Set condition\_field from self.get\_website\_properties(“condition\_field”).
- If not condition\_field.
  - If self.meta.is\_published\_field.
    - Set condition\_field from self.meta.is\_published\_field.
- Return condition\_field.

**Methods declared on this owner** [get website properties](operations-023.md#op-6a1b23f76549ab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L5256) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1583)

<a id="op-7e4f35f6600db4"></a>
### Website Generator.get page info

`operation_foundation_website_website_generator_business_behavior_website_generator_get_page_info`

**Inputs** self.

**Explicit results** route.

**Local steps**

- Set route from Platform.\_dict().
- Evaluate route.update(mapping(“doc” → self, “page\_or\_generator” → “Generator”, “ref\_doctype” → self.doctype, “idx” → self.idx, …)).
- Evaluate route.update(self.get\_website\_properties()).
- If not route.page\_title.
  - Set route.page\_title from self.get(self.get\_title\_field()).
- Set route.title from route.page\_title.
- Return route.

**Methods declared on this owner** [get website properties](operations-023.md#op-6a1b23f76549ab), [get title field](operations-023.md#op-a524e4f57c3916).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L5378) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1584)

<a id="op-f124b4fbc0b8df"></a>
### Website Generator.send indexing request

`operation_foundation_website_website_generator_business_behavior_website_generator_send_indexing_request`

**Inputs** self, operation\_type = “URL\_UPDATED”.

**Record and data access** read “Website Settings” via get\_single\_value.

**State and service calls** enqueue with “Platform.website.doctype.website\_settings.google\_indexing.publish\_site”.

**Local steps**

- If (Platform.db.get\_single\_value(“Website Settings”, “enable\_google\_indexing”) and self.is\_website\_published() and self.meta.allow\_guest\_to\_view).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Website Settings”, “enable\_google\_indexing”) → self.is\_website\_published() → self.meta.allow\_guest\_to\_view.
  - Set url from Platform.utils.get\_url(self.route).
  - Evaluate Platform.enqueue(“Platform.website.doctype.website\_settings.google\_indexing.publish\_site”, url = url, operation\_type = operation\_type).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is website published](operations-023.md#op-856cb5d1297c8c).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “enable\_google\_indexing”) · service or queued work from Platform.enqueue(“Platform.website.doctype.website\_settings.google\_indexing.publish\_site”, url = url, operation\_type = operation\_type).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L5712) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1598)

<a id="op-15ec7d6faf8300"></a>
### Website Generator.allow website search indexing

`operation_foundation_website_website_generator_business_behavior_website_generator_allow_website_search_indexing`

**Inputs** self.

**Explicit results** self.meta.index\_web\_pages\_for\_search.

**Local steps**

- Return self.meta.index\_web\_pages\_for\_search.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L5976) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1580)

<a id="op-2c64aa256682a7"></a>
### Website Generator.remove old route from index

`operation_foundation_website_website_generator_business_behavior_website_generator_remove_old_route_from_index`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.allow\_website\_search\_indexing() or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.allow\_website\_search\_indexing() → Platform.in\_test.
  - Return no value.
- Set old\_doc from self.get\_doc\_before\_save().
- If (old\_doc and old\_doc.route differs from self.route).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc → old\_doc.route differs from self.route.
  - Bind dependencies remove\_document\_from\_index.
  - Evaluate remove\_document\_from\_index(old\_doc.route).

If control reaches the end, it returns no value.

**Methods declared on this owner** [allow website search indexing](operations-024.md#op-15ec7d6faf8300).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L6021) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1595)

<a id="op-3425e2500fe408"></a>
### Website Generator.update website search index

`operation_foundation_website_website_generator_business_behavior_website_generator_update_website_search_index`

**Inputs** self.

**State and service calls** enqueue with update\_index\_for\_path · enqueue with remove\_document\_from\_index.

**Explicit results** no value.

**Local steps**

- If (not self.allow\_website\_search\_indexing() or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.allow\_website\_search\_indexing() → Platform.in\_test.
  - Return no value.
- Bind dependencies remove\_document\_from\_index, update\_index\_for\_path.
- If self.is\_website\_published().
  - Evaluate Platform.enqueue(update\_index\_for\_path, path = self.route, enqueue\_after\_commit = true).
- Otherwise.
  - If self.route.
    - Evaluate Platform.enqueue(remove\_document\_from\_index, path = self.route, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [allow website search indexing](operations-024.md#op-15ec7d6faf8300), [is website published](operations-023.md#op-856cb5d1297c8c).

**Values supplied outside this operation** service or queued work from Platform.enqueue(update\_index\_for\_path, path = self.route, enqueue\_after\_commit = true), Platform.enqueue(remove\_document\_from\_index, path = self.route, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0540.json#L6193) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1600)

## Record · Website meta tag

[Record definition](../../../../data/record-types/website_meta_tag.json)

<a id="op-1145540df26d92"></a>
### Website Meta Tag.get content

`operation_foundation_website_record_definitions_website_meta_tag_business_behavior_website_meta_tag_get_content`

**Inputs** self.

**Explicit results** (self.value or empty text).replace(whitespace '\\n', one space).

**Local steps**

- Return (self.value or empty text).replace(whitespace '\\n', one space).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.value → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L2458) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1454)

<a id="op-db66bc8d9e98c5"></a>
### Website Meta Tag.get meta dict

`operation_foundation_website_record_definitions_website_meta_tag_business_behavior_website_meta_tag_get_meta_mapping`

**Inputs** self.

**Explicit results** mapping(self.key → self.get\_content()).

**Local steps**

- Return mapping(self.key → self.get\_content()).

**Methods declared on this owner** [get content](operations-024.md#op-1145540df26d92).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L2530) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1455)

<a id="op-bd61b27bec0cc2"></a>
### Website Meta Tag.set in context

`operation_foundation_website_record_definitions_website_meta_tag_business_behavior_website_meta_tag_set_in_context`

**Inputs** self, context.

**Explicit results** context.

**Local steps**

- Evaluate context.setdefault(“metatags”, Platform.\_dict(mapping())).
- Set context.metatags at self.key from self.get\_content().
- Return context.

**Methods declared on this owner** [get content](operations-024.md#op-1145540df26d92).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L2597) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1456)

## Record · Website route meta

[Record definition](../../../../data/record-types/website_route_meta.json)

<a id="op-9e77c15964f6b9"></a>
### Website Route Meta.autoname

`operation_foundation_website_record_definitions_website_route_meta_business_behavior_website_route_meta_autoname`

**Inputs** self.

**Local steps**

- If (self.name and self.name.startswith(“/”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name → self.name.startswith(“/”).
  - Set self.name from self.name at slice 1 to no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L3383) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1457)

<a id="op-d6184cf18d6d4d"></a>
### Website Route Meta.clear cache

`operation_foundation_website_record_definitions_website_route_meta_business_behavior_website_route_meta_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies has\_meta\_tags.
- Evaluate has\_meta\_tags.clear\_cache().
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L3503) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1458)

## Record · Website script

[Record definition](../../../../data/record-types/website_script.json)

<a id="op-83b78699cf312e"></a>
### Website Script.on update

`operation_foundation_website_record_definitions_website_script_business_behavior_website_script_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(user = “Guest”).
- Bind dependencies clear\_cache.
- Evaluate clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L3587) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1461)

## Record · Website settings

[Record definition](../../../../data/record-types/website_settings.json)

<a id="op-3780c60d91ae91"></a>
### Authorize access

`operation_foundation_website_record_definitions_website_settings_google_indexing_business_behavior_authorize_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** reauthorize, code.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup, record mutation request.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L52) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1475)

<a id="op-ac1e8a3660561b"></a>
### Get google indexing object

`operation_foundation_website_record_definitions_website_settings_google_indexing_business_behavior_get_google_indexing_object`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Website Settings” via get\_doc.

**Explicit results** oauth\_obj.get\_google\_service\_object(account.get\_access\_token(), account.get\_password(fieldname = “indexing\_refresh\_token\_secret”, raise\_exception = false)).

**Local steps**

- Set account from Platform.get\_doc(“Website Settings”).
- Set oauth\_obj from GoogleOAuth(“indexing”).
- Return oauth\_obj.get\_google\_service\_object(account.get\_access\_token(), account.get\_password(fieldname = “indexing\_refresh\_token\_secret”, raise\_exception = false)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L53) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1476)

<a id="op-4685e749847f54"></a>
### Publish site

`operation_foundation_website_record_definitions_website_settings_google_indexing_business_behavior_publish_site`

**Inputs** url, operation\_type = “URL\_UPDATED”.

**Local steps**

- Bind dependencies HttpError.
- Set google\_indexing from get\_google\_indexing\_object().
- Set body from mapping(“url” → url, “type” → operation\_type).
- Attempt the following.
  - Evaluate google\_indexing.urlNotifications().publish(body = body, x\_\_xgafv = “2”).execute().
- On failure (HttpError) bound to e.
  - Evaluate Platform.log\_error(message = e, title = “API Indexing Issue”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L4221) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1477)

<a id="op-b9025be835b9eb"></a>
### Website Settings.validate

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_top\_bar\_items().
- Evaluate self.validate\_footer\_items().
- Evaluate self.validate\_home\_page().
- Evaluate self.validate\_google\_settings().
- Evaluate self.validate\_redirects().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate top bar items](operations-024.md#op-de374f1d501e0c), [validate footer items](operations-024.md#op-dc8be3ab1ad98e), [validate home page](operations-024.md#op-a4f55d91a38992), [validate google settings](operations-024.md#op-13cfe64b17be5c), [validate redirects](operations-024.md#op-a44ac09495ec5e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L4956) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1469)

<a id="op-a4f55d91a38992"></a>
### Website Settings.validate home page

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate_home_page`

**Inputs** self.

**State and service calls** msgprint with (translated “Invalid Home Page” + “ (Standard pages - home, login, products, blog, about, contact)”).

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- Bind dependencies PathResolver.
- If (self.home\_page and not PathResolver(self.home\_page).is\_valid\_path()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.home\_page → not PathResolver(self.home\_page).is\_valid\_path().
  - Evaluate Platform.msgprint((translated “Invalid Home Page” + “ (Standard pages - home, login, products, blog, about, contact)”)).
  - Set self.home\_page from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L5087) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1472)

<a id="op-de374f1d501e0c"></a>
### Website Settings.validate top bar items

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate_top_bar_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} does not exist in row {1}”.format(top\_bar\_item.parent\_label, top\_bar\_item.idx) · validation helper — translated “{0} in row {1} cannot have both URL and child items”.format(top\_bar\_item.parent\_label, top\_bar\_item.idx).

**Local steps**

- For each top\_bar\_item in self.get(“top\_bar\_items”).
  - If top\_bar\_item.parent\_label.
    - Set parent\_label\_item from self.get(“top\_bar\_items”, mapping(“label” → top\_bar\_item.parent\_label)).
    - If not parent\_label\_item.
      - Call the validation error handler Platform.throw(translated “{0} does not exist in row {1}”.format(top\_bar\_item.parent\_label, top\_bar\_item.idx)).
    - Otherwise.
      - If (not parent\_label\_item at 0 or parent\_label\_item at 0.url).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_label\_item at 0 → parent\_label\_item at 0.url.
        - Call the validation error handler Platform.throw(translated “{0} in row {1} cannot have both URL and child items”.format(top\_bar\_item.parent\_label, top\_bar\_item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L5272) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1474)

<a id="op-dc8be3ab1ad98e"></a>
### Website Settings.validate footer items

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate_footer_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} does not exist in row {1}”.format(footer\_item.parent\_label, footer\_item.idx) · validation helper — translated “{0} in row {1} cannot have both URL and child items”.format(footer\_item.parent\_label, footer\_item.idx).

**Local steps**

- For each footer\_item in self.get(“footer\_items”).
  - If footer\_item.parent\_label.
    - Set parent\_label\_item from self.get(“footer\_items”, mapping(“label” → footer\_item.parent\_label)).
    - If not parent\_label\_item.
      - Call the validation error handler Platform.throw(translated “{0} does not exist in row {1}”.format(footer\_item.parent\_label, footer\_item.idx)).
    - Otherwise.
      - If (not parent\_label\_item at 0 or parent\_label\_item at 0.url).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_label\_item at 0 → parent\_label\_item at 0.url.
        - Call the validation error handler Platform.throw(translated “{0} in row {1} cannot have both URL and child items”.format(footer\_item.parent\_label, footer\_item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L5604) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1470)

<a id="op-13cfe64b17be5c"></a>
### Website Settings.validate google settings

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate_google_settings`

**Inputs** self.

**Record and data access** read “Google Settings” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Enable Google API in Google Settings.”.

**Local steps**

- If (self.enable\_google\_indexing and not Platform.get\_cached\_value(“Google Settings”, no value, “enable”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_google\_indexing → not Platform.get\_cached\_value(“Google Settings”, no value, “enable”).
  - Call the validation error handler Platform.throw(translated “Enable Google API in Google Settings.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Google Settings”, no value, “enable”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L5936) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1471)

<a id="op-a44ac09495ec5e"></a>
### Website Settings.validate redirects

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_validate_redirects`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L6068) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1473)

<a id="op-ca497fcb6346f0"></a>
### Website Settings.on update

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-024.md#op-2efd7a4e7e5660).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L6352) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1468)

<a id="op-2efd7a4e7e5660"></a>
### Website Settings.clear cache

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(user = “Guest”).
- Bind dependencies clear\_cache.
- Evaluate clear\_cache().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L6403) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1466)

<a id="op-ae885f7ab474e0"></a>
### Website Settings.get access token

`operation_foundation_website_record_definitions_website_settings_business_behavior_website_settings_get_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValidationError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L51) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1467)
