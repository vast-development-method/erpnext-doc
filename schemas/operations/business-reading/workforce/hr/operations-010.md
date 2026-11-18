# Employment and attendance · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Employee hours utilization based on timesheet

<a id="op-5e30789403d073"></a>
### Employee Hours Report.set employee department and name

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_set_employee_department_and_name`

**Inputs** self.

**Record and data access** read “Employee” via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.stats\_by\_employee.
  - Return no value.
- Set employee\_details from mapping of employee at “name” → employee for employee drawn from Platform.get\_all(“Employee”, filters = mapping(“name” → list(“in”, list(self.stats\_by\_employee))), fields = list(“name”, “employee\_name”, “d ….
  - Draw employee from Platform.get\_all(“Employee”, filters = mapping(“name” → list(“in”, list(self.stats\_by\_employee))), fields = list(“name”, “employee\_name”, “department”)).
- For each tuple(emp, stats) in self.stats\_by\_employee.items().
  - Set employee from employee\_details.get(emp).
  - Set stats at “employee\_name” from employee.get(“employee\_name”) when employee, otherwise no value.
    - Value choice on employee — true gives employee.get(“employee\_name”), false gives no value.
  - Set stats at “department” from employee.get(“department”) when employee, otherwise no value.
    - Value choice on employee — true gives employee.get(“department”), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L4252) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1705) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L311)

<a id="op-9b520b294e23f2"></a>
### Employee Hours Report.calculate utilizations

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_calculate_utilizations`

**Inputs** self.

**Local steps**

- Set TOTAL\_HOURS from flt((self.standard\_working\_hours × self.day\_span), 2).
- For each tuple(\_\_, data) in self.stats\_by\_employee.items().
  - Set data at “total\_hours” from TOTAL\_HOURS.
  - Set data at “untracked\_hours” from flt(((TOTAL\_HOURS − data at “billed\_hours”) − data at “non\_billed\_hours”), 2).
  - If data at “untracked\_hours” &lt; 0.
    - Set data at “untracked\_hours” from 0.0.
  - Set data at “per\_util” from flt((((data at “billed\_hours” + data at “non\_billed\_hours”) ÷ TOTAL\_HOURS) × 100), 2).
  - Set data at “per\_util\_billed\_only” from flt(((data at “billed\_hours” ÷ TOTAL\_HOURS) × 100), 2).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L4646) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1695) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L301)

