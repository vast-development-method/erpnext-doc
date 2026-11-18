# Record lifecycle and persistence · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Communication

[Record definition](../../../../data/record-types/communication.json)

<a id="op-7ccdd0c77b4332"></a>
### Update parent document on communication

`operation_foundation_core_record_definitions_communication_business_behavior_update_parent_document_on_communication`

**Inputs** doc.

**State and service calls** call db\_set on parent.

**Explicit results** no value.

**Local steps**

- Set parent from get\_parent\_doc(doc).
- If not parent.
  - Return no value.
- Set status\_field from parent.meta.get\_field(“status”).
- If status\_field.
  - Set options from (status\_field.options or empty text).splitlines().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in status\_field.options → empty text.
  - If ((“Open” belongs to options and parent.status equals “Replied” and doc.sent\_or\_received equals “Received”) or (parent.doctype equals “Issue” and “Open” belongs to options and doc.sent\_or\_received equals “Received”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (“Open” belongs to options and parent.status equals “Replied” and doc.sent\_or\_received equals “Received”) → (parent.doctype equals “Issue” and “Open” belongs to options and doc.sent\_or\_received equals “Received”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in “Open” belongs to options → parent.status equals “Replied” → doc.sent\_or\_received equals “Received”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.doctype equals “Issue” → “Open” belongs to options → doc.sent\_or\_received equals “Received”.
    - Evaluate parent.db\_set(“status”, “Open”).
    - Evaluate parent.run\_method(“handle\_hold\_time”, “Replied”).
    - Evaluate apply\_assignment\_rule(parent).
- Evaluate update\_first\_response\_time(parent, doc).
- Evaluate set\_avg\_response\_time(parent, doc).
- Evaluate parent.run\_method(“notify\_communication”, doc).
- Evaluate parent.notify\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from parent.run\_method(“handle\_hold\_time”, “Replied”), parent.run\_method(“notify\_communication”, doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L3033) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1048)

<a id="op-4f810f32b789ab"></a>
### Update first response time

`operation_foundation_core_record_definitions_communication_business_behavior_update_first_response_time`

**Inputs** parent, communication.

**Record and data access** read “User” via get\_cached\_value.

**State and service calls** call db\_set on parent.

**Local steps**

- If (parent.meta.has\_field(“first\_response\_time”) and not parent.get(“first\_response\_time”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.meta.has\_field(“first\_response\_time”) → not parent.get(“first\_response\_time”).
  - If (is\_system\_user(communication.sender) or Platform.get\_cached\_value(“User”, Platform.session.user, “user\_type”) equals “System User”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_system\_user(communication.sender) → Platform.get\_cached\_value(“User”, Platform.session.user, “user\_type”) equals “System User”.
    - If (communication.sent\_or\_received equals “Sent” and communication.communication\_type equals “Communication”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in communication.sent\_or\_received equals “Sent” → communication.communication\_type equals “Communication”.
      - Set first\_responded\_on from communication.creation.
      - If parent.meta.has\_field(“first\_responded\_on”).
        - Evaluate parent.db\_set(“first\_responded\_on”, first\_responded\_on).
      - Set first\_response\_time from round(time\_diff\_in\_seconds(first\_responded\_on, parent.creation), 2).
      - Evaluate parent.db\_set(“first\_response\_time”, first\_response\_time).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “user\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L3513) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1047)

<a id="op-92da8c7001dcf2"></a>
### Set avg response time

`operation_foundation_core_record_definitions_communication_business_behavior_set_average_response_time`

**Inputs** parent, communication.

**Record and data access** read “Communication” via get\_list.

**State and service calls** call db\_set on parent.

**Local steps**

- If (parent.meta.has\_field(“avg\_response\_time”) and communication.sent\_or\_received equals “Sent”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.meta.has\_field(“avg\_response\_time”) → communication.sent\_or\_received equals “Sent”.
  - Set communications from Platform.get\_list(“Communication”, filters = mapping(“reference\_doctype” → parent.doctype, “reference\_name” → parent.name), fields = list(“sent\_or\_received”, “name”, “creation”), order\_by = “creation”).
  - If len(communications).
    - Set response\_times from list().
    - For each i in range(len(communications)).
      - If (communications at i.sent\_or\_received equals “Sent” and communications at (i − 1).sent\_or\_received equals “Received”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in communications at i.sent\_or\_received equals “Sent” → communications at (i − 1).sent\_or\_received equals “Received”.
        - Set response\_time from round(time\_diff\_in\_seconds(communications at i.creation, communications at (i − 1).creation), 2).
        - If response\_time &gt; 0.
          - Evaluate response\_times.append(response\_time).
    - If response\_times.
      - Set avg\_response\_time from (sum(response\_times) ÷ len(response\_times)).
      - Evaluate parent.db\_set(“avg\_response\_time”, avg\_response\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L3940) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1046)

<a id="op-b8296df2fd50ea"></a>
### Make

`operation_foundation_core_record_definitions_communication_email_business_behavior_make`

**Inputs** doctype = no value, name = no value, content = no value, subject = no value, sent\_or\_received = “Sent”, sender = no value, sender\_full\_name = no value, recipients = no value, communication\_medium = “Email”, send\_email = false, print\_html = no value, print\_format = no value, attachments = no value, send\_me\_a\_copy = false, cc = no value, bcc = no value, read\_receipt = no value, print\_letterhead = true, letterhead = no value, email\_template = no value, communication\_type = no value, send\_after = no value, print\_language = no value, now = false, raw\_html = false, add\_css = true, in\_reply\_to = no value, print\_style = no value, print\_settings = no value, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, str).

**Record and data access** read “Email Template” via get\_cached\_value.

**Explicit results** \_make(doctype = doctype, name = name, content = content, subject = subject, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Bind dependencies warn.
- If kwargs.
  - Evaluate warn(formatted text Options {kwargs} used in Platform.core.doctype.communication.email.make are deprecated or unsupported, category = DeprecationWarning).
- If not Platform.permissions.is\_system\_user().
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- If (doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Evaluate Platform.has\_permission(doctype, doc = name, ptype = “email”, throw = true).
- Otherwise.
  - Evaluate Platform.has\_permission(“Communication”, ptype = “create”, throw = true).
- If letterhead.
  - Evaluate Platform.has\_permission(“Letter Head”, doc = letterhead, ptype = “read”, throw = true).
- If (raw\_html and email\_template and not Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in raw\_html → email\_template → not Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”).
  - Evaluate warn(translated “Raw HTML can be used only with Email Templates having 'Use HTML' checked. Proceeding with plain text email.”, category = UserWarning).
  - Set raw\_html from false.
- Return \_make(doctype = doctype, name = name, content = content, subject = subject, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = name, ptype = “email”, throw = true), Platform.has\_permission(“Communication”, ptype = “create”, throw = true) and 1 further calls · configured or stored value from Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L164) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1050)

<a id="op-a254019cc53230"></a>
### Make

`operation_foundation_core_record_definitions_communication_email_business_behavior_make_2`

**Inputs** doctype = no value, name = no value, content = no value, subject = no value, sent\_or\_received = “Sent”, sender = no value, sender\_full\_name = no value, recipients = no value, communication\_medium = “Email”, send\_email = false, print\_html = no value, print\_format = no value, attachments = no value, send\_me\_a\_copy = false, cc = no value, bcc = no value, read\_receipt = no value, print\_letterhead = true, letterhead = no value, email\_template = no value, communication\_type = no value, add\_signature = true, send\_after = no value, print\_language = no value, now = false, raw\_html = false, add\_css = true, in\_reply\_to = no value, print\_style = no value, print\_settings = no value.

**Declared result** dict at tuple(str, str).

**Record and data access** resolve a document from mapping(“doctype” → “Communication”, “subject” → subject, “content” → content, “sender” → sender, …) via get\_doc · read “Email Template” via get\_cached\_value.

**State and service calls** call insert on comm.

**Explicit results** mapping(“name” → comm.name, “emails\_not\_sent\_to” → “, ”.join(emails\_not\_sent\_to)).

**Explicit failure paths** validation helper — translated “At least one recipient is required” · validation helper with Platform.OutgoingEmailError — translated “Unable to send mail because of a missing email account. Please setup default Email Account from Settings &gt; E …”.

**Local steps**

- Set sender from (sender or get\_formatted\_email(Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sender → get\_formatted\_email(Platform.session.user).
- Set recipients from list\_to\_str(recipients) when isinstance(recipients, list), otherwise recipients.
  - Value choice on isinstance(recipients, list) — true gives list\_to\_str(recipients), false gives recipients.
- Set cc from list\_to\_str(cc) when isinstance(cc, list), otherwise cc.
  - Value choice on isinstance(cc, list) — true gives list\_to\_str(cc), false gives cc.
- Set bcc from list\_to\_str(bcc) when isinstance(bcc, list), otherwise bcc.
  - Value choice on isinstance(bcc, list) — true gives list\_to\_str(bcc), false gives bcc.
- Set comm from Platform.get\_doc(mapping(“doctype” → “Communication”, “subject” → subject, “content” → content, “sender” → sender, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cc → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bcc → no value.
  - Value choice on attachments — true gives 1, false gives 0.
- Set comm.flags.skip\_add\_signature from (not add\_signature or (raw\_html and Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not add\_signature → (raw\_html and Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in raw\_html → Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”).
- If (cint(send\_email) and not (recipients or cc or bcc)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(send\_email) → not (recipients or cc or bcc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in recipients → cc → bcc.
  - Call the validation error handler Platform.throw(translated “At least one recipient is required”).
- Evaluate comm.insert(ignore\_permissions = true).
- If attachments.
  - If isinstance(attachments, str).
    - Set attachments from json.loads(attachments).
  - Evaluate add\_attachments(comm.name, attachments).
- If cint(send\_email).
  - If not comm.get\_outgoing\_email\_account().
    - Call the validation error handler Platform.throw(translated “Unable to send mail because of a missing email account. Please setup default Email Account from Settings &gt; E …”, exc = Platform.OutgoingEmailError).
  - Evaluate comm.send\_email(print\_html = print\_html, print\_format = print\_format, send\_me\_a\_copy = send\_me\_a\_copy, print\_letterhead = print\_letterhead, …).
- Set emails\_not\_sent\_to from comm.exclude\_emails\_list(include\_sender = send\_me\_a\_copy).
- Return mapping(“name” → comm.name, “emails\_not\_sent\_to” → “, ”.join(emails\_not\_sent\_to)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Email Template”, email\_template, “use\_html”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L2) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1051)

<a id="op-e6cba1ec5c43f7"></a>
### Validate email

`operation_foundation_core_record_definitions_communication_email_business_behavior_validate_email`

**Inputs** doc.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (doc.communication\_type differs from “Communication” or doc.communication\_medium differs from “Email” or doc.flags.in\_receive).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.communication\_type differs from “Communication” → doc.communication\_medium differs from “Email” → doc.flags.in\_receive.
  - Return no value.
- For each email in split\_emails(doc.recipients).
  - Evaluate validate\_email\_address(email, throw = true).
- For each email in split\_emails(doc.cc).
  - Evaluate validate\_email\_address(email, throw = true).
- For each email in split\_emails(doc.bcc).
  - Evaluate validate\_email\_address(email, throw = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1057)

<a id="op-88e3c8c4fca28b"></a>
### Set incoming outgoing accounts

`operation_foundation_core_record_definitions_communication_email_business_behavior_set_incoming_outgoing_accounts`

**Inputs** doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Bind dependencies EmailAccount.
- Set incoming\_email\_account from EmailAccount.find\_incoming(match\_by\_email = doc.sender, match\_by\_doctype = doc.reference\_doctype).
- Set doc.incoming\_email\_account from incoming\_email\_account.email\_id when incoming\_email\_account, otherwise no value.
  - Value choice on incoming\_email\_account — true gives incoming\_email\_account.email\_id, false gives no value.
- Set doc.outgoing\_email\_account from EmailAccount.find\_outgoing(match\_by\_email = doc.sender, match\_by\_doctype = doc.reference\_doctype).
- If doc.sent\_or\_received equals “Sent”.
  - Evaluate doc.db\_set(“email\_account”, doc.outgoing\_email\_account.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L315) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1054)

<a id="op-8b564802df3f22"></a>
### Add attachments

`operation_foundation_core_record_definitions_communication_email_business_behavior_add_attachments`

**Inputs** name, attachments.

**Declared result** no value.

**Record and data access** read “File” via get\_value.

**State and service calls** request new\_doc for “File” · call save on \_file.

**Local steps**

- For each a in attachments.
  - If isinstance(a, str).
    - Set attach from Platform.db.get\_value(“File”, mapping(“name” → a), list(“file\_url”, “is\_private”), as\_dict = 1).
    - Set file\_args from mapping(“file\_url” → attach.file\_url, “is\_private” → attach.is\_private).
  - Otherwise.
    - If (isinstance(a, dict) and “fcontent” belongs to a and “fname” belongs to a).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(a, dict) → “fcontent” belongs to a → “fname” belongs to a.
      - Set file\_args from mapping(“file\_name” → a at “fname”, “content” → a at “fcontent”, “is\_private” → 1).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Evaluate file\_args.update(mapping(“attached\_to\_doctype” → “Communication”, “attached\_to\_name” → name, “folder” → “Home/Attachments”)).
  - Set \_file from Platform.new\_doc(“File”).
  - Evaluate \_file.update(file\_args).
  - Evaluate \_file.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L561) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1049)

<a id="op-0d9abecbbbebee"></a>
### Mark email as seen

`operation_foundation_core_record_definitions_communication_email_business_behavior_mark_email_as_seen`

**Inputs** name = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = tuple(“GET”)).

**Local steps**

- Evaluate commit\_after\_response(deferred anonymous expression).
- Evaluate Platform.response.update(Platform.utils.get\_imaginary\_pixel\_response()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L1122) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1052)

<a id="op-c43460c5ca6b40"></a>
### Mark email as seen

`operation_foundation_core_record_definitions_communication_email_business_behavior_mark_email_as_seen_2`

**Inputs** name.

**Local steps**

- Attempt the following.
  - Evaluate update\_communication\_as\_read(name).
- On failure (Exception).
  - Evaluate Platform.log\_error(“Unable to mark as seen”, no value, “Communication”, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L1291) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1053)

<a id="op-db2239697ef8b3"></a>
### Update communication as read

`operation_foundation_core_record_definitions_communication_email_business_behavior_update_communication_as_read`

**Inputs** name.

**Record and data access** read “Communication” via get\_value.

**State and service calls** request set\_value on “Communication”.

**Explicit results** no value.

**Local steps**

- If (not name or not isinstance(name, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not isinstance(name, str).
  - Return no value.
- Set communication from Platform.db.get\_value(“Communication”, name, “read\_by\_recipient”, as\_dict = true).
- If (not communication or communication.read\_by\_recipient).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not communication → communication.read\_by\_recipient.
  - Return no value.
- Evaluate Platform.db.set\_value(“Communication”, name, mapping(“read\_by\_recipient” → 1, “delivery\_status” → “Read”, “read\_by\_recipient\_on” → get\_datetime())).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L1403) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1056)

<a id="op-2082527ebb0f41"></a>
### Undo email send

`operation_foundation_core_record_definitions_communication_email_business_behavior_undo_email_send`

**Inputs** communication\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Communication” via get\_doc · read “Email Queue” via get\_all · read “File” via get\_all.

**State and service calls** msgprint with translated “Email undo window is over. Cannot undo email.” · msgprint with translated “It is too late to undo this email. It is already being sent.” · request delete\_doc for “Email Queue” · request set\_value on “File”.

**Explicit results** communication\_data.

**Explicit failure paths** validation helper — translated “You are not authorized to undo this email” · validation helper — translated “Failed to delete communication”.

**Local steps**

- Set communication from Platform.get\_doc(“Communication”, communication\_name).
- If communication.owner differs from Platform.session.user.
  - Call the validation error handler Platform.throw(translated “You are not authorized to undo this email”).
- If (communication.sent\_or\_received differs from “Sent” or communication.communication\_medium differs from “Email”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication.sent\_or\_received differs from “Sent” → communication.communication\_medium differs from “Email”.
  - Call the validation error handler Platform.throw(translated “Failed to delete communication”).
- Set time\_elapsed\_in\_seconds from time\_diff\_in\_seconds(now\_datetime(), communication.creation).
- If time\_elapsed\_in\_seconds &gt; 10.
  - Evaluate Platform.msgprint(translated “Email undo window is over. Cannot undo email.”, alert = true, indicator = “red”, raise\_exception = 1).
- Set email\_queue\_records from Platform.get\_all(“Email Queue”, filters = mapping(“communication” → communication\_name), fields = list(“name”, “status”)).
- For each queue in email\_queue\_records.
  - If queue.status differs from “Not Sent”.
    - Evaluate Platform.msgprint(translated “It is too late to undo this email. It is already being sent.”, alert = true, indicator = “red”, raise\_exception = 1).
- For each queue in email\_queue\_records.
  - Evaluate Platform.delete\_doc(“Email Queue”, queue.name, ignore\_permissions = true).
- Set communication\_data from mapping(“subject” → communication.subject, “content” → communication.content, “recipients” → communication.recipients, “cc” → communication.cc, …).
- Set linked\_files from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → “Communication”, “attached\_to\_name” → communication\_name), pluck = “name”).
- If linked\_files.
  - For each file\_name in linked\_files.
    - Evaluate Platform.db.set\_value(“File”, file\_name, mapping(“attached\_to\_doctype” → no value, “attached\_to\_name” → no value)).
- Set communication\_data at “attachments” from linked\_files.
- Evaluate communication.delete(ignore\_permissions = true).
- Return communication\_data.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L1678) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1055)

<a id="op-1dc72e9f282e45"></a>
### Communication Email Mixin.is email communication

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_is_email_communication`

**Inputs** self.

**Explicit results** (self.communication\_type equals “Communication” and self.communication\_medium equals “Email”).

**Local steps**

- Return (self.communication\_type equals “Communication” and self.communication\_medium equals “Email”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.communication\_type equals “Communication” → self.communication\_medium equals “Email”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L2771) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1077)

<a id="op-c7e29835f350e4"></a>
### Communication Email Mixin.get owner

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_owner`

**Inputs** self.

**Explicit results** parent\_doc.owner when parent\_doc, otherwise no value.

**Local steps**

- Set parent\_doc from get\_parent\_doc(self).
- Return parent\_doc.owner when parent\_doc, otherwise no value.
  - Value choice on parent\_doc — true gives parent\_doc.owner, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L2855) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1075)

