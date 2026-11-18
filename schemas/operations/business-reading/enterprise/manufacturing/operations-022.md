# Production · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-9c7693c17b45b2"></a>
### Job Card.validate input from previous operations

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_input_from_previous_operations`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with OperationSequenceError — translated “Job Card {0}: Completed Qty and Process Loss of operation {1} add up to {2}, but the previous operation {3}  …”.format(bold(self.name), bold(self.operation), bold(self.get\_qty\_with\_uom(input\_qt ….

**Local steps**

- If (self.is\_corrective\_job\_card or self.track\_semi\_finished\_goods or not self.sequence\_id).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → self.track\_semi\_finished\_goods → not self.sequence\_id.
  - Return no value.
- Set previous\_operations from self.get\_previous\_operations().
- If not previous\_operations.
  - Return no value.
- Set previous from min(previous\_operations, key = deferred anonymous expression).
- Set precision from self.precision(“total\_completed\_qty”).
- Set input\_qty from flt((self.get\_operation\_input\_qty() + flt(self.process\_loss\_qty)), precision).
- Set excess\_qty from flt((input\_qty − flt(previous.completed\_qty)), precision).
- <a id="op-9c7693c17b45b2-guard-15"></a>If excess\_qty ≤ 0.
  - Return no value.
- If (previous.status equals “Completed” and excess\_qty ≤ flt(self.process\_loss\_qty, precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous.status equals “Completed” → excess\_qty ≤ flt(self.process\_loss\_qty, precision).
  - Set self.process\_loss\_qty from flt((self.process\_loss\_qty − excess\_qty), self.precision(“process\_loss\_qty”)).
  - Set self.for\_quantity from flt((self.for\_quantity − excess\_qty), self.precision(“for\_quantity”)).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Job Card {0}: Completed Qty and Process Loss of operation {1} add up to {2}, but the previous operation {3}  …”.format(bold(self.name), bold(self.operation), bold(self.get\_qty\_wi ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison excess\_qty ≤ 0, excess\_qty = 0 selects the branch that returns no value. With excess\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9c7693c17b45b2-guard-15)

**Methods declared on this owner** [get previous operations](operations-021.md#op-b9f7fc6e84e37d), [get operation input qty](operations-021.md#op-8fc5201c511be7), [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L841)

<a id="op-45f625da05bc1a"></a>
### Job Card.validate previous operation manufactured qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_previous_operation_manufactured_quantity`

**Inputs** self, row, current\_operation\_qty.