<a id="op-845474132ab91b"></a>
### Employee Hours Report.generate report summary

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_report_summary`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.report\_summary from list().
- If not self.data.
  - Return no value.
- Set avg\_utilization from 0.0.
- Set avg\_utilization\_billed\_only from 0.0.
- Set tuple(total\_billed, total\_non\_billed) from tuple(0.0, 0.0).
- Set total\_untracked from 0.0.
- For each row in self.data.
  - Update avg\_utilization using + row at “per\_util”.
  - Update avg\_utilization\_billed\_only using + row at “per\_util\_billed\_only”.
  - Update total\_billed using + row at “billed\_hours”.
  - Update total\_non\_billed using + row at “non\_billed\_hours”.
  - Update total\_untracked using + row at “untracked\_hours”.
- Update avg\_utilization using ÷ len(self.data).
- Set avg\_utilization from flt(avg\_utilization, 2).
- Update avg\_utilization\_billed\_only using ÷ len(self.data).
- Set avg\_utilization\_billed\_only from flt(avg\_utilization\_billed\_only, 2).
- Set THRESHOLD\_PERCENTAGE from 70.0.
- Set self.report\_summary from list(mapping(“value” → formatted text {avg\_utilization}%, “indicator” → “Red” when avg\_utilization &lt; THRESHOLD\_PERCENTAGE, otherwise “Green”, “label” → translated “Avg Utilization”, “datatype” → “Percentag ….
  - Value choice on avg\_utilization &lt; THRESHOLD\_PERCENTAGE — true gives “Red”, false gives “Green”.
  - Value choice on avg\_utilization\_billed\_only &lt; THRESHOLD\_PERCENTAGE — true gives “Red”, false gives “Green”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L5031) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1701) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L307)

<a id="op-d09d9c26568ead"></a>
### Employee Hours Report.generate chart data

`operation_workforce_human_resources_report_employee_hours_utilization_based_on_timesheet_business_behavior_employee_hours_report_generate_chart_data`

**Inputs** self.

**Local steps**

- Set self.chart from mapping().
- Set labels from list().
- Set billed\_hours from list().
- Set non\_billed\_hours from list().
- Set untracked\_hours from list().
- For each row in self.data.
  - Evaluate labels.append(row.get(“employee\_name”)).
  - Evaluate billed\_hours.append(row.get(“billed\_hours”)).
  - Evaluate non\_billed\_hours.append(row.get(“non\_billed\_hours”)).
  - Evaluate untracked\_hours.append(row.get(“untracked\_hours”)).
- Set self.chart from mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Billed Hours”, “values” → billed\_hours at slice no value to 30), mapping(“name” → translat ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0083.json#L5786) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1697) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L303)

## Report · Employee leave balance

<a id="op-265af70970c467"></a>
### Execute

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**Explicit results** tuple(columns, data, no value, charts).

**Explicit failure paths** validation helper — translated “"From Date" can not be greater than or equal to "To Date"”.

**Local steps**

- If filters.to\_date ≤ filters.from\_date.
  - Call the validation error handler Platform.throw(translated “"From Date" can not be greater than or equal to "To Date"”).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Set charts from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, charts).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L1987) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1718) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L324)

<a id="op-9dba07fd26b5b7"></a>
### Get columns

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Leave Type”, “fieldtype” → “Link”, “fieldname” → “leave\_type”, “width” → 200, …), mapping(“label” → translated “Employee”, “fieldtype” → “Link”, “fieldname” → “employee”, ….

**Local steps**

- Return list(mapping(“label” → translated “Leave Type”, “fieldtype” → “Link”, “fieldname” → “leave\_type”, “width” → 200, …), mapping(“label” → translated “Employee”, “fieldtype” → “Link”, “fieldname” → “employee”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L2208) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1723) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L329)

<a id="op-db7cdb19f1a090"></a>
### Get data

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_data`

**Inputs** filters.

**Declared result** list.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** data.

**Local steps**

- Set leave\_types from get\_leave\_types().
- Set active\_employees from get\_employees(filters).
- Set pairs\_with\_entries from get\_pairs\_with\_ledger\_entries(active\_employees, filters.to\_date).
- Set precision from cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)).
- Set consolidate\_leave\_types from (len(active\_employees) &gt; 1 and filters.consolidate\_leave\_types).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(active\_employees) &gt; 1 → filters.consolidate\_leave\_types.
- Set data from list().
- For each leave\_type in leave\_types.
  - Set rows from list().
  - For each employee in active\_employees.
    - If tuple(employee.name, leave\_type) does not belong to pairs\_with\_entries.
      - Continue with the next iteration or loop test.
    - Set balance from get\_balance\_details(employee.name, leave\_type, filters, precision).
    - If not any(balance.values()).
      - Continue with the next iteration or loop test.
    - Set row from Platform.\_dict() when consolidate\_leave\_types, otherwise Platform.\_dict(mapping(“leave\_type” → leave\_type)).
      - Value choice on consolidate\_leave\_types — true gives Platform.\_dict(), false gives Platform.\_dict(mapping(“leave\_type” → leave\_type)).
    - Evaluate row.update(employee = employee.name, employee\_name = employee.employee\_name, expanded names balance, indent = 1).
    - Evaluate rows.append(row).
  - If (consolidate\_leave\_types and rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in consolidate\_leave\_types → rows.
    - Evaluate data.append(mapping(“leave\_type” → leave\_type)).
  - Evaluate data.extend(rows).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L76) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1724) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L330)

<a id="op-328380992126ff"></a>
### Get balance details

`operation_workforce_binding_workforce_hr_report_employee_leave_balance_employee_leave_balance_get_balance_details`

**Inputs** employee, leave\_type, filters, precision.

