# Production · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-38637030a00ac1"></a>
### Work Order.secondary items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_secondary_items`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** secondary\_items\_generated · secondary\_items.

**Local steps**

- Set parent from Platform.qb.DocType(“Stock Entry”).
- Set child from Platform.qb.DocType(“Stock Entry Detail”).
- Set secondary\_items\_generated from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest ….
- If secondary\_items\_generated.
  - Evaluate self.set\_onload(“secondary\_items\_generated”, true).
  - Return secondary\_items\_generated.
- Otherwise.
  - Set secondary\_items from Platform.get\_query(“BOM”, filters = mapping(“name” → self.bom\_no), fields = list(“secondary\_items.item\_code”, “secondary\_items.secondary\_item\_type”, “secondary\_items.qty”, “secondary\_items.uom”, …)).run(as ….
  - Set secondary\_items from list of item for item drawn from secondary\_items where item.item\_code.
    - Draw item from secondary\_items, keep a combination only if (item.item\_code).
  - Set precision from Platform.get\_precision(“Work Order Additional Item”, “amount”).
  - For each item in secondary\_items.
    - Set item at “qty” from ((item.qty ÷ item.bom\_qty) × self.qty).
    - Set item at “amount” from flt(((flt(item.amount) × self.qty) ÷ item.bom\_qty), precision).
  - Return secondary\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L809)

<a id="op-f885b53abeab2f"></a>
### Work Order.non stock items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_non_stock_items`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** non\_stock\_items.

**Local steps**

- Set non\_stock\_items from Platform.get\_query(“BOM”, filters = mapping(“name” → self.bom\_no, “items.is\_stock\_item” → 0, “items.is\_phantom\_item” → 0), fields = list(“items.item\_code”, “items.qty”, “items.uom”, “items.base\_rate as rat ….
- For each item in non\_stock\_items.
  - Set item at “qty” from ((item.qty ÷ item.bom\_qty) × self.qty).
  - Set item at “amount” from (item.rate × item at “qty”).
- Return non\_stock\_items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L2691) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L800)

