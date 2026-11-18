# Shared value and file services · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Typst emitter

<a id="op-96622ac65b6bfb"></a>
### Typst Emitter.data field

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_data_field`

**Inputs** self, section, df, value\_markup = no value.

**Declared result** str.

**State and service calls** call insert on value\_args.

**Explicit results** empty text · self.\_text\_props(df, body) · \_aligned(self.\_text\_props(df, body), align) · \_aligned(self.\_text\_props(df, value\_text), “center”).

**Local steps**

- Set value from self.\_formatted\_value(df).
- If (not value and not df.get(“show\_empty”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not value → not df.get(“show\_empty”).
  - Return empty text.
- Set show\_label from (df.get(“show\_label”) or “show”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“show\_label”) → “show”.
- Set inline from (show\_label equals “inline” or section.get(“field\_orientation”) equals “left-right”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in show\_label equals “inline” → section.get(“field\_orientation”) equals “left-right”.
- Set label\_color from self.\_label\_color(df).
- Set value\_color from safe\_color(df.get(“value\_color”)).
- Set label from empty text.
- If (show\_label differs from “hide” and df.get(“label”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in show\_label differs from “hide” → df.get(“label”).
  - Set colon from (((show\_label equals “inline” and section.get(“field\_orientation”) differs from “left-right”) or self.print\_format.get(“show\_label\_colon”)) and not df.get(“hide\_colon”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ((show\_label equals “inline” and section.get(“field\_orientation”) differs from “left-right”) or self.print\_format.get(“show\_label\_colon”)) → not df.get(“hide\_colon”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (show\_label equals “inline” and section.get(“field\_orientation”) differs from “left-right”) → self.print\_format.get(“show\_label\_colon”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in show\_label equals “inline” → section.get(“field\_orientation”) differs from “left-right”.
  - Set label from muted\_text((translated df at “label” + “:” when colon, otherwise empty text), label\_color).
    - Value choice on colon — true gives “:”, false gives empty text.
- Set value\_args from list(q(value)).
- If value\_color.
  - Evaluate value\_args.insert(0, formatted text fill: rgb("{value\_color}")).
- Set value\_text from formatted text #text({“, ”.join(value\_args)}) when value\_markup is identical to no value, otherwise value\_markup.
  - Value choice on value\_markup is identical to no value — true gives formatted text #text({“, ”.join(value\_args)}), false gives value\_markup.
- Set align from df.get(“align”).
- Set gap\_effect from translate\_custom\_style((nested operand in the contract.get(“custom\_style”) or empty text)) at 0.get(“gap”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“custom\_style”) → empty text.
- If (inline and label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in inline → label.
  - Set gap\_pt from gap\_effect.
  - If gap\_pt is identical to no value.
    - Set gap from df.get(“label\_gap”).
    - Set gap\_pt from pt(gap) when gap, otherwise 4.
      - Value choice on gap — true gives pt(gap), false gives 4.
  - If (align belongs to tuple(“center”, “right”) and section.get(“field\_orientation”) differs from “left-right”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in align belongs to tuple(“center”, “right”) → section.get(“field\_orientation”) differs from “left-right”.
    - Set body from formatted text #grid(columns: (auto, 1fr), column-gutter: {gap\_pt}pt, &#91;{label}&#93;, &#91;#align({align})&#91;{value\_text}&#93;&#93;).
    - Return self.\_text\_props(df, body).
  - If (section.get(“field\_orientation”) equals “left-right” and align does not belong to tuple(“center”, “right”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“field\_orientation”) equals “left-right” → align does not belong to tuple(“center”, “right”).
    - If df.get(“label\_justify”) equals “space-between”.
      - Set body from formatted text #grid(columns: (auto, 1fr), column-gutter: {gap\_pt}pt, &#91;{label}&#93;, &#91;#align(right)&#91;{value\_text}&#93;&#93;).
      - Return self.\_text\_props(df, body).
    - If df.get(“label\_justify”) equals “space-evenly”.
      - Set body from formatted text #grid(columns: (1fr, auto, 1fr, auto, 1fr), column-gutter: {gap\_pt}pt, &#91;&#93;, &#91;{label}&#93;, &#91;&#93;, &#91;{value\_text}&#93;, &#91;&#93;).
      - Return self.\_text\_props(df, body).
  - Set body from formatted text #grid(columns: (auto, auto), column-gutter: {gap\_pt}pt, &#91;{label}&#93;, &#91;{value\_text}&#93;).
  - Return \_aligned(self.\_text\_props(df, body), align).
- If (show\_label equals “hide” and section.get(“field\_orientation”) equals “left-right” and align does not belong to tuple(“center”, “right”) and df.get(“label\_justify”) equals “space-evenly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in show\_label equals “hide” → section.get(“field\_orientation”) equals “left-right” → align does not belong to tuple(“center”, “right”) → df.get(“label\_justify”) equals “space-evenly”.
  - Return \_aligned(self.\_text\_props(df, value\_text), “center”).
- Set spacing from gap\_effect when gap\_effect is distinct from no value, otherwise 4.
  - Value choice on gap\_effect is distinct from no value — true gives gap\_effect, false gives 4.
- Set parts from list(formatted text &#91;{label}&#93;) when label, otherwise list().
  - Value choice on label — true gives list(formatted text &#91;{label}&#93;), false gives list().
- Evaluate parts.append(formatted text &#91;{value\_text}&#93;).
- Set body from ((formatted text #stack(spacing: {spacing}pt,  + “,\\n”.join(parts)) + “)”) when len(parts) &gt; 1, otherwise value\_text.
  - Value choice on len(parts) &gt; 1 — true gives ((formatted text #stack(spacing: {spacing}pt,  + “,\\n”.join(parts)) + “)”), false gives value\_text.
- Return \_aligned(self.\_text\_props(df, body), align).

**Methods declared on this owner** [formatted value](operations-052.md#op-c7b95df7bc89d4), [label color](operations-052.md#op-dfb10469774078), [text props](operations-053.md#op-01f06b410a435f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L100) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L55) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1005)

<a id="op-01f06b410a435f"></a>
### Typst Emitter.text props

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_text_props`

