# Integration and transport · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Notification

[Record definition](../../../../data/record-types/notification.json)

<a id="op-2d9cea56c99a4c"></a>
### Notification.create system notification

`operation_foundation_email_record_definitions_notification_business_behavior_notification_create_system_notification`

**Inputs** self, doc, context, template\_content = no value.

**Record and data access** read “Module Def” via get\_value.

**Explicit results** no value.

**Local steps**

- Bind local operation \_render for subsequent calls.
- If template\_content is identical to no value.
  - Set template\_content from self.get\_email\_template\_content(doc).
- If template\_content.
  - Set subject from template\_content at “subject”.
  - Set email\_content from template\_content at “message”.
- Otherwise.
  - Set subject from \_render(self.subject).
  - Set email\_content from \_render(self.message).
- Set attachments from self.get\_attachment(doc).
- Set tuple(recipients, cc, bcc) from self.get\_list\_of\_recipients(doc, context).
- Set users from ((recipients + cc) + bcc).
- If not users.
  - Return no value.
- Set notification\_doc from mapping(“type” → (self.notification\_type or “Alert”), “document\_type” → get\_reference\_doctype(doc), “document\_name” → get\_reference\_name(doc), “app” → Platform.db.get\_value(“Module Def”, self.module, “app\_ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.notification\_type → “Alert”.
  - Value choice on self.module — true gives Platform.db.get\_value(“Module Def”, self.module, “app\_name”), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.modified\_by → doc.owner.
  - Value choice on attachments — true gives json.dumps(attachments), false gives no value.
- Evaluate enqueue\_create\_notification(users, notification\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get email template content](operations-022.md#op-56cd1eb858af86), [get attachment](operations-023.md#op-af42e43dc76933), [get list of recipients](operations-023.md#op-9c501173a05eac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L217)

<a id="op-bd0663deb7e457"></a>
### Notification.create system notification.render

`operation_foundation_email_record_definitions_notification_business_behavior_notification_create_system_notification_render`

**Inputs** template.

**Explicit results** template · Platform.render\_template(template, context, restrict\_globals = true).

**Local steps**

- If not (template and “{” belongs to template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in template → “{” belongs to template.
  - Return template.
- Return Platform.render\_template(template, context, restrict\_globals = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L107) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L218)

<a id="op-c62c6bc30b600c"></a>
### Notification.send an email

`operation_foundation_email_record_definitions_notification_business_behavior_notification_send_an_email`

**Inputs** self, doc, context, template\_content = no value.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Bind dependencies formataddr.
- Bind dependencies make\_communication.
- If template\_content is identical to no value.
  - Set template\_content from self.get\_email\_template\_content(doc).
- If template\_content.
  - Set tuple(subject, message) from tuple(template\_content at “subject”, template\_content at “message”).
- Otherwise.
  - Set subject from self.subject.
  - If “{” belongs to subject.
    - Set subject from Platform.render\_template(self.subject, context, restrict\_globals = true).
  - Set message from Platform.render\_template(self.message, context, restrict\_globals = true).
- Set attachments from self.get\_attachment(doc).
- Set tuple(recipients, cc, bcc) from self.get\_list\_of\_recipients(doc, context).
- If not (recipients or cc or bcc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in recipients → cc → bcc.
  - Return no value.
- Set sender from no value.
- If (self.sender and self.sender\_email).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sender → self.sender\_email.
  - Set sender from formataddr(tuple(self.sender, self.sender\_email)).
- Set communication from no value.
- If doc.doctype differs from “Communication”.
  - Set communication from make\_communication(doctype = get\_reference\_doctype(doc), name = get\_reference\_name(doc), content = message, subject = subject, …).get(“name”).
  - Set comm from Platform.get\_lazy\_doc(“Communication”, communication).
  - Evaluate comm.get\_outgoing\_email\_account().
- Set print\_letterhead from any(generator of attachment.get(“print\_letterhead”) for attachment drawn from attachments where attachment.get(“print\_format\_attachment”) equals 1).
  - Draw attachment from attachments, keep a combination only if (attachment.get(“print\_format\_attachment”) equals 1).
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, sender = sender, cc = cc, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get email template content](operations-022.md#op-56cd1eb858af86), [get attachment](operations-023.md#op-af42e43dc76933), [get list of recipients](operations-023.md#op-9c501173a05eac).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, sender = sender, cc = cc, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L112) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L239)

<a id="op-8e61341cbbc191"></a>
### Notification.send a slack msg

`operation_foundation_email_record_definitions_notification_business_behavior_notification_send_a_slack_message`

**Inputs** self, doc, context.

**Local steps**

- Evaluate send\_slack\_message(webhook\_url = self.slack\_webhook\_url, message = Platform.render\_template(self.message, context, restrict\_globals = true), reference\_doctype = get\_reference\_doctype(doc), reference\_name = ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0229.json#L7336) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L238)

<a id="op-a11bb0717decba"></a>
### Notification.send sms

`operation_foundation_email_record_definitions_notification_business_behavior_notification_send_short_message_service`

**Inputs** self, doc, context.

**Local steps**

- Evaluate send\_via\_sms\_gateway(receiver\_list = self.get\_receiver\_list(doc, context, “mobile\_no”, self.get\_mobile\_no), msg = Platform.utils.strip\_html\_tags(Platform.render\_template(self.message, context, restrict\_glo ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get receiver list](operations-023.md#op-d429c0585e75ec).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L241)

<a id="op-648f1b4d68fc6d"></a>
### Notification.get mobile no

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_mobile_number`

**Inputs** doc, field.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “User” via get\_value · read “Customer” via get\_value.

**Explicit results** mobile\_no.

**Explicit failure paths** validation helper — translated “Field {0} on document {1} is neither a Mobile number field nor a Customer or User link”.format(field, doc.name).

**Local steps**

- Set option from doc.meta.get\_field(field).options.strip().
- If (option equals “Phone” or option equals “Mobile”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in option equals “Phone” → option equals “Mobile”.
  - Set mobile\_no from doc.get(field).
  - If not mobile\_no.
    - Evaluate doc.log\_error(translated “Notification: document {0} has no {1} number set (field: {2})”.format(field, doc.name, option, field)).
- Otherwise.
  - If option equals “User”.
    - Set user from doc.get(field).
    - Set mobile\_no from Platform.get\_value(“User”, user, “mobile\_no”).
    - If not mobile\_no.
      - Evaluate doc.log\_error(translated “Notification: user {0} has no Mobile number set”.format(user)).
  - Otherwise.
    - If option equals “Customer”.
      - Set customer from doc.get(field).
      - Set mobile\_no from Platform.get\_value(“Customer”, customer, “mobile\_no”).
      - If not mobile\_no.
        - Evaluate doc.log\_error(translated “Notification: customer {0} has no Mobile number set”.format(customer)).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Field {0} on document {1} is neither a Mobile number field nor a Customer or User link”.format(field, doc.name)).
- Return mobile\_no.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L186) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L224)

<a id="op-9c501173a05eac"></a>
### Notification.get list of recipients

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_list_of_recipients`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, doc, context.

**Explicit result forms** a structured result.

**Local structure** 8 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L844) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L223)

<a id="op-d429c0585e75ec"></a>
### Notification.get receiver list

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_receiver_list`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, doc, context, field\_on\_user, recipient\_extractor\_func.

**Explicit result forms** the result of a delegated call.

**Local structure** 9 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L1646) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L226)

<a id="op-af42e43dc76933"></a>
### Notification.get attachment

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_attachment`

**Inputs** self, doc.

**Declared result** list at dict.

**Record and data access** read “File” via get\_all.

**Explicit results** attachments.

**Local steps**

- Set attachments from list().
- If self.attach\_print.
  - Evaluate attachments.append(self.get\_print(doc)).
- If (self.attach\_files equals “From Field” and self.from\_attach\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attach\_files equals “From Field” → self.from\_attach\_field.
  - Evaluate attachments.append(mapping(“file\_url” → doc.get(self.from\_attach\_field))).
- Otherwise.
  - If self.attach\_files equals “All”.
    - Evaluate attachments.extend(Platform.get\_all(“File”, fields = list(“file\_url”), filters = mapping(“attached\_to\_doctype” → self.document\_type, “attached\_to\_name” → doc.name))).
- Return attachments.

**Methods declared on this owner** [get print](operations-023.md#op-d8c7cfbeb7d97c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L2239) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L220)

<a id="op-d8c7cfbeb7d97c"></a>
### Notification.get print

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_print`

**Inputs** self, doc.

**Record and data access** resolve a document from “Print Settings” via get\_doc · read “Print Format” via get\_value.

**Explicit results** mapping(“print\_format\_attachment” → 1, “doctype” → doc.doctype, “name” → doc.name, “print\_format” → self.print\_format, …).

**Local steps**

- Set print\_settings from Platform.get\_doc(“Print Settings”, “Print Settings”).
- Evaluate validate\_print\_for\_docstatus(doc, print\_settings.as\_dict()).
- Return mapping(“print\_format\_attachment” → 1, “doctype” → doc.doctype, “name” → doc.name, “print\_format” → self.print\_format, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“language”) → Platform.db.get\_value(“Print Format”, self.print\_format, “default\_print\_language”) when self.print\_format, otherwise no value.
  - Value choice on self.print\_format — true gives Platform.db.get\_value(“Print Format”, self.print\_format, “default\_print\_language”), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L108) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L225)

<a id="op-d4d0fef65cc4e0"></a>
### Notification.get template

`operation_foundation_email_record_definitions_notification_business_behavior_notification_get_template`

**Inputs** self, md\_as\_html = false.

**Explicit results** no value · Platform.utils.md\_to\_html(template) · template.

**Local steps**

- Set module from get\_doc\_module(self.module, self.doctype, self.name).
- Set path from os.path.join(os.path.dirname(module.\_\_file\_\_), Platform.scrub(self.name)).
- Set extension from FORMATS.get(self.message\_type, “.md”).
- Set file\_path from (path + extension).
- Set template from empty text.
- If os.path.exists(file\_path).
  - Within open(file\_path) bound as f.
    - Set template from f.read().
- If not template.
  - Return no value.
- If extension equals “.md”.
  - Return Platform.utils.md\_to\_html(template).
- Return template.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L3094) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L227)

<a id="op-f9f4d5d6e41ed6"></a>
### Notification.load standard properties

`operation_foundation_email_record_definitions_notification_business_behavior_notification_load_standard_properties`

**Inputs** self, context.

**Local steps**

- Set module from get\_doc\_module(self.module, self.doctype, self.name).
- If module.
  - If hasattr(module, “get\_context”).
    - Set out from module.get\_context(context).
    - If out.
      - Evaluate context.update(out).
- Set self.message from self.get\_template(md\_as\_html = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get template](operations-023.md#op-d4d0fef65cc4e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L3504) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L228)

<a id="op-1dcac7c56b8e33"></a>
### Notification.on trash

`operation_foundation_email_record_definitions_notification_business_behavior_notification_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You are not allowed to delete a standard Notification. You can disable it instead.”.

**Local steps**

- If self.is\_standard.
  - If (not Platform.conf.developer\_mode and not Platform.flags.in\_migrate and not Platform.flags.in\_patch).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_migrate → not Platform.flags.in\_patch.
    - Call the validation error handler Platform.throw(translated “You are not allowed to delete a standard Notification. You can disable it instead.”).
  - If (Platform.conf.developer\_mode and not Platform.flags.in\_test).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → not Platform.flags.in\_test.
    - Evaluate Platform.db.after\_commit(self.delete\_notification\_folder).
- Evaluate clear\_notification\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L3731) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L229)

<a id="op-4e36c3d53ae643"></a>
### Notification.delete notification folder

`operation_foundation_email_record_definitions_notification_business_behavior_notification_delete_notification_folder`

**Inputs** self.

**Local steps**

- Bind dependencies delete\_folder.
- Evaluate delete\_folder(self.module, “Notification”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L3963) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L219)

<a id="op-c9cefe14e20298"></a>
### Clear notification cache

`operation_foundation_email_record_definitions_notification_business_behavior_clear_notification_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.client\_cache.delete\_keys(“notifications::”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L4046) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L203)

<a id="op-98ba7ecb9272c6"></a>
### Get documents for today

`operation_foundation_email_record_definitions_notification_business_behavior_get_documents_for_today`

**Inputs** notification.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Notification” via get\_doc.

**Explicit results** list of d.name for d drawn from notification.get\_documents\_for\_today().

**Local steps**

- Set notification from Platform.get\_doc(“Notification”, notification).
- Evaluate notification.check\_permission(“read”).
- Return list of d.name for d drawn from notification.get\_documents\_for\_today().
  - Draw d from notification.get\_documents\_for\_today().

**Values supplied outside this operation** effective access from notification.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L4096) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L208)

<a id="op-b6aa35538125e2"></a>
### Trigger offset alerts

`operation_foundation_email_record_definitions_notification_business_behavior_trigger_offset_alerts`

**Inputs** no declared parameters.

**Local steps**

- Evaluate trigger\_notifications(no value, “offset”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L4259) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L250)

<a id="op-99bd5e40b7c920"></a>
### Trigger daily alerts

`operation_foundation_email_record_definitions_notification_business_behavior_trigger_daily_alerts`

**Inputs** no declared parameters.

**Local steps**

- Evaluate trigger\_notifications(no value, “daily”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L4306) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L248)

<a id="op-3d0f9632f76a12"></a>
### Trigger notifications

`operation_foundation_email_record_definitions_notification_business_behavior_trigger_notifications`

**Inputs** doc, method = no value.

**Record and data access** read “Notification” via get\_all · resolve a document from “Notification” via get\_doc.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_patch.
  - Return no value.
- If method equals “daily”.
  - Set doc\_list from Platform.get\_all(“Notification”, filters = mapping(“event” → tuple(“in”, tuple(“Days Before”, “Days After”)), “enabled” → 1)).
  - For each d in doc\_list.
    - Set alert from Platform.get\_doc(“Notification”, d.name).
    - For each doc in alert.get\_documents\_for\_today().
      - Evaluate evaluate\_alert(doc, alert, alert.event).
      - Evaluate Platform.db.commit().
- Otherwise.
  - If method equals “offset”.
    - Set doc\_list from Platform.get\_all(“Notification”, filters = mapping(“event” → tuple(“in”, tuple(“Minutes Before”, “Minutes After”)), “enabled” → 1)).
    - For each d in doc\_list.
      - Set alert from Platform.get\_doc(“Notification”, d.name).
      - For each doc in alert.get\_documents\_for\_this\_moment().
        - Evaluate evaluate\_alert(doc, alert, alert.event).
        - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L115) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L249)

<a id="op-2881c9e14b64c2"></a>
### Evaluate alert

`operation_foundation_email_record_definitions_notification_business_behavior_evaluate_alert`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc, alert, event.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging, record lookup, record mutation request, validation or user-notification service.

**Local structure** 10 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L105) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L205)

<a id="op-8fda45ee60c3ef"></a>
### Get comments for context

`operation_foundation_binding_foundation_email_doctype_notification_notification_get_comments_for_context`

**Inputs** doc.

**Record and data access** read “Comment” via get\_all · read “Communication” via get\_all.

**Explicit results** no value · (list of mapping(“comment” → truncate(c.content), “by” → (c.by or c.owner), “name” → c.name) for c drawn from comments at slice negative 100 to no value or no value).

**Local steps**

- If not doc.get(“name”).
  - Return no value.
- Set reference from mapping(“reference\_doctype” → doc.doctype, “reference\_name” → doc.name).
- Set comments from (Platform.get\_all(“Comment”, fields = list(“name”, “content”, “comment\_email as by”, “owner”, …), filters = (reference bitwise or mapping(“comment\_type” → “Comment”)), order\_by = “creation desc”, limit = 1 ….
- Evaluate comments.sort(key = deferred anonymous expression).
- Return (list of mapping(“comment” → truncate(c.content), “by” → (c.by or c.owner), “name” → c.name) for c drawn from comments at slice negative 100 to no value or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of mapping(“comment” → truncate(c.content), “by” → (c.by or c.owner), “name” → c.name) for c drawn from comments at slice negative 100 to no value → no value.
  - Draw c from comments at slice negative 100 to no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.by → c.owner.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L826)

<a id="op-05943f0422dde3"></a>
### Truncate

`operation_foundation_binding_foundation_email_doctype_notification_notification_truncate`

**Inputs** content.

**Explicit results** (content at slice no value to 97 + “...”) when len(content) &gt; 100, otherwise content.

**Local steps**

- Set content from (content or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → empty text.
- Return (content at slice no value to 97 + “...”) when len(content) &gt; 100, otherwise content.
  - Value choice on len(content) &gt; 100 — true gives (content at slice no value to 97 + “...”), false gives content.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L103) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L828)

<a id="op-2de48f9c0e289c"></a>
### Get context

`operation_foundation_email_record_definitions_notification_business_behavior_get_context`

**Inputs** doc.

**Explicit results** mapping(“doc” → doc, “nowdate” → nowdate, “Platform” → Platform.Platform).

**Local steps**

- Set Platform from namedtuple(“Platform”, list(“Platform”)).
- Set Platform from Platform(Platform = get\_safe\_globals().get(“Platform”)).
- Return mapping(“doc” → doc, “nowdate” → nowdate, “Platform” → Platform.Platform).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6221) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L207)

<a id="op-28be955d2ae0aa"></a>
### Get assignees

`operation_foundation_email_record_definitions_notification_business_behavior_get_assignees`

**Inputs** doc.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** list of d.allocated\_to for d drawn from assignees.

**Local steps**

- Set assignees from list().
- Set assignees from Platform.get\_all(“ToDo”, filters = mapping(“status” → “Open”, “reference\_name” → doc.name, “reference\_type” → doc.doctype), fields = list(“allocated\_to”)).
- Return list of d.allocated\_to for d drawn from assignees.
  - Draw d from assignees.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6384) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L206)
