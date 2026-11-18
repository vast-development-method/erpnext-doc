# Production · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-ea0e3a2172d00f"></a>
### Job Card.validate

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_time\_logs().
- Evaluate self.set\_status().
- Evaluate self.set\_operation\_id().
- Evaluate self.reset\_required\_items().
- Evaluate self.set\_hour\_rate().
- Evaluate self.validate\_sequence\_id().
- Evaluate self.set\_sub\_operations().
- Evaluate self.update\_sub\_operation\_status().
- If self.sub\_operations.
  - Evaluate self.set\_total\_completed\_qty\_from\_sub\_operations().
- Evaluate self.validate\_on\_hold().
- Evaluate self.validate\_pending\_qty().
- Evaluate self.validate\_work\_order().
- Evaluate self.set\_employees().
- If self.docstatus equals 1.
  - Evaluate self.validate\_input\_from\_previous\_operations().
  - Evaluate self.validate\_semi\_finished\_goods().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate time logs](operations-018.md#op-08f8db941f3219), [set status](operations-021.md#op-575a8477f4fcfd), [set operation id](operations-021.md#op-2e78cd97f30110), [reset required items](operations-020.md#op-70426cdf04bb4b), [set hour rate](operations-018.md#op-86cee13c7b2b47), [validate sequence id](operations-021.md#op-3c9e51d3e8eb1e), [set sub operations](operations-018.md#op-19a3b1e1fd8366), [update sub operation status](operations-019.md#op-e0cc6f4811d94f), [set total completed qty from sub operations](operations-018.md#op-446c02fcbf7c52), [validate on hold](operations-018.md#op-5102d97c6d5c76), [validate pending qty](operations-018.md#op-a54fa70b3bebc1), [validate work order](operations-022.md#op-cc887de2e2ae12), [set employees](operations-022.md#op-c24c3d4a3f0f60), [validate input from previous operations](operations-022.md#op-9c7693c17b45b2), [validate semi finished goods](operations-018.md#op-4656738a8e3b40).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L450)

<a id="op-a54fa70b3bebc1"></a>
### Job Card.validate pending qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_pending_qty`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Pending Qty {0} cannot be more than the {1} left after the Total Completed Qty”.format(bold(self.get\_qty\_with\_uom(self.pending\_qty)), bold(self.get\_qty\_with\_uom(remaining\_qty))).

**Local steps**

- Set precision from self.precision(“total\_completed\_qty”).
- Set remaining\_qty from flt((flt(self.for\_quantity) − flt(self.total\_completed\_qty)), precision).
- If (flt(self.pending\_qty, precision) &gt; 0 and flt(self.pending\_qty, precision) &gt; remaining\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.pending\_qty, precision) &gt; 0 → flt(self.pending\_qty, precision) &gt; remaining\_qty.
  - Call the validation error handler Platform.throw(translated “Pending Qty {0} cannot be more than the {1} left after the Total Completed Qty”.format(bold(self.get\_qty\_with\_uom(self.pending\_qty)), bold(self.get\_qty\_with\_uom(remaining\_qty)))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L844)

<a id="op-86cee13c7b2b47"></a>
### Job Card.set hour rate

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_set_hour_rate`

**Inputs** self.

**Record and data access** read “Work Order Operation” via get\_value · read “Workstation” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (self.is\_corrective\_job\_card or not (self.workstation and self.operation\_id)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → not (self.workstation and self.operation\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.workstation → self.operation\_id.
  - Return no value.
- Set operation from Platform.db.get\_value(“Work Order Operation”, self.operation\_id, list(“workstation”, “hour\_rate”), as\_dict = true).
- If (operation and operation.workstation equals self.workstation and flt(operation.hour\_rate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in operation → operation.workstation equals self.workstation → flt(operation.hour\_rate).
  - Set self.hour\_rate from operation.hour\_rate.
- Otherwise.
  - Set self.hour\_rate from flt(Platform.get\_cached\_value(“Workstation”, self.workstation, “hour\_rate”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workstation”, self.workstation, “hour\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L832)

<a id="op-4656738a8e3b40"></a>
### Job Card.validate semi finished goods

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_semi_finished_goods`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Job Card {0} has no completed quantity yet. Click Start Job when the work begins, then click Complete Job an …”.format(bold(self.name)).

**Local steps**

- If (not self.track\_semi\_finished\_goods or self.is\_subcontracted).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.track\_semi\_finished\_goods → self.is\_subcontracted.
  - Return no value.
- If (self.items and not self.transferred\_qty and not self.skip\_material\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.items → not self.transferred\_qty → not self.skip\_material\_transfer.
  - Evaluate self.throw\_materials\_not\_moved().
- If (self.docstatus equals 1 and not (self.total\_completed\_qty or self.process\_loss\_qty or self.pending\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → not (self.total\_completed\_qty or self.process\_loss\_qty or self.pending\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.total\_completed\_qty → self.process\_loss\_qty → self.pending\_qty.
  - Call the validation error handler Platform.throw(translated “Job Card {0} has no completed quantity yet. Click Start Job when the work begins, then click Complete Job an …”.format(bold(self.name)), title = translated “Job Not Done Yet”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw materials not moved](operations-018.md#op-5e5f0d8ceb06d1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L801) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L463)

<a id="op-5e5f0d8ceb06d1"></a>
### Job Card.throw materials not moved

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_throw_materials_not_moved`

**Inputs** self.

**Explicit failure paths** validation helper — ((message + text in the contract) + text in the contract.join(still\_to\_move)).

**Local steps**

- Set still\_to\_move from list of translated “{0}: {1} moved out of {2}”.format(bold(row.item\_code), self.get\_qty\_with\_uom(row.transferred\_qty, row.item\_code), self.get\_qty\_with\_uom(row.required\_qty, row.item\_code)) for row drawn f ….
  - Draw row from self.get\_rows\_to\_move().
- Set message from translated “Move the raw materials to the Work In Progress warehouse {0} first. Click Move Materials on Job Card {1} and …”.format(bold(self.wip\_warehouse), bold(self.name)).
- Call the validation error handler Platform.throw(((message + text in the contract) + text in the contract.join(still\_to\_move)), title = translated “Raw Materials Not Moved”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty with uom](operations-021.md#op-796d4d5f140d45), [get rows to move](operations-018.md#op-17a84c2d0e756e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L837)

<a id="op-17a84c2d0e756e"></a>
### Job Card.get rows to move

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_rows_to_move`

**Inputs** self.

**Explicit results** list of row for row drawn from self.items where flt(row.transferred\_qty) &lt; flt(row.required\_qty).

**Local steps**

- Return list of row for row drawn from self.items where flt(row.transferred\_qty) &lt; flt(row.required\_qty).
  - Draw row from self.items, keep a combination only if (flt(row.transferred\_qty) &lt; flt(row.required\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L823)

<a id="op-aed0fc51b26059"></a>
### Job Card.get material shortages

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_material_shortages`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** shortages.

**Local steps**

- Set rows from list of row for row drawn from self.get\_rows\_to\_move() where row.source\_warehouse.
  - Draw row from self.get\_rows\_to\_move(), keep a combination only if (row.source\_warehouse).
- Set in\_stock from get\_actual\_qty\_map(rows).
- Set shortages from list().
- For each row in rows.
  - Set key from tuple(row.item\_code, row.source\_warehouse).
  - Set qty\_to\_move from (flt(row.required\_qty) − flt(row.transferred\_qty)).
  - Set available from max(flt(in\_stock.get(key)), 0).
  - Set in\_stock at key from (available − qty\_to\_move).
  - If available &lt; qty\_to\_move.
    - Evaluate shortages.append(mapping(“name” → row.name, “item\_code” → row.item\_code, “warehouse” → row.source\_warehouse, “qty\_to\_move” → qty\_to\_move, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.stock\_uom → row.uom.
- Return shortages.

**Methods declared on this owner** [get rows to move](operations-018.md#op-17a84c2d0e756e).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L817)

<a id="op-bb00d404f16fda"></a>
### Job Card.on update

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_job\_card\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate job card qty](operations-018.md#op-9e519725fb00ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L2674) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L417)

<a id="op-5102d97c6d5c76"></a>
### Job Card.validate on hold

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_on_hold`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.is\_paused or (self.time\_logs and self.has\_qty\_left\_to\_make())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_paused → (self.time\_logs and self.has\_qty\_left\_to\_make()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.time\_logs → self.has\_qty\_left\_to\_make().
  - Return no value.
- Set self.is\_paused from 0.
- Evaluate self.set\_status().
- Evaluate self.update\_sub\_operation\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has qty left to make](operations-018.md#op-f512a70c8aa91d), [set status](operations-021.md#op-575a8477f4fcfd), [update sub operation status](operations-019.md#op-e0cc6f4811d94f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L793) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L457)

<a id="op-f512a70c8aa91d"></a>
### Job Card.has qty left to make

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_has_qty_left_to_make`

**Inputs** self.

**Explicit results** flt(made\_qty, precision) &lt; flt(self.for\_quantity, precision).

**Local steps**

- Set precision from self.precision(“total\_completed\_qty”).
- Set made\_qty from (flt(self.total\_completed\_qty) + flt(self.process\_loss\_qty)).
- Return flt(made\_qty, precision) &lt; flt(self.for\_quantity, precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L826)

<a id="op-a6a4b67e8f3a55"></a>
### Job Card.set manufactured qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_manufactured_quantity`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set table\_name from “Stock Entry”.
- Set child\_name from “Stock Entry Detail”.
- If self.is\_subcontracted.
  - Set table\_name from “Subcontracting Receipt Item”.
- Set table from Platform.qb.DocType(table\_name).
- Set query from Platform.qb.from\_(table).where((table.job\_card equals self.name bitwise and table.docstatus equals 1)).
- If self.is\_subcontracted.
  - Set query from query.select(Sum(table.qty)).
- Otherwise.
  - Set child from Platform.qb.DocType(child\_name).
  - Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(Sum(child.transfer\_qty)).where((table.purpose equa ….
- Set qty from (query.run() at 0 at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.0.
- Set self.manufactured\_qty from flt(qty).
- Evaluate self.db\_set(“manufactured\_qty”, self.manufactured\_qty).
- Evaluate self.update\_semi\_finished\_good\_details().
- Evaluate self.set\_status(update\_status = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update semi finished good details](operations-020.md#op-26cdb8c91e0ce6), [set status](operations-021.md#op-575a8477f4fcfd).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L428)

<a id="op-9e519725fb00ff"></a>
### Job Card.validate job card qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_job_card_quantity`

**Inputs** self.

**Record and data access** read “Work Order Operation” via get\_value · read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Qty To Manufacture in the job card cannot be greater than Qty To Manufacture in the work order for the opera …”.format(bold(self.operation), form\_link).

**Local steps**

- If (self.is\_corrective\_job\_card or not (self.operation\_id and self.work\_order)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → not (self.operation\_id and self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.operation\_id → self.work\_order.
  - Return no value.
- Set wo\_qty from self.get\_work\_order\_qty\_details().operation\_qty.
- Set completed\_qty from flt(Platform.db.get\_value(“Work Order Operation”, self.operation\_id, “completed\_qty”)).
- Set over\_production\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- Set wo\_qty from (wo\_qty + ((wo\_qty × over\_production\_percentage) ÷ 100)).
- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set job\_card\_qty from nested operand in the contract(nested operand in the contract).select(Sum((nested operand in the contract − nested operand in the contract))).where((((nested operand in the contract equals nested operand i ….run().
- Set job\_card\_qty from flt(job\_card\_qty at 0 at 0) when job\_card\_qty, otherwise 0.
  - Value choice on job\_card\_qty — true gives flt(job\_card\_qty at 0 at 0), false gives 0.
- If (job\_card\_qty and (job\_card\_qty − completed\_qty) &gt; wo\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_card\_qty → (job\_card\_qty − completed\_qty) &gt; wo\_qty.
  - Set form\_link from get\_link\_to\_form(“Manufacturing Settings”, “Manufacturing Settings”).
  - Call the validation error handler Platform.throw(translated “Qty To Manufacture in the job card cannot be greater than Qty To Manufacture in the work order for the opera …”.format(bold(self.operation), form\_link), title = translated “Extra ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get work order qty details](operations-018.md#op-6c7465b8beb049).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L455)

<a id="op-19a3b1e1fd8366"></a>
### Job Card.set sub operations

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_subordinate_operations`

**Inputs** self.

**Record and data access** read “Sub Operation” via get\_all.

**Local steps**

- If (not self.sub\_operations and self.operation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sub\_operations → self.operation.
  - Set self.sub\_operations from list().
  - For each row in Platform.get\_all(“Sub Operation”, filters = mapping(“parent” → self.operation), fields = list(“operation”, “idx”), order\_by = “idx”).
    - Set row.status from “Pending”.
    - Set row.sub\_operation from row.operation.
    - Evaluate self.append(“sub\_operations”, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L4373) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L434)

<a id="op-6c7465b8beb049"></a>
### Job Card.get work order qty details

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_work_order_qty_details`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value · read “Work Order Operation” via get\_value.

**Explicit results** work\_order.

**Local steps**

- Set work\_order from (Platform.db.get\_value(“Work Order”, self.work\_order, list(“qty”, “track\_semi\_finished\_goods”), as\_dict = true) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Work Order”, self.work\_order, list(“qty”, “track\_semi\_finished\_goods”), as\_dict = true) → Platform.\_dict().
- Set output\_qty from (self.operation\_id and Platform.db.get\_value(“Work Order Operation”, self.operation\_id, “output\_qty”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.operation\_id → Platform.db.get\_value(“Work Order Operation”, self.operation\_id, “output\_qty”).
- Set work\_order.operation\_qty from get\_operation\_qty(work\_order, mapping(“output\_qty” → output\_qty)).
- Return work\_order.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L825)

<a id="op-d073a22519dae3"></a>
### Job Card.convert to current operation qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_convert_to_current_operation_qty`

**Inputs** self, rows, fields.

**Local steps**

- Set work\_order from self.get\_work\_order\_qty\_details().
- Set precision from self.precision(“total\_completed\_qty”).
- For each row in rows.
  - Set operation\_qty from get\_operation\_qty(work\_order, row).
  - If (not operation\_qty or operation\_qty equals work\_order.operation\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not operation\_qty → operation\_qty equals work\_order.operation\_qty.
    - Continue with the next iteration or loop test.
  - For each field in fields.
    - Set row at field from flt(((flt(row.get(field)) × work\_order.operation\_qty) ÷ operation\_qty), precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get work order qty details](operations-018.md#op-6c7465b8beb049).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L812)

<a id="op-8a74af0425b498"></a>
### Job Card.set secondary items

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_secondary_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.semi\_fg\_bom and not self.bom\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.semi\_fg\_bom → not self.bom\_no.
  - Return no value.
- Set qty from flt(self.for\_quantity).
- If (not self.semi\_fg\_bom and self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.semi\_fg\_bom → self.work\_order.
  - Set work\_order from self.get\_work\_order\_qty\_details().
  - If work\_order.operation\_qty.
    - Set qty from ((qty × flt(work\_order.qty)) ÷ work\_order.operation\_qty).
- Set items\_dict from get\_bom\_items\_as\_dict((self.semi\_fg\_bom or self.bom\_no), self.company, qty = qty, fetch\_exploded = 0, fetch\_secondary\_items = 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.semi\_fg\_bom → self.bom\_no.
- For each values in items\_dict.values().
  - Set values from Platform.\_dict(values).
  - Set secondary\_item from mapping(“item\_code” → values.item\_code, “stock\_qty” → values.qty, “item\_name” → values.item\_name, “stock\_uom” → values.stock\_uom, …).
  - Update secondary\_item at “stock\_qty” using − flt((secondary\_item at “stock\_qty” × (flt(values.process\_loss\_per) ÷ 100)), self.precision(“for\_quantity”)).
  - Evaluate self.append(“secondary\_items”, secondary\_item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get work order qty details](operations-018.md#op-6c7465b8beb049).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L431)

<a id="op-08f8db941f3219"></a>
### Job Card.validate time logs

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_time_logs`

**Inputs** self, save = false.

**Explicit results** no value.

**Local steps**

- Set self.total\_time\_in\_mins from 0.0.
- Set self.total\_completed\_qty from 0.0.
- If not self.get(“time\_logs”).
  - Return no value.
- For each d in self.get(“time\_logs”).
  - Evaluate self.validate\_time\_log\_row(d).
- Set self.total\_time\_in\_mins from flt(get\_workstation\_minutes(self.time\_logs), self.precision(“total\_time\_in\_mins”)).
- Set self.total\_completed\_qty from flt(self.total\_completed\_qty, self.precision(“total\_completed\_qty”)).
- If (save and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in save → self.docstatus equals 1.
  - Evaluate self.save\_time\_log\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate time log row](operations-018.md#op-05dd89a471cfa0), [save time log totals](operations-018.md#op-38abe446cd99fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L466)

<a id="op-05dd89a471cfa0"></a>
### Job Card.validate time log row

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_time_log_row`

**Inputs** self, d.

**Explicit failure paths** validation helper — translated “Row {0}: From time must be less than to time”.format(d.idx).

**Local steps**

- If (d.to\_time and get\_datetime(d.from\_time) &gt; get\_datetime(d.to\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.to\_time → get\_datetime(d.from\_time) &gt; get\_datetime(d.to\_time).
  - Call the validation error handler Platform.throw(translated “Row {0}: From time must be less than to time”.format(d.idx)).
- Evaluate self.validate\_overlap\_in\_time\_log(d).
- If (d.from\_time and d.to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.from\_time → d.to\_time.
  - Set d.time\_in\_mins from (time\_diff\_in\_hours(d.to\_time, d.from\_time) × 60).
- If (d.completed\_qty and not self.sub\_operations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.completed\_qty → not self.sub\_operations.
  - Update self.total\_completed\_qty using + d.completed\_qty.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap in time log](operations-018.md#op-45a9c36126956f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L803) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L465)

<a id="op-45a9c36126956f"></a>
### Job Card.validate overlap in time log

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_overlap_in_time_log`

**Inputs** self, d.

**Explicit failure paths** validation helper with OverlapError — translated “Row {0}: From Time and To Time of {1} is overlapping with {2}”.format(d.idx, self.name, data.name).

**Local steps**

- Evaluate self.validate\_employee\_time\_overlap(d).
- Set open\_job\_cards from list().
- If d.get(“employee”).
  - Set open\_job\_cards from self.get\_open\_job\_cards(d.get(“employee”), workstation = self.workstation).
- Set data from self.get\_overlap\_for(d, open\_job\_cards = open\_job\_cards).
- If data.
  - Call the validation error handler Platform.throw(translated “Row {0}: From Time and To Time of {1} is overlapping with {2}”.format(d.idx, self.name, data.name), OverlapError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate employee time overlap](operations-018.md#op-22144c95d67614), [get open job cards](operations-019.md#op-9a1a52d2462a8e), [get overlap for](operations-019.md#op-ecc98152945d87).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L459)

<a id="op-22144c95d67614"></a>
### Job Card.validate employee time overlap

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_employee_time_overlap`

**Inputs** self, d.

**Explicit results** no value.

**Explicit failure paths** validation helper with OverlapError — message.

**Local steps**

- If not (d.get(“employee”) and d.from\_time and d.to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“employee”) → d.from\_time → d.to\_time.
  - Return no value.
- Set clash from (self.get\_employee\_clash\_in\_card(d) or self.get\_employee\_clash\_in\_other\_cards(d)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_employee\_clash\_in\_card(d) → self.get\_employee\_clash\_in\_other\_cards(d).
- If not clash.
  - Return no value.
- If (clash.name equals self.name or Platform.has\_permission(“Job Card”, “read”, doc = clash.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in clash.name equals self.name → Platform.has\_permission(“Job Card”, “read”, doc = clash.name).
  - Set message from translated “Row {0}: Employee {1} is already working from {2} to {3} on Job Card {4}”.format(d.idx, d.employee, clash.from\_time, clash.to\_time, …).
- Otherwise.
  - Set message from translated “Row {0}: Employee {1} is already working at this time on another Job Card”.format(d.idx, d.employee).
- Call the validation error handler Platform.throw(message, OverlapError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get employee clash in card](operations-018.md#op-5c68f018cd65cc), [get employee clash in other cards](operations-018.md#op-9d603bfd932e2d).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “read”, doc = clash.name).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L839)

<a id="op-5c68f018cd65cc"></a>
### Job Card.get employee clash in card

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_employee_clash_in_card`

**Inputs** self, d.

**Explicit results** Platform.\_dict(name = self.name, from\_time = row.from\_time, to\_time = row.to\_time).

**Local steps**

- For each row in self.time\_logs.
  - If (row is identical to d or row.employee differs from d.employee or not (row.from\_time and row.to\_time)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row is identical to d → row.employee differs from d.employee → not (row.from\_time and row.to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.from\_time → row.to\_time.
    - Continue with the next iteration or loop test.
  - If (get\_datetime(row.from\_time) &lt; get\_datetime(d.to\_time) and get\_datetime(row.to\_time) &gt; get\_datetime(d.from\_time)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_datetime(row.from\_time) &lt; get\_datetime(d.to\_time) → get\_datetime(row.to\_time) &gt; get\_datetime(d.from\_time).
    - Return Platform.\_dict(name = self.name, from\_time = row.from\_time, to\_time = row.to\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L814)

<a id="op-9d603bfd932e2d"></a>
### Job Card.get employee clash in other cards

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_employee_clash_in_other_cards`

**Inputs** self, d.

**Explicit results** clashes at 0 when clashes, otherwise no value.

**Local steps**

- Set jc from Platform.qb.DocType(“Job Card”).
- Set jctl from Platform.qb.DocType(“Job Card Time Log”).
- Set clashes from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- Return clashes at 0 when clashes, otherwise no value.
  - Value choice on clashes — true gives clashes at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L815)

<a id="op-38abe446cd99fc"></a>
### Job Card.save time log totals

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_save_time_log_totals`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(mapping(“total\_time\_in\_mins” → self.total\_time\_in\_mins, “total\_completed\_qty” → self.total\_completed\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L6141) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L421)

<a id="op-446c02fcbf7c52"></a>
### Job Card.set total completed qty from sub operations

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_total_completed_quantity_from_subordinate_operations`

**Inputs** self.

**Local steps**

- Set sub\_op\_total\_qty from list().
- For each row in self.sub\_operations.
  - Evaluate sub\_op\_total\_qty.append(flt(row.completed\_qty)).
- If sub\_op\_total\_qty.
  - Set self.total\_completed\_qty from min(sub\_op\_total\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L6236) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L436)
