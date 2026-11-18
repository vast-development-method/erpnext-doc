# Employment and attendance · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Employee attendance tool

[Record definition](../../../../data/record-types/employee_attendance_tool.json)

<a id="op-9d67e866f2b9fc"></a>
### Get unmarked attendance

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_get_unmarked_attendance`

**Inputs** employee\_list, attendance\_list.

**Declared result** list at dict.

**Explicit results** unmarked\_attendance.

**Local steps**

- Set marked\_employees from list of entry.employee for entry drawn from attendance\_list.
  - Draw entry from attendance\_list.
- Set unmarked\_attendance from list().
- For each entry in employee\_list.
  - If entry.employee does not belong to marked\_employees.
    - Evaluate unmarked\_attendance.append(entry).
- Return unmarked\_attendance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L2809) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L529) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L510)

<a id="op-fa6db27cb9ba7e"></a>
### Get unmarked attendance with shift

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_get_unmarked_attendance_with_shift`

**Inputs** unmarked\_attendance, shift, date.

**Record and data access** read “Shift Assignment” via get\_list · read “Employee” via get\_list.

**Explicit results** shiftwise\_unmarked\_attendance.

**Local steps**

- Set shift\_assigned\_employees from Platform.get\_list(“Shift Assignment”, filters = mapping(“shift\_type” → shift, “start\_date” → list(“&lt;=”, Platform.utils.getdate(date))), fields = list(“employee”)).
- Set default\_shift\_employees from Platform.get\_list(“Employee”, filters = mapping(“default\_shift” → shift), fields = list(“employee”)).
- Set all\_employees\_with\_shift from (shift\_assigned\_employees + default\_shift\_employees).
- Set distinct\_employees\_with\_shift from set of emp at “employee” for emp drawn from all\_employees\_with\_shift.
  - Draw emp from all\_employees\_with\_shift.
- Set shiftwise\_unmarked\_attendance from list().
- For each emp in unmarked\_attendance.
  - If emp at “employee” belongs to distinct\_employees\_with\_shift.
    - Evaluate shiftwise\_unmarked\_attendance.append(emp).
- Return shiftwise\_unmarked\_attendance.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0018.json#L3008) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L530) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L511)

<a id="op-a8c18c75645459"></a>
### Get permission check fields

`operation_workforce_binding_workforce_hr_doctype_employee_attendance_tool_employee_attendance_tool_get_permission_check_fields`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L54) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L105) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L105)

<a id="op-099b9308e4d9f9"></a>
### Mark employee attendance

`operation_workforce_human_resources_record_definitions_employee_attendance_tool_business_behavior_mark_employee_attendance`

**Inputs** employee\_list, status, date, leave\_type = no value, company = no value, late\_entry = no value, early\_exit = no value, shift = no value, mark\_half\_day = false, half\_day\_status = no value, half\_day\_employee\_list = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from dict(doctype = “Attendance”, employee = employee, attendance\_date = getdate(date), status = status, …) via get\_doc · read “Attendance” via get\_list · resolve a document from “Attendance” via get\_doc.

**State and service calls** call insert on attendance · call submit on attendance.

**Explicit results** no value.

**Local steps**

- If isinstance(employee\_list, str).
  - Set employee\_list from json.loads(employee\_list).
- If employee\_list.
  - Evaluate Platform.has\_permission(“Attendance”, “create”, throw = true).
  - Evaluate validate\_employee\_access(employee\_list, company).
- For each employee in employee\_list.
  - Set leave\_type from no value.
  - If (status equals “On Leave” and leave\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in status equals “On Leave” → leave\_type.
    - Set leave\_type from leave\_type.
  - Set attendance from Platform.get\_doc(dict(doctype = “Attendance”, employee = employee, attendance\_date = getdate(date), status = status, …)).
  - Evaluate attendance.insert().
  - Evaluate attendance.submit().
- If mark\_half\_day.
  - Evaluate Platform.has\_permission(“Attendance”, “write”, throw = true).
  - If isinstance(half\_day\_employee\_list, str).
    - Set half\_day\_employee\_list from json.loads(half\_day\_employee\_list).
  - Evaluate validate\_employee\_access(half\_day\_employee\_list, company).
  - Set eligible\_attendance from Platform.get\_list(“Attendance”, filters = mapping(“employee” → list(“in”, half\_day\_employee\_list), “attendance\_date” → date, “docstatus” → 1), fields = get\_permission\_check\_fields(“Attendance”), limit = 0).
  - If not eligible\_attendance.
    - Return no value.
  - For each row in eligible\_attendance.
    - Set attendance from Platform.get\_doc(doctype = “Attendance”, expanded names row).
    - Evaluate Platform.has\_permission(“Attendance”, “write”, doc = attendance, throw = true).
  - Set Attendance from Platform.qb.DocType(“Attendance”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(Attendance.early\_exit, (early\_exit or 0)).set(Attendance.modify\_half\_day\_status, 0).run().
    - Draw row from eligible\_attendance.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in late\_entry → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in early\_exit → 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Attendance”, “create”, throw = true), Platform.has\_permission(“Attendance”, “write”, throw = true) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L19) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L531) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L512)

