# Employment and attendance · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Shift assignment

[Record definition](../../../../data/record-types/shift_assignment.json)

<a id="op-59d423813e3245"></a>
### Is shift end after assignment

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_is_shift_end_after_assignment`

**Inputs** shift\_details, assignment, is\_midnight\_shift.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If shift\_details.actual\_start.date() &gt; assignment.end\_date.
  - Return true.
- If shift\_details.actual\_end.date() &gt; assignment.end\_date.
  - If not is\_midnight\_shift.
    - Return true.
  - If (shift\_details.actual\_end.date() equals shift\_details.end\_datetime.date() and shift\_details.start\_datetime.date() equals shift\_details.end\_datetime.date()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_details.actual\_end.date() equals shift\_details.end\_datetime.date() → shift\_details.start\_datetime.date() equals shift\_details.end\_datetime.date().
    - Return true.
  - Set next\_assignment\_day from add\_days(assignment.end\_date, 1).
  - If shift\_details.actual\_end.date() differs from next\_assignment\_day.
    - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L914) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1440) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L54)

<a id="op-86bd4b8de999f6"></a>
### Is timestamp within shift

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_is_timestamp_within_shift`

**Inputs** shift\_details, for\_timestamp.

**Declared result** bool.

**Explicit results** shift\_details.actual\_start ≤ for\_timestamp ≤ shift\_details.actual\_end.

**Local steps**

- Return shift\_details.actual\_start ≤ for\_timestamp ≤ shift\_details.actual\_end.
  - Compare adjacent operands in order, stopping at the first false comparison in shift\_details.actual\_start ≤ for\_timestamp ≤ shift\_details.actual\_end.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L1281) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1443) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L57)

<a id="op-550b04dff58d2c"></a>
### Adjust overlapping shifts

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_adjust_overlapping_shifts`

**Inputs** shifts.

**Local steps**

- For each i in range((len(shifts) − 1)).
  - Set curr\_shift from shifts at i.
  - Set next\_shift from shifts at (i + 1).
  - If (curr\_shift and next\_shift).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in curr\_shift → next\_shift.
    - Set next\_shift.actual\_start from max(curr\_shift.end\_datetime, next\_shift.actual\_start).
    - Set curr\_shift.actual\_end from min(next\_shift.actual\_start, curr\_shift.actual\_end).
  - Set shifts at i from curr\_shift.
  - Set shifts at (i + 1) from next\_shift.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L1364) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1422) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L36)

<a id="op-d2a88f05444b13"></a>
### Get shifts for date

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shifts_for_date`

**Inputs** employee, for\_timestamp.

**Declared result** list at dict at tuple(str, str).

