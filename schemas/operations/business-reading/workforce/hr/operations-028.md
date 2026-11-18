# Employment and attendance · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave application

[Record definition](../../../../data/record-types/leave_application.json)

<a id="op-af5ad306d7f7eb"></a>
### Get remaining leaves.get remaining leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_remaining_leaves_get_remaining_leaves`

**Inputs** remaining\_leaves, end\_date.

**Explicit results** remaining\_leaves.

**Local steps**

- If remaining\_leaves &gt; 0.
  - Set remaining\_days from (date\_diff(end\_date, date) + 1).
  - Set remaining\_leaves from min(remaining\_days, remaining\_leaves).
- Return remaining\_leaves.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L5263) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1155) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1134)

<a id="op-bc99063def1930"></a>
### Get manually expired leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_manually_expired_leaves`

**Inputs** employee, leave\_type, from\_date, end\_date.

**Explicit results** leaves at 0 at 0 when leaves, otherwise 0.0.

**Local steps**

- Set ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set leaves from nested operand in the contract(nested operand in the contract).select(ledger.leaves).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the c ….run().
- Return leaves at 0 at 0 when leaves, otherwise 0.0.
  - Value choice on leaves — true gives leaves at 0 at 0, false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L5399) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1151) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1130)

<a id="op-bf058db7806b21"></a>
### Get new and cf leaves taken

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_new_and_cash_flow_leaves_taken`

**Inputs** allocation, cf\_expiry.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(new\_leaves\_taken, cf\_leaves\_taken).

**Local steps**

- Set cf\_leaves\_taken from get\_leaves\_for\_period(allocation.employee, allocation.leave\_type, allocation.from\_date, cf\_expiry).
- Set new\_leaves\_taken from get\_leaves\_for\_period(allocation.employee, allocation.leave\_type, add\_days(cf\_expiry, 1), allocation.to\_date).
- If abs(cf\_leaves\_taken) &gt; allocation.unused\_leaves.
  - Update new\_leaves\_taken using + negative (abs(cf\_leaves\_taken) − allocation.unused\_leaves).
  - Set cf\_leaves\_taken from negative allocation.unused\_leaves.
- Return tuple(new\_leaves\_taken, cf\_leaves\_taken).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L5810) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1152) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1131)

<a id="op-891f9bdcb19389"></a>
### Get leaves for period

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leaves_for_period`

**Inputs** employee, leave\_type, from\_date, to\_date, skip\_expired\_leaves = true.

**Declared result** float.

**Record and data access** read “Leave Application” via get\_value.

**Explicit results** leave\_days.

**Local steps**

- Set leave\_entries from get\_leave\_entries(employee, leave\_type, from\_date, to\_date).
- Set leave\_days from 0.
- For each leave\_entry in leave\_entries.
  - Set inclusive\_period from (leave\_entry.from\_date ≥ getdate(from\_date) and leave\_entry.to\_date ≤ getdate(to\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_entry.from\_date ≥ getdate(from\_date) → leave\_entry.to\_date ≤ getdate(to\_date).
  - If (inclusive\_period and leave\_entry.transaction\_type equals “Leave Encashment”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in inclusive\_period → leave\_entry.transaction\_type equals “Leave Encashment”.
    - Update leave\_days using + leave\_entry.leaves.
  - Otherwise.
    - If (inclusive\_period and leave\_entry.transaction\_type equals “Leave Allocation” and leave\_entry.is\_expired and not skip\_expired\_leaves).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in inclusive\_period → leave\_entry.transaction\_type equals “Leave Allocation” → leave\_entry.is\_expired → not skip\_expired\_leaves.
      - Update leave\_days using + leave\_entry.leaves.
    - Otherwise.
      - If leave\_entry.transaction\_type equals “Leave Application”.
        - If inclusive\_period.
          - Update leave\_days using + leave\_entry.leaves.
          - Continue with the next iteration or loop test.
        - If leave\_entry.from\_date &lt; getdate(from\_date).
          - Set leave\_entry.from\_date from from\_date.
        - If leave\_entry.to\_date &gt; getdate(to\_date).
          - Set leave\_entry.to\_date from to\_date.
        - Set half\_day from 0.
        - Set half\_day\_date from no value.
        - If (leave\_entry.leaves modulo or format 1).
          - Set half\_day from 1.
          - Set half\_day\_date from Platform.db.get\_value(“Leave Application”, leave\_entry.transaction\_name, “half\_day\_date”).
        - Update leave\_days using + (get\_number\_of\_leave\_days(employee, leave\_type, leave\_entry.from\_date, leave\_entry.to\_date, holiday\_list = leave\_entry.holiday\_list, …) × negative 1).
- Return leave\_days.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L51) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1148) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1127)

