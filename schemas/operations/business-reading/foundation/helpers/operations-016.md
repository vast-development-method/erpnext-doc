# Shared value and file services · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-6f474f20dfa2a8"></a>
### Round based on smallest currency fraction

`operation_foundation_utils_data_business_behavior_round_based_on_smallest_currency_fraction`

**Inputs** value, currency, precision = 2.

**Record and data access** read “Currency” via get\_value.

**Explicit results** flt(value, precision).

**Local steps**

- Set smallest\_currency\_fraction\_value from flt(Platform.db.get\_value(“Currency”, currency, “smallest\_currency\_fraction\_value”, cache = true)).
- If smallest\_currency\_fraction\_value.
  - Set remainder\_val from remainder(value, smallest\_currency\_fraction\_value, precision).
  - If remainder\_val &gt; (smallest\_currency\_fraction\_value ÷ 2).
    - Update value using + (smallest\_currency\_fraction\_value − remainder\_val).
  - Otherwise.
    - Update value using − remainder\_val.
- Otherwise.
  - Set value from rounded(value).
- Return flt(value, precision).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L3815) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L37)

<a id="op-c03c96fb6dc989"></a>
### Encode

`operation_foundation_utils_data_business_behavior_encode`

**Inputs** obj, encoding = “utf-8”.

**Explicit results** out · obj.encode(encoding) · obj.

**Local steps**

- If isinstance(obj, list).
  - Set out from list().
  - For each o in obj.
    - If isinstance(o, str).
      - Evaluate out.append(o.encode(encoding)).
    - Otherwise.
      - Evaluate out.append(o).
  - Return out.
- Otherwise.
  - If isinstance(obj, str).
    - Return obj.encode(encoding).
  - Otherwise.
    - Return obj.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L4096) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1668)

<a id="op-1cb420d0f7854f"></a>
### Parse val

`operation_foundation_utils_data_business_behavior_parse_val`

**Inputs** v.

**Explicit results** v.

**Local steps**

- If isinstance(v, (datetime.date bitwise or datetime.datetime)).
  - Set v from str(v).
- Otherwise.
  - If isinstance(v, datetime.timedelta).
    - Set v from “:”.join(str(v).split(“:”) at slice no value to 2).
  - Otherwise.
    - If isinstance(v, int).
      - Set v from int(v).
- Return v.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L4343) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L27)

<a id="op-8f6068267732d2"></a>
### Get currency precision

`operation_foundation_binding_foundation_utils_data_get_currency_precision`

**Inputs** no declared parameters.

**Declared result** (int bitwise or no value).

**Explicit results** cint(currency\_precision) when currency\_precision does not belong to tuple(no value, empty text), otherwise no value.

**Local steps**

- Set currency\_precision from Platform.db.get\_default(“currency\_precision”).
- Return cint(currency\_precision) when currency\_precision does not belong to tuple(no value, empty text), otherwise no value.
  - Value choice on currency\_precision does not belong to tuple(no value, empty text) — true gives cint(currency\_precision), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L53) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L211)

<a id="op-3429075c707f66"></a>
### Fmt money

`operation_foundation_utils_data_business_behavior_format_money`

**Inputs** amount, precision = no value, currency = no value, format = no value.

**Declared result** str.

**Record and data access** read “Currency” via get\_value.

**Explicit results** amount.

**Local steps**

- Set number\_format from NumberFormat.from\_string(format) when format, otherwise get\_number\_format().
  - Value choice on format — true gives NumberFormat.from\_string(format), false gives get\_number\_format().
- If precision is identical to no value.
  - Set precision from get\_currency\_precision().
- If precision is identical to no value.
  - Set precision from number\_format.precision.
- If isinstance(amount, str).
  - Set amount from flt(amount, precision).
- If amount is identical to no value.
  - Set amount from 0.
