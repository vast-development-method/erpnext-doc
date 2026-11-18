# Shared value and file services · operations 58

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-f2992306d291ab"></a>
### Callback Manager.add

`operation_foundation_utils_initialize_business_behavior_callback_manager_add`

**Inputs** self, func.

**Declared result** no value.

**Local steps**

- Evaluate self.\_functions.append(func).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6487) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L196)

<a id="op-2d04992a8e19f6"></a>
### Callback Manager.invoke

`operation_foundation_utils_initialize_business_behavior_callback_manager_call`

**Inputs** self, func.

**Declared result** no value.

**Local steps**

- Evaluate self.add(func).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add](operations-058.md#op-f2992306d291ab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6557) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L198)

<a id="op-23a2d63f04a35b"></a>
### Callback Manager.run

`operation_foundation_utils_initialize_business_behavior_callback_manager_run`

**Inputs** self.

**Local steps**

- While self.\_functions.
  - Set \_func from self.\_functions.popleft().
  - Evaluate \_func().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6625) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L203)

<a id="op-a218d26475a071"></a>
### Callback Manager.reset

`operation_foundation_utils_initialize_business_behavior_callback_manager_reset`

**Inputs** self.

**Local steps**

- Evaluate self.\_functions.clear().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6712) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L202)

<a id="op-af856929f24225"></a>
### Callback Manager.len

`operation_foundation_utils_initialize_business_behavior_callback_manager_length`

**Inputs** self.

**Declared result** int.

**Explicit results** len(self.\_functions).

**Local steps**

- Return len(self.\_functions).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6765) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L201)

<a id="op-7dd443f3bc3cd5"></a>
### Callback Manager.bool

`operation_foundation_utils_initialize_business_behavior_callback_manager_boolean`

**Inputs** self.

**Declared result** bool.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6821) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L197)

<a id="op-9bf8056dd08504"></a>
### Callback Manager.cut

`operation_foundation_utils_initialize_business_behavior_callback_manager_cut`

**Inputs** self, count.

**Declared result** list.

**Explicit results** detached.

**Local steps**

- Set detached from list().
- While len(self.\_functions) &gt; count.
  - Evaluate detached.append(self.\_functions.pop()).
- Evaluate detached.reverse().
- Return detached.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6860) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L199)

<a id="op-c4da31ee8eb4d2"></a>
### Callback Manager.truncate

`operation_foundation_utils_initialize_business_behavior_callback_manager_truncate`

**Inputs** self, count.

**Declared result** no value.

**Local steps**

