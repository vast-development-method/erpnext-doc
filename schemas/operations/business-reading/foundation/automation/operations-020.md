# Workflow, automation and dispatch · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Events

<a id="op-68cee5c5cfb252"></a>
### Claim subscription

`operation_foundation_binding_foundation_automation_engine_events_claim_subscription`

**Inputs** name, payload.

**Declared result** int.

**State and service calls** call db\_set on subscription · request set\_value on QUEUE.

**Explicit results** 0 · 1 when matched, otherwise 0.

**Local steps**

- Set subscription from \_lock\_subscription(name).
- If subscription.status differs from “Waiting”.
  - Return 0.
- Set matched from get\_datetime(subscription.expires\_at) &gt; now\_datetime().
- Evaluate subscription.db\_set(mapping(“status” → “Matched” when matched, otherwise “Timed Out”, “event\_payload” → Platform.as\_json(payload) when matched, otherwise no value), update\_modified = false).
  - Value choice on matched — true gives “Matched”, false gives “Timed Out”.
  - Value choice on matched — true gives Platform.as\_json(payload), false gives no value.
- Evaluate Platform.db.set\_value(QUEUE, subscription.resume\_queue, “run\_after”, now(), update\_modified = false).
- Return 1 when matched, otherwise 0.
  - Value choice on matched — true gives 1, false gives 0.

**Values supplied outside this operation** clock or generated value from now\_datetime(), now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L404)

<a id="op-7b031697c92d2b"></a>
### Lock subscription

`operation_foundation_binding_foundation_automation_engine_events_lock_subscription`

**Inputs** name.

**Record and data access** resolve a document from SUBSCRIPTION via get\_doc.

**Explicit results** Platform.get\_doc(SUBSCRIPTION, name).

**Local steps**

- Set table from Platform.qb.DocType(SUBSCRIPTION).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals name).for\_update().run().
- Return Platform.get\_doc(SUBSCRIPTION, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L410)

<a id="op-a41af902a4692b"></a>
### Timeout seconds

`operation_foundation_binding_foundation_automation_engine_events_timeout_seconds`

**Inputs** params.

**Declared result** int.

**Explicit results** (cint(params at “timeout\_value”) × TIMEOUT\_UNITS at params at “timeout\_unit”).

**Local steps**

- Return (cint(params at “timeout\_value”) × TIMEOUT\_UNITS at params at “timeout\_unit”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L419)

<a id="op-dae9e7a06350a2"></a>
### Render

`operation_foundation_binding_foundation_automation_engine_events_render`

**Inputs** value, context.

**Explicit results** value · Platform.render\_template(value, mapping(“doc” → context.get(“trigger\_doc”), “context” → context, “payload” → (context.get(“payload”) or mapping()))).

**Local steps**

