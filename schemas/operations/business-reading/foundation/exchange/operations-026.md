# Integration and transport · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Oauth2 logins

<a id="op-a0c911e2feca94"></a>
### Login via salesforce

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_salesforce`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L4111) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L678)

<a id="op-f3a581422b9d53"></a>
### Login via fairlogin

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_fairlogin`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L4226) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L672)

<a id="op-9381921b3cc64c"></a>
### Login via keycloak

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_keycloak`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L4341) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L676)

<a id="op-d2d3ce7ce07f3c"></a>
### Custom

`operation_foundation_integrations_oauth2_logins_business_behavior_custom`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L4456) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L669)

<a id="op-6112e119729a84"></a>
### Decoder compat

`operation_foundation_integrations_oauth2_logins_business_behavior_decoder_compat`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** b.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L4734) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L670)

## Service · Platform providers

<a id="op-e73f6ff10d1bfc"></a>
### Migrate to

`operation_foundation_integrations_application_foundation_providers_initialize_business_behavior_migrate_to`

**Inputs** no declared parameters.

**Explicit results** Platformcloud\_migrator().

**Local steps**

- Bind dependencies Platformcloud\_migrator.
- Return Platformcloud\_migrator().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6454) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L636)

## Service · Platformcloud

<a id="op-847b7b7b52c216"></a>
### Get remote script

`operation_foundation_integrations_application_foundation_providers_frappecloud_business_behavior_get_remote_script`

**Inputs** remote\_site.

**Explicit results** no value · request.json() at “message”.

**Local steps**

- Evaluate print(“Retrieving Site Migrator...”).
- Set request\_url from formatted command or address in the contract.
- Set request from requests.get(request\_url).
- If (request.status\_code ÷ 100) differs from 2.
  - Evaluate print(formatted text Request exited with Status Code: {request.status\_code} Payload: {html2text(request.text)}).
  - Evaluate click.secho(“Some errors occurred while recovering the migration script. Please contact us @ Platform Cloud if this issue …”, fg = “yellow”).
  - Return no value.
- Return request.json() at “message”.

**Values supplied outside this operation** service or queued work from requests.get(request\_url).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L3321) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L634)

<a id="op-13fcd4754d1db1"></a>
### Platformcloud migrator

`operation_foundation_integrations_application_foundation_providers_frappecloud_business_behavior_managed_hosting_migrator`

**Inputs** no declared parameters.

**Local steps**

- Set remote\_site\_name from “Platformcloud.com”.
- Set script\_contents from get\_remote\_script(remote\_site = remote\_site\_name).
- Bind dependencies os.
- Bind dependencies sys.
- Bind dependencies tempfile.
- Set py from sys.executable.
- Set script from tempfile.NamedTemporaryFile(mode = “w”).
- Evaluate script.write(script\_contents).
- Evaluate print(formatted text Site Migrator stored at {script.name}).
- Evaluate os.execv(py, list(py, script.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L3608) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L635)

## Service · Platformcloud billing

<a id="op-12835289c84310"></a>
### Get base url

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_get_base_resource_address`

**Inputs** no declared parameters.

**Explicit results** url.

**Local steps**

- Set url from text in the contract.
- If (Platform.conf.developer\_mode and Platform.conf.get(“fc\_base\_url”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.conf.get(“fc\_base\_url”).
  - Set url from Platform.conf.get(“fc\_base\_url”).
- Return url.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L3865) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L624)

<a id="op-79def2fb06937b"></a>
### Get site login url

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_get_site_login_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L51) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L626)

<a id="op-e19fb4d527284c"></a>
### Get site name

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_get_site_name`

**Inputs** no declared parameters.

**Explicit results** site\_name.

**Local steps**

- Set site\_name from Platform.local.site.
- If (Platform.conf.developer\_mode and Platform.conf.get(“saas\_billing\_site\_name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.conf.get(“saas\_billing\_site\_name”).
  - Set site\_name from Platform.conf.get(“saas\_billing\_site\_name”).
- Return site\_name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L4043) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L627)

<a id="op-fc544bd702dc79"></a>
### Mock billing enabled

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_mock_billing_enabled`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool((Platform.conf.developer\_mode and Platform.conf.get(“mock\_fc\_billing”))).

**Local steps**

