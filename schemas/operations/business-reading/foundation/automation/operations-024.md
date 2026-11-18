# Workflow, automation and dispatch · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow model

<a id="op-9e15ddbed4b612"></a>
### Flow Model.validate

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_normalize().
- Evaluate self.\_apply\_provider().
- Evaluate self.\_validate\_model\_id().
- Evaluate self.\_validate\_base\_url().
- Evaluate self.\_validate\_extra\_params().
- Evaluate self.\_validate\_provider\_known().
- Evaluate self.\_resolve\_context\_window().

If control reaches the end, it returns no value.

**Methods declared on this owner** [normalize](operations-024.md#op-5601ec98c3d7b1), [apply provider](operations-024.md#op-4ed66a5570454c), [validate model id](operations-024.md#op-272735fa268865), [validate base url](operations-024.md#op-5631972a294161), [validate extra params](operations-024.md#op-30430f72a589e7), [validate provider known](operations-024.md#op-6ebd6e7f75db30), [resolve context window](operations-024.md#op-facfd991c15b6d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1024)

<a id="op-2504feb6809ff8"></a>
### Flow Model.after insert

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_after_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.enabled or self.embedding).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.enabled → self.embedding.
  - Return no value.
- Bind dependencies ensure\_builtin\_assistant.
- Evaluate ensure\_builtin\_assistant(model = self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1017)

<a id="op-7896afd0a6d3d7"></a>
### Flow Model.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_before_rename`

**Inputs** self, old, new, merge = false.

**Declared result** no value.

**Record and data access** resolve a document from “Flow Knowledge Settings” via get\_cached\_doc.

**State and service calls** request set\_single\_value on “Flow Knowledge Settings”.

**Local steps**

- If (not merge and Platform.get\_cached\_doc(“Flow Knowledge Settings”).embedding\_model equals old).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not merge → Platform.get\_cached\_doc(“Flow Knowledge Settings”).embedding\_model equals old.
  - Evaluate Platform.db.set\_single\_value(“Flow Knowledge Settings”, “embedding\_model”, validate\_name(self.doctype, new)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Flow Knowledge Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1019)

<a id="op-5601ec98c3d7b1"></a>
### Flow Model.normalize

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_normalize`

**Inputs** self.

**Local steps**

- For each field in tuple(“title”, “model\_id”, “base\_url”).
  - Set value from self.get(field).
  - If isinstance(value, str).
    - Evaluate self.set(field, value.strip()).
- If isinstance(self.api\_key, str).
  - Set self.api\_key from self.api\_key.strip().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1021)

<a id="op-4ed66a5570454c"></a>
### Flow Model.apply provider

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_apply_provider`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.provider.
  - Return no value.
