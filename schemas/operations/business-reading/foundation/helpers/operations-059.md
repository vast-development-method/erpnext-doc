# Shared value and file services · operations 59

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Verified command

<a id="op-f0798532a91548"></a>
### Get url using doc

`operation_foundation_utils_verified_command_business_behavior_get_resource_address_using_record`

**Inputs** doc, cmd.

**Explicit results** get\_url(cmd, params, doc.get\_nonce()).

**Local steps**

- Set params from doc.get\_signature\_params().
- Return get\_url(cmd, params, doc.get\_nonce()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3215) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1056)

## Service · Weasyprint

<a id="op-cd0e4eab7fb8ea"></a>
### Warn deprecated

`operation_foundation_binding_foundation_utils_weasyprint_warn_deprecated`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Use module bindings \_deprecation\_warned.
- If \_deprecation\_warned.
  - Return no value.
- Set \_deprecation\_warned from true.
- Evaluate warnings.warn(DEPRECATION\_MESSAGE, DeprecationWarning, stacklevel = 3).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L61) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L454)

<a id="op-7e181e8bcc9ac1"></a>
### Legacy generator

`operation_foundation_binding_foundation_utils_weasyprint_legacy_generator`

**Inputs** print\_format, doc, letterhead = no value.

**Declared result** PrintFormatGenerator.

**Explicit results** weasyprint\_legacy.PrintFormatGenerator(print\_format, doc, letterhead).

**Local steps**

- Evaluate warn\_deprecated().
- Return weasyprint\_legacy.PrintFormatGenerator(print\_format, doc, letterhead).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L39) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L432)

<a id="op-9117a069d8d9f6"></a>
### Print format doc

`operation_foundation_binding_foundation_utils_weasyprint_print_format_doc`

**Inputs** print\_format.

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Explicit results** Platform.get\_doc(“Print Format”, print\_format) · print\_format.

**Local steps**

- If isinstance(print\_format, str).
  - Return Platform.get\_doc(“Print Format”, print\_format).
- Return print\_format.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L60) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L453)

<a id="op-22fad8f7229826"></a>
### Download pdf

`operation_foundation_binding_foundation_utils_weasyprint_download_pdf`

**Inputs** doctype, name, print\_format, letterhead = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** download\_generator\_pdf(doctype, name, print\_format, letterhead).

**Local steps**

- Bind dependencies download\_generator\_pdf.
- Return download\_generator\_pdf(doctype, name, print\_format, letterhead).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L34) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L427)

<a id="op-a6d466eac2e1bc"></a>
### Get html

`operation_foundation_binding_foundation_utils_weasyprint_get_html`

**Inputs** doctype, name, print\_format, letterhead = no value.

**Explicit results** weasyprint\_legacy.get\_html(doctype, name, print\_format, letterhead) · get\_generator\_html(doctype, name, print\_format, letterhead).

**Local steps**

- Set print\_format from \_print\_format\_doc(print\_format).
- If uses\_legacy\_weasyprint(print\_format).
  - Evaluate warn\_deprecated().
  - Return weasyprint\_legacy.get\_html(doctype, name, print\_format, letterhead).
- Bind dependencies get\_generator\_html.
- Return get\_generator\_html(doctype, name, print\_format, letterhead).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L35) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L428)

<a id="op-9cc652cc3de7da"></a>
### Legacy generator from print context

`operation_foundation_binding_foundation_utils_weasyprint_legacy_generator_from_print_context`

**Inputs** print\_format.

**Declared result** (PrintFormatGenerator bitwise or no value).

**Record and data access** resolve a document from ctx.doctype via get\_doc.

**Explicit results** no value · legacy\_generator(pf, doc, letterhead).

**Local steps**

- Bind dependencies Document.
- Bind dependencies get\_print\_context.
- Set ctx from get\_print\_context().
- If ctx is identical to no value.
  - Set ctx from Platform.\_dict(Platform.form\_dict).
- If (not print\_format or not ctx.get(“doctype”) or not ctx.get(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → not ctx.get(“doctype”) → not ctx.get(“name”).
  - Return no value.
- Set pf from \_print\_format\_doc(print\_format).
- If not uses\_legacy\_weasyprint(pf).
  - Return no value.
- Set doc from ctx.get(“doc”).
- If not isinstance(doc, Document).
  - Set doc from Platform.get\_doc(ctx.doctype, ctx.name).
- Set letterhead from no value when Platform.utils.cint(ctx.get(“no\_letterhead”)), otherwise ctx.get(“letterhead”).
  - Value choice on Platform.utils.cint(ctx.get(“no\_letterhead”)) — true gives no value, false gives ctx.get(“letterhead”).
- Return legacy\_generator(pf, doc, letterhead).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L40) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L433)

