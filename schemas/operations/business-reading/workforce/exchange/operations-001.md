# Integrations and service calls · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-c11b3ca757a6a7"></a>
### Get current user info

`operation_workforce_application_interface_initialize_business_behavior_get_current_user_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “User” via get\_value.

**Explicit results** user.

**Local steps**

- Set current\_user from Platform.session.user.
- Set user from Platform.db.get\_value(“User”, current\_user, list(“name”, “first\_name”, “full\_name”, “user\_image”), as\_dict = true).
- Set user at “roles” from Platform.get\_roles(current\_user).
- Return user.

**Values supplied outside this operation** effective access from Platform.get\_roles(current\_user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L1438) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L17) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L17)

<a id="op-49b5801397f302"></a>
### Get current employee info

`operation_workforce_application_interface_initialize_business_behavior_get_current_employee_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** employee.

**Local steps**

- Set current\_user from Platform.session.user.
- Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → current\_user, “status” → “Active”), list(“name”, “first\_name”, “employee\_name”, “designation”, …), as\_dict = true).
- Return employee.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L1646) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L16) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L16)

<a id="op-5712bc7f304d55"></a>
### Get all employees

`operation_workforce_application_interface_initialize_business_behavior_get_all_employees`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_list.

**Explicit results** Platform.get\_list(“Employee”, fields = list(“name”, “employee\_name”, “designation”, “department”, …), limit = 999999).

**Local steps**

- Return Platform.get\_list(“Employee”, fields = list(“name”, “employee\_name”, “designation”, “department”, …), limit = 999999).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L1880) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L6) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L6)

<a id="op-ad30be812727e7"></a>
### Get reports to employee name

`operation_workforce_application_interface_initialize_business_behavior_get_reports_to_employee_name`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “Employee” via get\_value.

**Explicit results** (Platform.db.get\_value(“Employee”, employee, “employee\_name”) or empty text).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set reports\_to from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user, “status” → “Active”), “reports\_to”).
- If (not reports\_to or reports\_to differs from employee).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reports\_to → reports\_to differs from employee.
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Return (Platform.db.get\_value(“Employee”, employee, “employee\_name”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Employee”, employee, “employee\_name”) → empty text.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2064) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L36) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L36)

<a id="op-308c00809fbb3f"></a>
### Get current employee

`operation_workforce_application_interface_initialize_business_behavior_get_current_employee`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** employee.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Employee not found”.

**Local steps**

- Set employee from get\_current\_employee\_info().get(“name”).
- If not employee.
  - Call the validation error handler Platform.throw(translated “Employee not found”, Platform.PermissionError).
- Return employee.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2350) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L15) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L15)

<a id="op-2c4bf4e1932902"></a>
### Get hr settings

`operation_workforce_application_interface_initialize_business_behavior_get_human_resources_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** Platform.\_dict(allow\_employee\_checkin\_from\_mobile\_app = settings.allow\_employee\_checkin\_from\_mobile\_app, allow\_geolocation\_tracking = settings.allow\_geolocation\_tracking, prevent\_self\_leave\_approval = sett ….

**Local steps**

- Set settings from Platform.db.get\_singles\_dict(“HR Settings”, cast = true).
- Return Platform.\_dict(allow\_employee\_checkin\_from\_mobile\_app = settings.allow\_employee\_checkin\_from\_mobile\_app, allow\_geolocation\_tracking = settings.allow\_geolocation\_tracking, prevent\_self\_leave\_approval = sett ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2487) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L28) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L28)

<a id="op-d92a3de0f62126"></a>
### Get unread notifications count

`operation_workforce_application_interface_initialize_business_behavior_get_unread_notifications_count`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** int.

**Record and data access** read “PWA Notification” via count.

**Explicit results** Platform.db.count(“PWA Notification”, mapping(“to\_user” → Platform.session.user, “read” → 0)).

**Local steps**

- Return Platform.db.count(“PWA Notification”, mapping(“to\_user” → Platform.session.user, “read” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2652) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L40) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L40)

<a id="op-291567ae018d83"></a>
### Mark all notifications as read

`operation_workforce_application_interface_initialize_business_behavior_mark_all_notifications_as_read`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** request set\_value on “PWA Notification”.

**Local steps**

- Evaluate Platform.db.set\_value(“PWA Notification”, mapping(“to\_user” → Platform.session.user, “read” → 0), “read”, 1, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2773) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L43) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L43)

<a id="op-3b0f61a83ea296"></a>
### Are push notifications enabled

`operation_workforce_application_interface_initialize_business_behavior_are_push_notifications_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Record and data access** read “Push Notification Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”) · false.

