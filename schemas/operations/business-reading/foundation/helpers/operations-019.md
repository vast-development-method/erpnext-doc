# Shared value and file services · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-1819e6a9dcde58"></a>
### Guess date format.get date format

`operation_foundation_utils_data_business_behavior_guess_date_format_get_date_format`

**Inputs** date\_str.

**Explicit results** f.

**Local steps**

- For each f in DATE\_FORMATS.
  - Attempt the following.
    - Evaluate datetime.datetime.strptime(date\_str, f).
    - Return f.
  - On failure (ValueError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L2879) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1755)

<a id="op-d1d4ecaef4ddfe"></a>
### Guess date format.get time format

`operation_foundation_utils_data_business_behavior_guess_date_format_get_time_format`

**Inputs** time\_str.

**Explicit results** f.

**Local steps**

- For each f in TIME\_FORMATS.
  - Attempt the following.
    - Evaluate datetime.datetime.strptime(time\_str, f).
    - Return f.
  - On failure (ValueError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L2986) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1756)

<a id="op-c7e4ad3e6eb76b"></a>
### Validate json string

`operation_foundation_utils_data_business_behavior_validate_structured_data_string`

**Inputs** string.

**Declared result** no value.

**Explicit failure paths** Platform.ValidationError.

**Local steps**

- Attempt the following.
  - Evaluate orjson.loads(string).
- On failure (tuple(TypeError, ValueError)).
  - Raise Platform.ValidationError.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L3093) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L62)

<a id="op-1543f77f6b8055"></a>
### Parse json

`operation_foundation_utils_data_business_behavior_parse_structured_data`

**Inputs** val.

**Explicit results** val.

**Local steps**

- If isinstance(val, str).
  - Set val from orjson.loads(val).
- If isinstance(val, dict).
  - Set val from Platform.\_dict(val).
- Return val.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L101) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L25)

<a id="op-8105e4439d96c3"></a>
### Orjson dumps

`operation_foundation_utils_data_business_behavior_orjson_dumps`

**Inputs** obj, default = no value, option = no value, decode = true.

**Explicit results** json.dumps(obj, default = default) when decode, otherwise json.dumps(obj, default = default).encode() · value.decode() when decode, otherwise value.

**Local steps**

- If option is distinct from no value.
  - Set option from (option bitwise or DEFAULT\_ORJSON\_OPTIONS).
- Otherwise.
  - Set option from DEFAULT\_ORJSON\_OPTIONS.
- Attempt the following.
  - Set value from orjson.dumps(obj, default, option).
- On failure (orjson.JSONEncodeError).
  - Return json.dumps(obj, default = default) when decode, otherwise json.dumps(obj, default = default).encode().
    - Value choice on decode — true gives json.dumps(obj, default = default), false gives json.dumps(obj, default = default).encode().
- Return value.decode() when decode, otherwise value.
  - Value choice on decode — true gives value.decode(), false gives value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L3349) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L23)

<a id="op-cbc796c7f6cf8d"></a>
### Get user info for avatar

`operation_foundation_utils_data_business_behavior_get_user_info_for_avatar`

**Inputs** user\_id.

**Declared result** \_UserInfo.

**Record and data access** resolve a document from “User” via get\_cached\_doc.

**Explicit results** mapping(“email” → user.email, “image” → user.user\_image, “name” → user.full\_name) · mapping(“email” → user\_id, “image” → empty text, “name” → user\_id).

**Local steps**

- Attempt the following.
  - Set user from Platform.get\_cached\_doc(“User”, user\_id).
  - Return mapping(“email” → user.email, “image” → user.user\_image, “name” → user.full\_name).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return mapping(“email” → user\_id, “image” → empty text, “name” → user\_id).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“User”, user\_id).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L3637) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1741)

<a id="op-c8af57bbdac4cc"></a>
### Validate python code

`operation_foundation_utils_data_business_behavior_validate_implementation_language_code`

**Inputs** string, fieldname = no value, is\_expression = true.

**Declared result** no value.

**State and service calls** msgprint with Platform.\_(“{} Possibly invalid python code. &lt;br&gt;{}”).format(((fieldname + “: ”) or empty text), str(e)).

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not string.
  - Return no value.
- Attempt the following.
  - Evaluate compile\_command(string, symbol = “eval” when is\_expression, otherwise “exec”).
    - Value choice on is\_expression — true gives “eval”, false gives “exec”.
