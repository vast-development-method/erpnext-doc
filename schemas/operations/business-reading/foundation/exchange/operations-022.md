# Integration and transport · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Middlewares

<a id="op-c148a81e95fee1"></a>
### Static Data Middleware.invoke

`operation_foundation_middlewares_business_behavior_static_data_middleware_call`

**Inputs** self, environ, start\_response.

**Explicit results** super().\_\_call\_\_(environ, patch\_start\_response).

**Local steps**

- Set self.environ from environ.
- Bind local operation patch\_start\_response for subsequent calls.
- Return super().\_\_call\_\_(environ, patch\_start\_response).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L3194) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L892)

<a id="op-3575d625ae4fc5"></a>
### Static Data Middleware.invoke.patch start response

`operation_foundation_middlewares_business_behavior_static_data_middleware_call_patch_start_response`

**Inputs** status, headers, exc\_info = no value.

**Explicit results** start\_response(status, headers, exc\_info).

**Local steps**

- If (path bound to environ.get(“PATH\_INFO”, empty text) and path.startswith(“/files/”) and path.lower().endswith(FORCE\_DOWNLOAD\_EXTENSIONS)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in path bound to environ.get(“PATH\_INFO”, empty text) → path.startswith(“/files/”) → path.lower().endswith(FORCE\_DOWNLOAD\_EXTENSIONS).
  - Bind dependencies quote.
  - Set filename from Path(path).name.
  - Evaluate headers.append(tuple(“Content-Disposition”, formatted text attachment; filename\*=UTF-8''{quote(filename)})).
- Return start\_response(status, headers, exc\_info).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L3546) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L893)

<a id="op-0cc2558ea5a427"></a>
### Static Data Middleware.get directory loader

`operation_foundation_middlewares_business_behavior_static_data_middleware_get_directory_loader`

**Inputs** self, directory.

**Explicit results** loader.

**Local steps**

- Bind local operation loader for subsequent calls.
- Return loader.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L3816) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L198) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L894)

<a id="op-fb15e394a9cbbb"></a>
### Static Data Middleware.get directory loader.loader

`operation_foundation_middlewares_business_behavior_static_data_middleware_get_directory_loader_loader`

**Inputs** path.

**Explicit results** tuple(path.name, self.\_opener(path)).

**Explicit failure paths** NotFound.

**Local steps**

