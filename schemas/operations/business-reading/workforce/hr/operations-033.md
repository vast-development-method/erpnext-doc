# Employment and attendance · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Monthly attendance sheet

<a id="op-ec546cff7fe45e"></a>
### Get date range from filters

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_date_range_from_filters`

**Inputs** filters.

**Declared result** tuple.

**Explicit results** tuple(start\_date, end\_date) · tuple(getdate(filters.start\_date), getdate(filters.end\_date)).

**Local steps**

- If filters.filter\_based\_on equals “Month”.
  - Set total\_days from get\_total\_days\_in\_month(filters).
  - Set start\_date from getdate(formatted text {cstr(filters.year)}-{cstr(filters.month)}-01).
  - Set end\_date from getdate(formatted text {cstr(filters.year)}-{cstr(filters.month)}-{total\_days}).
  - Return tuple(start\_date, end\_date).
- Return tuple(getdate(filters.start\_date), getdate(filters.end\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L4198) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L33) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L382)

<a id="op-9a7328d3f98a57"></a>
### Get rows

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_rows`

**Inputs** employee\_details, filters, employee\_holiday\_map, attendance\_map.

**Declared result** list at dict.

**Explicit results** records.

**Local steps**

- Set records from list().
- For each tuple(employee, details) in employee\_details.items().
  - Set holidays from employee\_holiday\_map.get(employee, list()).
  - If filters.summarized\_view.
    - Set attendance from get\_attendance\_status\_for\_summarized\_view(employee, filters, holidays, details.joined\_in\_current\_period, …).
    - If not attendance.
      - Continue with the next iteration or loop test.
    - Set leave\_summary from get\_leave\_summary(employee, filters).
    - Set entry\_exits\_summary from get\_entry\_exits\_summary(employee, filters).
    - Set row from mapping(“employee” → employee, “employee\_name” → details.employee\_name).
    - Evaluate set\_defaults\_for\_summarized\_view(filters, row).
    - Evaluate row.update(attendance).
    - Evaluate row.update(leave\_summary).
    - Evaluate row.update(entry\_exits\_summary).
    - Evaluate records.append(row).
  - Otherwise.
    - Set employee\_attendance from attendance\_map.get(employee).
    - If not employee\_attendance.
      - Continue with the next iteration or loop test.
    - Set attendance\_for\_employee from get\_attendance\_status\_for\_detailed\_view(employee, filters, employee\_attendance, holidays).
    - For each record in attendance\_for\_employee.
      - Evaluate record.update(mapping(“employee” → employee, “employee\_name” → details.employee\_name)).
    - Evaluate records.extend(attendance\_for\_employee).
- Return records.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L4550) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L41) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L390)

<a id="op-321206c16f9579"></a>
### Set defaults for summarized view

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_set_defaults_for_summarized_view`

**Inputs** filters, row.

**Local steps**

- For each entry in get\_columns(filters).
  - If entry.get(“fieldtype”) equals “Float”.
    - Set row at entry.get(“fieldname”) from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L5216) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L43) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L392)

<a id="op-00af2683aa8f99"></a>
### Get attendance status for summarized view

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_status_for_summarized_view`

**Inputs** employee, filters, holidays, joined\_in\_current\_period, joined\_date.

**Declared result** dict.

