# Production · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-099ed6252837d5"></a>
### Job Card.set transferred qty in job card item.get job card items transferred qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_set_transferred_qty_in_job_card_item_get_job_card_items_transferred_qty`

**Inputs** ste\_doc.

**Explicit results** job\_card\_items\_transferred\_qty.

**Local steps**

- Bind dependencies Sum.
- Set job\_card\_items\_transferred\_qty from mapping().
- Set job\_card\_items from list of x.get(“job\_card\_item”) for x drawn from ste\_doc.get(“items”) where x.get(“job\_card\_item”).
  - Draw x from ste\_doc.get(“items”), keep a combination only if (x.get(“job\_card\_item”)).
- If job\_card\_items.
  - Set se from Platform.qb.DocType(“Stock Entry”).
  - Set sed from Platform.qb.DocType(“Stock Entry Detail”).
  - Set query from nested operand in the contract(nested operand in the contract).select(sed.job\_card\_item, Sum(nested operand in the contract.transfer\_qty)).where(((nested operand in the contract.isin(job\_card\_items) bitwis ….
  - Set job\_card\_items\_transferred\_qty from Platform.\_dict(query.run(as\_list = true)).
- Return job\_card\_items\_transferred\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L835)

<a id="op-e0ccbcdd643ff2"></a>
### Job Card.set transferred qty in job card item.validate over transfer

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_set_transferred_qty_in_job_card_item_validate_over_transfer`

**Inputs** row, transferred\_qty.

**Record and data access** read “Job Card Item” via get\_value.

**Explicit failure paths** validation helper with JobCardOverTransferError — translated “Row #{0}: Cannot transfer more than Required Qty {1} for Item {2} against Job Card {3}”.format(row.idx, Platform.bold(self.get\_qty\_with\_uom(required\_qty, row.item\_code)), Platform.bold(row.item ….

**Local steps**

- Set required\_qty from Platform.db.get\_value(“Job Card Item”, row.job\_card\_item, “required\_qty”).
- Set is\_excess from flt(transferred\_qty) &gt; flt(required\_qty).
- If is\_excess.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot transfer more than Required Qty {1} for Item {2} against Job Card {3}”.format(row.idx, Platform.bold(self.get\_qty\_with\_uom(required\_qty, row.item\_code)), Platfor ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L836)

<a id="op-4ac6489401d031"></a>
### Job Card.set transferred qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_transferred_quantity`

**Inputs** self, update\_status = false.

**Record and data access** read “Work Order” via get\_cached\_value.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies Sum.
- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.fg\_completed\_qty)).where(((nested operand in the contract.job\_card equals nested operand in the cont ….
- Set query from query.run().
- Set qty from 0.
- If (query and query at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query → query at 0 at 0.
  - Set qty from flt(query at 0 at 0).
- Evaluate self.db\_set(“transferred\_qty”, qty).
- Evaluate self.set\_status(update\_status).
- If (self.work\_order and not Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_goods”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → not Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_goods”).
  - Evaluate self.set\_transferred\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-021.md#op-575a8477f4fcfd), [set transferred qty in work order](operations-021.md#op-57915ed2a5ab83).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “track\_semi\_finished\_goods”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L437)

<a id="op-267303b8855d2b"></a>
### Job Card.has short transferred material

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_has_short_transferred_material`

**Inputs** self.

**Record and data access** read “Work Order Item” via get\_all · read “Job Card Item” via get\_all.

**Explicit results** false · true.

**Local steps**

- If not (self.work\_order and flt(self.for\_quantity)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → flt(self.for\_quantity).
  - Return false.
- Set wo\_qty from self.get\_work\_order\_qty\_details().operation\_qty.
- If not wo\_qty.
  - Return false.
- Set wo\_items from Platform.get\_all(“Work Order Item”, filters = mapping(“parent” → self.work\_order, “parenttype” → “Work Order”), fields = list(“item\_code”, “required\_qty”, “operation”, “operation\_row\_id”)).
- Set transferred from dict(Platform.get\_all(“Job Card Item”, filters = mapping(“parent” → self.name, “parenttype” → “Job Card”), fields = list(“item\_code”, “transferred\_qty”), as\_list = true)).
- Set other\_job\_cards\_qty from self.get\_other\_job\_cards\_qty().
- Set precision from self.precision(“transferred\_qty”, “items”).
- For each row in wo\_items.
  - If not self.is\_own\_material(row).
    - Continue with the next iteration or loop test.
  - Set expected from self.get\_required\_qty(row, wo\_qty, other\_job\_cards\_qty).
  - If flt(transferred.get(row.item\_code), precision) &lt; flt(expected, precision).
    - Return true.
- Return false.

**Methods declared on this owner** [get work order qty details](operations-018.md#op-6c7465b8beb049), [get other job cards qty](operations-020.md#op-257ca8f9c9c983), [is own material](operations-021.md#op-425f58526c0739), [get required qty](operations-020.md#op-d69a6c2d06c46d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L827)

<a id="op-425f58526c0739"></a>
### Job Card.is own material

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_is_own_material`

**Inputs** self, row.

**Explicit results** cint(row.operation\_row\_id) equals cint(self.operation\_row\_id) · row.operation equals self.operation.

**Local steps**

- If (row.operation\_row\_id and self.operation\_row\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.operation\_row\_id → self.operation\_row\_id.
  - Return cint(row.operation\_row\_id) equals cint(self.operation\_row\_id).
- Return row.operation equals self.operation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L828)

<a id="op-2dc64f4656be0f"></a>
### Job Card.get requested qty by item

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_requested_qty_by_item`

**Inputs** self.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(mr\_item.job\_card\_item).run()).

**Local steps**

- Set mr from Platform.qb.DocType(“Material Request”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(mr\_item.job\_card\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L821)

<a id="op-4129d2b73521c6"></a>
### Job Card.validate incoming material demand

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_incoming_material_demand`

**Inputs** self, material\_request.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only {0} {1} of {2} is pending to request in Job Card {3}.”.format(max(pending, 0.0), item.stock\_uom, item.item\_code, self.name).

**Local steps**

- If Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
  - Return no value.
- Set incoming from mapping().
- For each row in material\_request.items.
  - Set incoming at row.job\_card\_item from (incoming.get(row.job\_card\_item, 0.0) + flt(row.stock\_qty)).
- Set requested from self.get\_requested\_qty\_by\_item().
- For each item in self.items.
  - If item.name does not belong to incoming.
    - Continue with the next iteration or loop test.
  - Set pending from (flt(item.required\_qty) − flt(requested.get(item.name))).
  - If flt((incoming at item.name − pending), item.precision(“required\_qty”)) &gt; 0.
    - Call the validation error handler Platform.throw(translated “Only {0} {1} of {2} is pending to request in Job Card {3}.”.format(max(pending, 0.0), item.stock\_uom, item.item\_code, self.name), title = translated “Exceeds Pending Qty”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get requested qty by item](operations-021.md#op-2dc64f4656be0f).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L840)

<a id="op-ba1bed71f9dd28"></a>
### Job Card.set requested qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_set_requested_qty`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set requested from self.get\_requested\_qty\_by\_item().
- Set items from list of d for d drawn from self.items where flt(d.required\_qty) &gt; 0.
  - Draw d from self.items, keep a combination only if (flt(d.required\_qty) &gt; 0).
- Set requested\_fraction from min(generator of (flt(nested operand in the contract.get(nested operand in the contract.name)) ÷ flt(d.required\_qty)) for d drawn from items) when items, otherwise 0.0.
  - Value choice on items — true gives min(generator of (flt(requested.get(d.name)) ÷ flt(d.required\_qty)) for d drawn from items), false gives 0.0.
  - Draw d from items.
- Evaluate self.db\_set(“requested\_qty”, flt((requested\_fraction × flt(self.for\_quantity)), self.precision(“requested\_qty”))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get requested qty by item](operations-021.md#op-2dc64f4656be0f).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L833)

<a id="op-57915ed2a5ab83"></a>
### Job Card.set transferred qty in work order

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_transferred_quantity_in_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Work Order”, self.work\_order).
- Set qty from 0.0.
- If (doc.transfer\_material\_against equals “Job Card” and not doc.skip\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.transfer\_material\_against equals “Job Card” → not doc.skip\_transfer.
  - Set min\_qty from list().
  - Set precision from self.precision(“total\_completed\_qty”).
  - For each d in doc.operations.
    - Set completed\_qty from (((flt(d.completed\_qty) + flt(d.process\_loss\_qty)) + get\_upstream\_process\_loss(doc, d)) × flt(doc.qty)).
    - Set completed\_qty from flt((completed\_qty ÷ get\_operation\_qty(doc, d)), precision).
    - If completed\_qty.
      - Evaluate min\_qty.append(completed\_qty).
    - Otherwise.
      - Set min\_qty from list().
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If min\_qty.
    - Set qty from min(min\_qty).
  - Evaluate doc.db\_set(“material\_transferred\_for\_manufacturing”, qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L439)

<a id="op-575a8477f4fcfd"></a>
### Job Card.set status

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_status`

**Inputs** self, update\_status = false.

**Record and data access** read “Job Card Item” via get\_all.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.status from mapping(0 → “Open”, 1 → “Submitted”, 2 → “Cancelled”) at (self.docstatus or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus → 0.
- Set precision from self.precision(“total\_completed\_qty”).
- If (self.finished\_good and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.finished\_good → self.docstatus equals 1.
  - If flt((flt(self.manufactured\_qty) + flt(self.process\_loss\_qty)), precision) ≥ self.get\_qty\_to\_produce().
    - Set self.status from “Completed”.
  - Otherwise.
    - If (self.transferred\_qty &gt; 0 or self.skip\_material\_transfer).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.transferred\_qty &gt; 0 → self.skip\_material\_transfer.
      - Set self.status from “Work In Progress”.
- If (self.docstatus equals 0 and self.time\_logs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → self.time\_logs.
  - Set self.status from “Work In Progress”.
- If (not self.track\_semi\_finished\_goods and self.docstatus &lt; 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.track\_semi\_finished\_goods → self.docstatus &lt; 2.
  - If self.items.
    - Set item\_data from Platform.get\_all(“Job Card Item”, filters = mapping(“parent” → self.name), fields = list(“transferred\_qty”, “required\_qty”)).
    - Set all\_transferred from (item\_data and all(generator of flt(d.transferred\_qty) ≥ flt(d.required\_qty) for d drawn from item\_data)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_data → all(generator of flt(d.transferred\_qty) ≥ flt(d.required\_qty) for d drawn from item\_data).
      - Draw d from item\_data.
    - Set any\_transferred from any(generator of flt(d.transferred\_qty) &gt; 0 for d drawn from item\_data).
      - Draw d from item\_data.
    - If all\_transferred.
      - Set self.status from “Material Transferred”.
    - Otherwise.
      - If any\_transferred.
        - Set self.status from “Partially Transferred”.
  - Otherwise.
    - If flt(self.for\_quantity) ≤ flt(self.transferred\_qty).
      - Set self.status from “Material Transferred”.
  - If self.time\_logs.
    - Set self.status from “Work In Progress”.
  - Set completed\_qty from flt((flt(self.total\_completed\_qty) + flt(self.process\_loss\_qty)), precision).
  - If (self.docstatus equals 1 and (self.get\_qty\_to\_produce() ≤ completed\_qty or not self.items)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → (self.get\_qty\_to\_produce() ≤ completed\_qty or not self.items).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_qty\_to\_produce() ≤ completed\_qty → not self.items.
    - Set self.status from “Completed”.
- If self.is\_paused.
  - Set self.status from “On Hold”.
- If update\_status.
  - Evaluate self.db\_set(“status”, self.status).
- If self.workstation.
  - Evaluate self.update\_workstation\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty to produce](operations-021.md#op-887b1fab0b5a92), [update workstation status](operations-022.md#op-8ad35d0ced9364).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L432)

<a id="op-887b1fab0b5a92"></a>
### Job Card.get qty to produce

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_quantity_to_produce`

**Inputs** self.

**Explicit results** flt((flt(self.for\_quantity) − flt(self.pending\_qty)), self.precision(“total\_completed\_qty”)).

**Local steps**

- Return flt((flt(self.for\_quantity) − flt(self.pending\_qty)), self.precision(“total\_completed\_qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L406)

<a id="op-796d4d5f140d45"></a>
### Job Card.get qty with uom

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_quantity_with_unit_of_measure`

**Inputs** self, qty, item\_code = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** formatted text {flt(qty, self.precision(“total\_completed\_qty”))} {(uom or empty text)}.strip().

**Local steps**

- Set uom from self.stock\_uom.
- If item\_code.
  - Set uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
- Return formatted text {flt(qty, self.precision(“total\_completed\_qty”))} {(uom or empty text)}.strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uom → empty text.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0473.json#L4718) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L407)

<a id="op-1c834bc3b1e488"></a>
### Job Card.set wip warehouse

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_work_in_progress_warehouse`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If not self.wip\_warehouse.
  - Set self.wip\_warehouse from Platform.get\_cached\_value(“Company”, self.company, “default\_wip\_warehouse”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_wip\_warehouse”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0473.json#L5735) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L440)

<a id="op-de69b5d2862a89"></a>
### Job Card.set stock uom

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_stock_unit_of_measure`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set item\_code from (self.finished\_good or self.production\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.finished\_good → self.production\_item.
- If item\_code.
  - Set self.stock\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0473.json#L5843) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L433)

<a id="op-2e78cd97f30110"></a>
### Job Card.set operation id

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_set_operation_identifier`

**Inputs** self.

**Record and data access** read “Work Order Operation” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Operation {0} does not belong to the work order {1}”.format(bold(self.operation), get\_link\_to\_form(“Work Order”, self.work\_order)) · validation helper — translated “Operation {0} is added multiple times in the work order {1}. Please select the operation row.”.format(bold(self.operation), get\_link\_to\_form(“Work Order”, self.work\_order)).

**Local steps**

- If not (self.work\_order and self.operation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.operation.
  - Return no value.
- If (self.operation\_id and self.docstatus differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.operation\_id → self.docstatus differs from 0.
  - Return no value.
- Set operation\_rows from Platform.get\_all(“Work Order Operation”, filters = mapping(“parent” → self.work\_order, “operation” → self.operation), pluck = “name”).
- If self.operation\_id.
  - If (operation\_rows and self.operation\_id does not belong to operation\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in operation\_rows → self.operation\_id does not belong to operation\_rows.
    - Call the validation error handler Platform.throw(translated “Operation {0} does not belong to the work order {1}”.format(bold(self.operation), get\_link\_to\_form(“Work Order”, self.work\_order))).
- Otherwise.
  - If len(operation\_rows) equals 1.
    - Set self.operation\_id from operation\_rows at 0.
  - Otherwise.
    - If (operation\_rows and self.docstatus equals 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in operation\_rows → self.docstatus equals 0.
      - Call the validation error handler Platform.throw(translated “Operation {0} is added multiple times in the work order {1}. Please select the operation row.”.format(bold(self.operation), get\_link\_to\_form(“Work Order”, self.work\_order))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0473.json#L5966) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L429)

<a id="op-09118bd93c0d40"></a>
### Job Card.pause job

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_pause_job`

**Inputs** self, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Job Card {0} is already paused.”.format(bold(self.name)).

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).
- Evaluate self.validate\_docstatus().
- If self.is\_paused.
  - Call the validation error handler Platform.throw(translated “Job Card {0} is already paused.”.format(bold(self.name)), title = translated “Already Paused”).
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Evaluate self.db\_set(“is\_paused”, 1).
- Evaluate self.add\_time\_logs(to\_time = kwargs.end\_time, completed\_qty = 0.0, employees = self.employee).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docstatus](operations-022.md#op-65503f3ca6264d), [add time logs](operations-022.md#op-8245158e6b54c7).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L419)

<a id="op-5a3e180c1a8461"></a>
### Job Card.resume job

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_resume_job`

**Inputs** self, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Job Card {0} is not paused.”.format(bold(self.name)).

**Local steps**

- Evaluate Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).
- Evaluate self.validate\_docstatus().
- If not self.is\_paused.
  - Call the validation error handler Platform.throw(translated “Job Card {0} is not paused.”.format(bold(self.name)), title = translated “Not Paused”).
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Evaluate self.db\_set(“is\_paused”, 0).
- Evaluate self.add\_time\_logs(from\_time = kwargs.start\_time, employees = self.employee, completed\_qty = 0.0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docstatus](operations-022.md#op-65503f3ca6264d), [add time logs](operations-022.md#op-8245158e6b54c7).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Job Card”, “write”, doc = self, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L420)

<a id="op-3c9e51d3e8eb1e"></a>
### Job Card.validate sequence id

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_validate_sequence_identifier`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with OperationSequenceError — translated “{0}, complete the operation {1} before the operation {2}.”.format(message, bold(row.operation), bold(self.operation)) · validation helper — translated “The completed quantity {0} of an operation {1} cannot be greater than the completed quantity {2} of a previo …”.format(bold(self.get\_qty\_with\_uom(current\_operation\_qty)), bold(self.operation),  ….

**Local steps**

- If self.is\_new().
  - Return no value.
- If self.is\_corrective\_job\_card.
  - Return no value.
- If not (self.work\_order and self.sequence\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.sequence\_id.
  - Return no value.
- Set current\_operation\_qty from 0.0.
- Set data from self.get\_current\_operation\_data().
- If (data and len(data) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → len(data) &gt; 0.
  - Set current\_operation\_qty from flt(data at 0.completed\_qty).
- Update current\_operation\_qty using + flt(self.total\_completed\_qty).
- Set previous\_operations from self.get\_previous\_operations().
- Set message from “Job Card {}: As per the sequence of the operations in the work order {}”.format(bold(self.name), bold(get\_link\_to\_form(“Work Order”, self.work\_order))).
- For each row in previous\_operations.
  - If self.track\_semi\_finished\_goods.
    - Evaluate self.validate\_previous\_operation\_manufactured\_qty(row, current\_operation\_qty).
    - Continue with the next iteration or loop test.
  - If not row.completed\_qty.
    - Call the validation error handler Platform.throw(translated “{0}, complete the operation {1} before the operation {2}.”.format(message, bold(row.operation), bold(self.operation)), OperationSequenceError).
  - If (row.status differs from “Completed” and row.completed\_qty &lt; current\_operation\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.status differs from “Completed” → row.completed\_qty &lt; current\_operation\_qty.
    - Call the validation error handler Platform.throw(translated “{0}, complete the operation {1} before the operation {2}.”.format(message, bold(row.operation), bold(self.operation)), OperationSequenceError).
  - If row.completed\_qty &lt; current\_operation\_qty.
    - Call the validation error handler Platform.throw(translated “The completed quantity {0} of an operation {1} cannot be greater than the completed quantity {2} of a previo …”.format(bold(self.get\_qty\_with\_uom(current\_operation\_qty)), bold(se ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current operation data](operations-020.md#op-44eba10692aac0), [get previous operations](operations-021.md#op-b9f7fc6e84e37d), [validate previous operation manufactured qty](operations-022.md#op-45f625da05bc1a), [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L802) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L464)

<a id="op-b2231ba521502a"></a>
### Job Card.get manufactured qty per operation

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_manufactured_quantity_per_operation`

**Inputs** self, operation\_ids.

**Explicit results** dict(data).

**Local steps**

- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set data from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().
- Return dict(data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L399)

<a id="op-64e3527ad04ec9"></a>
### Job Card.validate later operations

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_validate_later_operations`

**Inputs** self.

**Record and data access** read “Work Order Operation” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper with OperationSequenceError — translated “Operation {0} has already completed or lost {1}, more than the {2} that operation {3} would have. Cancel the …”.format(bold(row.operation), bold(self.get\_qty\_with\_uom(used\_qty)), bold(self.get\_ ….

**Local steps**

- If (self.is\_corrective\_job\_card or not (self.work\_order and self.sequence\_id and self.operation\_id)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → not (self.work\_order and self.sequence\_id and self.operation\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.sequence\_id → self.operation\_id.
  - Return no value.
- Set data from self.get\_current\_operation\_data().
- Set operation\_qty from flt(data at 0.completed\_qty) when data, otherwise 0.0.
  - Value choice on data — true gives flt(data at 0.completed\_qty), false gives 0.0.
- Set later\_operations from Platform.get\_all(“Work Order Operation”, filters = mapping(“parent” → self.work\_order, “sequence\_id” → tuple(“&gt;”, self.sequence\_id)), fields = list(“operation”, “completed\_qty”, “process\_loss\_qty”, “output\_qty”)).
- If self.track\_semi\_finished\_goods.
  - Evaluate self.convert\_to\_current\_operation\_qty(later\_operations, list(“completed\_qty”)).
- For each row in later\_operations.
  - Set used\_qty from flt((flt(row.completed\_qty) + 0 when self.track\_semi\_finished\_goods, otherwise flt(row.process\_loss\_qty)), self.precision(“total\_completed\_qty”)).
    - Value choice on self.track\_semi\_finished\_goods — true gives 0, false gives flt(row.process\_loss\_qty).
  - If used\_qty &gt; operation\_qty.
    - Call the validation error handler Platform.throw(translated “Operation {0} has already completed or lost {1}, more than the {2} that operation {3} would have. Cancel the …”.format(bold(row.operation), bold(self.get\_qty\_with\_uom(used\_qty)), ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current operation data](operations-020.md#op-44eba10692aac0), [convert to current operation qty](operations-018.md#op-d073a22519dae3), [get qty with uom](operations-021.md#op-796d4d5f140d45).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L842)

<a id="op-b9f7fc6e84e37d"></a>
### Job Card.get previous operations

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_previous_operations`

**Inputs** self.

**Record and data access** read “Work Order Operation” via get\_all.

**Explicit results** previous\_operations.

**Local steps**

- Set previous\_operations from Platform.get\_all(“Work Order Operation”, fields = list(“name”, “operation”, “status”, “completed\_qty”, …), filters = mapping(“docstatus” → 1, “parent” → self.work\_order, “sequence\_id” → tuple(“&lt;”, self.seq ….
- If (self.track\_semi\_finished\_goods and previous\_operations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.track\_semi\_finished\_goods → previous\_operations.
  - Set totals from self.get\_manufactured\_qty\_per\_operation(list of row.name for row drawn from previous\_operations).
    - Draw row from previous\_operations.
  - For each row in previous\_operations.
    - Set row.manufactured\_qty from flt(totals.get(row.name)).
  - Evaluate self.convert\_to\_current\_operation\_qty(previous\_operations, list(“completed\_qty”, “manufactured\_qty”)).
- Return previous\_operations.

**Methods declared on this owner** [get manufactured qty per operation](operations-021.md#op-b2231ba521502a), [convert to current operation qty](operations-018.md#op-d073a22519dae3).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L404)

<a id="op-5bc555e68e5517"></a>
### Job Card.get current operation completed qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_current_operation_completed_quantity`

**Inputs** self.

**Explicit results** flt((current\_operation\_qty + flt(self.total\_completed\_qty)), self.precision(“total\_completed\_qty”)).

**Local steps**

- Set current\_operation\_qty from 0.0.
- Set data from self.get\_current\_operation\_data().
- If (data and len(data) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → len(data) &gt; 0.
  - Set current\_operation\_qty from flt(data at 0.completed\_qty).
- Return flt((current\_operation\_qty + flt(self.total\_completed\_qty)), self.precision(“total\_completed\_qty”)).

**Methods declared on this owner** [get current operation data](operations-020.md#op-44eba10692aac0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L397)

<a id="op-a414a68aa53731"></a>
### Job Card.get max completable qty

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_get_maximum_completable_quantity`

**Inputs** self.

**Explicit results** no value · flt((min\_completed\_qty − used\_qty), self.precision(“total\_completed\_qty”)).

**Local steps**

- If (self.is\_corrective\_job\_card or not (self.work\_order and self.sequence\_id)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_corrective\_job\_card → not (self.work\_order and self.sequence\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.sequence\_id.
  - Return no value.
- Set previous\_operations from self.get\_previous\_operations().
- If not previous\_operations.
  - Return no value.
- Set qty\_field from “manufactured\_qty” when self.track\_semi\_finished\_goods, otherwise “completed\_qty”.
  - Value choice on self.track\_semi\_finished\_goods — true gives “manufactured\_qty”, false gives “completed\_qty”.
- Set min\_completed\_qty from min(generator of flt(row.get(qty\_field)) for row drawn from previous\_operations).
  - Draw row from previous\_operations.
- Set used\_qty from self.get\_current\_operation\_completed\_qty() when self.track\_semi\_finished\_goods, otherwise self.get\_operation\_input\_qty().
  - Value choice on self.track\_semi\_finished\_goods — true gives self.get\_current\_operation\_completed\_qty(), false gives self.get\_operation\_input\_qty().
- Return flt((min\_completed\_qty − used\_qty), self.precision(“total\_completed\_qty”)).

**Methods declared on this owner** [get previous operations](operations-021.md#op-b9f7fc6e84e37d), [get current operation completed qty](operations-021.md#op-5bc555e68e5517), [get operation input qty](operations-021.md#op-8fc5201c511be7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L400)

<a id="op-8fc5201c511be7"></a>
### Job Card.get operation input qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_job_card_job_card_jobcard_get_operation_input_qty`

**Inputs** self.

**Explicit results** ((flt(submitted.completed\_qty) + flt(submitted.process\_loss\_qty)) + flt(self.total\_completed\_qty)).

**Local steps**

- Set submitted from self.get\_current\_operation\_data() at 0.
- Return ((flt(submitted.completed\_qty) + flt(submitted.process\_loss\_qty)) + flt(self.total\_completed\_qty)).

**Methods declared on this owner** [get current operation data](operations-020.md#op-44eba10692aac0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L818)