- Evaluate self.cut(count).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cut](operations-058.md#op-9bf8056dd08504).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L7019) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L204)

<a id="op-3a7a5ee761a729"></a>
### Safe eval

`operation_foundation_utils_initialize_business_behavior_safe_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** code, eval\_globals, eval\_locals.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L7087) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L268)

<a id="op-356a55a40a04e2"></a>
### Create folder

`operation_foundation_utils_initialize_business_behavior_create_folder`

**Inputs** path, with\_init = false.

**Local steps**

- Bind dependencies touch\_file.
- If not os.path.exists(path).
  - Evaluate os.makedirs(path).
  - If with\_init.
    - Evaluate touch\_file(os.path.join(path, “\_\_init\_\_.py”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L7175) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L207)

<a id="op-3fda5ee4caa551"></a>
### Get Platform version

`operation_foundation_utils_initialize_business_behavior_get_foundation_version`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** getattr(Platform, “\_\_version\_\_”, “unknown”).

**Local steps**

- Return getattr(Platform, “\_\_version\_\_”, “unknown”).

**Values supplied outside this operation** selected callable from getattr(Platform, “\_\_version\_\_”, “unknown”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L7337) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L229)

<a id="op-82b59eb5d5bc33"></a>
### Get app version

`operation_foundation_utils_initialize_business_behavior_get_application_version`

**Inputs** app\_name.

**Declared result** str.

**Explicit results** Platform.get\_attr((app\_name + “.\_\_version\_\_”)) · “0.0.1”.

**Local steps**

- Attempt the following.
  - Return Platform.get\_attr((app\_name + “.\_\_version\_\_”)).
- On failure (Exception).
  - Return “0.0.1”.

**Values supplied outside this operation** selected callable from Platform.get\_attr((app\_name + “.\_\_version\_\_”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L7389) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L214)

<a id="op-04327d36531a42"></a>
### Pulse host

`operation_foundation_utils_telemetry_pulse_utils_business_behavior_pulse_host`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** ensure\_http((nested operand in the contract.conf.get(“pulse\_host”) or DEFAULT\_PULSE\_HOST)).rstrip(“/”).

**Local steps**

- Return ensure\_http((nested operand in the contract.conf.get(“pulse\_host”) or DEFAULT\_PULSE\_HOST)).rstrip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“pulse\_host”) → DEFAULT\_PULSE\_HOST.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L1197) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2032) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L798)

<a id="op-d1adcf19a5a292"></a>
### Anonymize user

`operation_foundation_utils_telemetry_pulse_utils_business_behavior_anonymize_user`

**Inputs** user.

**Explicit results** user · formatted text user\_{user\_hash at slice no value to 12}.

**Local steps**

- If (not user or user belongs to Platform.STANDARD\_USERS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not user → user belongs to Platform.STANDARD\_USERS.
  - Return user.
- Set pattern from “^user\_&#91;a-f0-9&#93;{12}$”.
- If re.match(pattern, user).
  - Return user.
- Set site\_salt from (Platform.local.site or “default”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.site → “default”.
- Set hash\_input from formatted text {user}:{site\_salt}.encode().
- Set user\_hash from hashlib.sha256(hash\_input).hexdigest().
- Return formatted text user\_{user\_hash at slice no value to 12}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L1290) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L794)

<a id="op-f1bca52a44d272"></a>
### Parse interval

`operation_foundation_utils_telemetry_pulse_utils_business_behavior_parse_interval`

**Inputs** interval.

**Explicit results** no value · interval · int(interval) · (number × multipliers at unit).

**Explicit failure paths** ValueError(formatted text Invalid interval format: {interval}) · ValueError(formatted text Invalid time unit '{unit}'. Use: s, m, h, d, w, y).

**Local steps**

- If interval is identical to no value.
  - Return no value.
- If isinstance(interval, int).
  - Return interval.
- Set interval from str(interval).strip().lower().
- If interval at negative 1.isdigit().
  - Return int(interval).
- Set unit from interval at negative 1.
- Attempt the following.
  - Set number from int(interval at slice no value to negative 1).
- On failure (ValueError).
  - Raise ValueError(formatted text Invalid interval format: {interval}).
- Set multipliers from mapping(“s” → 1, “m” → 60, “h” → 3600, “d” → 86400, …).
- If unit does not belong to multipliers.
  - Raise ValueError(formatted text Invalid time unit '{unit}'. Use: s, m, h, d, w, y).
- Return (number × multipliers at unit).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L1584) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L797)

<a id="op-5458ec285f8f2d"></a>
### Utc iso

`operation_foundation_utils_telemetry_pulse_utils_business_behavior_coordinated_universal_time_iso`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** datetime.now(UTC).isoformat().

**Local steps**

- Return datetime.now(UTC).isoformat().

**Values supplied outside this operation** clock or generated value from datetime.now(UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L2068) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L795)

<a id="op-7e022fec3a474b"></a>
### Ensure http

`operation_foundation_utils_telemetry_pulse_utils_business_behavior_ensure_hypertext_transfer_protocol`

**Inputs** url.

**Declared result** str.

**Explicit results** url when url.startswith(tuple(text in the contract, text in the contract)), otherwise (text in the contract + url).

**Local steps**

- Return url when url.startswith(tuple(text in the contract, text in the contract)), otherwise (text in the contract + url).
  - Value choice on url.startswith(tuple(text in the contract, text in the contract)) — true gives url, false gives (text in the contract + url).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L2127) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L796)

## Service · Verified command

<a id="op-4ee979a77a9411"></a>
### Get signed params

`operation_foundation_utils_verified_command_business_behavior_get_signed_parameters`

**Inputs** params.

**Explicit results** ((params + “&amp;\_signature=”) + signature).

**Local steps**

- If not isinstance(params, str).
  - Set params from urlencode(params).
- Set signature from \_sign\_message(params).
- Return ((params + “&amp;\_signature=”) + signature).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1835) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1059)

<a id="op-79c5f7d1a7f62b"></a>
### Get secret

`operation_foundation_utils_verified_command_business_behavior_get_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1972) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1057)

