# Employment and attendance · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Shift assignment tool

[Record definition](../../../../data/record-types/shift_assignment_tool.json)

<a id="op-1a05ce294c177e"></a>
### Create shift assignment

`operation_workforce_human_resources_record_definitions_shift_assignment_tool_business_behavior_create_shift_assignment`

**Inputs** employee, company, shift\_type, start\_date, end\_date, status, shift\_location = no value, shift\_schedule\_assignment = no value.

**Declared result** str.

**State and service calls** request new\_doc for “Shift Assignment” · call save on assignment · call submit on assignment.

**Explicit results** assignment.

**Local steps**

- Set assignment from Platform.new\_doc(“Shift Assignment”).
- Set assignment.employee from employee.
- Set assignment.company from company.
- Set assignment.shift\_type from shift\_type.
- Set assignment.start\_date from start\_date.
- Set assignment.end\_date from end\_date.
- Set assignment.status from status.
- Set assignment.shift\_location from shift\_location.
- Set assignment.shift\_schedule\_assignment from shift\_schedule\_assignment.
- Evaluate assignment.save().
- Evaluate assignment.submit().
- Return assignment.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0069.json#L4809) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1466) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L80)

## Report · Shift attendance

<a id="op-0c3d19589f03dc"></a>
### Execute

`operation_workforce_human_resources_report_shift_attendance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart, …).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Set chart from get\_chart\_data(data).
- Set report\_summary from get\_report\_summary(data).
- Return tuple(columns, data, no value, chart, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L347) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L91) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L440)

<a id="op-416839e85522ff"></a>
### Get columns

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“fieldname” → “employee\_name”, “fieldtype” → “Data”, “label” → translated “ ….

**Local steps**

- Return list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“fieldname” → “employee\_name”, “fieldtype” → “Data”, “label” → translated “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L511) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L98) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L447)

<a id="op-baab97743e790e"></a>
### Get data

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from get\_attendance\_with\_checkins(filters).
- Set data from update\_data(data, filters).
- If filters.include\_attendance\_without\_checkins.
  - Evaluate data.extend(get\_attendance\_without\_checkins(filters)).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L2148) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L99) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L448)

<a id="op-85169d080e249d"></a>
### Get report summary

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_report_summary`

**Inputs** data.

**Explicit results** no value · list(mapping(“value” → present\_records, “indicator” → “Green”, “label” → translated “Present Records”, “datatype” → “Int”), mapping(“value” → half\_day\_records, “indicator” → “Blue”, “label” → translated “H ….

**Local steps**

- If not data.
  - Return no value.
- Set present\_records, half\_day\_records, absent\_records, late\_entries, early\_exits from 0.
- For each entry in data.
  - If entry.status equals “Present”.
    - Update present\_records using + 1.
  - Otherwise.
    - If entry.status equals “Half Day”.
      - Update half\_day\_records using + 1.
    - Otherwise.
      - Update absent\_records using + 1.
  - If entry.late\_entry.
    - Update late\_entries using + 1.
  - If entry.early\_exit.
    - Update early\_exits using + 1.
- Return list(mapping(“value” → present\_records, “indicator” → “Green”, “label” → translated “Present Records”, “datatype” → “Int”), mapping(“value” → half\_day\_records, “indicator” → “Blue”, “label” → translated “H ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L2296) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L100) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L449)

<a id="op-026781098179e7"></a>
### Get chart data

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** no value · chart.

**Local steps**

- If not data.
  - Return no value.
- Set total\_shift\_records from mapping().
- For each entry in data.
  - Evaluate total\_shift\_records.setdefault(entry.shift, 0).
  - Update total\_shift\_records at entry.shift using + 1.
- Set labels from list of translated d for d drawn from list(total\_shift\_records).
  - Draw d from list(total\_shift\_records).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Shift”, “values” → list(nested operand in the contract.values())))), “type” → “percentage”).
- Return chart.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L2927) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L97) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L446)

