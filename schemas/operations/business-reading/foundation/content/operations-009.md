# Web content and issued documents · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Print format

[Record definition](../../../../data/record-types/print_format.json)

<a id="op-07a1dce55f6ed5"></a>
### Print Format.extract images

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_extract_images`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies extract\_images\_from\_html.
- Bind dependencies is\_classic\_layout.
- If self.print\_format\_builder\_beta.
  - Return no value.
- If is\_classic\_layout(self.format\_data).
  - Set data from json.loads(self.format\_data).
  - For each df in data.
    - If (df.get(“fieldtype”) and df at “fieldtype” belongs to tuple(“HTML”, “Custom HTML”) and df.get(“options”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“fieldtype”) → df at “fieldtype” belongs to tuple(“HTML”, “Custom HTML”) → df.get(“options”).
      - Set df at “options” from extract\_images\_from\_html(self, df at “options”).
  - Set self.format\_data from json.dumps(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1668)

<a id="op-b73420741a6940"></a>
### Print Format.validate weasyprint choice

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_validate_weasyprint_choice`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “WeasyPrint is deprecated and cannot be selected for a new format. Use Chrome instead.”.

**Local steps**

- If (self.pdf\_generator differs from “WeasyPrint” or not self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pdf\_generator differs from “WeasyPrint” → not self.is\_new().
  - Return no value.
- If (Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return no value.
- Call the validation error handler Platform.throw(translated “WeasyPrint is deprecated and cannot be selected for a new format. Use Chrome instead.”, title = translated “Renderer unavailable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1671)

<a id="op-f9f98d00d4a8cb"></a>
### Print Format.validate weasyprint layout

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_validate_weasyprint_layout`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “WeasyPrint cannot render this format: {0}. Switch the PDF Renderer to Chrome.”.format(“, ”.join(blockers)).

**Local steps**

- If (self.pdf\_generator differs from “WeasyPrint” or self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pdf\_generator differs from “WeasyPrint” → self.is\_new().
  - Return no value.
- If (Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return no value.
- Bind dependencies legacy\_blockers.
- Attempt the following.
  - Set layout from Platform.parse\_json(self.format\_data) when self.format\_data, otherwise mapping().
    - Value choice on self.format\_data — true gives Platform.parse\_json(self.format\_data), false gives mapping().
- On failure (Exception).
  - Set layout from mapping().
- Set blockers from legacy\_blockers(self, layout).
- If not blockers.
  - Return no value.
- Set before from self.get\_doc\_before\_save().
- If (before and before.pdf\_generator equals “WeasyPrint”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.pdf\_generator equals “WeasyPrint”.
  - Attempt the following.
    - Set unchanged from Platform.parse\_json((before.format\_data or “{}”)) equals layout.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in before.format\_data → “{}”.
  - On failure (Exception).
    - Set unchanged from false.
  - If unchanged.
    - Return no value.
- Call the validation error handler Platform.throw(translated “WeasyPrint cannot render this format: {0}. Switch the PDF Renderer to Chrome.”.format(“, ”.join(blockers)), title = translated “WeasyPrint renderer unavailable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1672)

<a id="op-b54104075fb6f3"></a>
### Print Format.validate plutoprint renderer

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_validate_plutoprint_renderer`

**Inputs** self.

**State and service calls** msgprint with translated “PDF Generator set to Chromium: {0}”.format(“, ”.join(blockers)).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “This format cannot use the PlutoPrint renderer: {0}”.format(“, ”.join(blockers)).

**Local steps**

- Bind dependencies plutoprint\_blockers.
- If (self.pdf\_generator differs from “PlutoPrint” or not blockers bound to plutoprint\_blockers(self)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pdf\_generator differs from “PlutoPrint” → not blockers bound to plutoprint\_blockers(self).
  - Return no value.
- If self.is\_new().
  - Set self.pdf\_generator from “chrome”.
  - Evaluate Platform.msgprint(translated “PDF Generator set to Chromium: {0}”.format(“, ”.join(blockers)), alert = true).
  - Return no value.
- Call the validation error handler Platform.throw(translated “This format cannot use the PlutoPrint renderer: {0}”.format(“, ”.join(blockers)), title = translated “PlutoPrint renderer unavailable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1670)

<a id="op-ac806f5ba142f0"></a>
### Print Format.validate typst renderer

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_validate_typst_renderer`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “This format uses a Typst block, so its PDF Renderer must be Typst.” · validation helper — translated “This format cannot use the Typst renderer: {0}”.format(“, ”.join(blockers)).

**Local steps**

- Bind dependencies has\_typst\_blocks, typst\_blockers.
- Attempt the following.
  - Set layout from Platform.parse\_json(self.format\_data) when self.format\_data, otherwise mapping().
    - Value choice on self.format\_data — true gives Platform.parse\_json(self.format\_data), false gives mapping().
- On failure (Exception).
  - Set layout from mapping().
- If not isinstance(layout, dict).
  - Set layout from mapping().
- If self.pdf\_generator differs from “Typst”.
  - If has\_typst\_blocks(layout).
    - Call the validation error handler Platform.throw(translated “This format uses a Typst block, so its PDF Renderer must be Typst.”, title = translated “Typst block requires the Typst renderer”).
  - Return no value.
- Set blockers from typst\_blockers(self, layout).
- If blockers.
  - Call the validation error handler Platform.throw(translated “This format cannot use the Typst renderer: {0}”.format(“, ”.join(blockers)), title = translated “Typst renderer unavailable”).
- Evaluate self.\_validate\_typst\_block\_markup(layout).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate typst block markup](operations-009.md#op-cf6200f12bfab6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L4760) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1756)

<a id="op-cf6200f12bfab6"></a>
### Print Format.validate typst block markup

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_validate_typst_block_markup`

**Inputs** self, layout.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The Typst block in {0} has a template error: {1}”.format(where, str(e) at slice no value to 300) · validation helper — translated “The Typst block in {0} does not compile: {1}”.format(where, str(e) at slice no value to 300).

**Local steps**

- Bind dependencies get\_jenv.
- Bind dependencies compile\_typst\_source, has\_jinja, has\_typst\_blocks, render\_typst\_template.
- If not has\_typst\_blocks(layout).
  - Return no value.
- Attempt the following.
  - Bind dependencies typst.
- On failure (ImportError).
  - Return no value.
- Set sample\_doc from no value.
- Set sample\_loaded from false.
- For each tuple(where, df) in iter\_nodes(layout).
  - Set markup from (df.get(“typst”) or empty text).strip() when df.get(“fieldtype”) equals “Typst”, otherwise empty text.
    - Value choice on df.get(“fieldtype”) equals “Typst” — true gives (df.get(“typst”) or empty text).strip(), false gives empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“typst”) → empty text.
  - If not markup.
    - Continue with the next iteration or loop test.
  - If has\_jinja(markup).
    - If not sample\_loaded.
      - Set sample\_doc from self.\_typst\_sample\_doc().
      - Set sample\_loaded from true.
    - Attempt the following.
      - If sample\_doc is identical to no value.
        - Evaluate get\_jenv().parse(markup).
        - Continue with the next iteration or loop test.
      - Set markup from render\_typst\_template(markup, mapping(“doc” → sample\_doc)).
    - On failure (Exception) bound to e.
      - Call the validation error handler Platform.throw(translated “The Typst block in {0} has a template error: {1}”.format(where, str(e) at slice no value to 300), title = translated “Invalid Typst markup”).
  - Attempt the following.
    - Evaluate compile\_typst\_source(markup).
  - On failure (Exception) bound to e.
    - Call the validation error handler Platform.throw(translated “The Typst block in {0} does not compile: {1}”.format(where, str(e) at slice no value to 300), title = translated “Invalid Typst markup”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [typst sample doc](operations-009.md#op-bc5248173e6024).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L57) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1755)

<a id="op-bc5248173e6024"></a>
### Print Format.typst sample doc

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_typst_sample_record`

**Inputs** self.

**Record and data access** resolve a document from self.doc\_type via get\_doc · read self.doc\_type via get\_value.

**Explicit results** no value · Platform.get\_doc(self.doc\_type) · Platform.get\_doc(self.doc\_type, name) when name, otherwise no value.

**Local steps**

- If not self.doc\_type.
  - Return no value.
- If Platform.get\_meta(self.doc\_type).issingle.
  - Return Platform.get\_doc(self.doc\_type).
- Set name from Platform.db.get\_value(self.doc\_type, mapping(), “name”, order\_by = “modified desc”).
- Return Platform.get\_doc(self.doc\_type, name) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_doc(self.doc\_type, name), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L5953) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1751)

<a id="op-b94135b3406924"></a>
### Print Format.validate conditions

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_validate_conditions`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is not a valid condition: {1}”.format(Platform.bold(Platform.utils.escape\_html(where)), e.msg).

**Local steps**

- Attempt the following.
  - Set layout from Platform.parse\_json(self.format\_data) when self.format\_data, otherwise no value.
    - Value choice on self.format\_data — true gives Platform.parse\_json(self.format\_data), false gives no value.
- On failure (Exception).
  - Return no value.
- If not isinstance(layout, dict).
  - Return no value.
- For each tuple(where, condition) in \_iter\_conditions(layout).
  - Attempt the following.
    - Evaluate compile(condition, text in the contract, “eval”).
  - On failure (SyntaxError) bound to e.
    - Call the validation error handler Platform.throw(translated “{0} is not a valid condition: {1}”.format(Platform.bold(Platform.utils.escape\_html(where)), e.msg), title = translated “Invalid Condition”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L56) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1754)

<a id="op-3270778bd2957e"></a>
### Print Format.validate colors

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_validate_colors`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} must be a hex color code like #1a5fb4”.format(Platform.bold(self.meta.get\_translated\_label(fieldname))).

**Local steps**

- For each fieldname in tuple(“label\_color”, “value\_color”).
  - Set value from self.get(fieldname).
  - If (value and not re.fullmatch(“#&#91;0-9a-fA-F&#93;{6}”, value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → not re.fullmatch(“#&#91;0-9a-fA-F&#93;{6}”, value).
    - Call the validation error handler Platform.throw(translated “{0} must be a hex color code like #1a5fb4”.format(Platform.bold(self.meta.get\_translated\_label(fieldname)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0314.json#L6495) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1753)

<a id="op-6fd37efc07df3e"></a>
### Print Format.on update

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_on_update`

**Inputs** self.

**Local steps**

- If (hasattr(self, “old\_doc\_type”) and self.old\_doc\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “old\_doc\_type”) → self.old\_doc\_type.
  - Evaluate Platform.clear\_cache(doctype = self.old\_doc\_type).
- If self.doc\_type.
  - Evaluate Platform.clear\_cache(doctype = self.doc\_type).
- Evaluate self.export\_doc().
- Evaluate self.enqueue\_preview\_generation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export doc](operations-009.md#op-3f6b6b0ec603e0), [enqueue preview generation](operations-009.md#op-703a8fe82c31e3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L53) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1749)

<a id="op-703a8fe82c31e3"></a>
### Print Format.enqueue preview generation

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_printformat_enqueue_preview_generation`

**Inputs** self.

**State and service calls** enqueue with generate\_preview.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_patch or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_migrate → Platform.flags.in\_install → Platform.flags.in\_patch → Platform.in\_test.
  - Return no value.
- If (self.print\_format\_for differs from “DocType” or not self.doc\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.print\_format\_for differs from “DocType” → not self.doc\_type.
  - Return no value.
- Evaluate Platform.enqueue(generate\_preview, queue = “short”, enqueue\_after\_commit = true, job\_id = formatted text print\_format\_preview::{self.name}, deduplicate = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(generate\_preview, queue = “short”, enqueue\_after\_commit = true, job\_id = formatted text print\_format\_preview::{self.name}, deduplicate = true, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1667)

<a id="op-aafab85378e758"></a>
### Print Format.after rename

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_after_rename`

**Inputs** self, old, new, remaining positional values args, remaining named values kwargs.

**State and service calls** request set\_value on “Property Setter”.

**Local steps**

- If self.doc\_type.
  - Evaluate Platform.clear\_cache(doctype = self.doc\_type).
- Evaluate Platform.db.set\_value(“Property Setter”, mapping(“doctype\_or\_field” → “DocType”, “doc\_type” → self.doc\_type, “property” → “default\_print\_format”, “value” → old), “value”, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1743)

<a id="op-3f6b6b0ec603e0"></a>
### Print Format.export doc

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_export_record`

**Inputs** self.

**Explicit results** export\_module\_json(self, self.standard equals “Yes”, self.module).

**Local steps**

- Bind dependencies export\_module\_json.
- Return export\_module\_json(self, self.standard equals “Yes”, self.module).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L52) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1746)

<a id="op-776383283b7e4b"></a>
### Print Format.on trash

`operation_foundation_printing_record_definitions_print_format_business_behavior_print_format_on_trash`

**Inputs** self.

**Local steps**

- If self.doc\_type.
  - Evaluate Platform.clear\_cache(doctype = self.doc\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L343) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1748)

<a id="op-72dbe33d298213"></a>
### Iter conditions

`operation_foundation_printing_record_definitions_print_format_business_behavior_iter_conditions`

**Inputs** layout.

**Local steps**

- For each tuple(where, zone) in iter\_zones(layout).
  - yield values from \_condition(zone, where, “visible\_if”).
  - For each df in iter\_fields(zone).
    - Set label from (df.get(“label”) or df.get(“fieldname”) or translated “Field”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“label”) → df.get(“fieldname”) → translated “Field”.
    - yield values from \_condition(df, label, “visible\_if”).
    - yield values from \_condition(df, label, “row\_condition”).
    - Set table\_columns from df.get(“table\_columns”).
    - For each col in table\_columns when isinstance(table\_columns, list), otherwise list().
      - Value choice on isinstance(table\_columns, list) — true gives table\_columns, false gives list().
      - If isinstance(col, dict).
        - yield values from \_condition(col, (col.get(“label”) or label), “column\_condition”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“label”) → label.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L50) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1741)

<a id="op-873112f90498a9"></a>
### Condition

`operation_foundation_printing_record_definitions_print_format_business_behavior_condition`

**Inputs** holder, label, key.

**Local steps**

- Set condition from holder.get(key).
- If (isinstance(condition, str) and condition.strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(condition, str) → condition.strip().
  - yield tuple(label, condition).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L1187) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1737)

<a id="op-2d088c9af393b5"></a>
### Create custom format

`operation_foundation_printing_record_definitions_print_format_business_behavior_create_custom_format`

**Inputs** doctype, name, based\_on = “Standard”, beta = true.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Print Format” via get\_doc.

**State and service calls** request new\_doc for “Print Format” · msgprint with translated “{0} is rendered from an HTML file, so this format starts from the standard layout”.format(source.name) · call insert on doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “The classic builder can no longer create formats”.

**Local steps**

- If not Platform.parse\_json(beta).
  - Call the validation error handler Platform.throw(translated “The classic builder can no longer create formats”).
- Bind dependencies convert\_print\_format, is\_classic\_layout, renders\_from\_file.
- Set doc from Platform.new\_doc(“Print Format”).
- Set doc.doc\_type from doctype.
- Set doc.name from name.
- Set doc.print\_format\_builder\_beta from 1.
- Set source from no value.
- If (based\_on and based\_on differs from “Standard”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in based\_on → based\_on differs from “Standard”.
  - Set source from Platform.get\_doc(“Print Format”, based\_on).
  - Evaluate source.check\_permission(“read”).
  - If renders\_from\_file(source).
    - Evaluate Platform.msgprint(translated “{0} is rendered from an HTML file, so this format starts from the standard layout”.format(source.name), alert = true).
    - Set source from no value.
- If source.
  - Set doc.format\_data from source.format\_data.
  - For each fieldname in COPIED\_PRINT\_OPTIONS.
    - Evaluate doc.set(fieldname, source.get(fieldname)).
  - If (not doc.format\_data or is\_classic\_layout(doc.format\_data)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.format\_data → is\_classic\_layout(doc.format\_data).
    - Evaluate convert\_print\_format(doc).
    - Set doc.classic\_format\_data from no value.
- Otherwise.
  - Bind dependencies create\_default\_layout.
  - Set doc.format\_data from Platform.as\_json(create\_default\_layout(Platform.get\_meta(doctype))).
- Evaluate doc.insert().
- Return doc.

**Values supplied outside this operation** effective access from source.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L49) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1738)

<a id="op-bd848b80a5d68d"></a>
### Persist conversion

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_persist_conversion`

**Inputs** doc.

**State and service calls** request set\_value on “Print Format” · call save on doc.

**Local steps**

- Bind dependencies conversion\_values.
- If doc.standard equals “Yes”.
  - Evaluate Platform.db.set\_value(“Print Format”, doc.name, mapping(“format\_data” → doc.format\_data, expand conversion\_values(doc)), update\_modified = false).
  - Evaluate Platform.clear\_cache(doctype = doc.doc\_type).
- Otherwise.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1666)

<a id="op-9bed93cbc06582"></a>
### Convert to builder

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_convert_to_builder`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Explicit results** mapping(“dropped” → dropped).

**Explicit failure paths** validation helper — translated “{0} is rendered from an HTML file and cannot be converted”.format(Platform.bold(name)) · validation helper — translated “Standard print formats can only be converted in developer mode” · validation helper — translated “{0} is not a classic print format”.format(Platform.bold(name)).

**Local steps**

- Bind dependencies convert\_print\_format, renders\_from\_file.
- Evaluate \_require\_str(name = name).
- Set doc from Platform.get\_doc(“Print Format”, name).
- Evaluate doc.check\_permission(“write”).
- If renders\_from\_file(doc).
  - Call the validation error handler Platform.throw(translated “{0} is rendered from an HTML file and cannot be converted”.format(Platform.bold(name))).
- If (doc.standard equals “Yes” and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard equals “Yes” → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Standard print formats can only be converted in developer mode”).
- Set dropped from no value when doc.print\_format\_builder\_beta, otherwise convert\_print\_format(doc).
  - Value choice on doc.print\_format\_builder\_beta — true gives no value, false gives convert\_print\_format(doc).
- If dropped is identical to no value.
  - Call the validation error handler Platform.throw(translated “{0} is not a classic print format”.format(Platform.bold(name))).
- Evaluate \_persist\_conversion(doc).
- Return mapping(“dropped” → dropped).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1661)

<a id="op-2e35f29647ee37"></a>
### Restore classic layout

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_restore_classic_layout`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Print Format” via get\_doc.

**Explicit failure paths** validation helper — translated “Standard print formats can only be restored in developer mode” · validation helper — translated “{0} has no classic layout to restore”.format(Platform.bold(name)).

**Local steps**

- Bind dependencies restore\_classic\_format.
- Evaluate \_require\_str(name = name).
- Set doc from Platform.get\_doc(“Print Format”, name).
- Evaluate doc.check\_permission(“write”).
- If (doc.standard equals “Yes” and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard equals “Yes” → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Standard print formats can only be restored in developer mode”).
- If not restore\_classic\_format(doc).
  - Call the validation error handler Platform.throw(translated “{0} has no classic layout to restore”.format(Platform.bold(name))).
- Evaluate \_persist\_conversion(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1675)

<a id="op-71704ce5a68121"></a>
### Draft payload

`operation_foundation_printing_record_definitions_print_format_business_behavior_draft_payload`

**Inputs** data.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from data.items() where key belongs to BUILDER\_DRAFT\_FIELDS.

**Explicit failure paths** validation helper — translated “Draft data must be an object”.

**Local steps**

- Set data from Platform.parse\_json(data) when data, otherwise mapping().
  - Value choice on data — true gives Platform.parse\_json(data), false gives mapping().
- If not isinstance(data, dict).
  - Call the validation error handler Platform.throw(translated “Draft data must be an object”).
- Return mapping of key → value for tuple(key, value) drawn from data.items() where key belongs to BUILDER\_DRAFT\_FIELDS.
  - Draw tuple(key, value) from data.items(), keep a combination only if (key belongs to BUILDER\_DRAFT\_FIELDS).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L1720) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1740)

