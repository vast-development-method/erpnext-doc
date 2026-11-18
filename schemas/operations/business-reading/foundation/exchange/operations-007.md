# Integration and transport · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Discovery

<a id="op-891804eab75b08"></a>
### Doctype methods

`operation_foundation_application_interface_discovery_business_behavior_record_type_methods`

**Inputs** doctype.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“type” → “method\_index”, “doctype” → doctype, “methods” → methods).

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- Set methods from list of \_doctype\_method\_summary(doctype, name, fn) for tuple(name, fn, \_defining\_class) drawn from \_get\_doctype\_methods(doctype).
  - Draw tuple(name, fn, \_defining\_class) from \_get\_doctype\_methods(doctype).
- Return mapping(“type” → “method\_index”, “doctype” → doctype, “methods” → methods).

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L62) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L51)

<a id="op-a8e4881b85d5f2"></a>
### Doctype method

`operation_foundation_application_interface_discovery_business_behavior_record_type_method`

**Inputs** doctype, method.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_doctype\_method\_document(doctype, name, fn, defining\_class).

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Method {0} is not available for discovery on DocType {1}”.format(method, doctype).

**Local steps**

- Evaluate Platform.only\_for(SYSTEM\_USER\_ROLE).
- For each tuple(name, fn, defining\_class) in \_get\_doctype\_methods(doctype).
  - If name equals method.
    - Return \_doctype\_method\_document(doctype, name, fn, defining\_class).
- Call the validation error handler Platform.throw(translated “Method {0} is not available for discovery on DocType {1}”.format(method, doctype), Platform.DoesNotExistError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(SYSTEM\_USER\_ROLE).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L57) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L46)

<a id="op-d45fe43575cb6b"></a>
### Clear cache

`operation_foundation_application_interface_discovery_business_behavior_clear_cache`

**Inputs** user = no value.

**Local steps**

- Evaluate Platform.cache.delete\_keys(formatted text {DISCOVERY\_CACHE\_PREFIX}:).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L6493) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L22)

<a id="op-d2cffc045e1730"></a>
### Build cache

`operation_foundation_application_interface_discovery_business_behavior_build_cache`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Set items from list().
- Set search\_entries from list().
- For each path in \_discover\_whitelisted\_method\_paths().
  - If fn bound to \_get\_whitelisted\_method(path, ignore\_cache = true).
    - Set method from \_method\_summary(fn).
    - Evaluate items.append(method).
    - Set entry from mapping(“type” → “method”, expand method).
    - Evaluate search\_entries.append(mapping(“method” → method, “haystack” → \_method\_search\_text(entry, inspect.getdoc(fn)))).
- Evaluate Platform.cache.set\_value(PYTHON\_METHOD\_CACHE\_KEY, items, expires\_in\_sec = CACHE\_TTL).
- Evaluate Platform.cache.set\_value(PYTHON\_SEARCH\_CACHE\_KEY, search\_entries, expires\_in\_sec = CACHE\_TTL).
- Set doctype\_items from list().
- Set doctype\_search\_entries from list().
- For each tuple(doctype, method\_name, fn, \_defining\_class) in \_discover\_doctype\_methods().
  - Set method from \_doctype\_method\_summary(doctype, method\_name, fn).
  - Evaluate doctype\_items.append(method).
  - Evaluate doctype\_search\_entries.append(mapping(“method” → method, “haystack” → \_method\_search\_text(method, inspect.getdoc(fn)))).
- Evaluate Platform.cache.set\_value(DOCTYPE\_METHOD\_CACHE\_KEY, doctype\_items, expires\_in\_sec = CACHE\_TTL).
- Evaluate Platform.cache.set\_value(DOCTYPE\_SEARCH\_CACHE\_KEY, doctype\_search\_entries, expires\_in\_sec = CACHE\_TTL).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0004.json#L6583) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L31) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L20)

<a id="op-62f50edf730b30"></a>
### Search index

`operation_foundation_application_interface_discovery_business_behavior_search_index`

**Inputs** no declared parameters.

**Declared result** list at tuple at tuple(dict at tuple(str, Any), str).

**Explicit results** sorted(entries, key = deferred anonymous expression).

**Local steps**

- Set entries from list().
- For each item in \_get\_cached\_python\_search\_entries().
  - Set method from item at “method”.
  - Set entry from \_without\_none(mapping(“type” → “method”, expand method, “kind” → “rpc”)).
  - Evaluate entries.append(tuple(entry, formatted text {item at “haystack”} rpc)).