<a id="op-8816c465b2d702"></a>
### Communication Email Mixin.get notification recipient

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_notification_recipient`

**Inputs** self.

**Explicit results** no value · notification\_email · parent\_doc.owner.

**Local steps**

- Set parent\_doc from get\_parent\_doc(self).
- If not parent\_doc.
  - Return no value.
- Set notification\_email from parent\_doc.run\_method(“get\_notification\_email”).
- If notification\_email.
  - Return notification\_email.
- Return parent\_doc.owner.

**Values supplied outside this operation** selected callable from parent\_doc.run\_method(“get\_notification\_email”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L2934) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1073)

<a id="op-adffd53c59eabf"></a>
### Communication Email Mixin.get all email addresses

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_all_email_addresses`

**Inputs** self, exclude\_displayname = false.

**Explicit results** ((self.to\_list(exclude\_displayname = exclude\_displayname) + self.cc\_list(exclude\_displayname = exclude\_displayname)) + self.bcc\_list(exclude\_displayname = exclude\_displayname)).

**Local steps**

- Return ((self.to\_list(exclude\_displayname = exclude\_displayname) + self.cc\_list(exclude\_displayname = exclude\_displayname)) + self.bcc\_list(exclude\_displayname = exclude\_displayname)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L3070) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1063)