<a id="op-39791889d48bfe"></a>
### Writable format

`operation_foundation_printing_record_definitions_print_format_business_behavior_writable_format`

**Inputs** name, modified.

**Record and data access** resolve a document from “Print Format” via get\_doc · read “Print Format” via get\_value.

**Explicit results** doc.

**Explicit failure paths** validation helper with Platform.TimestampMismatchError — translated “{0} has changed since you opened it. Refresh to get the latest version.”.format(Platform.bold(name)).

**Local steps**

- Set doc from Platform.get\_doc(“Print Format”, name).
- Evaluate doc.check\_permission(“write”).
- Set current from Platform.db.get\_value(“Print Format”, name, “modified”, for\_update = true).
- If Platform.utils.cstr(current) differs from Platform.utils.cstr(modified).
  - Call the validation error handler Platform.throw(translated “{0} has changed since you opened it. Refresh to get the latest version.”.format(Platform.bold(name)), Platform.TimestampMismatchError).
- Return doc.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L1950) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1759)

<a id="op-39fb6ce847801b"></a>
### Save draft

`operation_foundation_printing_record_definitions_print_format_business_behavior_save_draft`

**Inputs** name, data, modified.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on doc.

**Explicit results** doc.modified.

**Local steps**

- Set doc from \_writable\_format(name, modified).
- Set payload from \_draft\_payload(data).
- Evaluate \_check\_draft(doc, payload).
- Evaluate doc.db\_set(“draft\_data”, Platform.as\_json(payload)).
- Return doc.modified.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L58) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1758)

<a id="op-71bbd303b76b22"></a>
### Check draft

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_check_draft`

**Inputs** doc, payload.

**Local steps**

- For each tuple(field, value) in payload.items().
  - Evaluate doc.set(field, value).
- Evaluate doc.validate\_colors().
- Evaluate doc.validate\_conditions().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1660)