**Explicit results** mapping() · mapping(“total\_present” → ((summary.total\_present + summary.total\_half\_day\_present) + summary.total\_half\_day\_worked), “total\_leaves” → (summary.total\_leaves + summary.total\_half\_day\_leave), “total\_absent”  ….

**Local steps**

- Set tuple(summary, attendance\_days) from get\_attendance\_summary\_and\_days(employee, filters).
- If not any(summary.values()).
  - Return mapping().
- Set total\_days from get\_dates\_in\_period(filters).
- Set total\_holidays, total\_unmarked\_days from 0.
- For each d in total\_days.
  - Set d from getdate(d).
  - If (d belongs to attendance\_days or (joined\_in\_current\_period and d &lt; joined\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d belongs to attendance\_days → (joined\_in\_current\_period and d &lt; joined\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in joined\_in\_current\_period → d &lt; joined\_date.
    - Continue with the next iteration or loop test.
  - Set status from get\_holiday\_status(d, holidays).
  - If status belongs to list(“Weekly Off”, “Holiday”).
    - Update total\_holidays using + 1.
  - Otherwise.
    - If not status.
      - Update total\_unmarked\_days using + 1.
- Return mapping(“total\_present” → ((summary.total\_present + summary.total\_half\_day\_present) + summary.total\_half\_day\_worked), “total\_leaves” → (summary.total\_leaves + summary.total\_half\_day\_leave), “total\_absent”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L5367) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L24) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L373)

<a id="op-ccf6941089ba09"></a>
### Get attendance summary and days

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_summary_and_days`

**Inputs** employee, filters.

**Declared result** tuple at tuple(dict, list).

**Explicit results** tuple(summary at 0, days).

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set present\_case from nested operand in the contract.terms.Case().when((Attendance.status equals “Present” bitwise or Attendance.status equals “Work From Home”), 1).else\_(0).
- Set sum\_present from Sum(present\_case).as\_(“total\_present”).
- Set absent\_case from nested operand in the contract.terms.Case().when(Attendance.status equals “Absent”, 1).else\_(0).
- Set sum\_absent from Sum(absent\_case).as\_(“total\_absent”).
- Set leave\_case from nested operand in the contract.terms.Case().when(Attendance.status equals “On Leave”, 1).else\_(0).
- Set sum\_leave from Sum(leave\_case).as\_(“total\_leaves”).
- Set leave\_application\_condition from Coalesce(Attendance.leave\_application, empty text) differs from empty text.
- Set half\_day\_leave\_case from nested operand in the contract.terms.Case().when((Attendance.status equals “Half Day” bitwise and leave\_application\_condition), 0.5).else\_(0).
- Set sum\_half\_day\_leave from Sum(half\_day\_leave\_case).as\_(“total\_half\_day\_leave”).
- Set half\_day\_worked\_case from nested operand in the contract().when((nested operand in the contract equals nested operand in the contract bitwise and leave\_application\_condition), 0).when(Attendance.status equals “Half Day”, 0.5).else\_(0).
- Set sum\_half\_day\_worked from Sum(half\_day\_worked\_case).as\_(“total\_half\_day\_worked”).
- Set half\_day\_absent\_case from nested operand in the contract.terms.Case().when((Attendance.status equals “Half Day” bitwise and Attendance.half\_day\_status equals “Absent”), 0.5).else\_(0).
- Set sum\_half\_day\_absent from Sum(half\_day\_absent\_case).as\_(“total\_half\_day\_absent”).
- Set half\_day\_present\_case from nested operand in the contract().when((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in the contract), 0).when(Attend ….
- Set sum\_half\_day\_present from Sum(half\_day\_present\_case).as\_(“total\_half\_day\_present”).
- Set attendance\_date\_condition from get\_date\_condition(Attendance.attendance\_date, filters).
- Set summary from nested operand in the contract(nested operand in the contract).select(sum\_present, sum\_absent, sum\_leave, sum\_half\_day\_leave, …).where((((nested operand in the contract equals nested operand in the contrac ….
- Set days from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
- Return tuple(summary at 0, days).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L5920) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L25) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L374)

<a id="op-9e456edb36765f"></a>
### Get attendance status for detailed view

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_status_for_detailed_view`

**Inputs** employee, filters, employee\_attendance, holidays.

**Declared result** list at dict.

**Explicit results** attendance\_values.

**Local steps**

- Set total\_days from get\_dates\_in\_period(filters).
- Set attendance\_values from list().
- For each tuple(shift, status\_dict) in employee\_attendance.items().
  - Set row from mapping(“shift” → shift).
  - For each d in total\_days.
    - Set d from getdate(d).
    - Set status from status\_dict.get(d).
    - If (status is identical to no value and holidays).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in status is identical to no value → holidays.
      - Set status from get\_holiday\_status(d, holidays).
    - Set abbr from status\_map.get(status, empty text).
    - Set row at d.strftime(“%d-%m-%Y”) from abbr.
  - Evaluate attendance\_values.append(row).
- Return attendance\_values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0088.json#L7496) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L23) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L372)

<a id="op-9fadf7327c2180"></a>
### Get holiday status

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_holiday_status`

**Inputs** holiday\_date, holidays.

**Declared result** str.

**Explicit results** status.

**Local steps**

- Set status from no value.
- If holidays.
  - For each holiday in holidays.
    - If holiday\_date equals holiday.get(“holiday\_date”).
      - If holiday.get(“weekly\_off”).
        - Set status from “Weekly Off”.
      - Otherwise.
        - Set status from “Holiday”.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return status.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0089.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L38) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L387)

<a id="op-ab3b84bdb962e1"></a>
### Get leave summary

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_leave_summary`

**Inputs** employee, filters.

**Declared result** dict at tuple(str, float).

**Explicit results** leaves.

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set day\_case from nested operand in the contract.terms.Case().when(Attendance.status equals “Half Day”, 0.5).else\_(1).
- Set sum\_leave\_days from Sum(day\_case).as\_(“leave\_days”).
- Set attendance\_date\_condition from get\_date\_condition(Attendance.attendance\_date, filters).
- Set leave\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and attendance\_date ….
- Set leaves from mapping().
- For each d in leave\_details.
  - Set leave\_type from Platform.scrub(d.leave\_type).
  - Set leaves at leave\_type from d.leave\_days.
- Return leaves.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0089.json#L208) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L39) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L388)

<a id="op-67ce7639a0a538"></a>
### Get entry exits summary

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_entry_exits_summary`

**Inputs** employee, filters.

**Declared result** dict at tuple(str, float).

**Explicit results** entry\_exits at 0.

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set late\_entry\_case from Platform.qb.terms.Case().when(Attendance.late\_entry equals “1”, “1”).
- Set count\_late\_entries from Count(late\_entry\_case).as\_(“total\_late\_entries”).
- Set early\_exit\_case from Platform.qb.terms.Case().when(Attendance.early\_exit equals “1”, “1”).
- Set count\_early\_exits from Count(early\_exit\_case).as\_(“total\_early\_exits”).
- Set attendance\_date\_condition from get\_date\_condition(Attendance.attendance\_date, filters).
- Set entry\_exits from nested operand in the contract(nested operand in the contract).select(count\_late\_entries, count\_early\_exits).where((((nested operand in the contract equals nested operand in the contract bitwise and nested ….
- Return entry\_exits at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0089.json#L807) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L37) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L386)

<a id="op-bbff8bfaab9598"></a>
### Get attendance years

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_attendance_years`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** whitespace '\\n'.join(generator of cstr(entry.year) for entry drawn from year\_list).

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set year\_list from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“year”)).distinct().run(as\_dict = true).
- If year\_list.
  - Evaluate year\_list.sort(key = deferred anonymous expression, reverse = true).
