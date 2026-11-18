# Record lifecycle and persistence · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Communication

[Record definition](../../../../data/record-types/communication.json)

<a id="op-b5bcbcec825b9e"></a>
### Communication.bcc list

`operation_foundation_core_record_definitions_communication_business_behavior_communication_blind_carbon_copy_list`

**Inputs** self, exclude\_displayname = true.

**Explicit results** self.\_get\_emails\_list(self.bcc, exclude\_displayname = exclude\_displayname).

**Local steps**

- Return self.\_get\_emails\_list(self.bcc, exclude\_displayname = exclude\_displayname).

**Methods declared on this owner** [get emails list](operations-004.md#op-5bca96592a414f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3723) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1014)

<a id="op-63fe23afff2bf0"></a>
### Communication.get attachments

`operation_foundation_core_record_definitions_communication_business_behavior_communication_get_attachments`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → self.name, “attached\_to\_doctype” → self.DOCTYPE)).

**Local steps**

- Return Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → self.name, “attached\_to\_doctype” → self.DOCTYPE)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3807) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1019)

<a id="op-69fb288c50e3f0"></a>
### Communication.notify change

`operation_foundation_core_record_definitions_communication_business_behavior_communication_notify_change`

**Inputs** self, action.

**State and service calls** publish realtime with “docinfo\_update”.

**Local steps**

- Evaluate Platform.publish\_realtime(“docinfo\_update”, mapping(“doc” → self.as\_dict(), “key” → “communications”, “action” → action), doctype = self.reference\_doctype, docname = self.reference\_name, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“docinfo\_update”, mapping(“doc” → self.as\_dict(), “key” → “communications”, “action” → action), doctype = self.reference\_doctype, docname = self.reference\_name, after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L3967) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1023)

<a id="op-60e47ba317226d"></a>
### Communication.set status

`operation_foundation_core_record_definitions_communication_business_behavior_communication_set_status`

**Inputs** self.

**Local steps**

- If (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Set self.status from “Linked”.
- Otherwise.
  - Set self.status from “Open”.
- If (self.send\_after and self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.send\_after → self.is\_new().
  - Set self.delivery\_status from “Scheduled”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L4123) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1033)

<a id="op-5fbb71fa2088d7"></a>
### Communication.mark email as spam

`operation_foundation_core_record_definitions_communication_business_behavior_communication_mark_email_as_spam`

**Inputs** self.

**Record and data access** read “Email Rule” via exists.

**Local steps**

- If (self.communication\_type equals “Communication” and self.communication\_medium equals “Email” and self.sent\_or\_received equals “Received” and Platform.db.exists(“Email Rule”, mapping(“email\_id” → self.sende ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.communication\_type equals “Communication” → self.communication\_medium equals “Email” → self.sent\_or\_received equals “Received” → Platform.db.exists(“Email Rule”, mapping(“email\_id” → self.sender, “is\_spam” → 1)).
  - Set self.email\_status from “Spam”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L4269) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1022)

<a id="op-96ad80d19c5b22"></a>
### Communication.find

`operation_foundation_core_record_definitions_communication_business_behavior_communication_find`

**Inputs** cls, name, ignore\_error = false.

**Wrappers, in declaration order** classmethod.

**Record and data access** resolve a document from cls.DOCTYPE via get\_doc.

**Explicit results** Platform.get\_doc(cls.DOCTYPE, name) · no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Return Platform.get\_doc(cls.DOCTYPE, name).
- On failure (Platform.DoesNotExistError).
  - If ignore\_error.
    - Return no value.
  - Propagate the active failure.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L4464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1017)

<a id="op-f66b8096d50594"></a>
### Communication.find one by filters

`operation_foundation_core_record_definitions_communication_business_behavior_communication_find_one_by_filters`

**Inputs** cls, order\_by (named only, default no value), remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Record and data access** read cls.DOCTYPE via get\_value.

