# Identity and access · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Auth

<a id="op-98e663210e5d29"></a>
### Validate oauth

`operation_foundation_auth_business_behavior_validate_delegated_authorization`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** authorization\_header.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L142)

<a id="op-a1931856ab5461"></a>
### Validate auth via api keys

`operation_foundation_auth_business_behavior_validate_authentication_via_application_programming_interface_keys`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** authorization\_header.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L7397) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L140)

<a id="op-a6dd28147de650"></a>
### Validate api key secret

`operation_foundation_auth_business_behavior_validate_application_programming_interface_key_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** api\_key, api\_secret, frappe\_authorization\_source.

**Locally raised failures** AuthenticationError.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L138)

<a id="op-e4d770d7bb90ef"></a>
### Validate auth via hooks

`operation_foundation_auth_business_behavior_validate_authentication_via_hooks`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L696) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L141)

<a id="op-54f63baeaf1e9d"></a>
### Check request ip

`operation_foundation_auth_business_behavior_check_request_internet_protocol`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0011.json#L784) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L91)

## Service · Concurrency limiter

<a id="op-f2727c4af2975c"></a>
### Web tier concurrency

`operation_foundation_concurrency_limiter_business_behavior_web_tier_concurrency`

**Inputs** no declared parameters.

**Wrappers, in declaration order** cache.

**Declared result** (int bitwise or no value).

**Explicit results** no value · (cfg.workers × cfg.threads).

**Local steps**

- If not os.environ.get(“SERVER\_SOFTWARE”, empty text).startswith(“gunicorn”).
  - Return no value.
- Attempt the following.
  - Set cfg from \_gunicorn\_config().
- On failure (SystemExit).
  - Return no value.
- Return (cfg.workers × cfg.threads).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L150) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L774)

<a id="op-210b87c3450702"></a>
### Gunicorn config

`operation_foundation_binding_foundation_concurrency_limiter_gunicorn_config`

**Inputs** no declared parameters.

**Explicit results** Settings().cfg.

**Local steps**

- Bind dependencies Application.
- Bind dependencies get\_default\_config\_file.
- Bind local type Settings (class body executes during definition).
- Return Settings().cfg.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L576)

<a id="op-8c7c2b262fd5b7"></a>
### Gunicorn config.Settings.get config from filename

`operation_foundation_binding_foundation_concurrency_limiter_gunicorn_config_settings_get_config_from_filename`

**Inputs** self, filename.

**Explicit results** vars(config) · super().get\_config\_from\_filename(filename).

**Local steps**

- If config bound to sys.modules.get(“\_\_config\_\_”).
  - Return vars(config).
- Return super().get\_config\_from\_filename(filename).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L577)

<a id="op-61ccc9d26bad50"></a>
### Gunicorn config.Settings.load config

`operation_foundation_binding_foundation_concurrency_limiter_gunicorn_config_settings_load_config`

**Inputs** self.

**Local steps**

- Set parser from self.cfg.parser().
- Set args from parser.parse\_args(sys.argv at slice 1 to no value).
- Set env\_args from parser.parse\_args(self.cfg.get\_cmd\_args\_from\_env()).
- If config\_file bound to (args.config or env\_args.config or get\_default\_config\_file()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.config → env\_args.config → get\_default\_config\_file().
  - Evaluate self.load\_config\_from\_file(config\_file).
- For each parsed in tuple(env\_args, args).
  - For each tuple(name, value) in vars(parsed).items().
    - If (value is distinct from no value and name differs from “args”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → name differs from “args”.
      - Evaluate self.cfg.set(name.lower(), value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L578)

<a id="op-24f8457513d04a"></a>
### Default limit

`operation_foundation_concurrency_limiter_business_behavior_default_limit`

**Inputs** no declared parameters.

**Declared result** (int bitwise or no value).

**Explicit results** max(1, (capacity floor divide 2)) when capacity, otherwise no value.

**Local steps**

- Set capacity from web\_tier\_concurrency().
- Return max(1, (capacity floor divide 2)) when capacity, otherwise no value.
  - Value choice on capacity — true gives max(1, (capacity floor divide 2)), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L4407) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L772)

<a id="op-27c98915706e5f"></a>
### Concurrent limit

`operation_foundation_concurrency_limiter_business_behavior_concurrent_limit`

**Inputs** limit = no value, wait\_timeout = \_DEFAULT\_WAIT\_TIMEOUT.

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L4875) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L769)

<a id="op-1e327eb80866b4"></a>
### Concurrent limit.decorator

`operation_foundation_concurrency_limiter_business_behavior_concurrent_limit_decorator`

**Inputs** fn.

**Declared result** Callable.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L5599) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L770)

<a id="op-f871e4bc82338b"></a>
### Concurrent limit.decorator.wrapper

`operation_foundation_concurrency_limiter_business_behavior_concurrent_limit_decorator_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs).

