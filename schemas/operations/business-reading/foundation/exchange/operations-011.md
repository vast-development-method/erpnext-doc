# Integration and transport · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email account

[Record definition](../../../../data/record-types/email_account.json)

<a id="op-e398e36c3a7b86"></a>
### Email Account.handle bad emails

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_handle_bad_emails`

**Inputs** self, uid, raw, reason.

**Record and data access** resolve a document from mapping(“raw” → raw\_str, “uid” → uid, “reason” → reason, “message\_id” → message\_id, …) via get\_doc.

**State and service calls** call insert on unhandled\_email · commit.

**Local steps**

- If cint(self.use\_imap).
  - Bind dependencies email.
  - Attempt the following.
    - If isinstance(raw, bytes).
      - Set raw\_str from raw.decode(“ASCII”, “replace”).
      - Set mail from email.message\_from\_string(raw\_str).
    - Otherwise.
      - Set raw\_str from raw.encode(errors = “replace”).decode().
      - Set mail from email.message\_from\_string(raw\_str).
    - Set message\_id from mail.get(“Message-ID”).
  - On failure (Exception).
    - Set raw\_str from “can't be parsed”.
    - Set message\_id from “can't be parsed”.
  - Set unhandled\_email from Platform.get\_doc(mapping(“raw” → raw\_str, “uid” → uid, “reason” → reason, “message\_id” → message\_id, …)).
  - Evaluate unhandled\_email.insert(ignore\_permissions = true).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L321) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L9)

<a id="op-c3411a54fa9720"></a>
### Email Account.send auto reply

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_send_auto_reply`

**Inputs** self, communication, email.

**State and service calls** sendmail.

**Local steps**

- Bind dependencies set\_incoming\_outgoing\_accounts.
- If self.enable\_auto\_reply.
  - Evaluate set\_incoming\_outgoing\_accounts(communication).
  - Set unsubscribe\_message from ((self.send\_unsubscribe\_message and translated “Leave this conversation”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.send\_unsubscribe\_message and translated “Leave this conversation”) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.send\_unsubscribe\_message → translated “Leave this conversation”.
  - Evaluate Platform.sendmail(recipients = list(email.from\_email), sender = self.email\_id, reply\_to = communication.incoming\_email\_account, subject = one space.join(list(translated “Re:”, communication.subject)), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in render\_template((self.auto\_reply\_message or empty text), communication.as\_dict(), restrict\_globals = true) → Platform.get\_template(“templates/emails/auto\_reply.html”).render(communication.as\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.auto\_reply\_message → empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = list(email.from\_email), sender = self.email\_id, reply\_to = communication.incoming\_email\_account, subject = one space.join(list(translated “Re:”, communication.subject)), …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L848) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L17)

<a id="op-b455a6a36ca02e"></a>
### Email Account.get unreplied notification emails

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_unreplied_notification_emails`

**Inputs** self.

**Explicit results** list of e.strip() for e drawn from self.send\_notification\_to.split(whitespace '\\n') where e.strip().

**Local steps**

- Set self.send\_notification\_to from self.send\_notification\_to.replace(“,”, whitespace '\\n').
- Return list of e.strip() for e drawn from self.send\_notification\_to.split(whitespace '\\n') where e.strip().
  - Draw e from self.send\_notification\_to.split(whitespace '\\n'), keep a combination only if (e.strip()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L1283) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L8)

<a id="op-6416f9d6937fdc"></a>
### Email Account.on trash

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_on_trash`

**Inputs** self.

**Local steps**

- Set Communication from Platform.qb.DocType(“Communication”).
- Evaluate nested operand in the contract(nested operand in the contract).set(Communication.email\_account, empty text).where(Communication.email\_account equals self.name).run().
- Evaluate remove\_user\_email\_inbox(email\_account = self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L1426) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L12)

<a id="op-ebab643f600d56"></a>
### Email Account.after delete

`operation_foundation_binding_foundation_email_doctype_email_account_email_account_emailaccount_after_delete`

**Inputs** self.

**Local steps**

- Bind dependencies delete\_relay\_app.
- Evaluate delete\_relay\_app(self.connected\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L99) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L824)

