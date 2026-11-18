# Integration and transport · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email queue

[Record definition](../../../../data/record-types/email_queue.json)

<a id="op-f5158a555a19d1"></a>
### Send Mail Context.build message

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_build_message`

**Inputs** self, recipient\_email.

**Declared result** bytes.

**Explicit results** empty text · message.

**Local steps**

- Set message from self.queue\_doc.message.
- If not message.
  - Return empty text.
- Set message from message.replace(self.message\_placeholder(“tracker”), self.get\_tracker\_str(recipient\_email)).
- Set message from message.replace(self.message\_placeholder(“unsubscribe\_url”), self.get\_unsubscribe\_str(recipient\_email)).
- Set message from message.replace(self.message\_placeholder(“cc”), self.get\_receivers\_str()).
- Set message from message.replace(self.message\_placeholder(“recipient”), self.get\_recipient\_str(recipient\_email)).
- Set message from self.include\_attachments(message).
- Return message.

**Methods declared on this owner** [message placeholder](operations-015.md#op-a19143892c1fa3), [get tracker str](operations-016.md#op-3b339c14705fcb), [get unsubscribe str](operations-016.md#op-9302daa2f1b9a1), [get receivers str](operations-016.md#op-a61f2001eac6e0), [get recipient str](operations-016.md#op-2bc29b1b6a3426), [include attachments](operations-016.md#op-f400c5995719b1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L5831) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L166)

<a id="op-3b339c14705fcb"></a>
### Send Mail Context.get tracker str

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_get_tracker_text`

**Inputs** self, recipient\_email.

**Declared result** str.

**Explicit results** quopri.encodestring(tracker\_url\_html.encode()).decode() · empty text.

**Local steps**

- Set tracker\_url from empty text.
- If self.queue\_doc.get(“email\_read\_tracker\_url”).
  - Set email\_read\_tracker\_url from self.queue\_doc.email\_read\_tracker\_url.
  - Set params from mapping(“recipient\_email” → recipient\_email, “reference\_name” → self.queue\_doc.reference\_name, “reference\_doctype” → self.queue\_doc.reference\_doctype).
  - Set tracker\_url from get\_url(formatted text {email\_read\_tracker\_url}?{get\_signed\_params(params)}).
- Otherwise.
  - If (self.email\_account\_doc and self.email\_account\_doc.track\_email\_status and self.queue\_doc.communication).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.email\_account\_doc → self.email\_account\_doc.track\_email\_status → self.queue\_doc.communication.
    - Set tracker\_url from formatted text {get\_url()}/api/method/Platform.core.doctype.communication.email.mark\_email\_as\_seen?name={self.queue\_doc.communication}.
- If tracker\_url.
  - Set tracker\_url\_html from formatted text &lt;img src="{tracker\_url}"/&gt;.
  - Return quopri.encodestring(tracker\_url\_html.encode()).decode().
- Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L6227) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L173)

<a id="op-9302daa2f1b9a1"></a>
### Send Mail Context.get unsubscribe str

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_get_unsubscribe_text`

**Inputs** self, recipient\_email.

**Declared result** str.

**Explicit results** quopri.encodestring(unsubscribe\_url.encode()).decode().

**Local steps**

- Set unsubscribe\_url from empty text.
- If (self.queue\_doc.add\_unsubscribe\_link and self.queue\_doc.reference\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.queue\_doc.add\_unsubscribe\_link → self.queue\_doc.reference\_doctype.
  - Set unsubscribe\_url from get\_unsubcribed\_url(reference\_doctype = self.queue\_doc.reference\_doctype, reference\_name = self.queue\_doc.reference\_name, email = recipient\_email, unsubscribe\_method = self.queue\_doc.unsubscribe\_method, …).
- Return quopri.encodestring(unsubscribe\_url.encode()).decode().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L6674) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L174)

<a id="op-a61f2001eac6e0"></a>
### Send Mail Context.get receivers str

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_get_receivers_text`

**Inputs** self.

**Explicit results** message.

**Local steps**