- For each tuple(path, \_script) in \_visible\_server\_scripts().
  - Set entry from mapping(“type” → “method”, “kind” → “rpc”, “path” → path).
  - Evaluate entries.append(tuple(entry, \_method\_search\_text(entry))).
- For each item in \_get\_cached\_doctype\_search\_entries().
  - Set entry from \_without\_none(mapping(expand item at “method”, “kind” → “doctype”)).
  - Evaluate entries.append(tuple(entry, formatted text {item at “haystack”} doctype)).
- Return sorted(entries, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L65) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L54)

<a id="op-c9342f60784c0e"></a>
### Method search text

`operation_foundation_application_interface_discovery_business_behavior_method_search_text`

**Inputs** entry, docstring = no value.

**Declared result** str.

**Explicit results** one space.join(generator of str((value or empty text)) for value drawn from tuple(nested operand in the contract.get(“type”), nested operand in the contract.get(“kind”), nested operand in the contract.get( ….lower().

**Local steps**

- Return one space.join(generator of str((value or empty text)) for value drawn from tuple(nested operand in the contract.get(“type”), nested operand in the contract.get(“kind”), nested operand in the contract.get( ….lower().
  - Draw value from tuple(entry.get(“type”), entry.get(“kind”), entry.get(“path”), entry.get(“doctype”), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L723) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L52) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L41)

<a id="op-331836403dd5c4"></a>
### Method index

`operation_foundation_application_interface_discovery_business_behavior_method_index`

**Inputs** no declared parameters.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** sorted(items, key = deferred anonymous expression).

**Local steps**

- Set items from list of mapping(expand item, “kind” → “rpc”) for item drawn from \_get\_cached\_python\_methods().
  - Draw item from \_get\_cached\_python\_methods().
- Evaluate items.extend(generator of mapping(“kind” → “rpc”, “path” → path) for tuple(path, \_script) drawn from \_visible\_server\_scripts()).
  - Draw tuple(path, \_script) from \_visible\_server\_scripts().
- Evaluate items.extend(generator of mapping(expand item, “kind” → “doctype”) for item drawn from \_doctype\_method\_index()).
  - Draw item from \_doctype\_method\_index().
- Return sorted(items, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1023) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L50) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L39)

<a id="op-ea48c3952177d9"></a>
### Doctype method index

`operation_foundation_application_interface_discovery_business_behavior_record_type_method_index`

**Inputs** no declared parameters.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_get\_required\_cache\_value(DOCTYPE\_METHOD\_CACHE\_KEY).

**Local steps**

- Return \_get\_required\_cache\_value(DOCTYPE\_METHOD\_CACHE\_KEY).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1459) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L60) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L49)

<a id="op-1292e9f764b696"></a>
### Get cached python methods

`operation_foundation_application_interface_discovery_business_behavior_get_cached_implementation_language_methods`

**Inputs** no declared parameters.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_get\_required\_cache\_value(PYTHON\_METHOD\_CACHE\_KEY).

**Local steps**

- Return \_get\_required\_cache\_value(PYTHON\_METHOD\_CACHE\_KEY).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1530) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L37) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L26)

<a id="op-cbc0464d2cf53e"></a>
### Get cached python search entries

`operation_foundation_application_interface_discovery_business_behavior_get_cached_implementation_language_search_entries`

**Inputs** no declared parameters.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_get\_required\_cache\_value(PYTHON\_SEARCH\_CACHE\_KEY).

**Local steps**

- Return \_get\_required\_cache\_value(PYTHON\_SEARCH\_CACHE\_KEY).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1601) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L38) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L27)

<a id="op-7743eb7c295656"></a>
### Get cached doctype search entries

`operation_foundation_application_interface_discovery_business_behavior_get_cached_record_type_search_entries`

**Inputs** no declared parameters.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** \_get\_required\_cache\_value(DOCTYPE\_SEARCH\_CACHE\_KEY).

**Local steps**

- Return \_get\_required\_cache\_value(DOCTYPE\_SEARCH\_CACHE\_KEY).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1672) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L39) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L28)

<a id="op-10ef418266dc88"></a>
### Get required cache value

`operation_foundation_application_interface_discovery_business_behavior_get_required_cache_value`

**Inputs** key.

**Declared result** Any.

**Explicit results** value.

**Explicit failure paths** validation helper with DiscoveryCacheUnavailable — translated “API discovery cache is being generated. Please try again in 10 seconds.”.

**Local steps**

- Set value from Platform.cache.get\_value(key, expires = true).
- If value is identical to no value.
  - Evaluate \_trigger\_cache\_build().
  - Call the validation error handler Platform.throw(translated “API discovery cache is being generated. Please try again in 10 seconds.”, DiscoveryCacheUnavailable).
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L42) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L31)

