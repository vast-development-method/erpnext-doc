# Integrations and service calls · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Roster

<a id="op-e8e9d95e0e6313"></a>
### Get schedule from assignment

`operation_workforce_application_interface_roster_business_behavior_get_schedule_from_assignment`

**Inputs** shift\_schedule\_assignment.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Shift Schedule Assignment” via get\_value · read “Shift Schedule” via get\_value · read “Assignment Rule Day” via get\_all.

**Explicit results** mapping(“frequency” → frequency, “repeat\_on\_days” → repeat\_on\_days).

**Local steps**

- Evaluate Platform.has\_permission(“Shift Schedule Assignment”, “read”, shift\_schedule\_assignment, throw = true).
- Set shift\_schedule from Platform.db.get\_value(“Shift Schedule Assignment”, shift\_schedule\_assignment, “shift\_schedule”).
- Set frequency from Platform.db.get\_value(“Shift Schedule”, shift\_schedule, “frequency”).
- Set repeat\_on\_days from Platform.get\_all(“Assignment Rule Day”, filters = mapping(“parent” → shift\_schedule), pluck = “day”).
- Return mapping(“frequency” → frequency, “repeat\_on\_days” → repeat\_on\_days).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Shift Schedule Assignment”, “read”, shift\_schedule\_assignment, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L1810) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L52) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L52)

<a id="op-f90c4cce3122f0"></a>
### Create shift schedule assignment

`operation_workforce_application_interface_roster_business_behavior_create_shift_schedule_assignment`

**Inputs** employee, company, shift\_type, status, start\_date, end\_date, repeat\_on\_days, frequency, shift\_location = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → “Shift Schedule Assignment”, “shift\_schedule” → shift\_schedule, “employee” → employee, “company” → company, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Shift Schedule Assignment”, “shift\_schedule” → shift\_schedule, “employee” → employee, “company” → company, …)) · enqueue with shift\_schedule\_assignment.create\_shifts.

**Explicit results** shift\_schedule\_assignment.create\_shifts(start\_date, end\_date).

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Evaluate Platform.has\_permission(“Shift Schedule Assignment”, “create”, throw = true).
- Set shift\_schedule from get\_or\_insert\_shift\_schedule(shift\_type, frequency, repeat\_on\_days).
- Set shift\_schedule\_assignment from Platform.get\_doc(mapping(“doctype” → “Shift Schedule Assignment”, “shift\_schedule” → shift\_schedule, “employee” → employee, “company” → company, …)).insert().
  - Value choice on end\_date — true gives 0, false gives 1.
- Evaluate capture(“shift\_schedule\_assignment\_created”, mapping(“frequency” → frequency, “status” → status, “has\_end\_date” → bool(end\_date), “repeat\_on\_days” → len((repeat\_on\_days or list())))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in repeat\_on\_days → list().
- If (not end\_date or date\_diff(end\_date, start\_date) ≤ 90).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not end\_date → date\_diff(end\_date, start\_date) ≤ 90.
  - Return shift\_schedule\_assignment.create\_shifts(start\_date, end\_date).
- Evaluate Platform.enqueue(shift\_schedule\_assignment.create\_shifts, timeout = 4500, start\_date = start\_date, end\_date = end\_date).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true), Platform.has\_permission(“Shift Schedule Assignment”, “create”, throw = true) · service or queued work from Platform.enqueue(shift\_schedule\_assignment.create\_shifts, timeout = 4500, start\_date = start\_date, end\_date = end\_date).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L2137) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L46) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L46)

<a id="op-291f646c6c4714"></a>
### Delete shift schedule assignment

`operation_workforce_application_interface_roster_business_behavior_delete_shift_schedule_assignment`

**Inputs** shift\_schedule\_assignment.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Shift Schedule Assignment” via get\_doc · read “Shift Assignment” via get\_all · resolve a document from “Shift Assignment” via get\_doc.

**State and service calls** call cancel on shift\_assignment\_doc · request delete\_doc for “Shift Assignment” · request delete\_doc for “Shift Schedule Assignment”.

**Local steps**

