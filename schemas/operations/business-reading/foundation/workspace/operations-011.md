# Forms, reports and navigation · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Contact

[Record definition](../../../../data/record-types/contact.json)

<a id="op-fbb983fe6bdf69"></a>
### Contact.has common link

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_has_common_link`

**Inputs** self, doc.

**Explicit results** true.

**Local steps**

- Set reference\_links from list of tuple(link.link\_doctype, link.link\_name) for link drawn from doc.links.
  - Draw link from doc.links.
- For each link in self.links.
  - If tuple(link.link\_doctype, link.link\_name) belongs to reference\_links.
    - Return true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L2998) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L845)

<a id="op-1b8ebc09b539e5"></a>
### Contact.add email

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_add_email`

**Inputs** self, email\_id, is\_primary = 0, autosave = false.

**Record and data access** read “Contact Email” via exists.

**State and service calls** call save on self.

**Local steps**

- If not Platform.db.exists(“Contact Email”, mapping(“email\_id” → email\_id, “parent” → self.name)).
  - Evaluate self.append(“email\_ids”, mapping(“email\_id” → email\_id, “is\_primary” → is\_primary)).
  - If autosave.
    - Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L837)

<a id="op-641aee69c96cbe"></a>
### Contact.add phone

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_add_phone`

**Inputs** self, phone, is\_primary\_phone = 0, is\_primary\_mobile\_no = 0, autosave = false.

**Record and data access** read “Contact Phone” via exists.

**State and service calls** call save on self.

**Local steps**

- If not Platform.db.exists(“Contact Phone”, mapping(“phone” → phone, “parent” → self.name)).
  - Evaluate self.append(“phone\_nos”, mapping(“phone” → phone, “is\_primary\_phone” → is\_primary\_phone, “is\_primary\_mobile\_no” → is\_primary\_mobile\_no)).
  - If autosave.
    - Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L3397) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L838)

<a id="op-081bd5e914646c"></a>
### Contact.set primary email

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_set_primary_email`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only one {0} can be set as primary.”.format(Platform.bold(translated “Email ID”)).

**Local steps**

- If not self.email\_ids.
  - Set self.email\_id from empty text.
  - Return no value.
- If len(list of email.email\_id for email drawn from self.email\_ids where email.is\_primary) &gt; 1.
  - Draw email from self.email\_ids, keep a combination only if (email.is\_primary).
  - Call the validation error handler Platform.throw(translated “Only one {0} can be set as primary.”.format(Platform.bold(translated “Email ID”))).
- If len(self.email\_ids) equals 1.
  - Set self.email\_ids at 0.is\_primary from 1.
- Set primary\_email\_exists from false.
- For each d in self.email\_ids.
  - If d.is\_primary equals 1.
    - Set primary\_email\_exists from true.
    - Set self.email\_id from d.email\_id.strip().
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not primary\_email\_exists.
  - Set self.email\_id from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L3669) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L849)

<a id="op-3dfb8843fac1ec"></a>
### Contact.set primary

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_set_primary`

**Inputs** self, fieldname.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only one {0} can be set as primary.”.format(Platform.bold(Platform.unscrub(fieldname))).

**Local steps**

- If len(self.phone\_nos) equals 0.
  - Evaluate setattr(self, fieldname, empty text).
  - Return no value.
- Set field\_name from (“is\_primary\_” + fieldname).
- Set is\_primary from list of phone.phone for phone drawn from self.phone\_nos where phone.get(field\_name).
  - Draw phone from self.phone\_nos, keep a combination only if (phone.get(field\_name)).
- If len(is\_primary) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Only one {0} can be set as primary.”.format(Platform.bold(Platform.unscrub(fieldname)))).
- Set primary\_number\_exists from false.
- For each d in self.phone\_nos.
  - If d.get(field\_name) equals 1.
    - Set primary\_number\_exists from true.
    - Evaluate setattr(self, fieldname, d.phone).
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not primary\_number\_exists.
  - Evaluate setattr(self, fieldname, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L4099) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L848)

<a id="op-9c1a54c56a7ce5"></a>
### Contact.get full name

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_get_full_name`

**Inputs** self.

**Declared result** str.

**Explicit results** get\_full\_name(self.first\_name, self.middle\_name, self.last\_name, self.company\_name).

**Local steps**

