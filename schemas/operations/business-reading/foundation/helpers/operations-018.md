# Shared value and file services · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-0aaf9acaa4e7ed"></a>
### Get filter

`operation_foundation_utils_data_business_behavior_get_filter`

**Inputs** doctype, filters, filters\_config = no value.

**Declared result** “Platform.\_dict”.

**Explicit results** f.

**Explicit failure paths** validation helper — Platform.\_(“Operator must be one of {0}”).format(“, ”.join(valid\_operators)).

**Local steps**

- Bind dependencies NestedSetHierarchy.
- Bind dependencies child\_table\_fields, default\_fields, optional\_fields.
- If isinstance(filters, FilterTuple).
  - Set ft from filters.
- Otherwise.
  - If not isinstance(filters, Filters).
    - Set ft from Filters(filters, doctype = doctype) at 0.
  - Otherwise.
    - Set ft from filters at 0.
- Set f from Platform.\_dict(doctype = ft at 0, fieldname = ft at 1, operator = ft at 2, value = ft at 3).
- Set f.fieldname from sanitize\_column(f.fieldname).
- Set valid\_operators from tuple(“=”, “!=”, “&gt;”, “&lt;”, …).
- If filters\_config.
  - Set additional\_operators from list of key.lower() for key drawn from filters\_config.
    - Draw key from filters\_config.
  - Set valid\_operators from tuple(set((valid\_operators + tuple(additional\_operators)))).
- If f.operator.lower() does not belong to valid\_operators.
  - Call the validation error handler Platform.throw(Platform.\_(“Operator must be one of {0}”).format(“, ”.join(valid\_operators))).
- If (f.doctype and f.fieldname does not belong to ((default\_fields + optional\_fields) + child\_table\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.doctype → f.fieldname does not belong to ((default\_fields + optional\_fields) + child\_table\_fields).
  - Set meta from Platform.get\_meta(f.doctype).
  - If not meta.has\_field(f.fieldname).
    - For each df in meta.get\_table\_fields(include\_computed = true).
      - If Platform.get\_meta(df.options).has\_field(f.fieldname).
        - Set f.doctype from df.options.
        - Leave the innermost loop without its normal-exhaustion alternative.
- Attempt the following.
  - Set df from Platform.get\_meta(f.doctype).get\_field(f.fieldname) when f.doctype, otherwise no value.
    - Value choice on f.doctype — true gives Platform.get\_meta(f.doctype).get\_field(f.fieldname), false gives no value.
- On failure (Platform.exceptions.DoesNotExistError).
  - Set df from no value.
- Set f.fieldtype from df.fieldtype when df, otherwise no value.
  - Value choice on df — true gives df.fieldtype, false gives no value.
- Return f.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L4428) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1695)

<a id="op-048e45c0b3102b"></a>
### Make filter tuple

`operation_foundation_utils_data_business_behavior_make_filter_tuple`

**Inputs** doctype, key, value.

**Explicit results** list(doctype, key, value at 0, value at 1) · list(doctype, key, “=”, value).

**Local steps**

- If isinstance(value, (list bitwise or tuple)).
  - Return list(doctype, key, value at 0, value at 1).
- Otherwise.
  - Return list(doctype, key, “=”, value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L5471) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L11)

<a id="op-5b4f20c0cd9e6a"></a>
### Make filter dict

`operation_foundation_utils_data_business_behavior_make_filter_mapping`

**Inputs** filters.

**Explicit results** \_filter.

**Local steps**

- Set \_filter from Platform.\_dict().
- For each f in filters.
  - Set \_filter at f at 1 from tuple(f at 2, f at 3).
- Return \_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L5613) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L10)

<a id="op-9a7dd6a80fe75f"></a>
### Sanitize column

`operation_foundation_utils_data_business_behavior_sanitize_column`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** column\_name.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L5740) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L42)

<a id="op-160d8dbcc405d3"></a>
### Sanitize column

`operation_foundation_utils_data_business_behavior_sanitize_column_2`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** column\_name, db\_type.

**Explicit result forms** a value selected from the current context.

**Local structure** 7 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L5834) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L43)

<a id="op-412ad5556f67b0"></a>
### Sanitize column.raise exception

`operation_foundation_utils_data_business_behavior_sanitize_column_raise_exception`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** no parameters.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L6574) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L44)

<a id="op-e56048beeb84cd"></a>
### Scrub urls

`operation_foundation_utils_data_business_behavior_scrub_resource_addresses`

**Inputs** html.

**Declared result** str.

**Explicit results** expand\_relative\_urls(html).

**Local steps**

- Return expand\_relative\_urls(html).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L6659) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L46)

<a id="op-ed69f382db8ad4"></a>
### Expand relative urls

`operation_foundation_utils_data_business_behavior_expand_relative_resource_addresses`

**Inputs** html.

**Declared result** str.

**Explicit results** html.

