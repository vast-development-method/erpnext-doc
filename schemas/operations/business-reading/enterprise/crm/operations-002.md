# Sales relationships · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appointment

[Record definition](../../../../data/record-types/appointment.json)

<a id="op-30981b6f508cdf"></a>
### Appointment.find party by contact email

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_find_party_by_contact_email`

**Inputs** self, doctype.

**Declared result** (str bitwise or no value).

**Record and data access** read “Contact Email” via get\_all · read “Dynamic Link” via get\_all.

**Explicit results** no value · party at 0 when party, otherwise no value.

**Local steps**

- Set contacts from Platform.get\_all(“Contact Email”, filters = mapping(“email\_id” → self.customer\_email, “parenttype” → “Contact”), pluck = “parent”).
- If not contacts.
  - Return no value.
- Set party from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → “Contact”, “parent” → tuple(“in”, contacts), “link\_doctype” → doctype), pluck = “link\_name”, limit = 1).
- Return party at 0 when party, otherwise no value.
  - Value choice on party — true gives party at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L469)

<a id="op-3d6eaaeefc1a16"></a>
### Appointment.create lead and link

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_create_lead_and_link`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Lead”, “lead\_name” → self.customer\_name, “email\_id” → self.customer\_email, “phone” → self.customer\_phone\_number) via get\_doc.

**State and service calls** call insert on lead.

**Explicit results** no value.

**Local steps**

- If self.party.
  - Return no value.
- Set lead from Platform.get\_doc(mapping(“doctype” → “Lead”, “lead\_name” → self.customer\_name, “email\_id” → self.customer\_email, “phone” → self.customer\_phone\_number)).
- If self.customer\_details.
  - Evaluate lead.append(“notes”, mapping(“note” → escape\_html(self.customer\_details), “added\_by” → Platform.session.user, “added\_on” → now())).
- Set self.party from lead.insert(ignore\_permissions = true).name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L3219) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1057)

<a id="op-da0e11706af80c"></a>
### Appointment.auto assign

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_auto_assign`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.\_assign.
  - Return no value.
- If agent bound to self.get\_free\_agent(get\_busy\_agents(self.scheduled\_time, exclude\_appointment = self.name)).
  - Evaluate self.assign\_agent(agent).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get free agent](operations-002.md#op-d21fea5a1190b4), [assign agent](operations-002.md#op-1394fe0f766eaf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1054)

<a id="op-d21fea5a1190b4"></a>
### Appointment.get free agent

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_get_free_agent`

**Inputs** self, busy\_agents.

**Declared result** (str bitwise or no value).

**Explicit results** existing\_assignee · next(generator of agent for agent drawn from agents where agent does not belong to busy\_agents, no value).

**Local steps**

- Set existing\_assignee from self.get\_assignee\_from\_latest\_opportunity().
- If (existing\_assignee and existing\_assignee does not belong to busy\_agents).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_assignee → existing\_assignee does not belong to busy\_agents.
  - Return existing\_assignee.
- Set agents from \_get\_agents\_sorted\_by\_asc\_workload(getdate(self.scheduled\_time)).
- Return next(generator of agent for agent drawn from agents where agent does not belong to busy\_agents, no value).
  - Draw agent from agents, keep a combination only if (agent does not belong to busy\_agents).

**Methods declared on this owner** [get assignee from latest opportunity](operations-002.md#op-bb87dfbdd8ea12).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L470)

<a id="op-bb87dfbdd8ea12"></a>
### Appointment.get assignee from latest opportunity

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_get_assignee_from_latest_opportunity`

**Inputs** self.

**Record and data access** read “Lead” via exists · read “Opportunity” via get\_all.

**Explicit results** no value · assignees at 0 when assignees, otherwise no value.

**Local steps**

- If (not self.party or not Platform.db.exists(“Lead”, self.party)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.party → not Platform.db.exists(“Lead”, self.party).
  - Return no value.
- Set opportunities from Platform.get\_all(“Opportunity”, filters = mapping(“party\_name” → self.party), fields = list(“\_assign”), order\_by = “creation desc”, limit = 1).
- Set assignees from (opportunities and Platform.parse\_json((opportunities at 0.\_assign or “&#91;&#93;”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in opportunities → Platform.parse\_json((opportunities at 0.\_assign or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in opportunities at 0.\_assign → “&#91;&#93;”.
- Return assignees at 0 when assignees, otherwise no value.
  - Value choice on assignees — true gives assignees at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L3795) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1060)

<a id="op-1394fe0f766eaf"></a>
### Appointment.assign agent

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_assign_agent`

**Inputs** self, agent.

**Local steps**

- If not Platform.has\_permission(doc = self, user = agent).
  - Evaluate add\_docshare(self.doctype, self.name, agent, flags = mapping(“ignore\_share\_permission” → true)).
- Evaluate add\_assignment(mapping(“doctype” → self.doctype, “name” → self.name, “assign\_to” → list(agent)), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doc = self, user = agent).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1053)

