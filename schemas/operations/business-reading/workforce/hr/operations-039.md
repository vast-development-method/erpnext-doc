# Employment and attendance · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Shift request

[Record definition](../../../../data/record-types/shift_request.json)

<a id="op-5be0ec485831cf"></a>
### Shift Request.on discard

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L4812) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1492) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L106)

<a id="op-3a4f76decc3048"></a>
### Shift Request.validate default shift

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_validate_default_shift`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “You can not request for your Default Shift: {0}”.format(Platform.bold(self.shift\_type)).

**Local steps**

- Set default\_shift from Platform.get\_value(“Employee”, self.employee, “default\_shift”).
- If self.shift\_type equals default\_shift.
  - Call the validation error handler Platform.throw(translated “You can not request for your Default Shift: {0}”.format(Platform.bold(self.shift\_type))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L4875) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1499) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L113)

<a id="op-7b56e958538c0f"></a>
### Shift Request.validate approver

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_validate_approver`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Only Approvers can Approve this Request.”.

**Local steps**

- Set department from Platform.get\_value(“Employee”, self.employee, “department”).
- Set shift\_approver from Platform.get\_value(“Employee”, self.employee, “shift\_request\_approver”).
- Set dept\_approver from Platform.qb.DocType(“Department Approver”).
- Set approvers from nested operand in the contract(nested operand in the contract).select(dept\_approver.approver).where((dept\_approver.parent equals department bitwise and dept\_approver.parentfield equals “shift\_request\_appro ….
- Set approvers from list of approver at 0 for approver drawn from approvers.
  - Draw approver from approvers.
- Evaluate approvers.append(shift\_approver).
- If self.approver does not belong to approvers.
  - Call the validation error handler Platform.throw(translated “Only Approvers can Approve this Request.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L5058) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1498) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L112)

<a id="op-d5fb396928bea0"></a>
### Shift Request.validate overlapping shift requests

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_validate_overlapping_shift_remote_requests`

**Inputs** self.

**Local steps**

- Set overlapping\_dates from self.get\_overlapping\_dates().
- If len(overlapping\_dates).
  - For each d in overlapping\_dates.
    - If has\_overlapping\_timings(self.shift\_type, d.shift\_type).
      - Evaluate self.throw\_overlap\_error(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overlapping dates](operations-039.md#op-633fb1ed84729f), [throw overlap error](operations-039.md#op-8dc2db2c99eefc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L5478) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1500) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L114)

<a id="op-633fb1ed84729f"></a>
### Shift Request.get overlapping dates

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_get_overlapping_dates`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If not self.name.
  - Set self.name from “New Shift Request”.
- Set shift from Platform.qb.DocType(“Shift Request”).
- Set query from nested operand in the contract.qb.from\_(shift).select(shift.name, shift.shift\_type).where(((((nested operand in the contract.employee equals nested operand in the contract.employee bitwise and nested opera ….
- If self.to\_date.
  - Set query from query.where(shift.from\_date ≤ self.to\_date).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L64) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1490) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L104)

<a id="op-8dc2db2c99eefc"></a>
### Shift Request.throw overlap error

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_throw_overlap_error`

**Inputs** self, shift\_details.

**Explicit failure paths** validation helper with OverlappingShiftRequestError — msg.

**Local steps**

- Set shift\_details from Platform.\_dict(shift\_details).
- Set msg from translated “Employee {0} has already applied for Shift {1}: {2} that overlaps within this period”.format(Platform.bold(self.employee), Platform.bold(shift\_details.shift\_type), get\_link\_to\_form(“Shift Reque ….
- Call the validation error handler Platform.throw(msg, title = translated “Overlapping Shift Requests”, exc = OverlappingShiftRequestError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L6039) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1496) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L110)

<a id="op-25647e19ed77af"></a>
### Get data

`operation_workforce_human_resources_record_definitions_shift_request_shift_request_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “shift\_request”, “transactions” → list(mapping(“items” → list(“Shift Assignment”)))).

**Local steps**

- Return mapping(“fieldname” → “shift\_request”, “transactions” → list(mapping(“items” → list(“Shift Assignment”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L6445) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1502) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L115)

## Record · Shift schedule

[Record definition](../../../../data/record-types/shift_schedule.json)

<a id="op-1822b5a39048a0"></a>
### Shift Schedule.before validate

`operation_workforce_human_resources_record_definitions_shift_schedule_business_behavior_shift_schedule_before_validate`

**Inputs** self.

**Local steps**

- Set to\_be\_deleted from list().
- Set seen\_days from set().
- For each d in self.repeat\_on\_days.
  - If d.day belongs to seen\_days.
    - Evaluate to\_be\_deleted.append(d).
  - Otherwise.
    - Evaluate seen\_days.add(d.day).
- For each d in to\_be\_deleted.
  - Evaluate self.remove(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L4045) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1522) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L135)

