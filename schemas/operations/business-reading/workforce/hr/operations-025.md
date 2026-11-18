# Employment and attendance · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave allocation

[Record definition](../../../../data/record-types/leave_allocation.json)

<a id="op-647d4f36d1c67d"></a>
### Leave Allocation.validate allocation overlap

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_allocation_overlap`

**Inputs** self.

**State and service calls** msgprint with translated “{0} already allocated for Employee {1} for period {2} to {3}”.format(self.leave\_type, self.employee, formatdate(self.from\_date), formatdate(self.to\_date)).

**Explicit failure paths** validation helper with OverlapError — (translated “Reference” + formatted text : &lt;a href="/app/Form/Leave Allocation/{leave\_allocation at 0 at 0}"&gt;{leave\_allocation at 0 at 0}&lt;/a&gt;).

**Local steps**

- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set leave\_allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand i ….run().
- If leave\_allocation.
  - Evaluate Platform.msgprint(translated “{0} already allocated for Employee {1} for period {2} to {3}”.format(self.leave\_type, self.employee, formatdate(self.from\_date), formatdate(self.to\_date))).
  - Call the validation error handler Platform.throw((translated “Reference” + formatted text : &lt;a href="/app/Form/Leave Allocation/{leave\_allocation at 0 at 0}"&gt;{leave\_allocation at 0 at 0}&lt;/a&gt;), OverlapError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L2477) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1027) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1007)

<a id="op-fe059bb444690e"></a>
### Leave Allocation.validate back dated allocation

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_back_dated_allocation`

**Inputs** self.

**Explicit failure paths** validation helper with BackDatedAllocationError — translated “Leave cannot be allocated before {0}, as leave balance has already been carry-forwarded in the future leave  …”.format(formatdate(future\_allocation at 0.from\_date), future\_allocation at 0.name).

**Local steps**

- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set future\_allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.name, LeaveAllocation.from\_date).where(((((nested operand in the contract bitwise and nested operand in the contract) b ….
- If future\_allocation.
  - Call the validation error handler Platform.throw(translated “Leave cannot be allocated before {0}, as leave balance has already been carry-forwarded in the future leave  …”.format(formatdate(future\_allocation at 0.from\_date), future\_alloca ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L3018) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1028) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1008)

<a id="op-45da0948a7f12f"></a>
### Leave Allocation.set total leaves allocated

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_set_total_leaves_allocated`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Leave Type” via get\_value.

**Explicit failure paths** validation helper — translated “Total leaves allocated is mandatory for Leave Type {0}”.format(self.leave\_type).

**Local steps**

- Set self.unused\_leaves from flt(get\_carry\_forwarded\_leaves(self.employee, self.leave\_type, self.from\_date, self.carry\_forward), self.precision(“unused\_leaves”)).
- Set self.total\_leaves\_allocated from flt((flt(self.unused\_leaves) + flt(self.new\_leaves\_allocated)), self.precision(“total\_leaves\_allocated”)).
- Evaluate self.limit\_carry\_forward\_based\_on\_max\_allowed\_leaves().
- If self.carry\_forward.
  - Evaluate self.set\_carry\_forwarded\_leaves\_in\_previous\_allocation().
- If (not self.total\_leaves\_allocated and not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_earned\_leave”) and not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_compensatory”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.total\_leaves\_allocated → not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_earned\_leave”) → not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_compensatory”).
  - Call the validation error handler Platform.throw(translated “Total leaves allocated is mandatory for Leave Type {0}”.format(self.leave\_type)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [limit carry forward based on max allowed leaves](operations-025.md#op-c24839cabb3848), [set carry forwarded leaves in previous allocation](operations-025.md#op-50add80796a7f0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L43) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1023) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1003)

<a id="op-c24839cabb3848"></a>
### Leave Allocation.limit carry forward based on max allowed leaves

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_limit_carry_forward_based_on_maximum_allowed_leaves`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Local steps**

- Set max\_leaves\_allowed from Platform.db.get\_value(“Leave Type”, self.leave\_type, “max\_leaves\_allowed”).
- If (max\_leaves\_allowed and self.total\_leaves\_allocated &gt; max\_leaves\_allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_leaves\_allowed → self.total\_leaves\_allocated &gt; max\_leaves\_allowed.
  - Set self.total\_leaves\_allocated from max\_leaves\_allowed.
  - Set self.unused\_leaves from (max\_leaves\_allowed − flt(self.new\_leaves\_allocated)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L3958) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1017) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L997)

<a id="op-50add80796a7f0"></a>
### Leave Allocation.set carry forwarded leaves in previous allocation

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_set_carry_forwarded_leaves_in_previous_allocation`

**Inputs** self, on\_cancel = false.

**State and service calls** request set\_value on “Leave Allocation”.

**Local steps**

- Set previous\_allocation from get\_previous\_allocation(self.from\_date, self.leave\_type, self.employee).
- If on\_cancel.
  - Set self.unused\_leaves from 0.0.
- If previous\_allocation.
  - Evaluate Platform.db.set\_value(“Leave Allocation”, previous\_allocation.name, “carry\_forwarded\_leaves\_count”, self.unused\_leaves).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L4138) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1022) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1002)

<a id="op-dafcbcd1855eeb"></a>
### Leave Allocation.validate total leaves allocated

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_validate_total_leaves_allocated`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**State and service calls** msgprint with translated text in the contract.

**Explicit failure paths** validation helper with OverAllocationError — translated text in the contract.

**Local steps**

- Set date\_difference from (date\_diff(self.to\_date, self.from\_date) + 1).
- If date\_difference &lt; self.total\_leaves\_allocated.
  - If Platform.db.get\_value(“Leave Type”, self.leave\_type, “allow\_over\_allocation”).
    - Evaluate Platform.msgprint(translated text in the contract, indicator = “orange”, alert = true).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated text in the contract, exc = OverAllocationError, title = translated “Over Allocation”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L4324) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1034) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1014)

