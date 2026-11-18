# Shared value and file services · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Html utils

<a id="op-d5ce9d1a8d5916"></a>
### Clean html

`operation_foundation_utils_hypertext_markup_utils_business_behavior_clean_document_markup`

**Inputs** html.

**Explicit results** html · nh3.clean(html, tags = set(“div”, “p”, “br”, “ul”, …), clean\_content\_tags = REMOVE\_CONTENT\_TAGS, strip\_comments = true).

**Local steps**

- If not isinstance(html, str).
  - Return html.
- Return nh3.clean(html, tags = set(“div”, “p”, “br”, “ul”, …), clean\_content\_tags = REMOVE\_CONTENT\_TAGS, strip\_comments = true).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L4654) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L177)

<a id="op-7e8520e5395791"></a>
### Clean email html

`operation_foundation_utils_hypertext_markup_utils_business_behavior_clean_email_document_markup`

**Inputs** html.

**Explicit results** html · nh3.clean(html, tags = set(“div”, “p”, “br”, “ul”, …), attributes = mapping(“\*” → set(“border”, “colspan”, “rowspan”, “src”, …)), clean\_content\_tags = REMOVE\_CONTENT\_TAGS, filter\_style\_properties = allowed ….

**Local steps**

- If not isinstance(html, str).
  - Return html.
- Set allowed\_css\_properties from set(“color”, “border-color”, “width”, “height”, …).
- Return nh3.clean(html, tags = set(“div”, “p”, “br”, “ul”, …), attributes = mapping(“\*” → set(“border”, “colspan”, “rowspan”, “src”, …)), clean\_content\_tags = REMOVE\_CONTENT\_TAGS, filter\_style\_properties = allowed ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L4847) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L178)

<a id="op-55f7492c2ca2ca"></a>
### Has html tags

`operation_foundation_utils_hypertext_markup_utils_business_behavior_has_document_markup_tags`

**Inputs** html.

**Declared result** bool.

**Explicit results** bool(HTML\_TAG\_PATTERN.search(html)).

**Local steps**

- Return bool(HTML\_TAG\_PATTERN.search(html)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L5364) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L181)

<a id="op-d2a72e94116adf"></a>
### Clean script and style

`operation_foundation_utils_hypertext_markup_utils_business_behavior_clean_script_and_style`

**Inputs** html.

**Explicit results** Platform.as\_unicode(soup).

**Local steps**

- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(html, “html5lib”).
- For each s in soup(list(“script”, “style”)).
  - Evaluate s.decompose().
- Return Platform.as\_unicode(soup).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L5437) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L179)

<a id="op-06b0a24b97a172"></a>
### Sanitize html

`operation_foundation_utils_hypertext_markup_utils_business_behavior_sanitize_document_markup`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** html, linkify, always\_sanitize, disallowed\_tags.

**Explicit result forms** a value selected from the current context.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L123) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L183)

<a id="op-bf1ae398e1668c"></a>
### Is json

`operation_foundation_utils_hypertext_markup_utils_business_behavior_is_structured_data`

**Inputs** text.

**Explicit results** false · true.

**Local steps**

- Attempt the following.
  - Evaluate json.loads(text).
- On failure (ValueError).
  - Return false.
- When the protected block completes normally.
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L6904) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L182)

<a id="op-d42c77e7dd5985"></a>
### Get icon html

`operation_foundation_utils_hypertext_markup_utils_business_behavior_get_icon_document_markup`

**Inputs** icon, small = false.

**Explicit results** formatted text &lt;span class="text-muted"&gt;{icon}&lt;/span&gt; · formatted text &lt;img style='width: 16px; height: 16px;' src={escape\_html(icon)}&gt; when small, otherwise formatted text &lt;img src={escape\_html(icon)}&gt; · formatted text &lt;i class={escape\_html(icon)}&gt;&lt;/i&gt;.

**Local steps**

- Bind dependencies is\_image.
- Set icon from (icon or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in icon → empty text.
- If (icon and EMOJI\_PATTERN.match(icon)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in icon → EMOJI\_PATTERN.match(icon).
  - Return formatted text &lt;span class="text-muted"&gt;{icon}&lt;/span&gt;.
- If is\_image(icon).
  - Return formatted text &lt;img style='width: 16px; height: 16px;' src={escape\_html(icon)}&gt; when small, otherwise formatted text &lt;img src={escape\_html(icon)}&gt;.
    - Value choice on small — true gives formatted text &lt;img style='width: 16px; height: 16px;' src={escape\_html(icon)}&gt;, false gives formatted text &lt;img src={escape\_html(icon)}&gt;.
- Otherwise.
  - Return formatted text &lt;i class={escape\_html(icon)}&gt;&lt;/i&gt;.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L6993) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L180)

<a id="op-660d570a1eff38"></a>
### Unescape html

