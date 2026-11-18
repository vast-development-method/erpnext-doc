# Workflow, automation and dispatch · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Auto repeat

[Record definition](../../../../data/record-types/auto_repeat.json)

<a id="op-d53d09b0712fb9"></a>
### Update reference

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_update_reference`

**Inputs** docname, reference.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Auto Repeat” via get\_doc.

**State and service calls** call db\_set on doc.

**Explicit results** “success”.

**Local steps**

- Set doc from Platform.get\_doc(“Auto Repeat”, str(docname)).
- Evaluate doc.check\_permission(“write”).
- Evaluate Platform.has\_permission(doc.reference\_doctype, “write”, str(reference), throw = true).
- Evaluate doc.db\_set(“reference\_document”, str(reference)).
- Return “success”.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”), Platform.has\_permission(doc.reference\_doctype, “write”, str(reference), throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L5116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L224)

<a id="op-bb9ca0bd3d9e77"></a>
### Generate message preview

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_generate_message_preview`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Auto Repeat” via get\_doc · resolve a document from auto\_repeat.reference\_doctype via get\_doc.

**Explicit results** mapping(“message” → msg\_preview, “subject” → subject\_preview).

**Local steps**

- Evaluate Platform.has\_permission(“Auto Repeat”, “write”, throw = true).
- Set auto\_repeat from Platform.get\_doc(“Auto Repeat”, str(name)).
- Set doc from Platform.get\_doc(auto\_repeat.reference\_doctype, auto\_repeat.reference\_document).
- Evaluate doc.check\_permission().
- Set subject\_preview from translated “Please add a subject to your email”.
- Set msg\_preview from Platform.render\_template(auto\_repeat.message, mapping(“doc” → doc), restrict\_globals = true).
- If auto\_repeat.subject.
  - Set subject\_preview from Platform.render\_template(auto\_repeat.subject, mapping(“doc” → doc), restrict\_globals = true).
- Return mapping(“message” → msg\_preview, “subject” → subject\_preview).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Auto Repeat”, “write”, throw = true), doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L5380) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L217)

## Record · Automation event subscription

<a id="op-7fa434e330ffcf"></a>
### Automation Event Subscription.autoname

`operation_foundation_binding_foundation_automation_doctype_automation_event_subscription_automation_event_subscription_automationeventsubscription_autoname`

**Inputs** self.

**Local steps**

- Set value from formatted text {self.run}:{self.step\_key}.
- Set self.name from hashlib.sha256(value.encode()).hexdigest().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L262)

<a id="op-ae405d3eddb3e8"></a>
### On doctype update

`operation_foundation_binding_foundation_automation_doctype_automation_event_subscription_automation_event_subscription_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Automation Event Subscription”.

**Local steps**

- Evaluate Platform.db.add\_index(“Automation Event Subscription”, list(“event\_name”, “correlation\_key”, “status”), index\_name = “event\_correlation\_status”).
- Evaluate Platform.db.add\_index(“Automation Event Subscription”, list(“status”, “expires\_at”), index\_name = “event\_expiry\_status”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L263)

## Record · Automation flow

<a id="op-25ebe647b5256c"></a>
### Automation Flow.validate

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_document\_type().
- Evaluate self.validate\_trigger\_config().
- Evaluate self.validate\_execution\_identity().
- Evaluate self.validate\_actions().
- If self.enabled.
  - Evaluate self.validate\_ready\_to\_enable().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate document type](operations-008.md#op-040fafd65e2407), [validate trigger config](operations-008.md#op-5cf80587b7eccc), [validate execution identity](operations-008.md#op-786c94e70dacd3), [validate actions](operations-008.md#op-2e85be47183914), [validate ready to enable](operations-008.md#op-0965f0815f5037).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L54) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L270)

<a id="op-0965f0815f5037"></a>
### Automation Flow.validate ready to enable

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_ready_to_enable`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enable an Automation Flow only after adding at least one action”.

**Local steps**

