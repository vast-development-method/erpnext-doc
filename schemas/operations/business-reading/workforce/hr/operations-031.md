# Employment and attendance · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave ledger entry

[Record definition](../../../../data/record-types/leave_ledger_entry.json)

<a id="op-3dd18566c22b2c"></a>
### Expire carried forward allocation

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_expire_carried_forward_allocation`

**Inputs** allocation.

**Local steps**

- Bind dependencies get\_leaves\_for\_period.
- Set leaves\_taken from get\_leaves\_for\_period(allocation.employee, allocation.leave\_type, allocation.from\_date, allocation.to\_date, skip\_expired\_leaves = false).
- Set leaves from (flt(allocation.leaves) + flt(leaves\_taken)).
- If leaves &gt; 0.
  - Set args from Platform.\_dict(transaction\_name = allocation.name, transaction\_type = “Leave Allocation”, leaves = (leaves × negative 1), is\_carry\_forward = allocation.is\_carry\_forward, …).
  - Evaluate create\_leave\_ledger\_entry(allocation, args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L612) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1328) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1304)

<a id="op-1787f71a5a2474"></a>
### On doctype update

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Leave Ledger Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“Leave Ledger Entry”, list(“transaction\_type”, “transaction\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L935) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1333) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1309)

## Record · Leave period

[Record definition](../../../../data/record-types/leave_period.json)

<a id="op-2339d3c0e175dd"></a>
### Leave Period.validate

`operation_workforce_human_resources_record_definitions_leave_period_business_behavior_leave_period_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate validate\_overlap(self, self.from\_date, self.to\_date, self.company).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-031.md#op-2393f7dba5f77d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L1519) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1338) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1314)

<a id="op-2393f7dba5f77d"></a>
### Leave Period.validate dates

`operation_workforce_human_resources_record_definitions_leave_period_business_behavior_leave_period_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To date can not be equal or less than from date”.

**Local steps**

- If getdate(self.from\_date) ≥ getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “To date can not be equal or less than from date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L1615) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1339) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1315)

<a id="op-96ba1fb92874b9"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_period_leave_period_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_period”, “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Leave Allocation”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_period”, “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Leave Allocation”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L1742) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1340) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1316)

## Record · Leave policy

[Record definition](../../../../data/record-types/leave_policy.json)

<a id="op-29531d1276522f"></a>
### Leave Policy.validate

`operation_workforce_human_resources_record_definitions_leave_policy_business_behavior_leave_policy_validate`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit failure paths** validation helper — translated “Maximum leave allowed in the leave type {0} is {1}”.format(lp\_detail.leave\_type, max\_leaves\_allowed).

**Local steps**

- If self.leave\_policy\_details.
  - For each lp\_detail in self.leave\_policy\_details.
    - Set max\_leaves\_allowed from Platform.db.get\_value(“Leave Type”, lp\_detail.leave\_type, “max\_leaves\_allowed”).
    - If (max\_leaves\_allowed &gt; 0 and lp\_detail.annual\_allocation &gt; max\_leaves\_allowed).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_leaves\_allowed &gt; 0 → lp\_detail.annual\_allocation &gt; max\_leaves\_allowed.
      - Call the validation error handler Platform.throw(translated “Maximum leave allowed in the leave type {0} is {1}”.format(lp\_detail.leave\_type, max\_leaves\_allowed)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L2204) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1377) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1353)

## Record · Leave policy assignment

[Record definition](../../../../data/record-types/leave_policy_assignment.json)

<a id="op-26ee58af979ade"></a>
### Leave Policy Assignment.validate

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_dates().
- Evaluate self.validate\_policy\_assignment\_overlap().
- Evaluate self.warn\_about\_carry\_forwarding().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set dates](operations-031.md#op-c18d42e049bfa4), [validate policy assignment overlap](operations-031.md#op-3e78825982ee76), [warn about carry forwarding](operations-031.md#op-32e1746fa534fe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L2978) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1359) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1335)

<a id="op-953ac4c39e0ca5"></a>
### Leave Policy Assignment.on submit

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.grant\_leave\_alloc\_for\_employee().

If control reaches the end, it returns no value.

**Methods declared on this owner** [grant leave alloc for employee](operations-031.md#op-1ba68873ae481d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L3069) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1357) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1333)

<a id="op-c18d42e049bfa4"></a>
### Leave Policy Assignment.set dates

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_set_dates`