- Return get\_full\_name(self.first\_name, self.middle\_name, self.last\_name, self.company\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L4570) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L841)

<a id="op-ab047789721800"></a>
### Contact.get vcard

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_get_vcard`

**Inputs** self.

**Explicit results** vcard.

**Local steps**

- Bind dependencies vCard.
- Bind dependencies Name.
- Set vcard from vCard().
- Set vcard.add(“fn”).value from self.full\_name.
- Set name from Name().
- If self.first\_name.
  - Set name.given from self.first\_name.
- If self.last\_name.
  - Set name.family from self.last\_name.
- If self.middle\_name.
  - Set name.additional from self.middle\_name.
- Set vcard.add(“n”).value from name.
- If self.designation.
  - Set vcard.add(“title”).value from self.designation.
- Set org\_list from list().
- If self.company\_name.
  - Evaluate org\_list.append(self.company\_name).
- If self.department.
  - Evaluate org\_list.append(self.department).
- If org\_list.
  - Set vcard.add(“org”).value from org\_list.
- For each row in self.email\_ids.
  - Set email from vcard.add(“email”).
  - Set email.value from row.email\_id.
  - If row.is\_primary.
    - Set email.type\_param from “pref”.
- For each row in self.phone\_nos.
  - Set tel from vcard.add(“tel”).
  - Set tel.value from row.phone.
  - If row.is\_primary\_phone.
    - Set tel.type\_param from “home”.
  - If row.is\_primary\_mobile\_no.
    - Set tel.type\_param from “cell”.
- Return vcard.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L4652) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L844)

<a id="op-74248cb5e04e8c"></a>
### Download vcard

`operation_foundation_contacts_record_definitions_contact_business_behavior_download_vcard`

**Inputs** contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_doc.

**Local steps**

- Set contact from Platform.get\_doc(“Contact”, contact).
- Evaluate contact.check\_permission().
- Set vcard from contact.get\_vcard().
- Evaluate make\_access\_log(doctype = “Contact”, document = contact.name, file\_type = “vcf”).
- Set Platform.response at “filename” from formatted text {contact.name}.vcf.
- Set Platform.response at “filecontent” from vcard.serialize().encode(“utf-8”).
- Set Platform.response at “type” from “binary”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from contact.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L5349) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L853)

<a id="op-f97ee4fd7a4456"></a>
### Download vcards

`operation_foundation_contacts_record_definitions_contact_business_behavior_download_vcards`

**Inputs** contacts.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_doc.

**Local steps**

- Bind dependencies json.
- Bind dependencies now.
- Set contact\_ids from Platform.parse\_json(contacts).
- Set vcards from list().
- For each contact\_id in contact\_ids.
  - Set contact from Platform.get\_doc(“Contact”, contact\_id).
  - Evaluate contact.check\_permission().
  - Set vcard from contact.get\_vcard().
  - Evaluate vcards.append(vcard.serialize()).
- Evaluate make\_access\_log(doctype = “Contact”, filters = json.dumps(list(list(“name”, “in”, contact\_ids)), ensure\_ascii = false, indent = whitespace '\\t'), file\_type = “vcf”).
- Set timestamp from now() at slice no value to 19.
- Set Platform.response at “filename” from formatted text {timestamp} Contacts.vcf.
- Set Platform.response at “filecontent” from whitespace '\\n'.join(vcards).encode(“utf-8”).
- Set Platform.response at “type” from “binary”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from contact.check\_permission() · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L5673) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L854)

<a id="op-1ccaea7d8ef7c9"></a>
### Get default contact

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_default_contact`

**Inputs** doctype, name.

**Record and data access** execute query text (SELECT, Contact c, Dynamic Link).

**Explicit results** contact.parent · out at 0.parent · no value.

**Local steps**

- Set out from Platform.db.sql(query text (SELECT, Contact c, Dynamic Link), tuple(doctype, name), as\_dict = true).
- If out.
  - For each contact in out.
    - If contact.is\_primary\_contact.
      - Return contact.parent.
  - Return out at 0.parent.
- Otherwise.
  - Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L154) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L861)

<a id="op-fba3b54c81b6fd"></a>
### Invite user

`operation_foundation_contacts_record_definitions_contact_business_behavior_invite_user`

