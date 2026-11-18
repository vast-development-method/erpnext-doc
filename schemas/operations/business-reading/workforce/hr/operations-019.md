# Employment and attendance · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Goal

[Record definition](../../../../data/record-types/goal.json)

<a id="op-9eb92afba6215b"></a>
### Goal.update goal progress in appraisal

`operation_workforce_human_resources_record_definitions_goal_business_behavior_goal_update_goal_progress_in_appraisal`

**Inputs** self.

**Record and data access** read “Appraisal” via get\_value · resolve a document from “Appraisal” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.appraisal\_cycle.
  - Return no value.
- Set appraisal from Platform.db.get\_value(“Appraisal”, mapping(“employee” → self.employee, “appraisal\_cycle” → self.appraisal\_cycle)).
- If appraisal.
  - Set appraisal from Platform.get\_doc(“Appraisal”, appraisal).
  - Evaluate appraisal.set\_goal\_score(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L759) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L822) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L802)

<a id="op-eb3da6a94f966f"></a>
### Get children

`operation_workforce_human_resources_record_definitions_goal_business_behavior_get_children`

**Inputs** doctype, parent, is\_root = false, remaining named values filters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read doctype via get\_list.

**Explicit results** goals.

**Local steps**

- Set query\_filters from list(list(“status”, “!=”, “Archived”)).
- Set query\_or\_filters from list().
- If filters.get(“company”).
  - Evaluate query\_filters.append(list(“company”, “=”, filters.get(“company”))).
- If filters.get(“employee”).
  - Evaluate query\_filters.append(list(“employee”, “=”, filters.get(“employee”))).
- If filters.get(“appraisal\_cycle”).
  - Evaluate query\_filters.append(list(“appraisal\_cycle”, “=”, filters.get(“appraisal\_cycle”))).
- If filters.get(“goal”).
  - Evaluate query\_filters.append(list(“parent\_goal”, “=”, filters.get(“goal”))).
- Otherwise.
  - If (parent and not is\_root).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → not is\_root.
    - Evaluate query\_filters.append(list(“parent\_goal”, “=”, parent)).
  - Otherwise.
    - Evaluate query\_filters.append(list(“parent\_goal”, “in”, list(empty text, no value))).
- If filters.get(“date\_range”).
  - Set tuple(from\_date, to\_date) from Platform.parse\_json(filters.get(“date\_range”)).
  - Evaluate query\_filters.append(list(“start\_date”, “between”, list(from\_date, to\_date))).
  - Evaluate query\_or\_filters.append(list(“end\_date”, “is”, “not set”)).
  - Evaluate query\_or\_filters.append(list(“end\_date”, “between”, list(from\_date, to\_date))).
- Set goals from Platform.get\_list(doctype, fields = list(“name as value”, “goal\_name as title”, “is\_group as expandable”, “status”, …), filters = query\_filters, or\_filters = query\_or\_filters when query\_or\_filters, otherwi ….
  - Value choice on query\_or\_filters — true gives query\_or\_filters, false gives no value.
- Evaluate \_update\_goal\_completion\_status(goals).
- Return goals.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L28) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L816) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L796)

<a id="op-0d555d61fb4f5e"></a>
### Update goal completion status

`operation_workforce_human_resources_record_definitions_goal_business_behavior_update_goal_completion_status`

**Inputs** goals.

**Declared result** list at dict.

**Record and data access** read “Goal” via count.

**Explicit results** goals.

**Local steps**

- For each goal in goals.
  - If goal.expandable.
    - Set total\_goals from Platform.db.count(“Goal”, dict(parent\_goal = goal.value)).
    - If total\_goals.
      - Set completed from (Platform.db.count(“Goal”, mapping(“parent\_goal” → goal.value, “status” → “Completed”)) or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.count(“Goal”, mapping(“parent\_goal” → goal.value, “status” → “Completed”)) → 0.
      - Set goal at “completion\_count” from translated “{0} of {1} Completed”.format(completed, total\_goals).
- Return goals.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L1898) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L828) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L808)

<a id="op-3b044fea0177ba"></a>
### Validate goal access

`operation_workforce_binding_workforce_hr_doctype_goal_goal_validate_goal_access`

**Inputs** employee.

