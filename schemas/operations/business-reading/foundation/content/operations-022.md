# Web content and issued documents · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Web page

[Record definition](../../../../data/record-types/web_page.json)

<a id="op-2617dc750dc238"></a>
### Web Page.set metatags

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_set_metatags`

**Inputs** self, context.

**Local steps**

- If not context.metatags.
  - Set context.metatags from mapping(“name” → (self.meta\_title or self.title), “description” → self.meta\_description, “image” → (self.meta\_image or find\_first\_image((context.main\_section or empty text))), “og:type” → “website”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta\_title → self.title.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta\_image → find\_first\_image((context.main\_section or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.main\_section → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L3202) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1425)

<a id="op-3903b79380d112"></a>
### Web Page.validate dates

`operation_foundation_website_record_definitions_web_page_business_behavior_web_page_validate_dates`

**Inputs** self.

**State and service calls** msgprint with translated “Clearing end date, as it cannot be in the past for published pages.”.

**Explicit failure paths** validation helper — translated “End Date cannot be before Start Date!”.

**Local steps**

- If self.end\_date.
  - If (self.start\_date and get\_datetime(self.end\_date) &lt; get\_datetime(self.start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.start\_date → get\_datetime(self.end\_date) &lt; get\_datetime(self.start\_date).
    - Call the validation error handler Platform.throw(translated “End Date cannot be before Start Date!”).
  - If (self.published and now() &gt; self.end\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.published → now() &gt; self.end\_date.
    - Set self.end\_date from no value.
    - Evaluate Platform.msgprint(translated “Clearing end date, as it cannot be in the past for published pages.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L3404) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1429)

<a id="op-0001cfa8ebdf2d"></a>
### Check publish status

`operation_foundation_website_record_definitions_web_page_business_behavior_check_publish_status`

**Inputs** no declared parameters.

**Record and data access** read “Web Page” via get\_all.

**State and service calls** request set\_value on “Web Page”.

**Local steps**

- Set web\_pages from Platform.get\_all(“Web Page”, fields = list(“name”, “published”, “start\_date”, “end\_date”)).
- Set now\_date from get\_datetime(now()).
- For each page in web\_pages.
  - Set start\_date from page.start\_date when page.start\_date, otherwise empty text.
    - Value choice on page.start\_date — true gives page.start\_date, false gives empty text.
  - Set end\_date from page.end\_date when page.end\_date, otherwise empty text.
    - Value choice on page.end\_date — true gives page.end\_date, false gives empty text.
  - If page.published.
    - If ((start\_date and now\_date &lt; start\_date) or (end\_date and now\_date &gt; end\_date)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (start\_date and now\_date &lt; start\_date) → (end\_date and now\_date &gt; end\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → now\_date &lt; start\_date.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → now\_date &gt; end\_date.
      - Evaluate Platform.db.set\_value(“Web Page”, page.name, “published”, 0).
  - Otherwise.
    - If start\_date.
      - If (not end\_date or (end\_date and now\_date &lt; end\_date)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not end\_date → (end\_date and now\_date &lt; end\_date).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → now\_date &lt; end\_date.
        - Evaluate Platform.db.set\_value(“Web Page”, page.name, “published”, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L3662) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1416)

<a id="op-fbb3f93d702e0a"></a>
### Get web blocks html

`operation_foundation_website_record_definitions_web_page_business_behavior_get_web_blocks_document_markup`

**Inputs** blocks.

**Record and data access** resolve a document from “Web Template” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Set out from Platform.\_dict(html = empty text, scripts = mapping(), styles = mapping()).
- Set extracted\_scripts from mapping().
- Set extracted\_styles from mapping().
- For each block in blocks.
  - Set web\_template from Platform.get\_cached\_doc(“Web Template”, block.web\_template).
  - Set rendered\_html from Platform.render\_template(“templates/includes/web\_block.html”, context = mapping(“web\_block” → block, “web\_template\_html” → web\_template.render(block.web\_template\_values), “web\_template\_type” → web\_template.type)).
  - Set tuple(html, scripts, styles) from extract\_script\_and\_style\_tags(rendered\_html).
  - Update out.html using + html.
  - If block.web\_template does not belong to extracted\_scripts.
    - Evaluate extracted\_scripts.setdefault(block.web\_template, list()).
    - Update extracted\_scripts at block.web\_template using + scripts.
  - If block.web\_template does not belong to extracted\_styles.
    - Evaluate extracted\_styles.setdefault(block.web\_template, list()).
    - Update extracted\_styles at block.web\_template using + styles.
- Set out.scripts from extracted\_scripts.
- Set out.styles from extracted\_styles.
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Web Template”, block.web\_template).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L4128) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1419)

<a id="op-19ab78493b7b15"></a>
### Extract script and style tags

`operation_foundation_website_record_definitions_web_page_business_behavior_extract_script_and_style_tags`

**Inputs** html.

**Explicit results** tuple(str(soup), scripts, styles).

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(html, “html.parser”).
- Set scripts from list().
- Set styles from list().
- For each script in soup.find\_all(“script”).
  - Evaluate scripts.append(script.string).
  - Evaluate script.extract().
- For each style in soup.find\_all(“style”).
  - Evaluate styles.append(style.string).
  - Evaluate style.extract().
- Return tuple(str(soup), scripts, styles).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L4654) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1417)

<a id="op-c95e01883a1967"></a>
### Get dynamic web pages

`operation_foundation_website_record_definitions_web_page_business_behavior_get_dynamic_web_pages`

**Inputs** no declared parameters.

**Wrappers, in declaration order** redis\_cache(ttl = (60 × 60)).

**Declared result** dict at tuple(str, str).

**Record and data access** read “Web Page” via get\_all.

**Explicit results** pages.

**Local steps**

- Set pages from Platform.get\_all(“Web Page”, fields = list(“name”, “route”, “modified”), filters = dict(published = 1, dynamic\_route = 1), update = mapping(“doctype” → “Web Page”)).
- Set get\_web\_pages\_with\_dynamic\_routes from (Platform.get\_hooks(“get\_web\_pages\_with\_dynamic\_routes”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“get\_web\_pages\_with\_dynamic\_routes”) → list().
- For each method in get\_web\_pages\_with\_dynamic\_routes.
  - Evaluate pages.extend(Platform.get\_attr(method)()).
- Return pages.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_web\_pages\_with\_dynamic\_routes”), Platform.get\_attr(method).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L4943) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1418)

## Record · Web page view

[Record definition](../../../../data/record-types/web_page_view.json)

<a id="op-75d09135376219"></a>
### Web Page View.clear old logs

`operation_foundation_website_record_definitions_web_page_view_business_behavior_web_page_view_clear_old_logs`

**Inputs** days = 180.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Web Page View”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L5266) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1437)

<a id="op-48af2a3d9e14cc"></a>
### Make view log

`operation_foundation_website_record_definitions_web_page_view_business_behavior_make_view_log`

**Inputs** referrer = no value, browser = no value, version = no value, user\_tz = no value, source = no value, campaign = no value, medium = no value, content = no value, visitor\_id = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** read “Web Page View” via exists.

**State and service calls** request new\_doc for “Web Page View”.

**Explicit results** no value.

**Local steps**

- If not is\_tracking\_enabled().
  - Return no value.
- Set path from Platform.request.headers.get(“Referer”).
- If not Platform.utils.is\_site\_link(path).
  - Return no value.
- Set path from urlparse(path).path.
- Set request\_dict from Platform.request.\_\_dict\_\_.
- Set user\_agent from request\_dict.get(“environ”, mapping()).get(“HTTP\_USER\_AGENT”).
- If referrer.
  - Set referrer from referrer.split(“?”, 1) at 0.
- If (path differs from “/” and path.startswith(“/”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in path differs from “/” → path.startswith(“/”).
  - Set path from path at slice 1 to no value.
- If path.startswith(tuple(“api/”, “app/”, “assets/”, “private/files/”)).
  - Return no value.
- Set is\_unique from (visitor\_id and not bool(Platform.db.exists(“Web Page View”, mapping(“visitor\_id” → visitor\_id)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in visitor\_id → not bool(Platform.db.exists(“Web Page View”, mapping(“visitor\_id” → visitor\_id))).
- Set view from Platform.new\_doc(“Web Page View”).
- Set view.path from path.
- Set view.referrer from referrer.
- Set view.browser from browser.
- Set view.browser\_version from version.
- Set view.time\_zone from user\_tz.
- Set view.user\_agent from user\_agent.
- Set view.is\_unique from is\_unique.
- Set view.source from source.
- Set view.campaign from campaign.
- Set view.medium from (medium or empty text).lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in medium → empty text.
- Set view.content from content.
- Set view.visitor\_id from visitor\_id.
- Attempt the following.
  - Evaluate view.deferred\_insert().
- On failure (Exception).
  - Evaluate Platform.clear\_last\_message().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L49) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1436)

<a id="op-bcd2ba99cb417e"></a>
### Get page view count

`operation_foundation_website_record_definitions_web_page_view_business_behavior_get_page_view_count`

**Inputs** path.

**Wrappers, in declaration order** Platform.whitelist(), redis\_cache(ttl = (5 × 60)).

**Record and data access** read “Web Page View” via count.

**Explicit results** Platform.db.count(“Web Page View”, filters = mapping(“path” → path)).

**Local steps**

- Return Platform.db.count(“Web Page View”, filters = mapping(“path” → path)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L6499) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1434)

<a id="op-4086ac9fc43c58"></a>
### Is tracking enabled

`operation_foundation_website_record_definitions_web_page_view_business_behavior_is_tracking_enabled`

**Inputs** no declared parameters.

**Explicit results** Platform.get\_website\_settings(“enable\_view\_tracking”).

**Local steps**

- Return Platform.get\_website\_settings(“enable\_view\_tracking”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0532.json#L6643) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1435)

## Record · Web template

[Record definition](../../../../data/record-types/web_template.json)

<a id="op-75be82c84c631b"></a>
### Web Template.validate

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enable developer mode to create a standard Web Template”.

**Local steps**

- If (self.standard and not Platform.conf.developer\_mode and not Platform.flags.in\_patch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard → not Platform.conf.developer\_mode → not Platform.flags.in\_patch.
  - Call the validation error handler Platform.throw(translated “Enable developer mode to create a standard Web Template”).
- For each field in self.fields.
  - If not field.fieldname.
    - Set field.fieldname from Platform.scrub(field.label).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L706) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1448)

<a id="op-a5ab0eb89976c2"></a>
### Web Template.before save

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_before_save`

