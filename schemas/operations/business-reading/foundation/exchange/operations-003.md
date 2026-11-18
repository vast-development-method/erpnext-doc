# Integration and transport · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Cloud billing

<a id="op-9771e2a5aa3ef9"></a>
### Confirm payment method

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_confirm_payment_method`

**Inputs** client, payload.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “confirm\_payment\_method”), payload).

**Local steps**

- Return client.post(\_path(client, “confirm\_payment\_method”), payload).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L182) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L556)

<a id="op-6a46bf21e0222d"></a>
### Remove payment method

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_remove_payment_method`

**Inputs** client, payment\_method.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “remove\_payment\_method”), mapping(“payment\_method” → payment\_method)).

**Local steps**

- Return client.post(\_path(client, “remove\_payment\_method”), mapping(“payment\_method” → payment\_method)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L273) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L565)

<a id="op-98282131bb58ec"></a>
### Create payment method checkout

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_create_payment_method_checkout`

**Inputs** client, redirect\_url, gateway = no value.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “create\_payment\_method\_checkout”), mapping(“redirect\_url” → redirect\_url, “gateway” → gateway)).

**Local steps**

- Return client.post(\_path(client, “create\_payment\_method\_checkout”), mapping(“redirect\_url” → redirect\_url, “gateway” → gateway)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L376) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L558)

<a id="op-927e602b23b25f"></a>
### Confirm payment method checkout

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_confirm_payment_method_checkout`

**Inputs** client, reference.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “confirm\_payment\_method\_checkout”), mapping(“reference” → reference)).

**Local steps**

- Return client.post(\_path(client, “confirm\_payment\_method\_checkout”), mapping(“reference” → reference)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L518) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L557)

<a id="op-63c95463de6f4c"></a>
### Reconcile payment setup

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_reconcile_payment_setup`

**Inputs** client.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “reconcile\_payment\_setup”), mapping()).

**Local steps**

- Return client.post(\_path(client, “reconcile\_payment\_setup”), mapping()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L626) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L564)

<a id="op-b7ec11bd889283"></a>
### Create topup checkout

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_create_topup_checkout`

**Inputs** client, amount, redirect\_url.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “create\_topup\_checkout”), mapping(“amount” → amount, “redirect\_url” → redirect\_url)).

**Local steps**

- Return client.post(\_path(client, “create\_topup\_checkout”), mapping(“amount” → amount, “redirect\_url” → redirect\_url)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L705) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L559)

<a id="op-f6dc916db0d085"></a>
### Invoices

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_billing_invoices`

**Inputs** client.

**Declared result** list.

**Explicit results** client.get(\_path(client, “list\_server\_invoices”)).

**Local steps**

- Return client.get(\_path(client, “list\_server\_invoices”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1481)

<a id="op-aa03013af787e7"></a>
### Invoice pdf

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_billing_invoice_pdf`

**Inputs** client, invoice.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “get\_server\_invoice\_pdf”), mapping(“invoice” → invoice)).

**Local steps**

- Return client.post(\_path(client, “get\_server\_invoice\_pdf”), mapping(“invoice” → invoice)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1480)

<a id="op-5568a4e31bbbd6"></a>
### Create invoice checkout

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_billing_create_invoice_checkout`

**Inputs** client, invoice, redirect\_url.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “create\_invoice\_checkout”), mapping(“invoice” → invoice, “redirect\_url” → redirect\_url)).

**Local steps**

- Return client.post(\_path(client, “create\_invoice\_checkout”), mapping(“invoice” → invoice, “redirect\_url” → redirect\_url)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1479)

<a id="op-65c607721e7b6c"></a>
### Checkout status

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_checkout_status`

**Inputs** client, reference.

**Declared result** dict.

**Explicit results** client.post(\_path(client, “get\_checkout\_status”), mapping(“reference” → reference)).

**Local steps**

- Return client.post(\_path(client, “get\_checkout\_status”), mapping(“reference” → reference)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L836) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L555)

<a id="op-7c75fbc1c7729c"></a>
### Path

`operation_foundation_integrations_application_foundation_providers_cloud_billing_business_behavior_path`