**Declared result** no value.

**Record and data access** read “Employee” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to update another employee's goal.”.

**Local steps**

- If has\_common(HR\_ROLES, Platform.get\_roles()).
  - Return no value.
- Set is\_own\_goal from Platform.db.get\_value(“Employee”, employee, “user\_id”) equals Platform.session.user.
- If not is\_own\_goal.
  - Call the validation error handler Platform.throw(translated “You are not permitted to update another employee's goal.”, Platform.PermissionError, title = translated “Not Permitted”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L62) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L113) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L113)

<a id="op-cb20eb9fe0b685"></a>
### Update progress

`operation_workforce_human_resources_record_definitions_goal_business_behavior_update_progress`

**Inputs** progress, goal.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Goal” via get\_doc.

**State and service calls** call save on goal.

**Explicit results** goal.

**Local steps**

- Set goal from Platform.get\_doc(“Goal”, goal).
- Evaluate validate\_goal\_access(goal.employee).
- Set goal.progress from progress.
- Set goal.flags.ignore\_mandatory from true.
- Evaluate goal.save().
- Return goal.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L30) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L829) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L809)

<a id="op-735788214205f4"></a>
### Update status

`operation_workforce_human_resources_record_definitions_goal_business_behavior_update_status`

**Inputs** status, goals.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Goal” via get\_doc.

**State and service calls** call save on goal.

**Explicit results** goals.

**Local steps**

- If isinstance(goals, str).
  - Bind dependencies json.
  - Set goals from json.loads(goals).
- For each goal in goals.
  - Set goal from Platform.get\_doc(“Goal”, goal).
  - Evaluate validate\_goal\_access(goal.employee).
  - Set goal.status from status.
  - If status equals “Completed”.
    - Set goal.progress from 100.
  - Set goal.flags.ignore\_mandatory from true.
  - Evaluate goal.save().
- Return goals.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L31) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L830) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L810)

<a id="op-56342c7dd3f251"></a>
### Add tree node

