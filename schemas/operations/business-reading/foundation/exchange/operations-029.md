# Integration and transport · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Receive

<a id="op-31d6c9a8b75565"></a>
### Email.get payload

`operation_foundation_email_receive_business_behavior_email_get_payload`

**Inputs** self, part.

**Explicit results** str(part.get\_payload(decode = true), str(charset), “ignore”) · str(part.get\_payload(decode = true), ALTERNATE\_CHARSET\_MAP.get(charset, “utf-8”), “ignore”) · part.get\_payload().

**Local steps**

- Set charset from self.get\_charset(part).
- Attempt the following.
  - Return str(part.get\_payload(decode = true), str(charset), “ignore”).
- On failure (LookupError).
  - Attempt the following.
    - Return str(part.get\_payload(decode = true), ALTERNATE\_CHARSET\_MAP.get(charset, “utf-8”), “ignore”).
  - On failure (Exception).
    - Return part.get\_payload().

**Methods declared on this owner** [get charset](operations-028.md#op-030f2da3f7c19d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L6220) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1096) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1528)

<a id="op-d18becd8129571"></a>
### Email.get attachment

`operation_foundation_email_receive_business_behavior_email_get_attachment`

**Inputs** self, part.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set fcontent from part.get\_payload(decode = true).
- If not fcontent.
  - Return no value.
- Set email\_account from getattr(self, “email\_account”, no value).
- Set attachment\_limit from cint(email\_account.attachment\_limit) when email\_account, otherwise 0.
  - Value choice on email\_account — true gives cint(email\_account.attachment\_limit), false gives 0.
- If (attachment\_limit and len(fcontent) &gt; ((attachment\_limit × 1024) × 1024)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attachment\_limit → len(fcontent) &gt; ((attachment\_limit × 1024) × 1024).
  - Return no value.
- Set content\_type from part.get\_content\_type().
- Set fname from part.get\_filename().
- If fname.
  - Attempt the following.
    - Set fname from fname.replace(whitespace '\\n', one space).replace(whitespace '\\r', empty text).
    - Set fname from cstr(decode\_header(fname) at 0 at 0).
  - On failure (Exception).
    - Set fname from get\_random\_filename(content\_type = content\_type).
- Otherwise.
  - Set fname from get\_random\_filename(content\_type = content\_type).
- While fname belongs to self.cid\_map.
  - Set fname from get\_random\_filename(content\_type = content\_type).
- Evaluate self.attachments.append(mapping(“content\_type” → content\_type, “fname” → fname, “fcontent” → fcontent)).
- Set cid from (cstr(part.get(“Content-Id”)) or empty text).strip(“&gt;&lt;”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(part.get(“Content-Id”)) → empty text.
- If cid.
  - Set self.cid\_map at fname from cid.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “email\_account”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L6472) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1094) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1526)

<a id="op-398cd9be45f06a"></a>
### Email.save attachments in doc

`operation_foundation_email_receive_business_behavior_email_save_attachments_in_record`

**Inputs** self, doc.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → unquote(attachment at “fname”), “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …) via get\_doc.

**State and service calls** call save on \_file.

**Explicit results** saved\_attachments.

**Local steps**

- Set saved\_attachments from list().
- For each attachment in self.attachments.
  - Attempt the following.
    - Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → unquote(attachment at “fname”), “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …)).
    - Evaluate \_file.save().
    - Evaluate saved\_attachments.append(\_file).
    - If attachment at “fname” belongs to self.cid\_map.
      - Set self.cid\_map at \_file.name from self.cid\_map at attachment at “fname”.
  - On failure (MaxFileSizeReachedError).
    - Take no action here.
  - On failure (Platform.FileAlreadyAttachedException).
    - Take no action here.
  - On failure (Platform.DuplicateEntryError).
    - Take no action here.
  - On failure (Platform.ValidationError).
    - Evaluate Platform.log\_error(translated “Unable to save email attachment {0}”.format(attachment at “fname”), reference\_doctype = doc.doctype, reference\_name = doc.name).