<a id="op-c1fdc1c8276bf3"></a>
### Work Order.show create job card button

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_show_create_job_card_button`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Set jc\_doctype from Platform.qb.DocType(“Job Card”).
- Set query from nested operand in the contract(nested operand in the contract).select(jc\_doctype.operation\_id, Sum((nested operand in the contract − nested operand in the contract))).where((jc\_doctype.docstatus &lt; 2 bitwis ….
- Set operation\_details from query.run(as\_list = 1).
- Set operation\_details from Platform.\_dict(operation\_details).
- For each d in self.operations.
  - Set job\_card\_qty from flt((get\_operation\_target\_qty(self, d) − flt(operation\_details.get(d.name))), d.precision(“completed\_qty”)).
  - <a id="op-c1fdc1c8276bf3-guard-18"></a>If job\_card\_qty &gt; 0.
    - Return true.
- Return false.

**Derived branch illustrations**

- At the comparison job\_card\_qty &gt; 0, job\_card\_qty = 1 selects the branch that returns true. With job\_card\_qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c1fdc1c8276bf3-guard-18)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L821)

<a id="op-cb57120f694880"></a>
### Work Order.on discard

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L3443) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L803)

<a id="op-2468cdc03226e2"></a>
### Work Order.before insert

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.enable\_reserve\_stock\_for\_produced\_serial\_no().

If control reaches the end, it returns no value.

**Methods declared on this owner** [enable reserve stock for produced serial no](operations-038.md#op-dd3f1cc95265de).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1043)

<a id="op-e396f168753df2"></a>
### Work Order.validate

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Local steps**

- Evaluate self.validate\_production\_item().
- If self.bom\_no.
  - Evaluate validate\_production\_bom(self.production\_item, self.bom\_no).
- If not self.subcontracting\_inward\_order.
  - Evaluate self.validate\_sales\_order().
- Evaluate self.set\_default\_warehouse().
- Evaluate self.set\_operation\_warehouses().
- Evaluate self.validate\_warehouse\_belongs\_to\_company().
- Evaluate self.check\_wip\_warehouse\_skip().
- Evaluate self.reset\_use\_multi\_level\_bom().
- Evaluate self.calculate\_operating\_cost().
- Evaluate self.validate\_qty().
- Evaluate self.validate\_transfer\_against().
- Evaluate self.validate\_operations().
- Set self.status from self.get\_status().
- Evaluate self.validate\_workstation\_type().
- Evaluate self.clear\_reserve\_stock\_if\_disabled().
- Evaluate self.set\_reserve\_stock().
- Evaluate self.validate\_fg\_warehouse\_for\_reservation().
- Evaluate self.validate\_dates().
- If self.source\_warehouse.
  - Evaluate self.set\_warehouses().
- Evaluate validate\_uom\_is\_integer(self, “stock\_uom”, list(“required\_qty”)).
- If (not len(self.get(“required\_items”)) or not Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_editing\_of\_items\_and\_quantities\_in\_work\_order”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not len(self.get(“required\_items”)) → not Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_editing\_of\_items\_and\_quantities\_in\_work\_order”).
  - Evaluate self.set\_required\_items(reset\_only\_qty = len(self.get(“required\_items”))).
- Otherwise.
  - Evaluate self.set\_rate\_for\_edited\_items().
- Evaluate self.set\_required\_item\_amounts().
- Evaluate self.enable\_auto\_reserve\_stock().
- Evaluate self.validate\_operations\_sequence().
- Evaluate self.validate\_subcontracting\_inward\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate production item](operations-041.md#op-4441dd77412c6a), [validate sales order](operations-038.md#op-4d9a1630532b95), [set default warehouse](operations-039.md#op-e49ccc119614ee), [set operation warehouses](operations-041.md#op-6a9e0641644e50), [validate warehouse belongs to company](operations-039.md#op-65bdd4766c556f), [check wip warehouse skip](operations-039.md#op-2f02b843bc3580), [reset use multi level bom](operations-038.md#op-f768488f837d69), [calculate operating cost](operations-039.md#op-730f15a256b6df), [validate qty](operations-041.md#op-3c8e7714ae4f37), [validate transfer against](operations-041.md#op-5ffcdd00c7a4a1), [validate operations](operations-041.md#op-f7179b450be773), [get status](operations-039.md#op-7a6d94ec35a98e), [validate workstation type](operations-038.md#op-65d00a00e7a7ec), [clear reserve stock if disabled](operations-038.md#op-37222e9a50f91a), [set reserve stock](operations-038.md#op-1a69974c1ccb1c), [validate fg warehouse for reservation](operations-038.md#op-c50c42ff9c3c6b), [validate dates](operations-038.md#op-20c9555a7422b0), [set warehouses](operations-038.md#op-75beb9350f1d45), [set required items](operations-041.md#op-2bf328b6767c61), [set rate for edited items](operations-041.md#op-df7e577faf3dc6), [set required item amounts](operations-041.md#op-6548508787acc9), [enable auto reserve stock](operations-038.md#op-9b9b79f49c4556), [validate operations sequence](operations-038.md#op-6ff86e51bbb960), [validate subcontracting inward order](operations-038.md#op-410f06f1054a78).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “allow\_editing\_of\_items\_and\_quantities\_in\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L838)

<a id="op-20c9555a7422b0"></a>
### Work Order.validate dates

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Planned End Date cannot be before Planned Start Date” · validation helper — translated “Actual End Date cannot be before Actual Start Date”.

**Local steps**

- If (self.planned\_start\_date and self.planned\_end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.planned\_start\_date → self.planned\_end\_date.
  - If get\_datetime(self.planned\_end\_date) &lt; get\_datetime(self.planned\_start\_date).
    - Call the validation error handler Platform.throw(translated “Planned End Date cannot be before Planned Start Date”).
- If (self.actual\_start\_date and self.actual\_end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.actual\_start\_date → self.actual\_end\_date.
  - If self.actual\_end\_date &lt; self.actual\_start\_date.
    - Call the validation error handler Platform.throw(translated “Actual End Date cannot be before Actual Start Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L4256) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L841)

<a id="op-c50c42ff9c3c6b"></a>
### Work Order.validate fg warehouse for reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_validate_fg_warehouse_for_reservation`

**Inputs** self.

