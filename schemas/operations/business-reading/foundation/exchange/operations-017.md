# Integration and transport · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email queue

[Record definition](../../../../data/record-types/email_queue.json)

<a id="op-a03021bbc12e2d"></a>
### Queue Builder.unsubscribe message

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_unsubscribe_message`

**Inputs** self.

**Explicit results** get\_unsubscribe\_message(self.\_unsubscribe\_message, self.expose\_recipients).

**Local steps**

- If self.should\_include\_unsubscribe\_link().
  - Return get\_unsubscribe\_message(self.\_unsubscribe\_message, self.expose\_recipients).

If control reaches the end, it returns no value.

**Methods declared on this owner** [should include unsubscribe link](operations-016.md#op-a15da2a3d73504).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L4489) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L163)

<a id="op-801dc71dda84b3"></a>
### Queue Builder.get outgoing email account

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_get_outgoing_email_account`

**Inputs** self.

**Explicit results** self.\_email\_account.

**Local steps**

- If self.\_email\_account.
  - Return self.\_email\_account.
- Set self.\_email\_account from EmailAccount.find\_outgoing(match\_by\_doctype = self.reference\_doctype, match\_by\_email = self.\_sender, \_raise\_error = true).
- Return self.\_email\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L4576) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L153)

<a id="op-027dc1787b7531"></a>
### Queue Builder.get unsubscribed user emails

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_get_unsubscribed_user_emails`

**Inputs** self.

**Explicit results** self.\_unsubscribed\_user\_emails.

**Local steps**

- If self.\_unsubscribed\_user\_emails is distinct from no value.
  - Return self.\_unsubscribed\_user\_emails.
- Set all\_ids from list(set(((self.recipients + self.cc) + self.bcc))).
- Set EmailUnsubscribe from DocType(“Email Unsubscribe”).
- If len(all\_ids) &gt; 0.
  - Set unsubscribed from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and (nested operand in the contract bitwise or nested operand in ….
- Otherwise.
  - Set unsubscribed from no value.
- Set self.\_unsubscribed\_user\_emails from (unsubscribed or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in unsubscribed → list().
- Return self.\_unsubscribed\_user\_emails.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L4707) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L154)

<a id="op-b487b3b4faefdb"></a>
### Queue Builder.final recipients

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_final_recipients`

**Inputs** self.

**Explicit results** list of mail\_id for mail\_id drawn from self.recipients where mail\_id does not belong to unsubscribed\_emails.

**Local steps**

- Set unsubscribed\_emails from self.get\_unsubscribed\_user\_emails().
- Return list of mail\_id for mail\_id drawn from self.recipients where mail\_id does not belong to unsubscribed\_emails.
  - Draw mail\_id from self.recipients, keep a combination only if (mail\_id does not belong to unsubscribed\_emails).

