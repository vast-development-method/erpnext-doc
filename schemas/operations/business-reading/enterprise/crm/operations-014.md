# Sales relationships · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-c915b72b8bbfb6"></a>
### Get last issue from customer

`operation_enterprise_customer_relationship_management_record_definitions_utils_business_behavior_get_last_issue_from_customer`

**Inputs** customer\_name.

**Record and data access** read “Issue” via get\_all.

**Explicit results** issues at 0 when issues, otherwise no value.

**Local steps**

- Set issues from Platform.get\_all(“Issue”, mapping(“customer” → customer\_name), list(“name”, “subject”, “customer”), order\_by = “′creation′ DESC”, limit = 1).
- Return issues at 0 when issues, otherwise no value.
  - Value choice on issues — true gives issues at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1282)

<a id="op-f369d8d7b2b1c0"></a>
### Get scheduled employees for popup

`operation_enterprise_customer_relationship_management_record_definitions_utils_business_behavior_get_scheduled_employees_for_popup`

**Inputs** communication\_medium.

**Record and data access** read “Communication Medium” via get\_value · read “Communication Medium Timeslot” via get\_all.

**Explicit results** list() · set() · set(nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).where((nested operand in the contract.isnotnull() bitwise and nested operand in the contract.user\_ …).

**Local steps**

- If not communication\_medium.
  - Return list().
- Set medium from Platform.db.get\_value(“Communication Medium”, communication\_medium, list(“disabled”, “catch\_all”), as\_dict = true).
- If (medium and medium.disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in medium → medium.disabled.
  - Return list().
- Set now\_time from Platform.utils.nowtime().
- Set weekday from Platform.utils.get\_weekday().
- Set available\_employee\_groups from Platform.get\_all(“Communication Medium Timeslot”, filters = mapping(“day\_of\_week” → weekday, “parent” → communication\_medium, “from\_time” → list(“&lt;=”, now\_time), “to\_time” → list(“&gt;=”, now\_time)), fields = ….
- Set available\_employee\_groups from tuple(list of emp.employee\_group for emp drawn from available\_employee\_groups).
  - Draw emp from available\_employee\_groups.
- If (not available\_employee\_groups and medium and medium.catch\_all).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not available\_employee\_groups → medium → medium.catch\_all.
  - Set available\_employee\_groups from tuple(medium.catch\_all).
- If not available\_employee\_groups.
  - Return set().
- Set member from Platform.qb.DocType(“Employee Group Table”).
- Set employee from Platform.qb.DocType(“Employee”).
- Return set(nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).where((nested operand in the contract.isnotnull() bitwise and nested operand in the contract.user\_ …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1283)

<a id="op-19e7e1daef733a"></a>
### Strip number

`operation_enterprise_customer_relationship_management_record_definitions_utils_business_behavior_strip_number`

**Inputs** number.

**Declared result** (str bitwise or no value).

**Explicit results** no value · empty text.join(generator of character for character drawn from number where character.isdigit()).lstrip(“0”).

**Local steps**

- If not number.
  - Return no value.
- Return empty text.join(generator of character for character drawn from number where character.isdigit()).lstrip(“0”).
  - Draw character from number, keep a combination only if (character.isdigit()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1284)

<a id="op-a24ff957613004"></a>
### Get phone number key

`operation_enterprise_binding_enterprise_crm_doctype_utils_get_phone_number_key`

**Inputs** number.

**Declared result** (str bitwise or no value).

**Explicit results** no value · digits at slice negative PHONE\_NUMBER\_MATCH\_LENGTH to no value.

**Local steps**

- Set digits from strip\_number(number).
- If (not digits or len(digits) &lt; MINIMUM\_PHONE\_NUMBER\_LENGTH).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not digits → len(digits) &lt; MINIMUM\_PHONE\_NUMBER\_LENGTH.
  - Return no value.
- Return digits at slice negative PHONE\_NUMBER\_MATCH\_LENGTH to no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L553)

<a id="op-ea67ed2603cb6d"></a>
### Get phone number like pattern

`operation_enterprise_binding_enterprise_crm_doctype_utils_get_phone_number_like_pattern`

**Inputs** key.

**Declared result** str.

**Explicit results** ((“%” + “%”.join(key at slice negative MINIMUM\_PHONE\_NUMBER\_LENGTH to no value)) + “%”).

**Local steps**

- Return ((“%” + “%”.join(key at slice negative MINIMUM\_PHONE\_NUMBER\_LENGTH to no value)) + “%”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L554)

<a id="op-7396a4e8fca780"></a>
### Get contacts with phone number

`operation_enterprise_binding_enterprise_crm_doctype_utils_get_contacts_with_phone_number`

**Inputs** number.

**Declared result** list at str.

**Record and data access** read “Contact Phone” via get\_all.

**Explicit results** list() · list(dict.fromkeys(generator of phone.parent for phone drawn from phones where get\_phone\_number\_key(phone.phone) equals key)).

**Local steps**

- If not key bound to get\_phone\_number\_key(number).
  - Return list().
- Set phones from Platform.get\_all(“Contact Phone”, filters = mapping(“parenttype” → “Contact”, “phone” → list(“like”, get\_phone\_number\_like\_pattern(key))), fields = list(“parent”, “phone”)).
- Return list(dict.fromkeys(generator of phone.parent for phone drawn from phones where get\_phone\_number\_key(phone.phone) equals key)).
  - Draw phone from phones, keep a combination only if (get\_phone\_number\_key(phone.phone) equals key).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L552)

<a id="op-869a0e275fb2eb"></a>
### Disable opportunity creation on contact us disabled

`operation_enterprise_customer_relationship_management_utils_business_behavior_disable_opportunity_creation_on_contact_us_disabled`

**Inputs** doc, method.

**State and service calls** request set\_single\_value on “CRM Settings”.

**Local steps**

- If doc.is\_disabled.
  - Evaluate Platform.db.set\_single\_value(“CRM Settings”, “enable\_opportunity\_creation\_from\_contact\_us”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0440.json#L7445) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1362)

<a id="op-259a7dda85c4f6"></a>
### Update lead phone numbers

`operation_enterprise_customer_relationship_management_utils_business_behavior_update_lead_phone_numbers`

**Inputs** contact, method.

**Record and data access** read “Lead” via get\_value.

**State and service calls** request set\_value on “Lead”.

**Explicit results** no value.

**Local steps**

- Set lead from contact.get\_link\_for(“Lead”).
- If not (lead and (contact.phone\_nos or had\_phone\_numbers(contact))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead → (contact.phone\_nos or had\_phone\_numbers(contact)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact.phone\_nos → had\_phone\_numbers(contact).
  - Return no value.
- Set numbers from get\_lead\_phone\_numbers(contact).
- Set current from Platform.db.get\_value(“Lead”, lead, list(numbers), as\_dict = true).
- If changed bound to mapping of field → number for tuple(field, number) drawn from numbers.items() where (current.get(field) or empty text) differs from number.
  - Draw tuple(field, number) from numbers.items(), keep a combination only if ((current.get(field) or empty text) differs from number).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current.get(field) → empty text.
  - Evaluate Platform.db.set\_value(“Lead”, lead, changed, update\_modified = false).
  - Evaluate link\_existing\_conversations\_of\_lead(lead).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1378)

<a id="op-fcf5f9bded70cc"></a>
### Get lead phone numbers

`operation_enterprise_binding_enterprise_crm_utils_get_lead_phone_numbers`

**Inputs** contact.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“phone” → (contact.phone or empty text), “mobile\_no” → (contact.mobile\_no or empty text)) · mapping(“phone” → first\_number, “mobile\_no” → first\_number).

**Local steps**

- If (contact.phone or contact.mobile\_no or not contact.phone\_nos).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact.phone → contact.mobile\_no → not contact.phone\_nos.
  - Return mapping(“phone” → (contact.phone or empty text), “mobile\_no” → (contact.mobile\_no or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact.phone → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact.mobile\_no → empty text.
- Set first\_number from contact.phone\_nos at 0.phone.
- Return mapping(“phone” → first\_number, “mobile\_no” → first\_number).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L577)

<a id="op-6bf5fa821f39fd"></a>
### Had phone numbers

`operation_enterprise_binding_enterprise_crm_utils_had_phone_numbers`

**Inputs** contact.

**Declared result** bool.

**Explicit results** bool((previous and previous.phone\_nos)).

**Local steps**

- Set previous from contact.get\_doc\_before\_save().
- Return bool((previous and previous.phone\_nos)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.phone\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L578)

<a id="op-7f4f7c8c59c36e"></a>
### Link existing conversations of lead

`operation_enterprise_binding_enterprise_crm_utils_link_existing_conversations_of_lead`

**Inputs** lead.

**Record and data access** resolve a document from “Lead” via get\_doc.

**Local steps**

- Bind dependencies link\_existing\_conversations.
- Evaluate link\_existing\_conversations(Platform.get\_doc(“Lead”, lead), “on\_update”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L579)

<a id="op-4a38fa3f38ee33"></a>
### Copy comments

`operation_enterprise_customer_relationship_management_utils_business_behavior_copy_comments`

**Inputs** doctype, docname, doc, ignore\_permissions = false.

**Record and data access** read “Comment” via get\_values · resolve a document from comment.update(mapping(“doctype” → “Comment”)) via get\_doc.

**State and service calls** call insert on comment.

**Explicit results** no value.

**Local steps**

- If not can\_read\_source(doctype, docname, ignore\_permissions).
  - Return no value.
- Set comments from Platform.db.get\_values(“Comment”, filters = mapping(“reference\_doctype” → doctype, “reference\_name” → docname, “comment\_type” → “Comment”), fieldname = “\*”).
- For each comment in comments.
  - Set comment from Platform.get\_doc(comment.update(mapping(“doctype” → “Comment”))).
  - Set comment.name from no value.
  - Set comment.reference\_doctype from doc.doctype.
  - Set comment.reference\_name from doc.name.
  - Evaluate comment.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1358)

<a id="op-f679826bc19fb4"></a>
### Link communications

`operation_enterprise_customer_relationship_management_utils_business_behavior_link_communications`

**Inputs** doctype, docname, doc, ignore\_permissions = false.

**Record and data access** resolve a document from “Communication” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not can\_read\_source(doctype, docname, ignore\_permissions).
  - Return no value.
- Set communication\_list from get\_linked\_communication\_list(doctype, docname).
- For each communication in communication\_list.
  - Set communication\_doc from Platform.get\_doc(“Communication”, communication).
  - Evaluate communication\_doc.add\_link(doc.doctype, doc.name, autosave = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1372)

<a id="op-9d6c448ed02906"></a>
### Get linked communication list

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_linked_communication_list`

**Inputs** doctype, docname.

**Record and data access** read “Communication” via get\_all · read “Communication Link” via get\_all.

**Explicit results** (communications + communication\_links).

**Local steps**

- Set communications from Platform.get\_all(“Communication”, filters = mapping(“reference\_doctype” → doctype, “reference\_name” → docname), pluck = “name”).
- Set communication\_links from Platform.get\_all(“Communication Link”, mapping(“link\_doctype” → doctype, “link\_name” → docname, “parent” → tuple(“not in”, communications)), pluck = “parent”).
- Return (communications + communication\_links).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0443.json#L1205) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1367)

<a id="op-721d33a1f3aa18"></a>
### Link communications with prospect

`operation_enterprise_customer_relationship_management_utils_business_behavior_link_communications_with_prospect`

**Inputs** communication, method.

**State and service calls** call db\_update on row.

**Local steps**

- Set prospect from get\_linked\_prospect(communication.reference\_doctype, communication.reference\_name).
- If prospect.
  - Set already\_linked from any(list of d.name for d drawn from communication.get(“timeline\_links”) where (d.link\_doctype equals “Prospect” and d.link\_name equals prospect)).
    - Draw d from communication.get(“timeline\_links”), keep a combination only if ((d.link\_doctype equals “Prospect” and d.link\_name equals prospect)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.link\_doctype equals “Prospect” → d.link\_name equals prospect.
  - If not already\_linked.
    - Set row from communication.append(“timeline\_links”).
    - Set row.link\_doctype from “Prospect”.
    - Set row.link\_name from prospect.
    - Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0443.json#L1463) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1373)

<a id="op-0385787c218ae4"></a>
### Update modified timestamp

`operation_enterprise_customer_relationship_management_utils_business_behavior_update_modified_timestamp`

**Inputs** communication, method.

**Record and data access** read “CRM Settings” via get\_single\_value.

**State and service calls** request set\_value on communication.reference\_doctype.

**Local steps**

- If (communication.reference\_doctype belongs to tuple(“Lead”, “Opportunity”) and communication.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in communication.reference\_doctype belongs to tuple(“Lead”, “Opportunity”) → communication.reference\_name.
  - If (communication.sent\_or\_received equals “Received” and Platform.db.get\_single\_value(“CRM Settings”, “update\_timestamp\_on\_new\_communication”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in communication.sent\_or\_received equals “Received” → Platform.db.get\_single\_value(“CRM Settings”, “update\_timestamp\_on\_new\_communication”).
    - Evaluate Platform.db.set\_value(dt = communication.reference\_doctype, dn = communication.reference\_name, field = “modified”, val = now(), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “update\_timestamp\_on\_new\_communication”) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1379)

<a id="op-d242bc77d484a3"></a>
### Get linked prospect

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_linked_prospect`

**Inputs** reference\_doctype, reference\_name.

**Record and data access** read “Prospect Lead” via get\_value · read “Opportunity” via get\_value · read “Prospect Opportunity” via get\_value.

**Explicit results** prospect.

**Local steps**

- Set prospect from no value.
- If reference\_doctype equals “Lead”.
  - Set prospect from Platform.db.get\_value(“Prospect Lead”, mapping(“lead” → reference\_name), “parent”).
- Otherwise.
  - If reference\_doctype equals “Opportunity”.
    - Set tuple(opportunity\_from, party\_name) from Platform.db.get\_value(“Opportunity”, reference\_name, list(“opportunity\_from”, “party\_name”)).
    - If opportunity\_from equals “Lead”.
      - Set prospect from Platform.db.get\_value(“Prospect Opportunity”, mapping(“opportunity” → reference\_name), “parent”).
    - If opportunity\_from equals “Prospect”.
      - Set prospect from party\_name.
- Return prospect.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1368)

<a id="op-355f0ef638fcae"></a>
### Link events with prospect

`operation_enterprise_customer_relationship_management_utils_business_behavior_link_events_with_prospect`

**Inputs** event, method.

**State and service calls** call save on event.

**Local steps**

- If event.event\_participants.
  - Set ref\_doctype from event.event\_participants at 0.reference\_doctype.
  - Set ref\_docname from event.event\_participants at 0.reference\_docname.
  - Set prospect from get\_linked\_prospect(ref\_doctype, ref\_docname).
  - If prospect.
    - Evaluate event.add\_participant(“Prospect”, prospect).
    - Evaluate event.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L393) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1374)