**Record and data access** read “Sales Order Item” via get\_all.

**Explicit failure paths** validation helper — translated “Warehouse {0} is not allowed for Sales Order {1}, it should be {2}”.format(self.fg\_warehouse, self.sales\_order, warehouses at 0).

**Local steps**

- If (self.reserve\_stock and self.sales\_order and not self.subcontracting\_inward\_order and not self.production\_plan\_sub\_assembly\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reserve\_stock → self.sales\_order → not self.subcontracting\_inward\_order → not self.production\_plan\_sub\_assembly\_item.
  - Set warehouses from Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → self.sales\_order, “item\_code” → self.production\_item), pluck = “warehouse”).
  - If self.fg\_warehouse does not belong to warehouses.
    - Call the validation error handler Platform.throw(translated “Warehouse {0} is not allowed for Sales Order {1}, it should be {2}”.format(self.fg\_warehouse, self.sales\_order, warehouses at 0), title = translated “Target Warehouse Reservation Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1107)

<a id="op-dd3f1cc95265de"></a>
### Work Order.enable reserve stock for produced serial no

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_enable_reserve_stock_for_produced_serial_no`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Sales Order Item” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.reserve\_stock or not self.sales\_order\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.reserve\_stock → not self.sales\_order\_item.
  - Return no value.
- If not Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Return no value.
- If Platform.db.get\_value(“Sales Order Item”, self.sales\_order\_item, “ensure\_delivery\_based\_on\_produced\_serial\_no”).
  - Set self.reserve\_stock from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L41) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1051)

<a id="op-37222e9a50f91a"></a>
### Work Order.clear reserve stock if disabled

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_clear_reserve_stock_if_disabled`

**Inputs** self.

**Local steps**

- If not self.subcontracting\_inward\_order.
  - Evaluate clear\_reserve\_stock\_if\_disabled(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1047)

<a id="op-1a69974c1ccb1c"></a>
### Work Order.set reserve stock

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_reserve_stock`

**Inputs** self.

**Local steps**

- For each row in self.required\_items.
  - Set row.reserve\_stock from self.reserve\_stock.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1094)

<a id="op-9b9b79f49c4556"></a>
### Work Order.enable auto reserve stock

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_enable_auto_reserve_stock`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (self.is\_new() and Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).
  - Set self.reserve\_stock from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1050)

