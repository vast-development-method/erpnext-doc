# Forms, reports and navigation · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Printview

<a id="op-4865dab0ef5b38"></a>
### Set link titles

`operation_foundation_public_pages_printview_business_behavior_set_link_titles`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- If not doc.get(“\_\_link\_titles”).
  - Evaluate setattr(doc, “\_\_link\_titles”, mapping()).
- Set meta from Platform.get\_meta(doc.doctype).
- Evaluate set\_title\_values\_for\_link\_and\_dynamic\_link\_fields(meta, doc).
- Evaluate set\_title\_values\_for\_table\_and\_multiselect\_fields(meta, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0546.json#L5846) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L77)

<a id="op-ddcb73e5750b5c"></a>
### Set title values for link and dynamic link fields

`operation_foundation_public_pages_printview_business_behavior_set_title_values_for_link_and_dynamic_link_fields`

**Inputs** meta, doc, parent\_doc = no value.

**Declared result** no value.

**Record and data access** read doctype via get\_cached\_value.

**Local steps**

- If (parent\_doc and not parent\_doc.get(“\_\_link\_titles”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doc → not parent\_doc.get(“\_\_link\_titles”).
  - Evaluate setattr(parent\_doc, “\_\_link\_titles”, mapping()).
- Otherwise.
  - If (doc and not doc.get(“\_\_link\_titles”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → not doc.get(“\_\_link\_titles”).
    - Evaluate setattr(doc, “\_\_link\_titles”, mapping()).
- For each field in (meta.get\_link\_fields() + meta.get\_dynamic\_link\_fields()).
  - If not doc.get(field.fieldname).
    - Continue with the next iteration or loop test.
  - Set doctype from field.options when field.fieldtype equals “Link”, otherwise doc.get(field.options).
    - Value choice on field.fieldtype equals “Link” — true gives field.options, false gives doc.get(field.options).
  - Set meta from Platform.get\_meta(doctype).
  - If (not meta or not meta.title\_field or not meta.show\_title\_field\_in\_link).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta → not meta.title\_field → not meta.show\_title\_field\_in\_link.
    - Continue with the next iteration or loop test.
  - Set link\_title from Platform.get\_cached\_value(doctype, doc.get(field.fieldname), meta.title\_field).
  - If parent\_doc.
    - Set parent\_doc.\_\_link\_titles at formatted text {doctype}::{doc.get(field.fieldname)} from link\_title.
  - Otherwise.
    - If doc.
      - Set doc.\_\_link\_titles at formatted text {doctype}::{doc.get(field.fieldname)} from link\_title.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doctype, doc.get(field.fieldname), meta.title\_field).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0546.json#L6026) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L78)

<a id="op-a4432bfd77e0c9"></a>
### Set title values for table and multiselect fields

`operation_foundation_public_pages_printview_business_behavior_set_title_values_for_table_and_multiselect_fields`

**Inputs** meta, doc.

**Declared result** no value.

**Local steps**

- For each field in meta.get\_table\_fields(include\_computed = true).
  - If not doc.get(field.fieldname).
    - Continue with the next iteration or loop test.
  - Set \_meta from Platform.get\_meta(field.options).
  - For each value in doc.get(field.fieldname).
    - Evaluate set\_title\_values\_for\_link\_and\_dynamic\_link\_fields(\_meta, value, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0546.json#L6681) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L79)

<a id="op-9021f996f62807"></a>
### Convert markdown

`operation_foundation_public_pages_printview_business_behavior_convert_markdown`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- For each field in doc.meta.fields.
  - If field.fieldtype equals “Text Editor”.
    - Set value from doc.get(field.fieldname).
    - If (value and “&lt;!-- markdown --&gt;” belongs to value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → “&lt;!-- markdown --&gt;” belongs to value.
      - Evaluate doc.set(field.fieldname, Platform.utils.md\_to\_html(value)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0546.json#L6905) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L57)

<a id="op-4b0350984f018c"></a>
### Get html and style

`operation_foundation_public_pages_printview_business_behavior_get_document_markup_and_style`

**Inputs** doc, name = no value, print\_format = no value, no\_letterhead = no value, letterhead = no value, trigger\_print = false, style = no value, settings = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, (str bitwise or no value)).

**Record and data access** resolve a document from Platform.parse\_json(doc) via get\_doc.

**Explicit results** mapping(“html” → html, “style” → get\_print\_style(style = style, print\_format = print\_format, overrides = overrides), “page\_style” → no value when is\_beta, otherwise get\_preview\_page\_css(print\_format, overrides)).

**Local steps**

- If (isinstance(doc, str) and isinstance(name, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(doc, str) → isinstance(name, str).
  - Set document from Platform.get\_lazy\_doc(doc, name, check\_permission = true).
- Otherwise.
  - Set document from Platform.get\_doc(Platform.parse\_json(doc), check\_permission = true).
  - Evaluate cast\_client\_values(document).
- Set tuple(print\_format, is\_beta) from resolve\_print\_format(print\_format, document.meta).
- Evaluate set\_link\_titles(document).
- If uses\_legacy\_weasyprint(print\_format).
  - Bind dependencies legacy\_generator.
  - Evaluate validate\_print(document).
  - Set html from legacy\_generator(print\_format, document, letterhead).get\_html\_preview().
  - If cint(trigger\_print).
    - Update html using + trigger\_print\_script.
- Otherwise.
  - If is\_beta.
    - Bind dependencies PrintFormatGenerator.
    - Evaluate validate\_print(document).
    - Set generator from PrintFormatGenerator(print\_format, document, letterhead, settings = Platform.parse\_json(settings), no\_letterhead = no\_letterhead).
    - Set html from generator.get\_html\_preview().
  - Otherwise.
    - Attempt the following.
      - Set html from get\_rendered\_template(doc = document, print\_format = print\_format, meta = document.meta, no\_letterhead = no\_letterhead, …).
    - On failure (Platform.TemplateNotFoundError).
      - Evaluate Platform.clear\_last\_message().
      - Set html from no value.
- Set overrides from get\_allowed\_print\_settings\_override(document, Platform.parse\_json(settings)).
- Return mapping(“html” → html, “style” → get\_print\_style(style = style, print\_format = print\_format, overrides = overrides), “page\_style” → no value when is\_beta, otherwise get\_preview\_page\_css(print\_format, overrides)).
  - Value choice on is\_beta — true gives no value, false gives get\_preview\_page\_css(print\_format, overrides).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L72) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L60)

<a id="op-99556d618bec2e"></a>
### Get preview page css

`operation_foundation_binding_foundation_www_printview_get_preview_page_css`

**Inputs** print\_format = no value, overrides = no value.

**Declared result** str.

**Explicit results** Platform.get\_template(“templates/print\_formats/preview\_page.css”).render(mapping(“page\_width” → page\_width, “page\_height” → page\_height, “page\_margin” → get\_page\_margin(print\_format))).

**Local steps**

- Set tuple(page\_width, page\_height) from get\_page\_size\_mm(overrides).
- Return Platform.get\_template(“templates/print\_formats/preview\_page.css”).render(mapping(“page\_width” → page\_width, “page\_height” → page\_height, “page\_margin” → get\_page\_margin(print\_format))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L85) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L478)

<a id="op-31a5d5daeab055"></a>
### Get rendered raw commands

`operation_foundation_public_pages_printview_business_behavior_get_rendered_raw_commands`

**Inputs** doc, name = no value, print\_format = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from Platform.parse\_json(doc) via get\_doc.

**Explicit results** mapping(“raw\_commands” → get\_rendered\_template(doc = document, print\_format = print\_format, meta = document.meta)).

**Explicit failure paths** validation helper with Platform.TemplateNotFoundError — translated “{0} is not a raw printing format.”.format(print\_format).

**Local steps**

- If (isinstance(doc, str) and isinstance(name, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(doc, str) → isinstance(name, str).
  - Set document from Platform.get\_lazy\_doc(doc, name, check\_permission = true).
- Otherwise.
  - Set document from Platform.get\_doc(Platform.parse\_json(doc), check\_permission = true).
  - Evaluate cast\_client\_values(document).
- Set print\_format from get\_print\_format\_doc(print\_format, meta = document.meta).
- If (not print\_format or (print\_format and not print\_format.raw\_printing)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → (print\_format and not print\_format.raw\_printing).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → not print\_format.raw\_printing.
  - Call the validation error handler Platform.throw(translated “{0} is not a raw printing format.”.format(print\_format), Platform.TemplateNotFoundError).
- Return mapping(“raw\_commands” → get\_rendered\_template(doc = document, print\_format = print\_format, meta = document.meta)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L76) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L66)

<a id="op-7121e432a93851"></a>
### Get allowed print settings override

`operation_foundation_public_pages_printview_business_behavior_get_allowed_print_settings_override`

**Inputs** doc, settings.

**Declared result** dict.

**Explicit results** mapping() · allowed.

**Local steps**

- If not settings.
  - Return mapping().
- Set doc\_settings from set((doc.get\_print\_settings() or list())) when hasattr(doc, “get\_print\_settings”), otherwise set().
  - Value choice on hasattr(doc, “get\_print\_settings”) — true gives set((doc.get\_print\_settings() or list())), false gives set().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_print\_settings() → list().
- Set page\_sizes from nested operand in the contract.get\_meta(“Print Settings”).get\_field(“pdf\_page\_size”).options.split(whitespace '\\n').
- Set allowed from mapping().
- For each tuple(key, value) in settings.items().
  - If key belongs to doc\_settings.
    - Set allowed at key from cint(value).
  - Otherwise.
    - If key belongs to tuple(“pdf\_page\_height”, “pdf\_page\_width”).
      - Set allowed at key from flt(value).
    - Otherwise.
      - If ((key equals “pdf\_page\_size” and value belongs to page\_sizes) or (key equals “page\_orientation” and value belongs to tuple(empty text, “Portrait”, “Landscape”)) or (key equals “print\_font” and isinstance(v ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (key equals “pdf\_page\_size” and value belongs to page\_sizes) → (key equals “page\_orientation” and value belongs to tuple(empty text, “Portrait”, “Landscape”)) → (key equals “print\_font” and isinstance(value, str) and re.fullmatch(“&#91;A-Za-z0-9 &#93;\*”, value)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in key equals “pdf\_page\_size” → value belongs to page\_sizes.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in key equals “page\_orientation” → value belongs to tuple(empty text, “Portrait”, “Landscape”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in key equals “print\_font” → isinstance(value, str) → re.fullmatch(“&#91;A-Za-z0-9 &#93;\*”, value).
        - Set allowed at key from value.
- Return allowed.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L70) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L58)

<a id="op-91ab3c0ea58f31"></a>
### Validate print for docstatus

`operation_foundation_public_pages_printview_business_behavior_validate_print_for_record_state`

**Inputs** doc, print\_settings = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to print draft documents” · validation helper with Platform.PermissionError — translated “Not allowed to print cancelled documents”.

**Local steps**

- If not doc.meta.is\_submittable.
  - Return no value.
- If print\_settings is identical to no value.
  - Set print\_settings from Platform.get\_cached\_doc(“Print Settings”).as\_dict().
- If (doc.docstatus.is\_draft() and not cint(print\_settings.get(“allow\_print\_for\_draft”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_draft() → not cint(print\_settings.get(“allow\_print\_for\_draft”)).
  - Call the validation error handler Platform.throw(translated “Not allowed to print draft documents”, Platform.PermissionError).
- If (doc.docstatus.is\_cancelled() and not cint(print\_settings.get(“allow\_print\_for\_cancelled”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_cancelled() → not cint(print\_settings.get(“allow\_print\_for\_cancelled”)).
  - Call the validation error handler Platform.throw(translated “Not allowed to print cancelled documents”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L81) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L82)

<a id="op-17781500e690ab"></a>
### Validate print permission

`operation_foundation_public_pages_printview_business_behavior_validate_print_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L82) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L83)

<a id="op-4a700750aba82c"></a>
### Validate print

`operation_foundation_public_pages_printview_business_behavior_validate_print`

**Inputs** doc, print\_settings = no value.

**Declared result** no value.

**Local steps**

- Evaluate validate\_print\_permission(doc).
- Evaluate validate\_print\_for\_docstatus(doc, print\_settings).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L1602) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L81)

<a id="op-0fae8e7d11ecd0"></a>
### Run before print

`operation_foundation_public_pages_printview_business_behavior_run_before_print`

**Inputs** doc, print\_settings.

**Declared result** no value.

**Local steps**

- Set doc.flags.in\_print from true.
- Set doc.flags.print\_settings from print\_settings.
- Evaluate set\_link\_titles(doc).
- Evaluate doc.run\_method(“before\_print”, print\_settings).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“before\_print”, print\_settings).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L80) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L76)

<a id="op-fa94467334caf2"></a>
### Validate key

`operation_foundation_public_pages_printview_business_behavior_validate_key`

**Inputs** key, doc.

**Declared result** no value.

**Record and data access** read “Document Share Key” via get\_cached\_value.

**Explicit results** no value · false.

**Explicit failure paths** Platform.exceptions.LinkExpired.

**Local steps**

- Set document\_key\_expiry from Platform.get\_cached\_value(“Document Share Key”, mapping(“reference\_doctype” → doc.doctype, “reference\_docname” → doc.name, “key” → key), list(“expires\_on”)).
- If document\_key\_expiry is distinct from no value.
  - If is\_expired(document\_key\_expiry at 0).
    - Raise Platform.exceptions.LinkExpired.
  - Otherwise.
    - Return no value.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Document Share Key”, mapping(“reference\_doctype” → doc.doctype, “reference\_docname” → doc.name, “key” → key), list(“expires\_on”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L1830) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L80)

<a id="op-984d6afb517f40"></a>
### Get letter head

`operation_foundation_public_pages_printview_business_behavior_get_letter_head`

**Inputs** doc, no\_letterhead, letterhead = no value.

**Declared result** dict.

**Record and data access** read “Letter Head” via get\_value.

**Explicit results** mapping() · Platform.db.get\_value(“Letter Head”, letterhead\_name, list(“content”, “footer”, “header\_script”, “footer\_script”, …), as\_dict = true) · (Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), list(“content”, “footer”, “header\_script”, “footer\_script”, …), as\_dict = true) or mapping()).

**Local steps**

- If no\_letterhead.
  - Return mapping().
- Set letterhead\_name from (letterhead or doc.get(“letter\_head”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in letterhead → doc.get(“letter\_head”).
- If letterhead\_name.
  - Return Platform.db.get\_value(“Letter Head”, letterhead\_name, list(“content”, “footer”, “header\_script”, “footer\_script”, …), as\_dict = true).
- Otherwise.
  - Return (Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), list(“content”, “footer”, “header\_script”, “footer\_script”, …), as\_dict = true) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), list(“content”, “footer”, “header\_script”, “footer\_script”, …), as\_dict = true) → mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L2079) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L62)

<a id="op-b1ac757a7e0974"></a>
### Get print format

`operation_foundation_public_pages_printview_business_behavior_get_print_format`

**Inputs** doctype, print\_format.

**Declared result** str.

**Record and data access** read “DocType” via get\_value · read “Module Def” via get\_cached\_value.

**Explicit results** pffile.read() · print\_format.raw\_commands · print\_format.html.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Print Format {0} is disabled”.format(print\_format.name) · validation helper with Platform.TemplateNotFoundError — translated “No template found at path: {0}”.format(path).

**Local steps**

- If print\_format.disabled.
  - Call the validation error handler Platform.throw(translated “Print Format {0} is disabled”.format(print\_format.name), Platform.DoesNotExistError).
- Set module from (print\_format.module or Platform.db.get\_value(“DocType”, doctype, “module”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.module → Platform.db.get\_value(“DocType”, doctype, “module”).
- Set is\_custom\_module from Platform.get\_cached\_value(“Module Def”, module, “custom”).
- If not is\_custom\_module.
  - Set path from os.path.join(get\_module\_path(module, “Print Format”, print\_format.name), (Platform.scrub(print\_format.name) + “.html”)).
  - If os.path.exists(path).
    - Within open(path) bound as pffile.
      - Return pffile.read().
- If print\_format.raw\_printing.
  - Return print\_format.raw\_commands.
- If print\_format.html.
  - Return print\_format.html.
- Call the validation error handler Platform.throw(translated “No template found at path: {0}”.format(path), Platform.TemplateNotFoundError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Module Def”, module, “custom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L2445) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L63)

<a id="op-d76d4fee1a634e"></a>
### Make layout

`operation_foundation_public_pages_printview_business_behavior_make_layout`

**Inputs** doc, meta, format\_data = no value.

**Declared result** list.

**Explicit results** layout.

**Local steps**

- Set tuple(layout, page) from tuple(list(), list()).
- Evaluate layout.append(page).
- Bind local operation get\_new\_section for subsequent calls.
- Bind local operation append\_empty\_field\_dict\_to\_page\_column for subsequent calls.
- For each df in (format\_data or meta.fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in format\_data → meta.fields.
  - If format\_data.
    - Set df from Platform.\_dict(df).
    - If df.fieldname.
      - Set original from meta.get\_field(df.fieldname).
      - If original.
        - Set newdf from original.as\_dict().
        - Set newdf.hide\_in\_print\_layout from original.get(“hide\_in\_print\_layout”).
        - Evaluate newdf.update(df).
        - Set df from newdf.
    - Set df.print\_hide from 0.
  - If (df.fieldtype equals “Section Break” or page equals list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype equals “Section Break” → page equals list().
    - If len(page) &gt; 1.
      - If not page at negative 1 at “has\_data”.
        - Remove page at negative 1.
    - Set section from get\_new\_section().
    - If (df.fieldtype equals “Section Break” and df.label).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Section Break” → df.label.
      - Set section at “label” from df.label.
    - Evaluate page.append(section).
  - Otherwise.
    - If df.fieldtype equals “Column Break”.
      - Evaluate page at negative 1 at “columns”.append(mapping(“fields” → list())).
    - Otherwise.
      - Evaluate append\_empty\_field\_dict\_to\_page\_column(page).
  - If (df.fieldtype equals “HTML” and df.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “HTML” → df.options.
    - Evaluate doc.set(df.fieldname, true).
  - If (df.fieldtype equals “Signature” and not doc.get(df.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Signature” → not doc.get(df.fieldname).
    - Set placeholder\_image from “/assets/Platform/images/signature-placeholder.png”.
    - Evaluate doc.set(df.fieldname, placeholder\_image).
  - If (is\_visible(df, doc) and has\_value(df, doc)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_visible(df, doc) → has\_value(df, doc).
    - Evaluate append\_empty\_field\_dict\_to\_page\_column(page).
    - Evaluate page at negative nested operand in the contract at “columns” at negative 1 at “fields”.append(df).
    - Set page at negative 1 at “has\_data” from true.
    - If df.fieldtype equals “Table”.
      - Set df.rows from list().
      - Set df.start from 0.
      - Set df.end from no value.
      - For each tuple(i, row) in enumerate(doc.get(df.fieldname)).
        - If row.get(“page\_break”).
          - Set df.end from i.
          - Set page from list(get\_new\_section()).
          - Evaluate layout.append(page).
          - Evaluate append\_empty\_field\_dict\_to\_page\_column(page).
          - Set df from copy.copy(df).
          - Set df.start from i.
          - Set df.end from no value.
          - Evaluate page at negative nested operand in the contract at “columns” at negative 1 at “fields”.append(df).
- Return layout.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L78) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L72)

<a id="op-a4c541f8c2e1d4"></a>
### Make layout.get new section

`operation_foundation_public_pages_printview_business_behavior_make_layout_get_new_section`

**Inputs** no declared parameters.

**Explicit results** mapping(“columns” → list(), “has\_data” → false).

**Local steps**

- Return mapping(“columns” → list(), “has\_data” → false).

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L4603) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L74)

<a id="op-3910bae36a66d8"></a>
### Make layout.append empty field dict to page column

`operation_foundation_public_pages_printview_business_behavior_make_layout_append_empty_field_mapping_to_page_column`

**Inputs** page.

**Local steps**

- If not page at negative 1 at “columns”.
  - Evaluate page at negative 1 at “columns”.append(mapping(“fields” → list())).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L4660) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L73)

<a id="op-3a6a2ab7d063bd"></a>
### Is visible

`operation_foundation_public_pages_printview_business_behavior_is_visible`

**Inputs** df, doc.

**Declared result** bool.

**Explicit results** false · not doc.is\_print\_hide(df.fieldname, df).

**Local steps**

- If df.fieldtype belongs to tuple(“Section Break”, “Column Break”, “Button”).
  - Return false.
- If ((df.permlevel or 0) &gt; 0 and not doc.has\_permlevel\_access\_to(df.fieldname, df)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (df.permlevel or 0) &gt; 0 → not doc.has\_permlevel\_access\_to(df.fieldname, df).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.permlevel → 0.
  - Return false.
- Return not doc.is\_print\_hide(df.fieldname, df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L3000) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L71)

<a id="op-a7e94f533e7b27"></a>
### Has value

`operation_foundation_public_pages_printview_business_behavior_has_value`

**Inputs** df, doc.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set value from doc.get(df.fieldname).
- If value belongs to tuple(no value, empty text).
  - Return false.
- Otherwise.
  - If (isinstance(value, str) and not strip\_html(value).strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → not strip\_html(value).strip().
    - If df.fieldtype belongs to list(“Text”, “Text Editor”).
      - Return true.
    - Return false.
  - Otherwise.
    - If (isinstance(value, list) and not len(value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, list) → not len(value).
      - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L4791) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L70)

<a id="op-c33e43ac89db89"></a>
### Get print style

`operation_foundation_public_pages_printview_business_behavior_get_print_style`

**Inputs** style = no value, print\_format = no value, for\_legacy = false, overrides = no value.

**Declared result** str.

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc · read “Print Style” via get\_value.

**Explicit results** css.

**Local steps**

- Set print\_settings from Platform.get\_cached\_doc(“Print Settings”).
- Set overrides from (overrides or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overrides → mapping().
- Set font from overrides.get(“print\_font”).
- If not style.
  - Set style from (print\_settings.print\_style or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_settings.print\_style → empty text.
- Set context from mapping(“print\_settings” → print\_settings, “print\_style” → style, “font” → get\_font(print\_settings, print\_format, for\_legacy), “page\_margin” → get\_page\_margin(print\_format)).
- Set css from Platform.get\_template(“templates/styles/standard.css”).render(context).
- Set style\_css from (style and Platform.db.get\_value(“Print Style”, mapping(“name” → style, “disabled” → 0), “css”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in style → Platform.db.get\_value(“Print Style”, mapping(“name” → style, “disabled” → 0), “css”).
- If style\_css.
  - Set css from ((css + whitespace '\\n') + style\_css).
- If font.
  - Set font\_url from formatted command or address in the contract.
  - Update css using + formatted text  @import url("{font\_url}");.
  - Update css using + formatted text  .print-format, .print-format :is(div, span, td, th, h1, h2, h3, h4) { font-family: {font}, sans-serif; }.
- If flt(print\_settings.font\_size).
  - Set css from (css + formatted text  .print-format { font-size: {flt(print\_settings.font\_size)}pt; }).
- For each at\_import in list(set(re.findall(“(@import url\\(&#91;^\\)&#93;+\\)&#91;;&#93;?)”, css))).
  - Set css from css.replace(at\_import, empty text).
  - Set css from (at\_import + css).
- If (print\_format and print\_format.css).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → print\_format.css.
  - Update css using + (whitespace '\\n\\n' + print\_format.css).
- If (overrides.get(“pdf\_page\_size”) or overrides.get(“page\_orientation”) equals “Landscape”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overrides.get(“pdf\_page\_size”) → overrides.get(“page\_orientation”) equals “Landscape”.
  - Set tuple(width, height) from get\_page\_size\_mm(overrides).
  - Update css using + formatted text  .print-format { page-size: Custom; page-width: {width}mm; page-height: {height}mm; }.
  - Update css using + formatted text  @page { size: {width}mm {height}mm; }.
- Return css.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L75) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L65)

<a id="op-323cf9bb565f6c"></a>
### Get page size mm

`operation_foundation_binding_foundation_www_printview_get_page_size_mm`

**Inputs** overrides = no value.

**Declared result** tuple at tuple(float, float).

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc.

**Explicit results** tuple(width, height).

**Local steps**

- Bind dependencies page\_size\_mm.
- Set page\_settings from (Platform.get\_cached\_doc(“Print Settings”).as\_dict() bitwise or (overrides or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in overrides → mapping().
- Set tuple(width, height) from page\_size\_mm(page\_settings).
- If page\_settings.get(“pdf\_page\_size”) differs from “Custom”.
  - Set tuple(width, height) from sorted(tuple(width, height)).
- If page\_settings.get(“page\_orientation”) equals “Landscape”.
  - Set tuple(width, height) from tuple(height, width).
- Return tuple(width, height).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L84) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L477)

<a id="op-b1bc5a6e4be34c"></a>
### Get page margin

`operation_foundation_binding_foundation_www_printview_get_page_margin`

**Inputs** print\_format = no value.

**Declared result** str.

**Explicit results** one space.join((list(“15mm”) × 4)) · one space.join(generator of margins.get(side, “15mm”) for side drawn from PAGE\_MARGIN\_SIDES).

**Local steps**

- Bind dependencies resolve\_pdf\_generator.
- If (not print\_format or not print\_format.css or (print\_format.pdf\_generator or resolve\_pdf\_generator()) does not belong to tuple(“chrome”, “PlutoPrint”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not print\_format → not print\_format.css → (print\_format.pdf\_generator or resolve\_pdf\_generator()) does not belong to tuple(“chrome”, “PlutoPrint”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.pdf\_generator → resolve\_pdf\_generator().
  - Return one space.join((list(“15mm”) × 4)).
- Set margins from get\_page\_rule\_margins(print\_format.css).
- Return one space.join(generator of margins.get(side, “15mm”) for side drawn from PAGE\_MARGIN\_SIDES).
  - Draw side from PAGE\_MARGIN\_SIDES.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L80) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L473)

<a id="op-5fadd3c32e3f6e"></a>
### Get page rule properties

`operation_foundation_binding_foundation_www_printview_get_page_rule_properties`

**Inputs** css.

**Local steps**

- Bind dependencies cssutils.
- Evaluate cssutils.log.setLog(Platform.logger(“cssutils”)).
- Set rules from list(cssutils.CSSParser(fetcher = deferred anonymous expression).parseString(css)).
- While rules.
  - Set rule from rules.pop(0).
  - If (isinstance(rule, cssutils.css.CSSPageRule) and not rule.selectorText).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(rule, cssutils.css.CSSPageRule) → not rule.selectorText.
    - yield values from rule.style.
  - Otherwise.
    - If (isinstance(rule, cssutils.css.CSSMediaRule) and (set(“all”, “print”) bitwise and set of nested operand in the contract.strip().lower() for medium drawn from nested operand in the contract.media.mediaText. ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(rule, cssutils.css.CSSMediaRule) → (set(“all”, “print”) bitwise and set of medium.strip().lower() for medium drawn from rule.media.mediaText.split(“,”)).
      - Draw medium from rule.media.mediaText.split(“,”).
      - Set rules at slice no value to 0 from list(rule.cssRules).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L82) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L475)
