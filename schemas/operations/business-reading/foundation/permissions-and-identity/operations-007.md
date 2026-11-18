# Identity and access · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Permissions

<a id="op-cb3577480283b6"></a>
### Get parent and ancestors

`operation_foundation_permissions_business_behavior_get_parent_and_ancestors`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, parent.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L4171) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1692)

<a id="op-837a75e59edb56"></a>
### Check app permission

`operation_foundation_permissions_business_behavior_check_application_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0312.json#L4255) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1683)

## Service · Rate limiter

<a id="op-a6dc16f63ee45b"></a>
### Apply

`operation_foundation_rate_limiter_business_behavior_apply`

**Inputs** no declared parameters.

**Local steps**

- Set rate\_limit from Platform.conf.rate\_limit.
- If rate\_limit.
  - Set Platform.local.rate\_limiter from RateLimiter(rate\_limit at “limit”, rate\_limit at “window”).
  - Evaluate Platform.local.rate\_limiter.apply().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L261) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L198)

<a id="op-f01ae9c296e4dc"></a>
### Update

`operation_foundation_rate_limiter_business_behavior_update`

**Inputs** no declared parameters.

**Local steps**

- If hasattr(Platform.local, “rate\_limiter”).
  - Evaluate Platform.local.rate\_limiter.update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L397) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L210)

<a id="op-d6ffb2952e364c"></a>
### Respond

`operation_foundation_rate_limiter_business_behavior_respond`

**Inputs** no declared parameters.

**Explicit results** Platform.local.rate\_limiter.respond().

**Local steps**

- If hasattr(Platform.local, “rate\_limiter”).
  - Return Platform.local.rate\_limiter.respond().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L476) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L209)

<a id="op-e2080bac3f7fd0"></a>
### Rate Limiter.initialize

`operation_foundation_rate_limiter_business_behavior_rate_limiter_initialize`

**Inputs** self, limit, window.

**Local steps**

- Set self.limit from int((limit × 1000000)).
- Set self.window from window.
- Set self.start from time.time().
- Set tuple(self.window\_number, self.spent) from divmod(int(self.start), self.window).
- Set self.key from Platform.cache.make\_key(formatted text rate-limit-counter-{self.window\_number}).
- Set self.counter from cint(Platform.cache.get(self.key)).
- If not self.counter.
  - Evaluate Platform.cache.incrby(self.key, 0).
  - Evaluate Platform.cache.expire(self.key, self.window).
- Set self.remaining from max((self.limit − self.counter), 0).
- Set self.reset from (self.window − self.spent).
- Set self.end from no value.
- Set self.duration from no value.
- Set self.rejected from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L555) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L204)

<a id="op-212045bfb8dd3f"></a>
### Rate Limiter.apply

`operation_foundation_rate_limiter_business_behavior_rate_limiter_apply`

**Inputs** self.

**Local steps**

- If self.counter &gt; self.limit.
  - Set self.rejected from true.
  - Evaluate self.reject().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reject](operations-007.md#op-bf942e9b3e1330).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1083) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L202)

<a id="op-bf942e9b3e1330"></a>
### Rate Limiter.reject

`operation_foundation_rate_limiter_business_behavior_rate_limiter_reject`

**Inputs** self.

**Explicit failure paths** Platform.TooManyRequestsError.

**Local steps**

- Raise Platform.TooManyRequestsError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1181) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L206)

<a id="op-cf13ca6400864a"></a>
### Rate Limiter.update

`operation_foundation_rate_limiter_business_behavior_rate_limiter_update`

**Inputs** self.

**Local steps**

- Evaluate self.record\_request\_end().
- Evaluate Platform.cache.incrby(self.key, self.duration).

If control reaches the end, it returns no value.

**Methods declared on this owner** [record request end](operations-007.md#op-010e26bccd9d6a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1227) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L208)

<a id="op-8473895cc2ab4d"></a>
### Rate Limiter.headers

`operation_foundation_rate_limiter_business_behavior_rate_limiter_headers`

**Inputs** self.

**Explicit results** headers.

**Local steps**

- Evaluate self.record\_request\_end().
- Set headers from mapping(“X-RateLimit-Reset” → self.reset, “X-RateLimit-Limit” → self.limit, “X-RateLimit-Remaining” → round(self.remaining, negative 6)).
- If self.rejected.
  - Set headers at “Retry-After” from self.reset.
- Return headers.

**Methods declared on this owner** [record request end](operations-007.md#op-010e26bccd9d6a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1318) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L203)

<a id="op-010e26bccd9d6a"></a>
### Rate Limiter.record request end

`operation_foundation_rate_limiter_business_behavior_rate_limiter_record_request_end`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.end is distinct from no value.
  - Return no value.
- Set self.end from time.time().
- Set self.duration from int(((self.end − self.start) × 1000000)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1494) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L205)

<a id="op-79968cf94c7095"></a>
### Rate Limiter.respond

`operation_foundation_rate_limiter_business_behavior_rate_limiter_respond`

**Inputs** self.

**Explicit results** Response(translated “Too Many Requests”, status = 429).

**Local steps**

- If self.rejected.
  - Return Response(translated “Too Many Requests”, status = 429).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0321.json#L1637) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L207)

<a id="op-70ed5ba9600e90"></a>
### Rate limit

`operation_foundation_rate_limiter_business_behavior_rate_limit`

**Inputs** key = no value, limit = 5, seconds = ((24 × 60) × 60), methods = “ALL”, ip\_based = true, endpoint = no value, user\_based = false.

**Explicit results** ratelimit\_decorator.

**Local steps**

- Bind local operation ratelimit\_decorator for subsequent calls.
- Return ratelimit\_decorator.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L105) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L199)

<a id="op-49b6f7d67c2879"></a>
### Rate limit.ratelimit decorator

`operation_foundation_rate_limiter_business_behavior_rate_limit_ratelimit_decorator`

**Inputs** fn.

**Explicit results** wrapper.

**Local steps**

- Set counter from (endpoint or formatted text {fn.\_\_module\_\_}.{fn.\_\_qualname\_\_}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in endpoint → formatted text {fn.\_\_module\_\_}.{fn.\_\_qualname\_\_}.
- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L106) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L200)

<a id="op-e90f3894c1e4fc"></a>
### Rate limit.ratelimit decorator.wrapper

`operation_foundation_rate_limiter_business_behavior_rate_limit_ratelimit_decorator_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs).