**Inputs** self.

**Record and data access** read “Leave Period” via get\_value · read “Employee” via get\_value.

**Local steps**

- If self.assignment\_based\_on equals “Leave Period”.
  - Set tuple(self.effective\_from, self.effective\_to) from Platform.db.get\_value(“Leave Period”, self.leave\_period, list(“from\_date”, “to\_date”)).
- Otherwise.
  - If self.assignment\_based\_on equals “Joining Date”.
    - Set self.effective\_from from Platform.db.get\_value(“Employee”, self.employee, “date\_of\_joining”).
    - If not self.effective\_to.
      - Set self.effective\_to from get\_last\_day(add\_months(self.effective\_from, 12)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L3120) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1358) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1334)

<a id="op-3e78825982ee76"></a>
### Leave Policy Assignment.validate policy assignment overlap

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_validate_policy_assignment_overlap`

**Inputs** self.

**Record and data access** read “Leave Policy Assignment” via get\_value.

**Explicit failure paths** validation helper — translated “Leave Policy: {0} already assigned for Employee {1} for period {2} to {3}”.format(bold(leave\_policy\_assignment), bold(self.employee), bold(formatdate(self.effective\_from)), bold(formatdate(self ….

**Local steps**

- Set leave\_policy\_assignment from Platform.db.get\_value(“Leave Policy Assignment”, mapping(“employee” → self.employee, “name” → tuple(“!=”, self.name), “docstatus” → 1, “effective\_to” → tuple(“&gt;=”, self.effective\_from), …), “leave\_policy”).
- If leave\_policy\_assignment.
  - Call the validation error handler Platform.throw(translated “Leave Policy: {0} already assigned for Employee {1} for period {2} to {3}”.format(bold(leave\_policy\_assignment), bold(self.employee), bold(formatdate(self.effective\_from)), bold( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L3425) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1360) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1336)

<a id="op-32e1746fa534fe"></a>
### Leave Policy Assignment.warn about carry forwarding

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_warn_about_carry_forwarding`

**Inputs** self.

**Record and data access** resolve a document from “Leave Policy” via get\_doc.

**State and service calls** msgprint with msg.

**Explicit results** no value.

**Local steps**

- If not self.carry\_forward.
  - Return no value.
- Set leave\_types from get\_leave\_type\_details().
- Set leave\_policy from Platform.get\_doc(“Leave Policy”, self.leave\_policy).
- For each policy in leave\_policy.leave\_policy\_details.
  - Set leave\_type from leave\_types.get(policy.leave\_type).
  - If not leave\_type.is\_carry\_forward.
    - Set msg from translated “Leaves for the Leave Type {0} won't be carry-forwarded since carry-forwarding is disabled.”.format(Platform.bold(get\_link\_to\_form(“Leave Type”, leave\_type.name))).
    - Evaluate Platform.msgprint(msg, indicator = “orange”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L3823) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1361) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1337)

<a id="op-1ba68873ae481d"></a>
### Leave Policy Assignment.grant leave alloc for employee

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_grant_leave_allocation_for_employee`

**Inputs** self.

**Record and data access** resolve a document from “Leave Policy” via get\_doc · read “Employee” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** leave\_allocations.

**Explicit failure paths** validation helper — translated “Leave already have been assigned for this Leave Policy Assignment”.

**Local steps**

- If self.leaves\_allocated.
  - Call the validation error handler Platform.throw(translated “Leave already have been assigned for this Leave Policy Assignment”).
- Otherwise.
  - Set leave\_allocations from mapping().
  - Set leave\_type\_details from get\_leave\_type\_details().
  - Set leave\_policy from Platform.get\_doc(“Leave Policy”, self.leave\_policy).
  - Set date\_of\_joining from Platform.db.get\_value(“Employee”, self.employee, “date\_of\_joining”).
  - For each leave\_policy\_detail in leave\_policy.leave\_policy\_details.
    - Set leave\_details from leave\_type\_details.get(leave\_policy\_detail.leave\_type).
    - If not leave\_details.is\_lwp.
      - Set tuple(leave\_allocation, new\_leaves\_allocated) from self.create\_leave\_allocation(leave\_policy\_detail.annual\_allocation, leave\_details, date\_of\_joining).
      - Set leave\_allocations at leave\_details.name from mapping(“name” → leave\_allocation, “leaves” → new\_leaves\_allocated).
  - Evaluate self.db\_set(“leaves\_allocated”, 1).
  - Return leave\_allocations.

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave allocation](operations-031.md#op-e4e3b82e7b42dd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L4149) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1356) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1332)

<a id="op-e4e3b82e7b42dd"></a>
### Leave Policy Assignment.create leave allocation

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_create_leave_allocation`

