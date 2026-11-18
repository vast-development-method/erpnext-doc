# Integration and transport · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Cloud settings

<a id="op-e2e913c593f85f"></a>
### Uninstall app

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_uninstall_application`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_marketplace.uninstall(PilotClient(), app).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_marketplace.
- Return cloud\_marketplace.uninstall(PilotClient(), app).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L433) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L620)

<a id="op-db794edf9cded3"></a>
### Update apps

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_update_apps`

**Inputs** apps = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_marketplace.update(PilotClient(), apps).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_marketplace.
- Return cloud\_marketplace.update(PilotClient(), apps).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L566) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L621)

<a id="op-e141527a094ac6"></a>
### Pilot request

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_pilot_request`

**Inputs** method = empty text, path = empty text, data = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”, “POST”)).

**Declared result** (dict bitwise or list).

**Explicit results** client.\_request(method, client.site\_path(path), payload).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid Cloud Settings operation.” · validation helper with Platform.PermissionError — translated “Use POST for a Cloud Settings action.” · validation helper with Platform.ValidationError — translated “Invalid Cloud Settings data.”.

**Local steps**

- Evaluate \_assert\_access().
- If (not isinstance(method, str) or not isinstance(path, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(method, str) → not isinstance(path, str).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings operation.”, Platform.ValidationError).
- Set method from method.upper().
- Set path from path.strip(“/”).
- If (method differs from “GET” and (not Platform.request or Platform.request.method differs from “POST”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method differs from “GET” → (not Platform.request or Platform.request.method differs from “POST”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.request → Platform.request.method differs from “POST”.
  - Call the validation error handler Platform.throw(translated “Use POST for a Cloud Settings action.”, Platform.PermissionError).
- Evaluate \_validate\_pilot\_path(method, path).
- Set payload from Platform.parse\_json(data) when data, otherwise no value.
  - Value choice on data — true gives Platform.parse\_json(data), false gives no value.
- If (payload is distinct from no value and (method differs from “PATCH” or not isinstance(payload, dict))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in payload is distinct from no value → (method differs from “PATCH” or not isinstance(payload, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method differs from “PATCH” → not isinstance(payload, dict).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings data.”, Platform.ValidationError).
- Set client from PilotClient().
- Return client.\_request(method, client.site\_path(path), payload).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1487)

<a id="op-ec5aec5132a993"></a>
### Validate pilot path

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_validate_pilot_path`

**Inputs** method, path.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid Cloud Settings operation.” · validation helper with Platform.ValidationError — translated “Invalid Cloud Settings query.” · validation helper with Platform.ValidationError — translated “Invalid Cloud Settings time window.”.

**Local steps**

- Set parsed from urlsplit(path).
- If (parsed.scheme or parsed.netloc or parsed.fragment or not any(generator of re.fullmatch(route, parsed.path) for route drawn from PILOT\_PASSTHROUGH\_ROUTES.get(method, tuple()))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.scheme → parsed.netloc → parsed.fragment → not any(generator of re.fullmatch(route, parsed.path) for route drawn from PILOT\_PASSTHROUGH\_ROUTES.get(method, tuple())).
  - Draw route from PILOT\_PASSTHROUGH\_ROUTES.get(method, tuple()).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings operation.”, Platform.ValidationError).
- If not parsed.query.
  - Return no value.
- Attempt the following.
  - Set query from parse\_qs(parsed.query, keep\_blank\_values = true, strict\_parsing = true).
- On failure (ValueError).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings query.”, Platform.ValidationError).
- If (method differs from “GET” or parsed.path does not belong to set(“monitoring”, “uptime”) or set(query) differs from set(“window”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method differs from “GET” → parsed.path does not belong to set(“monitoring”, “uptime”) → set(query) differs from set(“window”).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings query.”, Platform.ValidationError).
- If (len(query at “window”) differs from 1 or query at “window” at 0 does not belong to set(“30m”, “1h”, “6h”, “12h”, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(query at “window”) differs from 1 → query at “window” at 0 does not belong to set(“30m”, “1h”, “6h”, “12h”, …).
  - Call the validation error handler Platform.throw(translated “Invalid Cloud Settings time window.”, Platform.ValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1488)

<a id="op-404db73def9ed6"></a>
### Get task

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_task`

**Inputs** task\_id.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** mapping() · response at “task” · response when isinstance(response, dict), otherwise mapping().

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Task id is required.”.

**Local steps**

- Evaluate \_assert\_access().
- Set task\_id from (task\_id or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in task\_id → empty text.
- If not task\_id.
  - Call the validation error handler Platform.throw(translated “Task id is required.”, Platform.ValidationError).
- Attempt the following.
  - Set client from PilotClient().
  - Set response from client.get(client.site\_path(formatted text tasks/{quote(task\_id, safe = empty text)})).
- On failure (Platform.ValidationError).
  - Evaluate Platform.clear\_last\_message().
  - Return mapping().
- If (isinstance(response, dict) and isinstance(response.get(“task”), dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(response, dict) → isinstance(response.get(“task”), dict).
  - Return response at “task”.
- Return response when isinstance(response, dict), otherwise mapping().
  - Value choice on isinstance(response, dict) — true gives response, false gives mapping().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L710) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L600)

<a id="op-8fc480217d7aab"></a>
### Get billing

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_billing`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** cloud\_billing.summary(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.summary(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1172) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L590)

<a id="op-f0343269725c4f"></a>
### Get plan options

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_plan_options`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** cloud\_billing.get\_plan\_options(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.get\_plan\_options(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1288) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L599)

<a id="op-8f91e0fe6f13a8"></a>
### Change plan

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_change_plan`

**Inputs** plan.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.change\_plan(PilotClient(), plan).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.change\_plan(PilotClient(), plan).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1404) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L581)

<a id="op-b3c18a6c8c2898"></a>
### Get billing profile

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_billing_profile`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** cloud\_billing.get\_profile(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.get\_profile(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1537) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L591)

<a id="op-50a9be4cb6c8fb"></a>
### Save billing profile

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_save_billing_profile`

**Inputs** remaining named values fields.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.save\_profile(PilotClient(), fields).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.save\_profile(PilotClient(), fields).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1653) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L618)

