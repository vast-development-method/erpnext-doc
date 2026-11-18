# Relationship automation · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Actions

<a id="op-6298e789e1a4a0"></a>
### Require doctype

`operation_relationships_binding_crm_automation_actions_require_doctype`

**Inputs** doctype, allowed, label.

**Explicit failure paths** AutomationParamError(translated “{0} must act on {1}, not {2}”.format(label, “ or ”.join(allowed), doctype), fieldname = “target”).

**Local steps**

- If (doctype and doctype does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → doctype does not belong to allowed.
  - Raise AutomationParamError(translated “{0} must act on {1}, not {2}”.format(label, “ or ”.join(allowed), doctype), fieldname = “target”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L77) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L233) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L214)

<a id="op-14980742cf8b40"></a>
### As list

`operation_relationships_binding_crm_automation_actions_as_list`

**Inputs** value.

**Declared result** list.

**Explicit results** list() · list(parsed) when isinstance(parsed, list), otherwise list(parsed) · list(value) when isinstance(value, (list bitwise or tuple)), otherwise list(value).

**Local steps**

- If not value.
  - Return list().
- If isinstance(value, str).
  - Set parsed from Platform.parse\_json(value) when value.strip().startswith(“&#91;”), otherwise value.
    - Value choice on value.strip().startswith(“&#91;”) — true gives Platform.parse\_json(value), false gives value.
  - Return list(parsed) when isinstance(parsed, list), otherwise list(parsed).
    - Value choice on isinstance(parsed, list) — true gives list(parsed), false gives list(parsed).
- Return list(value) when isinstance(value, (list bitwise or tuple)), otherwise list(value).
  - Value choice on isinstance(value, (list bitwise or tuple)) — true gives list(value), false gives list(value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L69) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L225) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L206)

<a id="op-15aafe53c71399"></a>
### Parse overrides

`operation_relationships_binding_crm_automation_actions_parse_overrides`

**Inputs** overrides.

**Declared result** dict.

**Explicit results** mapping() · overrides.

**Explicit failure paths** AutomationParamError(translated “Deal field overrides must be a JSON object”, fieldname = “deal”).

**Local steps**

- If isinstance(overrides, str).
  - Set overrides from Platform.parse\_json(overrides).
- If not overrides.
  - Return mapping().
- If not isinstance(overrides, dict).
  - Raise AutomationParamError(translated “Deal field overrides must be a JSON object”, fieldname = “deal”).
- Return overrides.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L76) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L232) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L213)

<a id="op-372f44150533f1"></a>
### Adjust Lead Score.validate

`operation_relationships_binding_crm_automation_actions_adjustleadscore_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “Amount is required”, fieldname = “amount”) · AutomationParamError(translated “Minimum score is above the maximum”, fieldname = “min\_score”).

**Local steps**

- Evaluate require\_doctype(doctype, list(“CRM Lead”), self.label).
- If not params.get(“amount”).
  - Raise AutomationParamError(translated “Amount is required”, fieldname = “amount”).
- Set bounds from tuple(params.get(“min\_score”), params.get(“max\_score”)).
- If (all(generator of bound does not belong to tuple(no value, empty text) for bound drawn from bounds) and int(bounds at 0) &gt; int(bounds at 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in all(generator of bound does not belong to tuple(no value, empty text) for bound drawn from bounds) → int(bounds at 0) &gt; int(bounds at 1).
  - Draw bound from bounds.
  - Raise AutomationParamError(translated “Minimum score is above the maximum”, fieldname = “min\_score”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L68) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L224) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L205)

<a id="op-1b94a9d58b5c6f"></a>
### Adjust Lead Score.execute

`operation_relationships_binding_crm_automation_actions_adjustleadscore_execute`

**Inputs** self, doc, params, context.

**Explicit results** adjust\_lead\_score(doc, params at “amount”, reason = params.get(“reason”), min\_score = params.get(“min\_score”), max\_score = params.get(“max\_score”)).

**Local steps**

- Evaluate require\_doctype((doc and doc.doctype), list(“CRM Lead”), self.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype.
- Return adjust\_lead\_score(doc, params at “amount”, reason = params.get(“reason”), min\_score = params.get(“min\_score”), max\_score = params.get(“max\_score”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L67) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L223) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L204)

<a id="op-702eacb0316e49"></a>
### Set Lead Temperature.validate

`operation_relationships_binding_crm_automation_actions_setleadtemperature_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “Choose a lead temperature”, fieldname = “temperature”).