- Set site from get\_site\_name((Platform.app.\_site or self.environ.get(“HTTP\_HOST”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.app.\_site → self.environ.get(“HTTP\_HOST”).
- Set files\_path from (((Path(directory) ÷ site) ÷ “public”) ÷ “files”).
- Set requested\_path from Path(cstr(path)).
- Set path from (files\_path ÷ requested\_path).resolve().
- If (not path.is\_relative\_to(files\_path) or not path.is\_file()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not path.is\_relative\_to(files\_path) → not path.is\_file().
  - Raise NotFound.
- Return tuple(path.name, self.\_opener(path)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L4175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L895)

## Record · Notification

[Record definition](../../../../data/record-types/notification.json)

<a id="op-0167841579d85a"></a>
### Notification.onload

`operation_foundation_email_record_definitions_notification_business_behavior_notification_onload`

**Inputs** self.

**Local steps**

- If self.is\_standard.
  - Set self.message from self.get\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get template](operations-023.md#op-d4d0fef65cc4e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L6517) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L231)

<a id="op-d43a03c65a14d4"></a>
### Notification.autoname

`operation_foundation_email_record_definitions_notification_business_behavior_notification_autoname`

**Inputs** self.

**Local steps**

- If not self.name.
  - Set self.name from self.subject.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L6592) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L214)

<a id="op-297e413cf46e7b"></a>
### Notification.preview meets condition

`operation_foundation_email_record_definitions_notification_business_behavior_notification_preview_meets_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, preview\_document.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L6665) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L232)

<a id="op-65a56d7917c3f9"></a>
### Notification.preview message

`operation_foundation_email_record_definitions_notification_business_behavior_notification_preview_message`

**Inputs** self, preview\_document.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from self.document\_type via get\_cached\_doc.

**Explicit results** Platform.utils.strip\_html\_tags(msg) · msg · translated “Failed to render message: {}”.format(str(e)).

**Local steps**

- Attempt the following.
  - Set doc from Platform.get\_cached\_doc(self.document\_type, preview\_document).
  - Set template\_content from self.get\_email\_template\_content(doc).
  - If template\_content.
    - Set msg from template\_content at “message”.
  - Otherwise.
    - Set context from get\_context(doc).
    - Evaluate context.update(mapping(“alert” → self, “comments” → get\_comments\_for\_context(doc))).
    - If self.is\_standard.
      - Evaluate self.load\_standard\_properties(context).
    - Set msg from Platform.render\_template(self.message, context, restrict\_globals = true).
  - If self.channel equals “SMS”.
    - Return Platform.utils.strip\_html\_tags(msg).
  - Return msg.
- On failure (Exception) bound to e.
  - Return translated “Failed to render message: {}”.format(str(e)).

**Methods declared on this owner** [get email template content](operations-022.md#op-56cd1eb858af86), [load standard properties](operations-023.md#op-f9f4d5d6e41ed6).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.document\_type, preview\_document).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L109) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L233)

<a id="op-3376339d36bf59"></a>
### Notification.preview subject

`operation_foundation_email_record_definitions_notification_business_behavior_notification_preview_subject`

**Inputs** self, preview\_document.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from self.document\_type via get\_cached\_doc.

**Explicit results** (template\_content at “subject” or translated “No subject”) · translated “No subject” · Platform.render\_template(self.subject, context, restrict\_globals = true) · self.subject · translated “Failed to render subject: {}”.format(str(e)).

**Local steps**

- Attempt the following.
  - Set doc from Platform.get\_cached\_doc(self.document\_type, preview\_document).
  - Set template\_content from self.get\_email\_template\_content(doc).
  - If template\_content.
    - Return (template\_content at “subject” or translated “No subject”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in template\_content at “subject” → translated “No subject”.
  - Set context from get\_context(doc).
  - Evaluate context.update(mapping(“alert” → self, “comments” → get\_comments\_for\_context(doc))).
  - If self.is\_standard.
    - Evaluate self.load\_standard\_properties(context).
  - If not self.subject.
    - Return translated “No subject”.
  - If “{” belongs to self.subject.
    - Return Platform.render\_template(self.subject, context, restrict\_globals = true).
  - Return self.subject.
- On failure (Exception) bound to e.
  - Return translated “Failed to render subject: {}”.format(str(e)).

**Methods declared on this owner** [get email template content](operations-022.md#op-56cd1eb858af86), [load standard properties](operations-023.md#op-f9f4d5d6e41ed6).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(self.document\_type, preview\_document).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L110) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L234)

<a id="op-c85af77bb5353d"></a>
### Notification.before save

`operation_foundation_email_record_definitions_notification_business_behavior_notification_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_invalid\_condition().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove invalid condition](operations-022.md#op-a1a693b0d28417).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L989) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L215)

<a id="op-4995b75d2efa24"></a>
### Notification.validate

`operation_foundation_email_record_definitions_notification_business_behavior_notification_validate`

**Inputs** self.

**Record and data access** resolve a document from “Email Template” via get\_cached\_doc.

**Explicit failure paths** validation helper — translated “Please specify which date field must be checked” · validation helper — translated “Please specify which datetime field must be checked” · validation helper — translated “Please specify the minutes offset” · validation helper — translated “Please specify at least 10 minutes due to the trigger cadence of the scheduler” · validation helper — translated “Please specify which value field must be checked” · 3 additional forms in the steps below.

**Local steps**

- If self.channel belongs to tuple(“Email”, “Slack”, “System Notification”).
  - Evaluate validate\_template(self.subject).
- Evaluate validate\_template(self.message).
- If (self.event belongs to tuple(“Days Before”, “Days After”) and not self.date\_changed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.event belongs to tuple(“Days Before”, “Days After”) → not self.date\_changed.
  - Call the validation error handler Platform.throw(translated “Please specify which date field must be checked”).
- If self.event belongs to tuple(“Minutes Before”, “Minutes After”).
  - If not self.datetime\_changed.
    - Call the validation error handler Platform.throw(translated “Please specify which datetime field must be checked”).
  - If not self.minutes\_offset.
    - Call the validation error handler Platform.throw(translated “Please specify the minutes offset”).
  - If self.minutes\_offset &lt; 10.
    - Call the validation error handler Platform.throw(translated “Please specify at least 10 minutes due to the trigger cadence of the scheduler”).
- If (self.event equals “Value Change” and not self.value\_changed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.event equals “Value Change” → not self.value\_changed.
  - Call the validation error handler Platform.throw(translated “Please specify which value field must be checked”).
- If (self.attach\_files equals “From Field” and not self.from\_attach\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attach\_files equals “From Field” → not self.from\_attach\_field.
  - Call the validation error handler Platform.throw(translated “Please specify the field from which to attach files”).
- If (self.email\_template and self.channel differs from “Email”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.email\_template → self.channel differs from “Email”.
  - Call the validation error handler Platform.throw(translated “Email Template can only be used with the Email channel”).
- If self.email\_template.
  - Set email\_template from Platform.get\_cached\_doc(“Email Template”, self.email\_template).
  - If not email\_template.response\_.
    - Call the validation error handler Platform.throw(translated “Email Template {0} has no content to send”.format(self.email\_template)).
- Evaluate self.validate\_forbidden\_document\_types().
- Evaluate self.validate\_condition().
- Evaluate self.validate\_filters().
- Evaluate self.validate\_standard().
- Evaluate clear\_notification\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate forbidden document types](operations-022.md#op-7c4f75c99ada45), [validate condition](operations-022.md#op-201517239cb1e1), [validate filters](operations-022.md#op-ca6410faa400b3), [validate standard](operations-022.md#op-6b9aae66f9ab60).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Email Template”, self.email\_template).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L114) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L242)

<a id="op-34d61f66cdd42b"></a>
### Notification.clear cache

`operation_foundation_email_record_definitions_notification_business_behavior_notification_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- Evaluate clear\_notification\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L1717) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L216)

<a id="op-32341cae00d05c"></a>
### Notification.on update

`operation_foundation_email_record_definitions_notification_business_behavior_notification_on_update`

**Inputs** self.

**Local steps**

- Set path from export\_module\_json(self, self.is\_standard, self.module).
- If (path and self.message).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in path → self.message.
  - Set extension from FORMATS.get(self.message\_type, “.md”).
  - Set file\_path from (path + extension).
  - Within open(file\_path, “w”) bound as f.
    - Evaluate f.write(self.message).
  - If not os.path.exists((path + “.py”)).
    - Within open((path + “.py”), “w”) bound as f.
      - Evaluate f.write(multiline text in the contract).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L1790) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L230)

<a id="op-6b9aae66f9ab60"></a>
### Notification.validate standard

`operation_foundation_email_record_definitions_notification_business_behavior_notification_validate_standard`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot edit Standard Notification. To edit, please disable this and duplicate it”.

**Local steps**

- If (self.is\_standard and self.enabled and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.enabled → not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Cannot edit Standard Notification. To edit, please disable this and duplicate it”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2155) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L246)

<a id="op-a1a693b0d28417"></a>
### Notification.remove invalid condition

`operation_foundation_email_record_definitions_notification_business_behavior_notification_remove_invalid_condition`

**Inputs** self.

**Local steps**

- If self.condition\_type equals “Filters”.
  - Set self.condition from no value.
- Otherwise.
  - If self.condition\_type equals “Python”.
    - Set self.filters from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2269) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L236)

<a id="op-201517239cb1e1"></a>
### Notification.validate condition

`operation_foundation_email_record_definitions_notification_business_behavior_notification_validate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2384) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L243)

<a id="op-ca6410faa400b3"></a>
### Notification.validate filters

`operation_foundation_email_record_definitions_notification_business_behavior_notification_validate_filters`

**Inputs** self.

**State and service calls** request new\_doc for self.document\_type.

**Explicit results** no value.

**Local steps**

- If not self.filters.
  - Return no value.
- Set filters from json.loads(self.filters).
- Set dummy\_doc from Platform.new\_doc(self.document\_type).
- Evaluate evaluate\_filters(dummy\_doc, filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2611) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L244)

<a id="op-7c4f75c99ada45"></a>
### Notification.validate forbidden document types

`operation_foundation_email_record_definitions_notification_business_behavior_notification_validate_forbidden_document_types`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot set Notification with event {0} on Document Type {1}”.format(translated self.event, translated self.document\_type).

**Local steps**

- If (self.document\_type belongs to FORBIDDEN\_DOCUMENT\_TYPES or (Platform.get\_meta(self.document\_type).istable and self.event does not belong to DATE\_BASED\_EVENTS)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.document\_type belongs to FORBIDDEN\_DOCUMENT\_TYPES → (Platform.get\_meta(self.document\_type).istable and self.event does not belong to DATE\_BASED\_EVENTS).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_meta(self.document\_type).istable → self.event does not belong to DATE\_BASED\_EVENTS.
  - Call the validation error handler Platform.throw(translated “Cannot set Notification with event {0} on Document Type {1}”.format(translated self.event, translated self.document\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2758) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L245)

<a id="op-b3f442b8bc4d11"></a>
### Notification.get documents for today

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_documents_for_today`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L2969) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L222)

<a id="op-d5654a8b25fe91"></a>
### Notification.get documents for this moment

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_documents_for_this_moment`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L3577) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L221)

<a id="op-126a84adf39b5f"></a>
### Notification.queue send

`operation_foundation_email_record_definitions_notification_business_behavior_notification_queue_send`

**Inputs** self, doc, enqueue\_after\_commit = true.

**Explicit results** enqueue(“Platform.email.doctype.notification.notification.evaluate\_alert”, doc = doc, alert = self, now = Platform.in\_test, enqueue\_after\_commit = enqueue\_after\_commit).

**Local steps**

- Bind dependencies enqueue.
- Return enqueue(“Platform.email.doctype.notification.notification.evaluate\_alert”, doc = doc, alert = self, now = Platform.in\_test, enqueue\_after\_commit = enqueue\_after\_commit).

**Values supplied outside this operation** service or queued work from enqueue(“Platform.email.doctype.notification.notification.evaluate\_alert”, doc = doc, alert = self, now = Platform.in\_test, enqueue\_after\_commit = enqueue\_after\_commit).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L4331) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L235)

