# Production · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-792e713c5be460"></a>
### Operation Plan.validate previous output

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_validate_previous_output`

**Inputs** self, row, operation\_ids, label.

**Explicit failure paths** validation helper — translated “{0}: an operation output can be used only when each operation produces an item.”.format(label) · validation helper — translated “{0}: choose an earlier operation of this BOM.”.format(label) · validation helper — translated “{0}: an operation can use only the output of an earlier operation.”.format(label).

**Local steps**

- If not self.produces\_item\_at\_each\_operation.
  - Call the validation error handler Platform.throw(translated “{0}: an operation output can be used only when each operation produces an item.”.format(label)).
- If (cint(row.from\_operation\_id) does not belong to operation\_ids or not row.operation\_id).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(row.from\_operation\_id) does not belong to operation\_ids → not row.operation\_id.
  - Call the validation error handler Platform.throw(translated “{0}: choose an earlier operation of this BOM.”.format(label)).
- If operation\_ids.index(cint(row.from\_operation\_id)) ≥ operation\_ids.index(cint(row.operation\_id)).
  - Call the validation error handler Platform.throw(translated “{0}: an operation can use only the output of an earlier operation.”.format(label)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L774)

<a id="op-b266bc3436f487"></a>
### Operation Plan.validate node

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_validate_node`

**Inputs** self, node\_id, label.

**Explicit failure paths** validation helper — translated “{0}: design part node {1} does not exist.”.format(label, node\_id).

**Local steps**

- If (cint(node\_id) and cint(node\_id) does not belong to self.parts).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(node\_id) → cint(node\_id) does not belong to self.parts.
  - Call the validation error handler Platform.throw(translated “{0}: design part node {1} does not exist.”.format(label, node\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L772)

<a id="op-74ba0ece864194"></a>
### Operation Plan.get output item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_output_item`

**Inputs** self, row, is\_last.

**Declared result** (str bitwise or no value).

**Explicit results** self.get\_node\_item(row.bom\_node\_id) · self.get\_node\_item(row.output\_node\_id) when row.output\_node\_id, otherwise row.output\_item.

**Local steps**

- If is\_last.
  - Return self.get\_node\_item(row.bom\_node\_id).
- Return self.get\_node\_item(row.output\_node\_id) when row.output\_node\_id, otherwise row.output\_item.
  - Value choice on row.output\_node\_id — true gives self.get\_node\_item(row.output\_node\_id), false gives row.output\_item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L760)

<a id="op-8093c475249143"></a>
### Operation Plan.get material item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_material_item`

**Inputs** self, row.

**Declared result** (str bitwise or no value).

**Explicit results** self.get\_node\_item(row.part\_node\_id) · self.get\_output\_item(source, source is identical to operations at negative 1) when source, otherwise no value · row.item\_code.

**Local steps**

- If row.part\_node\_id.
  - Return self.get\_node\_item(row.part\_node\_id).
- If row.from\_operation\_id.
  - Set operations from self.operations at cint(row.bom\_node\_id).
  - Set source from next(generator of op for op drawn from operations where cint(op.operation\_id) equals cint(row.from\_operation\_id), no value).
    - Draw op from operations, keep a combination only if (cint(op.operation\_id) equals cint(row.from\_operation\_id)).
  - Return self.get\_output\_item(source, source is identical to operations at negative 1) when source, otherwise no value.
    - Value choice on source — true gives self.get\_output\_item(source, source is identical to operations at negative 1), false gives no value.
- Return row.item\_code.