## Report · Employee birthday

<a id="op-4d13e1e1b15140"></a>
### Execute

`operation_workforce_human_resources_report_employee_birthday_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”).

**Local steps**

- If not filters.
  - Set filters from mapping().
- If not filters at “company”.
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- Set columns from get\_columns().
- Set data from get\_employees(filters).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L3940) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1676) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L282)

<a id="op-c956aed29464cf"></a>
### Get columns

`operation_workforce_human_resources_report_employee_birthday_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Employee” + “:Link/Employee:120”), (translated “Name” + “:Data:200”), (translated “Date of Birth” + “:Date:100”), (translated “Branch” + “:Link/Branch:120”), …).

**Local steps**

- Return list((translated “Employee” + “:Link/Employee:120”), (translated “Name” + “:Data:200”), (translated “Date of Birth” + “:Date:100”), (translated “Branch” + “:Link/Branch:120”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L4166) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1677) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L283)

<a id="op-807b2620bd4190"></a>
### Get employees

`operation_workforce_human_resources_report_employee_birthday_business_behavior_get_employees`

**Inputs** filters.

**Explicit results** employees.

**Local steps**

- Set month from get\_filtered\_month(filters).
- Set employee from Platform.qb.DocType(“Employee”).
- Set employees from nested operand in the contract(nested operand in the contract).where(nested operand in the contract(nested operand in the contract, nested operand in the contract) equals month).where(Criterion.all(build\_q ….run().
- Return employees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L4428) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1678) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L284)

<a id="op-b814f65149c6aa"></a>
### Get filtered month

`operation_workforce_human_resources_report_employee_birthday_business_behavior_get_filtered_month`

**Inputs** filters.

**Explicit results** (list(“Jan”, “Feb”, “Mar”, “Apr”, …).index(filters at “month”) + 1).

**Local steps**

- Return (list(“Jan”, “Feb”, “Mar”, “Apr”, …).index(filters at “month”) + 1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0081.json#L4840) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1679) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L285)

## Record · Employee checkin

[Record definition](../../../../data/record-types/employee_checkin.json)

<a id="op-f9d73a5655e294"></a>
### Employee Checkin.before validate

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_before_validate`

**Inputs** self.

**Local steps**

- Set self.time from get\_datetime(self.time).replace(microsecond = 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L3506) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L546) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L526)

<a id="op-5df9dcba6bf36c"></a>
### Employee Checkin.validate

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_duplicate\_log().
- Evaluate self.validate\_time\_change().
- Evaluate self.fetch\_shift().
- Evaluate self.set\_geolocation().
- Evaluate self.validate\_distance\_from\_shift\_location().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate log](operations-008.md#op-75c96e08f4bc76), [validate time change](operations-008.md#op-4b6ef05ead85b3), [fetch shift](operations-008.md#op-38e07c6c59d908), [set geolocation](operations-008.md#op-152fbee8924f7e), [validate distance from shift location](operations-008.md#op-174be4e263742f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L3594) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L549) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L529)

<a id="op-75c96e08f4bc76"></a>
### Employee Checkin.validate duplicate log

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_validate_duplicate_log`

**Inputs** self.

**Record and data access** read “Employee Checkin” via exists.

**Explicit failure paths** validation helper — translated “This employee already has a log with the same timestamp.{0}”.format((text in the contract + doc\_link)).

**Local steps**

- Set doc from Platform.db.exists(“Employee Checkin”, mapping(“employee” → self.employee, “time” → self.time, “name” → tuple(“!=”, self.name), “log\_type” → self.log\_type)).
- If doc.
  - Set doc\_link from Platform.get\_desk\_link(“Employee Checkin”, doc).
  - Call the validation error handler Platform.throw(translated “This employee already has a log with the same timestamp.{0}”.format((text in the contract + doc\_link))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L3750) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L551) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L531)