<a id="op-b63b798acedb7b"></a>
### Get leave entries

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_entries`

**Inputs** employee, leave\_type, from\_date, to\_date.

**Explicit results** nested operand in the contract(nested operand in the contract).select(Ledger.employee, Ledger.leave\_type, Ledger.from\_date, Ledger.to\_date, …).where(((((nested operand in the contract bitwise and nested op ….

**Local steps**

- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Return nested operand in the contract(nested operand in the contract).select(Ledger.employee, Ledger.leave\_type, Ledger.from\_date, Ledger.to\_date, …).where(((((nested operand in the contract bitwise and nested op ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0052.json#L6827) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1146) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1126)

<a id="op-aa94936eee1e38"></a>
### Get holidays

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_holidays`

**Inputs** employee, from\_date, to\_date, leave\_application = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** int.

**Explicit results** len(holidays).

**Local steps**

- Evaluate validate\_leave\_access(employee, leave\_application).
- Set holidays from get\_holiday\_dates\_between\_range(employee, from\_date, to\_date).
- Return len(holidays).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L47) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1140) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1120)

<a id="op-c48d11cca5ae5b"></a>
### Is lwp

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_is_leave_without_pay`

**Inputs** leave\_type.

**Explicit results** ((lwp and cint(lwp at 0 at 0)) or 0).

**Local steps**

- Set LeaveType from Platform.qb.DocType(“Leave Type”).
- Set lwp from nested operand in the contract(nested operand in the contract).select(LeaveType.is\_lwp).where(LeaveType.name equals leave\_type).run().
- Return ((lwp and cint(lwp at 0 at 0)) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (lwp and cint(lwp at 0 at 0)) → 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lwp → cint(lwp at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1156) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1135)

<a id="op-27394c4cc47ed5"></a>
### Get events

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_value · read “Global Defaults” via get\_single\_value.

**Explicit results** events.

**Local steps**

- Bind dependencies json.
- Set filters from json.loads(filters).
- For each tuple(idx, filter) in enumerate(filters).
  - Set filters at idx from filter at slice 1 to negative 1.
- Set events from list().
- Set employee from Platform.db.get\_value(“Employee”, filters = mapping(“user\_id” → Platform.session.user), fieldname = list(“name”, “company”), as\_dict = true).
- If employee.
  - Set tuple(employee, company) from tuple(employee.name, employee.company).
- Otherwise.
  - Set employee from empty text.
  - Set company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
- If “Employee” belongs to Platform.get\_roles().
  - Evaluate add\_department\_leaves(events, start, end, employee, …).
- Evaluate add\_leaves(events, start, end, filters).
- Evaluate add\_block\_dates(events, start, end, employee, …).
- Evaluate add\_holidays(events, start, end, employee, …).
- Return events.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L229) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1139) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1119)

<a id="op-ce2300f1b60a49"></a>
### Add department leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_add_department_leaves`

**Inputs** events, start, end, employee, company.

**Record and data access** read “Employee” via get\_value · read “Employee” via get\_list.

**Local steps**