<a id="op-7d1a68decd4041"></a>
### Verify request

`operation_foundation_utils_verified_command_business_behavior_verify_request`

**Inputs** no declared parameters.

**Explicit results** true · false.

**Local steps**

- Set query\_string from Platform.safe\_decode((Platform.local.flags.signed\_query\_string or getattr(Platform.request, “query\_string”, no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.signed\_query\_string → getattr(Platform.request, “query\_string”, no value).
- Set signature\_string from “&amp;\_signature=”.
- If signature\_string belongs to query\_string.
  - Set tuple(params, given\_signature) from query\_string.split(signature\_string).
  - Set computed\_signature from \_sign\_message(params).
  - Set valid\_signature from hmac.compare\_digest(given\_signature, computed\_signature).
  - Set valid\_method from Platform.request.method equals “GET”.
  - Set valid\_request\_data from not (Platform.request.form or Platform.request.data).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.request.form → Platform.request.data.
  - If (valid\_signature and valid\_method and valid\_request\_data).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in valid\_signature → valid\_method → valid\_request\_data.
    - Return true.
- Evaluate Platform.respond\_as\_web\_page(translated “Invalid Link”, translated “This link is invalid or expired. Please make sure you have pasted correctly.”).
- Return false.

**Values supplied outside this operation** selected callable from getattr(Platform.request, “query\_string”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L2053) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1061)

<a id="op-dd80b341e53f22"></a>
### Sign message

`operation_foundation_utils_verified_command_business_behavior_sign_message`

**Inputs** message.

**Declared result** str.

**Explicit results** hmac.new(get\_secret().encode(), message.encode(), digestmod = hashlib.sha512).hexdigest().

**Local steps**

- Return hmac.new(get\_secret().encode(), message.encode(), digestmod = hashlib.sha512).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L2452) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1060)

<a id="op-3d663d9ae90355"></a>
### Get url

`operation_foundation_utils_verified_command_business_behavior_get_resource_address`

**Inputs** cmd, params, nonce = no value, secret = no value.

**Explicit results** Platform.utils.get\_url(empty text.join(list(“api/method/”, cmd, “?”, urlencode(params)))).

**Local steps**

- If not nonce.
  - Set nonce from params.
- Set signature from get\_signature(params, nonce, secret).
- Set params at “signature” from signature.
- Return Platform.utils.get\_url(empty text.join(list(“api/method/”, cmd, “?”, urlencode(params)))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L2574) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1055)

<a id="op-759cdc7e5488f5"></a>
### Get signature

`operation_foundation_utils_verified_command_business_behavior_get_signature`

**Inputs** params, nonce, secret = no value.

**Explicit results** signature.hexdigest().

**Local steps**

- Set params from empty text.join(generator of Platform.utils.cstr(p) for p drawn from params.values()).
  - Draw p from params.values().
- If not secret.
  - Set secret from (Platform.local.conf.get(“secret”) or “secret”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.get(“secret”) → “secret”.
- Set signature from hmac.new(str(nonce), digestmod = hashlib.md5).
- Evaluate signature.update(secret).
- Evaluate signature.update(params).
- Return signature.hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L2792) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1058)

<a id="op-c7a4cf3753b6ce"></a>
### Verify using doc

`operation_foundation_utils_verified_command_business_behavior_verify_using_record`

**Inputs** doc, signature, cmd.

**Explicit results** signature equals get\_signature(params, doc.get\_nonce()).

**Local steps**

- Set params from doc.get\_signature\_params().
- Return signature equals get\_signature(params, doc.get\_nonce()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L3097) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1062)