**Local steps**

- Evaluate require\_doctype(doctype, list(“CRM Lead”), self.label).
- If params.get(“temperature”) does not belong to temperature\_options().
  - Raise AutomationParamError(translated “Choose a lead temperature”, fieldname = “temperature”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L85) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L241) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L222)

<a id="op-cab4c00c1a3a4b"></a>
### Set Lead Temperature.execute

`operation_relationships_binding_crm_automation_actions_setleadtemperature_execute`

**Inputs** self, doc, params, context.

**Explicit results** set\_lead\_temperature(doc, params at “temperature”).

**Local steps**

- Evaluate require\_doctype((doc and doc.doctype), list(“CRM Lead”), self.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype.
- Return set\_lead\_temperature(doc, params at “temperature”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L84) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L240) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L221)

<a id="op-a21aa71a6d0564"></a>
### Convert Lead To Deal.validate

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “Unsupported conversion policy”, fieldname = “if\_converted”).

**Local steps**

- Evaluate require\_doctype(doctype, list(“CRM Lead”), self.label).
- If params.get(“if\_converted”) does not belong to tuple(no value, empty text, “Return Existing”, “Fail”).
  - Raise AutomationParamError(translated “Unsupported conversion policy”, fieldname = “if\_converted”).
- Evaluate self.\_validate\_overrides(params.get(“deal”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overrides](operations-001.md#op-0bec4cdf6cd733).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L74) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L230) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L211)

<a id="op-0bec4cdf6cd733"></a>
### Convert Lead To Deal.validate overrides

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_validate_overrides`

**Inputs** self, overrides.

**Explicit failure paths** AutomationParamError(translated “CRM Deal has no field {0}”.format(fieldname), fieldname = “deal”).

**Local steps**

- Set meta from Platform.get\_meta(“CRM Deal”).
- For each fieldname in parse\_overrides(overrides).
  - If not meta.has\_field(fieldname).
    - Raise AutomationParamError(translated “CRM Deal has no field {0}”.format(fieldname), fieldname = “deal”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L75) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L231) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L212)

<a id="op-be9f016041841e"></a>
### Convert Lead To Deal.output doctype

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_output_doctype`

**Inputs** self, params.

**Explicit results** “CRM Deal”.

**Local steps**

- Return “CRM Deal”.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L71) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L227) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L208)

<a id="op-06a4d767f868a3"></a>
### Convert Lead To Deal.execute

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_execute`

**Inputs** self, doc, params, context.

**Explicit results** self.\_result(doc, deal, reused).

**Local steps**

- Evaluate require\_doctype((doc and doc.doctype), list(“CRM Lead”), self.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype.
- Set reused from existing\_deal(doc.name).
- Set deal from convert\_to\_deal(doc.name, deal = self.\_overrides(doc, params, context), existing\_contact = render\_value(params.get(“existing\_contact”), doc, context), existing\_organization = render\_value(params.get(“exist ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“if\_converted”) → “Return Existing”.
- Return self.\_result(doc, deal, reused).

**Methods declared on this owner** [overrides](operations-001.md#op-c88ff40951af8b), [result](operations-001.md#op-78c0fa3b4942c3).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L70) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L226) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L207)

<a id="op-c88ff40951af8b"></a>
### Convert Lead To Deal.overrides

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_overrides`

**Inputs** self, doc, params, context.

**Declared result** dict.