<a id="op-7785e89834cceb"></a>
### Leave Allocation.create leave ledger entry

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_create_leave_ledger_entry`

**Inputs** self, submit = true.

**Record and data access** read “Leave Type” via get\_value.

**Local steps**

- If self.unused\_leaves.
  - Set expiry\_days from Platform.db.get\_value(“Leave Type”, self.leave\_type, “expire\_carry\_forwarded\_leaves\_after\_days”).
  - Set end\_date from add\_days(self.from\_date, (expiry\_days − 1)) when expiry\_days, otherwise self.to\_date.
    - Value choice on expiry\_days — true gives add\_days(self.from\_date, (expiry\_days − 1)), false gives self.to\_date.
  - Set args from dict(leaves = self.unused\_leaves, from\_date = self.from\_date, to\_date = min(getdate(end\_date), getdate(self.to\_date)), is\_carry\_forward = 1).
  - Evaluate create\_leave\_ledger\_entry(self, args, submit).
  - If (submit and getdate(end\_date) &lt; getdate()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in submit → getdate(end\_date) &lt; getdate().
    - Evaluate show\_expire\_leave\_dialog(self.unused\_leaves, self.leave\_type).
- Set args from dict(leaves = self.new\_leaves\_allocated, from\_date = self.from\_date, to\_date = self.to\_date, is\_carry\_forward = 0).
- Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L4614) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1014) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L994)

<a id="op-cef0b63f523758"></a>
### Leave Allocation.allocate leaves manually

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_allocate_leaves_manually`

**Inputs** self, new\_leaves, from\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Leave Type” via get\_value · read “Leave Policy Detail” via get\_value.

**State and service calls** call db\_set on self · msgprint with translated “{0} leaves allocated successfully”.format(Platform.bold(new\_leaves)).

**Explicit failure paths** validation helper — translated “Cannot allocate leaves outside the allocation period {0} - {1}”.format(Platform.bold(formatdate(self.from\_date)), Platform.bold(formatdate(self.to\_date))) · validation helper — msg.

**Local steps**