- Otherwise.
  - Set year\_list from list(Platform.\_dict(mapping(“year” → getdate().year))).
- Return whitespace '\\n'.join(generator of cstr(entry.year) for entry drawn from year\_list).
  - Draw entry from year\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0089.json#L1344) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L26) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L375)

<a id="op-fc83dfc7e6f93e"></a>
### Get chart data

`operation_workforce_human_resources_report_monthly_attendance_sheet_business_behavior_get_chart_data`

**Inputs** attendance\_map, filters.

**Declared result** dict.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Absent”, “values” → absent), mapping(“name” → translated “Present”, “values” → present), mapping(“name” → translat ….

**Local steps**

- Set days from get\_columns\_for\_days(filters).
- Set labels from list().
- Set absent from list().
- Set present from list().
- Set leave from list().
- For each day in days.
  - Evaluate labels.append(day at “label”).
  - Set total\_absent\_on\_day, total\_leaves\_on\_day, total\_present\_on\_day from 0.
  - For each tuple(\_\_, attendance\_dict) in attendance\_map.items().
    - For each tuple(\_\_, attendance) in attendance\_dict.items().
      - Set attendance\_on\_day from attendance.get(getdate(day at “fieldname”, parse\_day\_first = true)).
      - If attendance\_on\_day equals “On Leave”.
        - Update total\_leaves\_on\_day using + 1.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Otherwise.
        - If attendance\_on\_day equals “Absent”.
          - Update total\_absent\_on\_day using + 1.
        - Otherwise.
          - If attendance\_on\_day belongs to list(“Present”, “Work From Home”).
            - Update total\_present\_on\_day using + 1.
          - Otherwise.
            - If attendance\_on\_day equals “Half Day”.
              - Update total\_present\_on\_day using + 0.5.
              - Update total\_leaves\_on\_day using + 0.5.
  - Evaluate absent.append(total\_absent\_on\_day).
  - Evaluate present.append(total\_present\_on\_day).
  - Evaluate leave.append(total\_leaves\_on\_day).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Absent”, “values” → absent), mapping(“name” → translated “Present”, “values” → present), mapping(“name” → translat ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0089.json#L1740) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L27) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L376)

## Workspace · Organizational chart

<a id="op-bbc305bff15e4a"></a>
### Check access

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_check_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** company.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L131) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L182) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L182)

