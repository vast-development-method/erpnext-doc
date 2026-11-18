# Shared value and file services · operations 57

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-d33401305a74df"></a>
### Parse addr

`operation_foundation_utils_initialize_business_behavior_parse_addr`

**Inputs** email\_string.

**Explicit results** tuple(name, email) · tuple(no value, email).

**Local steps**

- Set tuple(name, email) from parseaddr(email\_string).
- If check\_format(email).
  - Set name from get\_name\_from\_email\_string(email\_string, email, name).
  - Return tuple(name, email).
- Otherwise.
  - Set email\_list from EMAIL\_STRING\_PATTERN.findall(email\_string).
  - If (len(email\_list) &gt; 0 and check\_format(email\_list at 0)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(email\_list) &gt; 0 → check\_format(email\_list at 0).
    - Set email from email\_list at 0.
    - Set name from get\_name\_from\_email\_string(email\_string, email, name).
    - Return tuple(name, email).
- Return tuple(no value, email).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L994) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L265)

<a id="op-876d8806ec8992"></a>
### Check format

`operation_foundation_utils_initialize_business_behavior_check_format`

**Inputs** email\_id.

**Explicit results** is\_valid.

**Local steps**

- Set is\_valid from false.
- Attempt the following.
  - Set pos from email\_id.rindex(“@”).
  - Set is\_valid from (pos &gt; 0 and email\_id.rindex(“.”) &gt; pos and (len(email\_id) − pos) &gt; 4).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pos &gt; 0 → email\_id.rindex(“.”) &gt; pos → (len(email\_id) − pos) &gt; 4.
- On failure (Exception).
  - Take no action here.
- Return is\_valid.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L1314) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L205)

<a id="op-025843cdf91491"></a>
### Get name from email string

`operation_foundation_utils_initialize_business_behavior_get_name_from_email_string`

**Inputs** email\_string, email\_id, name.

**Explicit results** name.

**Local steps**

- Set name from email\_string.replace(email\_id, empty text).
- Set name from EMAIL\_NAME\_PATTERN.sub(empty text, name).strip().
- If not name.
  - Set name from email\_id.
- Return name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L1515) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L234)

<a id="op-f2ef08839d679b"></a>
### Get installed apps info

`operation_foundation_utils_initialize_business_behavior_get_installed_apps_info`

**Inputs** no declared parameters.

**Explicit results** out.

**Local steps**

- Set out from list().
- Bind dependencies get\_versions.
- Evaluate out.extend(generator of mapping(“app\_name” → app, “version” → (version\_details.get(“branch\_version”) or version\_details.get(“version”)), “branch” → version\_details.get(“branch”)) for tuple(app, version\_det ….
  - Draw tuple(app, version\_details) from get\_versions().items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in version\_details.get(“branch\_version”) → version\_details.get(“version”).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L128) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L233)

<a id="op-46118eafd02381"></a>
### Get site info

`operation_foundation_utils_initialize_business_behavior_get_site_info`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_all · read “Activity Log” via get\_all.

**Explicit results** orjson.loads(Platform.as\_json(site\_info)).

**Local steps**

- Bind dependencies get\_emails\_sent\_this\_month.
- Bind dependencies get\_system\_managers.
- Set users from Platform.get\_all(“User”, filters = mapping(“user\_type” → “System User”, “name” → tuple(“not in”, Platform.STANDARD\_USERS)), fields = list(“name”, “enabled”, “last\_login”, “last\_active”, …)).
- Set system\_managers from get\_system\_managers(only\_name = true).
- For each u in users.
  - Set u.is\_system\_manager from 1 when u.name belongs to system\_managers, otherwise 0.
    - Value choice on u.name belongs to system\_managers — true gives 1, false gives 0.
  - Set u.full\_name from get\_fullname(u.name).
  - Set u.email from u.name.
  - Remove u at “name”.
- Set system\_settings from Platform.db.get\_singles\_dict(“System Settings”).
- Set space\_usage from Platform.\_dict((nested operand in the contract.local.conf.limits or mapping()).get(“space\_usage”, mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.limits → mapping().
- Set kwargs from mapping(“fields” → list(“user”, “creation”, “full\_name”), “filters” → mapping(“operation” → “Login”, “status” → “Success”), “limit” → 10).
- Set site\_info from mapping(“installed\_apps” → get\_installed\_apps\_info(), “users” → users, “country” → system\_settings.country, “language” → (system\_settings.language or “english”), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in system\_settings.language → “english”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in space\_usage.total → 0.
- For each method\_name in Platform.get\_hooks(“get\_site\_info”).
  - Evaluate site\_info.update((Platform.get\_attr(method\_name)(site\_info) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method\_name)(site\_info) → mapping().
- Return orjson.loads(Platform.as\_json(site\_info)).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_site\_info”), Platform.get\_attr(method\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L1917) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L241)

<a id="op-d9a2fddbe80b52"></a>
### Get db count

`operation_foundation_utils_initialize_business_behavior_get_database_count`

**Inputs** remaining positional values args.

**Record and data access** read doctype via count.

**Explicit results** orjson.loads(Platform.as\_json(db\_count)).

**Local steps**

- Set db\_count from mapping().
- For each doctype in args.
  - Set db\_count at doctype from Platform.db.count(doctype).
- Return orjson.loads(Platform.as\_json(db\_count)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L2964) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L219)

<a id="op-9ddca07de9b5db"></a>
### Call

`operation_foundation_utils_initialize_business_behavior_call`

**Inputs** fn, remaining positional values args, remaining named values kwargs.

**Explicit results** orjson.loads(Platform.as\_json(Platform.call(fn, expanded args, expanded names kwargs))).

**Local steps**

- Return orjson.loads(Platform.as\_json(Platform.call(fn, expanded args, expanded names kwargs))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L3100) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L194)

