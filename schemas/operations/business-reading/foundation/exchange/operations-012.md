# Integration and transport · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Email body

<a id="op-efbe4a5c3be847"></a>
### EMail.initialize

`operation_foundation_email_email_body_business_behavior_e_mail_initialize`

**Inputs** self, sender = empty text, recipients = tuple(), subject = empty text, alternative = 0, reply\_to = no value, cc = tuple(), bcc = tuple(), email\_account = no value, expose\_recipients = no value, x\_priority = 3.

**Local steps**

- Bind dependencies Charset.
- Evaluate Charset.add\_charset(“utf-8”, Charset.QP, Charset.QP, “utf-8”).
- If isinstance(recipients, str).
  - Set recipients from recipients.replace(“;”, “,”).replace(whitespace '\\n', empty text).
  - Set recipients from split\_emails(recipients).
- Set recipients from list of r for r drawn from generator of strip(r) for r drawn from recipients where r.
  - Draw r from generator of strip(r) for r drawn from recipients, keep a combination only if (r).
  - Draw r from recipients.
- Set self.sender from sender.
- Set self.reply\_to from (reply\_to or sender).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reply\_to → sender.
- Set self.recipients from recipients.
- Set self.subject from subject.
- Set self.expose\_recipients from expose\_recipients.
- Set self.msg\_root from MIMEMultipart(“mixed”, policy = policy.SMTP).
- Set self.msg\_alternative from MIMEMultipart(“alternative”, policy = policy.SMTP).
- Evaluate self.msg\_root.attach(self.msg\_alternative).
- Set self.cc from (cc or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cc → list().
- Set self.bcc from (bcc or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bcc → list().
- Set self.html\_set from false.
- Set self.x\_priority from x\_priority.
- Set self.email\_account from (email\_account or EmailAccount.find\_outgoing(match\_by\_email = sender, \_raise\_error = true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_account → EmailAccount.find\_outgoing(match\_by\_email = sender, \_raise\_error = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1458)

<a id="op-02cacd98d088ec"></a>
### EMail.set html

`operation_foundation_email_email_body_business_behavior_e_mail_set_document_markup`

**Inputs** self, message, text\_content = no value, footer = no value, print\_html = no value, formatted = no value, inline\_images = no value, header = no value.

**Local steps**

- If not formatted.
  - Set formatted from get\_formatted\_html(self.subject, message, footer, print\_html, email\_account = self.email\_account, header = header, sender = self.sender).
- If not self.html\_set.
  - If text\_content.
    - Evaluate self.set\_text(expand\_relative\_urls(text\_content)).
  - Otherwise.
    - Evaluate self.set\_html\_as\_text(expand\_relative\_urls(formatted)).
- Evaluate self.set\_part\_html(formatted, inline\_images).
- Set self.html\_set from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set text](operations-012.md#op-573f068288f8b8), [set html as text](operations-012.md#op-e5aa1b6ac31705), [set part html](operations-012.md#op-b72972f7c4108e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L766) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1462)

<a id="op-573f068288f8b8"></a>
### EMail.set text

`operation_foundation_email_email_body_business_behavior_e_mail_set_text`

**Inputs** self, message.

**Local steps**

- Bind dependencies MIMEText.
- Set part from MIMEText(message, “plain”, “utf-8”, policy = policy.SMTP).
- Evaluate self.msg\_alternative.attach(part).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L1112) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1469)

<a id="op-b72972f7c4108e"></a>
### EMail.set part html

`operation_foundation_email_email_body_business_behavior_e_mail_set_part_document_markup`

**Inputs** self, message, inline\_images.

**Local steps**

- Bind dependencies MIMEText.
- Set has\_inline\_images from EMBED\_PATTERN.search(message).
- If has\_inline\_images.
  - Set provided\_images from mapping().
  - If inline\_images.
    - For each img in inline\_images.
      - If (img.get(“filename”) and img.get(“filecontent”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in img.get(“filename”) → img.get(“filecontent”).
        - Set provided\_images at img at “filename” from img at “filecontent”.
        - Set basename from img at “filename”.rsplit(“/”, 1) at negative 1.
        - If basename does not belong to provided\_images.
          - Set provided\_images at basename from img at “filecontent”.
  - Set tuple(message, \_inline\_images) from replace\_filename\_with\_cid(message, provided\_images).
  - Set msg\_related from MIMEMultipart(“related”, policy = policy.SMTP).
  - Set html\_part from MIMEText(message, “html”, “utf-8”, policy = policy.SMTP).
  - Evaluate msg\_related.attach(html\_part).
  - For each image in \_inline\_images.
    - Evaluate self.add\_attachment(image.get(“filename”), image.get(“filecontent”), content\_id = image.get(“content\_id”), parent = msg\_related, inline = true).
  - Evaluate self.msg\_alternative.attach(msg\_related).
- Otherwise.
  - Evaluate self.msg\_alternative.attach(MIMEText(message, “html”, “utf-8”, policy = policy.SMTP)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add attachment](operations-012.md#op-6766f2c3307455).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L1234) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1468)

<a id="op-e5aa1b6ac31705"></a>
### EMail.set html as text

`operation_foundation_email_email_body_business_behavior_e_mail_set_document_markup_as_text`

**Inputs** self, html.

**Local steps**

- Evaluate self.set\_text(to\_markdown(html)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set text](operations-012.md#op-573f068288f8b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L1939) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1030) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1463)

<a id="op-b5fcb7af7af508"></a>
### EMail.set message

`operation_foundation_email_email_body_business_behavior_e_mail_set_message`

**Inputs** self, message, mime\_type = “text/html”, as\_attachment = 0, filename = “attachment.html”.

**Local steps**

- Bind dependencies MIMEText.
- Set tuple(\_maintype, subtype) from mime\_type.split(“/”).
- Set part from MIMEText(message, \_subtype = subtype, policy = policy.SMTP).
- If as\_attachment.
  - Set clean\_filename from re.sub(“&#91;\\r\\n&#93;”, empty text, str(filename)).
  - Evaluate part.add\_header(“Content-Disposition”, “attachment”, filename = clean\_filename).
- Evaluate self.msg\_root.attach(part).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L2016) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1466)

<a id="op-1478a3d7e2f042"></a>
### EMail.attach file

`operation_foundation_email_email_body_business_behavior_e_mail_attach_file`

**Inputs** self, n.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set \_file from Platform.get\_doc(“File”, mapping(“file\_name” → n)).
- Set content from \_file.get\_content().
- If not content.
  - Return no value.
- Evaluate self.add\_attachment(\_file.file\_name, content).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add attachment](operations-012.md#op-6766f2c3307455).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L2311) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1457)

<a id="op-6766f2c3307455"></a>
### EMail.add attachment

`operation_foundation_email_email_body_business_behavior_e_mail_add_attachment`

**Inputs** self, fname, fcontent, content\_type = no value, parent = no value, content\_id = no value, inline = false.

**Local steps**

- If not parent.
  - Set parent from self.msg\_root.
- Evaluate add\_attachment(fname, fcontent, content\_type, parent, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L2482) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1453)

<a id="op-ad02ed21200886"></a>
### EMail.add pdf attachment

`operation_foundation_email_email_body_business_behavior_e_mail_add_portable_document_attachment`

**Inputs** self, name, html, options = no value.

**Local steps**

- Evaluate self.add\_attachment(name, get\_pdf(html, options), “application/octet-stream”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add attachment](operations-012.md#op-6766f2c3307455).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L2640) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1455)

<a id="op-4adbd168a6e4ed"></a>
### EMail.validate

`operation_foundation_email_email_body_business_behavior_e_mail_validate`

**Inputs** self.

**Local steps**

- If not self.sender.
  - Set self.sender from self.email\_account.default\_sender.
- Evaluate validate\_email\_address(strip(self.sender), true).
- Evaluate self.validate\_reply\_to().
- If self.email\_account.add\_x\_original\_from.
  - Evaluate self.set\_header(“X-Original-From”, self.sender).
- Evaluate self.replace\_sender().
- Evaluate self.replace\_sender\_name().
- Set self.recipients from list of strip(r) for r drawn from self.recipients where r does not belong to Platform.STANDARD\_USERS.
  - Draw r from self.recipients, keep a combination only if (r does not belong to Platform.STANDARD\_USERS).
- Set self.cc from list of strip(r) for r drawn from self.cc where r does not belong to Platform.STANDARD\_USERS.
  - Draw r from self.cc, keep a combination only if (r does not belong to Platform.STANDARD\_USERS).
- Set self.bcc from list of strip(r) for r drawn from self.bcc where r does not belong to Platform.STANDARD\_USERS.
  - Draw r from self.bcc, keep a combination only if (r does not belong to Platform.STANDARD\_USERS).
- For each e in ((self.recipients + (self.cc or list())) + (self.bcc or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cc → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bcc → list().
  - Evaluate validate\_email\_address(e, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reply to](operations-012.md#op-157a1d7e4c9185), [set header](operations-012.md#op-700a3867c30241), [replace sender](operations-012.md#op-17203c06972208), [replace sender name](operations-012.md#op-edcad2d66a78db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L2746) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1470)

<a id="op-157a1d7e4c9185"></a>
### EMail.validate reply to

`operation_foundation_email_email_body_business_behavior_e_mail_validate_reply_to`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not self.email\_account.add\_reply\_to\_header.
  - Set self.reply\_to from no value.
  - Return no value.
- If self.email\_account.reply\_to\_addresses.
  - Set valid\_addresses from list of formataddr(tuple(reply\_to.\_name, reply\_to.email)) for reply\_to drawn from self.email\_account.reply\_to\_addresses where (reply\_to.email and validate\_email\_address(reply\_to.email, true)).
    - Draw reply\_to from self.email\_account.reply\_to\_addresses, keep a combination only if ((reply\_to.email and validate\_email\_address(reply\_to.email, true))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reply\_to.email → validate\_email\_address(reply\_to.email, true).
  - Set self.reply\_to from “, ”.join(valid\_addresses) when valid\_addresses, otherwise no value.
    - Value choice on valid\_addresses — true gives “, ”.join(valid\_addresses), false gives no value.
  - Return no value.
- Set fallback from (strip(self.reply\_to) or self.sender).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in strip(self.reply\_to) → self.sender.
- Set self.reply\_to from validate\_email\_address(fallback, true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L3292) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1471)

<a id="op-17203c06972208"></a>
### EMail.replace sender

`operation_foundation_email_email_body_business_behavior_e_mail_replace_sender`

**Inputs** self.

**Local steps**

- If cint(self.email\_account.always\_use\_account\_email\_id\_as\_sender).
  - Set tuple(sender\_name, \_) from parse\_addr(self.sender).
  - Set self.sender from email.utils.formataddr(tuple(str(Header((sender\_name or nested operand in the contract.email\_account.name), “utf-8”)), self.email\_account.email\_id)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sender\_name → self.email\_account.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L3623) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1460)

<a id="op-edcad2d66a78db"></a>
### EMail.replace sender name

`operation_foundation_email_email_body_business_behavior_e_mail_replace_sender_name`

**Inputs** self.

**Local steps**

- If cint(self.email\_account.always\_use\_account\_name\_as\_sender\_name).
  - Set tuple(\_, sender\_email) from parse\_addr(self.sender).
  - Set self.sender from email.utils.formataddr(tuple(str(Header(self.email\_account.name, “utf-8”)), sender\_email)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L3829) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1028) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1461)

<a id="op-9bba74f10d696b"></a>
### EMail.set message id

`operation_foundation_email_email_body_business_behavior_e_mail_set_message_identifier`

**Inputs** self, message\_id, is\_notification = false.

**Local steps**

- If message\_id.
  - Set message\_id from ((“&lt;” + message\_id) + “&gt;”).
- Otherwise.
  - Set message\_id from get\_message\_id().
  - Evaluate self.set\_header(“isnotification”, text in the contract).
- If is\_notification.
  - Evaluate self.set\_header(“isnotification”, text in the contract).
- Evaluate self.set\_header(“Message-Id”, message\_id).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header](operations-012.md#op-700a3867c30241).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L4017) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1467)

<a id="op-0d2d0af67075e4"></a>
### EMail.set in reply to

`operation_foundation_email_email_body_business_behavior_e_mail_set_in_reply_to`

**Inputs** self, in\_reply\_to.

**Local steps**

- Evaluate self.set\_header(“In-Reply-To”, in\_reply\_to).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header](operations-012.md#op-700a3867c30241).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L4223) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1032) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1465)

<a id="op-5e74ba53b167e2"></a>
### EMail.add headers

`operation_foundation_email_email_body_business_behavior_e_mail_add_headers`

**Inputs** self, headers.

**Explicit failure paths** validation helper — translated “Headers must be a dictionary”.

**Local steps**

- If not isinstance(headers, dict).
  - Call the validation error handler Platform.throw(translated “Headers must be a dictionary”).
- For each tuple(key, value) in headers.items().
  - If value is distinct from no value.
    - Set key from (“X-” + key) when not key.startswith(“X-”), otherwise key.
      - Value choice on not key.startswith(“X-”) — true gives (“X-” + key), false gives key.
    - Evaluate self.set\_header(key, value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header](operations-012.md#op-700a3867c30241).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L4290) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1454)

<a id="op-9769fb2c457f55"></a>
### EMail.make

`operation_foundation_email_email_body_business_behavior_e_mail_make`

**Inputs** self.

**Local steps**

- Set headers from mapping(“Subject” → strip(self.subject), “From” → self.sender, “To” → “, ”.join(self.recipients) when self.expose\_recipients equals “header”, otherwise “&lt;!--recipient--&gt;”, “Date” → email.utils.formatdate(), …).
  - Value choice on self.expose\_recipients equals “header” — true gives “, ”.join(self.recipients), false gives “&lt;!--recipient--&gt;”.
  - Value choice on self.reply\_to — true gives self.reply\_to, false gives no value.
  - Value choice on self.cc — true gives “, ”.join(self.cc), false gives no value.
- If self.x\_priority differs from 3.
  - Evaluate headers.update(mapping(“X-Priority” → str(self.x\_priority))).
- For each tuple(key, val) in headers.items().
  - If val.
    - Evaluate self.set\_header(key, val).
- For each hook in Platform.get\_hooks(“make\_email\_body\_message”).
  - Evaluate Platform.get\_attr(hook)(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header](operations-012.md#op-700a3867c30241).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“make\_email\_body\_message”), Platform.get\_attr(hook).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L4535) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1459)

<a id="op-700a3867c30241"></a>
### EMail.set header

`operation_foundation_email_email_body_business_behavior_e_mail_set_header`

**Inputs** self, key, value.

**Local steps**

- If key belongs to self.msg\_root.
  - Remove self.msg\_root at key.
- Set self.msg\_root at key from sanitize\_email\_header(value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L5030) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1031) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1464)

<a id="op-28d223dd473974"></a>
### EMail.as string

`operation_foundation_email_email_body_business_behavior_e_mail_as_string`

**Inputs** self.

**Explicit results** self.msg\_root.as\_string(policy = policy.SMTP).

**Local steps**

- Evaluate self.validate().
- Evaluate self.make().
- Return self.msg\_root.as\_string(policy = policy.SMTP).

**Methods declared on this owner** [validate](operations-012.md#op-4adbd168a6e4ed), [make](operations-012.md#op-9769fb2c457f55).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L5159) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1456)

<a id="op-cd1cab31ed79b9"></a>
### Get formatted html

`operation_foundation_email_email_body_business_behavior_get_formatted_document_markup`

**Inputs** subject, message, footer = no value, print\_html = no value, email\_account = no value, header = no value, unsubscribe\_link = no value, sender = no value, with\_container = false, raw\_html = false, add\_css = true, wrapper = “templates/emails/standard.html”.

**Explicit results** inline\_style\_in\_html(html, add\_css = add\_css).

**Local steps**

- Set email\_account from (email\_account or EmailAccount.find\_outgoing(match\_by\_email = sender)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_account → EmailAccount.find\_outgoing(match\_by\_email = sender).
- Set params from mapping(“site\_url” → get\_url(), “title” → subject, “print\_html” → print\_html, “subject” → subject).
- If raw\_html.
  - Set rendered\_email from Platform.render\_template(message, params).
- Otherwise.
  - Evaluate params.update(mapping(“brand\_logo” → get\_brand\_logo(email\_account) when (with\_container or header), otherwise no value, “brand\_name” → get\_brand\_name() when (with\_container or header), otherwise no value,  ….
    - Value choice on (with\_container or header) — true gives get\_brand\_logo(email\_account), false gives no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in with\_container → header.
    - Value choice on (with\_container or header) — true gives get\_brand\_name(), false gives no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in with\_container → header.
  - Set rendered\_email from Platform.get\_template(wrapper).render(params).
- Set html from scrub\_urls(rendered\_email).
- If unsubscribe\_link.
  - Set html from html.replace(“&lt;!--unsubscribe link here--&gt;”, unsubscribe\_link.html).
- Return inline\_style\_in\_html(html, add\_css = add\_css).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L72) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1478)

<a id="op-d7e33d5d23478b"></a>
### Get email html

`operation_foundation_email_email_body_business_behavior_get_email_document_markup`

**Inputs** template, args, subject, header = no value, with\_container = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_formatted\_html(subject, email at 0, header = header, with\_container = with\_container).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Bind dependencies json.
- Set with\_container from cint(with\_container).
- Set args from json.loads(args).
- If (header and header.startswith(“&#91;”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in header → header.startswith(“&#91;”).
  - Set header from json.loads(header).
- Set email from Platform.utils.jinja.get\_email\_from\_template(template, args).
- Return get\_formatted\_html(subject, email at 0, header = header, with\_container = with\_container).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L71) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1475)

<a id="op-7a631925f923dd"></a>
### Inline style in html

`operation_foundation_email_email_body_business_behavior_inline_style_in_document_markup`

**Inputs** html, add\_css = true.

**Explicit results** p.transform().

**Local steps**

- Bind dependencies Premailer.
- Bind dependencies bundled\_asset.
- If add\_css.
  - Set css\_files from Platform.get\_hooks(“email\_css”).
  - Set css\_files from list of bundled\_asset(path) for path drawn from css\_files.
    - Draw path from css\_files.
  - Set css\_files from list of path.lstrip(“/”) for path drawn from css\_files.
    - Draw path from css\_files.
  - Set css\_files from list of css\_file for css\_file drawn from css\_files where os.path.exists(os.path.abspath(css\_file)).
    - Draw css\_file from css\_files, keep a combination only if (os.path.exists(os.path.abspath(css\_file))).
- Otherwise.
  - Set css\_files from no value.
- Set p from Premailer(html = html, external\_styles = css\_files, strip\_important = false, allow\_loading\_external\_files = true).
- Return p.transform().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“email\_css”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L6323) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1482)

<a id="op-04777242869aae"></a>
### Add attachment

`operation_foundation_email_email_body_business_behavior_add_attachment`

**Inputs** fname, fcontent, content\_type = no value, parent = no value, content\_id = no value, inline = false.

**Explicit results** no value.

**Local steps**

- Bind dependencies mimetypes.
- Bind dependencies encoders.
- Bind dependencies MIMEAudio.
- Bind dependencies MIMEBase.
- Bind dependencies MIMEImage.
- Bind dependencies MIMEText.
- If not parent.
  - Return no value.
- If not content\_type.
  - Set tuple(content\_type, \_encoding) from mimetypes.guess\_type(fname).
- If content\_type is identical to no value.
  - Set content\_type from “application/octet-stream”.
- Set tuple(maintype, subtype) from content\_type.split(“/”, 1).
- If maintype equals “text”.
  - If isinstance(fcontent, bytes).
    - Set fcontent from fcontent.decode(“utf-8”).
  - Set part from MIMEText(fcontent, \_subtype = subtype, \_charset = “utf-8”).
- Otherwise.
  - If maintype equals “image”.
    - If isinstance(fcontent, str).
      - Set fcontent from fcontent.encode(“utf-8”).
    - Set part from MIMEImage(fcontent, \_subtype = subtype).
  - Otherwise.
    - If maintype equals “audio”.
      - If isinstance(fcontent, str).
        - Set fcontent from fcontent.encode(“utf-8”).
      - Set part from MIMEAudio(fcontent, \_subtype = subtype).
    - Otherwise.
      - If isinstance(fcontent, str).
        - Set fcontent from fcontent.encode(“utf-8”).
      - Set part from MIMEBase(maintype, subtype).
      - Evaluate part.set\_payload(fcontent).
      - Evaluate encoders.encode\_base64(part).
- If fname.
  - Set attachment\_type from “inline” when inline, otherwise “attachment”.
    - Value choice on inline — true gives “inline”, false gives “attachment”.
  - Set clean\_filename from re.sub(“&#91;\\r\\n&#93;”, empty text, str(fname)).
  - Evaluate part.add\_header(“Content-Disposition”, attachment\_type, filename = clean\_filename).
- If content\_id.
  - Evaluate part.add\_header(“Content-ID”, formatted text &lt;{content\_id}&gt;).
- Evaluate parent.attach(part).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L6681) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1452)

<a id="op-3f2b55c6d604e1"></a>
### Get message id

`operation_foundation_email_email_body_business_behavior_get_message_identifier`

**Inputs** no declared parameters.

**Explicit results** email.utils.make\_msgid(domain = Platform.local.site).

**Local steps**

- Return email.utils.make\_msgid(domain = Platform.local.site).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0233.json#L7650) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1480)
