# Record lifecycle and persistence · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Comment

[Record definition](../../../../data/record-types/comment.json)

<a id="op-3cbc10ff8dc8df"></a>
### Comment.on update

`operation_foundation_core_record_definitions_comment_business_behavior_comment_on_update`

**Inputs** self.

**Local steps**

- Evaluate update\_comment\_in\_doc(self).
- If not self.is\_new().
  - Evaluate self.notify\_change(“update”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify change](operations-004.md#op-e699ccfaaa847c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4094) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L971)

<a id="op-a6d76a4c1c6b1b"></a>
### Comment.on trash

`operation_foundation_core_record_definitions_comment_business_behavior_comment_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_comment\_from\_cache().
- Evaluate self.notify\_change(“delete”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove comment from cache](operations-004.md#op-5cf462930018b4), [notify change](operations-004.md#op-e699ccfaaa847c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4202) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L970)

<a id="op-e699ccfaaa847c"></a>
### Comment.notify change

`operation_foundation_core_record_definitions_comment_business_behavior_comment_notify_change`

**Inputs** self, action.

**State and service calls** publish realtime with “docinfo\_update”.

**Explicit results** no value.

**Local steps**

- Set key\_map from mapping(“Like” → “like\_logs”, “Assigned” → “assignment\_logs”, “Assignment Completed” → “assignment\_logs”, “Comment” → “comments”, …).
- Set key from key\_map.get(self.comment\_type).
- If not key.
  - Return no value.
- Evaluate Platform.publish\_realtime(“docinfo\_update”, mapping(“doc” → self.as\_dict(), “key” → key, “action” → action), doctype = self.reference\_doctype, docname = self.reference\_name, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“docinfo\_update”, mapping(“doc” → self.as\_dict(), “key” → key, “action” → action), doctype = self.reference\_doctype, docname = self.reference\_name, after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4283) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L969)

<a id="op-5cf462930018b4"></a>
### Comment.remove comment from cache

`operation_foundation_core_record_definitions_comment_business_behavior_comment_remove_comment_from_cache`

**Inputs** self.

**Local steps**

- Set \_comments from get\_comments\_from\_parent(self).
- For each c in list(\_comments).
  - If c.get(“name”) equals self.name.
    - Evaluate \_comments.remove(c).
- Evaluate update\_comments\_in\_parent(self.reference\_doctype, self.reference\_name, \_comments).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4582) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L972)

<a id="op-949116eb10ca72"></a>
### On doctype update

`operation_foundation_core_record_definitions_comment_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Comment”.

**Local steps**

- Evaluate Platform.db.add\_index(“Comment”, list(“reference\_doctype”, “reference\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4777) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L979)

<a id="op-06ca094551d9e9"></a>
### Has permission

`operation_foundation_core_record_definitions_comment_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L4855) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L978)

<a id="op-ffdac423824592"></a>
### Get permission query conditions

`operation_foundation_core_record_definitions_comment_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L5343) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L977)

<a id="op-36077e27bed20a"></a>
### Get document comments

`operation_foundation_core_record_definitions_comment_business_behavior_get_document_comments`

**Inputs** reference\_doctype, reference\_name, fields, comment\_types = no value, extra\_filters = no value, user = no value, remaining named values kwargs.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Comment” via get\_all.

**Explicit results** list() · Platform.get\_all(“Comment”, fields = fields, filters = filters, expanded names kwargs).

**Local steps**

- Set filters from list(list(“reference\_doctype”, “=”, reference\_doctype), list(“reference\_name”, “=”, reference\_name), expanded (extra\_filters or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extra\_filters → list().
- If comment\_types is identical to no value.
  - Set comment\_types from Platform.get\_all(“Comment”, filters = filters, pluck = “comment\_type”, distinct = true).
- Bind local operation permitted for subsequent calls.
- If not allowed bound to list of comment\_type for comment\_type drawn from comment\_types where permitted(comment\_type).
  - Draw comment\_type from comment\_types, keep a combination only if (permitted(comment\_type)).
  - Return list().
- Evaluate filters.append(list(“comment\_type”, “in”, allowed)).
- Return Platform.get\_all(“Comment”, fields = fields, filters = filters, expanded names kwargs).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L5622) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L975)

<a id="op-81ffa4965dca68"></a>
### Get document comments.permitted

`operation_foundation_core_record_definitions_comment_business_behavior_get_document_comments_permitted`

**Inputs** comment\_type.

**Declared result** bool.

**Explicit results** has\_controller\_permissions(probe, “read”, user = user).

**Local steps**

- Set probe from Platform.\_dict(doctype = “Comment”, name = no value, reference\_doctype = reference\_doctype, reference\_name = reference\_name, …).
- Return has\_controller\_permissions(probe, “read”, user = user).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L6263) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L976)