**Explicit failure paths** validation helper with OperationSequenceError — translated “Job Card {0}: As per the sequence of the operations in the work order {1}, submit the manufacturing entry fo …”.format(bold(self.name), bold(get\_link\_to\_form(“Work Order”, self.work\_order)), bo … · validation helper with OperationSequenceError — translated “The completed quantity {0} of an operation {1} cannot be greater than the manufactured quantity {2} of a pre …”.format(bold(self.get\_qty\_with\_uom(current\_operation\_qty)), bold(self.operation),  ….

**Local steps**

- Set manufactured\_qty from flt(row.manufactured\_qty).
- If not manufactured\_qty.
  - Call the validation error handler Platform.throw(translated “Job Card {0}: As per the sequence of the operations in the work order {1}, submit the manufacturing entry fo …”.format(bold(self.name), bold(get\_link\_to\_form(“Work Order”, self.w ….
- If manufactured\_qty &lt; current\_operation\_qty.
  - Call the validation error handler Platform.throw(translated “The completed quantity {0} of an operation {1} cannot be greater than the manufactured quantity {2} of a pre …”.format(bold(self.get\_qty\_with\_uom(current\_operation\_qty)), bold(se ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L460)

<a id="op-cc887de2e2ae12"></a>
### Job Card.validate work order

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_work_order`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You can't make any changes to Job Card since Work Order is closed.”.

**Local steps**

- If self.is\_work\_order\_closed().
  - Call the validation error handler Platform.throw(translated “You can't make any changes to Job Card since Work Order is closed.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is work order closed](operations-022.md#op-082c74472582c6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L469)

<a id="op-c24c3d4a3f0f60"></a>
### Job Card.set employees

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_employees`

**Inputs** self.

**Local steps**

- Set self.employee from list().
- For each item in self.time\_logs.
  - If not any(generator of d.employee equals item.employee for d drawn from self.employee).
    - Draw d from self.employee.
    - Evaluate self.append(“employee”, mapping(“employee” → item.employee, “completed\_qty” → 0.0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0474.json#L2648) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L425)

<a id="op-082c74472582c6"></a>
### Job Card.is work order closed

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_is_work_order_closed`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value.

**Explicit results** true · false.

**Local steps**

- If self.work\_order.
  - Set status from Platform.get\_value(“Work Order”, self.work\_order, “status”).
  - If status belongs to CLOSED\_WORK\_ORDER\_STATUSES.
    - Return true.
- Return false.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L412)

<a id="op-9b5fceb3cbef1b"></a>
### Job Card.update status in workstation

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_status_in_workstation`

**Inputs** self, status.

**State and service calls** request set\_value on “Workstation”.

**Explicit results** no value.

**Local steps**

- If not self.workstation.
  - Return no value.
- Evaluate Platform.db.set\_value(“Workstation”, self.workstation, “status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0474.json#L2995) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L444)

<a id="op-8245158e6b54c7"></a>
### Job Card.add time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_add_time_logs`

**Inputs** self, remaining named values kwargs.

**State and service calls** call db\_update on row · call save on self.

**Local steps**

- Set kwargs from Platform.\_dict(kwargs).
- If (not kwargs.employees and kwargs.to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.employees → kwargs.to\_time.
  - For each row in self.time\_logs.
    - If (not row.to\_time and row.from\_time).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.to\_time → row.from\_time.
      - Set row.to\_time from kwargs.to\_time.
      - Set row.time\_in\_mins from time\_diff\_in\_minutes(row.to\_time, row.from\_time).
      - If kwargs.get(“completed\_qty”) is distinct from no value.
        - Set row.completed\_qty from kwargs.completed\_qty.
        - Set row.process\_loss\_qty from flt(kwargs.process\_loss\_qty, row.precision(“process\_loss\_qty”)).
      - Evaluate row.db\_update().
- Otherwise.
  - Evaluate self.add\_time\_logs\_for\_employess(kwargs).
- Evaluate self.validate\_time\_logs(save = true).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add time logs for employess](operations-022.md#op-a850f16863a1a5), [validate time logs](operations-018.md#op-08f8db941f3219).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L384)

<a id="op-a850f16863a1a5"></a>
### Job Card.add time logs for employess

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_add_time_logs_for_employess`

**Inputs** self, kwargs.

**State and service calls** call db\_update on row · call db\_set on self.

**Explicit results** no value.

**Local steps**

- If (not kwargs.from\_time and not kwargs.to\_time and kwargs.get(“completed\_qty”) is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.from\_time → not kwargs.to\_time → kwargs.get(“completed\_qty”) is distinct from no value.
  - Evaluate self.update\_latest\_time\_log\_qty(kwargs).
  - Evaluate self.set\_status(update\_status = true).
  - Return no value.
- Set row from no value.
- Set update\_status from false.
- Set kwargs.employees from (kwargs.employees or list(Platform.\_dict(employee = no value))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.employees → list(Platform.\_dict(employee = no value)).
- Set cycle\_log from next(generator of row for row drawn from reversed(self.time\_logs) where not row.to\_time, no value).
  - Draw row from reversed(self.time\_logs), keep a combination only if (not row.to\_time).
- For each employee in kwargs.employees.
  - Set kwargs.employee from employee.get(“employee”).
  - If (kwargs.from\_time and not kwargs.to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.from\_time → not kwargs.to\_time.
    - If kwargs.get(“qty”) is distinct from no value.
      - Set kwargs.completed\_qty from kwargs.qty.
    - Set row from self.append(“time\_logs”, kwargs).
    - Evaluate row.db\_update().
    - Evaluate self.db\_set(“status”, “Work In Progress”).
  - Otherwise.
    - Set update\_status from true.
    - For each row in self.time\_logs.
      - If (row.to\_time or row.employee differs from kwargs.employee).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.to\_time → row.employee differs from kwargs.employee.
        - Continue with the next iteration or loop test.
      - Set row.to\_time from kwargs.to\_time.
      - Set row.time\_in\_mins from time\_diff\_in\_minutes(row.to\_time, row.from\_time).
      - If kwargs.get(“sub\_operation”).
        - Set row.operation from kwargs.get(“sub\_operation”).
      - If row is identical to cycle\_log.
        - Set row.completed\_qty from kwargs.completed\_qty.
        - Set row.process\_loss\_qty from flt(kwargs.process\_loss\_qty, row.precision(“process\_loss\_qty”)).
      - Evaluate row.db\_update().
  - Evaluate self.set\_status(update\_status = update\_status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update latest time log qty](operations-022.md#op-d05f89328c3c74), [set status](operations-021.md#op-575a8477f4fcfd).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L385)

<a id="op-d05f89328c3c74"></a>
### Job Card.update latest time log qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_update_latest_time_log_qty`

**Inputs** self, kwargs.

**State and service calls** call db\_update on self.time\_logs at negative 1.

**Explicit results** no value.

**Local steps**

- If not self.time\_logs.
  - Return no value.
- Set self.time\_logs at negative 1.completed\_qty from kwargs.completed\_qty.
- Evaluate self.time\_logs at negative 1.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L838)

<a id="op-8ad35d0ced9364"></a>
### Job Card.update workstation status

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_workstation_status`

**Inputs** self.

**Record and data access** read “Job Card” via get\_all · resolve a document from “Workstation” via get\_doc.

**State and service calls** call db\_set on workstation.

**Local steps**

- Set job\_cards from Platform.get\_all(“Job Card”, fields = list(“name”, “status”), filters = mapping(“workstation” → self.workstation, “docstatus” → 0, “status” → tuple(“!=”, “Completed”))).
- Set statuses from set of row.status for row drawn from job\_cards where row.name differs from self.name.
  - Draw row from job\_cards, keep a combination only if (row.name differs from self.name).
- If self.docstatus equals 0.
  - Evaluate statuses.add(self.status).
- Set status from “Off”.
- If “Work In Progress” belongs to statuses.
  - Set status from “Production”.
- Otherwise.
  - If “On Hold” belongs to statuses.
    - Set status from “Idle”.
- Set workstation from Platform.get\_doc(“Workstation”, self.workstation).
- If workstation.status differs from status.
  - Evaluate workstation.db\_set(“status”, status, notify = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L449)

<a id="op-0f7cba92137b67"></a>
### Job Card.start timer

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_start_timer`

**Inputs** self, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).
- Evaluate self.validate\_docstatus().
- Evaluate self.validate\_transfer\_qty().
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- If isinstance(kwargs.employees, str).
  - Set kwargs.employees from list(mapping(“employee” → kwargs.employees)).
- Evaluate self.validate\_not\_already\_started(kwargs.employees).
- If kwargs.start\_time.
  - Evaluate self.add\_time\_logs(from\_time = kwargs.start\_time, employees = kwargs.employees).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docstatus](operations-022.md#op-65503f3ca6264d), [validate transfer qty](operations-020.md#op-20d4d21de865b9), [validate not already started](operations-022.md#op-3ce867212e1ff7), [add time logs](operations-022.md#op-8245158e6b54c7).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L441)

<a id="op-3ce867212e1ff7"></a>
### Job Card.validate not already started

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_not_already_started`

**Inputs** self, employees.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Job Card {0} is already started for {1}.”.format(bold(self.name), “, ”.join(generator of bold((employee or translated “an operator”)) for employee drawn from already\_started)).

**Local steps**

- Set started\_employees from set of log.employee for log drawn from self.time\_logs where (log.from\_time and not log.to\_time).
  - Draw log from self.time\_logs, keep a combination only if ((log.from\_time and not log.to\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in log.from\_time → not log.to\_time.
- Set requested\_employees from set of row.get(“employee”) for row drawn from (employees or list()).
  - Draw row from (employees or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employees → list().
- Set already\_started from (started\_employees bitwise and requested\_employees) when requested\_employees, otherwise started\_employees.
  - Value choice on requested\_employees — true gives (started\_employees bitwise and requested\_employees), false gives started\_employees.
- If already\_started.
  - Call the validation error handler Platform.throw(translated “Job Card {0} is already started for {1}.”.format(bold(self.name), “, ”.join(generator of bold((employee or nested operand in the contract(nested operand in the contract))) for em ….
    - Draw employee from already\_started.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee → translated “an operator”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L843)

<a id="op-afb087747b2321"></a>
### Job Card.complete job card

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_complete_job_card`

**Inputs** self, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).
- Evaluate self.validate\_docstatus().
- Evaluate self.validate\_transfer\_qty().
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Evaluate self.set\_for\_quantity(kwargs).
- Evaluate self.validate\_complete\_job\_card\_qty(kwargs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docstatus](operations-022.md#op-65503f3ca6264d), [validate transfer qty](operations-020.md#op-20d4d21de865b9), [set for quantity](operations-022.md#op-8c038ba7365cd7), [validate complete job card qty](operations-022.md#op-57c4612303e43a).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L392)

<a id="op-8c038ba7365cd7"></a>
### Job Card.set for quantity

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_for_quantity`

**Inputs** self, kwargs.

**Explicit results** no value.

**Local steps**

- If not flt(kwargs.for\_quantity).
  - Return no value.
- Set processed\_qty from (flt(self.total\_completed\_qty) + flt(self.process\_loss\_qty)).
- If sub\_operation bound to self.get\_cycle\_sub\_operation(kwargs).
  - Set processed\_qty from self.get\_sub\_operation\_processed\_qty(sub\_operation).
  - If processed\_qty &lt; max(generator of self.get\_sub\_operation\_processed\_qty(row) for row drawn from self.sub\_operations).
    - Draw row from self.sub\_operations.
    - Return no value.
- Set self.for\_quantity from flt((processed\_qty + flt(kwargs.for\_quantity)), self.precision(“for\_quantity”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get cycle sub operation](operations-022.md#op-c7639a01607ef7), [get sub operation processed qty](operations-022.md#op-fa2b42be31b171).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L427)

<a id="op-fa2b42be31b171"></a>
### Job Card.get sub operation processed qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_sub_operation_processed_qty`

**Inputs** self, row.

**Explicit results** flt((flt(row.completed\_qty) + flt(row.process\_loss\_qty)), self.precision(“for\_quantity”)).

**Local steps**

- Return flt((flt(row.completed\_qty) + flt(row.process\_loss\_qty)), self.precision(“for\_quantity”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L824)

<a id="op-0aab7e103d39b4"></a>
### Job Card.get pending qty after cycle

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_pending_qty_after_cycle`

**Inputs** self, kwargs.

**Explicit results** flt(kwargs.pending\_qty) · max(flt(((self.for\_quantity − completed\_qty) − self.process\_loss\_qty), self.precision(“pending\_qty”)), 0.0).

**Local steps**

- Set sub\_operation from self.get\_cycle\_sub\_operation(kwargs).
- If not sub\_operation.
  - Return flt(kwargs.pending\_qty).
- Set completed\_qty from min(generator of (flt(row.completed\_qty) + flt(kwargs.qty) when row is identical to sub\_operation, otherwise 0.0) for row drawn from self.sub\_operations).
  - Draw row from self.sub\_operations.
  - Value choice on row is identical to sub\_operation — true gives flt(kwargs.qty), false gives 0.0.
- Return max(flt(((self.for\_quantity − completed\_qty) − self.process\_loss\_qty), self.precision(“pending\_qty”)), 0.0).

**Methods declared on this owner** [get cycle sub operation](operations-022.md#op-c7639a01607ef7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L820)

<a id="op-c7639a01607ef7"></a>
### Job Card.get cycle sub operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_cycle_sub_operation`

**Inputs** self, kwargs.

**Explicit results** no value · next(generator of row for row drawn from self.sub\_operations where row.sub\_operation equals kwargs.sub\_operation, no value).

**Local steps**

- If not kwargs.sub\_operation.
  - Return no value.
- Return next(generator of row for row drawn from self.sub\_operations where row.sub\_operation equals kwargs.sub\_operation, no value).
  - Draw row from self.sub\_operations, keep a combination only if (row.sub\_operation equals kwargs.sub\_operation).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L813)

<a id="op-65503f3ca6264d"></a>
### Job Card.validate docstatus

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_record_state`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cancelled Job Card cannot be processed.” · validation helper — translated “Submitted Job Card cannot be processed.”.

**Local steps**

- <a id="op-65503f3ca6264d-guard-2"></a>If self.docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “Cancelled Job Card cannot be processed.”).
- <a id="op-65503f3ca6264d-guard-5"></a>If self.docstatus equals 1.
  - Call the validation error handler Platform.throw(translated “Submitted Job Card cannot be processed.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Cancelled Job Card cannot be processed.”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-65503f3ca6264d-guard-2)
- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that calls the validation-error handler with translated “Submitted Job Card cannot be processed.”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-65503f3ca6264d-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0474.json#L5670) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L462)

<a id="op-57c4612303e43a"></a>
### Job Card.validate complete job card qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_complete_job_card_quantity`

**Inputs** self, kwargs.

**State and service calls** call save on self · call submit on self · msgprint with translated “Job Card {0} has been completed”.format(get\_link\_to\_form(“Job Card”, self.name)).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Completed quantity cannot be negative.” · validation helper — translated “Pending quantity cannot be negative.” · validation helper — translated “Process loss quantity cannot be negative.” · validation helper — translated “Pending quantity cannot be greater than the for quantity.”.

**Local steps**

- If flt(kwargs.qty) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Completed quantity cannot be negative.”).
- If (flt(kwargs.pending\_qty) and flt(kwargs.pending\_qty) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(kwargs.pending\_qty) → flt(kwargs.pending\_qty) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Pending quantity cannot be negative.”).
- If (flt(kwargs.process\_loss\_qty) and flt(kwargs.process\_loss\_qty) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(kwargs.process\_loss\_qty) → flt(kwargs.process\_loss\_qty) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Process loss quantity cannot be negative.”).
- If (flt(kwargs.pending\_qty) and flt(kwargs.pending\_qty) &gt; self.for\_quantity).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(kwargs.pending\_qty) → flt(kwargs.pending\_qty) &gt; self.for\_quantity.
  - Call the validation error handler Platform.throw(translated “Pending quantity cannot be greater than the for quantity.”).
- Evaluate self.validate\_completion\_qty\_split(kwargs).
- Set self.process\_loss\_qty from (flt(self.process\_loss\_qty) + flt(kwargs.process\_loss\_qty)).
- Set self.pending\_qty from self.get\_pending\_qty\_after\_cycle(kwargs).
- If kwargs.end\_time.
  - Evaluate self.add\_time\_logs(to\_time = kwargs.end\_time, completed\_qty = kwargs.qty, process\_loss\_qty = kwargs.process\_loss\_qty, employees = self.employee, …).
  - If self.docstatus equals 1.
    - Evaluate self.update\_work\_order().
- Otherwise.
  - Evaluate self.add\_time\_logs(completed\_qty = kwargs.qty, employees = self.employee).
  - Evaluate self.save().
- If kwargs.auto\_submit.
  - Evaluate self.submit().
  - If not self.finished\_good.
    - Return no value.
  - Evaluate self.make\_stock\_entry\_for\_semi\_fg\_item(kwargs.auto\_submit).
  - Evaluate Platform.msgprint(translated “Job Card {0} has been completed”.format(get\_link\_to\_form(“Job Card”, self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate completion qty split](operations-022.md#op-3447571c51b69c), [get pending qty after cycle](operations-022.md#op-0aab7e103d39b4), [add time logs](operations-022.md#op-8245158e6b54c7), [update work order](operations-020.md#op-8db504b795b5e5), [make stock entry for semi fg item](operations-022.md#op-3efd7612861afc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L451)

<a id="op-3447571c51b69c"></a>
### Job Card.validate completion qty split

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_completion_quantity_split`

**Inputs** self, kwargs.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Completed Quantity ({0}), Pending Quantity ({1}) and Process Loss Quantity ({2}) must add up to the Qty to M …”.format(bold(self.get\_qty\_with\_uom(kwargs.qty)), bold(self.get\_qty\_with\_uom(kwargs ….

**Local steps**

- If not flt(kwargs.for\_quantity).
  - Return no value.
- Set precision from self.precision(“total\_completed\_qty”).
- Set accounted\_qty from flt(((flt(kwargs.qty, precision) + flt(kwargs.pending\_qty, precision)) + flt(kwargs.process\_loss\_qty, precision))).
- If flt(accounted\_qty, precision) equals flt(kwargs.for\_quantity, precision).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Completed Quantity ({0}), Pending Quantity ({1}) and Process Loss Quantity ({2}) must add up to the Qty to M …”.format(bold(self.get\_qty\_with\_uom(kwargs.qty)), bold(self.get\_qty\_ ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L452)

<a id="op-aed42d001b5de5"></a>
### Job Card.get consumed process loss

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_consumed_process_loss`

**Inputs** self.

**Explicit results** (query.run() at 0 at 0 or 0).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Entry”).
- Set query from nested operand in the contract.qb.from\_(table).select(Sum(table.process\_loss\_qty)).where(((table.purpose equals “Manufacture” bitwise and table.job\_card equals self.name) bitwise and table.docstatus equals 1)).
- Return (query.run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0475.json#L587) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L396)

<a id="op-3efd7612861afc"></a>
### Job Card.make stock entry for semi fg item

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_make_stock_entry_for_semi_finished_goods_item`

**Inputs** self, auto\_submit = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Work Order” via get\_value · resolve a document from “Work Order” via get\_doc.

**State and service calls** call submit on ste.stock\_entry · call save on ste.stock\_entry · msgprint with translated “Stock Entry {0} has created”.format(get\_link\_to\_form(“Stock Entry”, ste.stock\_entry.name)).

**Explicit results** ste.stock\_entry.as\_dict().

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).
- Evaluate Platform.has\_permission(“Stock Entry”, “create”, throw = true).
- Evaluate validate\_job\_card\_submitted\_for\_manufacture(self).
- Bind dependencies ManufactureEntry.
- Set consumed\_process\_loss from self.get\_consumed\_process\_loss().
- Set ste from ManufactureEntry(mapping(“for\_quantity” → ((self.get\_qty\_to\_produce() − self.manufactured\_qty) − consumed\_process\_loss), “process\_loss\_qty” → max((self.process\_loss\_qty − consumed\_process\_loss), 0), “job\_c ….
- Evaluate ste.make\_stock\_entry().
- Set ste.stock\_entry.flags.ignore\_mandatory from true.
- Set wo\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
- Evaluate add\_additional\_cost(ste.stock\_entry, wo\_doc, self).
- Set ste.stock\_entry.pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
- Evaluate ste.stock\_entry.set\_secondary\_items\_from\_job\_card().
- For each row in ste.stock\_entry.items.
  - If ((row.secondary\_item\_type or row.valuation\_type) and not row.t\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (row.secondary\_item\_type or row.valuation\_type) → not row.t\_warehouse.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.secondary\_item\_type → row.valuation\_type.
    - Set row.t\_warehouse from self.target\_warehouse.
- If auto\_submit.
  - Evaluate ste.stock\_entry.submit().
- Otherwise.
  - Evaluate ste.stock\_entry.save().
- Evaluate Platform.msgprint(translated “Stock Entry {0} has created”.format(get\_link\_to\_form(“Stock Entry”, ste.stock\_entry.name))).
- Return ste.stock\_entry.as\_dict().

**Methods declared on this owner** [get consumed process loss](operations-022.md#op-aed42d001b5de5), [get qty to produce](operations-021.md#op-887b1fab0b5a92).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true), Platform.has\_permission(“Stock Entry”, “create”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L413)

<a id="op-0f94ad3ca2a055"></a>
### Get actual qty map

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_get_actual_qty_map`

**Inputs** rows.

**Explicit results** mapping() · mapping of tuple(row.item\_code, row.warehouse) → flt(row.actual\_qty) for row drawn from stock.

**Local steps**

- If not rows.
  - Return mapping().
- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set stock from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(neste ….
  - Draw row from rows.
  - Draw row from rows.
- Return mapping of tuple(row.item\_code, row.warehouse) → flt(row.actual\_qty) for row drawn from stock.
  - Draw row from stock.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L806)

<a id="op-df17634b598fe3"></a>
### Make subcontracting po

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_make_subcontracting_po`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Job Card”, source\_name, mapping(“Job Card” → mapping(“doctype” → “Purchase Order”)), target\_doc, …).
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L854)
