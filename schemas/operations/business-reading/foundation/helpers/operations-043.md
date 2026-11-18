# Shared value and file services · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Redis wrapper

<a id="op-730c5fdcac1507"></a>
### Redis Wrapper.lrange

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_lrange`

**Inputs** self, key, start, stop.

**Explicit results** super().lrange(self.make\_key(key), start, stop).

**Local steps**

- Return super().lrange(self.make\_key(key), start, stop).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1716) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L683)

<a id="op-e2623a310ef9bc"></a>
### Redis Wrapper.ltrim

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_ltrim`

**Inputs** self, key, start, stop.

**Explicit results** super().ltrim(self.make\_key(key), start, stop).

**Local steps**

- Return super().ltrim(self.make\_key(key), start, stop).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1825) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L684)

<a id="op-c5d1299286725d"></a>
### Redis Wrapper.hset

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hset`

**Inputs** self, name, key, value, shared = false, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- If key is identical to no value.
  - Return no value.
- Set \_name from self.make\_key(name, shared = shared).
- Set Platform.local.cache.setdefault(\_name, mapping()) at key from value.
- Attempt the following.
  - Evaluate super().hset(\_name, key, pickle.dumps(value, protocol = DEFAULT\_PICKLE\_PROTOCOL), expanded args, expanded names kwargs).
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L1934) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L679)

<a id="op-294e918d6375f1"></a>
### Redis Wrapper.hexists

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hexists`

**Inputs** self, name, key, shared = false.

**Declared result** bool.

**Explicit results** false · super().hexists(\_name, key).

**Local steps**

- If key is identical to no value.
  - Return false.
- Set \_name from self.make\_key(name, shared = shared).
- Attempt the following.
  - Return super().hexists(\_name, key).
- On failure (redis.exceptions.ConnectionError).
  - Return false.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L2251) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L675)

<a id="op-49f4e642586ae6"></a>
### Redis Wrapper.exists

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_exists`

**Inputs** self, remaining positional values names, user (named only, default no value), shared (named only, default no value).

**Declared result** int.

**Explicit results** super().exists(expanded names) · false.

**Local steps**

- Set names from list of self.make\_key(n, user = user, shared = shared) for n drawn from names.
  - Draw n from names.
- Attempt the following.
  - Return super().exists(expanded names).
- On failure (redis.exceptions.ConnectionError).
  - Return false.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L2464) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L665)

<a id="op-dde4135234980d"></a>
### Redis Wrapper.hgetall

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hgetall`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, name.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L2661) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L677)

<a id="op-378095e410007a"></a>
### Redis Wrapper.hget

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hget`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, name, key, generator, shared.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L2819) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L676)

<a id="op-e9233dfafd61f8"></a>
### Redis Wrapper.hdel

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hdel`

**Inputs** self, name, keys, shared = false, pipeline = no value.

**Explicit results** no value.

**Local steps**

- Set \_name from self.make\_key(name, shared = shared).
- Set name\_in\_local\_cache from \_name belongs to Platform.local.cache.
- If not isinstance(keys, (list bitwise or tuple)).
  - If (name\_in\_local\_cache and keys belongs to Platform.local.cache at \_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in name\_in\_local\_cache → keys belongs to Platform.local.cache at \_name.
    - Remove Platform.local.cache at \_name at keys.
  - If pipeline.
    - Evaluate pipeline.hdel(\_name, keys).
  - Otherwise.
    - Attempt the following.
      - Evaluate super().hdel(\_name, keys).
    - On failure (redis.exceptions.ConnectionError).
      - Take no action here.
  - Return no value.
- Set local\_pipeline from false.
- If pipeline is identical to no value.
  - Set pipeline from self.pipeline().
  - Set local\_pipeline from true.
- For each key in keys.
  - If name\_in\_local\_cache.
    - If key belongs to Platform.local.cache at \_name.
      - Remove Platform.local.cache at \_name at key.
  - Evaluate pipeline.hdel(\_name, key).
- If local\_pipeline.
  - Attempt the following.
    - Evaluate pipeline.execute().
  - On failure (redis.exceptions.ConnectionError).
    - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L3303) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L672)

<a id="op-3daf02123a9071"></a>
### Redis Wrapper.hdel names

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hdel_names`

**Inputs** self, names, key.

**Local steps**

- Set pipeline from self.pipeline().
- For each name in names.
  - Evaluate self.hdel(name, key, pipeline = pipeline).
- Attempt the following.
  - Evaluate pipeline.execute().
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [hdel](operations-043.md#op-e9233dfafd61f8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L3962) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L674)

<a id="op-412683710d9da9"></a>
### Redis Wrapper.hdel keys

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hdel_keys`

**Inputs** self, name\_starts\_with, key.

**Local steps**

- Set pipeline from self.pipeline().
- For each name in self.get\_keys(name\_starts\_with).
  - Set name from name.split(“\|”, 1) at 1.
  - Evaluate self.hdel(name, key, pipeline = pipeline).
- Attempt the following.
  - Evaluate pipeline.execute().
