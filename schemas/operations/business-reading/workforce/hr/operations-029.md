# Employment and attendance · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave block list

[Record definition](../../../../data/record-types/leave_block_list.json)

<a id="op-e48f9b7224a0a2"></a>
### Get applicable block lists

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_get_applicable_block_lists`

**Inputs** employee = no value, company = no value, all\_lists = false, leave\_type = no value.

**Record and data access** read “Employee” via get\_value · read “Leave Block List” via get\_all · read “Department” via get\_value · read “Leave Block List” via get\_value.

**Explicit results** list(set(block\_lists)).

**Local steps**

- Set block\_lists from list().
- Bind local operation add\_block\_list for subsequent calls.
- If not employee.
  - Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user)).
- If (not company and employee).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not company → employee.
  - Set company from Platform.db.get\_value(“Employee”, employee, “company”).
- If company.
  - Set conditions from mapping(“applies\_to\_all\_departments” → 1, “company” → company).
  - If leave\_type.
    - Set conditions at “leave\_type” from list(“IN”, tuple(leave\_type, empty text, no value)).
  - Evaluate add\_block\_list(Platform.db.get\_all(“Leave Block List”, filters = conditions, pluck = “name”)).
- If employee.
  - Set department from Platform.db.get\_value(“Employee”, employee, “department”).
  - If department.
    - Set block\_list from Platform.db.get\_value(“Department”, department, “leave\_block\_list”).
    - Set block\_list\_leave\_type from Platform.db.get\_value(“Leave Block List”, block\_list, “leave\_type”).
    - If (not block\_list\_leave\_type or not leave\_type or block\_list\_leave\_type equals leave\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not block\_list\_leave\_type → not leave\_type → block\_list\_leave\_type equals leave\_type.
      - Evaluate add\_block\_list(list(block\_list)).
- Return list(set(block\_lists)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L4411) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1261) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1237)

<a id="op-f6dd527d75b9d9"></a>
### Get applicable block lists.add block list

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_get_applicable_block_lists_add_block_list`

**Inputs** block\_list.

**Local steps**

- For each d in block\_list.
  - If (all\_lists or not is\_user\_in\_allow\_list(d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in all\_lists → not is\_user\_in\_allow\_list(d).
    - Evaluate block\_lists.append(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L5185) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1262) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1238)

<a id="op-f9d347c4f3f341"></a>
### Is user in allow list

`operation_workforce_human_resources_record_definitions_leave_block_list_business_behavior_is_user_in_allow_list`

**Inputs** block\_list.

**Record and data access** read “Leave Block List Allow” via get\_value.

**Explicit results** Platform.db.get\_value(“Leave Block List Allow”, mapping(“parent” → block\_list, “allow\_user” → Platform.session.user), “allow\_user”).

**Local steps**

- Return Platform.db.get\_value(“Leave Block List Allow”, mapping(“parent” → block\_list, “allow\_user” → Platform.session.user), “allow\_user”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L5293) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1263) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1239)