<a id="op-e58a3943e69196"></a>
### Get or insert shift schedule

`operation_workforce_human_resources_record_definitions_shift_schedule_business_behavior_get_or_insert_shift_schedule`

**Inputs** shift\_type, frequency, repeat\_on\_days.

**Declared result** str.

**Record and data access** read “Shift Schedule” via get\_all · resolve a document from “Shift Schedule” via get\_doc · resolve a document from mapping(“doctype” → “Shift Schedule”, “name” → random\_string(10), “shift\_type” → shift\_type, “frequency” → frequency, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Shift Schedule”, “name” → random\_string(10), “shift\_type” → shift\_type, “frequency” → frequency, …)) · call submit on doc.

**Explicit results** shift\_schedule.name · doc.name.

**Local steps**

- Set shift\_schedules from Platform.get\_all(“Shift Schedule”, pluck = “name”, filters = mapping(“shift\_type” → shift\_type, “frequency” → frequency, “docstatus” → 1)).
- For each shift\_schedule in shift\_schedules.
  - Set shift\_schedule from Platform.get\_doc(“Shift Schedule”, shift\_schedule).
  - Set shift\_schedule\_days from list of d.day for d drawn from shift\_schedule.repeat\_on\_days.
    - Draw d from shift\_schedule.repeat\_on\_days.
  - If sorted(repeat\_on\_days) equals sorted(shift\_schedule\_days).
    - Return shift\_schedule.name.
- Set doc from Platform.get\_doc(mapping(“doctype” → “Shift Schedule”, “name” → random\_string(10), “shift\_type” → shift\_type, “frequency” → frequency, …)).insert().
  - Draw day from repeat\_on\_days.
- Evaluate doc.submit().
- Return doc.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L4243) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1521) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L134)

## Record · Shift schedule assignment

[Record definition](../../../../data/record-types/shift_schedule_assignment.json)

<a id="op-d82d528e58f97f"></a>
### Shift Schedule Assignment.validate

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_shift_schedule_assignment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_existing\_shift\_assignments().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate existing shift assignments](operations-039.md#op-bbbff694d472c3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L4780) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1517) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L130)

<a id="op-bbbff694d472c3"></a>
### Shift Schedule Assignment.validate existing shift assignments

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_shift_schedule_assignment_validate_existing_shift_assignments`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- If (self.has\_value\_changed(“create\_shifts\_after”) and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“create\_shifts\_after”) → not self.is\_new().
  - Set tuple(existing\_shift\_assignments, last\_shift\_end\_date) from self.get\_existing\_shift\_assignments().
  - If existing\_shift\_assignments.
    - Call the validation error handler Platform.throw(msg = translated “Shift assignments for {0} after {1} are already created. Please change {2} date to a date later than {3} {4}”.format(Platform.bold(self.shift\_schedule), Platform.bold(self. ….
      - Draw shift from existing\_shift\_assignments.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing shift assignments](operations-039.md#op-339a8c35f9a9ac).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L4831) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1518) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L131)

<a id="op-339a8c35f9a9ac"></a>
### Shift Schedule Assignment.get existing shift assignments

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_shift_schedule_assignment_get_existing_shift_assignments`

**Inputs** self.

**Explicit results** tuple(existing\_shift\_assignments, last\_shift\_end\_date).

**Local steps**

- Set shift\_schedule\_assignment from Platform.qb.DocType(“Shift Schedule Assignment”).
- Set shift\_assignment from Platform.qb.DocType(“Shift Assignment”).
- Set query from nested operand in the contract(nested operand in the contract).select(shift\_assignment.name, shift\_assignment.end\_date).where(((nested operand in the contract.end\_date ≥ nested operand in the contract.crea ….
- Set existing\_shifts from query.run(as\_dict = true).
- Set existing\_shift\_assignments from list of shift.name for shift drawn from existing\_shifts.
  - Draw shift from existing\_shifts.
- Set last\_shift\_end\_date from existing\_shifts at negative 1.end\_date when existing\_shifts, otherwise no value.
  - Value choice on existing\_shifts — true gives existing\_shifts at negative 1.end\_date, false gives no value.
- Return tuple(existing\_shift\_assignments, last\_shift\_end\_date).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L5214) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1516) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L129)

<a id="op-ec79bddd154657"></a>
### Shift Schedule Assignment.create shifts

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_shift_schedule_assignment_create_shifts`

**Inputs** self, start\_date, end\_date = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Shift Schedule” via get\_doc.

**Local steps**

- Set shift\_schedule from Platform.get\_doc(“Shift Schedule”, self.shift\_schedule).
- Set gap from mapping(“Every Week” → 0, “Every 2 Weeks” → 1, “Every 3 Weeks” → 2, “Every 4 Weeks” → 3) at shift\_schedule.frequency.
- Set date from start\_date.
- Set individual\_assignment\_start from no value.
- Set week\_end\_day from get\_weekday(getdate(add\_days(start\_date, negative 1))).
- Set repeat\_on\_days from list of day.day for day drawn from shift\_schedule.repeat\_on\_days.
  - Draw day from shift\_schedule.repeat\_on\_days.
- If not end\_date.
  - Set end\_date from add\_days(start\_date, 90).
- While date ≤ end\_date.
  - Set weekday from get\_weekday(getdate(date)).
  - If weekday belongs to repeat\_on\_days.
    - If not individual\_assignment\_start.
      - Set individual\_assignment\_start from date.
    - If date equals end\_date.
      - Evaluate self.create\_individual\_assignment(shift\_schedule.shift\_type, individual\_assignment\_start, date).
      - Set individual\_assignment\_start from no value.
  - Otherwise.
    - If individual\_assignment\_start.
      - Evaluate self.create\_individual\_assignment(shift\_schedule.shift\_type, individual\_assignment\_start, add\_days(date, negative 1)).
      - Set individual\_assignment\_start from no value.
  - If (weekday equals week\_end\_day and gap).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in weekday equals week\_end\_day → gap.
    - If individual\_assignment\_start.
      - Evaluate self.create\_individual\_assignment(shift\_schedule.shift\_type, individual\_assignment\_start, date).
      - Set individual\_assignment\_start from no value.
    - Set date from add\_days(date, (7 × gap)).
  - Set date from add\_days(date, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create individual assignment](operations-039.md#op-2ba3537f322ec0).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L66) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1515) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L128)

<a id="op-2ba3537f322ec0"></a>
### Shift Schedule Assignment.create individual assignment

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_shift_schedule_assignment_create_individual_assignment`

**Inputs** self, shift\_type, start\_date, end\_date.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate create\_shift\_assignment(self.employee, self.company, shift\_type, start\_date, …).
- Evaluate self.db\_set(“create\_shifts\_after”, end\_date, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L6426) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1514) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L127)

