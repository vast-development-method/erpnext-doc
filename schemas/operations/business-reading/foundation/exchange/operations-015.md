# Integration and transport · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email queue

[Record definition](../../../../data/record-types/email_queue.json)

<a id="op-318154cd1ae2f5"></a>
### Email Queue.new

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_new`

**Inputs** cls, doc\_data, ignore\_permissions = false.

**Wrappers, in declaration order** classmethod.

**Declared result** EmailQueue.

**State and service calls** request new\_doc for cls.DOCTYPE · call insert on doc.

**Explicit results** no value · doc.

**Local steps**

- Set data from doc\_data.copy().
- If not data.get(“recipients”).
  - Return no value.
- If isinstance(data at “unsubscribe\_params”, dict).
  - Set data at “unsubscribe\_params” from json.dumps(data at “unsubscribe\_params”).
- Set recipients from data.pop(“recipients”).
- Set doc from Platform.new\_doc(cls.DOCTYPE).
- Evaluate doc.update(data).
- Evaluate doc.set\_recipients(recipients).
- Evaluate doc.insert(ignore\_permissions = ignore\_permissions).
- Return doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L623) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L129)

<a id="op-72f1e6b0383222"></a>
### Email Queue.find

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_find`

**Inputs** cls, name.

**Wrappers, in declaration order** classmethod.

**Declared result** EmailQueue.

**Record and data access** resolve a document from cls.DOCTYPE via get\_doc.

**Explicit results** Platform.get\_doc(cls.DOCTYPE, name).

**Local steps**

- Return Platform.get\_doc(cls.DOCTYPE, name).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L983) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L124)

<a id="op-f71ec570800ff8"></a>
### Email Queue.find one by filters

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_find_one_by_filters`

**Inputs** cls, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Record and data access** read cls.DOCTYPE via get\_value.

**Explicit results** cls.find(name) when name, otherwise no value.

**Local steps**

- Set name from Platform.db.get\_value(cls.DOCTYPE, kwargs).
- Return cls.find(name) when name, otherwise no value.
  - Value choice on name — true gives cls.find(name), false gives no value.

**Methods declared on this owner** [find](operations-015.md#op-72f1e6b0383222).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1059) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L125)

<a id="op-a168f690f00b30"></a>
### Email Queue.update db

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_update_database`

**Inputs** self, commit = false, remaining named values kwargs.

**State and service calls** request set\_value on self.DOCTYPE · commit.

**Local steps**

- Evaluate Platform.db.set\_value(self.DOCTYPE, self.name, kwargs).
- If commit.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1177) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L139)

<a id="op-af5440b542d7fe"></a>
### Email Queue.update status

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_update_status`

**Inputs** self, status, commit = false, remaining named values kwargs.

**Record and data access** read “Communication” via exists · resolve a document from “Communication” via get\_doc.

**Local steps**

- Evaluate self.update\_db(status = status, commit = commit, expanded names kwargs).
- If (self.communication and Platform.db.exists(“Communication”, self.communication)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.communication → Platform.db.exists(“Communication”, self.communication).
  - Set communication\_doc from Platform.get\_doc(“Communication”, self.communication).
  - Evaluate communication\_doc.set\_delivery\_status(commit = commit).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update db](operations-015.md#op-a168f690f00b30).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1301) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L140)

<a id="op-35c3d28ee1c5b2"></a>
### Email Queue.redact message

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_redact_message`

**Inputs** self.

**Local steps**

- Set message from Parser(policy = SMTP).parsestr(self.message).
- Evaluate message.clear\_content().
- Evaluate message.set\_content(REDACTED\_MESSAGE).
- Evaluate self.update\_db(message = message.as\_string(), commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update db](operations-015.md#op-a168f690f00b30).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1531) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L133)

<a id="op-825dc133246d11"></a>
### Email Queue.cc

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_carbon_copy`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** ((self.show\_as\_cc and self.show\_as\_cc.split(“,”)) or list()).

**Local steps**

- Return ((self.show\_as\_cc and self.show\_as\_cc.split(“,”)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.show\_as\_cc and self.show\_as\_cc.split(“,”)) → list().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.show\_as\_cc → self.show\_as\_cc.split(“,”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1705) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L122)

<a id="op-4025895fdfd5b6"></a>
### Email Queue.to

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_to`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** list of r.recipient for r drawn from self.recipients where r.recipient does not belong to self.cc.

**Local steps**

- Return list of r.recipient for r drawn from self.recipients where r.recipient does not belong to self.cc.
  - Draw r from self.recipients, keep a combination only if (r.recipient does not belong to self.cc).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1796) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L138)

