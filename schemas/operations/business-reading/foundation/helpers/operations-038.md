# Shared value and file services · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Print format generator

<a id="op-402bee7fd462ca"></a>
### Format field value

`operation_foundation_binding_foundation_utils_print_format_generator_format_field_value`

**Inputs** doc, df.

**Declared result** str.

**Explicit results** format\_datetime(value, formatted text {date\_format.replace(“mm”, “MM”)} {get\_user\_time\_format()}) · formatdate(value, date\_format) · doc.get\_formatted(fieldname).

**Local steps**

- Bind dependencies format\_datetime, formatdate, get\_user\_time\_format.
- Set fieldname from df.get(“fieldname”).
- Set date\_format from df.get(“date\_format”).
- Set value from doc.get(fieldname).
- If (date\_format and value and df.get(“fieldtype”) belongs to DATE\_FIELDTYPES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_format → value → df.get(“fieldtype”) belongs to DATE\_FIELDTYPES.
  - If df.get(“fieldtype”) equals “Datetime”.
    - Return format\_datetime(value, formatted text {date\_format.replace(“mm”, “MM”)} {get\_user\_time\_format()}).
  - Return formatdate(value, date\_format).
- Return doc.get\_formatted(fieldname).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L171) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L329)

<a id="op-f3c01e5a9a1b88"></a>
### Get formatted field values

`operation_foundation_utils_print_format_generator_business_behavior_get_formatted_field_values`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** mapping(“values” → values, “child” → child).

**Local steps**

- Bind dependencies table\_fields.
- Bind dependencies set\_link\_titles.
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate set\_link\_titles(doc).
- Bind local operation has\_access for subsequent calls.
- Bind local operation formatted\_fields for subsequent calls.
- Set values from mapping().
- Set child from mapping().
- For each df in doc.meta.fields.
  - If df.fieldtype belongs to table\_fields.
    - Set child at df.fieldname from list of formatted\_fields(row) for row drawn from (doc.get(df.fieldname) or list()).
      - Draw row from (doc.get(df.fieldname) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(df.fieldname) → list().
    - If (df.fieldtype equals “Table MultiSelect” and has\_access(doc, df)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Table MultiSelect” → has\_access(doc, df).
      - Attempt the following.
        - Set values at df.fieldname from doc.get\_formatted(df.fieldname).
      - On failure (Exception).
        - Take no action here.
  - Otherwise.
    - If has\_access(doc, df).
      - Attempt the following.
        - Set values at df.fieldname from doc.get\_formatted(df.fieldname).
      - On failure (Exception).
        - Continue with the next iteration or loop test.
- Return mapping(“values” → values, “child” → child).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L3560) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L490)

<a id="op-60f33c4b966497"></a>
### Get formatted field values.has access

