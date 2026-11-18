# Shared value and file services · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Typst emitter

<a id="op-2535ca4ed2a3e4"></a>
### Typst Emitter.initialize

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_initialize`

**Inputs** self, generator.

**Local steps**

- Set self.generator from generator.
- Set self.doc from generator.doc.
- Set self.print\_format from generator.print\_format.
- Set self.layout from generator.layout.
- Set self.assets from mapping().
- Set self.\_embedded from mapping().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L4971) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L63) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1013)

<a id="op-ca4ce5cb3e27e0"></a>
### Typst Emitter.prepare

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_prepare`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If hasattr(self, “header\_src”).
  - Return no value.
- Set lh from getattr(self.generator, “letterhead”, no value).
- Set header\_zone from self.layout.get(“header”).
- Set self.header\_src from self.\_section(header\_zone, zone = true) when isinstance(header\_zone, dict), otherwise empty text.
  - Value choice on isinstance(header\_zone, dict) — true gives self.\_section(header\_zone, zone = true), false gives empty text.
- Set lh\_header from self.\_letterhead\_image(lh, “header”).
- If lh\_header.
  - Set self.header\_src from whitespace '\\n'.join(generator of p for p drawn from tuple(lh\_header, self.header\_src) where p).
    - Draw p from tuple(lh\_header, self.header\_src), keep a combination only if (p).