<a id="op-24090f03a56bb6"></a>
### Trigger cache build

`operation_foundation_application_interface_discovery_business_behavior_trigger_cache_build`

**Inputs** no declared parameters.

**Declared result** no value.

**State and service calls** enqueue with “Platform.api.discovery.build\_cache”.

**Local steps**

- Evaluate Platform.enqueue(“Platform.api.discovery.build\_cache”, queue = “long”, job\_id = DISCOVERY\_BUILD\_JOB\_ID, deduplicate = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.api.discovery.build\_cache”, queue = “long”, job\_id = DISCOVERY\_BUILD\_JOB\_ID, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L1912) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L66) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L55)

<a id="op-79ce07e1223e58"></a>
### Method summary

`operation_foundation_application_interface_discovery_business_behavior_method_summary`

**Inputs** fn.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_without\_none(mapping(“kind” → “rpc”, “path” → formatted text {fn.\_\_module\_\_}.{fn.\_\_name\_\_}, “description” → docstring.splitlines() at 0 when docstring, otherwise no value)).

**Local steps**

- Set docstring from inspect.getdoc(fn).
- Return \_without\_none(mapping(“kind” → “rpc”, “path” → formatted text {fn.\_\_module\_\_}.{fn.\_\_name\_\_}, “description” → docstring.splitlines() at 0 when docstring, otherwise no value)).
  - Value choice on docstring — true gives docstring.splitlines() at 0, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L2031) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L54) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L43)

<a id="op-2e9e43c3d026c7"></a>
### Method document

`operation_foundation_application_interface_discovery_business_behavior_method_document`

**Inputs** path, fn.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_without\_none(mapping(“type” → “method”, “kind” → “rpc”, “path” → path, “name” → fn.\_\_name\_\_, …)).

**Local steps**

- Return \_without\_none(mapping(“type” → “method”, “kind” → “rpc”, “path” → path, “name” → fn.\_\_name\_\_, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L2247) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L49) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L38)

<a id="op-19b40b1ecf4b81"></a>
### Doctype method summary

`operation_foundation_application_interface_discovery_business_behavior_record_type_method_summary`

**Inputs** doctype, method, fn.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_without\_none(mapping(“type” → “method”, “kind” → “doctype”, “doctype” → doctype, “method” → method, …)).

**Local steps**

- Set docstring from inspect.getdoc(fn).
- Return \_without\_none(mapping(“type” → “method”, “kind” → “doctype”, “doctype” → doctype, “method” → method, …)).
  - Value choice on docstring — true gives docstring.splitlines() at 0, false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L2584) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L61) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L50)

<a id="op-9294becc567a0a"></a>
### Doctype method document

`operation_foundation_application_interface_discovery_business_behavior_record_type_method_document`

**Inputs** doctype, method, fn, defining\_class.

**Declared result** dict at tuple(str, Any).

**Explicit results** \_without\_none(mapping(“type” → “method”, “kind” → “doctype”, “doctype” → doctype, “method” → method, …)).

**Local steps**

- Set http\_methods from list of method for method drawn from Platform.allowed\_http\_methods\_for\_whitelisted\_func.get(fn, tuple()) where method belongs to set(“GET”, “POST”).
  - Draw method from Platform.allowed\_http\_methods\_for\_whitelisted\_func.get(fn, tuple()), keep a combination only if (method belongs to set(“GET”, “POST”)).
- Return \_without\_none(mapping(“type” → “method”, “kind” → “doctype”, “doctype” → doctype, “method” → method, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L2831) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L59) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L48)

<a id="op-ac3943799d5a5a"></a>
### Class path

`operation_foundation_application_interface_discovery_business_behavior_class_path`

**Inputs** class\_.

**Declared result** str.

**Explicit results** formatted text {class\_.\_\_module\_\_}.{class\_.\_\_name\_\_}.

**Local steps**

- Return formatted text {class\_.\_\_module\_\_}.{class\_.\_\_name\_\_}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L3302) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L32) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L21)

<a id="op-75e52ea7c380ef"></a>
### Method source

`operation_foundation_application_interface_discovery_business_behavior_method_source`

**Inputs** fn.

**Declared result** (str bitwise or no value).

**Explicit results** no value · inspect.getsource(fn).

**Local steps**

- Set app from fn.\_\_module\_\_.split(“.”, 1) at 0.
- If not any(Platform.get\_hooks(“expose\_discovery\_source”, app\_name = app)).
  - Return no value.
- Attempt the following.
  - Return inspect.getsource(fn).
