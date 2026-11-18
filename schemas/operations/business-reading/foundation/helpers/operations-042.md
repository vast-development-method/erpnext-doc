# Shared value and file services · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Redis semaphore

<a id="op-ac3e80b12fe9df"></a>
### Redis Semaphore.ensure tokens

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_ensure_tokens`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - If Platform.cache.exists(formatted text {self.key}:capacity, shared = self.shared).
    - Return no value.
  - Evaluate Platform.cache.set\_value(formatted text {self.key}:capacity, self.limit, expires\_in\_sec = self.CAPACITY\_TTL, shared = self.shared).
  - Evaluate Platform.cache.delete\_value(self.key, shared = self.shared).
  - For each i in range(1, (self.limit + 1)).
    - Evaluate Platform.cache.lpush(self.key, str(i), shared = self.shared).
- On failure (Exception).
  - Evaluate Platform.log\_error(formatted text RedisSemaphore({self.key}): Failed to initialize tokens).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L5552) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L654)

<a id="op-a41698bc1bc7e7"></a>
### Redis Semaphore.decode

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_decode`

**Inputs** result.

**Wrappers, in declaration order** staticmethod.

**Explicit results** result.decode() when isinstance(result, bytes), otherwise result.

**Local steps**

- Return result.decode() when isinstance(result, bytes), otherwise result.
  - Value choice on isinstance(result, bytes) — true gives result.decode(), false gives result.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L5951) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L653)

## Service · Redis wrapper

<a id="op-3150a95a8d58e3"></a>
### Redisearch Wrapper.sugadd

`operation_foundation_utils_shared_cache_wrapper_business_behavior_search_index_wrapper_sugadd`

**Inputs** self, key, remaining positional values suggestions, remaining named values kwargs.

**Explicit results** super().sugadd(self.client.make\_key(key), expanded suggestions, expanded names kwargs).

**Local steps**

- Return super().sugadd(self.client.make\_key(key), expanded suggestions, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6032) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L716)

<a id="op-9a26388b993998"></a>
### Redisearch Wrapper.suglen

`operation_foundation_utils_shared_cache_wrapper_business_behavior_search_index_wrapper_suglen`

**Inputs** self, key.

**Explicit results** super().suglen(self.client.make\_key(key)).

**Local steps**

- Return super().suglen(self.client.make\_key(key)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6146) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L719)

<a id="op-e7649c912ebd67"></a>
### Redisearch Wrapper.sugdel

`operation_foundation_utils_shared_cache_wrapper_business_behavior_search_index_wrapper_sugdel`

**Inputs** self, key, string.

**Explicit results** super().sugdel(self.client.make\_key(key), string).

**Local steps**

- Return super().sugdel(self.client.make\_key(key), string).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6234) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L717)

<a id="op-57f1fd42f4318d"></a>
### Redisearch Wrapper.sugget

`operation_foundation_utils_shared_cache_wrapper_business_behavior_search_index_wrapper_sugget`

**Inputs** self, key, remaining positional values args, remaining named values kwargs.

**Explicit results** super().sugget(self.client.make\_key(key), expanded args, expanded names kwargs).

**Local steps**

- Return super().sugget(self.client.make\_key(key), expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6333) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L718)

<a id="op-f9956487135d12"></a>
### Redis Wrapper.connected

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_connected`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Attempt the following.
  - Evaluate self.ping().
  - Return true.
- On failure (redis.exceptions.ConnectionError).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6447) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L661)

<a id="op-73b6a3073a88b3"></a>
### Redis Wrapper.invoke

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_call`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Return self.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6538) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L660)

<a id="op-ab24317c7721e6"></a>
### Redis Wrapper.make key

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_make_key`

**Inputs** self, key, user = no value, shared = false.

**Explicit results** key · formatted text {nested operand in the contract.local.conf.get(“db\_name”)}\|{key}.encode().

**Local steps**

- If shared.
  - Return key.
- If user.
  - If user is identical to true.
    - Set user from Platform.local.session.get(“user”).
  - Set key from formatted text user:{user}:{key}.
- Return formatted text {nested operand in the contract.local.conf.get(“db\_name”)}\|{key}.encode().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6575) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L685)

<a id="op-790ad1620dbe13"></a>
### Redis Wrapper.set value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_set_value`

**Inputs** self, key, val, user = no value, expires\_in\_sec = no value, shared = false.

**Declared result** int.

**Explicit results** len(serialized).

**Local steps**

- Set key from self.make\_key(key, user, shared).
- Set Platform.local.cache at key from val.
- Set serialized from pickle.dumps(val, protocol = DEFAULT\_PICKLE\_PROTOCOL).
- Within suppress(redis.exceptions.ConnectionError).
  - Evaluate self.set(name = key, value = serialized, ex = expires\_in\_sec).
- Return len(serialized).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L6838) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L689)

<a id="op-8f7a56d76bcf29"></a>
### Redis Wrapper.get value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_get_value`

**Inputs** self, key, generator = no value, user = no value, expires = false, shared = false, use\_local\_cache (named only, default true).

**Explicit results** self.\_get\_value\_with\_size(key, generator = generator, user = user, expires = expires, shared = shared, …) at 0.

**Local steps**

- Return self.\_get\_value\_with\_size(key, generator = generator, user = user, expires = expires, shared = shared, …) at 0.