<a id="op-5db157513b0058"></a>
### Get attendance with checkins

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_attendance_with_checkins`

**Inputs** filters.

**Explicit results** result.

**Local steps**

- Set attendance from Platform.qb.DocType(“Attendance”).
- Set checkin from Platform.qb.DocType(“Employee Checkin”).
- Set shift\_type from Platform.qb.DocType(“Shift Type”).
- Set query from nested operand in the contract(nested operand in the contract).inner\_join(checkin).on(checkin.attendance equals attendance.name).select(checkin.shift\_start, checkin.shift\_end, checkin.shift\_actual\_start, c ….
- For each field in filters.
  - If (field equals “late\_entry” and not filters.consider\_grace\_period).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals “late\_entry” → not filters.consider\_grace\_period.
    - Set query from query.where(attendance.in\_time &gt; checkin.shift\_start).
  - Otherwise.
    - If (field equals “early\_exit” and not filters.consider\_grace\_period).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals “early\_exit” → not filters.consider\_grace\_period.
      - Set query from query.where(attendance.out\_time &lt; checkin.shift\_end).
- Set result from query.run(as\_dict = true).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L3267) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L94) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L443)

<a id="op-a0d220de210181"></a>
### Get base attendance query

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_base_attendance_query`

**Inputs** filters.

**Explicit results** query.

**Local steps**

- Set attendance from Platform.qb.DocType(“Attendance”).
- Set shift\_type from Platform.qb.DocType(“Shift Type”).
- Set query from nested operand in the contract(nested operand in the contract).select(attendance.name, attendance.employee, attendance.employee\_name, attendance.shift, …).where(attendance.docstatus equals 1).groupby(atten ….
- For each field in filters.
  - If field equals “from\_date”.
    - Set query from query.where(attendance.attendance\_date ≥ filters.from\_date).
  - Otherwise.
    - If field equals “to\_date”.
      - Set query from query.where(attendance.attendance\_date ≤ filters.to\_date).
    - Otherwise.
      - If field belongs to list(“consider\_grace\_period”, “include\_attendance\_without\_checkins”).
        - Continue with the next iteration or loop test.
      - Otherwise.
        - If field equals “employment\_type”.
          - If filters.employment\_type.
            - Set employee from Platform.qb.DocType(“Employee”).
            - Set query from query.inner\_join(employee).on(attendance.employee equals employee.name).where(employee.employment\_type equals filters.employment\_type).
        - Otherwise.
          - Set query from query.where(attendance at field equals filters at field).
- Set query from query.where(Criterion.all(build\_qb\_match\_conditions(“Attendance”))).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L84) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L96) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L445)

<a id="op-aeff768797d02a"></a>
### Get attendance without checkins

`operation_workforce_human_resources_report_shift_attendance_business_behavior_get_attendance_without_checkins`

**Inputs** filters.

**Explicit results** result.

**Local steps**

- Set attendance from Platform.qb.DocType(“Attendance”).
- Set checkin from Platform.qb.DocType(“Employee Checkin”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(checkin).on(checkin.attendance equals attendance.name).where(checkin.attendance.isnull()).
- Set result from query.run(as\_dict = true).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L4505) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L95) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L444)

<a id="op-ba69dd106d1b78"></a>
### Update data

`operation_workforce_human_resources_report_shift_attendance_business_behavior_update_data`

**Inputs** data, filters.

**Explicit results** data.

**Local steps**

- For each d in data.
  - Evaluate update\_late\_entry(d, filters.consider\_grace\_period).
  - Evaluate update\_early\_exit(d, filters.consider\_grace\_period).
  - Set d.working\_hours from format\_float\_precision(d.working\_hours).
  - Set tuple(d.in\_time, d.out\_time) from format\_in\_out\_time(d.in\_time, d.out\_time, d.attendance\_date).
  - Set tuple(d.shift\_start, d.shift\_end) from convert\_datetime\_to\_time\_for\_same\_date(d.shift\_start, d.shift\_end).
  - Set tuple(d.shift\_actual\_start, d.shift\_actual\_end) from convert\_datetime\_to\_time\_for\_same\_date(d.shift\_actual\_start, d.shift\_actual\_end).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L4765) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L101) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L450)

<a id="op-851f99c37c89c3"></a>
### Format float precision

`operation_workforce_human_resources_report_shift_attendance_business_behavior_format_decimal_precision`

**Inputs** value.

**Explicit results** flt(value, precision).

**Local steps**

- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Return flt(value, precision).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L5093) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L92) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L441)

<a id="op-13d0a74529749f"></a>
### Format in out time

`operation_workforce_human_resources_report_shift_attendance_business_behavior_format_in_out_time`

**Inputs** in\_time, out\_time, attendance\_date.

**Explicit results** tuple(in\_time, out\_time).

