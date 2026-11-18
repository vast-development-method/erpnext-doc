# Integration and transport · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Email

<a id="op-75a54e3c0be8e5"></a>
### Get system managers

`operation_foundation_email_initialize_business_behavior_get_system_managers`

**Inputs** no declared parameters.

**Explicit results** Platform.db.sql\_list(query text (SELECT, Has Role, User)).

**Local steps**

- Return Platform.db.sql\_list(query text (SELECT, Has Role, User)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L2483) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1070) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1503)

<a id="op-8a3a0f3fb6eecd"></a>
### Relink

`operation_foundation_email_initialize_business_behavior_relink`

**Inputs** name, reference\_doctype = no value, reference\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** execute query text (UPDATE, Communication).

**Local steps**

- Evaluate Platform.has\_permission(“Communication”, “write”, name, throw = true).
- Evaluate Platform.db.sql(query text (UPDATE, Communication), tuple(reference\_doctype, reference\_name, name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Communication”, “write”, name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L74) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1071) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1504)

<a id="op-5128a74146f2b3"></a>
### Get communication doctype

`operation_foundation_email_initialize_business_behavior_get_communication_record_type`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “DocType” via get\_values.

**Explicit results** results.

**Local steps**

- Set can\_read from Platform.get\_user().get\_can\_read().
- Set com\_doctypes from Platform.db.get\_values(“DocType”, mapping(“issingle” → 0, “istable” → 0, “hide\_toolbar” → 0), pluck = “name”).
- Set results from list of list(dt) for dt drawn from list(set(com\_doctypes)) where dt belongs to can\_read.
  - Draw dt from list(set(com\_doctypes)), keep a combination only if (dt belongs to can\_read).
- Return results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L3014) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1068) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1501)

<a id="op-3f1d18ca38d85a"></a>
### Sendmail

`operation_foundation_email_initialize_business_behavior_sendmail`

**Inputs** recipients = no value, sender = empty text, subject = “No Subject”, message = “No Message”, as\_markdown = false, delayed = true, reference\_doctype = no value, reference\_name = no value, unsubscribe\_method = no value, unsubscribe\_params = no value, unsubscribe\_message = no value, add\_unsubscribe\_link = 1, attachments = no value, content = no value, doctype = no value, name = no value, reply\_to = no value, queue\_separately = false, cc = no value, bcc = no value, message\_id = no value, in\_reply\_to = no value, send\_after = no value, expose\_recipients = no value, send\_priority = 1, communication = no value, retry = 1, now = no value, read\_receipt = no value, is\_notification = false, inline\_images = no value, template = no value, args = no value, header = no value, print\_letterhead = false, with\_container = false, email\_read\_tracker\_url = no value, x\_priority = 3, email\_headers = no value, raw\_html = false, add\_css = true, redact\_message\_after\_send = false, wrapper = no value.

**Declared result** (EmailQueue bitwise or no value).

**Explicit results** q.

**Explicit failure paths** validation helper — Platform.\_(“At least one recipient is required”).

**Local steps**

- Bind dependencies get\_email\_from\_template.
- If recipients is identical to no value.
  - Set recipients from list().
- If cc is identical to no value.
  - Set cc from list().
- If bcc is identical to no value.
  - Set bcc from list().
- Set text\_content from no value.
- If template.
  - Set tuple(message, text\_content) from get\_email\_from\_template(template, args).
- Set message from (content or message).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → message.
- If as\_markdown.
  - Bind dependencies md\_to\_html.
  - Set message from md\_to\_html(message).
- If not delayed.
  - Set now from true.
- If (communication and not (recipients or cc or bcc)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in communication → not (recipients or cc or bcc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in recipients → cc → bcc.
  - Call the validation error handler Platform.throw(Platform.\_(“At least one recipient is required”)).
- Bind dependencies QueueBuilder.
- Set builder from QueueBuilder(recipients = recipients, sender = sender, subject = subject, message = message, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → reference\_doctype.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → reference\_name.
- Set q from builder.process(send\_now = false).
- If (now and q).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in now → q.
  - Evaluate Platform.db.after\_commit.add(q.send).
- Return q.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L75) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1072) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1505)