**Declared result** dict.

**Explicit results** mapping(“leaves\_allocated” → flt(allocated\_leaves, precision), “leaves\_expired” → leaves\_expired, “opening\_balance” → flt(opening, precision), “leaves\_taken” → flt(leaves\_taken, precision), …).

**Local steps**

- Set leaves\_taken from (get\_leaves\_for\_period(employee, leave\_type, filters.from\_date, filters.to\_date) × negative 1).
- Set tuple(new\_allocation, expired\_leaves, carry\_forwarded\_leaves) from get\_allocated\_and\_expired\_leaves(filters.from\_date, filters.to\_date, employee, leave\_type).
- Set on\_allocation\_boundary from is\_opening\_balance\_on\_allocation\_boundary(employee, leave\_type, filters).
- Set opening from get\_opening\_balance(employee, leave\_type, filters, carry\_forwarded\_leaves, …).
- Set allocated\_leaves from (new\_allocation + carry\_forwarded\_leaves).
- If on\_allocation\_boundary.
  - Update allocated\_leaves using − carry\_forwarded\_leaves.
- Set leaves\_expired from flt(expired\_leaves, precision).
- Set closing from ((allocated\_leaves + opening) − (leaves\_expired + leaves\_taken)).
- Return mapping(“leaves\_allocated” → flt(allocated\_leaves, precision), “leaves\_expired” → leaves\_expired, “opening\_balance” → flt(opening, precision), “leaves\_taken” → flt(leaves\_taken, precision), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L152) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L203) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L203)

<a id="op-f7bc7de80ff94b"></a>
### Get pairs with ledger entries

`operation_workforce_binding_workforce_hr_report_employee_leave_balance_employee_leave_balance_get_pairs_with_ledger_entries`

**Inputs** employees, to\_date.

**Declared result** set at tuple at tuple(str, str).

**Explicit results** set() · set of tuple(pair) for pair drawn from pairs.

**Local steps**

- If not employees.
  - Return set().
- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set pairs from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contrac ….run().
  - Draw employee from employees.
- Return set of tuple(pair) for pair drawn from pairs.
  - Draw pair from pairs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L153) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L204) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L204)

<a id="op-b17a82f5c0a08c"></a>
### Get leave types

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_leave_types`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).select(LeaveType.name).orderby(LeaveType.name).run(pluck = “name”).

**Local steps**

- Set LeaveType from Platform.qb.DocType(“Leave Type”).
- Return nested operand in the contract(nested operand in the contract).select(LeaveType.name).orderby(LeaveType.name).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L3998) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1728) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L334)

<a id="op-f22c6ad6401541"></a>
### Get employees

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_employees`

**Inputs** filters.

**Declared result** list at dict.

**Record and data access** read “Employee” via get\_list.

**Explicit results** Platform.get\_list(“Employee”, filters = conditions, fields = list(“name”, “employee\_name”, “department”)).

**Local steps**

- Set conditions from mapping().
- For each field in list(“company”, “department”).
  - If filters.get(field).
    - Set conditions at field from filters.get(field).
- If filters.get(“employee”).
  - Set conditions at “name” from filters.get(“employee”).
- If filters.get(“employee\_status”).
  - Set conditions at “status” from filters.get(“employee\_status”).
- Return Platform.get\_list(“Employee”, filters = conditions, fields = list(“name”, “employee\_name”, “department”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L4168) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1726) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L332)

<a id="op-b3cc4b231741e8"></a>
### Get opening balance

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_opening_balance`

**Inputs** employee, leave\_type, filters, carry\_forwarded\_leaves, on\_allocation\_boundary.

**Declared result** float.

**Explicit results** opening\_balance.

**Local steps**

- Set opening\_balance\_date from add\_days(filters.from\_date, negative 1).
- If on\_allocation\_boundary.
  - Set opening\_balance from carry\_forwarded\_leaves.
- Otherwise.
  - Set opening\_balance from get\_leave\_balance\_on(employee, leave\_type, opening\_balance\_date).
- Return opening\_balance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L4552) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1729) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L335)

<a id="op-47be8425c631c7"></a>
### Is opening balance on allocation boundary

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_is_opening_balance_on_allocation_boundary`