<a id="op-55733454326339"></a>
### Process auto shift creation

`operation_workforce_human_resources_record_definitions_shift_schedule_assignment_business_behavior_process_auto_shift_creation`

**Inputs** no declared parameters.

**Record and data access** read “Shift Schedule Assignment” via get\_all · resolve a document from “Shift Schedule Assignment” via get\_doc.

**Local steps**

- Set shift\_schedule\_assignments from Platform.get\_all(“Shift Schedule Assignment”, filters = mapping(“enabled” → 1, “create\_shifts\_after” → list(“&lt;=”, nowdate())), pluck = “name”).
- For each d in shift\_schedule\_assignments.
  - Attempt the following.
    - Set doc from Platform.get\_doc(“Shift Schedule Assignment”, d).
    - Set start\_date from doc.create\_shifts\_after.
    - Evaluate doc.create\_shifts(add\_days(doc.create\_shifts\_after, 1)).
    - Set text from translated “Shift Assignments created for the schedule between {0} and {1} via background job”.format(Platform.bold(format\_date(start\_date)), Platform.bold(format\_date(doc.create\_shifts\_after))).
    - Evaluate doc.add\_comment(comment\_type = “Info”, text = text).
  - On failure (Exception) bound to e.
    - Evaluate Platform.log\_error(e).
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../workforce-decision-contracts/part-0071.json#L6592) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1513) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L126)

## Record · Shift type

[Record definition](../../../../data/record-types/shift_type.json)

<a id="op-30d59120ecccc0"></a>
### Shift Type.validate

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_validate`

**Inputs** self.

**Local steps**

- Set start from get\_time(self.start\_time).
- Set end from get\_time(self.end\_time).
- Evaluate self.validate\_same\_start\_and\_end(start, end).
- Evaluate self.validate\_circular\_shift(start, end).
- Evaluate self.validate\_unlinked\_logs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate same start and end](operations-039.md#op-af65aca492294c), [validate circular shift](operations-039.md#op-bf334de191c6c9), [validate unlinked logs](operations-039.md#op-bd72b2a233e3fd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L71) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1545) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L158)

<a id="op-af65aca492294c"></a>
### Shift Type.validate same start and end

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_validate_same_start_and_end`

**Inputs** self, start\_time, end\_time.

**Explicit failure paths** validation helper.

**Local steps**

- If start\_time equals end\_time.
  - Call the validation error handler Platform.throw(title = translated “Invalid Shift Times”, msg = translated “Start time and end time cannot be same.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L887) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1548) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L160)

