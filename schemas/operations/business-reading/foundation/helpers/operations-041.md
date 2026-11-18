# Shared value and file services · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Queue

<a id="op-8ddedbbf4fb0ac"></a>
### Event Queue.is ratelimited

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_is_ratelimited`

**Inputs** self, event, interval.

**Explicit results** false · true.

**Local steps**

- If not interval.
  - Return false.
- Set interval\_seconds from parse\_interval(interval).
- Set event\_key from self.\_get\_event\_key(event).
- Set last\_sent\_key from formatted text {self.ratelimit\_prefix}{event\_key}.
- Set last\_sent from Platform.cache.get\_value(last\_sent\_key).
- If (last\_sent and (time.monotonic() − float(last\_sent)) &lt; interval\_seconds).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_sent → (time.monotonic() − float(last\_sent)) &lt; interval\_seconds.
  - Return true.
- Return false.

**Methods declared on this owner** [get event key](operations-041.md#op-bba50b96f50144).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2347) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L744)

<a id="op-bba50b96f50144"></a>
### Event Queue.get event key

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_get_event_key`

**Inputs** self, event.

**Explicit results** formatted text {event.get(“event\_name”)}:{event.get(“user”)}:{event.get(“team”)}:{event.get(“site”)}:{event.get(“app”)}.

**Local steps**

- Return formatted text {event.get(“event\_name”)}:{event.get(“user”)}:{event.get(“team”)}:{event.get(“site”)}:{event.get(“app”)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2622) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L740)

<a id="op-b06d354e90252c"></a>
### Event Queue.update ratelimit

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_update_ratelimit`

**Inputs** self, event, interval.

**Explicit results** no value.

**Local steps**

- If not interval.
  - Return no value.
- Set event\_key from self.\_get\_event\_key(event).
- Set last\_sent\_key from formatted text {self.ratelimit\_prefix}{event\_key}.
- Evaluate Platform.cache.set\_value(last\_sent\_key, time.monotonic()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get event key](operations-041.md#op-bba50b96f50144).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L2830) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L748)

<a id="op-91d8ef9a712b70"></a>
### Event Queue.queue event

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_queue_event`

**Inputs** self, event.

**Local steps**

- Evaluate Platform.cache.lpush(self.queue, Platform.as\_json(event)).
- Evaluate Platform.cache.ltrim(self.queue, 0, (self.queue\_size − 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L3009) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L746)

<a id="op-0b3ec56848f7ce"></a>
### Event Queue.batch process

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_batch_process`

**Inputs** self, fn, batch\_size = 100, max\_batches = 10, max\_retries = 3, backoff\_seconds = 1.

**Local steps**

- Set pending\_events from no value.
- Set retry\_attempts from 0.
- For each \_ in range(max\_batches).
  - Set events from (pending\_events or self.collect(batch\_size)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pending\_events → self.collect(batch\_size).
  - If not events.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Attempt the following.
    - Evaluate fn(events).
    - Set pending\_events from no value.
    - Set retry\_attempts from 0.
  - On failure (Exception) bound to e.
    - Update retry\_attempts using + 1.
    - If retry\_attempts &gt; max\_retries.
      - Evaluate Platform.logger(“pulse”).error(formatted text pulse-client - max retries reached: {e}).
      - Evaluate self.\_requeue\_events(events).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set pending\_events from events.
    - Evaluate time.sleep((backoff\_seconds × (2 to the power (retry\_attempts − 1)))).
    - Evaluate Platform.logger(“pulse”).error(formatted text pulse-client - retrying batch due to error: {e}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [collect](operations-041.md#op-ea0378f53798b1), [requeue events](operations-041.md#op-605e9d9cd9cd5e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L737)

<a id="op-ea0378f53798b1"></a>
### Event Queue.collect

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_collect`

**Inputs** self, batch\_size = 100.

**Explicit results** events.

**Local steps**

- Set events from list().
- For each \_ in range(batch\_size).
  - Set event\_json from Platform.cache.rpop(self.queue).
  - If not event\_json.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set data from self.\_decode\_event(event\_json).
  - If data.
    - Evaluate events.append(data).
- Return events.

**Methods declared on this owner** [decode event](operations-041.md#op-361c4e32abaaac).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L3643) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L738)

<a id="op-605e9d9cd9cd5e"></a>
### Event Queue.requeue events

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_requeue_events`

**Inputs** self, events.

**Local steps**

- For each event in reversed(events).
  - Evaluate Platform.cache.rpush(self.queue, Platform.as\_json(event)).
- Evaluate Platform.cache.ltrim(self.queue, negative self.queue\_size, negative 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L3851) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L747)

<a id="op-361c4e32abaaac"></a>
### Event Queue.decode event

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_decode_event`

**Inputs** self, event\_json.

**Explicit results** Platform.parse\_json(event\_json).

**Local steps**

- Set event\_json from event\_json.decode().
- Within suppress(JSONDecodeError).
  - Return Platform.parse\_json(event\_json).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L4021) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L739)