- If department bound to Platform.db.get\_value(“Employee”, employee, “department”).
  - Set department\_employees from Platform.get\_list(“Employee”, filters = mapping(“department” → department, “company” → company), pluck = “name”).
  - Set filters from list(list(“employee”, “in”, department\_employees)).
  - Evaluate add\_leaves(events, start, end, filters = filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L873) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1133) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1113)

<a id="op-8b4fcef76f045a"></a>
### Add leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_add_leaves`

**Inputs** events, start, end, filters = no value.

**Record and data access** read “HR Settings” via get\_single\_value · read “Leave Application” via get\_all · read “Leave Application” via get\_list.

**Local steps**

- If not filters.
  - Set filters from list().
- Evaluate filters.extend(list(list(“from\_date”, “&lt;=”, getdate(end)), list(“to\_date”, “&gt;=”, getdate(start)), list(“status”, “in”, list(“Approved”, “Open”)), list(“docstatus”, “&lt;”, 2))).
- Set fields from list(“name”, “from\_date”, “to\_date”, “color”, …).
- Set show\_leaves\_of\_all\_members from Platform.db.get\_single\_value(“HR Settings”, “show\_leaves\_of\_all\_department\_members\_in\_calendar”).
- If cint(show\_leaves\_of\_all\_members).
  - Set leave\_applications from Platform.get\_all(“Leave Application”, filters = filters, fields = fields).
- Otherwise.
  - Set leave\_applications from Platform.get\_list(“Leave Application”, filters = filters, fields = fields).
- For each d in leave\_applications.
  - Set d at “title” from formatted text {d at “employee\_name”} ({d at “leave\_type”}).
  - Set d at “allDay” from 1.
  - Set d at “doctype” from “Leave Application”.
  - Remove d at “employee\_name”.
  - Remove d at “leave\_type”.
  - If d does not belong to events.
    - Evaluate events.append(d).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “show\_leaves\_of\_all\_department\_members\_in\_calendar”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L1157) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1135) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1115)

<a id="op-0081773322bff5"></a>
### Add block dates

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_add_block_dates`

**Inputs** events, start, end, employee, company.

**Local steps**

- Set cnt from 0.
- Set block\_dates from get\_applicable\_block\_dates(start, end, employee, company, all\_lists = true).
- For each block\_date in block\_dates.
  - Evaluate events.append(mapping(“doctype” → “Leave Block List Date”, “from\_date” → block\_date.block\_date, “to\_date” → block\_date.block\_date, “title” → ((translated “Leave Blocked” + “: ”) + block\_date.reason), …)).
  - Update cnt using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L1879) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1132) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1112)

<a id="op-85113701c84b63"></a>
### Add holidays

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_add_holidays`

**Inputs** events, start, end, employee, company.

**Local steps**

- Bind dependencies get\_holidays\_for\_employee.
- For each holiday in get\_holidays\_for\_employee(employee, start, end, raise\_exception = false).
  - Evaluate events.append(mapping(“doctype” → “Holiday”, “from\_date” → holiday.holiday\_date, “to\_date” → holiday.holiday\_date, “title” → ((translated “Holiday” + “: ”) + cstr(holiday.description)), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L46) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1134) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1114)

<a id="op-a9e7a361bef38a"></a>
### Get mandatory approval

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_mandatory_approval`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** ((str bitwise or int) bitwise or bool).

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** mandatory.

**Local steps**

- Set mandatory from empty text.
- If doctype equals “Leave Application”.
  - Set mandatory from Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).
- Otherwise.
  - Set mandatory from Platform.db.get\_single\_value(“HR Settings”, “expense\_approver\_mandatory\_in\_expense\_claim”).
- Return mandatory.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”), Platform.db.get\_single\_value(“HR Settings”, “expense\_approver\_mandatory\_in\_expense\_claim”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L2720) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1150) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1129)

<a id="op-d7de3d76bc84c3"></a>
### Get approved leaves for period

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_approved_leaves_for_period`

**Inputs** employee, leave\_type, from\_date, to\_date.

**Explicit results** leave\_days.

**Local steps**

- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set query from nested operand in the contract.qb.from\_(LeaveApplication).select(LeaveApplication.employee, LeaveApplication.leave\_type, LeaveApplication.from\_date, LeaveApplication.to\_date, …).where((((LeaveApplication.e ….
- If leave\_type.
  - Set query from query.where(LeaveApplication.leave\_type equals leave\_type).
- Set leave\_applications from query.run(as\_dict = true).
- Set leave\_days from 0.
- For each leave\_app in leave\_applications.
  - If (leave\_app.from\_date ≥ getdate(from\_date) and leave\_app.to\_date ≤ getdate(to\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_app.from\_date ≥ getdate(from\_date) → leave\_app.to\_date ≤ getdate(to\_date).
    - Update leave\_days using + leave\_app.total\_leave\_days.
  - Otherwise.
    - If leave\_app.from\_date &lt; getdate(from\_date).
      - Set leave\_app.from\_date from from\_date.
    - If leave\_app.to\_date &gt; getdate(to\_date).
      - Set leave\_app.to\_date from to\_date.
    - Update leave\_days using + get\_number\_of\_leave\_days(employee, leave\_type, leave\_app.from\_date, leave\_app.to\_date).
- Return leave\_days.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L2938) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1137) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1117)

<a id="op-ef4f1d9e5f27db"></a>
### Get leave approver

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_approver`

**Inputs** employee, leave\_application = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** get\_employee\_leave\_approver(employee).

**Local steps**

- Evaluate validate\_leave\_access(employee, leave\_application).
- Return get\_employee\_leave\_approver(employee).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L48) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1142) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1122)

<a id="op-c11a54555d9f8a"></a>
### Get employee leave approver

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_employee_leave_approver`

**Inputs** employee.

**Declared result** str.

**Record and data access** read “Employee” via get\_value · read “Department Approver” via get\_value.

**Explicit results** leave\_approver.

**Local steps**

- Set tuple(leave\_approver, department) from Platform.db.get\_value(“Employee”, employee, list(“leave\_approver”, “department”)).
- If (not leave\_approver and department).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not leave\_approver → department.
  - Set leave\_approver from Platform.db.get\_value(“Department Approver”, mapping(“parent” → department, “parentfield” → “leave\_approvers”, “idx” → 1), “approver”).
- Return leave\_approver.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L3782) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1138) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1118)

<a id="op-0db21a0b57df93"></a>
### On doctype update

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Leave Application”.

**Local steps**

- Evaluate Platform.db.add\_index(“Leave Application”, list(“employee”, “from\_date”, “to\_date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L4024) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1204) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1182)

<a id="op-233744278e45aa"></a>
### Get leave approver and mandatory

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_get_leave_approver_and_mandatory`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** mapping(“is\_mandatory” → 1 when mandatory, otherwise 0, “leave\_approver” → get\_employee\_leave\_approver(employee)).

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set mandatory from Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).
- Return mapping(“is\_mandatory” → 1 when mandatory, otherwise 0, “leave\_approver” → get\_employee\_leave\_approver(employee)).
  - Value choice on mandatory — true gives 1, false gives 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true) · configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L4111) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1143) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1123)

<a id="op-25737b612064c3"></a>
### Validate leave access

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_validate_leave_access`

**Inputs** employee, leave\_application = no value.

**Record and data access** read “Employee” via get\_value · read “Leave Application” via get\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, employee, “user\_id”).
- Set leave\_approver from get\_employee\_leave\_approver(employee).
- If (Platform.session.user does not belong to tuple(employee\_user, leave\_approver) and not Platform.has\_permission(“Employee”, “read”, employee) and not (leave\_application and nested operand in the contract.db ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user does not belong to tuple(employee\_user, leave\_approver) → not Platform.has\_permission(“Employee”, “read”, employee) → not (leave\_application and Platform.db.get\_value(“Leave Application”, leave\_application, “employee”) equals employee and Platform.has\_permission(“Leave Application”, “read”, leave\_application)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_application → Platform.db.get\_value(“Leave Application”, leave\_application, “employee”) equals employee → Platform.has\_permission(“Leave Application”, “read”, leave\_application).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee), Platform.has\_permission(“Leave Application”, “read”, leave\_application).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L58) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1205) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1183)