<a id="op-2ba5bafe3192b7"></a>
### Link open tasks

`operation_enterprise_customer_relationship_management_utils_business_behavior_link_open_tasks`

**Inputs** ref\_doctype, ref\_docname, doc, ignore\_permissions = false.

**Record and data access** resolve a document from “ToDo” via get\_doc.

**State and service calls** call save on todo\_doc.

**Explicit results** no value.

**Local steps**

- If not can\_read\_source(ref\_doctype, ref\_docname, ignore\_permissions).
  - Return no value.
- Set todos from get\_open\_todos(ref\_doctype, ref\_docname).
- For each todo in todos.
  - Set todo\_doc from Platform.get\_doc(“ToDo”, todo.name).
  - Set todo\_doc.reference\_type from doc.doctype.
  - Set todo\_doc.reference\_name from doc.name.
  - Evaluate todo\_doc.save(ignore\_permissions = ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1376)

<a id="op-8ec4df1d2daf46"></a>
### Link open events

`operation_enterprise_customer_relationship_management_utils_business_behavior_link_open_events`

**Inputs** ref\_doctype, ref\_docname, doc, ignore\_permissions = false.

**Record and data access** resolve a document from “Event” via get\_doc.

**State and service calls** call save on event\_doc.

**Explicit results** no value.

