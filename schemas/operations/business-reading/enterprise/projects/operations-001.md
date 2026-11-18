# Projects and time · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Activity cost

[Record definition](../../../../data/record-types/activity_cost.json)

<a id="op-8703b6cdc6991e"></a>
### Activity Cost.validate

`operation_enterprise_projects_record_definitions_activity_cost_business_behavior_activity_cost_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_title().
- Evaluate self.check\_unique().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set title](operations-001.md#op-de8b24d31c85dd), [check unique](operations-001.md#op-f362adff553b3a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L6506) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L662)

<a id="op-de8b24d31c85dd"></a>
### Activity Cost.set title

`operation_enterprise_projects_record_definitions_activity_cost_business_behavior_activity_cost_set_title`

**Inputs** self.

**Local steps**

- If self.employee.
  - Set self.title from translated “{0} for {1}”.format(self.employee\_name, self.activity\_type).
- Otherwise.
  - Set self.title from self.activity\_type.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L661)

<a id="op-f362adff553b3a"></a>
### Activity Cost.check unique

`operation_enterprise_projects_record_definitions_activity_cost_business_behavior_activity_cost_check_unique`

**Inputs** self.

**Record and data access** read “Activity Cost” via exists · execute query text (SELECT, Activity Cost).

**Explicit failure paths** validation helper with DuplicationError — translated “Activity Cost exists for Employee {0} against Activity Type - {1}”.format(self.employee, self.activity\_type) · validation helper with DuplicationError — translated “Default Activity Cost exists for Activity Type - {0}”.format(self.activity\_type).

**Local steps**

- If self.employee.
  - If Platform.db.exists(“Activity Cost”, mapping(“employee” → self.employee, “activity\_type” → self.activity\_type, “name” → list(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “Activity Cost exists for Employee {0} against Activity Type - {1}”.format(self.employee, self.activity\_type), DuplicationError).
- Otherwise.
  - If Platform.db.sql(query text (SELECT, Activity Cost), tuple(self.activity\_type, self.name)).
    - Call the validation error handler Platform.throw(translated “Default Activity Cost exists for Activity Type - {0}”.format(self.activity\_type), DuplicationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L660)

## Report · Daily timesheet summary

<a id="op-0789c7633b3fe2"></a>
### Execute

`operation_enterprise_projects_report_daily_timesheet_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Otherwise.
  - If (filters.get(“from\_date”) or filters.get(“to\_date”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
    - Set filters at “from\_time” from “00:00:00”.
    - Set filters at “to\_time” from “24:00:00”.
- Set columns from get\_column().
- Set conditions from get\_conditions(filters).
- Set data from get\_data(conditions, filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L847)

<a id="op-481e084756cbd4"></a>
### Get column

`operation_enterprise_projects_report_daily_timesheet_summary_business_behavior_get_column`

**Inputs** no declared parameters.

**Explicit results** list((translated “Timesheet” + “:Link/Timesheet:120”), (translated “Employee” + “::150”), (translated “Employee Name” + “::150”), (translated “From Datetime” + “::140”), …).

**Local steps**

- Return list((translated “Timesheet” + “:Link/Timesheet:120”), (translated “Employee” + “::150”), (translated “Employee Name” + “::150”), (translated “From Datetime” + “::140”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L3446) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L848)

<a id="op-5c59a8cf975a5b"></a>
### Get data

`operation_enterprise_projects_report_daily_timesheet_summary_business_behavior_get_data`

**Inputs** conditions, filters.

**State and service calls** execute a supplied database query.

**Explicit results** time\_sheet.

**Local steps**

- Set time\_sheet from Platform.db.sql((query text (SELECT, Timesheet Detail) modulo or format conditions), filters, as\_list = 1).
- Return time\_sheet.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L849)

<a id="op-13e085b761bfef"></a>
### Get conditions

`operation_enterprise_binding_enterprise_projects_report_daily_timesheet_summary_daily_timesheet_summary_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from “′tabTimesheet′.docstatus = 1”.
- If filters.get(“from\_date”).
  - Update conditions using + “ and ′tabTimesheet Detail′.from\_time &gt;= timestamp(%(from\_date)s, %(from\_time)s)”.
- If filters.get(“to\_date”).
  - Update conditions using + “ and ′tabTimesheet Detail′.from\_time &lt; timestamp(%(to\_date)s, %(to\_time)s)”.
- Set match\_conditions from build\_match\_conditions(“Timesheet”).
- If match\_conditions.
  - Update conditions using + (“ and (%s)” modulo or format match\_conditions).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L252) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1377)

## Report · Delayed tasks summary

<a id="op-acd865efa5cf1b"></a>
### Execute

`operation_enterprise_projects_report_delayed_tasks_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, charts).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_columns().
- Set charts from get\_chart\_data(data).
- Return tuple(columns, data, no value, charts).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L851)