<a id="op-ce41a0f12b9888"></a>
### Email Account.after rename

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_after_rename`

**Inputs** self, old, new, merge = false.

**State and service calls** request set\_value on “Email Account”.

**Local steps**

- Evaluate Platform.db.set\_value(“Email Account”, new, “email\_account\_name”, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L1629) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1637)

<a id="op-c8633881009633"></a>
### Email Account.build email sync rule

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_build_email_sync_rule`

**Inputs** self.

**Explicit results** “UNSEEN” · formatted text UID {max\_uid}:{last\_uid} · (self.email\_sync\_option or “UNSEEN”).

**Local steps**

- If not self.use\_imap.
  - Return “UNSEEN”.
- If self.email\_sync\_option equals “ALL”.
  - Set max\_uid from get\_max\_email\_uid(self.name).
  - Set last\_uid from (max\_uid + int((self.initial\_sync\_count or 100))) when max\_uid equals 1, otherwise “\*”.
    - Value choice on max\_uid equals 1 — true gives (max\_uid + int((self.initial\_sync\_count or 100))), false gives “\*”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.initial\_sync\_count → 100.
  - Return formatted text UID {max\_uid}:{last\_uid}.
- Otherwise.
  - Return (self.email\_sync\_option or “UNSEEN”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.email\_sync\_option → “UNSEEN”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L1734) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1641)

<a id="op-050d37a2fbfa13"></a>
### Email Account.check automatic linking email account

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_check_automatic_linking_email_account`

**Inputs** self.

**Record and data access** read “Email Account” via exists.

**Explicit failure paths** validation helper — translated “Automatic Linking can be activated only if Incoming is enabled.” · validation helper — translated “Automatic Linking can be activated only for one Email Account.”.

**Local steps**

- If self.enable\_automatic\_linking.
  - If not self.enable\_incoming.
    - Call the validation error handler Platform.throw(translated “Automatic Linking can be activated only if Incoming is enabled.”).
  - If Platform.db.exists(“Email Account”, mapping(“enable\_automatic\_linking” → 1, “name” → tuple(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “Automatic Linking can be activated only for one Email Account.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L1982) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1642)

<a id="op-cee564f2d90a34"></a>
### Email Account.append email to sent folder

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_append_email_to_sent_folder`

**Inputs** self, message.

**Explicit results** no value.

**Local steps**

- If not (self.enable\_incoming and self.use\_imap).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_incoming → self.use\_imap.
  - Return no value.
- Attempt the following.
  - Set email\_server from self.get\_incoming\_server(in\_receive = true).
  - Set message from safe\_encode(message).
  - Set sent\_folder\_name from (self.sent\_folder\_name or “Sent”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.sent\_folder\_name → “Sent”.
  - Evaluate email\_server.imap.append(sent\_folder\_name, “\\Seen”, imaplib.Time2Internaldate(time.time()), message).
- On failure (Exception).
  - Evaluate self.log\_error(“Unable to add to Sent folder”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get incoming server](operations-009.md#op-0caa3ac947a329).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L2209) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1638)

<a id="op-657adb515d10d8"></a>
### Email Account.get oauth token

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_delegated_authorization_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L2488) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1659)

<a id="op-e7802070df0ad3"></a>
### Get append to

`operation_foundation_email_record_definitions_email_account_business_behavior_get_append_to`

**Inputs** doctype = no value, txt = no value, searchfield = no value, start = no value, page\_len = no value, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via get\_all · read “Property Setter” via get\_list.

**Explicit results** list of list(d) for d drawn from set(email\_append\_to\_list) where txt belongs to d.

**Local steps**

- Set txt from txt when txt, otherwise empty text.
  - Value choice on txt — true gives txt, false gives empty text.
- Set filters from mapping(“istable” → 0, “issingle” → 0, “email\_append\_to” → 1).
- Set email\_append\_to\_list from list of dt.name for dt drawn from Platform.get\_all(“DocType”, filters = filters, fields = list(“name”, “email\_append\_to”)).
  - Draw dt from Platform.get\_all(“DocType”, filters = filters, fields = list(“name”, “email\_append\_to”)).
- Evaluate email\_append\_to\_list.extend(generator of dt.doc\_type for dt drawn from Platform.get\_list(“Property Setter”, filters = mapping(“property” → “email\_append\_to”, “value” → 1), fields = list(“doc\_type”))).
  - Draw dt from Platform.get\_list(“Property Setter”, filters = mapping(“property” → “email\_append\_to”, “value” → 1), fields = list(“doc\_type”)).