`operation_foundation_utils_print_format_generator_business_behavior_get_formatted_field_values_has_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d, df.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L4412) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L492)

<a id="op-f9c47341fc77a4"></a>
### Get formatted field values.formatted fields

`operation_foundation_utils_print_format_generator_business_behavior_get_formatted_field_values_formatted_fields`

**Inputs** d.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each df in d.meta.fields.
  - If (df.fieldtype belongs to table\_fields or not has\_access(d, df)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype belongs to table\_fields → not has\_access(d, df).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set out at df.fieldname from d.get\_formatted(df.fieldname).
  - On failure (Exception).
    - Continue with the next iteration or loop test.
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L4511) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L491)

<a id="op-271cc8903fe9bd"></a>
### Builder preview generator

`operation_foundation_utils_print_format_generator_business_behavior_builder_preview_generator`

**Inputs** print\_format, doctype, name = no value, letterhead = no value, settings = no value.

**Declared result** “PrintFormatGenerator \| None”.

**Record and data access** resolve a document from Platform.parse\_json(print\_format) via get\_doc · resolve a document from doctype via get\_doc.

**Explicit results** no value · legacy\_generator(pf, doc, letterhead) · PrintFormatGenerator(pf, doc, letterhead, settings = Platform.parse\_json(settings)).

**Explicit failure paths** validation helper — translated “Expected an unsaved Print Format document”.

**Local steps**

- Bind dependencies printable\_sample.
- Bind dependencies validate\_print.
- Evaluate Platform.has\_permission(“Print Format”, “write”, throw = true).
- Set pf from Platform.get\_doc(Platform.parse\_json(print\_format)).
- If pf.doctype differs from “Print Format”.
  - Call the validation error handler Platform.throw(translated “Expected an unsaved Print Format document”).
- Set name from (name or printable\_sample(doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → printable\_sample(doctype).
- If not name.
  - Return no value.
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate validate\_print(doc).
- If uses\_legacy\_weasyprint(pf).
  - Bind dependencies legacy\_generator.
  - Return legacy\_generator(pf, doc, letterhead).
- Return PrintFormatGenerator(pf, doc, letterhead, settings = Platform.parse\_json(settings)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Print Format”, “write”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L36) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L486)

<a id="op-9cef8367f5ef02"></a>
### Render builder preview

`operation_foundation_utils_print_format_generator_business_behavior_render_builder_preview`

**Inputs** print\_format, doctype, name = no value, letterhead = no value, settings = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** generator.get\_html\_preview() when generator, otherwise empty text.

**Local steps**

- Set generator from \_builder\_preview\_generator(print\_format, doctype, name, letterhead, …).
- Return generator.get\_html\_preview() when generator, otherwise empty text.
  - Value choice on generator — true gives generator.get\_html\_preview(), false gives empty text.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L5208) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L527)

<a id="op-dfd41cda72fc95"></a>
### Download builder preview pdf

`operation_foundation_utils_print_format_generator_business_behavior_download_builder_preview_portable_document`

**Inputs** print\_format, doctype, name = no value, letterhead = no value, settings = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “No document available to preview”.

**Local steps**

- Set generator from \_builder\_preview\_generator(print\_format, doctype, name, letterhead, …).
- If not generator.
  - Call the validation error handler Platform.throw(translated “No document available to preview”).
- Set Platform.local.response.filename from “preview.pdf”.
- Set Platform.local.response.filecontent from generator.render\_pdf().
- Set Platform.local.response.type from “pdf”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L5438) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L487)

<a id="op-facf9bb24ea704"></a>
### Get html

`operation_foundation_utils_print_format_generator_business_behavior_get_document_markup`

**Inputs** doctype, name, print\_format, letterhead = no value, action\_banner = no value, style = no value, trigger\_print = false, settings = no value, no\_letterhead = no value, doc = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** generator.get\_html\_preview(action\_banner = action\_banner, trigger\_print = trigger\_print).

**Local steps**

- Bind dependencies validate\_print.
- Set doc from (doc or Platform.get\_doc(doctype, name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → Platform.get\_doc(doctype, name).
- Evaluate validate\_print(doc).
- Set generator from PrintFormatGenerator(print\_format, doc, letterhead, style = style, settings = settings, no\_letterhead = no\_letterhead).
- Return generator.get\_html\_preview(action\_banner = action\_banner, trigger\_print = trigger\_print).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L5776) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L489)

<a id="op-a6d2c01e9c358f"></a>
### Page size mm

`operation_foundation_binding_foundation_utils_print_format_generator_page_size_mm`

**Inputs** print\_settings.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple((flt(print\_settings.get(“pdf\_page\_width”)) or 210), (flt(print\_settings.get(“pdf\_page\_height”)) or 297)) · tuple(known) when known, otherwise tuple(210, 297).

**Local steps**

- Bind dependencies flt.
- Bind dependencies PageSize.
- Set size from print\_settings.get(“pdf\_page\_size”).
- If size equals “Custom”.
  - Return tuple((flt(print\_settings.get(“pdf\_page\_width”)) or 210), (flt(print\_settings.get(“pdf\_page\_height”)) or 297)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(print\_settings.get(“pdf\_page\_width”)) → 210.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(print\_settings.get(“pdf\_page\_height”)) → 297.
- Set known from PageSize.page\_sizes.get(size).
- Return tuple(known) when known, otherwise tuple(210, 297).
  - Value choice on known — true gives tuple(known), false gives tuple(210, 297).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L177) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L335)

<a id="op-a482edc879171d"></a>
### Page number html

`operation_foundation_binding_foundation_utils_print_format_generator_page_number_html`

**Inputs** position.

**Declared result** str.

**Explicit results** formatted text &lt;div style="text-align:{align};font-size:10px;padding:2px 0;"&gt;&lt;span class="page"&gt;&lt;/span&gt; {translated “of”} &lt;span class="topage"&gt;&lt;/span&gt;&lt;/div&gt;.

**Local steps**

- Set align from PAGE\_NUMBER\_ALIGN.get(position, “center”).
- Return formatted text &lt;div style="text-align:{align};font-size:10px;padding:2px 0;"&gt;&lt;span class="page"&gt;&lt;/span&gt; {translated “of”} &lt;span class="topage"&gt;&lt;/span&gt;&lt;/div&gt;.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L176) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L334)

<a id="op-7687c020934d13"></a>
### Layout page settings

`operation_foundation_binding_foundation_utils_print_format_generator_layout_page_settings`

**Inputs** layout.

**Declared result** dict.

**Explicit results** mapping() · settings.

**Local steps**

- Set page from layout.get(“page”) when isinstance(layout, dict), otherwise no value.
  - Value choice on isinstance(layout, dict) — true gives layout.get(“page”), false gives no value.
- If not isinstance(page, dict).
  - Return mapping().
- Set settings from mapping().
- Set sizes from nested operand in the contract.get\_meta(“Print Settings”).get\_field(“pdf\_page\_size”).options.split(whitespace '\\n').
- If (page.get(“size”) belongs to sizes and page.get(“size”) differs from “Custom”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in page.get(“size”) belongs to sizes → page.get(“size”) differs from “Custom”.
  - Set settings at “pdf\_page\_size” from page at “size”.
- If page.get(“orientation”) belongs to tuple(“Portrait”, “Landscape”).
  - Set settings at “page\_orientation” from page at “orientation”.
- Return settings.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L175) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L333)

<a id="op-3070388b734b37"></a>
### Get page size mm

`operation_foundation_binding_foundation_utils_print_format_generator_get_page_size_mm`

**Inputs** page = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** tuple at tuple(float, float).

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc.

**Explicit results** tuple(height, width) when settings.get(“page\_orientation”) equals “Landscape”, otherwise tuple(width, height).

**Local steps**

- Set settings from Platform.get\_cached\_doc(“Print Settings”).as\_dict().
- Evaluate settings.update(layout\_page\_settings(mapping(“page” → Platform.parse\_json(page) when page, otherwise no value))).
  - Value choice on page — true gives Platform.parse\_json(page), false gives no value.
- Set tuple(width, height) from page\_size\_mm(settings).
- Return tuple(height, width) when settings.get(“page\_orientation”) equals “Landscape”, otherwise tuple(width, height).
  - Value choice on settings.get(“page\_orientation”) equals “Landscape” — true gives tuple(height, width), false gives tuple(width, height).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L173) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L331)

<a id="op-b11def2620abb6"></a>
### Check conditions

`operation_foundation_binding_foundation_utils_print_format_generator_check_conditions`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doctype, name, conditions.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L168) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L326)

<a id="op-8f214664335d4e"></a>
### Condition locals

`operation_foundation_binding_foundation_utils_print_format_generator_condition_locals`

**Inputs** doc, print\_settings.

**Declared result** dict.

**Explicit results** mapping(“doc” → doc.as\_dict(), “print\_settings” → print\_settings.as\_dict()).

**Local steps**

- Return mapping(“doc” → doc.as\_dict(), “print\_settings” → print\_settings.as\_dict()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L170) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L328)

<a id="op-e09366b620dfba"></a>
### Print Format Generator.initialize

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_initialize`

