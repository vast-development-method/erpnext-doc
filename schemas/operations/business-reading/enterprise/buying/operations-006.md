# Purchasing · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Request for quotation

[Record definition](../../../../data/record-types/request_for_quotation.json)

<a id="op-f5e28dfb2e37e8"></a>
### Requestfor Quotation.on submit

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Submitted”).
- For each supplier in self.suppliers.
  - Set supplier.email\_sent from 0.
  - Set supplier.quote\_status from “Pending”.
- Evaluate self.send\_to\_supplier().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send to supplier](operations-006.md#op-e31f5c33ddd219).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L6029) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L18)

<a id="op-475cacacfdcd02"></a>
### Requestfor Quotation.before print

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_before_print`

**Inputs** self, settings = no value.

**Explicit results** no value.

**Local steps**

- If (self.vendor or not self.suppliers).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.vendor → not self.suppliers.
  - Return no value.
- Evaluate self.update\_supplier\_part\_no(self.suppliers at 0.supplier).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update supplier part no](operations-006.md#op-2fe25b90f86659).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L6166) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L10)

<a id="op-1c9badc107901d"></a>
### Requestfor Quotation.on cancel

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L6285) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L17)

<a id="op-816b60681953c4"></a>
### Requestfor Quotation.get supplier email preview

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_get_supplier_email_preview`

**Inputs** self, supplier.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** message.

**Local steps**

- Set rfq\_suppliers from list(filter(deferred anonymous expression, self.suppliers)).
- Set rfq\_supplier from rfq\_suppliers at 0.
- Evaluate self.validate\_email\_id(rfq\_supplier).
- Set message from self.supplier\_rfq\_mail(rfq\_supplier, empty text, self.get\_link(), true).
- Set message at “message” from sanitize\_html(message at “message”).
- Return message.

**Methods declared on this owner** [validate email id](operations-005.md#op-01094a51eead55), [supplier rfq mail](operations-006.md#op-97bffb32ccf9d1), [get link](operations-006.md#op-e7ca7ad7761f9b).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L15)

<a id="op-e31f5c33ddd219"></a>
### Requestfor Quotation.send to supplier

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_send_to_supplier`

**Inputs** self.

**State and service calls** call save on rfq\_supplier.

**Local steps**

- For each rfq\_supplier in self.suppliers.
  - If (rfq\_supplier.email\_id is distinct from no value and rfq\_supplier.send\_email).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in rfq\_supplier.email\_id is distinct from no value → rfq\_supplier.send\_email.
    - Evaluate self.validate\_email\_id(rfq\_supplier).
    - Set tuple(update\_password\_link, contact) from self.update\_supplier\_contact(rfq\_supplier, self.get\_link()).
    - Evaluate self.update\_supplier\_part\_no(rfq\_supplier.supplier).
    - Evaluate self.supplier\_rfq\_mail(rfq\_supplier, update\_password\_link, self.get\_link()).
    - Set rfq\_supplier.email\_sent from 1.
    - If not rfq\_supplier.contact.
      - Set rfq\_supplier.contact from contact.
    - Evaluate rfq\_supplier.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate email id](operations-005.md#op-01094a51eead55), [update supplier contact](operations-006.md#op-666b5e299c978d), [get link](operations-006.md#op-e7ca7ad7761f9b), [update supplier part no](operations-006.md#op-2fe25b90f86659), [supplier rfq mail](operations-006.md#op-97bffb32ccf9d1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L20)

<a id="op-e7ca7ad7761f9b"></a>
### Requestfor Quotation.get link

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_get_link`

**Inputs** self.

**Record and data access** read “Portal Menu Item” via get\_value.

**Explicit results** get\_url(formatted text {route}/{self.name}).

**Explicit failure paths** validation helper — translated “Please add Request for Quotation to the sidebar in Portal Settings.”.

**Local steps**

- Set route from Platform.db.get\_value(“Portal Menu Item”, mapping(“reference\_doctype” → “Request for Quotation”), list(“route”)).
- If not route.
  - Call the validation error handler Platform.throw(translated “Please add Request for Quotation to the sidebar in Portal Settings.”).
- Return get\_url(formatted text {route}/{self.name}).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L322) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L14)