<a id="op-80da604d5b6984"></a>
### Get weasyprint pdf

`operation_foundation_binding_foundation_utils_weasyprint_get_weasyprint_pdf`

**Inputs** print\_format, html, options, output, pdf\_generator = no value.

**Explicit results** no value · output · pdf.

**Local steps**

- If pdf\_generator differs from “WeasyPrint”.
  - Return no value.
- Set generator from legacy\_generator\_from\_print\_context(print\_format).
- If generator is identical to no value.
  - Return no value.
- Set pdf from generator.render\_pdf(password = (options or mapping()).get(“password”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → mapping().
- If output.
  - Bind dependencies PdfReader.
  - For each page in PdfReader(BytesIO(pdf)).pages.
    - Evaluate output.add\_page(page).
  - Return output.
- Return pdf.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L36) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L429)

## Service · Weasyprint legacy

<a id="op-06ad995b3739cb"></a>
### Legacy blockers

`operation_foundation_binding_foundation_utils_weasyprint_legacy_legacy_blockers`

**Inputs** print\_format, layout.

**Declared result** list at str.

**Record and data access** read “Letter Head” via get\_value.

**Explicit results** list(translated “Custom HTML format”) · list(translated “Not made in the Print Format Editor”) · blockers.

**Local steps**

- Bind dependencies iter\_nodes.
- If print\_format.get(“custom\_format”).
  - Return list(translated “Custom HTML format”).
- If not print\_format.get(“print\_format\_builder\_beta”).
  - Return list(translated “Not made in the Print Format Editor”).
- Set blockers from list().
- Bind local operation add for subsequent calls.
- If not isinstance(layout, dict).
  - Return blockers.
