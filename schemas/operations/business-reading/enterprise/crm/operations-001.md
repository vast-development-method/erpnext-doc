# Sales relationships · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appointment

[Record definition](../../../../data/record-types/appointment.json)

<a id="op-d52f5fdb296f75"></a>
### Appointment.check if latest

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_check_if_latest`

**Inputs** self.

**Local steps**

- Evaluate lock\_booking\_capacity().
- Evaluate super().check\_if\_latest().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L468)

<a id="op-4ad104f4ed9796"></a>
### Appointment.validate

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_appointment\_with().
- Evaluate self.validate\_status\_update().
- If self.has\_value\_changed(“scheduled\_time”).
  - Evaluate self.validate\_schedule().
- If (self.has\_value\_changed(“scheduled\_time”) or (self.status equals “Open” and self.has\_value\_changed(“status”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“scheduled\_time”) → (self.status equals “Open” and self.has\_value\_changed(“status”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Open” → self.has\_value\_changed(“status”).
  - Evaluate self.validate\_available\_time\_slot().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate appointment with](operations-001.md#op-475aa8ce636c06), [validate status update](operations-001.md#op-09f4d44a038b50), [validate schedule](operations-001.md#op-1c323122518f32), [validate available time slot](operations-001.md#op-1903a4f45d8366).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1072)

<a id="op-1c323122518f32"></a>
### Appointment.validate schedule

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_validate_schedule`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_backdated\_booking().
- If is\_appointment\_scheduling\_enabled().
  - Evaluate self.validate\_advanced\_booking().
  - Evaluate self.validate\_holiday().
  - Evaluate self.validate\_slot\_timing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate backdated booking](operations-001.md#op-c0474dc22b5578), [validate advanced booking](operations-001.md#op-2a015f5aecdfcf), [validate holiday](operations-001.md#op-1af143f968221a), [validate slot timing](operations-001.md#op-b4410dfdfbaae2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L474)

<a id="op-475aa8ce636c06"></a>
### Appointment.validate appointment with

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_validate_appointment_with`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Appointment With must be a Customer or a Lead”.

**Local steps**

- If (self.appointment\_with and self.appointment\_with does not belong to tuple(“Customer”, “Lead”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.appointment\_with → self.appointment\_with does not belong to tuple(“Customer”, “Lead”).
  - Call the validation error handler Platform.throw(translated “Appointment With must be a Customer or a Lead”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L472)

<a id="op-09f4d44a038b50"></a>
### Appointment.validate status update

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_status_update`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Appointments created manually cannot have 'Unverified' status.” · validation helper — translated “A verified appointment cannot be moved back to 'Unverified' status.” · validation helper — translated “An appointment booked through the portal can only be opened via email verification.”.

**Local steps**

- If not self.has\_value\_changed(“status”).
  - Return no value.
- If not self.created\_through\_portal.
  - <a id="op-09f4d44a038b50-guard-6"></a>If self.status equals “Unverified”.
    - Call the validation error handler Platform.throw(translated “Appointments created manually cannot have 'Unverified' status.”).
  - Return no value.
- If (self.status equals “Unverified” and self.email\_verified).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Unverified” → self.email\_verified.
  - Call the validation error handler Platform.throw(translated “A verified appointment cannot be moved back to 'Unverified' status.”).
- If (self.status equals “Open” and not self.email\_verified).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Open” → not self.email\_verified.
  - Call the validation error handler Platform.throw(translated “An appointment booked through the portal can only be opened via email verification.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Unverified”, self.status = “Unverified” selects the branch that calls the validation-error handler with translated “Appointments created manually cannot have 'Unverified' status.”. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-09f4d44a038b50-guard-6)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L6708) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1078)

<a id="op-c0474dc22b5578"></a>
### Appointment.validate backdated booking

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_backdated_booking`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Appointment cannot be scheduled for a past time.”.

**Local steps**

- If get\_datetime(self.scheduled\_time) &lt; now\_datetime().
  - Call the validation error handler Platform.throw(translated “Appointment cannot be scheduled for a past time.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0424.json#L7028) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1075)

<a id="op-2a015f5aecdfcf"></a>
### Appointment.validate advanced booking

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_advanced_booking`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Appointment can only be scheduled up to {0} day(s) in advance.”.format(advance\_booking\_days).

**Local steps**

