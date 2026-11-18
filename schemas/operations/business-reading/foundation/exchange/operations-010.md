# Integration and transport · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email account

[Record definition](../../../../data/record-types/email_account.json)

<a id="op-19459a94e29c04"></a>
### Email Account.from record

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_from_record`

**Inputs** cls, record.

**Wrappers, in declaration order** classmethod.

**State and service calls** request new\_doc for cls.DOCTYPE.

**Explicit results** email\_account.

**Local steps**

- Set email\_account from Platform.new\_doc(cls.DOCTYPE).
- Evaluate email\_account.update(record).
- Return email\_account.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1153) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1656)

<a id="op-f02ec19fdb7232"></a>
### Email Account.find

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find`

**Inputs** cls, name.

**Wrappers, in declaration order** classmethod.

**Record and data access** resolve a document from cls.DOCTYPE via get\_doc.

**Explicit results** Platform.get\_doc(cls.DOCTYPE, name).

**Local steps**

- Return Platform.get\_doc(cls.DOCTYPE, name).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1259) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1648)

<a id="op-5753d39fe68d3d"></a>
### Email Account.find one by filters

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_one_by_filters`

**Inputs** cls, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** “EmailAccount”.

**Record and data access** read cls.DOCTYPE via get\_value.

**Explicit results** cls.find(name) when name, otherwise no value.

**Local steps**

- Set name from Platform.db.get\_value(cls.DOCTYPE, kwargs).
- Return cls.find(name) when name, otherwise no value.
  - Value choice on name — true gives cls.find(name), false gives no value.

**Methods declared on this owner** [find](operations-010.md#op-f02ec19fdb7232).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1333) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1653)

<a id="op-92e6fee7593e54"></a>
### Email Account.find from config

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_from_configuration`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** account.

**Local steps**