<a id="op-0977c82fb09129"></a>
### Get safe filters

`operation_foundation_utils_initialize_business_behavior_get_safe_filters`

**Inputs** filters.

**Explicit results** filters · parsed.

**Local steps**

- Attempt the following.
  - Set parsed from orjson.loads(filters).
- On failure (tuple(TypeError, ValueError)).
  - Return filters.
- If (isinstance(parsed, (int bitwise or float)) and not isinstance(parsed, bool)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(parsed, (int bitwise or float)) → not isinstance(parsed, bool).
  - Return filters.
- Return parsed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L3212) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L238)

<a id="op-114416838ee9a8"></a>
### Create batch

`operation_foundation_utils_initialize_business_behavior_create_batch`

**Inputs** iterable, size.

**Declared result** Generator at Iterable.

**Local steps**

- Set total\_count from len(iterable).
- For each i in range(0, total\_count, size).
  - yield iterable at slice i to min((i + size), total\_count).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L126) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L206)

<a id="op-9af06e86214344"></a>
### Set request

`operation_foundation_utils_initialize_business_behavior_set_request`

**Inputs** remaining named values kwargs.

**Local steps**

- Bind dependencies EnvironBuilder.
- Bind dependencies Request.
- Set builder from EnvironBuilder(expanded names kwargs).
- Set Platform.local.request from Request(builder.get\_environ()).

If control reaches the end, it returns no value.

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L3604) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L272)

<a id="op-80992c62138800"></a>
### Get html for route

`operation_foundation_utils_initialize_business_behavior_get_document_markup_for_route`

**Inputs** route.

**Explicit results** Platform.safe\_decode(response.get\_data()).

**Local steps**

- Bind dependencies get\_response.
- Evaluate set\_request(method = “GET”, path = route).
- Set response from get\_response().
- Return Platform.safe\_decode(response.get\_data()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L3726) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L222)

<a id="op-ef5af4356e4d5b"></a>
### Get file size

`operation_foundation_utils_initialize_business_behavior_get_file_size`

**Inputs** path, format = false.

**Explicit results** num · formatted text {num}{unit}{suffix} · “{:.1f}{}{}”.format(num, “Yi”, suffix).

**Local steps**

- Set num from os.path.getsize(path).
- If not format.
  - Return num.
- Set suffix from “B”.
- For each unit in list(empty text, “Ki”, “Mi”, “Gi”, …).
  - If abs(num) &lt; 1024.
    - Return formatted text {num}{unit}{suffix}.
  - Update num using ÷ 1024.
- Return “{:.1f}{}{}”.format(num, “Yi”, suffix).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L3857) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L225)

<a id="op-6e37901b93315e"></a>
### Get build version

`operation_foundation_utils_initialize_business_behavior_get_build_version`

**Inputs** no declared parameters.

**Explicit results** str(os.path.getmtime(os.path.join(Platform.local.sites\_path, “assets/assets.json”))) · Platform.utils.random\_string(8).

**Local steps**

- Attempt the following.
  - Return str(os.path.getmtime(os.path.join(Platform.local.sites\_path, “assets/assets.json”))).
- On failure (OSError).
  - Return Platform.utils.random\_string(8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L4138) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L218)

<a id="op-808cc90bdb44c2"></a>
### Get assets json

`operation_foundation_utils_initialize_business_behavior_get_assets_structured_data`

**Inputs** no declared parameters.

**Explicit results** Platform.client\_cache.get\_value(“assets\_json”, shared = true, generator = \_get\_assets) · \_get\_assets().

**Local steps**

- Bind local operation \_get\_assets for subsequent calls.
- If not Platform.conf.developer\_mode.
  - Return Platform.client\_cache.get\_value(“assets\_json”, shared = true, generator = \_get\_assets).
- Otherwise.
  - Return \_get\_assets().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L4279) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L215)

<a id="op-381f91bf6764c5"></a>
### Get assets json.get assets

`operation_foundation_utils_initialize_business_behavior_get_assets_structured_data_get_assets`

**Inputs** no declared parameters.

**Explicit results** assets.

**Local steps**

- Set assets from Platform.parse\_json(Platform.read\_file(“assets/assets.json”)).
- If assets\_rtl bound to Platform.read\_file(“assets/assets-rtl.json”).
  - Evaluate assets.update(Platform.parse\_json(assets\_rtl)).
- Return assets.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L4519) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L216)