- If (from\_date and not getdate(self.from\_date) ≤ getdate(from\_date) ≤ getdate(self.to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → not getdate(self.from\_date) ≤ getdate(from\_date) ≤ getdate(self.to\_date).
  - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.from\_date) ≤ getdate(from\_date) ≤ getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “Cannot allocate leaves outside the allocation period {0} - {1}”.format(Platform.bold(formatdate(self.from\_date)), Platform.bold(formatdate(self.to\_date))), title = translated “In ….
- Set new\_allocation from (flt(self.total\_leaves\_allocated) + flt(new\_leaves)).
- Set new\_allocation\_without\_cf from flt((flt(self.get\_existing\_leave\_count()) + flt(new\_leaves)), self.precision(“total\_leaves\_allocated”)).
- Set max\_leaves\_allowed from Platform.db.get\_value(“Leave Type”, self.leave\_type, “max\_leaves\_allowed”).
- If (new\_allocation &gt; max\_leaves\_allowed and max\_leaves\_allowed &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_allocation &gt; max\_leaves\_allowed → max\_leaves\_allowed &gt; 0.
  - Set new\_allocation from max\_leaves\_allowed.
- Set annual\_allocation from Platform.db.get\_value(“Leave Policy Detail”, mapping(“parent” → self.leave\_policy, “leave\_type” → self.leave\_type), “annual\_allocation”).
- Set annual\_allocation from flt(annual\_allocation, self.precision(“total\_leaves\_allocated”)).
- If (new\_allocation differs from self.total\_leaves\_allocated and new\_allocation\_without\_cf ≤ annual\_allocation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_allocation differs from self.total\_leaves\_allocated → new\_allocation\_without\_cf ≤ annual\_allocation.
  - Evaluate self.db\_set(“total\_leaves\_allocated”, new\_allocation, update\_modified = false).
  - Set date from (from\_date or Platform.flags.current\_date or getdate()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.flags.current\_date → getdate().
  - Evaluate create\_additional\_leave\_ledger\_entry(self, new\_leaves, date).
  - Set text from translated “{0} leaves were manually allocated by {1} on {2}”.format(Platform.bold(new\_leaves), Platform.session.user, Platform.bold(formatdate(date))).
  - Evaluate self.add\_comment(comment\_type = “Info”, text = text).
  - Evaluate Platform.msgprint(translated “{0} leaves allocated successfully”.format(Platform.bold(new\_leaves)), indicator = “green”, alert = true).
- Otherwise.
  - Set msg from translated “Total leaves allocated cannot exceed annual allocation of {0}.”.format(Platform.bold(translated annual\_allocation)).
  - Update msg using + text in the contract.
  - Update msg using + translated “Reference: {0}”.format(get\_link\_to\_form(“Leave Policy”, self.leave\_policy)).
  - Call the validation error handler Platform.throw(msg, title = translated “Annual Allocation Exceeded”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing leave count](operations-024.md#op-348c8091fbf8d8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L41) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1012) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L992)

<a id="op-b86ec7bb5e09b3"></a>
### Leave Allocation.get monthly earned leave

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_get_monthly_earned_leave`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Employee” via get\_value · read “Leave Policy Detail” via get\_value · read “Leave Type” via get\_value.

**Explicit results** \_get\_monthly\_earned\_leave(doj, annual\_allocation, frequency, rounding).

**Local steps**

- Set doj from Platform.db.get\_value(“Employee”, self.employee, “date\_of\_joining”).
- Set annual\_allocation from Platform.db.get\_value(“Leave Policy Detail”, mapping(“parent” → self.leave\_policy, “leave\_type” → self.leave\_type), “annual\_allocation”).
- Set tuple(frequency, rounding) from Platform.db.get\_value(“Leave Type”, self.leave\_type, list(“earned\_leave\_frequency”, “rounding”)).
- Return \_get\_monthly\_earned\_leave(doj, annual\_allocation, frequency, rounding).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0042.json#L6478) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1016) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L996)

<a id="op-b3a381336a3a34"></a>
### Leave Allocation.create leave adjustment

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_create_leave_adjustment`

**Inputs** self, adjustment\_type, leaves\_to\_adjust, posting\_date, reason\_for\_adjustment = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** request new\_doc for “Leave Adjustment” · call save on leave\_adjustment · call submit on leave\_adjustment · msgprint with translated “Adjustment Created Successfully”.

**Local steps**

- Set leave\_adjustment from Platform.new\_doc(“Leave Adjustment”, employee = self.employee, leave\_type = self.leave\_type, adjustment\_type = adjustment\_type, leaves\_to\_adjust = leaves\_to\_adjust, …).
- Evaluate leave\_adjustment.save().
- Evaluate leave\_adjustment.submit().
- Evaluate Platform.msgprint(translated “Adjustment Created Successfully”, indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1013) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L993)

<a id="op-c4b2b1f26c64d7"></a>
### Leave Allocation.retry failed allocations

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_leave_allocation_retry_failed_allocations`

**Inputs** self, failed\_allocations.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Leave Type” via get\_cached\_doc · read “Leave Policy Detail” via get\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to complete this action”.

**Local steps**

- If not Platform.has\_permission(doctype = “Leave Allocation”, ptype = “write”, user = Platform.session.user).
  - Call the validation error handler Platform.throw(translated “You do not have permission to complete this action”, Platform.PermissionError).
- Bind dependencies update\_previous\_leave\_allocation.
- Set leave\_type from Platform.get\_cached\_doc(“Leave Type”, self.leave\_type).
- Set annual\_allocation from Platform.get\_value(“Leave Policy Detail”, mapping(“parent” → self.leave\_policy, “leave\_type” → self.leave\_type), “annual\_allocation”).
- Set requested\_dates from set of getdate(row at “allocation\_date”) for row drawn from failed\_allocations.
  - Draw row from failed\_allocations.
- Evaluate self.reload().
- For each row in self.earned\_leave\_schedule.
  - If not (row.failed and row.attempted and getdate(row.allocation\_date) belongs to requested\_dates).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.failed → row.attempted → getdate(row.allocation\_date) belongs to requested\_dates.
    - Continue with the next iteration or loop test.
  - Evaluate update\_previous\_leave\_allocation(self, annual\_allocation, leave\_type, row.number\_of\_leaves, allocated\_via = “Manually”, …).
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype = “Leave Allocation”, ptype = “write”, user = Platform.session.user) · configured or stored value from Platform.get\_cached\_doc(“Leave Type”, self.leave\_type).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L42) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1021) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1001)

<a id="op-1601b337acf172"></a>
### Get previous allocation

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_get_previous_allocation`

**Inputs** from\_date, leave\_type, employee.

**Explicit results** allocations at 0 when allocations, otherwise no value.

**Local steps**

- Set Allocation from Platform.qb.DocType(“Leave Allocation”).
- Set allocations from nested operand in the contract(nested operand in the contract).orderby(Allocation.to\_date, order = nested operand in the contract.qb.desc).limit(1).run(as\_dict = true).
- Return allocations at 0 when allocations, otherwise no value.
  - Value choice on allocations — true gives allocations at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L1602) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1010) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L990)

<a id="op-8da552079bde04"></a>
### Get leave allocation for period

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_get_leave_allocation_for_period`

**Inputs** employee, leave\_type, from\_date, to\_date, exclude\_allocation = no value.

**Explicit results** (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0.0).

**Local steps**

- Bind dependencies Sum.
- Set Allocation from Platform.qb.DocType(“Leave Allocation”).
- Return (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest … at 0 → 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L1975) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1009) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L989)

<a id="op-a08e305433891a"></a>
### Get carry forwarded leaves

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_get_carry_forwarded_leaves`

**Inputs** employee, leave\_type, date, carry\_forward = no value.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** unused\_leaves.

**Local steps**

- Set unused\_leaves from 0.0.
- Set previous\_allocation from get\_previous\_allocation(date, leave\_type, employee).
- If (carry\_forward and previous\_allocation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in carry\_forward → previous\_allocation.
  - Evaluate validate\_carry\_forward(leave\_type).
  - Set unused\_leaves from get\_unused\_leaves(employee, leave\_type, previous\_allocation.from\_date, previous\_allocation.to\_date).
  - If unused\_leaves.
    - Set max\_carry\_forwarded\_leaves from Platform.db.get\_value(“Leave Type”, leave\_type, “maximum\_carry\_forwarded\_leaves”).
    - If (max\_carry\_forwarded\_leaves and unused\_leaves &gt; flt(max\_carry\_forwarded\_leaves)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_carry\_forwarded\_leaves → unused\_leaves &gt; flt(max\_carry\_forwarded\_leaves).
      - Set unused\_leaves from flt(max\_carry\_forwarded\_leaves).
- Return unused\_leaves.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L2418) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1008) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L988)