- Set config from cls.get\_account\_details\_from\_site\_config().
- If config.
  - Set account from cls.from\_record(config).
  - Set account.\_from\_site\_config from true.
  - Return account.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get account details from site config](operations-010.md#op-75f84b39f1897c), [from record](operations-010.md#op-19459a94e29c04).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1456) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1651)

<a id="op-33efccdebd4662"></a>
### Email Account.create dummy

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_create_dummy`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.from\_record(mapping(“name” → “Notifications”, “email\_id” → “notifications@example.com”)).

**Local steps**

- Return cls.from\_record(mapping(“name” → “Notifications”, “email\_id” → “notifications@example.com”)).

**Methods declared on this owner** [from record](operations-010.md#op-19459a94e29c04).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L1583) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1645)

<a id="op-297b3e00b4cf91"></a>
### Email Account.find outgoing

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_outgoing`

**Inputs** cls, match\_by\_email = no value, match\_by\_doctype = no value, \_raise\_error = false.

**Wrappers, in declaration order** classmethod, cache\_email\_account(“outgoing\_email\_account”).

**Explicit results** doc.

**Explicit failure paths** validation helper with Platform.OutgoingEmailError — translated “Please setup default outgoing Email Account from Tools &gt; Email Account”.

**Local steps**

- If match\_by\_email.
  - Set match\_by\_email from parse\_addr(match\_by\_email) at 1.
  - Set doc from cls.find\_one\_by\_filters(enable\_outgoing = 1, email\_id = match\_by\_email).
  - If doc.
    - Return doc.
- If match\_by\_doctype.
  - Set doc from cls.find\_one\_by\_filters(enable\_outgoing = 1, enable\_incoming = 1, append\_to = match\_by\_doctype).
  - If doc.
    - Return doc.
- Set doc from cls.find\_default\_outgoing().
- If doc.
  - Return doc.
- If \_raise\_error.
  - Call the validation error handler Platform.throw(translated “Please setup default outgoing Email Account from Tools &gt; Email Account”, Platform.OutgoingEmailError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [find one by filters](operations-010.md#op-5753d39fe68d3d), [find default outgoing](operations-010.md#op-210e4e43f3c5d8).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L91) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1654)

<a id="op-210e4e43f3c5d8"></a>
### Email Account.find default outgoing

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_default_outgoing`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** (doc or (are\_emails\_muted() and cls.create\_dummy())).

**Local steps**

- Set doc from cls.find\_one\_by\_filters(enable\_outgoing = 1, default\_outgoing = 1).
- Set doc from (doc or cls.find\_from\_config()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → cls.find\_from\_config().
- Return (doc or (are\_emails\_muted() and cls.create\_dummy())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → (are\_emails\_muted() and cls.create\_dummy()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in are\_emails\_muted() → cls.create\_dummy().

**Methods declared on this owner** [find one by filters](operations-010.md#op-5753d39fe68d3d), [find from config](operations-010.md#op-92e6fee7593e54), [create dummy](operations-010.md#op-33efccdebd4662).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L2089) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1650)

<a id="op-c3b54b875a9a2d"></a>
### Email Account.find incoming

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_incoming`

**Inputs** cls, match\_by\_email = no value, match\_by\_doctype = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** doc.

**Local steps**

- If doc bound to cls.find\_default\_incoming().
  - Return doc.
- If (match\_by\_email and doc bound to cls.find\_one\_by\_filters(enable\_incoming = 1, email\_id = match\_by\_email)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in match\_by\_email → doc bound to cls.find\_one\_by\_filters(enable\_incoming = 1, email\_id = match\_by\_email).
  - Return doc.
- If (match\_by\_doctype and doc bound to cls.find\_one\_by\_filters(enable\_incoming = 1, append\_to = match\_by\_doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in match\_by\_doctype → doc bound to cls.find\_one\_by\_filters(enable\_incoming = 1, append\_to = match\_by\_doctype).
  - Return doc.

If control reaches the end, it returns no value.

**Methods declared on this owner** [find default incoming](operations-010.md#op-56501afbe61f36), [find one by filters](operations-010.md#op-5753d39fe68d3d).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L2255) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1652)

<a id="op-56501afbe61f36"></a>
### Email Account.find default incoming

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_find_default_incoming`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls.find\_one\_by\_filters(enable\_incoming = 1, default\_incoming = 1).

**Local steps**

- Return cls.find\_one\_by\_filters(enable\_incoming = 1, default\_incoming = 1).

**Methods declared on this owner** [find one by filters](operations-010.md#op-5753d39fe68d3d).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L2479) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1649)

<a id="op-75f84b39f1897c"></a>
### Email Account.get account details from site config

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_account_details_from_site_configuration`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Explicit results** mapping() · account\_details.

**Local steps**

- If not Platform.conf.get(“mail\_server”).
  - Return mapping().
- Set field\_to\_conf\_name\_map from mapping(“smtp\_server” → mapping(“conf\_names” → tuple(“mail\_server”)), “smtp\_port” → mapping(“conf\_names” → tuple(“mail\_port”)), “use\_tls” → mapping(“conf\_names” → tuple(“use\_tls”, “mail\_login”)), “use\_ssl\_ ….
- Set account\_details from mapping().
- For each tuple(doc\_field\_name, d) in field\_to\_conf\_name\_map.items().
  - Set tuple(conf\_names, default) from tuple((d.get(“conf\_names”) or list()), d.get(“default”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“conf\_names”) → list().
  - Set value from list of Platform.conf.get(k) for k drawn from conf\_names where Platform.conf.get(k).
    - Draw k from conf\_names, keep a combination only if (Platform.conf.get(k)).
  - Set account\_details at doc\_field\_name from ((value and value at 0) or default).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (value and value at 0) → default.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → value at 0.
- Return account\_details.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L92) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1658)

<a id="op-7643711ef0b33e"></a>
### Email Account.get access token

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L3408) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1657)

<a id="op-c7068b27a4375e"></a>
### Email Account.sendmail config

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_sendmail_configuration`

**Inputs** self.

**Explicit results** config.

**Local steps**

- Set config from mapping(“email\_account” → self.name, “server” → self.smtp\_server, “port” → cint(self.smtp\_port), “login” → (getattr(self, “login\_id”, no value) or self.email\_id), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self, “login\_id”, no value) → self.email\_id.
- If self.flags.validate\_smtp\_connection.
  - Set config at “timeout” from 15.
- Return config.

**Methods declared on this owner** [get access token](operations-010.md#op-7643711ef0b33e).

**Values supplied outside this operation** selected callable from getattr(self, “login\_id”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L3514) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L18)

<a id="op-c379b562ab3430"></a>
### Email Account.get smtp server

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_simple_mail_transfer_protocol_server`

**Inputs** self.

**Explicit results** self.\_smtp\_server\_instance.

**Local steps**

- Return self.\_smtp\_server\_instance.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L3882) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L7)

<a id="op-fb052f19f29811"></a>
### Email Account.smtp server instance

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_simple_mail_transfer_protocol_server_instance`

**Inputs** self.

**Wrappers, in declaration order** functools.cached\_property.

**Explicit results** SMTPServer(expanded names config).

**Local steps**

- Set config from self.sendmail\_config().
- Return SMTPServer(expanded names config).

**Methods declared on this owner** [sendmail config](operations-010.md#op-c7068b27a4375e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L3923) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L20)

<a id="op-6e4ea5f9baa267"></a>
### Email Account.get Platform mail client

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_foundation_mail_client`

**Inputs** self.

**Explicit results** self.\_Platform\_mail\_client.

**Local steps**

- Return self.\_Platform\_mail\_client.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4013) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L3)

<a id="op-ab53857c4d59ee"></a>
### Email Account.Platform mail client

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_foundation_mail_client`

**Inputs** self.

**Wrappers, in declaration order** functools.cached\_property.

**Explicit results** PlatformMail(self.Platform\_mail\_site, self.email\_id, access\_token = access\_token) · PlatformMail(self.Platform\_mail\_site, self.email\_id, self.api\_key, self.get\_password(“api\_secret”)).

**Explicit failure paths** validation helper — translated “Please Authorize OAuth for Email Account {0}”.format(Platform.bold(self.email\_account\_name)).

**Local steps**

- If self.auth\_method equals “OAuth”.
  - If access\_token bound to self.get\_access\_token().
    - Return PlatformMail(self.Platform\_mail\_site, self.email\_id, access\_token = access\_token).
  - Call the validation error handler Platform.throw(translated “Please Authorize OAuth for Email Account {0}”.format(Platform.bold(self.email\_account\_name)), title = translated “Platform Mail OAuth Error”).
- Otherwise.
  - Return PlatformMail(self.Platform\_mail\_site, self.email\_id, self.api\_key, self.get\_password(“api\_secret”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get access token](operations-010.md#op-7643711ef0b33e).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4054) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1655)

<a id="op-d56eabdede3866"></a>
### Email Account.remove unpicklable values

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_remove_unpicklable_values`

**Inputs** self, state.

**Local steps**

- Evaluate super().remove\_unpicklable\_values(state).
- Evaluate state.pop(“\_smtp\_server\_instance”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4365) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L16)