- Set shift\_schedule\_assignment\_doc from Platform.get\_doc(“Shift Schedule Assignment”, shift\_schedule\_assignment).
- Evaluate shift\_schedule\_assignment\_doc.check\_permission(“delete”).
- For each shift\_assignment\_name in Platform.get\_all(“Shift Assignment”, mapping(“shift\_schedule\_assignment” → shift\_schedule\_assignment), pluck = “name”).
  - Set shift\_assignment\_doc from Platform.get\_doc(“Shift Assignment”, shift\_assignment\_name).
  - Evaluate Platform.has\_permission(“Employee”, “read”, shift\_assignment\_doc.employee, throw = true).
  - Evaluate shift\_assignment\_doc.check\_permission(“cancel” when shift\_assignment\_doc.docstatus equals 1, otherwise “delete”).
    - Value choice on shift\_assignment\_doc.docstatus equals 1 — true gives “cancel”, false gives “delete”.
  - If shift\_assignment\_doc.docstatus equals 1.
    - Evaluate shift\_assignment\_doc.cancel().
  - Evaluate Platform.delete\_doc(“Shift Assignment”, shift\_assignment\_name, ignore\_permissions = true).
- Evaluate Platform.delete\_doc(“Shift Schedule Assignment”, shift\_schedule\_assignment, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from shift\_schedule\_assignment\_doc.check\_permission(“delete”), Platform.has\_permission(“Employee”, “read”, shift\_assignment\_doc.employee, throw = true) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L2895) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L47) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L47)

<a id="op-b79cf388654405"></a>
### Swap shift

`operation_workforce_application_interface_roster_business_behavior_swap_shift`

**Inputs** src\_shift, src\_date, tgt\_employee, tgt\_date, tgt\_shift.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Shift Assignment” via get\_doc · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Source and target shifts cannot be the same”.

**Local steps**

- If src\_shift equals tgt\_shift.
  - Call the validation error handler Platform.throw(translated “Source and target shifts cannot be the same”).
- Set src\_shift\_doc from Platform.get\_doc(“Shift Assignment”, src\_shift).
- Evaluate Platform.has\_permission(“Employee”, “read”, src\_shift\_doc.employee, throw = true).
- Evaluate src\_shift\_doc.check\_permission(“write”).
- Evaluate Platform.has\_permission(“Employee”, “read”, tgt\_employee, throw = true).
- Evaluate Platform.has\_permission(“Shift Assignment”, “create”, throw = true).
- If tgt\_shift.
  - Set tgt\_shift\_doc from Platform.get\_doc(“Shift Assignment”, tgt\_shift).
  - Evaluate Platform.has\_permission(“Employee”, “read”, tgt\_shift\_doc.employee, throw = true).
  - Evaluate tgt\_shift\_doc.check\_permission(“write”).
  - Set tgt\_company from tgt\_shift\_doc.company.
  - Evaluate break\_shift(tgt\_shift\_doc, tgt\_date).
- Otherwise.
  - Set tgt\_company from Platform.db.get\_value(“Employee”, tgt\_employee, “company”).
- Evaluate capture(“shift\_swapped”, mapping(“mutual\_swap” → bool(tgt\_shift))).
- Evaluate break\_shift(src\_shift\_doc, src\_date).
- Evaluate insert\_shift(tgt\_employee, tgt\_company, src\_shift\_doc.shift\_type, tgt\_date, …).
- If tgt\_shift.
  - Evaluate insert\_shift(src\_shift\_doc.employee, src\_shift\_doc.company, tgt\_shift\_doc.shift\_type, src\_date, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, src\_shift\_doc.employee, throw = true), src\_shift\_doc.check\_permission(“write”) and 4 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L3394) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L56) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L56)

<a id="op-4f83f990dd3a67"></a>
### Break shift

`operation_workforce_application_interface_roster_business_behavior_break_shift`

**Inputs** assignment, date.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Shift Assignment” via get\_doc.

**State and service calls** call cancel on assignment · call save on assignment.

**Explicit failure paths** validation helper — translated “Cannot break shift after end date” · validation helper — translated “Cannot break shift before start date”.

**Local steps**

- If isinstance(assignment, str).
  - Set assignment from Platform.get\_doc(“Shift Assignment”, assignment).
