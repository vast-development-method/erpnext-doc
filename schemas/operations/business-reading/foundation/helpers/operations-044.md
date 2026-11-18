# Shared value and file services · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Redis wrapper

<a id="op-6813b8ddfe6257"></a>
### Client Cache.set value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_set_value`

**Inputs** self, key, val, shared (named only, default false).

**Explicit results** no value.

**Local steps**

- Set key from self.redis.make\_key(key, shared = shared).
- Set size from self.redis.set\_value(key, val, shared = true).
- If not self.healthy.
  - Return no value.
- Evaluate self.ensure\_max\_size().
- Within self.lock.
  - Evaluate self.\_put(key, val, (time.monotonic() + self.local\_ttl), size).
- Set \_ from self.redis.get\_value(key, shared = true, use\_local\_cache = not self.healthy).

If control reaches the end, it returns no value.

**Methods declared on this owner** [ensure max size](operations-044.md#op-b7b3c2d2566952), [put](operations-044.md#op-5cf32302afb9a6).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L7565) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L711)

<a id="op-275cd4f19225b7"></a>
### Client Cache.get doc

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_get_record`

**Inputs** self, doctype, name = no value.

**Explicit results** self.get\_value(key, generator = deferred anonymous expression).

**Local steps**

- If not name.
  - Set name from doctype.
- Set key from Platform.get\_document\_cache\_key(doctype, name).
- Return self.get\_value(key, generator = deferred anonymous expression).

**Methods declared on this owner** [get value](operations-043.md#op-2038b27974579d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L7897) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L702)

<a id="op-b7b3c2d2566952"></a>
### Client Cache.ensure max size

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_ensure_maximum_size`

**Inputs** self.

**Local steps**

- If len(self.cache) ≥ self.maxsize.
  - Within self.lock, suppress(RuntimeError).
    - Evaluate self.\_pop(next(iter(self.cache))).
- If (self.maxsize\_bytes and self.\_total\_size &gt; self.maxsize\_bytes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.maxsize\_bytes → self.\_total\_size &gt; self.maxsize\_bytes.
  - Within self.lock, suppress(RuntimeError).
    - While (self.\_total\_size &gt; self.maxsize\_bytes and self.cache).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_total\_size &gt; self.maxsize\_bytes → self.cache.
      - Evaluate self.\_pop(next(iter(self.cache))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pop](operations-044.md#op-a8d864b8b50b1f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L699)

<a id="op-70e0ec46137408"></a>
### Client Cache.delete value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_delete_value`

**Inputs** self, key, shared (named only, default false).

**Local steps**

- Set key from self.redis.make\_key(key, shared = shared).
- Evaluate self.redis.delete\_value(key, shared = true).
- Within self.lock.
  - Evaluate self.\_pop(key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pop](operations-044.md#op-a8d864b8b50b1f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L354) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L698)

<a id="op-25ba58d98c15b2"></a>
### Client Cache.delete keys

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_delete_keys`

**Inputs** self, pattern.

**Local steps**

- Set keys from self.redis.get\_keys(pattern).
- Evaluate self.redis.delete\_value(keys, shared = true, make\_keys = false).
- Within self.lock.
  - For each key in keys.
    - Evaluate self.\_pop(key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pop](operations-044.md#op-a8d864b8b50b1f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L530) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L697)

<a id="op-a1a468b0363e95"></a>
### Client Cache.run invalidator thread

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_run_invalidator_thread`

**Inputs** self.

**Explicit results** self.\_watcher.run\_in\_thread(sleep\_time = 60, daemon = true, exception\_handler = self.\_exception\_handler).

**Local steps**

- Set self.\_watcher from self.invalidator.pubsub().
- Evaluate self.\_watcher.subscribe(expanded names mapping(“\_\_redis\_\_:invalidate” → self.\_handle\_invalidation, “clear\_persistent\_cache” → self.\_handle\_persistent\_cache\_invalidation)).
- Return self.\_watcher.run\_in\_thread(sleep\_time = 60, daemon = true, exception\_handler = self.\_exception\_handler).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L709) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L710)

<a id="op-e94b5d802fd14d"></a>
### Client Cache.erase persistent caches

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_erase_persistent_caches`

**Inputs** self, doctype (named only, default no value).

**Local steps**

- Attempt the following.
  - Evaluate self.redis.publish(“clear\_persistent\_cache”, json.dumps(mapping(“doctype” → doctype, “site” → Platform.local.site))).
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L888) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L700)

<a id="op-a5c8e042693c07"></a>
### Client Cache.handle invalidation

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_handle_invalidation`

**Inputs** self, message.

**Explicit results** no value.

**Local steps**

- If message at “data” is identical to no value.
  - Evaluate self.clear\_cache().
  - Return no value.
- Within self.lock.
  - For each key in message at “data”.
    - Evaluate self.\_pop(key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-044.md#op-5ad5118ba549b5), [pop](operations-044.md#op-a8d864b8b50b1f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L1043) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L704)

<a id="op-aaff10ac5a62eb"></a>
### Client Cache.handle persistent cache invalidation

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_handle_persistent_cache_invalidation`

**Inputs** self, message.

**Explicit results** no value.

**Local steps**

- Bind dependencies Platform.utils.caching.
- Bind dependencies clear\_controller\_cache.
- If message at “type” differs from “message”.
  - Return no value.
- Set payload from Platform.\_dict(json.loads(message at “data”)).
- Evaluate clear\_controller\_cache(payload.doctype, site = payload.site).
- If not payload.doctype.
  - Evaluate Platform.utils.caching.\_SITE\_CACHE.clear().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L1213) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L705)

<a id="op-fb98a9c1c37ce7"></a>
### Client Cache.exception handler

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_exception_handler`

**Inputs** self, exc, pubsub, pubsub\_thread.

**Explicit failure paths** propagate active failure.

**Local steps**

- If isinstance(exc, redis.exceptions.ConnectionError).
  - Evaluate self.clear\_cache().
  - Update self.connection\_retries using + 1.
  - If self.connection\_retries &gt; 10.
    - Set self.healthy from false.
    - Propagate the active failure.
  - Evaluate time.sleep(1).
- Otherwise.
  - Set self.healthy from false.
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cache](operations-044.md#op-5ad5118ba549b5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L1458) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L701)

<a id="op-5ad5118ba549b5"></a>
### Client Cache.clear cache

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_clear_cache`

**Inputs** self.

**Local steps**

- Within self.lock.
  - Evaluate self.\_clear().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear](operations-044.md#op-3bd6c5fcc788ea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L1687) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L696)

<a id="op-dcbba1d607c8b3"></a>
### Client Cache.statistics

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_statistics`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** CacheStatistics.

**Explicit results** CacheStatistics(hits = self.hits, misses = self.misses, capacity = self.maxsize, used = len(self.cache), …).

**Local steps**

- Return CacheStatistics(hits = self.hits, misses = self.misses, capacity = self.maxsize, used = len(self.cache), …).
  - Value choice on self.hits — true gives round((self.hits ÷ (self.hits + self.misses)), 2), false gives no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L1759) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L712)

<a id="op-9fd17bab16e4f0"></a>
### Client Cache.reset statistics

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_reset_statistics`

**Inputs** self.

**Local steps**

- Set self.hits, self.misses from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L2007) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L709)

<a id="op-5cf32302afb9a6"></a>
### Client Cache.put

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_put`

**Inputs** self, key, value, expiry, size.

**Local steps**

- Set old from self.cache.get(key).
- If old is distinct from no value.
  - Update self.\_total\_size using − old.size.
- Set self.cache at key from CachedValue(value = value, expiry = expiry, size = size).
- Update self.\_total\_size using + size.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L2062) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L708)

