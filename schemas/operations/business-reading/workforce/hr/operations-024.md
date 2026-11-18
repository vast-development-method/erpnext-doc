# Employment and attendance · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave adjustment

[Record definition](../../../../data/record-types/leave_adjustment.json)

<a id="op-4654884e569eba"></a>
### Leave Adjustment.before save

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_leaves\_after\_adjustment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set leaves after adjustment](operations-024.md#op-c2336256148648).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L984) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L964)

<a id="op-c2336256148648"></a>
### Leave Adjustment.set leaves after adjustment

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_set_leaves_after_adjustment`

**Inputs** self.

**Local steps**

- If self.adjustment\_type equals “Allocate”.
  - Set self.leaves\_after\_adjustment from (flt(self.allocated\_leaves) + flt(self.leaves\_to\_adjust)).
- Otherwise.
  - If self.adjustment\_type equals “Reduce”.
    - Set self.leaves\_after\_adjustment from (flt(self.allocated\_leaves) − flt(self.leaves\_to\_adjust)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L57) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L989) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L969)

<a id="op-888f3d37426db8"></a>
### Leave Adjustment.validate

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_leave\_adjustment().
- Evaluate self.validate\_non\_zero\_adjustment().
- Evaluate self.validate\_over\_allocation().
- Evaluate self.validate\_leave\_balance().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate leave adjustment](operations-024.md#op-7f27227b68a282), [validate non zero adjustment](operations-024.md#op-8d3e57ecf293af), [validate over allocation](operations-024.md#op-729632a25486bf), [validate leave balance](operations-024.md#op-8c1b77176cde16).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L252) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L990) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L970)

<a id="op-7f27227b68a282"></a>
### Leave Adjustment.validate duplicate leave adjustment

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_validate_duplicate_leave_adjustment`

**Inputs** self.

**Record and data access** read “Leave Adjustment” via exists.

**Explicit failure paths** validation helper.

**Local steps**

- Set duplicate\_adjustment from Platform.db.exists(“Leave Adjustment”, mapping(“employee” → self.employee, “leave\_allocation” → self.leave\_allocation, “docstatus” → 1)).
- If duplicate\_adjustment.
  - Call the validation error handler Platform.throw(title = translated “Duplicate Leave Adjustment”, msg = translated “Leave Adjustment for this allocation already exists: {0}. Please amend existing adjustment.”.format(get\_link\_to\_form(“Leave ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L363) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L991) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L971)

<a id="op-8d3e57ecf293af"></a>
### Leave Adjustment.validate non zero adjustment

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_validate_non_zero_adjustment`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enter a non-zero value to adjust.”.

**Local steps**

- <a id="op-8d3e57ecf293af-guard-2"></a>If self.leaves\_to\_adjust equals 0.
  - Call the validation error handler Platform.throw(translated “Enter a non-zero value to adjust.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.leaves\_to\_adjust equals 0, self.leaves\_to\_adjust = 0 selects the branch that calls the validation-error handler with translated “Enter a non-zero value to adjust.”. With self.leaves\_to\_adjust = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8d3e57ecf293af-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L611) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L993) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L973)

<a id="op-729632a25486bf"></a>
### Leave Adjustment.validate over allocation

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_validate_over_allocation`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Allocation is greater than the maximum allowed {0} for leave type {1}”.format(Platform.bold(max\_leaves\_allowed), Platform.bold(self.leave\_type)).

**Local steps**

- <a id="op-729632a25486bf-guard-2"></a>If self.adjustment\_type equals “Reduce”.
  - Return no value.
- Set max\_leaves\_allowed from Platform.db.get\_value(“Leave Type”, self.leave\_type, “max\_leaves\_allowed”).
- Set new\_allocation from (flt(self.allocated\_leaves) + flt(self.leaves\_to\_adjust)).
- If (max\_leaves\_allowed and new\_allocation &gt; max\_leaves\_allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_leaves\_allowed → new\_allocation &gt; max\_leaves\_allowed.
  - Call the validation error handler Platform.throw(translated “Allocation is greater than the maximum allowed {0} for leave type {1}”.format(Platform.bold(max\_leaves\_allowed), Platform.bold(self.leave\_type))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.adjustment\_type equals “Reduce”, self.adjustment\_type = “Reduce” selects the branch that returns no value. With self.adjustment\_type = “Allocate”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-729632a25486bf-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L707) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L994) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L974)