`operation_workforce_human_resources_record_definitions_goal_business_behavior_add_tree_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Goal” via exists · resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Set args from make\_tree\_args(expanded names args).
- If (args.parent\_goal equals “All Goals” or not Platform.db.exists(“Goal”, args.parent\_goal)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.parent\_goal equals “All Goals” → not Platform.db.exists(“Goal”, args.parent\_goal).
  - Set args.parent\_goal from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L2705) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L815) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L795)

## Service · Hiring vs attrition count

<a id="op-c630ee80bb3df4"></a>
### Get data

`operation_workforce_human_resources_dashboard_chart_source_hiring_vs_attrition_count_business_behavior_get_data`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Declared result** dict at tuple(str, list).

**Explicit results** mapping(“labels” → list of get\_period(r at 0, filters.get(“time\_interval”)) for r drawn from hiring\_data, “datasets” → list(mapping(“name” → translated “Hiring Count”, “values” → list of r at 1 for r drawn ….

**Local steps**

- If filters.
  - Set filters from Platform.parse\_json(filters).
- Set from\_date from filters.get(“from\_date”).
- Set to\_date from filters.get(“to\_date”).
- If not to\_date.
  - Set to\_date from getdate().
- Set permitted\_fields from Platform.model.get\_permitted\_fields(“Employee”, user = Platform.session.user).
- Set hiring from get\_records(from\_date, to\_date, “date\_of\_joining”, filters.get(“company”)) when “date\_of\_joining” belongs to permitted\_fields, otherwise list().
  - Value choice on “date\_of\_joining” belongs to permitted\_fields — true gives get\_records(from\_date, to\_date, “date\_of\_joining”, filters.get(“company”)), false gives list().
- Set attrition from get\_records(from\_date, to\_date, “relieving\_date”, filters.get(“company”)) when “relieving\_date” belongs to permitted\_fields, otherwise list().
  - Value choice on “relieving\_date” belongs to permitted\_fields — true gives get\_records(from\_date, to\_date, “relieving\_date”, filters.get(“company”)), false gives list().
- Set hiring\_data from get\_result(hiring, filters.get(“time\_interval”), from\_date, to\_date, …).
- Set attrition\_data from get\_result(attrition, filters.get(“time\_interval”), from\_date, to\_date, …).
- Return mapping(“labels” → list of get\_period(r at 0, filters.get(“time\_interval”)) for r drawn from hiring\_data, “datasets” → list(mapping(“name” → translated “Hiring Count”, “values” → list of r at 1 for r drawn ….
  - Draw r from hiring\_data.
  - Draw r from hiring\_data.
  - Draw r from attrition\_data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L1378) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L301) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L301)

<a id="op-f6299cd32bcd48"></a>
### Get records

`operation_workforce_human_resources_dashboard_chart_source_hiring_vs_attrition_count_business_behavior_get_records`

**Inputs** from\_date, to\_date, datefield, company.

**Declared result** tuple at tuple at tuple(str, float, int).

**Record and data access** read “Employee” via get\_list.

**Explicit results** data.

**Local steps**

- Set filters from list(list(“Employee”, “company”, “=”, company), list(“Employee”, datefield, “&gt;=”, from\_date), list(“Employee”, datefield, “&lt;=”, to\_date)).
- Set data from Platform.db.get\_list(“Employee”, fields = list(formatted text {datefield} as \_unit, mapping(“SUM” → 1), mapping(“COUNT” → “\*”)), filters = filters, group\_by = “\_unit”, order\_by = “\_unit asc”, …).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L2393) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L302) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L302)

## Record · Holiday list assignment

[Record definition](../../../../data/record-types/holiday_list_assignment.json)

<a id="op-2d2965992cfee6"></a>
### Holiday List Assignment.holiday list start

`operation_workforce_human_resources_record_definitions_holiday_list_assignment_business_behavior_holiday_list_assignment_holiday_list_start`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Holiday List” via get\_value.

**Explicit results** Platform.get\_value(“Holiday List”, self.holiday\_list, “from\_date”) when self.holiday\_list, otherwise no value.

**Local steps**

- Return Platform.get\_value(“Holiday List”, self.holiday\_list, “from\_date”) when self.holiday\_list, otherwise no value.
  - Value choice on self.holiday\_list — true gives Platform.get\_value(“Holiday List”, self.holiday\_list, “from\_date”), false gives no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L6711) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L842) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L822)

<a id="op-bffc68a797f943"></a>
### Holiday List Assignment.holiday list end

`operation_workforce_human_resources_record_definitions_holiday_list_assignment_business_behavior_holiday_list_assignment_holiday_list_end`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Holiday List” via get\_value.

**Explicit results** Platform.get\_value(“Holiday List”, self.holiday\_list, “to\_date”) when self.holiday\_list, otherwise no value.

**Local steps**

- Return Platform.get\_value(“Holiday List”, self.holiday\_list, “to\_date”) when self.holiday\_list, otherwise no value.
  - Value choice on self.holiday\_list — true gives Platform.get\_value(“Holiday List”, self.holiday\_list, “to\_date”), false gives no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L6808) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L841) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L821)

<a id="op-afa15824463036"></a>
### Holiday List Assignment.validate

`operation_workforce_human_resources_record_definitions_holiday_list_assignment_business_behavior_holiday_list_assignment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_assignment\_start\_date().
- Evaluate self.validate\_existing\_assignment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate assignment start date](operations-019.md#op-032dfc773ec7f0), [validate existing assignment](operations-019.md#op-d120e298098f56).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L6905) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L843) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L823)

<a id="op-d120e298098f56"></a>
### Holiday List Assignment.validate existing assignment

`operation_workforce_human_resources_record_definitions_holiday_list_assignment_business_behavior_holiday_list_assignment_validate_existing_assignment`

**Inputs** self.

**Record and data access** read “Holiday List Assignment” via exists.

**Explicit failure paths** validation helper with DuplicateAssignment — translated “Holiday List Assignment for {0} already exists for date {1}: {2}”.format(self.assigned\_to, format\_date(self.from\_date), get\_link\_to\_form(“Holiday List Assignment”, holiday\_list)).

**Local steps**

- Set holiday\_list from Platform.db.exists(“Holiday List Assignment”, mapping(“assigned\_to” → self.assigned\_to, “from\_date” → self.from\_date, “docstatus” → 1)).
- If holiday\_list.
  - Call the validation error handler Platform.throw(translated “Holiday List Assignment for {0} already exists for date {1}: {2}”.format(self.assigned\_to, format\_date(self.from\_date), get\_link\_to\_form(“Holiday List Assignment”, holiday\_list)) ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L6976) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L845) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L825)