<a id="op-08092f57ccf828"></a>
### Work Order.before save

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_skip\_transfer\_for\_operations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set skip transfer for operations](operations-038.md#op-77313d24d12c42).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L4506) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L788)

<a id="op-77313d24d12c42"></a>
### Work Order.set skip transfer for operations

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_skip_transfer_for_operations`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.track\_semi\_finished\_goods.
  - Return no value.
- For each op in self.operations.
  - Set op.skip\_material\_transfer from self.skip\_transfer.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L4557) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L818)

<a id="op-6ff86e51bbb960"></a>
### Work Order.validate operations sequence

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_operations_sequence`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #1: Sequence ID must be 1 for Operation {0}.”.format(Platform.bold(op.operation)) · validation helper — translated “Row #{0}: Sequence ID must be {1} or {2} for Operation {3}.”.format(op.idx, Platform.bold(sequence\_id), Platform.bold((sequence\_id + 1)), Platform.bold(op.operation)).

**Local steps**

- If all(list of not op.sequence\_id for op drawn from self.operations).
  - Draw op from self.operations.
  - For each op in self.operations.
    - Set op.sequence\_id from op.idx.
- Otherwise.
  - Set sequence\_id from 1.
  - For each op in self.operations.
    - If (op.idx equals 1 and op.sequence\_id differs from 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in op.idx equals 1 → op.sequence\_id differs from 1.
      - Call the validation error handler Platform.throw(translated “Row #1: Sequence ID must be 1 for Operation {0}.”.format(Platform.bold(op.operation))).
    - Otherwise.
      - If (op.sequence\_id differs from sequence\_id and op.sequence\_id differs from (sequence\_id + 1)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in op.sequence\_id differs from sequence\_id → op.sequence\_id differs from (sequence\_id + 1).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Sequence ID must be {1} or {2} for Operation {3}.”.format(op.idx, Platform.bold(sequence\_id), Platform.bold((sequence\_id + 1)), Platform.bold(op.operation))).
    - Set sequence\_id from op.sequence\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L4651) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L843)

<a id="op-410f06f1054a78"></a>
### Work Order.validate subcontracting inward order

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_subcontracting_inward_order`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order” via get\_cached\_value · read “Subcontracting Inward Order Item” via get\_cached\_value · read “Subcontracting Inward Order Received Item” via get\_all · read “Warehouse” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Source Warehouse {0} must be same as Customer Warehouse {1} in the Subcontracting Inward Order.”.format(get\_link\_to\_form(“Warehouse”, self.source\_warehouse), get\_link\_to\_form(“Warehouse”, rm\_re … · validation helper — translated “Target Warehouse {0} must be same as Delivery Warehouse {1} in the Subcontracting Inward Order Item.”.format(get\_link\_to\_form(“Warehouse”, self.fg\_warehouse), get\_link\_to\_form(“Warehouse”, deli … · validation helper — translated “Row #{0}: Source Warehouse {1} for item {2} must be same as Source Warehouse {3} in the Work Order.”.format(item.idx, get\_link\_to\_form(“Warehouse”, item.source\_warehouse), get\_link\_to\_form(“Ite … · validation helper — translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Customer Provided Item {1} has insufficient quantity in the Subcontracting Inward Order. Available …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), Platform.bold(((row.re … · 2 additional forms in the steps below.

**Local steps**

- If scio bound to self.subcontracting\_inward\_order.
  - If self.source\_warehouse differs from rm\_receipt\_warehouse bound to Platform.get\_cached\_value(“Subcontracting Inward Order”, scio, “customer\_warehouse”).
    - Call the validation error handler Platform.throw(translated “Source Warehouse {0} must be same as Customer Warehouse {1} in the Subcontracting Inward Order.”.format(get\_link\_to\_form(“Warehouse”, self.source\_warehouse), get\_link\_to\_form(“Wa ….
  - If self.fg\_warehouse differs from delivery\_warehouse bound to Platform.get\_cached\_value(“Subcontracting Inward Order Item”, self.subcontracting\_inward\_order\_item, “delivery\_warehouse”).
    - Call the validation error handler Platform.throw(translated “Target Warehouse {0} must be same as Delivery Warehouse {1} in the Subcontracting Inward Order Item.”.format(get\_link\_to\_form(“Warehouse”, self.fg\_warehouse), get\_link\_to\_form(“W ….
  - Set possible\_customer\_provided\_items from Platform.get\_all(“Subcontracting Inward Order Received Item”, mapping(“reference\_name” → self.subcontracting\_inward\_order\_item, “is\_customer\_provided\_item” → 1, “docstatus” → 1), list(“rm\_item\_code”, “rece ….
  - Set item\_codes from list().
  - For each item in self.required\_items.
    - If item.is\_customer\_provided\_item.
      - If item.source\_warehouse differs from self.source\_warehouse.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Source Warehouse {1} for item {2} must be same as Source Warehouse {3} in the Work Order.”.format(item.idx, get\_link\_to\_form(“Warehouse”, item.source\_warehouse), get\_li ….
      - Otherwise.
        - If item.item\_code belongs to item\_codes.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
        - Otherwise.
          - Set row from next(generator of i for i drawn from possible\_customer\_provided\_items where i.rm\_item\_code equals item.item\_code, no value).
            - Draw i from possible\_customer\_provided\_items, keep a combination only if (i.rm\_item\_code equals item.item\_code).
          - If row.
            - If item.required\_qty &gt; ((row.received\_qty − row.returned\_qty) − row.work\_order\_qty).
              - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} has insufficient quantity in the Subcontracting Inward Order. Available …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), Platfor ….
            - Otherwise.
              - Evaluate item\_codes.append(item.item\_code).
          - Otherwise.
            - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} does not exist in the Required Items table linked to the Subcontracting …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
    - Otherwise.
      - If Platform.get\_cached\_value(“Warehouse”, item.source\_warehouse, “customer”).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Source Warehouse {1} for item {2} cannot be a customer warehouse.”.format(item.idx, get\_link\_to\_form(“Warehouse”, item.source\_warehouse), get\_link\_to\_form(“Item”, item. ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order”, scio, “customer\_warehouse”), Platform.get\_cached\_value(“Subcontracting Inward Order Item”, self.subcontracting\_inward\_order\_item, “delivery\_warehouse”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0532.json#L5152) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L847)

<a id="op-75beb9350f1d45"></a>
### Work Order.set warehouses

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_warehouses`

**Inputs** self.

**Local steps**

- For each row in self.required\_items.
  - If not row.source\_warehouse.
    - Set row.source\_warehouse from self.source\_warehouse.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L819)