**Explicit results** nested operand in the contract(nested operand in the contract).select(assignment.name, assignment.shift\_type, assignment.start\_date, assignment.end\_date, …).where(((((nested operand in the contract bitwise ….

**Local steps**

- Set for\_date from for\_timestamp.date().
- Set prev\_day from add\_days(for\_date, negative 1).
- Set next\_day from add\_days(for\_date, 1).
- Set assignment from Platform.qb.DocType(“Shift Assignment”).
- Return nested operand in the contract(nested operand in the contract).select(assignment.name, assignment.shift\_type, assignment.start\_date, assignment.end\_date, …).where(((((nested operand in the contract bitwise ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L1645) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1437) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L51)

<a id="op-6de7146498ad85"></a>
### Get shift for timestamp

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_for_timestamp`

**Inputs** employee, for\_timestamp.

**Declared result** dict.

**Explicit results** get\_shift\_for\_time(shifts, for\_timestamp) · mapping().

**Local steps**

- Set shifts from get\_shifts\_for\_date(employee, for\_timestamp).
- If shifts.
  - Return get\_shift\_for\_time(shifts, for\_timestamp).
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L2141) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1433) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L47)

<a id="op-fef8db1a283b05"></a>
### Get employee shift

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_employee_shift`

**Inputs** employee, for\_timestamp = no value, consider\_default\_shift = false, next\_shift\_direction = no value.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** (shift\_details or mapping()).

**Local steps**

- If for\_timestamp is identical to no value.
  - Set for\_timestamp from now\_datetime().
- Set shift\_details from get\_shift\_for\_timestamp(employee, for\_timestamp).
- Set default\_shift from Platform.db.get\_value(“Employee”, employee, “default\_shift”, cache = true).
- If (not shift\_details and consider\_default\_shift).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not shift\_details → consider\_default\_shift.
  - Set shift\_details from get\_shift\_details(default\_shift, for\_timestamp).
- If (not shift\_details and next\_shift\_direction).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not shift\_details → next\_shift\_direction.
  - Set shift\_details from get\_prev\_or\_next\_shift(employee, for\_timestamp, consider\_default\_shift, default\_shift, …).
- Return (shift\_details or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in shift\_details → mapping().

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L2264) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1424) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L38)

<a id="op-afdb4e2a15cb3d"></a>
### Get prev or next shift

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_previous_or_next_shift`

**Inputs** employee, for\_timestamp, consider\_default\_shift, default\_shift, next\_shift\_direction.

**Declared result** dict.

**Record and data access** read “Shift Assignment” via get\_all.

**Explicit results** shift\_details · (shift\_details or mapping()).

**Local steps**

- Set MAX\_DAYS from 366.
- Set shift\_details from mapping().
- If (consider\_default\_shift and default\_shift).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in consider\_default\_shift → default\_shift.
  - Set direction from negative 1 when next\_shift\_direction equals “reverse”, otherwise 1.
    - Value choice on next\_shift\_direction equals “reverse” — true gives negative 1, false gives 1.
  - For each i in range(MAX\_DAYS).
    - Set date\_time from (for\_timestamp + timedelta(days = (direction × (i + 1)))).
    - Set shift\_details from get\_employee\_shift(employee, date\_time, consider\_default\_shift, no value).
    - If shift\_details.
      - Return shift\_details.
- Otherwise.
  - Set direction from “&lt;” when next\_shift\_direction equals “reverse”, otherwise “&gt;”.
    - Value choice on next\_shift\_direction equals “reverse” — true gives “&lt;”, false gives “&gt;”.
  - Set sort\_order from “desc” when next\_shift\_direction equals “reverse”, otherwise “asc”.
    - Value choice on next\_shift\_direction equals “reverse” — true gives “desc”, false gives “asc”.
  - Set shift\_dates from Platform.get\_all(“Shift Assignment”, list(“start\_date”, “end\_date”), mapping(“employee” → employee, “start\_date” → tuple(direction, for\_timestamp.date()), “docstatus” → 1, “status” → “Active”), as\_list = t ….
  - For each date\_range in shift\_dates.
    - Set tuple(start\_date, end\_date) from tuple(getdate(date\_range at 0), getdate(add\_days(date\_range at 1, 1))).
    - If reverse bound to next\_shift\_direction equals “reverse”.
      - Set end\_date from min(end\_date, for\_timestamp.date()).
    - Otherwise.
      - If next\_shift\_direction equals “forward”.
        - Set start\_date from max(start\_date, for\_timestamp.date()).
    - For each dt in generate\_date\_range(start\_date, end\_date, reverse = reverse).
      - Set shift\_details from get\_employee\_shift(employee, datetime.combine(dt, for\_timestamp.time()), consider\_default\_shift, no value).
      - If shift\_details.
        - Return shift\_details.
- Return (shift\_details or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in shift\_details → mapping().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L2634) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1428) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L42)

<a id="op-3280f29c73a5fc"></a>
### Get employee shift timings

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_employee_shift_timings`

**Inputs** employee, for\_timestamp = no value, consider\_default\_shift = false.

**Declared result** list at dict.

**Explicit results** tuple(prev\_shift, curr\_shift, next\_shift).

**Local steps**

- If for\_timestamp is identical to no value.
  - Set for\_timestamp from now\_datetime().
- Set prev\_shift, curr\_shift, next\_shift from no value.
- Set curr\_shift from get\_employee\_shift(employee, for\_timestamp, consider\_default\_shift, “forward”).
- If curr\_shift.
  - Set next\_shift from get\_employee\_shift(employee, (curr\_shift.start\_datetime + timedelta(days = 1)), consider\_default\_shift, “forward”).
- Set prev\_shift from get\_employee\_shift(employee, (curr\_shift.end\_datetime when curr\_shift, otherwise for\_timestamp + timedelta(days = negative 1)), consider\_default\_shift, “reverse”).
  - Value choice on curr\_shift — true gives curr\_shift.end\_datetime, false gives for\_timestamp.
- If curr\_shift.
  - If prev\_shift.
    - Set curr\_shift.actual\_start from prev\_shift.end\_datetime when curr\_shift.actual\_start &lt; prev\_shift.end\_datetime, otherwise curr\_shift.actual\_start.
      - Value choice on curr\_shift.actual\_start &lt; prev\_shift.end\_datetime — true gives prev\_shift.end\_datetime, false gives curr\_shift.actual\_start.
    - Set prev\_shift.actual\_end from curr\_shift.actual\_start when prev\_shift.actual\_end &gt; curr\_shift.actual\_start, otherwise prev\_shift.actual\_end.
      - Value choice on prev\_shift.actual\_end &gt; curr\_shift.actual\_start — true gives curr\_shift.actual\_start, false gives prev\_shift.actual\_end.
  - If next\_shift.
    - Set next\_shift.actual\_start from curr\_shift.end\_datetime when next\_shift.actual\_start &lt; curr\_shift.end\_datetime, otherwise next\_shift.actual\_start.
      - Value choice on next\_shift.actual\_start &lt; curr\_shift.end\_datetime — true gives curr\_shift.end\_datetime, false gives next\_shift.actual\_start.
    - Set curr\_shift.actual\_end from next\_shift.actual\_start when curr\_shift.actual\_end &gt; next\_shift.actual\_start, otherwise curr\_shift.actual\_end.
      - Value choice on curr\_shift.actual\_end &gt; next\_shift.actual\_start — true gives next\_shift.actual\_start, false gives curr\_shift.actual\_end.
- Return tuple(prev\_shift, curr\_shift, next\_shift).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L3581) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1425) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L39)

<a id="op-572cb55e11f8d4"></a>
### Get actual start end datetime of shift

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_actual_start_end_datetime_of_shift`

**Inputs** employee, for\_timestamp, consider\_default\_shift = false.

**Declared result** dict.

**Explicit results** get\_exact\_shift(shift\_timings\_as\_per\_timestamp, for\_timestamp).

**Local steps**

- Set shift\_timings\_as\_per\_timestamp from get\_employee\_shift\_timings(employee, for\_timestamp, consider\_default\_shift).
- Return get\_exact\_shift(shift\_timings\_as\_per\_timestamp, for\_timestamp).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L4203) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1423) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L37)

<a id="op-aa45cfdeb80a67"></a>
### Get exact shift

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_exact_shift`

**Inputs** shifts, for\_timestamp.

**Declared result** dict.

**Explicit results** next(generator of shift for shift drawn from shifts where (shift and for\_timestamp ≥ shift.actual\_start and for\_timestamp ≤ shift.actual\_end), mapping()).

**Local steps**

- Return next(generator of shift for shift drawn from shifts where (shift and for\_timestamp ≥ shift.actual\_start and for\_timestamp ≤ shift.actual\_end), mapping()).
  - Draw shift from shifts, keep a combination only if ((shift and for\_timestamp ≥ shift.actual\_start and for\_timestamp ≤ shift.actual\_end)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift → for\_timestamp ≥ shift.actual\_start → for\_timestamp ≤ shift.actual\_end.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L4329) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1427) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L41)