- Return bool((Platform.conf.developer\_mode and Platform.conf.get(“mock\_fc\_billing”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.conf.get(“mock\_fc\_billing”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L4174) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L629)

<a id="op-ec3f7db0bb4881"></a>
### Mock site info

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_mock_site_info`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“name” → site\_name, “site\_name” → site\_name, “base\_url” → get\_base\_url(), “trial\_end\_date” → add\_days(nowdate(), trial\_days), …).

**Local steps**

- Bind dependencies add\_days, cint, nowdate.
- Set trial\_days from (cint(Platform.conf.get(“mock\_fc\_trial\_days”)) or 7).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.get(“mock\_fc\_trial\_days”)) → 7.
- Set site\_name from get\_site\_name().
- Return mapping(“name” → site\_name, “site\_name” → site\_name, “base\_url” → get\_base\_url(), “trial\_end\_date” → add\_days(nowdate(), trial\_days), …).

**Values supplied outside this operation** clock or generated value from nowdate() · configured or stored value from Platform.get\_system\_settings(“setup\_complete”).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L4256) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L630)

<a id="op-411dcbcdb7d6a4"></a>
### Get headers

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_get_headers`

**Inputs** no declared parameters.

**Explicit results** mapping(“X-Site-Token” → Platform.conf.get(“fc\_communication\_secret”), “X-Site-User” → Platform.session.user, “X-Site” → get\_site\_name()).

**Explicit failure paths** validation helper — translated “You are not allowed to access this resource” · validation helper — translated “Communication secret not set”.

**Local steps**

- If Platform.get\_roles(Platform.session.user).count(“System Manager”) equals 0.
  - Call the validation error handler Platform.throw(translated “You are not allowed to access this resource”).
- If not Platform.conf.get(“fc\_communication\_secret”).
  - Call the validation error handler Platform.throw(translated “Communication secret not set”).
- Return mapping(“X-Site-Token” → Platform.conf.get(“fc\_communication\_secret”), “X-Site-User” → Platform.session.user, “X-Site” → get\_site\_name()).

**Values supplied outside this operation** effective access from Platform.get\_roles(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L4558) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L625)

<a id="op-6a86ef2f5017b9"></a>
### Post

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_post`

**Inputs** method, json = no value.

**Explicit results** requests.post(formatted text {get\_base\_url()}/api/method/{method}, headers = get\_headers(), json = json, timeout = tuple(5, 10)).

**Local steps**

- Bind dependencies requests.
- Return requests.post(formatted text {get\_base\_url()}/api/method/{method}, headers = get\_headers(), json = json, timeout = tuple(5, 10)).

**Values supplied outside this operation** service or queued work from requests.post(formatted text {get\_base\_url()}/api/method/{method}, headers = get\_headers(), json = json, timeout = tuple(5, 10)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L4833) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L631)

<a id="op-259553dd9ef211"></a>
### Current site info

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_current_site_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mock\_site\_info() · cached\_data · no value · site\_info.

**Local steps**

- Bind dependencies requests.
- Bind dependencies cint.
- Evaluate Platform.only\_for(“System Manager”).
- If mock\_billing\_enabled().
  - Return mock\_site\_info().
- Set cache\_key from formatted text fc\_current\_site\_info:{Platform.local.site}.
- Set cached\_data from Platform.cache().get\_value(cache\_key).
- If cached\_data.
  - Return cached\_data.
- Set res from mapping().
- Attempt the following.
  - Set request from post(“press.saas.api.site.info”).
- On failure (requests.RequestException).
  - Return no value.
- If request.status\_code equals 200.
  - Set res from request.json().get(“message”).
  - If (not res or not isinstance(res, dict)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not res → not isinstance(res, dict).
    - Return no value.
- Set site\_info from mapping(expand res, “site\_name” → get\_site\_name(), “base\_url” → get\_base\_url(), “setup\_complete” → cint(Platform.get\_system\_settings(“setup\_complete”))).
- Evaluate Platform.cache().set\_value(cache\_key, site\_info, expires\_in\_sec = 600).
- Return site\_info.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · configured or stored value from Platform.get\_system\_settings(“setup\_complete”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L50) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L623)

<a id="op-e8ad0fb8e87e40"></a>
### Api

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_application_programming_interface`

**Inputs** method, data = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** request.json().get(“message”).

**Explicit failure paths** validation helper — \_(“Failed while calling API {0}”, method).

**Local steps**

- If data is identical to no value.
  - Set data from mapping().
- Set request from post(formatted text press.saas.api.{method}, json = data).
- If request.status\_code equals 200.
  - Return request.json().get(“message”).
- Otherwise.
  - Call the validation error handler Platform.throw(\_(“Failed while calling API {0}”, method)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L5547) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L622)

<a id="op-d6679a504ed79e"></a>
### Is fc site

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_is_fc_site`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Explicit results** false · bool((mock\_billing\_enabled() or Platform.conf.get(“fc\_communication\_secret”))).

**Local steps**

- Set is\_system\_manager from Platform.get\_roles(Platform.session.user).count(“System Manager”).
- If not is\_system\_manager.
  - Return false.
- Return bool((mock\_billing\_enabled() or Platform.conf.get(“fc\_communication\_secret”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in mock\_billing\_enabled() → Platform.conf.get(“fc\_communication\_secret”).

**Values supplied outside this operation** effective access from Platform.get\_roles(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L5847) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L628)

<a id="op-c68e3b7c137805"></a>
### Send verification code

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_send_verification_code`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** request.json().get(“message”).

