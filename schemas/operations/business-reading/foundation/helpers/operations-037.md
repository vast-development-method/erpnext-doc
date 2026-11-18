# Shared value and file services · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Print format

<a id="op-565c33348f118b"></a>
### Download multi pdf

`operation_foundation_utils_print_format_business_behavior_download_multi_portable_document_2`

**Inputs** doctype, name, format = no value, no\_letterhead = false, letterhead = no value, options = no value, task\_id = no value.

**Record and data access** read “Print Format” via get\_value · resolve a document from mapping(“doctype” → “File”, “file\_name” → formatted text {filename}{task\_id}.pdf, “content” → merged\_pdf.getvalue(), “is\_private” → 1) via get\_doc.

**State and service calls** call save on \_file · publish realtime with formatted text task\_complete:{task\_id} · msgprint with failed.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set filename from empty text.
- Bind dependencies PdfWriter.
- Set pdf\_writer from PdfWriter().
- Set failed from list().
- If isinstance(options, str).
  - Set options from json.loads(options).
- Set format\_language from (format and Platform.db.get\_value(“Print Format”, format, “default\_print\_language”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in format → Platform.db.get\_value(“Print Format”, format, “default\_print\_language”).
- Bind local operation print\_into\_writer for subsequent calls.
- Bind local operation \_print\_into\_writer for subsequent calls.
- If not isinstance(doctype, dict).
  - Set result from json.loads(name).
  - Set total\_docs from len(result).
  - Set filename from formatted text {doctype}\_.
  - For each tuple(idx, ss) in enumerate(result).
    - Attempt the following.
      - Set first\_page from len(pdf\_writer.pages).
      - Set pdf\_writer from print\_into\_writer(doctype, ss).
      - Evaluate pdf\_writer.add\_outline\_item(str(ss), first\_page).
    - On failure (Platform.PermissionError) bound to e.
      - Evaluate publish\_failure(task\_id, e).
      - Propagate the active failure.
    - On failure (Exception).
      - Evaluate Platform.log\_error(title = “Error in Multi PDF download”, reference\_doctype = doctype, reference\_name = ss).
      - Evaluate failed.append(get\_link\_to\_form(doctype, ss)).
    - If task\_id.
      - Evaluate Platform.publish\_progress(percent = (((idx + 1) ÷ total\_docs) × 100), title = translated “PDF Generation in Progress”, description = translated “{0}/{1} complete \| Please leave this tab open until completi ….
  - If task\_id is identical to no value.
    - Set Platform.local.response.filename from “{doctype}.pdf”.format(doctype = doctype.replace(one space, “-”).replace(“/”, “-”)).
- Otherwise.
  - Set total\_docs from sum(list of len(doctype at dt) for dt drawn from doctype).
    - Draw dt from doctype.
  - Set count from 0.
  - For each doctype\_name in doctype.
    - Update filename using + formatted text {doctype\_name}\_.
    - For each doc\_name in doctype at doctype\_name.
      - Attempt the following.
        - Set first\_page from len(pdf\_writer.pages).
        - Set pdf\_writer from print\_into\_writer(doctype\_name, doc\_name).
        - Evaluate pdf\_writer.add\_outline\_item(str(doc\_name), first\_page).
      - On failure (Platform.PermissionError) bound to e.
        - Evaluate publish\_failure(task\_id, e).
        - Propagate the active failure.
      - On failure (Exception).
        - Evaluate Platform.log\_error(title = “Error in Multi PDF download”, reference\_doctype = doctype\_name, reference\_name = doc\_name).
        - Evaluate failed.append(get\_link\_to\_form(doctype\_name, doc\_name)).
      - Update count using + 1.
      - If task\_id.
        - Evaluate Platform.publish\_progress(percent = ((count ÷ total\_docs) × 100), title = translated “PDF Generation in Progress”, description = translated “{0}/{1} complete \| Please leave this tab open until completion.” ….
  - If task\_id is identical to no value.
    - Set Platform.local.response.filename from formatted text {name}.pdf.
- If password bound to (options or mapping()).get(“password”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → mapping().
  - Evaluate pdf\_writer.encrypt(password).
- Within BytesIO() bound as merged\_pdf.
  - Evaluate pdf\_writer.write(merged\_pdf).
  - If task\_id.
    - Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text {filename}{task\_id}.pdf, “content” → merged\_pdf.getvalue(), “is\_private” → 1)).
    - Evaluate \_file.save().
    - Evaluate Platform.publish\_realtime(formatted text task\_complete:{task\_id}, message = mapping(“file\_url” → \_file.unique\_url), user = Platform.session.user).
  - Otherwise.
    - Set Platform.local.response.filecontent from merged\_pdf.getvalue().
    - Set Platform.local.response.type from “pdf”.
- If failed.
  - Evaluate Platform.msgprint(failed, as\_list = true, indicator = “red”, realtime = true, title = translated “Failed to print {0} documents”.format(len(failed))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(formatted text task\_complete:{task\_id}, message = mapping(“file\_url” → \_file.unique\_url), user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L29) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L477)

<a id="op-7bf335872e7575"></a>
### Download multi pdf.print into writer

`operation_foundation_utils_print_format_business_behavior_download_multi_portable_document_print_into_writer`

**Inputs** print\_doctype, print\_name.

**Explicit results** \_print\_into\_writer(print\_doctype, print\_name).

**Local steps**

- Within print\_language(format\_language).
  - Return \_print\_into\_writer(print\_doctype, print\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L31) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L479)

<a id="op-32b732d56229fb"></a>
### Download multi pdf.print into writer

`operation_foundation_binding_foundation_utils_print_format_download_multi_pdf_print_into_writer`

**Inputs** print\_doctype, print\_name.

**Record and data access** resolve a document from print\_doctype via get\_doc.

**Explicit results** Platform.get\_print(print\_doctype, print\_name, format, as\_pdf = true, output = pdf\_writer, no\_letterhead = no\_letterhead, letterhead = letterhead, …) · pdf\_writer.

**Local steps**

- Bind dependencies \_print\_format\_doc\_or\_none, \_run\_print\_pdf\_hooks, renders\_through\_generator.
- Set pf\_doc from \_print\_format\_doc\_or\_none(format).
- If not renders\_through\_generator(pf\_doc).
  - Return Platform.get\_print(print\_doctype, print\_name, format, as\_pdf = true, output = pdf\_writer, no\_letterhead = no\_letterhead, letterhead = letterhead, …).
- Bind dependencies PdfReader.
- Bind dependencies uses\_legacy\_weasyprint.
- Bind dependencies PrintFormatGenerator.
- Bind dependencies set\_link\_titles, validate\_print.
- Set doc from Platform.get\_doc(print\_doctype, print\_name).
- Evaluate validate\_print(doc).
- Evaluate \_run\_print\_pdf\_hooks(print\_doctype, print\_name, format).
- If uses\_legacy\_weasyprint(pf\_doc).
  - Bind dependencies legacy\_generator.
  - Set pdf from legacy\_generator(pf\_doc, doc, letterhead).render\_pdf().
- Otherwise.
  - Evaluate set\_link\_titles(doc).
  - Set generator from PrintFormatGenerator(pf\_doc, doc, letterhead, no\_letterhead = no\_letterhead, settings = page\_settings(options)).
  - Set pdf from generator.render\_pdf().
- Evaluate make\_access\_log(doctype = doc.doctype, document = doc.name, file\_type = “PDF”, method = “Print”, …).
- For each page in PdfReader(BytesIO(pdf)).pages.
  - Evaluate pdf\_writer.add\_page(page).
- Return pdf\_writer.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L164) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L322)