**Methods declared on this owner** [get output item](operations-012.md#op-74ba0ece864194).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L758)

<a id="op-5475ddea4e35b6"></a>
### Operation Plan.get bom name

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_name`

**Inputs** self, node\_id.

**Declared result** str.

**Explicit results** self.design.design\_name · (self.parts at node\_id.part\_name or self.parts at node\_id.part\_number).

**Local steps**

- If not node\_id.
  - Return self.design.design\_name.
- Return (self.parts at node\_id.part\_name or self.parts at node\_id.part\_number).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.parts at node\_id.part\_name → self.parts at node\_id.part\_number.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L749)

<a id="op-2ca6b416b3dd31"></a>
### Operation Plan.get problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_problems`

**Inputs** self.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set problems from list().
- For each node\_id in self.bom\_node\_ids.
  - Evaluate problems.extend(self.get\_bom\_problems(node\_id)).
- Evaluate problems.extend(self.get\_duplicate\_problems()).
- Return problems.

**Methods declared on this owner** [get bom problems](operations-012.md#op-fa9cfd3156a37d), [get duplicate problems](operations-012.md#op-a47b4cd985ebcc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L761)

<a id="op-a47b4cd985ebcc"></a>
### Operation Plan.get duplicate problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_duplicate_problems`

**Inputs** self.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set tuple(problems, nodes) from tuple(list(), mapping()).
- For each node\_id in self.bom\_node\_ids.
  - Set item\_code from self.get\_node\_item(node\_id).
  - Set other from nodes.setdefault(item\_code, node\_id) when item\_code, otherwise node\_id.
    - Value choice on item\_code — true gives nodes.setdefault(item\_code, node\_id), false gives node\_id.
  - If other differs from node\_id.
    - Evaluate problems.append(translated “{0} and {1} are mapped to item {2}. Only one BOM can be made for an item.”.format(bold(self.get\_bom\_name(other)), bold(self.get\_bom\_name(node\_id)), bold(item\_code))).
- Return problems.

**Methods declared on this owner** [get bom name](operations-012.md#op-5475ddea4e35b6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L755)

<a id="op-fa9cfd3156a37d"></a>
### Operation Plan.get bom problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_problems`

**Inputs** self, node\_id.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set name from bold(self.get\_bom\_name(node\_id)).
- Set operations from self.operations at node\_id.
- Set problems from list().
- If not self.get\_node\_item(node\_id).
  - Evaluate problems.append(translated “{0}: map an item before creating its BOM.”.format(name)).
- If (not self.materials at node\_id and not operations).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.materials at node\_id → not operations.
  - Evaluate problems.append(translated “{0}: add raw materials or operations.”.format(name)).
- For each tuple(index, row) in enumerate(operations, start = 1).
  - Evaluate problems.extend(self.get\_operation\_problems(name, index, row, row is identical to operations at negative 1)).
- For each row in self.materials at node\_id.
  - If not self.get\_material\_item(row).
    - Evaluate problems.append(translated “{0}: map an item for every raw material.”.format(name)).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return problems.

**Methods declared on this owner** [get bom name](operations-012.md#op-5475ddea4e35b6), [get operation problems](operations-012.md#op-0db27de30d821d), [get material item](operations-012.md#op-8093c475249143).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L754)

<a id="op-0db27de30d821d"></a>
### Operation Plan.get operation problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_operation_problems`

**Inputs** self, name, index, row, is\_last.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set step from translated “{0} step {1} ({2})”.format(name, index, row.operation).
- Set problems from list().
- If not row.workstation\_type.
  - Evaluate problems.append(translated “{0}: set the Workstation Type.”.format(step)).
- If flt(row.time\_in\_mins) ≤ 0.
  - Evaluate problems.append(translated “{0}: set the operation time.”.format(step)).
- If (self.produces\_item\_at\_each\_operation and not is\_last and not self.get\_output\_item(row, is\_last)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.produces\_item\_at\_each\_operation → not is\_last → not self.get\_output\_item(row, is\_last).
  - Evaluate problems.append(translated “{0}: choose the item this step makes.”.format(step)).
- Return problems.

**Methods declared on this owner** [get output item](operations-012.md#op-74ba0ece864194).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L759)

<a id="op-1e2720723bb58f"></a>
### Operation Plan.get bom order

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_order`

**Inputs** self.

**Declared result** list at int.

**Explicit results** order.

**Local steps**

- Set node\_by\_item from mapping of self.get\_node\_item(node\_id) → node\_id for node\_id drawn from self.bom\_node\_ids.
  - Draw node\_id from self.bom\_node\_ids.
- Set tuple(order, visiting) from tuple(list(), set()).
- Bind local operation visit for subsequent calls.
- For each node\_id in self.bom\_node\_ids.
  - Evaluate visit(node\_id).
- Return order.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L752)

<a id="op-f388ca7ea63b87"></a>
### Operation Plan.get bom order.visit

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_order_visit`

**Inputs** node\_id.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “BOM {0} uses itself as a raw material.”.format(bold(self.get\_bom\_name(node\_id))).

**Local steps**

- If node\_id belongs to order.
  - Return no value.
- If node\_id belongs to visiting.
  - Call the validation error handler Platform.throw(translated “BOM {0} uses itself as a raw material.”.format(bold(self.get\_bom\_name(node\_id)))).
- Evaluate visiting.add(node\_id).
- For each item\_code in self.get\_items\_used(node\_id).
  - If node\_by\_item.get(item\_code, node\_id) differs from node\_id.
    - Evaluate visit(node\_by\_item at item\_code).
- Evaluate visiting.discard(node\_id).
- Evaluate order.append(node\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L753)

<a id="op-4739c6263e2abe"></a>
### Operation Plan.get items used

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_items_used`

**Inputs** self, node\_id.

**Declared result** set at str.

**Explicit results** items.

**Local steps**

- Set items from set of self.get\_material\_item(row) for row drawn from self.materials at node\_id.
  - Draw row from self.materials at node\_id.
- If self.produces\_item\_at\_each\_operation.
  - Evaluate items.update(generator of self.get\_output\_item(row, false) for row drawn from self.operations at node\_id at slice no value to negative 1).
    - Draw row from self.operations at node\_id at slice no value to negative 1.
- Return items.

**Methods declared on this owner** [get material item](operations-012.md#op-8093c475249143), [get output item](operations-012.md#op-74ba0ece864194).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L756)

<a id="op-d2ece24abcec25"></a>
### Operation Plan.make bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_make_bom`

**Inputs** self, node\_id, boms.

**Declared result** str.

**Explicit results** self.submit\_bom(bom).

**Local steps**

- Set operations from self.operations at node\_id.
- Set quantity from self.get\_bom\_quantity(node\_id).
- Set bom from self.new\_bom(node\_id).
- Evaluate bom.update(mapping(“with\_operations” → 1 when operations, otherwise 0, “track\_semi\_finished\_goods” → 1 when (operations and self.produces\_item\_at\_each\_operation), otherwise 0)).
  - Value choice on operations — true gives 1, false gives 0.
  - Value choice on (operations and self.produces\_item\_at\_each\_operation) — true gives 1, false gives 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in operations → self.produces\_item\_at\_each\_operation.
- For each row in operations.
  - Evaluate bom.append(“operations”, self.get\_bom\_operation(row, row is identical to operations at negative 1, boms, quantity)).
- Set stock\_uoms from self.get\_stock\_uoms(node\_id).
- For each row in self.materials at node\_id.
  - Evaluate bom.append(“items”, self.get\_material\_bom\_item(row, operations, boms, stock\_uoms, …)).
- Return self.submit\_bom(bom).

**Methods declared on this owner** [get bom operation](operations-012.md#op-27d86b043bff38), [get stock uoms](operations-012.md#op-12018c65814cf8), [get material bom item](operations-012.md#op-21fbb4010bc3c8).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L765)

<a id="op-27d86b043bff38"></a>
### Operation Plan.get bom operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_bom_operation`

**Inputs** self, row, is\_last, boms, quantity.

**Declared result** dict.

**Explicit results** operation.

**Local steps**

- Set operation from mapping(“operation” → row.operation, “workstation\_type” → row.workstation\_type, “time\_in\_mins” → row.time\_in\_mins).
- If self.produces\_item\_at\_each\_operation.
  - Set output\_item from self.get\_output\_item(row, is\_last).
  - Evaluate operation.update(mapping(“finished\_good” → output\_item, “finished\_good\_qty” → ((flt(row.output\_quantity) or 1) × quantity), “is\_final\_finished\_good” → 1 when is\_last, otherwise 0, “bom\_no” → empty text whe ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.output\_quantity) → 1.
    - Value choice on is\_last — true gives 1, false gives 0.
    - Value choice on is\_last — true gives empty text, false gives boms.get(output\_item, empty text).
- Return operation.

**Methods declared on this owner** [get output item](operations-012.md#op-74ba0ece864194).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L751)

<a id="op-21fbb4010bc3c8"></a>
### Operation Plan.get material bom item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_material_bom_item`

**Inputs** self, row, operations, boms, stock\_uoms, quantity.

**Declared result** dict.

**Explicit results** bom\_item.

**Local steps**

- Set item\_code from self.get\_material\_item(row).
- Set part from self.parts.get(cint(row.part\_node\_id)).
- Set uom from (row.uom or stock\_uoms.get(item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.uom → stock\_uoms.get(item\_code).
- Set bom\_item from self.get\_bom\_item(item\_code, (flt(row.qty) × quantity), uom, boms, …).
- If row.from\_operation\_id.
  - Evaluate bom\_item.update(mapping(“do\_not\_explode” → 1, “bom\_no” → empty text)).
- Set operation\_ids from list of cint(operation.operation\_id) for operation drawn from operations.
  - Draw operation from operations.
- If (row.operation\_id and self.produces\_item\_at\_each\_operation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.operation\_id → self.produces\_item\_at\_each\_operation.
  - Set bom\_item at “operation\_row\_id” from (operation\_ids.index(cint(row.operation\_id)) + 1).
- Otherwise.
  - If row.operation\_id.
    - Set bom\_item at “operation” from operations at operation\_ids.index(cint(row.operation\_id)).operation.
- Return bom\_item.

**Methods declared on this owner** [get material item](operations-012.md#op-8093c475249143).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L757)

<a id="op-12018c65814cf8"></a>
### Operation Plan.get stock uoms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_stock_uoms`

**Inputs** self, node\_id.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping of item.name → item.stock\_uom for item drawn from items.

**Local steps**

- Set item\_codes from list(set of self.get\_material\_item(row) for row drawn from self.materials at node\_id).
  - Draw row from self.materials at node\_id.
- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, item\_codes)), fields = list(“name”, “stock\_uom”)).
- Return mapping of item.name → item.stock\_uom for item drawn from items.
  - Draw item from items.

**Methods declared on this owner** [get material item](operations-012.md#op-8093c475249143).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L762)

<a id="op-53d66f13535cea"></a>
### Operation Plan.get used node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_get_used_node_ids`

**Inputs** self.

**Declared result** set at int.

**Explicit results** (node\_ids − set(0)).

**Local steps**

- Set node\_ids from set of cint(row.part\_node\_id) for row drawn from self.design.materials.
  - Draw row from self.design.materials.
- Evaluate node\_ids.update(generator of cint(row.output\_node\_id) for row drawn from self.design.operations).
  - Draw row from self.design.operations.
- Evaluate node\_ids.update(self.bom\_node\_ids).
- Return (node\_ids − set(0)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L763)

<a id="op-71d925b5e3b549"></a>
### Operation Plan.remap nodes

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_remap_nodes`

**Inputs** self, new\_node\_ids.

**Local steps**

- For each row in list(self.design.operations).
  - Evaluate self.remap\_row(row, tuple(“bom\_node\_id”, “output\_node\_id”), new\_node\_ids, “operations”).
- For each row in list(self.design.materials).
  - Evaluate self.remap\_row(row, tuple(“bom\_node\_id”, “part\_node\_id”), new\_node\_ids, “materials”).
- Set operation\_ids from set of cint(row.operation\_id) for row drawn from self.design.operations.
  - Draw row from self.design.operations.
- For each row in list(self.design.materials).
  - If (cint(row.from\_operation\_id) and cint(row.from\_operation\_id) does not belong to operation\_ids).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(row.from\_operation\_id) → cint(row.from\_operation\_id) does not belong to operation\_ids.
    - Evaluate self.design.remove(row).
  - Otherwise.
    - If cint(row.operation\_id) does not belong to operation\_ids.
      - Set row.operation\_id from 0.
- For each table in tuple(“operations”, “materials”).
  - For each tuple(index, row) in enumerate(self.design.get(table), start = 1).
    - Set row.idx from index.

If control reaches the end, it returns no value.

**Methods declared on this owner** [remap row](operations-012.md#op-cba58c0b71c878).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L767)

<a id="op-cba58c0b71c878"></a>
### Operation Plan.remap row

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_operation_plan_operationplan_remap_row`

**Inputs** self, row, fields, new\_node\_ids, table.

**State and service calls** msgprint with translated “A row in {0} was removed because its design part is not in the new design file.”.format(translated table.title()).

**Explicit results** no value.

**Local steps**

- For each field in fields.
  - If not cint(row.get(field)).
    - Continue with the next iteration or loop test.
  - If cint(row.get(field)) does not belong to new\_node\_ids.
    - Evaluate self.design.remove(row).
    - Evaluate Platform.msgprint(translated “A row in {0} was removed because its design part is not in the new design file.”.format(translated table.title())).
    - Return no value.
  - Evaluate row.set(field, new\_node\_ids at cint(row.get(field))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L768)

<a id="op-c0173cadf2e85f"></a>
### Part Tree Plan.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_init`

**Inputs** self, design.

**Local steps**

- Evaluate super().\_\_init\_\_(design).
- Set self.children from defaultdict(list).
- For each row in design.items.
  - If not row.exclude\_from\_bom.
    - Evaluate self.children at (row.parent\_node\_id or 0).append(row).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.parent\_node\_id → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L783)

<a id="op-ffb6ce7dfd95ee"></a>
### Part Tree Plan.get used node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_used_node_ids`

**Inputs** self.

**Declared result** set at int.

**Explicit results** node\_ids.

**Local steps**

- Set tuple(node\_ids, pending) from tuple(set(), list(0)).
- While pending.
  - For each row in self.children at pending.pop().
    - Evaluate node\_ids.add(row.node\_id).
    - Evaluate pending.append(row.node\_id).
- Return node\_ids.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L782)

<a id="op-5af9988268451f"></a>
### Part Tree Plan.get bom node ids

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_bom_node_ids`

**Inputs** self.

**Declared result** list at int.

**Explicit results** list(0, expanded generator of node\_id for node\_id drawn from self.get\_used\_node\_ids() where self.children at node\_id).

**Local steps**

- Return list(0, expanded generator of node\_id for node\_id drawn from self.get\_used\_node\_ids() where self.children at node\_id).
  - Draw node\_id from self.get\_used\_node\_ids(), keep a combination only if (self.children at node\_id).

**Methods declared on this owner** [get used node ids](operations-012.md#op-ffb6ce7dfd95ee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L776)

<a id="op-ca614e0c9b1638"></a>
### Part Tree Plan.get problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_problems`

**Inputs** self.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set problems from list().
- If not self.design.item\_code.
  - Evaluate problems.append(translated “Map the finished good to an item.”).
- If not self.children at 0.
  - Evaluate problems.append(translated “Add raw materials to the finished good.”).
- Set used from self.get\_used\_node\_ids().
- Set unmapped from list of (row.part\_name or row.part\_number) for row drawn from self.design.items where (row.node\_id belongs to used and not row.item\_code).
  - Draw row from self.design.items, keep a combination only if ((row.node\_id belongs to used and not row.item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.part\_name → row.part\_number.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.node\_id belongs to used → not row.item\_code.
- If unmapped.
  - Evaluate problems.append(translated “Map an item to these parts: {0}”.format(“, ”.join(unmapped))).
- Evaluate problems.extend(self.get\_duplicate\_problems()).
- Evaluate problems.extend(self.get\_assembly\_problems(used)).
- Evaluate problems.extend(self.get\_cycle\_problems(used)).
- Return problems.

**Methods declared on this owner** [get used node ids](operations-012.md#op-ffb6ce7dfd95ee), [get duplicate problems](operations-012.md#op-f26731965871fb), [get assembly problems](operations-013.md#op-b0ff79cfb3e1ba), [get cycle problems](operations-013.md#op-763fb3c899d3e0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L781)

<a id="op-f26731965871fb"></a>
### Part Tree Plan.get duplicate problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_duplicate_problems`

**Inputs** self.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set problems from list().
- For each siblings in self.children.values().
  - Set seen from mapping().
  - For each row in siblings.
    - If not row.item\_code.
      - Continue with the next iteration or loop test.
    - Set other from seen.setdefault(row.item\_code, row).
    - If (other is distinct from row and (self.children at row.node\_id or self.children at other.node\_id)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in other is distinct from row → (self.children at row.node\_id or self.children at other.node\_id).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.children at row.node\_id → self.children at other.node\_id.
      - Evaluate problems.append(translated “Parts {0} and {1} in the same assembly are mapped to item {2}.”.format(bold(other.part\_name), bold(row.part\_name), bold(row.item\_code))).
- Return problems.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L780)