**Inputs** client, method.

**Declared result** str.

**Explicit results** client.site\_path(formatted text central/{METHOD\_PREFIX}.{method}).

**Local steps**

- Return client.site\_path(formatted text central/{METHOD\_PREFIX}.{method}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L944) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L563)

## Service · Cloud marketplace

<a id="op-b65d8d24397a1e"></a>
### List apps

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_list_apps`

**Inputs** client.

**Declared result** dict.

**Explicit results** mapping(“apps” → apps, “categories” → categories, “update\_count” → update\_count).

**Local steps**

- Set catalog from client.get(client.site\_path(“marketplace”)).
- If not isinstance(catalog, list).
  - Set catalog from list().
- Set installed from \_installed\_versions(client).
- Set required\_by from \_get\_required\_by(list(installed)).
- Set apps from list of \_app\_row(entry, installed, required\_by) for entry drawn from catalog where entry.get(“name”).
  - Draw entry from catalog, keep a combination only if (entry.get(“name”)).
- Set apps from list of app for app drawn from apps where app at “name” differs from “Platform”.
  - Draw app from apps, keep a combination only if (app at “name” differs from “Platform”).
- Evaluate apps.sort(key = \_sort\_key).
- Set categories from sorted(set of app at “category” for app drawn from apps where app at “category”).
  - Draw app from apps, keep a combination only if (app at “category”).
- Set update\_count from sum(generator of 1 for app drawn from apps where app at “has\_update”).
  - Draw app from apps, keep a combination only if (app at “has\_update”).
- Return mapping(“apps” → apps, “categories” → categories, “update\_count” → update\_count).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L44) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L573)

<a id="op-8c1071fdc32579"></a>
### Install

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_install`

**Inputs** client, app.

**Declared result** dict.

**Explicit results** client.post(client.site\_path(“apps”), mapping(“app” → \_clean(app))).

**Local steps**

- Return client.post(client.site\_path(“apps”), mapping(“app” → \_clean(app))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L1528) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L570)

<a id="op-2b86df956da4a0"></a>
### Uninstall

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_uninstall`

**Inputs** client, app.

**Declared result** dict.

**Explicit results** client.delete(client.site\_path(formatted text apps/{quote(\_clean(app), safe = empty text)})).

**Local steps**

- Return client.delete(client.site\_path(formatted text apps/{quote(\_clean(app), safe = empty text)})).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L1653) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L575)

<a id="op-3bff0280af7125"></a>
### Update

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_update`

**Inputs** client, apps.

**Declared result** dict.

**Explicit results** client.post(client.site\_path(“actions/update-apps”), args).

**Local steps**

- Set names from Platform.parse\_json(apps) when apps, otherwise no value.
  - Value choice on apps — true gives Platform.parse\_json(apps), false gives no value.
- Set args from mapping().
- If names.
  - Set args at “apps” from list of \_clean(name) for name drawn from names.
    - Draw name from names.
- Return client.post(client.site\_path(“actions/update-apps”), args).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L1790) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L576)

<a id="op-ba5e409a1ea057"></a>
### Installed versions

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_installed_versions`

**Inputs** client.

**Declared result** dict.

**Explicit results** mapping of app at “name” → (app.get(“version”) or empty text) for app drawn from apps where app.get(“name”).

**Local steps**

- Set apps from client.get(client.site\_path(“apps”)).get(“apps”, list()).
- Return mapping of app at “name” → (app.get(“version”) or empty text) for app drawn from apps where app.get(“name”).
  - Draw app from apps, keep a combination only if (app.get(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app.get(“version”) → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L2006) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L571)

<a id="op-a44976b1ed4d84"></a>
### Get required by

`operation_foundation_binding_foundation_integrations_foundation_providers_cloud_marketplace_get_required_by`

**Inputs** installed\_apps.

**Declared result** dict at tuple(str, list at str).

**Explicit results** mapping of app → list of other for other drawn from installed\_apps where (other differs from app and is\_required\_by(app, other)) for app drawn from installed\_apps.

**Local steps**

- Bind dependencies is\_required\_by.
- Return mapping of app → list of other for other drawn from installed\_apps where (other differs from app and is\_required\_by(app, other)) for app drawn from installed\_apps.
  - Draw app from installed\_apps.
  - Draw other from installed\_apps, keep a combination only if ((other differs from app and is\_required\_by(app, other))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in other differs from app → is\_required\_by(app, other).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1482)

<a id="op-c1465a8cf43ad5"></a>
### App row

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_application_row`