- If (not isinstance(value, str) or “{{” does not belong to value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(value, str) → “{{” does not belong to value.
  - Return value.
- Return Platform.render\_template(value, mapping(“doc” → context.get(“trigger\_doc”), “context” → context, “payload” → (context.get(“payload”) or mapping()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.get(“payload”) → mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L415)

<a id="op-f3a7d8500da853"></a>
### Validate payload size

`operation_foundation_binding_foundation_automation_engine_events_validate_payload_size`

**Inputs** payload.

**Explicit failure paths** validation helper — translated “Automation event payload is too large”.

**Local steps**

- If len(Platform.as\_json(payload).encode()) &gt; settings.get(“event\_payload\_limit”).
  - Call the validation error handler Platform.throw(translated “Automation event payload is too large”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L421)

## Service · Extract

<a id="op-3689a733ee814d"></a>
### Extract

`operation_foundation_binding_foundation_flow_knowledge_extract_extract`

**Inputs** source.

**Declared result** list at ExtractedDoc.

**Explicit results** handler(source).

**Explicit failure paths** validation helper — translated “Unsupported source type: {0}”.format(source.source\_type).

**Local steps**

- Set handlers from mapping(“Text” → \_extract\_text\_source, “File” → \_extract\_file\_source, “URL” → \_extract\_url\_source, “DocType” → \_extract\_doctype\_source).
- Set handler from handlers.get(source.source\_type).
- If handler is identical to no value.
  - Call the validation error handler Platform.throw(translated “Unsupported source type: {0}”.format(source.source\_type)).
- Return handler(source).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1161)

<a id="op-5906a0e4029306"></a>
### Extract text source

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_text_source`

**Inputs** source.

**Declared result** list at ExtractedDoc.

**Explicit results** \_single((source.content or empty text).strip()).

**Local steps**

- Return \_single((source.content or empty text).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.content → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1170)

<a id="op-e8d8960927a6e1"></a>
### Extract file source

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_file_source`

**Inputs** source.

**Declared result** list at ExtractedDoc.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** \_single(extract\_file(file\_doc)).

**Local steps**

- Set file\_doc from Platform.get\_doc(“File”, mapping(“file\_url” → source.file)).
- Return \_single(extract\_file(file\_doc)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1166)

<a id="op-10550c431cb317"></a>
### Extract file

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_file`

**Inputs** file\_doc, max\_ocr\_pages = no value.

**Declared result** str.

**Explicit results** \_extract\_by\_extension(file\_doc.get\_content(), extension, max\_ocr\_pages).strip().

**Local steps**

- Set extension from nested operand in the contract.splitext((nested operand in the contract or nested operand in the contract or nested operand in the contract)) at 1.lower().lstrip(“.”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_doc.file\_name → file\_doc.file\_url → empty text.
- Return \_extract\_by\_extension(file\_doc.get\_content(), extension, max\_ocr\_pages).strip().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1165)

<a id="op-0e7a1f531a7e20"></a>
### Extract url source

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_url_source`

**Inputs** source.

**Declared result** list at ExtractedDoc.

**Explicit results** \_single(text.strip()).

**Explicit failure paths** validation helper — translated “The URL redirects; enter the address it leads to.”.

**Local steps**

- Bind dependencies requests.
- Set url from (source.url or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.url → empty text.
- Evaluate \_validate\_public\_url(url).
- Set response from requests.get(url, timeout = URL\_TIMEOUT, stream = true, allow\_redirects = false, headers = mapping(“User-Agent” → “Flow-Knowledge/1.0”)).
- If response.is\_redirect.
  - Call the validation error handler Platform.throw(translated “The URL redirects; enter the address it leads to.”).
- Evaluate response.raise\_for\_status().
- Set raw from \_read\_capped(response).
- Set content\_type from response.headers.get(“Content-Type”, empty text).lower().
- If (“application/pdf” belongs to content\_type or nested operand in the contract(nested operand in the contract) at 0.lower().endswith(“.pdf”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “application/pdf” belongs to content\_type → nested operand in the contract.split(“?”) at 0.lower().endswith(“.pdf”).
  - Set text from \_extract\_pdf(raw).
- Otherwise.
  - Set text from \_extract\_html(\_as\_text(raw)).
- Return \_single(text.strip()).

**Values supplied outside this operation** service or queued work from requests.get(url, timeout = URL\_TIMEOUT, stream = true, allow\_redirects = false, headers = mapping(“User-Agent” → “Flow-Knowledge/1.0”)).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1171)

<a id="op-1ab0f3ab27b521"></a>
### Resolve content fields

`operation_foundation_binding_foundation_flow_knowledge_extract_resolve_content_fields`

**Inputs** meta, raw.

**Declared result** list at str.

**Explicit results** fields.

**Explicit failure paths** validation helper — translated “No content fields configured.” · validation helper — translated “Unknown fields for {0}: {1}”.format(meta.name, “, ”.join(unknown)) · validation helper — translated “Child table fields are not supported as content fields: {0}”.format(“, ”.join(child)).

**Local steps**

- Set fields from list of f.strip() for f drawn from (raw or empty text).split(“,”) where f.strip().
  - Draw f from (raw or empty text).split(“,”), keep a combination only if (f.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in raw → empty text.
- If not fields.
  - Call the validation error handler Platform.throw(translated “No content fields configured.”, title = translated “Invalid Source”).
- Set allowed from (set of df.fieldname for df drawn from meta.fields bitwise or set(“name”, “creation”, “modified”, “owner”)).
  - Draw df from meta.fields.
- Set unknown from list of f for f drawn from fields where f does not belong to allowed.
  - Draw f from fields, keep a combination only if (f does not belong to allowed).
- If unknown.
  - Call the validation error handler Platform.throw(translated “Unknown fields for {0}: {1}”.format(meta.name, “, ”.join(unknown)), title = translated “Invalid Content Fields”).
- Set child from list of f for f drawn from fields where (df bound to meta.get\_field(f) and df.fieldtype belongs to CHILD\_FIELDTYPES).
  - Draw f from fields, keep a combination only if ((df bound to meta.get\_field(f) and df.fieldtype belongs to CHILD\_FIELDTYPES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df bound to meta.get\_field(f) → df.fieldtype belongs to CHILD\_FIELDTYPES.
- If child.
  - Call the validation error handler Platform.throw(translated “Child table fields are not supported as content fields: {0}”.format(“, ”.join(child)), title = translated “Invalid Content Fields”).
- Return fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1179)

<a id="op-a75c468151d388"></a>
### Extract doctype source

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_doctype_source`

**Inputs** source.

**Declared result** list at ExtractedDoc.

**Record and data access** read doctype via get\_all.

**Explicit results** docs.

**Local steps**

- Set doctype from source.reference\_doctype.
- Set meta from Platform.get\_meta(doctype).
- Set fields from resolve\_content\_fields(meta, source.content\_fields).
- Set rows from Platform.get\_all(doctype, filters = \_parse\_filters(source.filters), fields = list(“name”, expanded fields), limit\_page\_length = 0).
- Set docs from list().
- For each row in rows.
  - Set text from \_row\_to\_text(row, fields, meta).
  - If text.
    - Evaluate docs.append(ExtractedDoc(text = text, reference\_doctype = doctype, reference\_name = row at “name”)).
- Return docs.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1163)

<a id="op-e3f5cd8b37edc4"></a>
### Extract by extension

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_by_extension`

**Inputs** content, extension, max\_ocr\_pages = no value.

**Declared result** str.

**Explicit results** \_extract\_pdf(\_as\_bytes(content), max\_ocr\_pages) · \_extract\_xlsx(\_as\_bytes(content)) · \_extract\_docx(\_as\_bytes(content)) · \_extract\_html(\_as\_text(content)) · \_ocr\_image(\_as\_bytes(content)) · 1 additional forms in the steps below.

**Explicit failure paths** validation helper — translated “Unsupported file format: .{0}”.format((extension or “?”)).

**Local steps**

- If extension equals “pdf”.
  - Return \_extract\_pdf(\_as\_bytes(content), max\_ocr\_pages).
- If extension equals “xlsx”.
  - Return \_extract\_xlsx(\_as\_bytes(content)).
- If extension equals “docx”.
  - Return \_extract\_docx(\_as\_bytes(content)).
- If extension belongs to tuple(“html”, “htm”).
  - Return \_extract\_html(\_as\_text(content)).
- If extension belongs to IMAGE\_EXTENSIONS.
  - Return \_ocr\_image(\_as\_bytes(content)).
- If extension belongs to TEXT\_EXTENSIONS.
  - Return \_as\_text(content).
- Call the validation error handler Platform.throw(translated “Unsupported file format: .{0}”.format((extension or “?”)), title = translated “Unsupported Format”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extension → “?”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1162)

<a id="op-ef0d130addd1d2"></a>
### Extract pdf

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_pdf`

**Inputs** data, max\_ocr\_pages = no value.

**Declared result** str.

**Explicit results** whitespace '\\n\\n'.join(generator of page for page drawn from pages where page).

**Explicit failure paths** validation helper — translated “PDF is password protected and cannot be read.”.

**Local steps**

- Bind dependencies pdfplumber.
- Bind dependencies PDFPasswordIncorrect.
- Attempt the following.
  - Within pdfplumber.open(BytesIO(data)) bound as pdf.
    - Set pages from list of \_extract\_pdf\_page(page, ocr = (max\_ocr\_pages is identical to no value or i &lt; max\_ocr\_pages)) for tuple(i, page) drawn from enumerate(pdf.pages).
      - Draw tuple(i, page) from enumerate(pdf.pages).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in max\_ocr\_pages is identical to no value → i &lt; max\_ocr\_pages.
    - If (max\_ocr\_pages is distinct from no value and any(generator of page.images for page drawn from pdf.pages at slice max\_ocr\_pages to no value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_ocr\_pages is distinct from no value → any(generator of page.images for page drawn from pdf.pages at slice max\_ocr\_pages to no value).
      - Draw page from pdf.pages at slice max\_ocr\_pages to no value.
      - Evaluate pages.append(OCR\_SKIPPED.format(max\_ocr\_pages)).
- On failure (PDFPasswordIncorrect).
  - Call the validation error handler Platform.throw(translated “PDF is password protected and cannot be read.”, title = translated “Cannot Read PDF”).
- Return whitespace '\\n\\n'.join(generator of page for page drawn from pages where page).
  - Draw page from pages, keep a combination only if (page).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1168)

<a id="op-834e45150e97a2"></a>
### Extract pdf page

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_pdf_page`

**Inputs** page, ocr = true.

**Declared result** str.

**Explicit results** whitespace '\\n\\n'.join(generator of part for part drawn from parts where part).

**Local steps**

- Set parts from list().
- Set tables from page.find\_tables().
- For each table in tables.
  - Set markdown from \_table\_to\_markdown(table.extract()).
  - If markdown.
    - Evaluate parts.append(markdown).
- Set body from page.
- For each table in tables.
  - Set body from body.outside\_bbox(table.bbox).
- Set prose from \_clean\_pdf\_text((body.extract\_text() or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in body.extract\_text() → empty text.
- If prose.
  - Evaluate parts.append(prose).
- If (ocr and page.images).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ocr → page.images.
  - Evaluate parts.append(\_ocr\_image(\_render\_page\_png(page))).
- Return whitespace '\\n\\n'.join(generator of part for part drawn from parts where part).
  - Draw part from parts, keep a combination only if (part).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1169)

<a id="op-0c80b5d58b13a7"></a>
### Table to markdown

`operation_foundation_binding_foundation_flow_knowledge_extract_table_to_markdown`

**Inputs** table.

**Declared result** str.

**Explicit results** empty text · whitespace '\\n'.join(lines).

**Local steps**

- Set rows from list of row for row drawn from (table or list()) where row.
  - Draw row from (table or list()), keep a combination only if (row).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in table → list().
- If not rows.
  - Return empty text.
- Set lines from list().
- For each tuple(i, row) in enumerate(rows).
  - Set cells from list of nested operand in the contract.replace(whitespace '\\n', one space).replace(“\|”, “\\\|”).strip() for cell drawn from row.
    - Draw cell from row.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cell → empty text.
  - Evaluate lines.append(((“\| ” + “ \| ”.join(cells)) + “ \|”)).
  - If i equals 0.
    - Evaluate lines.append(((“\| ” + “ \| ”.join(generator of “---” for \_ drawn from cells)) + “ \|”)).
      - Draw \_ from cells.
- Return whitespace '\\n'.join(lines).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1182)

<a id="op-a3313eeb822983"></a>
### Render page png

`operation_foundation_binding_foundation_flow_knowledge_extract_render_page_png`

**Inputs** page.

**Declared result** bytes.

**State and service calls** call save on page.to\_image(resolution = resolution).original.

**Explicit results** buffer.getvalue().

**Local steps**

- Set buffer from BytesIO().
- Set resolution from min(OCR\_DPI, ((MAX\_OCR\_SIDE × 72) ÷ max(page.width, page.height, 1))).
- Evaluate page.to\_image(resolution = resolution).original.save(buffer, format = “PNG”).
- Return buffer.getvalue().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1177)

<a id="op-c467e0efe31399"></a>
### Ocr engine

`operation_foundation_binding_foundation_flow_knowledge_extract_ocr_engine`

**Inputs** no declared parameters.

**Explicit results** \_ocr\_engine\_instance.

**Local steps**

- Use module bindings \_ocr\_engine\_instance.
- If \_ocr\_engine\_instance is identical to no value.
  - Bind dependencies RapidOCR.
  - Set \_ocr\_engine\_instance from RapidOCR().
- Return \_ocr\_engine\_instance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1173)

<a id="op-2ba37022b66bd4"></a>
### Ocr image

`operation_foundation_binding_foundation_flow_knowledge_extract_ocr_image`

**Inputs** data.

**Declared result** str.

**Explicit results** empty text · whitespace '\\n'.join(result.txts).

**Local steps**

- Set result from \_ocr\_engine()(data).
- If not result.txts.
  - Return empty text.
- Return whitespace '\\n'.join(result.txts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1174)

<a id="op-5d609baf887110"></a>
### Extract xlsx

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_xlsx`

**Inputs** data.

**Declared result** str.

**Explicit results** whitespace '\\n\\n'.join(sheets).

**Local steps**

- Bind dependencies openpyxl.
- Set workbook from openpyxl.load\_workbook(BytesIO(data), read\_only = true, data\_only = true).
- Attempt the following.
  - Set sheets from list().
  - For each worksheet in workbook.worksheets.
    - Set rows from list().
    - For each row in worksheet.iter\_rows(values\_only = true).
      - Set cells from list of str(cell) for cell drawn from row where cell is distinct from no value.
        - Draw cell from row, keep a combination only if (cell is distinct from no value).
      - If cells.
        - Evaluate rows.append(whitespace '\\t'.join(cells)).
    - If rows.
      - Evaluate sheets.append(“# {0}\\n{1}”.format(worksheet.title, whitespace '\\n'.join(rows))).
  - Return whitespace '\\n\\n'.join(sheets).
- On exit, including pending return or failure.
  - Evaluate workbook.close().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1172)

<a id="op-92713290010b4e"></a>
### Extract docx

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_docx`

**Inputs** data.

**Declared result** str.

**Explicit results** whitespace '\\n\\n'.join(generator of p for p drawn from paragraphs where p).

**Local steps**

- Bind dependencies Document.
- Set document from Document(BytesIO(data)).
- Set paragraphs from list of p.text.strip() for p drawn from document.paragraphs.
  - Draw p from document.paragraphs.
- Return whitespace '\\n\\n'.join(generator of p for p drawn from paragraphs where p).
  - Draw p from paragraphs, keep a combination only if (p).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1164)

<a id="op-b19235f9b5dd7d"></a>
### Extract html

`operation_foundation_binding_foundation_flow_knowledge_extract_extract_html`

**Inputs** markup.

**Declared result** str.

**Explicit results** soup.get\_text(separator = one space, strip = true).

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(markup, “lxml”).
- For each tag in soup(list(“script”, “style”, “noscript”)).
  - Evaluate tag.decompose().
- Return soup.get\_text(separator = one space, strip = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1167)

<a id="op-da3a5d8574f44b"></a>
### Single

`operation_foundation_binding_foundation_flow_knowledge_extract_single`

**Inputs** text.

**Declared result** list at ExtractedDoc.

**Explicit results** list(ExtractedDoc(text = text)) when text, otherwise list().

**Local steps**

- Return list(ExtractedDoc(text = text)) when text, otherwise list().
  - Value choice on text — true gives list(ExtractedDoc(text = text)), false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1181)

<a id="op-f94a461571fe06"></a>
### As bytes

`operation_foundation_binding_foundation_flow_knowledge_extract_as_bytes`

**Inputs** content.

**Declared result** bytes.

**Explicit results** content when isinstance(content, bytes), otherwise content.encode(“utf-8”, “replace”).

**Local steps**

- Return content when isinstance(content, bytes), otherwise content.encode(“utf-8”, “replace”).
  - Value choice on isinstance(content, bytes) — true gives content, false gives content.encode(“utf-8”, “replace”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1158)