<a id="op-ab37ea0150407d"></a>
### Get data

`operation_enterprise_projects_report_delayed_tasks_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Task” via get\_list.

**Explicit results** tasks.

**Local steps**

- Set conditions from get\_conditions(filters).
- Set tasks from Platform.get\_list(“Task”, filters = conditions, fields = list(“name”, “subject”, “project”, “exp\_start\_date”, …), order\_by = “creation”).
- For each task in tasks.
  - If task.exp\_end\_date.
    - If task.completed\_on.
      - Set task.delay from date\_diff(task.completed\_on, task.exp\_end\_date).
    - Otherwise.
      - If task.status equals “Completed”.
        - Set task.delay from 0.
      - Otherwise.
        - Set task.delay from date\_diff(nowdate(), task.exp\_end\_date).
  - Otherwise.
    - Set task.delay from 0.
  - Set task.status from translated task.status.
  - Set task.priority from translated task.priority.
- Evaluate tasks.sort(key = deferred anonymous expression, reverse = true).
- Return tasks.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L855)

<a id="op-0f7b9c8f803588"></a>
### Get conditions

`operation_enterprise_projects_report_delayed_tasks_summary_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from Platform.\_dict(is\_template = 0, status = list(“!=”, “Cancelled”)).
- Set keys from list(“priority”, “status”, “project”).
- For each key in keys.
  - If filters.get(key).
    - Set conditions at key from filters.get(key).
- If filters.get(“from\_date”).
  - Set conditions.exp\_end\_date from list(“&gt;=”, filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set conditions.exp\_start\_date from list(“&lt;=”, filters.get(“to\_date”)).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L854)

<a id="op-ca4f92d3f89137"></a>
### Get chart data

`operation_enterprise_projects_report_delayed_tasks_summary_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** charts.

**Local steps**

- Set tuple(delay, on\_track) from tuple(0, 0).
- For each entry in data.
  - If entry.get(“delay”) &gt; 0.
    - Set delay from (delay + 1).
  - Otherwise.
    - Set on\_track from (on\_track + 1).
- Set labels from list().
- Set datasets from list().
- Set colors from list().
- If on\_track.
  - Evaluate labels.append(translated “On Track”).
  - Evaluate datasets.append(on\_track).
  - Evaluate colors.append(“#84D5BA”).
- If delay.
  - Evaluate labels.append(translated “Delayed”).
  - Evaluate datasets.append(delay).
  - Evaluate colors.append(“#CB4B5F”).
- Set charts from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Delayed”, “values” → datasets))), “type” → “percentage”, “colors” → colors).
- Return charts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0610.json#L5938) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L852)

<a id="op-ade9d666be4131"></a>
### Get columns

`operation_enterprise_projects_report_delayed_tasks_summary_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Task”, “options” → “Task”, …), mapping(“fieldname” → “subject”, “fieldtype” → “Data”, “label” → translated “Subject”, “width”  ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0611.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L853)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-1173ec00668ade"></a>
### Get project accounts

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_get_project_accounts`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** ProjectAccounts(project).build().

**Local steps**

- Evaluate check\_access(project).
- Evaluate Platform.has\_permission(“GL Entry”, “read”, throw = true).
- Return ProjectAccounts(project).build().

**Values supplied outside this operation** effective access from Platform.has\_permission(“GL Entry”, “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1167)

<a id="op-c6ae898e148247"></a>
### Get ledger entries

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_get_ledger_entries`