- Set letter\_head from layout.get(“letter\_head”).
- If (letter\_head and (nested operand in the contract.db.get\_value(“Letter Head”, letter\_head, “custom\_css”) or empty text).strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in letter\_head → (Platform.db.get\_value(“Letter Head”, letter\_head, “custom\_css”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Letter Head”, letter\_head, “custom\_css”) → empty text.
  - Evaluate add(translated “Letterhead with custom CSS”).
- Set styled\_fields from list().
- For each tuple(\_where, node) in iter\_nodes(layout).
  - Set fieldtype from node.get(“fieldtype”).
  - If (node.get(“condition”) or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“condition”) → empty text.
    - Evaluate add(translated “Visibility conditions”).
  - If not fieldtype.
    - If any(generator of node.get(key) for key drawn from SECTION\_STYLE\_KEYS).
      - Draw key from SECTION\_STYLE\_KEYS.
      - Evaluate add(translated “Section background, padding, radius or custom CSS”).
    - Continue with the next iteration or loop test.
  - If (fieldtype belongs to UNSUPPORTED\_FIELDTYPES and (fieldtype differs from “Image” or node.get(“custom”) or node.get(“image\_url”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype belongs to UNSUPPORTED\_FIELDTYPES → (fieldtype differs from “Image” or node.get(“custom”) or node.get(“image\_url”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldtype differs from “Image” → node.get(“custom”) → node.get(“image\_url”).
    - Evaluate add(translated “{0} block”.format(translated fieldtype)).
  - If (node.get(“custom\_style”) or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“custom\_style”) → empty text.
    - Evaluate styled\_fields.append((node.get(“label”) or node.get(“fieldname”) or “?”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“label”) → node.get(“fieldname”) → “?”.
  - If fieldtype equals “Table”.
    - If (node.get(“table\_bordered”) is identical to false or node.get(“table\_style”) does not belong to tuple(no value, empty text, “lined”) or node.get(“table\_header”) equals “plain” or any(generator of node.get( ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“table\_bordered”) is identical to false → node.get(“table\_style”) does not belong to tuple(no value, empty text, “lined”) → node.get(“table\_header”) equals “plain” → any(generator of node.get(key) for key drawn from TABLE\_STYLE\_KEYS).
      - Draw key from TABLE\_STYLE\_KEYS.
      - Evaluate add(translated “Table styling”).
    - For each col in (node.get(“table\_columns”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“table\_columns”) → list().
      - If not isinstance(col, dict).
        - Continue with the next iteration or loop test.
      - If col.get(“merged\_fields”).
        - Evaluate add(translated “Merged table columns”).
      - If (col.get(“column\_condition”) or empty text).strip().
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“column\_condition”) → empty text.
        - Evaluate add(translated “Table column conditions”).
- If styled\_fields.
  - Set shown from “, ”.join(styled\_fields at slice no value to 4).
  - Evaluate add(translated “Custom CSS on fields: {0}”.format(translated “{0} and {1} more”.format(shown, (len(styled\_fields) − 4)) when len(styled\_fields) &gt; 4, otherwise shown)).
    - Value choice on len(styled\_fields) &gt; 4 — true gives translated “{0} and {1} more”.format(shown, (len(styled\_fields) − 4)), false gives shown.
- Return blockers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L43) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L436)

<a id="op-bce22f0b779187"></a>
### Legacy blockers.add

`operation_foundation_binding_foundation_utils_weasyprint_legacy_legacy_blockers_add`

**Inputs** reason.

**Local steps**

- If reason does not belong to blockers.
  - Evaluate blockers.append(reason).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L44) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L437)

<a id="op-abf3acd86f1db0"></a>
### Download pdf

`operation_foundation_binding_foundation_utils_weasyprint_legacy_download_pdf`

**Inputs** doctype, name, print\_format, letterhead = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“print”).
- Set generator from PrintFormatGenerator(print\_format, doc, letterhead).
- Set pdf from generator.render\_pdf().
- Set Platform.local.response.filename from “{name}.pdf”.format(name = name.replace(one space, “-”).replace(“/”, “-”)).
- Set Platform.local.response.filecontent from pdf.
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“print”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L37) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L430)

<a id="op-22f09977b9c1f4"></a>
### Get html

`operation_foundation_binding_foundation_utils_weasyprint_legacy_get_html`

**Inputs** doctype, name, print\_format, letterhead = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** generator.get\_html\_preview().

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“print”).
- Set generator from PrintFormatGenerator(print\_format, doc, letterhead).
- Return generator.get\_html\_preview().

**Values supplied outside this operation** effective access from doc.check\_permission(“print”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L41) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L434)

<a id="op-4573b210d5907c"></a>
### Unwrap zone

`operation_foundation_binding_foundation_utils_weasyprint_legacy_unwrap_zone`

**Inputs** zone.

**Explicit results** zone · empty text · (fields at 0.get(“html”) or empty text).

**Local steps**

- If not isinstance(zone, dict).
  - Return zone.
- Set fields from list of f for col drawn from (zone.get(“columns”) or list()), then f drawn from (col.get(“fields”) or list()).
  - Draw col from (zone.get(“columns”) or list()).
  - Draw f from (col.get(“fields”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in zone.get(“columns”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“fields”) → list().
- If not fields.
  - Return empty text.
- If (len(fields) equals 1 and fields at 0.get(“fieldtype”) equals “HTML” and fields at 0.get(“fieldname”) equals ZONE\_HTML\_FIELDNAME).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fields) equals 1 → fields at 0.get(“fieldtype”) equals “HTML” → fields at 0.get(“fieldname”) equals ZONE\_HTML\_FIELDNAME.
  - Return (fields at 0.get(“html”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields at 0.get(“html”) → empty text.
- Return zone.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L59) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L452)

<a id="op-38afc703ad3618"></a>
### Print Format Generator.initialize

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_init`

**Inputs** self, print\_format, doc, letterhead = no value.

**Record and data access** resolve a document from “Print Format” via get\_doc · resolve a document from “Letter Head” via get\_doc.

**Local steps**

- Set self.base\_url from Platform.utils.get\_url().
- Set self.print\_format from print\_format when not isinstance(print\_format, str), otherwise Platform.get\_doc(“Print Format”, print\_format).
  - Value choice on not isinstance(print\_format, str) — true gives print\_format, false gives Platform.get\_doc(“Print Format”, print\_format).
- Set self.doc from doc.
- If letterhead equals translated “No Letterhead”.
  - Set letterhead from no value.
- Set self.letterhead from Platform.get\_doc(“Letter Head”, letterhead) when letterhead, otherwise no value.
  - Value choice on letterhead — true gives Platform.get\_doc(“Letter Head”, letterhead), false gives no value.
- Evaluate self.build\_context().
- Set self.layout from self.get\_layout(self.print\_format).
- Set self.context.layout from self.layout.

If control reaches the end, it returns no value.

**Methods declared on this owner** [build context](operations-059.md#op-257b6e9cb99a24), [get layout](operations-059.md#op-e8e53d19b0fdcb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L53) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L446)

<a id="op-257b6e9cb99a24"></a>
### Print Format Generator.build context

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_build_context`

**Inputs** self.

**Record and data access** resolve a document from “Print Settings” via get\_doc · resolve a document from “Print Style” via get\_doc.

**Local steps**

- Set self.print\_settings from Platform.get\_doc(“Print Settings”).
- Set page\_width\_map from mapping(“A4” → 210, “Letter” → 216).
- Set page\_size from no value.
- If self.print\_settings.pdf\_page\_size equals “Custom”.
  - Set page\_width from (Platform.utils.flt(self.print\_settings.pdf\_page\_width) or 210).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.flt(self.print\_settings.pdf\_page\_width) → 210.
  - Set page\_height from (Platform.utils.flt(self.print\_settings.pdf\_page\_height) or 297).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.flt(self.print\_settings.pdf\_page\_height) → 297.
  - Set page\_size from formatted text {page\_width}mm {page\_height}mm.
- Otherwise.
  - Set page\_width from (page\_width\_map.get(self.print\_settings.pdf\_page\_size) or 210).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_width\_map.get(self.print\_settings.pdf\_page\_size) → 210.
- Set body\_width from ((page\_width − self.print\_format.margin\_left) − self.print\_format.margin\_right).
- Set print\_style from Platform.get\_doc(“Print Style”, self.print\_settings.print\_style) when self.print\_settings.print\_style, otherwise no value.
  - Value choice on self.print\_settings.print\_style — true gives Platform.get\_doc(“Print Style”, self.print\_settings.print\_style), false gives no value.
- Set context from Platform.\_dict(mapping(“doc” → self.doc, “print\_format” → self.print\_format, “print\_settings” → self.print\_settings, “print\_style” → print\_style, …)).
- Set self.context from context.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L46) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L439)