**Inputs** self, annual\_allocation, leave\_details, date\_of\_joining.

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Leave Policy Assignment”, “reference\_name” → self.name, …) via get\_doc · resolve a document from “Leave Allocation” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Leave Policy Assignment”, “reference\_name” → self.name, …)) · call save on allocation · call submit on allocation.

**Explicit results** tuple(no value, 0) · tuple(allocation.name, new\_leaves\_allocated).

**Local steps**

- Set carry\_forward from self.carry\_forward.
- If (self.carry\_forward and not leave\_details.is\_carry\_forward).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.carry\_forward → not leave\_details.is\_carry\_forward.
  - Set carry\_forward from 0.
- Set new\_leaves\_allocated from self.get\_new\_leaves(annual\_allocation, leave\_details, date\_of\_joining).
- Set earned\_leave\_schedule from self.get\_earned\_leave\_schedule(annual\_allocation, leave\_details, date\_of\_joining, new\_leaves\_allocated) when leave\_details.is\_earned\_leave, otherwise list().
  - Value choice on leave\_details.is\_earned\_leave — true gives self.get\_earned\_leave\_schedule(annual\_allocation, leave\_details, date\_of\_joining, new\_leaves\_allocated), false gives list().
- If (new\_leaves\_allocated equals 0 and not leave\_details.is\_earned\_leave).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_leaves\_allocated equals 0 → not leave\_details.is\_earned\_leave.
  - Set text from translated “Leave allocation is skipped for {0}, because number of leaves to be allocated is 0.”.format(Platform.bold(leave\_details.name)).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Comment”, “reference\_doctype” → “Leave Policy Assignment”, “reference\_name” → self.name, …)).insert(ignore\_permissions = true).
  - Return tuple(no value, 0).
- Set allocation from Platform.get\_doc(doctype = “Leave Allocation”, employee = self.employee, leave\_type = leave\_details.name, from\_date = self.effective\_from, …).
  - Value choice on self.assignment\_based\_on equals “Leave Policy” — true gives self.leave\_period, false gives empty text.
- Evaluate allocation.save(ignore\_permissions = true).
- Evaluate allocation.submit().
- Return tuple(allocation.name, new\_leaves\_allocated).