<a id="op-8c56970812fa1c"></a>
### Get allowed companies

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_allowed_companies`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Company” via get\_list · read “Employee” via get\_value.

**Explicit results** companies · list() · list of company for company drawn from companies where company equals own\_company.

**Local steps**

- Set companies from Platform.get\_list(“Company”, pluck = “name”, order\_by = “name”).
- If can\_read\_all\_employees().
  - Return companies.
- If not is\_shown\_to\_all\_employees().
  - Return list().
- Set own\_company from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user, “status” → “Active”), “company”).
- Return list of company for company drawn from companies where company equals own\_company.
  - Draw company from companies, keep a combination only if (company equals own\_company).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L133) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L184) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L184)

<a id="op-0191f823bf21ae"></a>
### Can read all employees

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_can_read_all_employees`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L130) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L181) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L181)

<a id="op-70a52effc74fe9"></a>
### Is shown to all employees

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_is_shown_to_all_employees`

**Inputs** no declared parameters.

**Declared result** bool.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** bool(Platform.db.get\_single\_value(“HR Settings”, “show\_org\_chart\_to\_all\_employees”)).

**Local steps**

- Return bool(Platform.db.get\_single\_value(“HR Settings”, “show\_org\_chart\_to\_all\_employees”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “show\_org\_chart\_to\_all\_employees”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L149) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L200) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L200)

<a id="op-e7fa45e5be4ab3"></a>
### Get chart context

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_chart_context`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** mapping(“companies” → companies, “company” → company, “employee” → (employee and employee.name), “hidden\_from\_employees” → (not companies and not is\_shown\_to\_all\_employees())).

**Local steps**