<a id="op-9aadefce52ec09"></a>
### Get shift details

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_details`

**Inputs** shift\_type\_name, for\_timestamp = no value.

**Declared result** dict.

**Explicit results** Platform.\_dict() · Platform.\_dict(mapping(“shift\_type” → shift\_type, “start\_datetime” → start\_datetime, “end\_datetime” → end\_datetime, “actual\_start” → actual\_start, …)).

**Local steps**

- If not shift\_type\_name.
  - Return Platform.\_dict().
- If for\_timestamp is identical to no value.
  - Set for\_timestamp from now\_datetime().
- Set shift\_type from get\_shift\_type(shift\_type\_name).
- Set tuple(start\_datetime, end\_datetime) from get\_shift\_timings(shift\_type, for\_timestamp).
- Set actual\_start from (start\_datetime − timedelta(minutes = shift\_type.begin\_check\_in\_before\_shift\_start\_time)).
- Set actual\_end from (end\_datetime + timedelta(minutes = shift\_type.allow\_check\_out\_after\_shift\_end\_time)).
- Set allow\_overtime from shift\_type.allow\_overtime.
- Set overtime\_type from shift\_type.overtime\_type.
- Return Platform.\_dict(mapping(“shift\_type” → shift\_type, “start\_datetime” → start\_datetime, “end\_datetime” → end\_datetime, “actual\_start” → actual\_start, …)).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L4471) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1430) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L44)

<a id="op-61f9cec6fce6f3"></a>
### Get shift type

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_type`