- Evaluate Platform.has\_permission(“Employee”, “read”, assignment.employee, throw = true).
- Evaluate assignment.check\_permission(“write”).
- If (assignment.end\_date and date\_diff(assignment.end\_date, date) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in assignment.end\_date → date\_diff(assignment.end\_date, date) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Cannot break shift after end date”).
- If date\_diff(assignment.start\_date, date) &gt; 0.
  - Call the validation error handler Platform.throw(translated “Cannot break shift before start date”).
- Set employee from assignment.employee.
- Set company from assignment.company.
- Set shift\_type from assignment.shift\_type.
- Set status from assignment.status.
- Set end\_date from assignment.end\_date.
- Set shift\_location from assignment.shift\_location.
- If date\_diff(date, assignment.start\_date) equals 0.
  - Evaluate assignment.cancel().
  - Evaluate assignment.delete().
- Otherwise.
  - Set assignment.end\_date from add\_days(date, negative 1).
  - Evaluate assignment.save().
- If (not end\_date or date\_diff(end\_date, date) &gt; 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not end\_date → date\_diff(end\_date, date) &gt; 0.
  - Evaluate create\_shift\_assignment(employee, company, shift\_type, add\_days(date, 1), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, assignment.employee, throw = true), assignment.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L4238) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L45) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L45)

<a id="op-2fb1719cc39771"></a>
### Insert shift

`operation_workforce_application_interface_roster_business_behavior_insert_shift`

**Inputs** employee, company, shift\_type, start\_date, end\_date, status, shift\_location = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** read dict(mapping(“end\_date” → add\_days(start\_date, negative 1)), expanded names filters) via exists · read dict(mapping(“start\_date” → add\_days(end\_date, 1)), expanded names filters) via exists · read “Shift Assignment” via get\_value.

**State and service calls** request set\_value on “Shift Assignment” · request delete\_doc for “Shift Assignment”.

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Evaluate Platform.has\_permission(“Shift Assignment”, “create”, throw = true).
- Set filters from mapping(“doctype” → “Shift Assignment”, “employee” → employee, “company” → company, “shift\_type” → shift\_type, …).
- Set prev\_shift from Platform.db.exists(dict(mapping(“end\_date” → add\_days(start\_date, negative 1)), expanded names filters)).
- Set next\_shift from Platform.db.exists(dict(mapping(“start\_date” → add\_days(end\_date, 1)), expanded names filters)) when end\_date, otherwise no value.
  - Value choice on end\_date — true gives Platform.db.exists(dict(mapping(“start\_date” → add\_days(end\_date, 1)), expanded names filters)), false gives no value.
- If prev\_shift.
  - Evaluate Platform.has\_permission(“Shift Assignment”, “write”, prev\_shift, throw = true).
  - If next\_shift.
    - Evaluate Platform.has\_permission(“Shift Assignment”, “write”, next\_shift, throw = true).
    - Set end\_date from Platform.db.get\_value(“Shift Assignment”, next\_shift, “end\_date”).
    - Evaluate Platform.has\_permission(“Shift Assignment”, “delete”, next\_shift, throw = true).
    - Evaluate Platform.db.set\_value(“Shift Assignment”, next\_shift, “docstatus”, 2).
    - Evaluate Platform.delete\_doc(“Shift Assignment”, next\_shift).
  - Evaluate Platform.db.set\_value(“Shift Assignment”, prev\_shift, “end\_date”, (end\_date or no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in end\_date → no value.
- Otherwise.
  - If next\_shift.
    - Evaluate Platform.has\_permission(“Shift Assignment”, “write”, next\_shift, throw = true).
    - Evaluate Platform.db.set\_value(“Shift Assignment”, next\_shift, “start\_date”, start\_date).
  - Otherwise.
    - Evaluate create\_shift\_assignment(employee, company, shift\_type, start\_date, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true), Platform.has\_permission(“Shift Assignment”, “create”, throw = true) and 3 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L5012) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L55) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L55)

<a id="op-23b17068da4024"></a>
### Get holidays

`operation_workforce_application_interface_roster_business_behavior_get_holidays`

**Inputs** month\_start, month\_end, employee\_filters.

**Declared result** dict at tuple(str, list at dict).

**Record and data access** read “Employee” via get\_list · read “Holiday” via get\_all.

