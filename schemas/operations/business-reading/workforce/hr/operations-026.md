# Employment and attendance · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave application

[Record definition](../../../../data/record-types/leave_application.json)

<a id="op-a9125a07799c03"></a>
### Leave Application.before cancel

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_before_cancel`

**Inputs** self.

**Local steps**

- Set self.status from “Cancelled”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L4868) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1159) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1138)

<a id="op-8cbbf901941c59"></a>
### Leave Application.on discard

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L4915) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1178) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1157)

<a id="op-e5cefa2ac7617e"></a>
### Leave Application.on cancel

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_on_cancel`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Local steps**

- Evaluate self.create\_leave\_ledger\_entry(submit = false).
- If Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).
  - Evaluate self.notify\_employee().
- Evaluate self.cancel\_attendance().
- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave ledger entry](operations-027.md#op-d746e34cb3bd0a), [notify employee](operations-027.md#op-66beeda9965da8), [cancel attendance](operations-026.md#op-00041a085876dc), [publish update](operations-026.md#op-c04730ffb8624b).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L4978) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1177) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1156)

<a id="op-ea30fba6ff8422"></a>
### Leave Application.after delete

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-026.md#op-c04730ffb8624b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L5145) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1157) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1136)

<a id="op-c04730ffb8624b"></a>
### Leave Application.publish update

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:my\_leaves”, employee\_user).
- Evaluate Workforce.refetch\_resource(“Workforce:team\_leaves”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L5196) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1182) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1161)

<a id="op-5d1c65a03cba04"></a>
### Leave Application.validate applicable after

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_applicable_after`

**Inputs** self.

**Record and data access** resolve a document from “Leave Type” via get\_doc · read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “{0} applicable after {1} calendar days”.format(self.leave\_type, leave\_type.applicable\_after).

**Local steps**

- If self.leave\_type.
  - Set leave\_type from Platform.get\_doc(“Leave Type”, self.leave\_type).
  - If leave\_type.applicable\_after &gt; 0.
    - Set date\_of\_joining from Platform.db.get\_value(“Employee”, self.employee, “date\_of\_joining”).
    - Set number\_of\_days from date\_diff(getdate(self.from\_date), date\_of\_joining).
    - If number\_of\_days ≥ 0.
      - If number\_of\_days &lt; leave\_type.applicable\_after.
        - Call the validation error handler Platform.throw(translated “{0} applicable after {1} calendar days”.format(self.leave\_type, leave\_type.applicable\_after)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L5346) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1190) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1169)

<a id="op-df01a1c55939ed"></a>
### Leave Application.validate dates

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_dates`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value · resolve a document from “User” via get\_doc.