**Inputs** self, df, body.

**Declared result** str.

**Explicit results** formatted text #text({“, ”.join(props)})&#91;{body}&#93; when props, otherwise body.

**Local steps**

- Set props from list().
- If df.get(“bold”).
  - Evaluate props.append(“weight: "bold"”).
- If df.get(“font\_size”).
  - Evaluate props.append(formatted text size: {pt(Platform.utils.flt(df.get(“font\_size”)))}pt).
- Return formatted text #text({“, ”.join(props)})&#91;{body}&#93; when props, otherwise body.
  - Value choice on props — true gives formatted text #text({“, ”.join(props)})&#91;{body}&#93;, false gives body.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L32) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L425)

<a id="op-29c455a1ef59b0"></a>
### Typst Emitter.asset

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_asset`

**Inputs** self, suffix, data.

**Declared result** str.

**Explicit results** name.

**Local steps**

- Set name from formatted text asset\_{len(self.assets)}.{suffix}.
- Set self.assets at name from data.
- Return name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0518.json#L1191) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L50) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1000)

<a id="op-fa67082045ad73"></a>
### Typst Emitter.read site file

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_read_site_file`

**Inputs** self, src.

**Declared result** (bytes bitwise or no value).

**Record and data access** read “File” via get\_all.

**Explicit results** base64.b64decode(src.split(“,”, 1) at 1) · no value · f.read().

**Local steps**

- Bind dependencies base64.
- Bind dependencies os.
- If src.startswith(“data:”).
  - Attempt the following.
    - Return base64.b64decode(src.split(“,”, 1) at 1).
  - On failure (Exception).
    - Return no value.
- If src.startswith(tuple(text in the contract, text in the contract)).
  - Return no value.
- Set src from src.split(“?”, 1) at 0.
- If src.startswith(“/private/files/”).
  - Set file\_names from Platform.get\_all(“File”, filters = mapping(“file\_url” → src), pluck = “name”).
  - If not any(generator of Platform.has\_permission(“File”, doc = name, ptype = “read”) for name drawn from file\_names).
    - Draw name from file\_names.
    - Return no value.
  - Set tuple(root, rel) from tuple(Platform.get\_site\_path(“private”, “files”), src at slice len(“/private/files/”) to no value).
- Otherwise.
  - If src.startswith(“/files/”).
    - Set tuple(root, rel) from tuple(Platform.get\_site\_path(“public”, “files”), src at slice len(“/files/”) to no value).
  - Otherwise.
    - If src.startswith(“/assets/”).
      - Set tuple(app, \_, rel) from src at slice len(“/assets/”) to no value.partition(“/”).
      - If (not rel or app belongs to tuple(empty text, “.”, “..”) or app does not belong to os.listdir(Platform.get\_site\_path(“..”, “assets”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rel → app belongs to tuple(empty text, “.”, “..”) → app does not belong to os.listdir(Platform.get\_site\_path(“..”, “assets”)).
        - Return no value.
      - Set root from Platform.get\_site\_path(“..”, “assets”, app).
    - Otherwise.
      - Return no value.
- Set root from os.path.realpath(root).
- Set path from os.path.realpath(os.path.join(root, rel)).
- If not path.startswith((root + os.sep)).
  - Return no value.
- Attempt the following.
  - Within open(path, “rb”) bound as f.
    - Return f.read().
- On failure (OSError).
  - Return no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“File”, doc = name, ptype = “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L109) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L70) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1020)

