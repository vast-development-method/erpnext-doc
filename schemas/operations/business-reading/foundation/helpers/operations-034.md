# Shared value and file services · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Pdf

<a id="op-382e441c7b54d4"></a>
### Prepare options

`operation_foundation_utils_portable_document_business_behavior_prepare_options`

**Inputs** html, options.

**Record and data access** read “Print Settings” via get\_single\_value.

**Explicit results** tuple(html, options).

**Local steps**

- If not options.
  - Set options from mapping().
- Evaluate options.update(mapping(“print-media-type” → no value, “background” → no value, “images” → no value, “quiet” → no value, …)).
- If not options.get(“margin-right”).
  - Set options at “margin-right” from “15mm”.
- If not options.get(“margin-left”).
  - Set options at “margin-left” from “15mm”.
- Set tuple(html, html\_options) from read\_options\_from\_html(html).
- Evaluate options.update((html\_options or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in html\_options → mapping().
- Evaluate options.update(get\_cookie\_options()).
- Set html from inline\_private\_images(html).
- Set pdf\_page\_size from (options.get(“page-size”) or Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”) or “A4”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“page-size”) → Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”) → “A4”.
- If pdf\_page\_size equals “Custom”.
  - Evaluate options.pop(“page-size”, no value).
  - Set options at “page-height” from (options.get(“page-height”) or Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_height”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“page-height”) → Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_height”).
  - Set options at “page-width” from (options.get(“page-width”) or Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_width”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“page-width”) → Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_width”).
- Otherwise.
  - Set options at “page-size” from pdf\_page\_size.
- Return tuple(html, options).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_size”), Platform.db.get\_single\_value(“Print Settings”, “pdf\_page\_height”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L16) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L439)

<a id="op-ca9e28ecf313cd"></a>
### Get cookie options

`operation_foundation_utils_portable_document_business_behavior_get_cookie_options`

**Inputs** no declared parameters.

**Explicit results** options.

**Local steps**

- Set options from mapping().
- If (Platform.session and Platform.session.sid and hasattr(Platform.local, “request”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session → Platform.session.sid → hasattr(Platform.local, “request”).
  - Set cookiejar from formatted text /tmp/{Platform.generate\_hash()}.jar.
  - Set domain from Platform.utils.get\_host\_name().split(“:”, 1) at 0.
  - Within open(cookiejar, “w”) bound as f.
    - Evaluate f.write(formatted text sid={Platform.session.sid}; Domain={domain}; ).
  - Set options at “cookie-jar” from cookiejar.
- Return options.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L1278) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L422)

<a id="op-ef275854c22818"></a>
### Read options from html

`operation_foundation_utils_portable_document_business_behavior_read_options_from_document_markup`

**Inputs** html.

**Explicit results** tuple(str(soup), options).

**Local steps**

- Set options from mapping().
- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(html, “html5lib”).
- Evaluate options.update(prepare\_header\_footer(soup)).
- Evaluate toggle\_visible\_pdf(soup).
- Set valid\_styles from get\_print\_format\_styles(soup).
- Set attrs from tuple(“margin-top”, “margin-bottom”, “margin-left”, “margin-right”, …).
- Update options using bitwise or mapping of style.name → style.value for style drawn from valid\_styles where style.name belongs to attrs.
  - Draw style from valid\_styles, keep a combination only if (style.name belongs to attrs).
- Return tuple(str(soup), options).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L1601) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L440)

<a id="op-3700061ce8404f"></a>
### Get print format styles

`operation_foundation_utils_portable_document_business_behavior_get_print_format_styles`

**Inputs** soup.

**Declared result** list at “cssutils.css.Property”.

**Explicit results** valid\_styles.

**Local steps**

- Bind dependencies cssutils.
- Evaluate cssutils.log.setLog(Platform.logger(“cssutils”)).
- Set stylesheet from empty text.
- Set style\_tags from soup.find\_all(“style”).
- For each style\_tag in style\_tags.
  - Update stylesheet using + cstr(style\_tag.string).