**Inputs** self, print\_format, doc, letterhead = no value, style = no value, settings = no value, no\_letterhead = no value.

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Local steps**

- Set self.print\_format from print\_format when not isinstance(print\_format, str), otherwise Platform.get\_doc(“Print Format”, print\_format).
  - Value choice on not isinstance(print\_format, str) — true gives print\_format, false gives Platform.get\_doc(“Print Format”, print\_format).
- Set self.doc from doc.
- Set self.style from style.
- Set self.settings\_override from (settings or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings → mapping().
- Set self.\_header\_absorbs\_top\_margin from false.
- Set self.\_logged\_conditions from set().
- Set self.letterhead from no value.
- Evaluate self.build\_context().
- Set self.layout from self.get\_layout(self.print\_format).
- Set self.context.layout from self.layout.
- Set self.letterhead from self.get\_letterhead(letterhead, no\_letterhead).
- Set self.context.letterhead from self.letterhead.

If control reaches the end, it returns no value.

**Methods declared on this owner** [build context](operations-038.md#op-d0964ad3c47feb), [get layout](operations-039.md#op-75ab5db727bdb9), [get letterhead](operations-038.md#op-a0a837d99a9a32).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L6062) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L509)

<a id="op-a0a837d99a9a32"></a>
### Print Format Generator.get letterhead

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_letterhead`

**Inputs** self, letterhead, no\_letterhead.

**Record and data access** read “Letter Head” via get\_value · read “Letter Head” via exists · resolve a document from “Letter Head” via get\_cached\_doc.

**Explicit results** no value · Platform.get\_cached\_doc(“Letter Head”, name).

**Local steps**

- If no\_letterhead is identical to no value.
  - Set no\_letterhead from not cint(self.print\_settings.with\_letterhead).
- If (cint(no\_letterhead) or letterhead equals translated “No Letterhead”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(no\_letterhead) → letterhead equals translated “No Letterhead”.
  - Return no value.
- Set name from letterhead.
- If not name.
  - Set layout from (self.layout or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.layout → mapping().
  - If “letter\_head” belongs to layout.
    - Set name from layout.get(“letter\_head”).
    - If not name.
      - Return no value.
  - Otherwise.
    - Set name from (self.doc.get(“letter\_head”) or Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), “name”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“letter\_head”) → Platform.db.get\_value(“Letter Head”, mapping(“is\_default” → 1), “name”).
- If (not name or not Platform.db.exists(“Letter Head”, name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not Platform.db.exists(“Letter Head”, name).
  - Return no value.
- Return Platform.get\_cached\_doc(“Letter Head”, name).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Letter Head”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L45) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L505)

<a id="op-080dfdfa3b6426"></a>
### Print Format Generator.format page settings

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_format_page_settings`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping() · layout\_page\_settings(layout).

**Local steps**

- Attempt the following.
  - Set layout from Platform.parse\_json(self.print\_format.format\_data).
- On failure (ValueError).
  - Return mapping().
- Return layout\_page\_settings(layout).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L180) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L338)