<a id="op-2fe25b90f86659"></a>
### Requestfor Quotation.update supplier part no

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_update_supplier_part_number`

**Inputs** self, supplier.

**Record and data access** read “Item Supplier” via get\_value.

**Local steps**

- Set self.vendor from supplier.
- For each item in self.items.
  - Set item.supplier\_part\_no from Platform.db.get\_value(“Item Supplier”, mapping(“parent” → item.item\_code, “supplier” → supplier), “supplier\_part\_no”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L539) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L27)

<a id="op-666b5e299c978d"></a>
### Requestfor Quotation.update supplier contact

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_update_supplier_contact`

**Inputs** self, rfq\_supplier, link.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc.

**Explicit results** tuple(update\_password\_link, contact).

**Local steps**

- Set tuple(update\_password\_link, contact) from tuple(empty text, empty text).
- If Platform.db.exists(“User”, rfq\_supplier.email\_id).
  - Set user from Platform.get\_doc(“User”, rfq\_supplier.email\_id).
- Otherwise.
  - Set tuple(user, update\_password\_link) from self.create\_user(rfq\_supplier, link).
- Set contact from self.link\_supplier\_contact(rfq\_supplier, user).
- Return tuple(update\_password\_link, contact).

**Methods declared on this owner** [create user](operations-006.md#op-80663eb86b9f36), [link supplier contact](operations-006.md#op-ab8c48067e86ba).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L705) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L26)

<a id="op-ab8c48067e86ba"></a>
### Requestfor Quotation.link supplier contact

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_link_supplier_contact`

**Inputs** self, rfq\_supplier, user.

**Record and data access** resolve a document from “Contact” via get\_doc.

**State and service calls** request new\_doc for “Contact” · call save on contact.

**Explicit results** contact.name.

**Local steps**

- If rfq\_supplier.contact.
  - Set contact from Platform.get\_doc(“Contact”, rfq\_supplier.contact).
- Otherwise.
  - Set contact from Platform.new\_doc(“Contact”).
  - Set contact.first\_name from (rfq\_supplier.supplier\_name or rfq\_supplier.supplier).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rfq\_supplier.supplier\_name → rfq\_supplier.supplier.
  - Evaluate contact.append(“links”, mapping(“link\_doctype” → “Supplier”, “link\_name” → rfq\_supplier.supplier)).
  - Evaluate contact.append(“email\_ids”, mapping(“email\_id” → user.name, “is\_primary” → 1)).
- If (not contact.email\_id and not contact.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not contact.email\_id → not contact.user.
  - Set contact.email\_id from user.name.
  - Set contact.user from user.name.
- Evaluate contact.save(ignore\_permissions = true).
- If rfq\_supplier.supplier.
  - Evaluate self.update\_user\_in\_supplier(rfq\_supplier.supplier, user.name).
- If not rfq\_supplier.contact.
  - Return contact.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [update user in supplier](operations-006.md#op-d412d8cfcd6052).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L963) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L16)

<a id="op-d412d8cfcd6052"></a>
### Requestfor Quotation.update user in supplier

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_update_user_in_supplier`

**Inputs** self, supplier, user.

**Record and data access** read “Portal User” via exists · resolve a document from “Supplier” via get\_doc.

**State and service calls** call save on supplier\_doc.

**Local steps**

- If not Platform.db.exists(“Portal User”, mapping(“parenttype” → “Supplier”, “parent” → supplier, “user” → user)).
  - Set supplier\_doc from Platform.get\_doc(“Supplier”, supplier).
  - Evaluate supplier\_doc.append(“portal\_users”, mapping(“user” → user)).
  - Set supplier\_doc.flags.ignore\_validate from true.
  - Set supplier\_doc.flags.ignore\_mandatory from true.
  - Set supplier\_doc.flags.ignore\_permissions from true.
  - Evaluate supplier\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L28)