**Methods declared on this owner** [get unsubscribed user emails](operations-017.md#op-027dc1787b7531).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L5162) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L150)

<a id="op-1f99047ec3b34f"></a>
### Queue Builder.final cc

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_final_carbon_copy`

**Inputs** self.

**Explicit results** list of mail\_id for mail\_id drawn from self.cc where mail\_id does not belong to unsubscribed\_emails.

**Local steps**

- Set unsubscribed\_emails from self.get\_unsubscribed\_user\_emails().
- Return list of mail\_id for mail\_id drawn from self.cc where mail\_id does not belong to unsubscribed\_emails.
  - Draw mail\_id from self.cc, keep a combination only if (mail\_id does not belong to unsubscribed\_emails).

**Methods declared on this owner** [get unsubscribed user emails](operations-017.md#op-027dc1787b7531).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L5265) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L149)

<a id="op-c62e2eaaf5ea21"></a>
### Queue Builder.final bcc

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_final_blind_carbon_copy`

**Inputs** self.

**Explicit results** list of mail\_id for mail\_id drawn from self.bcc where mail\_id does not belong to unsubscribed\_emails.

**Local steps**

- Set unsubscribed\_emails from self.get\_unsubscribed\_user\_emails().
- Return list of mail\_id for mail\_id drawn from self.bcc where mail\_id does not belong to unsubscribed\_emails.
  - Draw mail\_id from self.bcc, keep a combination only if (mail\_id does not belong to unsubscribed\_emails).

**Methods declared on this owner** [get unsubscribed user emails](operations-017.md#op-027dc1787b7531).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L5370) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L148)

<a id="op-12738204836bcf"></a>
### Queue Builder.get attachments

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_get_attachments`

**Inputs** self.

**Explicit results** attachments.

**Local steps**

- Set attachments from list().
- If self.\_attachments.
  - For each att in self.\_attachments.
    - If (att.get(“fid”) or att.get(“file\_url”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in att.get(“fid”) → att.get(“file\_url”).
      - Evaluate attachments.append(att).
    - Otherwise.
      - If att.get(“print\_format\_attachment”) equals 1.
        - If not att.get(“lang”, no value).
          - Set job from getattr(Platform.local, “job”, no value).
          - If (job is distinct from no value and not job.lang\_resolved).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in job is distinct from no value → not job.lang\_resolved.
            - Evaluate Platform.set\_user\_lang(job.user).
            - Set job.lang\_resolved from true.
          - Set att at “lang” from Platform.local.lang.
        - Set att at “print\_letterhead” from self.print\_letterhead.
        - Evaluate attachments.append(att).
- Return attachments.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “job”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L99) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L151)

<a id="op-9171df3de192ae"></a>
### Queue Builder.prepare email content

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_prepare_email_content`

**Inputs** self.

**Record and data access** read “Communication” via get\_value.

**Explicit results** mail.

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- If email\_account.always\_bcc.
  - Set self.\_bcc from list(expanded self.bcc, email\_account.always\_bcc).
- Set mail from get\_email(recipients = self.final\_recipients(), sender = self.sender, subject = self.subject, formatted = self.email\_html\_content(), …).
- Evaluate mail.set\_message\_id(self.message\_id, self.is\_notification).
- If self.email\_headers.
  - Evaluate mail.add\_headers(self.email\_headers).
- If self.read\_receipt.
  - Set mail.msg\_root at “Disposition-Notification-To” from self.sender.
- If self.in\_reply\_to.
  - If message\_id bound to Platform.db.get\_value(“Communication”, self.in\_reply\_to, “message\_id”).
    - Set message\_id from message\_id.strip(“&lt;&gt; \\t\\n”).
    - Evaluate mail.set\_in\_reply\_to(formatted text &lt;{message\_id}&gt;).
- Return mail.

**Methods declared on this owner** [get outgoing email account](operations-017.md#op-801dc71dda84b3), [final recipients](operations-017.md#op-b487b3b4faefdb), [email html content](operations-016.md#op-3aeae7e7a841f3), [email text content](operations-016.md#op-53e5cbc5da0efa), [final cc](operations-017.md#op-1f99047ec3b34f), [final bcc](operations-017.md#op-c62e2eaaf5ea21).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L5782) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L156)

<a id="op-cfd42b5f54aade"></a>
### Queue Builder.process

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_process`

**Inputs** self, send\_now = false.

**Declared result** (EmailQueue bitwise or no value).

**State and service calls** enqueue with self.send\_emails.

**Explicit results** list() · q.

**Local steps**

- Set final\_recipients from self.final\_recipients().
- Set queue\_separately from ((final\_recipients and self.queue\_separately) or len(final\_recipients) &gt; 100).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (final\_recipients and self.queue\_separately) → len(final\_recipients) &gt; 100.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in final\_recipients → self.queue\_separately.
- If not ((final\_recipients + self.final\_cc()) + self.final\_bcc()).
  - Return list().
- Set queue\_data from self.as\_dict(include\_recipients = false).
- If not queue\_data.
  - Return list().
- If not queue\_separately.
  - Set recipients from list(set(((final\_recipients + self.final\_cc()) + self.final\_bcc()))).
  - Set q from EmailQueue.new(mapping(expand queue\_data, expand mapping(“recipients” → recipients)), ignore\_permissions = true).
  - Evaluate (send\_now and q.send()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in send\_now → q.send().
  - Return q.
- Otherwise.
  - If (send\_now and len(final\_recipients) ≥ 1000).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in send\_now → len(final\_recipients) ≥ 1000.
    - Set send\_now from false.
  - For each recipients in Platform.utils.create\_batch(final\_recipients, 1000).
    - Evaluate Platform.enqueue(self.send\_emails, queue\_data = queue\_data, final\_recipients = recipients, job\_name = Platform.utils.get\_job\_name(“send\_bulk\_emails\_for”, self.reference\_doctype, self.reference\_name), now = ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → send\_now.

If control reaches the end, it returns no value.

**Methods declared on this owner** [final recipients](operations-017.md#op-b487b3b4faefdb), [final cc](operations-017.md#op-1f99047ec3b34f), [final bcc](operations-017.md#op-c62e2eaaf5ea21), [as dict](operations-017.md#op-a3616030988446).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.send\_emails, queue\_data = queue\_data, final\_recipients = recipients, job\_name = Platform.utils.get\_job\_name(“send\_bulk\_emails\_for”, self.reference\_doctype, self.reference\_name), now = ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L6427) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L157)

<a id="op-c5e435efb28327"></a>
### Queue Builder.send emails

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_send_emails`

**Inputs** self, queue\_data, final\_recipients.

**Record and data access** resolve a document from “Email Queue” via get\_doc.

**State and service calls** commit.

**Local steps**

- Set queue\_names from list of EmailQueue.new(mapping(expand queue\_data, expand mapping(“recipients” → list(nested operand in the contract(nested operand in the contract)))), ignore\_permissions = true).name for r drawn from fina ….
  - Draw r from final\_recipients.
- Evaluate Platform.db.commit().
- Set Platform\_mail\_client from no value.
- Set smtp\_server\_instance from no value.
- For each name in queue\_names.
  - Set q from Platform.get\_doc(“Email Queue”, name, for\_update = true).
  - If (not Platform\_mail\_client and not smtp\_server\_instance).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform\_mail\_client → not smtp\_server\_instance.
    - Set email\_account from q.get\_email\_account(raise\_error = true).
    - If email\_account.service equals “Platform Mail”.
      - Set Platform\_mail\_client from email\_account.get\_Platform\_mail\_client().
    - Otherwise.
      - Set smtp\_server\_instance from email\_account.get\_smtp\_server().
  - Within suppress(Exception).
    - Evaluate q.send(smtp\_server\_instance = smtp\_server\_instance, Platform\_mail\_client = Platform\_mail\_client).
- If smtp\_server\_instance.
  - Evaluate smtp\_server\_instance.quit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [final cc](operations-017.md#op-1f99047ec3b34f), [final bcc](operations-017.md#op-c62e2eaaf5ea21).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L100) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L160)

<a id="op-a3616030988446"></a>
### Queue Builder.as dict

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_as_mapping`

**Inputs** self, include\_recipients = true.

**Explicit results** no value · d.

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- Set email\_account\_name from (email\_account and email\_account.is\_exists\_in\_db() and email\_account.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.is\_exists\_in\_db() → email\_account.name.
- Set mail from self.prepare\_email\_content().
- Attempt the following.
  - Set mail\_to\_string from cstr(mail.as\_string()).
- On failure (Platform.InvalidEmailAddressError).
  - Evaluate Platform.log\_error(title = “Invalid email address”, message = “Invalid email address Sender: {}, Recipients: {}, \\nTraceback: {} ”.format(self.sender, “, ”.join(self.final\_recipients()), traceback.format\_e ….
  - Return no value.
- Set d from mapping(“priority” → self.send\_priority, “attachments” → json.dumps(self.get\_attachments()), “message\_id” → get\_string\_between(“&lt;”, mail.msg\_root at “Message-Id”, “&gt;”), “message” → mail\_to\_string, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_account\_name → no value.
- If include\_recipients.
  - Set d at “recipients” from self.final\_recipients().
- Return d.

**Methods declared on this owner** [get outgoing email account](operations-017.md#op-801dc71dda84b3), [prepare email content](operations-017.md#op-9171df3de192ae), [final recipients](operations-017.md#op-b487b3b4faefdb), [get attachments](operations-017.md#op-12738204836bcf), [final cc](operations-017.md#op-1f99047ec3b34f), [final bcc](operations-017.md#op-c62e2eaaf5ea21).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L143)

## Record · Email queue recipient

[Record definition](../../../../data/record-types/email_queue_recipient.json)

<a id="op-97f1a287b87a95"></a>
### Email Queue Recipient.is mail to be sent

`operation_foundation_email_record_definitions_email_queue_recipient_business_behavior_email_queue_recipient_is_mail_to_be_sent`

**Inputs** self.

**Explicit results** self.status equals “Not Sent”.

**Local steps**

- Return self.status equals “Not Sent”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4023) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L185)

<a id="op-c4d5a208067109"></a>
### Email Queue Recipient.is mail sent

`operation_foundation_email_record_definitions_email_queue_recipient_business_behavior_email_queue_recipient_is_mail_sent`

**Inputs** self.

**Explicit results** self.status equals “Sent”.

**Local steps**

- Return self.status equals “Sent”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4076) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L184)

<a id="op-d9ea1b9c6bb78e"></a>
### Email Queue Recipient.update db

`operation_foundation_email_record_definitions_email_queue_recipient_business_behavior_email_queue_recipient_update_database`

**Inputs** self, commit = false, remaining named values kwargs.

**State and service calls** request set\_value on self.DOCTYPE · commit.

**Local steps**

- Evaluate Platform.db.set\_value(self.DOCTYPE, self.name, kwargs).
- If commit.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4129) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L186)

<a id="op-4e81af94b6e310"></a>
### On doctype update

`operation_foundation_email_record_definitions_email_queue_recipient_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Email Queue Recipient”.

**Local steps**

- Evaluate Platform.db.add\_index(“Email Queue Recipient”, list(“modified”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4253) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L187)

## Record · Email template

[Record definition](../../../../data/record-types/email_template.json)

<a id="op-46b3afaa3cc67e"></a>
### Email Template.response

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_response`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.response\_html when self.use\_html, otherwise self.response.

**Local steps**

- Return self.response\_html when self.use\_html, otherwise self.response.
  - Value choice on self.use\_html — true gives self.response\_html, false gives self.response.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4322) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L197)

<a id="op-786d7dfdc67581"></a>
### Email Template.validate

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_template(self.subject).
- Evaluate validate\_template(self.response\_).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4391) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L198)

<a id="op-fa810f362fca26"></a>
### Email Template.get formatted subject

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_get_formatted_subject`

**Inputs** self, doc.

**Explicit results** Platform.render\_template(self.subject, doc).

**Local steps**

- Return Platform.render\_template(self.subject, doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4471) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L195)

<a id="op-ef87bd59d9c58e"></a>
### Email Template.get formatted response

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_get_formatted_response`

**Inputs** self, doc.

**Explicit results** Platform.render\_template(self.response\_, doc).

**Local steps**

- Return Platform.render\_template(self.response\_, doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4542) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L194)

<a id="op-3e3ef2056c842f"></a>
### Email Template.get formatted email

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_get_formatted_email`

**Inputs** self, doc, sender = no value.

**Explicit results** mapping(“subject” → self.get\_formatted\_subject(doc), “message” → self.get\_formatted\_response(doc)).

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- If self.use\_html.
  - Set doc from self.inject\_email\_account(doc, sender).
- Return mapping(“subject” → self.get\_formatted\_subject(doc), “message” → self.get\_formatted\_response(doc)).

**Methods declared on this owner** [inject email account](operations-017.md#op-94b8b1b8eb4d6e), [get formatted subject](operations-017.md#op-fa810f362fca26), [get formatted response](operations-017.md#op-ef87bd59d9c58e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4613) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L193)

<a id="op-94b8b1b8eb4d6e"></a>
### Email Template.inject email account

`operation_foundation_email_record_definitions_email_template_business_behavior_email_template_inject_email_account`

**Inputs** self, doc, sender = no value.

**Explicit results** doc.

**Local steps**

- Bind dependencies EmailAccount.
- Bind dependencies get\_footer, get\_signature.
- If sender.
  - Set kwargs from mapping(“match\_by\_email” → sender).
- Otherwise.
  - Set kwargs from mapping(“match\_by\_doctype” → doc.get(“doctype”)).
- If email\_account bound to EmailAccount.find\_outgoing(expanded names kwargs).
  - Evaluate doc.update(mapping(“email\_signature” → get\_signature(email\_account), “email\_footer” → get\_footer(email\_account))).
- Return doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L4844) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L196)

<a id="op-4c21e4d75a3f54"></a>
### Get email template

`operation_foundation_email_record_definitions_email_template_business_behavior_get_email_template`

**Inputs** template\_name, doc, sender = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Email Template” via get\_doc.

**Explicit results** mapping(expand email\_template.get\_formatted\_email(doc, sender = sender), “use\_html” → email\_template.use\_html).

**Local steps**

- Set email\_template from Platform.get\_doc(“Email Template”, template\_name).
- Evaluate email\_template.check\_permission(“read”).
- Return mapping(expand email\_template.get\_formatted\_email(doc, sender = sender), “use\_html” → email\_template.use\_html).

**Values supplied outside this operation** effective access from email\_template.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L103) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L199)