## Record · Email account

[Record definition](../../../../data/record-types/email_account.json)

<a id="op-cca57ba9a7e7c0"></a>
### Cache email account

`operation_foundation_email_record_definitions_email_account_business_behavior_cache_email_account`

**Inputs** cache\_name.

**Explicit results** decorator\_cache\_email\_account.

**Local steps**

- Bind local operation decorator\_cache\_email\_account for subsequent calls.
- Return decorator\_cache\_email\_account.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L87) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1634)

<a id="op-83530cd899767f"></a>
### Cache email account.decorator cache email account

`operation_foundation_email_record_definitions_email_account_business_behavior_cache_email_account_decorator_cache_email_account`

**Inputs** func.

**Explicit results** wrapper\_cache\_email\_account.

**Local steps**

- Set signature from inspect.signature(func).
- Bind local operation wrapper\_cache\_email\_account for subsequent calls.
- Return wrapper\_cache\_email\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L88) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1635)

<a id="op-8080a84178b1af"></a>
### Cache email account.decorator cache email account.wrapper cache email account

`operation_foundation_email_record_definitions_email_account_business_behavior_cache_email_account_decorator_cache_email_account_wrapper_cache_email_account`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(func).

**Explicit results** account.

**Local steps**

- If not hasattr(Platform.local, cache\_name).
  - Evaluate setattr(Platform.local, cache\_name, mapping()).
- Set cached\_accounts from getattr(Platform.local, cache\_name).
- Set lookup from signature.bind(expanded args, expanded names kwargs).arguments.
- Set match\_by from tuple(lookup.get(“match\_by\_email”), lookup.get(“match\_by\_doctype”)).
- If account bound to cached\_accounts.get(match\_by).
  - Return account.
- Set account from func(expanded args, expanded names kwargs).
- If account.
  - Set cached\_accounts at match\_by from account.
- Return account.

**Values supplied outside this operation** selected callable from getattr(Platform.local, cache\_name).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L89) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1636)