**Local steps**

- Attempt the following.
  - Return Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”).
- On failure (Platform.DoesNotExistError).
  - Return false.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Push Notification Settings”, “enable\_push\_notification\_relay”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L2931) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L3) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L3)

<a id="op-bf619c2f284d86"></a>
### Get attendance calendar events

`operation_workforce_application_interface_initialize_business_behavior_get_attendance_calendar_events`

**Inputs** from\_date, to\_date.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, str).

**Explicit results** events.

**Local steps**

- Set employee from get\_current\_employee().
- Set holidays from get\_holidays\_for\_calendar(employee, from\_date, to\_date).
- Set attendance from get\_attendance\_for\_calendar(employee, from\_date, to\_date).
- Set events from mapping().
- Set date from getdate(from\_date).
- While date\_diff(to\_date, date) ≥ 0.
  - Set date\_str from date.strftime(“%Y-%m-%d”).
  - If date belongs to attendance.
    - Set events at date\_str from attendance at date.
  - Otherwise.
    - If date belongs to holidays.
      - Set events at date\_str from “Holiday”.
  - Set date from add\_days(date, 1).
- Return events.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L3047) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L9) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L9)

<a id="op-a6b2c8a8b8441d"></a>
### Get attendance for calendar

`operation_workforce_application_interface_initialize_business_behavior_get_attendance_for_calendar`

**Inputs** employee, from\_date, to\_date.

**Declared result** list at dict at tuple(str, str).

**Record and data access** read “Attendance” via get\_all.

**Explicit results** mapping of d at “attendance\_date” → d at “status” for d drawn from attendance.

**Local steps**

- Set attendance from Platform.get\_all(“Attendance”, mapping(“employee” → employee, “attendance\_date” → list(“between”, list(from\_date, to\_date)), “docstatus” → 1), list(“attendance\_date”, “status”)).
- Return mapping of d at “attendance\_date” → d at “status” for d drawn from attendance.
  - Draw d from attendance.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L3467) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L10) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L10)

<a id="op-b5448514ceffb6"></a>
### Get holidays for calendar

`operation_workforce_application_interface_initialize_business_behavior_get_holidays_for_calendar`

**Inputs** employee, from\_date, to\_date.

**Declared result** list at str.

**Explicit results** get\_holiday\_dates\_between\_range(employee, from\_date, to\_date, raise\_exception\_for\_holiday\_list = false).

**Local steps**

- Bind dependencies get\_holiday\_dates\_between\_range.
- Return get\_holiday\_dates\_between\_range(employee, from\_date, to\_date, raise\_exception\_for\_holiday\_list = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L4) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L26) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L26)

<a id="op-8f5d5e1527ca8e"></a>
### Get shift requests

`operation_workforce_application_interface_initialize_business_behavior_get_shift_remote_requests`

**Inputs** employee, approver\_id = no value, for\_approval = false, limit = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Shift Request” via get\_list.

**Explicit results** shift\_requests.

**Local steps**

- Set filters from get\_filters(“Shift Request”, employee, approver\_id, for\_approval).
- Set fields from list(“name”, “employee”, “employee\_name”, “shift\_type”, …).
- If workflow\_state\_field bound to get\_workflow\_state\_field(“Shift Request”).
  - Evaluate fields.append(workflow\_state\_field).
