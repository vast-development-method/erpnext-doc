# Projects and time · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Timesheet

[Record definition](../../../../data/record-types/timesheet.json)

<a id="op-37428ae54264c2"></a>
### Get activity cost

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_timesheet_get_activity_cost`

**Inputs** employee = no value, activity\_type = no value, currency = no value.

**Record and data access** read “Activity Cost” via get\_values · read “Activity Type” via get\_values.

**Explicit results** rate at 0 when rate, otherwise mapping().

**Explicit failure paths** validation helper — translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually.”.format(base\_currency, currency, nowdate()).

**Local steps**

- Set base\_currency from Platform.defaults.get\_global\_default(“currency”).
- Set rate from Platform.db.get\_values(“Activity Cost”, mapping(“employee” → employee, “activity\_type” → activity\_type), list(“costing\_rate”, “billing\_rate”), as\_dict = true).
- If (not rate and employee).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate → employee.
  - Set rate from Platform.db.get\_values(“Activity Cost”, mapping(“employee” → tuple(“is”, “not set”), “activity\_type” → activity\_type), list(“costing\_rate”, “billing\_rate”), as\_dict = true).
- If not rate.
  - Set rate from Platform.db.get\_values(“Activity Type”, mapping(“activity\_type” → activity\_type), list(“costing\_rate”, “billing\_rate”), as\_dict = true).
- If (rate and currency and currency differs from base\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate → currency → currency differs from base\_currency.
  - Set exchange\_rate from get\_exchange\_rate(base\_currency, currency).
  - If not exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually.”.format(base\_currency, currency, nowdate())).
  - Set rate at 0 at “costing\_rate” from (rate at 0 at “costing\_rate” × exchange\_rate).
  - Set rate at 0 at “billing\_rate” from (rate at 0 at “billing\_rate” × exchange\_rate).
- Return rate at 0 when rate, otherwise mapping().
  - Value choice on rate — true gives rate at 0, false gives mapping().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L244) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1369)

<a id="op-b2b0d8fba2d990"></a>
### Get events

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Timesheet Detail).format(conditions = conditions, match\_cond = get\_match\_cond(“Timesheet”)).

**Explicit results** Platform.db.sql(query text (SELECT, Timesheet Detail).format(conditions = conditions, match\_cond = get\_match\_cond(“Timesheet”)), mapping(“start” → start, “end” → end), as\_dict = true, update = mapping(“allDay” → 0)).

**Local steps**

- Set filters from json.loads(filters).
- Bind dependencies get\_event\_conditions.
- Set conditions from get\_event\_conditions(“Timesheet”, filters).
- Return Platform.db.sql(query text (SELECT, Timesheet Detail).format(conditions = conditions, match\_cond = get\_match\_cond(“Timesheet”)), mapping(“start” → start, “end” → end), as\_dict = true, update = mapping(“allDay” → 0)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L788)

<a id="op-dfc6bbf87c0aa6"></a>
### Get timesheets list

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_timesheets_list`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, order\_by = “creation”.

**Record and data access** read “Sales Invoice” via get\_all · read “Project” via get\_all.

**Explicit results** list() · query.where(nested operand in the contract.terms.Criterion.any(conditions)).run(as\_dict = true) · mapping().

**Local steps**

- Bind dependencies is\_website\_user.
- Bind dependencies get\_parents\_for\_user.
- Set customers from get\_parents\_for\_user(“Customer”) when is\_website\_user(), otherwise list().
  - Value choice on is\_website\_user() — true gives get\_parents\_for\_user(“Customer”), false gives list().