- Set companies from get\_allowed\_companies().
- Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user, “status” → “Active”), list(“name”, “company”), as\_dict = true).
- Set company from ((employee and employee.company) or Platform.defaults.get\_user\_default(“Company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (employee and employee.company) → Platform.defaults.get\_user\_default(“Company”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → employee.company.
- If company does not belong to companies.
  - Set company from companies at 0 when companies, otherwise no value.
    - Value choice on companies — true gives companies at 0, false gives no value.
- Return mapping(“companies” → companies, “company” → company, “employee” → (employee and employee.name), “hidden\_from\_employees” → (not companies and not is\_shown\_to\_all\_employees())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → employee.name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not companies → not is\_shown\_to\_all\_employees().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L135) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L186) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L186)

<a id="op-08beb7b2bfa7ea"></a>
### Get children

`operation_workforce_human_resources_page_organizational_chart_business_behavior_get_children`

**Inputs** company, parent = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_nodes(company, companies, get\_employees(company, mapping(“reports\_to” → parent))) · list() · get\_nodes(company, companies, get\_employees(company, mapping(“name” → list(“in”, roots)))).

**Local steps**

- Set companies from check\_access(company).
- If parent.
  - Return get\_nodes(company, companies, get\_employees(company, mapping(“reports\_to” → parent))).
- Set managers from mapping of employee.name → employee.reports\_to for employee drawn from get\_employees(company, fields = list(“name”, “reports\_to”)).
  - Draw employee from get\_employees(company, fields = list(“name”, “reports\_to”)).
- Set roots from list of name for tuple(name, manager) drawn from managers.items() where manager does not belong to managers.
  - Draw tuple(name, manager) from managers.items(), keep a combination only if (manager does not belong to managers).
- If not roots.
  - Return list().
- Return get\_nodes(company, companies, get\_employees(company, mapping(“name” → list(“in”, roots)))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L306) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L306)

<a id="op-9b19fb16ce791f"></a>
### Get all nodes

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_all_nodes`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Employee” via count.

**Explicit results** get\_nodes(company, companies, get\_employees(company)).

**Explicit failure paths** validation helper — translated “{0} has more than {1} active employees, too many to open at once. Find a person, or open teams one at a time.”.format(Platform.bold(company), EXPAND\_ALL\_LIMIT).

**Local steps**

- Set companies from check\_access(company).
- If Platform.db.count(“Employee”, mapping(“company” → company, “status” → “Active”)) &gt; EXPAND\_ALL\_LIMIT.
  - Call the validation error handler Platform.throw(translated “{0} has more than {1} active employees, too many to open at once. Find a person, or open teams one at a time.”.format(Platform.bold(company), EXPAND\_ALL\_LIMIT), title = translate ….
- Return get\_nodes(company, companies, get\_employees(company)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L132) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L183) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L183)

<a id="op-4bfc00597875b5"></a>
### Get directory

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_directory`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** list of Platform.\_dict(get\_person(employee, leave\_status, can\_email), manager = employee.reports\_to, new\_joiner = bool((employee.date\_of\_joining and getdate(nested operand in the contract.date\_of\_joining)  ….

**Local steps**

- Evaluate check\_access(company).
- Set employees from get\_employees(company, fields = list(expanded NODE\_FIELDS, “date\_of\_joining”, “date\_of\_birth”), order\_by = “lft”).
- Set names from list of employee.name for employee drawn from employees.
  - Draw employee from employees.
- Set leave\_status from get\_leave\_status(mapping of name → company for name drawn from names).
  - Draw name from names.
- Set can\_email from get\_email\_access(names).
- Set today from getdate().
- Set joined\_after from add\_days(today, negative NEW\_JOINER\_DAYS).
- Set reminders from Platform.\_dict(birthdays = cint(Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”)), anniversaries = cint(Platform.db.get\_single\_value(“HR Settings”, “send\_work\_anniversary\_reminders”))).
- Return list of Platform.\_dict(get\_person(employee, leave\_status, can\_email), manager = employee.reports\_to, new\_joiner = bool((employee.date\_of\_joining and getdate(nested operand in the contract.date\_of\_joining)  ….
  - Draw employee from employees.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee.date\_of\_joining → getdate(employee.date\_of\_joining) &gt; joined\_after.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_birthday\_reminders”), Platform.db.get\_single\_value(“HR Settings”, “send\_work\_anniversary\_reminders”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L136) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L187) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L187)

<a id="op-06db26e0e08db9"></a>
### Get celebration

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_celebration`

**Inputs** employee, today, reminders.

**Declared result** (dict bitwise or no value).

**Explicit results** mapping(“birthday” → true) · mapping(“years” → (today.year − getdate(employee.date\_of\_joining).year)) · no value.

**Local steps**

- If (reminders.birthdays and is\_anniversary(employee.date\_of\_birth, today)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reminders.birthdays → is\_anniversary(employee.date\_of\_birth, today).
  - Return mapping(“birthday” → true).
- If (reminders.anniversaries and is\_anniversary(employee.date\_of\_joining, today)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reminders.anniversaries → is\_anniversary(employee.date\_of\_joining, today).
  - Return mapping(“years” → (today.year − getdate(employee.date\_of\_joining).year)).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L134) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L185) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L185)

<a id="op-b1e02ffbd73ba7"></a>
### Is anniversary

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_is_anniversary`

**Inputs** day, today.

**Declared result** bool.

**Explicit results** false · (tuple(day.month, day.day) equals tuple(today.month, today.day) and day.year &lt; today.year).

**Local steps**

- If not day.
  - Return false.
- Set day from getdate(day).
- Return (tuple(day.month, day.day) equals tuple(today.month, today.day) and day.year &lt; today.year).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tuple(day.month, day.day) equals tuple(today.month, today.day) → day.year &lt; today.year.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L146) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L197) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L197)