**Methods declared on this owner** [get new leaves](operations-031.md#op-77589b53f44a9a), [get earned leave schedule](operations-031.md#op-c0e7f97ad99376).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L60) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1350) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1326)

<a id="op-77589b53f44a9a"></a>
### Leave Policy Assignment.get new leaves

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_get_new_leaves`

**Inputs** self, annual\_allocation, leave\_details, date\_of\_joining.

**Explicit results** flt(new\_leaves\_allocated, precision).

**Local steps**

- Bind dependencies get\_field\_precision.
- Set precision from get\_field\_precision(Platform.get\_meta(“Leave Allocation”).get\_field(“new\_leaves\_allocated”)).
- Set current\_date from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- If leave\_details.is\_compensatory.
  - Set new\_leaves\_allocated from 0.
- Otherwise.
  - If (leave\_details.is\_earned\_leave and current\_date &lt; getdate(self.effective\_to)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_details.is\_earned\_leave → current\_date &lt; getdate(self.effective\_to).
    - Set new\_leaves\_allocated from self.get\_leaves\_for\_passed\_period(annual\_allocation, leave\_details, date\_of\_joining).
  - Otherwise.
    - Set new\_leaves\_allocated from calculate\_pro\_rated\_leaves(annual\_allocation, date\_of\_joining, self.effective\_from, self.effective\_to, is\_earned\_leave = false).
- If (new\_leaves\_allocated &gt; annual\_allocation and not (leave\_details.is\_earned\_leave and leave\_details.earned\_leave\_frequency equals “Yearly”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_leaves\_allocated &gt; annual\_allocation → not (leave\_details.is\_earned\_leave and leave\_details.earned\_leave\_frequency equals “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_details.is\_earned\_leave → leave\_details.earned\_leave\_frequency equals “Yearly”.
  - Set new\_leaves\_allocated from annual\_allocation.
- Return flt(new\_leaves\_allocated, precision).

**Methods declared on this owner** [get leaves for passed period](operations-031.md#op-30716626df07a5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L5339) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1354) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1330)

<a id="op-30716626df07a5"></a>
### Leave Policy Assignment.get leaves for passed period

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_get_leaves_for_passed_period`

**Inputs** self, annual\_allocation, leave\_details, date\_of\_joining.

**Explicit results** new\_leaves\_allocated.

**Local steps**

- Set consider\_current\_period from is\_earned\_leave\_applicable\_for\_current\_period(date\_of\_joining, leave\_details.allocate\_on\_day, leave\_details.earned\_leave\_frequency, effective\_from = self.effective\_from).
- Set tuple(current\_date, from\_date) from self.get\_current\_and\_from\_date(date\_of\_joining).
- Set periods\_passed from self.get\_periods\_passed(leave\_details.earned\_leave\_frequency, current\_date, from\_date, consider\_current\_period).
- If periods\_passed &gt; 0.
  - Set new\_leaves\_allocated from self.calculate\_leaves\_for\_passed\_period(annual\_allocation, leave\_details, date\_of\_joining, periods\_passed, …).
- Otherwise.
  - Set new\_leaves\_allocated from 0.
- Return new\_leaves\_allocated.

**Methods declared on this owner** [get current and from date](operations-031.md#op-5bd6cccd3548f9), [get periods passed](operations-031.md#op-821a746d1890df), [calculate leaves for passed period](operations-031.md#op-4973d0596bd69e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L5803) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1353) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1329)

<a id="op-5bd6cccd3548f9"></a>
### Leave Policy Assignment.get current and from date

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_get_current_and_from_date`

**Inputs** self, date\_of\_joining.

**Explicit results** tuple(current\_date, from\_date).

**Local steps**

- Set current\_date from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- If current\_date &gt; getdate(self.effective\_to).
  - Set current\_date from getdate(self.effective\_to).
- Set from\_date from getdate(self.effective\_from).
- If getdate(date\_of\_joining) &gt; from\_date.
  - Set from\_date from getdate(date\_of\_joining).
- Return tuple(current\_date, from\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L6090) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1351) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1327)

<a id="op-821a746d1890df"></a>
### Leave Policy Assignment.get periods passed

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_get_periods_passed`

**Inputs** self, earned\_leave\_frequency, current\_date, from\_date, consider\_current\_period.

**Explicit results** max(calculate\_periods\_passed(current\_date, from\_date, periods\_per\_year, months\_per\_period, effective\_from = effective\_from, …), 0).

**Local steps**

- Set tuple(periods\_per\_year, months\_per\_period) from mapping(“Monthly” → tuple(12, 1), “Quarterly” → tuple(4, 3), “Half-Yearly” → tuple(2, 6), “Yearly” → tuple(1, 12)).get(earned\_leave\_frequency).
- Set effective\_from from self.effective\_from when earned\_leave\_frequency equals “Half-Yearly”, otherwise no value.
  - Value choice on earned\_leave\_frequency equals “Half-Yearly” — true gives self.effective\_from, false gives no value.
- Return max(calculate\_periods\_passed(current\_date, from\_date, periods\_per\_year, months\_per\_period, effective\_from = effective\_from, …), 0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L6357) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1355) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1331)