<a id="op-ae8507fdf1f18f"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_application_leave_application_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_application”, “transactions” → list(mapping(“items” → list(“Attendance”))), “reports” → list(mapping(“label” → translated “Reports”, “items” → list(“Employee Leave Balance”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_application”, “transactions” → list(mapping(“items” → list(“Attendance”))), “reports” → list(mapping(“label” → translated “Reports”, “items” → list(“Employee Leave Balance”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0053.json#L4580) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1206) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1184)

## Record · Leave block list

[Record definition](../../../../data/record-types/leave_block_list.json)

<a id="op-8313e5b63ad9a4"></a>
### Leave Block List.validate

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_leave_block_list_validate`

**Inputs** self.

**State and service calls** msgprint with ((translated “Date is repeated” + “:”) + d.block\_date).

**Local steps**

- Set dates from list().
- For each d in self.get(“leave\_block\_list\_dates”).
  - If d.block\_date belongs to dates.
    - Evaluate Platform.msgprint(((translated “Date is repeated” + “:”) + d.block\_date), raise\_exception = 1).
  - Evaluate dates.append(d.block\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L3367) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1266) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1242)

<a id="op-4823e06856554c"></a>
### Leave Block List.set weekly off dates

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_leave_block_list_set_weekly_off_dates`

**Inputs** self, start\_date, end\_date, days, reason.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Set date\_list from self.get\_block\_dates\_from\_date(start\_date, end\_date, days).
- For each date in date\_list.
  - Evaluate self.append(“leave\_block\_list\_dates”, mapping(“block\_date” → date, “reason” → reason)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get block dates from date](operations-028.md#op-a0a21bacdd1fcc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L3571) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1265) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1241)

<a id="op-a0a21bacdd1fcc"></a>
### Leave Block List.get block dates from date

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_leave_block_list_get_block_dates_from_date`

**Inputs** self, start\_date, end\_date, days.

**Explicit results** date\_list.

**Local steps**

- Set tuple(start\_date, end\_date) from tuple(getdate(start\_date), getdate(end\_date)).
- Bind dependencies calendar.
- Bind dependencies timedelta.
- Set date\_list from list().
- Set existing\_date\_list from list of getdate(d.block\_date) for d drawn from self.get(“leave\_block\_list\_dates”).
  - Draw d from self.get(“leave\_block\_list\_dates”).
- While start\_date ≤ end\_date.
  - If (start\_date does not belong to existing\_date\_list and calendar.day\_name at start\_date.weekday() belongs to days).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date does not belong to existing\_date\_list → calendar.day\_name at start\_date.weekday() belongs to days.
    - Evaluate date\_list.append(start\_date).
  - Update start\_date using + timedelta(days = 1).
- Return date\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L3788) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1264) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1240)

<a id="op-183259b66562f7"></a>
### Get applicable block dates

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_get_applicable_block_dates`

**Inputs** from\_date, to\_date, employee = no value, company = no value, all\_lists = false, leave\_type = no value.

**Record and data access** read “Leave Block List Date” via get\_all.

**Explicit results** Platform.db.get\_all(“Leave Block List Date”, filters = mapping(“parent” → list(“IN”, get\_applicable\_block\_lists(employee, company, all\_lists, leave\_type)), “block\_date” → list(“BETWEEN”, list(getdate(from\_ ….

**Local steps**

- Return Platform.db.get\_all(“Leave Block List Date”, filters = mapping(“parent” → list(“IN”, get\_applicable\_block\_lists(employee, company, all\_lists, leave\_type)), “block\_date” → list(“BETWEEN”, list(getdate(from\_ ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L4148) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1260) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1236)