**Inputs** shift\_type\_name.

**Declared result** dict.

**Record and data access** read “Shift Type” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Shift Type”, shift\_type\_name, list(“name”, “start\_time”, “end\_time”, “begin\_check\_in\_before\_shift\_start\_time”, …), as\_dict = 1).

**Local steps**

- Return Platform.get\_cached\_value(“Shift Type”, shift\_type\_name, list(“name”, “start\_time”, “end\_time”, “begin\_check\_in\_before\_shift\_start\_time”, …), as\_dict = 1).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Shift Type”, shift\_type\_name, list(“name”, “start\_time”, “end\_time”, “begin\_check\_in\_before\_shift\_start\_time”, …), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L4907) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1435) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L49)

<a id="op-7c2706da20ff88"></a>
### Get shift timings

`operation_workforce_human_resources_record_definitions_shift_assignment_business_behavior_get_shift_timings`

**Inputs** shift\_type, for\_timestamp.

**Declared result** tuple.

**Explicit results** tuple(start\_datetime, end\_datetime).

**Local steps**

- Set start\_time from shift\_type.start\_time.
- Set end\_time from shift\_type.end\_time.
- Set shift\_actual\_start from get\_time(((datetime.combine(for\_timestamp, nested operand in the contract.min.time()) + start\_time) − timedelta(minutes = shift\_type.begin\_check\_in\_before\_shift\_start\_time))).
- Set shift\_actual\_end from get\_time(((datetime.combine(for\_timestamp, nested operand in the contract.min.time()) + end\_time) + timedelta(minutes = shift\_type.allow\_check\_out\_after\_shift\_end\_time))).
- Set for\_time from get\_time(for\_timestamp.time()).
- Set start\_datetime, end\_datetime from no value.
- If start\_time &gt; end\_time.
  - If for\_time ≥ shift\_actual\_start.
    - Set start\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + start\_time).
    - Update for\_timestamp using + timedelta(days = 1).
    - Set end\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + end\_time).
  - Otherwise.
    - If for\_time &lt; shift\_actual\_start.
      - Set end\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + end\_time).
      - Update for\_timestamp using + timedelta(days = negative 1).
      - Set start\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + start\_time).
- Otherwise.
  - If (shift\_actual\_start &gt; shift\_actual\_end and for\_time &lt; shift\_actual\_start and get\_time(end\_time) &gt; shift\_actual\_end).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_actual\_start &gt; shift\_actual\_end → for\_time &lt; shift\_actual\_start → get\_time(end\_time) &gt; shift\_actual\_end.
    - Update for\_timestamp using + timedelta(days = negative 1).
    - Set end\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + end\_time).
    - Set start\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + start\_time).
  - Otherwise.
    - If (shift\_actual\_start &gt; shift\_actual\_end and for\_time &gt; shift\_actual\_end and get\_time(start\_time) &lt; shift\_actual\_start).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_actual\_start &gt; shift\_actual\_end → for\_time &gt; shift\_actual\_end → get\_time(start\_time) &lt; shift\_actual\_start.
      - Update for\_timestamp using + timedelta(days = 1).
      - Set start\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + start\_time).
      - Set end\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + end\_time).
    - Otherwise.
      - Set start\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + start\_time).
      - Set end\_datetime from (datetime.combine(for\_timestamp, datetime.min.time()) + end\_time).