**Inputs** project, root\_type = no value, start = 0, page\_length = 20.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list at dict.

**Record and data access** read “Project” via get\_value · read “GL Entry” via get\_list.

**Explicit results** Platform.get\_list(“GL Entry”, filters = filters, fields = LEDGER\_FIELDS, order\_by = “posting\_date desc, creation desc”, offset = max(start, 0), …).

**Local steps**

- Evaluate check\_access(project).
- Set company from Platform.db.get\_value(“Project”, project, “company”).
- Set period from current\_fiscal\_year(company).
- Set filters from mapping(“project” → project, “company” → company, “is\_cancelled” → 0, “posting\_date” → list(“between”, list(period.year\_start\_date, period.year\_end\_date))).
- Set filters at “account” from list(“in”, profit\_and\_loss\_accounts(company, root\_type)).
- Return Platform.get\_list(“GL Entry”, filters = filters, fields = LEDGER\_FIELDS, order\_by = “posting\_date desc, creation desc”, offset = max(start, 0), …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1166)

<a id="op-cb6a8d8ed48772"></a>
### Profit and loss accounts

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_profit_and_loss_accounts`

**Inputs** company, root\_type = no value.

**Declared result** list at str.

**Record and data access** read “Account” via get\_all.

**Explicit results** Platform.get\_all(“Account”, filters = filters, pluck = “name”).

**Local steps**

- Set filters from mapping(“company” → company, “report\_type” → “Profit and Loss”).
- If root\_type.
  - Set filters at “root\_type” from root\_type.
- Return Platform.get\_all(“Account”, filters = filters, pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1168)

<a id="op-a14335e7b3ad51"></a>
### Current fiscal year

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_current_fiscal_year`

**Inputs** company.

**Declared result** Platform.\_dict.

**Explicit results** get\_fiscal\_year(getdate(), company = company, as\_dict = true).

**Local steps**

- Return get\_fiscal\_year(getdate(), company = company, as\_dict = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1165)

<a id="op-16d6937962260b"></a>
### Project Accounts.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_init`

**Inputs** self, project.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set self.project from Platform.db.get\_value(“Project”, project, list(“name”, “company”), as\_dict = true).
- Set self.fiscal\_year from current\_fiscal\_year(self.project.company).
- Set self.can\_read\_budgets from can\_read(“Budget”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1176)

<a id="op-0987545edbd730"></a>
### Project Accounts.build

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_build`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** mapping(“project” → self.project.name, “company” → self.project.company, “currency” → Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”), “fiscal\_year” → self.fiscal\_year.name, …).

**Local steps**

- Set rows from list of self.account\_row(account) for account drawn from self.accounts.
  - Draw account from self.accounts.
- Return mapping(“project” → self.project.name, “company” → self.project.company, “currency” → Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”), “fiscal\_year” → self.fiscal\_year.name, …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_create(“Budget”) → can\_submit(“Budget”).

**Methods declared on this owner** [account row](operations-001.md#op-46ba5b79851bf9), [monthly](operations-002.md#op-d7d1bcbc8ad8c4).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L163) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1173)

<a id="op-46ba5b79851bf9"></a>
### Project Accounts.account row

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_account_row`

**Inputs** self, account.

**Declared result** dict.

**Explicit results** mapping(“account” → account.name, “account\_name” → account.account\_name, “root\_type” → account.root\_type, “actual” → spend at “actual”, …).

**Local steps**

- Set sign from negative 1 when account.root\_type equals “Income”, otherwise 1.
  - Value choice on account.root\_type equals “Income” — true gives negative 1, false gives 1.