- Set message from empty text.
- If self.queue\_doc.expose\_recipients equals “footer”.
  - Set to\_str from “, ”.join(self.queue\_doc.to).
  - Set cc\_str from “, ”.join(self.queue\_doc.cc).
  - Set message from formatted text This email was sent to {to\_str}.
  - Set message from formatted text {message} and copied to {cc\_str} when cc\_str, otherwise message.
    - Value choice on cc\_str — true gives formatted text {message} and copied to {cc\_str}, false gives message.
- Return message.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L6919) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L171)

<a id="op-2bc29b1b6a3426"></a>
### Send Mail Context.get recipient str

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_get_recipient_text`

**Inputs** self, recipient\_email.

**Explicit results** recipient\_email when self.queue\_doc.expose\_recipients differs from “header”, otherwise empty text.

**Local steps**

- Return recipient\_email when self.queue\_doc.expose\_recipients differs from “header”, otherwise empty text.
  - Value choice on self.queue\_doc.expose\_recipients differs from “header” — true gives recipient\_email, false gives empty text.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L7160) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L172)

<a id="op-f400c5995719b1"></a>
### Send Mail Context.include attachments

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_include_attachments`

**Inputs** self, message.

**Explicit results** safe\_encode(message\_obj.as\_string()).

**Local steps**

- Set message\_obj from self.get\_message\_object(message).
- For each attachment in self.attachments.
  - Evaluate add\_attachment(expanded names attachment, parent = message\_obj).
- Return safe\_encode(message\_obj.as\_string()).