**Explicit results** holidays.

**Local steps**

- Evaluate \_validate\_employee\_filters(employee\_filters).
- Set holidays from mapping().
- Set holiday\_lists from mapping().
- For each employee in Platform.get\_list(“Employee”, filters = employee\_filters, pluck = “name”).
  - If not holiday\_list bound to get\_holiday\_list\_for\_employee(employee, raise\_exception = false, as\_on = month\_end).
    - Continue with the next iteration or loop test.
  - If holiday\_list does not belong to holiday\_lists.
    - Set holiday\_lists at holiday\_list from Platform.get\_all(“Holiday”, filters = mapping(“parent” → holiday\_list, “holiday\_date” → list(“between”, list(month\_start, month\_end))), fields = list(“name as holiday”, “holiday\_date”, “description”, “weekly\_off”)).
  - Set holidays at employee from holiday\_lists at holiday\_list.copy().
- Return holidays.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L6134) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L50) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L50)

<a id="op-3541bcbee9858f"></a>
### Get leaves

`operation_workforce_application_interface_roster_business_behavior_get_leaves`

**Inputs** month\_start, month\_end, employee\_filters.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** group\_by\_employee(query.run(as\_dict = true)).

**Local steps**

- Evaluate \_validate\_employee\_filters(employee\_filters).
- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from Platform.qb.get\_query(“Leave Application”, fields = list(LeaveApplication.name.as\_(“leave”), LeaveApplication.employee, LeaveApplication.leave\_type, LeaveApplication.from\_date, …), filters = mapping(“docst ….
- Set query from query.left\_join(Employee).on(LeaveApplication.employee equals Employee.name).
- For each filter in employee\_filters.
  - Set query from query.where(Employee at filter equals employee\_filters at filter).
- Return group\_by\_employee(query.run(as\_dict = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L6617) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L51) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L51)

<a id="op-5571125386eb8a"></a>
### Get shifts

`operation_workforce_application_interface_roster_business_behavior_get_shifts`

**Inputs** month\_start, month\_end, employee\_filters, shift\_filters.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** group\_by\_employee(query.run(as\_dict = true)).

**Local steps**

- Evaluate \_validate\_employee\_filters(employee\_filters).
- Evaluate \_validate\_shift\_filters(shift\_filters).
- Set ShiftAssignment from Platform.qb.DocType(“Shift Assignment”).
- Set ShiftType from Platform.qb.DocType(“Shift Type”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from Platform.qb.get\_query(“Shift Assignment”, fields = list(ShiftAssignment.name, ShiftAssignment.employee, ShiftAssignment.shift\_type, ShiftAssignment.shift\_location, …), filters = mapping(“docstatus” → 1, “s ….
- Set query from query.where((ShiftAssignment.end\_date ≥ month\_start bitwise or ShiftAssignment.end\_date.isnull())).
- Set query from nested operand in the contract(nested operand in the contract).select(ShiftType.start\_time, ShiftType.end\_time, ShiftType.color).left\_join(Employee).on(ShiftAssignment.employee equals Employee.name).
- For each filter in employee\_filters.
  - Set query from query.where(Employee at filter equals employee\_filters at filter).
- For each filter in shift\_filters.
  - Set query from query.where(ShiftAssignment at filter equals shift\_filters at filter).
- Return group\_by\_employee(query.run(as\_dict = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L53) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L53)

<a id="op-bb4890422f69c5"></a>
### Group by employee

`operation_workforce_application_interface_roster_business_behavior_group_by_employee`

**Inputs** events.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** grouped\_events.

**Local steps**

- Set grouped\_events from mapping().
- For each event in events.
  - Evaluate grouped\_events.setdefault(event at “employee”, list()).append(mapping of k → v for tuple(k, v) drawn from event.items() where k differs from “employee”).
    - Draw tuple(k, v) from event.items(), keep a combination only if (k differs from “employee”).
- Return grouped\_events.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L869) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L54) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L54)

## Service · System settings

<a id="op-f26daa9feca2d6"></a>
### Get user pass login disabled

`operation_workforce_application_interface_system_settings_business_behavior_get_user_pass_login_disabled`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1096) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L59) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L59)
