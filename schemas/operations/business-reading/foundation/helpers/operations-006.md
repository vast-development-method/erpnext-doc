# Shared value and file services · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Browser

<a id="op-bf34c0f00c8496"></a>
### Browser.add page number

`operation_foundation_binding_foundation_utils_pdf_generator_browser_browser_add_page_number`

**Inputs** self, soup.

**Record and data access** read “Print Format” via exists · resolve a document from “Print Format” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies uses\_beta\_renderer.
- Bind dependencies page\_number\_html.
- If (self.is\_print\_designer or not self.print\_format).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_print\_designer → not self.print\_format.
  - Return no value.
- If any(generator of el.find(class\_ = list(“page”, “topage”)) for el drawn from soup.find\_all(id = list(“header-html”, “footer-html”))).
  - Draw el from soup.find\_all(id = list(“header-html”, “footer-html”)).
  - Return no value.
- If not Platform.db.exists(“Print Format”, self.print\_format, cache = true).
  - Return no value.
- Set print\_format from Platform.get\_cached\_doc(“Print Format”, self.print\_format).
- Set position from (print\_format.page\_number or empty text).lower().replace(one space, “\_”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.page\_number → empty text.
- If (uses\_beta\_renderer(print\_format) or not position.startswith(tuple(“top\_”, “bottom\_”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uses\_beta\_renderer(print\_format) → not position.startswith(tuple(“top\_”, “bottom\_”)).
  - Return no value.
- Set html\_id from “header-html” when position.startswith(“top\_”), otherwise “footer-html”.
  - Value choice on position.startswith(“top\_”) — true gives “header-html”, false gives “footer-html”.
- If not target bound to soup.find(id = html\_id).
  - Set target from soup.new\_tag(“div”, id = html\_id).
  - Evaluate soup.body.append(target).
- Evaluate target.append(BeautifulSoup(page\_number\_html(position), “html.parser”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Format”, self.print\_format).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L64) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L222)

<a id="op-222b6faad2bd79"></a>
### Browser.inject page no script

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_inject_page_number_script`

**Inputs** self, soup.

**Local steps**

- Set path from Platform.get\_app\_path(“Platform”, “utils”, “pdf\_generator”, “update\_page\_no.js”).
- Set tag from soup.new\_tag(“script”).
- Evaluate tag.append(soup.new\_string(Platform.read\_file(path))).
- Evaluate soup.head.append(tag).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L857) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L448)

<a id="op-ebc279e6ef01ea"></a>
### Browser.try async header footer pdf

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_try_async_header_footer_portable_document`

**Inputs** self.

**Local steps**

- If (self.header\_page and not self.is\_header\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.header\_page → not self.is\_header\_dynamic.
  - Evaluate self.header\_page.generate\_pdf(wait\_for\_pdf = false).
- If (self.footer\_page and not self.is\_footer\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.footer\_page → not self.is\_footer\_dynamic.
  - Evaluate self.footer\_page.generate\_pdf(wait\_for\_pdf = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L1057) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L460)

<a id="op-f74ddf1004490e"></a>
### Browser.get converted num

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_get_converted_number`

**Inputs** self, num\_str, unit = “px”.

**Explicit results** convert\_uom(parsed at “value”, parsed at “unit”, unit, only\_number = true).

**Local steps**

- Set parsed from parse\_float\_and\_unit(num\_str).
- If parsed.
  - Return convert\_uom(parsed at “value”, parsed at “unit”, unit, only\_number = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L1216) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L445)

<a id="op-eae748daa652b5"></a>
### Browser.parse pdf options from html

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_parse_portable_document_options_from_document_markup`

**Inputs** self.

**Local steps**

- Bind dependencies get\_print\_format\_styles.
- Bind dependencies PAGE\_LENGTH, PAGE\_MARGIN\_SIDES.
- Set soup from self.soup.
- Set options from self.\_get\_print\_format\_page\_margins().
- Set print\_format\_css from get\_print\_format\_styles(soup).
- Set attrs from tuple(“margin-top”, “margin-bottom”, “margin-left”, “margin-right”, …).
- Update options using bitwise or mapping of style.name → style.value for style drawn from print\_format\_css where (style.name belongs to attrs and (style.name does not belong to PAGE\_MARGIN\_SIDES or re.fullmatch(formatted text 0\|{PAGE\_LENG ….
  - Draw style from print\_format\_css, keep a combination only if ((style.name belongs to attrs and (style.name does not belong to PAGE\_MARGIN\_SIDES or re.fullmatch(formatted text 0\|{PAGE\_LENGTH}, style.value.strip())) and (style.name does not belong to tuple(“page-width” …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in style.name belongs to attrs → (style.name does not belong to PAGE\_MARGIN\_SIDES or re.fullmatch(formatted text 0\|{PAGE\_LENGTH}, style.value.strip())) → (style.name does not belong to tuple(“page-width”, “page-height”) or re.fullmatch(PAGE\_LENGTH, style.value.strip())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in style.name does not belong to PAGE\_MARGIN\_SIDES → re.fullmatch(formatted text 0\|{PAGE\_LENGTH}, style.value.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in style.name does not belong to tuple(“page-width”, “page-height”) → re.fullmatch(PAGE\_LENGTH, style.value.strip()).
- Evaluate self.options.update(options).
- Evaluate self.\_set\_page\_size\_from\_print\_format().
- Evaluate self.\_set\_page\_size\_from\_page\_rule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get print format page margins](operations-006.md#op-7a02cbd6ccea08), [set page size from print format](operations-006.md#op-74962903268516), [set page size from page rule](operations-006.md#op-ba6223e6851af6).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L20) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L453)

<a id="op-74962903268516"></a>
### Browser.set page size from print format

`operation_foundation_binding_foundation_utils_pdf_generator_browser_browser_set_page_size_from_print_format`

**Inputs** self.

**Record and data access** read “Print Format” via exists · read “Print Format” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If any(generator of self.options.get(key) for key drawn from tuple(“page-size”, “page-width”, “page-height”)).
  - Draw key from tuple(“page-size”, “page-width”, “page-height”).
  - Return no value.
- If (not self.print\_format or not Platform.db.exists(“Print Format”, self.print\_format, cache = true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.print\_format → not Platform.db.exists(“Print Format”, self.print\_format, cache = true).
  - Return no value.
- Set paper\_size from Platform.get\_cached\_value(“Print Format”, self.print\_format, “paper\_size”).
- If receipt\_width bound to RECEIPT\_WIDTHS.get(paper\_size).
  - Update self.options using bitwise or mapping(“page-width” → receipt\_width, “page-height” → “297mm”, “fit-height” → true).
- Otherwise.
  - If paper\_size.
    - Set self.options at “page-size” from paper\_size.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Print Format”, self.print\_format, “paper\_size”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L68) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L226)

<a id="op-ba6223e6851af6"></a>
### Browser.set page size from page rule

`operation_foundation_binding_foundation_utils_pdf_generator_browser_browser_set_page_size_from_page_rule`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_page\_rule\_size.
- If any(generator of self.options.get(key) for key drawn from tuple(“page-size”, “page-width”, “page-height”)).
  - Draw key from tuple(“page-size”, “page-width”, “page-height”).
  - Return no value.
- Set css from empty text.join(generator of cstr(tag.string) for tag drawn from self.soup.find\_all(“style”)).
  - Draw tag from self.soup.find\_all(“style”).
- For each tuple(key, value) in get\_page\_rule\_size(css).items().
  - If not self.options.get(key).
    - Set self.options at key from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L67) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L225)

<a id="op-7a02cbd6ccea08"></a>
### Browser.get print format page margins

`operation_foundation_binding_foundation_utils_pdf_generator_browser_browser_get_print_format_page_margins`

**Inputs** self.

**Explicit results** mapping() · get\_page\_rule\_margins(print\_format.css).

**Local steps**

- Bind dependencies uses\_beta\_renderer.
- Bind dependencies get\_page\_rule\_margins.
- Set print\_format from \_print\_format\_doc\_or\_none(self.print\_format).
- If (not print\_format or not print\_format.css or uses\_beta\_renderer(print\_format) or (print\_format.pdf\_generator or resolve\_pdf\_generator()) does not belong to tuple(“chrome”, “PlutoPrint”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → not print\_format.css → uses\_beta\_renderer(print\_format) → (print\_format.pdf\_generator or resolve\_pdf\_generator()) does not belong to tuple(“chrome”, “PlutoPrint”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.pdf\_generator → resolve\_pdf\_generator().
  - Return mapping().
- Return get\_page\_rule\_margins(print\_format.css).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L66) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L224)

<a id="op-4c5e2750275f15"></a>
### Browser.set default page size

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_set_default_page_size`

**Inputs** self.

**Record and data access** read “Print Settings” via get\_single\_value.

**Local steps**

- Set options from self.options.
- Set pdf\_page\_size from (options.get(“page-size”) or Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”) or “A4”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“page-size”) → Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”) → “A4”.
- If pdf\_page\_size equals “Custom”.
  - For each tuple(option, field) in tuple(tuple(“page-height”, “pdf\_page\_height”), tuple(“page-width”, “pdf\_page\_width”)).
    - If not options.get(option).
      - Set value from Platform.db.get\_single\_value(“Print Settings”, field).
      - Set options at option from formatted text {flt(value)}mm when value, otherwise no value.
        - Value choice on value — true gives formatted text {flt(value)}mm, false gives no value.
- Otherwise.
  - Set options at “page-size” from pdf\_page\_size.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”), Platform.db.get\_single\_value(“Print Settings”, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L23) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L456)

<a id="op-e6a174fc3e1c1f"></a>
### Browser.prepare options for pdf

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_prepare_options_for_portable_document`

**Inputs** self.

**Explicit failure paths** Platform.ValidationError(“Page size is required”) · Platform.ValidationError(“Custom page size requires page-height and page-width”) · Platform.ValidationError(“Invalid page size”) · validation helper — Platform.\_(“Margins leave no room for content on a {0}px wide page. Reduce them or use a larger page size.”).format(options.get(“page-width”)).

**Local steps**

- Evaluate self.\_parse\_pdf\_options\_from\_html().
- Evaluate self.\_set\_default\_page\_size().
- Set options from self.options.
- Set updated\_options from mapping(“scale” → 1, “printBackground” → true, “transferMode” → “ReturnAsStream”, “marginTop” → 0, …).
- If (not options.get(“page-height”) or not options.get(“page-width”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not options.get(“page-height”) → not options.get(“page-width”).
  - If not page\_size bound to self.options.get(“page-size”).
    - Raise Platform.ValidationError(“Page size is required”).
  - If page\_size equals “CUSTOM”.
    - Raise Platform.ValidationError(“Custom page size requires page-height and page-width”).
  - Set size from PageSize.get(page\_size).
  - If not size.
    - Raise Platform.ValidationError(“Invalid page size”).
  - Set options at “page-height” from convert\_uom(size at “height”, “mm”, “px”, only\_number = true).
  - Set options at “page-width” from convert\_uom(size at “width”, “mm”, “px”, only\_number = true).
- If isinstance(options at “page-height”, str).
  - Set options at “page-height” from self.\_get\_converted\_num(options at “page-height”).
- If isinstance(options at “page-width”, str).
  - Set options at “page-width” from self.\_get\_converted\_num(options at “page-width”).
- If (cstr(nested operand in the contract.get(“orientation”)).lower() equals “landscape” and options at “page-width” &lt; options at “page-height”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cstr(options.get(“orientation”)).lower() equals “landscape” → options at “page-width” &lt; options at “page-height”.
  - Set tuple(options at “page-width”, options at “page-height”) from tuple(options at “page-height”, options at “page-width”).
- Set updated\_options at “paperWidth” from convert\_uom(options at “page-width”, “px”, “in”, only\_number = true).
- Set min\_size from convert\_uom(30, “mm”, “px”, only\_number = true).
- Set default\_margin from “15mm” when options at “page-height” &gt; min\_size, otherwise “0mm”.
  - Value choice on options at “page-height” &gt; min\_size — true gives “15mm”, false gives “0mm”.
- If not self.header\_page.
  - Evaluate options.setdefault(“margin-top”, default\_margin).
- If not self.footer\_page.
  - Evaluate options.setdefault(“margin-bottom”, default\_margin).
- If not self.is\_print\_designer.
  - Set side\_margin from “15mm” when options at “page-width” &gt; min\_size, otherwise “0mm”.
    - Value choice on options at “page-width” &gt; min\_size — true gives “15mm”, false gives “0mm”.
  - If not options.get(“margin-right”).
    - Set options at “margin-right” from side\_margin.
  - If not options.get(“margin-left”).
    - Set options at “margin-left” from side\_margin.
- If options.get(“margin-left”).
  - Set updated\_options at “marginLeft” from convert\_uom(self.\_get\_converted\_num(options at “margin-left”), “px”, “in”, only\_number = true).
- If options.get(“margin-right”).
  - Set updated\_options at “marginRight” from convert\_uom(self.\_get\_converted\_num(options at “margin-right”), “px”, “in”, only\_number = true).
- Set self.printable\_width from (96 × ((updated\_options at “paperWidth” − updated\_options at “marginLeft”) − updated\_options at “marginRight”)).
- If self.printable\_width &lt; 0.
  - Call the validation error handler Platform.throw(Platform.\_(“Margins leave no room for content on a {0}px wide page. Reduce them or use a larger page size.”).format(options.get(“page-width”))).
- If self.header\_page.
  - Evaluate self.header\_page.set\_device\_metrics(width = int(self.printable\_width)).
  - Set self.header\_height from self.header\_page.get\_element\_height().
- If self.footer\_page.
  - Evaluate self.footer\_page.set\_device\_metrics(width = int(self.printable\_width)).
  - Set self.footer\_height from self.footer\_page.get\_element\_height().
- Set self.body\_page.options from updated\_options.copy().
- If self.header\_page.
  - Set self.header\_page.options from updated\_options.copy().
- If self.footer\_page.
  - Set self.footer\_page.options from updated\_options.copy().
- Set margin\_top from self.\_get\_converted\_num(options.get(“margin-top”, 0)).
- Set margin\_bottom from self.\_get\_converted\_num(options.get(“margin-bottom”, 0)).
- Set header\_with\_top\_margin from 0.
- Set header\_with\_spacing\_top\_margin from 0.
- Set footer\_with\_bottom\_margin from 0.
- Set footer\_height from 0.
- Set header\_owns\_top\_margin from bool(options.get(“header-includes-top-margin”)).
- If self.header\_page.
  - Set header\_with\_top\_margin from (self.header\_height + 0 when header\_owns\_top\_margin, otherwise margin\_top).
    - Value choice on header\_owns\_top\_margin — true gives 0, false gives margin\_top.
  - Set header\_spacing from options.get(“header-spacing”, 0).
  - Set header\_with\_spacing\_top\_margin from (header\_with\_top\_margin + header\_spacing).
  - Set self.header\_page.options at “paperHeight” from convert\_uom(header\_with\_spacing\_top\_margin, “px”, “in”, only\_number = true) when header\_with\_spacing\_top\_margin, otherwise 0.
    - Value choice on header\_with\_spacing\_top\_margin — true gives convert\_uom(header\_with\_spacing\_top\_margin, “px”, “in”, only\_number = true), false gives 0.
- Set margin\_top from convert\_uom(margin\_top, “px”, “in”, only\_number = true).
- If self.header\_page.
  - Set self.header\_page.options at “marginTop” from 0 when header\_owns\_top\_margin, otherwise margin\_top.
    - Value choice on header\_owns\_top\_margin — true gives 0, false gives margin\_top.
- Otherwise.
  - Set self.body\_page.options at “marginTop” from margin\_top.
- If self.footer\_page.
  - Set footer\_height from self.footer\_height.
  - Set footer\_with\_bottom\_margin from (footer\_height + margin\_bottom).
  - Set self.footer\_page.options at “paperHeight” from convert\_uom(footer\_with\_bottom\_margin, “px”, “in”, only\_number = true) when footer\_with\_bottom\_margin, otherwise 0.
    - Value choice on footer\_with\_bottom\_margin — true gives convert\_uom(footer\_with\_bottom\_margin, “px”, “in”, only\_number = true), false gives 0.
- Set margin\_bottom from convert\_uom(margin\_bottom, “px”, “in”, only\_number = true).
- If self.footer\_page.
  - Set self.footer\_page.options at “marginBottom” from margin\_bottom.
- Otherwise.
  - Set self.body\_page.options at “marginBottom” from margin\_bottom.
- Set body\_height from (options.get(“page-height”) − (header\_with\_spacing\_top\_margin + footer\_with\_bottom\_margin)).
- Set self.body\_page.options at “paperHeight” from convert\_uom(body\_height, “px”, “in”, only\_number = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse pdf options from html](operations-006.md#op-eae748daa652b5), [set default page size](operations-006.md#op-4c5e2750275f15), [get converted num](operations-006.md#op-f74ddf1004490e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L22) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L455)

<a id="op-d6ac8c05ddfa5b"></a>
### Browser.get rendered header footer

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_get_rendered_header_footer`

**Inputs** self, content, type, head, styles, css.

**Explicit results** Platform.call(hook\_func at negative 1, soup = self.soup, head = head, content = content, styles = styles, …).

**Local steps**

- Bind dependencies toggle\_visible\_pdf.
- Set html\_id from formatted text {type}-html.
- Set content from content.extract().
- Evaluate toggle\_visible\_pdf(content).
- Set id\_map from mapping(“header” → “pdf\_header\_html”, “footer” → “pdf\_footer\_html”).
- Set hook\_func from Platform.get\_hooks(id\_map.get(type)).
- Return Platform.call(hook\_func at negative 1, soup = self.soup, head = head, content = content, styles = styles, …).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(id\_map.get(type)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L4407) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L446)

<a id="op-05574c829719e6"></a>
### Browser.update header footer page

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_update_header_footer_page`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.header\_page and not self.footer\_page).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.header\_page → not self.footer\_page.
  - Return no value.
- Set total\_pages from len(self.body\_pdf.pages).
- If self.header\_page.
  - If self.is\_header\_dynamic.
    - Evaluate self.header\_page.evaluate(formatted text clone\_and\_update('{“#header-render-container” when self.is\_print\_designer, otherwise “.wrapper”}', {total\_pages}, {1 when self.is\_print\_designer, othe, await\_promise = true).
      - Value choice on self.is\_print\_designer — true gives “#header-render-container”, false gives “.wrapper”.
      - Value choice on self.is\_print\_designer — true gives 1, false gives 0.
- If self.footer\_page.
  - If self.is\_footer\_dynamic.
    - Evaluate self.footer\_page.evaluate(formatted text clone\_and\_update('{“#footer-render-container” when self.is\_print\_designer, otherwise “.wrapper”}', {total\_pages}, {1 when self.is\_print\_designer, othe, await\_promise = true).
      - Value choice on self.is\_print\_designer — true gives “#footer-render-container”, false gives “.wrapper”.
      - Value choice on self.is\_print\_designer — true gives 1, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L24) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L461)

<a id="op-a95bcb4e31315b"></a>
### Browser.update header footer page pd

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_update_header_footer_page_tabular_analysis`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.is\_print\_designer.
  - Return no value.
- If (not self.header\_page and not self.footer\_page).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.header\_page → not self.footer\_page.
  - Return no value.
- If (self.header\_page and not self.is\_header\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.header\_page → not self.is\_header\_dynamic.
  - Evaluate self.header\_page.evaluate(“clone\_and\_update('#header-render-container', 0, 1, 'Header', 0);”, await\_promise = true).
- If (self.footer\_page and not self.is\_footer\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.footer\_page → not self.is\_footer\_dynamic.
  - Evaluate self.footer\_page.evaluate(“clone\_and\_update('#footer-render-container', 0, 1, 'Footer', 0);”, await\_promise = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L5171) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L462)

<a id="op-e75af8d3916ead"></a>
### Browser.open header footer pages

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_open_header_footer_pages`

**Inputs** self.

**Local steps**

- Set self.header\_page from no value.
- Set self.footer\_page from no value.
- If header\_content bound to self.soup.find(id = “header-html”).
  - Set self.header\_page from self.new\_page(“header”).
  - Evaluate self.header\_page.set\_tab\_url(get\_host\_url()).
- If footer\_content bound to self.soup.find(id = “footer-html”).
  - Set self.footer\_page from self.new\_page(“footer”).
  - Evaluate self.footer\_page.set\_tab\_url(get\_host\_url()).
- Set self.header\_content from header\_content.
- Set self.footer\_content from footer\_content.

If control reaches the end, it returns no value.

**Methods declared on this owner** [new page](operations-005.md#op-0400f737887f81).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L5406) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L452)

<a id="op-59b383349f8a3c"></a>
### Browser.close

`operation_foundation_utils_portable_document_generator_browser_business_behavior_browser_close`

**Inputs** self.

**Local steps**

- Evaluate self.session.disconnect().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L5737) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L442)

<a id="op-09bb0913fd410b"></a>
### Page Size.get

`operation_foundation_utils_portable_document_generator_browser_business_behavior_page_size_get`

**Inputs** cls, name.

**Wrappers, in declaration order** classmethod.

**Explicit results** mapping(“width” → width, “height” → height) · no value.

**Local steps**

- If name belongs to cls.page\_sizes.
  - Set tuple(width, height) from cls.page\_sizes at name.
  - Return mapping(“width” → width, “height” → height).
- Otherwise.
  - Return no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L5790) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L463)

## Service · Caching

<a id="op-77e825dc56437f"></a>
### Generate request cache key

`operation_foundation_utils_caching_business_behavior_generate_request_cache_key`

**Inputs** args, kwargs.

**Declared result** tuple.

**Explicit results** args · tuple(args, \_KWD\_MARK, frozenset(kwargs.items())).

**Local steps**

- If not kwargs.
  - Return args.
- Return tuple(args, \_KWD\_MARK, frozenset(kwargs.items())).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L75) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1569)

<a id="op-f4b7b5d8d4de15"></a>
### Request cache

`operation_foundation_utils_caching_business_behavior_request_cache`

**Inputs** func.

**Declared result** Callable.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L5322) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1573)

<a id="op-76e4cbe9342eb4"></a>
### Request cache.wrapper

`operation_foundation_utils_caching_business_behavior_request_cache_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** func(expanded args, expanded names kwargs) · \_cache at func at args\_key · return\_val.

**Local steps**

- Set \_cache from getattr(Platform.local, “request\_cache”, no value).
- If \_cache is identical to no value.
  - Return func(expanded args, expanded names kwargs).
- Attempt the following.
  - Set args\_key from \_\_generate\_request\_cache\_key(args, kwargs).
- On failure (Exception).
  - Return func(expanded args, expanded names kwargs).
- Attempt the following.
  - Return \_cache at func at args\_key.
- On failure (TypeError).
  - Return func(expanded args, expanded names kwargs).
- On failure (KeyError).
  - Set return\_val from func(expanded args, expanded names kwargs).
  - Set \_cache at func at args\_key from return\_val.
  - Return return\_val.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request\_cache”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0465.json#L5725) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1574)

<a id="op-7615b3617fa481"></a>
### Site cache

`operation_foundation_utils_caching_business_behavior_site_cache`

**Inputs** ttl = no value, maxsize = no value.

**Declared result** Callable.

**Explicit results** time\_cache\_wrapper(ttl) · time\_cache\_wrapper.

**Local steps**

- Bind local operation time\_cache\_wrapper for subsequent calls.
- If callable(ttl).
  - Return time\_cache\_wrapper(ttl).
- Return time\_cache\_wrapper.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L76) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1575)

<a id="op-42dc17b1565300"></a>
### Site cache.time cache wrapper

`operation_foundation_utils_caching_business_behavior_site_cache_time_cache_wrapper`

**Inputs** func = no value.

**Declared result** Callable.

**Explicit results** site\_cache\_wrapper.

**Local steps**

- Bind local operation clear\_cache for subsequent calls.
- Set func.clear\_cache from clear\_cache.
- If (ttl is distinct from no value and not callable(ttl)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ttl is distinct from no value → not callable(ttl).
  - Set func.ttl from ttl.
  - Set func.expiration from (time.monotonic() + func.ttl).
- If (maxsize is distinct from no value and not callable(maxsize)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in maxsize is distinct from no value → not callable(maxsize).
  - Set func.maxsize from maxsize.
- Bind local operation site\_cache\_wrapper for subsequent calls.
- Return site\_cache\_wrapper.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L77) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1576)

<a id="op-035bee96559d68"></a>
### Site cache.time cache wrapper.clear cache

`operation_foundation_utils_caching_business_behavior_site_cache_time_cache_wrapper_clear_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate \_SITE\_CACHE at func.clear().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1577)

<a id="op-e4558dae706e1a"></a>
### Site cache.time cache wrapper.site cache wrapper

`operation_foundation_utils_caching_business_behavior_site_cache_time_cache_wrapper_site_cache_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** func(expanded args, expanded names kwargs) · function\_cache at arguments\_key · result.

**Local steps**

- Set site from getattr(Platform.local, “site”, no value).
- If not site.
  - Return func(expanded args, expanded names kwargs).
- Set arguments\_key from tuple(site, \_\_generate\_request\_cache\_key(args, kwargs)).
- If (hasattr(func, “ttl”) and time.monotonic() ≥ func.expiration).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(func, “ttl”) → time.monotonic() ≥ func.expiration.
  - Evaluate func.clear\_cache().
  - Set func.expiration from (time.monotonic() + func.ttl).
- Set function\_cache from \_SITE\_CACHE at func.
- Attempt the following.
  - Return function\_cache at arguments\_key.
- On failure (tuple(KeyError, RuntimeError)).
  - Take no action here.
- If (hasattr(func, “maxsize”) and len(function\_cache) ≥ func.maxsize).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(func, “maxsize”) → len(function\_cache) ≥ func.maxsize.
  - Within suppress(RuntimeError).
    - Evaluate function\_cache.pop(next(iter(function\_cache)), no value).
- Set result from func(expanded args, expanded names kwargs).
- Set function\_cache at arguments\_key from result.
- Return result.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “site”, no value) · clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L54) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1578)

<a id="op-f5e6fb345e8330"></a>
### Redis cache

`operation_foundation_utils_caching_business_behavior_cache_service_cache`

**Inputs** ttl = 3600, user = no value, shared = false.

**Declared result** Callable.

**Explicit results** wrapper(ttl) · wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- If callable(ttl).
  - Return wrapper(ttl).
- Return wrapper.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L72) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1564)
