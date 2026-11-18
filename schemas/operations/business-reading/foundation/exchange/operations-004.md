# Integration and transport · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Cloud settings

<a id="op-90523f8b526c39"></a>
### Pilot Client.post

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_post`

**Inputs** self, path, data = no value.

**Declared result** dict.

**Explicit results** self.\_request(“POST”, path, data).

**Local steps**

- Return self.\_request(“POST”, path, data).

**Methods declared on this owner** [request](operations-004.md#op-278aaf3d352265).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3642) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L611)

<a id="op-4665c49a48ff10"></a>
### Pilot Client.patch

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_patch`

**Inputs** self, path, data = no value.

**Declared result** dict.

**Explicit results** self.\_request(“PATCH”, path, data).

**Local steps**

- Return self.\_request(“PATCH”, path, data).

**Methods declared on this owner** [request](operations-004.md#op-278aaf3d352265).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3743) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L610)

<a id="op-e560c21c997f34"></a>
### Pilot Client.delete

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_delete`

**Inputs** self, path, data = no value.

**Declared result** dict.

**Explicit results** self.\_request(“DELETE”, path, data).

**Local steps**

- Return self.\_request(“DELETE”, path, data).

**Methods declared on this owner** [request](operations-004.md#op-278aaf3d352265).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3844) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L603)

<a id="op-af5dca236068cd"></a>
### Pilot Client.site path

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_site_path`

**Inputs** self, path.

**Declared result** str.

**Explicit results** formatted text sites/{quote(self.site, safe = empty text)}/{path.lstrip(“/”)}.

**Local steps**

- Return formatted text sites/{quote(self.site, safe = empty text)}/{path.lstrip(“/”)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3945) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L613)

<a id="op-b0eeaf2f38154c"></a>
### Pilot Client.domain path

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_domain_path`

**Inputs** self, domain, suffix = empty text.

**Declared result** str.

**Explicit results** self.site\_path(formatted text {path}/{suffix.lstrip(“/”)} when suffix, otherwise path).

**Local steps**

- Set path from formatted text domains/{quote(domain, safe = empty text)}.
- Return self.site\_path(formatted text {path}/{suffix.lstrip(“/”)} when suffix, otherwise path).
  - Value choice on suffix — true gives formatted text {path}/{suffix.lstrip(“/”)}, false gives path.

**Methods declared on this owner** [site path](operations-004.md#op-af5dca236068cd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L4070) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L604)

<a id="op-278aaf3d352265"></a>
### Pilot Client.request

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_request`

**Inputs** self, method, path, data = no value.

**Explicit results** payload.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Could not reach your server: {0}”.format(str(exc)) · validation helper with CloudMigrationConflictError when self.\_error\_code(payload) equals “migration\_conflict”, otherwise Platform.ValidationError — (self.\_error\_message(payload) or response.text or translated “Request to your server failed.”).

**Local steps**

