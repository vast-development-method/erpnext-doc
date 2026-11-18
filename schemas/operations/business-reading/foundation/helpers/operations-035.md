# Shared value and file services · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Pluto

<a id="op-2f9b94086d855b"></a>
### Plutoprint can render

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutoprint_can_render`

**Inputs** html.

**Declared result** bool.

**Explicit results** false · not GRID.search(html).

**Local steps**

- If importlib.util.find\_spec(“plutoprint”) is identical to no value.
  - Return false.
- Set html from (html or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in html → empty text.
- If (“data-barcode-value=” belongs to html or USER\_SCRIPT.search(html)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “data-barcode-value=” belongs to html → USER\_SCRIPT.search(html).
  - Return false.
- Return not GRID.search(html).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L159) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L317)

<a id="op-607632428d0eb5"></a>
### Plutoprint blockers

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutoprint_blockers`

**Inputs** print\_format = no value.

**Declared result** list at str.

**Explicit results** blockers.

**Local steps**

- Set blockers from list().
- If importlib.util.find\_spec(“plutoprint”) is identical to no value.
  - Evaluate blockers.append(translated “PlutoPrint is not installed on this server”).
- If print\_format.
  - Set source from whitespace '\\n'.join(generator of cstr(print\_format.get(field)) for field drawn from tuple(“html”, “css”, “format\_data”)).
    - Draw field from tuple(“html”, “css”, “format\_data”).
  - If SCRIPT.search(JINJA\_TAG.sub(empty text, source)).
    - Evaluate blockers.append(translated “JavaScript”).
  - If GRID.search(source).
    - Evaluate blockers.append(translated “CSS grid”).
- Return blockers.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L158) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L316)

<a id="op-cf21bd22914405"></a>
### Pluto Browser.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_init`

**Inputs** self, print\_format, html, options.

**Local steps**

- Evaluate super().\_\_init\_\_(self, print\_format, html, options).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L135) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L293)

<a id="op-b38e89b4e8d295"></a>
### Pluto Browser.add browser

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_add_browser`

**Inputs** self, browser\_id.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L132) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L290)

<a id="op-4e8c2f2408ba4b"></a>
### Pluto Browser.remove browser

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_remove_browser`

**Inputs** self, browser\_id.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L138) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L296)

<a id="op-f530eb3a052b45"></a>
### Pluto Browser.open

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_open`

**Inputs** self, generator.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L137) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L295)

<a id="op-b6e7120802f983"></a>
### Pluto Browser.close

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_close`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L133) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L291)

<a id="op-1b082f50eea753"></a>
### Pluto Browser.detach debug browser

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_detach_debug_browser`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L134) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L292)

<a id="op-f0b15f5057f060"></a>
### Pluto Browser.new page

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_new_page`

**Inputs** self, page\_type.

**Explicit results** page.

**Local steps**

- If not hasattr(self, “fetcher”).
  - Set self.fetcher from local\_resource\_fetcher(bool(self.options.get(“block-external-requests”))).
- Set page from PlutoPage(page\_type, self.fetcher).
- Set page.is\_print\_designer from self.is\_print\_designer.
- Return page.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L136) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L294)

<a id="op-af3e0b36edfa11"></a>
### Pluto Browser.update header footer page

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutobrowser_update_header_footer_page`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.header\_page and not self.footer\_page).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.header\_page → not self.footer\_page.
  - Return no value.
- Set total\_pages from len(self.body\_pdf.pages).
- If (self.header\_page and self.is\_header\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.header\_page → self.is\_header\_dynamic.
  - Evaluate self.header\_page.repeat\_for\_pages(total\_pages).
- If (self.footer\_page and self.is\_footer\_dynamic).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.footer\_page → self.is\_footer\_dynamic.
  - Evaluate self.footer\_page.repeat\_for\_pages(total\_pages).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L139) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L297)

<a id="op-c0768d3bcc6aca"></a>
### Pluto Page.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_init`

**Inputs** self, page\_type, fetcher.

**Local steps**

- Set self.type from page\_type.
- Set self.fetcher from fetcher.
- Set self.options from mapping().
- Set self.html from empty text.
- Set self.viewport\_width from VIEWPORT\_WIDTH.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L148) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L306)

<a id="op-d8b1d7e135dee7"></a>
### Pluto Page.send

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_send`

**Inputs** self, method, params = no value.

**Explicit results** tuple(no value, no value).

**Local steps**

- Return tuple(no value, no value).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L151) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L309)

<a id="op-d1fd0b2aa4b630"></a>
### Pluto Page.set tab url

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_set_tab_url`

**Inputs** self, url.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L154) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L312)

<a id="op-717584ce2f87b4"></a>
### Pluto Page.wait for navigate

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_wait_for_navigate`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L155) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L313)

<a id="op-c12ac411787267"></a>
### Pluto Page.set content

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_set_content`

**Inputs** self, html, wait\_for = no value.

**Local steps**

- Set self.html from html.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L152) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L310)

<a id="op-56bae3ce4a2b14"></a>
### Pluto Page.wait for set content

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_wait_for_set_content`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L156) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L314)

<a id="op-f683afe4efbbd4"></a>
### Pluto Page.set device metrics

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_set_device_metrics`