<a id="op-f81421baa2cf20"></a>
### Email Account.handle incoming connect error

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_handle_incoming_connect_error`

**Inputs** self, description.

**State and service calls** enqueue with self.\_disable\_broken\_incoming\_account.

**Local steps**

- If self.get\_failed\_attempts\_count() &gt; 5.
  - Evaluate Platform.enqueue(self.\_disable\_broken\_incoming\_account, description = description).
- Otherwise.
  - Evaluate self.set\_failed\_attempts\_count((self.get\_failed\_attempts\_count() + 1)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get failed attempts count](operations-010.md#op-fec71805385c5f), [set failed attempts count](operations-010.md#op-fa77494b08718f).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.\_disable\_broken\_incoming\_account, description = description).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4459) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L10)

<a id="op-d912c75d92a837"></a>
### Email Account.disable broken incoming account

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_disable_broken_incoming_account`

**Inputs** self, description.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If Platform.in\_test.
  - Return no value.
- Evaluate self.db\_set(“enable\_incoming”, 0).
- Set users from get\_system\_managers(only\_name = true).
- Set notification from mapping(“document\_type” → self.doctype, “document\_name” → self.name, “subject” → description, “from\_user” → “Administrator”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.email\_id → self.name.
- Evaluate enqueue\_create\_notification(users, notification).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4616) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1647)

<a id="op-fa77494b08718f"></a>
### Email Account.set failed attempts count

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_set_failed_attempts_count`

**Inputs** self, value.

**Local steps**

- Evaluate Platform.cache.set\_value(formatted text {self.name}:email-account-failed-attempts, value, expires\_in\_sec = ((2 × 60) × 60)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L4919) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L19)

<a id="op-fec71805385c5f"></a>
### Email Account.get failed attempts count

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_failed_attempts_count`

**Inputs** self.

**Explicit results** cint(Platform.cache.get\_value(formatted text {self.name}:email-account-failed-attempts)).

**Local steps**

- Return cint(Platform.cache.get\_value(formatted text {self.name}:email-account-failed-attempts)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L5036) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L2)