**Inputs** employee, leave\_type, filters.

**Declared result** bool.

**Explicit results** bool((allocation and allocation.get(“to\_date”) and opening\_balance\_date and getdate(allocation.get(“to\_date”)) equals getdate(opening\_balance\_date))).

**Local steps**

- Set opening\_balance\_date from add\_days(filters.from\_date, negative 1).
- Set allocation from get\_previous\_allocation(filters.from\_date, leave\_type, employee).
- Return bool((allocation and allocation.get(“to\_date”) and opening\_balance\_date and getdate(allocation.get(“to\_date”)) equals getdate(opening\_balance\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocation → allocation.get(“to\_date”) → opening\_balance\_date → getdate(allocation.get(“to\_date”)) equals getdate(opening\_balance\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L4743) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1730) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L336)

<a id="op-deae7c43ff0c76"></a>
### Get allocated and expired leaves

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_allocated_and_expired_leaves`

**Inputs** from\_date, to\_date, employee, leave\_type.

**Declared result** tuple at tuple(float, float, float).

**Explicit results** tuple(new\_allocation, expired\_leaves, carry\_forwarded\_leaves).

**Local steps**

- Set new\_allocation from 0.
- Set expired\_leaves from 0.
- Set carry\_forwarded\_leaves from 0.
- Set new\_allocation from get\_allocated\_leaves(from\_date, to\_date, employee, leave\_type).
- Set expired\_leaves from get\_expired\_leaves(from\_date, to\_date, employee, leave\_type).
- Set carry\_forwarded\_leaves from get\_cf\_leaves(from\_date, to\_date, employee, leave\_type).
- Return tuple(new\_allocation, expired\_leaves, carry\_forwarded\_leaves).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L5001) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1719) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L325)

<a id="op-4fb595c4df8a76"></a>
### Get allocated leaves

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_allocated_leaves`

**Inputs** from\_date, to\_date, employee, leave\_type.

**Explicit results** allocated\_leaves when allocated\_leaves, otherwise 0.0.

**Local steps**

- Set ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set allocated\_leaves from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise and nes … at 0.
- Return allocated\_leaves when allocated\_leaves, otherwise 0.0.
  - Value choice on allocated\_leaves — true gives allocated\_leaves, false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L5271) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1720) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L326)

<a id="op-42f50d2edc92da"></a>
### Get expired leaves

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_expired_leaves`

**Inputs** from\_date, to\_date, employee, leave\_type.

**Explicit results** expired\_leaves when expired\_leaves, otherwise 0.0.

**Local steps**

- Set ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set expired\_leaves from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
- Return expired\_leaves when expired\_leaves, otherwise 0.0.
  - Value choice on expired\_leaves — true gives expired\_leaves, false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L5673) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1727) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L333)

<a id="op-ad57678cfffaea"></a>
### Get cf leaves

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_cash_flow_leaves`

**Inputs** from\_date, to\_date, employee, leave\_type.

**Explicit results** cf\_leaves when cf\_leaves, otherwise 0.0.

**Local steps**

- Set ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set cf\_leaves from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise and nes … at 0.
- Return cf\_leaves when cf\_leaves, otherwise 0.0.
  - Value choice on cf\_leaves — true gives cf\_leaves, false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L6074) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1721) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L327)

