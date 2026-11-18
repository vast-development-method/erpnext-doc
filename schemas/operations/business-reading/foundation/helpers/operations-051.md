# Shared value and file services · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Typst emitter

<a id="op-58bf7e94cfa000"></a>
### Barcode blocker

`operation_foundation_utils_typst_emitter_business_behavior_barcode_blocker`

**Inputs** df, print\_format.

**Explicit results** no value · no value when df.get(“barcode\_format”) equals “QR”, otherwise translated “Barcode that is not a QR code” · translated “Barcode that is not a QR code”.

**Local steps**

- If df.get(“fieldtype”) differs from “Barcode”.
  - Return no value.
- If df.get(“custom”).
  - Return no value when df.get(“barcode\_format”) equals “QR”, otherwise translated “Barcode that is not a QR code”.
    - Value choice on df.get(“barcode\_format”) equals “QR” — true gives no value, false gives translated “Barcode that is not a QR code”.
- Attempt the following.
  - Set meta\_df from Platform.get\_meta(print\_format.doc\_type).get\_field(df.get(“fieldname”)).
- On failure (Exception).
  - Set meta\_df from no value.
- Bind dependencies is\_qr\_barcode\_options.
- If (meta\_df and is\_qr\_barcode\_options(meta\_df.options)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta\_df → is\_qr\_barcode\_options(meta\_df.options).
  - Return no value.
- Return translated “Barcode that is not a QR code”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L89) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L31) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L982)

<a id="op-da6d505fad0f87"></a>
### Letterhead blockers

`operation_foundation_utils_typst_emitter_business_behavior_letterhead_blockers`

**Inputs** lh.

**Declared result** list at str.

**Explicit results** list() · blockers.

**Local steps**

- If not lh.
  - Return list().