<a id="op-cd80b5c8c5f206"></a>
### Print Format Generator.get html preview

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_get_html_preview`

**Inputs** self.

**Explicit results** self.get\_main\_html().

**Local steps**

- Set tuple(header\_html, footer\_html) from self.get\_header\_footer\_html().
- Set self.context.header from header\_html.
- Set self.context.footer from footer\_html.
- Return self.get\_main\_html().

**Methods declared on this owner** [get header footer html](operations-059.md#op-ab37e4fcad0f9f), [get main html](operations-059.md#op-a3393e35645f6f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L50) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L443)

<a id="op-a3393e35645f6f"></a>
### Print Format Generator.get main html

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_get_main_html`

**Inputs** self.

**Explicit results** Platform.render\_template(formatted text {TEMPLATE\_DIR}/print\_format.html, self.context).

**Local steps**

- Set self.context.css from Platform.render\_template(formatted text {TEMPLATE\_DIR}/print\_format.css, self.context).
- Return Platform.render\_template(formatted text {TEMPLATE\_DIR}/print\_format.html, self.context).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L52) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L445)

<a id="op-ab37e4fcad0f9f"></a>
### Print Format Generator.get header footer html

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_get_header_footer_html`

**Inputs** self.

**Explicit results** tuple(header\_html, footer\_html).

**Local steps**

- Set header\_html, footer\_html from no value.
- If (self.letterhead or self.layout.get(“header”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.letterhead → self.layout.get(“header”).
  - Set header\_html from Platform.render\_template(formatted text {TEMPLATE\_DIR}/print\_header.html, self.context).
- If (self.letterhead or self.layout.get(“footer”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.letterhead → self.layout.get(“footer”).
  - Set footer\_html from Platform.render\_template(formatted text {TEMPLATE\_DIR}/print\_footer.html, self.context).
- Return tuple(header\_html, footer\_html).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L49) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L442)

<a id="op-5e3870a0a6416b"></a>
### Print Format Generator.render pdf

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_render_pdf`

**Inputs** self, password = no value.

**Explicit results** pdf.

**Local steps**

- Set tuple(HTML, \_CSS) from import\_weasyprint().
- Evaluate self.\_make\_header\_footer().
- Evaluate self.context.update(mapping(“header\_height” → self.header\_height, “footer\_height” → self.footer\_height)).
- Set main\_html from self.get\_main\_html().
- Set html from HTML(string = main\_html, base\_url = self.base\_url).
- Set main\_doc from html.render().
- If (self.header\_html or self.footer\_html).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.header\_html → self.footer\_html.
  - Evaluate self.\_apply\_overlay\_on\_main(main\_doc, self.header\_body, self.footer\_body).
- Set pdf from main\_doc.write\_pdf().
- If password.
  - Set pdf from encrypt\_pdf(pdf, password).
