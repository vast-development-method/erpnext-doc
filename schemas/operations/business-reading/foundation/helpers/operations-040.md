# Shared value and file services · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Print format generator

<a id="op-84967f5f16c158"></a>
### Print Format Generator.prepare html

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_prepare_html`

**Inputs** self, df.

**Local steps**

- If (df.get(“renderer”) equals “HTML” and not df.get(“\_hidden”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“renderer”) equals “HTML” → not df.get(“\_hidden”).
  - Set rendered from Platform.render\_template((df.get(“html”) or empty text), mapping(“doc” → self.doc)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“html”) → empty text.
  - Set df at “\_html” from BeautifulSoup(formatted text &lt;body&gt;{rendered}&lt;/body&gt;, “html5lib”).body.decode\_contents().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L183) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L341)

<a id="op-c959c8ca2ce695"></a>
### Print Format Generator.prepare barcode

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_prepare_barcode`

**Inputs** self, df.

**Explicit results** no value.

**Local steps**

- If df.get(“fieldtype”) differs from “Barcode”.
  - Return no value.
- If not df.get(“custom”).
  - Set meta\_df from Platform.get\_meta(self.doc.doctype).get\_field(df.get(“fieldname”)).
  - Set value from self.doc.get(df.get(“fieldname”)).
  - If (value and meta\_df and is\_qr\_barcode\_options(meta\_df.options)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → meta\_df → is\_qr\_barcode\_options(meta\_df.options).
    - Set df at “barcode\_format” from “QR”.
    - Set df at “\_qr\_data\_uri” from get\_qr\_code(str(value)).
  - Return no value.
- If df.get(“barcode\_format”) equals “QR”.
  - Set value from self.doc.get(df.get(“barcode\_field”)) when df.get(“barcode\_field”), otherwise df.get(“barcode\_value”).
    - Value choice on df.get(“barcode\_field”) — true gives self.doc.get(df.get(“barcode\_field”)), false gives df.get(“barcode\_value”).
  - If value.
    - Set df at “\_qr\_data\_uri” from get\_qr\_code(str(value)).
- Otherwise.
  - Set df at “\_barcode\_options” from Platform.as\_json(mapping(“format” → (df.get(“barcode\_format”) or “CODE128”), “displayValue” → bool(df.get(“show\_text”, true)), “height” → 40, “margin” → 0), indent = no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“barcode\_format”) → “CODE128”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0496.json#L3837) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L514)

<a id="op-cd8ee94dd049a8"></a>
### Print Format Generator.prepare linked field

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_prepare_linked_field`

**Inputs** self, df.

**Record and data access** resolve a document from link\_df.options via get\_doc · read link\_df.options via get\_value.

**Explicit results** no value.

**Local steps**

- If (df.get(“fieldtype”) differs from “Linked Field” or not df.get(“link\_path”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“fieldtype”) differs from “Linked Field” → not df.get(“link\_path”).
  - Return no value.
- Set path from df at “link\_path”.
- If “.” does not belong to path.
  - Return no value.
- Set tuple(link\_fieldname, target\_fieldname) from path.split(“.”, 1).
- Set link\_df from self.doc.meta.get\_field(link\_fieldname).
- If (not link\_df or link\_df.fieldtype differs from “Link” or not link\_df.options).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not link\_df → link\_df.fieldtype differs from “Link” → not link\_df.options.
  - Return no value.
- If not self.has\_field\_access(self.doc, self.doc.meta, link\_fieldname).
  - Return no value.
- Set name from self.doc.get(link\_fieldname).
- If (not name or not Platform.has\_permission(link\_df.options, “read”, doc = name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not Platform.has\_permission(link\_df.options, “read”, doc = name).
  - Return no value.
- Set target\_meta from Platform.get\_meta(link\_df.options).
- Set target\_df from target\_meta.get\_field(target\_fieldname).
- If not target\_df.
  - Return no value.
- If target\_df.permlevel.
  - Set target\_doc from Platform.get\_doc(link\_df.options, name).
  - If not target\_doc.has\_permlevel\_access\_to(target\_fieldname, target\_df).
    - Return no value.
- Set value from Platform.db.get\_value(link\_df.options, name, target\_fieldname).
- If value is identical to no value.
  - Return no value.
- If target\_df.fieldtype equals “Attach Image”.
  - Set df at “renderer” from “AttachImage”.
  - Set df at “\_value” from value.
  - Return no value.
- Set df at “\_value” from Platform.format\_value(value, df = target\_df, doc = self.doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has field access](operations-039.md#op-30402c5f9751a4).

**Values supplied outside this operation** effective access from Platform.has\_permission(link\_df.options, “read”, doc = name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L184) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L342)

<a id="op-061d934a2e963f"></a>
### Print Format Generator.prepare date format

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_prepare_date_format`

**Inputs** self, df.

**Local steps**

- If (df.get(“date\_format”) and df.get(“fieldtype”) belongs to DATE\_FIELDTYPES and self.doc.get(df.get(“fieldname”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“date\_format”) → df.get(“fieldtype”) belongs to DATE\_FIELDTYPES → self.doc.get(df.get(“fieldname”)).
  - Set df at “\_value” from format\_field\_value(self.doc, df).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L182) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L340)

<a id="op-0811ba1f0993d9"></a>
### Print Format Generator.process margin texts

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_process_margin_texts`

**Inputs** self, layout.

**Explicit results** layout.

**Local steps**

- For each key in tuple(expanded self.\_TOP\_POSITIONS, expanded self.\_BOTTOM\_POSITIONS).
  - Set text from layout.get((“text\_” + key)).
  - If (text and “{{” belongs to text).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in text → “{{” belongs to text.
    - Set layout at (“text\_” + key) from Platform.render\_template(text, self.context).
- Return layout.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0496.json#L4543) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L516)

## Service · Print utils

<a id="op-5874df47686e12"></a>
### Print format doc or none

`operation_foundation_utils_print_utils_business_behavior_print_format_record_or_none`

**Inputs** print\_format, doctype = no value.

**Record and data access** resolve a document from “Print Format” via get\_cached\_doc.

**Explicit results** no value · Platform.get\_cached\_doc(“Print Format”, print\_format).

**Local steps**

- If (not print\_format and doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not print\_format → doctype.
  - Set print\_format from Platform.get\_meta(doctype).default\_print\_format.
- If (not print\_format or print\_format equals “Standard”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → print\_format equals “Standard”.
  - Return no value.
- Attempt the following.
  - Return Platform.get\_cached\_doc(“Print Format”, print\_format).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Format”, print\_format).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L60) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L533)

<a id="op-49c82fb5f0a4c9"></a>
### Resolve pdf generator

`operation_foundation_utils_print_utils_business_behavior_resolve_portable_document_generator`

**Inputs** print\_format = no value, pdf\_generator = no value.

**Declared result** str.

**Record and data access** read “Print Settings” via get\_single\_value.

**Explicit results** stored · “chrome” · generator.

**Local steps**

- Bind dependencies uses\_beta\_renderer.
- Bind dependencies plutoprint\_blockers.
- If (print\_format and uses\_beta\_renderer(print\_format)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → uses\_beta\_renderer(print\_format).
  - Set stored from print\_format.get(“pdf\_generator”).
  - If stored belongs to tuple(“Typst”, “WeasyPrint”).
    - Return stored.
  - If (stored equals “PlutoPrint” and not plutoprint\_blockers(print\_format)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in stored equals “PlutoPrint” → not plutoprint\_blockers(print\_format).
    - Return stored.
  - Return “chrome”.
- Set generator from pdf\_generator.
- If generator is identical to no value.
  - Set generator from ((print\_format and print\_format.get(“pdf\_generator”)) or Platform.db.get\_single\_value(“Print Settings”, “pdf\_generator”) or “wkhtmltopdf”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (print\_format and print\_format.get(“pdf\_generator”)) → Platform.db.get\_single\_value(“Print Settings”, “pdf\_generator”) → “wkhtmltopdf”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → print\_format.get(“pdf\_generator”).
- If (generator equals “PlutoPrint” and plutoprint\_blockers(print\_format)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in generator equals “PlutoPrint” → plutoprint\_blockers(print\_format).
  - Return “chrome”.
- Return generator.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Print Settings”, “pdf\_generator”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L61) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L534)

<a id="op-e43ad21f4a2c40"></a>
### Run print pdf hooks

`operation_foundation_binding_foundation_utils_print_utils_run_print_pdf_hooks`

**Inputs** doctype, name, print\_format.

**Local steps**

- For each hook in Platform.get\_hooks(“on\_print\_pdf”).
  - Evaluate Platform.call(hook, doctype = doctype, name = name, print\_format = print\_format).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“on\_print\_pdf”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L204) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L274) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L362)

<a id="op-5b69df7e7fd409"></a>
### Renders through generator

`operation_foundation_binding_foundation_utils_print_utils_renders_through_generator`

**Inputs** print\_format.

**Declared result** bool.

**Explicit results** bool((print\_format and uses\_beta\_renderer(print\_format) and resolve\_pdf\_generator(print\_format) belongs to GENERATOR\_ENGINES)).

**Local steps**

- Bind dependencies uses\_beta\_renderer.
- Return bool((print\_format and uses\_beta\_renderer(print\_format) and resolve\_pdf\_generator(print\_format) belongs to GENERATOR\_ENGINES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → uses\_beta\_renderer(print\_format) → resolve\_pdf\_generator(print\_format) belongs to GENERATOR\_ENGINES.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L203) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L273) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L361)

<a id="op-9fbe9cf90086f5"></a>
### Get print

`operation_foundation_utils_print_utils_business_behavior_get_print`

**Inputs** doctype = no value, name = no value, print\_format = no value, style = no value, as\_pdf = false, doc = no value, output = no value, no\_letterhead = 0, password = no value, pdf\_options = no value, letterhead = no value, pdf\_generator = no value, settings = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** output · pdf · html · get\_pdf(html, options = pdf\_options, output = output).

**Local steps**

- Bind dependencies copy.
- Bind dependencies uses\_beta\_renderer.
- Bind dependencies get\_pdf.
- Bind dependencies restore\_print\_context, set\_print\_context.
- Bind dependencies get\_response\_without\_exception\_handling.
- Set local from Platform.local.
- Set pf\_doc from \_print\_format\_doc\_or\_none(print\_format).
- Set generator from local.form\_dict.get(“pdf\_generator”).
- If (not generator or (uses\_beta\_renderer(pf\_doc) and generator does not belong to GENERATOR\_ENGINES)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not generator → (uses\_beta\_renderer(pf\_doc) and generator does not belong to GENERATOR\_ENGINES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uses\_beta\_renderer(pf\_doc) → generator does not belong to GENERATOR\_ENGINES.
  - Set generator from resolve\_pdf\_generator(pf\_doc, pdf\_generator).
- Set settings from (settings or local.form\_dict.get(“settings”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings → local.form\_dict.get(“settings”).
- If (as\_pdf and generator equals “wkhtmltopdf” and settings).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in as\_pdf → generator equals “wkhtmltopdf” → settings.
  - Set settings from mapping of key → value for tuple(key, value) drawn from Platform.parse\_json(settings).items() where key differs from “print\_font”.
    - Draw tuple(key, value) from Platform.parse\_json(settings).items(), keep a combination only if (key differs from “print\_font”).
- Set original\_form\_dict from copy.deepcopy(local.form\_dict).
- Attempt the following.
  - Set local.form\_dict.pdf\_generator from generator.
  - Set local.form\_dict.doctype from doctype.
  - Set local.form\_dict.name from name.
  - Set local.form\_dict.format from print\_format.
  - Set local.form\_dict.style from style.
  - Set local.form\_dict.doc from doc.
  - Set local.form\_dict.no\_letterhead from no\_letterhead.
  - Set local.form\_dict.letterhead from letterhead.
  - Set local.form\_dict.settings from settings.
  - Set pdf\_options from (pdf\_options or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pdf\_options → mapping().
  - If password.
    - Set pdf\_options at “password” from password.
  - If (as\_pdf and generator belongs to tuple(expanded HTML\_PDF\_GENERATORS, “Typst”) and pf\_doc and uses\_beta\_renderer(pf\_doc)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in as\_pdf → generator belongs to tuple(expanded HTML\_PDF\_GENERATORS, “Typst”) → pf\_doc → uses\_beta\_renderer(pf\_doc).
    - Bind dependencies make\_access\_log.
    - Bind dependencies Document.
    - Bind dependencies validate\_print.
    - Set doc\_obj from doc when isinstance(doc, Document), otherwise Platform.get\_doc(doctype, name).
      - Value choice on isinstance(doc, Document) — true gives doc, false gives Platform.get\_doc(doctype, name).
    - Evaluate validate\_print(doc\_obj).
    - Evaluate \_run\_print\_pdf\_hooks(doctype, name, print\_format).
    - Set pdf from \_render\_builder\_pdf(pf\_doc, doc\_obj, letterhead, no\_letterhead, …).
    - Evaluate make\_access\_log(doctype = doc\_obj.doctype, document = doc\_obj.name, file\_type = “PDF”, method = “Print”, …).
    - If output.
      - Bind dependencies BytesIO.
      - Bind dependencies PdfReader.
      - For each page in PdfReader(BytesIO(pdf)).pages.
        - Evaluate output.add\_page(page).
      - Return output.
    - Return pdf.
  - Set response from get\_response\_without\_exception\_handling(“printview”, 200).
  - Set html from str(response.data, “utf-8”).
  - If not as\_pdf.
    - Return html.
  - If generator differs from “wkhtmltopdf”.
    - Set previous from set\_print\_context(doctype = doctype, name = name, doc = doc, letterhead = letterhead, …).
    - Attempt the following.
      - For each hook in Platform.get\_hooks(“pdf\_generator”).
        - Set pdf from Platform.call(hook, print\_format = print\_format, html = html, options = pdf\_options, output = output, …).
        - If pdf.
          - If (output and isinstance(pdf, bytes)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in output → isinstance(pdf, bytes).
            - Bind dependencies BytesIO.
            - Bind dependencies PdfReader.
            - Set reader from PdfReader(BytesIO(pdf)).
            - For each page in reader.pages.
              - Evaluate output.add\_page(page).
            - Return output.
          - Return pdf.
    - On exit, including pending return or failure.
      - Evaluate restore\_print\_context(previous).
  - Evaluate \_run\_print\_pdf\_hooks(doctype, name, print\_format).
  - Return get\_pdf(html, options = pdf\_options, output = output).
- On exit, including pending return or failure.
  - Set local.form\_dict from original\_form\_dict.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“pdf\_generator”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L59) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L531)

<a id="op-61daf7c944a3fc"></a>
### Render builder pdf

`operation_foundation_binding_foundation_utils_print_utils_render_builder_pdf`

**Inputs** print\_format, doc, letterhead, no\_letterhead, password = no value, style = no value, settings = no value.

**Explicit results** generator.render\_pdf(password = password).

**Local steps**

- Bind dependencies PrintFormatGenerator.
- Set generator from PrintFormatGenerator(print\_format, doc, letterhead, style = style, settings = Platform.parse\_json(settings) when settings, otherwise no value, no\_letterhead = no\_letterhead).
  - Value choice on settings — true gives Platform.parse\_json(settings), false gives no value.
- Return generator.render\_pdf(password = password).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L202) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L360)

<a id="op-2c5f5c95e6d20d"></a>
### Attach print

`operation_foundation_utils_print_utils_business_behavior_attach_print`

**Inputs** doctype, name, file\_name = no value, print\_format = no value, style = no value, html = no value, doc = no value, lang = no value, print\_letterhead = true, password = no value, letterhead = no value, settings = no value.

**Record and data access** resolve a document from doctype via get\_cached\_doc · read “Letter Head” via get\_value.

**Explicit results** mapping(“fname” → file\_name, “fcontent” → content).

**Local steps**

- Bind dependencies print\_language.
- Bind dependencies scrub\_urls.
- Bind dependencies get\_pdf.
- Set print\_settings from Platform.db.get\_singles\_dict(“Print Settings”).
- Set kwargs from dict(print\_format = print\_format, style = style, doc = doc, no\_letterhead = not print\_letterhead, …).
- Set Platform.local.flags.ignore\_print\_permissions from true.
- Set pf\_doc from \_print\_format\_doc\_or\_none(print\_format, doctype).
- Attempt the following.
  - Within print\_language(lang).
    - Set content from empty text.
    - If cint(print\_settings.send\_print\_as\_pdf).
      - Set ext from “.pdf”.
      - If html.
        - Set content from get\_pdf(html, options = mapping(“password” → password) when password, otherwise no value).
          - Value choice on password — true gives mapping(“password” → password), false gives no value.
      - Otherwise.
        - If renders\_through\_generator(pf\_doc).
          - Bind dependencies uses\_legacy\_weasyprint.
          - Bind dependencies validate\_print\_for\_docstatus.
          - Set doc\_obj from (doc or Platform.get\_cached\_doc(doctype, name)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → Platform.get\_cached\_doc(doctype, name).
          - Evaluate validate\_print\_for\_docstatus(doc\_obj).
          - Evaluate \_run\_print\_pdf\_hooks(doctype, name, print\_format).
          - Set letterhead\_name from letterhead when print\_letterhead, otherwise no value.
            - Value choice on print\_letterhead — true gives letterhead, false gives no value.
          - If uses\_legacy\_weasyprint(pf\_doc).
            - Bind dependencies legacy\_generator.
            - If (print\_letterhead and not letterhead\_name).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_letterhead → not letterhead\_name.
              - Set letterhead\_name from (doc\_obj.get(“letter\_head”) or Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), “name”)).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc\_obj.get(“letter\_head”) → Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), “name”).
            - Set content from legacy\_generator(pf\_doc, doc\_obj, letterhead\_name).render\_pdf(password = password).
          - Otherwise.
            - Set content from \_render\_builder\_pdf(pf\_doc, doc\_obj, letterhead\_name, not print\_letterhead, style = style, settings = settings, …).
          - Bind dependencies make\_access\_log.
          - Evaluate make\_access\_log(doctype = doc\_obj.doctype, document = doc\_obj.name, file\_type = “PDF”, method = “Print”, …).
        - Otherwise.
          - Set kwargs at “as\_pdf” from true.
          - Set content from get\_print(doctype, name, expanded names kwargs).
    - Otherwise.
      - Set ext from “.html”.
      - Set content from (html or scrub\_urls(get\_print(doctype, name, expanded names kwargs)).encode(“utf-8”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in html → scrub\_urls(get\_print(doctype, name, expanded names kwargs)).encode(“utf-8”).
- On exit, including pending return or failure.
  - Set Platform.local.flags.ignore\_print\_permissions from false.
- If not file\_name.
  - Set file\_name from name.
- Set file\_name from (cstr(file\_name).replace(one space, empty text).replace(“/”, “-”) + ext).
- Return mapping(“fname” → file\_name, “fcontent” → content).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(doctype, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L57) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L529)

<a id="op-384d16e5d77c06"></a>
### Setup chromium

`operation_foundation_binding_foundation_utils_print_utils_setup_chromium`

**Inputs** no declared parameters.

**Explicit results** executable.

**Explicit failure paths** RuntimeError(formatted text Failed to setup Chromium: {e}).

**Local steps**

- Bind dependencies click.
- Attempt the following.
  - Set executable from find\_or\_download\_chromium\_executable().
  - Evaluate click.echo(formatted text Chromium is already set up at {executable}).
- On failure (Exception) bound to e.
  - Evaluate click.echo(formatted text Failed to setup Chromium: {e}).
  - Raise RuntimeError(formatted text Failed to setup Chromium: {e}).
- Return executable.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L205) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L363)

<a id="op-27895c5966eb2b"></a>
### Find or download chromium executable

`operation_foundation_binding_foundation_utils_print_utils_find_or_download_chromium_executable`

**Inputs** no declared parameters.

**Explicit results** chromium\_path · str(exec\_path).

**Local steps**

- Bind dependencies platform.
- Bind dependencies shutil.
- Bind dependencies Path.
- Bind dependencies click.
- If chromium\_path bound to shutil.which(Platform.get\_common\_site\_config().get(“chromium\_path”, empty text)).
  - Return chromium\_path.
- Set bench\_path from Platform.utils.get\_bench\_path().
- Set chromium\_dir from os.path.join(bench\_path, “chromium”).
- Set platform\_name from platform.system().lower().
- If platform\_name does not belong to list(“linux”, “darwin”, “windows”).
  - Evaluate click.echo(formatted text Unsupported platform: {platform\_name}).
- Set executable\_name from EXECUTABLE\_PATHS.get(platform\_name).
- Set exec\_path from Path(chromium\_dir).joinpath(expanded executable\_name).
- If not exec\_path.exists().
  - Evaluate click.echo(“Chromium is not available. downloading...”).
  - Evaluate download\_chromium().
- Otherwise.
  - Evaluate make\_chromium\_executable(str(exec\_path)).
- If not exec\_path.exists().
  - Evaluate click.echo(“Error while downloading chrome”).
- Return str(exec\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L198) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L356)

<a id="op-3933caf6494c3d"></a>
### Download chromium

`operation_foundation_binding_foundation_utils_print_utils_download_chromium`

**Inputs** no declared parameters.

**Explicit failure paths** RuntimeError(formatted text Failed to rename extracted directory. Expected {chrome\_folder\_name}.) · RuntimeError(“Failed to rename executable. Expected chrome-headless-shell.”) · RuntimeError(“Download timed out.”) · RuntimeError(“Connection error.”) · RuntimeError(formatted text Failed to download Chromium: {e}) · 1 additional forms in the steps below.

**Local steps**

- Bind dependencies platform.
- Bind dependencies shutil.
- Bind dependencies zipfile.
- Bind dependencies click.
- Bind dependencies requests.
- Set bench\_path from Platform.utils.get\_bench\_path().
- Set chromium\_dir from os.path.join(bench\_path, “chromium”).
- If os.path.exists(chromium\_dir).
  - Evaluate click.echo(“Removing old Chromium directory...”).
  - Evaluate shutil.rmtree(chromium\_dir, ignore\_errors = true).
- Evaluate os.makedirs(chromium\_dir, exist\_ok = true).
- Set download\_url from get\_chromium\_download\_url().
- Set file\_name from os.path.basename(download\_url).
- Set zip\_path from os.path.join(chromium\_dir, file\_name).
- Attempt the following.
  - Evaluate click.echo(formatted text Downloading Chromium from {download\_url}...).
  - Set headers from mapping(“User-Agent” → “Wget/1.21.1”).
  - Within requests.get(download\_url, stream = true, timeout = tuple(10, 60), headers = headers) bound as r.
    - Evaluate r.raise\_for\_status().
    - Set total\_size from int(r.headers.get(“content-length”, 0)).
    - Set bar from click.progressbar(length = total\_size, label = “Downloading Chromium”).
    - Within open(zip\_path, “wb”) bound as f.
      - For each chunk in r.iter\_content(chunk\_size = 65536).
        - Evaluate f.write(chunk).
        - Evaluate bar.update(len(chunk)).
  - Evaluate click.echo(“Extracting Chromium...”).
  - Within zipfile.ZipFile(zip\_path, “r”) bound as zip\_ref.
    - Evaluate zip\_ref.extractall(chromium\_dir).
  - If os.path.exists(zip\_path).
    - Evaluate os.remove(zip\_path).
  - Set extracted from os.listdir(chromium\_dir) at 0.
  - Set executable\_path from EXECUTABLE\_PATHS at platform.system().lower().
  - Set chrome\_folder\_name from executable\_path at 0.
  - If extracted differs from chrome\_folder\_name.
    - Set extracted\_dir from os.path.join(chromium\_dir, extracted).
    - Set renamed\_dir from os.path.join(chromium\_dir, chrome\_folder\_name).
    - If os.path.exists(extracted\_dir).
      - Evaluate click.echo(formatted text Renaming {extracted\_dir} to {renamed\_dir}).
      - Evaluate os.rename(extracted\_dir, renamed\_dir).
    - Otherwise.
      - Raise RuntimeError(formatted text Failed to rename extracted directory. Expected {chrome\_folder\_name}.).
    - If os.path.exists(renamed\_dir).
      - Set executable\_shell from os.path.join(renamed\_dir, “chrome-headless-shell”).
      - If os.path.exists(executable\_shell).
        - Evaluate os.rename(executable\_shell, os.path.join(renamed\_dir, “headless\_shell”)).
      - Otherwise.
        - Raise RuntimeError(“Failed to rename executable. Expected chrome-headless-shell.”).
    - Set exec\_path from os.path.join(renamed\_dir, executable\_path at 1).
    - Evaluate make\_chromium\_executable(exec\_path).
  - Evaluate click.echo(formatted text Chromium is ready to use at: {chromium\_dir}).
- On failure (requests.Timeout).
  - Evaluate click.echo(“Download timed out. Check your internet connection.”).
  - Raise RuntimeError(“Download timed out.”).
- On failure (requests.ConnectionError).
  - Evaluate click.echo(“Failed to connect to Chromium download server.”).
  - Raise RuntimeError(“Connection error.”).
- On failure (requests.RequestException) bound to e.
  - Evaluate click.echo(formatted text Failed to download Chromium: {e}).
  - Raise RuntimeError(formatted text Failed to download Chromium: {e}).
- On failure (zipfile.BadZipFile) bound to e.
  - Evaluate click.echo(formatted text Failed to extract Chromium: {e}).
  - Raise RuntimeError(formatted text Failed to extract Chromium: {e}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.get(download\_url, stream = true, timeout = tuple(10, 60), headers = headers).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L197) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L355)

<a id="op-7df09a14af0540"></a>
### Get chromium download url

`operation_foundation_binding_foundation_utils_print_utils_get_chromium_download_url`

**Inputs** no declared parameters.

**Explicit results** chrome\_download\_url · formatted text {base\_url}{(relative\_path modulo or format version)}.

**Explicit failure paths** validation helper — formatted text No download path configured or Chromium download not available for platform: {platform\_key}.

**Local steps**

- Set common\_config from Platform.get\_common\_site\_config().
- Set chrome\_download\_url from common\_config.get(“chromium\_download\_url”, no value).
- If chrome\_download\_url.
  - Return chrome\_download\_url.
- Set download\_path from mapping(“linux64” → “%s/linux64/chrome-headless-shell-linux64.zip”, “mac-arm64” → “%s/mac-arm64/chrome-headless-shell-mac-arm64.zip”, “mac-x64” → “%s/mac-x64/chrome-headless-shell-mac-x64.zip”, “win32” → “ ….
- Set linux\_arm\_download\_path from mapping(“linux-arm64” → “%s/chromium-headless-shell-linux-arm64.zip”).
- Set platform\_key from calculate\_platform().
- Set version from “133.0.6943.35”.
- Set playwright\_build\_version from “1157”.
- Set base\_url from text in the contract.
- Set playwright\_base\_url from text in the contract.
- Set version from common\_config.get(“chromium\_version”, version).
- Set playwright\_build\_version from common\_config.get(“playwright\_chromium\_version”, playwright\_build\_version).
- Set base\_url from common\_config.get(“chromium\_download\_base\_url”, base\_url).
- Set playwright\_base\_url from common\_config.get(“playwright\_chromium\_download\_base\_url”, playwright\_base\_url).
- If platform\_key belongs to download\_path.
  - Set relative\_path from download\_path at platform\_key.
- Otherwise.
  - If platform\_key belongs to linux\_arm\_download\_path.
    - Set version from playwright\_build\_version.
    - Set base\_url from playwright\_base\_url.
    - Set relative\_path from linux\_arm\_download\_path at platform\_key.
  - Otherwise.
    - Call the validation error handler Platform.throw(formatted text No download path configured or Chromium download not available for platform: {platform\_key}).
- Return formatted text {base\_url}{(relative\_path modulo or format version)}.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L199) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L357)

<a id="op-4334a4d533751e"></a>
### Make chromium executable

`operation_foundation_binding_foundation_utils_print_utils_make_chromium_executable`

**Inputs** executable.

**Explicit results** no value.

**Explicit failure paths** RuntimeError(formatted text Chromium executable not found: {executable}.).

**Local steps**

- Bind dependencies click.
- If os.path.exists(executable).
  - If os.access(executable, os.X\_OK).
    - Evaluate click.echo(formatted text Chromium executable is already executable: {executable}).
    - Return no value.
  - Evaluate click.echo(formatted text Making Chromium executable: {executable}).
  - Evaluate os.chmod(executable, 493).
  - Evaluate click.echo(formatted text Chromium executable permissions set: {executable}).
- Otherwise.
  - Raise RuntimeError(formatted text Chromium executable not found: {executable}.).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L201) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L359)

<a id="op-c48752453be28d"></a>
### Calculate platform

`operation_foundation_binding_foundation_utils_print_utils_calculate_platform`

**Inputs** no declared parameters.

**Explicit results** “linux-arm64” · “linux64” · “mac-arm64” · “mac-x64” · “win32” · 2 additional forms in the steps below.

**Local steps**

- Bind dependencies platform.
- Set system from platform.system().lower().
- Set arch from platform.machine().lower().
- If (system equals “linux” and arch equals “aarch64”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “linux” → arch equals “aarch64”.
  - Return “linux-arm64”.
- Otherwise.
  - If (system equals “linux” and arch equals “x86\_64”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “linux” → arch equals “x86\_64”.
    - Return “linux64”.
  - Otherwise.
    - If (system equals “darwin” and arch equals “arm64”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “darwin” → arch equals “arm64”.
      - Return “mac-arm64”.
    - Otherwise.
      - If (system equals “darwin” and arch equals “x86\_64”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “darwin” → arch equals “x86\_64”.
        - Return “mac-x64”.
      - Otherwise.
        - If (system equals “windows” and arch equals “x86”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “windows” → arch equals “x86”.
          - Return “win32”.
        - Otherwise.
          - If (system equals “windows” and arch equals “x86\_64”).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in system equals “windows” → arch equals “x86\_64”.
            - Return “win64”.
- Return text in the contract.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L196) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L354)

<a id="op-1399a932c4458f"></a>
### Get linux distribution info

`operation_foundation_binding_foundation_utils_print_utils_get_linux_distribution_info`

**Inputs** no declared parameters.

**Explicit results** mapping(“id” → empty text, “version” → empty text) · mapping(“id” → distro.id().lower(), “version” → distro.version()).

**Local steps**

- Bind dependencies distro.
- If not distro.
  - Return mapping(“id” → empty text, “version” → empty text).
- Return mapping(“id” → distro.id().lower(), “version” → distro.version()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L200) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L358)

<a id="op-f1fee3c0d52a8c"></a>
### Parse float and unit

`operation_foundation_utils_print_utils_business_behavior_parse_decimal_and_unit`

**Inputs** input\_text, default\_unit = “px”.

**Explicit results** mapping(“value” → input\_text, “unit” → default\_unit) · no value · mapping(“value” → number, “unit” → unit at 0 when len(unit) equals 1, otherwise default\_unit).

**Local steps**

- If isinstance(input\_text, (int bitwise or float)).
  - Return mapping(“value” → input\_text, “unit” → default\_unit).
- If not isinstance(input\_text, str).
  - Return no value.
- Set number from float(re.search(“&#91;+-&#93;?(&#91;0-9&#93;\*&#91;.&#93;)?&#91;0-9&#93;+”, input\_text).group()).
- Set valid\_units from list(“px”, “mm”, “cm”, “in”).
- Set unit from list of match.group() for rx drawn from valid\_units where match bound to re.search(rx, input\_text).
  - Draw rx from valid\_units, keep a combination only if (match bound to re.search(rx, input\_text)).
- Return mapping(“value” → number, “unit” → unit at 0 when len(unit) equals 1, otherwise default\_unit).
  - Value choice on len(unit) equals 1 — true gives unit at 0, false gives default\_unit.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L1323) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L532)

<a id="op-d846d541666bdb"></a>
### Convert uom

`operation_foundation_utils_print_utils_business_behavior_convert_unit_of_measure`

**Inputs** number, from\_uom = “px”, to\_uom = “px”, only\_number = false.

**Declared result** float.

**Explicit results** round((number × converstion\_factor at 0 at formatted text from\_{from\_uom} at 0 at formatted text to\_{to\_uom}), 3) · formatted text {round((number × nested operand in the contract at nested operand in the contract at formatted text from\_{nested operand in the contract} at 0 at form.

**Local steps**

- Set unit\_values from mapping(“px” → 1, “mm” → 3.7795275591, “cm” → 37.795275591, “in” → 96).
- Set from\_px from tuple(mapping(“to\_px” → 1, “to\_mm” → (unit\_values at “px” ÷ unit\_values at “mm”), “to\_cm” → (unit\_values at “px” ÷ unit\_values at “cm”), “to\_in” → (unit\_values at “px” ÷ unit\_values at “in”))).
- Set from\_mm from tuple(mapping(“to\_mm” → 1, “to\_px” → (unit\_values at “mm” ÷ unit\_values at “px”), “to\_cm” → (unit\_values at “mm” ÷ unit\_values at “cm”), “to\_in” → (unit\_values at “mm” ÷ unit\_values at “in”))).
- Set from\_cm from tuple(mapping(“to\_cm” → 1, “to\_px” → (unit\_values at “cm” ÷ unit\_values at “px”), “to\_mm” → (unit\_values at “cm” ÷ unit\_values at “mm”), “to\_in” → (unit\_values at “cm” ÷ unit\_values at “in”))).
- Set from\_in from tuple(mapping(“to\_in” → 1, “to\_px” → (unit\_values at “in” ÷ unit\_values at “px”), “to\_mm” → (unit\_values at “in” ÷ unit\_values at “mm”), “to\_cm” → (unit\_values at “in” ÷ unit\_values at “cm”))).
- Set converstion\_factor from tuple(mapping(“from\_px” → from\_px, “from\_mm” → from\_mm, “from\_cm” → from\_cm, “from\_in” → from\_in)).
- If only\_number.
  - Return round((number × converstion\_factor at 0 at formatted text from\_{from\_uom} at 0 at formatted text to\_{to\_uom}), 3).
- Return formatted text {round((number × nested operand in the contract at nested operand in the contract at formatted text from\_{nested operand in the contract} at 0 at form.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L58) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L530)

## Service · Queue

<a id="op-ecf61a79f15cd4"></a>
### Event Queue.initialize

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_initialize`

**Inputs** self.

**Local steps**

- Set self.queue from “pulse-client:events”.
- Set self.queue\_size from 10000.
- Set self.ratelimit\_prefix from “pulse-client:last\_sent:”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2059) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L743)

<a id="op-22f5ea8539142f"></a>
### Event Queue.length

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_length`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** Platform.cache.llen(self.queue).

**Local steps**

- Return Platform.cache.llen(self.queue).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2140) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L745)

<a id="op-a1e4b0c28889a5"></a>
### Event Queue.add

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_add`

**Inputs** self, event, interval = no value.

**Explicit results** no value.

**Local steps**

- If self.\_is\_ratelimited(event, interval).
  - Return no value.
- Evaluate self.\_queue\_event(event).
- Evaluate self.\_update\_ratelimit(event, interval).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is ratelimited](operations-041.md#op-8ddedbbf4fb0ac), [queue event](operations-041.md#op-91d8ef9a712b70), [update ratelimit](operations-041.md#op-b06d354e90252c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2207) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L736)