<a id="op-4c6ba844b2b3b4"></a>
### Email Queue.attachments list

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_attachments_list`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** json.loads(self.attachments) when self.attachments, otherwise list().

**Local steps**

- Return json.loads(self.attachments) when self.attachments, otherwise list().
  - Value choice on self.attachments — true gives json.loads(self.attachments), false gives list().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1891) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L120)

<a id="op-21ef78e180bd22"></a>
### Email Queue.get email account

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_get_email_account`

**Inputs** self, raise\_error = false.

**Record and data access** resolve a document from “Email Account” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Email Account”, self.email\_account) · EmailAccount.find\_outgoing(match\_by\_email = self.sender, match\_by\_doctype = self.reference\_doctype, \_raise\_error = raise\_error).

**Local steps**

- If self.email\_account.
  - Return Platform.get\_cached\_doc(“Email Account”, self.email\_account).
- Return EmailAccount.find\_outgoing(match\_by\_email = self.sender, match\_by\_doctype = self.reference\_doctype, \_raise\_error = raise\_error).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Email Account”, self.email\_account).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L1969) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L127)

<a id="op-8c6f03b35191b7"></a>
### Email Queue.is to be sent

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_is_to_be_sent`

**Inputs** self.

**Explicit results** self.status belongs to list(“Not Sent”, “Partially Sent”).

**Local steps**

- Return self.status belongs to list(“Not Sent”, “Partially Sent”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L2115) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L128)

<a id="op-af5db2006de454"></a>
### Email Queue.can send now

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_can_send_now`

**Inputs** self.

**Explicit results** false · true.

**Local steps**

- If (Platform.are\_emails\_muted() or not self.is\_to\_be\_sent() or cint(Platform.db.get\_default(“suspend\_email\_queue”)) equals 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.are\_emails\_muted() → not self.is\_to\_be\_sent() → cint(Platform.db.get\_default(“suspend\_email\_queue”)) equals 1.
  - Return false.
- Return true.

**Methods declared on this owner** [is to be sent](operations-015.md#op-8c6f03b35191b7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L2177) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L121)

<a id="op-973b06fe7c2ee5"></a>
### Email Queue.send

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_send`

**Inputs** self, smtp\_server\_instance = no value, Platform\_mail\_client = no value, force\_send = false.

**Explicit results** no value.

**Local steps**

- If (not self.can\_send\_now() and not force\_send).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.can\_send\_now() → not force\_send.
  - Return no value.
- Within SendMailContext(self, smtp\_server\_instance, Platform\_mail\_client) bound as ctx.
  - Evaluate ctx.fetch\_outgoing\_server().
  - Bind local operation validate\_and\_prepare\_message for subsequent calls.
  - Bind local operation get\_smtp\_options for subsequent calls.
  - Set last\_message from no value.
  - For each recipient in self.recipients.
    - If recipient.is\_mail\_sent().
      - Continue with the next iteration or loop test.
    - Set message from ctx.build\_message(recipient.recipient).
    - Set last\_message from message.
    - If method bound to get\_hook\_method(“override\_email\_send”).
      - Evaluate method(self, self.sender, recipient.recipient, message).
    - Otherwise.
      - If (not Platform.in\_test or Platform.flags.testing\_email).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.in\_test → Platform.flags.testing\_email.
        - If ctx.email\_account\_doc.service equals “Platform Mail”.
          - Evaluate ctx.Platform\_mail\_client.send\_raw(sender = self.sender, recipients = recipient.recipient, message = message, is\_newsletter = self.reference\_doctype equals “Newsletter”).
        - Otherwise.
          - Set msg\_bytes from validate\_and\_prepare\_message(message).
          - Set tuple(mail\_options, rcpt\_options) from get\_smtp\_options().
          - Evaluate ctx.smtp\_server.session.sendmail(from\_addr = self.sender, to\_addrs = recipient.recipient, msg = msg\_bytes, mail\_options = mail\_options, …).
    - Evaluate ctx.update\_recipient\_status\_to\_sent(recipient).
  - If (Platform.in\_test and not Platform.flags.testing\_email).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.in\_test → not Platform.flags.testing\_email.
    - Set Platform.flags.sent\_mail from last\_message.
    - Return no value.
  - If (last\_message and ctx.email\_account\_doc.append\_emails\_to\_sent\_folder).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_message → ctx.email\_account\_doc.append\_emails\_to\_sent\_folder.
    - Evaluate ctx.email\_account\_doc.append\_email\_to\_sent\_folder(last\_message).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can send now](operations-015.md#op-af5db2006de454).

**Values supplied outside this operation** selected callable from get\_hook\_method(“override\_email\_send”) · service or queued work from ctx.smtp\_server.session.sendmail(from\_addr = self.sender, to\_addrs = recipient.recipient, msg = msg\_bytes, mail\_options = mail\_options, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L98) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L134)

<a id="op-a9f3ce0e156217"></a>
### Email Queue.send.validate and prepare message

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_send_validate_and_prepare_message`

**Inputs** raw\_message.

**Declared result** bytes.

**Explicit results** msg.

**Explicit failure paths** validation helper — translated “Email size {0:.2f} MB exceeds the maximum allowed size of {1:.2f} MB”.format(msg\_size\_mb, max\_size\_mb).

**Local steps**

- Set msg from raw\_message when isinstance(raw\_message, bytes), otherwise raw\_message.encode(“utf-8”).
  - Value choice on isinstance(raw\_message, bytes) — true gives raw\_message, false gives raw\_message.encode(“utf-8”).
- If ctx.smtp\_server.session.has\_extn(“SIZE”).
  - If max\_size bound to ctx.smtp\_server.session.esmtp\_features.get(“size”).
    - Set max\_size from int(max\_size).
    - If max\_size &gt; 0.
      - Set msg\_size from len(msg).
      - If msg\_size &gt; max\_size.
        - Set msg\_size\_mb from (msg\_size ÷ (1024 × 1024)).
        - Set max\_size\_mb from (max\_size ÷ (1024 × 1024)).
        - Call the validation error handler Platform.throw(translated “Email size {0:.2f} MB exceeds the maximum allowed size of {1:.2f} MB”.format(msg\_size\_mb, max\_size\_mb)).
- Return msg.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L5816) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L136)