- Set parsed\_sheet from cssutils.CSSParser(fetcher = deferred anonymous expression).parseString(stylesheet).
- Set valid\_styles from list().
- For each rule in parsed\_sheet.
  - If not isinstance(rule, cssutils.css.CSSStyleRule).
    - Continue with the next iteration or loop test.
  - If “.print-format” belongs to list of x.strip() for x drawn from rule.selectorText.split(“,”).
    - Draw x from rule.selectorText.split(“,”).
    - Evaluate valid\_styles.extend(generator of entry for entry drawn from rule.style).
      - Draw entry from rule.style.
- Return valid\_styles.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L10) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L426)

<a id="op-f9ab99ac973211"></a>
### Inline private images

`operation_foundation_utils_portable_document_business_behavior_inline_private_images`

**Inputs** html.

**Declared result** str.

**Explicit results** str(soup).

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(html, “html.parser”).
- For each img in soup.find\_all(“img”).
  - If b64 bound to \_get\_base64\_image(img at “src”).
    - Set img at “src” from b64.
- Return str(soup).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L2345) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L429)

<a id="op-7dc79cc9a44cac"></a>
### Get base64 image

`operation_foundation_utils_portable_document_business_behavior_get_base_64_image`

**Inputs** src.

**Explicit results** no value · formatted text data:{mime\_type};base64,{b64\_encoded\_image}.

**Local steps**

- Attempt the following.
  - Set parsed\_url from urlparse(src).
  - Set path from parsed\_url.path.
  - Set query from parse\_qs(parsed\_url.query).
  - Set mime\_type from mimetypes.guess\_type(path) at 0.
  - If (mime\_type is identical to no value or not mime\_type.startswith(“image/”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in mime\_type is identical to no value → not mime\_type.startswith(“image/”).
    - Return no value.
  - Set filename from ((query.get(“fid”) and query at “fid” at 0) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (query.get(“fid”) and query at “fid” at 0) → no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in query.get(“fid”) → query at “fid” at 0.
  - Set file from find\_file\_by\_url(path, name = filename).
  - If (not file or not file.is\_private).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not file → not file.is\_private.
    - Return no value.
  - Set b64\_encoded\_image from base64.b64encode(file.get\_content()).decode().
  - Return formatted text data:{mime\_type};base64,{b64\_encoded\_image}.
- On failure (Exception).
  - Evaluate Platform.logger(“pdf”).error(“Failed to convert inline images to base64”, exc\_info = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L2526) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L420)

<a id="op-a38c5b42316c0c"></a>
### Prepare header footer

`operation_foundation_utils_portable_document_business_behavior_prepare_header_footer`

**Inputs** soup.

**Explicit results** options.

**Local steps**

- Set options from mapping().
- Set head from soup.find(“head”).contents.
- Set styles from soup.find\_all(“style”).
- Set print\_css from bundled\_asset(“print.bundle.css”).lstrip(“/”).
- Set css from Platform.read\_file(os.path.join(Platform.local.sites\_path, print\_css)).
- For each html\_id in tuple(“header-html”, “footer-html”).
  - If content bound to soup.find(id = html\_id).
    - Set content from content.extract().
    - For each tag in soup.find\_all(id = html\_id).
      - Evaluate tag.extract().
    - Evaluate toggle\_visible\_pdf(content).
    - Set id\_map from mapping(“header-html” → “pdf\_header\_html”, “footer-html” → “pdf\_footer\_html”).
    - Set hook\_func from Platform.get\_hooks(id\_map.get(html\_id)).
    - Set html from Platform.call(hook\_func at negative 1, soup = soup, head = head, content = content, styles = styles, …).
    - Set fname from os.path.join(“/tmp”, formatted text Platform-pdf-{Platform.generate\_hash()}.html).
    - Within open(fname, “wb”) bound as f.
      - Evaluate f.write(html.encode(“utf-8”)).
    - Set options at html\_id from fname.
  - Otherwise.
    - If html\_id equals “header-html”.
      - Set options at “margin-top” from “15mm”.
    - Otherwise.
      - If html\_id equals “footer-html”.
        - Set options at “margin-bottom” from “15mm”.
- Return options.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(id\_map.get(html\_id)) · clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L3020) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L438)