<a id="op-4b6ef05ead85b3"></a>
### Employee Checkin.validate time change

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_validate_time_change`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- If (self.attendance and self.has\_value\_changed(“time”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attendance → self.has\_value\_changed(“time”).
  - Call the validation error handler Platform.throw(title = translated “Cannot Modify Time”, msg = translated “An attendance record is linked to this checkin. Please cancel the attendance before modifying time.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L4029) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L552) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L532)

<a id="op-152fbee8924f7e"></a>
### Employee Checkin.set geolocation

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_set_geolocation`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate set\_geolocation\_from\_coordinates(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L4174) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L548) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L528)

<a id="op-38e07c6c59d908"></a>
### Employee Checkin.fetch shift

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_fetch_shift`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Log Type is required for check-ins falling in the shift: {0}.”.format(shift\_actual\_timings.shift\_type.name).

**Local steps**

- If not shift\_actual\_timings bound to get\_actual\_start\_end\_datetime\_of\_shift(self.employee, get\_datetime(self.time), true).
  - Set self.shift from no value.
  - Set self.offshift from 1.
  - Return no value.
- If (shift\_actual\_timings.shift\_type.determine\_check\_in\_and\_check\_out equals “Strictly based on Log Type in Employee Checkin” and not self.log\_type and not self.skip\_auto\_attendance).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shift\_actual\_timings.shift\_type.determine\_check\_in\_and\_check\_out equals “Strictly based on Log Type in Employee Checkin” → not self.log\_type → not self.skip\_auto\_attendance.
  - Call the validation error handler Platform.throw(translated “Log Type is required for check-ins falling in the shift: {0}.”.format(shift\_actual\_timings.shift\_type.name)).
- If not self.attendance.
  - Set self.offshift from 0.
  - Set self.shift from shift\_actual\_timings.shift\_type.name.
  - Set self.shift\_actual\_start from shift\_actual\_timings.actual\_start.
  - Set self.shift\_actual\_end from shift\_actual\_timings.actual\_end.
  - Set self.shift\_start from shift\_actual\_timings.start\_datetime.
  - Set self.shift\_end from shift\_actual\_timings.end\_datetime.
  - Set self.overtime\_type from (shift\_actual\_timings.overtime\_type or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in shift\_actual\_timings.overtime\_type → no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L4244) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L547) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L527)

<a id="op-174be4e263742f"></a>
### Employee Checkin.validate distance from shift location

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_employee_checkin_validate_distance_from_shift_location`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value · read “Shift Assignment” via get\_all · read “Shift Location” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Latitude and longitude values are required for checking in.” · validation helper with CheckinRadiusExceededError — translated “You must be within {0} meters of your shift location to check in.”.format(checkin\_radius).

**Local steps**

- If not Platform.db.get\_single\_value(“HR Settings”, “allow\_geolocation\_tracking”).
  - Return no value.
- If not (self.latitude or self.longitude).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.latitude → self.longitude.
  - Call the validation error handler Platform.throw(translated “Latitude and longitude values are required for checking in.”).
- Set assignment\_locations from Platform.get\_all(“Shift Assignment”, filters = mapping(“employee” → self.employee, “shift\_type” → self.shift, “start\_date” → list(“&lt;=”, self.time), “shift\_location” → list(“is”, “set”), …), or\_filters = li ….
- If not assignment\_locations.
  - Return no value.
- Set tuple(checkin\_radius, latitude, longitude) from Platform.db.get\_value(“Shift Location”, assignment\_locations at 0, list(“checkin\_radius”, “latitude”, “longitude”)).
- If checkin\_radius ≤ 0.
  - Return no value.
- Set distance from get\_distance\_between\_coordinates(latitude, longitude, self.latitude, self.longitude).
- If distance &gt; checkin\_radius.
  - Call the validation error handler Platform.throw(translated “You must be within {0} meters of your shift location to check in.”.format(checkin\_radius), exc = CheckinRadiusExceededError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “allow\_geolocation\_tracking”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L4699) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L550) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L530)