**Local steps**

- If not can\_read\_source(ref\_doctype, ref\_docname, ignore\_permissions).
  - Return no value.
- Set events from get\_open\_events(ref\_doctype, ref\_docname).
- For each event in events.
  - Set event\_doc from Platform.get\_doc(“Event”, event.name).
  - Evaluate event\_doc.add\_participant(doc.doctype, doc.name).
  - Evaluate event\_doc.save(ignore\_permissions = ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1375)

<a id="op-021149731eea34"></a>
### Get open activities

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_open_activities`

**Inputs** ref\_doctype, ref\_docname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“tasks” → tasks, “events” → events, “tasks\_history” → tasks\_history, “events\_history” → events\_history).

**Local steps**

- Evaluate Platform.has\_permission(ref\_doctype, doc = ref\_docname, throw = true).
- Set tasks from get\_open\_todos(ref\_doctype, ref\_docname).
- Set events from get\_open\_events(ref\_doctype, ref\_docname).
- Set tasks\_history from get\_closed\_todos(ref\_doctype, ref\_docname).
- Set events\_history from get\_closed\_events(ref\_doctype, ref\_docname).
- Return mapping(“tasks” → tasks, “events” → events, “tasks\_history” → tasks\_history, “events\_history” → events\_history).

**Values supplied outside this operation** effective access from Platform.has\_permission(ref\_doctype, doc = ref\_docname, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1369)

<a id="op-a5487ef623d7db"></a>
### Get closed todos

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_closed_todos`

**Inputs** ref\_doctype, ref\_docname.

**Explicit results** get\_filtered\_todos(ref\_doctype, ref\_docname, status = tuple(“!=”, “Open”)).

**Local steps**

- Return get\_filtered\_todos(ref\_doctype, ref\_docname, status = tuple(“!=”, “Open”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1229) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1364)

<a id="op-429c8a1480bbf7"></a>
### Get open todos

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_open_todos`

**Inputs** ref\_doctype, ref\_docname.

**Explicit results** get\_filtered\_todos(ref\_doctype, ref\_docname, status = “Open”).

**Local steps**

- Return get\_filtered\_todos(ref\_doctype, ref\_docname, status = “Open”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1312) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1371)

<a id="op-d3e3aa9bf2c1f4"></a>
### Get open events

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_open_events`

**Inputs** ref\_doctype, ref\_docname.

**Explicit results** get\_filtered\_events(ref\_doctype, ref\_docname, open = true).

**Local steps**

- Return get\_filtered\_events(ref\_doctype, ref\_docname, open = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1386) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1370)
