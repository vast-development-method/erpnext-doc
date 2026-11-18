# Shared value and file services · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Password

<a id="op-42364d1d534c38"></a>
### Get password reset limit

`operation_foundation_utils_password_business_behavior_get_password_reset_limit`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L1948) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L401)

## Service · Password strength

<a id="op-eed6b7ac6405a4"></a>
### Test password strength

`operation_foundation_utils_password_strength_business_behavior_test_password_strength`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** password, user\_inputs.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L2052) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L417)

<a id="op-01eea9122ca38b"></a>
### Get feedback

`operation_foundation_utils_password_strength_business_behavior_get_feedback`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** score, sequence.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L2318) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L408)

<a id="op-e2bcb228b02606"></a>
### Get match feedback

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** match, is\_sole\_match.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L2748) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L409)

<a id="op-49b565cc8ef282"></a>
### Get match feedback.fun bruteforce

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_bruteforce`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L3676) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L410)

<a id="op-59ebcb853b68f5"></a>
### Get match feedback.fun dictionary

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_dictionary`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L3704) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L412)

<a id="op-7cbab3527c256a"></a>
### Get match feedback.fun spatial

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_spatial`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L3752) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L416)

<a id="op-666ec6462834d8"></a>
### Get match feedback.fun repeat

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_repeat`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L3956) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L414)

<a id="op-8b8088fa35b695"></a>
### Get match feedback.fun sequence

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_sequence`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L4197) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L415)

<a id="op-eb8c88a2e25d4f"></a>
### Get match feedback.fun regex

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_regular_expression`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L4258) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L413)

<a id="op-8e86caf597b70c"></a>
### Get match feedback.fun date

`operation_foundation_utils_password_strength_business_behavior_get_match_feedback_fun_date`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L4389) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L411)

<a id="op-2698a64c701b8e"></a>
### Get dictionary match feedback

`operation_foundation_utils_password_strength_business_behavior_get_dictionary_match_feedback`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** match, is\_sole\_match.

**Explicit result forms** a structured result.

**Local structure** 12 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L4474) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L407)

## Service · Pdf

<a id="op-202aa417f1a681"></a>
### Platform PDFKit.find options in meta

`operation_foundation_utils_portable_document_business_behavior_foundation_portable_document_kit_find_options_in_meta`

**Inputs** self, content.

**Explicit results** mapping().

**Local steps**

- Return mapping().

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L5354) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L419)

<a id="op-2e3405e44c7a26"></a>
### Pdf header html

`operation_foundation_utils_portable_document_business_behavior_portable_document_header_document_markup`

**Inputs** soup, head, content, styles, html\_id, css, path = no value.

**Explicit results** Platform.render\_template(path, mapping(“head” → head, “content” → content, “styles” → styles, “html\_id” → html\_id, …)).

**Local steps**

- If not path.
  - Set path from “templates/print\_formats/pdf\_header\_footer.html”.
- Return Platform.render\_template(path, mapping(“head” → head, “content” → content, “styles” → styles, “html\_id” → html\_id, …)).
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L5398) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L437)

<a id="op-8b80476e9bed54"></a>
### Pdf body html

`operation_foundation_utils_portable_document_business_behavior_portable_document_body_document_markup`

**Inputs** template, args, remaining named values kwargs.

**Explicit results** template.render(args, filters = mapping(“len” → len)).

**Explicit failure paths** validation helper with Platform.PrintFormatError — translated “Error in print format on line {0}: {1}”.format(\_guess\_template\_error\_line\_number(template), str(e)).

**Local steps**

- Bind dependencies safe\_render\_flags.
- Attempt the following.
  - Within safe\_render\_flags().
    - Return template.render(args, filters = mapping(“len” → len)).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Error in print format on line {0}: {1}”.format(\_guess\_template\_error\_line\_number(template), str(e)), exc = Platform.PrintFormatError, title = translated “Print Format Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L13) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L433)

<a id="op-5b5b6bf6c772c0"></a>
### Guess template error line number

`operation_foundation_utils_portable_document_business_behavior_guess_template_error_line_number`

**Inputs** template.

**Declared result** (int bitwise or no value).

**Explicit results** frame.lineno.

**Local steps**

- Within contextlib.suppress(Exception).
  - Bind dependencies sys.
  - Bind dependencies traceback.
  - Set tuple(\_, \_, tb) from sys.exc\_info().
  - For each frame in reversed(traceback.extract\_tb(tb)).
    - If template.filename belongs to frame.filename.
      - Return frame.lineno.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L5878) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L428)

<a id="op-77de475e618b97"></a>
### Pdf footer html

`operation_foundation_utils_portable_document_business_behavior_portable_document_footer_document_markup`

**Inputs** soup, head, content, styles, html\_id, css, path = no value.

**Explicit results** pdf\_header\_html(soup = soup, head = head, content = content, styles = styles, …).

**Local steps**

