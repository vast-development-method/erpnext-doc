# Integration and transport · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Receive

<a id="op-0dbc3366ea8710"></a>
### Email Server.connect pop

`operation_foundation_email_receive_business_behavior_email_server_connect_post_office_protocol`

**Inputs** self.

**State and service calls** msgprint with translated “Invalid Mail Server. Please rectify and try again.” · msgprint with translated “Invalid User Name or Support Password. Please rectify and try again.”.

**Explicit results** true · false.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - If cint(self.settings.use\_ssl).
    - Set self.pop from poplib.POP3\_SSL(self.settings.host, self.settings.incoming\_port, timeout = self.pop\_timeout, context = ssl.create\_default\_context()).
  - Otherwise.
    - Set self.pop from poplib.POP3(self.settings.host, self.settings.incoming\_port, timeout = self.pop\_timeout).
  - If self.settings.use\_oauth.
    - Evaluate Oauth(self.pop, self.settings.email\_account, self.settings.username, self.settings.access\_token).connect().
  - Otherwise.
    - Evaluate self.pop.user(self.settings.username).
    - Evaluate self.pop.pass\_(self.settings.password).
  - Return true.
- On failure (\_socket.error).
  - Evaluate Platform.log\_error(“POP: Unable to connect”).
  - Evaluate Platform.msgprint(translated “Invalid Mail Server. Please rectify and try again.”).
  - Propagate the active failure.
- On failure (poplib.error\_proto) bound to e.
  - If self.is\_temporary\_system\_problem(e).
    - Return false.
  - Otherwise.
    - Evaluate Platform.msgprint(translated “Invalid User Name or Support Password. Please rectify and try again.”).
    - Propagate the active failure.

**Methods declared on this owner** [is temporary system problem](operations-028.md#op-7bfd29d848c96a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L4846) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1539)

<a id="op-ade0ded2dd63c4"></a>
### Email Server.select imap folder

`operation_foundation_email_receive_business_behavior_email_server_select_internet_message_access_protocol_folder`

**Inputs** self, folder.

**Explicit results** res at 0 equals “OK”.

**Local steps**

- Set res from self.imap.select(formatted text "{folder}").
- Return res at 0 equals “OK”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L5428) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1551)

<a id="op-3e2ac84d881b06"></a>
### Email Server.logout