<a id="op-b02213d1b6927c"></a>
### Cleanup

`operation_foundation_utils_portable_document_business_behavior_cleanup`

**Inputs** options.

**Local steps**

- For each key in tuple(“header-html”, “footer-html”, “cookie-jar”).
  - If (options.get(key) and os.path.exists(options at key)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in options.get(key) → os.path.exists(options at key).
    - Evaluate os.remove(options at key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L3838) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L418)

<a id="op-1d8efb414b46d9"></a>
### Toggle visible pdf

`operation_foundation_utils_portable_document_business_behavior_toggle_visible_portable_document`

**Inputs** soup.

**Local steps**

- For each tag in soup.find\_all(attrs = mapping(“class” → “visible-pdf”)).
  - Evaluate tag.attrs at “class”.remove(“visible-pdf”).
- For each tag in soup.find\_all(attrs = mapping(“class” → “hidden-pdf”)).
  - Evaluate tag.extract().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L3990) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L441)

<a id="op-f101f6343aa68e"></a>
### Is wkhtmltopdf valid

`operation_foundation_utils_portable_document_business_behavior_is_wkhtmltopdf_valid`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L4183) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L430)

<a id="op-10669e5d51d834"></a>
### Get wkhtmltopdf version

`operation_foundation_utils_portable_document_business_behavior_get_wkhtmltopdf_version`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L4368) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L427)

<a id="op-3d7702f00ab4c5"></a>
### Pdf contains js

`operation_foundation_utils_portable_document_business_behavior_portable_document_contains_client_script`

**Inputs** file\_content.

**Explicit results** true · false.

**Local steps**

- Bind dependencies BytesIO.
- Bind dependencies PdfReader, errors.
- Bind dependencies IndirectObject.
- Set reader from PdfReader(BytesIO(file\_content)).
- Bind local operation has\_javascript for subsequent calls.
- Set root from reader.trailer.get(“/Root”, mapping()).
- Attempt the following.
  - If has\_javascript(root).
    - Return true.
  - For each page in reader.pages.
    - If has\_javascript(page).
      - Return true.
- On failure (errors.FileNotDecryptedError).
  - Take no action here.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L14) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L434)

<a id="op-0c2db42d97933f"></a>
### Pdf contains js.has javascript

`operation_foundation_utils_portable_document_business_behavior_portable_document_contains_client_script_has_client_language`

**Inputs** obj, seen = no value.

**Explicit results** false · true.

**Local steps**

- If seen is identical to no value.
  - Set seen from set().
- If isinstance(obj, IndirectObject).
  - Set key from tuple(obj.idnum, obj.generation).
  - If key belongs to seen.
    - Return false.
  - Evaluate seen.add(key).
  - Set obj from obj.get\_object().
- If isinstance(obj, dict).
  - For each tuple(key, value) in obj.items().
    - If key equals “/Parent”.
      - Continue with the next iteration or loop test.
    - If key equals “/JS”.
      - Return true.
    - If has\_javascript(value, seen).
      - Return true.
- Otherwise.
  - If isinstance(obj, list).
    - For each item in obj.
      - If has\_javascript(item, seen).
        - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L15) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L435)

<a id="op-f6bc0f92334f3f"></a>
### Get host url

`operation_foundation_utils_portable_document_business_behavior_get_host_resource_address`

**Inputs** no declared parameters.

**Explicit results** Platform.request.host\_url · (get\_url() + “/”).

**Local steps**

- If Platform.request.
  - Return Platform.request.host\_url.
- Otherwise.
  - Return (get\_url() + “/”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L5318) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L424)

## Service · Pdf merge

