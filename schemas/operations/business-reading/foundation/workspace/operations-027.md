# Forms, reports and navigation · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document follow

<a id="op-460ddf8345e1a8"></a>
### Get added row

`operation_foundation_desk_form_document_follow_business_behavior_get_added_row`

**Inputs** added, time, doctype, doc\_name, v, user.

**Explicit results** list of mapping(“time” → v.modified, “data” → mapping(“to” → d at 0, “time” → time), “doctype” → doctype, “doc\_name” → doc\_name, …) for d drawn from added where \_can\_read\_table\_field(doctype, d at 0, user).

**Local steps**

- Return list of mapping(“time” → v.modified, “data” → mapping(“to” → d at 0, “time” → time), “doctype” → doctype, “doc\_name” → doc\_name, …) for d drawn from added where \_can\_read\_table\_field(doctype, d at 0, user).
  - Draw d from added, keep a combination only if (\_can\_read\_table\_field(doctype, d at 0, user)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L662) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L167)

<a id="op-8f4c9b1a2fa12d"></a>
### Get field changed

`operation_foundation_desk_form_document_follow_business_behavior_get_field_changed`

**Inputs** changed, time, doctype, doc\_name, v, user.

**Explicit results** items.

**Local steps**

- Bind dependencies html2text.
- Set items from list().
- Set permitted\_fieldnames from Platform.get\_meta(doctype).get\_permitted\_fieldnames(permission\_type = “read”, user = user).
- For each d in changed.
  - If d at 0 does not belong to permitted\_fieldnames.
    - Continue with the next iteration or loop test.
  - Set d at 1 from d at 1 when d at 1, otherwise one space.
    - Value choice on d at 1 — true gives d at 1, false gives one space.
  - Set d at 2 from d at 2 when d at 2, otherwise one space.
    - Value choice on d at 2 — true gives d at 2, false gives one space.
  - Set d at 0 from d at 0 when d at 0, otherwise one space.
    - Value choice on d at 0 — true gives d at 0, false gives one space.
  - Evaluate items.append(mapping(“time” → v.modified, “data” → mapping(“time” → time, “field” → d at 0, “from” → html2text(str(d at 1)), “to” → html2text(str(d at 2))), “doctype” → doctype, “doc\_name” → doc\_name, …)).
- Return items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L924) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L170)

<a id="op-5a27a80cac2377"></a>
### Send hourly updates

`operation_foundation_desk_form_document_follow_business_behavior_send_hourly_updates`

**Inputs** no declared parameters.

**Local steps**

- Evaluate send\_document\_follow\_mails(“Hourly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L1518) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L181)

<a id="op-4a62ea1b3f8cc9"></a>
### Send daily updates

`operation_foundation_desk_form_document_follow_business_behavior_send_daily_updates`

**Inputs** no declared parameters.

**Local steps**

- Evaluate send\_document\_follow\_mails(“Daily”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L1562) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L178)

<a id="op-a9c6c48c598584"></a>
### Send weekly updates

`operation_foundation_desk_form_document_follow_business_behavior_send_weekly_updates`

**Inputs** no declared parameters.

**Local steps**

- Evaluate send\_document\_follow\_mails(“Weekly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L1606) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L182)

<a id="op-c6ac4bf938c76c"></a>
### Get filters

`operation_foundation_desk_form_document_follow_business_behavior_get_filters`

**Inputs** frequency, user.

**Explicit results** filters.

**Local steps**

- Set filters from list(list(“modified\_by”, “!=”, user)).
- If frequency equals “Weekly”.
  - Update filters using + list(list(“modified”, “&gt;”, Platform.utils.add\_days(Platform.utils.nowdate(), negative 7)), list(“modified”, “&lt;”, Platform.utils.nowdate())).
- Otherwise.
  - If frequency equals “Daily”.
    - Update filters using + list(list(“modified”, “&gt;”, Platform.utils.add\_days(Platform.utils.nowdate(), negative 1)), list(“modified”, “&lt;”, Platform.utils.nowdate())).
  - Otherwise.
    - If frequency equals “Hourly”.
      - Update filters using + list(list(“modified”, “&gt;”, Platform.utils.add\_to\_date(Platform.utils.now\_datetime(), hours = negative 1)), list(“modified”, “&lt;”, Platform.utils.now\_datetime())).