<a id="op-ba57ffcd201ff0"></a>
### Event Queue.get events

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_get_events`

**Inputs** self, limit = 20.

**Explicit results** events.

**Local steps**

- Set events from list().
- For each \_ in range(limit).
  - Set event\_json from Platform.cache.lindex(self.queue, \_).
  - If not event\_json.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set data from self.\_decode\_event(event\_json).
  - If data.
    - Evaluate events.append(data).
- Return events.

**Methods declared on this owner** [decode event](operations-041.md#op-361c4e32abaaac).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L4135) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L741)

<a id="op-28d2e4da46ca3a"></a>
### Event Queue.get last sent events

`operation_foundation_utils_telemetry_pulse_queue_business_behavior_event_queue_get_last_sent_events`

**Inputs** self, limit = 20.

**Explicit results** events.

**Local steps**

- Set events from list().
- Set keys from Platform.cache.get\_keys(formatted text {self.ratelimit\_prefix}\*) at slice no value to limit.
- For each key in keys.
  - Set last\_sent from Platform.cache.get\_value(key).
  - Set event\_key from key.replace(self.ratelimit\_prefix, empty text).
  - Evaluate events.append(mapping(“event\_key” → event\_key, “last\_sent” → last\_sent)).
- Return events.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L4347) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L742)

## Service · Redis queue

<a id="op-b3cc0e00fa5650"></a>
### Redis Queue.initialize

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_initialize`

**Inputs** self, conn.

**Local steps**

- Set self.conn from conn.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L2705) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L649)

<a id="op-e167154e22a54d"></a>
### Redis Queue.add user

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_add_user`

**Inputs** self, username, password = no value.

**Explicit results** Platform.\_dict(user\_settings) when is\_created, otherwise mapping().

**Local steps**

- Set password from (password or self.conn.acl\_genpass()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in password → self.conn.acl\_genpass().
- Set user\_settings from self.get\_new\_user\_settings(username, password).
- Set is\_created from self.conn.acl\_setuser(expanded names user\_settings).
- Return Platform.\_dict(user\_settings) when is\_created, otherwise mapping().
  - Value choice on is\_created — true gives Platform.\_dict(user\_settings), false gives mapping().

**Methods declared on this owner** [get new user settings](operations-041.md#op-f3a8578f8cb099).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L2759) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L643)

<a id="op-8f392cfcad7d40"></a>
### Redis Queue.get connection

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_get_connection`

**Inputs** cls, username = no value, password = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** conn.

**Local steps**

- Set conf from Platform.get\_site\_config().
- If conf.redis\_queue\_sentinel\_enabled.
  - Bind dependencies get\_sentinel\_connection.
  - Set sentinels from list of tuple(node.split(“:”)) for node drawn from conf.get(“redis\_queue\_sentinels”, list()).
    - Draw node from conf.get(“redis\_queue\_sentinels”, list()).
  - Set sentinel from get\_sentinel\_connection(sentinels = sentinels, sentinel\_username = conf.get(“redis\_queue\_sentinel\_username”), sentinel\_password = conf.get(“redis\_queue\_sentinel\_password”), master\_username = conf.get(“redi ….
  - Set conn from sentinel.master\_for(conf.get(“redis\_queue\_master\_service”)).
  - Evaluate conn.ping().
  - Return conn.
- Set conn from redis.from\_url(conf.redis\_queue, username = username, password = password).
- Evaluate conn.ping().
- Return conn.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L2952) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L647)

<a id="op-84db790cd720a3"></a>
### Redis Queue.new

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_new`

**Inputs** cls, username = “default”, password = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls(cls.get\_connection(username, password)).

**Local steps**

- Return cls(cls.get\_connection(username, password)).

**Methods declared on this owner** [get connection](operations-041.md#op-8f392cfcad7d40).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L3414) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L650)

<a id="op-05db69b998bd72"></a>
### Redis Queue.set admin password

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_set_admin_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, cur\_password, new\_password, reset\_passwords.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L3518) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L651)

<a id="op-f3a8578f8cb099"></a>
### Redis Queue.get new user settings

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_get_new_user_settings`

**Inputs** cls, username, password.

**Wrappers, in declaration order** classmethod.

**Explicit results** d.

**Local steps**

- Set d from mapping().
- Set d at “username” from username.
- Set d at “passwords” from (“+” + password).
- Set d at “reset\_keys” from true.
- Set d at “enabled” from true.
- Set d at “keys” from cls.get\_acl\_key\_rules().
- Set d at “commands” from cls.get\_acl\_command\_rules().
- Return d.

**Methods declared on this owner** [get acl key rules](operations-041.md#op-8b90009fa88e53), [get acl command rules](operations-041.md#op-727c14cd099834).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L3759) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L648)

<a id="op-8b90009fa88e53"></a>
### Redis Queue.get acl key rules

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_get_acl_key_rules`

**Inputs** cls, include\_key\_prefix = false.

**Wrappers, in declaration order** classmethod.

**Explicit results** list of (“~” + pattern) for pattern drawn from rules · rules.

**Local steps**

- Set rules from list(“rq:&#91;^q&#93;\*”, “rq:queues”, formatted text rq:queue:{get\_bench\_id()}:\*).
- If include\_key\_prefix.
  - Return list of (“~” + pattern) for pattern drawn from rules.
    - Draw pattern from rules.
- Return rules.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L3993) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L646)

<a id="op-727c14cd099834"></a>
### Redis Queue.get acl command rules

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_get_acl_command_rules`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** list(“+@all”, “-@admin”).

**Local steps**

- Return list(“+@all”, “-@admin”).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L4145) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L645)