**Explicit results** mapping of field → render\_value(value, doc, context) for tuple(field, value) drawn from overrides.items().

**Local steps**

- Set overrides from parse\_overrides(params.get(“deal”)).
- Return mapping of field → render\_value(value, doc, context) for tuple(field, value) drawn from overrides.items().
  - Draw tuple(field, value) from overrides.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L72) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L228) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L209)

<a id="op-78c0fa3b4942c3"></a>
### Convert Lead To Deal.result

`operation_relationships_binding_crm_automation_actions_convertleadtodeal_result`

**Inputs** self, lead, deal, reused.

**Declared result** dict.

**Record and data access** resolve a document from “CRM Deal” via get\_doc.

**Explicit results** mapping(“detail” → translated “Reused Deal {0}”.format(deal) when reused, otherwise translated “Created Deal {0}”.format(deal), “destination\_reference” → mapping(“doctype” → “CRM Deal”, “name” → deal), “co ….

**Local steps**

- Set deal\_doc from Platform.get\_doc(“CRM Deal”, deal).
- Return mapping(“detail” → translated “Reused Deal {0}”.format(deal) when reused, otherwise translated “Created Deal {0}”.format(deal), “destination\_reference” → mapping(“doctype” → “CRM Deal”, “name” → deal), “co ….
  - Value choice on reused — true gives translated “Reused Deal {0}”.format(deal), false gives translated “Created Deal {0}”.format(deal).
  - Value choice on deal\_doc.contacts — true gives deal\_doc.contacts at 0.contact, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L73) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L229) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L210)

<a id="op-b824f39796cedd"></a>
### Send Email To Record.validate

`operation_relationships_binding_crm_automation_actions_sendemailtorecord_validate`

**Inputs** self, params, doctype.

**Record and data access** read “Email Template” via exists.

**Explicit failure paths** AutomationParamError(translated “Pick a template or write a subject”, fieldname = “email\_template”) · AutomationParamError(translated “Unknown Email Template”, fieldname = “email\_template”).

**Local steps**

- Evaluate require\_doctype(doctype, self.applicable\_doctypes, self.label).
- If not (params.get(“email\_template”) or params.get(“subject”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“email\_template”) → params.get(“subject”).
  - Raise AutomationParamError(translated “Pick a template or write a subject”, fieldname = “email\_template”).
- If (params.get(“email\_template”) and not Platform.db.exists(“Email Template”, params at “email\_template”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“email\_template”) → not Platform.db.exists(“Email Template”, params at “email\_template”).
  - Raise AutomationParamError(translated “Unknown Email Template”, fieldname = “email\_template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L83) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L239) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L220)

<a id="op-6bb5e2a9999105"></a>
### Send Email To Record.execute

`operation_relationships_binding_crm_automation_actions_sendemailtorecord_execute`

**Inputs** self, doc, params, context.

**Record and data access** read “User” via get\_value.

**Explicit results** mapping(“detail” → translated “Emailed {0}: {1}”.format(recipient, subject), “communication” → sent.get(“name”), “recipient” → recipient, “sender” → sender).

**Explicit failure paths** AutomationParamError(translated “{0} has no email address”.format(doc.doctype when doc, otherwise empty text)).

**Local steps**