<a id="op-5e7c2c44f65846"></a>
### Email Account.autoname

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_autoname`

**Inputs** self.

**Local steps**

- If not self.email\_account\_name.
  - Set self.email\_account\_name from nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“.”, one space).replace(“-”, one space).title().
- Set self.name from self.email\_account\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L1353) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1639)

<a id="op-d4647b364333f2"></a>
### Email Account.validate

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Login Id is required” · validation helper — translated “You need to set one IMAP folder for {0}”.format(Platform.bold(self.email\_id)) · validation helper — translated “Append To can be one of {0}”.format(comma\_or(valid\_doctypes)) · validation helper — translated “Password is required or select Awaiting Password” · validation helper — translated “{0} is mandatory”.format(self.meta.get\_label(“send\_notification\_to”)).

**Local steps**

- If self.email\_id.
  - Evaluate validate\_email\_address(self.email\_id, true).
- If self.login\_id\_is\_different.
  - If not self.login\_id.
    - Call the validation error handler Platform.throw(translated “Login Id is required”).
- Otherwise.
  - Set self.login\_id from no value.
- If self.service equals “Sendgrid”.
  - Set self.login\_id from “apikey”.
- If self.service equals “Platform Mail”.
  - Set self.use\_imap from 0.
  - Set self.always\_use\_account\_email\_id\_as\_sender from 1.
  - If (self.auth\_method equals “Basic” or self.get\_oauth\_token()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.auth\_method equals “Basic” → self.get\_oauth\_token().
    - Evaluate self.validate\_Platform\_mail\_settings().
- If self.enable\_incoming.
  - If (self.use\_imap and not self.imap\_folder).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_imap → not self.imap\_folder.
    - Call the validation error handler Platform.throw(translated “You need to set one IMAP folder for {0}”.format(Platform.bold(self.email\_id))).
  - Set valid\_doctypes from set of d at 0 for d drawn from get\_append\_to().
    - Draw d from get\_append\_to().
  - For each folder in self.imap\_folder.
    - If (folder.append\_to and folder.append\_to does not belong to valid\_doctypes).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in folder.append\_to → folder.append\_to does not belong to valid\_doctypes.
      - Call the validation error handler Platform.throw(translated “Append To can be one of {0}”.format(comma\_or(valid\_doctypes))).
- If (Platform.local.flags.in\_patch or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.in\_patch → Platform.in\_test.
  - Return no value.
- Set use\_oauth from self.auth\_method equals “OAuth”.
- Set validate\_oauth from (use\_oauth and not (self.is\_new() and not self.get\_oauth\_token())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_oauth → not (self.is\_new() and not self.get\_oauth\_token()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.get\_oauth\_token().
- Set self.use\_starttls from cint((self.use\_imap and self.use\_starttls and not self.use\_ssl)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_imap → self.use\_starttls → not self.use\_ssl.
- If use\_oauth.
  - Set self.awaiting\_password from 0.
  - Set self.password from no value.
- If (not Platform.local.flags.in\_install and not self.awaiting\_password and not self.service equals “Platform Mail”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.local.flags.in\_install → not self.awaiting\_password → not self.service equals “Platform Mail”.
  - If (validate\_oauth or self.password or self.smtp\_server belongs to tuple(“127.0.0.1”, “localhost”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in validate\_oauth → self.password → self.smtp\_server belongs to tuple(“127.0.0.1”, “localhost”).
    - If self.enable\_incoming.
      - Set self.flags.validate\_imap\_pop\_connection from true.
      - Set server from self.get\_incoming\_server(in\_receive = self.use\_imap).
      - If self.use\_imap.
        - Attempt the following.
          - Evaluate self.validate\_imap\_folders\_exist(server).
        - On exit, including pending return or failure.
          - If (hasattr(server, “imap”) and server.imap is distinct from no value).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(server, “imap”) → server.imap is distinct from no value.
            - Evaluate server.logout().
      - Set self.no\_failed from 0.
    - If self.enable\_outgoing.
      - Evaluate self.validate\_smtp\_conn().
  - Otherwise.
    - If (self.enable\_incoming or (self.enable\_outgoing and not self.no\_smtp\_authentication)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.enable\_incoming → (self.enable\_outgoing and not self.no\_smtp\_authentication).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_outgoing → not self.no\_smtp\_authentication.
      - If not use\_oauth.
        - Call the validation error handler Platform.throw(translated “Password is required or select Awaiting Password”).
- If self.notify\_if\_unreplied.
  - If not self.send\_notification\_to.
    - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(self.meta.get\_label(“send\_notification\_to”))).
  - For each e in self.get\_unreplied\_notification\_emails().
    - Evaluate validate\_email\_address(e, true).
- If self.enable\_outgoing.
  - Evaluate self.validate\_reply\_to\_addresses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get oauth token](operations-011.md#op-657adb515d10d8), [validate Platform mail settings](operations-009.md#op-50553eb3804c2c), [get incoming server](operations-009.md#op-0caa3ac947a329), [validate imap folders exist](operations-009.md#op-6c64c39b8f0ab2), [validate smtp conn](operations-009.md#op-d6cbeeefa9c063), [get unreplied notification emails](operations-011.md#op-b455a6a36ca02e), [validate reply to addresses](operations-009.md#op-a8b5aa00bc7a5a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L96) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L22)

<a id="op-50553eb3804c2c"></a>
### Email Account.validate Platform mail settings

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate_foundation_mail_settings`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If self.service equals “Platform Mail”.
  - Set Platform\_mail\_client from self.get\_Platform\_mail\_client().
  - Evaluate Platform\_mail\_client.validate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Platform mail client](operations-010.md#op-6e4ea5f9baa267).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L3100) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L24)

<a id="op-6c64c39b8f0ab2"></a>
### Email Account.validate imap folders exist

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate_internet_message_access_protocol_folders_exist`

**Inputs** self, server.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Failed to retrieve the list of IMAP folders from the server. Please ensure the mailbox is accessible and the …” · validation helper — translated “No IMAP folders were found on the server. Please verify the email account settings and ensure the mailbox co …” · validation helper — translated “IMAP Folder name cannot be empty.” · validation helper — translated “The following configured IMAP folder(s) were not found or are not accessible on the server:&lt;br&gt;&lt;ul&gt;{0}&lt;/ul&gt;P …”.format(missing\_list).

**Local steps**

- If (not hasattr(server, “imap”) or server.imap is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(server, “imap”) → server.imap is identical to no value.
  - Evaluate server.connect().
- Set tuple(status, mailboxes) from server.imap.list().
- If status differs from “OK”.
  - Call the validation error handler Platform.throw(translated “Failed to retrieve the list of IMAP folders from the server. Please ensure the mailbox is accessible and the …”, title = translated “IMAP Folder Validation Failed”).
- If not mailboxes.
  - Call the validation error handler Platform.throw(translated “No IMAP folders were found on the server. Please verify the email account settings and ensure the mailbox co …”, title = translated “IMAP Folder Validation Failed”).
- Set missing\_folders from list().
- For each row in self.imap\_folder.
  - Set folder from row.folder\_name.strip().
  - If not folder.
    - Call the validation error handler Platform.throw(translated “IMAP Folder name cannot be empty.”).
  - Set tuple(status, \_response) from server.imap.select(formatted text "{folder}", readonly = true).
  - If status differs from “OK”.
    - Evaluate missing\_folders.append(folder).
    - Continue with the next iteration or loop test.
- If missing\_folders.
  - Set missing\_list from empty text.join(generator of formatted text &lt;li&gt;{Platform.utils.escape\_html(folder)}&lt;/li&gt; for folder drawn from missing\_folders).
    - Draw folder from missing\_folders.
  - Call the validation error handler Platform.throw(translated “The following configured IMAP folder(s) were not found or are not accessible on the server:&lt;br&gt;&lt;ul&gt;{0}&lt;/ul&gt;P …”.format(missing\_list), title = translated “IMAP Folder Not Found”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L3220) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L25)

<a id="op-d6cbeeefa9c063"></a>
### Email Account.validate smtp conn

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate_simple_mail_transfer_protocol_conn`

**Inputs** self.

**Explicit failure paths** validation helper — translated “SMTP Server is required”.

**Local steps**

- If not self.smtp\_server.
  - Call the validation error handler Platform.throw(translated “SMTP Server is required”).
- Set self.flags.validate\_smtp\_connection from true.
- Set session from self.get\_smtp\_server().session.
- Evaluate self.validate\_dsn(session).
- Remove self.\_smtp\_server\_instance.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get smtp server](operations-010.md#op-c379b562ab3430), [validate dsn](operations-009.md#op-fae79909cfe61c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L3943) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L27)

<a id="op-a8b5aa00bc7a5a"></a>
### Email Account.validate reply to addresses

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate_reply_to_addresses`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Reply To email is required”.

**Local steps**

- For each reply\_to in self.reply\_to\_addresses.
  - If not reply\_to.email.
    - Call the validation error handler Platform.throw(translated “Reply To email is required”).
  - Evaluate validate\_email\_address(reply\_to.email, true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L4122) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L26)

<a id="op-fae79909cfe61c"></a>
### Email Account.validate dsn

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_validate_dsn`

**Inputs** self, smtp\_session.

**Declared result** no value.

**State and service calls** msgprint with translated “The configured SMTP server does not support DSN (Delivery Status Notification).”.

**Explicit results** no value.

**Local steps**

- If not self.dsn\_notify\_type.
  - Return no value.
- If not smtp\_session.has\_extn(“DSN”).
  - Set self.dsn\_notify\_type from no value.
  - Evaluate Platform.msgprint(translated “The configured SMTP server does not support DSN (Delivery Status Notification).”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L4258) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L23)

