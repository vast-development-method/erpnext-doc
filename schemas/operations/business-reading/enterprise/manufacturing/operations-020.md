# Production · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-70426cdf04bb4b"></a>
### Job Card.reset required items

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_reset_required_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.items or not self.has\_value\_changed(“for\_quantity”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.items → not self.has\_value\_changed(“for\_quantity”).
  - Return no value.
- If any(generator of (flt(row.transferred\_qty) or flt(row.consumed\_qty)) for row drawn from self.items).
  - Draw row from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.transferred\_qty) → flt(row.consumed\_qty).
  - Return no value.
- Set self.items from list().
- Evaluate self.set\_required\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set required items](operations-020.md#op-86d7ad4c65cc83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L831)

<a id="op-31a20acbf88fdb"></a>
### Job Card.get required items

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_required_items`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set\_required\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set required items](operations-020.md#op-86d7ad4c65cc83).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L408)

<a id="op-86d7ad4c65cc83"></a>
### Job Card.set required items

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_set_required_items`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Item” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0} : Operation is required against the raw material item {1}”.format(d.idx, d.item\_code).

**Local steps**

- If not self.get(“work\_order”).
  - Return no value.
- Set doc from Platform.get\_doc(“Work Order”, self.get(“work\_order”)).
- If (not doc.track\_semi\_finished\_goods and (doc.transfer\_material\_against equals “Work Order” or doc.skip\_transfer)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.track\_semi\_finished\_goods → (doc.transfer\_material\_against equals “Work Order” or doc.skip\_transfer).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.transfer\_material\_against equals “Work Order” → doc.skip\_transfer.
  - Return no value.
- Set operation from next(generator of row for row drawn from doc.operations where row.name equals self.operation\_id, mapping()).
  - Draw row from doc.operations, keep a combination only if (row.name equals self.operation\_id).
- Set operation\_qty from get\_operation\_qty(doc, operation).
- Set other\_job\_cards\_qty from self.get\_other\_job\_cards\_qty().
- For each d in doc.required\_items.
  - If (not doc.track\_semi\_finished\_goods and not d.operation and not d.operation\_row\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.track\_semi\_finished\_goods → not d.operation → not d.operation\_row\_id.
    - Call the validation error handler Platform.throw(translated “Row {0} : Operation is required against the raw material item {1}”.format(d.idx, d.item\_code)).
  - If (self.is\_corrective\_job\_card or self.is\_own\_material(d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → self.is\_own\_material(d).
    - Evaluate self.append(“items”, mapping(“item\_code” → d.item\_code, “source\_warehouse” → (self.source\_warehouse or d.source\_warehouse), “uom” → Platform.db.get\_value(“Item”, d.item\_code, “stock\_uom”), “item\_name” → d. ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.source\_warehouse → d.source\_warehouse.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get other job cards qty](operations-020.md#op-257ca8f9c9c983), [is own material](operations-021.md#op-425f58526c0739), [get required qty](operations-020.md#op-d69a6c2d06c46d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L834)

<a id="op-257ca8f9c9c983"></a>
### Job Card.get other job cards qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_other_job_cards_qty`

**Inputs** self.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(for\_quantity = flt(for\_quantity.run() at 0 at 0), required\_qty = dict(required\_qty.run())).

**Local steps**

- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set job\_card\_item from Platform.qb.DocType(“Job Card Item”).
- Set other\_job\_cards from ((((job\_card.work\_order equals self.work\_order bitwise and job\_card.operation\_id equals self.operation\_id) bitwise and job\_card.name differs from (self.name or empty text)) bitwise and job\_card.docstatus &lt; ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- Set for\_quantity from nested operand in the contract.qb.from\_(job\_card).select(Sum(job\_card.for\_quantity)).where(other\_job\_cards).
- Set required\_qty from nested operand in the contract(nested operand in the contract).select(job\_card\_item.item\_code, Sum(nested operand in the contract.required\_qty)).where(other\_job\_cards).groupby(job\_card\_item.item\_code).
- Return Platform.\_dict(for\_quantity = flt(for\_quantity.run() at 0 at 0), required\_qty = dict(required\_qty.run())).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L819)

<a id="op-d69a6c2d06c46d"></a>
### Job Card.get required qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_required_qty`

**Inputs** self, d, operation\_qty, other\_job\_cards\_qty.

**Declared result** float.

**Explicit results** flt((total\_qty − flt(other\_job\_cards\_qty.required\_qty.get(d.item\_code))), precision).

**Local steps**

- Set precision from self.precision(“required\_qty”, “items”).
- Set total\_for\_quantity from (other\_job\_cards\_qty.for\_quantity + flt(self.for\_quantity)).
- Set total\_qty from flt(((flt(d.required\_qty) × total\_for\_quantity) ÷ flt(operation\_qty)), precision).
- Return flt((total\_qty − flt(other\_job\_cards\_qty.required\_qty.get(d.item\_code))), precision).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L822)

<a id="op-9c38fd70f4ef75"></a>
### Job Card.before save

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_expected\_and\_actual\_time().
- Evaluate self.set\_process\_loss().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set expected and actual time](operations-020.md#op-bf528cfe7f6781), [set process loss](operations-020.md#op-1057254d7aef60).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0472.json#L1306) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L390)

<a id="op-389d2147fca1a8"></a>
### Job Card.on submit

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_inspection().
- Evaluate self.validate\_transfer\_qty().
- Evaluate self.validate\_job\_card().
- Evaluate self.validate\_later\_operations().
- Evaluate self.update\_work\_order().
- Evaluate self.set\_transferred\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate inspection](operations-020.md#op-60f7cf30ea203f), [validate transfer qty](operations-020.md#op-20d4d21de865b9), [validate job card](operations-020.md#op-df474501a67981), [validate later operations](operations-021.md#op-64e3527ad04ec9), [update work order](operations-020.md#op-8db504b795b5e5), [set transferred qty](operations-021.md#op-4ac6489401d031).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L416)

<a id="op-a05a645ae5519b"></a>
### Job Card.on cancel

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“Quality Inspection”).
- Evaluate self.validate\_later\_operations().
- Evaluate self.update\_work\_order().
- Evaluate self.set\_transferred\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate later operations](operations-021.md#op-64e3527ad04ec9), [update work order](operations-020.md#op-8db504b795b5e5), [set transferred qty](operations-021.md#op-4ac6489401d031).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L414)

<a id="op-60f7cf30ea203f"></a>
### Job Card.validate inspection

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_inspection`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “BOM” via get\_value · read “Work Order Operation” via get\_value · read “Quality Inspection” via get\_value.

**State and service calls** msgprint with translated “Quality Inspection {0} is not submitted for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)) · msgprint with translated “Quality Inspection {0} is rejected for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)).

**Explicit failure paths** validation helper — translated “Quality Inspection is required for the item {0} before completing the job card {1}”.format(get\_link\_to\_form(“Item”, self.finished\_good), bold(self.name)) · validation helper with QualityInspectionNotSubmittedError — translated “Quality Inspection {0} is not submitted for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)) · validation helper with QualityInspectionRejectedError — translated “Quality Inspection {0} is rejected for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)).

**Local steps**

- Set tuple(action\_submit, action\_reject) from Platform.get\_single\_value(“Stock Settings”, list(“action\_if\_quality\_inspection\_is\_not\_submitted”, “action\_if\_quality\_inspection\_is\_rejected”)).
- Set bom\_inspection\_required from Platform.get\_value(“BOM”, self.bom\_no, “inspection\_required”).
- Set operation\_inspection\_required from Platform.get\_value(“Work Order Operation”, self.operation\_id, “quality\_inspection\_required”).
- If (bom\_inspection\_required and operation\_inspection\_required).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bom\_inspection\_required → operation\_inspection\_required.
  - If not self.quality\_inspection.
    - Call the validation error handler Platform.throw(translated “Quality Inspection is required for the item {0} before completing the job card {1}”.format(get\_link\_to\_form(“Item”, self.finished\_good), bold(self.name))).
  - Bind dependencies validate\_qi\_reference.
  - Evaluate validate\_qi\_reference(self, self, item\_code = self.production\_item).
  - Set tuple(qa\_status, docstatus) from Platform.get\_value(“Quality Inspection”, self.quality\_inspection, list(“status”, “docstatus”)).
  - If docstatus differs from 1.
    - If action\_submit equals “Stop”.
      - Call the validation error handler Platform.throw(translated “Quality Inspection {0} is not submitted for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)),  ….
    - Otherwise.
      - Evaluate Platform.msgprint(translated “Quality Inspection {0} is not submitted for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good) ….
  - Otherwise.
    - If qa\_status equals “Rejected”.
      - If action\_reject equals “Stop”.
        - Call the validation error handler Platform.throw(translated “Quality Inspection {0} is rejected for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)), title ….
      - Otherwise.
        - Evaluate Platform.msgprint(translated “Quality Inspection {0} is rejected for the item: {1}”.format(get\_link\_to\_form(“Quality Inspection”, self.quality\_inspection), get\_link\_to\_form(“Item”, self.finished\_good)), al ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, list(“action\_if\_quality\_inspection\_is\_not\_submitted”, “action\_if\_quality\_inspection\_is\_rejected”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L453)

<a id="op-20d4d21de865b9"></a>
### Job Card.validate transfer qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_transfer_quantity`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.track\_semi\_finished\_goods and self.skip\_material\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.track\_semi\_finished\_goods → self.skip\_material\_transfer.
  - Return no value.
- If (not self.finished\_good and not self.is\_corrective\_job\_card and self.items and (self.transferred\_qty &lt; self.for\_quantity or self.has\_short\_transferred\_material())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.finished\_good → not self.is\_corrective\_job\_card → self.items → (self.transferred\_qty &lt; self.for\_quantity or self.has\_short\_transferred\_material()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.transferred\_qty &lt; self.for\_quantity → self.has\_short\_transferred\_material().
  - Evaluate self.throw\_materials\_not\_moved().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has short transferred material](operations-021.md#op-267303b8855d2b), [throw materials not moved](operations-018.md#op-5e5f0d8ceb06d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L468)

<a id="op-df474501a67981"></a>
### Job Card.validate job card

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_job_card`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Transaction not allowed against stopped Work Order {0}”.format(get\_link\_to\_form(“Work Order”, self.work\_order)).

**Local steps**

- If (self.work\_order and Platform.get\_cached\_value(“Work Order”, self.work\_order, “status”) equals “Stopped”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → Platform.get\_cached\_value(“Work Order”, self.work\_order, “status”) equals “Stopped”.
  - Call the validation error handler Platform.throw(translated “Transaction not allowed against stopped Work Order {0}”.format(get\_link\_to\_form(“Work Order”, self.work\_order))).
- Evaluate self.validate\_not\_on\_hold().
- Evaluate self.validate\_time\_logs\_present().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not on hold](operations-020.md#op-18f579659f28cd), [validate time logs present](operations-020.md#op-4fa8ba69b343cf).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “status”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L454)

<a id="op-18f579659f28cd"></a>
### Job Card.validate not on hold

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_not_on_hold`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot submit Job Card {0} while it is On Hold. Please resume and complete the job before submission.”.format(get\_link\_to\_form(“Job Card”, self.name)).

**Local steps**

- If self.is\_paused.
  - Call the validation error handler Platform.throw(translated “Cannot submit Job Card {0} while it is On Hold. Please resume and complete the job before submission.”.format(get\_link\_to\_form(“Job Card”, self.name)), title = translated “Job Ca ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0472.json#L3083) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L792) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L456)

<a id="op-4fa8ba69b343cf"></a>
### Job Card.validate time logs present

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_time_logs_present`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Time logs are required for {0} {1}”.format(bold(“Job Card”), get\_link\_to\_form(“Job Card”, self.name)) · validation helper — translated “Row #{0}: From Time and To Time fields are required”.format(row.idx) · validation helper — translated “Total Completed Qty ({0}), Process Loss Qty ({1}) and Pending Qty ({2}) must add up to the Qty to Manufactur …”.format(bold(self.get\_qty\_with\_uom(self.total\_completed\_qty)), bold(self.get\_qty\_w ….

**Local steps**

- If (self.track\_semi\_finished\_goods and self.is\_subcontracted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.track\_semi\_finished\_goods → self.is\_subcontracted.
  - Return no value.
- If not self.time\_logs.
  - Call the validation error handler Platform.throw(translated “Time logs are required for {0} {1}”.format(bold(“Job Card”), get\_link\_to\_form(“Job Card”, self.name))).
- Otherwise.
  - If Platform.db.get\_single\_value(“Manufacturing Settings”, “enforce\_time\_logs”).
    - For each row in self.time\_logs.
      - If (not row.from\_time or not row.to\_time).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.from\_time → not row.to\_time.
        - Call the validation error handler Platform.throw(translated “Row #{0}: From Time and To Time fields are required”.format(row.idx)).
- Set precision from self.precision(“total\_completed\_qty”).
- Set accounted\_qty from flt(((flt(self.total\_completed\_qty, precision) + flt(self.process\_loss\_qty, precision)) + flt(self.pending\_qty, precision))).
- If (self.for\_quantity and flt(accounted\_qty, precision) differs from flt(self.for\_quantity, precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.for\_quantity → flt(accounted\_qty, precision) differs from flt(self.for\_quantity, precision).
  - Call the validation error handler Platform.throw(translated “Total Completed Qty ({0}), Process Loss Qty ({1}) and Pending Qty ({2}) must add up to the Qty to Manufactur …”.format(bold(self.get\_qty\_with\_uom(self.total\_completed\_qty)), bold ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “enforce\_time\_logs”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L467)

<a id="op-bf528cfe7f6781"></a>
### Job Card.set expected and actual time

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_expected_and_actual_time`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.time\_logs.
  - Set self.actual\_start\_date, self.actual\_end\_date from no value.
- For each tuple(child\_table, start\_field, end\_field, time\_required) in list(tuple(“scheduled\_time\_logs”, “expected\_start\_date”, “expected\_end\_date”, “time\_required”), tuple(“time\_logs”, “actual\_start\_date”, “actual\_end\_date”, “total\_time\_in\_mins”)).
  - If not self.get(child\_table).
    - Continue with the next iteration or loop test.
  - If self.set\_time\_for\_child\_table(child\_table, start\_field, end\_field, time\_required).
    - Return no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set time for child table](operations-020.md#op-f8787885f9f0ae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L426)

<a id="op-f8787885f9f0ae"></a>
### Job Card.set time for child table

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_time_for_child_table`

**Inputs** self, child\_table, start\_field, end\_field, time\_required.

**Explicit results** true · false.

**Local steps**

- Set time\_list from list().
- Set time\_in\_mins from 0.0.
- For each row in self.get(child\_table).
  - Update time\_in\_mins using + flt(row.get(“time\_in\_mins”)).
  - For each field in list(“from\_time”, “to\_time”).
    - If row.get(field).
      - Evaluate time\_list.append(get\_datetime(row.get(field))).
- If time\_list.
  - Evaluate self.set(start\_field, min(time\_list)).
  - If (end\_field equals “actual\_end\_date” and not self.time\_logs at negative 1.to\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_field equals “actual\_end\_date” → not self.time\_logs at negative 1.to\_time.
    - Evaluate self.set(end\_field, empty text).
    - Return true.
  - Evaluate self.set(end\_field, max(time\_list)).
- If child\_table equals “time\_logs”.
  - Set time\_in\_mins from flt(get\_workstation\_minutes(self.time\_logs), self.precision(“total\_time\_in\_mins”)).
- Evaluate self.set(time\_required, time\_in\_mins).
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L435)

<a id="op-1057254d7aef60"></a>
### Job Card.set process loss

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_process_loss`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If any(generator of row.status differs from “Complete” for row drawn from self.sub\_operations).
  - Draw row from self.sub\_operations.
  - Return no value.
- Set precision from self.precision(“total\_completed\_qty”).
- Set should\_set\_process\_loss from (self.total\_completed\_qty or self.process\_loss\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.total\_completed\_qty → self.process\_loss\_qty.
- Set self.process\_loss\_qty from 0.0.
- If (should\_set\_process\_loss and self.for\_quantity &gt; self.total\_completed\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in should\_set\_process\_loss → self.for\_quantity &gt; self.total\_completed\_qty.
  - Set self.process\_loss\_qty from max(((flt(self.for\_quantity, precision) − flt(self.total\_completed\_qty, precision)) − flt(self.pending\_qty, precision)), 0.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L430)

<a id="op-8db504b795b5e5"></a>
### Job Card.update work order

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_work_order`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.work\_order.
  - Return no value.
- If (self.is\_corrective\_job\_card and not cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_corrective\_job\_card → not cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”)).
  - Return no value.
- Set tuple(for\_quantity, time\_in\_mins, process\_loss\_qty, pending\_qty) from tuple(0, 0, 0, 0).
- Set data from self.get\_current\_operation\_data().
- If (data and len(data) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → len(data) &gt; 0.
  - Set for\_quantity from flt(data at 0.completed\_qty).
  - Set time\_in\_mins from flt(data at 0.time\_in\_mins).
  - Set process\_loss\_qty from flt(data at 0.process\_loss\_qty).
  - Set pending\_qty from flt(data at 0.pending\_qty).
- Set wo from Platform.get\_doc(“Work Order”, self.work\_order).
- If self.is\_corrective\_job\_card.
  - Evaluate self.update\_corrective\_in\_work\_order(wo).
- Otherwise.
  - If self.operation\_id.
    - Evaluate self.validate\_produced\_quantity(for\_quantity, process\_loss\_qty, wo).
    - Evaluate self.update\_work\_order\_data(for\_quantity, process\_loss\_qty, pending\_qty, time\_in\_mins, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current operation data](operations-020.md#op-44eba10692aac0), [update corrective in work order](operations-020.md#op-79fa0cc93dba1e), [validate produced quantity](operations-020.md#op-5dbe15b782e72b), [update work order data](operations-020.md#op-fd104dd42b918a).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L447)

<a id="op-26cdb8c91e0ce6"></a>
### Job Card.update semi finished good details

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_semi_finished_good_details`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Job Card” via get\_all.

**State and service calls** request set\_value on “Work Order Operation” · call db\_set on work\_order.

**Explicit results** no value.

**Local steps**

- If not self.operation\_id.
  - Return no value.
- Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order).
- If work\_order.production\_plan.
  - Evaluate ProductionPlanWorkOrderQuantities(work\_order.production\_plan).lock\_plan\_row(work\_order).
- Set job\_cards from Platform.get\_all(“Job Card”, filters = mapping(“work\_order” → self.work\_order, “operation\_id” → self.operation\_id, “docstatus” → 1, “is\_corrective\_job\_card” → 0), fields = list(“manufactured\_qty”, “total\_c ….
- Set completed\_qty from sum(generator of max(flt(row.manufactured\_qty), flt(row.total\_completed\_qty)) for row drawn from job\_cards).
  - Draw row from job\_cards.
- Evaluate Platform.db.set\_value(“Work Order Operation”, self.operation\_id, “completed\_qty”, completed\_qty).
- If (self.finished\_good and work\_order.production\_item equals self.finished\_good).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.finished\_good → work\_order.production\_item equals self.finished\_good.
  - Evaluate work\_order.db\_set(“produced\_qty”, sum(generator of flt(row.manufactured\_qty) for row drawn from job\_cards)).
    - Draw row from job\_cards.
  - If work\_order.production\_plan.
    - Evaluate ProductionPlanWorkOrderQuantities(work\_order.production\_plan).validate\_work\_order(work\_order, process\_loss\_qty = work\_order.process\_loss\_qty).
  - Evaluate work\_order.update\_work\_order\_qty\_in\_sales\_orders().
  - Evaluate work\_order.db\_set(“status”, work\_order.get\_status()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L443)

<a id="op-79fa0cc93dba1e"></a>
### Job Card.update corrective in work order

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_corrective_in_work_order`

**Inputs** self, wo.

**Record and data access** read “Job Card” via get\_all.

**State and service calls** call save on wo.

**Local steps**

- Set wo.corrective\_operation\_cost from 0.0.
- For each row in Platform.get\_all(“Job Card”, fields = list(“total\_time\_in\_mins”, “hour\_rate”), filters = mapping(“is\_corrective\_job\_card” → 1, “docstatus” → 1, “work\_order” → self.work\_order)).
  - Update wo.corrective\_operation\_cost using + (flt((row.total\_time\_in\_mins ÷ 60)) × flt(row.hour\_rate)).
- Evaluate wo.calculate\_operating\_cost().
- Set wo.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate wo.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0472.json#L6326) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L442)

<a id="op-5dbe15b782e72b"></a>
### Job Card.validate produced quantity

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_produced_quantity`

**Inputs** self, for\_quantity, process\_loss\_qty, wo.

**Explicit results** no value.

**Explicit failure paths** validation helper with JobCardCancelError — ((first\_part\_msg + one space) + second\_part\_msg).

**Local steps**

- <a id="op-5dbe15b782e72b-guard-2"></a>If self.docstatus &lt; 2.
  - Return no value.
- Set operation from next(generator of row for row drawn from wo.operations where row.name equals self.operation\_id, mapping()).
  - Draw row from wo.operations, keep a combination only if (row.name equals self.operation\_id).
- Set operation\_total from ((for\_quantity + process\_loss\_qty) × flt(wo.qty)).
- Set operation\_total from flt((operation\_total ÷ get\_operation\_qty(wo, operation)), wo.precision(“produced\_qty”)).
- If wo.produced\_qty &gt; operation\_total.
  - Set first\_part\_msg from translated “The {0} {1} is used to calculate the valuation cost for the finished good {2}.”.format(Platform.bold(translated “Job Card”), Platform.bold(self.name), Platform.bold(self.production\_item)).
  - Set second\_part\_msg from translated “Kindly cancel the Manufacturing Entries first against the work order {0}.”.format(Platform.bold(get\_link\_to\_form(“Work Order”, self.work\_order))).
  - Call the validation error handler Platform.throw(((first\_part\_msg + one space) + second\_part\_msg), JobCardCancelError, title = translated “Error”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus &lt; 2, self.docstatus = 0 (draft) selects the branch that returns no value. With self.docstatus = 2 (cancelled), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5dbe15b782e72b-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L461)

<a id="op-fd104dd42b918a"></a>
### Job Card.update work order data

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_update_work_order_data`

**Inputs** self, for\_quantity, process\_loss\_qty, pending\_qty, time\_in\_mins, wo.

**State and service calls** call save on wo.

**Local steps**

- Set jc from Platform.qb.DocType(“Job Card”).
- Set jctl from Platform.qb.DocType(“Job Card Time Log”).
- Set time\_data from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“start\_time”), nested operand in the contract.as\_(“end\_time”)).where(((((nested operand in the contr ….
- For each data in wo.operations.
  - If data.get(“name”) equals self.operation\_id.
    - Set data.completed\_qty from for\_quantity.
    - Set data.process\_loss\_qty from process\_loss\_qty.
    - Set data.pending\_qty from pending\_qty.
    - Set data.actual\_operation\_time from time\_in\_mins.
    - Set data.actual\_start\_time from time\_data at 0.start\_time when time\_data, otherwise no value.
      - Value choice on time\_data — true gives time\_data at 0.start\_time, false gives no value.
    - Set data.actual\_end\_time from time\_data at 0.end\_time when time\_data, otherwise no value.
      - Value choice on time\_data — true gives time\_data at 0.end\_time, false gives no value.
- Set wo.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate wo.update\_operation\_status(self.operation\_id).
- Evaluate wo.calculate\_operating\_cost().
- Evaluate wo.set\_actual\_dates().
- If wo.track\_semi\_finished\_goods.
  - Evaluate wo.set\_process\_loss\_qty().
  - Evaluate wo.update\_work\_order\_qty\_in\_sales\_orders().
- Set wo.status from wo.get\_status().
- Evaluate wo.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L448)

<a id="op-44eba10692aac0"></a>
### Job Card.get current operation data

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_current_operation_data`

**Inputs** self.

**Record and data access** read “Job Card” via get\_all.

**Explicit results** Platform.get\_all(“Job Card”, fields = list(mapping(“SUM” → “total\_time\_in\_mins”, “as” → “time\_in\_mins”), mapping(“SUM” → “total\_completed\_qty”, “as” → “completed\_qty”), mapping(“SUM” → “process\_loss\_qty”,  ….

**Local steps**

- Return Platform.get\_all(“Job Card”, fields = list(mapping(“SUM” → “total\_time\_in\_mins”, “as” → “time\_in\_mins”), mapping(“SUM” → “total\_completed\_qty”, “as” → “completed\_qty”), mapping(“SUM” → “process\_loss\_qty”,  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0473.json#L1140) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L398)

<a id="op-bca9c2d1f08ab2"></a>
### Job Card.set consumed qty in job card item

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_consumed_quantity_in_job_card_item`

**Inputs** self, ste\_doc.

**State and service calls** request set\_value on “Job Card Item”.

**Explicit results** no value.

**Local steps**

- Set jc\_item\_names from list of row.job\_card\_item for row drawn from ste\_doc.get(“items”) where row.get(“job\_card\_item”).
  - Draw row from ste\_doc.get(“items”), keep a combination only if (row.get(“job\_card\_item”)).
- If not jc\_item\_names.
  - Return no value.
- Set se from Platform.qb.DocType(“Stock Entry”).
- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).select(sed.job\_card\_item, Sum(nested operand in the contract.transfer\_qty)).where(((nested operand in the contract.isin(jc\_item\_names) bitwise ….
- Set itemwise\_consumed\_qty from Platform.\_dict(query.run(as\_list = true)).
- For each row in ste\_doc.items.
  - If not row.get(“job\_card\_item”).
    - Continue with the next iteration or loop test.
  - Set consumed\_qty from flt(itemwise\_consumed\_qty.get(row.job\_card\_item, 0.0)).
  - Evaluate Platform.db.set\_value(“Job Card Item”, row.job\_card\_item, “consumed\_qty”, consumed\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L424)

<a id="op-7cf4bcf4d7a7f8"></a>
### Job Card.set transferred qty in job card item

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_transferred_quantity_in_job_card_item`

**Inputs** self, ste\_doc.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**State and service calls** request set\_value on “Job Card Item”.

**Local steps**

- Bind local operation \_get\_job\_card\_items\_transferred\_qty for subsequent calls.
- Bind local operation \_validate\_over\_transfer for subsequent calls.
- Set job\_card\_items\_transferred\_qty from (\_get\_job\_card\_items\_transferred\_qty(ste\_doc) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_job\_card\_items\_transferred\_qty(ste\_doc) → mapping().
- Set allow\_excess from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
- For each row in ste\_doc.items.
  - If not row.job\_card\_item.
    - Continue with the next iteration or loop test.
  - Set transferred\_qty from flt(job\_card\_items\_transferred\_qty.get(row.job\_card\_item, 0.0)).
  - If not allow\_excess.
    - Evaluate \_validate\_over\_transfer(row, transferred\_qty).
  - Evaluate Platform.db.set\_value(“Job Card Item”, row.job\_card\_item, “transferred\_qty”, flt(transferred\_qty)).
- Evaluate self.set\_status(update\_status = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-021.md#op-575a8477f4fcfd).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L438)