- On failure (SyntaxError) bound to se.
  - Set line\_no from ((se.lineno − 1) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (se.lineno − 1) → 0.
  - Set offset from ((se.offset − 1) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (se.offset − 1) → 0.
  - Set error\_line from string when is\_expression, otherwise string.split(whitespace '\\n') at line\_no.
    - Value choice on is\_expression — true gives string, false gives string.split(whitespace '\\n') at line\_no.
  - Set msg from Platform.\_(“{} Invalid python code on line {}”).format((fieldname + “:”) when fieldname, otherwise empty text, (line\_no + 1)).
    - Value choice on fieldname — true gives (fieldname + “:”), false gives empty text.
  - Update msg using + formatted text &lt;br&gt;&lt;pre&gt;{error\_line}&lt;/pre&gt;.
  - Update msg using + formatted text &lt;pre&gt;{(one space × offset)}^&lt;/pre&gt;.
  - Call the validation error handler Platform.throw(msg, title = Platform.\_(“Syntax Error”)).
- On failure (Exception) bound to e.
  - Evaluate Platform.msgprint(Platform.\_(“{} Possibly invalid python code. &lt;br&gt;{}”).format(((fieldname + “: ”) or empty text), str(e)), indicator = “orange”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (fieldname + “: ”) → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L3882) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L61)

<a id="op-83b28948a17eab"></a>
### Unicode With Attrs.initialize

`operation_foundation_utils_data_business_behavior_unicode_with_attrs_initialize`

**Inputs** self, text.

**Local steps**

- Set self.toc\_html from text.toc\_html.
- Set self.metadata from text.metadata.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L4470) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L57)

<a id="op-fcac9c95d7f423"></a>
### Format timedelta

`operation_foundation_utils_data_business_behavior_format_timedelta`

**Inputs** o.

**Declared result** str.

**Explicit results** formatted text {int(hours)}:{int(minutes)}:{seconds}.

**Local steps**

- If isinstance(o, datetime.timedelta).
  - Set total\_seconds from o.total\_seconds().
- Otherwise.
  - Set total\_seconds from cint(o).
- Set tuple(hours, remainder) from divmod(total\_seconds, 3600).
- Set tuple(minutes, seconds) from divmod(remainder, 60).
- Set rounded\_seconds from round(seconds, 6).
- Set int\_seconds from int(seconds).
- If rounded\_seconds equals int\_seconds.
  - Set seconds from int\_seconds.
- Otherwise.
  - Set seconds from rounded\_seconds.
- Return formatted text {int(hours)}:{int(minutes)}:{seconds}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L4549) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1685)

<a id="op-f15b8200653334"></a>
### Parse timedelta

`operation_foundation_utils_data_business_behavior_parse_timedelta`

**Inputs** s.

**Declared result** datetime.timedelta.

**Explicit results** datetime.timedelta(expanded names mapping of key → float(val) for tuple(key, val) drawn from m.groupdict().items()).

**Local steps**

- If “day” belongs to s.
  - Set m from TIMEDELTA\_DAY\_PATTERN.match(s).
- Otherwise.
  - Set m from TIMEDELTA\_BASE\_PATTERN.match(s).
- Return datetime.timedelta(expanded names mapping of key → float(val) for tuple(key, val) drawn from m.groupdict().items()).
  - Draw tuple(key, val) from m.groupdict().items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L4947) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L26)

<a id="op-f5ce5a8049a4f2"></a>
### Get job name

`operation_foundation_utils_data_business_behavior_get_job_name`

**Inputs** key, doctype = no value, doc\_name = no value.

**Declared result** str.

**Explicit results** job\_name.

**Local steps**

- Set job\_name from key.
- If doctype.
  - Update job\_name using + formatted text \_{doctype}.
- If doc\_name.
  - Update job\_name using + formatted text \_{doc\_name}.
- Return job\_name.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5163) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1708)

<a id="op-9f0737184ed3fd"></a>
### Get imaginary pixel response

`operation_foundation_utils_data_business_behavior_get_imaginary_pixel_response`

**Inputs** no declared parameters.

**Explicit results** mapping(“type” → “binary”, “filename” → “imaginary\_pixel.png”, “filecontent” → byte value).

**Local steps**

- Return mapping(“type” → “binary”, “filename” → “imaginary\_pixel.png”, “filecontent” → byte value).

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5342) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1707)

<a id="op-f9bb21e3518a87"></a>
### Is site link

`operation_foundation_utils_data_business_behavior_is_site_link`

**Inputs** link.

**Declared result** bool.

**Explicit results** false · true · urlparse(link).netloc equals urlparse(Platform.utils.get\_url()).netloc.

**Local steps**

- If not link.
  - Return false.
- If link.startswith(“/”).
  - Return true.
- Return urlparse(link).netloc equals urlparse(Platform.utils.get\_url()).netloc.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5486) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L8)

<a id="op-f7a4cda511ceb8"></a>
### Bold

`operation_foundation_utils_data_business_behavior_bold`

**Inputs** text.

**Declared result** str.