<a id="op-4e3a004e6f8983"></a>
### Email Queue.send.get smtp options

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_send_get_simple_mail_transfer_protocol_options`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(list at str, list at str).

**Explicit results** tuple(mail\_options, rcpt\_options).

**Local steps**

- Set mail\_options from list().
- Set rcpt\_options from list().
- If not ctx.smtp\_server.session.has\_extn(“DSN”).
  - Return tuple(mail\_options, rcpt\_options).
- If dsn\_notify\_type bound to ctx.email\_account\_doc.dsn\_notify\_type.
  - Evaluate mail\_options.extend(list(“RET=FULL”, formatted text ENVID={self.name})).
  - Evaluate rcpt\_options.append(formatted text NOTIFY={dsn\_notify\_type}).
- Return tuple(mail\_options, rcpt\_options).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L6217) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L135)

<a id="op-a12a659552fe9b"></a>
### Email Queue.clear old logs

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Set days from (days or 31).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in days → 31.
- Set email\_queue from Platform.qb.DocType(“Email Queue”).
- Set email\_recipient from Platform.qb.DocType(“Email Queue Recipient”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(email\_queue.creation &lt; (Now() − Interval(days = days))).run().
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(email\_recipient.creation &lt; (Now() − Interval(days = days))).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L3774) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L123)

<a id="op-f56a6067eabb4e"></a>
### Send Mail Context.initialize

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_initialize`

**Inputs** self, queue\_doc, smtp\_server\_instance = no value, Platform\_mail\_client = no value.

**Local steps**

- Set self.queue\_doc from queue\_doc.
- Set self.smtp\_server from smtp\_server\_instance.
- Set self.Platform\_mail\_client from Platform\_mail\_client.
- Set self.sent\_to\_atleast\_one\_recipient from any(generator of rec.recipient for rec drawn from self.queue\_doc.recipients where rec.is\_mail\_sent()).
  - Draw rec from self.queue\_doc.recipients, keep a combination only if (rec.is\_mail\_sent()).
- Set self.email\_account\_doc from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L4136) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L176)