<a id="op-6d2feee935e34c"></a>
### Add log based on employee field

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_add_log_based_on_employee_field`

**Inputs** employee\_field\_value, timestamp, device\_id = no value, log\_type = no value, skip\_auto\_attendance = 0, employee\_fieldname = “attendance\_device\_id”, latitude = no value, longitude = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** Document.

**Record and data access** read “Employee” via get\_values.

**State and service calls** request new\_doc for “Employee Checkin” · call insert on doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “'employee\_field\_value' and 'timestamp' are required.” · validation helper — translated “'employee\_fieldname' must be one of {0}.”.format(“, ”.join(allowed\_employee\_fieldnames)) · validation helper — translated “No Employee found for the given employee field value. '{}': {}”.format(employee\_fieldname, employee\_field\_value).

**Local steps**

- If (not employee\_field\_value or not timestamp).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not employee\_field\_value → not timestamp.
  - Call the validation error handler Platform.throw(translated “'employee\_field\_value' and 'timestamp' are required.”).
- Set allowed\_employee\_fieldnames from set(“name”, “employee”, “attendance\_device\_id”).
- If employee\_fieldname does not belong to allowed\_employee\_fieldnames.
  - Call the validation error handler Platform.throw(translated “'employee\_fieldname' must be one of {0}.”.format(“, ”.join(allowed\_employee\_fieldnames))).
- Set employee from Platform.db.get\_values(“Employee”, mapping(employee\_fieldname → employee\_field\_value), list(“name”, “employee\_name”, employee\_fieldname), as\_dict = true).
- If employee.
  - Set employee from employee at 0.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “No Employee found for the given employee field value. '{}': {}”.format(employee\_fieldname, employee\_field\_value)).
- Set doc from Platform.new\_doc(“Employee Checkin”).
- Set doc.employee from employee.name.
- Set doc.employee\_name from employee.employee\_name.
- Set doc.time from timestamp.
- Set doc.device\_id from device\_id.
- Set doc.log\_type from log\_type.
- Set doc.latitude from latitude.
- Set doc.longitude from longitude.
- If cint(skip\_auto\_attendance) equals 1.
  - Set doc.skip\_auto\_attendance from “1”.
- Evaluate doc.insert().
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L5376) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L541) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L521)

<a id="op-bf75d6d6baa134"></a>
### Bulk fetch shift

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_bulk_fetch_shift`

**Inputs** checkins.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Employee Checkin” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- If isinstance(checkins, str).
  - Set checkins from Platform.json.loads(checkins).
- For each d in checkins.
  - Set doc from Platform.get\_doc(“Employee Checkin”, d).
  - Evaluate doc.fetch\_shift().
  - Set doc.flags.ignore\_validate from true.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L6278) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L542) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L522)

<a id="op-a01b3cdc017ba9"></a>
### Mark attendance and link log

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_mark_attendance_and_link_log`

**Inputs** logs, attendance\_status, attendance\_date, working\_hours = no value, late\_entry = false, early\_exit = false, in\_time = no value, out\_time = no value, shift = no value, overtime\_type = no value.

**Declared result** (Document bitwise or no value).

**State and service calls** savepoint “attendance\_creation”.

**Explicit results** no value · attendance.

**Explicit failure paths** validation helper — translated “{0} is an invalid Attendance Status.”.format(attendance\_status).

**Local steps**

- Set log\_names from list of x.name for x drawn from logs.
  - Draw x from logs.
- Set employee from logs at 0.employee.
- If attendance\_status equals “Skip”.
  - Evaluate skip\_attendance\_in\_checkins(log\_names).
  - Return no value.
- If attendance\_status does not belong to tuple(“Present”, “Absent”, “Half Day”).
  - Call the validation error handler Platform.throw(translated “{0} is an invalid Attendance Status.”.format(attendance\_status)).
- Attempt the following.
  - Evaluate Platform.db.savepoint(“attendance\_creation”).
  - Set attendance from create\_or\_update\_attendance(employee = employee, attendance\_date = attendance\_date, attendance\_status = attendance\_status, working\_hours = working\_hours, …).
  - If attendance\_status equals “Absent”.
    - Evaluate attendance.add\_comment(text = translated “Employee was marked Absent for not meeting the working hours threshold.”).
  - Evaluate update\_attendance\_in\_checkins(log\_names, attendance.name).
  - Return attendance.
- On failure (Platform.ValidationError) bound to e.
  - Evaluate handle\_attendance\_exception(log\_names, e).
  - Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0019.json#L6538) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L557) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L537)

<a id="op-6b86bf3272fb22"></a>
### Create or update attendance

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_create_or_update_attendance`