- Set blockers from list().
- If (lh.get(“custom\_css”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lh.get(“custom\_css”) → empty text.
  - Evaluate blockers.append(translated “Letterhead with custom CSS”).
- Set header\_is\_image from (lh.get(“source”) equals “Image” and lh.get(“image”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lh.get(“source”) equals “Image” → lh.get(“image”).
- If ((lh.get(“content”) or empty text).strip() and not header\_is\_image).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (lh.get(“content”) or empty text).strip() → not header\_is\_image.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lh.get(“content”) → empty text.
  - Evaluate blockers.append(translated “Letterhead with HTML content”).
- Set footer\_is\_image from (lh.get(“footer\_source”) equals “Image” and lh.get(“footer\_image”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lh.get(“footer\_source”) equals “Image” → lh.get(“footer\_image”).
- If ((lh.get(“footer”) or empty text).strip() and not footer\_is\_image).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (lh.get(“footer”) or empty text).strip() → not footer\_is\_image.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lh.get(“footer”) → empty text.
  - Evaluate blockers.append(translated “Letterhead footer with HTML content”).
- For each image in tuple((header\_is\_image and lh.get(“image”)), (footer\_is\_image and lh.get(“footer\_image”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in header\_is\_image → lh.get(“image”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in footer\_is\_image → lh.get(“footer\_image”).
  - If (image and str(image).startswith(tuple(text in the contract, text in the contract))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in image → str(image).startswith(tuple(text in the contract, text in the contract)).
    - Evaluate blockers.append(translated “Letterhead image loaded from a web address”).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return blockers.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L94) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L40) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L990)

<a id="op-35252e3ab903f3"></a>
### Image blocker

`operation_foundation_utils_typst_emitter_business_behavior_image_blocker`

**Inputs** df.

**Explicit results** no value · translated “Image loaded from a web address”.

**Local steps**

- If df.get(“fieldtype”) differs from “Image”.
  - Return no value.
- Set src from (df.get(“image\_url”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“image\_url”) → empty text.
- If src.startswith(tuple(text in the contract, text in the contract)).
  - Return translated “Image loaded from a web address”.
- Return no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L93) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L39) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L989)

<a id="op-f88d3bba2efefc"></a>
### Unsafe colors

`operation_foundation_binding_foundation_utils_typst_emitter_unsafe_colors`

**Inputs** df.

**Explicit results** list of df.get(key) for key drawn from \_COLOR\_KEYS where (df.get(key) and not safe\_color(df.get(key))).

**Local steps**

- Return list of df.get(key) for key drawn from \_COLOR\_KEYS where (df.get(key) and not safe\_color(df.get(key))).
  - Draw key from \_COLOR\_KEYS, keep a combination only if ((df.get(key) and not safe\_color(df.get(key)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(key) → not safe\_color(df.get(key)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L33) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L426)

<a id="op-179792a9a25cd4"></a>
### Has typst blocks

`operation_foundation_utils_typst_emitter_business_behavior_has_typst_blocks`

**Inputs** layout.

**Declared result** bool.

**Explicit results** false · any(generator of (df.get(“fieldtype”) equals “Typst” and (nested operand in the contract(nested operand in the contract) or empty text).strip()) for tuple(\_where, df) drawn from iter\_nodes(layout)).

**Local steps**

- If not isinstance(layout, dict).
  - Return false.
- Return any(generator of (df.get(“fieldtype”) equals “Typst” and (nested operand in the contract(nested operand in the contract) or empty text).strip()) for tuple(\_where, df) drawn from iter\_nodes(layout)).
  - Draw tuple(\_where, df) from iter\_nodes(layout).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“fieldtype”) equals “Typst” → (df.get(“typst”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“typst”) → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L92) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L38) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L988)

<a id="op-ce8ebb51f6dc45"></a>
### Typst font paths

`operation_foundation_utils_typst_emitter_business_behavior_typst_font_paths`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list(os.path.abspath(path)) when os.path.isdir(path), otherwise list().

**Local steps**

- Bind dependencies os.
- Set path from Platform.get\_site\_path(“private”, “files”, “typst\_fonts”).
- Return list(os.path.abspath(path)) when os.path.isdir(path), otherwise list().
  - Value choice on os.path.isdir(path) — true gives list(os.path.abspath(path)), false gives list().

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L1741) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L80) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1030)

<a id="op-5437213ce3a212"></a>
### Typst fonts

`operation_foundation_binding_foundation_utils_typst_emitter_typst_fonts`

**Inputs** no declared parameters.

**Explicit results** fonts.

**Local steps**

- Bind dependencies os.
- Bind dependencies typst.
- Set paths from typst\_font\_paths().
- Set families from sorted(generator of name for name drawn from os.listdir(paths at 0) where “.” does not belong to name) when paths, otherwise list().
  - Value choice on paths — true gives sorted(generator of name for name drawn from os.listdir(paths at 0) where “.” does not belong to name), false gives list().
  - Draw name from os.listdir(paths at 0), keep a combination only if (“.” does not belong to name).
- Set key from tuple(expanded paths, expanded families).
- Set fonts from \_typst\_fonts.get(key).
- If fonts is identical to no value.
  - Set fonts from typst.Fonts(font\_paths = paths).
  - Evaluate \_typst\_fonts.clear().
  - Set \_typst\_fonts at key from fonts.
- Return fonts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L23) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L416)

<a id="op-434a1d605ff739"></a>
### Compile typst source

`operation_foundation_utils_typst_emitter_business_behavior_compile_typst_source`

**Inputs** source.

**Declared result** bytes.

**Explicit results** typst.compile(path, root = tmp, font\_paths = typst\_fonts()).

**Local steps**

- Bind dependencies os.
- Bind dependencies tempfile.
- Bind dependencies typst.
- Within tempfile.TemporaryDirectory() bound as tmp.
  - Set path from os.path.join(tmp, “main.typ”).
  - Within open(path, “w”) bound as f.
    - Evaluate f.write(source).
  - Return typst.compile(path, root = tmp, font\_paths = typst\_fonts()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L90) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L983)

<a id="op-3dbaf370c16758"></a>
### Font family

`operation_foundation_binding_foundation_utils_typst_emitter_font_family`

**Inputs** font.

**Declared result** str.

**Explicit results** font when (font and font differs from “Default”), otherwise DEFAULT\_FONT.