**Local steps**

- Set url from get\_url().
- If url.endswith(“/”).
  - Set url from url at slice no value to negative 1.
- Bind local operation \_expand\_relative\_urls for subsequent calls.
- Set html from URLS\_NOT\_HTTP\_TAG\_PATTERN.sub(\_expand\_relative\_urls, html).
- Set html from URL\_NOTATION\_PATTERN.sub(\_expand\_relative\_urls, html).
- Return html.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L6718) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1671)

<a id="op-5288bdde5de026"></a>
### Expand relative urls.expand relative urls

`operation_foundation_utils_data_business_behavior_expand_relative_resource_addresses_expand_relative_resource_addresses`

**Inputs** match.

**State and service calls** call insert on to\_expand.

**Explicit results** empty text.join(to\_expand).

**Local steps**

- Set to\_expand from list(match.groups()).
- If not to\_expand at 2.startswith(tuple(“mailto”, “data:”, “tel:”)).
  - If not to\_expand at 2.startswith(“/”).
    - Set to\_expand at 2 from (“/” + to\_expand at 2).
  - Evaluate to\_expand.insert(2, url).
- If (“url” belongs to to\_expand at 0 and to\_expand at 1.startswith(“(”) and to\_expand at negative 1.endswith(“)”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “url” belongs to to\_expand at 0 → to\_expand at 1.startswith(“(”) → to\_expand at negative 1.endswith(“)”).
  - Evaluate to\_expand.append(“ !important”).
- Return empty text.join(to\_expand).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1672)

<a id="op-677a82547d9f53"></a>
### Quoted

`operation_foundation_utils_data_business_behavior_quoted`

**Inputs** url.

**Declared result** str.

**Explicit results** cstr(quote(encode(cstr(url)), safe = byte value)).

**Local steps**

- Return cstr(quote(encode(cstr(url)), safe = byte value)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L364) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L32)

<a id="op-002fc685b17292"></a>
### Quote urls

`operation_foundation_utils_data_business_behavior_quote_resource_addresses`

**Inputs** html.

**Declared result** str.

**Explicit results** URLS\_HTTP\_TAG\_PATTERN.sub(\_quote\_url, html).

**Local steps**

- Bind local operation \_quote\_url for subsequent calls.
- Return URLS\_HTTP\_TAG\_PATTERN.sub(\_quote\_url, html).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L492) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L30)

<a id="op-8c469f0600599f"></a>
### Quote urls.quote url

`operation_foundation_utils_data_business_behavior_quote_resource_addresses_quote_resource_address`

**Inputs** match.

**Explicit results** empty text.join(groups).

**Local steps**

- Set groups from list(match.groups()).
- Set groups at 2 from quoted(groups at 2).
- Return empty text.join(groups).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L675) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L31)

<a id="op-2a7deba88c1075"></a>
### Unique

`operation_foundation_utils_data_business_behavior_unique`

**Inputs** seq.

**Declared result** list at “T”.

**Explicit results** list of x for x drawn from seq where not (x belongs to seen or seen\_add(x)).

**Local steps**

- Set seen from set().
- Set seen\_add from seen.add.
- Return list of x for x drawn from seq where not (x belongs to seen or seen\_add(x)).
  - Draw x from seq, keep a combination only if (not (x belongs to seen or seen\_add(x))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in x belongs to seen → seen\_add(x).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L807) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L58)

<a id="op-62aa1e729626d0"></a>
### Strip

`operation_foundation_utils_data_business_behavior_strip`

**Inputs** val, chars = no value.

**Declared result** str.

**Explicit results** (nested operand in the contract or nested operand in the contract).replace(“﻿”, empty text).replace(“​”, empty text).strip(chars).

**Local steps**

- Return (nested operand in the contract or nested operand in the contract).replace(“﻿”, empty text).replace(“​”, empty text).strip(chars).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in val → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L976) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L48)

<a id="op-e834613a0be2f0"></a>
### Get string between

`operation_foundation_utils_data_business_behavior_get_string_between`

**Inputs** start, string, end.

**Declared result** str.

**Explicit results** empty text · out.group(1) when out, otherwise string.

**Local steps**

- If not string.
  - Return empty text.
- Set out from re.search(formatted text {start}(.\*){end}, string).
- Return out.group(1) when out, otherwise string.
  - Value choice on out — true gives out.group(1), false gives string.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1109) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1731)

<a id="op-becb3229e71bdf"></a>
### To markdown

`operation_foundation_utils_data_business_behavior_to_markdown`

**Inputs** html.

**Declared result** str.

**Explicit results** html2text((html or empty text)).

**Local steps**