<a id="op-3e7e29622b3afe"></a>
### Appointment.create calendar event

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_create_calendar_event`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Event”, “subject” → formatted text Appointment with {self.customer\_name}, “starts\_on” → self.scheduled\_time, “status” → “Open”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Event”, “subject” → formatted text Appointment with {self.customer\_name}, “starts\_on” → self.scheduled\_time, “status” → “Open”, …)) · call save on self.

**Explicit results** no value.

**Local steps**

- If self.calendar\_event.
  - Return no value.
- Set event from Platform.get\_doc(mapping(“doctype” → “Event”, “subject” → formatted text Appointment with {self.customer\_name}, “starts\_on” → self.scheduled\_time, “status” → “Open”, …)).insert(ignore\_permissions = true).
- Set self.calendar\_event from event.name.
- Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get event participants](operations-002.md#op-f94af230e9a817).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1056)

<a id="op-f94af230e9a817"></a>
### Appointment.get event participants

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_get_event_participants`

**Inputs** self.

**Explicit results** participants.

**Local steps**

- Set participants from list(dict(reference\_doctype = self.appointment\_with, reference\_docname = self.party)).
- If employee bound to \_get\_employee\_from\_user(self.\_assign).
  - Evaluate participants.append(dict(reference\_doctype = “Employee”, reference\_docname = employee.name)).
- Return participants.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L4649) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1061)

<a id="op-9f8eb5063f60fc"></a>
### Appointment.get verify url

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_get_verify_resource_address`

**Inputs** self.

**Explicit results** get\_url((“/book\_appointment/verify?” + urlencode(mapping(“key” → key))), allow\_header\_override = false).

**Local steps**

- Set key from self.generate\_verification\_key().
- Return get\_url((“/book\_appointment/verify?” + urlencode(mapping(“key” → key))), allow\_header\_override = false).

**Methods declared on this owner** [generate verification key](operations-002.md#op-4c8a9b3dd06597).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1062)

<a id="op-4c8a9b3dd06597"></a>
### Appointment.generate verification key

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_generate_verification_key`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** key.

**Local steps**

- Set key from Platform.generate\_hash().
- Evaluate self.db\_set(“verification\_token”, sha256\_hash(key), update\_modified = false).
- Return key.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L4950) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1059)

<a id="op-43551f38da8c2a"></a>
### Get booking settings

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_booking_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Appointment Booking Settings” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Appointment Booking Settings”).

**Local steps**

- Return Platform.get\_cached\_doc(“Appointment Booking Settings”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Appointment Booking Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L5071) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1084)

<a id="op-ade1d56d27bc67"></a>
### Lock booking capacity

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_lock_booking_capacity`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Appointment Booking Settings” via get\_single\_value.

**Explicit results** cint(Platform.db.get\_single\_value(“Appointment Booking Settings”, “number\_of\_agents”, for\_update = true)).

**Local steps**

- Return cint(Platform.db.get\_single\_value(“Appointment Booking Settings”, “number\_of\_agents”, for\_update = true)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Appointment Booking Settings”, “number\_of\_agents”, for\_update = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L475)

<a id="op-ba2d5fc4c753d6"></a>
### Is appointment scheduling enabled

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_is_appointment_scheduling_enabled`

**Inputs** no declared parameters.