- On failure (tuple(OSError, TypeError)).
  - Return no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“expose\_discovery\_source”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L3381) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L53) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L42)

<a id="op-09b272181e2580"></a>
### Visible server scripts

`operation_foundation_application_interface_discovery_business_behavior_visible_server_scripts`

**Inputs** no declared parameters.

**Declared result** list at tuple at tuple(str, str).

**Record and data access** read “Server Script” via get\_list.

**Explicit results** list() · sorted(generator of tuple(paths at script, script) for script drawn from permitted).

**Local steps**

- If not Platform.has\_permission(“Server Script”, “read”).
  - Return list().
- Set scripts from \_get\_api\_server\_scripts().
- If not scripts.
  - Return list().
- Set paths from mapping of script → path for tuple(path, script) drawn from scripts.items().
  - Draw tuple(path, script) from scripts.items().
- Set permitted from Platform.get\_list(“Server Script”, filters = mapping(“name” → tuple(“in”, list(paths))), pluck = “name”, limit\_page\_length = 0).
- Return sorted(generator of tuple(paths at script, script) for script drawn from permitted).
  - Draw script from permitted.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Server Script”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L68) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L57)

<a id="op-5b23b2c3c30c14"></a>
### Get api server scripts

`operation_foundation_binding_foundation_api_discovery_get_api_server_scripts`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping of path → script for tuple(path, script) drawn from get\_server\_script\_map().get(“\_api”, mapping()).items() where (isinstance(path, str) and path).

**Local steps**

- Return mapping of path → script for tuple(path, script) drawn from get\_server\_script\_map().get(“\_api”, mapping()).items() where (isinstance(path, str) and path).
  - Draw tuple(path, script) from get\_server\_script\_map().get(“\_api”, mapping()).items(), keep a combination only if ((isinstance(path, str) and path)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(path, str) → path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L260)

<a id="op-72c60a6f191932"></a>
### Get whitelisted method

`operation_foundation_application_interface_discovery_business_behavior_get_whitelisted_method`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** path, ignore\_cache.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L3821) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L43) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L32)

<a id="op-13923e5d4d9cb8"></a>
### Discover doctype methods

`operation_foundation_application_interface_discovery_business_behavior_discover_record_type_methods`

**Inputs** no declared parameters.

**Declared result** list at tuple at tuple(str, str, Callable, type).

**Record and data access** read “DocType” via get\_all.

**Explicit results** methods.

**Local steps**

- Set methods from list().
- Set doctypes from Platform.get\_all(“DocType”, filters = mapping(“istable” → 0), pluck = “name”, order\_by = “name”).
- For each doctype in doctypes.
  - Attempt the following.
    - Set doctype\_methods from \_get\_doctype\_methods(doctype).
  - On failure (Exception).
    - Continue with the next iteration or loop test.
  - Evaluate methods.extend(generator of tuple(doctype, method\_name, fn, defining\_class) for tuple(method\_name, fn, defining\_class) drawn from doctype\_methods where not \_is\_standard\_doctype\_method(defining\_class)).
    - Draw tuple(method\_name, fn, defining\_class) from doctype\_methods, keep a combination only if (not \_is\_standard\_doctype\_method(defining\_class)).
- Return methods.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L4116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L35) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L24)

<a id="op-774c400638ab38"></a>
### Get doctype methods

`operation_foundation_application_interface_discovery_business_behavior_get_record_type_methods`

**Inputs** doctype.

**Declared result** list at tuple at tuple(str, Callable, type).

**Explicit results** methods.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “DocType {0} is not available for discovery”.format(doctype).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If meta.istable.
  - Call the validation error handler Platform.throw(translated “DocType {0} is not available for discovery”.format(doctype), Platform.DoesNotExistError).
- Set controller from get\_controller(doctype).
- Set methods from list().
- For each method\_name in dir(controller).
  - Set defining\_class from \_defining\_class(controller, method\_name).
  - If not defining\_class.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set fn from \_unwrap\_method(getattr(controller, method\_name)).
  - On failure (tuple(AttributeError, TypeError)).
    - Continue with the next iteration or loop test.
  - If not callable(fn).
    - Continue with the next iteration or loop test.
  - If (fn does not belong to Platform.whitelisted or not \_doctype\_method\_applies(meta, method\_name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fn does not belong to Platform.whitelisted → not \_doctype\_method\_applies(meta, method\_name).
    - Continue with the next iteration or loop test.
  - Evaluate methods.append(tuple(method\_name, fn, defining\_class)).
- Return methods.

**Values supplied outside this operation** selected callable from get\_controller(doctype), getattr(controller, method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L4447) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L41) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L30)