<a id="op-032dfc773ec7f0"></a>
### Holiday List Assignment.validate assignment start date

`operation_workforce_human_resources_record_definitions_holiday_list_assignment_business_behavior_holiday_list_assignment_validate_assignment_start_date`

**Inputs** self.

**Record and data access** read “Holiday List” via get\_value.

**Explicit failure paths** validation helper — translated “Assignment start date cannot be outside holiday list dates”.

**Local steps**

- Set tuple(holiday\_list\_start, holiday\_list\_end) from Platform.db.get\_value(“Holiday List”, self.holiday\_list, list(“from\_date”, “to\_date”)).
- Set assignment\_start\_date from getdate(self.from\_date).
- If (assignment\_start\_date &lt; holiday\_list\_start or assignment\_start\_date &gt; holiday\_list\_end).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in assignment\_start\_date &lt; holiday\_list\_start → assignment\_start\_date &gt; holiday\_list\_end.
  - Call the validation error handler Platform.throw(translated “Assignment start date cannot be outside holiday list dates”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0034.json#L7253) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L844) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L824)

## Record · Hr settings

<a id="op-a81083e478d9ba"></a>
### HRSettings.validate

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_naming\_series().
- Use module bindings PROCEED\_WITH\_FREQUENCY\_CHANGE.
- If not PROCEED\_WITH\_FREQUENCY\_CHANGE.
  - Evaluate self.validate\_frequency\_change().
- Set PROCEED\_WITH\_FREQUENCY\_CHANGE from false.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set naming series](operations-019.md#op-303c7d427e4684), [validate frequency change](operations-019.md#op-d7dc8e7eb7ea43).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L1883) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L856) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L836)

<a id="op-303c7d427e4684"></a>
### HRSettings.set naming series

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_set_naming_series`

**Inputs** self.

**Local steps**

- Bind dependencies set\_by\_naming\_series.
- Evaluate set\_by\_naming\_series(“Employee”, “employee\_number”, self.get(“emp\_created\_by”) equals “Naming Series”, hide\_name\_field = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L1988) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L854) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L834)

<a id="op-d7dc8e7eb7ea43"></a>
### HRSettings.validate frequency change

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_validate_frequency_change`

**Inputs** self.

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set tuple(weekly\_job, monthly\_job) from tuple(no value, no value).
- Attempt the following.
  - Set weekly\_job from Platform.get\_doc(“Scheduled Job Type”, mapping(“method” → “Workforce.controllers.employee\_reminders.send\_reminders\_in\_advance\_weekly”)).
  - Set monthly\_job from Platform.get\_doc(“Scheduled Job Type”, mapping(“method” → “Workforce.controllers.employee\_reminders.send\_reminders\_in\_advance\_monthly”)).
- On failure (Platform.DoesNotExistError).
  - Return no value.
- Set next\_weekly\_trigger from weekly\_job.get\_next\_execution().
- Set next\_monthly\_trigger from monthly\_job.get\_next\_execution().
- If self.freq\_changed\_from\_monthly\_to\_weekly().
  - If next\_monthly\_trigger &lt; next\_weekly\_trigger.
    - Evaluate self.show\_freq\_change\_warning(next\_monthly\_trigger, next\_weekly\_trigger).
- Otherwise.
  - If self.freq\_changed\_from\_weekly\_to\_monthly().
    - If next\_monthly\_trigger &gt; next\_weekly\_trigger.
      - Evaluate self.show\_freq\_change\_warning(next\_weekly\_trigger, next\_monthly\_trigger).

If control reaches the end, it returns no value.

**Methods declared on this owner** [freq changed from monthly to weekly](operations-019.md#op-bb92c126d31ac3), [show freq change warning](operations-019.md#op-188bd8f49ed48d), [freq changed from weekly to monthly](operations-019.md#op-d756c1c66d81f5).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L2109) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L857) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L837)

<a id="op-d756c1c66d81f5"></a>
### HRSettings.freq changed from weekly to monthly

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_freq_changed_from_weekly_to_monthly`

**Inputs** self.

**Explicit results** (self.has\_value\_changed(“frequency”) and self.frequency equals “Monthly”).

**Local steps**

- Return (self.has\_value\_changed(“frequency”) and self.frequency equals “Monthly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“frequency”) → self.frequency equals “Monthly”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L2595) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L853) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L833)

<a id="op-bb92c126d31ac3"></a>
### HRSettings.freq changed from monthly to weekly

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_freq_changed_from_monthly_to_weekly`

**Inputs** self.

**Explicit results** (self.has\_value\_changed(“frequency”) and self.frequency equals “Weekly”).

**Local steps**

- Return (self.has\_value\_changed(“frequency”) and self.frequency equals “Weekly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“frequency”) → self.frequency equals “Weekly”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L2680) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L852) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L832)