**Explicit results** bool(cint(get\_booking\_settings().enable\_scheduling)).

**Local steps**

- Return bool(cint(get\_booking\_settings().enable\_scheduling)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L5122) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1089)

<a id="op-7d486c6b2ae3d2"></a>
### Get verification link expiry

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_verification_link_expiry`

**Inputs** no declared parameters.

**Explicit results** cint(get\_booking\_settings().verification\_link\_expiry\_duration).

**Local steps**

- Return cint(get\_booking\_settings().verification\_link\_expiry\_duration).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L5192) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1087)

<a id="op-cb4ed75cf66bb5"></a>
### Count overlapping appointments

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_count_overlapping_appointments`

**Inputs** scheduled\_time, appointment\_duration, exclude\_appointment = no value, for\_update = false.

**Explicit results** len(query.run()).

**Local steps**

- Set appointment from Platform.qb.DocType(“Appointment”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.scheduled\_time &gt; nested operand in the contract(nested operand in the contract, minutes = nested operand  ….
- If exclude\_appointment.
  - Set query from query.where(appointment.name differs from exclude\_appointment).
- If for\_update.
  - Set query from query.for\_update().
- Return len(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1080)

<a id="op-9e131d0cc96c04"></a>
### Handle expired unverified appointments

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_handle_expired_unverified_appointments`

**Inputs** no declared parameters.

**Record and data access** read “Appointment” via get\_all.

**State and service calls** request set\_value on “Appointment” · request delete\_doc for “Appointment”.

**Explicit results** no value.

**Local steps**

- Set expiry from get\_verification\_link\_expiry().
- If not expiry.
  - Return no value.
- Set cutoff from add\_to\_date(now\_datetime(), minutes = negative expiry).
- Set filters from mapping(“status” → “Unverified”, “creation” → tuple(“&lt;”, cutoff)).
- Set action from (get\_booking\_settings().action\_for\_expired\_unverified\_appointments or “Mark as Closed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_booking\_settings().action\_for\_expired\_unverified\_appointments → “Mark as Closed”.
- If action equals “Mark as Closed”.
  - Evaluate Platform.db.set\_value(“Appointment”, filters, “status”, “Closed”).
- Otherwise.
  - If action equals “Delete Permanently”.
    - For each name in Platform.get\_all(“Appointment”, filters = filters, pluck = “name”).
      - Evaluate Platform.delete\_doc(“Appointment”, name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L5663) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1088)

<a id="op-b8aab9808682c5"></a>
### Get agents sorted by asc workload

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_agents_sorted_by_ascending_workload`

**Inputs** date.

**Record and data access** read “Appointment” via get\_all.

**Explicit results** list of agent for tuple(agent, \_workload) drawn from reversed(workload.most\_common()).

**Local steps**

- Set workload from Counter(generator of agent.user for agent drawn from get\_booking\_settings().agent\_list).
  - Draw agent from get\_booking\_settings().agent\_list.
- Set assigns from Platform.get\_all(“Appointment”, filters = list(list(“\_assign”, “is”, “set”), list(“scheduled\_time”, “&gt;=”, getdate(date)), list(“scheduled\_time”, “&lt;”, add\_to\_date(getdate(date), days = 1))), pluck = “\_assign”).
- For each assign in assigns.
  - Set assignees from Platform.parse\_json(((assign or empty text).strip() or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (assign or empty text).strip() → “&#91;&#93;”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in assign → empty text.
  - If (assignees and assignees at 0 belongs to workload).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in assignees → assignees at 0 belongs to workload.
    - Update workload at assignees at 0 using + 1.
- Return list of agent for tuple(agent, \_workload) drawn from reversed(workload.most\_common()).
  - Draw tuple(agent, \_workload) from reversed(workload.most\_common()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L6069) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1081)

<a id="op-c8fd0c8bfd8c57"></a>
### Get busy agents

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_busy_agents`

**Inputs** scheduled\_time, exclude\_appointment = no value.

**Declared result** set at str.

**Record and data access** read “Appointment” via get\_all.

**Explicit results** set of assignee for assign drawn from assigns, then assignee drawn from Platform.parse\_json((assign or “&#91;&#93;”)).

**Local steps**

- Set duration from \_get\_appointment\_duration().
- Set assigns from Platform.get\_all(“Appointment”, filters = list(list(“scheduled\_time”, “&gt;”, add\_to\_date(scheduled\_time, minutes = negative duration)), list(“scheduled\_time”, “&lt;”, add\_to\_date(scheduled\_time, minutes = durat ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in exclude\_appointment → empty text.
- Return set of assignee for assign drawn from assigns, then assignee drawn from Platform.parse\_json((assign or “&#91;&#93;”)).
  - Draw assign from assigns.
  - Draw assignee from Platform.parse\_json((assign or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in assign → “&#91;&#93;”.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1085)

<a id="op-b2c109d67f8222"></a>
### Check agent availability

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_check_agent_availability`

**Inputs** agent\_email, scheduled\_time.

**Explicit results** agent\_email does not belong to get\_busy\_agents(scheduled\_time).

**Local steps**

- Return agent\_email does not belong to get\_busy\_agents(scheduled\_time).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L6810) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1079)

<a id="op-4f697e89bb652d"></a>
### Get booked slot times

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_booked_slot_times`

**Inputs** from\_time, to\_time.

**Record and data access** read “Appointment” via get\_all.

**Explicit results** Platform.get\_all(“Appointment”, filters = list(list(“scheduled\_time”, “&gt;”, from\_time), list(“scheduled\_time”, “&lt;”, to\_time), list(“status”, “not in”, list(“Closed”, “Unverified”))), pluck = “scheduled\_time”).

**Local steps**

- Return Platform.get\_all(“Appointment”, filters = list(list(“scheduled\_time”, “&gt;”, from\_time), list(“scheduled\_time”, “&lt;”, to\_time), list(“status”, “not in”, list(“Closed”, “Unverified”))), pluck = “scheduled\_time”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1083)

<a id="op-135e5bb0dbf4a4"></a>
### Get appointment duration

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_appointment_duration`

**Inputs** no declared parameters.

**Explicit results** cint(get\_booking\_settings().appointment\_duration).

**Local steps**

- Return cint(get\_booking\_settings().appointment\_duration).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0426.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1082)