**Inputs** entry, installed, required\_by.

**Declared result** dict.

**Explicit results** mapping(“name” → name, “title” → (entry.get(“title”) or name), “description” → (entry.get(“description”) or empty text), “logo\_url” → (entry.get(“logo\_url”) or empty text), …).

**Local steps**

- Set name from entry at “name”.
- Set installed\_version from installed.get(name, empty text).
- Set latest\_version from (entry.get(“version”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“version”) → empty text.
- Return mapping(“name” → name, “title” → (entry.get(“title”) or name), “description” → (entry.get(“description”) or empty text), “logo\_url” → (entry.get(“logo\_url”) or empty text), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“title”) → name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“description”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“logo\_url”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“category”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“stars”) → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“required\_version”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(installed\_version) → \_is\_newer(latest\_version, installed\_version).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L43) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L568)

<a id="op-a8e933cac0416e"></a>
### Sort key

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_sort_key`

**Inputs** app.

**Declared result** tuple.

**Explicit results** tuple(not app at “installed”, negative app at “stars”, app at “title”.lower()).

**Local steps**

- Return tuple(not app at “installed”, negative app at “stars”, app at “title”.lower()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L2777) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L574)

<a id="op-3fa9df64fb7e83"></a>
### Is newer

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_is_newer`

**Inputs** latest, current.

**Declared result** bool.

**Explicit results** false · latest\_parts &gt; current\_parts.

**Local steps**

- Set tuple(latest\_parts, current\_parts) from tuple(\_version\_tuple(latest), \_version\_tuple(current)).
- If (not latest\_parts or not current\_parts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not latest\_parts → not current\_parts.
  - Return false.
- Return latest\_parts &gt; current\_parts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L2880) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L572)

<a id="op-395c2ff218a8bd"></a>
### Version tuple

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_version_tuple`

**Inputs** version.

**Declared result** tuple.

**Explicit results** tuple(parts).

**Local steps**

- Set parts from list().
- For each chunk in version.split(“.”).
  - Set number from empty text.join(generator of char for char drawn from chunk where char.isdigit()).
    - Draw char from chunk, keep a combination only if (char.isdigit()).
  - If not number.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate parts.append(int(number)).
- Return tuple(parts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3042) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L577)

<a id="op-f5d5a53ec08521"></a>
### Clean

`operation_foundation_integrations_application_foundation_providers_cloud_marketplace_business_behavior_clean`

**Inputs** name.

**Declared result** str.

**Explicit results** name.

**Explicit failure paths** validation helper with Platform.ValidationError — Platform.\_(“App name is required.”).

**Local steps**

- Set name from (name or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → empty text.
- If not name.
  - Call the validation error handler Platform.throw(Platform.\_(“App name is required.”), Platform.ValidationError).
- Return name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3258) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L569)

## Service · Cloud settings

<a id="op-b42f977b0cd91a"></a>
### Pilot Client.initialize

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_initialize`

**Inputs** self.

**Local steps**

- Set self.endpoint from (Platform.conf.get(“pilot\_endpoint”) or empty text).rstrip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“pilot\_endpoint”) → empty text.
- Set self.token from Platform.conf.get(“pilot\_auth\_token”).
- Set self.site from Platform.local.site.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3403) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L608)

<a id="op-1f10c2defe2791"></a>
### Pilot Client.get

`operation_foundation_integrations_application_foundation_providers_cloud_settings_business_behavior_pilot_client_get`

**Inputs** self, path.

**Declared result** (dict bitwise or list).

**Explicit results** self.\_request(“GET”, path).

**Local steps**

- Return self.\_request(“GET”, path).

**Methods declared on this owner** [request](operations-004.md#op-278aaf3d352265).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0259.json#L3558) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L607)