`operation_foundation_utils_hypertext_markup_utils_business_behavior_unescape_document_markup`

**Inputs** value.

**Explicit results** unescape(value).

**Local steps**

- Bind dependencies unescape.
- Return unescape(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L7280) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L184)

## Service · Identicon

<a id="op-1e0b58b9c3f063"></a>
### Identicon.initialize

`operation_foundation_utils_identicon_business_behavior_identicon_initialize`

**Inputs** self, str\_, background = “#fafbfc”.

**Local steps**

- Set w, h from ((BORDER\_SIZE × 2) + (SQUARE\_SIZE × GRID\_SIZE)).
- Set self.image from Image.new(“RGB”, tuple(w, h), background).
- Set self.draw from ImageDraw.Draw(self.image).
- Set self.hash from self.digest(str\_).

If control reaches the end, it returns no value.

**Methods declared on this owner** [digest](operations-024.md#op-69bd929228282b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L7340) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L189)

<a id="op-69bd929228282b"></a>
### Identicon.digest

`operation_foundation_utils_identicon_business_behavior_identicon_digest`

**Inputs** self, str\_.

**Explicit results** int(md5(str\_.encode(“utf-8”), usedforsecurity = false).hexdigest(), 16).

**Local steps**

- Return int(md5(str\_.encode(“utf-8”), usedforsecurity = false).hexdigest(), 16).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L7553) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L187)

<a id="op-78911c57b30555"></a>
### Identicon.calculate

`operation_foundation_utils_identicon_business_behavior_identicon_calculate`

**Inputs** self.

**Local steps**

- Set color from tuple((self.hash bitwise and 255), ((self.hash shift right 8) bitwise and 255), ((self.hash shift right 16) bitwise and 255)).
- Update self.hash using shift right 24.
- Set square\_x, square\_y from 0.
- For each x in range(((GRID\_SIZE × (GRID\_SIZE + 1)) floor divide 2)).
  - If (self.hash bitwise and 1).
    - Set x from (BORDER\_SIZE + (square\_x × SQUARE\_SIZE)).
    - Set y from (BORDER\_SIZE + (square\_y × SQUARE\_SIZE)).
    - Evaluate self.draw.rectangle(tuple(x, y, (x + SQUARE\_SIZE), (y + SQUARE\_SIZE)), fill = color, outline = color).
    - Set x from (BORDER\_SIZE + (((GRID\_SIZE − 1) − square\_x) × SQUARE\_SIZE)).
    - Evaluate self.draw.rectangle(tuple(x, y, (x + SQUARE\_SIZE), (y + SQUARE\_SIZE)), fill = color, outline = color).
  - Update self.hash using shift right 1.
  - Update square\_y using + 1.
  - If square\_y equals GRID\_SIZE.
    - Set square\_y from 0.
    - Update square\_x using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L186)

<a id="op-bd0934ee6708d5"></a>
### Identicon.generate

`operation_foundation_utils_identicon_business_behavior_identicon_generate`

**Inputs** self.

**State and service calls** call save on self.image.

**Local steps**

- Evaluate self.calculate().
- Within open(“identicon.png”, “wb”) bound as out.
  - Evaluate self.image.save(out, “PNG”).