**Explicit results** cls.find(name) when name, otherwise no value.

**Local steps**

- Set name from Platform.db.get\_value(cls.DOCTYPE, kwargs, order\_by = order\_by).
- Return cls.find(name) when name, otherwise no value.
  - Value choice on name — true gives cls.find(name), false gives no value.

**Methods declared on this owner** [find](operations-005.md#op-96ad80d19c5b22).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L4600) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1018)

<a id="op-6148e510997df9"></a>
### Communication.update db

`operation_foundation_core_record_definitions_communication_business_behavior_communication_update_database`

**Inputs** self, remaining named values kwargs.

**State and service calls** request set\_value on self.DOCTYPE.

**Local steps**

- Evaluate Platform.db.set\_value(self.DOCTYPE, self.name, kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L4738) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1036)

<a id="op-097d60dc3cc74d"></a>
### Communication.set sender full name

`operation_foundation_core_record_definitions_communication_business_behavior_communication_set_sender_full_name`

**Inputs** self.

**Record and data access** read “User” via get\_value · read “Contact” via get\_value.

**Local steps**

- If (not self.sender\_full\_name and self.sender).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sender\_full\_name → self.sender.
  - If self.sender equals “Administrator”.
    - Set self.sender\_full\_name from Platform.db.get\_value(“User”, “Administrator”, “full\_name”).
    - Set self.sender from Platform.db.get\_value(“User”, “Administrator”, “email”).
  - Otherwise.
    - If self.sender equals “Guest”.
      - Set self.sender\_full\_name from self.sender.
      - Set self.sender from no value.
    - Otherwise.
      - If self.sent\_or\_received equals “Sent”.
        - Evaluate validate\_email\_address(self.sender, throw = true).
      - Set tuple(sender\_name, sender\_email) from parse\_addr(self.sender).
      - If sender\_name equals sender\_email.
        - Set sender\_name from no value.
      - Set self.sender from sender\_email.
      - Set self.sender\_full\_name from sender\_name.
      - If not self.sender\_full\_name.
        - Set self.sender\_full\_name from Platform.db.get\_value(“User”, self.sender, “full\_name”).
      - If not self.sender\_full\_name.
        - Set self.sender\_full\_name from Platform.db.get\_value(“Contact”, mapping(“email\_id” → sender\_email), “full\_name”).
      - If not self.sender\_full\_name.
        - Set self.sender\_full\_name from sender\_email.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L163) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1031)

<a id="op-01d41ce643e684"></a>
### Communication.set delivery status

`operation_foundation_core_record_definitions_communication_business_behavior_communication_set_delivery_status`

**Inputs** self, commit = false.

**Record and data access** read “Email Queue” via get\_all.

**State and service calls** call db\_set on self · commit.

**Explicit results** no value.

**Local steps**

- Set delivery\_status from no value.
- Set status\_counts from Counter(Platform.get\_all(“Email Queue”, pluck = “status”, filters = mapping(“communication” → self.name))).
- If self.sent\_or\_received equals “Received”.
  - Return no value.