<a id="op-25b494e9b62976"></a>
### Redis Queue.gen acl list

`operation_foundation_utils_shared_cache_queue_business_behavior_cache_service_queue_gen_acl_list`

**Inputs** cls, set\_admin\_password = false.

**Wrappers, in declaration order** classmethod.

**Explicit results** tuple(list(formatted text user {default\_username} on {default\_user\_password} ~\* &amp;\* +@all, formatted text user {bench\_username} on &gt;{bench\_user\_password} {bench\_user\_rule\_str}), mapping(“bench” → tuple(benc ….

**Local steps**

- Set bench\_username from get\_bench\_id().
- Set bench\_user\_rules from (cls.get\_acl\_key\_rules(include\_key\_prefix = true) + cls.get\_acl\_command\_rules()).
- Set bench\_user\_rule\_str from one space.join(bench\_user\_rules).strip().
- Set bench\_user\_password from random\_string(20).
- Set default\_username from “default”.
- Set \_default\_user\_password from random\_string(20) when set\_admin\_password, otherwise empty text.
  - Value choice on set\_admin\_password — true gives random\_string(20), false gives empty text.
- Set default\_user\_password from (“&gt;” + \_default\_user\_password) when \_default\_user\_password, otherwise “nopass”.
  - Value choice on \_default\_user\_password — true gives (“&gt;” + \_default\_user\_password), false gives “nopass”.
- Return tuple(list(formatted text user {default\_username} on {default\_user\_password} ~\* &amp;\* +@all, formatted text user {bench\_username} on &gt;{bench\_user\_password} {bench\_user\_rule\_str}), mapping(“bench” → tuple(benc ….

**Methods declared on this owner** [get acl key rules](operations-041.md#op-8b90009fa88e53), [get acl command rules](operations-041.md#op-727c14cd099834).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L4196) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L644)

## Service · Redis semaphore

<a id="op-844908b040cd13"></a>
### Redis Semaphore.initialize

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_initialize`

**Inputs** self, key, limit, wait\_timeout = 0, shared = false.

**Local steps**

- Set self.key from key.
- Set self.limit from limit.
- Set self.wait\_timeout from wait\_timeout.
- Set self.shared from shared.
- Set self.\_token from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L4630) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L657)

<a id="op-5d481dcc9d1a3b"></a>
### Redis Semaphore.acquire

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_acquire`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** self.\_decode(result) when result is distinct from no value, otherwise no value · self.\_decode(result at 1) · no value · “fallback”.

**Local steps**

- Attempt the following.
  - Evaluate self.\_ensure\_tokens().
  - If self.wait\_timeout ≤ 0.
    - Set result from Platform.cache.lpop(self.key, shared = self.shared).
    - Return self.\_decode(result) when result is distinct from no value, otherwise no value.
      - Value choice on result is distinct from no value — true gives self.\_decode(result), false gives no value.
  - If result bound to Platform.cache.blpop(self.key, timeout = int(self.wait\_timeout), shared = self.shared).
    - Return self.\_decode(result at 1).
  - Return no value.
- On failure (Exception).
  - Evaluate Platform.log\_error(formatted text RedisSemaphore({self.key}): Redis unavailable, skipping limit).
  - Return “fallback”.

**Methods declared on this owner** [ensure tokens](operations-042.md#op-ac3e80b12fe9df), [decode](operations-042.md#op-a41698bc1bc7e7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L4800) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L652)

<a id="op-c7fe27f606985f"></a>
### Redis Semaphore.release

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_release`

**Inputs** self, token.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If token equals “fallback”.
  - Return no value.
- Attempt the following.
  - Evaluate Platform.cache.lpush(self.key, token, shared = self.shared).
- On failure (Exception).
  - Evaluate Platform.log\_error(formatted text RedisSemaphore({self.key}): Failed to release token {token}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L5176) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L658)

<a id="op-a98d1d657627f4"></a>
### Redis Semaphore.enter context

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_enter`

**Inputs** self.

**Explicit results** self.\_token.

**Local steps**

- Set self.\_token from self.acquire().
- Return self.\_token.

**Methods declared on this owner** [acquire](operations-041.md#op-5d481dcc9d1a3b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L5374) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L655)

<a id="op-abb04dc090a50c"></a>
### Redis Semaphore.exit context

`operation_foundation_utils_shared_cache_semaphore_business_behavior_cache_service_semaphore_exit`

**Inputs** self, remaining positional values exc\_info.

**Local steps**

- If self.\_token is distinct from no value.
  - Evaluate self.release(self.\_token).
  - Set self.\_token from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [release](operations-041.md#op-c7fe27f606985f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0497.json#L5446) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L656)