<a id="op-71213f9e20d67a"></a>
### Print Format Generator.apply page orientation

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_apply_page_orientation`

**Inputs** self.

**Local steps**

- Set settings from self.print\_settings.
- If settings.get(“page\_orientation”) equals “Landscape”.
  - Set tuple(width, height) from page\_size\_mm(settings).
  - Set settings.pdf\_page\_size from “Custom”.
  - Set tuple(settings.pdf\_page\_width, settings.pdf\_page\_height) from tuple(height, width).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L178) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L336)

<a id="op-d0964ad3c47feb"></a>
### Print Format Generator.build context

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_build_context`

**Inputs** self.

**Record and data access** resolve a document from “Print Settings” via get\_doc · read “Print Style” via exists · resolve a document from “Print Style” via get\_cached\_doc.

**Local steps**

- Set self.print\_settings from Platform.get\_doc(“Print Settings”).
- Evaluate self.print\_settings.update(self.format\_page\_settings()).
- If self.settings\_override.
  - Bind dependencies get\_allowed\_print\_settings\_override.
  - Evaluate self.print\_settings.update(get\_allowed\_print\_settings\_override(self.doc, self.settings\_override)).
- Evaluate self.apply\_page\_orientation().
- Bind dependencies run\_before\_print.
- Evaluate run\_before\_print(self.doc, self.print\_settings.as\_dict()).
- Set self.doc.flags.absolute\_value from self.print\_format.absolute\_value.
- Set self.doc.absolute\_value from self.print\_format.absolute\_value.
- Set tuple(page\_width, page\_height) from page\_size\_mm(self.print\_settings).
- Set body\_width from ((page\_width − self.print\_format.margin\_left) − self.print\_format.margin\_right).
- Set style\_name from (self.style or self.print\_settings.print\_style).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.style → self.print\_settings.print\_style.
- Set print\_style from Platform.get\_cached\_doc(“Print Style”, style\_name) when (style\_name and Platform.db.exists(“Print Style”, mapping(“name” → style\_name, “disabled” → 0))), otherwise no value.
  - Value choice on (style\_name and Platform.db.exists(“Print Style”, mapping(“name” → style\_name, “disabled” → 0))) — true gives Platform.get\_cached\_doc(“Print Style”, style\_name), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in style\_name → Platform.db.exists(“Print Style”, mapping(“name” → style\_name, “disabled” → 0)).
