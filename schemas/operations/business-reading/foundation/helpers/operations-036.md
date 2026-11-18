# Shared value and file services · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Pluto

<a id="op-c0d19c1718e12f"></a>
### Pluto Page.close

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_close`

**Inputs** self.

**Local steps**

- Set self.html from empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L141) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L299)

<a id="op-92ef18ff082864"></a>
### Pluto Page.layout

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_layout`

**Inputs** self, width, height, margins, scale, user\_style = empty text.

**Explicit results** self.\_book((width ÷ scale), (height ÷ scale), list of (margin ÷ scale) for margin drawn from margins, user\_style = user\_style).

**Local steps**

- Return self.\_book((width ÷ scale), (height ÷ scale), list of (margin ÷ scale) for margin drawn from margins, user\_style = user\_style).
  - Draw margin from margins.

**Methods declared on this owner** [book](operations-036.md#op-c1e65dba49da0d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L149) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L307)

<a id="op-c1e65dba49da0d"></a>
### Pluto Page.book

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_book`

**Inputs** self, width, height, margins = no value, user\_style = empty text.

**Explicit results** book.

**Local steps**

- Bind dependencies plutoprint.
- Set height from (height or 100000).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in height → 100000.
- Set margins from (margins or tuple(0, 0, 0, 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in margins → tuple(0, 0, 0, 0).
- Set page\_rule from text in the contract.format(width, height, expanded margins).
- Set book from plutoprint.Book(plutoprint.PageSize(width, height), plutoprint.PageMargins(expanded margins), plutoprint.MEDIA\_TYPE\_PRINT).
- Set book.custom\_resource\_fetcher from self.fetcher.
- Set content\_width from (((width − margins at 1) − margins at 3) ÷ POINTS\_PER\_PX).
- Set html from CSS\_IN\_HTML.sub(deferred anonymous expression, self.html).
- Evaluate book.load\_html((html + page\_rule), user\_style = (BASE\_STYLE + user\_style), base\_url = get\_host\_url()).
- Return book.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L140) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L298)

<a id="op-fdc567a4110722"></a>
### Pluto Page.write

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_plutopage_write`

**Inputs** self, book, width, height, scale.

**Explicit results** stream.getvalue().

**Local steps**

- Bind dependencies plutoprint.
- Set stream from BytesIO().
- If scale equals 1.
  - Evaluate book.write\_to\_pdf\_stream(stream).
  - Return stream.getvalue().
- Set canvas from plutoprint.PDFCanvas.create\_for\_stream(stream, plutoprint.PageSize(width, height)).
- For each index in range(book.get\_page\_count()).
  - Evaluate canvas.save\_state().
  - Evaluate canvas.scale((scale × POINTS\_PER\_PX), (scale × POINTS\_PER\_PX)).
  - Evaluate book.render\_page(canvas, index).
  - Evaluate canvas.restore\_state().
  - Evaluate canvas.show\_page().
- Evaluate canvas.finish().
- Return stream.getvalue().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L157) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L315)

<a id="op-1db835c0164e16"></a>
### Inter ttf path

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_inter_ttf_path`

**Inputs** url.

**Declared result** (Path bitwise or no value).

**Explicit results** no value · next(generator of Path(path, name) for name drawn from os.listdir(path) where name.endswith(formatted text -{weight}.ttf), no value).

**Local steps**

- Bind dependencies DEFAULT\_FONT, \_font\_cache\_path, ensure\_typst\_fonts.
- If (not match bound to INTER\_WOFF2.search(url) or match.group(1).endswith(“Italic”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not match bound to INTER\_WOFF2.search(url) → match.group(1).endswith(“Italic”).
  - Return no value.
- If not path bound to \_font\_cache\_path(DEFAULT\_FONT).
  - Evaluate ensure\_typst\_fonts(no value).
  - Return no value.
- Set weight from INTER\_WEIGHTS.get(match.group(1), 400).
- Return next(generator of Path(path, name) for name drawn from os.listdir(path) where name.endswith(formatted text -{weight}.ttf), no value).
  - Draw name from os.listdir(path), keep a combination only if (name.endswith(formatted text -{weight}.ttf)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L127) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L285)

<a id="op-acecd3f111b9ec"></a>
### Cached inter faces

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_cached_inter_faces`

**Inputs** css.

**Declared result** str.