- Bind dependencies HTMLParser.
- Bind dependencies html2text.
- Attempt the following.
  - Return html2text((html or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in html → empty text.
- On failure (HTMLParser.HTMLParseError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1286) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L54)

<a id="op-598b21dd2eba5f"></a>
### Md to html

`operation_foundation_utils_data_business_behavior_explanatory_document_to_document_markup`

**Inputs** markdown\_text.

**Declared result** (“UnicodeWithAttrs” bitwise or no value).

**Explicit results** UnicodeWithAttrs(\_markdown((markdown\_text or empty text), extras = extras)).

**Local steps**

- Bind dependencies MarkdownError.
- Bind dependencies \_markdown.
- Set extras from mapping(“fenced-code-blocks” → no value, “tables” → no value, “header-ids” → no value, “toc” → no value, …).
- Attempt the following.
  - Return UnicodeWithAttrs(\_markdown((markdown\_text or empty text), extras = extras)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in markdown\_text → empty text.
- On failure (MarkdownError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1400) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1673)

<a id="op-ba7ac340e353e2"></a>
### Markdown

`operation_foundation_utils_data_business_behavior_markdown`

**Inputs** markdown\_text.

**Declared result** (“UnicodeWithAttrs” bitwise or no value).

**Explicit results** md\_to\_html(markdown\_text).

**Local steps**

- Return md\_to\_html(markdown\_text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1646) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L14)

<a id="op-84b8bc09a850ae"></a>
### Is subset

`operation_foundation_utils_data_business_behavior_is_subset`

**Inputs** list\_a, list\_b.

**Declared result** bool.

**Explicit results** len(list((set(list\_a) bitwise and set(list\_b)))) equals len(list\_a).

**Local steps**

- Return len(list((set(list\_a) bitwise and set(list\_b)))) equals len(list\_a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1716) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L9)

<a id="op-fb13f0fa19a85d"></a>
### Generate hash

`operation_foundation_utils_data_business_behavior_generate_hash`

**Inputs** remaining positional values args, remaining named values kwargs.

**Declared result** str.

**Explicit results** Platform.generate\_hash(expanded args, expanded names kwargs).

**Local steps**

- Return Platform.generate\_hash(expanded args, expanded names kwargs).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1851) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1686)

<a id="op-f15a980ff5b6dc"></a>
### Sha256 hash

`operation_foundation_utils_data_business_behavior_secure_hash_256_hash`

**Inputs** input.

**Declared result** str.

**Explicit results** hashlib.sha256(input).hexdigest().

**Local steps**

- If isinstance(input, str).
  - Set input from input.encode().
- Return hashlib.sha256(input).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L1924) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L47)

<a id="op-89bef41e5543cf"></a>
### Is sha256 hash

`operation_foundation_binding_foundation_utils_data_is_sha256_hash`

**Inputs** value.

**Declared result** bool.

**Explicit results** (len(value) equals 64 and all(generator of character belongs to “0123456789abcdef” for character drawn from value.lower())).

**Local steps**

- Return (len(value) equals 64 and all(generator of character belongs to “0123456789abcdef” for character drawn from value.lower())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(value) equals 64 → all(generator of character belongs to “0123456789abcdef” for character drawn from value.lower()).
  - Draw character from value.lower().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L55) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L213)

<a id="op-70ff5050e450e5"></a>
### Dict with keys

`operation_foundation_utils_data_business_behavior_mapping_with_keys`

**Inputs** dict, keys.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each key in dict.
  - If key belongs to keys.
    - Set out at key from dict at key.
- Return out.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L2056) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L13)

<a id="op-fbcc2d04a4694c"></a>
### Guess date format

`operation_foundation_utils_data_business_behavior_guess_date_format`

**Inputs** date\_string.

**Declared result** str.

**Explicit results** date\_format · time\_format · ((date\_format + one space) + time\_format).strip().

**Local steps**

- Set DATE\_FORMATS from list(“%d/%b/%y”, “%d/%b/%Y”, “%d %b %Y”, “%d %B %Y”, …).
- Set TIME\_FORMATS from list(“%H:%M:%S.%f”, “%H:%M:%S”, “%H:%M”, “%I:%M:%S.%f %p”, …).
- Bind local operation \_get\_date\_format for subsequent calls.
- Bind local operation \_get\_time\_format for subsequent calls.
- Set date\_format from no value.
- Set time\_format from no value.
- Set date\_string from date\_string.strip().
- Set date\_format from \_get\_date\_format(date\_string).
- If date\_format.
  - Return date\_format.
- Set time\_format from \_get\_time\_format(date\_string).
- If time\_format.
  - Return time\_format.
- If one space belongs to date\_string.
  - Set tuple(date\_str, time\_str) from date\_string.split(one space, 1).
  - Set date\_format from (\_get\_date\_format(date\_str) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_date\_format(date\_str) → empty text.
  - Set time\_format from (\_get\_time\_format(time\_str) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_time\_format(time\_str) → empty text.
  - If (date\_format and time\_format).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_format → time\_format.
    - Return ((date\_format + one space) + time\_format).strip().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L2177) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1754)