- Set shift\_requests from Platform.get\_list(“Shift Request”, fields = fields, filters = filters, order\_by = “creation desc”, limit = limit).
- If workflow\_state\_field.
  - For each application in shift\_requests.
    - Set application at “workflow\_state\_field” from workflow\_state\_field.
- Return shift\_requests.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L3963) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L37) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L37)

<a id="op-6f5c18f5352b0e"></a>
### Get attendance requests

`operation_workforce_application_interface_initialize_business_behavior_get_attendance_remote_requests`

**Inputs** employee, for\_approval = false, limit = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Attendance Request” via get\_list.

**Explicit results** attendance\_requests.

**Local steps**

- Set filters from get\_filters(“Attendance Request”, employee, no value, for\_approval).
- Set fields from list(“name”, “reason”, “employee”, “employee\_name”, …).
- If workflow\_state\_field bound to get\_workflow\_state\_field(“Attendance Request”).
  - Evaluate fields.append(workflow\_state\_field).
- Set attendance\_requests from Platform.get\_list(“Attendance Request”, fields = fields, filters = filters, order\_by = “creation desc”, limit = limit).
- If workflow\_state\_field.
  - For each application in attendance\_requests.
    - Set application at “workflow\_state\_field” from workflow\_state\_field.
- Return attendance\_requests.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L4429) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L11) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L11)

<a id="op-0e3e57d6b791d4"></a>
### Get filters

`operation_workforce_application_interface_initialize_business_behavior_get_filters`

**Inputs** doctype, employee, approver\_id = no value, for\_approval = false.

**Declared result** dict.

**Explicit results** filters.

**Local steps**

- Set filters from Platform.\_dict().
- If for\_approval.
  - Set filters.docstatus from 0.
  - Set filters.employee from tuple(“!=”, employee).
  - If workflow bound to get\_workflow(doctype).
    - Set allowed\_states from get\_allowed\_states\_for\_workflow(workflow, approver\_id).
    - Set filters at workflow.workflow\_state\_field from tuple(“in”, allowed\_states).
  - Otherwise.
    - If doctype differs from “Attendance Request”.
      - Set approver\_field\_map from mapping(“Shift Request” → “approver”, “Leave Application” → “leave\_approver”, “Expense Claim” → “expense\_approver”).
      - Set filters.status from “Open” when doctype equals “Leave Application”, otherwise “Draft”.
        - Value choice on doctype equals “Leave Application” — true gives “Open”, false gives “Draft”.
      - If approver\_id.
        - Set filters at approver\_field\_map at doctype from approver\_id.
- Otherwise.
  - Set filters.docstatus from tuple(“!=”, 2).
  - Set filters.employee from employee.
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L4871) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L25) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L25)

<a id="op-b1a69c86b4e4ca"></a>
### Get shift request approvers

`operation_workforce_application_interface_initialize_business_behavior_get_shift_request_approvers`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or list at str).

**Record and data access** read “Employee” via get\_cached\_value · read “Department Approver” via get\_value · read “User” via get\_value.

**State and service calls** call insert on department\_approvers.

**Explicit results** department\_approvers.

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set tuple(shift\_request\_approver, department) from Platform.get\_cached\_value(“Employee”, employee, list(“shift\_request\_approver”, “department”)).
- Set department\_approvers from list().
- If department.
  - Set department\_approvers from get\_department\_approvers(department, “shift\_request\_approver”).
  - If not shift\_request\_approver.
    - Set shift\_request\_approver from Platform.db.get\_value(“Department Approver”, mapping(“parent” → department, “parentfield” → “shift\_request\_approver”, “idx” → 1), “approver”).