<a id="op-a8d864b8b50b1f"></a>
### Client Cache.pop

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_post_office_protocol`

**Inputs** self, key.

**Local steps**

- Set entry from self.cache.pop(key, no value).
- If entry is distinct from no value.
  - Update self.\_total\_size using − entry.size.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L2270) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L707)

<a id="op-3bd6c5fcc788ea"></a>
### Client Cache.clear

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_clear`

**Inputs** self.

**Local steps**

- Evaluate self.cache.clear().
- Set self.\_total\_size from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L2385) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L695)

## Service · Response

<a id="op-88bfb516b15175"></a>
### Report error

`operation_foundation_utils_response_business_behavior_report_error`

**Inputs** status\_code.

**Explicit results** response.

**Local steps**

- Bind dependencies ApiVersion, get\_api\_version.
- Set allow\_traceback from (is\_traceback\_allowed() and (status\_code differs from 404 or Platform.conf.logging)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_traceback\_allowed() → (status\_code differs from 404 or Platform.conf.logging).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status\_code differs from 404 → Platform.conf.logging.
- Set traceback from Platform.utils.get\_traceback().
- Set tuple(exc\_type, exc\_value, \_) from sys.exc\_info().
- Select the first matching pattern against get\_api\_version().
  - Pattern ApiVersion.V1.
    - If allow\_traceback.
      - Evaluate Platform.errprint(traceback).
      - Set Platform.response.exception from traceback.splitlines() at negative 1.
    - Set Platform.response at “exc\_type” from exc\_type.\_\_name\_\_.
  - Pattern ApiVersion.V2.
    - Set error\_log from mapping(“type” → exc\_type.\_\_name\_\_).
    - If allow\_traceback.
      - Evaluate print(traceback).
      - Set error\_log at “exception” from traceback.
    - Evaluate \_link\_error\_with\_message\_log(error\_log, exc\_value, Platform.message\_log).
    - Set Platform.local.response.errors from list(error\_log).
- Set response from build\_response(“json”).
- Set response.status\_code from status\_code.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L62) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L552)

