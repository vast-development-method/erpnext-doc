# Production · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-44076aaa39692f"></a>
### Get operation qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_operation_qty`

**Inputs** work\_order, operation.

**Explicit results** flt(operation.get(“output\_qty”)) · flt(work\_order.get(“qty”)).

**Local steps**

- If (work\_order.get(“track\_semi\_finished\_goods”) and flt(operation.get(“output\_qty”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.get(“track\_semi\_finished\_goods”) → flt(operation.get(“output\_qty”)).
  - Return flt(operation.get(“output\_qty”)).
- Return flt(work\_order.get(“qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1006)

<a id="op-b6a035b39928c1"></a>
### Get upstream process loss

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_upstream_process_loss`

**Inputs** work\_order, operation = no value.

**Explicit results** 0 · flt(process\_loss\_qty).

**Local steps**

- If work\_order.get(“track\_semi\_finished\_goods”).
  - Return 0.
- Set process\_loss\_qty from 0.
- Set available\_qty from no value.
- For each tuple(sequence\_id, rows) in groupby(sorted((work\_order.get(“operations”) or list()), key = deferred anonymous expression), key = deferred anonymous expression).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_order.get(“operations”) → list().
  - If (operation is distinct from no value and sequence\_id ≥ cint(operation.get(“sequence\_id”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in operation is distinct from no value → sequence\_id ≥ cint(operation.get(“sequence\_id”)).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set rows from list(rows).
  - Update process\_loss\_qty using + max(generator of flt(row.process\_loss\_qty) when available\_qty is identical to no value, otherwise min(flt(row.process\_loss\_qty), max((available\_qty − nested operand in the contract(nested operand in the contra …).
    - Draw row from rows.
    - Value choice on available\_qty is identical to no value — true gives flt(row.process\_loss\_qty), false gives min(flt(row.process\_loss\_qty), max((available\_qty − flt(row.completed\_qty)), 0)).
  - Set available\_qty from min(generator of flt(row.completed\_qty) for row drawn from rows).
    - Draw row from rows.
- Return flt(process\_loss\_qty).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L6) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1016)

<a id="op-55d7e1cb5918f2"></a>
### Get operation target qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_operation_target_qty`

**Inputs** work\_order, operation.

**Explicit results** flt((get\_operation\_qty(work\_order, operation) − get\_upstream\_process\_loss(work\_order, operation)), operation.precision(“completed\_qty”)).

**Local steps**

- Return flt((get\_operation\_qty(work\_order, operation) − get\_upstream\_process\_loss(work\_order, operation)), operation.precision(“completed\_qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1007)

<a id="op-4bcc11456b6b38"></a>
### Split qty based on batch size

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_split_qty_based_on_batch_size`

**Inputs** wo\_doc, row, qty.

**Record and data access** read “Operation” via get\_value.

**Explicit results** qty.

**Local steps**

- If not cint(Platform.db.get\_value(“Operation”, row.operation, “create\_job\_card\_based\_on\_batch\_size”)).
  - Set row.batch\_size from (row.get(“qty”) or get\_operation\_qty(wo\_doc, row)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“qty”) → get\_operation\_qty(wo\_doc, row).
- Set row.job\_card\_qty from row.batch\_size.
- If (row.batch\_size and qty ≥ row.batch\_size).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_size → qty ≥ row.batch\_size.
  - Update qty using − row.batch\_size.
- Otherwise.
  - If qty &gt; 0.
    - Set row.job\_card\_qty from qty.
    - Set qty from 0.
- Evaluate get\_serial\_nos\_for\_job\_card(row, wo\_doc).
- Return qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1036)

<a id="op-ffe53c49291f2e"></a>
### Get serial nos for job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_serial_nos_for_job_card`

**Inputs** row, wo\_doc.

**Record and data access** read “Job Card” via get\_all.

**Explicit results** no value.

**Local steps**

- If not wo\_doc.has\_serial\_no.
  - Return no value.
- Set serial\_nos from get\_serial\_nos\_for\_work\_order(wo\_doc.name, wo\_doc.production\_item).
- Set used\_serial\_nos from list().
- For each d in Platform.get\_all(“Job Card”, fields = list(“serial\_no”), filters = mapping(“docstatus” → tuple(“&lt;”, 2), “work\_order” → wo\_doc.name, “operation\_id” → row.name)).
  - Evaluate used\_serial\_nos.extend(get\_serial\_nos(d.serial\_no)).
- Set serial\_nos from sorted(list((set(serial\_nos) − set(used\_serial\_nos)))).
- Set row.serial\_no from whitespace '\\n'.join(serial\_nos at slice 0 to cint(row.job\_card\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L2) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1012)

<a id="op-78a4021992f9c8"></a>
### Get serial nos for work order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_serial_nos_for_work_order`

**Inputs** work\_order, production\_item.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from list().
- For each d in Platform.get\_all(“Serial No”, fields = list(“name”), filters = mapping(“work\_order” → work\_order, “item\_code” → production\_item)).
  - Evaluate serial\_nos.append(d.name).
- Return serial\_nos.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L3) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1013)

<a id="op-4810b957538530"></a>
### Validate operation data

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_validate_operation_data`

**Inputs** row.

**Explicit failure paths** validation helper — translated “Quantity to Manufacture can not be zero for the operation {0}”.format(Platform.bold(row.get(“operation”))) · validation helper — translated “For operation {0}: Quantity ({1}) can not be greater than pending quantity({2})”.format(Platform.bold(row.get(“operation”)), Platform.bold(row.get(“qty”)), Platform.bold(row.get(“pending\_qty”))).

**Local steps**

- If flt(row.get(“qty”)) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Quantity to Manufacture can not be zero for the operation {0}”.format(Platform.bold(row.get(“operation”)))).
- If flt(row.get(“qty”)) &gt; flt(row.get(“pending\_qty”)).
  - Call the validation error handler Platform.throw(translated “For operation {0}: Quantity ({1}) can not be greater than pending quantity({2})”.format(Platform.bold(row.get(“operation”)), Platform.bold(row.get(“qty”)), Platform.bold(row.get( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L29) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1039)

<a id="op-de13b9f2a03a71"></a>
### Create job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_create_job_card`

**Inputs** work\_order, row, enable\_capacity\_planning = false, auto\_create = false.

**State and service calls** request new\_doc for “Job Card” · call insert on doc · msgprint with translated “Job card {0} created”.format(get\_link\_to\_form(“Job Card”, doc.name)) · call db\_set on doc.

**Explicit results** doc.

**Local steps**

- Set doc from Platform.new\_doc(“Job Card”).
- Set qty from (row.job\_card\_qty or work\_order.get(“qty”, 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.job\_card\_qty → work\_order.get(“qty”, 0).
- Evaluate doc.update(mapping(“work\_order” → work\_order.name, “workstation\_type” → row.get(“workstation\_type”), “operation” → row.get(“operation”), “workstation” → row.get(“workstation”), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“source\_warehouse”) → work\_order.get(“source\_warehouse”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“fg\_warehouse”) → work\_order.get(“fg\_warehouse”).
  - Value choice on (not work\_order.skip\_transfer or work\_order.from\_wip\_warehouse) — true gives (work\_order.wip\_warehouse or row.get(“wip\_warehouse”)), false gives (work\_order.source\_warehouse or row.get(“source\_warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not work\_order.skip\_transfer → work\_order.from\_wip\_warehouse.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_order.wip\_warehouse → row.get(“wip\_warehouse”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_order.source\_warehouse → row.get(“source\_warehouse”).
- If (work\_order.track\_semi\_finished\_goods or (work\_order.transfer\_material\_against equals “Job Card” and not work\_order.skip\_transfer)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_order.track\_semi\_finished\_goods → (work\_order.transfer\_material\_against equals “Job Card” and not work\_order.skip\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.transfer\_material\_against equals “Job Card” → not work\_order.skip\_transfer.
  - Evaluate doc.get\_required\_items().
- If work\_order.track\_semi\_finished\_goods.
  - Evaluate doc.set\_secondary\_items().
- If auto\_create.
  - Set doc.flags.ignore\_mandatory from true.
  - If enable\_capacity\_planning.
    - Evaluate doc.schedule\_time\_logs(row).
  - Evaluate doc.insert().
  - Evaluate Platform.msgprint(translated “Job card {0} created”.format(get\_link\_to\_form(“Job Card”, doc.name)), alert = true).
- If enable\_capacity\_planning.
  - Evaluate doc.db\_set(“status”, “Open”).
- Return doc.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L994)

<a id="op-556a2b25603e31"></a>
### Get work order operation data

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_work_order_operation_data`

**Inputs** work\_order, operation, workstation.

**Explicit results** d.

**Local steps**

- For each d in work\_order.operations.
  - If (d.operation equals operation and d.workstation equals workstation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.operation equals operation → d.workstation equals workstation.
    - Return d.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1018)

<a id="op-c5c649802311b6"></a>
### Create pick list

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_create_pick_list`

**Inputs** source\_name, target\_doc = no value, for\_qty = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** doc.

**Local steps**

- If for\_qty is identical to no value.
  - Set for\_qty from Platform.parse\_json((target\_doc or “{}”)).get(“for\_qty”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_doc → “{}”.
- Set for\_qty from \_validated\_for\_qty(for\_qty).
- Set work\_order from Platform.get\_doc(“Work Order”, source\_name).
- Set allocation from \_allocate\_material\_demand(work\_order, (for\_qty ÷ flt(work\_order.qty))).
- Set postprocess from partial(\_set\_pick\_list\_item\_qty, allocation\_by\_item = allocation).
- Set doc from get\_mapped\_doc(“Work Order”, source\_name, \_pick\_list\_mapping(postprocess, allocation), target\_doc).
- Evaluate \_validate\_material\_is\_pending(doc.locations).
- Set doc.purpose from “Material Transfer for Manufacture”.
- Set doc.for\_qty from for\_qty.
- If not doc.pick\_manually.
  - Evaluate doc.set\_item\_locations().
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L995)

<a id="op-6e7309c8c5718c"></a>
### Pick list mapping

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_pick_list_mapping`

**Inputs** postprocess, allocation.

**Explicit results** mapping(“Work Order” → mapping(“doctype” → “Pick List”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Work Order Item” → mapping(“doctype” → “Pick List Item”, “field\_no\_map” → list(“transferred\_qty ….

**Local steps**

- Return mapping(“Work Order” → mapping(“doctype” → “Pick List”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Work Order Item” → mapping(“doctype” → “Pick List Item”, “field\_no\_map” → list(“transferred\_qty ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L19) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1029)

<a id="op-f65d811dd8e77b"></a>
### Allocate material demand

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_allocate_material_demand`

**Inputs** work\_order, fraction.

**Explicit results** allocation.

**Local steps**

- Set required\_by\_item from mapping().
- Set covered\_by\_item from mapping().
- Set required\_by\_group from mapping().
- Set uom\_by\_item from mapping().
- For each row in work\_order.required\_items.
  - Set required\_by\_item at row.item\_code from (required\_by\_item.get(row.item\_code, 0.0) + flt(row.required\_qty)).
  - Evaluate uom\_by\_item.setdefault(row.item\_code, row.stock\_uom).
  - Evaluate covered\_by\_item.setdefault(row.item\_code, (flt(row.requested\_qty) + flt(row.picked\_qty))).
  - Update covered\_by\_item at row.item\_code using + flt(row.transferred\_qty).
  - Set key from \_allocation\_key(row).
  - Set required\_by\_group at key from (required\_by\_group.get(key, 0.0) + flt(row.required\_qty)).
- Set precision from Platform.get\_precision(“Work Order Item”, “required\_qty”).
- Set pending\_pool from mapping of item\_code → flt((required\_qty − covered\_by\_item at item\_code), precision) for tuple(item\_code, required\_qty) drawn from required\_by\_item.items().
  - Draw tuple(item\_code, required\_qty) from required\_by\_item.items().
- Set remaining\_by\_item from mapping of item\_code → min(\_round\_demand((required\_qty × fraction), uom\_by\_item at item\_code, precision), pending\_pool at item\_code) for tuple(item\_code, required\_qty) drawn from required\_by\_item.items().
  - Draw tuple(item\_code, required\_qty) from required\_by\_item.items().
- Set allocation from mapping().
- For each tuple(key, required\_qty) in required\_by\_group.items().
  - Set item\_code from key at 0.
  - If required\_by\_item at item\_code ≤ 0.
    - Continue with the next iteration or loop test.
  - Set pool\_share from ((pending\_pool at item\_code × required\_qty) ÷ required\_by\_item at item\_code).
  - Set qty from \_round\_demand(min((required\_qty × fraction), pool\_share), uom\_by\_item at item\_code, precision).
  - Set qty from min(qty, remaining\_by\_item at item\_code).
  - If qty &gt; 0.
    - Set allocation at key from qty.
    - Update remaining\_by\_item at item\_code using − qty.
- Return allocation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L990)

<a id="op-633945a2f62d5b"></a>
### Round demand

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_round_demand`

**Inputs** qty, stock\_uom, precision.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** math.ceil(flt(qty, 9)) · flt(qty, precision).

**Local steps**

- If cint(Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”)).
  - Return math.ceil(flt(qty, 9)).
- Return flt(qty, precision).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L22) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1032)

<a id="op-f03bfc96922690"></a>
### Allocation key

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_allocation_key`

**Inputs** row.

**Explicit results** tuple(row.item\_code, row.source\_warehouse, (cint(row.operation\_row\_id) or row.operation)).

**Local steps**

- Return tuple(row.item\_code, row.source\_warehouse, (cint(row.operation\_row\_id) or row.operation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(row.operation\_row\_id) → row.operation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L991)

<a id="op-c5df27d540f7cc"></a>
### Merge allocation per item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_merge_allocation_per_item`

**Inputs** allocation.

**Explicit results** merged.

**Local steps**

- Set merged from mapping().
- Set key\_by\_item from mapping().
- For each tuple(key, qty) in allocation.items().
  - Set item\_code from key at 0.
  - If item\_code belongs to key\_by\_item.
    - Update merged at key\_by\_item at item\_code using + qty.
  - Otherwise.
    - Set key\_by\_item at item\_code from key.
    - Set merged at key from qty.
- Return merged.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L18) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1028)

<a id="op-f6f19e19253cd1"></a>
### Validated for qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_validated_for_qty`

**Inputs** for\_qty.

**Explicit results** qty.

**Explicit failure paths** validation helper — translated “Quantity must be greater than zero.”.

**Local steps**

- Set qty from flt(for\_qty).
- If (not math.isfinite(qty) or qty ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not math.isfinite(qty) → qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Quantity must be greater than zero.”).
- Return qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L31) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1041)

<a id="op-06b75664cfec43"></a>
### Validate material is pending

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_validate_material_is_pending`

**Inputs** rows.

**Explicit failure paths** validation helper — translated “All required items have already been transferred, requested or picked.”.

**Local steps**

- If not rows.
  - Call the validation error handler Platform.throw(translated “All required items have already been transferred, requested or picked.”, title = translated “No Pending Materials”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L28) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1038)

<a id="op-8fde251666c98d"></a>
### Set pick list item qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_set_pick_list_item_qty`

**Inputs** source, target, source\_parent, allocation\_by\_item.

**Record and data access** read “Item” via get\_value.

**Explicit results** no value.

**Local steps**

- Set qty from allocation\_by\_item.pop(\_allocation\_key(source), 0.0).
- If qty ≤ 0.
  - Evaluate target.delete().
  - Return no value.
- Set target.qty from qty.
- Set target.stock\_qty from qty.
- Set target.uom from Platform.get\_value(“Item”, source.item\_code, “stock\_uom”).
- Set target.stock\_uom from target.uom.
- Set target.conversion\_factor from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1034)

<a id="op-960107cb886b88"></a>
### Get reserved qty for production

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_reserved_qty_for_production`

**Inputs** item\_code, warehouse, non\_completed\_production\_plans = no value, check\_production\_plan = false.

**Declared result** float.

**Explicit results** (query.run() at 0 at 0 or 0.0).

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set wo\_item from Platform.qb.DocType(“Work Order Item”).
- If check\_production\_plan.
  - Set qty\_field from wo\_item.required\_qty.
- Otherwise.
  - Set qty\_field from Case().
  - Set qty\_field from qty\_field.when((wo.skip\_transfer equals 0 bitwise and wo\_item.transferred\_qty &gt; wo\_item.required\_qty), 0.0).
  - Set qty\_field from qty\_field.when(wo.skip\_transfer equals 0, (wo\_item.required\_qty − wo\_item.transferred\_qty)).
  - Set qty\_field from qty\_field.when(wo\_item.consumed\_qty &gt; wo\_item.required\_qty, 0.0).
  - Set qty\_field from qty\_field.else\_((wo\_item.required\_qty − wo\_item.consumed\_qty)).
  - Set not\_subcontracted from (wo\_item.required\_qty − wo\_item.subcontracted\_qty).
  - Set qty\_field from nested operand in the contract().when(not\_subcontracted ≤ 0, 0.0).when(not\_subcontracted &lt; qty\_field, not\_subcontracted).else\_(qty\_field).
- Set query from nested operand in the contract(nested operand in the contract).from\_(wo\_item).select(Sum(qty\_field)).where((((wo\_item.item\_code equals item\_code bitwise and wo\_item.parent equals wo.name) bitwise and wo.do ….
- If check\_production\_plan.
  - Set query from query.where(wo.production\_plan.isnotnull()).
- Otherwise.
  - Set query from query.where(((wo.status.notin(list(“Stopped”, “Completed”, “Closed”)) bitwise and (wo\_item.required\_qty &gt; wo\_item.transferred\_qty bitwise or wo\_item.required\_qty &gt; wo\_item.consumed\_qty)) bitwise and Exists ….
- If non\_completed\_production\_plans.
  - Set query from query.where(wo.production\_plan.isin(non\_completed\_production\_plans)).
- Return (query.run() at 0 at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1010)

<a id="op-fc25f0248e1618"></a>
### Earlier operation making item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_earlier_operation_making_item`

**Inputs** wo, wo\_item.

**Explicit results** nested operand in the contract.qb.from\_(operation).select(operation.name).where(((operation.parent equals wo.name bitwise and operation.finished\_good equals wo\_item.item\_code) bitwise and operation.idx &lt; w ….

**Local steps**

- Set operation from Platform.qb.DocType(“Work Order Operation”).
- Return nested operand in the contract.qb.from\_(operation).select(operation.name).where(((operation.parent equals wo.name bitwise and operation.finished\_good equals wo\_item.item\_code) bitwise and operation.idx &lt; w ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L998)

<a id="op-b40240bf6c1067"></a>
### Make material request

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_material_request`

**Inputs** source\_name, target\_doc = no value, for\_qty = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Buying Settings” via get\_single\_value.

**Explicit results** doc.

**Local steps**

- Evaluate Platform.has\_permission(“Material Request”, “create”, throw = true).
- If (for\_qty is identical to no value and Platform.flags.args).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_qty is identical to no value → Platform.flags.args.
  - Set for\_qty from Platform.flags.args.for\_qty.
- Set work\_order from Platform.get\_doc(“Work Order”, source\_name).
- Set fraction from 1.0.
- If for\_qty is distinct from no value.
  - Set fraction from (\_validated\_for\_qty(for\_qty) ÷ flt(work\_order.qty)).
- Set allocation from \_allocate\_material\_demand(work\_order, fraction).
- If not cint(Platform.db.get\_single\_value(“Buying Settings”, “allow\_multiple\_items”)).
  - Set allocation from \_merge\_allocation\_per\_item(allocation).
- Set postprocess from partial(\_set\_material\_request\_item, allocation\_by\_item = allocation).
- Set doc from get\_mapped\_doc(“Work Order”, source\_name, \_material\_request\_mapping(postprocess, allocation), target\_doc).
- Evaluate \_validate\_material\_is\_pending(doc.items).
- Set doc.material\_request\_type from “Material Transfer”.
- Return doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Material Request”, “create”, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “allow\_multiple\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1022)

<a id="op-adc2ff9cc6467d"></a>
### Material request mapping

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_material_request_mapping`

**Inputs** postprocess, allocation.

**Explicit results** mapping(“Work Order” → mapping(“doctype” → “Material Request”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping(“name” → “work\_order”)), “Work Order Item” → mapping(“doctype” → “Ma ….

**Local steps**

- Return mapping(“Work Order” → mapping(“doctype” → “Material Request”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping(“name” → “work\_order”)), “Work Order Item” → mapping(“doctype” → “Ma ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L17) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1027)

<a id="op-8e655317640984"></a>
### Set material request item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_set_material_request_item`

**Inputs** source, target, source\_parent, allocation\_by\_item.

**Explicit results** no value.

**Local steps**

- Set qty from allocation\_by\_item.pop(\_allocation\_key(source), 0.0).
- If qty ≤ 0.
  - Evaluate target.delete().
  - Return no value.
- Set target.warehouse from source\_parent.wip\_warehouse.
- Set target.qty from qty.
- Set target.schedule\_date from nowdate().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L23) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1033)

<a id="op-043fa2e17858af"></a>
### Make stock return entry

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_stock_return_entry`

**Inputs** work\_order.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** request new\_doc for “Stock Entry”.

**Explicit results** no value · stock\_entry.

**Local steps**

- Bind dependencies get\_available\_materials.
- Set wo\_doc from Platform.get\_doc(“Work Order”, work\_order, check\_permission = “read”).
- Set non\_consumed\_items from get\_available\_materials(work\_order).
- If not non\_consumed\_items.
  - Return no value.
- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- Set stock\_entry.from\_bom from 1.
- Set stock\_entry.is\_return from 1.
- Set stock\_entry.work\_order from work\_order.
- Set stock\_entry.company from wo\_doc.company.
- Set stock\_entry.purpose from “Material Transfer for Manufacture”.
- Set stock\_entry.bom\_no from wo\_doc.bom\_no.
- Evaluate stock\_entry.add\_transfered\_raw\_materials\_in\_items().
- Evaluate stock\_entry.set\_stock\_entry\_type().
- Return stock\_entry.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L15) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1025)