- Return saved\_attachments.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L79) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1535)

<a id="op-c86385101d8a8e"></a>
### Email.get thread id

`operation_foundation_email_receive_business_behavior_email_get_thread_identifier`

**Inputs** self.

**Explicit results** ((l and l at 0) or no value).

**Local steps**

- Set l from THREAD\_ID\_PATTERN.findall(self.subject).
- Return ((l and l at 0) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (l and l at 0) → no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in l → l at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L7609) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1529)

<a id="op-c48f426e2c68fc"></a>
### Email.is reply

`operation_foundation_email_receive_business_behavior_email_is_reply`

**Inputs** self.

**Explicit results** bool(self.in\_reply\_to).

**Local steps**

- Return bool(self.in\_reply\_to).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L7706) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1532)

<a id="op-011ca18c4a8a12"></a>
### Inbound Mail.initialize

`operation_foundation_email_receive_business_behavior_inbound_mail_initialize`

**Inputs** self, content, email\_account, uid = no value, seen\_status = no value, append\_to = no value.

**Local steps**

- Set self.email\_account from email\_account.
- Set self.uid from (uid or negative 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uid → negative 1.
- Set self.append\_to from append\_to.
- Set self.seen\_status from (seen\_status or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in seen\_status → 0.
- Evaluate super().\_\_init\_\_(content).
- Set self.\_parent\_email\_queue from no value.
- Set self.\_parent\_communication from no value.
- Set self.\_reference\_document from no value.
- Set self.flags from Platform.\_dict().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1568)

<a id="op-718c78847274da"></a>
### Inbound Mail.get content

`operation_foundation_email_receive_business_behavior_inbound_mail_get_content`

**Inputs** self.

**Explicit results** clean\_email\_html(self.content).

**Local steps**

- If self.content\_type equals “text/html”.
  - Return clean\_email\_html(self.content).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L281) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1561)

<a id="op-e6755e2f737e7a"></a>
### Inbound Mail.process

`operation_foundation_email_receive_business_behavior_inbound_mail_process`

**Inputs** self.

**Explicit results** communication · self.\_build\_communication\_doc().

**Explicit failure paths** SentEmailInInboxError.

**Local steps**