**Inputs** employee, attendance\_date, attendance\_status, working\_hours = no value, shift = no value, late\_entry = false, early\_exit = false, in\_time = no value, out\_time = no value, overtime\_type = no value.

**Record and data access** resolve a document from “Attendance” via get\_doc.

**State and service calls** request set\_value on “Attendance” · request new\_doc for “Attendance” · call save on attendance · call submit on attendance.

**Explicit results** Platform.get\_doc(“Attendance”, attendance.name) · attendance.

**Local steps**

- If attendance bound to get\_existing\_half\_day\_attendance(employee, attendance\_date).
  - Evaluate Platform.db.set\_value(“Attendance”, attendance.name, mapping(“working\_hours” → working\_hours, “shift” → shift, “late\_entry” → late\_entry, “early\_exit” → early\_exit, …)).
    - Value choice on attendance\_status equals “Absent” — true gives “Absent”, false gives “Present”.
  - Return Platform.get\_doc(“Attendance”, attendance.name).
- Otherwise.
  - Set attendance from Platform.new\_doc(“Attendance”).
  - Evaluate attendance.update(mapping(“doctype” → “Attendance”, “employee” → employee, “attendance\_date” → attendance\_date, “status” → attendance\_status, …)).
  - If (overtime\_type and attendance\_status equals “Present”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in overtime\_type → attendance\_status equals “Present”.
    - Set overtime\_data from get\_overtime\_data(shift, working\_hours).
    - If overtime\_data.
      - Evaluate attendance.update(mapping(“overtime\_type” → overtime\_type, “standard\_working\_hours” → overtime\_data.get(“standard\_working\_hours”), “actual\_overtime\_duration” → overtime\_data.get(“actual\_overtime\_duration”))).
  - Evaluate attendance.save().
  - Evaluate attendance.submit().
- Return attendance.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L545) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L525)

<a id="op-9992e24d9b6793"></a>
### Get overtime data

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_get_overtime_data`

**Inputs** shift\_name, working\_hours.

**Record and data access** read “Shift Type” via get\_value.

**Explicit results** overtime\_data.

**Local steps**

- Set overtime\_data from mapping().
- Set shift\_type\_details from Platform.db.get\_value(doctype = “Shift Type”, filters = mapping(“name” → shift\_name), fieldname = list(“allow\_overtime”, “start\_time”, “end\_time”), as\_dict = true).
- If (not shift\_type\_details or not shift\_type\_details.allow\_overtime).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not shift\_type\_details → not shift\_type\_details.allow\_overtime.
  - Return overtime\_data.
- Set standard\_working\_hours from calculate\_time\_difference(shift\_type\_details.start\_time, shift\_type\_details.end\_time).
- If working\_hours &gt; standard\_working\_hours.
  - Set actual\_overtime\_duration from (working\_hours − standard\_working\_hours).
  - Set overtime\_data from mapping(“standard\_working\_hours” → standard\_working\_hours, “actual\_overtime\_duration” → actual\_overtime\_duration).
- Return overtime\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L847) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L555) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L535)

<a id="op-245f8df447b22f"></a>
### Get existing half day attendance

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_get_existing_half_day_attendance`

**Inputs** employee, attendance\_date.

**Record and data access** read “Attendance” via exists · resolve a document from “Attendance” via get\_doc.

**Explicit results** attendance\_doc · no value.

**Local steps**

- Set attendance\_name from Platform.db.exists(“Attendance”, mapping(“employee” → employee, “attendance\_date” → attendance\_date, “status” → “Half Day”, “modify\_half\_day\_status” → 1, …)).
- If attendance\_name.
  - Set attendance\_doc from Platform.get\_doc(“Attendance”, attendance\_name).
  - Return attendance\_doc.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L1188) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L554) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L534)