**Explicit failure paths** validation helper — translated “Backdated Leave Application is restricted. Please set the {} in {}”.format(Platform.bold(translated “Role Allowed to Create Backdated Leave Application”), get\_link\_to\_form(“HR Settings”, “HR Se … · validation helper — translated “Only users with the {0} role can create backdated leave applications”.format(translated allowed\_role) · validation helper — translated “To date cannot be before from date” · validation helper — translated “Half Day Date should be between From Date and To Date”.

**Local steps**

- If Platform.db.get\_single\_value(“HR Settings”, “restrict\_backdated\_leave\_application”).
  - If (self.from\_date and getdate(self.from\_date) &lt; getdate()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → getdate(self.from\_date) &lt; getdate().
    - Set allowed\_role from Platform.db.get\_single\_value(“HR Settings”, “role\_allowed\_to\_create\_backdated\_leave\_application”).
    - Set user from Platform.get\_doc(“User”, Platform.session.user).
    - Set user\_roles from list of d.role for d drawn from user.roles.
      - Draw d from user.roles.
    - If not allowed\_role.
      - Call the validation error handler Platform.throw(translated “Backdated Leave Application is restricted. Please set the {} in {}”.format(Platform.bold(translated “Role Allowed to Create Backdated Leave Application”), get\_link\_to\_form(“HR Se ….
    - If (allowed\_role and allowed\_role does not belong to user\_roles).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_role → allowed\_role does not belong to user\_roles.
      - Call the validation error handler Platform.throw(translated “Only users with the {0} role can create backdated leave applications”.format(translated allowed\_role)).
- If (self.from\_date and self.to\_date and getdate(self.to\_date) &lt; getdate(self.from\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date → getdate(self.to\_date) &lt; getdate(self.from\_date).
  - Call the validation error handler Platform.throw(translated “To date cannot be before from date”).
- If (self.half\_day and self.half\_day\_date and (getdate(self.half\_day\_date) &lt; getdate(self.from\_date) or getdate(self.half\_day\_date) &gt; getdate(self.to\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.half\_day → self.half\_day\_date → (getdate(self.half\_day\_date) &lt; getdate(self.from\_date) or getdate(self.half\_day\_date) &gt; getdate(self.to\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(self.half\_day\_date) &lt; getdate(self.from\_date) → getdate(self.half\_day\_date) &gt; getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “Half Day Date should be between From Date and To Date”).
- If not is\_lwp(self.leave\_type).
  - Evaluate self.validate\_dates\_across\_allocation().
  - Evaluate self.validate\_back\_dated\_application().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates across allocation](operations-026.md#op-efea7739e1ea3e), [validate back dated application](operations-026.md#op-829ee6f8253cd6).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “restrict\_backdated\_leave\_application”), Platform.db.get\_single\_value(“HR Settings”, “role\_allowed\_to\_create\_backdated\_leave\_application”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L57) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1195) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1174)

<a id="op-efea7739e1ea3e"></a>
### Leave Application.validate dates across allocation

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_dates_across_allocation`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Application period cannot be outside leave allocation period” · validation helper with LeaveAcrossAllocationsError — translated “Application period cannot be across two allocation records”.

**Local steps**

- If Platform.db.get\_value(“Leave Type”, self.leave\_type, “allow\_negative”).
  - Return no value.
- Set tuple(alloc\_on\_from\_date, alloc\_on\_to\_date) from self.get\_allocation\_based\_on\_application\_dates().
- If not (alloc\_on\_from\_date or alloc\_on\_to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in alloc\_on\_from\_date → alloc\_on\_to\_date.
  - Call the validation error handler Platform.throw(translated “Application period cannot be outside leave allocation period”).
- Otherwise.
  - If self.is\_separate\_ledger\_entry\_required(alloc\_on\_from\_date, alloc\_on\_to\_date).
    - Call the validation error handler Platform.throw(translated “Application period cannot be across two allocation records”, exc = LeaveAcrossAllocationsError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allocation based on application dates](operations-026.md#op-d747b7e6f6cf20), [is separate ledger entry required](operations-027.md#op-1005659e3fab23).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L6406) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1196) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1175)

<a id="op-d747b7e6f6cf20"></a>
### Leave Application.get allocation based on application dates

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_allocation_based_on_application_dates`

**Inputs** self.

**Declared result** tuple at tuple(dict, dict).

**Explicit results** tuple(allocation\_based\_on\_from\_date, allocation\_based\_on\_to\_date).

**Local steps**

- Bind local operation \_get\_leave\_allocation\_record for subsequent calls.
- Set allocation\_based\_on\_from\_date from \_get\_leave\_allocation\_record(self.from\_date).
- Set allocation\_based\_on\_to\_date from \_get\_leave\_allocation\_record(self.to\_date).
- Return tuple(allocation\_based\_on\_from\_date, allocation\_based\_on\_to\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1165) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1144)

<a id="op-6c80365c07b2ff"></a>
### Leave Application.get allocation based on application dates.get leave allocation record

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_allocation_based_on_application_dates_get_leave_allocation_record`

**Inputs** date.

**Explicit results** (allocation and allocation at 0).

**Local steps**

- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.name, LeaveAllocation.from\_date, LeaveAllocation.to\_date).where((((nested operand in the contract equals nested operand ….
- Return (allocation and allocation at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocation → allocation at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L439) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1166) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1145)

<a id="op-829ee6f8253cd6"></a>
### Leave Application.validate back dated application

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_back_dated_application`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Leave cannot be applied/cancelled before {0}, as leave balance has already been carry-forwarded in the futur …”.format(formatdate(future\_allocation at 0.from\_date), future\_allocation at 0.name).

**Local steps**

- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set future\_allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.name, LeaveAllocation.from\_date).where(((((nested operand in the contract bitwise and nested operand in the contract) b ….
- If future\_allocation.
  - Call the validation error handler Platform.throw(translated “Leave cannot be applied/cancelled before {0}, as leave balance has already been carry-forwarded in the futur …”.format(formatdate(future\_allocation at 0.from\_date), future\_alloca ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L760) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1192) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1171)

<a id="op-2d40054236b079"></a>
### Leave Application.get leave allocation

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_leave_allocation`

**Inputs** self.

**Explicit results** leave\_allocation at 0 when leave\_allocation, otherwise no value.

**Local steps**

- Set date from (self.posting\_date or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.posting\_date → getdate().
- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set leave\_allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.to\_date).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operan ….
- Return leave\_allocation at 0 when leave\_allocation, otherwise no value.
  - Value choice on leave\_allocation — true gives leave\_allocation at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L1159) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1171) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1150)

<a id="op-4ddcfffc33cfe6"></a>
### Leave Application.update attendance

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_update_attendance`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value · read “Attendance” via exists · resolve a document from “Attendance” via get\_doc.

**State and service calls** call cancel on attendance · request delete\_doc for “Attendance”.

**Explicit results** no value.

**Local steps**

- <a id="op-4ddcfffc33cfe6-guard-2"></a>If self.status differs from “Approved”.
  - Return no value.
- Set holiday\_dates from list().
- If not Platform.db.get\_value(“Leave Type”, self.leave\_type, “include\_holiday”).
  - Set holiday\_dates from get\_holiday\_dates\_for\_employee(self.employee, self.from\_date, self.to\_date).
- For each dt in daterange(getdate(self.from\_date), getdate(self.to\_date)).
  - Set date from dt.strftime(“%Y-%m-%d”).
  - Set attendance\_name from Platform.db.exists(“Attendance”, dict(employee = self.employee, attendance\_date = date, docstatus = tuple(“!=”, 2))).
  - If date belongs to holiday\_dates.
    - If attendance\_name.
      - Set attendance from Platform.get\_doc(“Attendance”, attendance\_name).
      - Set attendance.flags.ignore\_permissions from true.
      - If attendance.docstatus equals 1.
        - Evaluate attendance.cancel().
      - Evaluate Platform.delete\_doc(“Attendance”, attendance\_name, force = 1).
    - Continue with the next iteration or loop test.
  - Evaluate self.create\_or\_update\_attendance(attendance\_name, date).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status differs from “Approved”, self.status = “Open” selects the branch that returns no value. With self.status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4ddcfffc33cfe6-guard-2)

**Methods declared on this owner** [create or update attendance](operations-026.md#op-0c781585b36fe4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L1499) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1188) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1167)

<a id="op-0c781585b36fe4"></a>
### Leave Application.create or update attendance

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_create_or_update_attendance`

**Inputs** self, attendance\_name, date.

**Record and data access** resolve a document from “Attendance” via get\_doc.

**State and service calls** call db\_set on doc · request new\_doc for “Attendance” · call insert on doc · call submit on doc.

**Local steps**

- Set status from “Half Day” when (self.half\_day\_date and getdate(date) equals getdate(self.half\_day\_date)), otherwise “On Leave”.
  - Value choice on (self.half\_day\_date and getdate(date) equals getdate(self.half\_day\_date)) — true gives “Half Day”, false gives “On Leave”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.half\_day\_date → getdate(date) equals getdate(self.half\_day\_date).
- If attendance\_name.
  - Set doc from Platform.get\_doc(“Attendance”, attendance\_name).
  - Set half\_day\_status from no value when status equals “On Leave”, otherwise “Present”.
    - Value choice on status equals “On Leave” — true gives no value, false gives “Present”.
  - Set modify\_half\_day\_status from 1 when (doc.status equals “Absent” and status equals “Half Day”), otherwise 0.
    - Value choice on (doc.status equals “Absent” and status equals “Half Day”) — true gives 1, false gives 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.status equals “Absent” → status equals “Half Day”.
  - Evaluate doc.db\_set(mapping(“status” → status, “leave\_type” → self.leave\_type, “leave\_application” → self.name, “half\_day\_status” → half\_day\_status, …)).
- Otherwise.
  - Set doc from Platform.new\_doc(“Attendance”).
  - Set doc.employee from self.employee.
  - Set doc.employee\_name from self.employee\_name.
  - Set doc.attendance\_date from date.
  - Set doc.company from self.company.
  - Set doc.leave\_type from self.leave\_type.
  - Set doc.leave\_application from self.name.
  - Set doc.status from status.
  - Set doc.half\_day\_status from “Present” when status equals “Half Day”, otherwise no value.
    - Value choice on status equals “Half Day” — true gives “Present”, false gives no value.
  - Set doc.modify\_half\_day\_status from 1 when status equals “Half Day”, otherwise 0.
    - Value choice on status equals “Half Day” — true gives 1, false gives 0.
  - Set doc.flags.ignore\_validate from true.
  - Evaluate doc.insert(ignore\_permissions = true).
  - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L2078) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1163) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1142)

<a id="op-00041a085876dc"></a>
### Leave Application.cancel attendance

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_cancel_attendance`

**Inputs** self.

**State and service calls** request set\_value on “Attendance”.

**Local steps**

- If self.docstatus equals 2.
  - Set Attendance from Platform.qb.DocType(“Attendance”).
  - Set attendance from nested operand in the contract(nested operand in the contract).select(Attendance.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contra ….
  - For each name in attendance.
    - Evaluate Platform.db.set\_value(“Attendance”, name, “docstatus”, 2).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L2786) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1160) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1139)

<a id="op-850313d4c3bfab"></a>
### Leave Application.validate salary processed days

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_salary_processed_days`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Salary already processed for period between {0} and {1}, Leave application period cannot be between this dat …”.format(formatdate(last\_processed\_pay\_slip at 0 at 0), formatdate(last\_processed\_p ….

**Local steps**

- If not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_lwp”).
  - Return no value.
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Set last\_processed\_pay\_slip from nested operand in the contract(nested operand in the contract).orderby(SalarySlip.creation, order = Order.desc).limit(1).run().
- If last\_processed\_pay\_slip.
  - Call the validation error handler Platform.throw(translated “Salary already processed for period between {0} and {1}, Leave application period cannot be between this dat …”.format(formatdate(last\_processed\_pay\_slip at 0 at 0), formatdate(l ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L3158) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1203) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1181)

<a id="op-f49b4a7f22ea52"></a>
### Leave Application.show block day warning

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_show_block_day_warning`

**Inputs** self.

**State and service calls** msgprint with (translated “Warning: Leave application contains following block dates” + “:”) · msgprint with ((formatdate(d.block\_date) + “: ”) + d.reason).

**Local steps**

- Set block\_dates from get\_applicable\_block\_dates(self.from\_date, self.to\_date, self.employee, self.company, all\_lists = true, leave\_type = self.leave\_type).
- If block\_dates.
  - Evaluate Platform.msgprint((translated “Warning: Leave application contains following block dates” + “:”)).
  - For each d in block\_dates.
    - Evaluate Platform.msgprint(((formatdate(d.block\_date) + “: ”) + d.reason)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L3706) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1185) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1164)

<a id="op-9755303aea9580"></a>
### Leave Application.validate block days

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_block_days`

**Inputs** self.

**Explicit failure paths** validation helper with LeaveDayBlockedError — translated “You are not authorized to approve leaves on Block Dates”.

**Local steps**

- Set block\_dates from get\_applicable\_block\_dates(self.from\_date, self.to\_date, self.employee, self.company, leave\_type = self.leave\_type).
- If (block\_dates and self.status equals “Approved”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in block\_dates → self.status equals “Approved”.
  - Call the validation error handler Platform.throw(translated “You are not authorized to approve leaves on Block Dates”, LeaveDayBlockedError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L3950) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1194) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1173)

<a id="op-9e153ccdb44db9"></a>
### Leave Application.validate balance leaves

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_balance_leaves`

**Inputs** self.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “The day(s) on which you are applying for leave are holidays. You need not apply for leave.”.

**Local steps**

- Set precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 2.
- Set leave\_application from no value when self.is\_new(), otherwise self.name.
  - Value choice on self.is\_new() — true gives no value, false gives self.name.
- If (self.from\_date and self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date.
  - Set self.total\_leave\_days from get\_number\_of\_leave\_days(self.employee, self.leave\_type, self.from\_date, self.to\_date, leave\_application = leave\_application, …).
  - <a id="op-9e153ccdb44db9-guard-16"></a>If self.total\_leave\_days ≤ 0.
    - Call the validation error handler Platform.throw(translated “The day(s) on which you are applying for leave are holidays. You need not apply for leave.”).
  - If not is\_lwp(self.leave\_type).
    - Set leave\_balance from get\_leave\_balance\_on(self.employee, self.leave\_type, self.from\_date, self.to\_date, consider\_all\_leaves\_in\_the\_allocation\_period = true, for\_consumption = true, leave\_application = leave\_application).
    - Set leave\_balance\_for\_consumption from flt(leave\_balance.get(“leave\_balance\_for\_consumption”), precision).
    - If (self.status differs from “Rejected” and (leave\_balance\_for\_consumption &lt; self.total\_leave\_days or not leave\_balance\_for\_consumption)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status differs from “Rejected” → (leave\_balance\_for\_consumption &lt; self.total\_leave\_days or not leave\_balance\_for\_consumption).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in leave\_balance\_for\_consumption &lt; self.total\_leave\_days → not leave\_balance\_for\_consumption.
      - Evaluate self.show\_insufficient\_balance\_message(leave\_balance\_for\_consumption).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.total\_leave\_days ≤ 0, self.total\_leave\_days = 0 selects the branch that calls the validation-error handler with translated “The day(s) on which you are applying for leave are holidays. You need not apply for leave.”. With self.total\_leave\_days = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9e153ccdb44db9-guard-16)

**Methods declared on this owner** [show insufficient balance message](operations-026.md#op-9f3cd98117ae55).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L56) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1193) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1172)

<a id="op-9f3cd98117ae55"></a>
### Leave Application.show insufficient balance message

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_show_insufficient_balance_message`

**Inputs** self, leave\_balance\_for\_consumption.

**Declared result** no value.

**Record and data access** read “Leave Type” via get\_value.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper with InsufficientLeaveBalanceError — translated “Insufficient leave balance for Leave Type {0}”.format(Platform.bold(self.leave\_type)).

**Local steps**

- Set tuple(alloc\_on\_from\_date, alloc\_on\_to\_date) from self.get\_allocation\_based\_on\_application\_dates().
- If Platform.db.get\_value(“Leave Type”, self.leave\_type, “allow\_negative”).
  - If leave\_balance\_for\_consumption differs from self.leave\_balance.
    - Set msg from translated “Warning: Insufficient leave balance for Leave Type {0} in this allocation.”.format(Platform.bold(self.leave\_type)).
    - Update msg using + text in the contract.
    - Update msg using + translated “Actual balances aren't available because the leave application spans over different leave allocations. You c …”.
  - Otherwise.
    - Set msg from translated “Warning: Insufficient leave balance for Leave Type {0}.”.format(Platform.bold(self.leave\_type)).
  - Evaluate Platform.msgprint(msg, title = translated “Warning”, indicator = “orange”).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Insufficient leave balance for Leave Type {0}”.format(Platform.bold(self.leave\_type)), exc = InsufficientLeaveBalanceError, title = translated “Insufficient Balance”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allocation based on application dates](operations-026.md#op-d747b7e6f6cf20).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L4645) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1186) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1165)

<a id="op-b466c63a4e6f98"></a>
### Leave Application.validate leave overlap

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_leave_overlap`

**Inputs** self.

**Local steps**

- If not self.name.
  - Set self.name from “New Leave Application”.
- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set overlapping\_applications from nested operand in the contract(nested operand in the contract).select(LeaveApplication.name, LeaveApplication.leave\_type, LeaveApplication.posting\_date, LeaveApplication.from\_date, …).where(((((nested oper ….
- For each d in overlapping\_applications.
  - If (cint(self.half\_day) equals 1 and cint(d.half\_day) equals 1 and getdate(self.half\_day\_date) equals getdate(d.half\_day\_date) and (flt(self.total\_leave\_days) equals 0.5 or getdate(self.from\_date) equals getd ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.half\_day) equals 1 → cint(d.half\_day) equals 1 → getdate(self.half\_day\_date) equals getdate(d.half\_day\_date) → (flt(self.total\_leave\_days) equals 0.5 or getdate(self.from\_date) equals getdate(d.to\_date) or getdate(self.to\_date) equals getdate(d.from\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.total\_leave\_days) equals 0.5 → getdate(self.from\_date) equals getdate(d.to\_date) → getdate(self.to\_date) equals getdate(d.from\_date).
    - Set total\_leaves\_on\_half\_day from self.get\_total\_leaves\_on\_half\_day().
    - If total\_leaves\_on\_half\_day ≥ 1.
      - Evaluate self.throw\_overlap\_error(d).
  - Otherwise.
    - Evaluate self.throw\_overlap\_error(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get total leaves on half day](operations-026.md#op-fe5d924df85937), [throw overlap error](operations-026.md#op-a09991329f157d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L5135) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1200) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1178)

<a id="op-a09991329f157d"></a>
### Leave Application.throw overlap error

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_throw_overlap_error`

**Inputs** self, d.

**Explicit failure paths** validation helper with OverlapError — msg.

**Local steps**

- Set form\_link from get\_link\_to\_form(“Leave Application”, d.name).
- Set msg from translated “Employee {0} has already applied for {1} between {2} and {3} : {4}”.format(self.employee, d at “leave\_type”, formatdate(d at “from\_date”), formatdate(d at “to\_date”), …).
- Call the validation error handler Platform.throw(msg, OverlapError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L5942) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1187) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1166)

<a id="op-fe5d924df85937"></a>
### Leave Application.get total leaves on half day

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_total_leaves_on_half_day`

**Inputs** self.

**Explicit results** (leave\_count\_on\_half\_day\_date × 0.5).

**Local steps**

- Set LeaveApplication from Platform.qb.DocType(“Leave Application”).
- Set leave\_count\_on\_half\_day\_date from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract differs from nes … at 0.
- Return (leave\_count\_on\_half\_day\_date × 0.5).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L6174) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1172) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1151)

<a id="op-406eabee0a5c29"></a>
### Leave Application.validate max days

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate_maximum_days`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set max\_days from Platform.db.get\_value(“Leave Type”, self.leave\_type, “max\_continuous\_days\_allowed”).
- If not max\_days.
  - Return no value.
- Set details from self.get\_consecutive\_leave\_details().
- If details.total\_consecutive\_leaves &gt; cint(max\_days).
  - Set msg from translated “Leave of type {0} cannot be longer than {1}.”.format(get\_link\_to\_form(“Leave Type”, self.leave\_type), max\_days).
  - If details.leave\_applications.
    - Update msg using + (text in the contract + translated “Reference: {0}”.format(“, ”.join(generator of get\_link\_to\_form(“Leave Application”, name) for name drawn from details.leave\_applications))).
      - Draw name from details.leave\_applications.
  - Call the validation error handler Platform.throw(msg, title = translated “Maximum Consecutive Leaves Exceeded”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get consecutive leave details](operations-027.md#op-490fe2cfcfc3dd).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0050.json#L6531) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1201) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1179)