<a id="op-ef6327a877888a"></a>
### Search employees

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_search_employees`

**Inputs** company, txt = empty text.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_all.

**Explicit results** Platform.get\_all(“Employee”, filters = mapping(“company” → company, “status” → “Active”), or\_filters = mapping(“employee\_name” → list(“like”, formatted text %{txt}%), “name” → list(“like”, formatted text % ….

**Local steps**

- Evaluate check\_access(company).
- Set txt from txt at slice no value to SEARCH\_TEXT\_LIMIT.
- Return Platform.get\_all(“Employee”, filters = mapping(“company” → company, “status” → “Active”), or\_filters = mapping(“employee\_name” → list(“like”, formatted text %{txt}%), “name” → list(“like”, formatted text % ….
  - Value choice on txt — true gives mapping(“employee\_name” → list(“like”, formatted text %{txt}%), “name” → list(“like”, formatted text %{txt}%)), false gives no value.
  - Value choice on txt — true gives “employee\_name”, false gives “lft”.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L151) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L202) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L202)

<a id="op-98f86d22b37ace"></a>
### Get path

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_path`

**Inputs** company, employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** path at slice no value to no value with step negative 1.

**Local steps**

- Evaluate check\_access(company).
- Set path from list().
- While (employee and employee does not belong to path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → employee does not belong to path.
  - Set found from get\_employees(company, mapping(“name” → employee), fields = list(“reports\_to”)).
  - If not found.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate path.append(employee).
  - Set employee from found at 0.reports\_to.
- Return path at slice no value to no value with step negative 1.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L144) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L195) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L195)

<a id="op-573de75b2b16f1"></a>
### Get employees

`operation_workforce_binding_workforce_hr_page_organizational_chart_organizational_chart_get_employees`

**Inputs** company, filters = no value, fields = no value, order\_by = “employee\_name”.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Employee” via get\_all.

**Explicit results** Platform.get\_all(“Employee”, filters = mapping(“company” → company, “status” → “Active”, expand (filters or mapping())), fields = (fields or NODE\_FIELDS), order\_by = order\_by, limit = 0).

**Local steps**

- Return Platform.get\_all(“Employee”, filters = mapping(“company” → company, “status” → “Active”, expand (filters or mapping())), fields = (fields or NODE\_FIELDS), order\_by = order\_by, limit = 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields → NODE\_FIELDS.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L138) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L189) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L189)