- Evaluate self.image.show().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate](operations-024.md#op-78911c57b30555).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L556) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L188)

<a id="op-d6e5fbc08bdc0b"></a>
### Identicon.base64

`operation_foundation_utils_identicon_business_behavior_identicon_base_64`

**Inputs** self, format = “PNG”.

**State and service calls** call save on self.image.

**Explicit results** formatted text data:image/png;base64,{b64encode(buff.getvalue()).decode()}.

**Local steps**

- Evaluate self.calculate().
- Set self.image.encoderinfo from mapping().
- Set self.image.encoderconfig from tuple().
- Set buff from BytesIO().
- Evaluate self.image.save(buff, format = format.upper()).
- Return formatted text data:image/png;base64,{b64encode(buff.getvalue()).decode()}.

**Methods declared on this owner** [calculate](operations-024.md#op-78911c57b30555).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L695) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L185)

## Service · Image

<a id="op-6e071aa555b8fe"></a>
### Resize images

`operation_foundation_utils_image_business_behavior_resize_images`

**Inputs** path, maxdim = 700.

**State and service calls** call save on im.

**Local steps**

- Set size from tuple(maxdim, maxdim).
- For each tuple(basepath, folders, files) in os.walk(path).
  - For each fname in files.
    - Set extn from fname.rsplit(“.”, 1) at 1.
    - If extn belongs to tuple(“jpg”, “jpeg”, “png”, “gif”).
      - Set im from Image.open(os.path.join(basepath, fname)).
      - If (im.size at 0 &gt; size at 0 or im.size at 1 &gt; size at 1).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in im.size at 0 &gt; size at 0 → im.size at 1 &gt; size at 1.
        - Evaluate im.thumbnail(size, Image.Resampling.LANCZOS).
        - Evaluate im.save(os.path.join(basepath, fname)).
        - Evaluate print(formatted text resized {os.path.join(basepath, fname)}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L925) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L191)

<a id="op-f958f5976a6a6c"></a>
### Strip exif data

`operation_foundation_utils_image_business_behavior_strip_exchangeable_image_file_data`

**Inputs** content, content\_type.

**Declared result** bytes.

**State and service calls** call save on original\_image.

**Explicit results** content · output.getvalue().

**Local steps**

- Set original\_image from Image.open(io.BytesIO(content)).
- If not original\_image.getexif().
  - Return content.
- Set original\_image from ImageOps.exif\_transpose(original\_image).
- Set output from io.BytesIO().
- If (content\_type equals “image/jpeg” and original\_image.mode belongs to tuple(“RGBA”, “LA”, “P”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in content\_type equals “image/jpeg” → original\_image.mode belongs to tuple(“RGBA”, “LA”, “P”).
  - Set original\_image from Image.alpha\_composite(Image.new(“RGBA”, original\_image.size, “white”), original\_image.convert(“RGBA”)).convert(“RGB”).
- Evaluate original\_image.save(output, format = content\_type.split(“/”) at 1, exif = byte value).
- Return output.getvalue().

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L125) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L192)

<a id="op-0d06603b1df8cd"></a>
### Optimize image

`operation_foundation_utils_image_business_behavior_optimize_image`

**Inputs** content, content\_type, max\_width = 1024, max\_height = 768, optimize = true, quality = 85.

**State and service calls** call save on image · msgprint with Platform.\_(“Failed to optimize image: {0}”).format(str(e)).

**Explicit results** content · optimized\_content when len(optimized\_content) &lt; len(content), otherwise content.

**Local steps**

- If content\_type equals “image/svg+xml”.
  - Return content.
- Attempt the following.
  - Set image from Image.open(io.BytesIO(content)).
  - Set exif from image.getexif().
  - If (content\_type equals “image/jpeg” and image.mode belongs to tuple(“RGBA”, “LA”, “P”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in content\_type equals “image/jpeg” → image.mode belongs to tuple(“RGBA”, “LA”, “P”).
    - Set image from Image.alpha\_composite(Image.new(“RGBA”, image.size, “white”), image.convert(“RGBA”)).convert(“RGB”).
  - Set tuple(width, height) from image.size.
  - Set max\_height from max(min(max\_height, (height × 0.8)), 200).
  - Set max\_width from max(min(max\_width, (width × 0.8)), 200).
  - Set image\_format from content\_type.split(“/”) at 1.
  - Set size from tuple(max\_width, max\_height).
  - Evaluate image.thumbnail(size, Image.Resampling.LANCZOS).
  - Set output from io.BytesIO().
  - Evaluate image.save(output, format = image\_format, optimize = optimize, quality = quality, save\_all = true when image\_format equals “gif”, otherwise no value, …).
    - Value choice on image\_format equals “gif” — true gives true, false gives no value.
  - Set optimized\_content from output.getvalue().
  - Return optimized\_content when len(optimized\_content) &lt; len(content), otherwise content.
    - Value choice on len(optimized\_content) &lt; len(content) — true gives optimized\_content, false gives content.
- On failure (Exception) bound to e.
  - Evaluate Platform.msgprint(Platform.\_(“Failed to optimize image: {0}”).format(str(e))).
  - Return content.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L124) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L190)

## Service · Inplacevar

<a id="op-c7d69849034a5e"></a>
### Iadd

`operation_foundation_utils_inplacevar_business_behavior_iadd`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using + y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2430) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L285)

<a id="op-a5e3355cfebe45"></a>
### Isub

`operation_foundation_utils_inplacevar_business_behavior_isub`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using − y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2486) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L295)

<a id="op-7a308a03e5339f"></a>
### Imul

`operation_foundation_utils_inplacevar_business_behavior_imul`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using × y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2542) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L291)

<a id="op-8bfd12e25102cb"></a>
### Idiv

`operation_foundation_utils_inplacevar_business_behavior_idiv`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using ÷ y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2598) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L287)

<a id="op-41e4b5253e8282"></a>
### Ifloordiv

`operation_foundation_utils_inplacevar_business_behavior_ifloordiv`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using floor divide y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2654) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L288)

<a id="op-13095b1e8efa59"></a>
### Imod

`operation_foundation_utils_inplacevar_business_behavior_imod`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using modulo or format y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2710) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L290)

<a id="op-111c4e927b2f29"></a>
### Ipow

`operation_foundation_utils_inplacevar_business_behavior_ipow`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using to the power y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2766) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L293)

<a id="op-8e7d0a483c36bb"></a>
### Ilshift

`operation_foundation_utils_inplacevar_business_behavior_ilshift`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using shift left y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2822) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L289)