- Return pdf.

**Methods declared on this owner** [make header footer](operations-059.md#op-d6e205c2647d36), [get main html](operations-059.md#op-a3393e35645f6f), [apply overlay on main](operations-059.md#op-33507881f59717).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L57) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L450)

<a id="op-6e835da529f881"></a>
### Print Format Generator.compute overlay element

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_compute_overlay_element`

**Inputs** self, element.

**Explicit results** tuple(element\_body, element\_height).

**Local steps**

- Set tuple(HTML, CSS) from import\_weasyprint().
- Set html from HTML(string = getattr(self, formatted text {element}\_html), base\_url = self.base\_url).
- Set element\_doc from html.render(stylesheets = list(CSS(string = “@page {size: A4 portrait; margin: 0;}”))).
- Set element\_page from element\_doc.pages at 0.
- Set element\_body from PrintFormatGenerator.get\_element(element\_page.\_page\_box.all\_children(), “body”).
- Set element\_body from element\_body.copy\_with\_children(element\_body.all\_children()).
- Set element\_html from PrintFormatGenerator.get\_element(element\_page.\_page\_box.all\_children(), element).
- If element equals “header”.
  - Set element\_height from element\_html.height.
- If element equals “footer”.
  - Set element\_height from (element\_page.height − element\_html.position\_y).
- Return tuple(element\_body, element\_height).

**Values supplied outside this operation** selected callable from getattr(self, formatted text {element}\_html).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L47) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L440)

<a id="op-33507881f59717"></a>
### Print Format Generator.apply overlay on main

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_apply_overlay_on_main`

**Inputs** self, main\_doc, header\_body = no value, footer\_body = no value.

**Local steps**

- For each page in main\_doc.pages.
  - Set page\_body from PrintFormatGenerator.get\_element(page.\_page\_box.all\_children(), “body”).
  - If header\_body.
    - Update page\_body.children using + header\_body.all\_children().
  - If footer\_body.
    - Update page\_body.children using + footer\_body.all\_children().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L45) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L438)

<a id="op-d6e205c2647d36"></a>
### Print Format Generator.make header footer

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_make_header_footer`

**Inputs** self.

**Local steps**

- Set tuple(self.header\_html, self.footer\_html) from self.get\_header\_footer\_html().
- If self.header\_html.
  - Set tuple(header\_body, header\_height) from self.\_compute\_overlay\_element(“header”).
- Otherwise.
  - Set tuple(header\_body, header\_height) from tuple(no value, 0).
- If self.footer\_html.
  - Set tuple(footer\_body, footer\_height) from self.\_compute\_overlay\_element(“footer”).
- Otherwise.
  - Set tuple(footer\_body, footer\_height) from tuple(no value, 0).
- Set self.header\_body from header\_body.
- Set self.header\_height from header\_height.
- Set self.footer\_body from footer\_body.
- Set self.footer\_height from footer\_height.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get header footer html](operations-059.md#op-ab37e4fcad0f9f), [compute overlay element](operations-059.md#op-6e835da529f881).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L54) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L447)

<a id="op-e8e53d19b0fdcb"></a>
### Print Format Generator.get layout

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_get_layout`

**Inputs** self, print\_format.

**Explicit results** layout.

**Local steps**

- Set layout from Platform.parse\_json(print\_format.format\_data).
- Set layout from self.set\_field\_renderers(layout).
- Set layout from self.process\_margin\_texts(layout).
- Set layout from self.process\_zones(layout).
- Return layout.

**Methods declared on this owner** [set field renderers](operations-059.md#op-03052198a1d4b8), [process margin texts](operations-060.md#op-787ce2fb81d2b6), [process zones](operations-060.md#op-fc12226d51297a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L51) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L444)

<a id="op-03052198a1d4b8"></a>
### Print Format Generator.set field renderers

`operation_foundation_binding_foundation_utils_weasyprint_legacy_printformatgenerator_set_field_renderers`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- Set renderers from mapping(“HTML Editor” → “HTML”, “Markdown Editor” → “Markdown”).
- For each section in layout at “sections”.
  - For each column in section at “columns”.
    - For each df in column at “fields”.
      - Set fieldtype from df at “fieldtype”.
      - Set renderer\_name from fieldtype.replace(one space, empty text).
      - Set df at “renderer” from (renderers.get(fieldtype) or renderer\_name).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in renderers.get(fieldtype) → renderer\_name.
      - Set df at “section” from section.
- Return layout.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L58) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L451)