<a id="op-63f83cfe25e03c"></a>
### Email Account.before save

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_before_save`

**Inputs** self.

**State and service calls** msgprint with messages.

**Local steps**

- Set messages from list().
- Set as\_list from 1.
- If (not self.enable\_incoming and self.default\_incoming).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.enable\_incoming → self.default\_incoming.
  - Set self.default\_incoming from false.
  - Evaluate messages.append(translated “{} has been disabled. It can only be enabled if {} is checked.”.format(Platform.bold(translated “Default Incoming”), Platform.bold(translated “Enable Incoming”))).
- If (not self.enable\_outgoing and self.default\_outgoing).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.enable\_outgoing → self.default\_outgoing.
  - Set self.default\_outgoing from false.
  - Evaluate messages.append(translated “{} has been disabled. It can only be enabled if {} is checked.”.format(Platform.bold(translated “Default Outgoing”), Platform.bold(translated “Enable Outgoing”))).
- If messages.
  - If len(messages) equals 1.
    - Set tuple(as\_list, messages) from tuple(0, messages at 0).
  - Evaluate Platform.msgprint(messages, as\_list = as\_list, indicator = “orange”, title = translated “Defaults Updated”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L4406) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1640)

<a id="op-a86de12b034fcd"></a>
### Email Account.on update

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.check\_automatic\_linking\_email\_account().
- Evaluate self.there\_must\_be\_only\_one\_default().
- Evaluate setup\_user\_email\_inbox(email\_account = self.name, awaiting\_password = self.awaiting\_password, email\_id = self.email\_id, enable\_outgoing = self.enable\_outgoing, …).
- If (before bound to self.get\_doc\_before\_save() and before.connected\_app differs from self.connected\_app).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before bound to self.get\_doc\_before\_save() → before.connected\_app differs from self.connected\_app.
  - Bind dependencies delete\_relay\_app.
  - Evaluate delete\_relay\_app(before.connected\_app).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check automatic linking email account](operations-011.md#op-050d37a2fbfa13), [there must be only one default](operations-009.md#op-07cc874c2a945f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L94) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L13)

<a id="op-9a5cb3535144a5"></a>
### Email Account.clear cache

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- Evaluate Platform.client\_cache.delete\_value(“automatic\_linking\_email”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L5119) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1644)

<a id="op-07cc874c2a945f"></a>
### Email Account.there must be only one default

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_there_must_be_only_one_default`