<a id="op-f239f39f0ce6e2"></a>
### Typst Emitter.dimension

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_dimension`

**Inputs** width.

**Wrappers, in declaration order** staticmethod.

**Declared result** (str bitwise or no value).

**Explicit results** no value · value · formatted text {pt(value)}pt.

**Local steps**

- If width belongs to tuple(no value, empty text).
  - Return no value.
- Set value from str(width).strip().
- If re.fullmatch(“\\d+(\\.\\d+)?(mm\|cm\|in\|pt\|%)”, value).
  - Return value.
- If value.endswith(“px”).
  - Set value from value at slice no value to negative 2.
- Attempt the following.
  - Return formatted text {pt(value)}pt.
- On failure (ValueError).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0518.json#L2317) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L56) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1006)

<a id="op-427a3d6ca5201b"></a>
### Typst Emitter.embed image

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_embed_image`

**Inputs** self, src.

**Declared result** (str bitwise or no value).

**Explicit results** no value · self.\_embedded at src · name.

**Local steps**

- Bind dependencies io.
- Bind dependencies suppress.
- Bind dependencies ElementTree.
- Bind dependencies Image, ImageFile.
- If not src.
  - Return no value.
- Set src from str(src).
- If src belongs to self.\_embedded.
  - Return self.\_embedded at src.