**Explicit results** formatted text &lt;strong&gt;{text}&lt;/strong&gt;.

**Local steps**

- Return formatted text &lt;strong&gt;{text}&lt;/strong&gt;.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5646) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1089) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1648)

<a id="op-ab3ac953aeffd7"></a>
### Safe encode

`operation_foundation_utils_data_business_behavior_safe_encode`

**Inputs** param, encoding = “utf-8”.

**Explicit results** param.

**Local steps**

- Attempt the following.
  - Set param from param.encode(encoding).
- On failure (Exception).
  - Take no action here.
- Return param.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5730) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L41)

<a id="op-611869a3cdfd93"></a>
### Safe decode

`operation_foundation_utils_data_business_behavior_safe_decode`

**Inputs** param, encoding = “utf-8”, fallback\_map = no value.

**Explicit results** param.

**Local steps**

- Attempt the following.
  - Set param from param.decode(encoding).
- On failure (LookupError).
  - Attempt the following.
    - Set param from param.decode((fallback\_map or mapping()).get(encoding, “utf-8”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in fallback\_map → mapping().
  - On failure (Exception).
    - Take no action here.
- On failure (Exception).
  - Take no action here.
- Return param.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L5831) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L39)

<a id="op-642eb25ed941af"></a>
### As unicode

`operation_foundation_utils_data_business_behavior_as_unicode`

**Inputs** text, encoding = “utf-8”.

**Declared result** str.

**Explicit results** text · empty text · str(text, encoding) · str(text).

**Local steps**

- If isinstance(text, str).
  - Return text.
- Otherwise.
  - If text is identical to no value.
    - Return empty text.
  - Otherwise.
    - If isinstance(text, bytes).
      - Return str(text, encoding).
    - Otherwise.
      - Return str(text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6046) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1085) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1644)

<a id="op-579a3a787e4ffc"></a>
### Mock

`operation_foundation_utils_data_business_behavior_mock`

**Inputs** type, size = 1, locale = “en”.

**Explicit results** squashify(results).

**Explicit failure paths** ValueError(“Not a valid mock type.”).

**Local steps**

- Bind dependencies faker.
- Set results from list().
- Set fake from faker.Faker(locale).
- If type does not belong to dir(fake).
  - Raise ValueError(“Not a valid mock type.”).
- Otherwise.
  - For each \_ in range(size).
    - Set data from getattr(fake, type)().
    - Evaluate results.append(data).
- Bind dependencies squashify.
- Return squashify(results).

**Values supplied outside this operation** selected callable from getattr(fake, type).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6225) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L15)

<a id="op-d4686541bf94c8"></a>
### Recursive defaultdict

`operation_foundation_utils_data_business_behavior_recursive_defaultdict`

**Inputs** no declared parameters.

**Explicit results** defaultdict(recursive\_defaultdict).

**Local steps**

- Return defaultdict(recursive\_defaultdict).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6504) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L33)

<a id="op-85d50dd3665e72"></a>
### Get rss memory usage

`operation_foundation_utils_data_business_behavior_get_rss_memory_usage`

**Inputs** no declared parameters.

**Explicit results** rss.

**Local steps**

- Bind dependencies psutil.
- Set rss from (psutil.Process().memory\_info().rss floor divide (1024 × 1024)).
- Return rss.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6546) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1729)

<a id="op-59ddab847691a0"></a>
### Add trackers to url

`operation_foundation_utils_data_business_behavior_add_trackers_to_resource_address`

**Inputs** url, source, campaign = no value, medium = no value, content = no value.

**Declared result** str.

**Explicit results** url · urlunparse(url\_parts).

**Local steps**

- Bind local operation get\_utm\_values for subsequent calls.
- Set url\_parts from list(urlparse(url)).
- If url\_parts at 0 equals “mailto”.
  - Return url.
- Set tuple(source, medium, campaign) from Platform.cache.get\_value((((((“utm\_” + nested operand in the contract(nested operand in the contract)) + “\_”) + cstr(medium)) + “\_”) + cstr(campaign)), get\_utm\_values, shared = true).
- Set trackers from mapping(“utm\_source” → source).
- If medium.
  - Set trackers at “utm\_medium” from medium.
- If campaign.
  - Set trackers at “utm\_campaign” from campaign.
- If content.
  - Set trackers at “utm\_content” from content.
- Set query from (dict(parse\_qsl(url\_parts at 4)) bitwise or trackers).
- Set url\_parts at 4 from urlencode(query).
- Return urlunparse(url\_parts).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L6641) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1082) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1641)

<a id="op-592ba148dc20de"></a>
### Add trackers to url.get utm values

`operation_foundation_utils_data_business_behavior_add_trackers_to_resource_address_get_campaign_tracking_values`

**Inputs** no declared parameters.

