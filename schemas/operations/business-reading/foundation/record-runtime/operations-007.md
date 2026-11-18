# Record lifecycle and persistence · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Communication

[Record definition](../../../../data/record-types/communication.json)

<a id="op-321fb4243aef13"></a>
### Communication Email Mixin.mail sender fullname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_sender_fullname`

**Inputs** self.

**Explicit results** ((email\_account and email\_account.name) or translated “Notification”) · self.sender\_full\_name.

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- If not self.sender\_full\_name.
  - Return ((email\_account and email\_account.name) or translated “Notification”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (email\_account and email\_account.name) → translated “Notification”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.name.
- Return self.sender\_full\_name.

**Methods declared on this owner** [get outgoing email account](operations-007.md#op-905f124b7baa4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5301) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1083)

<a id="op-5d4221178377f8"></a>
### Communication Email Mixin.get mail sender with displayname

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_mail_sender_with_displayname`

**Inputs** self.

**Explicit results** get\_formatted\_email(self.mail\_sender\_fullname(), mail = self.mail\_sender()).

**Local steps**

- Return get\_formatted\_email(self.mail\_sender\_fullname(), mail = self.mail\_sender()).

**Methods declared on this owner** [mail sender fullname](operations-007.md#op-321fb4243aef13), [mail sender](operations-006.md#op-741f889ef35771).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5439) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1072)

<a id="op-15dc01ec825f2f"></a>
### Communication Email Mixin.get content

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_content`

**Inputs** self, print\_format = no value.

**Explicit results** (cstr(self.content) + self.get\_attach\_link(print\_format)) · self.content.

**Local steps**

- If (print\_format and Platform.get\_system\_settings(“attach\_view\_link”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format → Platform.get\_system\_settings(“attach\_view\_link”).
  - Return (cstr(self.content) + self.get\_attach\_link(print\_format)).
- Return self.content.

**Methods declared on this owner** [get attach link](operations-007.md#op-1afd487d80b7c1).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“attach\_view\_link”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5528) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1066)

<a id="op-1afd487d80b7c1"></a>
### Communication Email Mixin.get attach link

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_attach_link`

**Inputs** self, print\_format.

**Explicit results** Platform.get\_template(“templates/emails/print\_link.html”).render(mapping(“url” → get\_url(), “doctype” → self.reference\_doctype, “name” → self.reference\_name, “print\_format” → print\_format, …)).

**Local steps**

- Return Platform.get\_template(“templates/emails/print\_link.html”).render(mapping(“url” → get\_url(), “doctype” → self.reference\_doctype, “name” → self.reference\_name, “print\_format” → print\_format, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5673) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1065)

<a id="op-905f124b7baa4d"></a>
### Communication Email Mixin.get outgoing email account

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_outgoing_email_account`

**Inputs** self.

**Record and data access** read “Email Account” via exists.

**State and service calls** call db\_set on self.

**Explicit results** self.\_outgoing\_email\_account.

**Local steps**

- If not hasattr(self, “\_outgoing\_email\_account”).
  - If self.email\_account.
    - Set self.\_outgoing\_email\_account from EmailAccount.find(self.email\_account).
  - Otherwise.
    - Set self.\_outgoing\_email\_account from EmailAccount.find\_outgoing(match\_by\_email = self.sender\_mailid, match\_by\_doctype = self.reference\_doctype).
    - If (self.sent\_or\_received equals “Sent” and self.\_outgoing\_email\_account).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sent\_or\_received equals “Sent” → self.\_outgoing\_email\_account.
      - If Platform.db.exists(“Email Account”, self.\_outgoing\_email\_account.name).
        - Evaluate self.db\_set(“email\_account”, self.\_outgoing\_email\_account.name).
- Return self.\_outgoing\_email\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L5876) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1074)

<a id="op-69b8db1e6c3769"></a>
### Communication Email Mixin.get incoming email account

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_incoming_email_account`

**Inputs** self.

**Explicit results** self.\_incoming\_email\_account.

**Local steps**

- If not hasattr(self, “\_incoming\_email\_account”).
  - Set self.\_incoming\_email\_account from EmailAccount.find\_incoming(match\_by\_email = self.sender\_mailid, match\_by\_doctype = self.reference\_doctype).
- Return self.\_incoming\_email\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L6186) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1068)

<a id="op-ce7bef9204d731"></a>
### Communication Email Mixin.mail attachments

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_mail_attachments`

**Inputs** self, print\_format = no value, print\_html = no value, print\_language = no value, letterhead = no value, print\_style = no value, print\_settings = no value.

**Explicit results** final\_attachments.

**Local steps**

- Set final\_attachments from list().
- If (print\_format or print\_html).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format → print\_html.
  - Set d from mapping(“print\_format” → print\_format, “html” → print\_html, “print\_format\_attachment” → 1, “print\_as\_owner” → 1, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_language → Platform.local.lang.
  - If print\_style.
    - Set d at “style” from print\_style.
  - If print\_settings.
    - Set d at “settings” from print\_settings.
  - Evaluate final\_attachments.append(d).
- Evaluate final\_attachments.extend(generator of mapping(“fid” → a at “name”) for a drawn from (self.get\_attachments() or list())).
  - Draw a from (self.get\_attachments() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_attachments() → list().
- Return final\_attachments.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L3) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1078)

<a id="op-66cfae8dd1e671"></a>
### Communication Email Mixin.get unsubscribe message

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_unsubscribe_message`

**Inputs** self.

**Explicit results** translated “Leave this conversation” · empty text.

**Local steps**

- Set email\_account from self.get\_outgoing\_email\_account().
- If (email\_account and email\_account.send\_unsubscribe\_message).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.send\_unsubscribe\_message.
  - Return translated “Leave this conversation”.
- Return empty text.

**Methods declared on this owner** [get outgoing email account](operations-007.md#op-905f124b7baa4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L6670) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1076)

<a id="op-13e003c80ddb66"></a>
### Communication Email Mixin.exclude emails list

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_exclude_emails_list`

**Inputs** self, is\_inbound\_mail\_communcation = false, include\_sender = false.

**Declared result** list.

**Explicit results** list((set(all\_ids) − set(final\_ids))).

**Local steps**

- Set all\_ids from self.get\_all\_email\_addresses(exclude\_displayname = true).
- Set final\_ids from ((self.mail\_recipients(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation) + self.mail\_bcc(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation)) + self.mail\_cc(is\_inbound\_mail\_communcation ….
- Return list((set(all\_ids) − set(final\_ids))).

**Methods declared on this owner** [get all email addresses](operations-006.md#op-adffd53c59eabf), [mail recipients](operations-006.md#op-3f1e970b01df98), [mail bcc](operations-006.md#op-08feae944867e8), [mail cc](operations-006.md#op-84a26ca214b8ad).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L6779) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1060)

<a id="op-34776eefaaa410"></a>
### Communication Email Mixin.get assignees

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_get_assignees`

**Inputs** self.

**Explicit results** ToDo.get\_owners(filters) · list().

**Local steps**

- Set filters from mapping(“status” → “Open”, “reference\_name” → self.reference\_name, “reference\_type” → self.reference\_doctype).
- If (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Return ToDo.get\_owners(filters).
- Otherwise.
  - Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L7033) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1064)

<a id="op-9581ad50dcc78b"></a>
### Communication Email Mixin.filter thread notification disbled users

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_filter_thread_notification_disbled_users`

**Inputs** emails.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “User” via get\_all.

**Explicit results** list() · Platform.get\_all(“User”, pluck = “email”, filters = mapping(“email” → list(“in”, emails), “thread\_notify” → 0)).

**Local steps**

- If not emails.
  - Return list().
- Return Platform.get\_all(“User”, pluck = “email”, filters = mapping(“email” → list(“in”, emails), “thread\_notify” → 0)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0044.json#L7193) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1062)

<a id="op-866fcb8218a1af"></a>
### Communication Email Mixin.filter disabled users

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_filter_disabled_users`

**Inputs** emails.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “User” via get\_all.

**Explicit results** list() · Platform.get\_all(“User”, pluck = “email”, filters = mapping(“email” → list(“in”, emails), “enabled” → 0)).

**Local steps**

- If not emails.
  - Return list().
- Return Platform.get\_all(“User”, pluck = “email”, filters = mapping(“email” → list(“in”, emails), “enabled” → 0)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0045.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1061)

<a id="op-f6b63b90784a0a"></a>
### Communication Email Mixin.sendmail input dict

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_sendmail_input_mapping`

**Inputs** self, print\_html = no value, print\_format = no value, send\_me\_a\_copy = no value, print\_letterhead = no value, letterhead = no value, is\_inbound\_mail\_communcation = no value, print\_language = no value, raw\_html = false, add\_css = true, print\_style = no value, print\_settings = no value.

**Declared result** dict.

**Explicit results** mapping() · mapping(“recipients” → recipients, “cc” → cc, “bcc” → bcc, “expose\_recipients” → “header”, …).

**Local steps**

- Set outgoing\_email\_account from self.get\_outgoing\_email\_account().
- If not outgoing\_email\_account.
  - Return mapping().
- Set recipients from self.get\_mail\_recipients\_with\_displayname(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation).
- Set cc from self.get\_mail\_cc\_with\_displayname(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation, include\_sender = send\_me\_a\_copy).
- Set bcc from self.get\_mail\_bcc\_with\_displayname(is\_inbound\_mail\_communcation = is\_inbound\_mail\_communcation).
- If not (recipients or cc or bcc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in recipients → cc → bcc.
  - Return mapping().
- Set final\_attachments from self.mail\_attachments(print\_format = print\_format, print\_html = print\_html, print\_language = print\_language, letterhead = letterhead, …).
- Set incoming\_email\_account from self.get\_incoming\_email\_account().
- Set reply\_to from no value.
- If self.in\_reply\_to.
  - Set reply\_to from self.get\_mail\_sender\_with\_displayname().
- Otherwise.
  - If incoming\_email\_account.
    - Set reply\_to from incoming\_email\_account.email\_id.
- Return mapping(“recipients” → recipients, “cc” → cc, “bcc” → bcc, “expose\_recipients” → “header”, …).

**Methods declared on this owner** [get outgoing email account](operations-007.md#op-905f124b7baa4d), [get mail recipients with displayname](operations-006.md#op-718175013ad16e), [get mail cc with displayname](operations-006.md#op-d0e3c685e8daf4), [get mail bcc with displayname](operations-006.md#op-65662a29523b45), [mail attachments](operations-007.md#op-ce7bef9204d731), [get incoming email account](operations-007.md#op-69b8db1e6c3769), [get mail sender with displayname](operations-007.md#op-5d4221178377f8), [get content](operations-007.md#op-15dc01ec825f2f), [get unsubscribe message](operations-007.md#op-66cfae8dd1e671).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L5) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1085)

<a id="op-cd96e3ead080fb"></a>
### Communication Email Mixin.send email

`operation_foundation_core_record_definitions_communication_mixins_business_behavior_communication_email_mixin_send_email`

**Inputs** self, print\_html = no value, print\_format = no value, send\_me\_a\_copy = no value, print\_letterhead = no value, letterhead = no value, is\_inbound\_mail\_communcation = no value, print\_language = no value, now = false, raw\_html = false, add\_css = true, print\_style = no value, print\_settings = no value.

**State and service calls** sendmail.

**Local steps**

- If input\_dict bound to self.sendmail\_input\_dict(print\_html = print\_html, print\_format = print\_format, send\_me\_a\_copy = send\_me\_a\_copy, print\_letterhead = print\_letterhead, …).
  - Evaluate Platform.sendmail(now = now, expanded names input\_dict).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sendmail input dict](operations-007.md#op-f6b63b90784a0a).

**Values supplied outside this operation** service or queued work from Platform.sendmail(now = now, expanded names input\_dict).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L4) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1084)

## Record · Communication link

[Record definition](../../../../data/record-types/communication_link.json)

<a id="op-22ae9d6bf179a0"></a>
### On doctype update

`operation_foundation_core_record_definitions_communication_link_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Communication Link”.

**Local steps**

- Evaluate Platform.db.add\_index(“Communication Link”, list(“link\_doctype”, “link\_name”)).
- Evaluate Platform.db.add\_index(“Communication Link”, list(“link\_doctype”, “link\_name”, “communication\_date”, “parent”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0047.json#L3014) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1058)

## Service · Create new

<a id="op-1d063ca5de20dc"></a>
### Get new doc

`operation_foundation_model_create_new_business_behavior_get_new_record`

**Inputs** doctype, parent\_doc = no value, parentfield = no value, as\_dict = false.

**Record and data access** resolve a document from doc via get\_doc.

**Explicit results** doc · Platform.get\_doc(doc).

**Local steps**

- If doctype does not belong to Platform.local.new\_doc\_templates.
  - Set Platform.local.new\_doc\_templates at doctype from make\_new\_doc(doctype).
- Set doc from copy.deepcopy(Platform.local.new\_doc\_templates at doctype).
- Evaluate set\_dynamic\_default\_values(doc, parent\_doc, parentfield).
- If as\_dict.
  - Return doc.
- Otherwise.
  - Return Platform.get\_doc(doc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0268.json#L5801) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L912)

<a id="op-a4cee88d0034a1"></a>
### Make new doc

`operation_foundation_model_create_new_business_behavior_make_new_record`

**Inputs** doctype.

**Record and data access** resolve a document from mapping(“doctype” → doctype, “\_\_islocal” → 1, “owner” → Platform.session.user, “docstatus” → 0) via get\_doc.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.get\_doc(mapping(“doctype” → doctype, “\_\_islocal” → 1, “owner” → Platform.session.user, “docstatus” → 0)).
- Evaluate set\_user\_and\_static\_default\_values(doc).
- Evaluate doc.\_fix\_numeric\_types().
- Set doc from doc.get\_valid\_dict(sanitize = false).
- Set doc at “doctype” from doctype.
- Set doc at “\_\_islocal” from 1.
- If not getattr(doc.meta, “issingle”, false).
  - Set doc at “\_\_unsaved” from 1.
- Return doc.

**Values supplied outside this operation** selected callable from getattr(doc.meta, “issingle”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L69) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L915)

<a id="op-38adfd6dd4e5ce"></a>
### Set user and static default values

`operation_foundation_model_create_new_business_behavior_set_user_and_static_default_values`

**Inputs** doc.

**Record and data access** read df.options via exists.

**Local steps**

- Set user\_permissions from get\_user\_permissions().
- Set defaults from Platform.defaults.get\_defaults().
- For each df in doc.meta.get(“fields”).
  - If df.fieldtype belongs to data\_fieldtypes.
    - Set doctype\_user\_permissions from user\_permissions.get(df.options, list()).
    - Set tuple(allowed\_records, default\_doc) from filter\_allowed\_docs\_for\_doctype(doctype\_user\_permissions, df.parent, with\_default\_doc = true).
    - Set user\_default\_value from get\_user\_default\_value(df, defaults, doctype\_user\_permissions, allowed\_records, …).
    - If user\_default\_value is distinct from no value.
      - If (df.fieldtype differs from “Link” or Platform.db.exists(df.options, user\_default\_value, cache = true)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype differs from “Link” → Platform.db.exists(df.options, user\_default\_value, cache = true).
        - Evaluate doc.set(df.fieldname, user\_default\_value).
    - Otherwise.
      - If df.fieldname differs from doc.meta.title\_field.
        - Set static\_default\_value from get\_static\_default\_value(df, doctype\_user\_permissions, allowed\_records).
        - If static\_default\_value is distinct from no value.
          - Evaluate doc.set(df.fieldname, static\_default\_value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0268.json#L6403) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L917)

<a id="op-17565b31a8050f"></a>
### Get user default value

`operation_foundation_model_create_new_business_behavior_get_user_default_value`

**Inputs** df, defaults, doctype\_user\_permissions, allowed\_records, default\_doc.

**Explicit results** default\_doc · user\_default.

**Local steps**

- If (df.fieldtype equals “Link” and df.options differs from “User”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Link” → df.options differs from “User”.
  - If (not df.ignore\_user\_permissions and default\_doc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not df.ignore\_user\_permissions → default\_doc.
    - Return default\_doc.
  - Set user\_default from defaults.get(df.fieldname).
  - Set allowed\_by\_user\_permission from validate\_value\_via\_user\_permissions(df, doctype\_user\_permissions, allowed\_records, user\_default = user\_default).
  - If (user\_default and allowed\_by\_user\_permission).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_default → allowed\_by\_user\_permission.
    - Return user\_default.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0268.json#L6935) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L914)

<a id="op-cd16a491f43b9f"></a>
### Get static default value

`operation_foundation_model_create_new_business_behavior_get_static_default_value`

**Inputs** df, doctype\_user\_permissions, allowed\_records.

**Explicit results** Platform.session.user · nowdate() · df.default · df.options.split(whitespace '\\n', 1) at 0.

**Local steps**

- If df.get(“default”).
  - If df.default equals “\_\_user”.
    - Return Platform.session.user.
  - Otherwise.
    - If df.default equals “Today”.
      - Return nowdate().
    - Otherwise.
      - If not cstr(df.default).startswith(“:”).
        - Set is\_allowed\_default\_value from validate\_value\_via\_user\_permissions(df, doctype\_user\_permissions, allowed\_records).
        - If (df.fieldtype differs from “Link” or df.options equals “User” or is\_allowed\_default\_value).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype differs from “Link” → df.options equals “User” → is\_allowed\_default\_value.
          - Return df.default.
- Otherwise.
  - If (df.fieldtype equals “Select” and df.options and df.options does not belong to tuple(“&#91;Select&#93;”, “Loading...”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Select” → df.options → df.options does not belong to tuple(“&#91;Select&#93;”, “Loading...”).
    - Return df.options.split(whitespace '\\n', 1) at 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L913)

<a id="op-735dbf4cb08652"></a>
### Validate value via user permissions

`operation_foundation_model_create_new_business_behavior_validate_value_via_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** df, doctype\_user\_permissions, allowed\_records, user\_default.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L431) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L919)

<a id="op-ed670854ffd34b"></a>
### Set dynamic default values

`operation_foundation_model_create_new_business_behavior_set_dynamic_default_values`

**Inputs** doc, parent\_doc, parentfield.

**Local steps**

- Set user\_permissions from get\_user\_permissions().
- For each df in Platform.get\_meta(doc at “doctype”).get(“fields”).
  - If df.get(“default”).
    - If cstr(df.default).startswith(“:”).
      - Set default\_value from get\_default\_based\_on\_another\_field(df, user\_permissions, parent\_doc).
      - If (default\_value is distinct from no value and not doc.get(df.fieldname)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_value is distinct from no value → not doc.get(df.fieldname).
        - Set doc at df.fieldname from default\_value.
    - Otherwise.
      - If (df.fieldtype equals “Datetime” and df.default.lower() equals “now”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Datetime” → df.default.lower() equals “now”.
        - Set doc at df.fieldname from now\_datetime().
      - Otherwise.
        - If (df.fieldtype equals “Time” and df.default.lower() equals “now”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Time” → df.default.lower() equals “now”.
          - Set doc at df.fieldname from nowtime().
- If parent\_doc.
  - Set doc at “parent” from parent\_doc.name.
  - Set doc at “parenttype” from parent\_doc.doctype.
- If parentfield.
  - Set doc at “parentfield” from parentfield.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_user\_permissions() · clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, effective access, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L597) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L916)

<a id="op-90268c3bf40965"></a>
### User permissions exist

`operation_foundation_model_create_new_business_behavior_user_permissions_exist`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** df, doctype\_user\_permissions.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L1216) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L918)

<a id="op-584519cd78d3d6"></a>
### Get default based on another field

`operation_foundation_model_create_new_business_behavior_get_default_based_on_another_field`

**Inputs** df, user\_permissions, parent\_doc.

**Record and data access** read ref\_doctype via get\_value.

**Explicit results** default\_value.

**Local steps**

- Bind dependencies get\_allowed\_docs\_for\_doctype.
- Set ref\_doctype from df.default at slice 1 to no value.
- Set ref\_fieldname from ref\_doctype.lower().replace(one space, “\_”).
- Set reference\_name from parent\_doc.get(ref\_fieldname) when parent\_doc, otherwise Platform.db.get\_default(ref\_fieldname).
  - Value choice on parent\_doc — true gives parent\_doc.get(ref\_fieldname), false gives Platform.db.get\_default(ref\_fieldname).
- Set default\_value from Platform.db.get\_value(ref\_doctype, reference\_name, df.fieldname).
- Set is\_allowed\_default\_value from (not user\_permissions\_exist(df, user\_permissions.get(df.options)) or default\_value belongs to get\_allowed\_docs\_for\_doctype(user\_permissions at df.options, df.parent)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not user\_permissions\_exist(df, user\_permissions.get(df.options)) → default\_value belongs to get\_allowed\_docs\_for\_doctype(user\_permissions at df.options, df.parent).
- If is\_allowed\_default\_value.
  - Return default\_value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L1320) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L911)