- Set advance\_booking\_days from cint(get\_booking\_settings().advance\_booking\_days).
- If (advance\_booking\_days and date\_diff(self.scheduled\_time, now\_datetime()) &gt; advance\_booking\_days).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in advance\_booking\_days → date\_diff(self.scheduled\_time, now\_datetime()) &gt; advance\_booking\_days.
  - Call the validation error handler Platform.throw(translated “Appointment can only be scheduled up to {0} day(s) in advance.”.format(advance\_booking\_days)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1073)

<a id="op-1af143f968221a"></a>
### Appointment.validate holiday

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_holiday`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please add a valid Holiday List on Appointment Booking Settings.” · validation helper — translated “Appointment cannot be scheduled on a holiday.”.

**Local steps**

- Set holiday\_list from get\_booking\_settings().holiday\_list.
- If not holiday\_list.
  - Call the validation error handler Platform.throw(translated “Please add a valid Holiday List on Appointment Booking Settings.”).
- If is\_holiday(holiday\_list, getdate(self.scheduled\_time)).
  - Call the validation error handler Platform.throw(translated “Appointment cannot be scheduled on a holiday.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1076)

<a id="op-b4410dfdfbaae2"></a>
### Appointment.validate slot timing

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_slot_timing`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No availability of slots are found. Please add on Appointment Booking Settings.” · validation helper — translated “Appointment must be scheduled within the available slot timings.”.

**Local steps**

- Set settings from get\_booking\_settings().
- If not settings.availability\_of\_slots.
  - Call the validation error handler Platform.throw(translated “No availability of slots are found. Please add on Appointment Booking Settings.”).