- If not self.actions.
  - Call the validation error handler Platform.throw(translated “Enable an Automation Flow only after adding at least one action”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L281)

<a id="op-2e85be47183914"></a>
### Automation Flow.validate actions

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_actions`

**Inputs** self.

**Local steps**

- Bind dependencies get\_action.
- Set keys from set().
- Set targets from self.get\_action\_targets().
- For each row in self.actions.
  - Evaluate self.set\_step\_key(row, keys).
  - Evaluate self.validate\_step(row).
  - Evaluate self.validate\_branch(row).
  - Evaluate self.validate\_action\_aliases(row, targets).
  - If row.step\_type belongs to tuple(expanded WAIT\_STEP\_TYPES, “If”).
    - Continue with the next iteration or loop test.
  - Set action from get\_action(row.action\_type).
  - Evaluate self.validate\_action\_context(action).
  - Evaluate self.validate\_action\_params(action, row, targets).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get action targets](operations-008.md#op-1e4b98568c0be5), [set step key](operations-008.md#op-3fbb8216a93a97), [validate step](operations-008.md#op-4a7aa8e1470503), [validate branch](operations-008.md#op-ba2258cfae74f9), [validate action aliases](operations-008.md#op-d3b6931b325497), [validate action context](operations-008.md#op-685b931036f263), [validate action params](operations-008.md#op-145547a49b3543).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L274)

<a id="op-145547a49b3543"></a>
### Automation Flow.validate action params

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_action_params`

**Inputs** self, action, row, targets.

**Explicit failure paths** validation helper — translated “Row {0}: {1}”.format(row.idx, str(e)).

**Local steps**

- Bind dependencies AutomationParamError.
- Set params from Platform.parse\_json(row.params) when row.params, otherwise mapping().
  - Value choice on row.params — true gives Platform.parse\_json(row.params), false gives mapping().
- Attempt the following.
  - Evaluate action.validate(params, targets.get(row.target)).
- On failure (AutomationParamError) bound to e.
  - Call the validation error handler Platform.throw(translated “Row {0}: {1}”.format(row.idx, str(e))).
- Evaluate targets.update(action.output\_targets(params, row.output\_alias)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L273)

<a id="op-1e4b98568c0be5"></a>
### Automation Flow.get action targets

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_get_action_targets`

**Inputs** self.

**Explicit results** get\_relationship\_targets(self.document\_type, self.relationships).

**Local steps**

- Bind dependencies get\_relationship\_targets.
- Return get\_relationship\_targets(self.document\_type, self.relationships).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L264)

<a id="op-d3b6931b325497"></a>
### Automation Flow.validate action aliases

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_action_aliases`

**Inputs** self, row, targets.

**Explicit failure paths** validation helper — translated “Row {0}: unknown target alias {1}”.format(row.idx, row.target) · validation helper — translated “Row {0}: duplicate output alias {1}”.format(row.idx, row.output\_alias).

**Local steps**

- Bind dependencies validate\_related\_condition.
- Set row.target from (row.target or “trigger”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.target → “trigger”.
- If row.target does not belong to targets.
  - Call the validation error handler Platform.throw(translated “Row {0}: unknown target alias {1}”.format(row.idx, row.target)).
- Evaluate validate\_related\_condition(row.related\_condition, targets).
- If (row.output\_alias and row.output\_alias belongs to targets).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.output\_alias → row.output\_alias belongs to targets.
  - Call the validation error handler Platform.throw(translated “Row {0}: duplicate output alias {1}”.format(row.idx, row.output\_alias)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L55) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L271)

<a id="op-3fbb8216a93a97"></a>
### Automation Flow.set step key

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_set_step_key`

**Inputs** self, row, keys.

**Explicit failure paths** validation helper — translated “Row {0}: Step Key must be unique”.format(row.idx).

**Local steps**

- Set row.step\_key from (row.step\_key or formatted text step\_{row.idx}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.step\_key → formatted text step\_{row.idx}.
- If row.step\_key belongs to keys.
  - Call the validation error handler Platform.throw(translated “Row {0}: Step Key must be unique”.format(row.idx)).
- Evaluate keys.add(row.step\_key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L269)

<a id="op-786c94e70dacd3"></a>
### Automation Flow.validate execution identity

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_execution_identity`