**Local steps**

- Return font when (font and font differs from “Default”), otherwise DEFAULT\_FONT.
  - Value choice on (font and font differs from “Default”) — true gives font, false gives DEFAULT\_FONT.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in font → font differs from “Default”.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L18) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L411)

<a id="op-1815d84ab3cfc7"></a>
### Font cache path

`operation_foundation_binding_foundation_utils_typst_emitter_font_cache_path`

**Inputs** family.

**Declared result** (str bitwise or no value).

**Explicit results** no value · path when (os.path.isdir(path) and os.listdir(path)), otherwise no value.

**Local steps**

- Bind dependencies os.
- Set safe\_family from re.sub(“&#91;^A-Za-z0-9 \_-&#93;”, empty text, family).replace(one space, “\_”).
- If not safe\_family.
  - Return no value.
- Set path from os.path.join(Platform.get\_site\_path(“private”, “files”, “typst\_fonts”), safe\_family).
- Return path when (os.path.isdir(path) and os.listdir(path)), otherwise no value.
  - Value choice on (os.path.isdir(path) and os.listdir(path)) — true gives path, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isdir(path) → os.listdir(path).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L17) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L410)

<a id="op-41d9f7fb4576cd"></a>
### Ensure typst fonts

`operation_foundation_utils_typst_emitter_business_behavior_ensure_typst_fonts`

**Inputs** family.

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Set family from font\_family(family).
- Set safe\_family from re.sub(“&#91;^A-Za-z0-9 \_-&#93;”, empty text, family).replace(one space, “\_”).
- If not safe\_family.
  - Return no value.
- Bind dependencies time.
- Set root from Platform.get\_site\_path(“private”, “files”, “typst\_fonts”).
- Set target from os.path.join(root, safe\_family).
- If (os.path.isdir(target) and os.listdir(target)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isdir(target) → os.listdir(target).
  - Return no value.
- Set sentinel from os.path.join(root, formatted text .{safe\_family}.unavailable).
- If (os.path.exists(sentinel) and (time.time() − os.path.getmtime(sentinel)) &lt; 86400).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.exists(sentinel) → (time.time() − os.path.getmtime(sentinel)) &lt; 86400.
  - Return no value.
- Bind local operation mark\_unavailable for subsequent calls.
- Attempt the following.
  - Bind dependencies requests.
  - Set urls from list().
  - For each weight in tuple(400, 500, 600, 700).
    - Set css from requests.get(text in the contract, params = mapping(“family” → formatted text {family}:wght@{weight}), headers = mapping(“User-Agent” → “Mozilla/4.0”), timeout = 5).text.
    - Set found from re.findall(text in the contract, css).
    - If found.
      - Evaluate urls.append(tuple(weight, found at 0)).
  - If not urls.
    - Evaluate mark\_unavailable().
    - Return no value.
  - Set scratch from formatted text {target}.partial-{os.getpid()}.
  - Evaluate os.makedirs(scratch, exist\_ok = true).
  - Attempt the following.
    - For each tuple(weight, url) in urls.
      - Set ttf from requests.get(url, timeout = 10).content.
      - Within open(os.path.join(scratch, formatted text {safe\_family}-{weight}.ttf), “wb”) bound as f.
        - Evaluate f.write(ttf).
    - If not os.path.isdir(target).
      - Evaluate os.rename(scratch, target).
  - On exit, including pending return or failure.
    - If os.path.isdir(scratch).
      - Bind dependencies shutil.
      - Evaluate shutil.rmtree(scratch, ignore\_errors = true).
- On failure (Exception).
  - Evaluate mark\_unavailable().
  - Evaluate Platform.log\_error(title = formatted text Typst font fetch failed: {family}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.get(text in the contract, params = mapping(“family” → formatted text {family}:wght@{weight}), headers = mapping(“User-Agent” → “Mozilla/4.0”), timeout = 5), requests.get(url, timeout = 10).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L91) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L34) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L984)

<a id="op-d18c930565721b"></a>
### Ensure typst fonts.mark unavailable