<a id="op-7cfd8da9d221dd"></a>
### Email Account.receive

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_receive`

**Inputs** self.

**State and service calls** commit · rollback.

**Explicit failure paths** Exception(Platform.as\_json(exceptions)).

**Local steps**

- Set exceptions from list().
- Set inbound\_mails from self.get\_inbound\_mails().
- For each mail in inbound\_mails.
  - Attempt the following.
    - Set communication from mail.process().
    - Evaluate Platform.db.commit().
    - If (communication and mail.flags.is\_new\_communication).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in communication → mail.flags.is\_new\_communication.
      - If self.enable\_auto\_reply.
        - Evaluate self.send\_auto\_reply(communication, mail).
      - Evaluate communication.send\_email(is\_inbound\_mail\_communcation = true).
  - On failure (SentEmailInInboxError).
    - Evaluate Platform.db.rollback().
  - On failure (Exception).
    - Evaluate Platform.db.rollback().
    - Attempt the following.
      - Evaluate self.log\_error(title = “EmailAccount.receive”).
      - If self.use\_imap.
        - Evaluate self.handle\_bad\_emails(mail.uid, mail.raw\_message, Platform.get\_traceback()).
      - Evaluate exceptions.append(Platform.get\_traceback()).
    - On failure (Exception).
      - Evaluate Platform.db.rollback().
    - When the protected block completes normally.
      - Evaluate Platform.db.commit().
  - When the protected block completes normally.
    - Evaluate Platform.db.commit().
- If exceptions.
  - Raise Exception(Platform.as\_json(exceptions)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get inbound mails](operations-010.md#op-d815f92d1548ce), [send auto reply](operations-011.md#op-c3411a54fa9720), [handle bad emails](operations-011.md#op-e398e36c3a7b86).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L5131) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L15)

<a id="op-d815f92d1548ce"></a>
### Email Account.get inbound mails

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_inbound_mails`

**Inputs** self.

**Declared result** list at InboundMail.

**State and service calls** call db\_set on self.

**Explicit results** list() · mails.

**Local steps**

- Set mails from list().
- Bind local operation process\_mail for subsequent calls.
- If not self.enable\_incoming.
  - Return list().
- Attempt the following.
  - If self.service equals “Platform Mail”.
    - Set Platform\_mail\_client from self.get\_Platform\_mail\_client().
    - Set messages from Platform\_mail\_client.pull\_raw(last\_received\_at = self.last\_received\_at).
    - Evaluate process\_mail(messages).
    - Evaluate self.db\_set(“last\_received\_at”, messages at “last\_received\_at”, update\_modified = false).
  - Otherwise.
    - Set email\_sync\_rule from self.build\_email\_sync\_rule().
    - Set email\_server from self.get\_incoming\_server(in\_receive = true, email\_sync\_rule = email\_sync\_rule).
    - If self.use\_imap.
      - For each folder in self.imap\_folder.
        - If email\_server.select\_imap\_folder(folder.folder\_name).
          - Set email\_server.settings at “uid\_validity” from folder.uidvalidity.
          - Set messages from (email\_server.get\_messages(folder = formatted text "{folder.folder\_name}") or mapping()).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_server.get\_messages(folder = formatted text "{folder.folder\_name}") → mapping().
          - Evaluate process\_mail(messages, folder.append\_to).
    - Otherwise.
      - Set messages from (email\_server.get\_messages() or mapping()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_server.get\_messages() → mapping().
      - Evaluate process\_mail(messages).
    - Evaluate email\_server.logout().
- On failure (Exception).
  - Evaluate self.log\_error(title = translated “Error while connecting to email account {0}”.format(self.name)).
  - Return list().
- Return mails.

**Methods declared on this owner** [get Platform mail client](operations-010.md#op-6e4ea5f9baa267), [build email sync rule](operations-011.md#op-c8633881009633), [get incoming server](operations-009.md#op-0caa3ac947a329).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0221.json#L5703) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L4)

<a id="op-4f742cd91523e0"></a>
### Email Account.get inbound mails.process mail

`operation_foundation_email_record_definitions_email_account_business_behavior_email_account_get_inbound_mails_process_mail`

**Inputs** messages, append\_to = no value.

**Local steps**

- For each tuple(index, message) in enumerate(messages.get(“latest\_messages”, list())).
  - Set uid from messages at “uid\_list” at index when messages.get(“uid\_list”), otherwise no value.
    - Value choice on messages.get(“uid\_list”) — true gives messages at “uid\_list” at index, false gives no value.
  - Set seen\_status from messages.get(“seen\_status”, mapping()).get(uid).
  - If (self.email\_sync\_option differs from “UNSEEN” or seen\_status differs from “SEEN”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.email\_sync\_option differs from “UNSEEN” → seen\_status differs from “SEEN”.
    - Evaluate mails.append(InboundMail(message, self, Platform.safe\_decode(uid), seen\_status, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0222.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L5)