- If number\_format.decimal\_separator.
  - Set decimals\_after from str(round((amount modulo or format 1), precision)).
  - Set parts from decimals\_after.split(“.”).
  - Set parts from parts at 1 when len(parts) &gt; 1, otherwise parts at 0.
    - Value choice on len(parts) &gt; 1 — true gives parts at 1, false gives parts at 0.
  - Set decimals from parts.
  - If precision &gt; 2.
    - If len(decimals) &lt; 3.
      - If currency.
        - Set fraction from (Platform.db.get\_value(“Currency”, currency, “fraction\_units”, cache = true) or 100).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Currency”, currency, “fraction\_units”, cache = true) → 100.
        - Set precision from (len(cstr(fraction)) − 1).
      - Otherwise.
        - Set precision from number\_format.precision.
    - Otherwise.
      - If len(decimals) &lt; precision.
        - Set precision from len(decimals).
- Set amount from (“%.\*f” modulo or format tuple(precision, round(flt(amount), precision))).
- If amount.find(“.”) equals negative 1.
  - Set decimals from empty text.
- Otherwise.
  - Set decimals from amount.split(“.”) at 1.
- Set parts from list().
- Set minus from empty text.
- If flt(amount) &lt; 0.
  - Set minus from “-”.
- Set amount from cstr(abs(flt(amount))).split(“.”, 1) at 0.
- If len(amount) &gt; 3.
  - Evaluate parts.append(amount at slice negative 3 to no value).
  - Set amount from amount at slice no value to negative 3.
  - Set val from 2 when number\_format.string equals “#,##,###.##”, otherwise 3.
    - Value choice on number\_format.string equals “#,##,###.##” — true gives 2, false gives 3.
  - While len(amount) &gt; val.
    - Evaluate parts.append(amount at slice negative val to no value).
    - Set amount from amount at slice no value to negative val.