<a id="op-80663eb86b9f36"></a>
### Requestfor Quotation.create user

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_create_user`

**Inputs** self, rfq\_supplier, link.

**Record and data access** read “Contact” via get\_value · resolve a document from mapping(“doctype” → “User”, “send\_welcome\_email” → 1, “email” → rfq\_supplier.email\_id, “first\_name” → (contact\_name or rfq\_supplier.supplier\_name or rfq\_supplier.supplier), …) via get\_doc.

**State and service calls** call save on user.

**Explicit results** tuple(user, get\_url(“/login#forgot”)).

**Local steps**

- Set contact\_name from no value.
- If rfq\_supplier.contact.
  - Set name\_fields from Platform.get\_value(“Contact”, rfq\_supplier.contact, list(“first\_name”, “middle\_name”, “last\_name”)).
  - If name\_fields.
    - Set contact\_name from get\_full\_name(expanded name\_fields).
- Set user from Platform.get\_doc(mapping(“doctype” → “User”, “send\_welcome\_email” → 1, “email” → rfq\_supplier.email\_id, “first\_name” → (contact\_name or rfq\_supplier.supplier\_name or rfq\_supplier.supplier), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact\_name → rfq\_supplier.supplier\_name → rfq\_supplier.supplier.
- Evaluate user.save(ignore\_permissions = true).
- Return tuple(user, get\_url(“/login#forgot”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L12)

<a id="op-97bffb32ccf9d1"></a>
### Requestfor Quotation.supplier rfq mail

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_supplier_request_for_quotation_mail`

**Inputs** self, data, update\_password\_link, rfq\_link, preview = false.

**Record and data access** resolve a document from “Contact” via get\_doc · read “Buying Settings” via get\_single\_value · read “Email Account” via get\_value · read “Email Template” via get\_value · read “Supplier” via get\_value · 1 additional forms in the steps below.

**Explicit results** mapping(“message” → rendered\_message, “subject” → rendered\_subject).

**Local steps**

- Set full\_name from get\_user\_fullname(Platform.session at “user”).
- If full\_name equals “Guest”.
  - Set full\_name from “Administrator”.
- Set doc\_args from self.as\_dict().
- If data.get(“contact”).
  - Set contact from Platform.get\_doc(“Contact”, data.get(“contact”)).
  - Set doc\_args at “contact” from contact.as\_dict().
