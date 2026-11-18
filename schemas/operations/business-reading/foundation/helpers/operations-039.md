# Shared value and file services · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Print format generator

<a id="op-9b957aa64b0063"></a>
### Print Format Generator.page options

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_page_options`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() · options.

**Local steps**

- Bind dependencies convert\_uom.
- Set size from self.print\_settings.get(“pdf\_page\_size”).
- If not size.
  - Return mapping().
- Set options from mapping(“page-size” → size).
- If size equals “Custom”.
  - For each tuple(option, setting) in tuple(tuple(“page-height”, “pdf\_page\_height”), tuple(“page-width”, “pdf\_page\_width”)).
    - Set value from self.print\_settings.get(setting).
    - If value.
      - Set options at option from convert\_uom(value, “mm”, “px”, only\_number = true).
- Return options.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L181) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L339)

<a id="op-72d6c4834ea7dc"></a>
### Print Format Generator.render typst pdf

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_typst_portable_document`

**Inputs** self, password = no value.

**Explicit results** pdf.

**Explicit failure paths** validation helper — translated “This format can no longer render through Typst: {0}”.format(“, ”.join(blockers)).

**Local steps**

- Bind dependencies os.
- Bind dependencies tempfile.
- Bind dependencies typst.
- Bind dependencies encrypt\_pdf.
- Bind dependencies TypstEmitter, ensure\_typst\_fonts, letterhead\_blockers, typst\_blockers, typst\_fonts.
- Set blockers from typst\_blockers(self.print\_format, self.layout).
- If self.letterhead.
  - Set blockers from list(dict.fromkeys((blockers + letterhead\_blockers(nested operand in the contract.letterhead.as\_dict())))).
- If blockers.
  - Call the validation error handler Platform.throw(translated “This format can no longer render through Typst: {0}”.format(“, ”.join(blockers)), title = translated “Typst renderer unavailable”).
- Evaluate ensure\_typst\_fonts(self.print\_format.get(“font”)).
- Set emitter from TypstEmitter(self).
- Evaluate emitter.prepare().
- Set repeat from cint(self.print\_settings.get(“repeat\_header\_footer”)).
- Within tempfile.TemporaryDirectory() bound as tmp.
  - Bind local operation write for subsequent calls.
  - Bind dependencies json.
  - Set written from set().
  - Bind local operation write\_assets for subsequent calls.
  - Set heights from mapping(“pfhdr” → 0.0, “pfftr” → 0.0).
  - If (repeat and (emitter.header\_src or emitter.footer\_src)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in repeat → (emitter.header\_src or emitter.footer\_src).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in emitter.header\_src → emitter.footer\_src.
    - Evaluate write\_assets(emitter.assets).
    - Set measure\_path from write(“measure.typ”, emitter.measure\_source()).
    - For each label in list(heights).
      - Set found from json.loads(typst.query(measure\_path, formatted text &lt;{label}&gt;, root = tmp, font\_paths = typst\_fonts())).
      - If found.
        - Set heights at label from float((found at 0.get(“value”) or 0)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in found at 0.get(“value”) → 0.
  - Set tuple(source, assets) from emitter.emit(repeat\_header\_footer = repeat, header\_height\_pt = heights at “pfhdr”, footer\_height\_pt = heights at “pfftr”).
  - Set path from write(“main.typ”, source).
  - Evaluate write\_assets(assets).
  - Set pdf from typst.compile(path, root = tmp, font\_paths = typst\_fonts()).
- If password.
  - Set pdf from encrypt\_pdf(pdf, password).
- Return pdf.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L54) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L521)

<a id="op-d72eafae899414"></a>
### Print Format Generator.render typst pdf.write

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_typst_portable_document_write`

**Inputs** name, content, mode = “w”.

**Explicit results** path.

**Local steps**

- Set path from os.path.join(tmp, name).
- Within open(path, mode) bound as f.
  - Evaluate f.write(content).
- Return path.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L804) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L522)

<a id="op-740d03a667d885"></a>
### Print Format Generator.render typst pdf.write assets

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_typst_portable_document_write_assets`

**Inputs** assets.

**Local steps**

- For each tuple(name, data) in assets.items().
  - If name does not belong to written.
    - Evaluate written.add(name).
    - Evaluate write(name, data, “wb”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L954) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L523)