**Record and data access** read “UTM Source” via get\_value · read “UTM Campaign” via get\_value · read “UTM Medium” via get\_value.

**Explicit results** tuple(\_source, \_medium, \_campaign).

**Local steps**

- Set \_source from (Platform.db.get\_value(“UTM Source”, source, “slug”) or source).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Source”, source, “slug”) → source.
- Set \_campaign from (Platform.db.get\_value(“UTM Campaign”, campaign, “slug”) or campaign).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Campaign”, campaign, “slug”) → campaign.
- Set \_medium from (Platform.db.get\_value(“UTM Medium”, medium, “slug”) or medium).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Medium”, medium, “slug”) → medium.
- Return tuple(\_source, \_medium, \_campaign).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L7422) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1083) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1642)

<a id="op-ce63e0950ec70a"></a>
### Parse and map trackers from url

`operation_foundation_utils_data_business_behavior_parse_and_map_trackers_from_resource_address`

**Inputs** url, create = false.

**Declared result** dict.

**Explicit results** map\_trackers(url\_trackers, create).

**Local steps**

- Set query from urlparse(url).query.
- Set url\_trackers from dict(parse\_qsl(query)).
- Return map\_trackers(url\_trackers, create).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0477.json#L7646) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L24)

<a id="op-d5ff3b191eb0da"></a>
### Map trackers

`operation_foundation_utils_data_business_behavior_map_trackers`

**Inputs** url\_trackers, create = false.

**Record and data access** read “UTM Source” via get\_value · read “UTM Source” via exists · read “UTM Medium” via get\_value · read “UTM Medium” via exists · read “UTM Campaign” via get\_value · 1 additional forms in the steps below.

**State and service calls** request new\_doc for “UTM Source” · call save on source · request new\_doc for “UTM Medium” · call save on medium · request new\_doc for “UTM Campaign” · 1 additional forms in the steps below.

**Explicit results** Platform\_trackers.

**Local steps**

- Set Platform\_trackers from mapping().
- If url\_source bound to url\_trackers.get(“utm\_source”, url\_trackers.get(“source”)).
  - Set source from (Platform.db.get\_value(“UTM Source”, mapping(“slug” → slug(url\_source)), “name”) or url\_source).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Source”, mapping(“slug” → slug(url\_source)), “name”) → url\_source.
  - If (create and source equals url\_source and not Platform.db.exists(“UTM Source”, source)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in create → source equals url\_source → not Platform.db.exists(“UTM Source”, source).
    - Set source from Platform.new\_doc(“UTM Source”).
    - Set source.name from url\_source.
    - Set source.description from formatted text Autogenerated from {url\_trackers}.
    - Evaluate source.save(ignore\_permissions = true).
  - Set Platform\_trackers at “utm\_source” from source.
- If url\_medium bound to url\_trackers.get(“utm\_medium”, url\_trackers.get(“medium”)).
  - Set medium from (Platform.db.get\_value(“UTM Medium”, mapping(“slug” → slug(url\_medium)), “name”) or url\_medium).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Medium”, mapping(“slug” → slug(url\_medium)), “name”) → url\_medium.
  - If (create and medium equals url\_medium and not Platform.db.exists(“UTM Medium”, medium)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in create → medium equals url\_medium → not Platform.db.exists(“UTM Medium”, medium).
    - Set medium from Platform.new\_doc(“UTM Medium”).
    - Set medium.name from url\_medium.
    - Set medium.description from formatted text Autogenerated from {url\_trackers}.
    - Evaluate medium.save(ignore\_permissions = true).
  - Set Platform\_trackers at “utm\_medium” from medium.
- If url\_campaign bound to url\_trackers.get(“utm\_campaign”, url\_trackers.get(“campaign”)).
  - Set campaign from (Platform.db.get\_value(“UTM Campaign”, mapping(“slug” → slug(url\_campaign)), “name”) or url\_campaign).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UTM Campaign”, mapping(“slug” → slug(url\_campaign)), “name”) → url\_campaign.
  - If (create and campaign equals url\_campaign and not Platform.db.exists(“UTM Campaign”, campaign)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in create → campaign equals url\_campaign → not Platform.db.exists(“UTM Campaign”, campaign).
    - Set campaign from Platform.new\_doc(“UTM Campaign”).
    - Set campaign.name from url\_campaign.
    - Set campaign.campaign\_description from formatted text Autogenerated from {url\_trackers}.
    - Evaluate campaign.save(ignore\_permissions = true).
  - Set Platform\_trackers at “utm\_campaign” from campaign.
- If url\_content bound to url\_trackers.get(“utm\_content”, url\_trackers.get(“content”)).
  - Set Platform\_trackers at “utm\_content” from url\_content.
- Return Platform\_trackers.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L12)
