# Employment and attendance · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave application

[Record definition](../../../../data/record-types/leave_application.json)

<a id="op-490fe2cfcfc3dd"></a>
### Leave Application.get consecutive leave details

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_consecutive_leave_details`

**Inputs** self.

**Declared result** dict.

**Explicit results** Platform.\_dict(mapping(“total\_consecutive\_leaves” → total\_consecutive\_leaves, “leave\_applications” → leave\_applications)).

**Local steps**

- Set leave\_applications from set().
- Bind local operation \_get\_first\_from\_date for subsequent calls.
- Bind local operation \_get\_last\_to\_date for subsequent calls.
- Set first\_from\_date from \_get\_first\_from\_date(self.from\_date).
- Set last\_to\_date from \_get\_last\_to\_date(self.to\_date).
- Set total\_consecutive\_leaves from get\_number\_of\_leave\_days(self.employee, self.leave\_type, first\_from\_date, last\_to\_date).
- Return Platform.\_dict(mapping(“total\_consecutive\_leaves” → total\_consecutive\_leaves, “leave\_applications” → leave\_applications)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1167) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1146)

<a id="op-5ba895740b0d60"></a>
### Leave Application.get consecutive leave details.get first from date

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_consecutive_leave_details_get_first_from_date`

**Inputs** reference\_date.

**Record and data access** read “Leave Application” via get\_value.

**Explicit results** \_get\_first\_from\_date(application.from\_date) · reference\_date.

**Local steps**

- Set prev\_date from add\_days(reference\_date, negative 1).
- Set application from Platform.db.get\_value(“Leave Application”, mapping(“employee” → self.employee, “leave\_type” → self.leave\_type, “to\_date” → prev\_date, “docstatus” → list(“!=”, 2), …), list(“name”, “from\_date”), as\_dict = true).
- If application.
  - Evaluate leave\_applications.add(application.name).
  - Return \_get\_first\_from\_date(application.from\_date).
- Return reference\_date.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L834) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1168) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1147)

<a id="op-eabf047e2ba0f6"></a>
### Leave Application.get consecutive leave details.get last to date

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_consecutive_leave_details_get_last_to_date`

**Inputs** reference\_date.

**Record and data access** read “Leave Application” via get\_value.

**Explicit results** \_get\_last\_to\_date(application.to\_date) · reference\_date.

**Local steps**

- Set next\_date from add\_days(reference\_date, 1).
- Set application from Platform.db.get\_value(“Leave Application”, mapping(“employee” → self.employee, “leave\_type” → self.leave\_type, “from\_date” → next\_date, “docstatus” → list(“!=”, 2), …), list(“name”, “to\_date”), as\_dict = true).
- If application.
  - Evaluate leave\_applications.add(application.name).
  - Return \_get\_last\_to\_date(application.to\_date).
- Return reference\_date.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L1163) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1169) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1148)

<a id="op-1016772ab91cf0"></a>
### Leave Application.validate attendance

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_attendance`

**Inputs** self.

**Record and data access** read “Attendance” via get\_all.