<a id="op-8c1b77176cde16"></a>
### Leave Adjustment.validate leave balance

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_validate_leave_balance`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Reduction is more than {0}'s available leave balance {1} for leave type {2}”.format(Platform.bold(self.employee\_name), Platform.bold(leave\_balance), Platform.bold(self.leave\_type)).

**Local steps**

- <a id="op-8c1b77176cde16-guard-2"></a>If self.adjustment\_type equals “Allocate”.
  - Return no value.
- Set leave\_balance from get\_leave\_balance\_on(employee = self.employee, leave\_type = self.leave\_type, date = self.posting\_date).
- If leave\_balance &lt; self.leaves\_to\_adjust.
  - Call the validation error handler Platform.throw(translated “Reduction is more than {0}'s available leave balance {1} for leave type {2}”.format(Platform.bold(self.employee\_name), Platform.bold(leave\_balance), Platform.bold(self.leave\_type))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.adjustment\_type equals “Allocate”, self.adjustment\_type = “Allocate” selects the branch that returns no value. With self.adjustment\_type = “Reduce”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8c1b77176cde16-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1008) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L992) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L972)

<a id="op-efd6ace73dac23"></a>
### Leave Adjustment.on submit

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_leave\_ledger\_entry(submit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave ledger entry](operations-024.md#op-fa1225042e12b7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1286) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L988) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L968)

<a id="op-986ae7a3683bb6"></a>
### Leave Adjustment.on cancel

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.create\_leave\_ledger\_entry(submit = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave ledger entry](operations-024.md#op-fa1225042e12b7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1348) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L987) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L967)

<a id="op-fa1225042e12b7"></a>
### Leave Adjustment.create leave ledger entry

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_leave_adjustment_create_leave_ledger_entry`

**Inputs** self, submit.

**Record and data access** read “Leave Type” via get\_value.

**Local steps**

- Set is\_lwp from Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_lwp”).
- Set args from dict(leaves = self.leaves\_to\_adjust when self.adjustment\_type equals “Allocate”, otherwise (negative 1 × self.leaves\_to\_adjust), from\_date = self.from\_date, to\_date = self.to\_date, is\_lwp = is\_lwp).
  - Value choice on self.adjustment\_type equals “Allocate” — true gives self.leaves\_to\_adjust, false gives (negative 1 × self.leaves\_to\_adjust).
- Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1410) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L986) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L966)

<a id="op-488235ea26b165"></a>
### Get leave allocation for posting date

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_get_leave_allocation_for_posting_date`

**Inputs** employee, leave\_type, posting\_date.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Leave Allocation” via get\_list.

**Explicit results** Platform.get\_list(“Leave Allocation”, mapping(“employee” → employee, “leave\_type” → leave\_type, “from\_date” → list(“&lt;=”, posting\_date), “to\_date” → list(“&gt;=”, posting\_date), …), list(“name”)).

**Local steps**

- Return Platform.get\_list(“Leave Allocation”, mapping(“employee” → employee, “leave\_type” → leave\_type, “from\_date” → list(“&lt;=”, posting\_date), “to\_date” → list(“&gt;=”, posting\_date), …), list(“name”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1645) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L983) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L963)

<a id="op-6119ce11e8d643"></a>
### Get allocated leave types

`operation_workforce_human_resources_record_definitions_leave_adjustment_business_behavior_get_allocated_leave_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** tuple at tuple at tuple(str, str).

**Record and data access** read “Leave Allocation” via get\_list.

**Explicit results** Platform.get\_list(“Leave Allocation”, mapping(“employee” → filters.get(“employee”), “docstatus” → 1), list(“leave\_type”, “name”), as\_list = 1).

**Local steps**

- Return Platform.get\_list(“Leave Allocation”, mapping(“employee” → filters.get(“employee”), “docstatus” → 1), list(“leave\_type”, “name”), as\_list = 1).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L1892) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L982) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L962)

## Record · Leave allocation

[Record definition](../../../../data/record-types/leave_allocation.json)