- If customers.
  - Set sales\_invoices from Platform.get\_all(“Sales Invoice”, filters = mapping(“customer” → list(“in”, customers), “docstatus” → list(“!=”, 2)), pluck = “name”).
  - Set projects from Platform.get\_all(“Project”, filters = mapping(“customer” → list(“in”, customers)), pluck = “name”).
  - If not (sales\_invoices or projects).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sales\_invoices → projects.
    - Return list().
  - Set table from Platform.qb.DocType(“Timesheet”).
  - Set child\_table from Platform.qb.DocType(“Timesheet Detail”).
  - Set query from nested operand in the contract(nested operand in the contract).orderby(table.end\_date).limit(limit\_page\_length).offset(limit\_start).
  - Set conditions from list().
  - If sales\_invoices.
    - Evaluate conditions.extend(list(table.sales\_invoice.isin(sales\_invoices), child\_table.sales\_invoice.isin(sales\_invoices))).
  - If projects.
    - Evaluate conditions.append(child\_table.project.isin(projects)).
  - Return query.where(nested operand in the contract.terms.Criterion.any(conditions)).run(as\_dict = true).
- Otherwise.
  - Return mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L794)

<a id="op-df0479b4ab1bbb"></a>
### Get list context

`operation_enterprise_projects_record_definitions_timesheet_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Timesheets”, …).

**Local steps**

- Return mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Timesheets”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1027) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L789)

<a id="op-da846cfebd71f5"></a>
### Get data

`operation_enterprise_projects_record_definitions_timesheet_timesheet_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “time\_sheet”, “transactions” → list(mapping(“label” → translated “References”, “items” → list(“Sales Invoice”)))).

**Local steps**