<a id="op-188bd8f49ed48d"></a>
### HRSettings.show freq change warning

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_human_resources_settings_show_freq_change_warning`

**Inputs** self, from\_date, to\_date.

**State and service calls** msgprint.

**Local steps**

- Set from\_date from Platform.bold(format\_date(from\_date)).
- Set to\_date from Platform.bold(format\_date(to\_date)).
- Set raise\_exception from Platform.ValidationError.
- If (Platform.flags.in\_test or Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_test → Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_migrate.
  - Set raise\_exception from false.
- Evaluate Platform.msgprint(msg = Platform.\_(“Employees will miss holiday reminders from {0} until {1}. &lt;br&gt; Do you want to proceed with this change?”).format(from\_date, to\_date), title = Platform.\_(“Confirm change  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L32) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L855) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L835)

<a id="op-57ff88f9a133d1"></a>
### Set proceed with frequency change

`operation_workforce_human_resources_record_definitions_human_resources_settings_business_behavior_set_proceed_with_frequency_change`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Use module bindings PROCEED\_WITH\_FREQUENCY\_CHANGE.
- Set PROCEED\_WITH\_FREQUENCY\_CHANGE from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3162) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L858) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L838)

## Record · Interview

[Record definition](../../../../data/record-types/interview.json)

<a id="op-e634b2328f1f09"></a>
### Interview.validate

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_interview().
- Evaluate self.validate\_designation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate interview](operations-019.md#op-81e85a13eea0dd), [validate designation](operations-020.md#op-e95dd9777eb034).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3223) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L872) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L852)

<a id="op-d0233ef8890f0e"></a>
### Interview.on submit

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only Interviews with Cleared or Rejected status can be submitted.”.

**Local steps**

- <a id="op-d0233ef8890f0e-guard-2"></a>If self.status does not belong to list(“Cleared”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “Only Interviews with Cleared or Rejected status can be submitted.”, title = translated “Not Allowed”).
- Evaluate self.show\_job\_applicant\_update\_dialog().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to list(“Cleared”, “Rejected”), self.status = “Pending” selects the branch that calls the validation-error handler with translated “Only Interviews with Cleared or Rejected status can be submitted.”. With self.status = “Cleared”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d0233ef8890f0e-guard-2)

**Methods declared on this owner** [show job applicant update dialog](operations-020.md#op-020395449faed8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3294) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L869) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L849)

<a id="op-81e85a13eea0dd"></a>
### Interview.validate duplicate interview

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_validate_duplicate_interview`

**Inputs** self.

**Record and data access** read “Interview” via exists.

**Explicit failure paths** validation helper — translated “Job Applicants are not allowed to appear twice for the same Interview Type. Interview {0} already scheduled  …”.format(Platform.bold(get\_link\_to\_form(“Interview”, duplicate\_interview)), Platfor ….

**Local steps**

- Set duplicate\_interview from Platform.db.exists(“Interview”, mapping(“job\_applicant” → self.job\_applicant, “interview\_type” → self.interview\_type, “docstatus” → 1)).
- If duplicate\_interview.
  - Call the validation error handler Platform.throw(translated “Job Applicants are not allowed to appear twice for the same Interview Type. Interview {0} already scheduled  …”.format(Platform.bold(get\_link\_to\_form(“Interview”, duplicate\_inter ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3443) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L874) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L854)