**Methods declared on this owner** [get value with size](operations-042.md#op-904c89446e99c9).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L7125) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L670)

<a id="op-904c89446e99c9"></a>
### Redis Wrapper.get value with size

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_get_value_with_size`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, key, generator, user, expires, shared, use\_local\_cache.

**Explicit result forms** a structured result.

**Observed service boundaries** record mutation request.

**Local structure** 4 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L7299) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L671)

<a id="op-5798d4bf05f7e7"></a>
### Redis Wrapper.expire key

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_expire_key`

**Inputs** self, key, time, user (named only, default no value), shared (named only, default false).

**Explicit results** self.expire(key, time).

**Local steps**

- Set key from self.make\_key(key, user, shared).
- Attempt the following.
  - Return self.expire(key, time).
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L7852) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L666)

<a id="op-1c65fa349fad01"></a>
### Redis Wrapper.get all

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_get_all`

**Inputs** self, key.

**Explicit results** ret.

**Local steps**

- Set ret from mapping().
- For each k in self.get\_keys(key).
  - Set ret at key from self.get\_value(k).
- Return ret.

**Methods declared on this owner** [get keys](operations-042.md#op-fe2246ce37f3ed), [get value](operations-042.md#op-8f7a56d76bcf29).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L668)

<a id="op-fe2246ce37f3ed"></a>
### Redis Wrapper.get keys

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_get_keys`

**Inputs** self, key, user = no value, shared = false.

**Explicit results** self.keys(key) · list of k for k drawn from list(Platform.local.cache) where regex.match(cstr(k)).

**Local steps**

- Attempt the following.
  - Set key from self.make\_key((key + “\*”), user = user, shared = shared).
  - Return self.keys(key).
- On failure (redis.exceptions.ConnectionError).
  - Set regex from re.compile(cstr(key).replace(“\|”, “\\\|”).replace(“\*”, “&#91;\\w&#93;\*”)).
  - Return list of k for k drawn from list(Platform.local.cache) where regex.match(cstr(k)).
    - Draw k from list(Platform.local.cache), keep a combination only if (regex.match(cstr(k))).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L135) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L669)

<a id="op-a46bc2e6f4b1ec"></a>
### Redis Wrapper.delete keys

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_delete_keys`

**Inputs** self, key, user = no value, shared = false.

**Local steps**

- Evaluate self.delete\_value(self.get\_keys(key, user = user, shared = shared), make\_keys = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete value](operations-042.md#op-5b5fcdc282ff5b), [get keys](operations-042.md#op-fe2246ce37f3ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L467) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L663)

<a id="op-4c791a4e86d420"></a>
### Redis Wrapper.delete key

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_delete_key`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate self.delete\_value(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete value](operations-042.md#op-5b5fcdc282ff5b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L601) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L662)

<a id="op-5b5fcdc282ff5b"></a>
### Redis Wrapper.delete value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_delete_value`

**Inputs** self, keys, user = no value, make\_keys = true, shared = false.

**Explicit results** no value.

**Local steps**

- If not keys.
  - Return no value.
- If not isinstance(keys, (list bitwise or tuple)).
  - Set keys from tuple(keys).
- If make\_keys.
  - Set keys from list of self.make\_key(k, shared = shared, user = user) for k drawn from keys.
    - Draw k from keys.
- Set local\_cache from Platform.local.cache.
- For each key in keys.
  - Evaluate local\_cache.pop(key, no value).
- Attempt the following.
  - Evaluate self.unlink(expanded keys).
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L679) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L664)

<a id="op-0d411cd4fdf740"></a>
### Redis Wrapper.lpush

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_lpush`

**Inputs** self, key, value, user = no value, shared = false.

**Explicit results** super().lpush(self.make\_key(key, user = user, shared = shared), value).

**Local steps**

- Return super().lpush(self.make\_key(key, user = user, shared = shared), value).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1025) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L682)

<a id="op-81c422f9647910"></a>
### Redis Wrapper.rpush

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_rpush`

**Inputs** self, key, value.

**Explicit results** super().rpush(self.make\_key(key), value).

**Local steps**

- Return super().rpush(self.make\_key(key), value).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1165) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L687)

<a id="op-b05716a964a6b5"></a>
### Redis Wrapper.lpop

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_lpop`

**Inputs** self, key, user = no value, shared = false.

**Explicit results** super().lpop(self.make\_key(key, user = user, shared = shared)).

**Local steps**

- Return super().lpop(self.make\_key(key, user = user, shared = shared)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1263) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L681)

<a id="op-7e9362b7afccc2"></a>
### Redis Wrapper.rpop

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_rpop`

**Inputs** self, key.

**Explicit results** super().rpop(self.make\_key(key)).

**Local steps**

- Return super().rpop(self.make\_key(key)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1392) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L686)

<a id="op-c61a6911271fb9"></a>
### Redis Wrapper.blpop

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_blpop`

**Inputs** self, key, timeout = 0, user = no value, shared = false.

**Explicit results** super().blpop(self.make\_key(key, user = user, shared = shared), timeout = timeout).

**Local steps**

- Return super().blpop(self.make\_key(key, user = user, shared = shared), timeout = timeout).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1479) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L659)

<a id="op-ba91b89013c2e6"></a>
### Redis Wrapper.llen

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_llen`

**Inputs** self, key.

**Explicit results** super().llen(self.make\_key(key)).

**Local steps**

- Return super().llen(self.make\_key(key)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1629) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L680)
