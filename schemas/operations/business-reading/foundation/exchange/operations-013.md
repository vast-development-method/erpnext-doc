# Integration and transport · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Email body

<a id="op-88d68f5802342d"></a>
### Get signature

`operation_foundation_email_email_body_business_behavior_get_signature`

**Inputs** email\_account.

**Explicit results** (text in the contract + email\_account.signature) · empty text.

**Local steps**

- If (email\_account and email\_account.add\_signature and email\_account.signature).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.add\_signature → email\_account.signature.
  - Return (text in the contract + email\_account.signature).
- Otherwise.
  - Return empty text.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L7713) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1481)

<a id="op-e5c08b5db47fef"></a>
### Get footer

`operation_foundation_email_email_body_business_behavior_get_footer`

**Inputs** email\_account, footer = no value.

**Explicit results** footer.

**Local steps**

- Set footer from (footer or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in footer → empty text.
- Set args from mapping().
- If (email\_account and email\_account.footer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.footer.
  - Evaluate args.update(mapping(“email\_account\_footer” → email\_account.footer)).
- Set sender\_address from Platform.db.get\_default(“email\_footer\_address”).
- If sender\_address.
  - Evaluate args.update(mapping(“sender\_address” → sender\_address)).
- If not cint(Platform.db.get\_default(“disable\_standard\_email\_footer”)).
  - Evaluate args.update(mapping(“default\_mail\_footer” → Platform.get\_hooks(“default\_mail\_footer”))).
- Update footer using + Platform.utils.jinja.get\_email\_from\_template(“email\_footer”, args) at 0.
- Return footer.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“default\_mail\_footer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1477)

<a id="op-123b3adbacbc6e"></a>
### Replace filename with cid

`operation_foundation_email_email_body_business_behavior_replace_filename_with_cid`

**Inputs** message, provided\_images = no value.

**Explicit results** tuple(message, inline\_images).

**Local steps**

- If provided\_images is identical to no value.
  - Set provided\_images from mapping().
- Set inline\_images from list().
- While true.
  - Set matches from EMBED\_PATTERN.search(message).
  - If not matches.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set groups from matches.groups().
  - Set img\_path from groups at 0.
  - Set img\_path\_escaped from Platform.utils.html\_utils.unescape\_html(img\_path).
  - Set filename from img\_path\_escaped.rsplit(“/”) at negative 1.
  - Set filecontent from (provided\_images.get(img\_path\_escaped) or provided\_images.get(filename)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in provided\_images.get(img\_path\_escaped) → provided\_images.get(filename).
  - If not filecontent.
    - Set filecontent from get\_filecontent\_from\_path(img\_path\_escaped).
  - If not filecontent.
    - Set message from re.sub(formatted text embed=&#91;'"&#93;{re.escape(img\_path)}&#91;'"&#93;, empty text, message).
    - Continue with the next iteration or loop test.
  - Set content\_id from random\_string(10).
  - Evaluate inline\_images.append(mapping(“filename” → filename, “filecontent” → filecontent, “content\_id” → content\_id)).
  - Set message from re.sub(formatted text embed=&#91;'"&#93;{re.escape(img\_path)}&#91;'"&#93;, formatted text src="cid:{content\_id}", message).
- Return tuple(message, inline\_images).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L389) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1483)

<a id="op-dce04a9f545954"></a>
### Get filecontent from path

`operation_foundation_email_email_body_business_behavior_get_filecontent_from_path`

**Inputs** path.

**Explicit results** no value · filecontent.

**Local steps**

- If not path.
  - Return no value.
- If path.startswith(“/”).
  - Set path from path at slice 1 to no value.
- If path.startswith(“assets/”).
  - Set base\_path from os.path.abspath(“assets”).
  - Set full\_path from os.path.abspath(path).
- Otherwise.
  - If path.startswith(“files/”).
    - Set base\_path from os.path.abspath(Platform.get\_site\_path(“public”, “files”)).
    - Set full\_path from os.path.abspath(Platform.get\_site\_path(“public”, path)).
  - Otherwise.
    - If path.startswith(“private/files/”).
      - Set base\_path from os.path.abspath(Platform.get\_site\_path(“private”, “files”)).
      - Set full\_path from os.path.abspath(Platform.get\_site\_path(path)).
    - Otherwise.
      - Return no value.
- If os.path.commonpath(tuple(base\_path, full\_path)) differs from base\_path.
  - Return no value.
- If os.path.exists(full\_path).
  - Within open(full\_path, “rb”) bound as f.
    - Set filecontent from f.read().
  - Return filecontent.
- Otherwise.
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L1038) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1476)

<a id="op-4f88b7f1ddaecf"></a>
### Get header

`operation_foundation_email_email_body_business_behavior_get_header`

**Inputs** header = no value.