**Local steps**

- If (in\_time and not out\_time and in\_time.date() equals attendance\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_time → not out\_time → in\_time.date() equals attendance\_date.
  - Set in\_time from in\_time.time().
- Otherwise.
  - If (out\_time and not in\_time and out\_time.date() equals attendance\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in out\_time → not in\_time → out\_time.date() equals attendance\_date.
    - Set out\_time from out\_time.time().
  - Otherwise.
    - Set tuple(in\_time, out\_time) from convert\_datetime\_to\_time\_for\_same\_date(in\_time, out\_time).
- Return tuple(in\_time, out\_time).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L5210) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L93) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L442)

<a id="op-fe9ef96a86628c"></a>
### Convert datetime to time for same date

`operation_workforce_human_resources_report_shift_attendance_business_behavior_convert_datetime_to_time_for_same_date`

**Inputs** start, end.

**Explicit results** tuple(start, end).

**Local steps**

- If (start and end and start.date() equals end.date()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start → end → start.date() equals end.date().
  - Set start from start.time().
  - Set end from end.time().
- Otherwise.
  - Set start from format\_datetime(start).
  - Set end from format\_datetime(end).
- Return tuple(start, end).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L5464) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L90) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L439)

<a id="op-e386c434f3ab55"></a>
### Update late entry

`operation_workforce_human_resources_report_shift_attendance_business_behavior_update_late_entry`

**Inputs** entry, consider\_grace\_period.

**Local steps**

- If consider\_grace\_period.
  - If entry.late\_entry.
    - Set entry\_grace\_period from entry.late\_entry\_grace\_period when entry.enable\_late\_entry\_marking, otherwise 0.
      - Value choice on entry.enable\_late\_entry\_marking — true gives entry.late\_entry\_grace\_period, false gives 0.
    - Set start\_time from (entry.shift\_start + timedelta(minutes = entry\_grace\_period)).
    - Set entry.late\_entry\_hrs from (entry.in\_time − start\_time).
- Otherwise.
  - If (entry.in\_time and entry.in\_time &gt; entry.shift\_start).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.in\_time → entry.in\_time &gt; entry.shift\_start.
    - Set entry.late\_entry from 1.
    - Set entry.late\_entry\_hrs from (entry.in\_time − entry.shift\_start).
- If entry.late\_entry\_hrs.
  - Set entry.late\_entry\_hrs from format\_duration(entry.late\_entry\_hrs.total\_seconds()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L5679) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L103) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L452)

<a id="op-429f8eaf31e17e"></a>
### Update early exit

`operation_workforce_human_resources_report_shift_attendance_business_behavior_update_early_exit`

**Inputs** entry, consider\_grace\_period.

**Local steps**

- If consider\_grace\_period.
  - If entry.early\_exit.
    - Set exit\_grace\_period from entry.early\_exit\_grace\_period when entry.enable\_early\_exit\_marking, otherwise 0.
      - Value choice on entry.enable\_early\_exit\_marking — true gives entry.early\_exit\_grace\_period, false gives 0.
    - Set end\_time from (entry.shift\_end − timedelta(minutes = exit\_grace\_period)).
    - Set entry.early\_exit\_hrs from (end\_time − entry.out\_time).
- Otherwise.
  - If (entry.out\_time and entry.out\_time &lt; entry.shift\_end).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.out\_time → entry.out\_time &lt; entry.shift\_end.
    - Set entry.early\_exit from 1.
    - Set entry.early\_exit\_hrs from (entry.shift\_end − entry.out\_time).