`operation_foundation_email_receive_business_behavior_email_server_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L5545) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1546)

<a id="op-1db1c89f943ad3"></a>
### Email Server.get messages

`operation_foundation_email_receive_business_behavior_email_server_get_messages`

**Inputs** self, folder = “INBOX”.

**Explicit results** out.

**Local steps**

- Set self.latest\_messages from list().
- Set self.seen\_status from mapping().
- Set self.uid\_reindexed from false.
- Set email\_list from self.get\_new\_mails(folder).
- For each tuple(i, uid) in enumerate(email\_list at slice no value to 100).
  - Attempt the following.
    - Evaluate self.retrieve\_message(uid, (i + 1), folder).
  - On failure (tuple(\_socket.timeout, LoginLimitExceeded)).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set out from mapping(“latest\_messages” → self.latest\_messages).
- If self.settings.use\_imap.
  - Evaluate out.update(mapping(“uid\_list” → email\_list, “seen\_status” → self.seen\_status, “uid\_reindexed” → self.uid\_reindexed)).
- Return out.

**Methods declared on this owner** [get new mails](operations-028.md#op-b4c06d769e7ba3), [retrieve message](operations-028.md#op-d29d0cd9937609).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L5730) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1541)

<a id="op-b4c06d769e7ba3"></a>
### Email Server.get new mails

`operation_foundation_email_receive_business_behavior_email_server_get_new_mails`

**Inputs** self, folder.

**Explicit results** email\_list.

**Local steps**

- Set email\_list from list().
- If cint(self.settings.use\_imap).
  - Evaluate self.check\_imap\_uidvalidity(folder).
  - Set readonly from self.settings.email\_sync\_rule differs from “UNSEEN”.
  - Evaluate self.imap.select(folder, readonly = readonly).
  - Set tuple(\_response, message) from self.imap.uid(“search”, no value, self.settings.email\_sync\_rule).
  - If message at 0.
    - Set email\_list from message at 0.split().
- Otherwise.
  - Set email\_list from self.pop.list() at 1.
- Return email\_list.

**Methods declared on this owner** [check imap uidvalidity](operations-028.md#op-0408cab6df2d46).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L6105) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1542)

<a id="op-0408cab6df2d46"></a>
### Email Server.check imap uidvalidity

`operation_foundation_email_receive_business_behavior_email_server_check_internet_message_access_protocol_unique_identifier_validity`

**Inputs** self, folder.

**State and service calls** request set\_value on “Email Account” · request set\_value on “Communication” · request set\_value on “IMAP Folder”.

**Local steps**

- Set uid\_validity from self.settings.uid\_validity.
- Set tuple(\_response, message) from self.imap.status(folder, “(UIDVALIDITY UIDNEXT)”).
- Set current\_uid\_validity from (self.parse\_imap\_response(“UIDVALIDITY”, message at 0) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.parse\_imap\_response(“UIDVALIDITY”, message at 0) → 0.
- Set uidnext from int((self.parse\_imap\_response(“UIDNEXT”, message at 0) or “1”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.parse\_imap\_response(“UIDNEXT”, message at 0) → “1”.
- Evaluate Platform.db.set\_value(“Email Account”, self.settings.email\_account, “uidnext”, uidnext).
- If uid\_validity is identical to no value.
  - Set Platform.flags.initial\_sync from true.
- If (not uid\_validity or uid\_validity differs from current\_uid\_validity).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not uid\_validity → uid\_validity differs from current\_uid\_validity.
  - Evaluate Platform.db.set\_value(“Communication”, mapping(“communication\_medium” → “Email”, “email\_account” → self.settings.email\_account), “uid”, negative 1, update\_modified = false).
  - If self.settings.use\_imap.
    - If folder at 0 equals folder at negative 1 equals “"”.
      - Compare adjacent operands in order, stopping at the first false comparison in folder at 0 equals folder at negative 1 equals “"”.
      - Set folder from folder at slice 1 to negative 1.
    - Evaluate Platform.db.set\_value(“IMAP Folder”, mapping(“parent” → self.settings.email\_account\_name, “folder\_name” → folder), mapping(“uidvalidity” → current\_uid\_validity, “uidnext” → uidnext), update\_modified = false).
  - Otherwise.
    - Evaluate Platform.db.set\_value(“Email Account”, self.settings.email\_account\_name, mapping(“uidvalidity” → current\_uid\_validity, “uidnext” → uidnext), update\_modified = false).
  - Set sync\_count from 100 when uid\_validity, otherwise int(self.settings.initial\_sync\_count).
    - Value choice on uid\_validity — true gives 100, false gives int(self.settings.initial\_sync\_count).
  - Set from\_uid from 1 when (uidnext &lt; (sync\_count + 1) or (uidnext − sync\_count) &lt; 1), otherwise (uidnext − sync\_count).
    - Value choice on (uidnext &lt; (sync\_count + 1) or (uidnext − sync\_count) &lt; 1) — true gives 1, false gives (uidnext − sync\_count).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in uidnext &lt; (sync\_count + 1) → (uidnext − sync\_count) &lt; 1.
  - Set self.settings.email\_sync\_rule from formatted text UID {from\_uid}:{uidnext}.
  - Set self.uid\_reindexed from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse imap response](operations-028.md#op-5d397414e8392a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L6436) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1536)

<a id="op-5d397414e8392a"></a>
### Email Server.parse imap response

`operation_foundation_email_receive_business_behavior_email_server_parse_internet_message_access_protocol_response`

**Inputs** self, cmd, response.

**Explicit results** match at 0 when match, otherwise no value.

**Local steps**

- Set pattern from formatted text (?&lt;={cmd} )&#91;0-9&#93;\*.
- Set match from re.search(pattern, response.decode(“utf-8”), (re.U bitwise or re.I)).
- Return match at 0 when match, otherwise no value.
  - Value choice on match — true gives match at 0, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1548)

<a id="op-d29d0cd9937609"></a>
### Email Server.retrieve message

`operation_foundation_email_receive_business_behavior_email_server_retrieve_message`

**Inputs** self, uid, msg\_num, folder.

**Declared result** no value.

**Explicit results** no value · self.retrieve\_message(uid, msg\_num, folder).

**Explicit failure paths** propagate active failure · LoginLimitExceeded(e).

**Local steps**

- Attempt the following.
  - If cint(self.settings.use\_imap).
    - Set tuple(\_status, data) from self.imap.uid(“fetch”, uid, “(BODY.PEEK&#91;&#93; FLAGS)”).
    - If (\_status differs from “OK” or not data).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_status differs from “OK” → not data.
      - Return no value.
    - Set raw\_email from next(generator of part at 1 for part drawn from data where (isinstance(part, tuple) and byte value belongs to part at 0), no value).
      - Draw part from data, keep a combination only if ((isinstance(part, tuple) and byte value belongs to part at 0)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(part, tuple) → byte value belongs to part at 0.
    - If raw\_email is identical to no value.
      - Return no value.
    - Set flags\_line from next(generator of part for part drawn from data where (isinstance(part, bytes) and byte value belongs to part), no value).
      - Draw part from data, keep a combination only if ((isinstance(part, bytes) and byte value belongs to part)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(part, bytes) → byte value belongs to part.
    - If flags\_line is distinct from no value.
      - Evaluate self.get\_email\_seen\_status(uid, flags\_line).
    - Evaluate self.latest\_messages.append(raw\_email).
  - Otherwise.
    - Set msg from self.pop.retr(msg\_num).
    - Evaluate self.latest\_messages.append(byte value.join(msg at 1)).
- On failure (\_socket.timeout).
  - Propagate the active failure.
- On failure (imaplib.IMAP4.abort).
  - If self.retry\_count &lt; self.retry\_limit.
    - Evaluate self.connect().
    - Update self.retry\_count using + 1.
    - Evaluate self.imap.select(folder, readonly = self.settings.email\_sync\_rule differs from “UNSEEN”).
    - Return self.retrieve\_message(uid, msg\_num, folder).
- On failure (Exception) bound to e.
  - If self.has\_login\_limit\_exceeded(e).
    - Raise LoginLimitExceeded(e) with cause e.
  - Evaluate Platform.log\_error(“Unable to fetch email”, self.make\_error\_msg(uid, msg\_num)).
- Evaluate self.\_post\_retrieve\_cleanup(uid, msg\_num).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get email seen status](operations-028.md#op-2bf9f3e381edd5), [connect](operations-027.md#op-2e4639fb508fe8), [has login limit exceeded](operations-028.md#op-a445e53773c6bf), [make error msg](operations-028.md#op-24fa41401a3bb3), [post retrieve cleanup](operations-028.md#op-b9a6cef6a4cf97).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L80) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1550)

<a id="op-2bf9f3e381edd5"></a>
### Email Server.get email seen status

`operation_foundation_email_receive_business_behavior_email_server_get_email_seen_status`

**Inputs** self, uid, flag\_string.

**Explicit results** no value.

**Local steps**

- If (not flag\_string or not isinstance(flag\_string, (str bitwise or bytes))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not flag\_string → not isinstance(flag\_string, (str bitwise or bytes)).
  - Return no value.
- Set flags from list().
- For each flag in (imaplib.ParseFlags(flag\_string) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in imaplib.ParseFlags(flag\_string) → list().
  - Set match from WORDS\_PATTERN.search(Platform.as\_unicode(flag)).
  - Evaluate flags.append(match.group(0)).
- If “Seen” belongs to flags.
  - Evaluate self.seen\_status.update(mapping(uid → “SEEN”)).
- Otherwise.
  - Evaluate self.seen\_status.update(mapping(uid → “UNSEEN”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L1035) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1540)

<a id="op-a445e53773c6bf"></a>
### Email Server.has login limit exceeded

`operation_foundation_email_receive_business_behavior_email_server_has_login_limit_exceeded`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, e.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L1379) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1543)

<a id="op-b9a6cef6a4cf97"></a>
### Email Server.post retrieve cleanup

`operation_foundation_email_receive_business_behavior_email_server_post_retrieve_cleanup`

**Inputs** self, uid, msg\_num.

**Local steps**

- Within suppress(Exception).
  - If not cint(self.settings.use\_imap).
    - Evaluate self.pop.dele(msg\_num).
  - Otherwise.
    - If self.settings.email\_sync\_rule equals “UNSEEN”.
      - Evaluate self.imap.uid(“STORE”, uid, “+FLAGS”, “(\\SEEN)”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L1464) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1549)

<a id="op-7bfd29d848c96a"></a>
### Email Server.is temporary system problem

`operation_foundation_email_receive_business_behavior_email_server_is_temporary_system_problem`

**Inputs** self, e.

**Explicit results** any(generator of (message belongs to strip(cstr(e)) or message belongs to strip(cstr(nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contrac …).

**Local steps**

- Set messages from tuple(“-ERR &#91;SYS/TEMP&#93; Temporary system problem. Please try again later.”, “Connection timed out”).
- Return any(generator of (message belongs to strip(cstr(e)) or message belongs to strip(cstr(nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contrac …).
  - Draw message from messages.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in message belongs to strip(cstr(e)) → message belongs to strip(cstr(getattr(e, “strerror”, empty text))).

**Values supplied outside this operation** selected callable from getattr(e, “strerror”, empty text).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L1676) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1545)

<a id="op-24fa41401a3bb3"></a>
### Email Server.make error msg

`operation_foundation_email_receive_business_behavior_email_server_make_error_message`

**Inputs** self, uid, msg\_num.

**Explicit results** formatted text  Date: {partial\_mail.date} From: {partial\_mail.from\_email} Subject: {partial\_mail.subject}   Traceback: {traceback}  · traceback.

**Local steps**

- Set partial\_mail from no value.
- Set traceback from Platform.get\_traceback(with\_context = true).
- Within suppress(Exception).
  - If not cint(self.settings.use\_imap).
    - Set headers from byte value.join(self.pop.top(msg\_num, 5) at 1).
  - Otherwise.
    - Set headers from self.imap.uid(“fetch”, uid, “(BODY.PEEK&#91;HEADER&#93;)”) at 1 at 0 at 1.
  - Set partial\_mail from Email(headers).
- If partial\_mail.
  - Return formatted text  Date: {partial\_mail.date} From: {partial\_mail.from\_email} Subject: {partial\_mail.subject}   Traceback: {traceback}.
- Return traceback.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L1882) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1547)

<a id="op-b55e9efe9ddba6"></a>
### Email Server.update flag

`operation_foundation_email_receive_business_behavior_email_server_update_flag`

**Inputs** self, folder, uid\_list = no value.

**Explicit results** no value.

**Local steps**

- If not uid\_list.
  - Return no value.
- If not self.connect().
  - Return no value.
- Evaluate self.imap.select(folder).
- For each tuple(uid, operation) in uid\_list.items().
  - If not uid.
    - Continue with the next iteration or loop test.
  - Set op from “+FLAGS” when operation equals “Read”, otherwise “-FLAGS”.
    - Value choice on operation equals “Read” — true gives “+FLAGS”, false gives “-FLAGS”.
  - Attempt the following.
    - Evaluate self.imap.uid(“STORE”, uid, op, “(\\SEEN)”).
  - On failure (Exception).
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Methods declared on this owner** [connect](operations-027.md#op-2e4639fb508fe8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L2294) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1552)

<a id="op-e5a440b73e27ac"></a>
### Email.initialize

`operation_foundation_email_receive_business_behavior_email_initialize`

**Inputs** self, content.

**Local steps**

- If isinstance(content, bytes).
  - Set self.mail from email.message\_from\_bytes(content).
- Otherwise.
  - Set self.mail from email.message\_from\_string(content).
- Set self.raw\_message from content.
- Set self.text\_content from empty text.
- Set self.html\_content from empty text.
- Set self.attachments from list().
- Set self.cid\_map from mapping().
- Evaluate self.parse().
- Evaluate self.set\_content\_and\_type().
- Evaluate self.set\_subject().
- Evaluate self.set\_from().
- Set message\_id from (self.mail.get(“Message-ID”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“Message-ID”) → empty text.
- Set self.message\_id from get\_string\_between(“&lt;”, message\_id, “&gt;”).
- If self.mail at “Date”.
  - Attempt the following.
    - Set utc from email.utils.mktime\_tz(email.utils.parsedate\_tz(self.mail at “Date”)).
    - Set utc\_dt from datetime.datetime.fromtimestamp(utc, tz = datetime.UTC).
    - Set self.date from convert\_utc\_to\_system\_timezone(utc\_dt).strftime(“%Y-%m-%d %H:%M:%S”).
  - On failure (Exception).
    - Set self.date from now().
- Otherwise.
  - Set self.date from now().
- If self.date &gt; now().
  - Set self.date from now().

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse](operations-028.md#op-b5d0df5473895c), [set content and type](operations-028.md#op-d731ddcbc75c06), [set subject](operations-028.md#op-0c9f170e471266), [set from](operations-028.md#op-ae989eccc29668).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L2575) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1099) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1531)

<a id="op-8c6d90883d2520"></a>
### Email.in reply to

`operation_foundation_email_receive_business_behavior_email_in_reply_to`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** get\_string\_between(“&lt;”, in\_reply\_to, “&gt;”).

**Local steps**

- Set in\_reply\_to from (self.mail.get(“In-Reply-To”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“In-Reply-To”) → empty text.
- Return get\_string\_between(“&lt;”, in\_reply\_to, “&gt;”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L3264) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1530)

<a id="op-b5d0df5473895c"></a>
### Email.parse

`operation_foundation_email_receive_business_behavior_email_parse`

**Inputs** self.

**Local steps**

- For each part in self.mail.walk().
  - Evaluate self.process\_part(part).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process part](operations-028.md#op-87d2ea3492cc9e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L3373) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1533)

<a id="op-0c9f170e471266"></a>
### Email.set subject

`operation_foundation_email_receive_business_behavior_email_set_subject`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set raw\_subject from self.mail.get(“Subject”).
- If not raw\_subject.
  - Set self.subject from “No Subject”.
  - Return no value.
- Set decoded\_fragments from list().
- For each tuple(fragment, charset) in decode\_header(raw\_subject).
  - If isinstance(fragment, bytes).
    - Set charset from (charset or “utf-8”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in charset → “utf-8”.
    - Attempt the following.
      - Set fragment from fragment.decode(charset, errors = “replace”).
    - On failure (LookupError).
      - Set fragment from fragment.decode(“utf-8”, errors = “replace”).
  - Evaluate decoded\_fragments.append(fragment).
- Set subject from empty text.join(decoded\_fragments).strip().
- Set self.subject from subject at slice no value to 140 when subject, otherwise “No Subject”.
  - Value choice on subject — true gives subject at slice no value to 140, false gives “No Subject”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L3460) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1555)

<a id="op-ae989eccc29668"></a>
### Email.set from

`operation_foundation_email_receive_business_behavior_email_set_from`

**Inputs** self.

**Record and data access** read “Email Account” via get\_value.

**Explicit results** no value.

**Local steps**

- Set self.from\_real\_name from no value.
- Set \_from\_email from self.decode\_email((self.mail.get(“X-Original-From”) or self.mail at “From”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mail.get(“X-Original-From”) → self.mail at “From”.
- Set \_reply\_to from self.decode\_email(self.mail.get(“Reply-To”)).
- If not \_from\_email.
  - Evaluate Platform.log\_error(formatted text Email missing ′From′ header. UID: {getattr(self, “uid”, “unknown”)}, str(self.mail)).
  - Set self.from\_email from no value.
  - Return no value.
- If (\_reply\_to and not Platform.db.get\_value(“Email Account”, mapping(“email\_id” → extract\_email\_id(\_reply\_to), “enable\_incoming” → 1), “email\_id”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_reply\_to → not Platform.db.get\_value(“Email Account”, mapping(“email\_id” → extract\_email\_id(\_reply\_to), “enable\_incoming” → 1), “email\_id”).
  - Set self.from\_email from extract\_email\_id(\_reply\_to).
- Otherwise.
  - Set self.from\_email from extract\_email\_id(\_from\_email).
- Set self.from\_email from self.from\_email.lower().
- Set self.from\_real\_name from parse\_addr(\_from\_email) at 0 when “@” belongs to \_from\_email, otherwise \_from\_email.
  - Value choice on “@” belongs to \_from\_email — true gives parse\_addr(\_from\_email) at 0, false gives \_from\_email.

If control reaches the end, it returns no value.

**Methods declared on this owner** [decode email](operations-028.md#op-da9878f2545a69).

**Values supplied outside this operation** selected callable from getattr(self, “uid”, “unknown”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L81) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1554)

<a id="op-da9878f2545a69"></a>
### Email.decode email

`operation_foundation_email_receive_business_behavior_email_decode_email`

**Inputs** email.

**Wrappers, in declaration order** staticmethod.

**Declared result** (str bitwise or no value).

**Explicit results** no value · “, ”.join(emails) · decoded.

**Local steps**

- If not email.
  - Return no value.
- Set email from Platform.as\_unicode(email).
- Attempt the following.
  - Set parts from decode\_header(email).
- On failure (HeaderParseError).
  - Set emails from re.findall(“(&lt;.\*?&gt;)”, email).
  - Return “, ”.join(emails).
- Set decoded from empty text.
- For each tuple(part, encoding) in parts.
  - If encoding.
    - Attempt the following.
      - Update decoded using + part.decode(encoding, “replace”).
    - On failure (LookupError).
      - Update decoded using + part.decode(“utf-8”, “replace”).
  - Otherwise.
    - Update decoded using + safe\_decode(part).
- If (decoded and “@” belongs to decoded and “@” does not belong to email).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in decoded → “@” belongs to decoded → “@” does not belong to email.
  - Set decoded\_addr\_spec from parse\_addr(decoded) at 1.
  - If (decoded\_addr\_spec and decoded.strip() equals decoded\_addr\_spec).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in decoded\_addr\_spec → decoded.strip() equals decoded\_addr\_spec.
    - Evaluate Platform.log\_error(title = translated “Malformed Address Header”, message = translated “Rejected malformed encoded address header with synthesized '@': {0}”.format(repr(email))).
    - Return no value.
- Return decoded.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L77) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1093) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1525)

<a id="op-d731ddcbc75c06"></a>
### Email.set content and type

`operation_foundation_email_receive_business_behavior_email_set_content_and_type`

**Inputs** self.

**Local steps**

- Set tuple(self.content, self.content\_type) from tuple(“&#91;Blank Email&#93;”, “text/plain”).
- If self.html\_content.
  - Set tuple(self.content, self.content\_type) from tuple(self.html\_content, “text/html”).
- Otherwise.
  - Set tuple(self.content, self.content\_type) from tuple(EmailReplyParser.read(self.text\_content).text.replace(whitespace '\\n', whitespace '\\n\\n'), “text/plain”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L5040) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1553)

<a id="op-87d2ea3492cc9e"></a>
### Email.process part

`operation_foundation_email_receive_business_behavior_email_process_part`

**Inputs** self, part.

**Local steps**

- Set content\_type from part.get\_content\_type().
- If content\_type equals “text/plain”.
  - Update self.text\_content using + self.get\_payload(part).
  - If part.get\_filename().
    - Evaluate self.get\_attachment(part).
- Otherwise.
  - If (content\_type equals “text/html” and part.get\_content\_disposition() differs from “attachment”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in content\_type equals “text/html” → part.get\_content\_disposition() differs from “attachment”.
    - Update self.html\_content using + self.get\_payload(part).
  - Otherwise.
    - If content\_type equals “message/rfc822”.
      - Evaluate self.show\_attached\_email\_headers\_in\_content(part).
    - Otherwise.
      - If (part.get\_filename() or “image” belongs to content\_type).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.get\_filename() → “image” belongs to content\_type.
        - Evaluate self.get\_attachment(part).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payload](operations-029.md#op-31d6c9a8b75565), [get attachment](operations-029.md#op-d18becd8129571), [show attached email headers in content](operations-028.md#op-457e9b7d09e89c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L78) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1534)

<a id="op-457e9b7d09e89c"></a>
### Email.show attached email headers in content

`operation_foundation_email_receive_business_behavior_email_show_attached_email_headers_in_content`

**Inputs** self, part.

**Local steps**

- Bind dependencies escape.
- Set message from list(part.walk()) at 1.
- Set headers from list().
- For each key in tuple(“From”, “To”, “Subject”, “Date”).
  - Set value from self.decode\_email(message.get(key)).
  - If value.
    - Evaluate headers.append(formatted text {translated key}: {escape(value)}).
- Update self.text\_content using + whitespace '\\n'.join(headers).
- Update self.html\_content using + (text in the contract + whitespace '\\n'.join(generator of formatted text &lt;p&gt;{h}&lt;/p&gt; for h drawn from headers)).
  - Draw h from headers.
- If (not message.is\_multipart() and message.get\_content\_type() equals “text/plain”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not message.is\_multipart() → message.get\_content\_type() equals “text/plain”.
  - Set text\_content from self.get\_payload(message).
  - Update self.text\_content using + text\_content.
  - Update self.html\_content using + markdown(text\_content).

If control reaches the end, it returns no value.

**Methods declared on this owner** [decode email](operations-028.md#op-da9878f2545a69), [get payload](operations-029.md#op-31d6c9a8b75565).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L82) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1556)

<a id="op-030f2da3f7c19d"></a>
### Email.get charset

`operation_foundation_email_receive_business_behavior_email_get_charset`

**Inputs** self, part.

**Explicit results** (part.get\_content\_charset() or chardet.detect(safe\_encode(cstr(part))) at “encoding”).

**Local steps**

- Return (part.get\_content\_charset() or chardet.detect(safe\_encode(cstr(part))) at “encoding”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.get\_content\_charset() → chardet.detect(safe\_encode(cstr(part))) at “encoding”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0236.json#L6102) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1095) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1527)