**Explicit results** no value · email\_header.

**Local steps**

- Bind dependencies get\_email\_from\_template.
- If not header.
  - Return no value.
- If isinstance(header, str).
  - Set header from list(header, no value).
- If len(header) equals 1.
  - Evaluate header.append(no value).
- Set tuple(title, indicator) from header.
- If not title.
  - Set title from Platform.get\_hooks(“app\_title”) at negative 1.
- Set tuple(email\_header, \_text) from get\_email\_from\_template(“email\_header”, mapping(“header\_title” → title, “indicator” → indicator)).
- Return email\_header.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L1673) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1479)

<a id="op-5a70cf5757db65"></a>
### Sanitize email header

`operation_foundation_email_email_body_business_behavior_sanitize_email_header`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** header.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L1997) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1484)

<a id="op-7060f1cae2f8e1"></a>
### Get brand logo

`operation_foundation_email_email_body_business_behavior_get_brand_logo`

**Inputs** email\_account.

**Explicit results** ((email\_account and email\_account.get(“brand\_logo”)) or Platform.get\_website\_settings(“app\_logo”)).

**Local steps**

- Return ((email\_account and email\_account.get(“brand\_logo”)) or Platform.get\_website\_settings(“app\_logo”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (email\_account and email\_account.get(“brand\_logo”)) → Platform.get\_website\_settings(“app\_logo”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in email\_account → email\_account.get(“brand\_logo”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L2067) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1472)

<a id="op-23471c8f976d87"></a>
### Get brand name

`operation_foundation_email_email_body_business_behavior_get_brand_name`

**Inputs** no declared parameters.

**Explicit results** (Platform.get\_website\_settings(“app\_name”) or Platform.get\_system\_settings(“app\_name”)).

**Local steps**

- Return (Platform.get\_website\_settings(“app\_name”) or Platform.get\_system\_settings(“app\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_website\_settings(“app\_name”) → Platform.get\_system\_settings(“app\_name”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“app\_name”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L2170) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1473)

## Record · Email domain

[Record definition](../../../../data/record-types/email_domain.json)

<a id="op-ea5ca292140bda"></a>
### Get error message

`operation_foundation_email_record_definitions_email_domain_business_behavior_get_error_message`

**Inputs** event.

**Explicit results** mapping(“incoming” → tuple(translated “Incoming email account not correct”, translated “Error connecting via IMAP/POP3: {e}”), “outgoing” → tuple(translated “Outgoing email account not correct”, translated ….

**Local steps**

- Return mapping(“incoming” → tuple(translated “Incoming email account not correct”, translated “Error connecting via IMAP/POP3: {e}”), “outgoing” → tuple(translated “Outgoing email account not correct”, translated ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L834) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L98)

<a id="op-1030fa97b8ec46"></a>
### Handle error

`operation_foundation_email_record_definitions_email_domain_business_behavior_handle_error`

**Inputs** event.

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L973) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L99)

<a id="op-b902bd67d3b34c"></a>
### Handle error.decorator

`operation_foundation_email_record_definitions_email_domain_business_behavior_handle_error_decorator`

**Inputs** fn.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L1222) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L100)

<a id="op-d12cf587cec1da"></a>
### Handle error.decorator.wrapper

`operation_foundation_email_record_definitions_email_domain_business_behavior_handle_error_decorator_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(fn).

**Explicit failure paths** validation helper.

**Local steps**

- Set tuple(err\_title, err\_message) from get\_error\_message(event).
- Attempt the following.
  - Evaluate fn(expanded args, expanded names kwargs).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(title = err\_title, msg = err\_message.format(e = e)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L1447) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L101)

<a id="op-48b25a79243097"></a>
### Email Domain.validate

`operation_foundation_email_record_definitions_email_domain_business_behavior_email_domain_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (Platform.local.flags.in\_patch or Platform.in\_test or Platform.local.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.in\_patch → Platform.in\_test → Platform.local.flags.in\_install.
  - Return no value.
- Evaluate self.validate\_incoming\_server\_conn().
- Evaluate self.validate\_outgoing\_server\_conn().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate incoming server conn](operations-013.md#op-05938af3364cd7), [validate outgoing server conn](operations-013.md#op-fb581559ba6b4b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L1648) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L95)

<a id="op-72b8ab8fd1c4bd"></a>
### Email Domain.on update

`operation_foundation_email_record_definitions_email_domain_business_behavior_email_domain_on_update`

**Inputs** self.

**Record and data access** read “Email Account” via get\_all · resolve a document from “Email Account” via get\_doc.

**State and service calls** call save on email\_account · msgprint with translated “Error has occurred in {0}”.format(email\_account.name).

**Local steps**

- For each email\_account in Platform.get\_all(“Email Account”, filters = mapping(“domain” → self.name)).
  - Attempt the following.
    - Set email\_account from Platform.get\_doc(“Email Account”, email\_account.name).
    - For each attr in EMAIL\_DOMAIN\_FIELDS.
      - Evaluate email\_account.set(attr, self.get(attr, default = 0)).
    - Evaluate email\_account.save().
  - On failure (Exception) bound to e.
    - Evaluate Platform.msgprint(translated “Error has occurred in {0}”.format(email\_account.name), raise\_exception = e.\_\_class\_\_).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L1777) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L94)