**Inputs** self.

**State and service calls** request set\_value on “Email Account”.

**Local steps**

- For each field in tuple(“default\_incoming”, “default\_outgoing”).
  - If self.get(field).
    - Evaluate Platform.db.set\_value(“Email Account”, mapping(field → 1, “name” → tuple(“!=”, self.name)), field, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L95) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L21)

<a id="op-59f7c4255a6a10"></a>
### Email Account.get domain values

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_domain_values`

**Inputs** self, domain.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Email Domain” via get\_value.

**Explicit results** Platform.db.get\_value(“Email Domain”, domain, EMAIL\_DOMAIN\_FIELDS, as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(“Email Domain”, “read”, domain, throw = true).
- Return Platform.db.get\_value(“Email Domain”, domain, EMAIL\_DOMAIN\_FIELDS, as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Email Domain”, “read”, domain, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L93) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1660)

<a id="op-0caa3ac947a329"></a>
### Email Account.get incoming server

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_incoming_server`

**Inputs** self, in\_receive = false, email\_sync\_rule = “UNSEEN”.

**Explicit results** email\_server.

**Explicit failure paths** validation helper — translated “{0} is required”.format(“Email Server”).

**Local steps**

- Set oauth\_token from self.get\_oauth\_token().
- Set args from Platform.\_dict(mapping(“email\_account\_name” → self.email\_account\_name, “email\_account” → self.name, “host” → self.email\_server, “use\_ssl” → self.use\_ssl, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self, “login\_id”, no value) → self.email\_id.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.initial\_sync\_count → 100.
  - Value choice on oauth\_token — true gives oauth\_token.get\_password(“access\_token”), false gives no value.
- If self.password.
  - Set args.password from self.get\_password().
- If not args.get(“host”).
  - Call the validation error handler Platform.throw(translated “{0} is required”.format(“Email Server”)).
- If self.flags.validate\_imap\_pop\_connection.
  - Set args.timeout from 30.
- Set email\_server from EmailServer(Platform.\_dict(args)).
- Evaluate self.check\_email\_server\_connection(email\_server, in\_receive).
- If (not in\_receive and self.use\_imap).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not in\_receive → self.use\_imap.
  - Evaluate email\_server.imap.logout().
- Return email\_server.

**Methods declared on this owner** [get oauth token](operations-011.md#op-657adb515d10d8), [check email server connection](operations-009.md#op-3ba9ae1c7ba44b).

**Values supplied outside this operation** selected callable from getattr(self, “login\_id”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0220.json#L5599) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L6)

<a id="op-3ba9ae1c7ba44b"></a>
### Email Account.check email server connection

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_check_email_server_connection`

**Inputs** self, email\_server, in\_receive.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — cstr(e) · propagate active failure.

**Local steps**

- Set is\_background\_receive from (in\_receive and not bool(self.flags.validate\_imap\_pop\_connection)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_receive → not bool(self.flags.validate\_imap\_pop\_connection).
- Attempt the following.
  - Evaluate email\_server.connect().
  - Evaluate self.set\_failed\_attempts\_count(0).
- On failure (tuple(error\_proto, imaplib.IMAP4.error)) bound to e.
  - Set message from cstr(e).lower().replace(one space, empty text).
  - Set auth\_error\_codes from list(“authenticationfailed”, “loginfailed”).
  - Set other\_error\_codes from list(“err&#91;auth&#93;”, “errtemporaryerror”, “loginviayourwebbrowser”).
  - Set all\_error\_codes from (auth\_error\_codes + other\_error\_codes).
  - If (is\_background\_receive and any(generator of t belongs to message for t drawn from all\_error\_codes)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_background\_receive → any(generator of t belongs to message for t drawn from all\_error\_codes).
    - Draw t from all\_error\_codes.
    - Set error\_message from translated “Authentication failed while receiving emails from Email Account: {0}.”.format(self.name).
    - Set error\_message from ((translated “Email Account Disabled.” + one space) + error\_message).
    - Update error\_message using + (text in the contract + translated “Message from server: {0}”.format(cstr(e))).
    - Evaluate self.handle\_incoming\_connect\_error(description = error\_message).
    - Return no value.
  - Otherwise.
    - If (not is\_background\_receive and any(generator of t belongs to message for t drawn from auth\_error\_codes)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_background\_receive → any(generator of t belongs to message for t drawn from auth\_error\_codes).
      - Draw t from auth\_error\_codes.
      - Evaluate SMTPServer.throw\_invalid\_credentials\_exception().
    - Otherwise.
      - Call the validation error handler Platform.throw(cstr(e)).
- On failure (OSError).
  - If is\_background\_receive.
    - Set description from Platform.message\_log.pop() when Platform.message\_log, otherwise “Socket Error”.
      - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives “Socket Error”.
    - Evaluate self.db\_set(“no\_failed”, (self.no\_failed + 1)).
    - If self.no\_failed &gt; 2.
      - Evaluate self.handle\_incoming\_connect\_error(description = description).
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set failed attempts count](operations-010.md#op-fa77494b08718f), [handle incoming connect error](operations-010.md#op-f81421baa2cf20).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L90) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1643)

<a id="op-c2b0660d64145f"></a>
### Email Account.password

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L864) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L14)

<a id="op-cbc76bf1744e71"></a>
### Email Account.default sender

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_default_sender`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** email.utils.formataddr(tuple(self.name, self.get(“email\_id”))).

**Local steps**

- Return email.utils.formataddr(tuple(self.name, self.get(“email\_id”))).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L987) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1646)

<a id="op-c28aa89643be36"></a>
### Email Account.is exists in db

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_is_exists_in_database`

**Inputs** self.

**Explicit results** self.find\_one\_by\_filters(name = self.name).

**Local steps**

- Return self.find\_one\_by\_filters(name = self.name).

**Methods declared on this owner** [find one by filters](operations-010.md#op-5753d39fe68d3d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1086) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L11)