- If (self.is\_sender\_same\_as\_receiver() and not self.is\_reply()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_sender\_same\_as\_receiver() → not self.is\_reply().
  - If Platform.in\_test.
    - Evaluate print(“WARN: Cannot pull email. Sender same as recipient inbox”).
  - Raise SentEmailInInboxError.
- Set communication from self.is\_exist\_in\_system().
- If communication.
  - Evaluate communication.update\_db(uid = self.uid).
  - Set data from self.as\_dict().
  - If (data.get(“bcc”) and not communication.bcc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“bcc”) → not communication.bcc.
    - Evaluate communication.update\_db(bcc = data.get(“bcc”)).
  - Evaluate communication.reload().
  - Return communication.
- Set self.flags.is\_new\_communication from true.
- Return self.\_build\_communication\_doc().

**Methods declared on this owner** [is sender same as receiver](operations-029.md#op-7df3854955c12f), [is exist in system](operations-029.md#op-c768401715b25c), [as dict](operations-030.md#op-c4f865a01387fa), [build communication doc](operations-029.md#op-d386dd9e6df81e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L363) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1576)

<a id="op-d386dd9e6df81e"></a>
### Inbound Mail.build communication doc

`operation_foundation_email_receive_business_behavior_inbound_mail_build_communication_record`

**Inputs** self.

**Record and data access** resolve a document from data via get\_doc.

**State and service calls** call insert on communication · call save on communication.

**Explicit results** communication.

**Local steps**

- Set data from self.as\_dict().
- Set data at “doctype” from “Communication”.
- If self.parent\_communication().
  - Set data at “in\_reply\_to” from self.parent\_communication().name.
- Set append\_to from self.append\_to when self.email\_account.use\_imap, otherwise self.email\_account.append\_to.
  - Value choice on self.email\_account.use\_imap — true gives self.append\_to, false gives self.email\_account.append\_to.
- If self.reference\_document().
  - Set data at “reference\_doctype” from self.reference\_document().doctype.
  - Set data at “reference\_name” from self.reference\_document().name.
- Otherwise.
  - If (append\_to and append\_to differs from “Communication”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in append\_to → append\_to differs from “Communication”.
    - Set reference\_name from self.\_create\_reference\_document(append\_to).
    - If reference\_name.
      - Set data at “reference\_doctype” from append\_to.
      - Set data at “reference\_name” from reference\_name.
- If self.is\_notification().
  - Set data at “unread\_notification\_sent” from 1.
- If self.seen\_status.
  - Set data at “\_seen” from json.dumps(self.get\_users\_linked\_to\_account(self.email\_account)).
- Set communication from Platform.get\_doc(data).
- Set communication.flags.in\_receive from true.
- Evaluate communication.insert(ignore\_permissions = true).
- Evaluate communication.reload().
- Set communication.\_attachments from self.save\_attachments\_in\_doc(communication).
- Set communication.content from sanitize\_html(self.replace\_inline\_images(communication.\_attachments)).
- Evaluate communication.save().
- Return communication.

**Methods declared on this owner** [as dict](operations-030.md#op-c4f865a01387fa), [parent communication](operations-029.md#op-58aa0b03efa997), [reference document](operations-029.md#op-a6e370d4eb7fe8), [create reference document](operations-029.md#op-fff7ec69735267), [is notification](operations-029.md#op-cf7504d606cd7b), [get users linked to account](operations-029.md#op-4412b4448ecfc2), [replace inline images](operations-029.md#op-91620b219fc233).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L83) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1558)

<a id="op-91620b219fc233"></a>
### Inbound Mail.replace inline images

`operation_foundation_email_receive_business_behavior_inbound_mail_replace_inline_images`

**Inputs** self, attachments.

**Explicit results** content.

**Local steps**

- Set content from self.content.
- For each file in attachments.
  - If self.cid\_map.get(file.name).
    - Set content from content.replace(formatted text cid:{self.cid\_map at file.name}, file.unique\_url).
- Return content.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L1565) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1578)

<a id="op-cf7504d606cd7b"></a>
### Inbound Mail.is notification

`operation_foundation_email_receive_business_behavior_inbound_mail_is_notification`

**Inputs** self.

**Explicit results** (isnotification and “notification” belongs to isnotification).

**Local steps**

- Set isnotification from self.mail.get(“isnotification”).
- Return (isnotification and “notification” belongs to isnotification).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isnotification → “notification” belongs to isnotification.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L1748) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1570)

<a id="op-c768401715b25c"></a>
### Inbound Mail.is exist in system

`operation_foundation_email_receive_business_behavior_inbound_mail_is_exist_in_system`

**Inputs** self.

**Explicit results** no value · Communication.find\_one\_by\_filters(message\_id = self.message\_id, email\_account = self.email\_account.name, sent\_or\_received = “Received”, order\_by = “creation DESC”).

**Local steps**

- Bind dependencies Communication.
- If not self.message\_id.
  - Return no value.
- Return Communication.find\_one\_by\_filters(message\_id = self.message\_id, email\_account = self.email\_account.name, sent\_or\_received = “Received”, order\_by = “creation DESC”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L1846) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1569)

<a id="op-7df3854955c12f"></a>
### Inbound Mail.is sender same as receiver

`operation_foundation_email_receive_business_behavior_inbound_mail_is_sender_same_as_receiver`

**Inputs** self.

**Explicit results** self.from\_email equals self.email\_account.email\_id.