<a id="op-05938af3364cd7"></a>
### Email Domain.validate incoming server conn

`operation_foundation_email_record_definitions_email_domain_business_behavior_email_domain_validate_incoming_server_conn`

**Inputs** self.

**Wrappers, in declaration order** handle\_error(“incoming”).

**Local steps**

- Set self.incoming\_port from get\_port(self).
- If self.use\_imap.
  - Set conn\_method from imaplib.IMAP4\_SSL when self.use\_ssl, otherwise imaplib.IMAP4.
    - Value choice on self.use\_ssl — true gives imaplib.IMAP4\_SSL, false gives imaplib.IMAP4.
- Otherwise.
  - Set conn\_method from poplib.POP3\_SSL when self.use\_ssl, otherwise poplib.POP3.
    - Value choice on self.use\_ssl — true gives poplib.POP3\_SSL, false gives poplib.POP3.
- Set self.use\_starttls from cint((self.use\_imap and self.use\_starttls and not self.use\_ssl)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_imap → self.use\_starttls → not self.use\_ssl.
- Set incoming\_conn from conn\_method(self.email\_server, port = self.incoming\_port, timeout = 15).
- Evaluate incoming\_conn.logout() when self.use\_imap, otherwise incoming\_conn.quit().
  - Value choice on self.use\_imap — true gives incoming\_conn.logout(), false gives incoming\_conn.quit().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L2106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L96)

<a id="op-fb581559ba6b4b"></a>
### Email Domain.validate outgoing server conn

`operation_foundation_email_record_definitions_email_domain_business_behavior_email_domain_validate_outgoing_server_conn`

**Inputs** self.

**Wrappers, in declaration order** handle\_error(“outgoing”).

**Local steps**

- Set conn\_method from smtplib.SMTP.
- If self.use\_ssl\_for\_outgoing.
  - Set self.smtp\_port from (self.smtp\_port or 465).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.smtp\_port → 465.
  - Set conn\_method from smtplib.SMTP\_SSL.
- Otherwise.
  - If self.use\_tls.
    - Set self.smtp\_port from (self.smtp\_port or 587).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.smtp\_port → 587.
- Evaluate conn\_method((self.smtp\_server or empty text), cint(self.smtp\_port), timeout = 15).quit().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.smtp\_server → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L2448) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L97)

## Record · Email group

[Record definition](../../../../data/record-types/email_group.json)

<a id="op-314e88c54ae6ce"></a>
### Email Group.onload

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_onload`

**Inputs** self.

**Record and data access** read “DocType” via get\_all · read “DocField” via get\_all.

**Local steps**

- Set singles from list of d.name for d drawn from Platform.get\_all(“DocType”, “name”, mapping(“issingle” → 1)).
  - Draw d from Platform.get\_all(“DocType”, “name”, mapping(“issingle” → 1)).
- Set self.get(“\_\_onload”).import\_types from list of mapping(“value” → d.parent, “label” → formatted text {d.parent} ({d.label})) for d drawn from Platform.get\_all(“DocField”, tuple(“parent”, “label”), mapping(“options” → “Email”)) where d.parent doe ….
  - Draw d from Platform.get\_all(“DocField”, tuple(“parent”, “label”), mapping(“options” → “Email”)), keep a combination only if (d.parent does not belong to singles).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L3380) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L111)

<a id="op-6b4b954f65752e"></a>
### Email Group.import from

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_import_from`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_all · resolve a document from mapping(“doctype” → “Email Group Member”, “email\_group” → self.name, “email” → email, “unsubscribed” → user.get(unsubscribed\_field) when unsubscribed\_field, otherwise 0) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Group Member”, “email\_group” → self.name, “email” → email, “unsubscribed” → user.get(unsubscribed\_field) when unsubscribed\_field, otherwise 0)) · msgprint with translated “{0} subscribers added”.format(added).

**Explicit results** self.update\_total\_subscribers().