- Set data from self.\_read\_site\_file(src).
- Set name from no value.
- If data is distinct from no value.
  - Set kind from filetype.image\_match(data).
  - Within suppress(OSError, SyntaxError, Image.DecompressionBombError).
    - If (kind and kind.extension belongs to tuple(“png”, “apng”, “jpg”, “gif”, …)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in kind → kind.extension belongs to tuple(“png”, “apng”, “jpg”, “gif”, …).
      - If kind.extension equals “gif”.
        - Set parser from ImageFile.Parser().
        - Evaluate parser.feed(data).
        - Evaluate parser.close().
      - Otherwise.
        - Within Image.open(io.BytesIO(data)) bound as image.
          - Evaluate image.verify().
      - Set name from self.\_asset(“png” when kind.extension equals “apng”, otherwise kind.extension, data).
        - Value choice on kind.extension equals “apng” — true gives “png”, false gives kind.extension.
    - Otherwise.
      - If (not kind and nested operand in the contract(nested operand in the contract, nested operand in the contract) at 0.lower().endswith(“.svg”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kind → nested operand in the contract.split(“?”, 1) at 0.lower().endswith(“.svg”).
        - Set root from ElementTree.fromstring(data, ElementTree.XMLParser(encoding = “utf-8”)).
        - If root.tag.rpartition(“}”) at 2 equals “svg”.
          - Set name from self.\_asset(“svg”, data).
- Set self.\_embedded at src from name.
- Return name.

**Methods declared on this owner** [read site file](operations-053.md#op-fa67082045ad73), [asset](operations-053.md#op-29c455a1ef59b0).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L101) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L57) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1007)

<a id="op-f5868eed3a48cc"></a>
### Typst Emitter.image

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_image`

**Inputs** self, df.

**Declared result** str.

**Explicit results** empty text · \_aligned(formatted text #image("{name}", width: {width}), df.get(“align”)).

**Explicit failure paths** validation helper — translated “The Typst renderer cannot embed this image: {0}”.format(Platform.bold(str(src) at slice no value to 100)).

**Local steps**

- Set src from (df.get(“image\_url”) or df.get(“\_value”) or self.doc.get(df.get(“fieldname”)) when df.get(“fieldname”), otherwise empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“image\_url”) → df.get(“\_value”) → self.doc.get(df.get(“fieldname”)) when df.get(“fieldname”), otherwise empty text.
  - Value choice on df.get(“fieldname”) — true gives self.doc.get(df.get(“fieldname”)), false gives empty text.
- If not src.
  - Return empty text.
- Set name from self.\_embed\_image(src).
- If name is identical to no value.
  - If df.get(“image\_url”).
    - Call the validation error handler Platform.throw(translated “The Typst renderer cannot embed this image: {0}”.format(Platform.bold(str(src) at slice no value to 100)), title = translated “Typst renderer unavailable”).
  - Return empty text.
- Set width from (self.\_dimension(df.get(“width”)) or “100%”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_dimension(df.get(“width”)) → “100%”.
- Return \_aligned(formatted text #image("{name}", width: {width}), df.get(“align”)).

**Methods declared on this owner** [embed image](operations-053.md#op-427a3d6ca5201b), [dimension](operations-053.md#op-f239f39f0ce6e2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L104) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L62) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1012)

<a id="op-cf23d0eca43f58"></a>
### Typst Emitter.barcode

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_barcode`

**Inputs** self, df.

**Declared result** str.

**Explicit results** empty text · \_aligned(formatted text #image("{name}", width: {width}), df.get(“align”)).

**Local steps**

- Set data\_uri from df.get(“\_qr\_data\_uri”).
- If not data\_uri.
  - Return empty text.
- Set data from self.\_read\_site\_file(data\_uri).
- If data is identical to no value.
  - Return empty text.
- Set name from self.\_asset(“svg”, data).
- Set width from (self.\_dimension(df.get(“width”)) or “35mm”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_dimension(df.get(“width”)) → “35mm”.
- Return \_aligned(formatted text #image("{name}", width: {width}), df.get(“align”)).

**Methods declared on this owner** [read site file](operations-053.md#op-fa67082045ad73), [asset](operations-053.md#op-29c455a1ef59b0), [dimension](operations-053.md#op-f239f39f0ce6e2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0518.json#L3533) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L51) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1001)

<a id="op-a389865e21662b"></a>
### Typst Emitter.rating

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_rating`

**Inputs** self, df.

**Declared result** str.

**Explicit results** formatted text #box(image("{self.\_asset(“svg”, svg.encode())}", height: 1.5em)).

**Local steps**

- Set total from (Platform.utils.cint(df.get(“options”)) or 5).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.cint(df.get(“options”)) → 5.
- Set filled from min(int(((nested operand in the contract.utils.flt(nested operand in the contract.get(nested operand in the contract(nested operand in the contract))) × total) + 0.5)), total).
- Set stars from empty text.join(generator of formatted text &lt;path transform="translate({(24 × i)})" fill="{color}" stroke="{color}" d="{RATING\_STAR\_PATH}"/&gt; for tuple(i, color) drawn from enumerate(((list(“#f6c35e”) × fil ….
  - Draw tuple(i, color) from enumerate(((list(“#f6c35e”) × filled) + (list(“#dce0e3”) × (total − filled)))).
- Set svg from formatted command or address in the contract.
- Return formatted text #box(image("{self.\_asset(“svg”, svg.encode())}", height: 1.5em)).

**Methods declared on this owner** [asset](operations-053.md#op-29c455a1ef59b0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L29) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L422)

<a id="op-993d1844e0aede"></a>
### Typst Emitter.repeater

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_repeater`

**Inputs** self, df.

**Declared result** str.

**Explicit results** empty text · (((self.\_block\_label(df) + formatted text #table(columns: ({“, ”.join(widths)}), align: ({“, ”.join(aligns)},), stroke: none, inset: 4pt, ) + “,\\n”.join(cells)) + “)”).

**Local steps**

- Set source from df.get(“source”).
- Set rows from df.get(“\_rows”) when df.get(“\_rows”) is distinct from no value, otherwise self.doc.get(source) when source, otherwise no value.
  - Value choice on df.get(“\_rows”) is distinct from no value — true gives df.get(“\_rows”), false gives self.doc.get(source) when source, otherwise no value.
  - Value choice on source — true gives self.doc.get(source), false gives no value.
- Set rows from (rows or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().
- Set columns from (df.get(“repeater\_columns”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“repeater\_columns”) → list().
- If (not rows or not columns).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rows → not columns.
  - Return empty text.
- Set widths from \_fr\_widths(columns).
- Set aligns from list of col.get(“align”) when col.get(“align”) belongs to tuple(“left”, “center”, “right”), otherwise “left” for col drawn from columns.
  - Draw col from columns.
  - Value choice on col.get(“align”) belongs to tuple(“left”, “center”, “right”) — true gives col.get(“align”), false gives “left”.
- Set fills from list of formatted text fill: rgb("{color}"),  when color bound to safe\_color(col.get(“color”)), otherwise empty text for col drawn from columns.
  - Draw col from columns.
  - Value choice on color bound to safe\_color(col.get(“color”)) — true gives formatted text fill: rgb("{color}"), , false gives empty text.
- Set cells from list().
- For each row in rows.
  - For each tuple(col, fill) in zip(columns, fills, strict = true).
    - Set parts from list().
    - For each tok in (col.get(“template”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“template”) → list().
      - If not isinstance(tok, dict).
        - Continue with the next iteration or loop test.
      - If tok.get(“t”) equals “f”.
        - Evaluate parts.append(\_text\_value(row.get\_formatted(tok.get(“v”)))).
      - Otherwise.
        - Evaluate parts.append(str((tok.get(“v”) or empty text))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in tok.get(“v”) → empty text.
    - Set text from empty text.join(parts).
    - Evaluate cells.append(formatted text &#91;#text({fill}{q(text)})&#93; when text, otherwise “&#91;&#93;”).
      - Value choice on text — true gives formatted text &#91;#text({fill}{q(text)})&#93;, false gives “&#91;&#93;”.
- Return (((self.\_block\_label(df) + formatted text #table(columns: ({“, ”.join(widths)}), align: ({“, ”.join(aligns)},), stroke: none, inset: 4pt, ) + “,\\n”.join(cells)) + “)”).

**Methods declared on this owner** [block label](operations-053.md#op-4106d12b9bb197).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0518.json#L3864) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L71) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1021)

<a id="op-b4fee85ac437ba"></a>
### Typst Emitter.table

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_table`

**Inputs** self, df, keep\_together = false.

**Declared result** str.

**Explicit results** empty text · ((self.\_block\_label(df) + earlier\_pages) + self.\_min\_height(df, tables at negative 1, len(columns), stroke equals rule)).

**Local steps**

- Set columns from (df.get(“table\_columns”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“table\_columns”) → list().
- If not columns.
  - Return empty text.
- Set rows from df.get(“\_rows”) when df.get(“\_rows”) is distinct from no value, otherwise self.doc.get(df.get(“fieldname”)).
  - Value choice on df.get(“\_rows”) is distinct from no value — true gives df.get(“\_rows”), false gives self.doc.get(df.get(“fieldname”)).
- Set rows from (rows or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().
- If not rows.
  - Return empty text.
- Set widths from \_fr\_widths(columns).
- Set aligns from list of “right” when col.get(“fieldtype”) belongs to RIGHT\_ALIGNED\_FIELDTYPES, otherwise “left” for col drawn from columns.
  - Draw col from columns.
  - Value choice on col.get(“fieldtype”) belongs to RIGHT\_ALIGNED\_FIELDTYPES — true gives “right”, false gives “left”.
- Set header\_cells from list of formatted text #text(weight: 600, size: 0.85em, {q(translated (nested operand in the contract.get(“label”) or empty text))}) for col drawn from columns.
  - Draw col from columns.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“label”) → empty text.
- Set pages from list(list()).
- For each tuple(i, row) in enumerate(rows).
  - If (i and row.get(“page\_break”) and not keep\_together).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in i → row.get(“page\_break”) → not keep\_together.
    - Evaluate pages.append(list()).
  - Update pages at negative 1 using + list of self.\_table\_cell(row, col) for col drawn from columns.
    - Draw col from columns.
- Set header\_mode from df.get(“table\_header”).
- Set show\_header from header\_mode differs from “none”.
- Set header\_bg from no value when header\_mode equals “plain”, otherwise (safe\_color(df.get(“table\_header\_bg”)) or “#f3f4f6”).
  - Value choice on header\_mode equals “plain” — true gives no value, false gives (safe\_color(df.get(“table\_header\_bg”)) or “#f3f4f6”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in safe\_color(df.get(“table\_header\_bg”)) → “#f3f4f6”.
- Set rule from hairline(df.get(“table\_border\_color”)).
- If (df.get(“table\_bordered”) is distinct from false or df.get(“table\_style”) equals “bordered”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“table\_bordered”) is distinct from false → df.get(“table\_style”) equals “bordered”.
  - Set stroke from rule.
- Otherwise.
  - Set stroke from formatted text (\_, y) =&gt; if y &gt; 0 { (top: {rule}) }.
- Set parts from list(formatted text columns: ({“, ”.join(widths)}), formatted text align: ({“, ”.join(aligns)},), formatted text stroke: {stroke}, formatted text inset: {pt(df.get(“table\_cell\_padding”), 8)}pt).
- If show\_header.
  - If header\_bg.
    - Evaluate parts.append(formatted text fill: (\_, row) =&gt; if row == 0 { rgb("{header\_bg}") }).
  - Set cells from list(((“table.header(” + “, ”.join(generator of formatted text &#91;{cell}&#93; for cell drawn from header\_cells)) + “)”)).
    - Draw cell from header\_cells.
- Otherwise.
  - Set cells from list().
- Set tables from list of (((“table(” + “, ”.join(parts)) + “,\\n”) + “,\\n”.join((cells + list of formatted text &#91;{cell}&#93; for cell drawn from page))) for page drawn from pages.
  - Draw page from pages.
  - Draw cell from page.
- Set earlier\_pages from empty text.join(generator of formatted text #{table}) #colbreak()  for table drawn from tables at slice no value to negative 1).
  - Draw table from tables at slice no value to negative 1.
- Return ((self.\_block\_label(df) + earlier\_pages) + self.\_min\_height(df, tables at negative 1, len(columns), stroke equals rule)).

**Methods declared on this owner** [table cell](operations-053.md#op-def6fb4278ec7d), [block label](operations-053.md#op-4106d12b9bb197), [min height](operations-053.md#op-47bf9d8e62ef75).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L4) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L74) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1024)

<a id="op-47bf9d8e62ef75"></a>
### Typst Emitter.min height

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_min_height`

**Inputs** df, table, ncols, bordered.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** ((“#” + table) + “)”) · formatted text #layout(size =&gt; { let tbl = {table}) let h = measure(tbl, width: size.width).height if h &lt; {min\_height}pt { {table}, {cap}) } else { tbl } }).

**Local steps**

- Set min\_height from pt(df.get(“table\_min\_height”)).
- If not min\_height.
  - Return ((“#” + table) + “)”).
- Set cap from formatted text table.cell(colspan: {ncols}, inset: 0pt{empty text when bordered, otherwise “, stroke: none”})&#91;#v({min\_height}pt - h)&#93;.
  - Value choice on bordered — true gives empty text, false gives “, stroke: none”.
- Return formatted text #layout(size =&gt; { let tbl = {table}) let h = measure(tbl, width: size.width).height if h &lt; {min\_height}pt { {table}, {cap}) } else { tbl } }).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L26) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L419)

<a id="op-4106d12b9bb197"></a>
### Typst Emitter.block label

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_block_label`

**Inputs** self, df.

**Declared result** str.

**Explicit results** empty text · (muted\_text(translated df at “label”, self.\_label\_color()) + “\\n#v(3pt)\\n”).

**Local steps**

- If (not df.get(“label”) or (df.get(“show\_label”) or “show”) equals “hide”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df.get(“label”) → (df.get(“show\_label”) or “show”) equals “hide”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“show\_label”) → “show”.
  - Return empty text.
- Return (muted\_text(translated df at “label”, self.\_label\_color()) + “\\n#v(3pt)\\n”).

**Methods declared on this owner** [label color](operations-052.md#op-dfb10469774078).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0518.json#L6226) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L52) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1002)

<a id="op-def6fb4278ec7d"></a>
### Typst Emitter.table cell

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_table_cell`

**Inputs** self, row, col.

**Declared result** str.

**Explicit results** thumb · formatted text #grid(columns: (auto, 1fr), column-gutter: 6pt, align: top, &#91;{thumb}&#93;, &#91;{body}&#93;) · body · empty text · formatted text #text({q(row.get(“idx”))}) · 2 additional forms in the steps below.

**Local steps**

- Bind dependencies format\_field\_value.
- Set merged from col.get(“merged\_fields”).
- If merged.
  - Set merged from list(mapping(“fieldname” → col.get(“fieldname”), “fieldtype” → col.get(“fieldtype”), “date\_format” → col.get(“date\_format”)), expanded merged).
  - Set img\_fn from next(generator of mf.get(“fieldname”) for mf drawn from merged where (mf.get(“fieldname”) and mf.get(“fieldtype”) belongs to MERGE\_IMAGE\_FIELDTYPES), no value).
    - Draw mf from merged, keep a combination only if ((mf.get(“fieldname”) and mf.get(“fieldtype”) belongs to MERGE\_IMAGE\_FIELDTYPES)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in mf.get(“fieldname”) → mf.get(“fieldtype”) belongs to MERGE\_IMAGE\_FIELDTYPES.
  - Set lines from list().
  - Set first\_text from true.
  - For each mf in merged.
    - Set fieldname from mf.get(“fieldname”).
    - If (not fieldname or mf.get(“fieldtype”) belongs to MERGE\_IMAGE\_FIELDTYPES).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fieldname → mf.get(“fieldtype”) belongs to MERGE\_IMAGE\_FIELDTYPES.
      - Continue with the next iteration or loop test.
    - Set raw from format\_field\_value(row, mf).
    - Set value from \_text\_value(empty text when raw is identical to no value, otherwise str(raw)).
      - Value choice on raw is identical to no value — true gives empty text, false gives str(raw).
    - If not value.strip().
      - Continue with the next iteration or loop test.
    - Set label from empty text.
    - If mf.get(“show\_label”).
      - Set doctype from row.get(“doctype”).
      - Set label from (\_((nested operand in the contract.get\_meta(doctype).get\_label(fieldname) or fieldname), context = doctype) + “:”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_meta(doctype).get\_label(fieldname) → fieldname.
    - If first\_text.
      - Set line from formatted text #text(weight: 500, {q(value)}).
      - If label.
        - Set line from formatted text #text(weight: 600, {q(label)}) {line}.
      - Set first\_text from false.
    - Otherwise.
      - Set line from muted\_text(value).
      - If label.
        - Set line from formatted text #text(size: 0.85em, weight: 600, fill: rgb("{MUTED}"), {q(label)}) {line}.
    - Evaluate lines.append(line).
  - If not lines.
    - Set body from empty text.
  - Otherwise.
    - If len(lines) equals 1.
      - Set body from lines at 0.
    - Otherwise.
      - If col.get(“merge\_direction”) equals “horizontal”.
        - Set body from “ #h(3pt) ”.join(lines).
      - Otherwise.
        - Set body from ((“#stack(spacing: 3pt, ” + “, ”.join(generator of formatted text &#91;{line}&#93; for line drawn from lines)) + “)”).
          - Draw line from lines.
  - If img\_fn.
    - Set thumb from self.\_table\_thumb(row, col, img\_fn, merged).
    - If not body.
      - Return thumb.
    - Return formatted text #grid(columns: (auto, 1fr), column-gutter: 6pt, align: top, &#91;{thumb}&#93;, &#91;{body}&#93;).
  - Return body.
- Set fieldname from col.get(“fieldname”).
- If not fieldname.
  - Return empty text.
- If fieldname equals “idx”.
  - Return formatted text #text({q(row.get(“idx”))}).
- Set fieldtype from col.get(“fieldtype”).
- Set src from row.get((col.get(“options”) or empty text)) when fieldtype equals “Image”, otherwise row.get(fieldname).
  - Value choice on fieldtype equals “Image” — true gives row.get((col.get(“options”) or empty text)), false gives row.get(fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“options”) → empty text.
- If is\_image\_column(fieldtype, src).
  - Set name from self.\_embed\_image(src).
  - If not name.
    - Return empty text.
  - Return formatted text #box(width: 100%, height: 75pt)&#91;#image("{name}", width: 100%, height: 100%, fit: "contain")&#93;.
- Return formatted text #text({q(\_text\_value(format\_field\_value(row, col)))}).

**Methods declared on this owner** [table thumb](operations-053.md#op-ac7975ccf6d209), [embed image](operations-053.md#op-427a3d6ca5201b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L5) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L75) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1025)

<a id="op-ac7975ccf6d209"></a>
### Typst Emitter.table thumb

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_table_thumb`

**Inputs** self, row, col, img\_fn, merged.

**Declared result** str.

**Explicit results** formatted text #box(width: {size}pt, height: {size}pt, radius: 4.5pt, clip: true)&#91;#image("{name}", width: {size}pt, height: {size}pt, fit: "cover")&#93; · formatted text #box(width: {size}pt, height: {size}pt, radius: 4.5pt, fill: color.hsl({hue}deg, 65%, 92%))&#91;#align(center + horizon)&#91;#text(size: {round((size × 0.4),.

**Local steps**

- Set size from pt(Platform.utils.cint(col.get(“image\_size”)), 40).
- Set src from str((row.get(img\_fn) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(img\_fn) → empty text.
- Set img\_type from next(generator of mf.get(“fieldtype”) for mf drawn from merged where mf.get(“fieldname”) equals img\_fn, no value).
  - Draw mf from merged, keep a combination only if (mf.get(“fieldname”) equals img\_fn).
- Set name from no value.
- If is\_image\_column(img\_type, src).
  - Set name from self.\_embed\_image(src).
- If name.
  - Return formatted text #box(width: {size}pt, height: {size}pt, radius: 4.5pt, clip: true)&#91;#image("{name}", width: {size}pt, height: {size}pt, fit: "cover")&#93;.
- Set first\_txt from next(generator of str((row.get(mf at “fieldname”) or empty text)) for mf drawn from merged where (mf.get(“fieldname”) and mf at “fieldname” differs from img\_fn), empty text).
  - Draw mf from merged, keep a combination only if ((mf.get(“fieldname”) and mf at “fieldname” differs from img\_fn)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(mf at “fieldname”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mf.get(“fieldname”) → mf at “fieldname” differs from img\_fn.
- Set abbr from (Platform.utils.get\_abbr(first\_txt) or “?”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.get\_abbr(first\_txt) → “?”.
- Set idx from “abcdefghijklmnopqrstuvwxyz0123456789”.find((abbr at slice no value to 1 or “a”).lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in abbr at slice no value to 1 → “a”.
- Set hue from ((max(idx, 0) × 37) modulo or format 360).
- Return formatted text #box(width: {size}pt, height: {size}pt, radius: 4.5pt, fill: color.hsl({hue}deg, 65%, 92%))&#91;#align(center + horizon)&#91;#text(size: {round((size × 0.4),.

**Methods declared on this owner** [embed image](operations-053.md#op-427a3d6ca5201b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L76) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1026)

## Service · User

<a id="op-d18703cca3ecb2"></a>
### User Permissions.initialize

`operation_foundation_utils_user_business_behavior_user_permissions_initialize`

**Inputs** self, name = empty text.

**Local steps**

- Set self.defaults from no value.
- Set self.name from (name or Platform.session.get(“user”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → Platform.session.get(“user”).
- Set self.roles from list().
- Set self.all\_read from list().
- Set self.can\_create from list().
- Set self.can\_select from list().
- Set self.can\_read from list().
- Set self.can\_write from list().
- Set self.can\_submit from list().
- Set self.can\_cancel from list().
- Set self.can\_delete from list().
- Set self.can\_search from list().
- Set self.can\_get\_report from list().
- Set self.can\_import from list().
- Set self.can\_export from list().
- Set self.can\_print from list().
- Set self.can\_email from list().
- Set self.allow\_modules from list().
- Set self.permitted\_modules from list().
- Set self.in\_create from list().
- Evaluate self.setup\_user().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup user](operations-053.md#op-69f8f769763d75).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L13) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1051)

<a id="op-69f8f769763d75"></a>
### User Permissions.setup user

`operation_foundation_utils_user_business_behavior_user_permissions_setup_user`

**Inputs** self.

**Record and data access** resolve a document from user\_doc via get\_doc.

**Local steps**

- Bind local operation get\_user\_doc for subsequent calls.
- If (not Platform.flags.in\_install\_db and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.in\_install\_db → not Platform.in\_test.
  - Set user\_doc from Platform.cache.hget(“user\_doc”, self.name, get\_user\_doc).
  - If user\_doc.
    - Set self.doc from Platform.get\_doc(user\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1053)

<a id="op-3d389157775679"></a>
### User Permissions.setup user.get user doc

`operation_foundation_utils_user_business_behavior_user_permissions_setup_user_get_user_record`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “User” via get\_doc.

**Explicit results** user.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set user from no value.
- Attempt the following.
  - Set user from Platform.get\_doc(“User”, self.name).as\_dict().
- On failure (Platform.DoesNotExistError).
  - Take no action here.
- On failure (Exception) bound to e.
  - If not Platform.db.is\_table\_missing(e).
    - Propagate the active failure.
- Return user.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L1727) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1054)

<a id="op-2f243219c66d92"></a>
### User Permissions.get roles

`operation_foundation_utils_user_business_behavior_user_permissions_get_roles`

**Inputs** self.

**Explicit results** self.roles.

**Local steps**

- If not self.roles.
  - Set self.roles from get\_roles(self.name).
- Return self.roles.

**Values supplied outside this operation** effective access from get\_roles(self.name).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L1906) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1050)

<a id="op-58a1f6ad4f4576"></a>
### User Permissions.build doctype map

`operation_foundation_utils_user_business_behavior_user_permissions_build_record_type_map`

**Inputs** self.

**Record and data access** read “DocType” via get\_all.

**Local steps**

- Set self.doctype\_map from mapping().
- Set active\_domains from Platform.get\_active\_domains().
- Set all\_doctypes from Platform.get\_all(“DocType”, fields = list(“name”, “in\_create”, “module”, “istable”, …)).
- For each dt in all\_doctypes.
  - If (not dt.restrict\_to\_domain or dt.restrict\_to\_domain belongs to active\_domains).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not dt.restrict\_to\_domain → dt.restrict\_to\_domain belongs to active\_domains.
    - Set self.doctype\_map at dt at “name” from dt.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L12) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L96) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1045)

<a id="op-c114ca664f0d90"></a>
### User Permissions.build perm map

`operation_foundation_utils_user_business_behavior_user_permissions_build_permission_map`

**Inputs** self.

**Local steps**

- Set self.perm\_map from mapping().
- For each r in get\_valid\_perms().
  - Set dt from r at “parent”.
  - If dt does not belong to self.perm\_map.
    - Set self.perm\_map at dt from mapping().
  - Set rights from get\_rights(dt).
  - For each k in rights.
    - If not self.perm\_map at dt.get(k).
      - Set self.perm\_map at dt at k from r.get(k).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L10) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L94) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1043)

<a id="op-82efdc63b420cf"></a>
### User Permissions.build permissions

`operation_foundation_utils_user_business_behavior_user_permissions_build_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 23 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L11) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L95) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1044)

<a id="op-4f77aea73a455b"></a>
### User Permissions.get defaults

`operation_foundation_utils_user_business_behavior_user_permissions_get_defaults`

**Inputs** self.

**Explicit results** self.defaults.

**Local steps**

- Bind dependencies Platform.defaults.
- Set self.defaults from Platform.defaults.get\_defaults(self.name).
- Return self.defaults.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L4932) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1049)

<a id="op-a8252c73f3eccc"></a>
### User Permissions.get

`operation_foundation_utils_user_business_behavior_user_permissions_get`

**Inputs** self, key.

**Explicit results** getattr(self, key).

**Local steps**

- If not self.can\_read.
  - Evaluate self.build\_permissions().
- Return getattr(self, key).

**Methods declared on this owner** [build permissions](operations-053.md#op-82efdc63b420cf).

**Values supplied outside this operation** selected callable from getattr(self, key).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L5027) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L97) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1046)
