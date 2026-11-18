# Integration and transport · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Webhook

[Record definition](../../../../data/record-types/webhook.json)

<a id="op-5d292535da7f80"></a>
### Webhook.execute for doc

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_execute_for_record`

**Inputs** self, doc.

**Local steps**

- Evaluate enqueue\_webhook(doc, self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L231) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L835)

<a id="op-d5385a0212e615"></a>
### Webhook.validate docevent

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_docevent`

**Inputs** self.

**Record and data access** read “DocType” via get\_value.

**Explicit failure paths** validation helper — translated “DocType must be Submittable for the selected Doc Event”.

**Local steps**

- If self.webhook\_doctype.
  - Set is\_submittable from Platform.get\_value(“DocType”, self.webhook\_doctype, “is\_submittable”).
  - If (not is\_submittable and self.webhook\_docevent belongs to list(“on\_submit”, “on\_cancel”, “on\_update\_after\_submit”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_submittable → self.webhook\_docevent belongs to list(“on\_submit”, “on\_cancel”, “on\_update\_after\_submit”).
    - Call the validation error handler Platform.throw(translated “DocType must be Submittable for the selected Doc Event”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L299) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L841)

<a id="op-5f2922cb0d7137"></a>
### Webhook.validate condition

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L489) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L840)

<a id="op-83c216cf6a345c"></a>
### Webhook.validate request url

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_request_resource_address`

**Inputs** self.

**Explicit failure paths** Platform.ValidationError · validation helper with e — translated “Check Request URL”.

**Local steps**

- Attempt the following.
  - Set request\_url from urlparse(self.request\_url).netloc.
  - If not request\_url.
    - Raise Platform.ValidationError.
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Check Request URL”, exc = e).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L706) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L844)

<a id="op-d802490e1ea3fc"></a>
### Webhook.validate request body

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_request_body`

**Inputs** self.

**Local steps**

- If self.request\_structure.
  - If self.request\_structure equals “Form URL-Encoded”.
    - Set self.webhook\_json from no value.
  - Otherwise.
    - If self.request\_structure equals “JSON”.
      - Evaluate validate\_template(self.webhook\_json).
      - Set self.webhook\_data from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L871) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L843)

<a id="op-4cb66eeca6e688"></a>
### Webhook.validate repeating fields

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_repeating_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Same Field is entered more than once”.

**Local steps**

- Set webhook\_data from list of entry.fieldname for entry drawn from self.webhook\_data.
  - Draw entry from self.webhook\_data.
- If len(webhook\_data) differs from len(set(webhook\_data)).
  - Call the validation error handler Platform.throw(translated “Same Field is entered more than once”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L1027) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L842)

<a id="op-99a0129885c108"></a>
### Webhook.validate secret

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L1194) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L845)

<a id="op-d8d6c612bab573"></a>
### Webhook.preview meets condition

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_preview_meets_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, preview\_document.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L1347) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L837)