- Evaluate parts.append(amount).
- Evaluate parts.reverse().
- Set amount from (number\_format.thousands\_separator.join(parts) + (((precision and number\_format.decimal\_separator) and (number\_format.decimal\_separator + decimals)) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ((precision and number\_format.decimal\_separator) and (number\_format.decimal\_separator + decimals)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (precision and number\_format.decimal\_separator) → (number\_format.decimal\_separator + decimals).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in precision → number\_format.decimal\_separator.
- If amount differs from “0”.
  - Set amount from (minus + amount).
- If (currency and Platform.defaults.get\_global\_default(“hide\_currency\_symbol”) does not belong to tuple(“1”, “Yes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in currency → Platform.defaults.get\_global\_default(“hide\_currency\_symbol”) does not belong to tuple(“1”, “Yes”).
  - Set symbol from (Platform.db.get\_value(“Currency”, currency, “symbol”, cache = true) or currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Currency”, currency, “symbol”, cache = true) → currency.
  - Set symbol\_on\_right from Platform.db.get\_value(“Currency”, currency, “symbol\_on\_right”, cache = true).
  - If symbol\_on\_right.
    - Set amount from formatted text {amount} {Platform.\_(symbol)}.
  - Otherwise.
    - Set amount from formatted text {Platform.\_(symbol)} {amount}.
- Return amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L88) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1683)

<a id="op-efdd2ae75a090e"></a>
### Getattr

`operation_foundation_utils_data_business_behavior_getattr`

**Inputs** name.

**Explicit failure paths** AttributeError(formatted text module {\_\_name\_\_} has no attribute {name}).

**Local steps**

- If name equals “number\_format\_info”.
  - Bind dependencies deprecation\_warning.
  - Bind dependencies NUMBER\_FORMAT\_MAP.
  - Evaluate record a compatibility advisory for the invoked interface.
- Otherwise.
  - Attempt the following.
    - Evaluate globals() at name.
  - On failure (KeyError).
    - Raise AttributeError(formatted text module {\_\_name\_\_} has no attribute {name}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L6474) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1194) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1752)

<a id="op-c5bf267f799f4d"></a>
### Money in words

`operation_foundation_utils_data_business_behavior_money_in_words`

**Inputs** number, main\_currency = no value, fraction\_currency = no value.

**Record and data access** read “Currency” via get\_value.

**Explicit results** empty text · \_(“{0}.”, context = “Money in words”).format(out) · \_(“{0} only.”, context = “Money in words”).format(out).

**Local steps**

- Bind dependencies get\_defaults.
- Set \_ from Platform.\_.
- Attempt the following.
  - Set number from float(number).
- On failure (ValueError).
  - Return empty text.
- Set number from flt(number).
- If number &lt; 0.
  - Return empty text.
- Set d from get\_defaults().
- If not main\_currency.
  - Set main\_currency from d.get(“currency”, “INR”).
- If not fraction\_currency.
  - Set fraction\_currency from Platform.db.get\_value(“Currency”, main\_currency, “fraction”, cache = true).
- Set number\_format from get\_number\_format().
- Set fraction\_units from Platform.db.get\_value(“Currency”, main\_currency, “fraction\_units”, cache = true).
- If fraction\_units.
  - Set fraction\_length from math.ceil(math.log10(fraction\_units)).
- Otherwise.
  - If (not fraction\_units or not fraction\_currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fraction\_units → not fraction\_currency.
    - Set fraction\_units, fraction\_length from 0.
- Set n from (formatted text %.{fraction\_length}f modulo or format number).
- Set numbers from n.split(“.”).
- Set tuple(main, fraction) from numbers when len(numbers) &gt; 1, otherwise list(n, “00”).
  - Value choice on len(numbers) &gt; 1 — true gives numbers, false gives list(n, “00”).
- If len(fraction) &lt; fraction\_length.
  - Set zeros from (“0” × (fraction\_length − len(fraction))).
  - Update fraction using + zeros.
- Set in\_million from true.
- If number\_format.string equals “#,##,###.##”.
  - Set in\_million from false.
- Bind local operation fraction\_in\_words for subsequent calls.
- If (main equals “0” and fraction belongs to list(“0”, “00”, “000”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in main equals “0” → fraction belongs to list(“0”, “00”, “000”).
  - Set out from ((\_(main\_currency, context = “Currency”) + one space) + translated “Zero”).
- Otherwise.
  - If main equals “0”.
    - Set out from formatted text {fraction\_in\_words()} {\_(fraction\_currency, context = “Currency”)}.
  - Otherwise.
    - If main\_currency equals “DZD”.
      - Set out from ((in\_words(main, in\_million).title() + one space) + \_(“Dinars”, context = “Currency”)).
    - Otherwise.
      - Set out from ((\_(main\_currency, context = “Currency”) + one space) + in\_words(main, in\_million).title()).
    - If cint(fraction).
      - Set out from ((((((out + one space) + translated “and”) + one space) + fraction\_in\_words()) + one space) + \_(fraction\_currency, context = “Currency”)).
- If main\_currency equals “DZD”.
  - Return \_(“{0}.”, context = “Money in words”).format(out).
- Return \_(“{0} only.”, context = “Money in words”).format(out).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L99) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L16)

<a id="op-2e443c3731942e"></a>
### Money in words.fraction in words

`operation_foundation_utils_data_business_behavior_money_in_words_fraction_in_words`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** in\_words((Decimal(formatted text 0.{fraction}) × fraction\_units), in\_million).title().

**Local steps**

- Return in\_words((Decimal(formatted text 0.{fraction}) × fraction\_units), in\_million).title().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L100) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L17)

<a id="op-ad4aeece241797"></a>
### In words

`operation_foundation_utils_data_business_behavior_in_words`

**Inputs** integer, in\_million = true.

**Declared result** str.

**Explicit results** ret.replace(“-”, one space).

**Local steps**

- Bind dependencies num2words.
- Set locale from “en\_IN” when not in\_million, otherwise Platform.local.lang.
  - Value choice on not in\_million — true gives “en\_IN”, false gives Platform.local.lang.
- Set integer from int(integer).
- Attempt the following.
  - Set ret from num2words(integer, lang = locale).