<a id="op-429b4555440801"></a>
### Update comment in doc

`operation_foundation_core_record_definitions_comment_business_behavior_update_comment_in_record`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If (doc.doctype equals “Comment” and doc.comment\_type differs from “Comment”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Comment” → doc.comment\_type differs from “Comment”.
  - Return no value.
- If (doc.reference\_doctype and doc.reference\_name and doc.content).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name → doc.content.
  - Set \_comments from get\_comments\_from\_parent(doc).
  - If any(generator of c.get(“name”) equals doc.name for c drawn from \_comments).
    - Draw c from \_comments.
    - Return no value.
  - Evaluate \_comments.append(mapping(“name” → doc.name)).
  - Evaluate update\_comments\_in\_parent(doc.reference\_doctype, doc.reference\_name, \_comments).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L160) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L980)

<a id="op-52d33dfe3a7604"></a>
### Get comments from parent

`operation_foundation_core_record_definitions_comment_business_behavior_get_comments_from_parent`

**Inputs** doc.

**Record and data access** read doc.reference\_doctype via get\_value.

**Explicit results** json.loads(\_comments) · list().

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - If is\_virtual\_doctype(doc.reference\_doctype).
    - Set \_comments from “&#91;&#93;”.
  - Otherwise.
    - Set \_comments from (Platform.db.get\_value(doc.reference\_doctype, doc.reference\_name, “\_comments”) or “&#91;&#93;”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(doc.reference\_doctype, doc.reference\_name, “\_comments”) → “&#91;&#93;”.
- On failure (Exception) bound to e.
  - If Platform.db.is\_missing\_table\_or\_column(e).
    - Set \_comments from “&#91;&#93;”.
  - Otherwise.
    - Propagate the active failure.
- Attempt the following.
  - Return json.loads(\_comments).
- On failure (ValueError).
  - Return list().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L7389) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L974)

<a id="op-f09dbff6c6ca61"></a>
### Update comments in parent

`operation_foundation_core_record_definitions_comment_business_behavior_update_comments_in_parent`

**Inputs** reference\_doctype, reference\_name, \_comments.

**Record and data access** read “DocType” via get\_value · read reference\_doctype via get\_cached\_value.

**State and service calls** request set\_value on reference\_doctype.

**Explicit results** no value.

**Explicit failure paths** Platform.DataTooLongException · propagate active failure.

**Local steps**

- If (not reference\_doctype or not reference\_name or Platform.db.get\_value(“DocType”, reference\_doctype, “issingle”) or is\_virtual\_doctype(reference\_doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reference\_doctype → not reference\_name → Platform.db.get\_value(“DocType”, reference\_doctype, “issingle”) → is\_virtual\_doctype(reference\_doctype).
  - Return no value.
- Set \_comments from list of mapping(“name” → c at “name”) for c drawn from \_comments at slice negative 100 to no value where c.get(“name”).
  - Draw c from \_comments at slice negative 100 to no value, keep a combination only if (c.get(“name”)).
- Attempt the following.
  - Evaluate Platform.db.set\_value(reference\_doctype, reference\_name, “\_comments”, json.dumps(\_comments), update\_modified = false).
- On failure (Exception) bound to e.
  - If (Platform.db.is\_missing\_column(e) and getattr(Platform.local, “request”, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.is\_missing\_column(e) → getattr(Platform.local, “request”, no value).
    - Take no action here.
  - Otherwise.
    - If Platform.db.is\_data\_too\_long(e).
      - Raise Platform.DataTooLongException.
    - Otherwise.
      - Propagate the active failure.
- When the protected block completes normally.
  - If Platform.flags.in\_patch.
    - Return no value.
  - If route bound to Platform.get\_cached\_value(reference\_doctype, reference\_name, “route”).
    - Evaluate clear\_cache(route).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value) · configured or stored value from Platform.get\_cached\_value(reference\_doctype, reference\_name, “route”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L161) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L981)

## Record · Communication

[Record definition](../../../../data/record-types/communication.json)

<a id="op-d7110fea1ddc8b"></a>
### Communication.onload

`operation_foundation_core_record_definitions_communication_business_behavior_communication_onload`

**Inputs** self.

**Record and data access** read “Email Flag Queue” via get\_value · resolve a document from mapping(“doctype” → “Email Flag Queue”, “action” → “Read”, “communication” → self.name, “uid” → self.uid, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Flag Queue”, “action” → “Read”, “communication” → self.name, “uid” → self.uid, …)) · commit.

**Explicit results** no value.

**Local steps**

- If (self.communication\_type equals “Communication” and self.communication\_medium equals “Email” and self.sent\_or\_received equals “Received” and self.uid and self.uid differs from negative 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.communication\_type equals “Communication” → self.communication\_medium equals “Email” → self.sent\_or\_received equals “Received” → self.uid → self.uid differs from negative 1.
  - Set email\_flag\_queue from Platform.db.get\_value(“Email Flag Queue”, mapping(“communication” → self.name, “is\_completed” → 0)).
  - If email\_flag\_queue.
    - Return no value.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Flag Queue”, “action” → “Read”, “communication” → self.name, “uid” → self.uid, …)).insert(ignore\_permissions = true).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L712) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1026)