- Set prefix from formatted text {self.provider}/.
- If (self.model\_id and not self.model\_id.startswith(prefix)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.model\_id → not self.model\_id.startswith(prefix).
  - Set self.model\_id from (prefix + self.model\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1018)

<a id="op-272735fa268865"></a>
### Flow Model.validate model id

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_validate_model_id`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Model ID must be in &lt;code&gt;provider/model&lt;/code&gt; form (e.g. &lt;code&gt;anthropic/claude-sonnet-4-6&lt;/code&gt;). Only l …”.

**Local steps**

- If not MODEL\_ID\_PATTERN.match((self.model\_id or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.model\_id → empty text.
  - Call the validation error handler Platform.throw(translated “Model ID must be in &lt;code&gt;provider/model&lt;/code&gt; form (e.g. &lt;code&gt;anthropic/claude-sonnet-4-6&lt;/code&gt;). Only l …”, title = translated “Invalid Model ID”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1027)

<a id="op-5631972a294161"></a>
### Flow Model.validate base url

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_validate_base_url`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Base URL must be an absolute http(s) URL.”.

**Local steps**

- If not self.base\_url.
  - Return no value.
- Set parsed from urlparse(self.base\_url).
- If (parsed.scheme does not belong to tuple(“http”, “https”) or not parsed.netloc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.scheme does not belong to tuple(“http”, “https”) → not parsed.netloc.
  - Call the validation error handler Platform.throw(translated “Base URL must be an absolute http(s) URL.”, title = translated “Invalid Base URL”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1025)

<a id="op-30430f72a589e7"></a>
### Flow Model.validate extra params

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_validate_extra_params`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Extra Params must be valid JSON.” · validation helper — translated “Extra Params must be a JSON object.”.

**Local steps**

- Set self.extra\_params from (self.extra\_params or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.extra\_params → no value.
- Attempt the following.
  - Set params from self.model\_params().
- On failure (ValueError).
  - Call the validation error handler Platform.throw(translated “Extra Params must be valid JSON.”, title = translated “Invalid Extra Params”).
- If not isinstance(params, dict).
  - Call the validation error handler Platform.throw(translated “Extra Params must be a JSON object.”, title = translated “Invalid Extra Params”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [model params](operations-024.md#op-0b103a61d6619a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1026)

<a id="op-0b103a61d6619a"></a>
### Flow Model.model params

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_model_params`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** Platform.parse\_json(self.extra\_params) when self.extra\_params, otherwise mapping().

**Local steps**

- Return Platform.parse\_json(self.extra\_params) when self.extra\_params, otherwise mapping().
  - Value choice on self.extra\_params — true gives Platform.parse\_json(self.extra\_params), false gives mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1020)

<a id="op-facfd991c15b6d"></a>
### Flow Model.resolve context window

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_resolve_context_window`

**Inputs** self.

**Local steps**

- Set self.context\_window from (\_detect\_context\_window(self.model\_id) or self.context\_window or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_detect\_context\_window(self.model\_id) → self.context\_window → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1022)

<a id="op-6ebd6e7f75db30"></a>
### Flow Model.validate provider known

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_validate_provider_known`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — str(e) at slice no value to 500.

**Local steps**

- Bind dependencies SITE\_PROVIDER.
- If self.provider equals SITE\_PROVIDER.
  - Return no value.
- Attempt the following.
  - Bind dependencies litellm.
- On failure (ImportError).
  - Return no value.
- Attempt the following.
  - Evaluate litellm.get\_llm\_provider(self.model\_id).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(str(e) at slice no value to 500, title = translated “Invalid Model ID”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1028)

<a id="op-0db12f919959cc"></a>
### Flow Model.test connection

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_flowmodel_test_connection`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“ok” → true, “message” → translated “Connection OK”).

**Explicit failure paths** validation helper — translated “LiteLLM is not installed. Run &lt;code&gt;bench setup requirements&lt;/code&gt;.” · validation helper — (str(e) at slice no value to 500 or type(e).\_\_name\_\_).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Attempt the following.
  - Bind dependencies litellm.
- On failure (ImportError).
  - Call the validation error handler Platform.throw(translated “LiteLLM is not installed. Run &lt;code&gt;bench setup requirements&lt;/code&gt;.”, title = translated “Missing Dependency”).
- Bind dependencies litellm\_route, resolve\_provider\_credentials.
- Set provider\_creds from resolve\_provider\_credentials(self.model\_id, self.provider).
- Set api\_key from (self.get\_password(“api\_key”, raise\_exception = false) or provider\_creds.get(“api\_key”) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_password(“api\_key”, raise\_exception = false) → provider\_creds.get(“api\_key”) → no value.
- Set tuple(model, base\_url) from litellm\_route(self.model\_id, (self.base\_url or provider\_creds.get(“base\_url”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.base\_url → provider\_creds.get(“base\_url”).
- Set kwargs from mapping(expand self.model\_params(), “model” → model, “api\_key” → api\_key, “messages” → list(mapping(“role” → “user”, “content” → “ping”)), …).
- If base\_url.
  - Set kwargs at “api\_base” from base\_url.
- Attempt the following.
  - Evaluate litellm.completion(expanded names kwargs).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw((str(e) at slice no value to 500 or type(e).\_\_name\_\_), title = translated type(e).\_\_name\_\_).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in str(e) at slice no value to 500 → type(e).\_\_name\_\_.
- Return mapping(“ok” → true, “message” → translated “Connection OK”).

**Methods declared on this owner** [model params](operations-024.md#op-0b103a61d6619a).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1023)

<a id="op-c9c01dde93ea41"></a>
### Detect context window

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_detect_context_window`

**Inputs** model\_id.

**Declared result** int.

**Explicit results** int(window) · 0.

**Local steps**

- Bind dependencies litellm.
- For each candidate in tuple(model\_id, model\_id.partition(“/”) at 2).
  - Attempt the following.
    - Set window from litellm.get\_model\_info(candidate).get(“max\_input\_tokens”).
  - On failure (Exception).
    - Continue with the next iteration or loop test.
  - If window.
    - Return int(window).
- Return 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1016)