**Explicit failure paths** validation helper with AttendanceAlreadyMarkedError — translated “Attendance for employee {0} is already marked for the following dates: {1}”.format(self.employee, ((text in the contract + “&lt;/li&gt;&lt;li&gt;”.join(generator of get\_link\_to\_form(“Attendance”, nested op ….

**Local steps**

- Set attendance\_dates from Platform.get\_all(“Attendance”, filters = list(list(“employee”, “=”, self.employee), list(“attendance\_date”, “between”, list(self.from\_date, self.to\_date)), list(“status”, “in”, list(“Present”, “Work From H ….
- If attendance\_dates.
  - Call the validation error handler Platform.throw(translated “Attendance for employee {0} is already marked for the following dates: {1}”.format(self.employee, ((text in the contract + “&lt;/li&gt;&lt;li&gt;”.join(generator of nested operand in the con ….
    - Draw a from attendance\_dates.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L1488) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1191) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1170)

<a id="op-5927b17310e1be"></a>
### Leave Application.validate optional leave

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_optional_leave`

**Inputs** self.

**Record and data access** read “Leave Period” via get\_value · read mapping(“doctype” → “Holiday”, “parent” → optional\_holiday\_list, “holiday\_date” → day) via exists.

**Explicit failure paths** validation helper — translated “Cannot find active Leave Period” · validation helper — translated “Optional Holiday List not set for leave period {0}”.format(leave\_period at 0 at “name”) · validation helper with NotAnOptionalHoliday — translated “{0} is not in Optional Holiday List”.format(formatdate(day)).

**Local steps**

- Set leave\_period from get\_leave\_period(self.from\_date, self.to\_date, self.company).
- If not leave\_period.
  - Call the validation error handler Platform.throw(translated “Cannot find active Leave Period”).
- Set optional\_holiday\_list from Platform.db.get\_value(“Leave Period”, leave\_period at 0 at “name”, “optional\_holiday\_list”).
- If not optional\_holiday\_list.
  - Call the validation error handler Platform.throw(translated “Optional Holiday List not set for leave period {0}”.format(leave\_period at 0 at “name”)).
- Set day from getdate(self.from\_date).
- While day ≤ getdate(self.to\_date).
  - If not Platform.db.exists(mapping(“doctype” → “Holiday”, “parent” → optional\_holiday\_list, “holiday\_date” → day)).
    - Call the validation error handler Platform.throw(translated “{0} is not in Optional Holiday List”.format(formatdate(day)), NotAnOptionalHoliday).
  - Set day from add\_days(day, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L1932) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1202) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1180)

<a id="op-daf6c3e3da92b5"></a>
### Leave Application.set half day date

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_set_half_day_date`

**Inputs** self.

**Local steps**

- If (self.from\_date equals self.to\_date and self.half\_day equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date equals self.to\_date → self.half\_day equals 1.
  - Set self.half\_day\_date from self.from\_date.
- If self.half\_day equals 0.
  - Set self.half\_day\_date from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L2477) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1183) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1162)

<a id="op-66beeda9965da8"></a>
### Leave Application.notify employee

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_notify_employee`

**Inputs** self.

**Record and data access** resolve a document from “Leave Application” via get\_doc · read “HR Settings” via get\_single\_value · resolve a document from “Email Template” via get\_doc.

**State and service calls** msgprint with translated “Please set default template for Leave Status Notification in HR Settings.”.

**Explicit results** no value.

**Local steps**

- Set employee\_email from get\_employee\_email(self.employee).
- If not employee\_email.
  - Return no value.
- Set parent\_doc from Platform.get\_doc(“Leave Application”, self.name).
- Set args from parent\_doc.as\_dict().
- Set template from Platform.db.get\_single\_value(“HR Settings”, “leave\_status\_notification\_template”).
- If not template.
  - Evaluate Platform.msgprint(translated “Please set default template for Leave Status Notification in HR Settings.”).
  - Return no value.
- Set email\_template from Platform.get\_doc(“Email Template”, template).
- Set subject from Platform.render\_template(email\_template.subject, args).
- Set message from Platform.render\_template(email\_template.response\_, args).
- Evaluate self.notify(mapping(“message” → message, “message\_to” → employee\_email, “subject” → subject, “notify” → “employee”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify](operations-027.md#op-6f571e373cf378).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “leave\_status\_notification\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L2626) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1175) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1154)

<a id="op-63d763b6f10d3e"></a>
### Leave Application.notify leave approver

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_notify_leave_approver`

**Inputs** self.

**Record and data access** resolve a document from “Leave Application” via get\_doc · read “HR Settings” via get\_single\_value · resolve a document from “Email Template” via get\_doc.

**State and service calls** msgprint with translated “Please set default template for Leave Approval Notification in HR Settings.”.

**Explicit results** no value.

**Local steps**

- If self.leave\_approver.
  - Set parent\_doc from Platform.get\_doc(“Leave Application”, self.name).
  - Set args from parent\_doc.as\_dict().
  - Set template from Platform.db.get\_single\_value(“HR Settings”, “leave\_approval\_notification\_template”).
  - If not template.
    - Evaluate Platform.msgprint(translated “Please set default template for Leave Approval Notification in HR Settings.”).
    - Return no value.
  - Set email\_template from Platform.get\_doc(“Email Template”, template).
  - Set subject from Platform.render\_template(email\_template.subject, args).
  - Set message from Platform.render\_template(email\_template.response\_, args).
  - Evaluate self.notify(mapping(“message” → message, “message\_to” → self.leave\_approver, “subject” → subject)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify](operations-027.md#op-6f571e373cf378).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “leave\_approval\_notification\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L3082) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1176) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1155)

<a id="op-6f571e373cf378"></a>
### Leave Application.notify

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_notify`

**Inputs** self, args.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** sendmail · msgprint with translated “Email sent to {0}”.format(contact).

**Local steps**

- Set args from Platform.\_dict(args).
- If cint(self.follow\_via\_email).
  - Set contact from args.message\_to.
  - If not isinstance(contact, list).
    - If not args.notify equals “employee”.
      - Set contact from (Platform.get\_doc(“User”, contact).email or contact).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_doc(“User”, contact).email → contact.
  - Set sender from dict().
  - Set sender at “email” from Platform.get\_doc(“User”, Platform.session.user).email.
  - Set sender at “full\_name” from get\_fullname(sender at “email”).
  - Attempt the following.
    - Evaluate Platform.sendmail(recipients = contact, sender = sender at “email”, subject = args.subject, message = args.message).
    - Evaluate Platform.msgprint(translated “Email sent to {0}”.format(contact)).
  - On failure (Platform.OutgoingEmailError).
    - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = contact, sender = sender at “email”, subject = args.subject, message = args.message).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L3489) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1174) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1153)

<a id="op-d746e34cb3bd0a"></a>
### Leave Application.create leave ledger entry

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_create_leave_ledger_entry`

**Inputs** self, submit = true.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.status differs from “Approved” and submit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status differs from “Approved” → submit.
  - Return no value.
- Set expiry\_date from get\_allocation\_expiry\_for\_cf\_leaves(self.employee, self.leave\_type, self.to\_date, self.from\_date).
- Set lwp from Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_lwp”).
- If expiry\_date.
  - Evaluate self.create\_ledger\_entry\_for\_intermediate\_allocation\_expiry(expiry\_date, submit, lwp).
- Otherwise.
  - Set tuple(alloc\_on\_from\_date, alloc\_on\_to\_date) from self.get\_allocation\_based\_on\_application\_dates().
  - If self.is\_separate\_ledger\_entry\_required(alloc\_on\_from\_date, alloc\_on\_to\_date).
    - Evaluate self.create\_separate\_ledger\_entries(alloc\_on\_from\_date, alloc\_on\_to\_date, submit, lwp).
  - Otherwise.
    - Set raise\_exception from false when Platform.flags.in\_patch, otherwise true.
      - Value choice on Platform.flags.in\_patch — true gives false, false gives true.
    - Set args from dict(leaves = (self.total\_leave\_days × negative 1), from\_date = self.from\_date, to\_date = self.to\_date, is\_lwp = lwp, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_exception, as\_on = self.from\_date) → empty text.
    - Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create ledger entry for intermediate allocation expiry](operations-027.md#op-a093b0840328db), [get allocation based on application dates](operations-026.md#op-d747b7e6f6cf20), [is separate ledger entry required](operations-027.md#op-1005659e3fab23), [create separate ledger entries](operations-027.md#op-7d15603656320a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L53) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1161) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1140)

<a id="op-1005659e3fab23"></a>
### Leave Application.is separate ledger entry required

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_is_separate_ledger_entry_required`

**Inputs** self, alloc\_on\_from\_date = no value, alloc\_on\_to\_date = no value.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If ((alloc\_on\_from\_date and not alloc\_on\_to\_date) or (not alloc\_on\_from\_date and alloc\_on\_to\_date) or (alloc\_on\_from\_date and alloc\_on\_to\_date and alloc\_on\_from\_date.name differs from alloc\_on\_to\_date.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (alloc\_on\_from\_date and not alloc\_on\_to\_date) → (not alloc\_on\_from\_date and alloc\_on\_to\_date) → (alloc\_on\_from\_date and alloc\_on\_to\_date and alloc\_on\_from\_date.name differs from alloc\_on\_to\_date.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in alloc\_on\_from\_date → not alloc\_on\_to\_date.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not alloc\_on\_from\_date → alloc\_on\_to\_date.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in alloc\_on\_from\_date → alloc\_on\_to\_date → alloc\_on\_from\_date.name differs from alloc\_on\_to\_date.name.
  - Return true.
- Return false.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L4542) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1173) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1152)

<a id="op-7d15603656320a"></a>
### Leave Application.create separate ledger entries

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_create_separate_ledger_entries`

**Inputs** self, alloc\_on\_from\_date, alloc\_on\_to\_date, submit, lwp.

**Explicit failure paths** validation helper — translated “Leave Application period cannot be across two non-consecutive leave allocations {0} and {1}.”.format(get\_link\_to\_form(“Leave Allocation”, alloc\_on\_from\_date.name), get\_link\_to\_form(“Leave Alloc ….

**Local steps**

- If (submit and alloc\_on\_from\_date and alloc\_on\_to\_date and add\_days(alloc\_on\_from\_date.to\_date, 1) differs from alloc\_on\_to\_date.from\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in submit → alloc\_on\_from\_date → alloc\_on\_to\_date → add\_days(alloc\_on\_from\_date.to\_date, 1) differs from alloc\_on\_to\_date.from\_date.
  - Call the validation error handler Platform.throw(translated “Leave Application period cannot be across two non-consecutive leave allocations {0} and {1}.”.format(get\_link\_to\_form(“Leave Allocation”, alloc\_on\_from\_date.name), get\_link\_to\_fo ….
- Set raise\_exception from false when Platform.flags.in\_patch, otherwise true.
  - Value choice on Platform.flags.in\_patch — true gives false, false gives true.
- If alloc\_on\_from\_date.
  - Set first\_alloc\_end from alloc\_on\_from\_date.to\_date.
  - Set second\_alloc\_start from add\_days(alloc\_on\_from\_date.to\_date, 1).
- Otherwise.
  - Set first\_alloc\_end from add\_days(alloc\_on\_to\_date.from\_date, negative 1).
  - Set second\_alloc\_start from alloc\_on\_to\_date.from\_date.
- Set leaves\_in\_first\_alloc from get\_number\_of\_leave\_days(self.employee, self.leave\_type, self.from\_date, first\_alloc\_end, …).
- Set leaves\_in\_second\_alloc from get\_number\_of\_leave\_days(self.employee, self.leave\_type, second\_alloc\_start, self.to\_date, …).
- Set args from dict(is\_lwp = lwp).
- If leaves\_in\_first\_alloc.
  - Evaluate args.update(dict(from\_date = self.from\_date, to\_date = first\_alloc\_end, leaves = (leaves\_in\_first\_alloc × negative 1), holiday\_list = (get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_e ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_exception, as\_on = self.from\_date) → empty text.
  - Evaluate create\_leave\_ledger\_entry(self, args, submit).
- If leaves\_in\_second\_alloc.
  - Evaluate args.update(dict(from\_date = second\_alloc\_start, to\_date = self.to\_date, leaves = (leaves\_in\_second\_alloc × negative 1), holiday\_list = (get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_exception, as\_on = second\_alloc\_start) → empty text.
  - Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L55) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1164) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1143)

<a id="op-a093b0840328db"></a>
### Leave Application.create ledger entry for intermediate allocation expiry

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_create_ledger_entry_for_intermediate_allocation_expiry`

**Inputs** self, expiry\_date, submit, lwp.

**Local steps**

- Set raise\_exception from false when Platform.flags.in\_patch, otherwise true.
  - Value choice on Platform.flags.in\_patch — true gives false, false gives true.
- Set leaves from get\_number\_of\_leave\_days(self.employee, self.leave\_type, self.from\_date, expiry\_date, …).
- If leaves.
  - Set args from dict(from\_date = self.from\_date, to\_date = expiry\_date, leaves = (leaves × negative 1), is\_lwp = lwp, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_exception, as\_on = self.from\_date) → empty text.
  - Evaluate create\_leave\_ledger\_entry(self, args, submit).
- If getdate(expiry\_date) differs from getdate(self.to\_date).
  - Set start\_date from add\_days(expiry\_date, 1).
  - Set leaves from get\_number\_of\_leave\_days(self.employee, self.leave\_type, start\_date, self.to\_date, …).
  - If leaves.
    - Set args from dict(from\_date = start\_date, to\_date = self.to\_date, leaves = (leaves × negative 1), is\_lwp = lwp, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_holiday\_list\_for\_employee(self.employee, raise\_exception = raise\_exception, as\_on = start\_date) → empty text.
    - Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L54) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1162) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1141)

<a id="op-686622a0fdb8a1"></a>
### Leave Application.validate leave approver

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_leave_approver`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Leave Approver is mandatory”.

**Local steps**

- If (self.docstatus differs from 2 and not self.leave\_approver and Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus differs from 2 → not self.leave\_approver → Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).
  - Call the validation error handler Platform.throw(translated “Leave Approver is mandatory”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L6115) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1199) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1177)

<a id="op-be2f59441019a0"></a>
### Leave Application.set leave approver name

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_set_leave_approver_name`

**Inputs** self.

**Local steps**

- If not self.leave\_approver.
  - Set self.leave\_approver\_name from no value.
- Otherwise.
  - If (not self.leave\_approver\_name or self.has\_value\_changed(“leave\_approver”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.leave\_approver\_name → self.has\_value\_changed(“leave\_approver”).
    - Set self.leave\_approver\_name from get\_fullname(self.leave\_approver).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L6268) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1184) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1163)

<a id="op-bef34830bba880"></a>
### Leave Application.validate for self approval

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_for_self_approval`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Self-approval for leaves is not allowed”.

**Local steps**

- Set self\_leave\_approval\_not\_allowed from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_leave\_approval”).
- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”).
- If (self\_leave\_approval\_not\_allowed and employee\_user equals Platform.session.user and not get\_workflow\_name(“Leave Application”) and self.status equals “Approved”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self\_leave\_approval\_not\_allowed → employee\_user equals Platform.session.user → not get\_workflow\_name(“Leave Application”) → self.status equals “Approved”.
  - Call the validation error handler Platform.throw(translated “Self-approval for leaves is not allowed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_leave\_approval”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L6419) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1197) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1176)

<a id="op-3e6b36d8c6c538"></a>
### Leave Application.onload

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_onload`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Local steps**

- Evaluate self.set\_onload(“self\_leave\_approval\_not\_allowed”, Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_leave\_approval”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “prevent\_self\_leave\_approval”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0051.json#L6679) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1181) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1160)

<a id="op-b840915c38316e"></a>
### Get allocation expiry for cf leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_allocation_expiry_for_cash_flow_leaves`

**Inputs** employee, leave\_type, to\_date, from\_date.

**Declared result** str.

**Explicit results** expiry at 0 at 0 when expiry, otherwise empty text.

**Local steps**

- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set expiry from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….run().
- Return expiry at 0 at 0 when expiry, otherwise empty text.
  - Value choice on expiry — true gives expiry at 0 at 0, false gives empty text.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1136) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1116)

<a id="op-93b835b8bf0af6"></a>
### Get number of leave days

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_number_of_leave_days`

**Inputs** employee, leave\_type, from\_date, to\_date, half\_day = no value, half\_day\_date = no value, holiday\_list = no value, leave\_application = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** number\_of\_days.

**Local steps**

- Evaluate validate\_leave\_access(employee, leave\_application).
- Set number\_of\_days from 0.
- If cint(half\_day) equals 1.
  - If getdate(from\_date) equals getdate(to\_date).
    - Set number\_of\_days from 0.5.
  - Otherwise.
    - If (half\_day\_date and getdate(from\_date) ≤ getdate(half\_day\_date) ≤ getdate(to\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in half\_day\_date → getdate(from\_date) ≤ getdate(half\_day\_date) ≤ getdate(to\_date).
      - Compare adjacent operands in order, stopping at the first false comparison in getdate(from\_date) ≤ getdate(half\_day\_date) ≤ getdate(to\_date).
      - Set number\_of\_days from (date\_diff(to\_date, from\_date) + 0.5).
    - Otherwise.
      - Set number\_of\_days from (date\_diff(to\_date, from\_date) + 1).
- Otherwise.
  - Set number\_of\_days from (date\_diff(to\_date, from\_date) + 1).
- If not Platform.db.get\_value(“Leave Type”, leave\_type, “include\_holiday”).
  - Set number\_of\_days from (flt(number\_of\_days) − flt(get\_holidays(employee, from\_date, to\_date, leave\_application = leave\_application))).
- Return number\_of\_days.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L52) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1153) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1132)

<a id="op-7b9dfc1691bdeb"></a>
### Get leave details

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_details`

**Inputs** employee, date, for\_salary\_slip = false, leave\_application = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “System Settings” via get\_single\_value · read “Leave Type” via get\_list.

**Explicit results** mapping(“leave\_allocation” → leave\_allocation, “leave\_approver” → get\_employee\_leave\_approver(employee), “lwps” → lwp).

**Local steps**

- Evaluate validate\_leave\_access(employee, leave\_application).
- Set allocation\_records from get\_leave\_allocation\_records(employee, date).
- Set leave\_allocation from mapping().
- Set precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 2.
- For each d in allocation\_records.
  - Set allocation from allocation\_records.get(d, Platform.\_dict()).
  - Set to\_date from date when for\_salary\_slip, otherwise allocation.to\_date.
    - Value choice on for\_salary\_slip — true gives date, false gives allocation.to\_date.
  - Set remaining\_leaves from get\_leave\_balance\_on(employee, d, date, to\_date = to\_date, consider\_all\_leaves\_in\_the\_allocation\_period = false when for\_salary\_slip, otherwise true, leave\_application = leave\_application).
    - Value choice on for\_salary\_slip — true gives false, false gives true.
  - Set leaves\_taken from (get\_leaves\_for\_period(employee, d, allocation.from\_date, to\_date) × negative 1).
  - Set leaves\_pending from get\_leaves\_pending\_approval\_for\_period(employee, d, allocation.from\_date, to\_date).
  - Set expired\_leaves from (allocation.total\_leaves\_allocated − (remaining\_leaves + leaves\_taken)).
  - Set leave\_allocation at d from mapping(“total\_leaves” → flt(allocation.total\_leaves\_allocated, precision), “expired\_leaves” → flt(expired\_leaves, precision) when expired\_leaves &gt; 0, otherwise 0, “leaves\_taken” → flt(leaves\_taken, precis ….
    - Value choice on expired\_leaves &gt; 0 — true gives flt(expired\_leaves, precision), false gives 0.
- Set lwp from Platform.get\_list(“Leave Type”, filters = mapping(“is\_lwp” → 1), pluck = “name”).
- Return mapping(“leave\_allocation” → leave\_allocation, “leave\_approver” → get\_employee\_leave\_approver(employee), “lwps” → lwp).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L50) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1145) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1125)

<a id="op-63e4b6e893e4d5"></a>
### Get leave balance on

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_balance_on`

**Inputs** employee, leave\_type, date, to\_date = no value, consider\_all\_leaves\_in\_the\_allocation\_period = false, for\_consumption = false, leave\_application = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, float).

**Explicit results** remaining\_leaves · remaining\_leaves.get(“leave\_balance”).

**Local steps**

- Evaluate validate\_leave\_access(employee, leave\_application).
- If not to\_date.
  - Set to\_date from nowdate().
- Set allocation\_records from get\_leave\_allocation\_records(employee, date, leave\_type).
- Set allocation from allocation\_records.get(leave\_type, Platform.\_dict()).
- Set end\_date from allocation.to\_date when (allocation and cint(consider\_all\_leaves\_in\_the\_allocation\_period)), otherwise date.
  - Value choice on (allocation and cint(consider\_all\_leaves\_in\_the\_allocation\_period)) — true gives allocation.to\_date, false gives date.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocation → cint(consider\_all\_leaves\_in\_the\_allocation\_period).
- Set cf\_expiry from get\_allocation\_expiry\_for\_cf\_leaves(employee, leave\_type, to\_date, allocation.from\_date).
- Set leaves\_taken from get\_leaves\_for\_period(employee, leave\_type, allocation.from\_date, end\_date).
- Set manually\_expired\_leaves from get\_manually\_expired\_leaves(employee, leave\_type, allocation.from\_date, end\_date).
- Set remaining\_leaves from get\_remaining\_leaves(allocation, leaves\_taken, date, cf\_expiry, …).
- If for\_consumption.
  - Return remaining\_leaves.
- Otherwise.
  - Return remaining\_leaves.get(“leave\_balance”).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L49) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1144) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1124)

<a id="op-f61a26b431756f"></a>
### Get leave allocation records

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_allocation_records`

**Inputs** employee, date, leave\_type = no value.

**Explicit results** allocated\_leaves.

**Local steps**

- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set LeaveAdjustment from Platform.qb.DocType(“Leave Adjustment”).
- Set cf\_leave\_case from nested operand in the contract.terms.Case().when(Ledger.is\_carry\_forward equals “1”, Ledger.leaves).else\_(0).
- Set sum\_cf\_leaves from Sum(cf\_leave\_case).as\_(“cf\_leaves”).
- Set new\_leaves\_case from nested operand in the contract.terms.Case().when(Ledger.is\_carry\_forward equals “0”, Ledger.leaves).else\_(0).
- Set sum\_new\_leaves from Sum(new\_leaves\_case).as\_(“new\_leaves”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.transaction\_name equals nested operand in the contract.name).select(sum\_cf\_leaves, sum\_new\_leaves, Min(neste ….
- If leave\_type.
  - Set query from query.where(Ledger.leave\_type equals leave\_type).
- Set query from query.groupby(Ledger.employee, Ledger.leave\_type).
- Set allocation\_details from query.run(as\_dict = true).
- Set allocated\_leaves from Platform.\_dict().
- For each d in allocation\_details.
  - Evaluate allocated\_leaves.setdefault(d.leave\_type, Platform.\_dict(mapping(“from\_date” → d.from\_date, “to\_date” → d.to\_date, “total\_leaves\_allocated” → (flt(d.cf\_leaves) + flt(d.new\_leaves)), “unused\_leaves” → d.cf\_ ….
- Return allocated\_leaves.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L2676) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1141) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1121)

<a id="op-075e78b6c250e2"></a>
### Get leaves pending approval for period

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leaves_pending_approval_for_period`

**Inputs** employee, leave\_type, from\_date, to\_date.

**Declared result** float.

**Record and data access** read “Leave Application” via get\_all.

**Explicit results** leaves at “leaves” when leaves at “leaves”, otherwise 0.0.

**Local steps**

- Set leaves from Platform.get\_all(“Leave Application”, filters = mapping(“employee” → employee, “leave\_type” → leave\_type, “status” → “Open”), or\_filters = mapping(“from\_date” → list(“between”, tuple(from\_date, to\_date)),  … at 0.
- Return leaves at “leaves” when leaves at “leaves”, otherwise 0.0.
  - Value choice on leaves at “leaves” — true gives leaves at “leaves”, false gives 0.0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L4175) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1149) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1128)

<a id="op-e3b88c1180d731"></a>
### Get remaining leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_remaining_leaves`

**Inputs** allocation, leaves\_taken, date, cf\_expiry, manually\_expired\_leaves.

**Declared result** dict at tuple(str, float).

**Explicit results** Platform.\_dict(leave\_balance = leave\_balance, leave\_balance\_for\_consumption = remaining\_leaves).

**Local steps**

- Bind local operation \_get\_remaining\_leaves for subsequent calls.
- If (cf\_expiry and allocation.unused\_leaves).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cf\_expiry → allocation.unused\_leaves.
  - Set tuple(new\_leaves\_taken, cf\_leaves\_taken) from get\_new\_and\_cf\_leaves\_taken(allocation, cf\_expiry).
  - If getdate(date) &gt; getdate(cf\_expiry).
    - Set cf\_leaves, remaining\_cf\_leaves from 0.
  - Otherwise.
    - Set cf\_leaves from (flt(allocation.unused\_leaves) + flt(cf\_leaves\_taken)).
    - Set remaining\_cf\_leaves from \_get\_remaining\_leaves(cf\_leaves, cf\_expiry).
  - Set leave\_balance from (((flt(allocation.new\_leaves\_allocated) + flt(new\_leaves\_taken)) + flt(cf\_leaves)) + flt(manually\_expired\_leaves)).
  - Set leave\_balance\_for\_consumption from (((flt(allocation.new\_leaves\_allocated) + flt(new\_leaves\_taken)) + flt(remaining\_cf\_leaves)) + flt(manually\_expired\_leaves)).
- Otherwise.
  - Set leave\_balance, leave\_balance\_for\_consumption from ((flt(allocation.total\_leaves\_allocated) + flt(leaves\_taken)) + flt(manually\_expired\_leaves)).
- Set remaining\_leaves from \_get\_remaining\_leaves(leave\_balance\_for\_consumption, allocation.to\_date).
- Return Platform.\_dict(leave\_balance = leave\_balance, leave\_balance\_for\_consumption = remaining\_leaves).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L4518) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1154) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1133)