<a id="op-4f2495daff5824"></a>
### Get employee from user

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_get_employee_from_user`

**Inputs** user.

**Record and data access** read “Employee” via get\_value · resolve a document from “Employee” via get\_doc.

**Explicit results** Platform.get\_doc(“Employee”, employee\_docname) when employee\_docname, otherwise no value.

**Local steps**

- Set employee\_docname from Platform.db.get\_value(“Employee”, mapping(“user\_id” → user)).
- Return Platform.get\_doc(“Employee”, employee\_docname) when employee\_docname, otherwise no value.
  - Value choice on employee\_docname — true gives Platform.get\_doc(“Employee”, employee\_docname), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0426.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1086)

## Record · Appointment booking settings

[Record definition](../../../../data/record-types/appointment_booking_settings.json)

<a id="op-52bc90f84ff7a2"></a>
### Appointment Booking Settings.validate

`operation_enterprise_customer_relationship_management_record_definitions_appointment_booking_settings_business_behavior_appointment_booking_settings_validate`

**Inputs** self.

**Local steps**

- Set self.number\_of\_agents from len(self.agent\_list).
- Evaluate self.validate\_appointment\_duration().
- Evaluate self.validate\_appointment\_scheduling().
- Evaluate self.validate\_portal\_booking().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate appointment duration](operations-002.md#op-6bd7a699f706c8), [validate appointment scheduling](operations-003.md#op-0f932cdadd69b9), [validate portal booking](operations-003.md#op-aa95ef1494ba5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1031)

<a id="op-6bd7a699f706c8"></a>
### Appointment Booking Settings.validate appointment duration

`operation_enterprise_binding_enterprise_crm_doctype_appointment_booking_settings_appointment_booking_settings_appointmentbookingsettings_validate_appointment_duration`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Appointment Duration must be greater than 0 minutes.”.

**Local steps**

- If cint(self.appointment\_duration) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Appointment Duration must be greater than 0 minutes.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L476)