<a id="op-2528cb300f2f27"></a>
### Print Format Generator.build html for chrome

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_build_document_markup_for_chrome`

**Inputs** self.

**Explicit results** self.get\_main\_html().

**Local steps**

- Set self.context.for\_chrome from true.
- Set self.\_header\_absorbs\_top\_margin from false.
- Set self.context.repeat\_frame from false.
- Set repeat from self.print\_settings.repeat\_header\_footer.
- If repeat.
  - Set header from self.\_render\_overlay(“header”).
  - Set footer from self.\_render\_overlay(“footer”).
  - Set self.context.header from formatted text &lt;div id="header-html"&gt;{header}&lt;/div&gt; when header, otherwise empty text.
    - Value choice on header — true gives formatted text &lt;div id="header-html"&gt;{header}&lt;/div&gt;, false gives empty text.
  - Set self.context.footer from formatted text &lt;div id="footer-html"&gt;{footer}&lt;/div&gt; when footer, otherwise empty text.
    - Value choice on footer — true gives formatted text &lt;div id="footer-html"&gt;{footer}&lt;/div&gt;, false gives empty text.
  - Set self.context.chrome\_layout\_header from empty text.
  - Set self.context.chrome\_layout\_footer from empty text.
- Otherwise.
  - Set self.context.chrome\_layout\_header from (self.\_render\_overlay(“header”, with\_page\_no = false) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_render\_overlay(“header”, with\_page\_no = false) → empty text.
  - Set footer\_once from self.\_render\_overlay(“footer”, with\_page\_no = false).
  - Set self.context.chrome\_layout\_footer from formatted text &lt;div class="print-footer-once"&gt;{footer\_once}&lt;/div&gt; when footer\_once, otherwise empty text.
    - Value choice on footer\_once — true gives formatted text &lt;div class="print-footer-once"&gt;{footer\_once}&lt;/div&gt;, false gives empty text.
  - Set page\_no\_header from self.\_render\_page\_no\_overlay(“header”).
  - Set page\_no\_footer from self.\_render\_page\_no\_overlay(“footer”).
  - Set self.context.header from formatted text &lt;div id="header-html"&gt;{page\_no\_header}&lt;/div&gt; when page\_no\_header, otherwise empty text.
    - Value choice on page\_no\_header — true gives formatted text &lt;div id="header-html"&gt;{page\_no\_header}&lt;/div&gt;, false gives empty text.
  - Set self.context.footer from formatted text &lt;div id="footer-html"&gt;{page\_no\_footer}&lt;/div&gt; when page\_no\_footer, otherwise empty text.
    - Value choice on page\_no\_footer — true gives formatted text &lt;div id="footer-html"&gt;{page\_no\_footer}&lt;/div&gt;, false gives empty text.
- Return self.get\_main\_html().

**Methods declared on this owner** [render overlay](operations-039.md#op-b516dd1e6494a9), [render page no overlay](operations-039.md#op-ee5c6111226e23), [get main html](operations-038.md#op-9aa1c3c0bf2d22).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L42) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L498)

<a id="op-e7780b1e2b6c4c"></a>
### Print Format Generator.reserve top margin

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_reserve_top_margin`

**Inputs** self, html.

**Declared result** str.

**Explicit results** html · formatted text &lt;div style="padding-top:{top\_margin}mm"&gt;{html}&lt;/div&gt;.

**Local steps**