**Explicit failure paths** validation helper — translated “Failed to request login to Platform Cloud”.

**Local steps**

- Set request from post(“press.api.developer.saas.send\_verification\_code”, json = mapping(“domain” → get\_site\_name())).
- If request.status\_code equals 200.
  - Return request.json().get(“message”).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Failed to request login to Platform Cloud”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6025) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L632)

<a id="op-9b745fd04c4926"></a>
### Verify verification code

`operation_foundation_integrations_application_foundation_providers_frappecloud_billing_business_behavior_verify_verification_code`

**Inputs** verification\_code, route.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“base\_url” → get\_base\_url(), “login\_token” → request.json() at “login\_token”).

**Explicit failure paths** validation helper — translated “Invalid Code. Please try again.”.

**Local steps**

- Set request from post(“press.api.developer.saas.verify\_verification\_code”, json = mapping(“domain” → get\_site\_name(), “verification\_code” → verification\_code, “route” → route)).
- If request.status\_code equals 200.
  - Return mapping(“base\_url” → get\_base\_url(), “login\_token” → request.json() at “login\_token”).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Invalid Code. Please try again.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6236) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L633)

## Service · Platformmail

<a id="op-f031306d13a0b5"></a>
### Platform Mail.initialize

`operation_foundation_email_frappemail_business_behavior_foundation_mail_initialize`

**Inputs** self, site, email, api\_key = no value, api\_secret = no value, access\_token = no value.

**Declared result** no value.

**Local steps**

- Set self.site from site.
- Set self.email from email.
- Set self.api\_key from api\_key.
- Set self.api\_secret from api\_secret.
- Set self.access\_token from access\_token.
- Set self.client from self.get\_client(self.site, self.email, self.api\_key, self.api\_secret, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get client](operations-026.md#op-8046d4fb9bd155).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L2255) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1487)

<a id="op-8046d4fb9bd155"></a>
### Platform Mail.get client

`operation_foundation_email_frappemail_business_behavior_foundation_mail_get_client`

**Inputs** site, email, api\_key = no value, api\_secret = no value, access\_token = no value.

**Wrappers, in declaration order** staticmethod.

**Declared result** (PlatformClient bitwise or PlatformOAuth2Client).

**Explicit results** client.

**Local steps**

- If hasattr(Platform.local, “Platform\_mail\_clients”).
  - If client bound to Platform.local.Platform\_mail\_clients.get(email).
    - Return client.
- Otherwise.
  - Set Platform.local.Platform\_mail\_clients from mapping().
- Set client from PlatformOAuth2Client(url = site, access\_token = access\_token) when access\_token, otherwise PlatformClient(url = site, api\_key = api\_key, api\_secret = api\_secret).
  - Value choice on access\_token — true gives PlatformOAuth2Client(url = site, access\_token = access\_token), false gives PlatformClient(url = site, api\_key = api\_key, api\_secret = api\_secret).
- Set Platform.local.Platform\_mail\_clients at email from client.
- Return client.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L2543) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1486)

<a id="op-30c8cfc34c6cf0"></a>
### Platform Mail.request

`operation_foundation_email_frappemail_business_behavior_foundation_mail_request`

**Inputs** self, method, endpoint, params = no value, data = no value, json = no value, files = no value, headers = no value, timeout = tuple(60, 120), raw\_response = false.

**Declared result** (Any bitwise or no value).

**Explicit results** response.json() · self.client.post\_process(response).

**Local steps**

- Set url from urljoin(self.client.url, endpoint).
- Set headers from (headers or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in headers → mapping().
- Evaluate headers.update(self.client.headers).
- If files.
  - Evaluate headers.pop(“content-type”, no value).
- Set response from self.client.session.request(method = method, url = url, params = params, data = data, …).
- Evaluate raise\_for\_status(response).
- If raw\_response.
  - Return response.json().
- Return self.client.post\_process(response).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L2897) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1489)

<a id="op-314b9af3b56c6b"></a>
### Platform Mail.validate

`operation_foundation_email_frappemail_business_behavior_foundation_mail_validate`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set endpoint from “/auth/validate”.
- Set data from mapping(“email” → self.email).
- Evaluate self.request(“POST”, endpoint = endpoint, data = data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [request](operations-026.md#op-30c8cfc34c6cf0).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L3467) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1491)
