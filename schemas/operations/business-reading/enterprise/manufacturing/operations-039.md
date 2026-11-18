# Production · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-e49ccc119614ee"></a>
### Work Order.set default warehouse

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_default_warehouse`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (not self.wip\_warehouse and not self.skip\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.wip\_warehouse → not self.skip\_transfer.
  - Set self.wip\_warehouse from Platform.get\_cached\_value(“Company”, self.company, “default\_wip\_warehouse”).
- If not self.fg\_warehouse.
  - Set self.fg\_warehouse from self.get\_default\_fg\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get default fg warehouse](operations-039.md#op-cd6aacf2d8126e).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_wip\_warehouse”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L812)

<a id="op-cd6aacf2d8126e"></a>
### Work Order.get default fg warehouse

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_default_fg_warehouse`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (self.get\_bom\_target\_warehouse() or Platform.get\_cached\_value(“Company”, self.company, “default\_fg\_warehouse”) or self.get\_production\_item\_warehouse()).

**Local steps**

- Return (self.get\_bom\_target\_warehouse() or Platform.get\_cached\_value(“Company”, self.company, “default\_fg\_warehouse”) or self.get\_production\_item\_warehouse()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_bom\_target\_warehouse() → Platform.get\_cached\_value(“Company”, self.company, “default\_fg\_warehouse”) → self.get\_production\_item\_warehouse().

**Methods declared on this owner** [get bom target warehouse](operations-039.md#op-a113db1ee71247), [get production item warehouse](operations-039.md#op-72148a7d1b4a0b).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_fg\_warehouse”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1058)

<a id="op-a113db1ee71247"></a>
### Work Order.get bom target warehouse

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_bom_target_warehouse`

**Inputs** self.

**Record and data access** read “BOM” via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Explicit results** warehouse.

**Local steps**

- Set warehouse from (self.bom\_no and Platform.get\_cached\_value(“BOM”, self.bom\_no, “default\_target\_warehouse”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.bom\_no → Platform.get\_cached\_value(“BOM”, self.bom\_no, “default\_target\_warehouse”).
- If (warehouse and Platform.get\_cached\_value(“Warehouse”, warehouse, “company”) equals self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → Platform.get\_cached\_value(“Warehouse”, warehouse, “company”) equals self.company.
  - Return warehouse.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, self.bom\_no, “default\_target\_warehouse”), Platform.get\_cached\_value(“Warehouse”, warehouse, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1055)

<a id="op-72148a7d1b4a0b"></a>
### Work Order.get production item warehouse

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_get_production_item_warehouse`

**Inputs** self.

**Explicit results** no value · (get\_item\_defaults(self.production\_item, self.company).get(“default\_warehouse”) or get\_item\_group\_defaults(self.production\_item, self.company).get(“default\_warehouse”)).

**Local steps**

- If not self.production\_item.
  - Return no value.
- Return (get\_item\_defaults(self.production\_item, self.company).get(“default\_warehouse”) or get\_item\_group\_defaults(self.production\_item, self.company).get(“default\_warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(self.production\_item, self.company).get(“default\_warehouse”) → get\_item\_group\_defaults(self.production\_item, self.company).get(“default\_warehouse”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L2211) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L795)

<a id="op-2f02b843bc3580"></a>
### Work Order.check wip warehouse skip

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_check_work_in_progress_warehouse_skip`

**Inputs** self.

**Local steps**

- If (self.skip\_transfer and not self.from\_wip\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_transfer → not self.from\_wip\_warehouse.
  - Set self.wip\_warehouse from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L2377) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L791)

<a id="op-65bdd4766c556f"></a>
### Work Order.validate warehouse belongs to company

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_warehouse_belongs_to_company`

**Inputs** self.

**Local steps**

- Set warehouses from list(self.fg\_warehouse, self.wip\_warehouse).
- For each d in self.get(“required\_items”).
  - If d.source\_warehouse does not belong to warehouses.
    - Evaluate warehouses.append(d.source\_warehouse).
- For each wh in warehouses.
  - Evaluate validate\_warehouse\_company(wh, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L2459) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L850)

<a id="op-730f15a256b6df"></a>
### Work Order.calculate operating cost

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_calculate_operating_cost`

**Inputs** self.

**Local steps**

- Set tuple(self.planned\_operating\_cost, self.actual\_operating\_cost) from tuple(0.0, 0.0).
- Set job\_card\_costs from self.get\_job\_card\_operating\_costs().
- For each d in self.get(“operations”).
  - Evaluate self.set\_operation\_cost(d, job\_card\_costs).
  - Update self.planned\_operating\_cost using + flt(d.planned\_operating\_cost).
  - Update self.actual\_operating\_cost using + flt(d.actual\_operating\_cost).
- Set variable\_cost from self.actual\_operating\_cost when self.actual\_operating\_cost, otherwise self.planned\_operating\_cost.
  - Value choice on self.actual\_operating\_cost — true gives self.actual\_operating\_cost, false gives self.planned\_operating\_cost.
- Set self.total\_operating\_cost from ((flt(self.additional\_operating\_cost) + flt(variable\_cost)) + flt(self.corrective\_operation\_cost)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get job card operating costs](operations-039.md#op-09f7274ca4c141), [set operation cost](operations-039.md#op-1ee969d05fab5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L790)

<a id="op-1ee969d05fab5d"></a>
### Work Order.set operation cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_operation_cost`

**Inputs** d, job\_card\_costs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- If (not d.hour\_rate and d.workstation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.hour\_rate → d.workstation.
  - Set d.hour\_rate from get\_hour\_rate(d.workstation).
- Set d.planned\_operating\_cost from flt((flt(d.hour\_rate) × (flt(d.time\_in\_mins) ÷ 60.0)), d.precision(“planned\_operating\_cost”)).
- Set actual\_cost from job\_card\_costs.get(d.name).
- If actual\_cost is identical to no value.
  - Set actual\_cost from (flt(d.hour\_rate) × (flt(d.actual\_operation\_time) ÷ 60.0)).
- Set d.actual\_operating\_cost from flt(actual\_cost, d.precision(“actual\_operating\_cost”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1090)

<a id="op-09f7274ca4c141"></a>
### Work Order.get job card operating costs

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_job_card_operating_costs`

**Inputs** self.

**Explicit results** mapping() · mapping of row.operation\_id → flt(row.cost) for row drawn from rows.

**Local steps**

- If (self.docstatus differs from 1 or not self.get(“operations”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → not self.get(“operations”).
  - Return mapping().
- Set job\_card from Platform.qb.DocType(“Job Card”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Return mapping of row.operation\_id → flt(row.cost) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1063)

<a id="op-736bd65327b36c"></a>
### Work Order.validate work order against so

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_work_order_against_sales_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Sales) · execute query text (SELECT, Packed Item) · read “Manufacturing Settings” via get\_single\_value · read “Item” via get\_value.

**Explicit failure paths** validation helper with OverProductionError — translated “Cannot produce more Item {0} than Sales Order quantity {1} {2}”.format(get\_link\_to\_form(“Item”, self.production\_item), Platform.bold(so\_qty), Platform.bold(Platform.get\_value(“Item”, self.produ ….

**Local steps**

- Bind dependencies get\_qty\_before\_process\_loss.
- Set wo from Platform.qb.DocType(“Work Order”).
- Set plan\_item from Platform.qb.DocType(“Production Plan Item”).
- Set ordered\_qty\_against\_so from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract differs from nes … at 0.
- Set so\_item\_qty from Platform.db.sql(query text (SELECT, Sales), tuple(self.sales\_order, self.production\_item)) at 0 at 0.
- Set dnpi\_qty from Platform.db.sql(query text (SELECT, Packed Item), tuple(self.sales\_order, self.production\_item)) at 0 at 0.
- Set so\_qty from (flt(so\_item\_qty) + flt(dnpi\_qty)).
- Set allowance\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”)).
- Set max\_qty from get\_qty\_before\_process\_loss(((so\_qty + ((allowance\_percentage ÷ 100) × so\_qty)) − flt(ordered\_qty\_against\_so)), self.\_planned\_process\_loss\_percentage(), self.stock\_uom).
- Set precision from self.precision(“qty”).
- If flt(self.qty, precision) &gt; flt(max\_qty, precision).
  - Call the validation error handler Platform.throw(translated “Cannot produce more Item {0} than Sales Order quantity {1} {2}”.format(get\_link\_to\_form(“Item”, self.production\_item), Platform.bold(so\_qty), Platform.bold(Platform.get\_value(“It ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [planned process loss percentage](operations-039.md#op-a389c4d240926f).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L851)

<a id="op-a389c4d240926f"></a>
### Work Order.planned process loss percentage

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_planned_process_loss_percentage`

**Inputs** self.

**Record and data access** read “Production Plan Item” via get\_value.

**Explicit results** 0 · Platform.db.get\_value(“Production Plan Item”, self.production\_plan\_item, “process\_loss\_percentage”).

**Local steps**

- If not self.production\_plan\_item.
  - Return 0.
- Return Platform.db.get\_value(“Production Plan Item”, self.production\_plan\_item, “process\_loss\_percentage”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1079)

<a id="op-1bfa8d77f2544a"></a>
### Work Order.update status

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_status`

**Inputs** self, status = no value.

**State and service calls** call db\_set on self.

**Explicit results** (status or self.status).

**Local steps**

- If self.docstatus equals 1.
  - Evaluate self.refresh\_material\_transferred\_for\_manufacturing().
- If self.status differs from “Closed”.
  - If status does not belong to list(“Stopped”, “Closed”).
    - Set status from self.get\_status(status).
  - If status differs from self.status.
    - Evaluate self.db\_set(“status”, status).
- Evaluate self.update\_required\_items().
- Return (status or self.status).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status → self.status.

**Methods declared on this owner** [refresh material transferred for manufacturing](operations-042.md#op-9e2e8ec34d746a), [get status](operations-039.md#op-7a6d94ec35a98e), [update required items](operations-041.md#op-22bb7434c16a91).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L832)

<a id="op-7a6d94ec35a98e"></a>
### Work Order.get status

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_get_status`

**Inputs** self, status = no value.

**Explicit results** status.

**Local steps**

- If not status.
  - Set status from self.status.
- If (self.docstatus equals 1 and status equals “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → status equals “Closed”.
  - Return status.
- If self.docstatus equals 0.
  - Set status from “Draft”.
- Otherwise.
  - If self.docstatus equals 1.
    - If status does not belong to list(“Closed”, “Stopped”).
      - Set status from “Not Started”.
      - If (flt(self.material\_transferred\_for\_manufacturing) &gt; 0 or self.\_has\_transferred\_material()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.material\_transferred\_for\_manufacturing) &gt; 0 → self.\_has\_transferred\_material().
        - Set status from “In Process”.
      - Set precision from Platform.get\_precision(“Work Order”, “produced\_qty”).
      - Set total\_qty from (flt(self.produced\_qty, precision) + flt(self.process\_loss\_qty, precision)).
      - If flt(total\_qty, precision) ≥ flt(self.qty, precision).
        - Set status from “Completed”.
  - Otherwise.
    - Set status from “Cancelled”.
- If (self.skip\_transfer and self.produced\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.skip\_transfer → self.produced\_qty.
  - Set precision from Platform.get\_precision(“Work Order”, “produced\_qty”).
  - Set total\_qty from (flt(self.produced\_qty, precision) + flt(self.process\_loss\_qty, precision)).
  - If flt(self.qty, precision) &gt; flt(total\_qty, precision).
    - Set status from “In Process”.
- If status differs from “Completed”.
  - If not all(generator of d.status equals “Pending” for d drawn from self.operations).
    - Draw d from self.operations.
    - Set status from “In Process”.
- If (status equals “Not Started” and self.reserve\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status equals “Not Started” → self.reserve\_stock.
  - If any(generator of row.stock\_reserved\_qty for row drawn from self.required\_items).
    - Draw row from self.required\_items.
    - If any(generator of row.stock\_reserved\_qty &lt; row.required\_qty for row drawn from self.required\_items).
      - Draw row from self.required\_items.
      - Set status from “Stock Partially Reserved”.
    - Otherwise.
      - Set status from “Stock Reserved”.
- Return status.

**Methods declared on this owner** [has transferred material](operations-039.md#op-3e943f6295fbec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L796)

<a id="op-3e943f6295fbec"></a>
### Work Order.has transferred material

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_has_transferred_material`

**Inputs** self.

**Explicit results** (flt(transferred\_qty) − flt(returned\_qty)) &gt; 0.

**Local steps**

- Set ste from Platform.qb.DocType(“Stock Entry”).
- Set ste\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set mr\_ste from Platform.qb.DocType(“Stock Entry”).
- Set mr\_child from Platform.qb.DocType(“Stock Entry Detail”).
- Set mr\_sourced\_stock\_entries from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(mr\_child.parent).where((((nested operand in the co ….
- Set common\_filters from ((ste.work\_order equals self.name bitwise and ste.docstatus equals 1) bitwise and ste.purpose equals “Material Transfer for Manufacture”).
- Set transferred\_qty from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest … at 0.
- Set returned\_qty from nested operand in the contract(nested operand in the contract).where((common\_filters bitwise and nested operand in the contract equals nested operand in the contract)).run() at 0 at 0.
- Return (flt(transferred\_qty) − flt(returned\_qty)) &gt; 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1073)

<a id="op-194365f5292df0"></a>
### Work Order.update work order qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_work_order_quantity`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper with StockOverProductionError — translated “{0} ({1}) cannot be greater than planned quantity ({2}) in Work Order {3}”.format(translated “Manufactured Qty (including Process Loss)” when purpose equals “Manufacture”, otherwise translated  ….

**Local steps**

- If self.track\_semi\_finished\_goods.
  - Return no value.
- Evaluate self.set\_process\_loss\_qty().
- Set overproduction\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
- Set transfer\_extra\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”)).
- For each tuple(purpose, fieldname) in tuple(tuple(“Manufacture”, “produced\_qty”), tuple(“Material Transfer for Manufacture”, “material\_transferred\_for\_manufacturing”), tuple(“Material Transfer for Manufacture”, “additional\_transferred\_qty”)).
  - If (purpose equals “Material Transfer for Manufacture” and self.operations and self.transfer\_material\_against equals “Job Card”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose equals “Material Transfer for Manufacture” → self.operations → self.transfer\_material\_against equals “Job Card”.
    - Continue with the next iteration or loop test.
  - Set qty from self.get\_transferred\_or\_manufactured\_qty(purpose, fieldname).
  - Set allowance\_percentage from overproduction\_percentage.
  - If purpose equals “Material Transfer for Manufacture”.
    - Set allowance\_percentage from (transfer\_extra\_percentage or overproduction\_percentage).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in transfer\_extra\_percentage → overproduction\_percentage.
  - Set completed\_qty from (self.qty + ((allowance\_percentage ÷ 100) × self.qty)).
  - Set qty\_to\_validate from (qty + flt(self.process\_loss\_qty)) when purpose equals “Manufacture”, otherwise qty.
    - Value choice on purpose equals “Manufacture” — true gives (qty + flt(self.process\_loss\_qty)), false gives qty.
  - Set precision from self.precision(fieldname).
  - If flt(qty\_to\_validate, precision) &gt; flt(completed\_qty, precision).
    - Call the validation error handler Platform.throw(translated “{0} ({1}) cannot be greater than planned quantity ({2}) in Work Order {3}”.format(translated “Manufactured Qty (including Process Loss)” when purpose equals “Manufacture”, otherw ….
      - Value choice on purpose equals “Manufacture” — true gives translated “Manufactured Qty (including Process Loss)”, false gives translated self.meta.get\_label(fieldname).
  - If purpose equals “Manufacture”.
    - Evaluate self.validate\_produced\_qty\_covers\_disassembly(qty, precision).
  - Evaluate self.db\_set(fieldname, qty).
  - If (purpose equals “Manufacture” and self.production\_plan).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose equals “Manufacture” → self.production\_plan.
    - Evaluate ProductionPlanWorkOrderQuantities(self.production\_plan).validate\_work\_order(self, process\_loss\_qty = self.process\_loss\_qty).
  - Bind dependencies update\_produced\_qty\_in\_so\_item.
  - If (self.sales\_order and self.sales\_order\_item and not self.production\_plan\_sub\_assembly\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sales\_order → self.sales\_order\_item → not self.production\_plan\_sub\_assembly\_item.
    - Evaluate update\_produced\_qty\_in\_so\_item(self.sales\_order, self.sales\_order\_item).
- Evaluate self.update\_work\_order\_qty\_in\_sales\_orders().
- If self.production\_plan.
  - Evaluate self.set\_produced\_qty\_for\_sub\_assembly\_item().
  - Evaluate self.update\_production\_plan\_status().
- If self.additional\_transferred\_qty.
  - Evaluate self.validate\_additional\_transferred\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set process loss qty](operations-039.md#op-d6dba9bc0d4134), [get transferred or manufactured qty](operations-039.md#op-67c1568be00a5d), [validate produced qty covers disassembly](operations-039.md#op-d98c2ef4b92b44), [update work order qty in sales orders](operations-040.md#op-4dd2788d870eea), [set produced qty for sub assembly item](operations-040.md#op-16e7a9419fcadf), [update production plan status](operations-039.md#op-7342cce86e4f9b), [validate additional transferred qty](operations-039.md#op-cd969083d3adde).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”), Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L835)

<a id="op-cd969083d3adde"></a>
### Work Order.validate additional transferred qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_additional_transferred_quantity`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated multiline text in the contract.format(actual\_qty, allowed\_qty).

**Local steps**

- Set transfer\_extra\_materials\_percentage from Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”).
- Set allowed\_qty from (flt(self.qty) + flt(((flt(self.qty) × flt(transfer\_extra\_materials\_percentage)) ÷ 100))).
- Set actual\_qty from (flt(self.material\_transferred\_for\_manufacturing) + flt(self.additional\_transferred\_qty)).
- Set precision from Platform.get\_precision(“Work Order”, “qty”).
- If flt((allowed\_qty − actual\_qty), precision) &lt; 0.
  - Call the validation error handler Platform.throw(translated multiline text in the contract.format(actual\_qty, allowed\_qty)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L839)

<a id="op-d98c2ef4b92b44"></a>
### Work Order.validate produced qty covers disassembly

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_validate_produced_qty_covers_disassembly`

**Inputs** self, produced\_qty, precision.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Manufactured Qty ({0}) cannot be less than the Disassembled Qty ({1}) of Work Order {2}. Cancel the disassem …”.format(flt(produced\_qty, precision), flt(self.disassembled\_qty, precision), self.name).

**Local steps**

- If flt(produced\_qty, precision) ≥ flt(self.disassembled\_qty, precision).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Manufactured Qty ({0}) cannot be less than the Disassembled Qty ({1}) of Work Order {2}. Cancel the disassem …”.format(flt(produced\_qty, precision), flt(self.disassembled\_qty, pr ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1109)

<a id="op-e650e8d95ae573"></a>
### Work Order.update disassembled qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_disassembled_quantity`

**Inputs** self, qty, is\_cancel = false.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Cannot disassemble more than produced quantity.”.

**Local steps**

- Set precision from self.precision(“disassembled\_qty”).
- If is\_cancel.
  - Set self.disassembled\_qty from max(0, flt((self.disassembled\_qty − qty), precision)).
- Otherwise.
  - If self.docstatus equals 1.
    - Set self.disassembled\_qty from flt((self.disassembled\_qty + qty), precision).
- If (not is\_cancel and self.disassembled\_qty &gt; self.produced\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_cancel → self.disassembled\_qty &gt; self.produced\_qty.
  - Call the validation error handler Platform.throw(translated “Cannot disassemble more than produced quantity.”).
- Evaluate self.db\_set(“disassembled\_qty”, self.disassembled\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L824)

<a id="op-67c1568be00a5d"></a>
### Work Order.get transferred or manufactured qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_get_transferred_or_manufactured_quantity`

**Inputs** self, purpose, fieldname.

**Explicit results** flt(query.run() at 0 at 0).

**Local steps**

- Set parent from Platform.qb.DocType(“Stock Entry”).
- Set query from Platform.qb.from\_(parent).where((((parent.work\_order equals self.name bitwise and parent.docstatus equals 1) bitwise and parent.purpose equals purpose) bitwise and parent.is\_additional\_transfer\_entry equal ….
- If purpose equals “Manufacture”.
  - Set child from Platform.qb.DocType(“Stock Entry Detail”).
  - Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(Sum(child.transfer\_qty)).where(child.is\_finished\_i ….
- Otherwise.
  - Set job\_card from Platform.qb.DocType(“Job Card”).
  - Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.job\_card equals nested operand in the contract.name).where(IfNull(job\_card.is\_corrective\_job\_card, 0) equals ….
- Return flt(query.run() at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L797)

<a id="op-d6dba9bc0d4134"></a>
### Work Order.set process loss qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_process_loss_quantity`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value.

**State and service calls** call db\_set on self.

**Local steps**

- Set quantities from no value.
- If (self.docstatus equals 1 and self.production\_plan).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.production\_plan.
  - Set quantities from ProductionPlanWorkOrderQuantities(self.production\_plan).
  - Evaluate quantities.lock\_plan\_row(self).
- Set process\_loss\_qty from self.\_process\_loss\_qty().
- If quantities.
  - Set previous\_loss\_qty from Platform.db.get\_value(“Work Order”, self.name, “process\_loss\_qty”, for\_update = true).
  - If process\_loss\_qty &lt; flt(previous\_loss\_qty).
    - Evaluate quantities.validate\_work\_order(self, process\_loss\_qty = process\_loss\_qty).
- Evaluate self.db\_set(“process\_loss\_qty”, process\_loss\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process loss qty](operations-039.md#op-2d68e2048bd2b7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L814)

<a id="op-6d0204dc09dc93"></a>
### Work Order.process loss in finished good units

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_process_loss_in_finished_good_units`

**Inputs** self, row.

**Explicit results** 0.0 · flt(process\_loss\_qty, self.precision(“process\_loss\_qty”)).

**Local steps**

- Set operation\_qty from get\_operation\_qty(self, row).
- If not operation\_qty.
  - Return 0.0.
- Set process\_loss\_qty from ((flt(row.process\_loss\_qty) × flt(self.qty)) ÷ operation\_qty).
- Return flt(process\_loss\_qty, self.precision(“process\_loss\_qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1081)

<a id="op-2d68e2048bd2b7"></a>
### Work Order.process loss qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_process_loss_qty`

**Inputs** self.

**Explicit results** flt(sum(generator of self.\_process\_loss\_in\_finished\_good\_units(row) for row drawn from self.operations)) · flt(process\_loss\_qty).

**Local steps**

- If self.track\_semi\_finished\_goods.
  - Return flt(sum(generator of self.\_process\_loss\_in\_finished\_good\_units(row) for row drawn from self.operations)).
    - Draw row from self.operations.
- Set table from Platform.qb.DocType(“Stock Entry”).
- Set process\_loss\_qty from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
- Return flt(process\_loss\_qty).

**Methods declared on this owner** [process loss in finished good units](operations-039.md#op-6d0204dc09dc93).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1082)

<a id="op-7342cce86e4f9b"></a>
### Work Order.update production plan status

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_production_plan_status`

**Inputs** self.

**Record and data access** resolve a document from “Production Plan” via get\_doc · read “Work Order” via get\_all.

**Local steps**

- Set production\_plan from Platform.get\_doc(“Production Plan”, self.production\_plan).
- Set production\_plan.flags.ignore\_permissions from true.
- Set produced\_qty from 0.
- If self.production\_plan\_item.
  - Set total\_qty from Platform.get\_all(“Work Order”, fields = list(mapping(“SUM” → “produced\_qty”, “as” → “produced\_qty”)), filters = mapping(“docstatus” → 1, “production\_plan” → self.production\_plan, “production\_plan\_item” → s ….
  - Set produced\_qty from total\_qty at 0 at 0 when total\_qty, otherwise 0.
    - Value choice on total\_qty — true gives total\_qty at 0 at 0, false gives 0.
- Evaluate self.update\_status().
- Evaluate production\_plan.run\_method(“update\_produced\_pending\_qty”, produced\_qty, self.production\_plan\_item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-039.md#op-1bfa8d77f2544a).

**Values supplied outside this operation** selected callable from production\_plan.run\_method(“update\_produced\_pending\_qty”, produced\_qty, self.production\_plan\_item).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L828)

<a id="op-853e07d5695a23"></a>
### Work Order.validate warehouse

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_warehouse`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Work-in-Progress Warehouse is required before Submit” · validation helper — translated “Target Warehouse is required before Submit”.

**Local steps**

- If (not self.wip\_warehouse and not self.skip\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.wip\_warehouse → not self.skip\_transfer.
  - Call the validation error handler Platform.throw(translated “Work-in-Progress Warehouse is required before Submit”).
- If (not self.fg\_warehouse and not self.track\_semi\_finished\_goods).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.fg\_warehouse → not self.track\_semi\_finished\_goods.
  - Call the validation error handler Platform.throw(translated “Target Warehouse is required before Submit”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L3039) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L849)