`operation_foundation_utils_typst_emitter_business_behavior_ensure_typst_fonts_mark_unavailable`

**Inputs** no declared parameters.

**Local steps**

- Evaluate os.makedirs(root, exist\_ok = true).
- Within open(sentinel, “w”).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L3458) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L35) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L985)

<a id="op-18fc466593ec86"></a>
### Q

`operation_foundation_utils_typst_emitter_business_behavior_q`

**Inputs** value.

**Declared result** str.

**Explicit results** json.dumps(text, ensure\_ascii = false).

**Local steps**

- Set text from \_CONTROL\_CHARS.sub(empty text, str(value when value is distinct from no value, otherwise empty text)).
  - Value choice on value is distinct from no value — true gives value, false gives empty text.
- Return json.dumps(text, ensure\_ascii = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L3550) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L43) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L993)

<a id="op-e93e996f886892"></a>
### Typst escape

`operation_foundation_utils_typst_emitter_business_behavior_typst_escape`

**Inputs** value.

**Explicit results** str(value) · \_TYPST\_DOT\_MARKUP.sub(“\\1\\2\\\\.”, \_TYPST\_SPECIALS.sub(“\\\\\\1”, text)).

**Local steps**

- If isinstance(value, TypstRaw).
  - Return str(value).
- Set text from \_CONTROL\_CHARS.sub(empty text, str(value when value is distinct from no value, otherwise empty text)).
  - Value choice on value is distinct from no value — true gives value, false gives empty text.
- Return \_TYPST\_DOT\_MARKUP.sub(“\\1\\2\\\\.”, \_TYPST\_SPECIALS.sub(“\\\\\\1”, text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L8) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L79) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1029)

<a id="op-c232f32f43f443"></a>
### Render typst template

`operation_foundation_utils_typst_emitter_business_behavior_render_typst_template`

**Inputs** markup, context.

**Declared result** str.

**Explicit results** env.from\_string(markup).render(context).

**Local steps**

- Bind dependencies get\_jenv, safe\_render\_flags.
- Set env from get\_jenv().overlay(finalize = typst\_escape, autoescape = false).
- Set env.filters from env.filters.copy().
- Set env.filters at “typst\_raw” from TypstRaw.
- Within safe\_render\_flags().
  - Return env.from\_string(markup).render(context).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L95) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L44) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L994)

<a id="op-64055e2ef2c086"></a>
### Has jinja

`operation_foundation_utils_typst_emitter_business_behavior_has_document_template`

**Inputs** markup.

**Declared result** bool.

**Explicit results** (“{{” belongs to markup or “{%” belongs to markup).

**Local steps**

- Return (“{{” belongs to markup or “{%” belongs to markup).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “{{” belongs to markup → “{%” belongs to markup.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4057) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L37) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L987)

<a id="op-d9ee8ba3dda145"></a>
### Safe color

`operation_foundation_utils_typst_emitter_business_behavior_safe_color`

**Inputs** value, default = no value.

**Explicit results** value.strip() · default.

**Local steps**

- If (isinstance(value, str) and COLOR\_PATTERN.fullmatch(value.strip())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → COLOR\_PATTERN.fullmatch(value.strip()).
  - Return value.strip().
- Return default.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4135) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L45) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L995)

<a id="op-9c614dc65d7a7b"></a>
### Hairline

`operation_foundation_binding_foundation_utils_typst_emitter_hairline`

**Inputs** color = no value.

**Declared result** str.

**Explicit results** formatted text 0.6pt + rgb("{color}") when color, otherwise HAIRLINE.

**Local steps**

- Set color from safe\_color(color).
- Return formatted text 0.6pt + rgb("{color}") when color, otherwise HAIRLINE.
  - Value choice on color — true gives formatted text 0.6pt + rgb("{color}"), false gives HAIRLINE.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L19) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L412)

<a id="op-b3bf065e919673"></a>
### Muted text

`operation_foundation_utils_typst_emitter_business_behavior_muted_text`

**Inputs** text, color = MUTED.

**Declared result** str.

**Explicit results** formatted text #text(size: 0.85em, fill: rgb("{color}"), {q(text)}).

**Local steps**

- Return formatted text #text(size: 0.85em, fill: rgb("{color}"), {q(text)}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4263) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L41) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L991)

<a id="op-b241bf2219115a"></a>
### Aligned

`operation_foundation_utils_typst_emitter_business_behavior_aligned`

**Inputs** body, align.

**Declared result** str.

**Explicit results** formatted text #align({align})&#91;{body}&#93; · body.

**Local steps**

- If (body and align belongs to tuple(“center”, “right”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in body → align belongs to tuple(“center”, “right”).
  - Return formatted text #align({align})&#91;{body}&#93;.
- Return body.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4363) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L30) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L981)

<a id="op-7aac76c100270f"></a>
### Fr widths

`operation_foundation_utils_typst_emitter_business_behavior_fr_widths`

**Inputs** columns.

**Declared result** list at str.

**Explicit results** widths.

**Local steps**

- Set widths from list().
- For each col in columns.
  - Set width from Platform.utils.flt(col.get(“width”)).
  - Evaluate widths.append(formatted text {round(width, 2)}fr when width, otherwise “1fr”).
    - Value choice on width — true gives formatted text {round(width, 2)}fr, false gives “1fr”.
- Return widths.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4502) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L36) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L986)