- On failure (NotImplementedError).
  - Set ret from num2words(integer, lang = “en”).
- On failure (OverflowError).
  - Set ret from num2words(integer, lang = “en”).
- Return ret.replace(“-”, one space).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L104) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L2)

<a id="op-b45031442e43f5"></a>
### Is html

`operation_foundation_utils_data_business_behavior_is_document_markup`

**Inputs** text.

**Declared result** bool.

**Explicit results** false · HTML\_TAG\_PATTERN.search(text).

**Local steps**

- If not isinstance(text, str).
  - Return false.
- Return HTML\_TAG\_PATTERN.search(text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L384) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L4)

<a id="op-70881ed6df411d"></a>
### Is image

`operation_foundation_utils_data_business_behavior_is_image`

**Inputs** filepath.

**Declared result** bool.

**Explicit results** (guess\_type(filepath) at 0 or empty text).startswith(“image/”).

**Local steps**

- Bind dependencies guess\_type.
- Set filepath from (filepath or empty text).split(“?”, 1) at 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filepath → empty text.
- Return (guess\_type(filepath) at 0 or empty text).startswith(“image/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in guess\_type(filepath) at 0 → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L482) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L5)

<a id="op-9a66492bd52069"></a>
### Validate egress url

`operation_foundation_utils_data_business_behavior_validate_egress_resource_address`

**Inputs** url.

**Declared result** no value.

**Explicit failure paths** ValueError(formatted text Disallowed scheme: {parsed.scheme}) · ValueError(“URL has no hostname”) · ValueError(formatted text Cannot resolve host {hostname}) · ValueError(formatted text Requests to internal address {ip} are not permitted).

**Local steps**

- Bind dependencies ipaddress.
- Bind dependencies socket.
- Set parsed from urlparse(url).
- If parsed.scheme does not belong to tuple(“http”, “https”).
  - Raise ValueError(formatted text Disallowed scheme: {parsed.scheme}).
- Set hostname from parsed.hostname.
- If not hostname.
  - Raise ValueError(“URL has no hostname”).
- Attempt the following.
  - Set addr\_info from socket.getaddrinfo(hostname, no value).
- On failure (socket.gaierror) bound to exc.
  - Raise ValueError(formatted text Cannot resolve host {hostname}) with cause exc.
- For each record in addr\_info.
  - Attempt the following.
    - Set ip from ipaddress.ip\_address(record at 4 at 0).
  - On failure (tuple(ValueError, IndexError)).
    - Continue with the next iteration or loop test.
  - If (ip.is\_private or ip.is\_loopback or ip.is\_link\_local or ip.is\_reserved).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ip.is\_private → ip.is\_loopback → ip.is\_link\_local → ip.is\_reserved.
    - Raise ValueError(formatted text Requests to internal address {ip} are not permitted).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(hostname, no value).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L632) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L60)

<a id="op-d955c0542a5ef9"></a>
### Get image thumbnail uri

`operation_foundation_utils_data_business_behavior_get_image_thumbnail_resource_identifier`

**Inputs** url, max\_dim = 400, quality = 80.

**Declared result** str.

**State and service calls** call save on img.

**Explicit results** url · cache at key · data\_uri.

**Local steps**