<a id="op-b887d0414e6c1d"></a>
### Get bench relative path

`operation_foundation_utils_initialize_business_behavior_get_site_management_relative_path`

**Inputs** file\_path.

**Explicit results** os.path.abspath(file\_path).

**Local steps**

- If not os.path.exists(file\_path).
  - Set base\_path from “..”.
- Otherwise.
  - If file\_path.startswith(os.sep).
    - Set base\_path from os.sep.
  - Otherwise.
    - Set base\_path from “.”.
- Set file\_path from os.path.join(base\_path, file\_path).
- If not os.path.exists(file\_path).
  - Evaluate print(formatted text Invalid path {file\_path at slice 3 to no value}).
  - Evaluate sys.exit(1).
- Return os.path.abspath(file\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L4664) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L244)

<a id="op-65afc07b5e0892"></a>
### Groupby metric

`operation_foundation_utils_initialize_business_behavior_groupby_metric`

**Inputs** iterable, key.

**Explicit results** records.

**Local steps**

- Set records from mapping().
- For each tuple(category, items) in iterable.items().
  - If items.
    - For each item in items.
      - Evaluate records.setdefault(item at key, mapping()).setdefault(category, list()).append(item).
- Return records.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L4975) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L254)

<a id="op-6ade2351e5ac62"></a>
### Get table name

`operation_foundation_utils_initialize_business_behavior_get_table_name`

**Inputs** table\_name, wrap\_in\_backticks = false.

**Declared result** str.

**Explicit results** formatted text ′{name}′ · name.

**Local steps**

- Set name from formatted text tab{table\_name} when not table\_name.startswith(“\_\_”), otherwise table\_name.
  - Value choice on not table\_name.startswith(“\_\_”) — true gives formatted text tab{table\_name}, false gives table\_name.
- If wrap\_in\_backticks.
  - Return formatted text ′{name}′.
- Return name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L129) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L249)

<a id="op-5d91560c7d5794"></a>
### Squashify

`operation_foundation_utils_initialize_business_behavior_squashify`

**Inputs** what.

**Explicit results** what at 0 · what.

**Local steps**

- If (isinstance(what, Sequence) and len(what) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(what, Sequence) → len(what) equals 1.
  - Return what at 0.
- Return what.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L5383) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L274)

<a id="op-6b2db358f6d95d"></a>
### Safe json loads

`operation_foundation_utils_initialize_business_behavior_safe_structured_data_loads`

**Inputs** remaining positional values args.

**Explicit results** squashify(results).

**Local steps**

- Set results from list().
- For each arg in args.
  - Attempt the following.
    - Set arg from orjson.loads(arg).
  - On failure (Exception).
    - Take no action here.
  - Evaluate results.append(arg).
- Return squashify(results).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L5495) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L269)

<a id="op-78cb4f6c4d3a8d"></a>
### Dictify

`operation_foundation_utils_initialize_business_behavior_dictify`

**Inputs** arg.

**Explicit results** arg.

**Local steps**

- If isinstance(arg, MutableSequence).
  - For each tuple(i, a) in enumerate(arg).
    - Set arg at i from dictify(a).
- Otherwise.
  - If isinstance(arg, MutableMapping).
    - Set arg from Platform.\_dict(arg).
- Return arg.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L5649) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L209)

<a id="op-689f2cd529f3e9"></a>
### Add user info

`operation_foundation_utils_initialize_business_behavior_add_user_info`

**Inputs** user, user\_info.

**Declared result** no value.

**Record and data access** read “User” via get\_all.

**Explicit results** no value.

**Local steps**

- If not user.
  - Return no value.
- If isinstance(user, str).
  - Set user from list(user).
- Set missing\_users from list of u for u drawn from user where u does not belong to user\_info.
  - Draw u from user, keep a combination only if (u does not belong to user\_info).
- If not missing\_users.
  - Return no value.
- Set missing\_info from Platform.get\_all(“User”, mapping(“name” → tuple(“in”, missing\_users)), list(“full\_name”, “user\_image”, “name”, “email”, …)).
- For each info in missing\_info.
  - Evaluate user\_info.setdefault(info.name, Platform.\_dict()).update(fullname = (info.full\_name or info.name), image = info.user\_image, name = info.name, email = info.email, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in info.full\_name → info.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L5839) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L193)

<a id="op-7430116379b214"></a>
### Is git url

`operation_foundation_utils_initialize_business_behavior_is_goods_in_transit_resource_address`

**Inputs** url.

**Declared result** bool.

**Explicit results** bool(re.match(pattern, url)).

**Local steps**

- Set pattern from “(?:git\|ssh\|https?\|\\w\*@&#91;-\\w.&#93;+):(\\/\\/)?(.\*?)(\\.git)?(\\/?\|\\#&#91;-\\d\\w.\_&#93;+?)$”.
- Return bool(re.match(pattern, url)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6342) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L257)

<a id="op-514d490055f396"></a>
### Callback Manager.initialize

`operation_foundation_utils_initialize_business_behavior_callback_manager_initialize`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.\_functions from deque().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6432) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L200)