- Return list of list(d) for d drawn from set(email\_append\_to\_list) where txt belongs to d.
  - Draw d from set(email\_append\_to\_list), keep a combination only if (txt belongs to d).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L2672) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L28)

<a id="op-34da20ea3395a4"></a>
### Notify unreplied

`operation_foundation_email_record_definitions_email_account_business_behavior_notify_unreplied`

**Inputs** no declared parameters.

**Record and data access** read “Email Account” via get\_all · resolve a document from “Email Account” via get\_doc · read “Communication” via get\_all · resolve a document from “Communication” via get\_doc · read comm.reference\_doctype via get\_value.

**State and service calls** sendmail with comm.reference\_doctype · call db\_set on comm.

**Local steps**

- For each email\_account in Platform.get\_all(“Email Account”, “name”, filters = mapping(“enable\_incoming” → 1, “notify\_if\_unreplied” → 1)).
  - Set email\_account from Platform.get\_doc(“Email Account”, email\_account.name).
  - If email\_account.use\_imap.
    - Set append\_to from list of folder.append\_to for folder drawn from email\_account.imap\_folder where folder.append\_to.
      - Draw folder from email\_account.imap\_folder, keep a combination only if (folder.append\_to).
  - Otherwise.
    - Set append\_to from email\_account.append\_to.
  - If append\_to.
    - For each comm in Platform.get\_all(“Communication”, “name”, filters = list(mapping(“sent\_or\_received” → “Received”), mapping(“reference\_doctype” → tuple(“in”, append\_to)), mapping(“unread\_notification\_sent” → 0), mapping(“e ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_account.unreplied\_for\_mins → 30.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_account.unreplied\_for\_mins → 30.
      - Set comm from Platform.get\_doc(“Communication”, comm.name).
      - If Platform.db.get\_value(comm.reference\_doctype, comm.reference\_name, “status”) equals “Open”.
        - Evaluate Platform.sendmail(recipients = email\_account.get\_unreplied\_notification\_emails(), content = comm.content, subject = comm.subject, doctype = comm.reference\_doctype, …).
      - Evaluate comm.db\_set(“unread\_notification\_sent”, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now() · service or queued work from Platform.sendmail(recipients = email\_account.get\_unreplied\_notification\_emails(), content = comm.content, subject = comm.subject, doctype = comm.reference\_doctype, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L97) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1259) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L32)

<a id="op-ab0edfe8f38856"></a>
### Pull

`operation_foundation_email_record_definitions_email_account_business_behavior_pull`

**Inputs** now = false.

**Local steps**

- Bind dependencies has\_token.
- Set doctype from Platform.qb.DocType(“Email Account”).
- Set email\_accounts from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.enable ….
- For each email\_account in email\_accounts.
  - If (email\_account.auth\_method equals “OAuth” and not email\_account.backend\_app\_flow and not has\_token(email\_account.connected\_app, email\_account.connected\_user)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account.auth\_method equals “OAuth” → not email\_account.backend\_app\_flow → not has\_token(email\_account.connected\_app, email\_account.connected\_user).
    - Continue with the next iteration or loop test.
  - If now.
    - Evaluate pull\_from\_email\_account(email\_account.name).
  - Otherwise.
    - Set job\_name from formatted text pull\_from\_email\_account\|{email\_account.name}.
    - Set queued\_jobs from get\_jobs(site = Platform.local.site, key = “job\_name”) at Platform.local.site.
    - If job\_name does not belong to queued\_jobs.
      - Evaluate enqueue(pull\_from\_email\_account, “short”, event = “all”, job\_name = job\_name, email\_account = email\_account.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(pull\_from\_email\_account, “short”, event = “all”, job\_name = job\_name, email\_account = email\_account.name).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L4078) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1261) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L34)

<a id="op-e8fedc5d06dbb3"></a>
### Pull emails

`operation_foundation_email_record_definitions_email_account_business_behavior_pull_emails`

**Inputs** email\_account.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** msgprint with translated “Emails are already being pulled from this account.”.

**Local steps**

- Evaluate Platform.has\_permission(“Email Account”, “read”, throw = true).
- Set job\_name from formatted text pull\_from\_email\_account\|{email\_account}.
- Set queued\_jobs from get\_jobs(site = Platform.local.site, key = “job\_name”) at Platform.local.site.
- If job\_name does not belong to queued\_jobs.
  - Evaluate pull\_from\_email\_account(email\_account).
- Otherwise.
  - Evaluate Platform.msgprint(translated “Emails are already being pulled from this account.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Email Account”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L4666) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1262) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L35)