- Bind dependencies base64.
- Bind dependencies io.
- Bind dependencies os.
- If (not url or not isinstance(url, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not url → not isinstance(url, str).
  - Return url.
- If not (url.startswith(text in the contract) or url.startswith(text in the contract) or url.startswith(“/”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url.startswith(text in the contract) → url.startswith(text in the contract) → url.startswith(“/”).
  - Return url.
- Set cache from getattr(Platform.local, “\_print\_thumbnail\_cache”, no value).
- If cache is identical to no value.
  - Set cache, Platform.local.\_print\_thumbnail\_cache from mapping().
- Set key from tuple(url, max\_dim, quality).
- If key belongs to cache.
  - Return cache at key.
- If not url.startswith(“/”).
  - Attempt the following.
    - Evaluate validate\_egress\_url(url).
  - On failure (ValueError).
    - Return url.
- Attempt the following.
  - If url.startswith(“/”).
    - Set base from os.path.realpath(Platform.get\_site\_path(“public”)).
    - Set path from os.path.realpath(os.path.join(base, url.lstrip(“/”))).
    - If (os.path.commonpath(tuple(base, path)) differs from base or not os.path.isfile(path)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.path.commonpath(tuple(base, path)) differs from base → not os.path.isfile(path).
      - Return url.
    - Within open(path, “rb”) bound as f.
      - Set content from f.read().
  - Otherwise.
    - Bind dependencies requests.
    - Set r from requests.get(url, timeout = 5, stream = true, allow\_redirects = false).
    - Evaluate r.raise\_for\_status().
    - Set tuple(chunks, total) from tuple(list(), 0).
    - For each chunk in r.iter\_content(8192).
      - Evaluate chunks.append(chunk).
      - Update total using + len(chunk).
      - If total &gt; ((20 × 1024) × 1024).
        - Return url.
    - Set content from byte value.join(chunks).
  - Bind dependencies Image.
  - Set img from Image.open(io.BytesIO(content)).
  - Evaluate img.thumbnail(tuple(max\_dim, max\_dim), Image.Resampling.LANCZOS).
  - Set fmt from “PNG” when img.mode belongs to tuple(“RGBA”, “LA”, “P”), otherwise “JPEG”.
    - Value choice on img.mode belongs to tuple(“RGBA”, “LA”, “P”) — true gives “PNG”, false gives “JPEG”.
  - If (fmt equals “JPEG” and img.mode differs from “RGB”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fmt equals “JPEG” → img.mode differs from “RGB”.
    - Set img from img.convert(“RGB”).
  - Set buf from io.BytesIO().
  - Set save\_kwargs from mapping(“format” → fmt, “optimize” → true).
  - If fmt equals “JPEG”.
    - Set save\_kwargs at “quality” from quality.
  - Evaluate img.save(buf, expanded names save\_kwargs).
  - Set encoded from base64.b64encode(buf.getvalue()).decode(“ascii”).
  - Set data\_uri from formatted text data:image/{fmt.lower()};base64,{encoded}.
  - Set cache at key from data\_uri.
  - Return data\_uri.
- On failure (Exception).
  - Return url.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_print\_thumbnail\_cache”, no value) · service or queued work from requests.get(url, timeout = 5, stream = true, allow\_redirects = false).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L92) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1706)

<a id="op-af77cb59b1ecc2"></a>
### Get thumbnail base64 for image

`operation_foundation_utils_data_business_behavior_get_thumbnail_base_64_for_image`

**Inputs** src.

**Declared result** (dict at tuple(str, str) bitwise or no value).

**Explicit results** no value · cache().hget(“thumbnail\_base64”, src, generator = \_get\_base64).

**Explicit failure paths** validation helper — formatted text Invalid source for image: {src}.

**Local steps**

- Bind dependencies file\_exists.
- Bind dependencies Image.
- Bind dependencies cache, safe\_decode.
- Bind dependencies get\_local\_image.
- If not src.
  - Call the validation error handler Platform.throw(formatted text Invalid source for image: {src}).
- If (not src.startswith(“/files”) or “..” belongs to src).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not src.startswith(“/files”) → “..” belongs to src.
  - Return no value.
- If src.endswith(“.svg”).
  - Return no value.
- Bind local operation \_get\_base64 for subsequent calls.
- Return cache().hget(“thumbnail\_base64”, src, generator = \_get\_base64).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L2619) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1733)

<a id="op-0ea29ca3a5d532"></a>
### Get thumbnail base64 for image.get base64

`operation_foundation_utils_data_business_behavior_get_thumbnail_base_64_for_image_get_base_64`

**Inputs** no declared parameters.

**Explicit results** no value · mapping(“base64” → formatted text data:image/{extn};base64,{safe\_decode(base64\_string)}, “width” → original\_size at 0, “height” → original\_size at 1).

**Local steps**

- Set file\_path from Platform.get\_site\_path(“public”, src.lstrip(“/”)).
- If not file\_exists(file\_path).
  - Return no value.
- Attempt the following.
  - Set tuple(image, \_unused\_filename, extn) from get\_local\_image(src).
- On failure (OSError).
  - Return no value.
- Set original\_size from image.size.
- Set size from tuple(50, 50).
- Evaluate image.thumbnail(size, Image.Resampling.LANCZOS).
- Set base64\_string from image\_to\_base64(image, extn).
- Return mapping(“base64” → formatted text data:image/{extn};base64,{safe\_decode(base64\_string)}, “width” → original\_size at 0, “height” → original\_size at 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L3286) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1734)