- Set parts from list().
- For each s in (self.layout.get(“sections”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.layout.get(“sections”) → list().
  - Set body from self.\_section(s).
  - Update parts using + list(body, self.\_page\_break(s, body)).
- Set self.body\_src from whitespace '\\n'.join(generator of part for part drawn from parts where part).
  - Draw part from parts, keep a combination only if (part).
- Set footer\_zone from self.layout.get(“footer”).
- Set self.footer\_src from self.\_section(footer\_zone, zone = true) when isinstance(footer\_zone, dict), otherwise empty text.
  - Value choice on isinstance(footer\_zone, dict) — true gives self.\_section(footer\_zone, zone = true), false gives empty text.
- Set lh\_footer from self.\_letterhead\_image(lh, “footer”).
- If lh\_footer.
  - Set self.footer\_src from whitespace '\\n'.join(generator of p for p drawn from tuple(self.footer\_src, lh\_footer) where p).
    - Draw p from tuple(self.footer\_src, lh\_footer), keep a combination only if (p).

If control reaches the end, it returns no value.

**Methods declared on this owner** [section](operations-052.md#op-51de6e15145fa2), [letterhead image](operations-052.md#op-9f074a28329317), [page break](operations-052.md#op-70ec2dabb71be5).

**Values supplied outside this operation** selected callable from getattr(self.generator, “letterhead”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L108) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L69) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1019)

<a id="op-9f074a28329317"></a>
### Typst Emitter.letterhead image

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_letterhead_image`

**Inputs** self, lh, side.

**Declared result** str.

**Explicit results** empty text · \_aligned(body, (lh.get(formatted text {prefix}align) or “Left”).lower()).

**Local steps**

- If not lh.
  - Return empty text.
- Set prefix from empty text when side equals “header”, otherwise “footer\_”.
  - Value choice on side equals “header” — true gives empty text, false gives “footer\_”.
- If lh.get(formatted text {prefix}source) differs from “Image”.
  - Return empty text.
- Set src from lh.get(formatted text {prefix}image).
- If not src.
  - Return empty text.
- Set name from self.\_embed\_image(src).
- If name is identical to no value.
  - Return empty text.
- Set args from list(formatted text "{name}").
- Set width from Platform.utils.flt(lh.get(formatted text {prefix}image\_width)).
- Set height from Platform.utils.flt(lh.get(formatted text {prefix}image\_height)).
- If width.
  - Evaluate args.append(formatted text width: {pt(width)}pt).
- Otherwise.
  - If height.
    - Evaluate args.append(formatted text height: {pt(height)}pt).
- Set body from formatted text #image({“, ”.join(args)}).
- Return \_aligned(body, (lh.get(formatted text {prefix}align) or “Left”).lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lh.get(formatted text {prefix}align) → “Left”.

**Methods declared on this owner** [embed image](operations-053.md#op-427a3d6ca5201b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L5796) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L65) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1015)

<a id="op-88be04425004ec"></a>
### Typst Emitter.page size mm

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_page_size_two_digit_month`

**Inputs** self.

**Declared result** tuple at tuple(float, float).

**Record and data access** resolve a document from “Print Settings” via get\_cached\_doc.

**Explicit results** page\_size\_mm((getattr(self.generator, “print\_settings”, no value) or Platform.get\_cached\_doc(“Print Settings”))).

**Local steps**

- Bind dependencies page\_size\_mm.
- Return page\_size\_mm((getattr(self.generator, “print\_settings”, no value) or Platform.get\_cached\_doc(“Print Settings”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self.generator, “print\_settings”, no value) → Platform.get\_cached\_doc(“Print Settings”).

**Values supplied outside this operation** selected callable from getattr(self.generator, “print\_settings”, no value) · configured or stored value from Platform.get\_cached\_doc(“Print Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L107) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L68) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1018)

<a id="op-ee4b5ddf767a62"></a>
### Typst Emitter.margin mm

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_margin_mm`

**Inputs** self, side.

**Declared result** float.

**Explicit results** 15 when margin is identical to no value, otherwise Platform.utils.flt(margin).

**Local steps**

- Set margin from self.print\_format.get(formatted text margin\_{side}).
- Return 15 when margin is identical to no value, otherwise Platform.utils.flt(margin).
  - Value choice on margin is identical to no value — true gives 15, false gives Platform.utils.flt(margin).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L25) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L418)

<a id="op-67f5ee6cddacb2"></a>
### Typst Emitter.measure source

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_measure_source`

**Inputs** self.

**Declared result** str.

**Explicit results** whitespace '\\n'.join(lines).

**Local steps**

- Evaluate self.prepare().
- Set tuple(page\_width, page\_height) from self.\_page\_size\_mm().
- Set inner from round(((page\_width − self.\_margin\_mm(“left”)) − self.\_margin\_mm(“right”)), 2).
- Set lines from list(formatted text #set page(width: {page\_width}mm, height: {page\_height}mm), self.\_text\_setup(), empty text).
- For each tuple(label, src) in tuple(tuple(“pfhdr”, self.header\_src), tuple(“pfftr”, self.footer\_src)).
  - If src.
    - Evaluate lines.append(formatted text #context &#91;#metadata(measure(box(width: {inner}mm)&#91;{src}&#93;).height.pt()) &lt;{label}&gt;&#93;).
- Return whitespace '\\n'.join(lines).

**Methods declared on this owner** [prepare](operations-052.md#op-ca4ce5cb3e27e0), [page size mm](operations-052.md#op-88be04425004ec), [margin mm](operations-052.md#op-ee4b5ddf767a62), [text setup](operations-052.md#op-d1d326915c3078).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L105) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L66) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1016)

<a id="op-c6bce96c21cb1b"></a>
### Typst Emitter.emit

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_emit`

**Inputs** self, repeat\_header\_footer = false, header\_height\_pt = 0, footer\_height\_pt = 0.

**Explicit results** tuple(whitespace '\\n'.join(generator of line for line drawn from lines where line), self.assets).

**Local steps**

- Evaluate self.prepare().
- Set in\_page\_header from bool((repeat\_header\_footer and self.header\_src)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repeat\_header\_footer → self.header\_src.
- Set in\_page\_footer from bool((repeat\_header\_footer and self.footer\_src)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repeat\_header\_footer → self.footer\_src.
- Set lines from list(self.\_page\_setup(header\_zone = self.header\_src when in\_page\_header, otherwise no value, footer\_zone = self.footer\_src when in\_page\_footer, otherwise no value, header\_height\_pt = header\_height\_pt, foot ….
  - Value choice on in\_page\_header — true gives self.header\_src, false gives no value.
  - Value choice on in\_page\_footer — true gives self.footer\_src, false gives no value.
- If (self.header\_src and not in\_page\_header).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.header\_src → not in\_page\_header.
  - Evaluate lines.append(self.header\_src).
- Evaluate lines.append(self.body\_src).
- If (self.footer\_src and not in\_page\_footer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.footer\_src → not in\_page\_footer.
  - Evaluate lines.append(self.footer\_src).
- Return tuple(whitespace '\\n'.join(generator of line for line drawn from lines where line), self.assets).
  - Draw line from lines, keep a combination only if (line).

**Methods declared on this owner** [prepare](operations-052.md#op-ca4ce5cb3e27e0), [page setup](operations-052.md#op-65d07f326652fb), [text setup](operations-052.md#op-d1d326915c3078).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0516.json#L7305) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L58) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1008)

<a id="op-65d07f326652fb"></a>
### Typst Emitter.page setup

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_page_setup`

**Inputs** self, header\_zone = no value, footer\_zone = no value, header\_height\_pt = 0, footer\_height\_pt = 0.

**Declared result** str.

**State and service calls** call insert on slots at “footer”.

**Explicit results** ((“#set page(” + “, ”.join(args)) + “)”).

**Local steps**

- Set pf from self.print\_format.
- Set top from self.\_margin\_mm(“top”).
- Set bottom from self.\_margin\_mm(“bottom”).
- Set top\_expr from formatted text {top}mm + {round((header\_height\_pt + 12), 2)}pt when header\_zone, otherwise formatted text {top}mm.
  - Value choice on header\_zone — true gives formatted text {top}mm + {round((header\_height\_pt + 12), 2)}pt, false gives formatted text {top}mm.
- Set bottom\_expr from formatted text {bottom}mm + {round((footer\_height\_pt + 12), 2)}pt when footer\_zone, otherwise formatted text {bottom}mm.
  - Value choice on footer\_zone — true gives formatted text {bottom}mm + {round((footer\_height\_pt + 12), 2)}pt, false gives formatted text {bottom}mm.
- Set margins from formatted text (top: {top\_expr}, bottom: {bottom\_expr}, left: {self.\_margin\_mm(“left”)}mm, right: {self.\_margin\_mm(“right”)}mm).
- Set tuple(page\_width, page\_height) from self.\_page\_size\_mm().
- Set args from list(formatted text width: {page\_width}mm, formatted text height: {page\_height}mm, formatted text margin: {margins}).
- Set background from self.\_page\_background().
- If background.
  - Evaluate args.append(formatted text background: {background}).
- Set slots from mapping(“header” → list(), “footer” → list()).
- Set position from PAGE\_NUMBER\_POSITIONS.get((pf.get(“page\_number”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pf.get(“page\_number”) → empty text.
- If position.
  - Set tuple(slot, align) from position.
  - Evaluate slots at slot.append(formatted text &#91;#context &#91;#set text(size: 7pt, fill: rgb("{MUTED}"))   #set align({align})   #counter(page).display("1")#text({q(((one space + translated “of”) + one).
- If header\_zone.
  - Evaluate slots at “header”.append(formatted text &#91;{header\_zone}&#93;).
- If footer\_zone.
  - Evaluate slots at “footer”.insert(0, formatted text &#91;{footer\_zone}&#93;).
- For each tuple(slot, parts) in slots.items().
  - If not parts.
    - Continue with the next iteration or loop test.
  - Set content from parts at 0 when len(parts) equals 1, otherwise ((“stack(spacing: 6pt, ” + “, ”.join(parts)) + “)”).
    - Value choice on len(parts) equals 1 — true gives parts at 0, false gives ((“stack(spacing: 6pt, ” + “, ”.join(parts)) + “)”).
  - Evaluate args.append(formatted text {slot}: {content}).
  - If slot equals “header”.
    - Evaluate args.append(“header-ascent: 8pt” when header\_zone, otherwise “header-ascent: 30%”).
      - Value choice on header\_zone — true gives “header-ascent: 8pt”, false gives “header-ascent: 30%”.
  - Otherwise.
    - If footer\_zone.
      - Evaluate args.append(“footer-descent: 8pt”).
- Return ((“#set page(” + “, ”.join(args)) + “)”).

**Methods declared on this owner** [margin mm](operations-052.md#op-ee4b5ddf767a62), [page size mm](operations-052.md#op-88be04425004ec), [page background](operations-052.md#op-00ebfe549f1b14).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L106) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L67) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1017)

<a id="op-00ebfe549f1b14"></a>
### Typst Emitter.page background

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_page_background`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text &#91;#image("{name}", width: 100%, height: 100%, fit: "stretch")#place(top + left, rect(width: 100%, height: 100%, fill: rgb(255, 255, 255, {veil})))&#93;.

**Explicit failure paths** validation helper — translated “The Typst renderer cannot embed this background image: {0}”.format(Platform.bold(background at “image” at slice no value to 100)).

**Local steps**

- Set background from self.layout.get(“background”).
- If not background.
  - Return no value.
- Set name from self.\_embed\_image(background at “image”).
- If not name.
  - Call the validation error handler Platform.throw(translated “The Typst renderer cannot embed this background image: {0}”.format(Platform.bold(background at “image” at slice no value to 100)), title = translated “Typst renderer unavailable”).
- Set veil from round(((255 × (100 − background at “opacity”)) ÷ 100)).
- Return formatted text &#91;#image("{name}", width: 100%, height: 100%, fit: "stretch")#place(top + left, rect(width: 100%, height: 100%, fill: rgb(255, 255, 255, {veil})))&#93;.

**Methods declared on this owner** [embed image](operations-053.md#op-427a3d6ca5201b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L27) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L420)

<a id="op-d1d326915c3078"></a>
### Typst Emitter.text setup

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_text_setup`

**Inputs** self.

**Declared result** str.

**Explicit results** ((“#set text(” + “, ”.join(args)) + “)”).

**Local steps**

- Set pf from self.print\_format.
- Set size\_pt from pt(pf.font\_size, 14).
- Set args from list(formatted text size: {size\_pt}pt).
- Evaluate args.append(formatted text font: ({q(font\_family(pf.get(“font”)))}, "Libertinus Serif")).
- Set lang from (Platform.local.lang or “en”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.
- Set lang from (get\_parent\_language(lang) or lang).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_parent\_language(lang) → lang.
- If re.fullmatch(“&#91;a-zA-Z&#93;{2,3}”, lang).
  - Evaluate args.append(formatted text lang: {q(lang)}).
- Evaluate args.append(formatted text dir: {“rtl” when is\_rtl(), otherwise “ltr”}).
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
- Set value\_color from safe\_color(pf.get(“value\_color”)).
- If value\_color.
  - Evaluate args.append(formatted text fill: rgb("{value\_color}")).
- Return ((“#set text(” + “, ”.join(args)) + “)”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L7) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L77) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1027)

<a id="op-51de6e15145fa2"></a>
### Typst Emitter.section

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_section`

**Inputs** self, section, zone = false.

**Declared result** str.

**Explicit results** empty text · (out + formatted text  #v({(bottom + 6)}pt)).

**Local steps**

- If section.get(“\_hidden”).
  - Return empty text.
- Set columns from list of c for c drawn from (section.get(“columns”) or list()) where isinstance(c, dict).
  - Draw c from (section.get(“columns”) or list()), keep a combination only if (isinstance(c, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“columns”) → list().
- If not columns.
  - Return empty text.
- Set shrink from section.get(“justify”) belongs to SHRINK\_JUSTIFY.
- Set rendered from list of self.\_column(section, c, shrink = shrink) for c drawn from columns.
  - Draw c from columns.
- Set rendered\_columns from list of body for tuple(body, \_printed) drawn from rendered.
  - Draw tuple(body, \_printed) from rendered.
- If not any(rendered\_columns).
  - Return empty text.
- If (section.get(“label”) and not zone and not any(generator of printed for tuple(\_body, printed) drawn from rendered)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“label”) → not zone → not any(generator of printed for tuple(\_body, printed) drawn from rendered).
  - Draw tuple(\_body, printed) from rendered.
  - Return empty text.
- Set grid from self.\_columns\_grid(section, columns, rendered\_columns).
- Set body from grid.
- If (section.get(“label”) and section.get(“show\_label”) differs from “hide” and not zone).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“label”) → section.get(“show\_label”) differs from “hide” → not zone.
  - Set label from formatted text #text(size: 1.1em, weight: 700, {q(translated section at “label”)}).
  - If section.get(“field\_borders”).
    - Set pad from formatted text {pt(section.get(“cell\_padding”), 8)}pt.
    - Set color from (safe\_color(section.get(“border\_color”)) or “#e2e2e2”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in safe\_color(section.get(“border\_color”)) → “#e2e2e2”.
    - Set ruled from formatted text stroke: (bottom: 0.75pt + rgb("{color}")), inset: (bottom: {pad}), outset: (x: {pad}).
    - Set spacing from pad.
  - Otherwise.
    - Set ruled from “stroke: (bottom: 1.125pt + rgb("#e2e2e2")), inset: (bottom: 0.35em)”.
    - Set spacing from “0.75em”.
  - Set heading from formatted text #block(width: 100%, sticky: true, below: {spacing}, {ruled})&#91;{label}&#93;.
  - Set body from formatted text {heading} {body}.
- Set block\_args from self.\_section\_block\_args(section).
- If section.get(“keep\_together”).
  - Set args from “, ”.join(block\_args).
  - Set out from formatted text #layout(size =&gt; { let body = &#91;{body}&#93; let h = measure(block({args}, breakable: false, body), width: size.width).height block({args}, breakable: h &gt; si.
- Otherwise.
  - Set out from formatted text #block({“, ”.join(block\_args)})&#91; {body} &#93;.
- Set out from self.\_apply\_style\_effects(out, section.get(“custom\_style”)).
- Set margin from (section.get(“margin”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“margin”) → mapping().
- Set top from pt(margin.get(“top”)).
- Set bottom from pt(margin.get(“bottom”)).
- If translate\_custom\_style((nested operand in the contract(nested operand in the contract) or empty text)) at 0.get(“space\_before”) is distinct from no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“custom\_style”) → empty text.
  - Set top from 0.
- If top.
  - Set out from formatted text #v({top}pt) {out}.
- Return (out + formatted text  #v({(bottom + 6)}pt)).

**Methods declared on this owner** [column](operations-052.md#op-ac9bd115c46228), [columns grid](operations-052.md#op-e9722a25abe567), [section block args](operations-052.md#op-e832c0ee02004a), [apply style effects](operations-052.md#op-402c4bf135a42b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L2) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L72) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1022)

<a id="op-70ec2dabb71be5"></a>
### Typst Emitter.page break

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_page_break`

**Inputs** self, section, body.

**Declared result** str.

**Explicit results** “#pagebreak(weak: true)” · empty text.

**Local steps**

- If (section.get(“page\_break”) and not section.get(“\_hidden”) and (body or not section.get(“label”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“page\_break”) → not section.get(“\_hidden”) → (body or not section.get(“label”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in body → not section.get(“label”).
  - Return “#pagebreak(weak: true)”.
- Return empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L28) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L421)

<a id="op-e832c0ee02004a"></a>
### Typst Emitter.section block args

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_section_block_arguments`

**Inputs** self, section.

**Declared result** list at str.

**Explicit results** args.

**Local steps**

- Set args from list(“width: 100%”).
- If section.get(“field\_borders”).
  - Evaluate args.append(formatted text stroke: {hairline(section.get(“border\_color”))}).
  - Evaluate args.append(“radius: 4pt”).
  - Set pad from (Platform.utils.flt(section.get(“cell\_padding”), 0) or 8).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.flt(section.get(“cell\_padding”), 0) → 8.
  - Evaluate args.append(formatted text inset: {pt(pad)}pt).
  - Evaluate args.append(“clip: true”).
- Set background from safe\_color(section.get(“background”)).
- If background.
  - Evaluate args.append(formatted text fill: rgb("{background}")).
- Set padding from (section.get(“padding”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“padding”) → mapping().
- If (padding and not section.get(“field\_borders”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in padding → not section.get(“field\_borders”).
  - Evaluate args.append(“inset: (top: {top}pt, bottom: {bottom}pt, left: {left}pt, right: {right}pt)”.format(expanded names mapping of k → pt(padding.get(k)) for k drawn from tuple(“top”, “bottom”, “left”, “right”))).
    - Draw k from tuple(“top”, “bottom”, “left”, “right”).
- If (section.get(“radius”) is distinct from no value and not section.get(“field\_borders”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“radius”) is distinct from no value → not section.get(“field\_borders”).
  - Evaluate args.append(formatted text radius: {pt(section at “radius”)}pt).
- Return args.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L3) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L73) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1023)

<a id="op-e9722a25abe567"></a>
### Typst Emitter.columns grid

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_columns_grid`

**Inputs** self, section, columns, rendered\_columns.

**Declared result** str.

**Explicit results** cells at 0 at slice 1 to negative 1 · ((formatted text #pad(y: -{pad}pt, grid(columns: ({“, ”.join(widths)}), column-gutter: {gutter}pt, inset: (y: {pad}pt), align: top,  + “,\\n”.join(divided)) + “))”) · ((formatted text #grid(columns: ({“, ”.join(widths)}), column-gutter: {gap\_pt}pt, align: top,  + “,\\n”.join(cells)) + “)”).

**Local steps**

- Set gap from section.get(“gap”).
- Set style\_gap from translate\_custom\_style((nested operand in the contract.get(“custom\_style”) or empty text)) at 0.get(“gap”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“custom\_style”) → empty text.
- If style\_gap is distinct from no value.
  - Set gap\_pt from style\_gap.
- Otherwise.
  - Set gap\_pt from pt(gap when gap is distinct from no value, otherwise 20).
    - Value choice on gap is distinct from no value — true gives gap, false gives 20.
- Set widths from \_fr\_widths(columns).
- Set justify from section.get(“justify”).
- Set cells from list of formatted text &#91;{(body or empty text)}&#93; for body drawn from rendered\_columns.
  - Draw body from rendered\_columns.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in body → empty text.
- If justify belongs to tuple(“space-between”, “space-evenly”, “center”, “right-end”).
  - Set widths from (list(“auto”) × len(columns)).
  - If (justify equals “space-between” and len(columns) &gt; 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in justify equals “space-between” → len(columns) &gt; 1.
    - Set spaced from list().
    - For each tuple(i, cell) in enumerate(cells).
      - If i.
        - Evaluate spaced.append(“&#91;&#93;”).
      - Evaluate spaced.append(cell).
    - Set widths from ((list(“auto”, “1fr”) × (len(columns) − 1)) + list(“auto”)).
    - Set cells from spaced.
  - Otherwise.
    - If justify equals “right-end”.
      - Set widths from list(“1fr”, expanded (list(“auto”) × len(columns))).
      - Set cells from list(“&#91;&#93;”, expanded cells).
    - Otherwise.
      - If justify equals “center”.
        - Set widths from list(“1fr”, expanded (list(“auto”) × len(columns)), “1fr”).
        - Set cells from list(“&#91;&#93;”, expanded cells, “&#91;&#93;”).
      - Otherwise.
        - If justify equals “space-evenly”.
          - Set tuple(spaced, w) from tuple(list(), list()).
          - For each cell in cells.
            - Update spaced using + list(“&#91;&#93;”, cell).
            - Update w using + list(“1fr”, “auto”).
          - Evaluate spaced.append(“&#91;&#93;”).
          - Evaluate w.append(“1fr”).
          - Set tuple(cells, widths) from tuple(spaced, w).
- If len(cells) equals 1.
  - Return cells at 0 at slice 1 to negative 1.
- If section.get(“field\_borders”).
  - Set pad from pt(section.get(“cell\_padding”), 8).
  - Set gutter from pad.
  - Set rule from “none” when section.get(“grid\_borders”) equals “rows”, otherwise hairline(section.get(“border\_color”)).
    - Value choice on section.get(“grid\_borders”) equals “rows” — true gives “none”, false gives hairline(section.get(“border\_color”)).
  - Set divided from list(cells at 0).
  - For each cell in cells at slice 1 to no value.
    - Evaluate divided.append((formatted text grid.cell(stroke: (left: {rule}), inset: (left: {pad}pt)) + cell)).
  - Return ((formatted text #pad(y: -{pad}pt, grid(columns: ({“, ”.join(widths)}), column-gutter: {gutter}pt, inset: (y: {pad}pt), align: top,  + “,\\n”.join(divided)) + “))”).
- Return ((formatted text #grid(columns: ({“, ”.join(widths)}), column-gutter: {gap\_pt}pt, align: top,  + “,\\n”.join(cells)) + “)”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L99) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L54) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1004)

<a id="op-ac9bd115c46228"></a>
### Typst Emitter.column

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_column`

**Inputs** self, section, column, shrink = false.

**Declared result** str.

**Explicit results** tuple(empty text, false) · tuple(self.\_shrink\_to\_content(rendered, body) when shrink, otherwise body, printed).

**Local steps**

- Set rendered from list of tuple(df, self.\_field(section, df)) for df drawn from (column.get(“fields”) or list()).
  - Draw df from (column.get(“fields”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column.get(“fields”) → list().
- Set rendered from list of tuple(df, body) for tuple(df, body) drawn from rendered where body.
  - Draw tuple(df, body) from rendered, keep a combination only if (body).
- Set parts from list of body for tuple(\_, body) drawn from rendered.
  - Draw tuple(\_, body) from rendered.
- If not parts.
  - Return tuple(empty text, false).
- Set printed from any(generator of not self.\_is\_placeholder(df) for tuple(df, \_) drawn from rendered).
  - Draw tuple(df, \_) from rendered.
- If (section.get(“field\_borders”) and section.get(“grid\_borders”) differs from “columns” and len(parts) &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in section.get(“field\_borders”) → section.get(“grid\_borders”) differs from “columns” → len(parts) &gt; 1.
  - Set pad from pt(section.get(“cell\_padding”), 8).
  - Set ruled from (list of formatted text #block(width: 100%, stroke: (bottom: {hairline(section.get(“border\_color”))}), inset: (bottom: {pad}pt), outset: (x: {pad}pt))&#91;{p}&#93; for p drawn from parts at slice no value to negat ….
    - Draw p from parts at slice no value to negative 1.
  - Set body from ((formatted text #stack(spacing: {pad}pt,  + “,\\n”.join(generator of formatted text &#91;{p}&#93; for p drawn from ruled)) + “)”).
    - Draw p from ruled.
- Otherwise.
  - If len(parts) equals 1.
    - Set body from parts at 0.
  - Otherwise.
    - Set body from ((“#stack(spacing: 8pt,\\n” + “,\\n”.join(generator of formatted text &#91;{p}&#93; for p drawn from parts)) + “)”).
      - Draw p from parts.
- Return tuple(self.\_shrink\_to\_content(rendered, body) when shrink, otherwise body, printed).
  - Value choice on shrink — true gives self.\_shrink\_to\_content(rendered, body), false gives body.

**Methods declared on this owner** [field](operations-052.md#op-4ece71001a3cc9), [is placeholder](operations-052.md#op-672f8abd4c9566), [shrink to content](operations-052.md#op-1ce055e7bf168f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L98) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L53) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1003)

<a id="op-672f8abd4c9566"></a>
### Typst Emitter.is placeholder

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_is_placeholder`

**Inputs** self, df.

**Declared result** bool.

**Explicit results** (bool(df.get(“show\_empty”)) and not self.\_formatted\_value(mapping(expand df, “show\_empty” → 0))).

**Local steps**

- Return (bool(df.get(“show\_empty”)) and not self.\_formatted\_value(mapping(expand df, “show\_empty” → 0))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(df.get(“show\_empty”)) → not self.\_formatted\_value(mapping(expand df, “show\_empty” → 0)).

**Methods declared on this owner** [formatted value](operations-052.md#op-c7b95df7bc89d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L24) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L417)

<a id="op-1ce055e7bf168f"></a>
### Typst Emitter.shrink to content

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_shrink_to_content`

**Inputs** rendered, body.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** body · formatted text #layout(size =&gt; { let w = measure(&#91;{ruler}&#93;, width: size.width).width block(width: w)&#91;{body}&#93; }).

**Local steps**

- Set natural from list of b for tuple(df, b) drawn from rendered where df.get(“fieldtype”) does not belong to FULL\_WIDTH\_FIELDTYPES.
  - Draw tuple(df, b) from rendered, keep a combination only if (df.get(“fieldtype”) does not belong to FULL\_WIDTH\_FIELDTYPES).
- If (not natural or len(natural) equals len(rendered)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not natural → len(natural) equals len(rendered).
  - Return body.
- Set ruler from natural at 0 when len(natural) equals 1, otherwise ((“#stack(spacing: 8pt,\\n” + “,\\n”.join(generator of formatted text &#91;{p}&#93; for p drawn from natural)) + “)”).
  - Value choice on len(natural) equals 1 — true gives natural at 0, false gives ((“#stack(spacing: 8pt,\\n” + “,\\n”.join(generator of formatted text &#91;{p}&#93; for p drawn from natural)) + “)”).
  - Draw p from natural.
- Return formatted text #layout(size =&gt; { let w = measure(&#91;{ruler}&#93;, width: size.width).width block(width: w)&#91;{body}&#93; }).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L30) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L423)

<a id="op-4ece71001a3cc9"></a>
### Typst Emitter.field

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_field`

**Inputs** self, section, df.

**Declared result** str.

**Explicit results** empty text · self.\_apply\_style\_effects(body, df.get(“custom\_style”)).

**Local steps**

- If df.get(“\_hidden”).
  - Return empty text.
- Set body from self.\_field\_body(section, df).
- If not body.
  - Return empty text.
- Return self.\_apply\_style\_effects(body, df.get(“custom\_style”)).

**Methods declared on this owner** [field body](operations-052.md#op-a2008d67828653), [apply style effects](operations-052.md#op-402c4bf135a42b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0517.json#L5714) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L59) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1009)

<a id="op-402c4bf135a42b"></a>
### Typst Emitter.apply style effects

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_apply_style_effects`

**Inputs** self, body, style.

**Declared result** str.

**Explicit results** body.

**Local steps**

- If (not isinstance(style, str) or not style.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(style, str) → not style.strip().
  - Return body.
- Set tuple(effects, \_unknown) from translate\_custom\_style(style).
- If not effects.
  - Return body.
- If effects.get(“bold”).
  - Set body from formatted text #text(weight: 700)&#91;{body}&#93;.
- Set strokes from list().
- If effects.get(“stroke\_top”).
  - Evaluate strokes.append(formatted text top: {effects at “stroke\_top”}).
- If effects.get(“stroke\_bottom”).
  - Evaluate strokes.append(formatted text bottom: {effects at “stroke\_bottom”}).
- Set insets from list().
- If effects.get(“inset\_top”).
  - Evaluate insets.append(formatted text top: {effects at “inset\_top”}pt).
- If effects.get(“inset\_bottom”).
  - Evaluate insets.append(formatted text bottom: {effects at “inset\_bottom”}pt).
- If (strokes or insets).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in strokes → insets.
  - Set args from list(“width: 100%”).
  - If strokes.
    - Evaluate args.append(formatted text stroke: ({“, ”.join(strokes)})).
  - If insets.
    - Evaluate args.append(formatted text inset: ({“, ”.join(insets)})).
  - Set body from formatted text #block({“, ”.join(args)})&#91;{body}&#93;.
- If effects.get(“space\_before”).
  - Set body from formatted text #v({effects at “space\_before”}pt) {body}.
- Return body.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0517.json#L5895) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L49) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L999)

<a id="op-a2008d67828653"></a>
### Typst Emitter.field body

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_field_body`

**Inputs** self, section, df.

**Declared result** str.

**Explicit results** self.\_typst\_block(df) · “#line(length: 100%, stroke: 0.6pt + rgb("#d1d5db"))” · formatted text #v({pt(height)}pt) · self.\_table(df, keep\_together = (section.get(“keep\_together”) or in\_zone)) · self.\_barcode(df) · 7 additional forms in the steps below.

**Local steps**

- Set fieldtype from (df.get(“fieldtype”) or “Data”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“fieldtype”) → “Data”.
- If fieldtype equals “Typst”.
  - Return self.\_typst\_block(df).
- If fieldtype equals “Divider”.
  - Return “#line(length: 100%, stroke: 0.6pt + rgb("#d1d5db"))”.
- If fieldtype equals “Spacer”.
  - Set height from (Platform.utils.flt(df.get(“height”)) or 13).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.flt(df.get(“height”)) → 13.
  - Return formatted text #v({pt(height)}pt).
- If fieldtype equals “Table”.
  - Set in\_zone from (section is identical to self.layout.get(“header”) or section is identical to self.layout.get(“footer”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in section is identical to self.layout.get(“header”) → section is identical to self.layout.get(“footer”).
  - Return self.\_table(df, keep\_together = (section.get(“keep\_together”) or in\_zone)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“keep\_together”) → in\_zone.
- If fieldtype equals “Barcode”.
  - Return self.\_barcode(df).
- If fieldtype equals “Image”.
  - Return self.\_image(df).
- If (fieldtype equals “Attach Image” or df.get(“renderer”) equals “AttachImage”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldtype equals “Attach Image” → df.get(“renderer”) equals “AttachImage”.
  - Return self.\_data\_field(section, df, value\_markup = self.\_image(df)).
- If fieldtype equals “Signature”.
  - Set name from self.\_embed\_image(self.doc.get(df.get(“fieldname”))).
  - Set image from formatted text #scale({PX\_TO\_PT}, reflow: true, image("{name}")) when name, otherwise empty text.
    - Value choice on name — true gives formatted text #scale({PX\_TO\_PT}, reflow: true, image("{name}")), false gives empty text.
  - Return self.\_data\_field(section, df, value\_markup = image).
- If fieldtype equals “Rating”.
  - Return self.\_data\_field(section, df, value\_markup = self.\_rating(df)).
- If fieldtype equals “Repeater”.
  - Return self.\_repeater(df).
- If fieldtype equals “Static Text”.
  - Return self.\_static\_text(df).
- Return self.\_data\_field(section, df).

**Methods declared on this owner** [typst block](operations-052.md#op-1417c1179189da), [table](operations-053.md#op-b4fee85ac437ba), [barcode](operations-053.md#op-cf23d0eca43f58), [image](operations-053.md#op-f5868eed3a48cc), [data field](operations-053.md#op-96622ac65b6bfb), [embed image](operations-053.md#op-427a3d6ca5201b), [rating](operations-053.md#op-a389865e21662b), [repeater](operations-053.md#op-993d1844e0aede), [static text](operations-052.md#op-d7037037342fae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L102) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L60) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1010)

<a id="op-d7037037342fae"></a>
### Typst Emitter.static text

`operation_foundation_binding_foundation_utils_typst_emitter_typstemitter_static_text`

**Inputs** self, df.

**Declared result** str.

**Explicit results** empty text · out.

**Local steps**

- Set text from (df.get(“text”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“text”) → empty text.
- If not text.
  - Return empty text.
- Set out from self.\_text\_props(df, typst\_escape(translated text).replace(whitespace '\\n', “ \\\\n”)).
- If df.get(“align”) belongs to tuple(“center”, “right”).
  - Set out from formatted text #align({df at “align”})&#91;{out}&#93;.
- Return out.

**Methods declared on this owner** [text props](operations-053.md#op-01f06b410a435f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L31) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L424)

<a id="op-1417c1179189da"></a>
### Typst Emitter.typst block

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_typst_block`

**Inputs** self, df.

**Declared result** str.

**Explicit results** markup · render\_typst\_template(markup, mapping(“doc” → self.doc)).strip().

**Explicit failure paths** validation helper — translated “The Typst block could not render its template: {0}”.format(str(e) at slice no value to 300).

**Local steps**

- Set markup from (df.get(“typst”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“typst”) → empty text.
- If (not markup or not has\_jinja(markup)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not markup → not has\_jinja(markup).
  - Return markup.
- Attempt the following.
  - Return render\_typst\_template(markup, mapping(“doc” → self.doc)).strip().
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “The Typst block could not render its template: {0}”.format(str(e) at slice no value to 300), title = translated “Invalid Typst block”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0517.json#L7287) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L78) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1028)

<a id="op-c7b95df7bc89d4"></a>
### Typst Emitter.formatted value

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_formatted_value`

**Inputs** self, df.

**Explicit results** \_text\_value((df.get(“\_value”) or empty text)) · empty text · translated “Yes” when Platform.utils.cint(value), otherwise translated “No” · Platform.utils.cstr(value).rsplit(“/”, 1) at negative 1 · \_text\_value(self.doc.get\_formatted(fieldname)).

**Local steps**

- If (df.get(“fieldtype”) equals “Linked Field” or df.get(“\_value”) is distinct from no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“fieldtype”) equals “Linked Field” → df.get(“\_value”) is distinct from no value.
  - Return \_text\_value((df.get(“\_value”) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“\_value”) → empty text.
- Set fieldname from df.get(“fieldname”).
- If not fieldname.
  - Return empty text.
- Set value from self.doc.get(fieldname).
- If (not value and not df.get(“show\_empty”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not value → not df.get(“show\_empty”).
  - Return empty text.
- If df.get(“fieldtype”) equals “Check”.
  - Return translated “Yes” when Platform.utils.cint(value), otherwise translated “No”.
    - Value choice on Platform.utils.cint(value) — true gives translated “Yes”, false gives translated “No”.
- If df.get(“fieldtype”) equals “Attach”.
  - Return Platform.utils.cstr(value).rsplit(“/”, 1) at negative 1.
- Return \_text\_value(self.doc.get\_formatted(fieldname)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L103) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L61) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1011)

<a id="op-dfb10469774078"></a>
### Typst Emitter.label color

`operation_foundation_utils_typst_emitter_business_behavior_typst_emitter_label_color`

**Inputs** self, df = no value.

**Declared result** str.

**Explicit results** (safe\_color(df.get(“label\_color”)) when df, otherwise no value or safe\_color(self.print\_format.get(“label\_color”)) or MUTED).

**Local steps**

- Return (safe\_color(df.get(“label\_color”)) when df, otherwise no value or safe\_color(self.print\_format.get(“label\_color”)) or MUTED).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in safe\_color(df.get(“label\_color”)) when df, otherwise no value → safe\_color(self.print\_format.get(“label\_color”)) → MUTED.
  - Value choice on df — true gives safe\_color(df.get(“label\_color”)), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0517.json#L7903) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L64) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1014)