- Bind dependencies make.
- Evaluate require\_doctype((doc and doc.doctype), self.applicable\_doctypes, self.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype.
- Set recipient from doc.get(“email”) when doc, otherwise no value.
  - Value choice on doc — true gives doc.get(“email”), false gives no value.
- If not recipient.
  - Raise AutomationParamError(translated “{0} has no email address”.format(doc.doctype when doc, otherwise empty text)).
    - Value choice on doc — true gives doc.doctype, false gives empty text.
- Set tuple(subject, message) from self.\_content(doc, params).
- Set sender from params.get(“sender”).
- Set sent from make(doctype = doc.doctype, name = doc.name, subject = subject, content = message, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sender → no value.
  - Value choice on sender — true gives Platform.db.get\_value(“User”, sender, “full\_name”), false gives no value.
- Return mapping(“detail” → translated “Emailed {0}: {1}”.format(recipient, subject), “communication” → sent.get(“name”), “recipient” → recipient, “sender” → sender).

**Methods declared on this owner** [content](operations-001.md#op-3badb3baebb7fc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L82) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L238) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L219)

<a id="op-3badb3baebb7fc"></a>
### Send Email To Record.content

`operation_relationships_binding_crm_automation_actions_sendemailtorecord_content`

**Inputs** self, doc, params.

**Record and data access** resolve a document from “Email Template” via get\_doc.

**Explicit results** tuple(params.get(“subject”), (params.get(“message”) or empty text)) · tuple(template.get\_formatted\_subject(context), template.get\_formatted\_response(context)).

**Local steps**

- If not params.get(“email\_template”).
  - Return tuple(params.get(“subject”), (params.get(“message”) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“message”) → empty text.
- Set template from Platform.get\_doc(“Email Template”, params at “email\_template”).
- Set context from mapping(“doc” → doc, “target” → doc).
- Return tuple(template.get\_formatted\_subject(context), template.get\_formatted\_response(context)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L81) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L237) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L218)

<a id="op-62753db7f2af9b"></a>
### Send CRMNotification.validate

`operation_relationships_binding_crm_automation_actions_sendcrmnotification_validate`

**Inputs** self, params, doctype.

**Explicit failure paths** AutomationParamError(translated “At least one recipient is required”, fieldname = “recipients”) · AutomationParamError(translated “Write the notification text”, fieldname = “notification\_text”).

**Local steps**

- Evaluate require\_doctype(doctype, self.applicable\_doctypes, self.label).
- If not as\_list(params.get(“recipients”)).
  - Raise AutomationParamError(translated “At least one recipient is required”, fieldname = “recipients”).
- If not params.get(“notification\_text”).
  - Raise AutomationParamError(translated “Write the notification text”, fieldname = “notification\_text”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L80) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L236) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L217)

<a id="op-a31d2494893178"></a>
### Send CRMNotification.execute

`operation_relationships_binding_crm_automation_actions_sendcrmnotification_execute`

**Inputs** self, doc, params, context.

**Explicit results** translated “No recipients to notify” · translated “Notified {0}”.format(“, ”.join(recipients)).

**Local steps**

- Evaluate require\_doctype((doc and doc.doctype), self.applicable\_doctypes, self.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.doctype.
- Set recipients from resolve\_recipients(as\_list(params.get(“recipients”)), doc).
- If not recipients.
  - Return translated “No recipients to notify”.
- Set text from render\_value((params.get(“notification\_text”) or empty text), doc, context).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“notification\_text”) → empty text.
- Set message from render\_value((params.get(“message”) or empty text), doc, context).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“message”) → empty text.
- For each user in recipients.
  - Evaluate self.\_notify(doc, user, text, message).
- Return translated “Notified {0}”.format(“, ”.join(recipients)).

**Methods declared on this owner** [notify](operations-001.md#op-98b7169705ba47).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L78) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L234) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L215)

<a id="op-98b7169705ba47"></a>
### Send CRMNotification.notify

`operation_relationships_binding_crm_automation_actions_sendcrmnotification_notify`

**Inputs** self, doc, user, text, message.

**Record and data access** resolve a document from mapping(“doctype” → “CRM Notification”, “from\_user” → Platform.session.user, “to\_user” → user, “type” → “Automation”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Notification”, “from\_user” → Platform.session.user, “to\_user” → user, “type” → “Automation”, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Notification”, “from\_user” → Platform.session.user, “to\_user” → user, “type” → “Automation”, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L79) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L235) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L216)

## Service · Events

<a id="op-4f9eaaad98908b"></a>
### On communication