<a id="op-5fb1df448ca2cf"></a>
### Calculate working hours

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_calculate_working_hours`

**Inputs** logs, check\_in\_out\_type, working\_hours\_calc\_type.

**Explicit results** tuple(total\_hours, in\_time, out\_time).

**Local steps**

- Set total\_hours from 0.
- Set in\_time, out\_time from no value.
- If check\_in\_out\_type equals “Alternating entries as IN and OUT during the same shift”.
  - Set in\_time from logs at 0.time.
  - If len(logs) ≥ 2.
    - Set out\_time from logs at negative 1.time.
  - If working\_hours\_calc\_type equals “First Check-in and Last Check-out”.
    - Set total\_hours from time\_diff\_in\_hours(in\_time, logs at negative 1.time).
  - Otherwise.
    - If working\_hours\_calc\_type equals “Every Valid Check-in and Check-out”.
      - Set logs from logs at slice no value to no value.
      - While len(logs) ≥ 2.
        - Update total\_hours using + time\_diff\_in\_hours(logs at 0.time, logs at 1.time).
        - Remove logs at slice no value to 2.
- Otherwise.
  - If check\_in\_out\_type equals “Strictly based on Log Type in Employee Checkin”.
    - If working\_hours\_calc\_type equals “First Check-in and Last Check-out”.
      - Set first\_in\_log\_index from find\_index\_in\_dict(logs, “log\_type”, “IN”).
      - Set first\_in\_log from logs at first\_in\_log\_index when (first\_in\_log\_index or first\_in\_log\_index equals 0), otherwise no value.
        - Value choice on (first\_in\_log\_index or first\_in\_log\_index equals 0) — true gives logs at first\_in\_log\_index, false gives no value.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_in\_log\_index → first\_in\_log\_index equals 0.
      - Set last\_out\_log\_index from find\_index\_in\_dict(reversed(logs), “log\_type”, “OUT”).
      - Set last\_out\_log from logs at ((len(logs) − 1) − last\_out\_log\_index) when (last\_out\_log\_index or last\_out\_log\_index equals 0), otherwise no value.
        - Value choice on (last\_out\_log\_index or last\_out\_log\_index equals 0) — true gives logs at ((len(logs) − 1) − last\_out\_log\_index), false gives no value.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in last\_out\_log\_index → last\_out\_log\_index equals 0.
      - Set in\_time from getattr(first\_in\_log, “time”, no value).
      - Set out\_time from getattr(last\_out\_log, “time”, no value).
      - If (first\_in\_log and last\_out\_log).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in first\_in\_log → last\_out\_log.
        - Set total\_hours from time\_diff\_in\_hours(in\_time, out\_time).
    - Otherwise.
      - If working\_hours\_calc\_type equals “Every Valid Check-in and Check-out”.
        - Set in\_log, out\_log from no value.
        - For each log in logs.
          - If (in\_log and out\_log).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_log → out\_log.
            - If not in\_time.
              - Set in\_time from in\_log.time.
            - Set out\_time from out\_log.time.
            - Update total\_hours using + time\_diff\_in\_hours(in\_log.time, out\_log.time).
            - Set in\_log, out\_log from no value.
          - If not in\_log.
            - Set in\_log from log when log.log\_type equals “IN”, otherwise no value.
              - Value choice on log.log\_type equals “IN” — true gives log, false gives no value.
            - If (in\_log and not in\_time).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_log → not in\_time.
              - Set in\_time from in\_log.time.
          - Otherwise.
            - If not out\_log.
              - Set out\_log from log when log.log\_type equals “OUT”, otherwise no value.
                - Value choice on log.log\_type equals “OUT” — true gives log, false gives no value.
        - If (in\_log and out\_log).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_log → out\_log.
          - Set out\_time from out\_log.time.
          - Update total\_hours using + time\_diff\_in\_hours(in\_log.time, out\_log.time).
- Return tuple(total\_hours, in\_time, out\_time).

**Values supplied outside this operation** selected callable from getattr(first\_in\_log, “time”, no value), getattr(last\_out\_log, “time”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L1419) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L544) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L524)

<a id="op-7ad502f6751419"></a>
### Time diff in hours

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_time_diff_in_hours`

**Inputs** start, end.

**Explicit results** round((float((end − start).total\_seconds()) ÷ 3600), 2).

**Local steps**

- Return round((float((end − start).total\_seconds()) ÷ 3600), 2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L2637) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L559) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L539)

<a id="op-d490803914f205"></a>
### Find index in dict

`operation_workforce_human_resources_record_definitions_employee_checkin_business_behavior_find_index_in_mapping`

**Inputs** dict\_list, key, value.

**Explicit results** next(generator of index for tuple(index, d) drawn from enumerate(dict\_list) where d at key equals value, no value).

**Local steps**

- Return next(generator of index for tuple(index, d) drawn from enumerate(dict\_list) where d at key equals value, no value).
  - Draw tuple(index, d) from enumerate(dict\_list), keep a combination only if (d at key equals value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0020.json#L2737) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L553) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L533)