**Methods declared on this owner** [get message object](operations-015.md#op-073115ab53e266).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L102) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L175)

<a id="op-01a177280c0125"></a>
### Send Mail Context.attachments

`operation_foundation_binding_foundation_email_doctype_email_queue_email_queue_sendmailcontext_attachments`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at dict.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** attachments.

**Local steps**

- Set attachments from list().
- For each attachment in self.queue\_doc.attachments\_list.
  - If attachment.get(“fcontent”).
    - Continue with the next iteration or loop test.
  - Set file\_filters from mapping().
  - If attachment.get(“fid”).
    - Set file\_filters at “name” from attachment.get(“fid”).
  - Otherwise.
    - If attachment.get(“file\_url”).
      - Set file\_filters at “file\_url” from attachment.get(“file\_url”).
  - If file\_filters.
    - Set \_file from Platform.get\_doc(“File”, file\_filters).
    - Set fcontent from \_file.get\_content().
    - Evaluate attachment.update(mapping(“fname” → \_file.file\_name, “fcontent” → fcontent)).
    - Evaluate attachment.pop(“fid”, no value).
    - Evaluate attachment.pop(“file\_url”, no value).
    - Evaluate attachments.append(attachment).
  - Otherwise.
    - If attachment.get(“print\_format\_attachment”) equals 1.
      - Evaluate attachment.pop(“print\_format\_attachment”, no value).
      - If (attachment.pop(“print\_as\_owner”, no value) and not Platform.request).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in attachment.pop(“print\_as\_owner”, no value) → not Platform.request.
        - Set session\_user from Platform.session.user.
        - Evaluate Platform.set\_user(self.queue\_doc.owner).
        - Attempt the following.
          - Set print\_format\_file from Platform.attach\_print(expanded names attachment).
        - On exit, including pending return or failure.
          - Evaluate Platform.set\_user(session\_user).
      - Otherwise.
        - Set print\_format\_file from Platform.attach\_print(expanded names attachment).
      - Evaluate self.\_store\_file(print\_format\_file at “fname”, print\_format\_file at “fcontent”).
      - Evaluate attachments.append(print\_format\_file).
- Return attachments.

**Methods declared on this owner** [store file](operations-016.md#op-b7c9fb55a5df6c).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L100) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L825)

<a id="op-b7c9fb55a5df6c"></a>
### Send Mail Context.store file

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_mail_context_store_file`

**Inputs** self, file\_name, content.

**Record and data access** read “File” via exists.

**State and service calls** request new\_doc for “File” · call insert on file.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_system\_settings(“store\_attached\_pdf\_document”).
  - Return no value.
- Set file\_data from Platform.\_dict(file\_name = file\_name, is\_private = 1).
- If self.queue\_doc.communication.
  - Set file\_data.attached\_to\_doctype from “Communication”.
  - Set file\_data.attached\_to\_name from self.queue\_doc.communication.
- Otherwise.
  - Set file\_data.attached\_to\_doctype from self.queue\_doc.doctype.
  - Set file\_data.attached\_to\_name from self.queue\_doc.name.
- If Platform.db.exists(“File”, file\_data).
  - Return no value.
- Set file from Platform.new\_doc(“File”, expanded names file\_data).
- Set file.content from content.
- Evaluate file.insert().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“store\_attached\_pdf\_document”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L749) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L179)

<a id="op-a78e970b659f19"></a>
### Retry sending

`operation_foundation_email_record_definitions_email_queue_business_behavior_retry_sending`

**Inputs** queues.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- If not Platform.has\_permission(“Email Queue”, throw = true).
  - Return no value.
- If isinstance(queues, str).
  - Set queues from json.loads(queues).
- If not queues.
  - Return no value.
- Set email\_queue from Platform.qb.DocType(“Email Queue”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(email\_queue.modified\_by, nested operand in the contract.session.user).where((nested operand in the contrac ….run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Email Queue”, throw = true) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L101) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L165)

<a id="op-fb5815161d8090"></a>
### Send now

`operation_foundation_email_record_definitions_email_queue_business_behavior_send_now`

**Inputs** name, force\_send = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set record from EmailQueue.find(name).
- If record.
  - Evaluate record.check\_permission().
  - Evaluate record.send(force\_send = force\_send).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from record.check\_permission().

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L1524) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L181)

<a id="op-db6a95b6a1d5b7"></a>
### Toggle sending

`operation_foundation_email_record_definitions_email_queue_business_behavior_toggle_sending`

**Inputs** enable.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “Activity Log”, “user” → Platform.session.user, “status” → “Success”, “subject” → formatted text Email Queue sending {action.lower()}) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Activity Log”, “user” → Platform.session.user, “status” → “Success”, “subject” → formatted text Email Queue sending {action.lower()})).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set suspend\_value from 0 when sbool(enable), otherwise 1.
  - Value choice on sbool(enable) — true gives 0, false gives 1.
- Evaluate Platform.db.set\_default(“suspend\_email\_queue”, suspend\_value).
- Set action from “Resumed” when suspend\_value equals 0, otherwise “Suspended”.
  - Value choice on suspend\_value equals 0 — true gives “Resumed”, false gives “Suspended”.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Activity Log”, “user” → Platform.session.user, “status” → “Success”, “subject” → formatted text Email Queue sending {nested operand in the contract.lower()})).insert(i ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L1692) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L182)

<a id="op-edc06f69473ae7"></a>
### On doctype update

`operation_foundation_email_record_definitions_email_queue_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Email Queue”.

**Local steps**

- Evaluate Platform.db.add\_index(“Email Queue”, tuple(“status”, “send\_after”, “priority”, “creation”), “index\_bulk\_flush”).
- Evaluate Platform.db.add\_index(“Email Queue”, list(“message\_id(140)”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L2055) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L142)

<a id="op-c23d809ce4b511"></a>
### Get email retry limit

`operation_foundation_email_record_definitions_email_queue_business_behavior_get_email_retry_limit`

**Inputs** no declared parameters.

**Explicit results** (cint(Platform.db.get\_system\_setting(“email\_retry\_limit”)) or 3).

**Local steps**

- Return (cint(Platform.db.get\_system\_setting(“email\_retry\_limit”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_system\_setting(“email\_retry\_limit”)) → 3.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L2195) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L141)

<a id="op-6bfd364421f6b6"></a>
### Queue Builder.initialize

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_initialize`

**Inputs** self, recipients = no value, sender = no value, subject = no value, message = no value, text\_content = no value, reference\_doctype = no value, reference\_name = no value, unsubscribe\_method = no value, unsubscribe\_params = no value, unsubscribe\_message = no value, attachments = no value, reply\_to = no value, cc = no value, bcc = no value, message\_id = no value, in\_reply\_to = no value, send\_after = no value, expose\_recipients = no value, send\_priority = 1, communication = no value, read\_receipt = no value, queue\_separately = false, is\_notification = false, add\_unsubscribe\_link = 1, inline\_images = no value, header = no value, print\_letterhead = false, with\_container = false, email\_read\_tracker\_url = no value, x\_priority = 3, email\_headers = no value, raw\_html = false, add\_css = true, redact\_message\_after\_send = false, wrapper = no value.

**Local steps**

- Set self.\_unsubscribe\_method from unsubscribe\_method.
- Set self.\_recipients from recipients.
- Set self.\_cc from cc.
- Set self.\_bcc from bcc.
- Set self.\_send\_after from send\_after.
- Set self.\_sender from sender.
- Set self.\_text\_content from text\_content.
- Set self.\_message from message.
- Set self.\_x\_priority from x\_priority.
- Set self.\_add\_unsubscribe\_link from add\_unsubscribe\_link.
- Set self.\_unsubscribe\_message from unsubscribe\_message.
- Set self.\_attachments from attachments.
- Set self.\_unsubscribed\_user\_emails from no value.
- Set self.\_email\_account from no value.
- Set self.unsubscribe\_params from unsubscribe\_params.
- Set self.subject from subject.
- Set self.reference\_doctype from reference\_doctype.
- Set self.reference\_name from reference\_name.
- Set self.expose\_recipients from expose\_recipients.
- Set self.with\_container from with\_container.
- Set self.header from header.
- Set self.reply\_to from reply\_to.
- Set self.message\_id from message\_id.
- Set self.in\_reply\_to from in\_reply\_to.
- Set self.send\_priority from send\_priority.
- Set self.communication from communication.
- Set self.read\_receipt from read\_receipt.
- Set self.queue\_separately from queue\_separately.
- Set self.is\_notification from is\_notification.
- Set self.inline\_images from inline\_images.
- Set self.print\_letterhead from print\_letterhead.
- Set self.email\_read\_tracker\_url from email\_read\_tracker\_url.
- Set self.email\_headers from email\_headers.
- Set self.raw\_html from raw\_html.
- Set self.add\_css from add\_css.
- Set self.redact\_message\_after\_send from redact\_message\_after\_send.
- Set self.email\_wrapper from (wrapper or “templates/emails/standard.html”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in wrapper → “templates/emails/standard.html”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L2275) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L155)

<a id="op-fdf3fa84fc2c08"></a>
### Queue Builder.unsubscribe method

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_unsubscribe_method`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.\_unsubscribe\_method or “/api/method/Platform.email.queue.unsubscribe”).

**Local steps**

- Return (self.\_unsubscribe\_method or “/api/method/Platform.email.queue.unsubscribe”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_unsubscribe\_method → “/api/method/Platform.email.queue.unsubscribe”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3338) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L164)