<a id="op-934e8553331cdd"></a>
### Communication.validate

`operation_foundation_core_record_definitions_communication_business_behavior_communication_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_reference().
- If not self.user.
  - Set self.user from Platform.session.user.
- If not self.subject.
  - Set self.subject from strip\_html((self.content or empty text) at slice no value to 141).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.content → empty text.
- If not self.sent\_or\_received.
  - Set self.seen from 1.
  - Set self.sent\_or\_received from “Sent”.
- If not self.send\_after.
  - Set self.send\_after from no value.
- Evaluate validate\_email(self).
- If self.communication\_medium equals “Email”.
  - Evaluate self.parse\_email\_for\_timeline\_links().
  - Evaluate self.set\_timeline\_links().
  - Evaluate self.deduplicate\_timeline\_links().
- Evaluate self.set\_sender\_full\_name().
- If self.is\_new().
  - Evaluate self.set\_status().
  - Evaluate self.mark\_email\_as\_spam().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reference](operations-004.md#op-804b1e3d16d07a), [parse email for timeline links](operations-005.md#op-f029bdeb87ab66), [set timeline links](operations-005.md#op-7634b62db8c026), [deduplicate timeline links](operations-005.md#op-58fb4e810c916d), [set sender full name](operations-005.md#op-097d60dc3cc74d), [set status](operations-005.md#op-60e47ba317226d), [mark email as spam](operations-005.md#op-5fbb71fa2088d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L1121) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1037)

<a id="op-804b1e3d16d07a"></a>
### Communication.validate reference

`operation_foundation_core_record_definitions_communication_business_behavior_communication_validate_reference`

**Inputs** self.

**Record and data access** read self.reference\_doctype via get\_value.

**Explicit failure paths** validation helper — translated “Cannot create a {0} against a child document: {1}”.format(translated self.communication\_type, translated self.reference\_doctype) · validation helper with Platform.CircularLinkingError — translated “Please make sure the Reference Communication Docs are not circularly linked.”.

**Local steps**

- If (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - If not self.reference\_owner.
    - Set self.reference\_owner from Platform.db.get\_value(self.reference\_doctype, self.reference\_name, “owner”).
  - If Platform.get\_meta(self.reference\_doctype).istable.
    - Call the validation error handler Platform.throw(translated “Cannot create a {0} against a child document: {1}”.format(translated self.communication\_type, translated self.reference\_doctype)).
  - If self.reference\_doctype equals “Communication”.
    - Set circular\_linking from false.
    - Set doc from get\_parent\_doc(self).
    - While doc.reference\_doctype equals “Communication”.
      - If get\_parent\_doc(doc).name equals self.name.
        - Set circular\_linking from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set doc from get\_parent\_doc(doc).
    - If circular\_linking.
      - Call the validation error handler Platform.throw(translated “Please make sure the Reference Communication Docs are not circularly linked.”, Platform.CircularLinkingError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L1569) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1038)

<a id="op-6248d96c1919b2"></a>
### Communication.after insert

`operation_foundation_core_record_definitions_communication_business_behavior_communication_after_insert`

**Inputs** self.

**State and service calls** request set\_value on “Communication”.

**Explicit results** no value.

**Local steps**

- If not (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Return no value.
- If (self.reference\_doctype equals “Communication” and self.sent\_or\_received equals “Sent”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype equals “Communication” → self.sent\_or\_received equals “Sent”.
  - Evaluate Platform.db.set\_value(“Communication”, self.reference\_name, “status”, “Replied”).
- Evaluate self.notify\_change(“add”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify change](operations-005.md#op-69fb288c50e3f0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L2078) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1012)

<a id="op-3c9399eed12a28"></a>
### Communication.set signature in email content

`operation_foundation_core_record_definitions_communication_business_behavior_communication_set_signature_in_email_content`

**Inputs** self.

**Record and data access** read “User” via get\_value · read “Email Account” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.content.
  - Return no value.
- Set soup from BeautifulSoup(self.content, “html.parser”).
- Set email\_body from soup.find(“div”, mapping(“class” → “ql-editor read-mode”)).
- If not email\_body.
  - Return no value.
- Set user\_email\_signature from Platform.db.get\_value(“User”, self.sender, “email\_signature”) when self.sender, otherwise no value.
  - Value choice on self.sender — true gives Platform.db.get\_value(“User”, self.sender, “email\_signature”), false gives no value.
- Set signature from (user\_email\_signature or Platform.db.get\_value(“Email Account”, mapping(“default\_outgoing” → 1, “add\_signature” → 1), “signature”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_email\_signature → Platform.db.get\_value(“Email Account”, mapping(“default\_outgoing” → 1, “add\_signature” → 1), “signature”).
- If not signature.
  - Return no value.
- Set soup from BeautifulSoup(signature, “html.parser”).
- Set html\_signature from soup.find(“div”, mapping(“class” → “ql-editor read-mode”)).
- Set \_signature from no value.
- If html\_signature.
  - Set \_signature from html\_signature.encode\_contents().
- If (cstr(\_signature) or signature) does not belong to self.content.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(\_signature) → signature.
  - Set self.content from formatted text {self.content}&lt;/p&gt;&lt;br&gt;&lt;p class="signature"&gt;{signature}.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L2283) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1032)

<a id="op-7b56ac2c6e0c13"></a>
### Communication.before save

`operation_foundation_core_record_definitions_communication_business_behavior_communication_before_save`

**Inputs** self.

**Local steps**

- If not self.flags.skip\_add\_signature.
  - Evaluate self.set\_signature\_in\_email\_content().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set signature in email content](operations-004.md#op-3c9399eed12a28).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L2845) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1013)

<a id="op-83941628a58270"></a>
### Communication.on update

`operation_foundation_core_record_definitions_communication_business_behavior_communication_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate update\_comment\_in\_doc(self).
- Set parent from get\_parent\_doc(self).
- If (method bound to getattr(parent, “on\_communication\_update”, no value) and callable(method)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method bound to getattr(parent, “on\_communication\_update”, no value) → callable(method).
  - Evaluate parent.on\_communication\_update(self).
  - Return no value.
- Evaluate update\_parent\_document\_on\_communication(self).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(parent, “on\_communication\_update”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L162) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1025)