<a id="op-c11067d7cf88f7"></a>
### Get provider models

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_get_provider_models`

**Inputs** provider = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** list() · sorted(set of (prefix + model) for model drawn from \_live\_models(provider)) · sorted(set of model when model.startswith(prefix), otherwise (prefix + model) for model drawn from catalog).

**Local steps**

- If (not provider or not Platform.has\_permission(“Flow Model”, “write”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not provider → not Platform.has\_permission(“Flow Model”, “write”).
  - Return list().
- Set provider from provider.strip().lower().
- Set prefix from formatted text {provider}/.
- Attempt the following.
  - Return sorted(set of (prefix + model) for model drawn from \_live\_models(provider)).
    - Draw model from \_live\_models(provider).
- On failure (Exception).
  - Bind dependencies litellm.
  - Set catalog from litellm.models\_by\_provider.get(provider, set()).
  - Return sorted(set of model when model.startswith(prefix), otherwise (prefix + model) for model drawn from catalog).
    - Draw model from catalog.
    - Value choice on model.startswith(prefix) — true gives model, false gives (prefix + model).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Flow Model”, “write”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1029)

<a id="op-0110d527ecf68a"></a>
### Live models

`operation_foundation_binding_foundation_flow_doctype_flow_model_flow_model_live_models`

**Inputs** provider.

**Declared result** list at str.

**Record and data access** resolve a document from “Flow Provider” via get\_doc.

**Explicit results** list of str(model\_id).removeprefix(“models/”) for model\_id drawn from ids where model\_id.

**Local steps**

- Bind dependencies MODEL\_ENDPOINTS.
- Set doc from Platform.get\_doc(“Flow Provider”, provider).
- Set api\_key from (doc.get\_password(“api\_key”, raise\_exception = false) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_password(“api\_key”, raise\_exception = false) → empty text.
- Set base from (doc.base\_url or empty text).rstrip(“/”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.base\_url → empty text.
- If provider equals “ollama\_chat”.
  - Set url from formatted text {base}/v1/models.
- Otherwise.
  - Set url from base when base.endswith(“/models”), otherwise formatted text {base}/models when base, otherwise MODEL\_ENDPOINTS at provider.
    - Value choice on base — true gives base when base.endswith(“/models”), otherwise formatted text {base}/models, false gives MODEL\_ENDPOINTS at provider.
    - Value choice on base.endswith(“/models”) — true gives base, false gives formatted text {base}/models.
- Set params from mapping().
- If provider equals “anthropic”.
  - Set headers from mapping(“x-api-key” → api\_key, “anthropic-version” → “2023-06-01”).
  - Set params from mapping(“limit” → 1000).
- Otherwise.
  - If provider equals “gemini”.
    - Set headers from mapping(“x-goog-api-key” → api\_key).
    - Set params from mapping(“pageSize” → 1000).
  - Otherwise.
    - Set headers from mapping(“Authorization” → formatted text Bearer {api\_key}) when api\_key, otherwise mapping().
      - Value choice on api\_key — true gives mapping(“Authorization” → formatted text Bearer {api\_key}), false gives mapping().
- If provider equals “openrouter”.
  - Set params from mapping(“output\_modalities” → “text,embeddings”).
- Set response from requests.get(url, headers = headers, params = params, timeout = 10).
- Evaluate response.raise\_for\_status().
- Set data from response.json().
- Set ids from generator of (row.get(“id”) or row.get(“name”)) for row drawn from data.get(“data”, data.get(“models”)).
  - Draw row from data.get(“data”, data.get(“models”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“id”) → row.get(“name”).
- Return list of str(model\_id).removeprefix(“models/”) for model\_id drawn from ids where model\_id.
  - Draw model\_id from ids, keep a combination only if (model\_id).

**Values supplied outside this operation** service or queued work from requests.get(url, headers = headers, params = params, timeout = 10).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1030)

## Record · Flow provider

<a id="op-e1c25c978874aa"></a>
### Flow Provider.autoname

`operation_foundation_binding_foundation_flow_doctype_flow_provider_flow_provider_flowprovider_autoname`

**Inputs** self.

**Local steps**

- Set self.provider from (self.provider or empty text).strip().lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.provider → empty text.
- Set self.name from self.provider.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1031)

<a id="op-3e024167caf080"></a>
### Flow Provider.validate

`operation_foundation_binding_foundation_flow_doctype_flow_provider_flow_provider_flowprovider_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_normalize().
- Evaluate self.\_validate\_provider\_known().
- Evaluate self.\_validate\_base\_url().

If control reaches the end, it returns no value.