<a id="op-0a006999652714"></a>
### Queue Builder.get emails list

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_get_emails_list`

**Inputs** self, emails = no value.

**Explicit results** list of each for each drawn from set(emails) where each.

**Local steps**

- Set emails from split\_emails(emails) when isinstance(emails, str), otherwise (emails or list()).
  - Value choice on isinstance(emails, str) — true gives split\_emails(emails), false gives (emails or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in emails → list().
- Return list of each for each drawn from set(emails) where each.
  - Draw each from set(emails), keep a combination only if (each).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3399) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L152)

<a id="op-e9eb0db5f86194"></a>
### Queue Builder.recipients

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_recipients`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.\_get\_emails\_list(self.\_recipients).

**Local steps**

- Return self.\_get\_emails\_list(self.\_recipients).

**Methods declared on this owner** [get emails list](operations-016.md#op-0a006999652714).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3547) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L158)

<a id="op-8d260f84300ab8"></a>
### Queue Builder.cc

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_carbon_copy`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.\_get\_emails\_list(self.\_cc).

**Local steps**

- Return self.\_get\_emails\_list(self.\_cc).

**Methods declared on this owner** [get emails list](operations-016.md#op-0a006999652714).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3612) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L145)

<a id="op-a2db68e2c0235f"></a>
### Queue Builder.bcc

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_blind_carbon_copy`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.\_get\_emails\_list(self.\_bcc).

**Local steps**

- Return self.\_get\_emails\_list(self.\_bcc).

**Methods declared on this owner** [get emails list](operations-016.md#op-0a006999652714).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3677) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L144)

<a id="op-5b435824cc331a"></a>
### Queue Builder.send after

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_send_after`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** add\_days(nowdate(), self.\_send\_after) · self.\_send\_after.

**Local steps**

- If isinstance(self.\_send\_after, int).
  - Return add\_days(nowdate(), self.\_send\_after).
- Return self.\_send\_after.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3742) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L159)

<a id="op-64aec9b9a6a5be"></a>
### Queue Builder.sender

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_sender`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** email\_account.default\_sender · self.\_sender.

**Local steps**

- If (not self.\_sender or self.\_sender equals “Administrator”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.\_sender → self.\_sender equals “Administrator”.
  - Set email\_account from self.get\_outgoing\_email\_account().
  - Return email\_account.default\_sender.
- Return self.\_sender.

**Methods declared on this owner** [get outgoing email account](operations-017.md#op-801dc71dda84b3).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3858) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L161)

<a id="op-53e5cbc5da0efa"></a>
### Queue Builder.email text content

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_email_text_content`

**Inputs** self.

**Explicit results** (self.\_text\_content + unsubscribe\_text\_message) · (text\_content + unsubscribe\_text\_message).

**Local steps**

- Set unsubscribe\_msg from self.unsubscribe\_message().
- Set unsubscribe\_text\_message from ((unsubscribe\_msg and unsubscribe\_msg.text) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (unsubscribe\_msg and unsubscribe\_msg.text) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in unsubscribe\_msg → unsubscribe\_msg.text.
- If self.\_text\_content.
  - Return (self.\_text\_content + unsubscribe\_text\_message).
- Attempt the following.
  - Set text\_content from html\_to\_plain\_text(self.\_message).
- On failure (Exception).
  - Set text\_content from “See html attachment”.
- Return (text\_content + unsubscribe\_text\_message).

**Methods declared on this owner** [unsubscribe message](operations-017.md#op-a03021bbc12e2d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L3986) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L147)

<a id="op-3aeae7e7a841f3"></a>
### Queue Builder.email html content

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_email_document_markup_content`

**Inputs** self.

**Explicit results** get\_formatted\_html(self.subject, self.\_message, header = self.header, email\_account = email\_account, unsubscribe\_link = self.unsubscribe\_message(), with\_container = self.with\_container, …).

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- Return get\_formatted\_html(self.subject, self.\_message, header = self.header, email\_account = email\_account, unsubscribe\_link = self.unsubscribe\_message(), with\_container = self.with\_container, …).

**Methods declared on this owner** [get outgoing email account](operations-017.md#op-801dc71dda84b3), [unsubscribe message](operations-017.md#op-a03021bbc12e2d).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L4192) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L146)

<a id="op-a15da2a3d73504"></a>
### Queue Builder.should include unsubscribe link

`operation_foundation_email_record_definitions_email_queue_business_behavior_queue_builder_should_include_unsubscribe_link`

**Inputs** self.

**Explicit results** (self.\_add\_unsubscribe\_link equals 1 and self.reference\_doctype and (self.\_unsubscribe\_message or self.reference\_doctype equals “Newsletter”)).

**Local steps**

- Return (self.\_add\_unsubscribe\_link equals 1 and self.reference\_doctype and (self.\_unsubscribe\_message or self.reference\_doctype equals “Newsletter”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_add\_unsubscribe\_link equals 1 → self.reference\_doctype → (self.\_unsubscribe\_message or self.reference\_doctype equals “Newsletter”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_unsubscribe\_message → self.reference\_doctype equals “Newsletter”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0227.json#L4388) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L162)