<a id="op-5c74877ffdb231"></a>
### Get email templates

`operation_foundation_email_record_definitions_email_template_business_behavior_get_email_templates`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Email Template” via get\_list.

**Explicit results** Platform.get\_list(“Email Template”, filters = mapping(“name” → tuple(“like”, formatted text %{txt}%)), or\_filters = list(list(“reference\_doctype”, “=”, reference\_doctype), list(“reference\_doctype”, “is”, “ ….

**Local steps**

- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set reference\_doctype from (filters or mapping()).get(“reference\_doctype”, empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return Platform.get\_list(“Email Template”, filters = mapping(“name” → tuple(“like”, formatted text %{txt}%)), or\_filters = list(list(“reference\_doctype”, “=”, reference\_doctype), list(“reference\_doctype”, “is”, “ ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L104) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L200)

## Record · Email unsubscribe

[Record definition](../../../../data/record-types/email_unsubscribe.json)

<a id="op-b04137eb89b45b"></a>
### Email Unsubscribe.validate

`operation_foundation_email_record_definitions_email_unsubscribe_business_behavior_email_unsubscribe_validate`

**Inputs** self.

**Record and data access** read self.doctype via get\_value · read “Email Unsubscribe” via get\_all.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Reference DocType and Reference Name are required” · validation helper — translated “Delete this record to allow sending to this email address” · validation helper with Platform.DuplicateEntryError — translated “{0} already unsubscribed”.format(self.email) · validation helper with Platform.DuplicateEntryError — translated “{0} already unsubscribed for {1} {2}”.format(self.email, self.reference\_doctype, self.reference\_name).

**Local steps**

- If (not self.global\_unsubscribe and not (self.reference\_doctype and self.reference\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.global\_unsubscribe → not (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Call the validation error handler Platform.throw(translated “Reference DocType and Reference Name are required”, Platform.MandatoryError).
- If (not self.global\_unsubscribe and Platform.db.get\_value(self.doctype, self.name, “global\_unsubscribe”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.global\_unsubscribe → Platform.db.get\_value(self.doctype, self.name, “global\_unsubscribe”).
  - Call the validation error handler Platform.throw(translated “Delete this record to allow sending to this email address”).
- If self.global\_unsubscribe.
  - If Platform.get\_all(“Email Unsubscribe”, filters = mapping(“email” → self.email, “global\_unsubscribe” → 1, “name” → list(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “{0} already unsubscribed”.format(self.email), Platform.DuplicateEntryError).
- Otherwise.
  - If Platform.get\_all(“Email Unsubscribe”, filters = mapping(“email” → self.email, “reference\_doctype” → self.reference\_doctype, “reference\_name” → self.reference\_name, “name” → list(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “{0} already unsubscribed for {1} {2}”.format(self.email, self.reference\_doctype, self.reference\_name), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L5719) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L202)
