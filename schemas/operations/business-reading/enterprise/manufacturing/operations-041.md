# Production · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-c8bdb41034bf45"></a>
### Work Order.get work order qty against sales order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_work_order_qty_against_sales_order`

**Inputs** self.

**Explicit results** query.run(as\_list = 1).

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set plan\_item from Platform.qb.DocType(“Production Plan Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.production\_plan\_item).select(Sum(qty\_against\_sales\_order(wo, plan ….
- If self.product\_bundle\_item.
  - Set query from query.where(wo.product\_bundle\_item equals self.product\_bundle\_item).
- Otherwise.
  - Set query from query.where((wo.production\_item equals self.production\_item bitwise and wo.sales\_order\_item equals self.sales\_order\_item)).
- Return query.run(as\_list = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1072)

<a id="op-454162196d3239"></a>
### Work Order.update work order qty in combined so

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_work_order_quantity_in_combined_sales_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Product Bundle Item) · resolve a document from “Production Plan” via get\_doc · read “Production Plan Item” via get\_value.

**State and service calls** request set\_value on “Sales Order Item”.

**Local steps**

- Set total\_bundle\_qty from 1.
- If self.product\_bundle\_item.
  - Set total\_bundle\_qty from Platform.db.sql(query text (SELECT, Product Bundle Item), Platform.db.escape(self.product\_bundle\_item)) at 0 at 0.
  - If not total\_bundle\_qty.
    - Set total\_bundle\_qty from 1.
- Set prod\_plan from Platform.get\_doc(“Production Plan”, self.production\_plan).
- Set item\_reference from Platform.get\_value(“Production Plan Item”, self.production\_plan\_item, “sales\_order\_item”).
- Set ordered\_qty from self.get\_ordered\_qty\_of\_plan\_item().
- For each plan\_reference in prod\_plan.prod\_plan\_references.
  - If plan\_reference.item\_reference differs from item\_reference.
    - Continue with the next iteration or loop test.
  - Set allocated\_qty from min(flt(plan\_reference.qty), ordered\_qty).
  - Update ordered\_qty using − allocated\_qty.
  - Evaluate Platform.db.set\_value(“Sales Order Item”, plan\_reference.sales\_order\_item, “work\_order\_qty”, (allocated\_qty ÷ total\_bundle\_qty)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ordered qty of plan item](operations-041.md#op-776720c7ae632c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L836)

<a id="op-776720c7ae632c"></a>
### Work Order.get ordered qty of plan item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_ordered_qty_of_plan_item`

**Inputs** self.

**Explicit results** flt(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0).

**Local steps**

- Set work\_order from Platform.qb.DocType(“Work Order”).
- Set plan\_item from Platform.qb.DocType(“Production Plan Item”).
- Return flt(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1065)

<a id="op-26e29b30c59274"></a>
### Work Order.update completed qty in material request

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_completed_quantity_in_material_request`

**Inputs** self.

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Local steps**

- If (self.material\_request and self.material\_request\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.material\_request → self.material\_request\_item.
  - Evaluate Platform.get\_doc(“Material Request”, self.material\_request).update\_completed\_qty(list(self.material\_request\_item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L822)

<a id="op-7ac05e9bff8b50"></a>
### Work Order.set work order operations

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_work_order_operations`

**Inputs** self.

**Record and data access** read “BOM” via get\_cached\_value · resolve a document from “BOM” via get\_doc.

**Explicit results** no value.

**Local steps**

- Bind local operation \_get\_operations for subsequent calls.
- Evaluate self.set(“operations”, list()).
- If not self.bom\_no.
  - Return no value.
- If (not self.use\_multi\_level\_bom and not Platform.get\_cached\_value(“BOM”, self.bom\_no, “with\_operations”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.use\_multi\_level\_bom → not Platform.get\_cached\_value(“BOM”, self.bom\_no, “with\_operations”).
  - Return no value.
- Set groups from list().
- If self.use\_multi\_level\_bom.
  - Set bom\_tree from Platform.get\_doc(“BOM”, self.bom\_no).get\_tree\_representation().
  - Set bom\_traversal from reversed(bom\_tree.level\_order\_traversal()).
  - For each node in bom\_traversal.
    - If node.is\_bom.
      - Set qty from (node.exploded\_qty ÷ node.bom\_qty).
      - Evaluate groups.append(tuple(\_get\_operations(node.name), qty, node.exploded\_qty, true)).
- Set bom\_qty from Platform.get\_cached\_value(“BOM”, self.bom\_no, “quantity”).
- Evaluate groups.append(tuple(\_get\_operations(self.bom\_no), bom\_qty, 1, false)).
- Set batch\_size\_flags from get\_batch\_size\_flags(generator of d.operation for tuple(data, expanded \_) drawn from groups, then d drawn from data).
  - Draw tuple(data, expanded \_) from groups.
  - Draw d from data.
- Set operations from list().
- For each tuple(data, qty, units, exploded) in groups.
  - For each d in data.
    - If not d.fixed\_time.
      - Set d.time\_in\_mins from get\_operation\_time\_per\_unit(d, qty, units, exploded, …).
    - Set d.status from “Pending”.
    - Set d.output\_qty from self.\_operation\_output\_qty(d, qty, exploded).
    - If (self.track\_semi\_finished\_goods and not d.sequence\_id).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.track\_semi\_finished\_goods → not d.sequence\_id.
      - Set d.sequence\_id from d.idx.
    - Evaluate operations.append(d).
- For each tuple(correct\_index, operation) in enumerate(operations, start = 1).
  - Set operation.idx from correct\_index.
- Evaluate self.set(“operations”, operations).
- Evaluate self.calculate\_time().
- Evaluate self.set\_operation\_warehouses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [operation output qty](operations-041.md#op-27ca362c4a1cf2), [calculate time](operations-041.md#op-c0bcbdb73edf00), [set operation warehouses](operations-041.md#op-6a9e0641644e50).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, self.bom\_no, “with\_operations”), Platform.get\_cached\_value(“BOM”, self.bom\_no, “quantity”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L820)

<a id="op-4aa8bc40e3cd09"></a>
### Work Order.set work order operations.get operations

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_work_order_operations_get_operations`

**Inputs** bom\_no.

**Record and data access** read “BOM Operation” via get\_all.

**Explicit results** Platform.get\_all(“BOM Operation”, filters = mapping(“parent” → bom\_no), fields = list(“operation”, “description”, “workstation”, “idx”, …), order\_by = “idx”).

**Local steps**

- Return Platform.get\_all(“BOM Operation”, filters = mapping(“parent” → bom\_no), fields = list(“operation”, “description”, “workstation”, “idx”, …), order\_by = “idx”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1096)

<a id="op-27ca362c4a1cf2"></a>
### Work Order.operation output qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_operation_output_qty`

**Inputs** self, d, qty, exploded.

**Explicit results** 0 · flt((per\_unit × flt(self.qty)), self.precision(“output\_qty”, “operations”)).

**Local steps**

- Set finished\_good\_qty from flt(d.pop(“finished\_good\_qty”, 0)).
- If not (finished\_good\_qty and flt(qty) and d.finished\_good).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in finished\_good\_qty → flt(qty) → d.finished\_good.
  - Return 0.
- If d.finished\_good equals self.production\_item.
  - Return 0.
- Set per\_unit from (finished\_good\_qty × flt(qty)) when exploded, otherwise (finished\_good\_qty ÷ flt(qty)).
  - Value choice on exploded — true gives (finished\_good\_qty × flt(qty)), false gives (finished\_good\_qty ÷ flt(qty)).
- Return flt((per\_unit × flt(self.qty)), self.precision(“output\_qty”, “operations”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1077)

<a id="op-6a9e0641644e50"></a>
### Work Order.set operation warehouses

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_operation_warehouses`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.track\_semi\_finished\_goods or not self.operations).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.track\_semi\_finished\_goods → not self.operations.
  - Return no value.
- Set operations from self.operations.
- Set last\_idx from (len(operations) − 1).
- For each tuple(idx, op) in enumerate(operations).
  - If not op.source\_warehouse.
    - Set op.source\_warehouse from self.source\_warehouse.
  - If not op.fg\_warehouse.
    - Set op.fg\_warehouse from self.fg\_warehouse when idx equals last\_idx, otherwise self.source\_warehouse.
      - Value choice on idx equals last\_idx — true gives self.fg\_warehouse, false gives self.source\_warehouse.
  - If not op.wip\_warehouse.
    - Set op.wip\_warehouse from self.wip\_warehouse.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L813)

<a id="op-c0bcbdb73edf00"></a>
### Work Order.calculate time

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_calculate_time`

**Inputs** self.

**Local steps**

- For each d in self.get(“operations”).
  - If not d.fixed\_time.
    - Set d.time\_in\_mins from (flt(d.time\_in\_mins) × flt(self.qty)).
- Evaluate self.calculate\_operating\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate operating cost](operations-039.md#op-730f15a256b6df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1044)

<a id="op-342c6a67c8f3da"></a>
### Work Order.get holidays

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_holidays`

**Inputs** self, workstation.

**Record and data access** read “Workstation” via get\_value · read “Holiday” via get\_all.

**Explicit results** holidays at holiday\_list.

**Local steps**

- Set holiday\_list from Platform.db.get\_value(“Workstation”, workstation, “holiday\_list”).
- Set holidays from mapping().
- If holiday\_list does not belong to holidays.
  - Set holiday\_list\_days from list of getdate(d at 0) for d drawn from Platform.get\_all(“Holiday”, fields = list(“holiday\_date”), filters = mapping(“parent” → holiday\_list), order\_by = “holiday\_date”, limit\_page\_length = 0, …).
    - Draw d from Platform.get\_all(“Holiday”, fields = list(“holiday\_date”), filters = mapping(“parent” → holiday\_list), order\_by = “holiday\_date”, limit\_page\_length = 0, …).
  - Set holidays at holiday\_list from holiday\_list\_days.
- Return holidays at holiday\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1061)

<a id="op-f640e351fbe053"></a>
### Work Order.update operation status

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_operation_status`

**Inputs** self, operation\_id = no value.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Completed Qty cannot be greater than 'Qty to Manufacture'”.

**Local steps**

- Set allowance\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- For each d in self.get(“operations”).
  - Set precision from d.precision(“completed\_qty”).
  - Set operation\_qty from get\_operation\_qty(self, d).
  - Set max\_allowed\_qty\_for\_wo from (operation\_qty + ((allowance\_percentage ÷ 100) × operation\_qty)).
  - Set qty from flt((flt(d.completed\_qty, precision) + flt(d.process\_loss\_qty, precision)), precision).
  - Set operation\_target\_qty from get\_operation\_target\_qty(self, d).
  - If (not qty and operation\_target\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not qty → operation\_target\_qty.
    - Set d.status from “Pending”.
  - Otherwise.
    - If qty &lt; operation\_target\_qty.
      - Set d.status from “Work in Progress”.
    - Otherwise.
      - If qty equals flt(operation\_qty, precision).
        - Set d.status from “Completed”.
      - Otherwise.
        - If (qty ≤ flt(max\_allowed\_qty\_for\_wo, precision) or d.name differs from operation\_id).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty ≤ flt(max\_allowed\_qty\_for\_wo, precision) → d.name differs from operation\_id.
          - Set d.status from “Completed”.
        - Otherwise.
          - Call the validation error handler Platform.throw(translated “Completed Qty cannot be greater than 'Qty to Manufacture'”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L825)

<a id="op-2bd21cd351cdfd"></a>
### Work Order.set actual dates

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_actual_dates`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.get(“operations”).
  - Set actual\_start\_dates from list of d.actual\_start\_time for d drawn from self.get(“operations”) where d.actual\_start\_time.
    - Draw d from self.get(“operations”), keep a combination only if (d.actual\_start\_time).
  - If actual\_start\_dates.
    - Set self.actual\_start\_date from min(actual\_start\_dates).
  - Set actual\_end\_dates from list of d.actual\_end\_time for d drawn from self.get(“operations”) where d.actual\_end\_time.
    - Draw d from self.get(“operations”), keep a combination only if (d.actual\_end\_time).
  - If actual\_end\_dates.
    - Set self.actual\_end\_date from max(actual\_end\_dates).
- Otherwise.
  - Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
  - Set posting\_datetime from CombineDatetime(stock\_entry.posting\_date, stock\_entry.posting\_time).
  - Set data from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“start\_date”), nested operand in the contract.as\_(“end\_date”)).where(((nested operand in the contrac ….
  - Set start\_date from data at 0.start\_date.
  - Set end\_date from data at 0.end\_date when self.status equals “Completed”, otherwise no value.
    - Value choice on self.status equals “Completed” — true gives data at 0.end\_date, false gives no value.
  - Set lead\_time from flt((time\_diff\_in\_hours(end\_date, start\_date) × 60)) when (start\_date and end\_date), otherwise 0.
    - Value choice on (start\_date and end\_date) — true gives flt((time\_diff\_in\_hours(end\_date, start\_date) × 60)), false gives 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → end\_date.
  - Evaluate self.db\_set(mapping(“actual\_start\_date” → start\_date, “actual\_end\_date” → end\_date, “lead\_time” → lead\_time)).
- Evaluate self.set\_lead\_time().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set lead time](operations-041.md#op-fcdd4ef6dc7f16).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L810)

<a id="op-fcdd4ef6dc7f16"></a>
### Work Order.set lead time

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_lead_time`

**Inputs** self.

**Local steps**

- If (self.actual\_start\_date and self.actual\_end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.actual\_start\_date → self.actual\_end\_date.
  - Set self.lead\_time from flt((time\_diff\_in\_hours(self.actual\_end\_date, self.actual\_start\_date) × 60)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1089)

<a id="op-4441dd77412c6a"></a>
### Work Order.validate production item

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_production_item`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper with ItemHasVariantError — translated “Work Order cannot be raised against a Item Template”.

**Local steps**

- If Platform.get\_cached\_value(“Item”, self.production\_item, “has\_variants”).
  - Call the validation error handler Platform.throw(translated “Work Order cannot be raised against a Item Template”, ItemHasVariantError).
- If self.production\_item.
  - Evaluate validate\_end\_of\_life(self.production\_item).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.production\_item, “has\_variants”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L844)

<a id="op-3c8e7714ae4f37"></a>
### Work Order.validate qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_quantity`

**Inputs** self.

**Record and data access** read “UOM” via get\_cached\_value.

**State and service calls** msgprint with translated “Warning: Quantity exceeds maximum producible quantity based on quantity of raw materials received through th …”.format(get\_link\_to\_form(“Subcontracting Inward Order”, self.subcontracting\_inward\_order)).

**Explicit failure paths** validation helper — translated “Quantity to Manufacture must be greater than 0.” · validation helper — translated “Batch Size cannot be negative.” · validation helper — translated “Qty To Manufacture ({0}) cannot be a fraction for the UOM {2}. To allow this, disable '{1}' in the UOM {2}.”.format(flt(self.qty, self.precision(“qty”)), Platform.bold(translated “Must be Whole ….

**Local steps**

- <a id="op-3c8e7714ae4f37-guard-2"></a>If self.qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Quantity to Manufacture must be greater than 0.”).
- If flt(self.batch\_size) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Batch Size cannot be negative.”).
- If (self.stock\_uom and Platform.get\_cached\_value(“UOM”, self.stock\_uom, “must\_be\_whole\_number”) and abs((cint(self.qty) − flt(self.qty, nested operand in the contract.precision(“qty”)))) &gt; 1e-07).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.stock\_uom → Platform.get\_cached\_value(“UOM”, self.stock\_uom, “must\_be\_whole\_number”) → abs((cint(self.qty) − flt(self.qty, self.precision(“qty”)))) &gt; 1e-07.
  - Call the validation error handler Platform.throw(translated “Qty To Manufacture ({0}) cannot be a fraction for the UOM {2}. To allow this, disable '{1}' in the UOM {2}.”.format(flt(self.qty, self.precision(“qty”)), Platform.bold(translated ….
- If (self.subcontracting\_inward\_order and self.qty &gt; self.max\_producible\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → self.qty &gt; self.max\_producible\_qty.
  - Evaluate Platform.msgprint(translated “Warning: Quantity exceeds maximum producible quantity based on quantity of raw materials received through th …”.format(get\_link\_to\_form(“Subcontracting Inward Order”, self.sub ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.qty ≤ 0, self.qty = 0 selects the branch that calls the validation-error handler with translated “Quantity to Manufacture must be greater than 0.”. With self.qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3c8e7714ae4f37-guard-2)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, self.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L845)

<a id="op-5ffcdd00c7a4a1"></a>
### Work Order.validate transfer against

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_transfer_against`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Setting {0} is required”.format(translated self.meta.get\_label(“transfer\_material\_against”)).

**Local steps**

- <a id="op-5ffcdd00c7a4a1-guard-2"></a>If self.docstatus differs from 1.
  - Return no value.
- If not self.operations.
  - Set self.transfer\_material\_against from “Work Order”.
- If not self.transfer\_material\_against.
  - Call the validation error handler Platform.throw(translated “Setting {0} is required”.format(translated self.meta.get\_label(“transfer\_material\_against”)), title = translated “Missing value”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that returns no value. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5ffcdd00c7a4a1-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L848)

<a id="op-f7179b450be773"></a>
### Work Order.validate operations

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_operations`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Operation Time must be greater than 0 for Operation {0}”.format(d.operation).

**Local steps**

- For each d in self.operations.
  - If (not d.batch\_size or d.batch\_size ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.batch\_size → d.batch\_size ≤ 0.
    - Set d.batch\_size from 1.
  - If d.time\_in\_mins ≤ 0.
    - Call the validation error handler Platform.throw(translated “Operation Time must be greater than 0 for Operation {0}”.format(d.operation)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0534.json#L2111) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L842)

<a id="op-22bb7434c16a91"></a>
### Work Order.update required items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_required_items`

**Inputs** self.

**Local steps**

- If self.docstatus equals 1.
  - Evaluate self.update\_returned\_qty().
- Evaluate self.update\_consumed\_qty\_for\_required\_items().
- If self.docstatus equals 1.
  - Evaluate self.update\_transferred\_qty\_for\_required\_items().
  - Evaluate self.update\_reserved\_qty\_for\_production().
- Evaluate self.validate\_reserved\_qty().
- If self.status equals “Closed”.
  - Evaluate self.update\_subcontracting\_inward\_order\_received\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update returned qty](operations-042.md#op-f27d84ab7dbb1d), [update consumed qty for required items](operations-042.md#op-1011763a46381c), [update transferred qty for required items](operations-042.md#op-4f878759c4272e), [update reserved qty for production](operations-041.md#op-d40b48267db3bf), [validate reserved qty](operations-042.md#op-88341bc70ac7f2), [update subcontracting inward order received items](operations-040.md#op-62168b44418fa5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L829)

<a id="op-d40b48267db3bf"></a>
### Work Order.update reserved qty for production

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_reserved_quantity_for_production`

**Inputs** self, items = no value.

**Local steps**

- For each d in self.required\_items.
  - If d.source\_warehouse.
    - Set stock\_bin from get\_bin(d.item\_code, d.source\_warehouse).
    - Evaluate stock\_bin.update\_reserved\_qty\_for\_production().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L830)

<a id="op-269f4b3689a606"></a>
### Work Order.get items and operations from bom

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_get_items_and_operations_from_bill_of_materials`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** check\_if\_scrap\_warehouse\_mandatory(self.bom\_no).

**Local steps**

- If not self.fg\_warehouse.
  - Set self.fg\_warehouse from self.get\_default\_fg\_warehouse().
- Evaluate self.set\_required\_items().
- Evaluate self.set\_work\_order\_operations().
- Return check\_if\_scrap\_warehouse\_mandatory(self.bom\_no).

**Methods declared on this owner** [get default fg warehouse](operations-039.md#op-cd6aacf2d8126e), [set required items](operations-041.md#op-2bf328b6767c61), [set work order operations](operations-041.md#op-7ac05e9bff8b50).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L794)

<a id="op-c07e058a6f1777"></a>
### Work Order.set available qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_available_quantity`

**Inputs** self.

**Local steps**

- Set items\_by\_warehouse from mapping().
- For each d in self.get(“required\_items”).
  - For each warehouse in tuple(d.source\_warehouse, self.wip\_warehouse).
    - If warehouse.
      - Evaluate items\_by\_warehouse.setdefault(warehouse, set()).add(d.item\_code).
- Set available\_qty from get\_latest\_stock\_qty\_for\_items(items\_by\_warehouse).
- For each d in self.get(“required\_items”).
  - If d.source\_warehouse.
    - Set d.available\_qty\_at\_source\_warehouse from available\_qty.get(tuple(d.item\_code, d.source\_warehouse)).
  - If self.wip\_warehouse.
    - Set d.available\_qty\_at\_wip\_warehouse from available\_qty.get(tuple(d.item\_code, self.wip\_warehouse)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L811)

<a id="op-2bf328b6767c61"></a>
### Work Order.set required items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_required_items`

**Inputs** self, reset\_only\_qty = false, reset\_source\_warehouse = false.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If not reset\_only\_qty.
  - Set self.required\_items from list().
- Set operation from no value.
- If (self.get(“operations”) and len(self.operations) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“operations”) → len(self.operations) equals 1.
  - Set operation from self.operations at 0.operation.
- If (self.bom\_no and self.qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.bom\_no → self.qty.
  - Set item\_dict from get\_bom\_items\_as\_dict(self.bom\_no, self.company, qty = self.qty, fetch\_exploded = self.use\_multi\_level\_bom).
  - If reset\_only\_qty.
    - For each d in self.get(“required\_items”).
      - If bom\_item bound to find\_bom\_item(item\_dict, d).
        - Set d.required\_qty from bom\_item.get(“qty”).
      - If not d.operation.
        - Set d.operation from operation.
  - Otherwise.
    - For each item in sorted(item\_dict.values(), key = deferred anonymous expression).
      - Evaluate self.append(“required\_items”, mapping(“rate” → item.rate, “amount” → (item.rate × item.qty), “operation” → (item.operation or operation), “item\_code” → item.item\_code, …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.operation → operation.
        - Value choice on not reset\_source\_warehouse — true gives (self.source\_warehouse or item.source\_warehouse or item.default\_warehouse or get\_item\_group\_defaults(item.item\_code, self.company).get(“default\_warehouse”)), false gives self.source\_warehouse.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.source\_warehouse → item.source\_warehouse → item.default\_warehouse → get\_item\_group\_defaults(item.item\_code, self.company).get(“default\_warehouse”).
      - If (self.subcontracting\_inward\_order and not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
        - Set self.required\_items at negative 1.source\_warehouse from item.default\_warehouse.
      - If not self.project.
        - Set self.project from item.get(“project”).
  - Evaluate self.set\_available\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set available qty](operations-041.md#op-c07e058a6f1777).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L817)

<a id="op-df7e577faf3dc6"></a>
### Work Order.set rate for edited items

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_rate_for_edited_items`

**Inputs** self.

**Record and data access** resolve a document from “BOM” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- Set previous\_items from mapping of d.name → d.item\_code for d drawn from previous.required\_items when previous, otherwise mapping().
  - Value choice on previous — true gives mapping of d.name → d.item\_code for d drawn from previous.required\_items, false gives mapping().
  - Draw d from previous.required\_items.
- Set bom\_items from get\_bom\_items\_as\_dict(self.bom\_no, self.company, fetch\_exploded = self.use\_multi\_level\_bom).
- Set edited\_rows from list of d for d drawn from self.get(“required\_items”) where is\_edited\_item(d, previous\_items, bom\_items).
  - Draw d from self.get(“required\_items”), keep a combination only if (is\_edited\_item(d, previous\_items, bom\_items)).
- If not edited\_rows.
  - Return no value.
- Set bom\_doc from Platform.get\_cached\_doc(“BOM”, self.bom\_no).
- For each d in edited\_rows.
  - Set d.rate from flt(get\_raw\_material\_rate(d, self, bom\_doc), d.precision(“rate”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“BOM”, self.bom\_no).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1092)

<a id="op-6548508787acc9"></a>
### Work Order.set required item amounts

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_required_item_amounts`

**Inputs** self.

**Local steps**

- For each d in self.get(“required\_items”).
  - Set d.amount from flt((flt(d.rate) × flt(d.required\_qty)), d.precision(“amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1093)