<a id="op-0d58f22383991c"></a>
### Get unused leaves

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_get_unused_leaves`

**Inputs** employee, leave\_type, from\_date, to\_date.

**Record and data access** read “Leave Ledger Entry” via get\_all.

**Explicit results** flt(leaves at 0 at “leaves”).

**Local steps**

- Set leaves from Platform.get\_all(“Leave Ledger Entry”, filters = mapping(“employee” → employee, “leave\_type” → leave\_type, “from\_date” → tuple(“&gt;=”, from\_date), “to\_date” → tuple(“&lt;=”, to\_date)), or\_filters = mapping(“is\_ ….
- Return flt(leaves at 0 at “leaves”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L2746) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1011) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L991)

<a id="op-eb0a99f0b3df02"></a>
### Validate carry forward

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_validate_carry_forward`

**Inputs** leave\_type.

**Record and data access** read “Leave Type” via get\_value.

**Explicit failure paths** validation helper — translated “Leave Type {0} cannot be carry-forwarded”.format(leave\_type).

**Local steps**

- If not Platform.db.get\_value(“Leave Type”, leave\_type, “is\_carry\_forward”).
  - Call the validation error handler Platform.throw(translated “Leave Type {0} cannot be carry-forwarded”.format(leave\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L3055) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1036) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1016)