**Local steps**

- Return self.from\_email equals self.email\_account.email\_id.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L1980) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1572)

<a id="op-1d8e611fe0b760"></a>
### Inbound Mail.is reply to system sent mail

`operation_foundation_email_receive_business_behavior_inbound_mail_is_reply_to_system_sent_mail`

**Inputs** self.

**Explicit results** (self.is\_reply() and Platform.local.site belongs to self.in\_reply\_to).

**Local steps**

- Return (self.is\_reply() and Platform.local.site belongs to self.in\_reply\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_reply() → Platform.local.site belongs to self.in\_reply\_to.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L2041) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1571)

<a id="op-d44a78ff7f6cd9"></a>
### Inbound Mail.parent email queue

`operation_foundation_email_receive_business_behavior_inbound_mail_parent_email_queue`

**Inputs** self.

**Explicit results** self.\_parent\_email\_queue.

**Local steps**

- Bind dependencies EmailQueue.
- If self.\_parent\_email\_queue is distinct from no value.
  - Return self.\_parent\_email\_queue.
- Set parent\_email\_queue from empty text.
- If self.is\_reply\_to\_system\_sent\_mail().
  - Set parent\_email\_queue from EmailQueue.find\_one\_by\_filters(message\_id = self.in\_reply\_to).
- Set self.\_parent\_email\_queue from (parent\_email\_queue or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_email\_queue → empty text.
- Return self.\_parent\_email\_queue.

**Methods declared on this owner** [is reply to system sent mail](operations-029.md#op-1d8e611fe0b760).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L2124) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1575)

<a id="op-58aa0b03efa997"></a>
### Inbound Mail.parent communication

`operation_foundation_email_receive_business_behavior_inbound_mail_parent_communication`

**Inputs** self.

**Explicit results** self.\_parent\_communication · empty text.

**Local steps**

- Bind dependencies Communication.
- If self.\_parent\_communication is distinct from no value.
  - Return self.\_parent\_communication.
- If not self.is\_reply().
  - Return empty text.
- Set communication from Communication.find\_one\_by\_filters(message\_id = self.in\_reply\_to, order\_by = “creation DESC”).
- If not communication.
  - If (self.parent\_email\_queue() and self.parent\_email\_queue().communication).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.parent\_email\_queue() → self.parent\_email\_queue().communication.
    - Set communication from Communication.find(self.parent\_email\_queue().communication, ignore\_error = true).
  - Otherwise.
    - Set reference from self.in\_reply\_to.
    - If “@” belongs to self.in\_reply\_to.
      - Set tuple(reference, \_) from self.in\_reply\_to.split(“@”, 1).
    - Set communication from Communication.find(reference, ignore\_error = true).
- Set self.\_parent\_communication from (communication or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in communication → empty text.
- Return self.\_parent\_communication.

**Methods declared on this owner** [parent email queue](operations-029.md#op-d44a78ff7f6cd9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L2314) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1574)

<a id="op-a6e370d4eb7fe8"></a>
### Inbound Mail.reference document

`operation_foundation_email_receive_business_behavior_inbound_mail_reference_document`

**Inputs** self.

**Explicit results** self.\_reference\_document.

**Local steps**

- If self.\_reference\_document is distinct from no value.
  - Return self.\_reference\_document.
- Set reference\_document from empty text.
- Set parent\_email\_queue from self.parent\_email\_queue().
- Set parent\_communication from self.parent\_communication().
- Set parent from no value.
- If (parent\_email\_queue and parent\_email\_queue.reference\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_email\_queue → parent\_email\_queue.reference\_doctype.
  - Set parent from parent\_email\_queue.
- Otherwise.
  - If (parent\_communication and parent\_communication.reference\_doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_communication → parent\_communication.reference\_doctype.
    - Set parent from parent\_communication.
- If parent.
  - Set tuple(reference\_doctype, reference\_name) from tuple(parent.reference\_doctype, parent.reference\_name).
  - Set reference\_document from self.get\_doc(reference\_doctype, reference\_name, ignore\_error = true).
- If (not reference\_document and self.email\_account.append\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not reference\_document → self.email\_account.append\_to.
  - Set reference\_document from self.match\_record\_by\_subject\_and\_sender(self.email\_account.append\_to).
- If (not reference\_document and self.is\_reply\_to\_system\_sent\_mail()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not reference\_document → self.is\_reply\_to\_system\_sent\_mail().
  - Set reference\_document from parent\_communication.
- Set self.\_reference\_document from (reference\_document or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_document → empty text.
- Return self.\_reference\_document.

**Methods declared on this owner** [parent email queue](operations-029.md#op-d44a78ff7f6cd9), [parent communication](operations-029.md#op-58aa0b03efa997), [get doc](operations-029.md#op-0b566bd1252c20), [match record by subject and sender](operations-029.md#op-aa894cb3852ed7), [is reply to system sent mail](operations-029.md#op-1d8e611fe0b760).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L2755) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1577)

<a id="op-5f82e3fb967977"></a>
### Inbound Mail.get reference name from subject

`operation_foundation_email_receive_business_behavior_inbound_mail_get_reference_name_from_subject`

**Inputs** self.

**Explicit results** self.subject.rsplit(“#”, 1) at negative 1.strip(“ ()”).

**Local steps**

- Return self.subject.rsplit(“#”, 1) at negative 1.strip(“ ()”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L3228) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1565)

<a id="op-aa894cb3852ed7"></a>
### Inbound Mail.match record by subject and sender

`operation_foundation_email_receive_business_behavior_inbound_mail_match_record_by_subject_and_sender`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_value · read self.email\_account.append\_to via get\_value.

**Explicit results** no value · record.

**Local steps**

- Set name from self.get\_reference\_name\_from\_subject().
- Set email\_fields from self.get\_email\_fields(doctype).
- Set sender\_is\_system\_user from bool((self.from\_email and is\_system\_user(self.from\_email))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_email → is\_system\_user(self.from\_email).
- If (email\_fields.sender\_field and not sender\_is\_system\_user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_fields.sender\_field → not sender\_is\_system\_user.
  - Set name from Platform.db.get\_value(doctype, mapping(“name” → name, email\_fields.sender\_field → self.from\_email)).
- Set record from self.get\_doc(doctype, name, ignore\_error = true) when name, otherwise no value.
  - Value choice on name — true gives self.get\_doc(doctype, name, ignore\_error = true), false gives no value.
- If not record.
  - If not email\_fields.subject\_field.
    - Return no value.
  - Set subject from self.clean\_subject(self.subject).
  - Set filters from mapping(email\_fields.subject\_field → tuple(“like”, formatted text %{subject}%), “creation” → tuple(“&gt;”, self.get\_relative\_dt(days = negative 60))).
  - If (email\_fields.sender\_field and not (len(subject) &gt; 10 and sender\_is\_system\_user)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_fields.sender\_field → not (len(subject) &gt; 10 and sender\_is\_system\_user).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(subject) &gt; 10 → sender\_is\_system\_user.
    - Set filters at email\_fields.sender\_field from self.from\_email.
  - Set name from Platform.db.get\_value(self.email\_account.append\_to, filters = filters).
  - Set record from self.get\_doc(doctype, name, ignore\_error = true) when name, otherwise no value.
    - Value choice on name — true gives self.get\_doc(doctype, name, ignore\_error = true), false gives no value.
- Return record.

**Methods declared on this owner** [get reference name from subject](operations-029.md#op-5f82e3fb967977), [get email fields](operations-030.md#op-62709fdc724efa), [get doc](operations-029.md#op-0b566bd1252c20), [clean subject](operations-029.md#op-e21a3f5587298f), [get relative dt](operations-029.md#op-58975e77a985f6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L85) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1573)

<a id="op-fff7ec69735267"></a>
### Inbound Mail.create reference document

`operation_foundation_email_receive_business_behavior_inbound_mail_create_reference_document`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_value.

**State and service calls** request new\_doc for doctype · call insert on parent.

**Explicit results** parent.name · Platform.db.get\_value(doctype, mapping(email\_fields.sender\_field → self.from\_email)).

**Local steps**

- Set parent from Platform.new\_doc(doctype).
- Set email\_fields from self.get\_email\_fields(doctype).
- If email\_fields.subject\_field.
  - Evaluate parent.set(email\_fields.subject\_field, Platform.as\_unicode(self.subject) at slice no value to 140).
- If email\_fields.sender\_field.
  - Evaluate parent.set(email\_fields.sender\_field, Platform.as\_unicode(self.from\_email)).
- If email\_fields.sender\_name\_field.
  - Evaluate parent.set(email\_fields.sender\_name\_field, Platform.as\_unicode(self.from\_real\_name)).
- If email\_fields.recipient\_account\_field.
  - Evaluate parent.set(email\_fields.recipient\_account\_field, self.email\_account.name).
- Set parent.flags.ignore\_mandatory from true.
- Attempt the following.
  - Evaluate parent.insert(ignore\_permissions = true).
  - Return parent.name.
- On failure (Platform.DuplicateEntryError).
  - Return Platform.db.get\_value(doctype, mapping(email\_fields.sender\_field → self.from\_email)).

**Methods declared on this owner** [get email fields](operations-030.md#op-62709fdc724efa).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L3874) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1560)

<a id="op-0b566bd1252c20"></a>
### Inbound Mail.get doc

`operation_foundation_email_receive_business_behavior_inbound_mail_get_record`

**Inputs** doctype, docname, ignore\_error = false.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** Platform.get\_doc(doctype, docname) · no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Return Platform.get\_doc(doctype, docname).
- On failure (Platform.DoesNotExistError).
  - If ignore\_error.
    - Return no value.
  - Propagate the active failure.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L4377) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1564)

<a id="op-58975e77a985f6"></a>
### Inbound Mail.get relative dt

`operation_foundation_email_receive_business_behavior_inbound_mail_get_relative_record_type`

**Inputs** days.

**Wrappers, in declaration order** staticmethod.

**Explicit results** add\_days(get\_datetime(), days).

**Local steps**

- Return add\_days(get\_datetime(), days).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L4509) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1566)

<a id="op-4412b4448ecfc2"></a>
### Inbound Mail.get users linked to account

`operation_foundation_email_receive_business_behavior_inbound_mail_get_users_linked_to_account`

**Inputs** email\_account.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “User Email” via get\_all.

**Explicit results** list(set of user.get(“parent”) for user drawn from users).

**Local steps**

- Set users from Platform.get\_all(“User Email”, filters = mapping(“email\_account” → email\_account.name), fields = list(“parent”)).
- Return list(set of user.get(“parent”) for user drawn from users).
  - Draw user from users.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0237.json#L4579) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1567)

<a id="op-e21a3f5587298f"></a>
### Inbound Mail.clean subject

`operation_foundation_email_receive_business_behavior_inbound_mail_clean_subject`

**Inputs** subject.

**Wrappers, in declaration order** staticmethod.

**Explicit results** Platform.as\_unicode(strip(re.sub(regex, empty text, subject, count = 0, flags = re.IGNORECASE))).

**Local steps**

- Set regex from “^(\\s\*(fw\|fwd\|wg)\\b&#91;^:&#93;\*:)?(\\s\*(re\|aw)\\b&#91;^:&#93;\*:\\s\*)\*”.
- Return Platform.as\_unicode(strip(re.sub(regex, empty text, subject, count = 0, flags = re.IGNORECASE))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L84) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1559)