**Explicit failure paths** exc.

**Local steps**

- If getattr(Platform.local, “request”, no value) is identical to no value.
  - Return fn(expanded args, expanded names kwargs).
- Set \_limit from cint(limit) when limit is distinct from no value, otherwise \_default\_limit().
  - Value choice on limit is distinct from no value — true gives cint(limit), false gives \_default\_limit().
- If \_limit is identical to no value.
  - Return fn(expanded args, expanded names kwargs).
- Set key from formatted text concurrency:{fn.\_\_module\_\_}.{fn.\_\_qualname\_\_}.
- Set sem from RedisSemaphore(key, \_limit, wait\_timeout, shared = true).
- Set token from sem.acquire().
- If not token.
  - Set retry\_after from max(1, int(wait\_timeout)).
  - If headers bound to getattr(Platform.local, “response\_headers”, no value) is distinct from no value.
    - Evaluate headers.set(“Retry-After”, str(retry\_after)).
  - Set exc from ServiceUnavailableError(Platform.\_(“Server is busy. Please try again in a few seconds.”)).
  - Set exc.retry\_after from retry\_after.
  - Raise exc.
- Attempt the following.
  - Return fn(expanded args, expanded names kwargs).
- On exit, including pending return or failure.
  - Evaluate sem.release(token).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value), getattr(Platform.local, “response\_headers”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L6269) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L771)

<a id="op-a46f5a21672c27"></a>
### Get stats

`operation_foundation_concurrency_limiter_business_behavior_get_stats`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“default\_limit” → \_default\_limit(), “web\_tier\_concurrency” → web\_tier\_concurrency()).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Return mapping(“default\_limit” → \_default\_limit(), “web\_tier\_concurrency” → web\_tier\_concurrency()).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0031.json#L6908) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L773)

## Service · Oauth

<a id="op-c701cae2333894"></a>
### OAuth Web Request Validator.validate client id

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_client_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, request, args, kwargs.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L28) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1591)

<a id="op-2f02a313a381d4"></a>
### OAuth Web Request Validator.validate redirect uri

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_redirect_resource_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, redirect\_uri, request, args, kwargs.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L32) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1595)

<a id="op-649adc30739fd9"></a>
### OAuth Web Request Validator.get default redirect uri

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_default_redirect_resource_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, request, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L23) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1581)

<a id="op-b01d7d83ab274d"></a>
### OAuth Web Request Validator.validate scopes

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_scopes`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, scopes, client, request, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L5756) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1598)

<a id="op-5f777cfaae3994"></a>
### OAuth Web Request Validator.get default scopes

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_default_scopes`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, request, args, kwargs.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L5902) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1582)

<a id="op-00e967de1f01c8"></a>
### OAuth Web Request Validator.validate response type

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_response_type`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, response\_type, client, request, args, kwargs.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L6008) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1597)

<a id="op-e46a47c6db2ab1"></a>
### OAuth Web Request Validator.save authorization code

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_save_authorization_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, request, args, kwargs.

**Observed service boundaries** record mutation request, transaction control.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L6145) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1588)

<a id="op-364d35851e3e3b"></a>
### OAuth Web Request Validator.authenticate client

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_authenticate_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, request, args, kwargs.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L20) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1575)

<a id="op-228f3d86934d81"></a>
### OAuth Web Request Validator.authenticate client id

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_authenticate_client_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, request, args, kwargs.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L21) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1576)

<a id="op-ea74d6b93d110d"></a>
### OAuth Web Request Validator.validate code

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, client, request, args, kwargs.

**Explicit result forms** Boolean false, Boolean true, a comparison result.

**Observed service boundaries** record lookup, record mutation request, transaction control.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L29) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1592)