<a id="op-4973d0596bd69e"></a>
### Leave Policy Assignment.calculate leaves for passed period

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_calculate_leaves_for_passed_period`

**Inputs** self, annual\_allocation, leave\_details, date\_of\_joining, periods\_passed, consider\_current\_period.

**Explicit results** leaves.

**Local steps**

- Bind dependencies get\_periodically\_earned\_leave.
- Bind dependencies get\_sub\_period\_start\_and\_end.
- Set periodically\_earned\_leave from get\_periodically\_earned\_leave(date\_of\_joining, annual\_allocation, leave\_details.earned\_leave\_frequency, leave\_details.rounding, pro\_rated = false).
- Set period\_end\_date from get\_pro\_rata\_period\_end\_date(consider\_current\_period).
- If getdate(self.effective\_from) ≤ date\_of\_joining ≤ period\_end\_date.
  - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.effective\_from) ≤ date\_of\_joining ≤ period\_end\_date.
  - Set tuple(start\_date, end\_date) from get\_sub\_period\_start\_and\_end(date\_of\_joining, leave\_details.earned\_leave\_frequency, effective\_from = self.effective\_from).
  - Set leaves from get\_periodically\_earned\_leave(date\_of\_joining, annual\_allocation, leave\_details.earned\_leave\_frequency, leave\_details.rounding, …).
  - Update leaves using + (periodically\_earned\_leave × (periods\_passed − 1)).
- Otherwise.
  - Set leaves from (periodically\_earned\_leave × periods\_passed).
- Return leaves.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L6639) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1349) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1325)

<a id="op-c0e7f97ad99376"></a>
### Leave Policy Assignment.get earned leave schedule

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_leave_policy_assignment_get_earned_leave_schedule`

**Inputs** self, annual\_allocation, leave\_details, date\_of\_joining, new\_leaves\_allocated.

**Explicit results** schedule.

**Local steps**

- Bind dependencies get\_complete\_month\_count, get\_expected\_allocation\_date\_for\_period, get\_monthly\_earned\_leave, get\_sub\_period\_start\_and\_end.
- Set today from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- Set from\_date, last\_allocated\_date from getdate(self.effective\_from).
- Set to\_date from getdate(self.effective\_to).
- Set months\_to\_add from mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(leave\_details.earned\_leave\_frequency).
- Set periodically\_earned\_leave from get\_monthly\_earned\_leave(date\_of\_joining, annual\_allocation, leave\_details.earned\_leave\_frequency, leave\_details.rounding, pro\_rated = false).
- Set date from get\_expected\_allocation\_date\_for\_period(leave\_details.earned\_leave\_frequency, leave\_details.allocate\_on\_day, from\_date, date\_of\_joining, effective\_from = self.effective\_from).
- If (leave\_details.earned\_leave\_frequency equals “Half-Yearly” and self.assignment\_based\_on equals “Joining Date” and to\_date ≥ add\_months(from\_date, 12)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in leave\_details.earned\_leave\_frequency equals “Half-Yearly” → self.assignment\_based\_on equals “Joining Date” → to\_date ≥ add\_months(from\_date, 12).
  - Set max\_allocations from ((get\_complete\_month\_count(to\_date, from\_date) floor divide months\_to\_add) + 1).
- Otherwise.
  - Set max\_allocations from 0.
- Set schedule from list().
- Set allocations\_added from 0.
- If new\_leaves\_allocated.
  - Evaluate schedule.append(mapping(“allocation\_date” → today, “number\_of\_leaves” → new\_leaves\_allocated, “is\_allocated” → 1, “allocated\_via” → “Leave Policy Assignment”, …)).
  - Update allocations\_added using + 1.
  - Set last\_allocated\_date from get\_sub\_period\_start\_and\_end(today, leave\_details.earned\_leave\_frequency, effective\_from = self.effective\_from) at 1.
- While date ≤ to\_date.
  - Set date\_already\_passed from today &gt; date.
  - If date ≥ last\_allocated\_date.
    - Set row from mapping(“allocation\_date” → date, “number\_of\_leaves” → periodically\_earned\_leave, “is\_allocated” → 1 when date\_already\_passed, otherwise 0, “allocated\_via” → “Leave Policy Assignment” when date\_already\_pas ….
      - Value choice on date\_already\_passed — true gives 1, false gives 0.
      - Value choice on date\_already\_passed — true gives “Leave Policy Assignment”, false gives no value.
      - Value choice on date\_already\_passed — true gives 1, false gives 0.
    - Evaluate schedule.append(row).
    - Update allocations\_added using + 1.
    - If (max\_allocations and allocations\_added ≥ max\_allocations).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_allocations → allocations\_added ≥ max\_allocations.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Set date from get\_expected\_allocation\_date\_for\_period(leave\_details.earned\_leave\_frequency, leave\_details.allocate\_on\_day, add\_to\_date(date, months = months\_to\_add), date\_of\_joining, effective\_from = self.effective\_from).
- If from\_date &lt; getdate(date\_of\_joining).
  - Set tuple(pro\_rated\_period\_start, pro\_rated\_period\_end) from get\_sub\_period\_start\_and\_end(date\_of\_joining, leave\_details.earned\_leave\_frequency, effective\_from = self.effective\_from).
  - Set pro\_rated\_earned\_leave from get\_monthly\_earned\_leave(date\_of\_joining, annual\_allocation, leave\_details.earned\_leave\_frequency, leave\_details.rounding, …).
  - Set schedule at 0 at “number\_of\_leaves” from pro\_rated\_earned\_leave.
- If (annual\_allocation and leave\_details.earned\_leave\_frequency differs from “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in annual\_allocation → leave\_details.earned\_leave\_frequency differs from “Yearly”.
  - Set schedule from cap\_schedule\_to\_annual\_allocation(schedule, annual\_allocation).
- Return schedule.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L61) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1352) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1328)