<a id="op-e0de99b4c3bce3"></a>
### List markers

`operation_foundation_binding_foundation_utils_typst_emitter_list_markers`

**Inputs** value.

**Declared result** str.

**Explicit results** value.

**Local steps**

- Bind local operation mark for subsequent calls.
- Set pattern from re.compile(“&lt;(ol\|ul)&#91;^&gt;&#93;\*&gt;((?:(?!&lt;&#91;ou&#93;l&#91;^&gt;&#93;\*&gt;).)\*?)&lt;/\\1&gt;”, (re.I bitwise or re.S)).
- While true.
  - Set tuple(value, count) from pattern.subn(mark, value).
  - If not count.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L20) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L413)

<a id="op-084961899bfc06"></a>
### List markers.mark

`operation_foundation_binding_foundation_utils_typst_emitter_list_markers_mark`

**Inputs** match.

**Explicit results** (whitespace '\\n' + empty text.join(generator of formatted text &lt;x-li&gt;{i}. {item} for tuple(i, item) drawn from enumerate(items, 1))) · (whitespace '\\n' + re.sub(text in the contract, text in the contract, body, flags = re.I)).

**Local steps**

- Set body from match.group(2).
- If match.group(1).lower() equals “ol”.
  - Set items from re.split(text in the contract, body, flags = re.I) at slice 1 to no value.
  - Return (whitespace '\\n' + empty text.join(generator of formatted text &lt;x-li&gt;{i}. {item} for tuple(i, item) drawn from enumerate(items, 1))).
    - Draw tuple(i, item) from enumerate(items, 1).
- Return (whitespace '\\n' + re.sub(text in the contract, text in the contract, body, flags = re.I)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L21) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L414)

<a id="op-9bc2d1bae24ca7"></a>
### Text value

`operation_foundation_utils_typst_emitter_business_behavior_text_value`

**Inputs** html\_ish.

**Declared result** str.

**Explicit results** value · unescape\_html(value).strip().

**Local steps**

- Set value from str((html\_ish or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in html\_ish → empty text.
- If “&lt;” does not belong to value.
  - Return value.
- Set value from \_list\_markers(value).
- Set value from re.sub(text in the contract, whitespace '\\n', value, flags = re.I).
- Set value from re.sub(“&lt;/(p\|div\|tr\|li\|h&#91;1-6&#93;)&gt;&#91; \\t&#93;\*\\n?”, whitespace '\\n', value, flags = re.I).
- Set value from re.sub(“&lt;/t&#91;dh&#93;&gt;(?=&lt;t&#91;dh&#93;)”, one space, value, flags = re.I).
- Set value from Platform.utils.strip\_html(value).
- Return unescape\_html(value).strip().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L96) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L46) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L996)