- Return mapping(“fieldname” → “time\_sheet”, “transactions” → list(mapping(“label” → translated “References”, “items” → list(“Sales Invoice”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1170) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L846)

## Report · Timesheet billing summary

<a id="op-e9668d7f0c8cda"></a>
### Execute

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, no value, …).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set group\_fieldname from filters.pop(“group\_by”, no value).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns(filters, group\_fieldname).
- Set data from get\_data(filters).
- Set data from get\_filtered\_data(“Timesheet”, columns, data, Platform.session.user).
- Set report\_summary from get\_report\_summary(data).
- If group\_fieldname.
  - Set data from group\_by(data, group\_fieldname).
- Return tuple(columns, data, no value, no value, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L872)

<a id="op-b8a16ae4773b4a"></a>
### Get columns

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_get_columns`

**Inputs** filters, group\_fieldname = no value.

**Explicit results** columns.

**Local steps**

- Set group\_columns from mapping(“date” → mapping(“label” → translated “Date”, “fieldtype” → “Date”, “fieldname” → “date”, “width” → 150), “project” → mapping(“label” → translated “Project”, “fieldtype” → “Link”, “fieldname” → “pr ….
- Set columns from list().
- If group\_fieldname belongs to group\_columns.
  - Set group\_columns at group\_fieldname at “hidden” from 0.
  - Evaluate columns.append(group\_columns.pop(group\_fieldname)).
- Evaluate columns.extend(group\_columns.values()).
- Evaluate columns.extend(list(mapping(“label” → translated “Employee Name”, “fieldtype” → “data”, “fieldname” → “employee\_name”, “hidden” → 1), mapping(“label” → translated “Timesheet”, “fieldtype” → “Link”, “fieldn ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L873)

<a id="op-2429389bace378"></a>
### Get data

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Timesheet” via get\_list.

**Explicit results** data.

**Local steps**

- Set \_filters from list().
- If filters.get(“employee”).
  - Evaluate \_filters.append(tuple(“employee”, “=”, filters.get(“employee”))).
- If filters.get(“project”).
  - Evaluate \_filters.append(tuple(“Timesheet Detail”, “project”, “=”, filters.get(“project”))).
- If filters.get(“from\_date”).
  - Evaluate \_filters.append(tuple(“Timesheet Detail”, “from\_time”, “&gt;=”, filters.get(“from\_date”))).
- If filters.get(“to\_date”).
  - Evaluate \_filters.append(tuple(“Timesheet Detail”, “from\_time”, “&lt;”, add\_days(getdate(filters.get(“to\_date”)), 1))).
- If not filters.get(“include\_draft\_timesheets”).
  - Evaluate \_filters.append(tuple(“docstatus”, “=”, DocStatus.submitted())).
- Otherwise.
  - Evaluate \_filters.append(tuple(“docstatus”, “in”, tuple(DocStatus.submitted(), DocStatus.draft()))).
- Set data from Platform.get\_list(“Timesheet”, fields = list(“name as timesheet”, “′tabTimesheet′.employee”, “′tabTimesheet′.employee\_name”, “′tabTimesheet Detail′.from\_time as date”, …), filters = \_filters, order\_by = “′ ….
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L874)

<a id="op-8fcf1e28ddbe82"></a>
### Group by

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_group_by`

**Inputs** data, fieldname.

**Explicit results** grouped\_data.

**Local steps**

- Set groups from mapping().
- For each row in data.
  - Evaluate groups.setdefault(get\_group\_value(row, fieldname), list()).append(row).
- Set grouped\_data from list().
- For each group in sorted(groups, key = deferred anonymous expression).
  - Set hours, billing\_hours, billing\_amount from 0.
  - Set child\_rows from list().
  - For each row in groups at group.
    - Update hours using + (row.get(“hours”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“hours”) → 0.
    - Update billing\_hours using + (row.get(“billing\_hours”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“billing\_hours”) → 0.
    - Update billing\_amount using + (row.get(“billing\_amount”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“billing\_amount”) → 0.
    - Set \_row from row.copy().
    - Set \_row at fieldname from no value.
    - Set \_row at “indent” from 1.
    - Set \_row at “is\_group” from 0.
    - Evaluate child\_rows.append(\_row).
  - Set group\_row from mapping(fieldname → group, “hours” → hours, “billing\_hours” → billing\_hours, “billing\_amount” → billing\_amount, …).
  - If fieldname equals “employee”.
    - Set group\_row at “employee\_name” from groups at group at 0.get(“employee\_name”).
  - Evaluate grouped\_data.append(group\_row).
  - Evaluate grouped\_data.extend(child\_rows).
- Return grouped\_data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L1883) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L877)

<a id="op-53a78034cfb4d6"></a>
### Get group value

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_get_group_value`

**Inputs** row, fieldname.

**Explicit results** getdate(value) when (fieldname equals “date” and value), otherwise value.

**Local steps**

- Set value from row.get(fieldname).
- Return getdate(value) when (fieldname equals “date” and value), otherwise value.
  - Value choice on (fieldname equals “date” and value) — true gives getdate(value), false gives value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname equals “date” → value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L2637) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L875)

<a id="op-3f0ba5c044af66"></a>
### Get report summary

`operation_enterprise_projects_report_timesheet_billing_summary_business_behavior_get_report_summary`

**Inputs** data.

**Explicit results** no value · list(mapping(“value” → totals at “hours”, “indicator” → “Blue”, “label” → translated “Total Working Hours”, “datatype” → “Float”), mapping(“value” → totals at “billing\_hours”, “indicator” → “Blue”, “label” ….

**Local steps**

- If not data.
  - Return no value.
- Set totals from dict.fromkeys(VALUE\_FIELDNAMES, 0.0).
- For each row in data.
  - For each value\_fieldname in VALUE\_FIELDNAMES.
    - Update totals at value\_fieldname using + (row.get(value\_fieldname) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(value\_fieldname) → 0.
- Return list(mapping(“value” → totals at “hours”, “indicator” → “Blue”, “label” → translated “Total Working Hours”, “datatype” → “Float”), mapping(“value” → totals at “billing\_hours”, “indicator” → “Blue”, “label” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0613.json#L2764) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L876)

## Record · Timesheet detail

[Record definition](../../../../data/record-types/timesheet_detail.json)

<a id="op-8bdf8f183e6f54"></a>
### Timesheet Detail.set to time

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_set_to_time`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.from\_time and self.hours).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_time → self.hours.
  - Return no value.
- Set \_to\_time from get\_datetime(add\_to\_date(self.from\_time, hours = self.hours, as\_datetime = true)).
- If abs(time\_diff\_in\_seconds(\_to\_time, self.to\_time)) ≥ 1.
  - Set self.to\_time from \_to\_time.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1295) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L823)