<a id="op-7069c83c8e2838"></a>
### Image to base64

`operation_foundation_utils_data_business_behavior_image_to_base_64`

**Inputs** image, extn.

**Declared result** bytes.

**State and service calls** call save on image.

**Explicit results** base64.b64encode(buffered.getvalue()).

**Local steps**

- Bind dependencies BytesIO.
- Set buffered from BytesIO().
- If extn.lower() belongs to tuple(“jpg”, “jpe”).
  - Set extn from “JPEG”.
- Evaluate image.save(buffered, extn).
- Return base64.b64encode(buffered.getvalue()).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L3673) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1758)

<a id="op-318243f6f9d2ac"></a>
### Pdf to base64

`operation_foundation_utils_data_business_behavior_portable_document_to_base_64`

**Inputs** filename.

**Declared result** (bytes bitwise or no value).

**Explicit results** no value · base64\_string.

**Local steps**

- Bind dependencies get\_file\_path.
- If (“../” belongs to filename or filename.rsplit(“.”) at negative 1 does not belong to list(“pdf”, “PDF”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “../” belongs to filename → filename.rsplit(“.”) at negative 1 does not belong to list(“pdf”, “PDF”).
  - Return no value.
- Set file\_path from get\_file\_path(filename).
- If not file\_path.
  - Return no value.
- Within open(file\_path, “rb”) bound as pdf\_file.
  - Set base64\_string from base64.b64encode(pdf\_file.read()).
- Return base64\_string.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L3872) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L28)

<a id="op-ff167acddc52ba"></a>
### Strip html

`operation_foundation_utils_data_business_behavior_strip_document_markup`

**Inputs** text.

**Declared result** str.

**Explicit results** \_striptags\_re.sub(empty text, text).

**Local steps**

- Return \_striptags\_re.sub(empty text, text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L4140) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L49)

<a id="op-7e33588e402e09"></a>
### Escape html

`operation_foundation_utils_data_business_behavior_escape_document_markup`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** text.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L4205) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1669)

<a id="op-2bdd45969a012b"></a>
### Pretty date

`operation_foundation_utils_data_business_behavior_pretty_date`

**Inputs** iso\_datetime, mini = false.

**Declared result** str.

**Explicit results** empty text · format\_timedelta((iso\_datetime − now\_dt), add\_direction = not mini, locale = locale, format = “long” when not mini, otherwise “narrow”).

**Local steps**

- If not iso\_datetime.
  - Return empty text.
- Bind dependencies format\_timedelta.
- If isinstance(iso\_datetime, str).
  - Set iso\_datetime from get\_datetime(iso\_datetime).
- Set now\_dt from now\_datetime().
- Set locale from Platform.local.lang.replace(“-”, “\_”) when Platform.local.lang, otherwise no value.
  - Value choice on Platform.local.lang — true gives Platform.local.lang.replace(“-”, “\_”), false gives no value.
- Return format\_timedelta((iso\_datetime − now\_dt), add\_direction = not mini, locale = locale, format = “long” when not mini, otherwise “narrow”).
  - Value choice on not mini — true gives “long”, false gives “narrow”.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L4410) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L29)

<a id="op-0501b369771a6b"></a>
### Comma or