- Bind dependencies requests.
- Attempt the following.
  - Set response from requests.request(method, formatted text {self.endpoint}/api/v1/{path.lstrip(“/”)}, json = data, headers = mapping(“Authorization” → formatted text Bearer {self.token}), timeout = (cint(Platform.conf.get(“c ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.get(“cloud\_settings\_timeout”)) → 30.
- On failure (requests.RequestException) bound to exc.
  - Call the validation error handler Platform.throw(translated “Could not reach your server: {0}”.format(str(exc)), Platform.ValidationError).
- Set payload from self.\_parse(response).
- If response.ok.
  - Return payload.
- Call the validation error handler Platform.throw((self.\_error\_message(payload) or response.text or translated “Request to your server failed.”), CloudMigrationConflictError when self.\_error\_code(payload) equals “migration\_conflict”, otherw ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_error\_message(payload) → response.text → translated “Request to your server failed.”.
  - Value choice on self.\_error\_code(payload) equals “migration\_conflict” — true gives CloudMigrationConflictError, false gives Platform.ValidationError.

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse](operations-004.md#op-98180296f246aa), [error message](operations-004.md#op-0dc45a70e07bae), [error code](operations-004.md#op-20aeb019464b5c).

**Values supplied outside this operation** service or queued work from requests.request(method, formatted text {self.endpoint}/api/v1/{path.lstrip(“/”)}, json = data, headers = mapping(“Authorization” → formatted text Bearer {self.token}), timeout = (cint(Platform.conf.get(“c ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L49) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L612)

<a id="op-20aeb019464b5c"></a>
### Pilot Client.error code

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_error_code`

**Inputs** payload.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** str((error.get(“code”) or empty text)) when isinstance(error, dict), otherwise empty text.

**Local steps**

- Set error from payload.get(“error”) when isinstance(payload, dict), otherwise no value.
  - Value choice on isinstance(payload, dict) — true gives payload.get(“error”), false gives no value.
- Return str((error.get(“code”) or empty text)) when isinstance(error, dict), otherwise empty text.
  - Value choice on isinstance(error, dict) — true gives str((error.get(“code”) or empty text)), false gives empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in error.get(“code”) → empty text.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L4857) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L605)

<a id="op-98180296f246aa"></a>
### Pilot Client.parse

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_parse`

**Inputs** response.

**Wrappers, in declaration order** staticmethod.

**Explicit results** response.json() · mapping().

**Local steps**

- Attempt the following.
  - Return response.json().
- On failure (ValueError).
  - Return mapping().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L5031) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L609)

<a id="op-0dc45a70e07bae"></a>
### Pilot Client.error message

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_error_message`

**Inputs** payload.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** empty text · str(error) when error, otherwise empty text.

**Local steps**

- If not isinstance(payload, dict).
  - Return empty text.
- Set error from (payload.get(“error”) or payload.get(“message”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payload.get(“error”) → payload.get(“message”).
- If isinstance(error, dict).
  - Set error from (error.get(“message”) or error.get(“detail”) or error.get(“error”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in error.get(“message”) → error.get(“detail”) → error.get(“error”).
- Return str(error) when error, otherwise empty text.
  - Value choice on error — true gives str(error), false gives empty text.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L5112) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L606)

<a id="op-7a486cffe04d02"></a>
### Is v2 site

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_is_v2_site`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool((Platform.conf.get(“pilot\_endpoint”) and Platform.conf.get(“pilot\_auth\_token”))).

**Local steps**

- Return bool((Platform.conf.get(“pilot\_endpoint”) and Platform.conf.get(“pilot\_auth\_token”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.get(“pilot\_endpoint”) → Platform.conf.get(“pilot\_auth\_token”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1486)

<a id="op-7fc4861f40795a"></a>
### Is cloud settings enabled

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_is_cloud_settings_enabled`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · CLOUD\_SETTINGS\_ROLE belongs to Platform.get\_roles().

**Local steps**

- If not is\_v2\_site().
  - Return false.
- If Platform.session.user equals “Guest”.
  - Return false.
- Return CLOUD\_SETTINGS\_ROLE belongs to Platform.get\_roles().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L48) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L602)

<a id="op-35bb3d818944ee"></a>
### Get boot context

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_boot_context`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“enabled” → false) · \_safe\_context().

**Local steps**

- If not is\_cloud\_settings\_enabled().
  - Return mapping(“enabled” → false).
- Return \_safe\_context().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L5559) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L592)

<a id="op-7b3b907d908f7f"></a>
### Assert access

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_assert_access`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have access to Cloud Settings for this site.”.

**Local steps**

- If not is\_cloud\_settings\_enabled().
  - Call the validation error handler Platform.throw(translated “You do not have access to Cloud Settings for this site.”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L5647) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L580)

<a id="op-cafd9b27d92768"></a>
### Safe context

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_safe_context`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“enabled” → true, “provider” → (Platform.conf.get(“cloud\_provider”) or “Platform\_cloud”), “site\_name” → Platform.local.site, “server\_url” → (Platform.conf.get(“cloud\_server\_url”) or Platform.conf.g ….

**Local steps**

- Return mapping(“enabled” → true, “provider” → (Platform.conf.get(“cloud\_provider”) or “Platform\_cloud”), “site\_name” → Platform.local.site, “server\_url” → (Platform.conf.get(“cloud\_server\_url”) or Platform.conf.g ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“cloud\_provider”) → “Platform\_cloud”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“cloud\_server\_url”) → Platform.conf.get(“pilot\_endpoint”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L5740) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L617)

<a id="op-30e044a2f03c6b"></a>
### Embed bundle

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_embed_bundle`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping() · mapping(“js” → formatted text {base}/embed/cloud-settings/cloud-settings.js{query}, “module” → formatted text {base}/embed/cloud-settings/esm/cloud-settings.js{query}).

**Local steps**

- Set base from (Platform.conf.get(“cloud\_settings\_embed\_url”) or Platform.conf.get(“pilot\_endpoint”) or empty text).rstrip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“cloud\_settings\_embed\_url”) → Platform.conf.get(“pilot\_endpoint”) → empty text.
- If not base.
  - Return mapping().
- Set version from Platform.conf.get(“cloud\_settings\_embed\_version”).
- Set query from formatted text ?v={quote(str(version), safe = empty text)} when version, otherwise empty text.
  - Value choice on version — true gives formatted text ?v={quote(str(version), safe = empty text)}, false gives empty text.
- Return mapping(“js” → formatted text {base}/embed/cloud-settings/cloud-settings.js{query}, “module” → formatted text {base}/embed/cloud-settings/esm/cloud-settings.js{query}).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L45) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L588)

<a id="op-d88fba9f1d3a28"></a>
### Get context

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_context`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** \_safe\_context().

**Local steps**

- Evaluate \_assert\_access().
- Return \_safe\_context().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L6249) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L594)

<a id="op-7365d8b561571c"></a>
### Get account url

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_account_resource_address`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** response when isinstance(response, dict), otherwise mapping().

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Set response from client.get(client.site\_path(“account-url”)).
- Return response when isinstance(response, dict), otherwise mapping().
  - Value choice on isinstance(response, dict) — true gives response, false gives mapping().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L6340) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L589)

<a id="op-4bc67de5ec8ec4"></a>
### Get domains

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_domains`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** mapping(“primary” → primary, “domains” → list(rows.values())).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Pilot returned an invalid domain.”.

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Set response from client.get(client.site\_path(“domains”)).
- Set primary from (response.get(“primary”) or client.site).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in response.get(“primary”) → client.site.
- Set rows from mapping(client.site → \_domain\_row(client.site, primary, is\_default = true)).
- For each route in (response.get(“domains”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in response.get(“domains”) → list().
  - Set domain from route.get(“domain”) when isinstance(route, dict), otherwise route.
    - Value choice on isinstance(route, dict) — true gives route.get(“domain”), false gives route.
  - If (not isinstance(domain, str) or not domain).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(domain, str) → not domain.
    - Call the validation error handler Platform.throw(translated “Pilot returned an invalid domain.”, Platform.ValidationError).
  - Set row from \_domain\_row(domain, primary, is\_default = domain equals client.site).
  - If isinstance(route, dict).
    - Evaluate row.update(public\_scheme = route.get(“public\_scheme”), tls = bool(route.get(“tls”))).
  - Set rows at domain from row.
- Return mapping(“primary” → primary, “domains” → list(rows.values())).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L47) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L596)

<a id="op-0442277de19c87"></a>
### Get domain dns records

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_domain_dns_records`

**Inputs** domain.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** mapping(“records” → list(expanded records.get(“cname”, list()), expanded records.get(“a”, list())), “cname” → records.get(“cname”, list()), “a” → records.get(“a”, list())).

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Set records from (client.get(client.domain\_path(\_clean\_domain(domain), “dns-records”)) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in client.get(client.domain\_path(\_clean\_domain(domain), “dns-records”)) → mapping().
- Return mapping(“records” → list(expanded records.get(“cname”, list()), expanded records.get(“a”, list())), “cname” → records.get(“cname”, list()), “a” → records.get(“a”, list())).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L46) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L595)

<a id="op-3c8909bde0f48f"></a>
### Add domain

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_add_domain`

**Inputs** domain.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** client.post(client.site\_path(“domains”), mapping(“domain” → \_clean\_domain(domain))).

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Return client.post(client.site\_path(“domains”), mapping(“domain” → \_clean\_domain(domain))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L7142) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L578)

<a id="op-420d76275e4b87"></a>
### Remove domain

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_remove_domain`

**Inputs** domain.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** client.delete(client.domain\_path(\_clean\_domain(domain))).

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Return client.delete(client.domain\_path(\_clean\_domain(domain))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L7325) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L615)

<a id="op-52eb0e4d890bbf"></a>
### Set primary domain

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_set_primary_domain`

**Inputs** domain.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** client.patch(client.domain\_path(\_clean\_domain(domain)), mapping(“primary” → true)).

**Local steps**

- Evaluate \_assert\_access().
- Set client from PilotClient().
- Return client.patch(client.domain\_path(\_clean\_domain(domain)), mapping(“primary” → true)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L619)

<a id="op-e266252d201f8d"></a>
### Get marketplace apps

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_marketplace_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** cloud\_marketplace.list\_apps(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_marketplace.
- Return cloud\_marketplace.list\_apps(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L184) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L597)

<a id="op-2733e9baba0a09"></a>
### Install app

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_install_application`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_marketplace.install(PilotClient(), app).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_marketplace.
- Return cloud\_marketplace.install(PilotClient(), app).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L300) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L601)