<a id="op-be46014dd70987"></a>
### Webhook.preview request body

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_preview_request_body`

**Inputs** self, preview\_document.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from self.webhook\_doctype via get\_cached\_doc.

**Explicit results** Platform.as\_json(get\_webhook\_data(doc, self)) · translated “Failed to compute request body: {}”.format(str(e)).

**Local steps**

- Attempt the following.
  - Set doc from Platform.get\_cached\_doc(self.webhook\_doctype, preview\_document).
  - Return Platform.as\_json(get\_webhook\_data(doc, self)).
- On failure (Exception) bound to e.
  - Set Platform.local.message\_log from list().
  - Return translated “Failed to compute request body: {}”.format(str(e)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.webhook\_doctype, preview\_document).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L1675) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L838)

<a id="op-7724d7dd04c3aa"></a>
### Get context

`operation_foundation_integrations_record_definitions_webhook_business_behavior_get_context`

**Inputs** doc.

**Explicit results** mapping(“doc” → doc, “utils” → get\_safe\_globals().get(“Platform”).get(“utils”)).

**Local steps**

- Return mapping(“doc” → doc, “utils” → get\_safe\_globals().get(“Platform”).get(“utils”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L1907) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L831)

<a id="op-bff5855f56f2a2"></a>
### Enqueue webhook

`operation_foundation_integrations_record_definitions_webhook_business_behavior_enqueue_webhook`

**Inputs** doc, webhook.

**Declared result** no value.

**Record and data access** resolve a document from “Webhook” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** e.

**Local steps**

- Set request\_url, headers, data, r from no value.
- Attempt the following.
  - If not isinstance(webhook, Document).
    - Set webhook from Platform.get\_doc(“Webhook”, webhook.get(“name”)).
  - Set request\_url from webhook.request\_url.
  - If webhook.is\_dynamic\_url.
    - Set request\_url from Platform.render\_template(webhook.request\_url, get\_context(doc)).
  - Set data from get\_webhook\_data(doc, webhook).
  - Set headers from get\_webhook\_headers(doc, webhook, data = data).
- On failure (Exception) bound to e.
  - Evaluate Platform.logger().debug(mapping(“enqueue\_webhook\_error” → e)).
  - Evaluate log\_request(webhook.name, doc.doctype, doc.name, request\_url, …).
  - Return no value.
- For each i in range(3).
  - Attempt the following.
    - Set r from requests.request(method = webhook.request\_method, url = request\_url, data = Platform.as\_json(data), headers = headers, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in webhook.timeout → 5.
    - Evaluate r.raise\_for\_status().
    - Evaluate Platform.logger().debug(mapping(“webhook\_success” → r.text)).
    - Evaluate log\_request(webhook.name, doc.doctype, doc.name, request\_url, …).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - On failure (requests.exceptions.ReadTimeout) bound to e.
    - Evaluate Platform.logger().debug(mapping(“webhook\_error” → e, “try” → (i + 1))).
    - Evaluate log\_request(webhook.name, doc.doctype, doc.name, request\_url, …).
  - On failure (Exception) bound to e.
    - Evaluate Platform.logger().debug(mapping(“webhook\_error” → e, “try” → (i + 1))).
    - Evaluate log\_request(webhook.name, doc.doctype, doc.name, request\_url, …).
    - If i &lt; 2.
      - Evaluate sleep(((3 × i) + 1)).
      - Continue with the next iteration or loop test.
    - If webhook.webhook\_docevent equals “workflow\_transition”.
      - Raise e.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.request(method = webhook.request\_method, url = request\_url, data = Platform.as\_json(data), headers = headers, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L60) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L829)

<a id="op-8c74ba8bc621d5"></a>
### Log request

`operation_foundation_integrations_record_definitions_webhook_business_behavior_log_request`

**Inputs** webhook, doctype, docname, url, headers, data, res = no value.

**Record and data access** resolve a document from mapping(“doctype” → “Webhook Request Log”, “webhook” → webhook, “reference\_doctype” → doctype, “reference\_document” → docname, …) via get\_doc.

**State and service calls** call save on request\_log.

**Local steps**

- Set request\_log from Platform.get\_doc(mapping(“doctype” → “Webhook Request Log”, “webhook” → webhook, “reference\_doctype” → doctype, “reference\_document” → docname, …)).
  - Value choice on Platform.session.user — true gives Platform.session.user, false gives no value.
  - Value choice on headers — true gives Platform.as\_json(headers), false gives no value.
  - Value choice on data — true gives Platform.as\_json(data), false gives no value.
  - Value choice on res is distinct from no value — true gives res.text, false gives no value.
- Evaluate request\_log.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L62) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L834)

<a id="op-5946de5053ef52"></a>
### Get webhook headers

`operation_foundation_integrations_record_definitions_webhook_business_behavior_get_webhook_headers`

**Inputs** doc, webhook, data = no value.

**Explicit results** headers.

**Local steps**

- Set headers from mapping().
- If webhook.enable\_security.
  - If data is identical to no value.
    - Set data from get\_webhook\_data(doc, webhook).
  - Set signature from base64.b64encode(hmac.new(nested operand in the contract(nested operand in the contract).encode(“utf8”), nested operand in the contract(nested operand in the contract).encode(“utf8”), hashlib.sha256).digest()).
  - Set headers at WEBHOOK\_SECRET\_HEADER from signature.
- If webhook.webhook\_headers.
  - For each h in webhook.webhook\_headers.
    - If (h.get(“key”) and h.get(“value”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in h.get(“key”) → h.get(“value”).
      - Set headers at h.get(“key”) from h.get(“value”).
- Return headers.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L61) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L833)

<a id="op-15ef5403c019ea"></a>
### Get webhook data

`operation_foundation_integrations_record_definitions_webhook_business_behavior_get_webhook_data`

**Inputs** doc, webhook.

**Explicit results** data.

**Local steps**

- Set data from mapping().
- Set doc from doc.as\_dict(convert\_dates\_to\_str = true).
- If webhook.webhook\_data.
  - Set data from mapping of w.key → doc.get(w.fieldname) for w drawn from webhook.webhook\_data.
    - Draw w from webhook.webhook\_data.
- Otherwise.
  - If webhook.webhook\_json.
    - Set data from Platform.render\_template(webhook.webhook\_json, get\_context(doc)).
    - Set data from json.loads(data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L5908) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L832)

<a id="op-e2879ce20ffc8c"></a>
### Get all queues

`operation_foundation_integrations_record_definitions_webhook_business_behavior_get_all_queues`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_queues\_timeout().keys().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Return get\_queues\_timeout().keys().

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L830)

## Record · Webhook request log

[Record definition](../../../../data/record-types/webhook_request_log.json)

<a id="op-87596841e51a03"></a>
### Webhook Request Log.clear old logs

`operation_foundation_integrations_record_definitions_webhook_request_log_business_behavior_webhook_request_log_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Webhook Request Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6269) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L850)