<a id="op-0432c96759e981"></a>
### Notification.send

`operation_foundation_email_record_definitions_notification_business_behavior_notification_send`

**Inputs** self, doc.

**State and service calls** call save on doc.

**Local steps**

- Set context from get\_context(doc).
- Evaluate context.update(mapping(“alert” → self, “comments” → get\_comments\_for\_context(doc))).
- If self.is\_standard.
  - Evaluate self.load\_standard\_properties(context).
- Evaluate self.send\_notification\_by\_channel(doc, context).
- If self.set\_property\_after\_alert.
  - Set allow\_update from true.
  - If (doc.docstatus.is\_submitted() and not doc.meta.get\_field(self.set\_property\_after\_alert).allow\_on\_submit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus.is\_submitted() → not doc.meta.get\_field(self.set\_property\_after\_alert).allow\_on\_submit.
    - Set allow\_update from false.
  - Attempt the following.
    - If (allow\_update and not doc.flags.in\_notification\_update).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in allow\_update → not doc.flags.in\_notification\_update.
      - Set fieldname from self.set\_property\_after\_alert.
      - Set value from self.property\_value.
      - If doc.meta.get\_field(fieldname).fieldtype belongs to Platform.model.numeric\_fieldtypes.
        - Set value from Platform.utils.cint(value).
      - Evaluate doc.reload().
      - Evaluate doc.set(fieldname, value).
      - Set doc.flags.updater\_reference from mapping(“doctype” → self.doctype, “docname” → self.name, “label” → translated “via Notification”).
      - Set doc.flags.in\_notification\_update from true.
      - Evaluate doc.save(ignore\_permissions = true).
      - Set doc.flags.in\_notification\_update from false.
  - On failure (Exception).
    - Evaluate self.log\_error(“Document update failed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [load standard properties](operations-023.md#op-f9f4d5d6e41ed6), [send notification by channel](operations-022.md#op-c6a97df74edd14).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L111) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L237)

<a id="op-c6a97df74edd14"></a>
### Notification.send notification by channel

`operation_foundation_email_record_definitions_notification_business_behavior_notification_send_notification_by_channel`

**Inputs** self, doc, context.

**Local steps**

- Attempt the following.
  - Set template\_content from self.get\_email\_template\_content(doc).
  - If self.channel equals “Email”.
    - Evaluate self.send\_an\_email(doc, context, template\_content).
  - Otherwise.
    - If self.channel equals “Slack”.
      - Evaluate self.send\_a\_slack\_msg(doc, context).
    - Otherwise.
      - If self.channel equals “SMS”.
        - Evaluate self.send\_sms(doc, context).
      - Otherwise.
        - If self.channel equals “System Notification”.
          - Evaluate self.create\_system\_notification(doc, context, template\_content).
  - If (self.send\_system\_notification and self.channel differs from “System Notification”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.send\_system\_notification → self.channel differs from “System Notification”.
    - Evaluate self.create\_system\_notification(doc, context, template\_content).
- On failure (Exception).
  - Evaluate self.log\_error(“Failed to send Notification”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get email template content](operations-022.md#op-56cd1eb858af86), [send an email](operations-023.md#op-c62c6bc30b600c), [send a slack msg](operations-023.md#op-8e61341cbbc191), [send sms](operations-023.md#op-a11bb0717decba), [create system notification](operations-023.md#op-2d9cea56c99a4c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L113) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L240)

<a id="op-56cd1eb858af86"></a>
### Notification.get email template content

`operation_foundation_binding_foundation_email_doctype_notification_notification_notification_get_email_template_content`

**Inputs** self, doc.

**Record and data access** resolve a document from “Email Template” via get\_cached\_doc.

**Explicit results** no value · mapping(“subject” → subject, “message” → message).

**Explicit failure paths** validation helper — translated “Email Template {0} has no content to send”.format(self.email\_template).

**Local steps**

- If not self.email\_template.
  - Return no value.
- Set email\_template from Platform.get\_cached\_doc(“Email Template”, self.email\_template).
- Set doc\_dict from doc.as\_dict().
- If email\_template.use\_html.
  - Set doc\_dict from email\_template.inject\_email\_account(doc\_dict, self.sender\_email).
- Set subject from Platform.render\_template(email\_template.subject, doc\_dict, restrict\_globals = true).
- Set message from Platform.render\_template(email\_template.response\_, doc\_dict, restrict\_globals = true).
- If not message.
  - Call the validation error handler Platform.throw(translated “Email Template {0} has no content to send”.format(self.email\_template)).
- Return mapping(“subject” → subject, “message” → message).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Email Template”, self.email\_template).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L827)
