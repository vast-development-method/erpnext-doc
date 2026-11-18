# Workflow, automation and dispatch · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Conditions

<a id="op-5ebcb687cd9ed2"></a>
### Condition fieldnames

`operation_foundation_binding_foundation_automation_engine_conditions_condition_fieldnames`

**Inputs** condition.

**Declared result** (set at str bitwise or no value).

**Explicit results** no value · names.

**Local steps**

- Attempt the following.
  - Set tree from ast.parse((condition or empty text), mode = “eval”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition → empty text.
- On failure (tuple(SyntaxError, ValueError)).
  - Return no value.
- Set names from set().
- For each node in ast.walk(tree).
  - If not isinstance(node, ast.Attribute).
    - Continue with the next iteration or loop test.
  - If (not isinstance(node.value, ast.Name) or node.value.id differs from “doc”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(node.value, ast.Name) → node.value.id differs from “doc”.
    - Return no value.
  - Evaluate names.add(node.attr).
- Return names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L361)

<a id="op-f15cfc67e29e32"></a>
### Condition values

`operation_foundation_binding_foundation_automation_engine_conditions_condition_values`

**Inputs** condition, scope.

**Declared result** dict.

**Explicit results** mapping() · values.

**Local steps**

- Attempt the following.
  - Set tree from ast.parse((condition or empty text), mode = “eval”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition → empty text.
- On failure (tuple(SyntaxError, ValueError)).
  - Return mapping().
- Set values from mapping().
- For each node in ast.walk(tree).
  - If (not isinstance(node, ast.Attribute) or not isinstance(node.value, ast.Name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(node, ast.Attribute) → not isinstance(node.value, ast.Name).
    - Continue with the next iteration or loop test.
  - Set record from scope.get(node.value.id).
  - If record is identical to no value.
    - Continue with the next iteration or loop test.
  - Set values at formatted text {node.value.id}.{node.attr} from record.get(node.attr).
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L362)

<a id="op-4ecd2cc9e93014"></a>
### Validate condition

`operation_foundation_binding_foundation_flow_utils_conditions_validate_condition`

**Inputs** condition.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Condition must be a single Python expression: {0}”.format(str(e)).

**Local steps**

- If not condition.
  - Return no value.
- Attempt the following.
  - Evaluate ast.parse(condition, mode = “eval”).
- On failure (SyntaxError) bound to e.
  - Call the validation error handler Platform.throw(translated “Condition must be a single Python expression: {0}”.format(str(e)), title = translated “Invalid Condition”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1423)

<a id="op-7187a83975494c"></a>
### Evaluate condition

`operation_foundation_binding_foundation_flow_utils_conditions_evaluate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** condition, context.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0005.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1422)

## Service · Config

<a id="op-4d484338452a70"></a>
### Get config

`operation_foundation_realtime_configuration_business_behavior_get_configuration`

**Inputs** sites\_path = no value, embedded = false.

**Declared result** RealtimeConfig.

**Explicit results** RealtimeConfig(port = int((conf.get(“socketio\_port”) or DEFAULT\_SOCKETIO\_PORT)), redis\_queue = (conf.get(“redis\_queue”) or DEFAULT\_REDIS\_QUEUE), uds = (conf.get(“socketio\_uds”) or no value), default\_site = ….

**Local steps**

- Bind dependencies Platform.
- Set default\_sites\_path from “sites” when os.path.isdir(“sites”), otherwise “.”.
  - Value choice on os.path.isdir(“sites”) — true gives “sites”, false gives “.”.
- Set sites\_path from os.path.abspath((sites\_path or getattr(Platform.local, “sites\_path”, no value) or default\_sites\_path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sites\_path → getattr(Platform.local, “sites\_path”, no value) → default\_sites\_path.
- Set conf from Platform.get\_common\_site\_config(sites\_path = sites\_path).
- Set webserver\_port from conf.get(“webserver\_port”).
- Return RealtimeConfig(port = int((conf.get(“socketio\_port”) or DEFAULT\_SOCKETIO\_PORT)), redis\_queue = (conf.get(“redis\_queue”) or DEFAULT\_REDIS\_QUEUE), uds = (conf.get(“socketio\_uds”) or no value), default\_site = ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“socketio\_port”) → DEFAULT\_SOCKETIO\_PORT.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“redis\_queue”) → DEFAULT\_REDIS\_QUEUE.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“socketio\_uds”) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“default\_site”) → no value.
  - Value choice on webserver\_port — true gives int(webserver\_port), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“webserver\_host”) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“socketio\_worker\_threads”) → DEFAULT\_WORKER\_THREADS.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “sites\_path”, no value).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L110) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L244)

## Service · Context

<a id="op-5a7a2d72f6bc64"></a>
### Platform context

`operation_foundation_realtime_context_business_behavior_foundation_context`

**Inputs** site, user.

**Wrappers, in declaration order** contextmanager.

**State and service calls** commit · rollback.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies Platform.
- Evaluate Platform.init(site, force = true).
- Evaluate Platform.connect().
- Evaluate Platform.set\_user(user).
- Attempt the following.
  - yield Platform.
  - Evaluate Platform.db.commit().
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Propagate the active failure.
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0323.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L245)

## Service · Core

<a id="op-55164b7fe0da68"></a>
### Require doc

`operation_foundation_binding_foundation_automation_engine_actions_core_require_doc`

**Inputs** doc, action\_type.

**Explicit failure paths** AutomationParamError(translated “{0} requires a target document”.format(action\_type)).

**Local steps**

- If doc is identical to no value.
  - Raise AutomationParamError(translated “{0} requires a target document”.format(action\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L325)

<a id="op-f83d2358a9f60d"></a>
### As list

`operation_foundation_binding_foundation_automation_engine_actions_core_as_list`

**Inputs** value.

**Declared result** list.

**Explicit results** list() · list(parsed) when isinstance(parsed, list), otherwise list(parsed) · list(value).

**Local steps**

- If not value.
  - Return list().
- If isinstance(value, str).
  - Set parsed from Platform.parse\_json(value) when value.strip().startswith(“&#91;”), otherwise value.
    - Value choice on value.strip().startswith(“&#91;”) — true gives Platform.parse\_json(value), false gives value.
  - Return list(parsed) when isinstance(parsed, list), otherwise list(parsed).
    - Value choice on isinstance(parsed, list) — true gives list(parsed), false gives list(parsed).
- Return list(value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L307)

<a id="op-e20368e305e080"></a>
### Set Field Value.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_setfieldvalue_validate`

**Inputs** self, params, doctype.

**Explicit results** no value.

**Explicit failure paths** AutomationParamError(translated “Set at least one field”, fieldname = “field”) · AutomationParamError(translated “{0} has no field {1}”.format(doctype, field), fieldname = “field”).

**Local steps**

- Set pairs from self.\_pairs(params).
- If not pairs.
  - Raise AutomationParamError(translated “Set at least one field”, fieldname = “field”).
- If not doctype.
  - Return no value.
- Set meta from Platform.get\_meta(doctype).
- For each field in pairs.
  - If not meta.get\_field(field).
    - Raise AutomationParamError(translated “{0} has no field {1}”.format(doctype, field), fieldname = “field”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pairs](operations-016.md#op-74840a49d149df).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L339)

<a id="op-49131cff89bcde"></a>
### Set Field Value.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_setfieldvalue_execute`

**Inputs** self, doc, params, context.

**State and service calls** call save on doc.

**Explicit results** translated “Set {0}”.format(“, ”.join(pairs)).

**Local steps**

- Evaluate \_require\_doc(doc, self.label).
- Set pairs from self.\_pairs(params).
- For each tuple(field, value) in pairs.items().
  - Evaluate doc.set(field, render\_value(value, doc, context)).
- Evaluate doc.save().
- Return translated “Set {0}”.format(“, ”.join(pairs)).

**Methods declared on this owner** [pairs](operations-016.md#op-74840a49d149df).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L337)

<a id="op-74840a49d149df"></a>
### Set Field Value.pairs

`operation_foundation_binding_foundation_automation_engine_actions_core_setfieldvalue_pairs`

**Inputs** self, params.

**Declared result** dict.

**Explicit results** pairs.

**Local steps**

- Set values from (params.get(“values”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“values”) → mapping().
- If isinstance(values, str).
  - Set values from (Platform.parse\_json(values) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(values) → mapping().
- Set pairs from dict(values).
- If params.get(“field”).
  - Set pairs at params at “field” from params.get(“value”).
- Return pairs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L338)

<a id="op-2950e80ecddfe0"></a>
### Create Document.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_createdocument_validate`

**Inputs** self, params, doctype.

**Record and data access** read “DocType” via exists.

**Explicit failure paths** AutomationParamError(translated “Target Document Type is required”, fieldname = “doctype”) · AutomationParamError(translated “Unknown DocType”, fieldname = “doctype”).

**Local steps**

- If not params.get(“doctype”).
  - Raise AutomationParamError(translated “Target Document Type is required”, fieldname = “doctype”).
- If not Platform.db.exists(“DocType”, params.get(“doctype”)).
  - Raise AutomationParamError(translated “Unknown DocType”, fieldname = “doctype”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L317)

<a id="op-24b51a59f3dd95"></a>
### Create Document.output doctype

`operation_foundation_binding_foundation_automation_engine_actions_core_createdocument_output_doctype`

**Inputs** self, params.

**Explicit results** params.get(“doctype”).

**Local steps**

- Return params.get(“doctype”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L316)

<a id="op-09a64e9415b55e"></a>
### Create Document.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_createdocument_execute`

**Inputs** self, doc, params, context.

**State and service calls** request new\_doc for params at “doctype” · call insert on target.

**Explicit results** mapping(“detail” → translated “Created {0} {1}”.format(params at “doctype”, target.name), “destination\_reference” → mapping(“doctype” → target.doctype, “name” → target.name)).

**Local steps**

- Set target from Platform.new\_doc(params at “doctype”).
- Set values from params.get(“values”).
- If isinstance(values, str).
  - Set values from Platform.parse\_json(values).
- For each tuple(field, value) in (values or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → mapping().
  - Evaluate target.set(field, render\_value(value, doc, context)).
- Evaluate target.insert().
- Return mapping(“detail” → translated “Created {0} {1}”.format(params at “doctype”, target.name), “destination\_reference” → mapping(“doctype” → target.doctype, “name” → target.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L315)

<a id="op-ac5a4adb0f0a75"></a>
### Increment Field Value.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_incrementfieldvalue_validate`

**Inputs** self, params, doctype.

**Explicit results** no value.

**Explicit failure paths** AutomationParamError(translated “Field is required”, fieldname = “field”) · AutomationParamError(translated “Choose a numeric field”, fieldname = “field”).

**Local steps**

- Set field from params.get(“field”).
- If not field.
  - Raise AutomationParamError(translated “Field is required”, fieldname = “field”).
- If not doctype.
  - Return no value.
- Set df from Platform.get\_meta(doctype).get\_field(field).
- If (not df or df.fieldtype does not belong to NUMERIC\_FIELDTYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → df.fieldtype does not belong to NUMERIC\_FIELDTYPES.
  - Raise AutomationParamError(translated “Choose a numeric field”, fieldname = “field”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L105) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L321)

<a id="op-f95dd92783382a"></a>
### Increment Field Value.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_incrementfieldvalue_execute`

**Inputs** self, doc, params, context.

**State and service calls** call save on doc.

**Explicit results** mapping(“detail” → translated “Changed {0} by {1}”.format(field, amount), “old\_value” → old\_value, “new\_value” → (old\_value + amount), “delta” → amount).

**Local steps**

- Evaluate \_require\_doc(doc, self.label).
- Set field from params at “field”.
- Set amount from flt(render\_value(params.get(“amount”), doc, context)).
- Evaluate self.\_lock(doc).
- Evaluate doc.reload().
- Set old\_value from flt(doc.get(field)).
- Evaluate doc.set(field, (old\_value + amount)).
- Evaluate doc.save().
- Return mapping(“detail” → translated “Changed {0} by {1}”.format(field, amount), “old\_value” → old\_value, “new\_value” → (old\_value + amount), “delta” → amount).

**Methods declared on this owner** [lock](operations-016.md#op-7c56be97fcf395).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L319)

<a id="op-7c56be97fcf395"></a>
### Increment Field Value.lock

`operation_foundation_binding_foundation_automation_engine_actions_core_incrementfieldvalue_lock`

**Inputs** self, doc.

**Local steps**

- Set table from Platform.qb.DocType(doc.doctype).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals nested operand in the contract.name).for\_update().run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L320)

<a id="op-2494e9757119d9"></a>
### Recipient tokens

`operation_foundation_binding_foundation_automation_engine_actions_core_recipient_tokens`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“name” → OWNER\_TOKEN, “full\_name” → translated “Document owner”), mapping(“name” → ASSIGNEES\_TOKEN, “full\_name” → translated “Assignees”)).

**Local steps**

- Return list(mapping(“name” → OWNER\_TOKEN, “full\_name” → translated “Document owner”), mapping(“name” → ASSIGNEES\_TOKEN, “full\_name” → translated “Assignees”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L107) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L323)

<a id="op-198419898976d0"></a>
### Resolve recipients

`operation_foundation_binding_foundation_automation_engine_actions_core_resolve_recipients`

**Inputs** recipients, doc.

**Declared result** list.

**Explicit results** list(dict.fromkeys(generator of user for user drawn from resolved where user)).

**Local steps**

- Set resolved from list().
- For each recipient in recipients.
  - If recipient equals OWNER\_TOKEN.
    - Evaluate resolved.append(doc.owner when doc, otherwise no value).
      - Value choice on doc — true gives doc.owner, false gives no value.
  - Otherwise.
    - If recipient equals ASSIGNEES\_TOKEN.
      - Evaluate resolved.extend(\_assignees(doc)).
    - Otherwise.
      - Evaluate resolved.append(recipient).
- Return list(dict.fromkeys(generator of user for user drawn from resolved where user)).
  - Draw user from resolved, keep a combination only if (user).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L326)

<a id="op-43764d792060bf"></a>
### Assignees

`operation_foundation_binding_foundation_automation_engine_actions_core_assignees`

**Inputs** doc.

**Declared result** list.

**Explicit results** list() · (Platform.parse\_json((doc.get(“\_assign”) or “&#91;&#93;”)) or list()).

**Local steps**

- If not doc.
  - Return list().
- Return (Platform.parse\_json((doc.get(“\_assign”) or “&#91;&#93;”)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json((doc.get(“\_assign”) or “&#91;&#93;”)) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“\_assign”) → “&#91;&#93;”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L308)

<a id="op-58631d853459c8"></a>
### Send Notification.validate

`operation_foundation_binding_foundation_automation_engine_actions_core_sendnotification_validate`

**Inputs** self, params, doctype.

**Record and data access** read “Email Template” via exists.

**Explicit failure paths** AutomationParamError(translated “At least one recipient is required”, fieldname = “recipients”) · AutomationParamError(translated “Unknown Email Template”, fieldname = “email\_template”).

**Local steps**

- If not \_as\_list(params.get(“recipients”)).
  - Raise AutomationParamError(translated “At least one recipient is required”, fieldname = “recipients”).
- If (params.get(“email\_template”) and not Platform.db.exists(“Email Template”, params at “email\_template”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in params.get(“email\_template”) → not Platform.db.exists(“Email Template”, params at “email\_template”).
  - Raise AutomationParamError(translated “Unknown Email Template”, fieldname = “email\_template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L336)

<a id="op-b20f299bf7b241"></a>
### Send Notification.execute

`operation_foundation_binding_foundation_automation_engine_actions_core_sendnotification_execute`

**Inputs** self, doc, params, context.

**State and service calls** sendmail.

**Explicit results** translated “No recipients to notify” · self.\_notify\_system(doc, recipients, subject, message) · translated “Emailed {0}”.format(“, ”.join(recipients)).

**Local steps**

- Set tuple(subject, message) from self.\_content(params, doc, context).
- Set recipients from resolve\_recipients(\_as\_list(params.get(“recipients”)), doc).
- If not recipients.
  - Return translated “No recipients to notify”.
- If params.get(“channel”) equals “System”.
  - Return self.\_notify\_system(doc, recipients, subject, message).
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, message = message, reference\_doctype = doc.doctype when doc, otherwise no value, …).
  - Value choice on doc — true gives doc.doctype, false gives no value.
  - Value choice on doc — true gives doc.name, false gives no value.
- Return translated “Emailed {0}”.format(“, ”.join(recipients)).

**Methods declared on this owner** [content](operations-016.md#op-959336f70faecd), [notify system](operations-016.md#op-8ad624fa5b46ce).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, message = message, reference\_doctype = doc.doctype when doc, otherwise no value, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L118) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L334)

<a id="op-959336f70faecd"></a>
### Send Notification.content

`operation_foundation_binding_foundation_automation_engine_actions_core_sendnotification_content`

**Inputs** self, params, doc, context.

**Record and data access** resolve a document from “Email Template” via get\_doc.

**Explicit results** tuple(Platform.render\_template(template.subject, render\_context(doc, context)), Platform.render\_template((template.response or template.response\_html or empty text), render\_context(doc, context))) · tuple(render\_value((params.get(“subject”) or empty text), doc, context), render\_value((params.get(“message”) or empty text), doc, context)).

**Local steps**

- If params.get(“email\_template”).
  - Set template from Platform.get\_doc(“Email Template”, params at “email\_template”).
  - Return tuple(Platform.render\_template(template.subject, render\_context(doc, context)), Platform.render\_template((template.response or template.response\_html or empty text), render\_context(doc, context))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in template.response → template.response\_html → empty text.
- Return tuple(render\_value((params.get(“subject”) or empty text), doc, context), render\_value((params.get(“message”) or empty text), doc, context)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“subject”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“message”) → empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L117) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L333)

<a id="op-8ad624fa5b46ce"></a>
### Send Notification.notify system

`operation_foundation_binding_foundation_automation_engine_actions_core_sendnotification_notify_system`

**Inputs** self, doc, recipients, subject, message.

**Record and data access** resolve a document from mapping(“doctype” → “Notification Log”, “for\_user” → user, “type” → “Alert”, “subject” → subject, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → user, “type” → “Alert”, “subject” → subject, …)).

**Explicit results** translated “Notified {0}”.format(“, ”.join(recipients)).

**Local steps**

- Evaluate \_require\_doc(doc, self.label).
- For each user in recipients.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Notification Log”, “for\_user” → user, “type” → “Alert”, “subject” → subject, …)).insert(ignore\_permissions = true).
- Return translated “Notified {0}”.format(“, ”.join(recipients)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L119) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L335)