<a id="op-fec4a9e92a0dc0"></a>
### Get chart data

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_chart_data`

**Inputs** data, filters.

**Declared result** dict.

**Explicit results** no value · chart.

**Local steps**

- Set labels from list().
- Set datasets from list().
- Set employee\_data from data.
- If not data.
  - Return no value.
- If (data and filters.employee).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → filters.employee.
  - Evaluate get\_dataset\_for\_chart(employee\_data, datasets, labels).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “bar”, “colors” → list(“#456789”, “#EE8888”, “#7E77BF”)).
- Return chart.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L6458) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1722) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L328)

<a id="op-1edc10d9842b11"></a>
### Get dataset for chart

`operation_workforce_human_resources_report_employee_leave_balance_business_behavior_get_dataset_for_chart`

**Inputs** employee\_data, datasets, labels.

**Declared result** list.

**Local steps**

- Set leaves from list().
- Set employee\_data from sorted(employee\_data, key = deferred anonymous expression).
- For each tuple(key, group) in groupby(employee\_data, deferred anonymous expression).
  - For each grp in group.
    - If grp.closing\_balance.
      - Evaluate leaves.append(Platform.\_dict(mapping(“leave\_type” → grp.leave\_type, “closing\_balance” → grp.closing\_balance))).
  - If leaves.
    - Evaluate labels.append(key).
- For each leave in leaves.
  - Evaluate datasets.append(mapping(“name” → leave.leave\_type, “values” → list(leave.closing\_balance))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0084.json#L6720) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1725) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L331)

## Report · Employee leave balance summary

<a id="op-c327b000e2fbc5"></a>
### Execute

`operation_workforce_human_resources_report_employee_leave_balance_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set LeaveType from Platform.qb.DocType(“Leave Type”).
- Set leave\_types from nested operand in the contract(nested operand in the contract).select(LeaveType.name).orderby(LeaveType.name, order = Platform.qb.asc).run(pluck = “name”).
- Set columns from get\_columns(leave\_types).
- Set data from get\_data(filters, leave\_types).
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0085.json#L5191) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1731) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L337)

<a id="op-bc582a9cfaa051"></a>
### Get columns

`operation_workforce_human_resources_report_employee_leave_balance_summary_business_behavior_get_columns`

**Inputs** leave\_types.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Employee” + “:Link/Employee:150”), (translated “Employee Name” + “::200”), (translated “Department” + “:Link/Department:150”)).
- For each leave\_type in leave\_types.
  - Evaluate columns.append((translated leave\_type + “:Float:160”)).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0085.json#L5459) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1732) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L338)

<a id="op-818dfefbd2c424"></a>
### Get conditions

`operation_workforce_human_resources_report_employee_leave_balance_summary_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from mapping(“company” → filters.company).
- If filters.get(“employee\_status”).
  - Evaluate conditions.update(mapping(“status” → filters.get(“employee\_status”))).
- If filters.get(“department”).
  - Evaluate conditions.update(mapping(“department” → filters.get(“department”))).
- If filters.get(“employee”).
  - Evaluate conditions.update(mapping(“employee” → filters.get(“employee”))).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0085.json#L5657) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1733) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L339)

<a id="op-e8e4c2019addab"></a>
### Get data

`operation_workforce_human_resources_report_employee_leave_balance_summary_business_behavior_get_data`

**Inputs** filters, leave\_types.

**Record and data access** read “Employee” via get\_list.

**Explicit results** data.

**Local steps**

- Set conditions from get\_conditions(filters).
- Set active\_employees from Platform.get\_list(“Employee”, filters = conditions, fields = list(“name”, “employee\_name”, “department”, “user\_id”)).
- Set data from list().
- For each employee in active\_employees.
  - Set row from list(employee.name, employee.employee\_name, employee.department).
  - Set available\_leave from get\_leave\_details(employee.name, filters.date).
  - For each leave\_type in leave\_types.
    - Set remaining from 0.
    - If leave\_type belongs to available\_leave at “leave\_allocation”.
      - Set remaining from available\_leave at “leave\_allocation” at leave\_type at “remaining\_leaves”.
    - Update row using + list(remaining).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0085.json#L5998) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1734) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L340)

## Record · Employee onboarding

[Record definition](../../../../data/record-types/employee_onboarding.json)

<a id="op-5749e75348c761"></a>
### Employee Onboarding.validate

`operation_workforce_human_resources_record_definitions_employee_onboarding_business_behavior_employee_onboarding_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.set\_employee().
- Evaluate self.validate\_duplicate\_employee\_onboarding().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set employee](operations-011.md#op-585233c5e91342), [validate duplicate employee onboarding](operations-011.md#op-1a78489534abbf).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0023.json#L5688) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L606) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L586)