**Inputs** self.

**Local steps**

- If Platform.conf.developer\_mode.
  - If self.standard.
    - Evaluate self.export\_to\_files().
  - Set was\_standard from (self.get\_doc\_before\_save() or mapping()).get(“standard”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_doc\_before\_save() → mapping().
  - If (was\_standard and not self.standard).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in was\_standard → not self.standard.
    - Evaluate self.import\_from\_files().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export to files](operations-022.md#op-90dd55e69c3749), [import from files](operations-022.md#op-eb23da7f649dde).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L904) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1438)

<a id="op-e1839473571945"></a>
### Web Template.on update

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_on_update`

**Inputs** self.

**Record and data access** read “Web Page” via get\_all.

**Local steps**

- Set routes from Platform.get\_all(“Web Page”, filters = list(list(“Web Page Block”, “web\_template”, “=”, self.name), list(“Web Page”, “published”, “=”, 1)), pluck = “route”).
- For each route in routes.
  - Evaluate clear\_cache(route).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1091) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1446)

<a id="op-93a1a0fbfb48b9"></a>
### Web Template.on trash

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_on_trash`

**Inputs** self.

**Local steps**

- If (Platform.conf.developer\_mode and self.standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.standard.
  - Evaluate rmtree(self.get\_template\_folder()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get template folder](operations-022.md#op-af51f86a57b192).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1287) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1445)

<a id="op-90dd55e69c3749"></a>
### Web Template.export to files

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_export_to_files`

**Inputs** self.

**Local steps**

- Set tuple(html, self.template) from tuple(self.template, empty text).
- Evaluate write\_document\_file(self, create\_init = true).
- Evaluate self.create\_template\_file(html).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create template file](operations-022.md#op-6ad2170cb88cd6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1383) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1440)

<a id="op-eb23da7f649dde"></a>
### Web Template.import from files

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_import_from_files`

**Inputs** self.

**Local steps**

- Set self.template from self.get\_template(standard = true).
- Evaluate rmtree(self.get\_template\_folder()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get template](operations-022.md#op-d8a01f4f9bc11f), [get template folder](operations-022.md#op-af51f86a57b192).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1510) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1444)

<a id="op-6ad2170cb88cd6"></a>
### Web Template.create template file

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_create_template_file`

**Inputs** self, html = no value.

**Local steps**

- If self.standard.
  - Set path from self.get\_template\_path().
  - If not os.path.exists(path).
    - Within open(path, “w”) bound as template\_file.
      - If html.
        - Evaluate template\_file.write(html).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get template path](operations-022.md#op-c7ab9685510cf3).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1615) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1439)

<a id="op-af51f86a57b192"></a>
### Web Template.get template folder

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_get_template_folder`

**Inputs** self.

**Explicit results** os.path.join(module\_path, doctype, docname).

**Local steps**

- Set module from (self.module or “Website”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.module → “Website”.
- Set module\_path from get\_module\_path(module).
- Set tuple(doctype, docname) from scrub\_dt\_dn(self.doctype, self.name).
- Return os.path.join(module\_path, doctype, docname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1798) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1442)

<a id="op-c7ab9685510cf3"></a>
### Web Template.get template path

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_get_template_path`

**Inputs** self.

**Explicit results** os.path.join(folder, file\_name).

**Local steps**

- Set folder from self.get\_template\_folder().
- Set file\_name from (Platform.scrub(self.name) + “.html”).
- Return os.path.join(folder, file\_name).

**Methods declared on this owner** [get template folder](operations-022.md#op-af51f86a57b192).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L1969) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1443)

<a id="op-d8a01f4f9bc11f"></a>
### Web Template.get template

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_get_template`

**Inputs** self, standard = false.

**Explicit results** template.

**Local steps**

- If standard.
  - Set template from self.get\_template\_path().
  - Within open(template) bound as template\_file.
    - Set template from template\_file.read().
- Otherwise.
  - Set template from self.template.
- Return template.

**Methods declared on this owner** [get template path](operations-022.md#op-c7ab9685510cf3).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L2103) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1441)

<a id="op-308db9b94e70b4"></a>
### Web Template.render

`operation_foundation_website_record_definitions_web_template_business_behavior_web_template_render`

**Inputs** self, values = no value.

**Explicit results** Platform.render\_template(template, values).

**Local steps**

- If not values.
  - Set values from mapping().
- Set values from Platform.parse\_json(values).
- Evaluate values.update(mapping(“values” → values)).
- Set template from self.get\_template(self.standard).
- Return Platform.render\_template(template, values).

**Methods declared on this owner** [get template](operations-022.md#op-d8a01f4f9bc11f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0533.json#L2261) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1447)

## Report · Website analytics

<a id="op-07902066967604"></a>
### Execute

`operation_foundation_website_report_website_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** WebsiteAnalytics(filters).run().

**Local steps**

- Return WebsiteAnalytics(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L2514) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1507)

<a id="op-0fe9e87b47b43e"></a>
### Website Analytics.initialize

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If not self.filters.to\_date.
  - Set self.filters.to\_date from datetime.now().
- If not self.filters.from\_date.
  - Set self.filters.from\_date from Platform.utils.add\_days(self.filters.to\_date, negative 7).
- If not self.filters.range.
  - Set self.filters.range from “Daily”.
- Set self.filters.to\_date from Platform.utils.add\_days(self.filters.to\_date, 1).
- Set self.query\_filters from mapping(“creation” → list(“between”, list(self.filters.from\_date, self.filters.to\_date))).
- Set self.group\_by from self.filters.group\_by.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L2578) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1514)

<a id="op-69cf0a7c5ee900"></a>
### Website Analytics.run

`operation_foundation_website_report_website_analytics_business_behavior_website_analytics_run`

**Inputs** self.

**Explicit results** tuple(columns, data at slice no value to 250, no value, chart, …).

**Local steps**

- Set columns from self.get\_columns().
- Set data from self.get\_data().
- Set chart from self.get\_chart\_data().
- Set summary from self.get\_report\_summary().
- Return tuple(columns, data at slice no value to 250, no value, chart, …).

**Methods declared on this owner** [get columns](operations-023.md#op-927817b26071d6), [get data](operations-023.md#op-75c2af9c50d0ab), [get chart data](operations-023.md#op-9d81da879c4bb8), [get report summary](operations-023.md#op-2007009df4141b).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0537.json#L2988) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1517)