- Set shift\_request\_approver\_name from Platform.db.get\_value(“User”, shift\_request\_approver, “full\_name”, cache = true).
- If (shift\_request\_approver and shift\_request\_approver does not belong to list of approver.name for approver drawn from department\_approvers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_request\_approver → shift\_request\_approver does not belong to list of approver.name for approver drawn from department\_approvers.
  - Draw approver from department\_approvers.
  - Evaluate department\_approvers.insert(0, mapping(“name” → shift\_request\_approver, “full\_name” → shift\_request\_approver\_name)).
- Return department\_approvers.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true) · configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“shift\_request\_approver”, “department”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L8) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L38) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L38)

<a id="op-5476b35f779707"></a>
### Get shifts

`operation_workforce_application_interface_initialize_business_behavior_get_shifts`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict at tuple(str, str).

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Local steps**

- Set employee from get\_current\_employee().
- Set ShiftAssignment from Platform.qb.DocType(“Shift Assignment”).
- Set ShiftType from Platform.qb.DocType(“Shift Type”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L5971) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L39) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L39)

<a id="op-7a3b27303bb20c"></a>
### Get leave applications

`operation_workforce_application_interface_initialize_business_behavior_get_leave_applications`

**Inputs** employee, approver\_id = no value, for\_approval = false, limit = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Leave Application” via get\_list.

**Explicit results** applications.

**Local steps**

- Set filters from get\_filters(“Leave Application”, employee, approver\_id, for\_approval).
- Set fields from list(“name”, “posting\_date”, “employee”, “employee\_name”, …).
- If workflow\_state\_field bound to get\_workflow\_state\_field(“Leave Application”).
  - Evaluate fields.append(workflow\_state\_field).
- Set applications from Platform.get\_list(“Leave Application”, fields = fields, filters = filters, order\_by = “posting\_date desc”, limit = limit).
- If workflow\_state\_field.
  - For each application in applications.
    - Set application at “workflow\_state\_field” from workflow\_state\_field.
- Return applications.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L29) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L29)

<a id="op-2d93243f7af45d"></a>
### Get leave balance map

`operation_workforce_application_interface_initialize_business_behavior_get_leave_balance_map`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, dict at tuple(str, float)).

**Explicit results** leave\_map.

**Local steps**

- Bind dependencies get\_leave\_details.
- Set employee from get\_current\_employee().
- Set date from getdate().
- Set leave\_map from mapping().
- Set leave\_details from get\_leave\_details(employee, date).
- Set allocation from leave\_details at “leave\_allocation”.
- For each tuple(leave\_type, details) in allocation.items().
  - Set leave\_map at leave\_type from mapping(“allocated\_leaves” → details.get(“total\_leaves”), “balance\_leaves” → details.get(“remaining\_leaves”)).
- Return leave\_map.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L6935) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L31) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L31)

<a id="op-3094c2c7b70647"></a>
### Get holidays for employee

`operation_workforce_application_interface_initialize_business_behavior_get_holidays_for_employee`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list() · holidays.

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set holiday\_list from get\_holiday\_list\_for\_employee(employee, raise\_exception = false).
- If not holiday\_list.
  - Return list().
- Set Holiday from Platform.qb.DocType(“Holiday”).
- Set holidays from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
- For each holiday in holidays.
  - Set holiday at “description” from strip\_html((holiday at “description” or empty text)).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in holiday at “description” → empty text.
- Return holidays.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L5) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L27) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L27)

<a id="op-d2d53c69a4c85c"></a>
### Get leave approval details

`operation_workforce_application_interface_initialize_business_behavior_get_leave_approval_details`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Employee” via get\_cached\_value · read “Department Approver” via get\_value · read “User” via get\_value · read “HR Settings” via get\_single\_value.