<a id="op-7273251db5f87b"></a>
### Cap schedule to annual allocation

`operation_workforce_binding_workforce_hr_doctype_leave_policy_assignment_leave_policy_assignment_cap_schedule_to_annual_allocation`

**Inputs** schedule, annual\_allocation.

**Explicit results** capped\_schedule.

**Local steps**

- Bind dependencies get\_field\_precision.
- Set precision from get\_field\_precision(Platform.get\_meta(“Leave Allocation”).get\_field(“new\_leaves\_allocated”)).
- Set annual\_allocation from flt(annual\_allocation, precision).
- Set capped\_schedule from list().
- Set scheduled\_leaves from 0.0.
- For each row in schedule.
  - If not row.get(“is\_allocated”).
    - Set leaves\_left\_in\_quota from flt((annual\_allocation − scheduled\_leaves), precision).
    - If leaves\_left\_in\_quota ≤ 0.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - If flt(row at “number\_of\_leaves”, precision) &gt; leaves\_left\_in\_quota.
      - Set row at “number\_of\_leaves” from leaves\_left\_in\_quota.
  - Set scheduled\_leaves from flt((scheduled\_leaves + flt(row at “number\_of\_leaves”, precision)), precision).
  - Evaluate capped\_schedule.append(row).
- Return capped\_schedule.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L85) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L136) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L136)

<a id="op-c4081b5611d8b4"></a>
### Get pro rata period end date

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_get_pro_rata_period_end_date`

**Inputs** consider\_current\_month.

**Explicit results** period\_end\_date.

**Local steps**

- Set date from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- If consider\_current\_month.
  - Set period\_end\_date from get\_last\_day(date).
- Otherwise.
  - Set period\_end\_date from get\_last\_day(add\_months(date, negative 1)).
- Return period\_end\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L1283) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1347) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1323)

<a id="op-7868ee52fb14c5"></a>
### Calculate periods passed

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_calculate_periods_passed`

**Inputs** current\_date, from\_date, periods\_per\_year, months\_per\_period, consider\_current\_period, effective\_from = no value.

**Explicit results** periods\_passed.

**Local steps**

- If effective\_from.
  - Bind dependencies get\_complete\_month\_count.
  - Set effective\_from from getdate(effective\_from).
  - Set from\_period from (get\_complete\_month\_count(from\_date, effective\_from) floor divide months\_per\_period).
  - Set current\_period from (get\_complete\_month\_count(current\_date, effective\_from) floor divide months\_per\_period).
- Otherwise.
  - Set from\_period from ((from\_date.year × periods\_per\_year) + ((from\_date.month − 1) floor divide months\_per\_period)).
  - Set current\_period from ((current\_date.year × periods\_per\_year) + ((current\_date.month − 1) floor divide months\_per\_period)).
- Set periods\_passed from (current\_period − from\_period).
- If consider\_current\_period.
  - Update periods\_passed using + 1.
- Return periods\_passed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L1460) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1342) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1318)