<a id="op-bafee45c15d53d"></a>
### PDFTransformer.initialize

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_initialize`

**Inputs** self, browser.

**Explicit results** no value.

**Local steps**

- Set self.browser from browser.
- Set self.body\_pdf from browser.body\_pdf.
- Set self.is\_print\_designer from browser.is\_print\_designer.
- Set self.encrypt\_password from self.browser.options.get(“password”, no value).
- Evaluate self.\_set\_header\_pdf().
- Evaluate self.\_set\_footer\_pdf().
- If (not self.header\_pdf and not self.footer\_pdf).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.header\_pdf → not self.footer\_pdf.
  - Return no value.
- Set self.no\_of\_pages from len(self.body\_pdf.pages).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header pdf](operations-034.md#op-67077f4d64ccd9), [set footer pdf](operations-034.md#op-d50ca3ac2c49a1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L5938) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L466)

<a id="op-67077f4d64ccd9"></a>
### PDFTransformer.set header pdf

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_set_header_portable_document`

**Inputs** self.

**Local steps**

- Set self.header\_pdf from no value.
- If hasattr(self.browser, “header\_pdf”).
  - Set self.header\_pdf from self.browser.header\_pdf.
  - Set self.is\_header\_dynamic from self.browser.is\_header\_dynamic.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L6204) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L468)

<a id="op-d50ca3ac2c49a1"></a>
### PDFTransformer.set footer pdf

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_set_footer_portable_document`

**Inputs** self.

**Local steps**

- Set self.footer\_pdf from no value.
- If hasattr(self.browser, “footer\_pdf”).
  - Set self.footer\_pdf from self.browser.footer\_pdf.
  - Set self.is\_footer\_dynamic from self.browser.is\_footer\_dynamic.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L6331) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L467)

<a id="op-f3988dc6c76653"></a>
### PDFTransformer.transform pdf

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_transform_portable_document`

**Inputs** self, output = no value.

**Explicit results** self.\_encrypt\_raw(body) · body · output · self.get\_file\_data\_from\_writer(writer).

**Local steps**