<a id="op-b302ad433928fa"></a>
### Show expire leave dialog

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_show_expire_leave_dialog`

**Inputs** expired\_leaves, leave\_type.

**State and service calls** msgprint.

**Local steps**

- Evaluate Platform.msgprint(title = translated “Leaves Expired”, msg = translated “{0} leaves from allocation for {1} leave type have expired and will be processed during the next scheduled j …”.format(Platform.bold ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L3194) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1035) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1015)

<a id="op-99448f154559de"></a>
### Expire carried forward allocation

`operation_workforce_human_resources_record_definitions_leave_allocation_business_behavior_expire_carried_forward_allocation`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to complete this action”.

**Local steps**

- If Platform.has\_permission(doctype = “Leave Allocation”, ptype = “submit”, user = Platform.session.user).
  - Evaluate process\_expired\_allocation().
- Otherwise.
  - Call the validation error handler Platform.throw(translated “You do not have permission to complete this action”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype = “Leave Allocation”, ptype = “submit”, user = Platform.session.user).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L3489) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1007) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L987)

<a id="op-df41c71fd3dd79"></a>
### Get data

`operation_workforce_human_resources_record_definitions_leave_allocation_leave_allocation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “leave\_allocation”, “transactions” → list(mapping(“items” → list(“Compensatory Leave Request”)), mapping(“items” → list(“Leave Encashment”)), mapping(“items” → list(“Leave Adjustment”)))).

**Local steps**

- Return mapping(“fieldname” → “leave\_allocation”, “transactions” → list(mapping(“items” → list(“Compensatory Leave Request”)), mapping(“items” → list(“Leave Encashment”)), mapping(“items” → list(“Leave Adjustment”)))).

[Applicable decision contract](../../../workforce-decision-contracts/part-0043.json#L3682) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1037) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1017)

## Record · Leave application

[Record definition](../../../../data/record-types/leave_application.json)

<a id="op-cc3b5f92bc87e3"></a>
### Leave Application.get feed

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_get_feed`

**Inputs** self.

**Explicit results** translated “{0}: From {0} of type {1}”.format(self.employee\_name, self.leave\_type).

**Local steps**

- Return translated “{0}: From {0} of type {1}”.format(self.employee\_name, self.leave\_type).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L3595) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1170) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1149)

<a id="op-c290e67d112f75"></a>
### Leave Application.after insert

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.notify\_approver().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L3676) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1158) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1137)

<a id="op-e343acb7b27ce2"></a>
### Leave Application.validate

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_validate`

**Inputs** self.

**Record and data access** read “Leave Type” via get\_value.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate set\_employee\_name(self).
- Evaluate self.validate\_dates().
- Evaluate self.validate\_balance\_leaves().
- Evaluate self.validate\_leave\_overlap().
- Evaluate self.validate\_max\_days().
- Evaluate self.show\_block\_day\_warning().
- Evaluate self.validate\_block\_days().
- Evaluate self.validate\_salary\_processed\_days().
- Evaluate self.validate\_attendance().
- Evaluate self.set\_half\_day\_date().
- If Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_optional\_leave”).
  - Evaluate self.validate\_optional\_leave().