- Set scheduled\_time from get\_datetime(self.scheduled\_time).
- Set day\_of\_week from WEEKDAYS at scheduled\_time.weekday().
- Set slot\_start from timedelta(hours = scheduled\_time.hour, minutes = scheduled\_time.minute, seconds = scheduled\_time.second).
- Set slot\_end from (slot\_start + timedelta(minutes = cint(settings.appointment\_duration))).
- Set containing\_slots from list of slot for slot drawn from settings.availability\_of\_slots where (slot.day\_of\_week equals day\_of\_week and slot.from\_time ≤ slot\_start and slot\_end ≤ slot.to\_time).
  - Draw slot from settings.availability\_of\_slots, keep a combination only if ((slot.day\_of\_week equals day\_of\_week and slot.from\_time ≤ slot\_start and slot\_end ≤ slot.to\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in slot.day\_of\_week equals day\_of\_week → slot.from\_time ≤ slot\_start → slot\_end ≤ slot.to\_time.
- If not containing\_slots.
  - Call the validation error handler Platform.throw(translated “Appointment must be scheduled within the available slot timings.”).
- Evaluate self.validate\_on\_slot\_grid(list of (slot\_start − slot.from\_time) for slot drawn from containing\_slots, (slot\_end − slot\_start)).
  - Draw slot from containing\_slots.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate on slot grid](operations-001.md#op-482cdd226ea490).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1077)

<a id="op-482cdd226ea490"></a>
### Appointment.validate on slot grid

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_validate_on_slot_grid`

**Inputs** self, offsets, duration.

**Explicit failure paths** validation helper — translated “Appointment must start at the beginning of an available slot.”.

**Local steps**

- If (self.created\_through\_portal and duration and all(generator of (offset modulo or format duration) for offset drawn from offsets)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.created\_through\_portal → duration → all(generator of (offset modulo or format duration) for offset drawn from offsets).
  - Draw offset from offsets.
  - Call the validation error handler Platform.throw(translated “Appointment must start at the beginning of an available slot.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L473)

<a id="op-1903a4f45d8366"></a>
### Appointment.validate available time slot

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_validate_available_time_slot`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Time slot is not available”.

**Local steps**

- Set number\_of\_agents from lock\_booking\_capacity().
- If not number\_of\_agents.
  - Return no value.
- Set booked from count\_overlapping\_appointments(self.scheduled\_time, cint(get\_booking\_settings().appointment\_duration), exclude\_appointment = self.name, for\_update = true).
- If booked ≥ number\_of\_agents.
  - Call the validation error handler Platform.throw(translated “Time slot is not available”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1074)

<a id="op-0a03d98d07d826"></a>
### Appointment.before insert

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_before_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.created\_through\_portal.
  - Set self.status from “Unverified”.
  - Return no value.
- Evaluate self.link\_customer\_lead().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link customer lead](operations-001.md#op-5dc894a6a32357).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1059) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1055)

<a id="op-009d30ef9dd46c"></a>
### Appointment.after insert

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_after_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.created\_through\_portal and self.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.created\_through\_portal → self.party.
  - Evaluate self.auto\_assign().
  - Evaluate self.create\_calendar\_event().
  - Return no value.
- Evaluate self.send\_confirmation\_email().

If control reaches the end, it returns no value.

**Methods declared on this owner** [auto assign](operations-002.md#op-da0e11706af80c), [create calendar event](operations-002.md#op-3e7e29622b3afe), [send confirmation email](operations-001.md#op-db1f8bf7d9e904).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1147) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1052)

<a id="op-d559e5cdd6a70e"></a>
### Appointment.on update

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_on_update`

**Inputs** self.

**Local steps**

- Set status\_changed from self.has\_value\_changed(“status”).
- Set email\_just\_verified from (bool((self.created\_through\_portal and self.email\_verified)) and self.has\_value\_changed(“email\_verified”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool((self.created\_through\_portal and self.email\_verified)) → self.has\_value\_changed(“email\_verified”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.created\_through\_portal → self.email\_verified.
- Evaluate self.link\_auto\_assign\_and\_create\_calendar\_event().
- If email\_just\_verified.
  - Evaluate self.send\_appointment\_confirmed\_email().
- If status\_changed.
  - Evaluate self.update\_event\_and\_assignments\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link auto assign and create calendar event](operations-001.md#op-87572406b3036a), [send appointment confirmed email](operations-001.md#op-7235b0a958fb31), [update event and assignments status](operations-001.md#op-9d0531e21e12f8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1276) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1066)

<a id="op-5301578cbca122"></a>
### Appointment.on trash

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_on_trash`

**Inputs** self.

**State and service calls** call db\_set on self · request delete\_doc for “Event”.

**Explicit results** no value.

**Local steps**

- If not self.calendar\_event.
  - Return no value.
- Set event from self.calendar\_event.
- Evaluate self.db\_set(“calendar\_event”, no value, update\_modified = false).
- Evaluate Platform.delete\_doc(“Event”, event, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1495) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1065)

<a id="op-db1f8bf7d9e904"></a>
### Appointment.send confirmation email

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_send_confirmation_email`

**Inputs** self.

**State and service calls** msgprint with translated “Please check your email to confirm the appointment.”.

**Local steps**

- Evaluate self.send\_email\_to\_customer(template = “confirm\_appointment”, subject = translated “Appointment Confirmation”, args = mapping(“link” → self.\_get\_verify\_url(), “expiry\_minutes” → get\_verification\_link\_expiry())).
- Evaluate Platform.msgprint(translated “Please check your email to confirm the appointment.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [send email to customer](operations-001.md#op-fdcaec07df32ea), [get verify url](operations-002.md#op-9f8eb5063f60fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1654) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1068)

<a id="op-7235b0a958fb31"></a>
### Appointment.send appointment confirmed email

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_send_appointment_confirmed_email`

**Inputs** self.

**Local steps**

- Evaluate self.send\_email\_to\_customer(template = “appointment\_confirmed”, subject = translated “Appointment Confirmed”, args = mapping(“scheduled\_time” → Platform.utils.format\_datetime(self.scheduled\_time)), referen ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [send email to customer](operations-001.md#op-fdcaec07df32ea).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L1838) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1067)

<a id="op-fdcaec07df32ea"></a>
### Appointment.send email to customer

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_send_email_to_customer`

**Inputs** self, template, subject, args, remaining named values kwargs.

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.sendmail(recipients = list(self.customer\_email), template = template, args = mapping(“full\_name” → self.customer\_name, “site\_url” → get\_url(allow\_header\_override = false), expand args), subject =  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = list(self.customer\_email), template = template, args = mapping(“full\_name” → self.customer\_name, “site\_url” → get\_url(allow\_header\_override = false), expand args), subject =  ….

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1069)

<a id="op-87572406b3036a"></a>
### Appointment.link auto assign and create calendar event

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_link_auto_assign_and_create_calendar_event`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or (self.created\_through\_portal and not self.email\_verified)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → (self.created\_through\_portal and not self.email\_verified).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.created\_through\_portal → not self.email\_verified.
  - Return no value.
- If not self.calendar\_event.
  - Evaluate self.link\_customer\_lead().
  - Evaluate self.auto\_assign().
  - Evaluate self.create\_calendar\_event().
- Evaluate self.sync\_calendar\_event().
- Evaluate self.reassign\_if\_agent\_busy().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link customer lead](operations-001.md#op-5dc894a6a32357), [auto assign](operations-002.md#op-da0e11706af80c), [create calendar event](operations-002.md#op-3e7e29622b3afe), [sync calendar event](operations-001.md#op-b03cc173786145), [reassign if agent busy](operations-001.md#op-a5ea34253cb707).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1063)

<a id="op-a5ea34253cb707"></a>
### Appointment.reassign if agent busy

`operation_enterprise_binding_enterprise_crm_doctype_appointment_appointment_appointment_reassign_if_agent_busy`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.\_assign and self.has\_value\_changed(“scheduled\_time”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_assign → self.has\_value\_changed(“scheduled\_time”).
  - Return no value.
- Set busy\_agents from get\_busy\_agents(self.scheduled\_time, exclude\_appointment = self.name).
- Set current\_agents from Platform.parse\_json(self.\_assign).
- If not busy\_agents.intersection(current\_agents).
  - Return no value.
- If agent bound to self.get\_free\_agent(busy\_agents).
  - Evaluate clear\_assignments(self.doctype, self.name, ignore\_permissions = true).
  - Evaluate self.assign\_agent(agent).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get free agent](operations-002.md#op-d21fea5a1190b4), [assign agent](operations-002.md#op-1394fe0f766eaf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L471)

<a id="op-b03cc173786145"></a>
### Appointment.sync calendar event

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_sync_calendar_event`

**Inputs** self.

**Record and data access** resolve a document from “Event” via get\_doc.

**State and service calls** call save on cal\_event.

**Explicit results** no value.

**Local steps**

- If (not self.calendar\_event or not self.has\_value\_changed(“scheduled\_time”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.calendar\_event → not self.has\_value\_changed(“scheduled\_time”).
  - Return no value.
- Set cal\_event from Platform.get\_doc(“Event”, self.calendar\_event).
- Set cal\_event.starts\_on from self.scheduled\_time.
- Evaluate cal\_event.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L2384) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1070)

<a id="op-9d0531e21e12f8"></a>
### Appointment.update event and assignments status

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_update_event_and_assignments_status`

**Inputs** self.

**State and service calls** request set\_value on “Event” · request set\_value on “ToDo”.

**Explicit results** no value.

**Local steps**

- <a id="op-9d0531e21e12f8-guard-3"></a>If self.status equals “Unverified”.
  - Return no value.
- Set is\_closed from self.status equals “Closed”.
- Set new\_status from “Closed” when is\_closed, otherwise “Open”.
  - Value choice on is\_closed — true gives “Closed”, false gives “Open”.
- If self.calendar\_event.
  - Evaluate Platform.db.set\_value(“Event”, self.calendar\_event, “status”, new\_status).
- Set todo\_filters from mapping(“reference\_type” → “Appointment”, “reference\_name” → self.name, “status” → “Open” when is\_closed, otherwise “Closed”).
  - Value choice on is\_closed — true gives “Open”, false gives “Closed”.
- Evaluate Platform.db.set\_value(“ToDo”, todo\_filters, “status”, new\_status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Unverified”, self.status = “Unverified” selects the branch that returns no value. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9d0531e21e12f8-guard-3)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L2565) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1071)

<a id="op-5dc894a6a32357"></a>
### Appointment.link customer lead

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_link_customer_lead`

**Inputs** self.

**Local steps**

- If not self.party.
  - Set customer from self.find\_party\_by\_email(“Customer”).
  - Set self.appointment\_with from “Customer” when customer, otherwise “Lead”.
    - Value choice on customer — true gives “Customer”, false gives “Lead”.
  - Set self.party from (customer or self.find\_party\_by\_email(“Lead”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer → self.find\_party\_by\_email(“Lead”).
- Evaluate self.create\_lead\_and\_link().

If control reaches the end, it returns no value.

**Methods declared on this owner** [find party by email](operations-001.md#op-45c764546529b4), [create lead and link](operations-002.md#op-3d6eaaeefc1a16).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0425.json#L2880) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1064)

<a id="op-45c764546529b4"></a>
### Appointment.find party by email

`operation_enterprise_customer_relationship_management_record_definitions_appointment_business_behavior_appointment_find_party_by_email`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_all.

**Explicit results** party at 0 when party, otherwise self.find\_party\_by\_contact\_email(doctype).

**Local steps**

- Set party from Platform.get\_all(doctype, filters = mapping(“email\_id” → self.customer\_email), limit = 1, pluck = “name”).
- Return party at 0 when party, otherwise self.find\_party\_by\_contact\_email(doctype).
  - Value choice on party — true gives party at 0, false gives self.find\_party\_by\_contact\_email(doctype).

**Methods declared on this owner** [find party by contact email](operations-002.md#op-30981b6f508cdf).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1058)