**Inputs** contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_doc · resolve a document from mapping(“doctype” → “User”, “first\_name” → contact.first\_name, “last\_name” → contact.last\_name, “email” → contact.email\_id, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “User”, “first\_name” → contact.first\_name, “last\_name” → contact.last\_name, “email” → contact.email\_id, …)).

**Explicit results** user.name.

**Explicit failure paths** validation helper — translated “Please set Email Address”.

**Local steps**

- Set contact from Platform.get\_doc(“Contact”, contact).
- Evaluate contact.check\_permission().
- If not contact.email\_id.
  - Call the validation error handler Platform.throw(translated “Please set Email Address”).
- Set user from Platform.get\_doc(mapping(“doctype” → “User”, “first\_name” → contact.first\_name, “last\_name” → contact.last\_name, “email” → contact.email\_id, …)).insert().
- Return user.name.

**Values supplied outside this operation** effective access from contact.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L6708) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L863)

<a id="op-2ebf38d49dd113"></a>
### Get contact details

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contact_details`

**Inputs** contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_doc.

**Explicit results** mapping(“contact\_person” → contact.get(“name”), “contact\_display” → contact.get(“full\_name”), “contact\_email” → contact.get(“email\_id”), “contact\_mobile” → contact.get(“mobile\_no”), …).

**Local steps**

- Set contact from Platform.get\_doc(“Contact”, contact).
- Evaluate contact.check\_permission().
- Return mapping(“contact\_person” → contact.get(“name”), “contact\_display” → contact.get(“full\_name”), “contact\_email” → contact.get(“email\_id”), “contact\_mobile” → contact.get(“mobile\_no”), …).

**Values supplied outside this operation** effective access from contact.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L7042) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L855)

<a id="op-06d1d95b9eb739"></a>
### Update contact

`operation_foundation_contacts_record_definitions_contact_business_behavior_update_contact`

**Inputs** doc, method.

**Record and data access** read “Contact” via get\_value · resolve a document from “Contact” via get\_doc.

**State and service calls** call save on contact.

**Local steps**

- Set contact\_name from Platform.db.get\_value(“Contact”, mapping(“email\_id” → doc.name)).
- If contact\_name.
  - Set contact from Platform.get\_doc(“Contact”, contact\_name).
  - For each key in tuple(“first\_name”, “last\_name”, “phone”).
    - If doc.get(key).
      - Evaluate contact.set(key, doc.get(key)).
  - Set contact.flags.ignore\_mandatory from true.
  - Evaluate contact.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L864)

<a id="op-bdd153179b83af"></a>
### Contact query

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**State and service calls** execute a supplied database query.

**Explicit results** list() · Platform.db.sql(formatted text select  ′tabContact′.name, ′tabContact′.full\_name, ′tabContact′.company\_name  from  ′tabContact′, ′tabDynamic Link′  where  ′tabDynamic Link′., mapping(“txt” → ((“%”  ….

**Local steps**

- Bind dependencies get\_match\_cond.
- Set doctype from “Contact”.
- If (not Platform.get\_meta(doctype).get\_field(searchfield) and searchfield does not belong to Platform.db.DEFAULT\_COLUMNS).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.get\_meta(doctype).get\_field(searchfield) → searchfield does not belong to Platform.db.DEFAULT\_COLUMNS.
  - Return list().
- Set link\_doctype from filters.pop(“link\_doctype”, no value).
- Set link\_name from filters.pop(“link\_name”, no value).
- Return Platform.db.sql(formatted text select  ′tabContact′.name, ′tabContact′.full\_name, ′tabContact′.company\_name  from  ′tabContact′, ′tabDynamic Link′  where  ′tabDynamic Link′., mapping(“txt” → ((“%”  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L153) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L847)

<a id="op-b03589f2f60d1a"></a>
### Address query

`operation_foundation_contacts_record_definitions_contact_business_behavior_address_query`

**Inputs** links.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Address).

**Explicit results** result.

**Local steps**

- Bind dependencies json.
- Set links from list of mapping(“link\_doctype” → d.get(“link\_doctype”), “link\_name” → d.get(“link\_name”)) for d drawn from json.loads(links).
  - Draw d from json.loads(links).
- Set result from list().
- For each link in links.
  - If not Platform.has\_permission(doctype = link.get(“link\_doctype”), ptype = “read”, doc = link.get(“link\_name”)).
    - Continue with the next iteration or loop test.
  - Set res from Platform.db.sql(query text (SELECT, Address), mapping(“link\_doctype” → link.get(“link\_doctype”), “link\_name” → link.get(“link\_name”)), as\_dict = true).
  - Evaluate result.extend(list of l.name for l drawn from res).
    - Draw l from res.
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype = link.get(“link\_doctype”), ptype = “read”, doc = link.get(“link\_name”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L152) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L836)

<a id="op-69d428d019c815"></a>
### Get contact with phone number

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contact_with_phone_number`