<a id="op-0db73ac3812278"></a>
### Is earned leave applicable for current period

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_is_earned_leave_applicable_for_current_period`

**Inputs** date\_of\_joining, allocate\_on\_day, earned\_leave\_frequency, effective\_from = no value.

**Explicit results** condition\_map.get(earned\_leave\_frequency).

**Local steps**

- Set date from (getdate(Platform.flags.current\_date) or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(Platform.flags.current\_date) → getdate().
- If (earned\_leave\_frequency equals “Half-Yearly” and effective\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in earned\_leave\_frequency equals “Half-Yearly” → effective\_from.
  - Bind dependencies get\_half\_year\_periods.
  - Set tuple(period\_start, period\_end) from get\_half\_year\_periods(date, effective\_from).
  - Set half\_yearly\_condition from ((allocate\_on\_day equals “First Day” and date ≥ period\_start) or (allocate\_on\_day equals “Last Day” and date equals period\_end)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (allocate\_on\_day equals “First Day” and date ≥ period\_start) → (allocate\_on\_day equals “Last Day” and date equals period\_end).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “First Day” → date ≥ period\_start.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Last Day” → date equals period\_end.
- Otherwise.
  - Bind dependencies get\_semester\_end, get\_semester\_start.
  - Set half\_yearly\_condition from ((allocate\_on\_day equals “First Day” and date ≥ get\_semester\_start(date)) or (allocate\_on\_day equals “Last Day” and date equals get\_semester\_end(date))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (allocate\_on\_day equals “First Day” and date ≥ get\_semester\_start(date)) → (allocate\_on\_day equals “Last Day” and date equals get\_semester\_end(date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “First Day” → date ≥ get\_semester\_start(date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Last Day” → date equals get\_semester\_end(date).
- Set condition\_map from mapping(“Monthly” → ((allocate\_on\_day equals “Date of Joining” and date.day ≥ date\_of\_joining.day) or (allocate\_on\_day equals “First Day” and date ≥ get\_first\_day(date)) or (allocate\_on\_day equals “Last Da ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (allocate\_on\_day equals “Date of Joining” and date.day ≥ date\_of\_joining.day) → (allocate\_on\_day equals “First Day” and date ≥ get\_first\_day(date)) → (allocate\_on\_day equals “Last Day” and date equals get\_last\_day(date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Date of Joining” → date.day ≥ date\_of\_joining.day.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “First Day” → date ≥ get\_first\_day(date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Last Day” → date equals get\_last\_day(date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (allocate\_on\_day equals “First Day” and date ≥ get\_quarter\_start(date)) → (allocate\_on\_day equals “Last Day” and date equals get\_quarter\_ending(date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “First Day” → date ≥ get\_quarter\_start(date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Last Day” → date equals get\_quarter\_ending(date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (allocate\_on\_day equals “First Day” and date ≥ get\_year\_start(date)) → (allocate\_on\_day equals “Last Day” and date equals get\_year\_ending(date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “First Day” → date ≥ get\_year\_start(date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocate\_on\_day equals “Last Day” → date equals get\_year\_ending(date).
- Return condition\_map.get(earned\_leave\_frequency).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L1807) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1348) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1324)

<a id="op-aca6c9b1840905"></a>
### Calculate pro rated leaves

`operation_workforce_human_resources_record_definitions_leave_policy_assignment_business_behavior_calculate_pro_rated_leaves`

**Inputs** leaves, date\_of\_joining, period\_start\_date, period\_end\_date, is\_earned\_leave = false.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** leaves · flt(leaves, precision) · rounded(leaves).

**Local steps**

- If (not leaves or getdate(date\_of\_joining) ≤ getdate(period\_start\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not leaves → getdate(date\_of\_joining) ≤ getdate(period\_start\_date).
  - Return leaves.
- Set precision from cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”, cache = true)).
- Set actual\_period from (date\_diff(period\_end\_date, date\_of\_joining) + 1).
- Set complete\_period from (date\_diff(period\_end\_date, period\_start\_date) + 1).
- Update leaves using × (actual\_period ÷ complete\_period).
- If is\_earned\_leave.
  - Return flt(leaves, precision).
- Return rounded(leaves).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0062.json#L2652) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1343) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1319)