<a id="op-df0b343a5a6779"></a>
### Pull from email account

`operation_foundation_email_record_definitions_email_account_business_behavior_pull_from_email_account`

**Inputs** email\_account.

**Record and data access** resolve a document from “Email Account” via get\_doc.

**Local steps**

- Set email\_account from Platform.get\_doc(“Email Account”, email\_account).
- Evaluate email\_account.receive().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L4953) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1263) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L36)

<a id="op-515458a2f8004e"></a>
### Get max email uid

`operation_foundation_email_record_definitions_email_account_business_behavior_get_maximum_email_unique_identifier`

**Inputs** email\_account.

**Record and data access** read “Communication” via get\_all.

**Explicit results** (cint(result at 0.get(“uid”, 0)) + 1) · 1.

**Local steps**

- If result bound to Platform.get\_all(“Communication”, filters = mapping(“communication\_medium” → “Email”, “sent\_or\_received” → “Received”, “email\_account” → email\_account, “uid” → tuple(“&gt;”, 0)), fields = list(mapping(“MAX” → ….
  - Return (cint(result at 0.get(“uid”, 0)) + 1).
- Return 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L5040) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1258) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L31)

<a id="op-df07205a4393c3"></a>
### Setup user email inbox

`operation_foundation_email_record_definitions_email_account_business_behavior_setup_user_email_inbox`

**Inputs** email\_account, awaiting\_password, email\_id, enable\_outgoing, used\_oauth.

**Record and data access** read “User” via get\_values · read “User Email” via get\_value.

**State and service calls** msgprint with translated “Enabled email inbox for user {0}”.format(users).

**Explicit results** no value.

**Local steps**

- Bind dependencies ask\_pass\_update.
- Bind local operation add\_user\_email for subsequent calls.
- Set update\_user\_email\_settings from false.
- If not all(list(email\_account, email\_id)).
  - Return no value.
- Set user\_names from Platform.db.get\_values(“User”, mapping(“email” → email\_id), as\_dict = true).
- If not user\_names.
  - Return no value.
- For each user in user\_names.
  - Set user\_name from user.get(“name”).
  - Set user\_inbox from (Platform.db.get\_value(“User Email”, mapping(“email\_account” → email\_account, “parent” → user\_name), list(“name”)) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“User Email”, mapping(“email\_account” → email\_account, “parent” → user\_name), list(“name”)) → no value.
  - If not user\_inbox.
    - Evaluate add\_user\_email(user\_name).
  - Otherwise.
    - Set update\_user\_email\_settings from true.
- If update\_user\_email\_settings.
  - Set UserEmail from Platform.qb.DocType(“User Email”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(UserEmail.used\_oauth, (used\_oauth or 0)).where(UserEmail.email\_account equals email\_account).run().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in awaiting\_password → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in enable\_outgoing → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in used\_oauth → 0.
- Otherwise.
  - Set users from “ and ”.join(list of Platform.bold(user.get(“name”)) for user drawn from user\_names).
    - Draw user from user\_names.
  - Evaluate Platform.msgprint(translated “Enabled email inbox for user {0}”.format(users)).
- Evaluate ask\_pass\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L5311) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L39)

<a id="op-2ea8e97ec0cd71"></a>
### Setup user email inbox.add user email

`operation_foundation_email_record_definitions_email_account_business_behavior_setup_user_email_inbox_add_user_email`