**Explicit results** css · INTER\_WOFF2\_HINT.sub(“\\1”, css).

**Local steps**

- If not INTER\_WOFF2.search(css).
  - Return css.
- Set css from FONT\_FACE.sub(deferred anonymous expression, css).
- Return INTER\_WOFF2\_HINT.sub(“\\1”, css).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L126) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L284)

<a id="op-0a5b8e546805d7"></a>
### Local resource fetcher

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_local_resource_fetcher`

**Inputs** block\_external\_requests = false.

**Explicit results** Fetcher().

**Local steps**

- Bind dependencies plutoprint.
- Bind dependencies read\_local\_resource.
- Bind local type Fetcher (class body executes during definition).
- Return Fetcher().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L128) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L286)

<a id="op-b4d9117a56e82b"></a>
### Local resource fetcher.Fetcher.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_local_resource_fetcher_fetcher_init`

**Inputs** self.

**Local steps**

- Evaluate super().\_\_init\_\_().
- Set self.cache from mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L131) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L289)

<a id="op-045af8dc37f041"></a>
### Local resource fetcher.Fetcher.fetch url

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_local_resource_fetcher_fetcher_fetch_url`

**Inputs** self, url.

**Explicit results** self.cache at url.

**Local steps**

- If url does not belong to self.cache.
  - Set self.cache at url from self.fetch(url).
- Return self.cache at url.

**Methods declared on this owner** [fetch](operations-036.md#op-45a202d6959b3d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L130) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L288)

<a id="op-45a202d6959b3d"></a>
### Local resource fetcher.Fetcher.fetch

`operation_foundation_binding_foundation_utils_pdf_generator_pluto_local_resource_fetcher_fetcher_fetch`

**Inputs** self, url.

**Explicit results** plutoprint.default\_resource\_fetcher.fetch\_url(ttf.resolve().as\_uri()) · plutoprint.default\_resource\_fetcher.fetch\_url(formatted text data:{content\_type};base64,{content}) · resource.

**Explicit failure paths** plutoprint.Error(formatted text Blocked {url}) · plutoprint.Error(formatted text Cannot read {url}) · plutoprint.Error(formatted text Not a page resource: {url}).

**Local steps**

- If url.lower().startswith(“file:”).
  - Raise plutoprint.Error(formatted text Blocked {url}).
- If url.startswith(get\_host\_url()).
  - If ttf bound to inter\_ttf\_path(url).
    - Return plutoprint.default\_resource\_fetcher.fetch\_url(ttf.resolve().as\_uri()).
  - If not resource bound to read\_local\_resource(url).
    - Raise plutoprint.Error(formatted text Cannot read {url}).
  - Set tuple(content, content\_type) from resource.
  - Set content\_type from (content\_type or mimetypes.guess\_type(url.split(“?”) at 0) at 0 or “application/octet-stream”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in content\_type → mimetypes.guess\_type(url.split(“?”) at 0) at 0 → “application/octet-stream”.
  - If content\_type equals “text/css”.
    - Set content from base64.b64decode(content).decode().
    - Set content from cached\_inter\_faces(BREAK\_WORD.sub(“\\1normal”, content)).encode().
    - Set content from base64.b64encode(content).decode().
  - Return plutoprint.default\_resource\_fetcher.fetch\_url(formatted text data:{content\_type};base64,{content}).
- If (block\_external\_requests and not url.startswith(“data:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in block\_external\_requests → not url.startswith(“data:”).
  - Raise plutoprint.Error(formatted text Blocked {url}).
- Set resource from plutoprint.default\_resource\_fetcher.fetch\_url(url).
- If resource.get\_mime\_type() equals “text/html”.
  - Raise plutoprint.Error(formatted text Not a page resource: {url}).
- Return resource.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L129) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L287)

## Service · Preview

<a id="op-bcb22a80b2ba6f"></a>
### Get preview from html

`operation_foundation_utils_preview_business_behavior_get_preview_from_document_markup`

**Inputs** html, format = “jpg”, width = 1280, height = 720.

**Declared result** bytes.

**Explicit results** capture\_screenshot(format, html = html, width = width, height = height).

**Local steps**

- Return capture\_screenshot(format, html = html, width = width, height = height).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L313) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L473)

<a id="op-21036c69d6ae1e"></a>
### Get preview from url

`operation_foundation_utils_preview_business_behavior_get_preview_from_resource_address`

**Inputs** url, wait\_for = 0, headers = no value, format = “jpg”.

**Declared result** bytes.

**Explicit results** capture\_screenshot(format, url = url, wait\_for = cint(wait\_for), headers = headers).

**Local steps**

- Return capture\_screenshot(format, url = url, wait\_for = cint(wait\_for), headers = headers).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L451) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L474)

<a id="op-ff66bb1081f335"></a>
### Get image format

`operation_foundation_utils_preview_business_behavior_get_image_format`

**Inputs** format.

**Declared result** str.

**Explicit results** “jpeg” when format equals “jpg”, otherwise format.

**Explicit failure paths** validation helper — translated “Invalid format. Supported formats are {0}”.format(“, ”.join(SUPPORTED\_FORMATS)).

**Local steps**

- If format does not belong to SUPPORTED\_FORMATS.
  - Call the validation error handler Platform.throw(translated “Invalid format. Supported formats are {0}”.format(“, ”.join(SUPPORTED\_FORMATS))).
- Return “jpeg” when format equals “jpg”, otherwise format.
  - Value choice on format equals “jpg” — true gives “jpeg”, false gives format.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L610) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L472)

<a id="op-d00242cbbfb3b1"></a>
### Capture screenshot

`operation_foundation_utils_preview_business_behavior_capture_screenshot`

**Inputs** format, html (named only, default no value), url (named only, default no value), wait\_for (named only, default 0), headers (named only, default no value), width (named only, default 1280), height (named only, default 720).

**Declared result** bytes.

**Explicit results** page.capture\_screenshot(image\_format = image\_format).

**Explicit failure paths** RuntimeError(formatted text Error creating browser context: {error}) · propagate active failure.

**Local steps**

- Bind dependencies get\_host\_url.
- Bind dependencies CDPSocketClient.
- Bind dependencies ChromePDFGenerator.
- Bind dependencies Page.
- Set image\_format from get\_image\_format(format).
- Set generator from ChromePDFGenerator().
- Set browser\_id from Platform.utils.random\_string(10).
- Evaluate generator.add\_browser(browser\_id).
- Set session, page from no value.
- Attempt the following.
  - Attempt the following.
    - If not generator.\_devtools\_url.
      - Evaluate generator.\_set\_devtools\_url().
    - Set session from CDPSocketClient(generator.\_devtools\_url).
    - Evaluate session.connect().
    - Set tuple(context, error) from session.send(“Target.createBrowserContext”, mapping(“disposeOnDetach” → true)).
    - If error.
      - Raise RuntimeError(formatted text Error creating browser context: {error}).
    - Set page from Page(session, context at “browserContextId”, “screenshot”).
    - Set page.is\_print\_designer from false.
    - Evaluate page.set\_media\_emulation(“screen”).
    - Evaluate page.set\_device\_metrics(width, height).
    - If html is distinct from no value.
      - Evaluate page.set\_tab\_url(get\_host\_url()).
      - Evaluate page.wait\_for\_navigate().
      - Evaluate page.set\_content(html, wait\_for = list(“load”, “DOMContentLoaded”, “networkIdle”)).
      - Evaluate page.wait\_for\_set\_content().
    - Otherwise.
      - If headers.
        - Evaluate page.send(“Network.enable”).
        - Evaluate page.send(“Network.setExtraHTTPHeaders”, mapping(“headers” → headers)).
      - Evaluate page.navigate(url).
      - If wait\_for.
        - Evaluate time.sleep((wait\_for ÷ 1000)).
    - Return page.capture\_screenshot(image\_format = image\_format).
  - On exit, including pending return or failure.
    - Evaluate safe\_execute((page and page.close)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in page → page.close.
    - Evaluate safe\_execute((session and session.disconnect)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in session → session.disconnect.
    - Evaluate generator.remove\_browser(browser\_id).
- On failure (Exception).
  - Set proc from generator.\_chromium\_process.
  - If (proc is distinct from no value and proc.poll() is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in proc is distinct from no value → proc.poll() is distinct from no value.
    - Evaluate generator.\_close\_browser().
  - Propagate the active failure.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L27) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L471)

<a id="op-a1c102e7640c9c"></a>
### Safe execute

`operation_foundation_utils_preview_business_behavior_safe_execute`

**Inputs** fn.

**Local steps**

- If fn.
  - Attempt the following.
    - Evaluate fn().
  - On failure (Exception).
    - Evaluate Platform.log\_error(“Preview cleanup failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L1790) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L475)

## Service · Print format

<a id="op-8f6084a76c3aba"></a>
### Get max bulk print docs

`operation_foundation_binding_foundation_utils_print_format_get_max_bulk_print_docs`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Print Settings” via get\_single\_value.

**Explicit results** (Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_bulk\_print\_docs”)) or Platform.cint(Platform.conf.get(“max\_bulk\_print\_docs”)) or 100).

**Local steps**

- Return (Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_bulk\_print\_docs”)) or Platform.cint(Platform.conf.get(“max\_bulk\_print\_docs”)) or 100).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_bulk\_print\_docs”)) → Platform.cint(Platform.conf.get(“max\_bulk\_print\_docs”)) → 100.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Print Settings”, “max\_bulk\_print\_docs”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L190) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L348)

<a id="op-8a86b08bfb6910"></a>
### Get max concurrent bulk exports

`operation_foundation_binding_foundation_utils_print_format_get_max_concurrent_bulk_exports`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Print Settings” via get\_single\_value.

**Explicit results** (Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_concurrent\_bulk\_exports”)) or Platform.cint(Platform.conf.get(“max\_concurrent\_bulk\_exports”)) or 5).

**Local steps**

- Return (Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_concurrent\_bulk\_exports”)) or Platform.cint(Platform.conf.get(“max\_concurrent\_bulk\_exports”)) or 5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cint(Platform.db.get\_single\_value(“Print Settings”, “max\_concurrent\_bulk\_exports”)) → Platform.cint(Platform.conf.get(“max\_concurrent\_bulk\_exports”)) → 5.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Print Settings”, “max\_concurrent\_bulk\_exports”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L191) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L349)

<a id="op-1c128bea0a5570"></a>
### Enforce multi pdf async rate limit

`operation_foundation_binding_foundation_utils_print_format_enforce_multi_pdf_async_rate_limit`

**Inputs** no declared parameters.

**Explicit failure paths** validation helper with Platform.RateLimitExceededError — translated “You hit the rate limit because of too many requests. Please try after sometime.”.

**Local steps**

- Set cache\_key from Platform.cache.make\_key(formatted text rl:multi\_pdf\_async:{Platform.session.user}).
- Evaluate Platform.cache.set(cache\_key, 0, nx = true, ex = MULTI\_PDF\_ASYNC\_RATE\_WINDOW).
- If Platform.cache.incrby(cache\_key, 1) &gt; MULTI\_PDF\_ASYNC\_RATE\_LIMIT.
  - Call the validation error handler Platform.throw(translated “You hit the rate limit because of too many requests. Please try after sometime.”, Platform.RateLimitExceededError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L167) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L325)

<a id="op-d652c39e41ed51"></a>
### Get multi pdf doc count

`operation_foundation_binding_foundation_utils_print_format_get_multi_pdf_doc_count`

**Inputs** doctype, name.

**Declared result** int.

**Explicit results** sum(list of len(doctype at dt) for dt drawn from doctype) · len(Platform.parse\_json(name)).

**Local steps**

- If isinstance(doctype, dict).
  - Return sum(list of len(doctype at dt) for dt drawn from doctype).
    - Draw dt from doctype.
- Return len(Platform.parse\_json(name)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L192) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L350)

<a id="op-ea8132f73cd6e5"></a>
### Download multi pdf

`operation_foundation_utils_print_format_business_behavior_download_multi_portable_document`

**Inputs** doctype, name, format = no value, no\_letterhead = false, letterhead = no value, options = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.concurrent\_limit().

**Explicit results** \_download\_multi\_pdf(doctype, name, format, no\_letterhead, …).

**Explicit failure paths** validation helper — translated “Cannot generate PDF for more than {0} documents at a time”.format(max\_docs).

**Local steps**

- Set max\_docs from get\_max\_bulk\_print\_docs().
- If \_get\_multi\_pdf\_doc\_count(doctype, name) &gt; max\_docs.
  - Call the validation error handler Platform.throw(translated “Cannot generate PDF for more than {0} documents at a time”.format(max\_docs)).
- Return \_download\_multi\_pdf(doctype, name, format, no\_letterhead, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L28) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L476)

<a id="op-6dcdf1b2223385"></a>
### Download multi pdf async

`operation_foundation_utils_print_format_business_behavior_download_multi_portable_document_async`

**Inputs** doctype, name, format = no value, no\_letterhead = false, letterhead = no value, options = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue with \_download\_multi\_pdf.

**Explicit results** mapping(“task\_id” → task\_id).

**Explicit failure paths** validation helper — translated “Cannot generate PDF for more than {0} documents at a time”.format(max\_docs) · validation helper with Platform.RateLimitExceededError — translated “You already have the maximum number of bulk PDF exports in progress. Please wait for one to finish.”.

**Local steps**

- Evaluate \_enforce\_multi\_pdf\_async\_rate\_limit().
- Set doc\_count from \_get\_multi\_pdf\_doc\_count(doctype, name).
- Set max\_docs from get\_max\_bulk\_print\_docs().
- If doc\_count &gt; max\_docs.
  - Call the validation error handler Platform.throw(translated “Cannot generate PDF for more than {0} documents at a time”.format(max\_docs)).
- Set task\_id from str(uuid.uuid4()).
- Set job from no value.
- For each slot in range(get\_max\_concurrent\_bulk\_exports()).
  - Set job from Platform.enqueue(\_download\_multi\_pdf, doctype = doctype, name = name, task\_id = task\_id, format = format, …).
    - Value choice on doc\_count &gt; 20 — true gives “long”, false gives “short”.
  - If job is distinct from no value.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If job is identical to no value.
  - Call the validation error handler Platform.throw(translated “You already have the maximum number of bulk PDF exports in progress. Please wait for one to finish.”, Platform.RateLimitExceededError).
- Set Platform.local.response at “http\_status\_code” from http.HTTPStatus.CREATED.
- Return mapping(“task\_id” → task\_id).

**Values supplied outside this operation** clock or generated value from uuid.uuid4() · service or queued work from Platform.enqueue(\_download\_multi\_pdf, doctype = doctype, name = name, task\_id = task\_id, format = format, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L30) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L478)

<a id="op-4edc71360fdb9d"></a>
### Page settings

`operation_foundation_binding_foundation_utils_print_format_page_settings`

**Inputs** pdf\_options.

**Declared result** dict.

**Explicit results** settings.

**Local steps**

- Set pdf\_options from (pdf\_options or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pdf\_options → mapping().
- Set settings from mapping().
- For each tuple(option, setting) in tuple(tuple(“page-size”, “pdf\_page\_size”), tuple(“page-height”, “pdf\_page\_height”), tuple(“page-width”, “pdf\_page\_width”)).
  - If pdf\_options.get(option).
    - Set settings at setting from pdf\_options at option.
- If (“pdf\_page\_height” belongs to settings and “pdf\_page\_size” does not belong to settings).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “pdf\_page\_height” belongs to settings → “pdf\_page\_size” does not belong to settings.
  - Set settings at “pdf\_page\_size” from “Custom”.
- Return settings.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L193) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L351)

<a id="op-a00ae0780c82a2"></a>
### Classic page options

`operation_foundation_binding_foundation_utils_print_format_classic_page_options`

**Inputs** pdf\_options.

**Declared result** dict.

**Explicit results** pdf\_options.

**Local steps**

- Set pdf\_options from dict((pdf\_options or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pdf\_options → mapping().
- For each option in tuple(“page-height”, “page-width”).
  - If isinstance(pdf\_options.get(option), (int bitwise or float)).
    - Set pdf\_options at option from formatted text {pdf\_options at option}mm.
    - Set pdf\_options at “page-size” from “Custom”.
- Return pdf\_options.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L163) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L321)

<a id="op-0cab3c03cc4462"></a>
### Publish failure

`operation_foundation_binding_foundation_utils_print_format_publish_failure`

**Inputs** task\_id, error.

**State and service calls** publish realtime with formatted text task\_complete:{task\_id}.

**Local steps**

- If task\_id.
  - Evaluate Platform.publish\_realtime(formatted text task\_complete:{task\_id}, message = mapping(“error” → (str(error) or translated “You are not permitted to print one of the selected documents”)), user = Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(error) → translated “You are not permitted to print one of the selected documents”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(formatted text task\_complete:{task\_id}, message = mapping(“error” → (str(error) or translated “You are not permitted to print one of the selected documents”)), user = Platform.session.user).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L194) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L352)