- On failure (redis.exceptions.ConnectionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get keys](operations-042.md#op-fe2246ce37f3ed), [hdel](operations-043.md#op-e9233dfafd61f8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4156) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L673)

<a id="op-7930d31b291c07"></a>
### Redis Wrapper.hkeys

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_hkeys`

**Inputs** self, name.

**Explicit results** super().hkeys(self.make\_key(name)) · list().

**Local steps**

- Attempt the following.
  - Return super().hkeys(self.make\_key(name)).
- On failure (redis.exceptions.ConnectionError).
  - Return list().

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4388) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L678)

<a id="op-5d6703641c8eef"></a>
### Redis Wrapper.sadd

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_sadd`

**Inputs** self, name, remaining positional values values.

**Local steps**

- Evaluate super().sadd(self.make\_key(name), expanded values).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4510) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L688)

<a id="op-7bac0dde530c4b"></a>
### Redis Wrapper.srem

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_srem`

**Inputs** self, name, remaining positional values values.

**Local steps**

- Evaluate super().srem(self.make\_key(name), expanded values).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4609) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L694)

<a id="op-46d78f98e8e031"></a>
### Redis Wrapper.sismember

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_sismember`

**Inputs** self, name, value.

**Explicit results** super().sismember(self.make\_key(name), value).

**Local steps**

- Return super().sismember(self.make\_key(name), value).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4708) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L690)

<a id="op-1a794c1a2897db"></a>
### Redis Wrapper.spop

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_spop`

**Inputs** self, name.

**Explicit results** super().spop(self.make\_key(name)).

**Local steps**

- Return super().spop(self.make\_key(name)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4806) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L692)

<a id="op-4f0e660e853027"></a>
### Redis Wrapper.srandmember

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_srandmember`

**Inputs** self, name, count = no value.

**Explicit results** super().srandmember(self.make\_key(name)).

**Local steps**

- Return super().srandmember(self.make\_key(name)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4893) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L693)

<a id="op-2856407bfbd337"></a>
### Redis Wrapper.smembers

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_smembers`

**Inputs** self, name.

**Explicit results** super().smembers(self.make\_key(name)).

**Local steps**

- Return super().smembers(self.make\_key(name)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L4990) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L691)

<a id="op-5ebaf8f784f712"></a>
### Redis Wrapper.ft

`operation_foundation_utils_shared_cache_wrapper_business_behavior_cache_service_wrapper_ft`

**Inputs** self, index\_name = “idx”.

**Explicit results** RedisearchWrapper(client = self, index\_name = self.make\_key(index\_name)).

**Local steps**

- Return RedisearchWrapper(client = self, index\_name = self.make\_key(index\_name)).

**Methods declared on this owner** [make key](operations-042.md#op-ab24317c7721e6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L5077) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L667)

<a id="op-6b75bddae4bd20"></a>
### Setup cache

`operation_foundation_utils_shared_cache_wrapper_business_behavior_setup_cache`

**Inputs** no declared parameters.

**Declared result** RedisWrapper.

**Explicit results** sentinel.master\_for(Platform.conf.get(“redis\_cache\_master\_service”), redis\_class = RedisWrapper) · RedisWrapper.from\_url(Platform.conf.get(“redis\_cache”)).

**Local steps**

- If Platform.conf.redis\_cache\_sentinel\_enabled.
  - Set sentinels from list of tuple(node.split(“:”)) for node drawn from Platform.conf.get(“redis\_cache\_sentinels”, list()).
    - Draw node from Platform.conf.get(“redis\_cache\_sentinels”, list()).
  - Set sentinel from get\_sentinel\_connection(sentinels = sentinels, sentinel\_username = Platform.conf.get(“redis\_cache\_sentinel\_username”), sentinel\_password = Platform.conf.get(“redis\_cache\_sentinel\_password”), master\_usernam ….
  - Return sentinel.master\_for(Platform.conf.get(“redis\_cache\_master\_service”), redis\_class = RedisWrapper).
- Return RedisWrapper.from\_url(Platform.conf.get(“redis\_cache”)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L5176) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L720)

<a id="op-a063ef8aff909d"></a>
### Get sentinel connection

`operation_foundation_utils_shared_cache_wrapper_business_behavior_get_sentinel_connection`

**Inputs** sentinels, sentinel\_username = no value, sentinel\_password = no value, master\_username = no value, master\_password = no value.

**Explicit results** Sentinel(sentinels = sentinels, sentinel\_kwargs = sentinel\_kwargs, username = master\_username, password = master\_password).

**Local steps**

- Bind dependencies Sentinel.
- Set sentinel\_kwargs from mapping().
- If sentinel\_username.
  - Set sentinel\_kwargs at “username” from sentinel\_username.
- If sentinel\_password.
  - Set sentinel\_kwargs at “password” from sentinel\_password.
- Return Sentinel(sentinels = sentinels, sentinel\_kwargs = sentinel\_kwargs, username = master\_username, password = master\_password).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L5546) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L715)

<a id="op-a9cdae32aa89b6"></a>
### Client Tracking Mixin.initialize

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_tracking_mixin_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set self.\_invalidator\_id from kwargs.pop(“\_invalidator\_id”).
- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Evaluate self.register\_connect\_callback(self.\_enable\_client\_tracking).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L5791) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L714)

<a id="op-09fe87454278fb"></a>
### Client Tracking Mixin.enable client tracking

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_tracking_mixin_enable_client_tracking`