**Inputs** self.

**Record and data access** read “User” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Automation User {0} is disabled or missing”.format(self.automation\_user).

**Local steps**

- Set self.run\_as from (self.run\_as or “Automation User”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.run\_as → “Automation User”.
- If self.run\_as differs from “Automation User”.
  - Return no value.
- Set self.automation\_user from (self.automation\_user or “Administrator”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.automation\_user → “Administrator”.
- If not Platform.db.get\_value(“User”, self.automation\_user, “enabled”).
  - Call the validation error handler Platform.throw(translated “Automation User {0} is disabled or missing”.format(self.automation\_user)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L279)

<a id="op-ba2258cfae74f9"></a>
### Automation Flow.validate branch

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_branch`

**Inputs** self, row.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Branch is only meaningful inside an If step”.format(row.idx) · validation helper — translated “Row {0}: Parent Step must be an earlier row”.format(row.idx) · validation helper — translated “Row {0}: Parent Step {1} is not an If step”.format(row.idx, row.parent\_step) · validation helper — translated “Row {0}: choose the If or Else branch”.format(row.idx).

**Local steps**

- If not row.parent\_step.
  - If row.branch.
    - Call the validation error handler Platform.throw(translated “Row {0}: Branch is only meaningful inside an If step”.format(row.idx)).
  - Return no value.
- If row.parent\_step ≥ row.idx.
  - Call the validation error handler Platform.throw(translated “Row {0}: Parent Step must be an earlier row”.format(row.idx)).
- If not self.if\_step\_at(row.parent\_step).
  - Call the validation error handler Platform.throw(translated “Row {0}: Parent Step {1} is not an If step”.format(row.idx, row.parent\_step)).
- If row.branch does not belong to tuple(“If”, “Else”).
  - Call the validation error handler Platform.throw(translated “Row {0}: choose the If or Else branch”.format(row.idx)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [if step at](operations-008.md#op-8f8c046b564a3f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L275)

<a id="op-8f8c046b564a3f"></a>
### Automation Flow.if step at

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_if_step_at`

**Inputs** self, idx.

**Explicit results** next(generator of r for r drawn from self.actions where (r.idx equals idx and r.step\_type equals “If”), no value).

**Local steps**

- Return next(generator of r for r drawn from self.actions where (r.idx equals idx and r.step\_type equals “If”), no value).
  - Draw r from self.actions, keep a combination only if ((r.idx equals idx and r.step\_type equals “If”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in r.idx equals idx → r.step\_type equals “If”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L265)

<a id="op-685b931036f263"></a>
### Automation Flow.validate action context

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_action_context`

**Inputs** self, action.

**Explicit failure paths** validation helper — translated “{0} requires a Document Type”.format(action.label) · validation helper — translated “{0} does not support {1} triggers”.format(action.label, self.trigger\_type).

**Local steps**

- If (action.requires\_document and not self.document\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in action.requires\_document → not self.document\_type.
  - Call the validation error handler Platform.throw(translated “{0} requires a Document Type”.format(action.label)).
- If (action.supported\_trigger\_types and self.trigger\_type does not belong to action.supported\_trigger\_types).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in action.supported\_trigger\_types → self.trigger\_type does not belong to action.supported\_trigger\_types.
  - Call the validation error handler Platform.throw(translated “{0} does not support {1} triggers”.format(action.label, self.trigger\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L272)

<a id="op-4a7aa8e1470503"></a>
### Automation Flow.validate step

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_step`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row {0}: unsupported Step Type {1}”.format(row.idx, row.step\_type) · validation helper — translated “Action Type is required for action steps” · validation helper — translated “Row {0}: an If step needs a Step Condition”.format(row.idx).

**Local steps**

- Set row.step\_type from (row.step\_type or “Action”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.step\_type → “Action”.
- If row.step\_type does not belong to STEP\_TYPES.
  - Call the validation error handler Platform.throw(translated “Row {0}: unsupported Step Type {1}”.format(row.idx, row.step\_type)).
- If (row.step\_type equals “Action” and not row.action\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.step\_type equals “Action” → not row.action\_type.
  - Call the validation error handler Platform.throw(translated “Action Type is required for action steps”).
- If (row.step\_type equals “If” and not row.step\_condition).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.step\_type equals “If” → not row.step\_condition.
  - Call the validation error handler Platform.throw(translated “Row {0}: an If step needs a Step Condition”.format(row.idx)).
- If row.step\_type equals “Wait”.
  - Evaluate self.validate\_wait(row).
- If row.step\_type equals “WaitForEvent”.
  - Evaluate self.validate\_event\_wait(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate wait](operations-008.md#op-e978e9ee249fc0), [validate event wait](operations-008.md#op-cecf142da1c845).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L282)

<a id="op-e978e9ee249fc0"></a>
### Automation Flow.validate wait

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_wait`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Wait steps require a duration value and unit” · validation helper — translated “Row {0}: Wait unit must be one of {1}”.format(row.idx, “, ”.join(WAIT\_UNITS)).

**Local steps**

- Set params from Platform.parse\_json(row.params) when row.params, otherwise mapping().
  - Value choice on row.params — true gives Platform.parse\_json(row.params), false gives mapping().
- If (not params.get(“value”) or not params.get(“unit”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not params.get(“value”) → not params.get(“unit”).
  - Call the validation error handler Platform.throw(translated “Wait steps require a duration value and unit”).
- If params at “unit” does not belong to WAIT\_UNITS.
  - Call the validation error handler Platform.throw(translated “Row {0}: Wait unit must be one of {1}”.format(row.idx, “, ”.join(WAIT\_UNITS))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L284)

<a id="op-cecf142da1c845"></a>
### Automation Flow.validate event wait

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_event_wait`

**Inputs** self, row.

**Local steps**

- Bind dependencies validate\_wait\_params.
- Evaluate validate\_wait\_params(Platform.parse\_json(row.params) when row.params, otherwise mapping()).
  - Value choice on row.params — true gives Platform.parse\_json(row.params), false gives mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L278)

<a id="op-040fafd65e2407"></a>
### Automation Flow.validate document type

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_document_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Automation Flow cannot target a child table: {0}”.format(self.document\_type).

**Local steps**

- If (self.document\_type and Platform.get\_meta(self.document\_type).istable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.document\_type → Platform.get\_meta(self.document\_type).istable.
  - Call the validation error handler Platform.throw(translated “Automation Flow cannot target a child table: {0}”.format(self.document\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L277)

<a id="op-5cf80587b7eccc"></a>
### Automation Flow.validate trigger config

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_trigger_config`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} trigger requires a Document Type”.format(self.trigger\_type) · validation helper — translated “Field Value Changed trigger requires a Trigger Field” · validation helper — translated “Date Based trigger requires a Date Field and a Date Direction” · validation helper — translated “Custom Event trigger requires an event name”.

**Local steps**

- Set needs\_doctype from (self.trigger\_type belongs to DOC\_TRIGGER\_TYPES or self.trigger\_type equals “Date Based”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.trigger\_type belongs to DOC\_TRIGGER\_TYPES → self.trigger\_type equals “Date Based”.
- If (needs\_doctype and not self.document\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in needs\_doctype → not self.document\_type.
  - Call the validation error handler Platform.throw(translated “{0} trigger requires a Document Type”.format(self.trigger\_type)).
- If (self.trigger\_type equals “Field Value Changed” and not self.trigger\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trigger\_type equals “Field Value Changed” → not self.trigger\_field.
  - Call the validation error handler Platform.throw(translated “Field Value Changed trigger requires a Trigger Field”).
- If (self.trigger\_type equals “Date Based” and not (self.date\_field and self.date\_direction)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trigger\_type equals “Date Based” → not (self.date\_field and self.date\_direction).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.date\_field → self.date\_direction.
  - Call the validation error handler Platform.throw(translated “Date Based trigger requires a Date Field and a Date Direction”).
- If (self.trigger\_type equals “Custom Event” and not self.custom\_event).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trigger\_type equals “Custom Event” → not self.custom\_event.
  - Call the validation error handler Platform.throw(translated “Custom Event trigger requires an event name”).
- If self.trigger\_type equals “Field Value Changed”.
  - Evaluate self.validate\_field\_exists(“trigger\_field”).
- If self.trigger\_type equals “Date Based”.
  - Evaluate self.validate\_field\_exists(“date\_field”, fieldtypes = tuple(“Date”, “Datetime”)).
- If self.trigger\_type equals “Scheduled”.
  - Evaluate self.validate\_cron().
- Evaluate self.set\_next\_run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate field exists](operations-008.md#op-09642bf4b71f09), [validate cron](operations-008.md#op-7ae7d561397524), [set next run](operations-008.md#op-75934d45702baf).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L283)

<a id="op-09642bf4b71f09"></a>
### Automation Flow.validate field exists

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_field_exists`

**Inputs** self, fieldname, fieldtypes = no value.

**Explicit failure paths** validation helper — translated “{0}: {1} is not a valid field on {2}”.format(translated self.meta.get\_label(fieldname), value, self.document\_type).

**Local steps**

- Bind dependencies std\_fields.
- Set value from self.get(fieldname).
- Set df from Platform.get\_meta(self.document\_type).get\_field(value).
- Set df from (df or next(generator of f for f drawn from std\_fields where f at “fieldname” equals value, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df → next(generator of f for f drawn from std\_fields where f at “fieldname” equals value, no value).
  - Draw f from std\_fields, keep a combination only if (f at “fieldname” equals value).
- If (not df or (fieldtypes and df.get(“fieldtype”) does not belong to fieldtypes)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → (fieldtypes and df.get(“fieldtype”) does not belong to fieldtypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtypes → df.get(“fieldtype”) does not belong to fieldtypes.
  - Call the validation error handler Platform.throw(translated “{0}: {1} is not a valid field on {2}”.format(translated self.meta.get\_label(fieldname), value, self.document\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L280)

<a id="op-75934d45702baf"></a>
### Automation Flow.set next run

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_set_next_run`

**Inputs** self.

**Local steps**

- Bind dependencies next\_fire.
- If self.trigger\_type differs from “Scheduled”.
  - Set self.next\_run from no value.
- Otherwise.
  - If (self.has\_value\_changed(“cron\_expression”) or not self.next\_run).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“cron\_expression”) → not self.next\_run.
    - Set self.next\_run from next\_fire(self.cron\_expression, Platform.utils.now\_datetime()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L268)

<a id="op-7ae7d561397524"></a>
### Automation Flow.validate cron

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_validate_cron`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Scheduled trigger requires a Cron Expression” · validation helper — translated “Invalid cron expression: {0}”.format(self.cron\_expression).

**Local steps**

- Bind dependencies croniter.
- If not self.cron\_expression.
  - Call the validation error handler Platform.throw(translated “Scheduled trigger requires a Cron Expression”).
- If not croniter.is\_valid(self.cron\_expression).
  - Call the validation error handler Platform.throw(translated “Invalid cron expression: {0}”.format(self.cron\_expression)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L276)

<a id="op-22b3463aebd6b6"></a>
### Automation Flow.on update

`operation_foundation_binding_foundation_automation_doctype_automation_flow_automation_flow_automationflow_on_update`

**Inputs** self.

**Local steps**

- Evaluate clear\_automation\_cache(self.document\_type).
- Set before from self.get\_doc\_before\_save().
- If (before and before.document\_type and before.document\_type differs from self.document\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.document\_type → before.document\_type differs from self.document\_type.
  - Evaluate clear\_automation\_cache(before.document\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L51) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L267)