<a id="op-28d7ead274aeb7"></a>
### Download pdf

`operation_foundation_utils_print_format_business_behavior_download_portable_document`

**Inputs** doctype, name, format = no value, doc = no value, no\_letterhead = 0, language = no value, letterhead = no value, pdf\_generator = no value, style = no value, settings = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), Platform.concurrent\_limit().

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Set doc from (doc or Platform.get\_doc(doctype, name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → Platform.get\_doc(doctype, name).
- Evaluate validate\_print\_permission(doc).
- Within print\_language(language).
  - Set pdf\_file from Platform.get\_print(doctype, name, format, doc = doc, as\_pdf = true, letterhead = letterhead, no\_letterhead = no\_letterhead, …).
- Set Platform.local.response.filename from “{name}.pdf”.format(name = name.replace(one space, “-”).replace(“/”, “-”)).
- Set Platform.local.response.filecontent from pdf\_file.
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L32) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L480)

<a id="op-04b1dac1e98eb0"></a>
### Report to pdf

`operation_foundation_utils_print_format_business_behavior_report_to_portable_document`

**Inputs** html, orientation = “Landscape”.

**Wrappers, in declaration order** Platform.whitelist(), Platform.concurrent\_limit().

**Local steps**

- Evaluate make\_access\_log(file\_type = “PDF”, method = “PDF”, page = html).
- Set Platform.local.response.filename from “report.pdf”.
- Set Platform.local.response.filecontent from get\_pdf(html, mapping(“orientation” → orientation, “proxy” → text in the contract, “bypass-proxy-for” → \_pdf\_bypass\_proxy\_hosts(), “load-error-handling” → “ignore”), smart\_shrinking = true).
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L6466) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L485)