- Bind dependencies PdfWriter.
- Set header from self.header\_pdf.
- Set body from self.body\_pdf.
- Set footer from self.footer\_pdf.
- If (not header and not footer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not header → not footer.
  - If self.encrypt\_password.
    - Return self.\_encrypt\_raw(body).
  - Return body.
- Set body\_height from body.pages at 0.mediabox.top.
- Set body\_transform, header\_height, footer\_height from 0.
- If footer.
  - Set footer\_height from footer.pages at 0.mediabox.top.
  - Set body\_transform from footer\_height.
- If header.
  - Set header\_height from header.pages at 0.mediabox.top.
  - Set header\_transform from (body\_height + footer\_height).
- Set page\_top from ((header\_height + body\_height) + footer\_height).
- If header.
  - For each h in header.pages.
    - Evaluate self.\_transform(h, page\_top, header\_transform).
- For each p in body.pages.
  - Evaluate self.\_transform(p, page\_top, body\_transform).
  - If header.
    - If self.is\_header\_dynamic.
      - Evaluate p.merge\_page(header.pages at min(p.page\_number, (len(header.pages) − 1))).
    - Otherwise.
      - If self.is\_print\_designer.
        - If p.page\_number equals 0.
          - Evaluate p.merge\_page(header.pages at 0).
        - Otherwise.
          - If p.page\_number equals (self.no\_of\_pages − 1).
            - Evaluate p.merge\_page(header.pages at 3).
          - Otherwise.
            - If (p.page\_number modulo or format 2) equals 0.
              - Evaluate p.merge\_page(header.pages at 2).
            - Otherwise.
              - Evaluate p.merge\_page(header.pages at 1).
      - Otherwise.
        - Evaluate p.merge\_page(header.pages at 0).
  - If footer.
    - If (self.is\_footer\_dynamic and len(footer.pages) &gt; 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_footer\_dynamic → len(footer.pages) &gt; 1.
      - Evaluate p.merge\_page(footer.pages at min(p.page\_number, (len(footer.pages) − 1))).
    - Otherwise.
      - If self.is\_print\_designer.
        - If p.page\_number equals 0.
          - Evaluate p.merge\_page(footer.pages at 0).
        - Otherwise.
          - If p.page\_number equals (self.no\_of\_pages − 1).
            - Evaluate p.merge\_page(footer.pages at 3).
          - Otherwise.
            - If (p.page\_number modulo or format 2) equals 0.
              - Evaluate p.merge\_page(footer.pages at 2).
            - Otherwise.
              - Evaluate p.merge\_page(footer.pages at 1).
      - Otherwise.
        - Evaluate p.merge\_page(footer.pages at 0).
- Set writer from (output or PdfWriter()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in output → PdfWriter().
- Set first\_new\_page from len(writer.pages).
- Evaluate writer.append\_pages\_from\_reader(body).
- For each page in writer.pages at slice first\_new\_page to no value.
  - Evaluate page.compress\_content\_streams().
- If output.
  - Return output.
- If self.encrypt\_password.
  - Evaluate writer.encrypt(self.encrypt\_password).
- Return self.get\_file\_data\_from\_writer(writer).

**Methods declared on this owner** [encrypt raw](operations-034.md#op-922c3131efee9c), [transform](operations-034.md#op-a81a9604ce7d57), [get file data from writer](operations-034.md#op-2860cc9456ac2c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L26) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L470)

<a id="op-922c3131efee9c"></a>
### PDFTransformer.encrypt raw

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_encrypt_raw`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** self, body.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0492.json#L7899) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L464)

<a id="op-a81a9604ce7d57"></a>
### PDFTransformer.transform

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_transform`

**Inputs** self, page, page\_top, ty.

**Explicit results** page.

**Local steps**

- Bind dependencies FloatObject.
- Set page.mediabox.upper\_right from tuple(page.mediabox.right, page\_top).
- Set content from page.get\_contents().
- Evaluate content.set\_data(((formatted text q 1 0 0 1 0 {nested operand in the contract(nested operand in the contract)} cm .encode() + content.get\_data()) + byte value)).
- Evaluate page.replace\_contents(content).
- For each annotation in page.get(“/Annots”, list()).
  - Set annotation from annotation.get\_object().
  - For each key in tuple(“/Rect”, “/QuadPoints”).
    - If key belongs to annotation.
      - Set points from annotation at key.
      - Set points at slice 1 to no value with step 2 from list of FloatObject((y + ty)) for y drawn from points at slice 1 to no value with step 2.
        - Draw y from points at slice 1 to no value with step 2.
- Return page.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L25) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L469)

<a id="op-2860cc9456ac2c"></a>
### PDFTransformer.get file data from writer

`operation_foundation_utils_portable_document_generator_portable_document_merge_business_behavior_portable_document_transformer_get_file_data_from_writer`

**Inputs** self, writer\_obj.

**Explicit results** stream.read().

**Local steps**

- Bind dependencies BytesIO.
- Set stream from BytesIO().
- Evaluate writer\_obj.write(stream).
- Evaluate stream.seek(0).
- Return stream.read().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L181) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L465)

## Service · Platformcloud

<a id="op-c032f2b47bcdf5"></a>
### On Platformcloud

`operation_foundation_utils_frappecloud_business_behavior_on_managed_hosting`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** Platform.local.site.endswith(Platform\_CLOUD\_DOMAINS).

**Local steps**

- Return Platform.local.site.endswith(Platform\_CLOUD\_DOMAINS).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0481.json#L3786) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L149)

## Service · Pluto

<a id="op-9eb8c5734eeaa3"></a>
### Resolve container queries

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_resolve_container_queries`

**Inputs** css, width.

**Declared result** str.

**Explicit results** CONTAINER\_QUERY.sub(resolve, css).

**Local steps**

- Bind local operation resolve for subsequent calls.
- Return CONTAINER\_QUERY.sub(resolve, css).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L160) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L318)

<a id="op-73d71242304927"></a>
### Resolve container queries.resolve

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_resolve_container_queries_resolve`

**Inputs** query.

**Explicit results** “@media all” when matches, otherwise “@media not all”.

**Local steps**

- Set limit from (float(query.group(2)) × PX\_PER\_UNIT at query.group(3).lower()).
- Set matches from width ≥ limit when query.group(1).lower() equals “min”, otherwise width ≤ limit.
  - Value choice on query.group(1).lower() equals “min” — true gives width ≥ limit, false gives width ≤ limit.
- Return “@media all” when matches, otherwise “@media not all”.
  - Value choice on matches — true gives “@media all”, false gives “@media not all”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L161) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L319)