`operation_foundation_utils_data_business_behavior_comma_or`

**Inputs** some\_list, add\_quotes = true.

**Declared result** str.

**Explicit results** comma\_sep(some\_list, pattern, add\_quotes).

**Local steps**

- Bind dependencies Locale.
- Attempt the following.
  - Set locale from Locale.parse(Platform.local.lang, sep = “-”).
  - Set pattern from locale.list\_patterns at “or” at “2” when len(some\_list) equals 2, otherwise “end”.
    - Value choice on len(some\_list) equals 2 — true gives “2”, false gives “end”.
- On failure (Exception).
  - Set pattern from Platform.\_(“{0} or {1}”).
- Return comma\_sep(some\_list, pattern, add\_quotes).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L85) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1094) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1653)

<a id="op-560415546993de"></a>
### Comma and

`operation_foundation_utils_data_business_behavior_comma_and`

**Inputs** some\_list, add\_quotes = true.

**Declared result** str.

**Explicit results** comma\_sep(some\_list, pattern, add\_quotes).

**Local steps**

- Bind dependencies Locale.
- Attempt the following.
  - Set locale from Locale.parse(Platform.local.lang, sep = “-”).
  - Set pattern from locale.list\_patterns at “standard” at “2” when len(some\_list) equals 2, otherwise “end”.
    - Value choice on len(some\_list) equals 2 — true gives “2”, false gives “end”.
- On failure (Exception).
  - Set pattern from Platform.\_(“{0} and {1}”).
- Return comma\_sep(some\_list, pattern, add\_quotes).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L84) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1093) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1652)

<a id="op-6aae339db8b875"></a>
### Comma sep

`operation_foundation_utils_data_business_behavior_comma_separation`

**Inputs** some\_list, pattern, add\_quotes = true.

**Declared result** str.

**Explicit results** empty text · some\_list at 0 · pattern.format(“, ”.join(generator of Platform.\_(s) for s drawn from some\_list at slice no value to negative 1), some\_list at negative 1) · some\_list.

**Local steps**

- If isinstance(some\_list, (list bitwise or tuple)).
  - Set some\_list from list of str(s) for s drawn from list(some\_list).
    - Draw s from list(some\_list).
  - If not some\_list.
    - Return empty text.
  - Otherwise.
    - If len(some\_list) equals 1.
      - Return some\_list at 0.
    - Otherwise.
      - Set some\_list from list of “'{}'”.format(s) for s drawn from some\_list when add\_quotes, otherwise list of “{}”.format(s) for s drawn from some\_list.
        - Value choice on add\_quotes — true gives list of “'{}'”.format(s) for s drawn from some\_list, false gives list of “{}”.format(s) for s drawn from some\_list.
        - Draw s from some\_list.
        - Draw s from some\_list.
      - Return pattern.format(“, ”.join(generator of Platform.\_(s) for s drawn from some\_list at slice no value to negative 1), some\_list at negative 1).
        - Draw s from some\_list at slice no value to negative 1.
- Otherwise.
  - Return some\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L5170) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1095) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1654)

<a id="op-cf4900e3b4fdda"></a>
### New line sep

`operation_foundation_utils_data_business_behavior_new_line_separation`

**Inputs** some\_list.

**Declared result** str.

**Explicit results** empty text · some\_list at 0 · format(whitespace '\\n '.join(some\_list)) · some\_list.

**Local steps**

- If isinstance(some\_list, (list bitwise or tuple)).
  - Set some\_list from list of str(s) for s drawn from list(some\_list).
    - Draw s from list(some\_list).
  - If not some\_list.
    - Return empty text.
  - Otherwise.
    - If len(some\_list) equals 1.
      - Return some\_list at 0.
    - Otherwise.
      - Set some\_list from list of “{}”.format(s) for s drawn from some\_list.
        - Draw s from some\_list.
      - Return format(whitespace '\\n '.join(some\_list)).
- Otherwise.
  - Return some\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L5611) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L19)