<a id="op-0ebe8e8967e001"></a>
### Communication.on trash

`operation_foundation_core_record_definitions_communication_business_behavior_communication_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.notify\_change(“delete”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify change](operations-005.md#op-69fb288c50e3f0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3166) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1024)

<a id="op-ab97e8c78eb986"></a>
### Communication.sender mailid

`operation_foundation_core_record_definitions_communication_business_behavior_communication_sender_mailid`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** parse\_addr(self.sender) at 1 when self.sender, otherwise empty text.

**Local steps**

- Return parse\_addr(self.sender) at 1 when self.sender, otherwise empty text.
  - Value choice on self.sender — true gives parse\_addr(self.sender) at 1, false gives empty text.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3227) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1029)

<a id="op-5bca96592a414f"></a>
### Communication.get emails list

`operation_foundation_core_record_definitions_communication_business_behavior_communication_get_emails_list`

**Inputs** emails = no value, exclude\_displayname = false.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of email.lower() for email drawn from set of parse\_addr(email) at 1 for email drawn from emails where email · list of email for email drawn from set(emails) where email.

**Local steps**

- Set emails from split\_emails(emails) when isinstance(emails, str), otherwise (emails or list()).
  - Value choice on isinstance(emails, str) — true gives split\_emails(emails), false gives (emails or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in emails → list().
- If exclude\_displayname.
  - Return list of email.lower() for email drawn from set of parse\_addr(email) at 1 for email drawn from emails where email.
    - Draw email from set of parse\_addr(email) at 1 for email drawn from emails, keep a combination only if (email).
    - Draw email from emails.
- Return list of email for email drawn from set(emails) where email.
  - Draw email from set(emails), keep a combination only if (email).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3310) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1020)

<a id="op-4e9e7fe09ad56d"></a>
### Communication.to list

`operation_foundation_core_record_definitions_communication_business_behavior_communication_to_list`

**Inputs** self, exclude\_displayname = true.

**Explicit results** self.\_get\_emails\_list(self.recipients, exclude\_displayname = exclude\_displayname).

**Local steps**

- Return self.\_get\_emails\_list(self.recipients, exclude\_displayname = exclude\_displayname).

**Methods declared on this owner** [get emails list](operations-004.md#op-5bca96592a414f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3557) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1035)

<a id="op-9c73a41751a731"></a>
### Communication.cc list

`operation_foundation_core_record_definitions_communication_business_behavior_communication_carbon_copy_list`

**Inputs** self, exclude\_displayname = true.

**Explicit results** self.\_get\_emails\_list(self.cc, exclude\_displayname = exclude\_displayname).

**Local steps**

- Return self.\_get\_emails\_list(self.cc, exclude\_displayname = exclude\_displayname).

**Methods declared on this owner** [get emails list](operations-004.md#op-5bca96592a414f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3639) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1015)