<a id="op-bf334de191c6c9"></a>
### Shift Type.validate circular shift

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_validate_circular_shift`

**Inputs** self, start\_time, end\_time.

**Explicit failure paths** validation helper.

**Local steps**

- Set tuple(shift\_start, shift\_end) from self.get\_shift\_start\_and\_shift\_end(start\_time, end\_time).
- If self.get\_total\_shift\_duration\_in\_minutes(shift\_start, shift\_end) ≥ 1440.
  - Set max\_label from self.get\_max\_shift\_buffer\_label().
  - Call the validation error handler Platform.throw(title = translated “Invalid Shift Times”, msg = translated “Please reduce {0} to avoid shift time overlapping with itself”.format(Platform.bold(max\_label))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get shift start and shift end](operations-039.md#op-3472ddb7b9198e), [get total shift duration in minutes](operations-039.md#op-3a6a3c1f972c52), [get max shift buffer label](operations-039.md#op-c8b77ca91d3803).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L1032) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1547) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L159)

<a id="op-3472ddb7b9198e"></a>
### Shift Type.get shift start and shift end

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_shift_start_and_shift_end`

**Inputs** self, start\_time, end\_time.

**Declared result** tuple at datetime.

**Explicit results** tuple(shift\_start, shift\_end).

**Local steps**

- Set shift\_start from datetime.combine(getdate(), start\_time).
- If start\_time &lt; end\_time.
  - Set shift\_end from datetime.combine(getdate(), end\_time).
- Otherwise.
  - If start\_time &gt; end\_time.
    - Set shift\_end from datetime.combine(add\_days(getdate(), 1), end\_time).
- Return tuple(shift\_start, shift\_end).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L1304) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1533) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L146)

<a id="op-3a6a3c1f972c52"></a>
### Shift Type.get total shift duration in minutes

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_total_shift_duration_in_minutes`

**Inputs** self, shift\_start, shift\_end.

**Declared result** int.

**Explicit results** ((round((nested operand in the contract(nested operand in the contract, nested operand in the contract).total\_seconds() ÷ 60)) + (self.allow\_check\_out\_after\_shift\_end\_time or 0)) + (self.begin\_check\_in\_bef ….

**Local steps**

- Return ((round((nested operand in the contract(nested operand in the contract, nested operand in the contract).total\_seconds() ÷ 60)) + (self.allow\_check\_out\_after\_shift\_end\_time or 0)) + (self.begin\_check\_in\_bef ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.allow\_check\_out\_after\_shift\_end\_time → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.begin\_check\_in\_before\_shift\_start\_time → 0.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L1573) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1535) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L148)

<a id="op-c8b77ca91d3803"></a>
### Shift Type.get max shift buffer label

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_get_maximum_shift_buffer_label`

**Inputs** self.

**Declared result** str.

**Explicit results** max(labels, key = labels.get).

**Local steps**

- Set labels from mapping(translated self.meta.get\_label(“allow\_check\_out\_after\_shift\_end\_time”) → self.allow\_check\_out\_after\_shift\_end\_time, translated self.meta.get\_label(“begin\_check\_in\_before\_shift\_start\_time”) → self.b ….
- Return max(labels, key = labels.get).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L1731) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1531) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L144)

<a id="op-bd72b2a233e3fd"></a>
### Shift Type.validate unlinked logs

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_validate_unlinked_logs`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- If (self.is\_field\_modified(“start\_time”) and self.unlinked\_checkins\_exist()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_field\_modified(“start\_time”) → self.unlinked\_checkins\_exist().
  - Call the validation error handler Platform.throw(title = translated “Unmarked Check-in Logs Found”, msg = translated “Mark attendance for existing check-in/out logs before changing shift settings”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is field modified](operations-039.md#op-e27a7c817817b6), [unlinked checkins exist](operations-039.md#op-ab7eaf0bf69c8e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L1918) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1549) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L161)

<a id="op-e27a7c817817b6"></a>
### Shift Type.is field modified

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_is_field_modified`

**Inputs** self, fieldname.

**Explicit results** (not self.is\_new() and self.has\_value\_changed(fieldname)).

**Local steps**

- Return (not self.is\_new() and self.has\_value\_changed(fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(fieldname).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L2278) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1537) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L150)

<a id="op-ab7eaf0bf69c8e"></a>
### Shift Type.unlinked checkins exist

`operation_workforce_human_resources_record_definitions_shift_type_business_behavior_shift_type_unlinked_checkins_exist`

**Inputs** self.

**Record and data access** read “Employee Checkin” via exists.

**Explicit results** Platform.db.exists(“Employee Checkin”, mapping(“shift” → self.name, “attendance” → list(“is”, “not set”), “skip\_auto\_attendance” → 0, “offshift” → 0)).

**Local steps**

- Return Platform.db.exists(“Employee Checkin”, mapping(“shift” → self.name, “attendance” → list(“is”, “not set”), “skip\_auto\_attendance” → 0, “offshift” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0072.json#L2364) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1544) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L157)