<a id="op-bd8a109338e572"></a>
### Get payment gateways

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_payment_gateways`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list.

**Explicit results** cloud\_billing.get\_gateways(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.get\_gateways(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1779) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L598)

<a id="op-05bb76a1a33560"></a>
### Add payment method

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_add_payment_method`

**Inputs** method\_type = “Card”, contact = no value, gateway = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.add\_payment\_method(PilotClient(), method\_type, contact, gateway).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.add\_payment\_method(PilotClient(), method\_type, contact, gateway).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L1895) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L579)

<a id="op-f8383f65822748"></a>
### Confirm payment method

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_confirm_payment_method`

**Inputs** remaining named values payload.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.confirm\_payment\_method(PilotClient(), payload).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.confirm\_payment\_method(PilotClient(), payload).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2086) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L583)

<a id="op-bc42b061584e2f"></a>
### Create payment method checkout

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_create_payment_method_checkout`

**Inputs** redirect\_url, gateway = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.create\_payment\_method\_checkout(PilotClient(), redirect\_url, gateway).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.create\_payment\_method\_checkout(PilotClient(), redirect\_url, gateway).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2212) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L585)

<a id="op-55759d70a8785e"></a>
### Confirm payment method checkout

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_confirm_payment_method_checkout`

**Inputs** reference.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.confirm\_payment\_method\_checkout(PilotClient(), reference).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.confirm\_payment\_method\_checkout(PilotClient(), reference).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2372) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L584)

<a id="op-ddb53aedbf36a7"></a>
### Remove payment method

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_remove_payment_method`

**Inputs** payment\_method.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.remove\_payment\_method(PilotClient(), payment\_method).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.remove\_payment\_method(PilotClient(), payment\_method).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2505) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L616)

<a id="op-f27d520a5a4c53"></a>
### Reconcile payment setup

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_reconcile_payment_setup`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.reconcile\_payment\_setup(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.reconcile\_payment\_setup(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2638) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L614)

<a id="op-3081b557cfbd3b"></a>
### Create topup checkout

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_create_topup_checkout`

**Inputs** amount, redirect\_url.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.create\_topup\_checkout(PilotClient(), amount, redirect\_url).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.create\_topup\_checkout(PilotClient(), amount, redirect\_url).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2754) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L586)

<a id="op-29bbb8cc1bc5b1"></a>
### Get invoices

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_get_invoices`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list.

**Explicit results** cloud\_billing.invoices(PilotClient()).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.invoices(PilotClient()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1485)

<a id="op-d7f9bf9644d746"></a>
### Get invoice pdf

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_get_invoice_pdf`

**Inputs** invoice.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.invoice\_pdf(PilotClient(), invoice).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.invoice\_pdf(PilotClient(), invoice).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1484)

<a id="op-55922f937cb308"></a>
### Create invoice checkout

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_settings_create_invoice_checkout`

**Inputs** invoice, redirect\_url.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.create\_invoice\_checkout(PilotClient(), invoice, redirect\_url).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.create\_invoice\_checkout(PilotClient(), invoice, redirect\_url).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1483)

<a id="op-11ce6d94f15282"></a>
### Get checkout status

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_get_checkout_status`

**Inputs** reference.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** cloud\_billing.checkout\_status(PilotClient(), reference).

**Local steps**

- Evaluate \_assert\_access().
- Bind dependencies cloud\_billing.
- Return cloud\_billing.checkout\_status(PilotClient(), reference).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L2903) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L593)

<a id="op-f3829246218b60"></a>
### Clean domain

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_clean_domain`

**Inputs** domain.

**Declared result** str.

**Explicit results** domain.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Domain is required.”.

**Local steps**

- Set domain from (domain or empty text).strip().lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in domain → empty text.
- If not domain.
  - Call the validation error handler Platform.throw(translated “Domain is required.”, Platform.ValidationError).
- Return domain.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L3036) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L582)

<a id="op-802aefee12dd8d"></a>
### Domain row

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_domain_row`

**Inputs** domain, primary, is\_default = false.

**Declared result** dict.

**Explicit results** mapping(“domain” → domain, “is\_default” → is\_default, “is\_primary” → domain equals primary).

**Local steps**

- Return mapping(“domain” → domain, “is\_default” → is\_default, “is\_primary” → domain equals primary).

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L3188) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L587)