**Inputs** self, width = VIEWPORT\_WIDTH, height = 720, scale\_factor = 1.

**Local steps**

- Set self.viewport\_width from width.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L153) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L311)

<a id="op-9248773f253d49"></a>
### Pluto Page.get content width

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_get_content_width`

**Inputs** self.

**Explicit results** self.\_book((self.viewport\_width × POINTS\_PER\_PX), no value).get\_document\_width().

**Local steps**

- Return self.\_book((self.viewport\_width × POINTS\_PER\_PX), no value).get\_document\_width().

**Methods declared on this owner** [book](operations-036.md#op-c1e65dba49da0d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L144) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L302)

<a id="op-7b29f980c33eba"></a>
### Pluto Page.get content height

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_get_content_height`

**Inputs** self.

**Explicit results** self.\_book((self.viewport\_width × POINTS\_PER\_PX), no value).get\_document\_height().

**Local steps**

- Update self.html using + formatted text &lt;style&gt;{MEASURE\_STYLE}&lt;/style&gt;.
- Return self.\_book((self.viewport\_width × POINTS\_PER\_PX), no value).get\_document\_height().

**Methods declared on this owner** [book](operations-036.md#op-c1e65dba49da0d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L143) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L301)

<a id="op-c45e500c5575de"></a>
### Pluto Page.get element height

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_get_element_height`

**Inputs** self, selector = “body”.

**Explicit results** math.ceil(book.get\_document\_height()).

**Local steps**

- Set book from self.\_book((self.viewport\_width × POINTS\_PER\_PX), no value, user\_style = MEASURE\_STYLE).
- Return math.ceil(book.get\_document\_height()).

**Methods declared on this owner** [book](operations-036.md#op-c1e65dba49da0d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L145) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L303)

<a id="op-d039cb1eb99318"></a>
### Pluto Page.repeat for pages

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_repeat_for_pages`

**Inputs** self, total\_pages.

**Explicit results** no value.

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(self.html, “html5lib”).
- If not template bound to soup.select\_one(“.wrapper”).
  - Return no value.
- Set now from now\_datetime().
- Set values from mapping(“topage” → total\_pages, “date” → format\_date(now), “isodate” → now.isoformat(), “time” → format\_time(now)).
- Set previous from template.
- For each page\_no in range(1, (total\_pages + 1)).
  - Set wrapper from template when page\_no equals 1, otherwise copy.copy(template).
    - Value choice on page\_no equals 1 — true gives template, false gives copy.copy(template).
  - For each tuple(class\_name, value) in mapping(expand values, “page” → page\_no).items().
    - For each element in wrapper.select(formatted text .{class\_name}).
      - Set element.string from cstr(value).
  - If page\_no &gt; 1.
    - Evaluate previous.insert\_after(wrapper).
    - Set previous from wrapper.
- Set self.html from str(soup).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L150) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L308)

<a id="op-bfb6aaa727730d"></a>
### Pluto Page.generate pdf

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_generate_pdf`

**Inputs** self, wait\_for\_pdf = true, raw = false.

**Explicit results** no value · pdf when raw, otherwise PdfReader(BytesIO(pdf)).

**Local steps**

- If not wait\_for\_pdf.
  - Return no value.
- Bind dependencies PdfReader.
- Set options from self.options.
- Set width from (options at “paperWidth” × POINTS\_PER\_INCH).
- Set height from (options at “paperHeight” × POINTS\_PER\_INCH).
- Set margins from list of (options.get(side, 0) × POINTS\_PER\_INCH) for side drawn from tuple(“marginTop”, “marginRight”, “marginBottom”, “marginLeft”).
  - Draw side from tuple(“marginTop”, “marginRight”, “marginBottom”, “marginLeft”).
- Set scale from (options.get(“scale”) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“scale”) → 1.
- Set book from self.\_layout(width, height, margins, scale).
- Set content\_width from ((width − margins at 1) − margins at 3).
- Set overflow from ((book.get\_document\_width() × POINTS\_PER\_PX) × scale).
- If overflow &gt; (content\_width + 1).
  - Update scale using × max((content\_width ÷ overflow), MAX\_SHRINK).
  - Remove book.
  - Set book from self.\_layout(width, height, margins, scale).
- If book.get\_page\_count() &gt; 1.
  - Remove book.
  - Set book from self.\_layout(width, height, margins, scale, …).
- Set pdf from self.\_write(book, width, height, scale).
- Return pdf when raw, otherwise PdfReader(BytesIO(pdf)).
  - Value choice on raw — true gives pdf, false gives PdfReader(BytesIO(pdf)).

**Methods declared on this owner** [layout](operations-036.md#op-92ef18ff082864), [write](operations-036.md#op-fdc567a4110722).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L142) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L300)

<a id="op-668af33cdfdd02"></a>
### Pluto Page.get pdf stream id

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_get_pdf_stream_id`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L147) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L305)

<a id="op-d171291a677195"></a>
### Pluto Page.get pdf from stream

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_get_pdf_from_stream`

**Inputs** self, stream\_id, raw = false.

**Explicit results** self.generate\_pdf(raw = raw).

**Local steps**

- Return self.generate\_pdf(raw = raw).

**Methods declared on this owner** [generate pdf](operations-035.md#op-bfb6aaa727730d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L146) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L304)