<a id="op-f768488f837d69"></a>
### Work Order.reset use multi level bom

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_reset_use_multi_level_bill_of_materials`

**Inputs** self.

**Local steps**

- Set previous from no value when self.is\_new(), otherwise self.get\_doc\_before\_save().
  - Value choice on self.is\_new() — true gives no value, false gives self.get\_doc\_before\_save().
- Evaluate self.sync\_operations\_with\_bom(previous).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync operations with bom](operations-038.md#op-74e35506585355).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L808)

<a id="op-74e35506585355"></a>
### Work Order.sync operations with bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_sync_operations_with_bom`

**Inputs** self, previous.

**Explicit results** no value.

**Local steps**

- If previous is identical to no value.
  - Return no value.
- If (previous.bom\_no differs from self.bom\_no or previous.use\_multi\_level\_bom differs from self.use\_multi\_level\_bom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous.bom\_no differs from self.bom\_no → previous.use\_multi\_level\_bom differs from self.use\_multi\_level\_bom.
  - Evaluate self.get\_items\_and\_operations\_from\_bom().
- Otherwise.
  - If (flt(previous.qty) differs from flt(self.qty) and flt(previous.qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(previous.qty) differs from flt(self.qty) → flt(previous.qty).
    - Evaluate self.scale\_saved\_operation\_time(previous).
    - Evaluate self.scale\_saved\_output\_qty(previous).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get items and operations from bom](operations-041.md#op-269f4b3689a606), [scale saved operation time](operations-038.md#op-aa88181f5953a0), [scale saved output qty](operations-038.md#op-ad079404886ba6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1099)

<a id="op-ad079404886ba6"></a>
### Work Order.scale saved output qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_scale_saved_output_qty`

**Inputs** self, previous.

**Local steps**

- Set saved\_rows from mapping of row.name → row for row drawn from previous.get(“operations”).
  - Draw row from previous.get(“operations”).
- For each d in self.get(“operations”).
  - Set saved from saved\_rows.get(d.name).
  - If (saved and flt(saved.output\_qty) and flt(saved.output\_qty) equals flt(d.output\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in saved → flt(saved.output\_qty) → flt(saved.output\_qty) equals flt(d.output\_qty).
    - Set output\_qty from ((flt(saved.output\_qty) × flt(self.qty)) ÷ flt(previous.qty)).
    - Set d.output\_qty from flt(output\_qty, d.precision(“output\_qty”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1088)

<a id="op-aa88181f5953a0"></a>
### Work Order.scale saved operation time

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_scale_saved_operation_time`

**Inputs** self, previous.

**Local steps**

- Set saved\_rows from mapping of row.name → row for row drawn from previous.get(“operations”).
  - Draw row from previous.get(“operations”).
- Set fixed\_flags from self.get\_fixed\_time\_flags().
- Set occurrence from mapping().
- For each d in self.get(“operations”).
  - Set key from tuple((d.bom or self.bom\_no), d.operation).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.bom → self.bom\_no.
  - Set idx, occurrence at key from (occurrence.get(key, negative 1) + 1).
  - Set flags from fixed\_flags.get(key, list()).
  - Set is\_fixed from flags at (idx modulo or format len(flags)) when flags, otherwise false.
    - Value choice on flags — true gives flags at (idx modulo or format len(flags)), false gives false.
  - Set saved from saved\_rows.get(d.name).
  - If (not saved or is\_fixed or flt(saved.time\_in\_mins) differs from flt(d.time\_in\_mins)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not saved → is\_fixed → flt(saved.time\_in\_mins) differs from flt(d.time\_in\_mins).
    - Continue with the next iteration or loop test.
  - Set d.time\_in\_mins from ((flt(saved.time\_in\_mins) × flt(self.qty)) ÷ flt(previous.qty)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get fixed time flags](operations-038.md#op-ca26390c5e02f6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1087)

<a id="op-ca26390c5e02f6"></a>
### Work Order.get fixed time flags

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_fixed_time_flags`

**Inputs** self.

**Record and data access** read “BOM Operation” via get\_all.

**Explicit results** flags.

**Local steps**

- Set boms from set of (d.bom or self.bom\_no) for d drawn from self.get(“operations”).
  - Draw d from self.get(“operations”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.bom → self.bom\_no.
- Set flags from mapping().
- For each row in Platform.get\_all(“BOM Operation”, filters = mapping(“parent” → list(“in”, list(boms)), “parenttype” → “BOM”), fields = list(“parent”, “operation”, “fixed\_time”), order\_by = “idx”).
  - Evaluate flags.setdefault(tuple(row.parent, row.operation), list()).append(cint(row.fixed\_time)).
- Return flags.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1060)

<a id="op-65d00a00e7a7ec"></a>
### Work Order.validate workstation type

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_workstation_type`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Workstation or Workstation Type is mandatory for an operation {1}”.format(row.idx, row.operation).

**Local steps**

- If not self.docstatus.is\_submitted().
  - Return no value.
- For each row in self.operations.
  - If (not row.workstation and not row.workstation\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.workstation → not row.workstation\_type.
    - Call the validation error handler Platform.throw(translated “Row {0}: Workstation or Workstation Type is mandatory for an operation {1}”.format(row.idx, row.operation)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L227) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L852)

<a id="op-4d9a1630532b95"></a>
### Work Order.validate sales order

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_sales_order`

**Inputs** self.

**Record and data access** read “Material Request Item” via get\_value · read “Material Request Plan Item” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Sales Order {0} is not valid”.format(self.sales\_order).

**Local steps**

- If self.production\_plan\_sub\_assembly\_item.
  - Return no value.
- Set production\_item from self.production\_item.
- If (self.material\_request\_item and mr\_plan\_item bound to Platform.get\_value(“Material Request Item”, self.material\_request\_item, “material\_request\_plan\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.material\_request\_item → mr\_plan\_item bound to Platform.get\_value(“Material Request Item”, self.material\_request\_item, “material\_request\_plan\_item”).
  - If main\_item\_code bound to Platform.get\_value(“Material Request Plan Item”, mr\_plan\_item, “main\_item\_code”).
    - Set production\_item from main\_item\_code.
- If self.sales\_order.
  - Evaluate check\_on\_hold\_or\_closed\_status(“Sales Order”, self.sales\_order).
  - Set SalesOrder from Platform.qb.DocType(“Sales Order”).
  - Set SalesOrderItem from Platform.qb.DocType(“Sales Order Item”).
  - Set PackedItem from Platform.qb.DocType(“Packed Item”).
  - Set ProductBundleItem from Platform.qb.DocType(“Product Bundle Item”).
  - Set so\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.item\_code).select(SalesOrder.name, SalesOrder.project, SalesOrd ….
  - If self.sales\_order\_item.
    - Set so\_query from so\_query.where(SalesOrderItem.name equals self.sales\_order\_item).
  - Set so from so\_query.run(as\_dict = 1).
  - If not so.
    - Set packed\_so\_query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
    - If self.sales\_order\_item.
      - Set packed\_so\_query from packed\_so\_query.where((PackedItem.name equals self.sales\_order\_item bitwise or SalesOrderItem.name equals self.sales\_order\_item)).
    - Set so from packed\_so\_query.run(as\_dict = 1).
  - If len(so).
    - If not self.expected\_delivery\_date.
      - Set self.expected\_delivery\_date from so at 0.delivery\_date.
    - If so at 0.project.
      - Set self.project from so at 0.project.
    - If not self.material\_request.
      - Evaluate self.validate\_work\_order\_against\_so().
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Sales Order {0} is not valid”.format(self.sales\_order)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate work order against so](operations-039.md#op-736bd65327b36c).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L846)