<a id="op-7a8fd4f4b3d929"></a>
### Leave Allocation.validate

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_period().
- Evaluate self.validate\_allocation\_overlap().
- Evaluate self.validate\_lwp().
- Evaluate set\_employee\_name(self).
- Evaluate self.set\_total\_leaves\_allocated().
- Evaluate self.validate\_leave\_days\_and\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate period](operations-024.md#op-2f48de93ded86e), [validate allocation overlap](operations-025.md#op-647d4f36d1c67d), [validate lwp](operations-024.md#op-39631cca77c905), [set total leaves allocated](operations-025.md#op-45da0948a7f12f), [validate leave days and dates](operations-024.md#op-abfc32ac4937c3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L6219) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1025) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1005)

<a id="op-abfc32ac4937c3"></a>
### Leave Allocation.validate leave days and dates

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_leave_days_and_dates`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_back\_dated\_allocation().
- Evaluate self.validate\_total\_leaves\_allocated().
- Evaluate self.validate\_leave\_allocation\_days().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate back dated allocation](operations-025.md#op-fe059bb444690e), [validate total leaves allocated](operations-025.md#op-dafcbcd1855eeb), [validate leave allocation days](operations-024.md#op-dc4043b8cf5d95).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0041.json#L6371) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1031) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1011)

<a id="op-dc4043b8cf5d95"></a>
### Leave Allocation.validate leave allocation days

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_leave_allocation_days`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value · read “Employee” via get\_value.

**Explicit failure paths** validation helper with OverAllocationError — translated “Total allocated leaves are more than maximum allocation allowed for {0} leave type for employee {1} in the period”.format(self.leave\_type, self.employee).

**Local steps**

- Set max\_leaves\_allowed from Platform.db.get\_value(“Leave Type”, self.leave\_type, “max\_leaves\_allowed”).
- If max\_leaves\_allowed &gt; 0.
  - Set tuple(from\_date, to\_date) from tuple(self.from\_date, self.to\_date).
  - Set company from Platform.db.get\_value(“Employee”, self.employee, “company”).
  - For each period in (get\_leave\_period(self.from\_date, self.to\_date, company) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_leave\_period(self.from\_date, self.to\_date, company) → list().
    - If (period.from\_date ≤ getdate(self.from\_date) and getdate(self.to\_date) ≤ period.to\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in period.from\_date ≤ getdate(self.from\_date) → getdate(self.to\_date) ≤ period.to\_date.
      - Set tuple(from\_date, to\_date) from tuple(period.from\_date, period.to\_date).
  - Set leave\_allocated from get\_leave\_allocation\_for\_period(self.employee, self.leave\_type, from\_date, to\_date, exclude\_allocation = self.name).
  - If (leave\_allocated + flt(self.new\_leaves\_allocated)) &gt; max\_leaves\_allowed.
    - Call the validation error handler Platform.throw(translated “Total allocated leaves are more than maximum allocation allowed for {0} leave type for employee {1} in the period”.format(self.leave\_type, self.employee), OverAllocationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L44) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1030) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1010)

<a id="op-059f5e7cc990a4"></a>
### Leave Allocation.on submit

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_leave\_ledger\_entry().
- Set allocation from get\_previous\_allocation(self.from\_date, self.leave\_type, self.employee).
- If (self.carry\_forward and allocation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.carry\_forward → allocation.
  - Evaluate expire\_allocation(allocation).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave ledger entry](operations-025.md#op-7785e89834cceb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L442) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1019) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L999)

<a id="op-e280f7cebc6af2"></a>
### Leave Allocation.on cancel

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.create\_leave\_ledger\_entry(submit = false).
- If self.leave\_policy\_assignment.
  - Evaluate self.update\_leave\_policy\_assignments\_when\_no\_allocations\_left().
- If self.carry\_forward.
  - Evaluate self.set\_carry\_forwarded\_leaves\_in\_previous\_allocation(on\_cancel = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create leave ledger entry](operations-025.md#op-7785e89834cceb), [update leave policy assignments when no allocations left](operations-024.md#op-9c8f6cd2bff86c), [set carry forwarded leaves in previous allocation](operations-025.md#op-50add80796a7f0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L585) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1018) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L998)

<a id="op-2dfbb18d080952"></a>
### Leave Allocation.on update after submit

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_on_update_after_submit`

**Inputs** self.

**State and service calls** call db\_update on self.

**Local steps**

- If self.has\_value\_changed(“new\_leaves\_allocated”).
  - Evaluate self.validate\_earned\_leave\_update().
  - Evaluate self.validate\_against\_leave\_applications().
  - Set self.total\_leaves\_allocated from (flt(self.unused\_leaves) + flt(self.new\_leaves\_allocated)).
  - Evaluate self.validate\_leave\_days\_and\_dates().
  - Set leaves\_to\_be\_added from flt((self.new\_leaves\_allocated − self.get\_existing\_leave\_count()), self.precision(“new\_leaves\_allocated”)).
  - Set args from mapping(“leaves” → leaves\_to\_be\_added, “from\_date” → self.from\_date, “to\_date” → self.to\_date, “is\_carry\_forward” → 0).
  - Evaluate create\_leave\_ledger\_entry(self, args, true).
  - Evaluate self.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate earned leave update](operations-024.md#op-e43badfcf2355f), [validate against leave applications](operations-024.md#op-47e5ec2d85389b), [validate leave days and dates](operations-024.md#op-abfc32ac4937c3), [get existing leave count](operations-024.md#op-348c8091fbf8d8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L726) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1020) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1000)

<a id="op-348c8091fbf8d8"></a>
### Leave Allocation.get existing leave count

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_get_existing_leave_count`

**Inputs** self.

**Record and data access** read “Leave Ledger Entry” via get\_all.

**Explicit results** ledger\_entries at 0.total\_leaves when ledger\_entries, otherwise 0.

**Local steps**

- Set ledger\_entries from Platform.get\_all(“Leave Ledger Entry”, filters = mapping(“transaction\_type” → “Leave Allocation”, “transaction\_name” → self.name, “employee” → self.employee, “company” → self.company, …), fields = list(map ….
- Return ledger\_entries at 0.total\_leaves when ledger\_entries, otherwise 0.
  - Value choice on ledger\_entries — true gives ledger\_entries at 0.total\_leaves, false gives 0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L1112) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1015) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L995)

<a id="op-e43badfcf2355f"></a>
### Leave Allocation.validate earned leave update

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_earned_leave_update`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.leave\_policy\_assignment and Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_earned\_leave”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.leave\_policy\_assignment → Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_earned\_leave”).
  - Set msg from translated “Cannot update allocation for {0} after submission”.format(Platform.bold(translated “Earned Leaves”)).
  - Update msg using + text in the contract.
  - Update msg using + translated “Earned Leaves are auto-allocated via scheduler based on the annual allocation set in the Leave Policy: {0}”.format(get\_link\_to\_form(“Leave Policy”, self.leave\_policy)).
  - Call the validation error handler Platform.throw(msg, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L1396) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1029) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1009)

<a id="op-47e5ec2d85389b"></a>
### Leave Allocation.validate against leave applications

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_against_leave_applications`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**State and service calls** msgprint with translated “Note: Total allocated leaves {0} shouldn't be less than already approved leaves {1} for the period”.format(self.total\_leaves\_allocated, leaves\_taken).

**Explicit failure paths** validation helper with LessAllocationError — translated “Total allocated leaves {0} cannot be less than already approved leaves {1} for the period”.format(self.total\_leaves\_allocated, leaves\_taken).

**Local steps**

- Set leaves\_taken from get\_approved\_leaves\_for\_period(self.employee, self.leave\_type, self.from\_date, self.to\_date).
- If flt(leaves\_taken) &gt; flt(self.total\_leaves\_allocated).
  - If Platform.db.get\_value(“Leave Type”, self.leave\_type, “allow\_negative”).
    - Evaluate Platform.msgprint(translated “Note: Total allocated leaves {0} shouldn't be less than already approved leaves {1} for the period”.format(self.total\_leaves\_allocated, leaves\_taken)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Total allocated leaves {0} cannot be less than already approved leaves {1} for the period”.format(self.total\_leaves\_allocated, leaves\_taken), LessAllocationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L1696) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1026) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1006)

<a id="op-9c8f6cd2bff86c"></a>
### Leave Allocation.update leave policy assignments when no allocations left

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_update_leave_policy_assignments_when_number_allocations_left`

**Inputs** self.

**Record and data access** read “Leave Allocation” via get\_list.

**State and service calls** request set\_value on “Leave Policy Assignment”.

**Local steps**

- Set allocations from Platform.db.get\_list(“Leave Allocation”, filters = mapping(“docstatus” → 1, “leave\_policy\_assignment” → self.leave\_policy\_assignment)).
- If len(allocations) equals 0.
  - Evaluate Platform.db.set\_value(“Leave Policy Assignment”, self.leave\_policy\_assignment, “leaves\_allocated”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L2013) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1024) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1004)

<a id="op-2f48de93ded86e"></a>
### Leave Allocation.validate period

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_period`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To date cannot be before from date”.

**Local steps**

- If date\_diff(self.to\_date, self.from\_date) &lt; 0.
  - Call the validation error handler Platform.throw(translated “To date cannot be before from date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L45) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1033) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1013)

<a id="op-39631cca77c905"></a>
### Leave Allocation.validate lwp

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_leave_without_pay`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Explicit failure paths** validation helper — translated “Leave Type {0} cannot be allocated since it is leave without pay”.format(self.leave\_type).

**Local steps**

- If Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_lwp”).
  - Call the validation error handler Platform.throw(translated “Leave Type {0} cannot be allocated since it is leave without pay”.format(self.leave\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L2334) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1032) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1012)