- Return tuple(start\_datetime, end\_datetime).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0067.json#L5055) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1434) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L48)

## Record · Shift assignment tool

[Record definition](../../../../data/record-types/shift_assignment_tool.json)

<a id="op-de972dd21f4c91"></a>
### Shift Assignment Tool.get employees

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_employees`

**Inputs** self, advanced\_filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** self.get\_shift\_requests(filters) · self.get\_employees\_for\_assigning\_shift(filters).

**Local steps**

- If not advanced\_filters.
  - Set advanced\_filters from list().
- Set quick\_filter\_fields from list(“company”, “branch”, “department”, “designation”, …).
- Set filters from list of list(d, “=”, self.get(d)) for d drawn from quick\_filter\_fields where self.get(d).
  - Draw d from quick\_filter\_fields, keep a combination only if (self.get(d)).
- Update filters using + advanced\_filters.
- If self.action equals “Process Shift Requests”.
  - Return self.get\_shift\_requests(filters).
- Return self.get\_employees\_for\_assigning\_shift(filters).

**Methods declared on this owner** [get shift requests](operations-037.md#op-b96429f712f396), [get employees for assigning shift](operations-037.md#op-8d9b67a6ecc214).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0068.json#L6200) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1472) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L86)

<a id="op-8d9b67a6ecc214"></a>
### Shift Assignment Tool.get employees for assigning shift

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_employees_for_assigning_shift`