**Explicit failure paths** validation helper — translated “Either key, IP flag, or User flag is required.” · validation helper with Platform.RateLimitExceededError — translated “You hit the rate limit because of too many requests. Please try after sometime.”.

**Local steps**

- If (not Platform.request or (methods differs from “ALL” and Platform.request.method and nested operand in the contract.request.method.upper() does not belong to methods)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.request → (methods differs from “ALL” and Platform.request.method and Platform.request.method.upper() does not belong to methods).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in methods differs from “ALL” → Platform.request.method → Platform.request.method.upper() does not belong to methods.
  - Return fn(expanded args, expanded names kwargs).
- Set \_limit from limit() when callable(limit), otherwise limit.
  - Value choice on callable(limit) — true gives limit(), false gives limit.
- Set ip from Platform.local.request\_ip when ip\_based is identical to true, otherwise no value.
  - Value choice on ip\_based is identical to true — true gives Platform.local.request\_ip, false gives no value.
- Set user\_key from Platform.form\_dict.get(key, empty text) when key, otherwise no value.
  - Value choice on key — true gives Platform.form\_dict.get(key, empty text), false gives no value.
- If user\_based.
  - Set user from Platform.session.user.
  - If (user and user differs from “Guest”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user → user differs from “Guest”.
    - Set identity from user.
  - Otherwise.
    - If ip.
      - Set identity from ip.
    - Otherwise.
      - Set identity from (getattr(Platform.local, “request\_ip”, no value) or “Guest”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.local, “request\_ip”, no value) → “Guest”.
  - If (key and user\_key).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key → user\_key.
    - Set identity from formatted text {identity}:{user\_key}.
- Otherwise.
  - Set identity from no value.
  - If (key and ip\_based).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key → ip\_based.
    - Set identity from “:”.join(list(ip, user\_key)).
  - Set identity from (identity or ip or user\_key).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in identity → ip → user\_key.
- If not identity.
  - Call the validation error handler Platform.throw(translated “Either key, IP flag, or User flag is required.”).
- Set cache\_key from Platform.cache.make\_key(formatted text rl:{counter}:{identity}).
- If not callable(seconds).
  - Update cache\_key using + formatted text :{seconds}.encode().
- Set value from Platform.cache.get(cache\_key).
- If not value.
  - Evaluate Platform.cache.setex(cache\_key, seconds, 0).
- Set value from Platform.cache.incrby(cache\_key, 1).
- If value &gt; \_limit.
  - Call the validation error handler Platform.throw(translated “You hit the rate limit because of too many requests. Please try after sometime.”, Platform.RateLimitExceededError).
- Return fn(expanded args, expanded names kwargs).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request\_ip”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L107) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L201)

## Service · Sessions

<a id="op-2dbbf9d4eaa6bd"></a>
### Hash sid

`operation_foundation_binding_foundation_sessions_hash_sid`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sid.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1714)

<a id="op-73fc1cb47285c4"></a>
### Clear

`operation_foundation_sessions_business_behavior_clear`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L1917) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L554)

<a id="op-1d5ada111bf02e"></a>
### Clear sessions

`operation_foundation_sessions_business_behavior_clear_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, keep\_current, force.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L28) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L557)

<a id="op-f58298846fb93e"></a>
### Get sessions to clear

`operation_foundation_sessions_business_behavior_get_sessions_to_clear`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, keep\_current, force.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L32) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L568)

<a id="op-72f1f7cd9ee6b1"></a>
### Delete session

`operation_foundation_sessions_business_behavior_delete_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sid, user, reason, sid\_hash.

**Explicit result forms** no value.

**Observed service boundaries** transaction control.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L29) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L558)

<a id="op-a0f713e067725d"></a>
### Clear all sessions

`operation_foundation_sessions_business_behavior_clear_all_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** reason.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L26) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L555)

<a id="op-6c958dabdaaf82"></a>
### Get expired sessions

`operation_foundation_sessions_business_behavior_get_expired_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L3408) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L563)

<a id="op-6ed72a5abd9ee5"></a>
### Clear expired sessions

`operation_foundation_sessions_business_behavior_clear_expired_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L27) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L556)

<a id="op-0ac7c4c7a2e624"></a>
### Get

`operation_foundation_sessions_business_behavior_get`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 7 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L30) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L560)