- Evaluate self.validate\_applicable\_after().
- Evaluate self.validate\_for\_self\_approval().
- Evaluate self.validate\_leave\_approver().
- Evaluate self.set\_leave\_approver\_name().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-026.md#op-df01a1c55939ed), [validate balance leaves](operations-026.md#op-9e153ccdb44db9), [validate leave overlap](operations-026.md#op-b466c63a4e6f98), [validate max days](operations-026.md#op-406eabee0a5c29), [show block day warning](operations-026.md#op-f49b4a7f22ea52), [validate block days](operations-026.md#op-9755303aea9580), [validate salary processed days](operations-026.md#op-850313d4c3bfab), [validate attendance](operations-027.md#op-1016772ab91cf0), [set half day date](operations-027.md#op-daf6c3e3da92b5), [validate optional leave](operations-027.md#op-5927b17310e1be), [validate applicable after](operations-026.md#op-5d1c65a03cba04), [validate for self approval](operations-027.md#op-bef34830bba880), [validate leave approver](operations-027.md#op-686622a0fdb8a1), [set leave approver name](operations-027.md#op-be2f59441019a0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L3725) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1189) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1168)

<a id="op-7ce5ab3260ac93"></a>
### Leave Application.on update

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_on_update`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value.

**Local steps**

- If (self.status equals “Open” and self.docstatus &lt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Open” → self.docstatus &lt; 1.
  - If Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).
    - Evaluate self.notify\_leave\_approver().
- Evaluate share\_doc\_with\_approver(self, self.leave\_approver).
- Evaluate self.publish\_update().
- Evaluate self.notify\_approval\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify leave approver](operations-027.md#op-63d763b6f10d3e), [publish update](operations-026.md#op-c04730ffb8624b).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L4135) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1180) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1159)

<a id="op-f2487ccc2f4cce"></a>
### Leave Application.on submit

`operation_workforce_human_resources_record_definitions_leave_application_business_behavior_leave_application_on_submit`

**Inputs** self.

**Record and data access** read “HR Settings” via get\_single\_value · read “Leave Type” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only Leave Applications with status 'Approved' and 'Rejected' can be submitted”.

**Local steps**

- <a id="op-f2487ccc2f4cce-guard-2"></a>If self.status belongs to list(“Open”, “Cancelled”).
  - Call the validation error handler Platform.throw(translated “Only Leave Applications with status 'Approved' and 'Rejected' can be submitted”).
- Evaluate self.validate\_back\_dated\_application().
- Evaluate self.update\_attendance().
- If Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).
  - Evaluate self.notify\_employee().
- Evaluate self.create\_leave\_ledger\_entry().
- Set leave\_allocation from self.get\_leave\_allocation().
- If not leave\_allocation.
  - Return no value.
- Set to\_date from leave\_allocation.get(“to\_date”).
- Set can\_expire from not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_carry\_forward”).
- If (to\_date &lt; getdate() and can\_expire).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_date &lt; getdate() → can\_expire.
  - Set args from Platform.\_dict(leaves = self.total\_leave\_days, from\_date = to\_date, to\_date = to\_date, is\_carry\_forward = 0).
  - Evaluate create\_leave\_ledger\_entry(self, args).
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status belongs to list(“Open”, “Cancelled”), self.status = “Open” selects the branch that calls the validation-error handler with translated “Only Leave Applications with status 'Approved' and 'Rejected' can be submitted”. With self.status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f2487ccc2f4cce-guard-2)

**Methods declared on this owner** [validate back dated application](operations-026.md#op-829ee6f8253cd6), [update attendance](operations-026.md#op-4ddcfffc33cfe6), [notify employee](operations-027.md#op-66beeda9965da8), [create leave ledger entry](operations-027.md#op-d746e34cb3bd0a), [get leave allocation](operations-026.md#op-2d40054236b079).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “send\_leave\_notification”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0049.json#L4350) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1179) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1158)