<a id="op-7491f491fd2847"></a>
### Communication Email Mixin.get email with displayname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_email_with_displayname`

**Inputs** self, email\_address.

**Explicit results** email\_address · email\_map.get(email, email).

**Local steps**

- Set tuple(display\_name, email) from parse\_addr(email\_address).
- If (display\_name and display\_name differs from email).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in display\_name → display\_name differs from email.
  - Return email\_address.
- Set email\_map from mapping of parse\_addr(email) at 1 → email for email drawn from self.get\_all\_email\_addresses().
  - Draw email from self.get\_all\_email\_addresses().
- Return email\_map.get(email, email).

**Methods declared on this owner** [get all email addresses](operations-006.md#op-adffd53c59eabf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L3198) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1067)

<a id="op-3f1e970b01df98"></a>
### Communication Email Mixin.mail recipients

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_recipients`

**Inputs** self, is\_inbound\_mail\_communcation = false.

**Explicit results** list() · self.\_final\_recipients.

**Local steps**

- If is\_inbound\_mail\_communcation.
  - Return list().
- If hasattr(self, “\_final\_recipients”).
  - Return self.\_final\_recipients.
- Set to from self.to\_list().
- Set self.\_final\_recipients from list(filter(deferred anonymous expression, to)).
- Return self.\_final\_recipients.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L3407) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1081)

<a id="op-718175013ad16e"></a>
### Communication Email Mixin.get mail recipients with displayname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_mail_recipients_with_displayname`

**Inputs** self, is\_inbound\_mail\_communcation = false.

**Explicit results** list of self.get\_email\_with\_displayname(email) for email drawn from to\_list.

**Local steps**

- Set to\_list from self.mail\_recipients(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation).
- Return list of self.get\_email\_with\_displayname(email) for email drawn from to\_list.
  - Draw email from to\_list.

**Methods declared on this owner** [mail recipients](operations-006.md#op-3f1e970b01df98), [get email with displayname](operations-006.md#op-7491f491fd2847).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L3607) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1071)

<a id="op-84a26ca214b8ad"></a>
### Communication Email Mixin.mail cc

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_carbon_copy`

**Inputs** self, is\_inbound\_mail\_communcation = false, include\_sender = false.

**Record and data access** read “User” via get\_value.

**Explicit results** self.\_final\_cc.

**Local steps**

- If hasattr(self, “\_final\_cc”).
  - Return self.\_final\_cc.
- Set cc from self.cc\_list().
- If include\_sender.
  - Set sender from self.sender\_mailid.
  - If Platform.session.user does not belong to Platform.STANDARD\_USERS.
    - Set sender from Platform.db.get\_value(“User”, Platform.session.user, “email”).
  - Evaluate cc.append(sender).
- If is\_inbound\_mail\_communcation.
  - If notification\_recipient bound to self.get\_notification\_recipient().
    - Evaluate cc.append(notification\_recipient).
  - Set cc from (set(cc) − set(self.sender\_mailid)).
  - Set assignees from (set(self.get\_assignees()) − set(self.sender\_mailid)).
  - For each assignee in assignees.copy().
    - If not is\_email\_enabled\_for\_feature(assignee, “enable\_email\_threads\_on\_assigned\_document”).
      - Evaluate assignees.remove(assignee).
  - Evaluate cc.update(assignees).
- Set cc from (set(cc) − set(self.filter\_thread\_notification\_disbled\_users(cc))).
- Set cc from (cc − set(self.mail\_recipients(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation))).
- If is\_inbound\_mail\_communcation.
  - Set cc from (cc − set((self.cc\_list() + self.to\_list()))).
- Set self.\_final\_cc from list of m for m drawn from cc where (m and m does not belong to Platform.STANDARD\_USERS).
  - Draw m from cc, keep a combination only if ((m and m does not belong to Platform.STANDARD\_USERS)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in m → m does not belong to Platform.STANDARD\_USERS.
- Return self.\_final\_cc.

**Methods declared on this owner** [get notification recipient](operations-006.md#op-8816c465b2d702), [get assignees](operations-007.md#op-34776eefaaa410), [filter thread notification disbled users](operations-007.md#op-9581ad50dcc78b), [mail recipients](operations-006.md#op-3f1e970b01df98).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L3729) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1080)

<a id="op-d0e3c685e8daf4"></a>
### Communication Email Mixin.get mail cc with displayname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_mail_carbon_copy_with_displayname`

**Inputs** self, is\_inbound\_mail\_communcation = false, include\_sender = false.

**Explicit results** list of self.get\_email\_with\_displayname(email) for email drawn from cc\_list where email.

**Local steps**

- Set cc\_list from self.mail\_cc(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation, include\_sender = include\_sender).
- Return list of self.get\_email\_with\_displayname(email) for email drawn from cc\_list where email.
  - Draw email from cc\_list, keep a combination only if (email).

**Methods declared on this owner** [mail cc](operations-006.md#op-84a26ca214b8ad), [get email with displayname](operations-006.md#op-7491f491fd2847).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L4519) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1070)

<a id="op-08feae944867e8"></a>
### Communication Email Mixin.mail bcc

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_blind_carbon_copy`

**Inputs** self, is\_inbound\_mail\_communcation = false.

**Explicit results** self.\_final\_bcc.

**Local steps**

- If hasattr(self, “\_final\_bcc”).
  - Return self.\_final\_bcc.
- Set bcc from set(self.bcc\_list()).
- If is\_inbound\_mail\_communcation.
  - Set bcc from (bcc − set(self.sender\_mailid)).
- Set bcc from (bcc − set(self.filter\_thread\_notification\_disbled\_users(bcc))).
- Set bcc from (bcc − set(self.mail\_recipients(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation))).
- If is\_inbound\_mail\_communcation.
  - Set bcc from (bcc − set((self.bcc\_list() + self.to\_list()))).
- Set self.\_final\_bcc from list of m for m drawn from bcc where m does not belong to Platform.STANDARD\_USERS.
  - Draw m from bcc, keep a combination only if (m does not belong to Platform.STANDARD\_USERS).
- Return self.\_final\_bcc.

**Methods declared on this owner** [filter thread notification disbled users](operations-007.md#op-9581ad50dcc78b), [mail recipients](operations-006.md#op-3f1e970b01df98).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L4667) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1079)

<a id="op-65662a29523b45"></a>
### Communication Email Mixin.get mail bcc with displayname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_mail_blind_carbon_copy_with_displayname`

**Inputs** self, is\_inbound\_mail\_communcation = false.

**Explicit results** list of self.get\_email\_with\_displayname(email) for email drawn from bcc\_list where email.

**Local steps**

- Set bcc\_list from self.mail\_bcc(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation).
- Return list of self.get\_email\_with\_displayname(email) for email drawn from bcc\_list where email.
  - Draw email from bcc\_list, keep a combination only if (email).

**Methods declared on this owner** [mail bcc](operations-006.md#op-08feae944867e8), [get email with displayname](operations-006.md#op-7491f491fd2847).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5067) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1069)

<a id="op-741f889ef35771"></a>
### Communication Email Mixin.mail sender

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_sender`

**Inputs** self.

**Explicit results** email\_account.email\_id · self.sender\_mailid.

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- If (not self.sender\_mailid and email\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sender\_mailid → email\_account.
  - Return email\_account.email\_id.
- Return self.sender\_mailid.

**Methods declared on this owner** [get outgoing email account](operations-007.md#op-905f124b7baa4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5194) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1082)