<a id="op-c7d541c504ae4f"></a>
### Pdf bypass proxy hosts

`operation_foundation_utils_print_format_business_behavior_portable_document_bypass_proxy_hosts`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** sorted(hosts).

**Local steps**

- Set hosts from set(\_hostname(Platform.utils.get\_url(allow\_header\_override = false))).
- Evaluate hosts.update(generator of \_hostname(domain at “domain” when isinstance(domain, dict), otherwise domain) for domain drawn from (Platform.conf.domains or list())).
  - Draw domain from (Platform.conf.domains or list()).
  - Value choice on isinstance(domain, dict) — true gives domain at “domain”, false gives domain.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.domains → list().
- Evaluate hosts.discard(no value).
- Return sorted(hosts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L33) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L482)

<a id="op-cd74ab1e4b4d80"></a>
### Hostname

`operation_foundation_utils_print_format_business_behavior_hostname`

**Inputs** value.

**Declared result** (str bitwise or no value).

**Explicit results** urlparse(value).hostname.

**Local steps**

- If “://” does not belong to value.
  - Set value from (“//” + value).
- Return urlparse(value).hostname.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0493.json#L6971) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L481)

<a id="op-6e48d08eea7a9e"></a>
### Render letterhead for print

`operation_foundation_utils_print_format_business_behavior_render_letterhead_for_print`

**Inputs** letterhead = no value, doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Letter Head” via get\_value.

**Explicit results** mapping() · rendered.

**Local steps**

- If not Platform.has\_permission(“Letter Head”, “read”).
  - Return mapping().
- If isinstance(doc, str).
  - Attempt the following.
    - Set doc from json.loads(doc).
  - On failure (Exception).
    - Set doc from mapping().
- Set letter\_head from Platform.\_dict((Platform.db.get\_value(“Letter Head”, (letterhead or mapping(“is\_default” → 1)), list(“content”, “footer”, “header\_script”, “footer\_script”), as\_dict = true) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Letter Head”, (letterhead or mapping(“is\_default” → 1)), list(“content”, “footer”, “header\_script”, “footer\_script”), as\_dict = true) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in letterhead → mapping(“is\_default” → 1).
- Bind dependencies BeautifulSoup.
- Set context\_doc from Platform.\_dict((doc or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → mapping().
- Set rendered from mapping().
- If letter\_head.content.
  - Set header from render\_template(letter\_head.content, mapping(“doc” → context\_doc)).
  - Set header from str(BeautifulSoup(header, “html.parser”)).
  - If letter\_head.header\_script.
    - Update header using + formatted text  &lt;script&gt; {letter\_head.header\_script} &lt;/script&gt;.
  - Set rendered at “header” from header.
- If letter\_head.footer.
  - Set footer from render\_template(letter\_head.footer, mapping(“doc” → context\_doc)).
  - Set footer from str(BeautifulSoup(footer, “html.parser”)).
  - If letter\_head.footer\_script.
    - Update footer using + formatted text  &lt;script&gt; {letter\_head.footer\_script} &lt;/script&gt;.
  - Set rendered at “footer” from footer.
- Return rendered.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Letter Head”, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L35) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L484)

<a id="op-3fbe870b166af7"></a>
### Render report jinja

`operation_foundation_binding_foundation_utils_print_format_render_report_jinja`

**Inputs** print\_format, data = no value, columns = no value, filters = no value, letterhead = no value, no\_letterhead = 0.

**Wrappers, in declaration order** Platform.whitelist(), Platform.read\_only().

**Declared result** dict.

**Record and data access** read “Print Settings” via get\_single.

**Explicit results** mapping(“body” → body, “letter\_head” → letter\_head).

**Explicit failure paths** validation helper — translated “Print Format {0} is not a Jinja format”.format(print\_format) · validation helper — translated “Print Format {0} has no HTML body”.format(print\_format).

**Local steps**

- Set pf from get\_permitted\_report\_print\_format(print\_format).
- If pf.print\_format\_type differs from “Jinja”.
  - Call the validation error handler Platform.throw(translated “Print Format {0} is not a Jinja format”.format(print\_format)).
- If not pf.html.
  - Call the validation error handler Platform.throw(translated “Print Format {0} has no HTML body”.format(print\_format)).
- Set filters from Platform.parse\_json((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set rows from Platform.parse\_json((data or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → list().
- Set cols from Platform.parse\_json((columns or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in columns → list().
- Set rows from list of Platform.\_dict(row) when isinstance(row, dict), otherwise row for row drawn from rows.
  - Draw row from rows.
  - Value choice on isinstance(row, dict) — true gives Platform.\_dict(row), false gives row.
- Set context from mapping(“report” → Platform.\_dict(name = pf.report, report\_name = pf.report), “filters” → filters, “columns” → cols, “data” → rows, …).
- Set html from render\_template(pf.html, context, safe\_render = true).
- Set body from formatted text &lt;style&gt;{(pf.css or empty text)}&lt;/style&gt;{html}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pf.css → empty text.
- Set letter\_head from no value when cint(no\_letterhead), otherwise (render\_letterhead\_for\_print(letterhead = letterhead, doc = filters) or no value).
  - Value choice on cint(no\_letterhead) — true gives no value, false gives (render\_letterhead\_for\_print(letterhead = letterhead, doc = filters) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in render\_letterhead\_for\_print(letterhead = letterhead, doc = filters) → no value.
- Return mapping(“body” → body, “letter\_head” → letter\_head).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L195) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L353)

<a id="op-dbd7a0f710187f"></a>
### Download report pdf

`operation_foundation_binding_foundation_utils_print_format_download_report_pdf`

**Inputs** report\_name, filters = no value, orientation = “Landscape”, print\_format = no value, letterhead = no value, no\_letterhead = 0, columns = no value, visible\_idx = no value, custom\_columns = no value, applied\_filters = no value, ignore\_prepared\_report = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)), Platform.concurrent\_limit().

**Declared result** no value.

**Record and data access** read “Print Format” via get\_value · read “Report” via get\_cached\_value · read “User” via get\_cached\_value · read “Print Settings” via get\_single.

**Explicit failure paths** validation helper — translated “Print Format {0} does not belong to report {1}”.format(Platform.bold(print\_format), Platform.bold(translated report\_name)) · validation helper with Platform.PermissionError — translated “You don't have permission to print: {0}”.format(translated ref\_doctype) · validation helper — translated “No data to export”.

**Local steps**

- Bind dependencies numeric\_fieldtypes.
- Bind dependencies get\_print\_style.
- Set filters from (Platform.parse\_json(filters) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → mapping().
- Set visible\_idx from (Platform.parse\_json(visible\_idx) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(visible\_idx) → list().
- If (print\_format and Platform.db.get\_value(“Print Format”, print\_format, “report”) differs from report\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → Platform.db.get\_value(“Print Format”, print\_format, “report”) differs from report\_name.
  - Call the validation error handler Platform.throw(translated “Print Format {0} does not belong to report {1}”.format(Platform.bold(print\_format), Platform.bold(translated report\_name)), title = translated “Invalid Print Format”).
- Set ref\_doctype from Platform.get\_cached\_value(“Report”, report\_name, “ref\_doctype”).
- If not Platform.has\_permission(ref\_doctype, “print”).
  - Call the validation error handler Platform.throw(translated “You don't have permission to print: {0}”.format(translated ref\_doctype), Platform.PermissionError).
- Set data from Platform.\_dict(run(report\_name, filters, ignore\_prepared\_report = ignore\_prepared\_report, custom\_columns = Platform.parse\_json(custom\_columns), are\_default\_filters = false)).
- If not data.columns.
  - Call the validation error handler Platform.throw(translated “No data to export”, title = translated “No Data”).
- Evaluate make\_access\_log(report\_name = report\_name, filters = filters, file\_type = “PDF”, method = “Print”).
- Set report\_columns from list of get\_column\_as\_dict(column) for column drawn from data.columns.
  - Draw column from data.columns.
- Set masked\_fields from set of field.fieldname for field drawn from Platform.get\_meta(ref\_doctype).get\_masked\_fields().
  - Draw field from Platform.get\_meta(ref\_doctype).get\_masked\_fields().
- For each column in report\_columns.
  - If column.fieldname belongs to masked\_fields.
    - Evaluate column.update(fieldtype = “Data”, options = no value).
- Set total\_row from data.result.pop() when (cint(data.add\_total\_row) and data.result), otherwise no value.
  - Value choice on (cint(data.add\_total\_row) and data.result) — true gives data.result.pop(), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(data.add\_total\_row) → data.result.
- Set rows from normalize\_result((data.result or list()), report\_columns).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.result → list().
- If visible\_idx.
  - Set numbered\_rows from list of tuple((index + 1), rows at index) for index drawn from visible\_idx where 0 ≤ index &lt; len(rows).
    - Draw index from visible\_idx, keep a combination only if (0 ≤ index &lt; len(rows)).
    - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ index &lt; len(rows).
  - If total\_row.
    - Set total\_row from (numbered\_rows and add\_total\_row(list of row for tuple(\_, row) drawn from numbered\_rows, report\_columns) at negative 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in numbered\_rows → add\_total\_row(list of row for tuple(\_, row) drawn from numbered\_rows, report\_columns) at negative 1.
      - Draw tuple(\_, row) from numbered\_rows.
- Otherwise.
  - Set numbered\_rows from list(enumerate(rows, start = 1)).
- If total\_row.
  - Set fieldnames from list of column.fieldname for column drawn from report\_columns.
    - Draw column from report\_columns.
  - Evaluate numbered\_rows.append(tuple(no value, Platform.\_dict(zip(fieldnames, total\_row, strict = false), is\_total\_row = true))).
- If print\_format.
  - Set rendered from render\_report\_jinja(print\_format, data = list of row for tuple(\_, row) drawn from numbered\_rows, columns = report\_columns, filters = filters, letterhead = letterhead, …).
    - Draw tuple(\_, row) from numbered\_rows.
  - Set tuple(content, letter\_head) from tuple(rendered at “body”, rendered at “letter\_head”).
  - Set printed\_columns from report\_columns.
- Otherwise.
  - Set system\_time\_zone from ZoneInfo(get\_system\_timezone()).
  - Set user\_time\_zone from ZoneInfo((Platform.get\_cached\_value(“User”, Platform.session.user, “time\_zone”) or get\_system\_timezone())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“User”, Platform.session.user, “time\_zone”) → get\_system\_timezone().
  - Bind local operation format\_value for subsequent calls.
  - Set columns from Platform.parse\_json(columns).
  - Set printed\_columns from list of column for fieldname drawn from columns, then column drawn from report\_columns where column.fieldname equals fieldname when columns, otherwise list of column for column drawn from report\_columns wh ….
    - Value choice on columns — true gives list of column for fieldname drawn from columns, then column drawn from report\_columns where column.fieldname equals fieldname, false gives list of column for column drawn from report\_columns where not column.hidden.
    - Draw fieldname from columns.
    - Draw column from report\_columns, keep a combination only if (column.fieldname equals fieldname).
    - Draw column from report\_columns, keep a combination only if (not column.hidden).
  - Set letter\_head from no value when cint(no\_letterhead), otherwise render\_letterhead\_for\_print(letterhead, (filters bitwise or mapping(“company” → (nested operand in the contract.get(“company”) or nested operand in the contract ….
    - Value choice on cint(no\_letterhead) — true gives no value, false gives render\_letterhead\_for\_print(letterhead, (filters bitwise or mapping(“company” → (filters.get(“company”) or nested operand in the contract.defaults.get\_user\_default(“company”))))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → Platform.defaults.get\_user\_default(“company”).
  - Set content from Platform.get\_template(“templates/print\_formats/report\_print\_grid.html”).render(mapping(“title” → report\_name, “applied\_filters” → mapping of label → format\_filter\_value(value) for tuple(label, value) drawn ….
    - Draw tuple(label, value) from (Platform.parse\_json(applied\_filters) or mapping()).items().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(applied\_filters) → mapping().
    - Value choice on numbered\_rows — true gives numbered\_rows at 0 at 1, false gives no value.
    - Draw tuple(\_, row) from numbered\_rows.
- Set print\_settings from Platform.get\_single(“Print Settings”).
- Set html from Platform.get\_template(“templates/print\_formats/report\_print\_template.html”).render(mapping(“title” → translated report\_name, “lang” → Platform.local.lang, “landscape” → orientation equals “Landscape”, “pri ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_settings.print\_style → “Redesign”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(printed\_columns) &gt; 20 → (not print\_format or Platform.get\_cached\_value(“Report”, report\_name, “is\_standard”) differs from “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → Platform.get\_cached\_value(“Report”, report\_name, “is\_standard”) differs from “Yes”.
- Set Platform.local.response.filename from formatted text {report\_name}.pdf.
- Set Platform.local.response.filecontent from get\_pdf(html, mapping(“orientation” → orientation, “block-external-requests” → true, “shrink-to-fit” → true)).
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Report”, report\_name, “ref\_doctype”), Platform.get\_cached\_value(“User”, Platform.session.user, “time\_zone”) and 1 further calls · effective access from Platform.has\_permission(ref\_doctype, “print”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L165) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L323)

<a id="op-de4d3c63b21355"></a>
### Download report pdf.format value

`operation_foundation_binding_foundation_utils_print_format_download_report_pdf_format_value`

**Inputs** value, column, row.

**Explicit results** Platform.format(value, column, row) · value.

**Local steps**

- Attempt the following.
  - If column.fieldtype equals “Datetime”.
    - Set value from nested operand in the contract(nested operand in the contract).replace(tzinfo = system\_time\_zone).astimezone(user\_time\_zone).replace(tzinfo = no value).
  - Return Platform.format(value, column, row).
- On failure (tuple(Platform.ValidationError, ValueError, TypeError)).
  - Return value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L166) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L324)

<a id="op-c9328dd9ef06f8"></a>
### Print by server

`operation_foundation_utils_print_format_business_behavior_print_by_server`

**Inputs** doctype, name, printer\_setting, print\_format = no value, doc = no value, no\_letterhead = 0, file\_path = no value, style = no value, settings = no value, letterhead = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Network Printer Settings” via get\_doc.

**Explicit failure paths** validation helper — translated “You need to install pycups to use this feature!” · validation helper — translated “Printing failed”.

**Local steps**

- Set print\_settings from Platform.get\_doc(“Network Printer Settings”, printer\_setting).
- Attempt the following.
  - Bind dependencies cups.
- On failure (ImportError).
  - Call the validation error handler Platform.throw(translated “You need to install pycups to use this feature!”).
- Set file\_path from no value.
- Attempt the following.
  - Evaluate cups.setServer(print\_settings.server\_ip).
  - Evaluate cups.setPort(print\_settings.port).
  - Set conn from cups.Connection().
  - Bind dependencies PdfWriter.
  - Set output from PdfWriter().
  - Set output from Platform.get\_print(doctype, name, print\_format, style = style, doc = doc, no\_letterhead = no\_letterhead, letterhead = letterhead, …).
  - Within tempfile.NamedTemporaryFile(prefix = “Platform-pdf-”, suffix = “.pdf”, delete = false) bound as f.
    - Set file\_path from f.name.
    - Evaluate output.write(f).
  - Evaluate conn.printFile(print\_settings.printer\_name, file\_path, name, mapping()).
- On failure (cups.IPPError).
  - Call the validation error handler Platform.throw(translated “Printing failed”).
- On exit, including pending return or failure.
  - If file\_path.
    - Evaluate os.remove(file\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L34) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L483)

## Service · Print format generator

<a id="op-82bfa3cefdbe29"></a>
### Render jinja template

`operation_foundation_utils_print_format_generator_business_behavior_render_document_template_template`

**Inputs** template, doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** Platform.render\_template(template, mapping(“doc” → doc)).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Failed to render template: {0}”.format(str(e)).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate doc.check\_permission(“print”).
- Attempt the following.
  - Return Platform.render\_template(template, mapping(“doc” → doc)).
- On failure (Exception) bound to e.
  - Evaluate Platform.clear\_last\_message().
  - Call the validation error handler Platform.throw(translated “Failed to render template: {0}”.format(str(e)), Platform.ValidationError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”), doc.check\_permission(“print”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L1625) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L528)

<a id="op-982fccf52ae21f"></a>
### Download pdf

`operation_foundation_utils_print_format_generator_business_behavior_download_portable_document`

**Inputs** doctype, name, print\_format = no value, letterhead = no value, settings = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.concurrent\_limit().

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** download\_jinja\_pdf(doctype, cstr(name), format = print\_format.name when print\_format, otherwise no value, letterhead = letterhead).

**Local steps**

- Bind dependencies make\_access\_log.
- Bind dependencies \_run\_print\_pdf\_hooks.
- Bind dependencies resolve\_print\_format, validate\_print.
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate validate\_print(doc).
- Set tuple(print\_format, is\_beta) from resolve\_print\_format(print\_format, doc.meta).
- If not is\_beta.
  - Bind dependencies download\_jinja\_pdf.
  - Return download\_jinja\_pdf(doctype, cstr(name), format = print\_format.name when print\_format, otherwise no value, letterhead = letterhead).
    - Value choice on print\_format — true gives print\_format.name, false gives no value.
- Evaluate \_run\_print\_pdf\_hooks(doctype, name, print\_format.name).
- If uses\_legacy\_weasyprint(print\_format).
  - Bind dependencies legacy\_generator.
  - Set pdf from legacy\_generator(print\_format, doc, letterhead).render\_pdf().
- Otherwise.
  - Set generator from PrintFormatGenerator(print\_format, doc, letterhead, settings = Platform.parse\_json(settings)).
  - Set pdf from generator.render\_pdf().
- Evaluate make\_access\_log(doctype = doc.doctype, document = doc.name, file\_type = “PDF”, method = “Print”, …).
- Set Platform.local.response.filename from “{name}.pdf”.format(name = cstr(name).replace(one space, “-”).replace(“/”, “-”)).
- Set Platform.local.response.filecontent from pdf.
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L37) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L488)

<a id="op-d2746df09193db"></a>
### Get print context

`operation_foundation_binding_foundation_utils_print_format_generator_get_print_context`

**Inputs** no declared parameters.

**Explicit results** getattr(Platform.local, “print\_context”, no value).

**Local steps**

- Return getattr(Platform.local, “print\_context”, no value).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “print\_context”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L174) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L332)

<a id="op-a26418cd494418"></a>
### Set print context

`operation_foundation_binding_foundation_utils_print_format_generator_set_print_context`

**Inputs** remaining named values values.

**Explicit results** previous.

**Local steps**

- Set previous from get\_print\_context().
- Set Platform.local.print\_context from Platform.\_dict(values).
- Return previous.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L188) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L346)

<a id="op-0da24f09db6cc8"></a>
### Restore print context

`operation_foundation_binding_foundation_utils_print_format_generator_restore_print_context`

**Inputs** previous.

**Local steps**

- If previous is identical to no value.
  - Set Platform.local.print\_context from no value.
- Otherwise.
  - Set Platform.local.print\_context from previous.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L187) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L345)

<a id="op-8760aba55cbea0"></a>
### Generator from print context

`operation_foundation_binding_foundation_utils_print_format_generator_generator_from_print_context`

**Inputs** print\_format.

**Declared result** “PrintFormatGenerator \| None”.

**Record and data access** resolve a document from “Print Format” via get\_doc · resolve a document from ctx.doctype via get\_doc.

**Explicit results** ctx.generator · no value · PrintFormatGenerator(pf, doc, ctx.get(“letterhead”), settings = Platform.parse\_json(ctx.get(“settings”)) when ctx.get(“settings”), otherwise no value, no\_letterhead = ctx.get(“no\_letterhead”)).

**Local steps**

- Bind dependencies Document.
- Set ctx from get\_print\_context().
- If ctx is identical to no value.
  - Set ctx from Platform.\_dict(Platform.form\_dict).
  - Evaluate ctx.pop(“generator”, no value).
- If ctx.get(“generator”).
  - Return ctx.generator.
- If (not print\_format or not ctx.get(“doctype”) or not ctx.get(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → not ctx.get(“doctype”) → not ctx.get(“name”).
  - Return no value.
- Set pf from Platform.get\_doc(“Print Format”, print\_format).
- If not pf.get(“print\_format\_builder\_beta”).
  - Return no value.
- Set doc from ctx.get(“doc”).
- If not isinstance(doc, Document).
  - Set doc from Platform.get\_doc(ctx.doctype, ctx.name).
- Return PrintFormatGenerator(pf, doc, ctx.get(“letterhead”), settings = Platform.parse\_json(ctx.get(“settings”)) when ctx.get(“settings”), otherwise no value, no\_letterhead = ctx.get(“no\_letterhead”)).
  - Value choice on ctx.get(“settings”) — true gives Platform.parse\_json(ctx.get(“settings”)), false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L172) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L330)

<a id="op-43063465ae91dd"></a>
### Render html pdf

`operation_foundation_binding_foundation_utils_print_format_generator_render_html_pdf`

**Inputs** print\_format, html, options, pdf\_generator.

**Explicit results** render(print\_format = print\_format, html = html, options = options, output = no value, …).

**Local steps**

- Bind dependencies get\_chrome\_pdf, get\_plutoprint\_pdf.
- Set render from get\_plutoprint\_pdf when pdf\_generator equals “PlutoPrint”, otherwise get\_chrome\_pdf.
  - Value choice on pdf\_generator equals “PlutoPrint” — true gives get\_plutoprint\_pdf, false gives get\_chrome\_pdf.
- Return render(print\_format = print\_format, html = html, options = options, output = no value, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L186) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L344)

<a id="op-6aa2e4062a0b84"></a>
### Get typst pdf

`operation_foundation_utils_print_format_generator_business_behavior_get_typst_portable_document`

**Inputs** print\_format, html, options, output, pdf\_generator = no value.

**Explicit results** no value · generator.render\_typst\_pdf(password = (options or mapping()).get(“password”)).

**Local steps**

- If pdf\_generator differs from “Typst”.
  - Return no value.
- Set generator from generator\_from\_print\_context(print\_format).
- If generator is identical to no value.
  - Return no value.
- Return generator.render\_typst\_pdf(password = (options or mapping()).get(“password”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L39) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L494)

<a id="op-83af1cd9e4f05e"></a>
### Classic layout message

`operation_foundation_binding_foundation_utils_print_format_generator_classic_layout_message`

**Inputs** no declared parameters.

**Explicit results** translated “This format still has a classic layout. Convert it to the new builder first.”.

**Local steps**

- Return translated “This format still has a classic layout. Convert it to the new builder first.”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L169) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L327)

<a id="op-a15123b9a5213c"></a>
### Zone from html

`operation_foundation_binding_foundation_utils_print_format_generator_zone_from_html`

**Inputs** html.

**Declared result** dict.

**Explicit results** mapping(“columns” → list(mapping(“label” → empty text, “fields” → fields))).

**Local steps**

- Set fields from list().
- If (isinstance(html, str) and html.strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(html, str) → html.strip().
  - Evaluate fields.append(mapping(“fieldtype” → “HTML”, “fieldname” → “\_zone\_html”, “label” → empty text, “html” → html)).
- Return mapping(“columns” → list(mapping(“label” → empty text, “fields” → fields))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L189) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L347)

<a id="op-8839a477ad478a"></a>
### Is qr barcode options

`operation_foundation_utils_print_format_generator_business_behavior_is_quick_response_barcode_options`

**Inputs** options.

**Declared result** bool.

**Explicit results** true · nested operand in the contract.loads(options).get(“format”, empty text).lower() belongs to tuple(“qr”, “qrcode”) · false.

**Local steps**

- Bind dependencies json.
- Set options from (options or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → empty text.
- If options.lower() belongs to tuple(“qr”, “qrcode”).
  - Return true.
- Attempt the following.
  - Return nested operand in the contract.loads(options).get(“format”, empty text).lower() belongs to tuple(“qr”, “qrcode”).
- On failure (Exception).
  - Return false.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L3094) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L495)

<a id="op-d18d2251b511ce"></a>
### Get qr code

`operation_foundation_utils_print_format_generator_business_behavior_get_quick_response_code`

**Inputs** value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** (“data:image/svg+xml;base64,” + base64.b64encode(stream.getvalue()).decode()).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Barcode value must be text under 2000 characters”.

**Local steps**

- Bind dependencies base64.
- Bind dependencies io.
- If (not isinstance(value, str) or len(value) &gt; 2000).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(value, str) → len(value) &gt; 2000.
  - Call the validation error handler Platform.throw(translated “Barcode value must be text under 2000 characters”, Platform.ValidationError).
- Bind dependencies qrcreate.
- Set stream from io.BytesIO().
- Evaluate qrcreate(value).svg(stream, scale = 5, quiet\_zone = 1).
- Return (“data:image/svg+xml;base64,” + base64.b64encode(stream.getvalue()).decode()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L38) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L493)