<a id="op-d0f2e120b891c3"></a>
### Is traceback allowed

`operation_foundation_utils_response_business_behavior_is_traceback_allowed`

**Inputs** no declared parameters.

**Explicit results** (Platform.db and (Platform.\_dev\_server or (Platform.get\_system\_settings(“allow\_error\_traceback”) and not nested operand in the contract.local.flags.disable\_traceback and is\_system\_user()))).

**Local steps**

- Bind dependencies is\_system\_user.
- Return (Platform.db and (Platform.\_dev\_server or (Platform.get\_system\_settings(“allow\_error\_traceback”) and not nested operand in the contract.local.flags.disable\_traceback and is\_system\_user()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db → (Platform.\_dev\_server or (Platform.get\_system\_settings(“allow\_error\_traceback”) and not Platform.local.flags.disable\_traceback and is\_system\_user())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.\_dev\_server → (Platform.get\_system\_settings(“allow\_error\_traceback”) and not Platform.local.flags.disable\_traceback and is\_system\_user()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_system\_settings(“allow\_error\_traceback”) → not Platform.local.flags.disable\_traceback → is\_system\_user().

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“allow\_error\_traceback”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L3016) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L546)

<a id="op-917a92b654b5e2"></a>
### Link error with message log

`operation_foundation_utils_response_business_behavior_link_error_with_message_log`

**Inputs** error\_log, exception, message\_logs.

**Explicit results** no value.

**Local steps**

- For each message in list(message\_logs).
  - If message.get(“\_\_Platform\_exc\_id”) equals getattr(exception, “\_\_Platform\_exc\_id”, no value).
    - Evaluate error\_log.update(message).
    - Evaluate message\_logs.remove(message).
    - Evaluate error\_log.pop(“raise\_exception”, no value).
    - Evaluate error\_log.pop(“\_\_Platform\_exc\_id”, no value).
    - Return no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(exception, “\_\_Platform\_exc\_id”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L3142) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L547)

<a id="op-8e22162d448681"></a>
### Build response

`operation_foundation_utils_response_business_behavior_build_response`

**Inputs** response\_type = no value.

**Explicit results** response\_type\_map at (Platform.response.get(“type”) or response\_type)().

**Local steps**

- If (“docs” belongs to Platform.local.response and not Platform.local.response.docs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “docs” belongs to Platform.local.response → not Platform.local.response.docs.
  - Remove Platform.local.response at “docs”.
- Set response\_type\_map from mapping(“csv” → as\_csv, “txt” → as\_txt, “download” → as\_raw, “json” → as\_json, …).
- Return response\_type\_map at (Platform.response.get(“type”) or response\_type)().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.response.get(“type”) → response\_type.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L3374) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L542)

<a id="op-3b570b201dc75e"></a>
### As csv

`operation_foundation_utils_response_business_behavior_as_comma_separated_values`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.mimetype from “text/csv”.
- Set filename from formatted text {Platform.response at “doctype”}.csv.
- Set filename from filename.encode(“utf-8”).decode(“unicode-escape”, “ignore”).
- Evaluate response.headers.add(“Content-Disposition”, “attachment”, filename = filename).
- Set response.data from Platform.response at “result”.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L3656) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L536)

<a id="op-401fa2537fadf2"></a>
### As txt

`operation_foundation_utils_response_business_behavior_as_text_resource`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.mimetype from “text”.
- Set filename from formatted text {Platform.response at “doctype”}.txt.
- Set filename from filename.encode(“utf-8”).decode(“unicode-escape”, “ignore”).
- Evaluate response.headers.add(“Content-Disposition”, “attachment”, filename = filename).
- Set response.data from Platform.response at “result”.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L3896) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L541)

<a id="op-4c7aa6e6bbf46f"></a>
### As raw

`operation_foundation_utils_response_business_behavior_as_raw`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.mimetype from (Platform.response.get(“content\_type”) or mimetypes.guess\_type(Platform.response at “filename”) at 0 or “application/unknown”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.response.get(“content\_type”) → mimetypes.guess\_type(Platform.response at “filename”) at 0 → “application/unknown”.
- Set filename from Platform.response at “filename”.encode(“utf-8”).decode(“unicode-escape”, “ignore”).
- Evaluate response.headers.add(“Content-Disposition”, Platform.response.get(“display\_content\_as”, “attachment”), filename = filename).
- Set response.data from Platform.response at “filecontent”.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L4136) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L539)

<a id="op-c97c1d15318e4d"></a>
### As json

`operation_foundation_utils_response_business_behavior_as_structured_data`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Evaluate make\_logs().
- Set response from Response().
- If Platform.local.response.http\_status\_code.
  - Set response.status\_code from Platform.local.response at “http\_status\_code”.
  - Remove Platform.local.response at “http\_status\_code”.
- Set response.mimetype from “application/json”.
- Set response.data from orjson\_dumps(Platform.local.response, default = json\_handler).
- Return response.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L4443) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L540)