**Inputs** user.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set user from Platform.get\_doc(“User”, user).
- Set row from user.append(“user\_emails”, mapping()).
- Set row.email\_id from email\_id.
- Set row.email\_account from email\_account.
- Set row.awaiting\_password from (awaiting\_password or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in awaiting\_password → 0.
- Set row.used\_oauth from (used\_oauth or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in used\_oauth → 0.
- Set row.enable\_outgoing from (enable\_outgoing or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in enable\_outgoing → 0.
- Evaluate user.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L6329) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L40)

<a id="op-573cf69b9f7b7b"></a>
### Remove user email inbox

`operation_foundation_email_record_definitions_email_account_business_behavior_remove_user_email_inbox`

**Inputs** email\_account.

**Record and data access** read “User Email” via get\_all · resolve a document from “User” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- If not email\_account.
  - Return no value.
- Set users from Platform.get\_all(“User Email”, filters = mapping(“email\_account” → email\_account), fields = list(“parent as name”)).
- For each user in users.
  - Set doc from Platform.get\_doc(“User”, user.get(“name”)).
  - Set to\_remove from list of row for row drawn from doc.user\_emails where row.email\_account equals email\_account.
    - Draw row from doc.user\_emails, keep a combination only if (row.email\_account equals email\_account).
  - Evaluate list of doc.remove(row) for row drawn from to\_remove.
    - Draw row from to\_remove.
  - Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L6579) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L37)

<a id="op-580d8faee10a2c"></a>
### Set email password

`operation_foundation_email_record_definitions_email_account_business_behavior_set_email_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** email\_account, password.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup, record lookup, record mutation request, transaction control.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0223.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L38)

<a id="op-aaea98bd34ba38"></a>
### Get automatic email link

`operation_foundation_email_record_definitions_email_account_business_behavior_get_automatic_email_link`

**Inputs** no declared parameters.

**Explicit results** Platform.client\_cache.get\_value(“automatic\_linking\_email”, generator = check\_db).

**Local steps**

- Bind local operation check\_db for subsequent calls.
- Return Platform.client\_cache.get\_value(“automatic\_linking\_email”, generator = check\_db).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0223.json#L325) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L29)

<a id="op-9a0a10f8829a30"></a>
### Get automatic email link.check db

`operation_foundation_email_record_definitions_email_account_business_behavior_get_automatic_email_link_check_database`

**Inputs** no declared parameters.

**Record and data access** read “Email Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Email Account”, mapping(“enable\_incoming” → 1, “enable\_automatic\_linking” → 1), “email\_id”).

**Local steps**

- Return Platform.db.get\_value(“Email Account”, mapping(“enable\_incoming” → 1, “enable\_automatic\_linking” → 1), “email\_id”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0223.json#L472) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L30)

<a id="op-94ebc9b0a9902f"></a>
### On doctype update

`operation_foundation_email_record_definitions_email_account_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**Declared result** no value.

**State and service calls** request add\_unique on “Email Account”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Email Account”, list(“email\_id”, “enable\_incoming”, “enable\_outgoing”), constraint\_name = “unique\_email\_account\_type”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0223.json#L573) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L33)

## Service · Email body

<a id="op-3c169e9767d633"></a>
### Get email

`operation_foundation_email_email_body_business_behavior_get_email`

**Inputs** recipients, sender = empty text, msg = empty text, subject = “&#91;No Subject&#93;”, text\_content = no value, footer = no value, print\_html = no value, formatted = no value, attachments = no value, content = no value, reply\_to = no value, cc = no value, bcc = no value, email\_account = no value, expose\_recipients = no value, inline\_images = no value, header = no value, x\_priority = 3.

**Explicit results** emailobj.

**Local steps**

- Set content from (content or msg).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → msg.
- If cc is identical to no value.
  - Set cc from list().
- If bcc is identical to no value.
  - Set bcc from list().
- If inline\_images is identical to no value.
  - Set inline\_images from list().
- Set emailobj from EMail(sender, recipients, subject, reply\_to = reply\_to, cc = cc, bcc = bcc, email\_account = email\_account, …).
- If not content.strip().startswith(“&lt;”).
  - Set content from markdown(content).
- Evaluate emailobj.set\_html(content, text\_content, footer = footer, header = header, print\_html = print\_html, formatted = formatted, …).
- If isinstance(attachments, dict).
  - Set attachments from list(attachments).
- For each attach in (attachments or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in attachments → list().
  - If attach.get(“fcontent”) is identical to no value.
    - Continue with the next iteration or loop test.
  - Evaluate emailobj.add\_attachment(expanded names attach).
- Return emailobj.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0232.json#L6761) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1474)