<a id="op-739994eeaec2f9"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_block_list_leave_block_list_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_block\_list”, “transactions” → list(mapping(“items” → list(“Department”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_block\_list”, “transactions” → list(mapping(“items” → list(“Department”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L5410) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1267) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1243)

## Record · Leave control panel

[Record definition](../../../../data/record-types/leave_control_panel.json)

<a id="op-d8bf8e8f438139"></a>
### Leave Control Panel.validate fields

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_validate_fields`

**Inputs** self, employees.

**Local steps**

- Set mandatory\_fields from list().
- If self.dates\_based\_on equals “Leave Period”.
  - Evaluate mandatory\_fields.append(“leave\_period”).
- Otherwise.
  - If self.dates\_based\_on equals “Joining Date”.
    - Evaluate mandatory\_fields.append(“to\_date”).
  - Otherwise.
    - Evaluate mandatory\_fields.extend(list(“from\_date”, “to\_date”)).
- If self.allocate\_based\_on\_leave\_policy.
  - Evaluate mandatory\_fields.append(“leave\_policy”).
- Otherwise.
  - Evaluate mandatory\_fields.extend(list(“leave\_type”, “no\_of\_days”)).
- Evaluate validate\_bulk\_tool\_fields(self, mandatory\_fields, employees, “from\_date”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0057.json#L6780) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1281) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1257)

<a id="op-01c268d82e005a"></a>
### Leave Control Panel.allocate leave

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_allocate_leave`

**Inputs** self, employees.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** self.create\_leave\_policy\_assignments(employees) · self.create\_leave\_allocations(employees).

**Local steps**

- Evaluate self.validate\_fields(employees).
- If self.allocate\_based\_on\_leave\_policy.
  - Return self.create\_leave\_policy\_assignments(employees).
- Return self.create\_leave\_allocations(employees).

**Methods declared on this owner** [validate fields](operations-029.md#op-d8bf8e8f438139), [create leave policy assignments](operations-029.md#op-08a8f7c80707b4), [create leave allocations](operations-029.md#op-8c814853543594).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1273) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1249)

<a id="op-8c814853543594"></a>
### Leave Control Panel.create leave allocations

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_create_leave_allocations`

**Inputs** self, employees.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**State and service calls** savepoint savepoint · request new\_doc for “Leave Allocation” · call insert on allocation · call submit on allocation · rollback · 1 additional forms in the steps below.

**Local steps**

- Set tuple(from\_date, to\_date) from self.get\_from\_to\_date().
- Set failure from list().
- Set success from list().
- Set savepoint from “before\_allocation\_submission”.
- For each employee in employees.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Set allocation from Platform.new\_doc(“Leave Allocation”).
    - Set allocation.employee from employee.
    - Set allocation.leave\_type from self.leave\_type.
    - Set allocation.from\_date from (from\_date or Platform.db.get\_value(“Employee”, employee, “date\_of\_joining”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.db.get\_value(“Employee”, employee, “date\_of\_joining”).
    - Set allocation.to\_date from to\_date.
    - Set allocation.carry\_forward from cint(self.carry\_forward).
    - Set allocation.new\_leaves\_allocated from flt(self.no\_of\_days).
    - Evaluate allocation.insert().
    - Evaluate allocation.submit().
    - Evaluate success.append(mapping(“doc” → get\_link\_to\_form(“Leave Allocation”, allocation.name), “employee” → employee)).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate allocation.log\_error(formatted text Leave Allocation failed for employee {employee}).
    - Evaluate failure.append(employee).
- Evaluate Platform.clear\_messages().
- Evaluate Platform.publish\_realtime(“completed\_bulk\_leave\_allocation”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get from to date](operations-029.md#op-4a427f136201b2).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_bulk\_leave\_allocation”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L172) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1274) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1250)

<a id="op-08a8f7c80707b4"></a>
### Leave Control Panel.create leave policy assignments

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_create_leave_policy_assignments`

**Inputs** self, employees.

**Declared result** dict.

**Record and data access** read “Employee” via get\_value.

**State and service calls** savepoint savepoint · request new\_doc for “Leave Policy Assignment” · call save on assignment · call submit on assignment · rollback · 1 additional forms in the steps below.

**Local steps**

- Set tuple(from\_date, to\_date) from self.get\_from\_to\_date().
- Set assignment\_based\_on from no value when self.dates\_based\_on equals “Custom Range”, otherwise self.dates\_based\_on.
  - Value choice on self.dates\_based\_on equals “Custom Range” — true gives no value, false gives self.dates\_based\_on.
- Set failure from list().
- Set success from list().
- Set savepoint from “before\_assignment\_submission”.
- For each employee in employees.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Set assignment from Platform.new\_doc(“Leave Policy Assignment”).
    - Set assignment.employee from employee.
    - Set assignment.assignment\_based\_on from assignment\_based\_on.
    - Set assignment.leave\_policy from self.leave\_policy.
    - Set assignment.effective\_from from (from\_date or Platform.db.get\_value(“Employee”, employee, “date\_of\_joining”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.db.get\_value(“Employee”, employee, “date\_of\_joining”).
    - Set assignment.effective\_to from to\_date.
    - Set assignment.leave\_period from self.get(“leave\_period”).
    - Set assignment.carry\_forward from self.carry\_forward.
    - Evaluate assignment.save().
    - Evaluate assignment.submit().
    - Evaluate success.append(mapping(“doc” → get\_link\_to\_form(“Leave Policy Assignment”, assignment.name), “employee” → employee)).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Evaluate assignment.log\_error(formatted text Leave Policy Assignment failed for employee {employee}).
    - Evaluate failure.append(employee).
- Evaluate Platform.clear\_messages().
- Evaluate Platform.publish\_realtime(“completed\_bulk\_leave\_policy\_assignment”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get from to date](operations-029.md#op-4a427f136201b2).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“completed\_bulk\_leave\_policy\_assignment”, message = mapping(“success” → success, “failure” → failure), doctype = “Bulk Salary Structure Assignment”, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L892) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1275) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1251)

<a id="op-4a427f136201b2"></a>
### Leave Control Panel.get from to date

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_get_from_to_date`

**Inputs** self.

**Record and data access** read “Leave Period” via get\_value.

**Explicit results** tuple(no value, self.to\_date) · Platform.db.get\_value(“Leave Period”, self.leave\_period, list(“from\_date”, “to\_date”)) · tuple(self.from\_date, self.to\_date).

**Local steps**

- If self.dates\_based\_on equals “Joining Date”.
  - Return tuple(no value, self.to\_date).
- Otherwise.
  - If (self.dates\_based\_on equals “Leave Period” and self.leave\_period).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.dates\_based\_on equals “Leave Period” → self.leave\_period.
    - Return Platform.db.get\_value(“Leave Period”, self.leave\_period, list(“from\_date”, “to\_date”)).
  - Otherwise.
    - Return tuple(self.from\_date, self.to\_date).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L1661) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1279) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1255)

<a id="op-1cee37f3ae9c0a"></a>
### Leave Control Panel.get employees

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_get_employees`

**Inputs** self, advanced\_filters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Record and data access** read “Employee” via get\_list.

**Explicit results** self.get\_employees\_without\_allocations(all\_employees, from\_date, to\_date) · list().

**Local steps**

- Set tuple(from\_date, to\_date) from self.get\_from\_to\_date().
- If (to\_date and (from\_date or self.dates\_based\_on equals “Joining Date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_date → (from\_date or self.dates\_based\_on equals “Joining Date”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → self.dates\_based\_on equals “Joining Date”.
  - If all\_employees bound to Platform.get\_list(“Employee”, filters = (self.get\_filters() + advanced\_filters), fields = list(“name”, “employee”, “employee\_name”, “company”, …)).
    - Return self.get\_employees\_without\_allocations(all\_employees, from\_date, to\_date).
- Return list().

**Methods declared on this owner** [get from to date](operations-029.md#op-4a427f136201b2), [get filters](operations-029.md#op-51b248775a974d), [get employees without allocations](operations-029.md#op-ffe02c7d440236).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L1871) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1276) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1252)

<a id="op-ffe02c7d440236"></a>
### Leave Control Panel.get employees without allocations

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_get_employees_without_allocations`

**Inputs** self, all\_employees, from\_date, to\_date.

**Declared result** list.

**Record and data access** read “Leave Policy Detail” via get\_all.

**Explicit results** list of d for d drawn from all\_employees where d.name does not belong to employees\_with\_allocations.

**Local steps**

- Set Allocation from Platform.qb.DocType(“Leave Allocation”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from nested operand in the contract(nested operand in the contract).select(Employee.name).distinct().where((Allocation.docstatus equals 1 bitwise and Allocation.employee.isin(list of d.name for d drawn from all ….
  - Draw d from all\_employees.
- If self.dates\_based\_on equals “Joining Date”.
  - Set from\_date from Employee.date\_of\_joining.
- Set query from query.where(((Allocation.from\_date at slice from\_date to to\_date bitwise or Allocation.to\_date at slice from\_date to to\_date) bitwise or (((nested operand in the contract.from\_date ≤ from\_date bitwise and  ….
- If (self.allocate\_based\_on\_leave\_policy and self.leave\_policy).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.allocate\_based\_on\_leave\_policy → self.leave\_policy.
  - Set leave\_types from Platform.get\_all(“Leave Policy Detail”, mapping(“parent” → self.leave\_policy), pluck = “leave\_type”).
  - Set query from query.where(Allocation.leave\_type.isin(leave\_types)).
- Otherwise.
  - If (not self.allocate\_based\_on\_leave\_policy and self.leave\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.allocate\_based\_on\_leave\_policy → self.leave\_type.
    - Set query from query.where(Allocation.leave\_type equals self.leave\_type).
- Set employees\_with\_allocations from query.run(pluck = true).
- Return list of d for d drawn from all\_employees where d.name does not belong to employees\_with\_allocations.
  - Draw d from all\_employees, keep a combination only if (d.name does not belong to employees\_with\_allocations).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L2190) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1277) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1253)

<a id="op-35f8b5be6d8c33"></a>
### Leave Control Panel.get latest leave period

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_get_latest_leave_period`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Leave Period” via get\_value.

**Explicit results** Platform.db.get\_value(“Leave Period”, mapping(“is\_active” → 1, “company” → (self.company or get\_default\_company())), “name”, order\_by = “from\_date desc”).

**Local steps**

- Return Platform.db.get\_value(“Leave Period”, mapping(“is\_active” → 1, “company” → (self.company or get\_default\_company())), “name”, order\_by = “from\_date desc”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.company → get\_default\_company().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L3072) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1280) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1256)

<a id="op-51b248775a974d"></a>
### Leave Control Panel.get filters

`operation_workforce_human_resources_record_definitions_leave_control_panel_business_behavior_leave_control_panel_get_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filter\_fields from list(“company”, “employment\_type”, “branch”, “department”, …).
- Set filters from list(list(“status”, “=”, “Active”)).
- For each d in filter\_fields.
  - If self.get(d).
    - If d equals “employee\_grade”.
      - Evaluate filters.append(list(“grade”, “=”, self.get(d))).
    - Otherwise.
      - Evaluate filters.append(list(d, “=”, self.get(d))).
- Return filters.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L3233) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1278) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1254)

## Record · Leave encashment

[Record definition](../../../../data/record-types/leave_encashment.json)

<a id="op-801e5c86069809"></a>
### Leave Encashment.validate

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_validate`

**Inputs** self.

**Local steps**

- Evaluate set\_employee\_name(self).
- Evaluate validate\_active\_employee(self.employee).
- Set self.encashment\_date from (self.encashment\_date or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.encashment\_date → getdate().
- Evaluate self.get\_leave\_details\_for\_encashment().
- Evaluate self.set\_status().
- If not self.pay\_via\_payment\_entry.
  - Evaluate self.set\_salary\_structure().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get leave details for encashment](operations-029.md#op-3830c36cf5efdd), [set status](operations-030.md#op-d8ed85a45200b1), [set salary structure](operations-029.md#op-61647d3fcb2f99).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6154) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1308) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1284)

<a id="op-61647d3fcb2f99"></a>
### Leave Encashment.set salary structure

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_salary_structure`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No Salary Structure assigned to Employee {0} on the given date {1}”.format(self.employee, Platform.bold(format\_date(self.encashment\_date))).

**Local steps**

- Set self.\_salary\_structure from get\_assigned\_salary\_structure(self.employee, self.encashment\_date).
- If not self.\_salary\_structure.
  - Call the validation error handler Platform.throw(translated “No Salary Structure assigned to Employee {0} on the given date {1}”.format(self.employee, Platform.bold(format\_date(self.encashment\_date)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6349) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1305) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1281)

<a id="op-75a83cb1daa09b"></a>
### Leave Encashment.before submit

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_before_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You can only submit Leave Encashment for a valid encashment amount”.

**Local steps**

- If (not self.encashment\_amount or self.encashment\_amount ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.encashment\_amount → self.encashment\_amount ≤ 0.
  - Call the validation error handler Platform.throw(translated “You can only submit Leave Encashment for a valid encashment amount”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6541) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1289) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1265)

<a id="op-b5b6b41a0722e4"></a>
### Leave Encashment.on submit

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If not self.leave\_allocation.
  - Evaluate self.db\_set(“leave\_allocation”, self.get\_leave\_allocation().get(“name”)).
- If self.pay\_via\_payment\_entry.
  - Evaluate self.create\_gl\_entries().
- Otherwise.
  - Evaluate self.create\_additional\_salary().
- Evaluate self.set\_encashed\_leaves\_in\_allocation().
- Evaluate self.create\_leave\_ledger\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get leave allocation](operations-030.md#op-eadf6c94feec76), [create gl entries](operations-030.md#op-f00cc8beb11f8f), [create additional salary](operations-029.md#op-a5da8729e83cd1), [set encashed leaves in allocation](operations-030.md#op-d6da9ebc7942e1), [create leave ledger entry](operations-030.md#op-247628f04d0ed0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6655) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1299) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1275)

<a id="op-3da1c579bbd1f3"></a>
### Leave Encashment.on cancel

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Additional Salary” via get\_doc · read “Leave Allocation” via get\_value.

**State and service calls** call cancel on Platform.get\_doc(“Additional Salary”, self.additional\_salary) · call db\_set on self · request set\_value on “Leave Allocation”.

**Local steps**

- If self.additional\_salary.
  - Evaluate Platform.get\_doc(“Additional Salary”, self.additional\_salary).cancel().
  - Evaluate self.db\_set(“additional\_salary”, empty text).
- If self.leave\_allocation.
  - Evaluate Platform.db.set\_value(“Leave Allocation”, self.leave\_allocation, “total\_leaves\_encashed”, (Platform.db.get\_value(“Leave Allocation”, self.leave\_allocation, “total\_leaves\_encashed”) − self.encashment\_days)).
- If self.pay\_via\_payment\_entry.
  - Evaluate self.create\_gl\_entries(cancel = true).
- Evaluate self.create\_leave\_ledger\_entry(submit = false).
- Set self.ignore\_linked\_doctypes from list(“GL Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”).
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create gl entries](operations-030.md#op-f00cc8beb11f8f), [create leave ledger entry](operations-030.md#op-247628f04d0ed0), [set status](operations-030.md#op-d8ed85a45200b1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L6866) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1297) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1273)

<a id="op-3830c36cf5efdd"></a>
### Leave Encashment.get leave details for encashment

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_get_leave_details_for_encashment`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set\_leave\_balance().
- Evaluate self.set\_actual\_encashable\_days().
- Evaluate self.set\_encashment\_days().
- Evaluate self.set\_encashment\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set leave balance](operations-029.md#op-1e15b837019a4e), [set actual encashable days](operations-029.md#op-3704325a08e1d9), [set encashment days](operations-029.md#op-8420faf0d449fe), [set encashment amount](operations-030.md#op-f1b7758e5910ea).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0058.json#L7264) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1296) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1272)

<a id="op-b24189fa629df0"></a>
### Leave Encashment.get encashment settings

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_get_encashment_settings`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Leave Type”, self.leave\_type, list(“allow\_encashment”, “non\_encashable\_leaves”, “max\_encashable\_leaves”), as\_dict = true).

**Local steps**

- Return Platform.get\_cached\_value(“Leave Type”, self.leave\_type, list(“allow\_encashment”, “non\_encashable\_leaves”, “max\_encashable\_leaves”), as\_dict = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Leave Type”, self.leave\_type, list(“allow\_encashment”, “non\_encashable\_leaves”, “max\_encashable\_leaves”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1293) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1269)

<a id="op-3704325a08e1d9"></a>
### Leave Encashment.set actual encashable days

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_actual_encashable_days`

**Inputs** self.

**State and service calls** msgprint with translated “Excluded {0} Non-Encashable Leaves for {1}”.format(bold(encashment\_settings.non\_encashable\_leaves), leave\_form\_link) · msgprint with translated “Maximum encashable leaves for {0} are {1}”.format(leave\_form\_link, bold(encashment\_settings.max\_encashable\_leaves)).

**Explicit failure paths** validation helper — translated “Leave Type {0} is not encashable”.format(self.leave\_type).

**Local steps**

- Set encashment\_settings from self.get\_encashment\_settings().
- If not encashment\_settings.allow\_encashment.
  - Call the validation error handler Platform.throw(translated “Leave Type {0} is not encashable”.format(self.leave\_type)).
- Set self.actual\_encashable\_days from self.leave\_balance.
- Set leave\_form\_link from get\_link\_to\_form(“Leave Type”, self.leave\_type).
- If encashment\_settings.non\_encashable\_leaves.
  - Set actual\_encashable\_days from (self.leave\_balance − encashment\_settings.non\_encashable\_leaves).
  - Set self.actual\_encashable\_days from actual\_encashable\_days when actual\_encashable\_days &gt; 0, otherwise 0.
    - Value choice on actual\_encashable\_days &gt; 0 — true gives actual\_encashable\_days, false gives 0.
  - Evaluate Platform.msgprint(translated “Excluded {0} Non-Encashable Leaves for {1}”.format(bold(encashment\_settings.non\_encashable\_leaves), leave\_form\_link)).
- If encashment\_settings.max\_encashable\_leaves.
  - Set self.actual\_encashable\_days from min(self.actual\_encashable\_days, encashment\_settings.max\_encashable\_leaves).
  - Evaluate Platform.msgprint(translated “Maximum encashable leaves for {0} are {1}”.format(leave\_form\_link, bold(encashment\_settings.max\_encashable\_leaves)), title = translated “Encashment Limit Applied”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get encashment settings](operations-029.md#op-b24189fa629df0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L115) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1300) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1276)

<a id="op-8420faf0d449fe"></a>
### Leave Encashment.set encashment days

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_encashment_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Encashment Days cannot exceed {0} {1} as per Leave Type settings”.format(bold(translated “Actual Encashable Days”), self.actual\_encashable\_days).

**Local steps**

- If not self.encashment\_days.
  - Set self.encashment\_days from self.actual\_encashable\_days.
- If self.encashment\_days &gt; self.actual\_encashable\_days.
  - Call the validation error handler Platform.throw(translated “Encashment Days cannot exceed {0} {1} as per Leave Type settings”.format(bold(translated “Actual Encashable Days”), self.actual\_encashable\_days)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L621) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1303) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1279)

<a id="op-1e15b837019a4e"></a>
### Leave Encashment.set leave balance

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_leave_balance`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No Leaves Allocated to Employee: {0} for Leave Type: {1}”.format(self.employee, self.leave\_type).

**Local steps**

- Set allocation from self.get\_leave\_allocation().
- If not allocation.
  - Call the validation error handler Platform.throw(translated “No Leaves Allocated to Employee: {0} for Leave Type: {1}”.format(self.employee, self.leave\_type)).
- Set self.leave\_balance from ((allocation.total\_leaves\_allocated − allocation.carry\_forwarded\_leaves\_count) + get\_leaves\_for\_period(self.employee, self.leave\_type, allocation.from\_date, self.encashment\_date)).
- Set self.leave\_allocation from allocation.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get leave allocation](operations-030.md#op-eadf6c94feec76).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L812) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1304) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1280)

<a id="op-a5da8729e83cd1"></a>
### Leave Encashment.create additional salary

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_create_additional_salary`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “Leave Type” via get\_value.

**State and service calls** request new\_doc for “Additional Salary” · call submit on additional\_salary.

**Explicit failure paths** validation helper — translated “Please set Earning Component for Leave type: {0}.”.format(self.leave\_type).

**Local steps**

- Set additional\_salary from Platform.new\_doc(“Additional Salary”).
- Set additional\_salary.company from Platform.get\_value(“Employee”, self.employee, “company”).
- Set additional\_salary.employee from self.employee.
- Set additional\_salary.currency from self.currency.
- Set earning\_component from Platform.get\_value(“Leave Type”, self.leave\_type, “earning\_component”).
- If not earning\_component.
  - Call the validation error handler Platform.throw(translated “Please set Earning Component for Leave type: {0}.”.format(self.leave\_type)).
- Set additional\_salary.salary\_component from earning\_component.
- Set additional\_salary.payroll\_date from self.encashment\_date.
- Set additional\_salary.amount from self.encashment\_amount.
- Set additional\_salary.overwrite\_salary\_structure\_amount from 0.
- Set additional\_salary.ref\_doctype from self.doctype.
- Set additional\_salary.ref\_docname from self.name.
- Evaluate additional\_salary.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L1057) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1290) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1266)