- If entry.early\_exit\_hrs.
  - Set entry.early\_exit\_hrs from format\_duration(entry.early\_exit\_hrs.total\_seconds()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0093.json#L6000) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L102) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L451)

## Record · Shift location

[Record definition](../../../../data/record-types/shift_location.json)

<a id="op-07f37bd5e1a61a"></a>
### Shift Location.validate

`operation_workforce_human_resources_record_definitions_shift_location_business_behavior_shift_location_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_geolocation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set geolocation](operations-038.md#op-2237e32097eeda).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L3475) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1487) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L101)

<a id="op-2237e32097eeda"></a>
### Shift Location.set geolocation

`operation_workforce_human_resources_record_definitions_shift_location_business_behavior_shift_location_set_geolocation`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate set\_geolocation\_from\_coordinates(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L3526) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1486) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L100)

## Record · Shift request

[Record definition](../../../../data/record-types/shift_request.json)

<a id="op-a8785ec1d2b2ca"></a>
### Shift Request.validate

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_from\_to\_dates(“from\_date”, “to\_date”).
- Evaluate self.validate\_overlapping\_shift\_requests().
- Evaluate self.validate\_approver().
- Evaluate self.validate\_default\_shift().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlapping shift requests](operations-039.md#op-d5fb396928bea0), [validate approver](operations-039.md#op-7b56e958538c0f), [validate default shift](operations-039.md#op-3a4f76decc3048).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L65) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1497) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L111)

<a id="op-c064a94d8d7df0"></a>
### Shift Request.on update

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_on_update`

**Inputs** self.

**Local steps**

- Evaluate share\_doc\_with\_approver(self, self.approver).
- Evaluate self.notify\_approval\_status().
- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-038.md#op-d2314be5964347).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L3770) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1494) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L108)

<a id="op-8a456c9afd8dcf"></a>
### Shift Request.after delete

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.publish\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish update](operations-038.md#op-d2314be5964347).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L3869) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1488) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L102)

<a id="op-d2314be5964347"></a>
### Shift Request.publish update

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_publish_update`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set employee\_user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”, cache = true).
- Evaluate Workforce.refetch\_resource(“Workforce:my\_shift\_requests”, employee\_user).
- Evaluate Workforce.refetch\_resource(“Workforce:team\_shift\_requests”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L3920) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1495) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L109)

<a id="op-8e63245815d027"></a>
### Shift Request.after insert

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.notify\_approver().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L4070) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1489) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L103)

<a id="op-73a35b3b779fef"></a>
### Shift Request.on submit

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_on_submit`

**Inputs** self.

**State and service calls** request new\_doc for “Shift Assignment” · call insert on assignment\_doc · call submit on assignment\_doc · msgprint with translated “Shift Assignment: {0} created for Employee: {1}”.format(Platform.bold(assignment\_doc.name), Platform.bold(self.employee)).

**Explicit failure paths** validation helper — translated “Only Shift Request with status 'Approved' and 'Rejected' can be submitted”.

**Local steps**

- <a id="op-73a35b3b779fef-guard-2"></a>If self.status does not belong to list(“Approved”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “Only Shift Request with status 'Approved' and 'Rejected' can be submitted”).
- If self.status equals “Approved”.
  - Set assignment\_doc from Platform.new\_doc(“Shift Assignment”).
  - Set assignment\_doc.company from self.company.
  - Set assignment\_doc.shift\_type from self.shift\_type.
  - Set assignment\_doc.employee from self.employee.
  - Set assignment\_doc.start\_date from self.from\_date.
  - If self.to\_date.
    - Set assignment\_doc.end\_date from self.to\_date.
  - Set assignment\_doc.shift\_request from self.name.
  - Set assignment\_doc.flags.ignore\_permissions from 1.
  - Evaluate assignment\_doc.insert().
  - Evaluate assignment\_doc.submit().
  - Evaluate Platform.msgprint(translated “Shift Assignment: {0} created for Employee: {1}”.format(Platform.bold(assignment\_doc.name), Platform.bold(self.employee))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to list(“Approved”, “Rejected”), self.status = “Draft” selects the branch that calls the validation-error handler with translated “Only Shift Request with status 'Approved' and 'Rejected' can be submitted”. With self.status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-73a35b3b779fef-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L4119) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1493) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L107)

<a id="op-a8c77ccef575cb"></a>
### Shift Request.on cancel

`operation_workforce_human_resources_record_definitions_shift_request_business_behavior_shift_request_on_cancel`

**Inputs** self.

**Record and data access** read “Shift Assignment” via get\_all · resolve a document from “Shift Assignment” via get\_doc.

**State and service calls** call cancel on shift\_assignment\_doc.

**Local steps**

- Set shift\_assignment\_list from Platform.db.get\_all(“Shift Assignment”, mapping(“employee” → self.employee, “shift\_request” → self.name, “docstatus” → 1)).
- If shift\_assignment\_list.
  - For each shift in shift\_assignment\_list.
    - Set shift\_assignment\_doc from Platform.get\_doc(“Shift Assignment”, shift at “name”).
    - Evaluate shift\_assignment\_doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0070.json#L4587) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1491) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L105)