**Explicit results** dict(leave\_approver = leave\_approver, leave\_approver\_name = leave\_approver\_name, department\_approvers = department\_approvers, is\_mandatory = Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mand ….

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set tuple(leave\_approver, department) from Platform.get\_cached\_value(“Employee”, employee, list(“leave\_approver”, “department”)).
- If (not leave\_approver and department).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not leave\_approver → department.
  - Set leave\_approver from Platform.db.get\_value(“Department Approver”, mapping(“parent” → department, “parentfield” → “leave\_approvers”, “idx” → 1), “approver”).
- Set leave\_approver\_name from Platform.db.get\_value(“User”, leave\_approver, “full\_name”, cache = true).
- Set department\_approvers from get\_department\_approvers(department, “leave\_approvers”).
- If (leave\_approver and leave\_approver does not belong to list of approver.name for approver drawn from department\_approvers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_approver → leave\_approver does not belong to list of approver.name for approver drawn from department\_approvers.
  - Draw approver from department\_approvers.
  - Evaluate department\_approvers.append(mapping(“name” → leave\_approver, “full\_name” → leave\_approver\_name)).
- Return dict(leave\_approver = leave\_approver, leave\_approver\_name = leave\_approver\_name, department\_approvers = department\_approvers, is\_mandatory = Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mand ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true) · configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“leave\_approver”, “department”)), Platform.db.get\_single\_value(“HR Settings”, “leave\_approver\_mandatory\_in\_leave\_application”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L7) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L30) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L30)

<a id="op-336f9ad2e7cd38"></a>
### Get department approvers

`operation_workforce_application_interface_initialize_business_behavior_get_department_approvers`

**Inputs** department, parentfield.

**Declared result** list at str.

**Record and data access** read “Department” via get\_value · read “Department” via get\_all.

**Explicit results** list() · department\_approvers.

**Local steps**

- If not department.
  - Return list().
- Set department\_details from Platform.db.get\_value(“Department”, department, list(“lft”, “rgt”), as\_dict = true).
- Set departments from Platform.get\_all(“Department”, filters = mapping(“lft” → tuple(“&lt;=”, department\_details.lft), “rgt” → tuple(“&gt;=”, department\_details.rgt), “disabled” → 0), pluck = “name”).
- Set Approver from Platform.qb.DocType(“Department Approver”).
- Set User from Platform.qb.DocType(“User”).
- Set department\_approvers from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“name”), nested operand in the contract.as\_(“full\_name”)).where((nested operand in the contract.pare ….
- Return department\_approvers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L1148) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L18) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L18)

<a id="op-27831b6e82ca1e"></a>
### Get leave types

`operation_workforce_application_interface_initialize_business_behavior_get_leave_types`

**Inputs** employee, date.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** leave\_types.

**Local steps**

- Bind dependencies get\_leave\_details.
- Set date from (date or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date → getdate().
- Set leave\_details from get\_leave\_details(employee, date).
- Set leave\_types from (list(leave\_details at “leave\_allocation”.keys()) + leave\_details at “lwps”).
- Return leave\_types.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L1770) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L32) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L32)

<a id="op-d064f513ef5d5f"></a>
### Get expense claims

`operation_workforce_application_interface_initialize_business_behavior_get_expense_claims`

**Inputs** employee, approver\_id = no value, for\_approval = false, limit = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Expense Claim” via get\_list.

**Explicit results** claims.

**Local steps**

- Set filters from get\_filters(“Expense Claim”, employee, approver\_id, for\_approval).
- Set fields from list(“′tabExpense Claim′.name”, “′tabExpense Claim′.posting\_date”, “′tabExpense Claim′.employee”, “′tabExpense Claim′.employee\_name”, …).
- If workflow\_state\_field bound to get\_workflow\_state\_field(“Expense Claim”).
  - Evaluate fields.append(workflow\_state\_field).
- Set claims from Platform.get\_list(“Expense Claim”, fields = fields, filters = filters, order\_by = “′tabExpense Claim′.posting\_date desc”, group\_by = “′tabExpense Claim′.name”, …).
- If workflow\_state\_field.
  - For each claim in claims.
    - Set claim at “workflow\_state\_field” from workflow\_state\_field.
- Return claims.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L1980) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L23) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L23)