<a id="op-f571afa9b7e48f"></a>
### Timesheet Detail.set project

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_set_project`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Local steps**

- If (self.task and not self.project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.task → not self.project.
  - Set self.project from Platform.db.get\_value(“Task”, self.task, “project”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1504) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L822)

<a id="op-6b2c66cd994508"></a>
### Timesheet Detail.calculate hours

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_calculate_hours`

**Inputs** self.

**Local steps**

- If (self.to\_time and self.from\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_time → self.from\_time.
  - Set self.hours from time\_diff\_in\_hours(self.to\_time, self.from\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1626) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L821)

<a id="op-4e805c318484dc"></a>
### Timesheet Detail.update billing hours

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_update_billing_hours`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.is\_billable.
  - Set self.billing\_hours from 0.
  - Return no value.
- If flt(self.billing\_hours) equals 0.0.
  - Set self.billing\_hours from self.hours.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L1728) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L824)

<a id="op-659a19fd7dc261"></a>
### Timesheet Detail.update cost

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_update_cost`

**Inputs** self, employee, currency = no value, exchange\_rate = 1.0.

**Local steps**

- Bind dependencies \_get\_activity\_cost.
- Evaluate self.update\_billing\_hours().
- Set needs\_rate from (not flt(self.costing\_rate) or (self.is\_billable and not flt(self.billing\_rate))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not flt(self.costing\_rate) → (self.is\_billable and not flt(self.billing\_rate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_billable → not flt(self.billing\_rate).
- Set rate from \_get\_activity\_cost(employee, self.activity\_type, currency) when (self.activity\_type and needs\_rate), otherwise mapping().
  - Value choice on (self.activity\_type and needs\_rate) — true gives \_get\_activity\_cost(employee, self.activity\_type, currency), false gives mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.activity\_type → needs\_rate.
- Set self.billing\_rate from (flt(self.billing\_rate) or flt(rate.get(“billing\_rate”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.billing\_rate) → flt(rate.get(“billing\_rate”)).
- Set self.costing\_rate from (flt(self.costing\_rate) or flt(rate.get(“costing\_rate”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.costing\_rate) → flt(rate.get(“costing\_rate”)).
- Set self.billing\_amount from (self.billing\_rate × flt(self.billing\_hours)).
- Set self.costing\_amount from (self.costing\_rate × flt(self.hours)).
- Set exchange\_rate from (flt(exchange\_rate) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(exchange\_rate) → 1.0.
- Set self.base\_billing\_rate from flt((self.billing\_rate × exchange\_rate), self.precision(“base\_billing\_rate”)).
- Set self.base\_costing\_rate from flt((self.costing\_rate × exchange\_rate), self.precision(“base\_costing\_rate”)).
- Set self.base\_billing\_amount from flt((self.billing\_amount × exchange\_rate), self.precision(“base\_billing\_amount”)).
- Set self.base\_costing\_amount from flt((self.costing\_amount × exchange\_rate), self.precision(“base\_costing\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update billing hours](operations-016.md#op-4e805c318484dc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L825)

<a id="op-be0121493033a2"></a>
### Timesheet Detail.validate dates

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Hours value must be greater than zero.”.format(self.idx) · validation helper — translated “To Time cannot be before from date”.

**Local steps**

- If flt(self.hours) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Row {0}: Hours value must be greater than zero.”.format(self.idx)).
- If (self.from\_time and self.to\_time and time\_diff\_in\_hours(self.to\_time, self.from\_time) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_time → self.to\_time → time\_diff\_in\_hours(self.to\_time, self.from\_time) &lt; 0.
  - Call the validation error handler Platform.throw(translated “To Time cannot be before from date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L827)

<a id="op-62b557d8c00654"></a>
### Timesheet Detail.validate parent project

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_validate_parent_project`

**Inputs** self, parent\_project.

**Explicit failure paths** validation helper — translated “Row {0}: Project must be same as the one set in the Timesheet: {1}.”.format(self.idx, parent\_project).

**Local steps**

- If (parent\_project and parent\_project differs from self.project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_project → parent\_project differs from self.project.
  - Call the validation error handler Platform.throw(translated “Row {0}: Project must be same as the one set in the Timesheet: {1}.”.format(self.idx, parent\_project)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L2749) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L828)

<a id="op-3acef95c66d497"></a>
### Timesheet Detail.validate task project

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_validate_task_project`

**Inputs** self.

**Record and data access** read “Task” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Task {1} does not belong to Project {2}”.format(self.idx, Platform.bold(self.task), Platform.bold(self.project)).

**Local steps**

- If (self.task and self.project).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.task → self.project.
  - Set task\_project from Platform.db.get\_value(“Task”, self.task, “project”).
  - If (task\_project and task\_project differs from self.project).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in task\_project → task\_project differs from self.project.
    - Call the validation error handler Platform.throw(translated “Row {0}: Task {1} does not belong to Project {2}”.format(self.idx, Platform.bold(self.task), Platform.bold(self.project))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L2894) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L829)

<a id="op-bd6d37d79b7555"></a>
### Timesheet Detail.validate activity type

`operation_enterprise_binding_enterprise_projects_doctype_timesheet_detail_timesheet_detail_timesheetdetail_validate_activity_type`

**Inputs** self.

**Record and data access** read “Activity Type” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Activity Type {1} is disabled”.format(self.idx, Platform.bold(self.activity\_type)).

**Local steps**

- If (self.activity\_type and Platform.get\_cached\_value(“Activity Type”, self.activity\_type, “disabled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.activity\_type → Platform.get\_cached\_value(“Activity Type”, self.activity\_type, “disabled”).
  - Call the validation error handler Platform.throw(translated “Row {0}: Activity Type {1} is disabled”.format(self.idx, Platform.bold(self.activity\_type))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Activity Type”, self.activity\_type, “disabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L243) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1368)

<a id="op-626b89f4525643"></a>
### Timesheet Detail.validate billing hours

`operation_enterprise_projects_record_definitions_timesheet_detail_business_behavior_timesheet_detail_validate_billing_hours`

**Inputs** self.

**State and service calls** msgprint with translated “Warning - Row {0}: Billing Hours are more than Actual Hours”.format(self.idx).

**Local steps**

- If flt(self.billing\_hours) &gt; flt(self.hours).
  - Evaluate Platform.msgprint(translated “Warning - Row {0}: Billing Hours are more than Actual Hours”.format(self.idx), indicator = “orange”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L3157) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L826)

## Service · Utils

<a id="op-c50d773153ee12"></a>
### Query task

`operation_enterprise_projects_utils_business_behavior_query_task`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, Task).format(searchfield, “%s”, “%s”, match\_conditions, …).

**Explicit results** Platform.db.sql(query text (SELECT, Task).format(searchfield, “%s”, “%s”, match\_conditions, …), tuple(search\_string, search\_string, order\_by\_string, order\_by\_string, …)).

**Local steps**

- Bind dependencies build\_match\_conditions.
- Set search\_string from (“%%%s%%” modulo or format txt).
- Set order\_by\_string from (“%s%%” modulo or format txt).
- Set match\_conditions from build\_match\_conditions(“Task”).
- Set match\_conditions from formatted text and ({match\_conditions}) when match\_conditions, otherwise empty text.
  - Value choice on match\_conditions — true gives formatted text and ({match\_conditions}), false gives empty text.
- Return Platform.db.sql(query text (SELECT, Task).format(searchfield, “%s”, “%s”, match\_conditions, …), tuple(search\_string, search\_string, order\_by\_string, order\_by\_string, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L880)