- Return pdf\_header\_html(soup = soup, head = head, content = content, styles = styles, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0490.json#L6093) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L436)

<a id="op-0bc8cefcef63e5"></a>
### Get pdf

`operation_foundation_utils_portable_document_business_behavior_get_portable_document`

**Inputs** html, options = no value, output = no value, smart\_shrinking = false.

**Explicit results** output · filedata.

**Explicit failure paths** validation helper — translated “PDF generation failed because of broken image links” · propagate active failure.

**Local steps**

- Set html from scrub\_urls(html).
- Set tuple(html, options) from prepare\_options(html, options).
- Evaluate options.update(mapping(“disable-javascript” → empty text, “disable-local-file-access” → empty text)).
- Set filedata from empty text.
- If (not smart\_shrinking and Version(get\_wkhtmltopdf\_version()) &gt; Version(“0.12.3”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not smart\_shrinking → Version(get\_wkhtmltopdf\_version()) &gt; Version(“0.12.3”).
  - Evaluate options.update(mapping(“disable-smart-shrinking” → empty text)).
- Attempt the following.
  - Set filedata from pdfkit.from\_string(html, options = (options or mapping()), verbose = true).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → mapping().
  - Bind dependencies PdfReader, PdfWriter.
  - Set reader from PdfReader(io.BytesIO(filedata)).
- On failure (OSError) bound to e.
  - If any(list of error belongs to str(e) for error drawn from PDF\_CONTENT\_ERRORS).
    - Draw error from PDF\_CONTENT\_ERRORS.
    - If not filedata.
      - Evaluate print(html, options).
      - Call the validation error handler Platform.throw(translated “PDF generation failed because of broken image links”).
    - If output.
      - Evaluate output.append\_pages\_from\_reader(reader).
  - Otherwise.
    - Propagate the active failure.
- On exit, including pending return or failure.
  - Evaluate cleanup(options).
- If “password” belongs to options.
  - Set password from options at “password”.
- If output.
  - Evaluate output.append\_pages\_from\_reader(reader).
  - Return output.
- Set writer from PdfWriter().
- Evaluate writer.append\_pages\_from\_reader(reader).
- If “password” belongs to options.
  - Evaluate writer.encrypt(password).
- Set filedata from get\_file\_data\_from\_writer(writer).
- Return filedata.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L9) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L425)

<a id="op-cf9cf5352d3206"></a>
### Measure time

`operation_foundation_utils_portable_document_business_behavior_measure_time`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Bind dependencies time.
- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L11) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L431)

<a id="op-a9296eaa6400c7"></a>
### Measure time.wrapper

`operation_foundation_utils_portable_document_business_behavior_measure_time_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** result.

**Local steps**

- Set start\_time from time.time().
- Set result from func(expanded args, expanded names kwargs).
- Set end\_time from time.time().
- Evaluate print(formatted text Function {func.\_\_name\_\_} took {(end\_time − start\_time)} seconds).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L12) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L432)

<a id="op-8c181b4b41cf01"></a>
### Encrypt pdf

`operation_foundation_binding_foundation_utils_pdf_encrypt_pdf`

**Control responsibility** Protected data and signing. Key ownership, the selected cryptographic provider and verification status govern the protected data.

**Declared inputs** content, password.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L63) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L221)

<a id="op-bdb0dc2f153be2"></a>
### Get chrome pdf

`operation_foundation_utils_portable_document_business_behavior_get_chrome_portable_document`

**Inputs** print\_format, html, options, output, pdf\_generator = no value.

**Wrappers, in declaration order** measure\_time.

**Explicit results** no value · transformer.transform\_pdf(output = output).

**Local steps**

- Bind dependencies Browser.
- Bind dependencies ChromePDFGenerator.
- Bind dependencies PDFTransformer.
- If pdf\_generator differs from “chrome”.
  - Return no value.
- Set generator from ChromePDFGenerator().
- Set browser from no value.
- Attempt the following.
  - Set browser from Browser(generator, print\_format, html, options).
  - Set transformer from PDFTransformer(browser).
  - Return transformer.transform\_pdf(output = output).
- On exit, including pending return or failure.
  - Evaluate generator.\_close\_browser().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L8) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L421)

<a id="op-499ab38f1099cd"></a>
### Get plutoprint pdf

`operation_foundation_binding_foundation_utils_pdf_get_plutoprint_pdf`

**Inputs** print\_format, html, options, output, pdf\_generator = no value.

**Explicit results** no value · get\_chrome\_pdf(print\_format, html, options, output, pdf\_generator = “chrome”) · PDFTransformer(PlutoBrowser(print\_format, html, options)).transform\_pdf(output = output).

**Local steps**

- Bind dependencies PDFTransformer.
- Bind dependencies PlutoBrowser, plutoprint\_can\_render.
- If pdf\_generator differs from “PlutoPrint”.
  - Return no value.
- Set options from (options or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options → mapping().
- If (options.get(“page-ranges”) or not plutoprint\_can\_render(html)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in options.get(“page-ranges”) → not plutoprint\_can\_render(html).
  - Return get\_chrome\_pdf(print\_format, html, options, output, pdf\_generator = “chrome”).
- Return PDFTransformer(PlutoBrowser(print\_format, html, options)).transform\_pdf(output = output).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L162) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L320)

<a id="op-cccc248d41d3e2"></a>
### Get file data from writer

`operation_foundation_utils_portable_document_business_behavior_get_file_data_from_writer`

**Inputs** writer\_obj.

**Explicit results** stream.read().

**Local steps**

- Set stream from io.BytesIO().
- Evaluate writer\_obj.write(stream).
- Evaluate stream.seek(0).
- Return stream.read().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0491.json#L502) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L423)