- If (status\_counts.get(“Not Sent”) or status\_counts.get(“Sending”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status\_counts.get(“Not Sent”) → status\_counts.get(“Sending”).
  - Set delivery\_status from “Sending”.
- Otherwise.
  - If status\_counts.get(“Error”).
    - Set delivery\_status from “Error”.
  - Otherwise.
    - If status\_counts.get(“Expired”).
      - Set delivery\_status from “Expired”.
    - Otherwise.
      - If status\_counts.get(“Sent”).
        - Set delivery\_status from “Sent”.
- If delivery\_status.
  - Evaluate self.db\_set(“delivery\_status”, delivery\_status).
  - Evaluate self.notify\_change(“update”).
  - Evaluate self.notify\_update().
  - If commit.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify change](operations-005.md#op-69fb288c50e3f0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L5545) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1030)

<a id="op-f029bdeb87ab66"></a>
### Communication.parse email for timeline links

`operation_foundation_core_record_definitions_communication_business_behavior_communication_parse_email_for_timeline_links`

**Inputs** self.

**Record and data access** read “Email Account” via get\_value · read “DocType” via exists · read doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_value(“Email Account”, filters = mapping(“enable\_automatic\_linking” → 1)).
  - Return no value.
- For each tuple(doctype, docname) in parse\_email(list(self.recipients, self.cc, self.bcc)).
  - Set doctype from (Platform.db.exists(“DocType”, doctype, cache = true) or Platform.db.exists(“DocType”, Platform.unscrub(doctype), cache = true)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“DocType”, doctype, cache = true) → Platform.db.exists(“DocType”, Platform.unscrub(doctype), cache = true).
  - If doctype.
    - Set docname from Platform.db.get\_value(doctype, docname, ignore = true).
  - If not (doctype and docname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → docname.
    - Continue with the next iteration or loop test.
  - Evaluate self.add\_link(doctype, docname).
  - If not self.reference\_doctype.
    - Set self.reference\_doctype from doctype.
    - Set self.reference\_name from docname.

If control reaches the end, it returns no value.

**Methods declared on this owner** [add link](operations-005.md#op-27446e75e382cb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L6030) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1027)

<a id="op-7634b62db8c026"></a>
### Communication.set timeline links

`operation_foundation_core_record_definitions_communication_business_behavior_communication_set_timeline_links`

**Inputs** self.

**Record and data access** read “Email Account” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.sent\_or\_received equals “Received” and self.find\_one\_by\_filters(message\_id = self.message\_id, email\_account = self.email\_account, sent\_or\_received = “Sent”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sent\_or\_received equals “Received” → self.find\_one\_by\_filters(message\_id = self.message\_id, email\_account = self.email\_account, sent\_or\_received = “Sent”).
  - Return no value.
- Set contacts from list().
- Set create\_contact\_enabled from (self.email\_account and Platform.db.get\_value(“Email Account”, self.email\_account, “create\_contact”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.email\_account → Platform.db.get\_value(“Email Account”, self.email\_account, “create\_contact”).
- Set contacts from get\_contacts(list(self.sender, self.recipients, self.cc, self.bcc), auto\_create\_contact = create\_contact\_enabled).
- For each contact\_name in contacts.
  - Evaluate self.add\_link(“Contact”, contact\_name).
  - Evaluate add\_contact\_links\_to\_communication(self, contact\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [find one by filters](operations-005.md#op-f66b8096d50594), [add link](operations-005.md#op-27446e75e382cb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L6483) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1034)

<a id="op-58fb4e810c916d"></a>
### Communication.deduplicate timeline links

`operation_foundation_core_record_definitions_communication_business_behavior_communication_deduplicate_timeline_links`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.timeline\_links.
  - Return no value.
- Set unique\_links from set of tuple(link.link\_doctype, link.link\_name) for link drawn from self.timeline\_links.
  - Draw link from self.timeline\_links.
- Set self.timeline\_links from list().
- For each tuple(doctype, name) in unique\_links.
  - Evaluate self.add\_link(doctype, name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add link](operations-005.md#op-27446e75e382cb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L6837) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1016)

<a id="op-27446e75e382cb"></a>
### Communication.add link

`operation_foundation_core_record_definitions_communication_business_behavior_communication_add_link`

**Inputs** self, link\_doctype, link\_name, autosave = false.

**Record and data access** read link\_doctype via get\_value.

**State and service calls** call save on self.

**Local steps**

- Set title\_field from Platform.get\_meta(link\_doctype).get\_title\_field().
- Set link\_title from Platform.db.get\_value(link\_doctype, link\_name, title\_field, cache = true, order\_by = no value) when title\_field differs from “name”, otherwise no value.
  - Value choice on title\_field differs from “name” — true gives Platform.db.get\_value(link\_doctype, link\_name, title\_field, cache = true, order\_by = no value), false gives no value.
- Evaluate self.append(“timeline\_links”, mapping(“link\_doctype” → link\_doctype, “link\_name” → link\_name, “link\_title” → (link\_title or link\_name), “communication\_date” → self.communication\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_title → link\_name.
- If autosave.
  - Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L7014) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1011)

<a id="op-9c8b630bbabb3c"></a>
### Communication.get links

`operation_foundation_core_record_definitions_communication_business_behavior_communication_get_links`

**Inputs** self.

**Explicit results** self.timeline\_links.

**Local steps**

- Return self.timeline\_links.

[Applicable decision contract](../../../foundation-decision-contracts/part-0042.json#L7345) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1021)

<a id="op-5a8db8f016306e"></a>
### Communication.remove link

`operation_foundation_core_record_definitions_communication_business_behavior_communication_remove_link`

**Inputs** self, link\_doctype, link\_name, autosave = false, ignore\_permissions = true.

**State and service calls** call save on self.

**Local steps**

- For each l in list(self.timeline\_links).
  - If (l.link\_doctype equals link\_doctype and l.link\_name equals link\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in l.link\_doctype equals link\_doctype → l.link\_name equals link\_name.
    - Evaluate self.timeline\_links.remove(l).
- If autosave.
  - Evaluate self.save(ignore\_permissions = ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1028)

<a id="op-033d922ea0d4d7"></a>
### On doctype update

`operation_foundation_core_record_definitions_communication_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Communication”.

**Local steps**

- Evaluate Platform.db.add\_index(“Communication”, list(“status”, “communication\_type”)).
- Evaluate Platform.db.add\_index(“Communication”, list(“message\_id(140)”)).
- Evaluate Platform.db.add\_index(“Communication”, list(“reference\_doctype”, “reference\_name”, “communication\_date”, “communication\_type”), index\_name = “comm\_ref\_type\_date\_idx”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L221) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1044)

<a id="op-8e6fbb713cae7f"></a>
### Has permission

`operation_foundation_core_record_definitions_communication_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L421) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1043)

<a id="op-eeb6e7cefb8622"></a>
### Get permission query conditions for communication

`operation_foundation_core_record_definitions_communication_business_behavior_get_permission_query_conditions_for_communication`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, no value, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L691) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1042)

<a id="op-31c30efa842559"></a>
### Get contacts

`operation_foundation_core_record_definitions_communication_business_behavior_get_contacts`

**Inputs** email\_strings, auto\_create\_contact = false.

**Declared result** list at str.

**Record and data access** resolve a document from mapping(“doctype” → “Contact”, “first\_name” → contact\_name, “name” → contact\_name) via get\_doc.

**State and service calls** call insert on contact.

**Explicit results** contacts.

**Local steps**

- Set email\_addrs from get\_emails(email\_strings).
- Set contacts from list().
- For each email in email\_addrs.
  - Set email from get\_email\_without\_link(email).
  - Set contact\_name from get\_contact\_name(email).
  - If (not contact\_name and email and auto\_create\_contact).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not contact\_name → email → auto\_create\_contact.
    - Set email\_parts from email.split(“@”).
    - Set first\_name from Platform.unscrub(email\_parts at 0).
    - Attempt the following.
      - Set contact\_name from formatted text {first\_name}-{email\_parts at 1} when first\_name equals “Contact”, otherwise first\_name.
        - Value choice on first\_name equals “Contact” — true gives formatted text {first\_name}-{email\_parts at 1}, false gives first\_name.
      - Set contact from Platform.get\_doc(mapping(“doctype” → “Contact”, “first\_name” → contact\_name, “name” → contact\_name)).
      - Evaluate contact.add\_email(email\_id = email, is\_primary = true).
      - Evaluate contact.insert(ignore\_permissions = true).
      - Set contact\_name from contact.name.
    - On failure (Exception).
      - Set contact\_name from no value.
      - Evaluate contact.log\_error(“Unable to add contact”).
  - If contact\_name.
    - Evaluate contacts.append(contact\_name).
- Return contacts.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L1063) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1039)

<a id="op-ac36fd7abc1874"></a>
### Get emails

`operation_foundation_core_record_definitions_communication_business_behavior_get_emails`

**Inputs** email\_strings.

**Declared result** list at str.

**Explicit results** email\_addrs.

**Local steps**

- Set email\_addrs from list().
- For each email\_string in email\_strings.
  - If email\_string.
    - Set result from getaddresses(list(email\_string)).
    - Evaluate email\_addrs.extend(generator of email at 1 for email drawn from result).
      - Draw email from result.
- Return email\_addrs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L1674) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1041)

<a id="op-4014e29aecef6d"></a>
### Add contact links to communication

`operation_foundation_core_record_definitions_communication_business_behavior_add_contact_links_to_communication`

**Inputs** communication, contact\_name.

**Record and data access** read “Dynamic Link” via get\_all.

**Local steps**

- Set contact\_links from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → “Contact”, “parent” → contact\_name), fields = list(“link\_doctype”, “link\_name”)).
- If contact\_links.
  - For each contact\_link in contact\_links.
    - Evaluate communication.add\_link(contact\_link.link\_doctype, contact\_link.link\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L1855) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1010)

<a id="op-64a74531bd35a9"></a>
### Parse email

`operation_foundation_core_record_definitions_communication_business_behavior_parse_email`

**Inputs** email\_strings.

**Local steps**

- For each email\_string in email\_strings.
  - If not email\_string.
    - Continue with the next iteration or loop test.
  - For each email in email\_string.split(“,”).
    - Set local\_part from email.split(“@”, 1) at 0.strip(“"”).
    - Set tuple(\_user, detail) from tuple(no value, no value).
    - If “+” belongs to local\_part.
      - Set tuple(\_user, detail) from local\_part.split(“+”, 1).
    - Otherwise.
      - If “--” belongs to local\_part.
        - Set tuple(detail, \_user) from local\_part.rsplit(“--”, 1).
    - If not detail.
      - Continue with the next iteration or loop test.
    - Set document\_parts from no value.
    - If “=” belongs to detail.
      - Set document\_parts from detail.split(“=”, 1).
    - Otherwise.
      - If “+” belongs to detail.
        - Set document\_parts from detail.split(“+”, 1).
    - If (not document\_parts or len(document\_parts) differs from 2).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not document\_parts → len(document\_parts) differs from 2.
      - Continue with the next iteration or loop test.
    - Set doctype from unquote\_plus(document\_parts at 0).
    - Set docname from unquote\_plus(document\_parts at 1).
    - yield tuple(doctype, docname).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L2066) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1045)

<a id="op-67e4c9ab989959"></a>
### Get email without link

`operation_foundation_core_record_definitions_communication_business_behavior_get_email_without_link`

**Inputs** email.

**Record and data access** read “Email Account” via get\_all.

**Explicit results** email · formatted text {user}@{domain}.

**Local steps**

- If not Platform.get\_all(“Email Account”, filters = mapping(“enable\_automatic\_linking” → 1)).
  - Return email.
- Attempt the following.
  - Set \_email from email.split(“@”).
  - Set \_local\_part from \_email at 0.strip(“"”).
  - If “+” belongs to \_local\_part.
    - Set user from \_local\_part.split(“+”, 1) at 0.
  - Otherwise.
    - If “--” belongs to \_local\_part.
      - Set user from \_local\_part.split(“--”, 1) at 1.
    - Otherwise.
      - Set user from \_local\_part.
  - Set domain from \_email at 1.
- On failure (IndexError).
  - Return email.
- Return formatted text {user}@{domain}.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0043.json#L2646) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1040)