<a id="op-10e61c2e9a3a81"></a>
### Send Mail Context.fetch outgoing server

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_fetch_outgoing_server`

**Inputs** self.

**Local steps**

- Set self.email\_account\_doc from self.queue\_doc.get\_email\_account(raise\_error = true).
- If self.email\_account\_doc.service equals “Platform Mail”.
  - If not self.Platform\_mail\_client.
    - Set self.Platform\_mail\_client from self.email\_account\_doc.get\_Platform\_mail\_client().
- Otherwise.
  - If not self.smtp\_server.
    - Set self.smtp\_server from self.email\_account\_doc.get\_smtp\_server().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L4353) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L169)

<a id="op-be70164a308387"></a>
### Send Mail Context.enter context

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_enter`

**Inputs** self.

**Explicit results** self.

**Local steps**

- Evaluate self.queue\_doc.update\_status(status = “Sending”, commit = true).
- Return self.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L4561) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L167)

<a id="op-2601bee3256aba"></a>
### Send Mail Context.exit context

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_exit`

**Inputs** self, exc\_type, exc\_val, exc\_tb.

**Local steps**

- If exc\_type.
  - Set update\_fields from mapping(“error” → Platform.get\_traceback()).
  - If self.queue\_doc.retry &lt; get\_email\_retry\_limit().
    - Evaluate update\_fields.update(mapping(“status” → “Partially Sent” when self.sent\_to\_atleast\_one\_recipient, otherwise “Not Sent”, “retry” → (self.queue\_doc.retry + 1))).
      - Value choice on self.sent\_to\_atleast\_one\_recipient — true gives “Partially Sent”, false gives “Not Sent”.
  - Otherwise.
    - Evaluate update\_fields.update(mapping(“status” → “Error”)).
    - Evaluate self.notify\_failed\_email().
- Otherwise.
  - Set update\_fields from mapping(“status” → “Sent”).
- Evaluate self.queue\_doc.update\_status(expanded names update\_fields, commit = true).
- If (not exc\_type and self.queue\_doc.redact\_message\_after\_send).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not exc\_type → self.queue\_doc.redact\_message\_after\_send.
  - Attempt the following.
    - Evaluate self.queue\_doc.redact\_message().
  - On failure (Exception).
    - Evaluate Platform.log\_error(title = “Failed to redact email message after send”, reference\_doctype = self.queue\_doc.doctype, reference\_name = self.queue\_doc.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify failed email](operations-015.md#op-b6dc96396cd730).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L4640) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L168)

<a id="op-b6dc96396cd730"></a>
### Send Mail Context.notify failed email

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_notify_failed_email`

**Inputs** self.

**Wrappers, in declaration order** savepoint(catch = Exception).

**State and service calls** request new\_doc for “Notification Log” · call insert on notification.

**Local steps**

- Set subject from Parser(policy = SMTP).parsestr(self.queue\_doc.message) at “Subject”.
- Set notification from Platform.new\_doc(“Notification Log”).
- Set notification.for\_user from self.queue\_doc.owner.
- Evaluate notification.set(“type”, “Alert”).
- Set notification.from\_user from self.queue\_doc.owner.
- Set notification.document\_type from self.queue\_doc.doctype.
- Set notification.document\_name from self.queue\_doc.name.
- Set notification.subject from (translated “Failed to send email with subject:” + formatted text  {subject}).
- Evaluate notification.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L5139) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L178)

<a id="op-9a782359387a7e"></a>
### Send Mail Context.update recipient status to sent

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_update_recipient_status_to_sent`

**Inputs** self, recipient.

**Local steps**

- Set self.sent\_to\_atleast\_one\_recipient from true.
- Evaluate recipient.update\_db(status = “Sent”, commit = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L5498) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L180)

<a id="op-073115ab53e266"></a>
### Send Mail Context.get message object

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_get_message_object`

**Inputs** self, message.

**Explicit results** Parser(policy = policy).parsestr(message).

**Local steps**

- Set policy from SMTP.clone(refold\_source = “none”).
- Return Parser(policy = policy).parsestr(message).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L5590) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L170)

<a id="op-a19143892c1fa3"></a>
### Send Mail Context.message placeholder

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_message_placeholder`

**Inputs** self, placeholder\_key.

**Explicit results** map.get(placeholder\_key).

**Local steps**

- Set map from mapping(“tracker” → “&lt;!--email\_open\_check--&gt;”, “unsubscribe\_url” → “&lt;!--unsubscribe\_url--&gt;”, “cc” → “&lt;!--cc\_message--&gt;”, “recipient” → “&lt;!--recipient--&gt;”).
- Return map.get(placeholder\_key).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L5702) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L177)