**Inputs** number.

**Record and data access** read “Contact Phone” via get\_all.

**Explicit results** no value · contacts at 0.parent when contacts, otherwise no value.

**Local steps**

- If not number.
  - Return no value.
- Set contacts from Platform.get\_all(“Contact Phone”, filters = list(list(“phone”, “like”, formatted text %{number})), fields = list(“parent”), limit = 1).
- Return contacts at 0.parent when contacts, otherwise no value.
  - Value choice on contacts — true gives contacts at 0.parent, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L1858) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L858)

<a id="op-581f92faf54651"></a>
### Get contact name

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contact_name`

**Inputs** email\_id.

**Declared result** (str bitwise or no value).

**Record and data access** read “Contact Email” via get\_all · read “Contact” via exists.

**Explicit results** contact\_id.

**Local steps**

- For each contact\_id in Platform.get\_all(“Contact Email”, filters = mapping(“email\_id” → email\_id, “parenttype” → “Contact”), pluck = “parent”).
  - If Platform.db.exists(“Contact”, contact\_id).
    - Return contact\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L2052) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L857)

<a id="op-f850e24da38c19"></a>
### Get contacts linking to

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contacts_linking_to`

**Inputs** doctype, docname, fields = no value.

**Record and data access** read “Contact” via get\_list.

**Explicit results** Platform.get\_list(“Contact”, fields = fields, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, docname))).

**Local steps**

- Return Platform.get\_list(“Contact”, fields = fields, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, docname))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L2245) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L860)

<a id="op-2bb2c5cfcf8b3b"></a>
### Get contacts linked from

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contacts_linked_from`

**Inputs** doctype, docname, fields = no value.

**Record and data access** read doctype via get\_value · read “Contact” via get\_list.

**Explicit results** list() · Platform.get\_list(“Contact”, fields = fields, filters = mapping(“name” → tuple(“in”, contact\_names))).

**Local steps**

- Set link\_fields from Platform.get\_meta(doctype).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Contact”)).
- If not link\_fields.
  - Return list().
- Set contact\_names from Platform.get\_value(doctype, docname, fieldname = list of f.fieldname for f drawn from link\_fields).
  - Draw f from link\_fields.
- If not contact\_names.
  - Return list().
- Return Platform.get\_list(“Contact”, fields = fields, filters = mapping(“name” → tuple(“in”, contact\_names))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L2405) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L859)

<a id="op-a35f2f7dcf2e03"></a>
### Get full name

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_full_name`

**Inputs** first = no value, middle = no value, last = no value, company = no value.

**Declared result** str.

**Explicit results** full\_name.

**Local steps**

- Set full\_name from one space.join(filter(no value, list of cstr(f).strip() for f drawn from list(first, middle, last))).
  - Draw f from list(first, middle, last).
- If (not full\_name and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not full\_name → company.
  - Set full\_name from company.
- Return full\_name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L2730) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L862)

<a id="op-dd00501bce5901"></a>
### Get contact display list

`operation_foundation_contacts_record_definitions_contact_business_behavior_get_contact_display_list`

**Inputs** doctype, name.

**Declared result** list at dict.

**Record and data access** read “Contact” via get\_list.

**Explicit results** list() · Platform.get\_list(“Contact”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name), list(“Dynamic Link”, “parenttype”, “=”, “Contact”)), fields = l ….

**Local steps**

- If not Platform.has\_permission(“Contact”, “read”).
  - Return list().
- Return Platform.get\_list(“Contact”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name), list(“Dynamic Link”, “parenttype”, “=”, “Contact”)), fields = l ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0035.json#L2993) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L856)

## Service · Contact

<a id="op-120d3291c94261"></a>
### Get context