- Return filters.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate(), Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L1650) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L171)

<a id="op-cc3e7178869370"></a>
### Can read child table field

`operation_foundation_desk_form_document_follow_business_behavior_can_read_child_table_field`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, table\_field, child\_field, user.

**Explicit result forms** Boolean false, a comparison result.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L2145) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L163)

<a id="op-86a05a52bdabdc"></a>
### Can read table field

`operation_foundation_desk_form_document_follow_business_behavior_can_read_table_field`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, table\_field, user.

**Explicit result forms** Boolean false, a comparison result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L2411) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L164)

## Service · Error

<a id="op-341dce90369767"></a>
### Get context

`operation_foundation_public_pages_error_business_behavior_get_context`

**Inputs** context.

**Explicit results** no value · mapping(“error” → nested operand in the contract().replace(“&lt;”, “&amp;lt;”).replace(“&gt;”, “&amp;gt;”) when is\_traceback\_allowed(), otherwise empty text).

**Local steps**

- If Platform.flags.in\_migrate.
  - Return no value.
- If not context.title.
  - Set context.title from translated “Server Error”.
- If not context.message.
  - Set context.message from translated “There was an error building this page”.
- Return mapping(“error” → nested operand in the contract().replace(“&lt;”, “&amp;lt;”).replace(“&gt;”, “&amp;gt;”) when is\_traceback\_allowed(), otherwise empty text).
  - Value choice on is\_traceback\_allowed() — true gives Platform.get\_traceback().replace(“&lt;”, “&amp;lt;”).replace(“&gt;”, “&amp;gt;”), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L5462) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L34)

## Record · Event

[Record definition](../../../../data/record-types/event.json)

<a id="op-3a415741bc780e"></a>
### Event.validate