`operation_relationships_binding_crm_automation_events_on_communication`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If (not \_enabled() or doc.reference\_doctype does not belong to CRM\_REFERENCE\_DOCTYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not \_enabled() → doc.reference\_doctype does not belong to CRM\_REFERENCE\_DOCTYPES.
  - Return no value.
- If doc.communication\_type differs from “Communication”.
  - Return no value.
- Set event from “crm.prospect\_message\_sent” when doc.sent\_or\_received equals “Sent”, otherwise “crm.prospect\_message\_received”.
  - Value choice on doc.sent\_or\_received equals “Sent” — true gives “crm.prospect\_message\_sent”, false gives “crm.prospect\_message\_received”.
- Set thread from \_email\_thread\_key(doc).
- Set payload from \_message\_payload(doc, doc.name, “Email”, thread).
- Evaluate \_emit\_correlated(event, doc, payload, list(thread, \_record\_key(doc))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L95) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L251) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L232)

<a id="op-73f0e7f74312d8"></a>
### On whatsapp message

`operation_relationships_binding_crm_automation_events_on_whatsapp_message`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If (not \_enabled() or doc.reference\_doctype does not belong to CRM\_REFERENCE\_DOCTYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not \_enabled() → doc.reference\_doctype does not belong to CRM\_REFERENCE\_DOCTYPES.
  - Return no value.
- Set outgoing from doc.get(“type”) equals “Outgoing”.
- Set event from “crm.prospect\_message\_sent” when outgoing, otherwise “crm.prospect\_message\_received”.
  - Value choice on outgoing — true gives “crm.prospect\_message\_sent”, false gives “crm.prospect\_message\_received”.
- Set thread from doc.get(“message\_id”) when outgoing, otherwise doc.get(“reply\_to\_message\_id”).
  - Value choice on outgoing — true gives doc.get(“message\_id”), false gives doc.get(“reply\_to\_message\_id”).
- Set payload from \_message\_payload(doc, doc.name, “WhatsApp”, thread).
- Evaluate \_emit\_correlated(event, doc, payload, list(thread, \_record\_key(doc))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L98) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L254) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L235)

<a id="op-301fae5757f210"></a>
### On lead update

`operation_relationships_binding_crm_automation_events_on_lead_update`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If (not \_enabled() or not doc.has\_value\_changed(“status”) or doc.status differs from QUALIFIED\_STATUS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not \_enabled() → not doc.has\_value\_changed(“status”) → doc.status differs from QUALIFIED\_STATUS.
  - Return no value.
- Evaluate emit(“crm.lead\_qualified”, doc = doc, payload = mapping(“lead” → doc.name, “status” → doc.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L97) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L253) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L234)

<a id="op-ccfaa3fcb0e9c9"></a>
### On deal update

`operation_relationships_binding_crm_automation_events_on_deal_update`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If (not \_enabled() or not doc.has\_value\_changed(“status”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not \_enabled() → not doc.has\_value\_changed(“status”).
  - Return no value.
- Set before from doc.get\_doc\_before\_save().
- Set payload from mapping(“deal” → doc.name, “status” → doc.status, “previous\_status” → before.status when before, otherwise no value).
  - Value choice on before — true gives before.status, false gives no value.
- Evaluate emit(“crm.deal\_stage\_changed”, doc = doc, payload = payload, correlation\_key = doc.name).
- Evaluate \_emit\_deal\_outcome(doc, payload).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L96) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L252) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L233)

<a id="op-ff950471bff59e"></a>
### Emit lead converted

`operation_relationships_binding_crm_automation_events_emit_lead_converted`

**Inputs** lead, deal, contact = no value, organization = no value.

**Explicit results** no value.

**Local steps**

- If not \_enabled().
  - Return no value.
- Set payload from mapping(“lead” → lead.name, “deal” → deal, “contact” → contact, “organization” → organization).
- Evaluate emit(“crm.lead\_converted”, doc = lead, payload = payload, correlation\_key = lead.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L89) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L245) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L226)