**Inputs** self, filters.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from Platform.qb.get\_query(Employee, fields = list(Employee.employee, Employee.employee\_name, Employee.branch, Employee.department, …), filters = filters).where(((Employee.status equals “Active” bitwise and Emp ….
- If self.end\_date.
  - Set query from query.where((Employee.relieving\_date ≥ self.end\_date bitwise or Employee.relieving\_date.isnull())).
- Set self.allow\_multiple\_shifts from Platform.db.get\_single\_value(“HR Settings”, “allow\_multiple\_shift\_assignments”).
- If self.action equals “Assign Shift Schedule”.
  - Set query from query.where(Employee.employee.notin(SubQuery(self.get\_query\_for\_employees\_with\_same\_shift\_schedule()))).
- Otherwise.
  - If self.status equals “Active”.
    - Set query from query.where(Employee.employee.notin(SubQuery(self.get\_query\_for\_employees\_with\_shifts()))).
- Set query from query.where(Criterion.all(build\_qb\_match\_conditions(“Employee”))).
- Return query.run(as\_dict = true).

**Methods declared on this owner** [get query for employees with same shift schedule](operations-037.md#op-814f15bffae7d5), [get query for employees with shifts](operations-037.md#op-5ce4b02c6624b5).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “allow\_multiple\_shift\_assignments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0068.json#L6538) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1473) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L87)

<a id="op-b96429f712f396"></a>
### Shift Assignment Tool.get shift requests

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_shift_remote_requests`

**Inputs** self, filters.

**Explicit results** data.

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set ShiftRequest from Platform.qb.DocType(“Shift Request”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.employee equals nested operand in the contract.name).select(ShiftRequest.name, ShiftRequest.shift\_type, Shif ….
- If self.shift\_type\_filter.
  - Set query from query.where(ShiftRequest.shift\_type equals self.shift\_type\_filter).
- If self.approver.
  - Set query from query.where(ShiftRequest.approver equals self.approver).
- If self.from\_date.
  - Set query from query.where((ShiftRequest.to\_date ≥ self.from\_date bitwise or ShiftRequest.to\_date.isnull())).
- If self.to\_date.
  - Set query from query.where(ShiftRequest.from\_date ≤ self.to\_date).
- Set query from query.where(Criterion.all(build\_qb\_match\_conditions(“Employee”))).
- Set data from query.run(as\_dict = true).
- For each d in data.
  - Set d.employee\_name from ((d.employee + “: ”) + d.employee\_name).
  - Set d.shift\_request from get\_link\_to\_form(“Shift Request”, d.name).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1477) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L91)

<a id="op-5ce4b02c6624b5"></a>
### Shift Assignment Tool.get query for employees with shifts

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_query_for_employees_with_shifts`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set ShiftAssignment from Platform.qb.DocType(“Shift Assignment”).
- Set query from nested operand in the contract(nested operand in the contract).select(ShiftAssignment.employee).distinct().where(((ShiftAssignment.status equals “Active” bitwise and ShiftAssignment.docstatus equals 1) bit ….
- If self.end\_date.
  - Set query from query.where(ShiftAssignment.start\_date ≤ self.end\_date).
- If self.allow\_multiple\_shifts.
  - Set query from self.get\_query\_checking\_overlapping\_shift\_timings(query, ShiftAssignment, self.shift\_type).
- Return query.

**Methods declared on this owner** [get query checking overlapping shift timings](operations-037.md#op-f9451a310508b6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L799) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1476) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L90)

<a id="op-814f15bffae7d5"></a>
### Shift Assignment Tool.get query for employees with same shift schedule

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_query_for_employees_with_same_shift_schedule`

**Inputs** self.

**Record and data access** read “Assignment Rule Day” via get\_all · read “Shift Schedule” via get\_value.

**Explicit results** query.

**Local steps**

- Set days from Platform.get\_all(“Assignment Rule Day”, mapping(“parent” → self.shift\_schedule), pluck = “day”).
- Set ShiftScheduleAssignment from Platform.qb.DocType(“Shift Schedule Assignment”).
- Set ShiftSchedule from Platform.qb.DocType(“Shift Schedule”).
- Set Day from Platform.qb.DocType(“Assignment Rule Day”).
- Set query from nested operand in the contract(nested operand in the contract).select(ShiftScheduleAssignment.employee).distinct().where((ShiftScheduleAssignment.enabled equals 1 bitwise and Day.day.isin(days))).
- If self.allow\_multiple\_shifts.
  - Set shift\_type from Platform.db.get\_value(“Shift Schedule”, self.shift\_schedule, “shift\_type”).
  - Set query from self.get\_query\_checking\_overlapping\_shift\_timings(query, ShiftSchedule, shift\_type).
- Return query.

**Methods declared on this owner** [get query checking overlapping shift timings](operations-037.md#op-f9451a310508b6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L1167) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1475) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L89)

<a id="op-f9451a310508b6"></a>
### Shift Assignment Tool.get query checking overlapping shift timings

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_get_query_checking_overlapping_shift_timings`

**Inputs** self, query, doctype, shift\_type.

**Record and data access** read “Shift Type” via get\_value.

**Explicit results** query.left\_join(ShiftType).on(doctype.shift\_type equals ShiftType.name).where((end\_time\_case ≥ shift\_start bitwise and ShiftType.start\_time ≤ shift\_end)).

**Local steps**

- Set tuple(shift\_start, shift\_end) from Platform.db.get\_value(“Shift Type”, shift\_type, list(“start\_time”, “end\_time”)).
- If shift\_end &lt; shift\_start.
  - Update shift\_end using + timedelta(hours = 24).
- Set ShiftType from Platform.qb.DocType(“Shift Type”).
- Set end\_time\_case from Case().when(ShiftType.end\_time &lt; ShiftType.start\_time, (ShiftType.end\_time + Interval(hours = 24))).else\_(ShiftType.end\_time).
- Return query.left\_join(ShiftType).on(doctype.shift\_type equals ShiftType.name).where((end\_time\_case ≥ shift\_start bitwise and ShiftType.start\_time ≤ shift\_end)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L1734) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1474) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L88)

<a id="op-4dda9bd45cb4c1"></a>
### Shift Assignment Tool.bulk assign

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_bulk_assign`

**Inputs** self, employees.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with self.\_bulk\_assign · msgprint with translated “Creation of {0} has been queued. It may take a few minutes.”.format(doctype).

**Explicit results** self.\_bulk\_assign(employees).

**Explicit failure paths** validation helper — translated “Invalid Action”.

**Local steps**

- If self.action equals “Assign Shift”.
  - Set mandatory\_fields from list(“shift\_type”).
  - Set doctype from “Shift Assignments”.
- Otherwise.
  - If self.action equals “Assign Shift Schedule”.
    - Set mandatory\_fields from list(“shift\_schedule”).
    - Set doctype from “Shift Schedule Assignments”.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid Action”).
- Evaluate mandatory\_fields.extend(list(“company”, “start\_date”)).
- Evaluate validate\_bulk\_tool\_fields(self, mandatory\_fields, employees, “start\_date”, …).
- If (self.action equals “Assign Shift” and len(employees) ≤ 30).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.action equals “Assign Shift” → len(employees) ≤ 30.
  - Return self.\_bulk\_assign(employees).
- Evaluate Platform.enqueue(self.\_bulk\_assign, timeout = 3000, employees = employees).
- Evaluate Platform.msgprint(translated “Creation of {0} has been queued. It may take a few minutes.”.format(doctype), alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [bulk assign](operations-037.md#op-c5a7c2078b10d0).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.\_bulk\_assign, timeout = 3000, employees = employees).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L2171) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1467) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L81)

<a id="op-c5a7c2078b10d0"></a>
### Shift Assignment Tool.bulk assign

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_bulk_assign_2`

**Inputs** self, employees.

**State and service calls** savepoint savepoint · rollback · publish realtime with event.

**Local steps**

- Set tuple(success, failure) from tuple(list(), list()).
- Set count from 0.
- Set savepoint from “before\_assignment”.
- If self.action equals “Assign Shift”.
  - Set doctype from “Shift Assignment”.
  - Set event from “completed\_bulk\_shift\_assignment”.
- Otherwise.
  - Set doctype from “Shift Schedule Assignment”.
  - Set event from “completed\_bulk\_shift\_schedule\_assignment”.
- For each d in employees.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Set assignment from self.create\_shift\_schedule\_assignment(d) when self.action equals “Assign Shift Schedule”, otherwise create\_shift\_assignment(d, self.company, self.shift\_type, self.start\_date, …).
      - Value choice on self.action equals “Assign Shift Schedule” — true gives self.create\_shift\_schedule\_assignment(d), false gives create\_shift\_assignment(d, self.company, self.shift\_type, self.start\_date, …).
    - If self.action equals “Assign Shift Schedule”.
      - Evaluate assignment.create\_shifts(self.start\_date, self.end\_date).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate Platform.log\_error(formatted text Bulk Assignment - {doctype} failed for employee {d}., reference\_doctype = doctype).
    - Evaluate failure.append(d).
  - When the protected block completes normally.
    - Evaluate success.append(mapping(“doc” → get\_link\_to\_form(doctype, assignment.name), “employee” → d)).
  - Update count using + 1.
  - Evaluate Platform.publish\_progress(((count × 100) ÷ len(employees)), title = translated “Creating {0}...”.format(doctype)).
- Evaluate Platform.clear\_messages().
- Evaluate Platform.publish\_realtime(event, message = mapping(“success” → success, “failure” → failure), doctype = “Shift Assignment Tool”, after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create shift schedule assignment](operations-037.md#op-972a2cc6afaef6).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event, message = mapping(“success” → success, “failure” → failure), doctype = “Shift Assignment Tool”, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L2709) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1468) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L82)

<a id="op-2a001b4fe0ba18"></a>
### Shift Assignment Tool.bulk process shift requests

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_bulk_process_shift_remote_requests`

**Inputs** self, shift\_requests, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with self.\_bulk\_process\_shift\_requests · msgprint with translated “Processing of Shift Requests has been queued. It may take a few minutes.”.

**Explicit results** self.\_bulk\_process\_shift\_requests(shift\_requests, status).

**Explicit failure paths** validation helper — translated “Please select at least one Shift Request to perform this action.”.

**Local steps**

- If not shift\_requests.
  - Call the validation error handler Platform.throw(translated “Please select at least one Shift Request to perform this action.”, title = translated “No Shift Requests Selected”).
- If len(shift\_requests) ≤ 30.
  - Return self.\_bulk\_process\_shift\_requests(shift\_requests, status).
- Evaluate Platform.enqueue(self.\_bulk\_process\_shift\_requests, timeout = 3000, shift\_requests = shift\_requests, status = status).
- Evaluate Platform.msgprint(translated “Processing of Shift Requests has been queued. It may take a few minutes.”, alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [bulk process shift requests](operations-037.md#op-8a3dac025388c4).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.\_bulk\_process\_shift\_requests, timeout = 3000, shift\_requests = shift\_requests, status = status).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L3548) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1469) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L83)

<a id="op-8a3dac025388c4"></a>
### Shift Assignment Tool.bulk process shift requests

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_bulk_process_shift_remote_requests_2`

**Inputs** self, shift\_requests, status.

**Record and data access** resolve a document from “Shift Request” via get\_doc.

**State and service calls** call save on shift\_request · call submit on shift\_request · publish realtime with “completed\_bulk\_shift\_request\_processing”.

**Local steps**

- Set tuple(success, failure) from tuple(list(), list()).
- Set count from 0.
- For each d in shift\_requests.
  - Attempt the following.
    - Set shift\_request from Platform.get\_doc(“Shift Request”, d at “shift\_request”).
    - Set shift\_request.status from status.
    - Evaluate shift\_request.save().
    - Evaluate shift\_request.submit().
  - On failure (Exception).
    - Evaluate Platform.log\_error(formatted text Bulk Processing - Processing failed for Shift Request {d at “shift\_request”}., reference\_doctype = “Shift Request”).
    - Evaluate failure.append(d at “employee”).
  - When the protected block completes normally.
    - Evaluate success.append(mapping(“doc” → get\_link\_to\_form(“Shift Request”, shift\_request.name), “employee” → d at “employee”)).
  - Update count using + 1.
  - Evaluate Platform.publish\_progress(((count × 100) ÷ len(shift\_requests)), title = translated “Processing Requests...”).
- Evaluate Platform.clear\_messages().
- Evaluate Platform.publish\_realtime(“completed\_bulk\_shift\_request\_processing”, message = mapping(“success” → success, “failure” → failure, “for\_processing” → true), doctype = “Shift Assignment Tool”, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_bulk\_shift\_request\_processing”, message = mapping(“success” → success, “failure” → failure, “for\_processing” → true), doctype = “Shift Assignment Tool”, after\_commit = true).

**Boundaries to resolve** stored data, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L3892) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1470) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L84)

<a id="op-972a2cc6afaef6"></a>
### Shift Assignment Tool.create shift schedule assignment

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_shift_assignment_tool_create_shift_schedule_assignment`

**Inputs** self, employee.

**Declared result** str.

**State and service calls** request new\_doc for “Shift Schedule Assignment” · call save on assignment.

**Explicit results** assignment.

**Local steps**

- Set assignment from Platform.new\_doc(“Shift Schedule Assignment”).
- Set assignment.shift\_schedule from self.shift\_schedule.
- Set assignment.employee from employee.
- Set assignment.company from self.company.
- Set assignment.shift\_status from self.status.
- Set assignment.shift\_location from self.shift\_location.
- Set assignment.enabled from 0 when self.end\_date, otherwise 1.
  - Value choice on self.end\_date — true gives 0, false gives 1.
- Set assignment.create\_shifts\_after from self.start\_date.
- Set assignment.flags.ingore\_validate from true.
- Evaluate assignment.save().
- Return assignment.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L4530) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1471) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L85)