- Set self.context from Platform.\_dict(mapping(“doc” → self.doc, “print\_format” → self.print\_format, “print\_settings” → self.print\_settings, “print\_style” → print\_style, …)).
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [format page settings](operations-038.md#op-080dfdfa3b6426), [apply page orientation](operations-038.md#op-71213f9e20d67a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Print Style”, style\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L41) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L497)

<a id="op-2f329ba93cca20"></a>
### Print Format Generator.get html preview

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_document_markup_preview`

**Inputs** self, action\_banner = no value, trigger\_print = false.

**Explicit results** self.get\_main\_html().

**Local steps**

- Set repeat from self.print\_settings.repeat\_header\_footer.
- Set frame\_header from self.\_render\_overlay(“header”, with\_page\_no = false) when repeat, otherwise no value.
  - Value choice on repeat — true gives self.\_render\_overlay(“header”, with\_page\_no = false), false gives no value.
- Set frame\_footer from self.\_render\_overlay(“footer”, with\_page\_no = false) when repeat, otherwise no value.
  - Value choice on repeat — true gives self.\_render\_overlay(“footer”, with\_page\_no = false), false gives no value.
- If (repeat and (frame\_header or frame\_footer)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repeat → (frame\_header or frame\_footer).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in frame\_header → frame\_footer.
  - Set self.context.repeat\_frame from true.
  - Set self.context.frame\_header from (frame\_header or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in frame\_header → empty text.
  - Set self.context.frame\_footer from (frame\_footer or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in frame\_footer → empty text.
  - Set self.context.header from empty text.
  - Set self.context.footer from empty text.
- Otherwise.
  - Set self.context.repeat\_frame from false.
  - Set tuple(header\_html, footer\_html) from self.get\_header\_footer\_html().
  - Set self.context.header from header\_html.
  - Set self.context.footer from footer\_html.
- Set self.context.action\_banner from action\_banner.
- If trigger\_print.
  - Bind dependencies trigger\_print\_script.
  - Set self.context.trigger\_print\_script from trigger\_print\_script.
- Return self.get\_main\_html().

**Methods declared on this owner** [render overlay](operations-039.md#op-b516dd1e6494a9), [get header footer html](operations-038.md#op-fb5db4a47c5e6d), [get main html](operations-038.md#op-9aa1c3c0bf2d22).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L7630) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L502)

<a id="op-9aa1c3c0bf2d22"></a>
### Print Format Generator.get main html

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_main_document_markup`

**Inputs** self.

**Explicit results** Platform.render\_template(“templates/print\_format/print\_format.html”, self.context).

**Local steps**

- Set self.context.css from Platform.render\_template(“templates/print\_format/print\_format.css”, self.context).
- Return Platform.render\_template(“templates/print\_format/print\_format.html”, self.context).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0494.json#L8152) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L506)

<a id="op-fb5db4a47c5e6d"></a>
### Print Format Generator.get header footer html

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_get_header_footer_document_markup`

**Inputs** self.

**Explicit results** tuple(header\_html, footer\_html).

**Local steps**

- Set header\_html, footer\_html from no value.
- If self.letterhead.
  - Set header\_html from Platform.render\_template(“templates/print\_format/print\_header.html”, self.context).
  - Set footer\_html from Platform.render\_template(“templates/print\_format/print\_footer.html”, self.context).
- Return tuple(header\_html, footer\_html).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0495.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L503)

<a id="op-c64e9f5e27862a"></a>
### Print Format Generator.render pdf

`operation_foundation_utils_print_format_generator_business_behavior_print_format_generator_render_portable_document`

**Inputs** self, password = no value.

**Explicit results** pdf · self.underlay\_background(pdf, background, password, html\_generator) when background, otherwise pdf.

**Explicit failure paths** validation helper — translated “This format uses a Typst block, which only the Typst renderer can print. Set the PDF Renderer to Typst or re …”.

**Local steps**

- Bind dependencies HTML\_PDF\_GENERATORS.
- Set pf from self.print\_format.
- Set generator\_name from (pf.get(“pdf\_generator”) or “chrome”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pf.get(“pdf\_generator”) → “chrome”.
- If generator\_name equals “PlutoPrint”.
  - Bind dependencies resolve\_pdf\_generator.
  - Set generator\_name from resolve\_pdf\_generator(pf).
- If generator\_name does not belong to tuple(expanded HTML\_PDF\_GENERATORS, “wkhtmltopdf”).
  - Set previous from set\_print\_context(doctype = self.doc.doctype, name = self.doc.name, doc = self.doc, letterhead = (self.letterhead and self.letterhead.name), …).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.letterhead → self.letterhead.name.
  - Attempt the following.
    - For each hook in Platform.get\_hooks(“pdf\_generator”).
      - Set pdf from Platform.call(hook, print\_format = pf.name, html = no value, options = mapping(“password” → password) when password, otherwise mapping(), output = no value, …).
        - Value choice on password — true gives mapping(“password” → password), false gives mapping().
      - If pdf.
        - Return pdf.
  - On exit, including pending return or failure.
    - Evaluate restore\_print\_context(previous).
- Bind dependencies has\_typst\_blocks.
- If has\_typst\_blocks(self.layout).
  - Call the validation error handler Platform.throw(translated “This format uses a Typst block, which only the Typst renderer can print. Set the PDF Renderer to Typst or re …”, title = translated “Chromium renderer unavailable”).
- Set html from self.\_build\_html\_for\_chrome().
- Set options from mapping(“margin-top” → formatted text {pf.margin\_top}mm, “margin-bottom” → formatted text {pf.margin\_bottom}mm, “margin-left” → formatted text {pf.margin\_left}mm, “margin-right” → formatted text {pf.margin\_right}mm).
- If self.\_header\_absorbs\_top\_margin.
  - Set options at “header-includes-top-margin” from true.
- If password.
  - Set options at “password” from password.
- Evaluate options.update(self.page\_options()).
- Set background from self.layout.get(“background”).
- If background.
  - Evaluate options.pop(“password”, no value).
- Set html\_generator from generator\_name when generator\_name belongs to HTML\_PDF\_GENERATORS, otherwise “chrome”.
  - Value choice on generator\_name belongs to HTML\_PDF\_GENERATORS — true gives generator\_name, false gives “chrome”.
- Set pdf from render\_html\_pdf(pf.name, html, options, html\_generator).
- Return self.underlay\_background(pdf, background, password, html\_generator) when background, otherwise pdf.
  - Value choice on background — true gives self.underlay\_background(pdf, background, password, html\_generator), false gives pdf.

**Methods declared on this owner** [build html for chrome](operations-039.md#op-2528cb300f2f27), [page options](operations-039.md#op-9b957aa64b0063), [underlay background](operations-038.md#op-f4a831f9aa6e5f).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“pdf\_generator”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L53) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L520)

<a id="op-f4a831f9aa6e5f"></a>
### Print Format Generator.underlay background

`operation_foundation_binding_foundation_utils_print_format_generator_printformatgenerator_underlay_background`

**Inputs** self, pdf, background, password = no value, pdf\_generator = “chrome”.

**Declared result** bytes.

**Explicit results** out.getvalue().

**Local steps**

- Bind dependencies BytesIO.
- Bind dependencies PdfReader, PdfWriter.
- Set tuple(width, height) from page\_size\_mm(self.print\_settings).
- Set html from formatted text &lt;!DOCTYPE html&gt;&lt;html&gt;&lt;head&gt;&lt;style&gt;@page{margin:0}html,body{margin:0}.print-format{margin-top:0mm;margin-bottom:0mm;margin-left:0mm;margin-right:0mm}&lt;/.
- Set options from mapping(“margin-top” → “0mm”, “margin-bottom” → “0mm”, “margin-left” → “0mm”, “margin-right” → “0mm”).
- Evaluate options.update(self.page\_options()).
- Set background\_pdf from render\_html\_pdf(self.print\_format.name, html, options, pdf\_generator).
- Set background\_page from PdfReader(BytesIO(background\_pdf)).pages at 0.
- Set writer from PdfWriter(clone\_from = BytesIO(pdf)).
- For each page in writer.pages.
  - Evaluate page.merge\_page(background\_page, over = false).
- If password.
  - Evaluate writer.encrypt(password).
- Set out from BytesIO().
- Evaluate writer.write(out).
- Return out.getvalue().

**Methods declared on this owner** [page options](operations-039.md#op-9b957aa64b0063).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L185) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L343)