- Set booked from self.ledger\_totals.get(account.name, mapping()).
- Set budget from self.budgets.get(account.name).
- Set expense from account.root\_type equals “Expense”.
- Set spend from mapping(“actual” → (sign × flt(booked.get(“balance”))), “ordered” → self.ordered.get(account.name, 0) when expense, otherwise 0, “requested” → self.requested.get(account.name, 0) when expense, otherwise 0, ….
  - Value choice on expense — true gives self.ordered.get(account.name, 0), false gives 0.
  - Value choice on expense — true gives self.requested.get(account.name, 0), false gives 0.
- Return mapping(“account” → account.name, “account\_name” → account.account\_name, “root\_type” → account.root\_type, “actual” → spend at “actual”, …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget → budget\_summary(budget, spend).
  - Value choice on expense — true gives account\_status(budget, spend), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1169)

<a id="op-132634f1f219e1"></a>
### Project Accounts.ordered

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ordered`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of account → flt(amount) for tuple(account, amount) drawn from self.ordered\_by\_account().

**Local steps**

- Return mapping of account → flt(amount) for tuple(account, amount) drawn from self.ordered\_by\_account().
  - Draw tuple(account, amount) from self.ordered\_by\_account().

**Methods declared on this owner** [ordered by account](operations-001.md#op-c5e90153b9fb90).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1182)

<a id="op-6df7b5599fe758"></a>
### Project Accounts.requested

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_requested`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of account → flt(amount) for tuple(account, amount) drawn from self.requested\_by\_account().

**Local steps**

- Return mapping of account → flt(amount) for tuple(account, amount) drawn from self.requested\_by\_account().
  - Draw tuple(account, amount) from self.requested\_by\_account().

**Methods declared on this owner** [requested by account](operations-001.md#op-fefb10f8b30ac7).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1185)

<a id="op-c5e90153b9fb90"></a>
### Project Accounts.ordered by account

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_ordered_by_account`

**Inputs** self.

**Declared result** list at tuple at tuple(str, float).

**Explicit results** self.by\_expense\_account(query, item, unbilled, “Purchase Order”).

**Local steps**

- Set tuple(item, order) from tuple(qb.DocType(“Purchase Order Item”), qb.DocType(“Purchase Order”)).
- Set unbilled from ((item.amount − item.billed\_amt) × Coalesce(order.conversion\_rate, 1)).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.status differs from “Closed”).where(item.amount &gt; item.billed\_amt).where(order.transaction\_date at slice  ….
- Return self.by\_expense\_account(query, item, unbilled, “Purchase Order”).

**Methods declared on this owner** [by expense account](operations-001.md#op-67334a92a2f161).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1183)

<a id="op-fefb10f8b30ac7"></a>
### Project Accounts.requested by account

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_requested_by_account`

**Inputs** self.

**Declared result** list at tuple at tuple(str, float).

**Explicit results** self.by\_expense\_account(query, item, unordered, “Material Request”).

**Local steps**

- Set tuple(item, request) from tuple(qb.DocType(“Material Request Item”), qb.DocType(“Material Request”)).
- Set unordered from (((item.stock\_qty − item.ordered\_qty) × item.rate) ÷ item.conversion\_factor).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.status differs from “Stopped”).where(item.stock\_qty &gt; item.ordered\_qty).where(request.transaction\_date at ….
- Return self.by\_expense\_account(query, item, unordered, “Material Request”).

**Methods declared on this owner** [by expense account](operations-001.md#op-67334a92a2f161).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1186)

<a id="op-67334a92a2f161"></a>
### Project Accounts.by expense account

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_accounts_projectaccounts_by_expense_account`

**Inputs** self, query, item, amount, doctype.

**Declared result** list at tuple at tuple(str, float).

**Explicit results** list() · nested operand in the contract(nested operand in the contract).select(item.expense\_account, Sum(amount)).groupby(item.expense\_account).run().

**Local steps**

- If not can\_read(doctype).
  - Return list().
- Set readable from Platform.qb.get\_query(doctype, fields = list(“name”), ignore\_permissions = false).
- Return nested operand in the contract(nested operand in the contract).select(item.expense\_account, Sum(amount)).groupby(item.expense\_account).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L164) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1174)