`operation_foundation_desk_record_definitions_event_business_behavior_event_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Daily Events should finish on the Same Day.” · validation helper — translated “Select Google Calendar to which event should be synced.”.

**Local steps**

- If not self.starts\_on.
  - Set self.starts\_on from now\_datetime().
- Set self.ends\_on from no value when self.starts\_on equals self.ends\_on, otherwise self.ends\_on.
  - Value choice on self.starts\_on equals self.ends\_on — true gives no value, false gives self.ends\_on.
- If (self.starts\_on and self.ends\_on).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.starts\_on → self.ends\_on.
  - Evaluate self.validate\_from\_to\_dates(“starts\_on”, “ends\_on”).
- If (self.repeat\_on equals “Daily” and self.ends\_on and getdate(self.starts\_on) differs from getdate(self.ends\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repeat\_on equals “Daily” → self.ends\_on → getdate(self.starts\_on) differs from getdate(self.ends\_on).
  - Call the validation error handler Platform.throw(translated “Daily Events should finish on the Same Day.”).
- If (self.sync\_with\_google\_calendar and not self.google\_calendar).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sync\_with\_google\_calendar → not self.google\_calendar.
  - Call the validation error handler Platform.throw(translated “Select Google Calendar to which event should be synced.”).
- If not self.sync\_with\_google\_calendar.
  - Set self.add\_video\_conferencing from 0.
- If (self.google\_meet\_link and not self.google\_meet\_link.startswith(text in the contract)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.google\_meet\_link → not self.google\_meet\_link.startswith(text in the contract).
  - Set self.google\_meet\_link from empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L3629) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L749)

<a id="op-26db480d275f4d"></a>
### Event.before save

`operation_foundation_desk_record_definitions_event_business_behavior_event_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_participants\_email().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set participants email](operations-027.md#op-69f9041088de3b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L4116) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L741)

<a id="op-8e5a21165ee16f"></a>
### Event.on update

`operation_foundation_desk_record_definitions_event_business_behavior_event_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.sync\_communication().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync communication](operations-027.md#op-e888cdb9936fa6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L4167) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L744)

<a id="op-1faf5f2102d3c5"></a>
### Event.on trash

`operation_foundation_desk_record_definitions_event_business_behavior_event_on_trash`

**Inputs** self.

**Record and data access** read “Communication” via get\_all.

**State and service calls** request delete\_doc for “Communication”.

**Local steps**

- Set communications from Platform.get\_all(“Communication”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name), pluck = “name”).
- For each communication in communications.
  - Evaluate Platform.delete\_doc(“Communication”, communication, force = true).
- Evaluate self.remove\_event\_from\_user\_settings().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove event from user settings](operations-027.md#op-2b00b8cbce322e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L4218) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L743)

<a id="op-e888cdb9936fa6"></a>
### Event.sync communication

`operation_foundation_desk_record_definitions_event_business_behavior_event_sync_communication`

**Inputs** self.

**Record and data access** read “Communication” via get\_all · resolve a document from “Communication” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.event\_participants.
  - Return no value.
- For each participant in self.event\_participants.
  - If communications bound to Platform.get\_all(“Communication”, filters = list(list(“Communication”, “reference\_doctype”, “=”, self.doctype), list(“Communication”, “reference\_name”, “=”, self.name), list(“Communication Link”, “link\_doc ….
    - For each comm in communications.
      - Set communication from Platform.get\_doc(“Communication”, comm).
      - Evaluate self.update\_communication(participant, communication).
  - Otherwise.
    - Set meta from Platform.get\_meta(participant.reference\_doctype).
    - If (hasattr(meta, “allow\_events\_in\_timeline”) and meta.allow\_events\_in\_timeline equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(meta, “allow\_events\_in\_timeline”) → meta.allow\_events\_in\_timeline equals 1.
      - Evaluate self.create\_communication(participant).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update communication](operations-027.md#op-255e3f588b14e6), [create communication](operations-027.md#op-2118bdf8cd4e7f).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L133) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L747)

<a id="op-2118bdf8cd4e7f"></a>
### Event.create communication

`operation_foundation_desk_record_definitions_event_business_behavior_event_create_communication`

**Inputs** self, participant.

**State and service calls** request new\_doc for “Communication”.

**Local steps**

- Set communication from Platform.new\_doc(“Communication”).
- Evaluate self.update\_communication(participant, communication).
- Set self.communication from communication.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [update communication](operations-027.md#op-255e3f588b14e6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L4863) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L742)

<a id="op-255e3f588b14e6"></a>
### Event.update communication

`operation_foundation_desk_record_definitions_event_business_behavior_event_update_communication`

**Inputs** self, participant, communication.

**State and service calls** call save on communication.

**Local steps**

- Set communication.communication\_medium from “Event”.
- Set communication.subject from self.subject.
- Set communication.content from self.description when self.description, otherwise self.subject.
  - Value choice on self.description — true gives self.description, false gives self.subject.
- Set communication.communication\_date from self.starts\_on.
- Set communication.sender from self.owner.
- Set communication.sender\_full\_name from get\_fullname(self.owner).
- Set communication.reference\_doctype from self.doctype.
- Set communication.reference\_name from self.name.
- Set communication.communication\_medium from communication\_mapping.get(self.event\_category) when self.event\_category, otherwise empty text.
  - Value choice on self.event\_category — true gives communication\_mapping.get(self.event\_category), false gives empty text.
- Set communication.status from “Linked”.
- Evaluate communication.add\_link(participant.reference\_doctype, participant.reference\_docname).
- Evaluate communication.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L4996) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L748)

<a id="op-61dda6bc9af439"></a>
### Event.add participant

`operation_foundation_desk_record_definitions_event_business_behavior_event_add_participant`

**Inputs** self, doctype, docname.

**Local steps**

- Evaluate self.append(“event\_participants”, mapping(“reference\_doctype” → doctype, “reference\_docname” → docname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L5394) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L739)

<a id="op-0b44779ec0d879"></a>
### Event.add participants

`operation_foundation_desk_record_definitions_event_business_behavior_event_add_participants`

**Inputs** self, participants.

**Local steps**

- For each participant in participants.
  - Evaluate self.add\_participant(participant at “doctype”, participant at “docname”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add participant](operations-027.md#op-61dda6bc9af439).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L5504) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L740)

<a id="op-69f9041088de3b"></a>
### Event.set participants email

`operation_foundation_desk_record_definitions_event_business_behavior_event_set_participants_email`

**Inputs** self.

**Record and data access** read “Contact” via get\_value.

**Local steps**

- For each participant in self.event\_participants.
  - If participant.email.
    - Continue with the next iteration or loop test.
  - If participant.reference\_doctype differs from “Contact”.
    - Set participant\_contact from get\_default\_contact(participant.reference\_doctype, participant.reference\_docname).
  - Otherwise.
    - Set participant\_contact from participant.reference\_docname.
  - Set participant.email from Platform.get\_value(“Contact”, participant\_contact, “email\_id”) when participant\_contact, otherwise no value.
    - Value choice on participant\_contact — true gives Platform.get\_value(“Contact”, participant\_contact, “email\_id”), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L5610) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L746)

<a id="op-2b00b8cbce322e"></a>
### Event.remove event from user settings

`operation_foundation_desk_record_definitions_event_business_behavior_event_remove_event_from_user_settings`

**Inputs** self.

**Local steps**

- Set user\_settings from get\_user\_settings(“Event”, for\_update = true).
- If user\_settings.
  - Set user\_settings from json.loads(user\_settings).
  - If “notifications” belongs to user\_settings.
    - Set notifications from user\_settings.get(“notifications”).
    - Set completedEvents from notifications.get(“completedEvents”, list()).
    - If self.name belongs to completedEvents.
      - Evaluate completedEvents.remove(self.name).
      - Set notifications at “completedEvents” from completedEvents.
    - Set updated\_notifications from notifications.
    - Set user\_settings at “notifications” from updated\_notifications.
  - Evaluate update\_user\_settings(“Event”, json.dumps(user\_settings), for\_update = true).
  - Evaluate sync\_user\_settings().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L5827) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L745)

<a id="op-e1012230d6ee12"></a>
### Update attending status

`operation_foundation_desk_record_definitions_event_business_behavior_update_attending_status`

**Inputs** event\_name, attendee, status.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Event” via get\_doc.

**State and service calls** request set\_value on “Event” · request set\_value on “Event Participants”.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to update attendance for another user.” · validation helper — translated “Attendee not found in this event.”.

**Local steps**

- Set event\_doc from Platform.get\_doc(“Event”, event\_name).
- Set caller from Platform.session.user.
- If attendee differs from caller.
  - If (event\_doc.owner differs from caller and not Platform.has\_permission(“Event”, “write”, event\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in event\_doc.owner differs from caller → not Platform.has\_permission(“Event”, “write”, event\_name).
    - Call the validation error handler Platform.throw(translated “You are not allowed to update attendance for another user.”, Platform.PermissionError).
- If event\_doc.owner equals caller.
  - Evaluate Platform.db.set\_value(“Event”, event\_name, “attending”, status).
  - Return no value.
- For each participant in event\_doc.event\_participants.
  - If participant.email equals attendee.
    - Evaluate Platform.db.set\_value(“Event Participants”, participant.name, “attending”, status).
    - Return no value.
- Call the validation error handler Platform.throw(translated “Attendee not found in this event.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Event”, “write”, event\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0170.json#L6223) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L756)

<a id="op-6195f4d25873da"></a>
### Delete communication

`operation_foundation_desk_record_definitions_event_business_behavior_delete_communication`

**Inputs** event, reference\_doctype, reference\_docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from reference\_doctype via get\_doc · read “Communication” via get\_list.

**State and service calls** request delete\_doc for “Communication”.

**Local steps**

- If isinstance(event, str).
  - Set event from json.loads(event).
- Set deleted\_participant from Platform.get\_doc(reference\_doctype, reference\_docname).
- Set comms from Platform.get\_list(“Communication”, filters = list(list(“Communication”, “reference\_doctype”, “=”, event.get(“doctype”)), list(“Communication”, “reference\_name”, “=”, event.get(“name”)), list(“Communication ….
- For each comm in comms.
  - Evaluate Platform.delete\_doc(“Communication”, comm).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L132) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L737)

<a id="op-6271a997c73026"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_event_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L458) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L752)

<a id="op-b08b3d2161fbf8"></a>
### Has permission

`operation_foundation_desk_record_definitions_event_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0171.json#L843) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L753)