**Methods declared on this owner** [normalize](operations-024.md#op-34a92f6847c83a), [validate provider known](operations-024.md#op-6ae489ab664534), [validate base url](operations-024.md#op-6f5b16ad7fcbc1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1033)

<a id="op-34a92f6847c83a"></a>
### Flow Provider.normalize

`operation_foundation_binding_foundation_flow_doctype_flow_provider_flow_provider_flowprovider_normalize`

**Inputs** self.

**Local steps**

- Set self.provider from (self.provider or empty text).strip().lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.provider → empty text.
- If isinstance(self.base\_url, str).
  - Set self.base\_url from self.base\_url.strip().
- If isinstance(self.api\_key, str).
  - Set self.api\_key from self.api\_key.strip().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1032)

<a id="op-6ae489ab664534"></a>
### Flow Provider.validate provider known

`operation_foundation_binding_foundation_flow_doctype_flow_provider_flow_provider_flowprovider_validate_provider_known`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unknown provider {0}. It must be a LiteLLM provider name (e.g. openai, anthropic, openrouter, gemini).”.format(Platform.bold(self.provider)).

**Local steps**

- Bind dependencies SITE\_PROVIDER.
- If self.provider equals SITE\_PROVIDER.
  - Return no value.
- Attempt the following.
  - Bind dependencies litellm.
- On failure (ImportError).
  - Return no value.
- Set known from set of p.value for p drawn from litellm.provider\_list.
  - Draw p from litellm.provider\_list.
- If self.provider does not belong to known.
  - Call the validation error handler Platform.throw(translated “Unknown provider {0}. It must be a LiteLLM provider name (e.g. openai, anthropic, openrouter, gemini).”.format(Platform.bold(self.provider)), title = translated “Invalid Provider”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1059) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1035)

<a id="op-6f5b16ad7fcbc1"></a>
### Flow Provider.validate base url

`operation_foundation_binding_foundation_flow_doctype_flow_provider_flow_provider_flowprovider_validate_base_url`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Base URL must be an absolute http(s) URL.”.

**Local steps**

- If not self.base\_url.
  - Return no value.
- Set parsed from urlparse(self.base\_url).
- If (parsed.scheme does not belong to tuple(“http”, “https”) or not parsed.netloc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.scheme does not belong to tuple(“http”, “https”) → not parsed.netloc.
  - Call the validation error handler Platform.throw(translated “Base URL must be an absolute http(s) URL.”, title = translated “Invalid Base URL”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1034)

## Record · Flow run

<a id="op-62034f7b08414e"></a>
### Flow Run.validate

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_flowrun_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_validate\_json\_fields().
- Evaluate self.\_validate\_status\_invariants().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate json fields](operations-024.md#op-cf9e83fbf54fdc), [validate status invariants](operations-024.md#op-517f012e971876).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1062) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1038)

<a id="op-2cff1b6b755e99"></a>
### Flow Run.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_flowrun_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A run belongs to its chat. Delete the chat to remove it.”.

**Local steps**

- Call the validation error handler Platform.throw(translated “A run belongs to its chat. Delete the chat to remove it.”, title = translated “Cannot Delete”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1061) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1037)

<a id="op-cf9e83fbf54fdc"></a>
### Flow Run.validate json fields

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_flowrun_validate_json_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} must be valid JSON.”.format(fieldname).

**Local steps**

- For each fieldname in JSON\_FIELDS.
  - Set value from self.get(fieldname).
  - If value belongs to tuple(no value, empty text).
    - Continue with the next iteration or loop test.
  - If not isinstance(value, str).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Evaluate json.loads(value).
  - On failure (tuple(TypeError, ValueError)).
    - Call the validation error handler Platform.throw(translated “{0} must be valid JSON.”.format(fieldname), title = translated “Invalid JSON”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1063) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1039)

<a id="op-517f012e971876"></a>
### Flow Run.validate status invariants

`operation_foundation_binding_foundation_flow_doctype_flow_run_flow_run_flowrun_validate_status_invariants`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Paused runs must have at least one pending question.” · validation helper — translated “Failed runs must include an error message.”.

**Local steps**

- If (self.status equals “Paused” and not \_json\_has\_items(self.questions)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Paused” → not \_json\_has\_items(self.questions).
  - Call the validation error handler Platform.throw(translated “Paused runs must have at least one pending question.”).
- If (self.status equals “Failed” and not self.error).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Failed” → not self.error.
  - Call the validation error handler Platform.throw(translated “Failed runs must include an error message.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1064) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1040)