- Evaluate doc\_args.update(mapping(“supplier” → data.get(“supplier”), “supplier\_name” → data.get(“supplier\_name”), “update\_password\_link” → formatted text &lt;a href="{update\_password\_link}" class="btn btn-default btn-x ….
- Set fixed\_procurement\_email from Platform.db.get\_single\_value(“Buying Settings”, “fixed\_email”).
- If fixed\_procurement\_email.
  - Set sender from Platform.db.get\_value(“Email Account”, fixed\_procurement\_email, “email\_id”).
- Otherwise.
  - Set sender from ((Platform.session.user does not belong to STANDARD\_USERS and Platform.session.user) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (Platform.session.user does not belong to STANDARD\_USERS and Platform.session.user) → no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user does not belong to STANDARD\_USERS → Platform.session.user.
- Set message\_template from self.mfs\_html when self.use\_html, otherwise self.message\_for\_supplier.
  - Value choice on self.use\_html — true gives self.mfs\_html, false gives self.message\_for\_supplier.
- Set rendered\_message from Platform.render\_template(message\_template, doc\_args, restrict\_globals = true).
- Set subject\_source from (self.subject or Platform.get\_value(“Email Template”, self.email\_template, “subject”) or translated “Request for Quotation”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.subject → Platform.get\_value(“Email Template”, self.email\_template, “subject”) → translated “Request for Quotation”.
- Set rendered\_subject from Platform.render\_template(subject\_source, doc\_args, restrict\_globals = true).
- If preview.
  - Return mapping(“message” → rendered\_message, “subject” → rendered\_subject).
- Set attachments from list().
- If self.send\_attached\_files.
  - Set attachments from self.get\_attachments().
- If self.send\_document\_print.
  - Set supplier\_language from Platform.db.get\_value(“Supplier”, data.supplier, “language”).
  - Set system\_language from Platform.db.get\_single\_value(“System Settings”, “language”).
  - Evaluate attachments.append(Platform.attach\_print(self.doctype, self.name, doc = self, print\_format = (self.meta.default\_print\_format or “Standard”), lang = (supplier\_language or system\_language), letterhead = self ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.default\_print\_format → “Standard”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in supplier\_language → system\_language.
- Evaluate self.send\_email(data, sender, rendered\_subject, rendered\_message, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get attachments](operations-006.md#op-aa5c206d8996a9), [send email](operations-006.md#op-277cfddceeda85).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “fixed\_email”), Platform.db.get\_single\_value(“System Settings”, “language”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L2175) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L23)

<a id="op-277cfddceeda85"></a>
### Requestfor Quotation.send email

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_send_email`

**Inputs** self, data, sender, subject, message, attachments.

**State and service calls** msgprint with translated “Email Sent to Supplier {0}”.format(data.supplier).

**Local steps**

- Evaluate make(subject = subject, content = message, recipients = data.email\_id, sender = sender, …) at “name”.
- Evaluate Platform.msgprint(translated “Email Sent to Supplier {0}”.format(data.supplier)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L3461) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L19)

<a id="op-aa5c206d8996a9"></a>
### Requestfor Quotation.get attachments

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_get_attachments`

**Inputs** self.

**Explicit results** list of d.name for d drawn from get\_attachments(self.doctype, self.name).

**Local steps**

- Return list of d.name for d drawn from get\_attachments(self.doctype, self.name).
  - Draw d from get\_attachments(self.doctype, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L3710) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L13)

<a id="op-bdbf2cd9984ba0"></a>
### Requestfor Quotation.update rfq supplier status

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_update_request_for_quotation_supplier_status`

**Inputs** self, sup\_name = no value.

**Record and data access** execute query text (SELECT, Supplier Quotation Item).

**Local steps**

- For each supplier in self.suppliers.
  - If (sup\_name is identical to no value or supplier.supplier equals sup\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sup\_name is identical to no value → supplier.supplier equals sup\_name.
    - Set quote\_status from translated “Received”.
    - For each item in self.items.
      - Set sqi\_count from Platform.db.sql(query text (SELECT, Supplier Quotation Item), mapping(“supplier” → supplier.supplier, “rqi” → item.name), as\_dict = 1) at 0.
      - If sqi\_count.count equals 0.
        - Set quote\_status from translated “Pending”.
    - Set supplier.quote\_status from quote\_status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L25)

<a id="op-4a52001e2fd338"></a>
### Send supplier emails

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_send_supplier_emails`

**Inputs** rfq\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Request for Quotation” via get\_doc.

**Local steps**

- Evaluate check\_portal\_enabled(“Request for Quotation”).
- Set rfq from Platform.get\_doc(“Request for Quotation”, rfq\_name, check\_permission = “write”).
- If rfq.docstatus equals 1.
  - Evaluate rfq.send\_to\_supplier().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L33)

<a id="op-f635b3fdfc166e"></a>
### Check portal enabled

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_check_portal_enabled`

**Inputs** reference\_doctype.

**Record and data access** read “Portal Menu Item” via get\_value.

**Explicit failure paths** validation helper — translated “The Access to Request for Quotation From Portal is Disabled. To Allow Access, Enable it in Portal Settings.”.

**Local steps**

- If not Platform.db.get\_value(“Portal Menu Item”, mapping(“reference\_doctype” → reference\_doctype), “enabled”).
  - Call the validation error handler Platform.throw(translated “The Access to Request for Quotation From Portal is Disabled. To Allow Access, Enable it in Portal Settings.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L5)

<a id="op-33f24d3c98f1fa"></a>
### Get list context

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Request for Quotation”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L4745) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L6)

<a id="op-9f84f8a806241f"></a>
### Make supplier quotation from rfq

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_make_supplier_quotation_from_rfq`

**Inputs** source\_name, target\_doc = no value, for\_supplier = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation postprocess for subsequent calls.
- Set doclist from get\_mapped\_doc(“Request for Quotation”, source\_name, mapping(“Request for Quotation” → mapping(“doctype” → “Supplier Quotation”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping(“o ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L829) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L69)

<a id="op-bde03e8be2ffcf"></a>
### Make supplier quotation from rfq.postprocess

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_make_supplier_quotation_from_rfq_postprocess`

**Inputs** source, target\_doc.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- If for\_supplier.
  - Set target\_doc.supplier from for\_supplier.
  - Set args from \_get\_party\_details(for\_supplier, party\_type = “Supplier”, ignore\_permissions = true).
  - Set target\_doc.currency from (args.currency or get\_party\_account\_currency(“Supplier”, for\_supplier, source.company)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.currency → get\_party\_account\_currency(“Supplier”, for\_supplier, source.company).
  - Set target\_doc.buying\_price\_list from (args.buying\_price\_list or Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.buying\_price\_list → Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”).
- Evaluate set\_missing\_values(source, target\_doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L830) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L70)

<a id="op-7adddfc6239396"></a>
### Create supplier quotation

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_create_supplier_quotation`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Portal User” via get\_all · resolve a document from mapping(“doctype” → “Supplier Quotation”, “supplier” → supplier, “terms” → doc.get(“terms”), “company” → rfq.company, …) via get\_doc · read “Buying Settings” via get\_single\_value.

**State and service calls** call save on sq\_doc · msgprint with translated “Supplier Quotation {0} Created”.format(sq\_doc.name).

**Explicit results** sq\_doc.name.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set supplier from doc.get(“supplier”).
- If Platform.session.user does not belong to Platform.get\_all(“Portal User”, mapping(“parenttype” → “Supplier”, “parent” → supplier), pluck = “user”).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set rfq from get\_quotable\_rfq(doc.get(“name”), supplier).
- Evaluate validate\_existing\_supplier\_quotation(supplier, rfq.name).
- Set sq\_doc from Platform.get\_doc(mapping(“doctype” → “Supplier Quotation”, “supplier” → supplier, “terms” → doc.get(“terms”), “company” → rfq.company, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“currency”) → get\_party\_account\_currency(“Supplier”, supplier, rfq.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“buying\_price\_list”) → Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”).
- Evaluate add\_items(sq\_doc, supplier, rfq, doc.get(“items”)).
- Set sq\_doc.flags.ignore\_permissions from true.
- Evaluate sq\_doc.run\_method(“set\_missing\_values”).
- Evaluate sq\_doc.save().
- Evaluate Platform.msgprint(translated “Supplier Quotation {0} Created”.format(sq\_doc.name)).
- Return sq\_doc.name.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”) · selected callable from sq\_doc.run\_method(“set\_missing\_values”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L826) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L66)

<a id="op-36f3866520c01c"></a>
### Get quotable rfq

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_get_quotable_rfq`

**Inputs** rfq\_name, supplier.

**Record and data access** resolve a document from “Request for Quotation” via get\_doc.

**Explicit results** rfq.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set rfq from Platform.get\_doc(“Request for Quotation”, rfq\_name).
- If (rfq.docstatus differs from 1 or supplier does not belong to set of row.supplier for row drawn from rfq.suppliers).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rfq.docstatus differs from 1 → supplier does not belong to set of row.supplier for row drawn from rfq.suppliers.
  - Draw row from rfq.suppliers.
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Return rfq.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L828) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L68)

<a id="op-ac5bc625758019"></a>
### Validate existing supplier quotation

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_validate_existing_supplier_quotation`

**Inputs** supplier, request\_for\_quotation.

**Explicit failure paths** validation helper — translated “Supplier Quotation {0} already exists against Request for Quotation {1}”.format(Platform.bold(existing\_quotation at 0.name), Platform.bold(request\_for\_quotation)).

**Local steps**

- Set rfq from Platform.qb.DocType(“Request for Quotation”).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals request\_for\_quotation).for\_update().run().
- Set sq from Platform.qb.DocType(“Supplier Quotation”).
- Set sqi from Platform.qb.DocType(“Supplier Quotation Item”).
- Set existing\_quotation from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
- If existing\_quotation.
  - Call the validation error handler Platform.throw(translated “Supplier Quotation {0} already exists against Request for Quotation {1}”.format(Platform.bold(existing\_quotation at 0.name), Platform.bold(request\_for\_quotation))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L832) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L72)

<a id="op-f6afaa544ce321"></a>
### Add items

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_add_items`

**Inputs** sq\_doc, supplier, rfq, items.

**Explicit failure paths** validation helper — translated “Row {0} is not part of Request for Quotation {1}.”.format(data.idx, rfq.name).

**Local steps**

- Set rfq\_rows from mapping of row.name → row for row drawn from rfq.items.
  - Draw row from rfq.items.
- Set dimension\_fields from get\_accounting\_dimensions().
- For each data in items.
  - If isinstance(data, dict).
    - Set data from Platform.\_dict(data).
  - If data.name does not belong to rfq\_rows.
    - Call the validation error handler Platform.throw(translated “Row {0} is not part of Request for Quotation {1}.”.format(data.idx, rfq.name)).
  - Evaluate create\_rfq\_items(sq\_doc, supplier, rfq\_rows at data.name, data, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L64)