- Set top\_margin from float((self.print\_format.margin\_top or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.print\_format.margin\_top → 0.
- If not top\_margin.
  - Return html.
- Set self.\_header\_absorbs\_top\_margin from true.
- Return formatted text &lt;div style="padding-top:{top\_margin}mm"&gt;{html}&lt;/div&gt;.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0495.json#L3008) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L525)

<a id="op-ee5c6111226e23"></a>
### Print Format Generator.render page no overlay

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_page_number_overlay`

**Inputs** self, kind.

**Declared result** (str bitwise or no value).

**Explicit results** no value · page\_no\_html · (page\_no\_html + self.\_reserve\_top\_margin(empty text)).

**Local steps**

- Set is\_header from kind equals “header”.
- Set page\_pos from (nested operand in the contract.print\_format.page\_number or empty text).lower().replace(one space, “\_”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.print\_format.page\_number → empty text.
- Set valid\_positions from self.\_TOP\_POSITIONS when is\_header, otherwise self.\_BOTTOM\_POSITIONS.
  - Value choice on is\_header — true gives self.\_TOP\_POSITIONS, false gives self.\_BOTTOM\_POSITIONS.
- If page\_pos does not belong to valid\_positions.
  - Return no value.
- Set page\_no\_html from self.\_page\_number\_html(page\_pos).
- If not is\_header.
  - Return page\_no\_html.
- Return (page\_no\_html + self.\_reserve\_top\_margin(empty text)).

**Methods declared on this owner** [page number html](operations-039.md#op-e1f073425912c8), [reserve top margin](operations-039.md#op-e7780b1e2b6c4c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0495.json#L3176) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L519)

<a id="op-b516dd1e6494a9"></a>
### Print Format Generator.render overlay

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_overlay`

**Inputs** self, kind, with\_page\_no = true.

**Declared result** (str bitwise or no value).

**Explicit results** no value · (whitespace '\\n'.join(parts) or no value).

**Local steps**

- Set is\_header from kind equals “header”.
- Set page\_pos from (nested operand in the contract.print\_format.page\_number or empty text).lower().replace(one space, “\_”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.print\_format.page\_number → empty text.
- Set valid\_positions from self.\_TOP\_POSITIONS when is\_header, otherwise self.\_BOTTOM\_POSITIONS.
  - Value choice on is\_header — true gives self.\_TOP\_POSITIONS, false gives self.\_BOTTOM\_POSITIONS.
- Set wants\_page\_no from (with\_page\_no and page\_pos belongs to valid\_positions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in with\_page\_no → page\_pos belongs to valid\_positions.
- If is\_header.
  - Set letterhead\_html from (self.letterhead and self.letterhead.content).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.letterhead → self.letterhead.content.
  - Set layout\_template from self.layout.get(“header”) when self.layout, otherwise no value.
    - Value choice on self.layout — true gives self.layout.get(“header”), false gives no value.
- Otherwise.
  - Set letterhead\_html from (self.letterhead and self.letterhead.footer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.letterhead → self.letterhead.footer.
  - Set layout\_template from self.layout.get(“footer”) when self.layout, otherwise no value.
    - Value choice on self.layout — true gives self.layout.get(“footer”), false gives no value.
- If not (letterhead\_html or wants\_page\_no or layout\_template).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in letterhead\_html → wants\_page\_no → layout\_template.
  - Return no value.
- Set page\_no\_html from self.\_page\_number\_html(page\_pos) when wants\_page\_no, otherwise no value.
  - Value choice on wants\_page\_no — true gives self.\_page\_number\_html(page\_pos), false gives no value.
- Set ctx from mapping(“doc” → self.context.doc).
- Set parts from list().
- Set body\_parts from list().
- If (is\_header and page\_no\_html).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_header → page\_no\_html.
  - Evaluate parts.append(page\_no\_html).
- If letterhead\_html.
  - Evaluate body\_parts.append(((text in the contract + Platform.render\_template(letterhead\_html, ctx)) + “&lt;/div&gt;”)).
- If layout\_template.
  - Set zone\_class from “document-header-content” when is\_header, otherwise “document-footer-content”.
    - Value choice on is\_header — true gives “document-header-content”, false gives “document-footer-content”.
  - Set zone\_html from self.\_render\_zone\_section(layout\_template, ctx at “doc”, zone\_class).
  - If zone\_html.
    - Evaluate body\_parts.append(zone\_html).
- If (not is\_header and page\_no\_html).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_header → page\_no\_html.
  - Evaluate body\_parts.append(page\_no\_html).
- If (is\_header and page\_no\_html).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_header → page\_no\_html.
  - Set body\_parts from list(self.\_reserve\_top\_margin(whitespace '\\n'.join(body\_parts))).
- Evaluate parts.extend(body\_parts).
- Return (whitespace '\\n'.join(parts) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in whitespace '\\n'.join(parts) → no value.

**Methods declared on this owner** [page number html](operations-039.md#op-e1f073425912c8), [render zone section](operations-039.md#op-ba3758dd774cd3), [reserve top margin](operations-039.md#op-e7780b1e2b6c4c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L52) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L518)

<a id="op-ba3758dd774cd3"></a>
### Print Format Generator.render zone section

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_zone_section`

**Inputs** self, section, doc, zone\_class = empty text.

**Declared result** str.

**Explicit results** html.strip().

**Local steps**

- Set eval\_locals from condition\_locals(doc, self.print\_settings).
- For each column in section.get(“columns”, list()).
  - For each df in column.get(“fields”, list()).
    - If “renderer” does not belong to df.
      - Evaluate self.\_prepare\_field(df, section, eval\_locals).
- Set html from Platform.render\_template(self.\_ZONE\_SECTION\_TEMPLATE, mapping(“section” → section, “doc” → doc, “zone\_class” → zone\_class)).
- Return html.strip().

**Methods declared on this owner** [prepare field](operations-039.md#op-424d968d61e589).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L55) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L524)

<a id="op-e1f073425912c8"></a>
### Print Format Generator.page number html

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_page_number_document_markup`

**Inputs** self, position.

**Declared result** str.

**Explicit results** page\_number\_html(position).

**Local steps**

- Return page\_number\_html(position).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L49) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L513)

<a id="op-75ab5db727bdb9"></a>
### Print Format Generator.get layout

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_layout`

**Inputs** self, print\_format.

**Explicit results** self.get\_processed\_layout(create\_default\_layout(Platform.get\_meta(print\_format.doc\_type))) · self.get\_processed\_layout(layout).

**Explicit failure paths** validation helper — classic\_layout\_message().

**Local steps**

- If not print\_format.format\_data.
  - Bind dependencies create\_default\_layout.
  - Return self.get\_processed\_layout(create\_default\_layout(Platform.get\_meta(print\_format.doc\_type))).
- Attempt the following.
  - Set layout from (Platform.parse\_json(print\_format.format\_data) or copy.deepcopy(self.EMPTY\_LAYOUT)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(print\_format.format\_data) → copy.deepcopy(self.EMPTY\_LAYOUT).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = formatted text Unreadable print format layout: {print\_format.name}).
  - Set layout from copy.deepcopy(self.EMPTY\_LAYOUT).
- If isinstance(layout, list).
  - Call the validation error handler Platform.throw(classic\_layout\_message()).
- Return self.get\_processed\_layout(layout).

**Methods declared on this owner** [get processed layout](operations-039.md#op-ba753e4cae9998).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L44) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L504)

<a id="op-ba753e4cae9998"></a>
### Print Format Generator.get processed layout

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_processed_layout`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Set layout from self.normalise\_layout(layout).
- Set layout from self.apply\_permlevel\_access(layout).
- Set layout from self.set\_field\_renderers(layout).
- Set layout from self.prune\_table\_columns(layout).
- Set layout from self.process\_margin\_texts(layout).
- Return layout.

**Methods declared on this owner** [normalise layout](operations-039.md#op-d8860be8b2b69e), [apply permlevel access](operations-039.md#op-7f8da21ccffcee), [set field renderers](operations-039.md#op-c2c813a5fe1b13), [prune table columns](operations-039.md#op-541e0a54b756d1), [process margin texts](operations-040.md#op-0811ba1f0993d9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0495.json#L5189) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L507)

<a id="op-d8860be8b2b69e"></a>
### Print Format Generator.normalise layout

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_normalise_layout`

**Inputs** self, layout.

**Explicit results** copy.deepcopy(self.EMPTY\_LAYOUT) · layout.

**Local steps**

- If not isinstance(layout, dict).
  - Return copy.deepcopy(self.EMPTY\_LAYOUT).
- Bind local operation clean\_zone for subsequent calls.
- Bind local operation clean\_field for subsequent calls.
- Set sections from layout.get(“sections”).
- Set layout at “sections” from list of clean\_zone(s) for s drawn from sections where isinstance(s, dict) when isinstance(sections, list), otherwise list().
  - Value choice on isinstance(sections, list) — true gives list of clean\_zone(s) for s drawn from sections where isinstance(s, dict), false gives list().
  - Draw s from sections, keep a combination only if (isinstance(s, dict)).
- For each zone in tuple(“header”, “footer”).
  - Set layout at zone from clean\_zone(layout.get(zone)).
- Set layout at “background” from self.clean\_background(layout.get(“background”)).
- Return layout.

**Methods declared on this owner** [clean background](operations-039.md#op-2625392dee5f5c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L47) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L510)

<a id="op-8fd9a3db841625"></a>
### Print Format Generator.normalise layout.clean zone

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_normalise_layout_clean_zone`

**Inputs** zone.

**Explicit results** mapping(“columns” → list()) · cleaned.

**Local steps**

- If isinstance(zone, str).
  - Set zone from zone\_from\_html(zone).
- If not isinstance(zone, dict).
  - Return mapping(“columns” → list()).
- Set columns from list of mapping(expand col, “fields” → list of clean\_field(f) for f drawn from (col.get(“fields”) or list()) where isinstance(f, dict)) for col drawn from (zone.get(“columns”) or list()) where isinstance(col, dict).
  - Draw col from (zone.get(“columns”) or list()), keep a combination only if (isinstance(col, dict)).
  - Draw f from (col.get(“fields”) or list()), keep a combination only if (isinstance(f, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“fields”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in zone.get(“columns”) → list().
- Set cleaned from mapping(expand zone, “columns” → columns).
- If cleaned.get(“justify”) does not belong to self.JUSTIFY\_MODES.
  - Evaluate cleaned.pop(“justify”, no value).
- Return cleaned.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L48) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L512)

<a id="op-3d88363615edde"></a>
### Print Format Generator.normalise layout.clean field

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_normalise_layout_clean_field`

**Inputs** df.

**Explicit results** df · mapping(expand df, “table\_columns” → list of c for c drawn from table\_columns where isinstance(c, dict)).

**Local steps**

- If “table\_columns” does not belong to df.
  - Return df.
- Set table\_columns from df at “table\_columns”.
- If not isinstance(table\_columns, list).
  - Set table\_columns from list().
- Return mapping(expand df, “table\_columns” → list of c for c drawn from table\_columns where isinstance(c, dict)).
  - Draw c from table\_columns, keep a combination only if (isinstance(c, dict)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0495.json#L6646) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L511)

<a id="op-2625392dee5f5c"></a>
### Print Format Generator.clean background

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_clean_background`

**Inputs** background.

**Wrappers, in declaration order** staticmethod.

**Explicit results** no value · mapping(“image” → image, “url” → quote(image, safe = “:/?&amp;=%#”), “opacity” → 100 when opacity belongs to tuple(no value, empty text), otherwise max(0, min(100, cint(opacity)))).

**Local steps**

- If not isinstance(background, dict).
  - Return no value.
- Set image from background.get(“image”).
- If (not isinstance(image, str) or not BACKGROUND\_IMAGE\_URL.fullmatch(image)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(image, str) → not BACKGROUND\_IMAGE\_URL.fullmatch(image).
  - Return no value.
- Set opacity from background.get(“opacity”).
- Return mapping(“image” → image, “url” → quote(image, safe = “:/?&amp;=%#”), “opacity” → 100 when opacity belongs to tuple(no value, empty text), otherwise max(0, min(100, cint(opacity)))).
  - Value choice on opacity belongs to tuple(no value, empty text) — true gives 100, false gives max(0, min(100, cint(opacity))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L179) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L337)

<a id="op-30402c5f9751a4"></a>
### Print Format Generator.has field access

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_has_field_access`

**Inputs** doc, meta, fieldname, source\_fieldname = no value.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** true · doc.has\_permlevel\_access\_to(fieldname, df).

**Local steps**

- Set fieldname from (source\_fieldname or fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_fieldname → fieldname.
- If not fieldname.
  - Return true.
- Set df from meta.get\_field(fieldname).
- If (not df or not (df.permlevel or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → not (df.permlevel or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.permlevel → 0.
  - Return true.
- Return doc.has\_permlevel\_access\_to(fieldname, df).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L46) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L508)

<a id="op-7f8da21ccffcee"></a>
### Print Format Generator.apply permlevel access

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_apply_permission_level_access`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Set meta from self.doc.meta.
- For each column in iter\_layout\_columns(layout).
  - Set fields from list of df for df drawn from column.get(“fields”, list()) where self.has\_field\_access(self.doc, meta, df.get(“fieldname”), (df.get(“source\_fieldname”) or (nested operand in the contract.get(“fieldtype”) eq ….
    - Draw df from column.get(“fields”, list()), keep a combination only if (self.has\_field\_access(self.doc, meta, df.get(“fieldname”), (df.get(“source\_fieldname”) or (df.get(“fieldtype”) equals “Repeater” and df.get(“source”)) or (df.get(“custom”) and df.get(“barcode\_field”))))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“source\_fieldname”) → (df.get(“fieldtype”) equals “Repeater” and df.get(“source”)) → (df.get(“custom”) and df.get(“barcode\_field”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“fieldtype”) equals “Repeater” → df.get(“source”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“custom”) → df.get(“barcode\_field”).
  - Set column at “fields” from fields.
  - For each df in fields.
    - If df.get(“fieldtype”) equals “Repeater”.
      - Set rows from (self.doc.get(df.get(“source”)) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(df.get(“source”)) → list().
      - If not rows.
        - Continue with the next iteration or loop test.
      - Set tuple(child, child\_meta) from tuple(rows at 0, rows at 0.meta).
      - For each col in (df.get(“repeater\_columns”) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“repeater\_columns”) → list().
        - Set col at “template” from list of tok for tok drawn from (col.get(“template”) or list()) where not (isinstance(tok, dict) and tok.get(“t”) equals “f” and not self.has\_field\_access(child, child\_meta, nested operand in the contract.get(“v”))).
          - Draw tok from (col.get(“template”) or list()), keep a combination only if (not (isinstance(tok, dict) and tok.get(“t”) equals “f” and not self.has\_field\_access(child, child\_meta, tok.get(“v”)))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“template”) → list().
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(tok, dict) → tok.get(“t”) equals “f” → not self.has\_field\_access(child, child\_meta, tok.get(“v”)).
      - Continue with the next iteration or loop test.
    - If (df.get(“fieldtype”) differs from “Table” or not df.get(“table\_columns”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“fieldtype”) differs from “Table” → not df.get(“table\_columns”).
      - Continue with the next iteration or loop test.
    - Set rows from (self.doc.get(df.get(“fieldname”)) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(df.get(“fieldname”)) → list().
    - If not rows.
      - Continue with the next iteration or loop test.
    - Set tuple(child, child\_meta) from tuple(rows at 0, rows at 0.meta).
    - Set df at “table\_columns” from list of col for col drawn from df at “table\_columns” where self.has\_field\_access(child, child\_meta, col.get(“fieldname”)).
      - Draw col from df at “table\_columns”, keep a combination only if (self.has\_field\_access(child, child\_meta, col.get(“fieldname”))).
    - For each col in df at “table\_columns”.
      - If col.get(“merged\_fields”).
        - Set col at “merged\_fields” from list of mf for mf drawn from col at “merged\_fields” where self.has\_field\_access(child, child\_meta, mf.get(“fieldname”)).
          - Draw mf from col at “merged\_fields”, keep a combination only if (self.has\_field\_access(child, child\_meta, mf.get(“fieldname”))).
- Return layout.

**Methods declared on this owner** [has field access](operations-039.md#op-30402c5f9751a4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L40) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L496)

<a id="op-541e0a54b756d1"></a>
### Print Format Generator.prune table columns

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_prune_table_columns`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Bind dependencies column\_has\_value.
- Set eval\_locals from condition\_locals(self.doc, self.print\_settings).
- For each column in iter\_layout\_columns(layout).
  - For each df in column.get(“fields”, list()).
    - If (df.get(“fieldtype”) differs from “Table” or not df.get(“table\_columns”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“fieldtype”) differs from “Table” → not df.get(“table\_columns”).
      - Continue with the next iteration or loop test.
    - Set rows from df.get(“\_rows”) when df.get(“\_rows”) is distinct from no value, otherwise self.doc.get(df.get(“fieldname”)).
      - Value choice on df.get(“\_rows”) is distinct from no value — true gives df.get(“\_rows”), false gives self.doc.get(df.get(“fieldname”)).
    - Set rows from (rows or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().
    - Set kept from list().
    - For each col in df at “table\_columns”.
      - If not self.column\_condition\_met(col, eval\_locals).
        - Continue with the next iteration or loop test.
      - If (rows and col.get(“fieldname”) differs from “idx” and not column\_has\_value(rows, col.get(“fieldname”), Platform.\_dict(col))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in rows → col.get(“fieldname”) differs from “idx” → not column\_has\_value(rows, col.get(“fieldname”), Platform.\_dict(col)).
        - Continue with the next iteration or loop test.
      - Evaluate kept.append(col).
    - Set total from sum(generator of (col.get(“width”) or 0) for col drawn from kept).
      - Draw col from kept.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“width”) → 0.
    - If total.
      - For each col in kept.
        - If col.get(“width”).
          - Set col at “width” from round(((col at “width” ÷ total) × 100), 2).
    - Set df at “table\_columns” from kept.
- Return layout.

**Methods declared on this owner** [column condition met](operations-039.md#op-e8a0cc98f7e4ae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L51) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L517)

<a id="op-4ad954f56104f9"></a>
### Print Format Generator.eval condition

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_evaluate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, condition, eval\_locals, where.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0496.json#L1917) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L500)

<a id="op-e8a0cc98f7e4ae"></a>
### Print Format Generator.column condition met

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_column_condition_met`

**Inputs** self, col, eval\_locals.

**Explicit results** true · self.eval\_condition(condition, eval\_locals, formatted text column {(col.get(“label”) or col.get(“fieldname”))}).

**Local steps**

- Set condition from col.get(“column\_condition”).
- If not condition.
  - Return true.
- Return self.eval\_condition(condition, eval\_locals, formatted text column {(col.get(“label”) or col.get(“fieldname”))}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“label”) → col.get(“fieldname”).

**Methods declared on this owner** [eval condition](operations-039.md#op-4ad954f56104f9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0496.json#L2218) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L499)

<a id="op-424d968d61e589"></a>
### Print Format Generator.prepare field

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_prepare_field`

**Inputs** self, df, section, eval\_locals.

**Local steps**

- If df.get(“visible\_if”).
  - Set df at “\_hidden” from not self.eval\_condition(df at “visible\_if”, eval\_locals, formatted text field {(df.get(“label”) or df.get(“fieldname”))}).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“label”) → df.get(“fieldname”).
- Set fieldtype from df.get(“fieldtype”, “Data”).
- Set df at “renderer” from (self.\_FIELD\_RENDERERS.get(fieldtype) or fieldtype.replace(one space, empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_FIELD\_RENDERERS.get(fieldtype) → fieldtype.replace(one space, empty text).
- Set df at “section” from section.
- Evaluate self.prepare\_barcode(df).
- Evaluate self.prepare\_linked\_field(df).
- Evaluate self.prepare\_date\_format(df).
- Evaluate self.filter\_conditional\_rows(df).
- Evaluate self.prepare\_html(df).

If control reaches the end, it returns no value.

**Methods declared on this owner** [eval condition](operations-039.md#op-4ad954f56104f9), [prepare barcode](operations-040.md#op-c959c8ca2ce695), [prepare linked field](operations-040.md#op-cd8ee94dd049a8), [prepare date format](operations-040.md#op-061d934a2e963f), [filter conditional rows](operations-039.md#op-8067c877fb3539), [prepare html](operations-040.md#op-84967f5f16c158).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L50) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L515)

<a id="op-c2c813a5fe1b13"></a>
### Print Format Generator.set field renderers

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_set_field_renderers`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Set eval\_locals from condition\_locals(self.doc, self.print\_settings).
- For each section in layout at “sections”.
  - If section.get(“visible\_if”).
    - Set section at “\_hidden” from not self.eval\_condition(section at “visible\_if”, eval\_locals, formatted text section {(section.get(“label”) or empty text)}).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“label”) → empty text.
- For each tuple(\_where, zone) in iter\_zones(layout).
  - For each df in iter\_fields(zone).
    - Evaluate self.\_prepare\_field(df, zone, eval\_locals).
- Return layout.

**Methods declared on this owner** [eval condition](operations-039.md#op-4ad954f56104f9), [prepare field](operations-039.md#op-424d968d61e589).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L56) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L526)

<a id="op-8067c877fb3539"></a>
### Print Format Generator.filter conditional rows

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_filter_conditional_rows`

**Inputs** self, df.

**Explicit results** no value.

**Local steps**

- Set fieldtype from df.get(“fieldtype”).
- If fieldtype equals “Repeater”.
  - Set source from df.get(“source”).
- Otherwise.
  - If fieldtype equals “Table”.
    - Set source from df.get(“fieldname”).
  - Otherwise.
    - Return no value.
- If (not df.get(“row\_condition”) or not source).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df.get(“row\_condition”) → not source.
  - Return no value.
- Set condition from df at “row\_condition”.
- Set eval\_locals from condition\_locals(self.doc, self.print\_settings).
- Set kept from list().
- For each row in (self.doc.get(source) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(source) → list().
  - If self.eval\_condition(condition, mapping(expand eval\_locals, “row” → row.as\_dict()), formatted text rows of {source}).
    - Evaluate kept.append(row).
- Set df at “\_rows” from kept.

If control reaches the end, it returns no value.

**Methods declared on this owner** [eval condition](operations-039.md#op-4ad954f56104f9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L43) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L501)