`operation_foundation_public_pages_contact_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Contact Us Settings” via get\_doc.

**Explicit results** out.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- Set doc from Platform.get\_doc(“Contact Us Settings”, “Contact Us Settings”).
- If doc.is\_disabled.
  - Set Platform.local.flags.redirect\_location from “/404”.
  - Raise Platform.Redirect.
- If doc.query\_options.
  - Set query\_options from list of opt.strip() for opt drawn from doc.query\_options.replace(“,”, whitespace '\\n').split(whitespace '\\n') where opt.
    - Draw opt from doc.query\_options.replace(“,”, whitespace '\\n').split(whitespace '\\n'), keep a combination only if (opt).
- Otherwise.
  - Set query\_options from list(“Sales”, “Support”, “General”).
- Set out from mapping().
- Evaluate out.update(doc.as\_dict()).
- Evaluate out.update(mapping(“query\_options” → query\_options, “parents” → list(mapping(“name” → translated “Home”, “route” → “/”)))).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L2865) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L29)

<a id="op-a29777b09e9b37"></a>
### Send message

`operation_foundation_public_pages_contact_business_behavior_send_message`

**Inputs** sender, message, subject = “Website Query”.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(limit = 100, seconds = (60 × 60)).

**Record and data access** resolve a document from “Contact Us Settings” via get\_doc · read “Contact Us Settings” via get\_single\_value · read “System Settings” via get\_single\_value · resolve a document from “Communication” via get\_doc.

**State and service calls** sendmail · call insert on Platform.get\_doc(doctype = “Communication”, sender = sender, subject = \_(“New Message from Website Contact Page”, system\_language), sent\_or\_received = “Received”, …).

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(“Contact Us Settings”, “Contact Us Settings”).
- If doc.is\_disabled.
  - Return no value.
- Set sender from validate\_email\_address(sender, throw = true).
- Set message from escape\_html(message).
- Within suppress(Platform.OutgoingEmailError).
  - If forward\_to\_email bound to Platform.db.get\_single\_value(“Contact Us Settings”, “forward\_to\_email”).
    - Evaluate Platform.sendmail(recipients = forward\_to\_email, reply\_to = sender, content = message, subject = subject).
  - If Platform.get\_single\_value(“Contact Us Settings”, “send\_acknowledgement\_email”).
    - Set reply from translated “Thank you for reaching out to us. We will get back to you at the earliest.”.
    - Evaluate Platform.sendmail(recipients = sender, content = formatted text &lt;div style='white-space: pre-wrap'&gt;{reply}&lt;/div&gt;, subject = translated “We've received your query!”).
- Evaluate Platform.clear\_last\_message().
- Set system\_language from Platform.db.get\_single\_value(“System Settings”, “language”).
- Evaluate Platform.get\_doc(doctype = “Communication”, sender = sender, subject = \_(“New Message from Website Contact Page”, system\_language), sent\_or\_received = “Received”, …).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Contact Us Settings”, “forward\_to\_email”), Platform.get\_single\_value(“Contact Us Settings”, “send\_acknowledgement\_email”) and 1 further calls · service or queued work from Platform.sendmail(recipients = forward\_to\_email, reply\_to = sender, content = message, subject = subject), Platform.sendmail(recipients = sender, content = formatted text &lt;div style='white-space: pre-wrap'&gt;{reply}&lt;/div&gt;, subject = translated “We've received your query!”).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L3279) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L30)

## Service · Conversation

<a id="op-5d64533b4882c3"></a>
### Ask clarification

`operation_foundation_binding_foundation_studio_ai_agent_tools_conversation_ask_clarification`

**Inputs** ctx, args.

**Declared result** no value.

**State and service calls** commit.

**Local steps**

- Set question from (args.get(“question”) or “Could you clarify?”).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“question”) → “Could you clarify?”.
- Set options from list of str(o).strip() for o drawn from (args.get(“options”) or list()) where str(o).strip().
  - Draw o from (args.get(“options”) or list()), keep a combination only if (str(o).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“options”) → list().
- Evaluate AISession.try\_append\_message(ctx.session\_id, “assistant”, question, message\_type = “clarification”, task\_type = “agent”, metadata = mapping(“status” → “clarification”, “options” → options)).
- Evaluate Platform.db.commit().
- Evaluate ctx.emit(“clarify”, question = question, options = options).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1758)