**Explicit failure paths** validation helper — translated “No Email field found in {0}”.format(doctype).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set email\_field from next(generator of d.fieldname for d drawn from meta.fields where (d.fieldtype belongs to tuple(“Data”, “Small Text”, “Text”, “Code”) and d.options equals “Email”), no value).
  - Draw d from meta.fields, keep a combination only if ((d.fieldtype belongs to tuple(“Data”, “Small Text”, “Text”, “Code”) and d.options equals “Email”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype belongs to tuple(“Data”, “Small Text”, “Text”, “Code”) → d.options equals “Email”.
- If not email\_field.
  - Call the validation error handler Platform.throw(translated “No Email field found in {0}”.format(doctype), title = translated “Invalid Doctype”).
- Set unsubscribed\_field from “unsubscribed” when meta.get\_field(“unsubscribed”), otherwise no value.
  - Value choice on meta.get\_field(“unsubscribed”) — true gives “unsubscribed”, false gives no value.
- Set added from 0.
- For each user in Platform.get\_all(doctype, list(email\_field, (unsubscribed\_field or “name”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in unsubscribed\_field → “name”.
  - Within contextlib.suppress(Platform.UniqueValidationError, Platform.InvalidEmailAddressError).
    - Set email from parse\_addr(user.get(email\_field)) at 1 when user.get(email\_field), otherwise no value.
      - Value choice on user.get(email\_field) — true gives parse\_addr(user.get(email\_field)) at 1, false gives no value.
    - If email.
      - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Group Member”, “email\_group” → self.name, “email” → email, “unsubscribed” → nested operand in the contract.get(unsubscribed\_field) when unsubscribed\_field, other ….
        - Value choice on unsubscribed\_field — true gives user.get(unsubscribed\_field), false gives 0.
      - Update added using + 1.
- Evaluate Platform.msgprint(translated “{0} subscribers added”.format(added)).
- Return self.update\_total\_subscribers().

**Methods declared on this owner** [update total subscribers](operations-013.md#op-21bfc077933e42).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L3722) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L109)

<a id="op-21bfc077933e42"></a>
### Email Group.update total subscribers

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_update_total_subscribers`

**Inputs** self.

**State and service calls** call db\_update on self.

**Explicit results** self.total\_subscribers.

**Local steps**

- Set self.total\_subscribers from self.get\_total\_subscribers().
- Evaluate self.db\_update().
- Return self.total\_subscribers.

**Methods declared on this owner** [get total subscribers](operations-013.md#op-9343b7737f8601).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L4485) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L113)

<a id="op-9343b7737f8601"></a>
### Email Group.get total subscribers

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_get_total_subscribers`

**Inputs** self.

**Record and data access** execute query text (SELECT, Email).

**Explicit results** Platform.db.sql(query text (SELECT, Email), self.name) at 0 at 0.

**Local steps**

- Return Platform.db.sql(query text (SELECT, Email), self.name) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L4576) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L107)

<a id="op-8514cbdf37006f"></a>
### Email Group.preview welcome url

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_preview_welcome_resource_address`

**Inputs** self, email = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Explicit results** self.get\_welcome\_url(email).

**Local steps**

- Return self.get\_welcome\_url(email).

**Methods declared on this owner** [get welcome url](operations-013.md#op-70f873b6dd25f8).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L4700) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L112)

<a id="op-70f873b6dd25f8"></a>
### Email Group.get welcome url

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_get_welcome_resource_address`

**Inputs** self, email = no value.

**Declared result** (str bitwise or no value).

**Explicit results** no value · add\_query\_params(self.welcome\_url, mapping(“email” → email, “email\_group” → self.name)) when self.add\_query\_parameters, otherwise self.welcome\_url.

**Local steps**

- If not self.welcome\_url.
  - Return no value.
- Return add\_query\_params(self.welcome\_url, mapping(“email” → email, “email\_group” → self.name)) when self.add\_query\_parameters, otherwise self.welcome\_url.
  - Value choice on self.add\_query\_parameters — true gives add\_query\_params(self.welcome\_url, mapping(“email” → email, “email\_group” → self.name)), false gives self.welcome\_url.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L4807) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L108)

<a id="op-521b52074ef945"></a>
### Email Group.on trash

`operation_foundation_email_record_definitions_email_group_business_behavior_email_group_on_trash`

**Inputs** self.

**Record and data access** read “Email Group Member” via get\_all.

**State and service calls** request delete\_doc for “Email Group Member”.

**Local steps**

- For each d in Platform.get\_all(“Email Group Member”, “name”, mapping(“email\_group” → self.name)).
  - Evaluate Platform.delete\_doc(“Email Group Member”, d.name, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L4982) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L110)

<a id="op-38c56419465990"></a>
### Import from

`operation_foundation_email_record_definitions_email_group_business_behavior_import_from`

**Inputs** name, doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Email Group” via get\_doc.

**Explicit results** nlist.import\_from(doctype).

**Local steps**

- Set nlist from Platform.get\_doc(“Email Group”, name).
- If nlist.has\_permission(“write”).
  - Return nlist.import\_from(doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from nlist.has\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L5138) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L114)