**Inputs** self, conn.

**Explicit failure paths** Exception(“Redis version is not supported, upgrade to Redis 6.0 or higher.”) · propagate active failure.

**Local steps**

- Attempt the following.
  - Evaluate conn.send\_command(“CLIENT”, “TRACKING”, “ON”, “redirect”, …).
  - Evaluate conn.read\_response().
- On failure (ResponseError) bound to e.
  - If (“client ID” belongs to str(e) and “does not exist” belongs to str(e)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in “client ID” belongs to str(e) → “does not exist” belongs to str(e).
    - Set Platform.client\_cache.healthy from false.
  - Otherwise.
    - If “unknown subcommand” belongs to str(e).lower().
      - Raise Exception(“Redis version is not supported, upgrade to Redis 6.0 or higher.”).
    - Otherwise.
      - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L5934) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L713)

<a id="op-8e77d3441692bb"></a>
### Client Cache.initialize

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_initialize`

**Inputs** self, maxsize = 1024, ttl = (10 × 60), monitor = no value, maxsize\_bytes = 0.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set self.maxsize from (maxsize or 1024).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in maxsize → 1024.
- Set self.maxsize\_bytes from (maxsize\_bytes or cint(Platform.conf.get(“client\_cache\_max\_bytes”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in maxsize\_bytes → cint(Platform.conf.get(“client\_cache\_max\_bytes”)).
- Set self.local\_ttl from ttl.
- Set self.lock from threading.RLock().
- Set self.cache from mapping().
- Set self.\_total\_size from 0.
- Set self.invalidator from Platform.cache.
- Set self.healthy from true.
- Set self.connection\_retries from 0.
- Set self.invalidator\_id from no value.
- Attempt the following.
  - Set self.invalidator\_id from self.invalidator.client\_id().
- On failure (redis.exceptions.ConnectionError).
  - Set self.redis from Platform.cache.
  - Set self.healthy from false.
- Set self.hits, self.misses from 0.
- If not self.invalidator\_id.
  - Return no value.
- Set redis\_url from (Platform.conf.get(“redis\_cache”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“redis\_cache”) → empty text.
- If redis\_url.startswith(“unix://”).
  - Set connection\_class from \_TrackedUnixDomainSocketConnection.
- Otherwise.
  - If redis\_url.startswith(“rediss://”).
    - Set connection\_class from \_TrackedSSLConnection.
  - Otherwise.
    - Set connection\_class from \_TrackedConnection.
- Set self.redis from RedisWrapper.from\_url(redis\_url, connection\_class = connection\_class, \_invalidator\_id = self.invalidator\_id, protocol = 2).
- Set self.invalidator\_thread from self.run\_invalidator\_thread().

If control reaches the end, it returns no value.

**Methods declared on this owner** [run invalidator thread](operations-044.md#op-a1a468b0363e95).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L78) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L706)

<a id="op-2038b27974579d"></a>
### Client Cache.get value

`operation_foundation_utils_shared_cache_wrapper_business_behavior_client_cache_get_value`

**Inputs** self, key, shared (named only, default false), generator (named only, default no value).

**Explicit results** self.redis.get\_value(key, shared = shared, generator = generator) · val.value · val · no value.

**Local steps**

- If not self.healthy.
  - Return self.redis.get\_value(key, shared = shared, generator = generator).
- Set key from self.redis.make\_key(key, shared = shared).
- Attempt the following.
  - Set val from self.cache at key.
  - If time.monotonic() &lt; val.expiry.
    - Update self.hits using + 1.
    - Return val.value.
- On failure (KeyError).
  - Take no action here.
- Update self.misses using + 1.
- Within self.lock.
  - Evaluate self.\_pop(key).
  - Set self.cache at key from \_PLACEHOLDER\_VALUE.
- Set tuple(val, size) from self.redis.\_get\_value\_with\_size(key, shared = true, use\_local\_cache = not self.healthy).
- If val is identical to no value.
  - If generator.
    - Set val from generator().
    - Evaluate self.set\_value(key, val, shared = true).
    - Return val.
  - Otherwise.
    - Return no value.
- Evaluate self.ensure\_max\_size().
- Within self.lock.
  - If key belongs to self.cache.
    - Evaluate self.\_put(key, val, (time.monotonic() + self.local\_ttl), size).
- Return val.

**Methods declared on this owner** [pop](operations-044.md#op-a8d864b8b50b1f), [set value](operations-044.md#op-6813b8ddfe6257), [ensure max size](operations-044.md#op-b7b3c2d2566952), [put](operations-044.md#op-5cf32302afb9a6).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0498.json#L6894) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L703)
