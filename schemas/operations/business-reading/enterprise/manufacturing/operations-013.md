# Production · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-b0ff79cfb3e1ba"></a>
### Part Tree Plan.get assembly problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_assembly_problems`

**Inputs** self, used.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set tuple(problems, assemblies) from tuple(list(), mapping()).
- For each row in self.design.items.
  - If (row.node\_id does not belong to used or not row.item\_code or not self.children at row.node\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.node\_id does not belong to used → not row.item\_code → not self.children at row.node\_id.
    - Continue with the next iteration or loop test.
  - Set materials from sorted(generator of tuple((part.item\_code or empty text), (part.uom or empty text), flt(qty)) for tuple(part, qty) drawn from self.merge\_rows(row.node\_id)).
    - Draw tuple(part, qty) from self.merge\_rows(row.node\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.item\_code → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in part.uom → empty text.
  - Set tuple(other, other\_materials) from assemblies.setdefault(row.item\_code, tuple(row, materials)).
  - If (other is distinct from row and other\_materials differs from materials).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in other is distinct from row → other\_materials differs from materials.
    - Evaluate problems.append(translated “Assemblies {0} and {1} are mapped to item {2} but have different raw materials.”.format(bold((other.part\_name or other.part\_number)), bold((row.part\_name or row.part\_number)), b ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in other.part\_name → other.part\_number.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.part\_name → row.part\_number.
- Return problems.

**Methods declared on this owner** [merge rows](operations-013.md#op-9cf5ed92e5fa45).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L775)

<a id="op-763fb3c899d3e0"></a>
### Part Tree Plan.get cycle problems

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_cycle_problems`

**Inputs** self, used.

**Declared result** list at str.

**Explicit results** problems.

**Local steps**

- Set problems from list().
- For each row in self.design.items.
  - If (row.node\_id does not belong to used or not row.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.node\_id does not belong to used → not row.item\_code.
    - Continue with the next iteration or loop test.
  - Set parent from self.parts.get(row.parent\_node\_id).
  - Set ancestor\_items from set(self.design.item\_code).
  - While parent.
    - Evaluate ancestor\_items.add(parent.item\_code).
    - Set parent from self.parts.get(parent.parent\_node\_id).
  - If row.item\_code belongs to ancestor\_items.
    - Evaluate problems.append(translated “Part {0} is mapped to item {1}, which is also its own assembly.”.format(bold((row.part\_name or row.part\_number)), bold(row.item\_code))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.part\_name → row.part\_number.
- Return problems.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L779)

<a id="op-e5b39840dd0a22"></a>
### Part Tree Plan.get bom order

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_bom_order`

**Inputs** self.

**Declared result** list at int.

**Explicit results** order.

**Local steps**

- Set order from list().
- Bind local operation visit for subsequent calls.
- Evaluate visit(0).
- Return order.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L777)

<a id="op-d8dd15ec71265e"></a>
### Part Tree Plan.get bom order.visit

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_get_bom_order_visit`

**Inputs** node\_id.

**Local steps**

- For each row in self.children at node\_id.
  - If self.children at row.node\_id.
    - Evaluate visit(row.node\_id).
- Evaluate order.append(node\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L778)

<a id="op-bc83e381171cdd"></a>
### Part Tree Plan.make bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_make_bom`

**Inputs** self, node\_id, boms.

**Declared result** str.

**Explicit results** self.submit\_bom(bom).

**Local steps**

- Set bom from self.new\_bom(node\_id).
- Set quantity from self.get\_bom\_quantity(node\_id).
- If not node\_id.
  - Evaluate self.set\_routing(bom).
- For each tuple(part, qty) in self.merge\_rows(node\_id).
  - Set bom\_item from self.get\_bom\_item(part.item\_code, (qty × quantity), part.uom, boms, …).
  - Set bom\_item at “operation” from part.operation when bom.with\_operations, otherwise no value.
    - Value choice on bom.with\_operations — true gives part.operation, false gives no value.
  - Evaluate bom.append(“items”, bom\_item).
- Return self.submit\_bom(bom).

**Methods declared on this owner** [set routing](operations-013.md#op-e8834eb77f1bc6), [merge rows](operations-013.md#op-9cf5ed92e5fa45).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L784)

<a id="op-e8834eb77f1bc6"></a>
### Part Tree Plan.set routing

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_set_routing`

**Inputs** self, bom.

**Explicit results** no value.

**Local steps**

- If self.design.is\_phantom.
  - Return no value.
- If (self.design.routing or any(generator of row.operation for row drawn from self.design.items)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.design.routing → any(generator of row.operation for row drawn from self.design.items).
  - Draw row from self.design.items.
  - Evaluate bom.update(mapping(“routing” → self.design.routing, “with\_operations” → 1)).
  - Set bom.transfer\_material\_against from “Work Order”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L786)

<a id="op-9cf5ed92e5fa45"></a>
### Part Tree Plan.merge rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_part_tree_plan_parttreeplan_merge_rows`

**Inputs** self, node\_id.

**Declared result** list at tuple.

**Explicit results** list(merged.values()).

**Local steps**

- Set merged from mapping().
- For each row in self.children at node\_id.
  - Set key from tuple(row.item\_code, row.uom).
  - Set tuple(part, qty) from merged.get(key, tuple(row, 0)).
  - Set merged at key from tuple(part, (qty + flt(row.qty))).
- Return list(merged.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L785)

<a id="op-f73ea4d168d55b"></a>
### Read step file

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_read_step_file`

**Inputs** content.

**Declared result** dict.

**Explicit results** mapping(“design\_name” → root at “part\_name”, “part\_number” → root at “part\_number”, “parts” → root at “children”) · mapping(“design\_name” → no value, “part\_number” → no value, “parts” → roots).

**Explicit failure paths** validation helper — translated “The STEP file is incomplete or damaged.”.

**Local steps**

- Attempt the following.
  - Set roots from StepProductStructure(content).get\_tree().
- On failure (tuple(AttributeError, IndexError, KeyError, ValueError)).
  - Call the validation error handler Platform.throw(translated “The STEP file is incomplete or damaged.”, title = translated “Invalid Design File”).
- If len(roots) equals 1.
  - Set root from roots at 0.
  - Return mapping(“design\_name” → root at “part\_name”, “part\_number” → root at “part\_number”, “parts” → root at “children”).
- Return mapping(“design\_name” → no value, “part\_number” → no value, “parts” → roots).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L788)

<a id="op-08abfbffed5603"></a>
### Step Arguments.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_init`

**Inputs** self, content, position.

**Local steps**

- Set self.content from content.
- Set self.position from position.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L789)

<a id="op-7fe38842ab6316"></a>
### Step Arguments.read list

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_read_list`

**Inputs** self.

**Declared result** list.

**Explicit results** values.

**Local steps**

- Set values from list().
- While true.
  - Evaluate self.skip\_spaces().
  - Set character from self.content at self.position.
  - If character equals “)”.
    - Update self.position using + 1.
    - Return values.
  - If character equals “,”.
    - Update self.position using + 1.
    - Continue with the next iteration or loop test.
  - Evaluate values.append(self.read\_value()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [skip spaces](operations-013.md#op-a534f95918ba84), [read value](operations-013.md#op-f896021d1ae4e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L790)

<a id="op-f896021d1ae4e0"></a>
### Step Arguments.read value

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_read_value`

**Inputs** self.

**Explicit results** self.read\_string() · self.read\_list() · self.read\_reference() · self.read\_token().

**Local steps**

- Set character from self.content at self.position.
- If character equals “'”.
  - Return self.read\_string().
- If character equals “(”.
  - Update self.position using + 1.
  - Return self.read\_list().
- If character equals “#”.
  - Return self.read\_reference().
- Return self.read\_token().

**Methods declared on this owner** [read string](operations-013.md#op-5070ef1911cf0d), [read list](operations-013.md#op-7fe38842ab6316), [read reference](operations-013.md#op-e8a813987ef539), [read token](operations-013.md#op-a043abbaae3410).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L794)

<a id="op-5070ef1911cf0d"></a>
### Step Arguments.read string

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_read_string`

**Inputs** self.

**Declared result** str.

**Explicit results** decode\_step\_string(self.content at slice start to end.replace(“''”, “'”)).

**Local steps**

- Set start from (self.position + 1).
- Set end from start.
- While true.
  - Set end from self.content.index(“'”, end).
  - If self.content at slice (end + 1) to (end + 2) differs from “'”.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Update end using + 2.
- Set self.position from (end + 1).
- Return decode\_step\_string(self.content at slice start to end.replace(“''”, “'”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L792)

<a id="op-e8a813987ef539"></a>
### Step Arguments.read reference

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_read_reference`

**Inputs** self.

**Declared result** int.

**Explicit results** int(match.group(1)).

**Local steps**

- Set match from REFERENCE.match(self.content, self.position).
- Set self.position from match.end().
- Return int(match.group(1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L791)

<a id="op-a043abbaae3410"></a>
### Step Arguments.read token

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_read_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L793)

<a id="op-a534f95918ba84"></a>
### Step Arguments.skip spaces

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_steparguments_skip_spaces`

**Inputs** self.

**Local steps**

- While self.content at self.position.isspace().
  - Update self.position using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L795)

<a id="op-b198d7a49e5439"></a>
### Decode step string

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_decode_step_string`

**Inputs** value.

**Declared result** str.

**Explicit results** value.replace(“\\\\”, “\\”).

**Local steps**

- Set value from UNICODE\_ESCAPE.sub(deferred anonymous expression, value).
- Set value from LATIN\_ESCAPE.sub(deferred anonymous expression, value).
- Return value.replace(“\\\\”, “\\”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L787)

<a id="op-d4cf28ef274556"></a>
### Step Product Structure.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_init`

**Inputs** self, content.

**Local steps**

- Set self.entities from mapping().
- For each match in PRODUCT\_ENTITY.finditer(content).
  - Set arguments from StepArguments(content, match.end()).read\_list().
  - Set self.entities at int(match.group(1)) from tuple(match.group(2), arguments).
- Set self.children from defaultdict(Counter).
- Set self.used\_definitions from set().
- Set self.part\_count from 0.
- For each tuple(entity\_type, arguments) in self.entities.values().
  - If entity\_type equals “NEXT\_ASSEMBLY\_USAGE\_OCCURRENCE”.
    - Update self.children at arguments at 3 at arguments at 4 using + 1.
    - Evaluate self.used\_definitions.add(arguments at 4).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L800)

<a id="op-2e310f07d5bf08"></a>
### Step Product Structure.root definitions

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_root_definitions`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at int.

**Explicit results** definitions · list of definition for definition drawn from definitions where (definition belongs to self.children and definition does not belong to self.used\_definitions).

**Local steps**

- Set definitions from list of entity\_id for tuple(entity\_id, tuple(entity\_type, \_arguments)) drawn from self.entities.items() where entity\_type equals “PRODUCT\_DEFINITION”.
  - Draw tuple(entity\_id, tuple(entity\_type, \_arguments)) from self.entities.items(), keep a combination only if (entity\_type equals “PRODUCT\_DEFINITION”).
- If not self.children.
  - Return definitions.
- Return list of definition for definition drawn from definitions where (definition belongs to self.children and definition does not belong to self.used\_definitions).
  - Draw definition from definitions, keep a combination only if ((definition belongs to self.children and definition does not belong to self.used\_definitions)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in definition belongs to self.children → definition does not belong to self.used\_definitions.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L801)

<a id="op-b6cd7ab548f717"></a>
### Step Product Structure.get tree

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_get_tree`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list of self.get\_node(definition, 1, set()) for definition drawn from roots.

**Explicit failure paths** validation helper — translated “The STEP file has no product structure.”.

**Local steps**

- Set roots from self.root\_definitions.
- If not roots.
  - Call the validation error handler Platform.throw(translated “The STEP file has no product structure.”, title = translated “Invalid Design File”).
- Return list of self.get\_node(definition, 1, set()) for definition drawn from roots.
  - Draw definition from roots.

**Methods declared on this owner** [get node](operations-013.md#op-95d26d2b61c594).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L799)

<a id="op-95d26d2b61c594"></a>
### Step Product Structure.get node

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_get_node`

**Inputs** self, definition, quantity, ancestors.

**Declared result** dict.

**Explicit results** node.

**Explicit failure paths** validation helper — translated “The STEP file has an assembly that contains itself.” · validation helper — translated “The STEP file has more than {0} parts.”.format(MAX\_PARTS).

**Local steps**

- If definition belongs to ancestors.
  - Call the validation error handler Platform.throw(translated “The STEP file has an assembly that contains itself.”, title = translated “Invalid Design File”).
- Update self.part\_count using + 1.
- If self.part\_count &gt; MAX\_PARTS.
  - Call the validation error handler Platform.throw(translated “The STEP file has more than {0} parts.”.format(MAX\_PARTS), title = translated “Invalid Design File”).
- Set node from self.get\_product(definition).
- Set node at “quantity” from quantity.
- Set node at “children” from list of self.get\_node(child, child\_quantity, (ancestors bitwise or set(definition))) for tuple(child, child\_quantity) drawn from self.children at definition.items().
  - Draw tuple(child, child\_quantity) from self.children at definition.items().
- Return node.

**Methods declared on this owner** [get product](operations-013.md#op-fc4668c96b4ce9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L797)

<a id="op-fc4668c96b4ce9"></a>
### Step Product Structure.get product

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_get_product`

**Inputs** self, definition.

**Declared result** dict.

**Explicit results** mapping(“part\_number” → (part\_number or part\_name), “part\_name” → (part\_name or part\_number), “description” → description).

**Local steps**

- Set formation from self.get\_arguments(definition, “PRODUCT\_DEFINITION”) at 2.
- Set product from self.get\_arguments(formation, “PRODUCT\_DEFINITION\_FORMATION”, “PRODUCT\_DEFINITION\_FORMATION\_WITH\_SPECIFIED\_SOURCE”) at 2.
- Set tuple(part\_number, part\_name, description) from self.get\_arguments(product, “PRODUCT”) at slice no value to 3.
- Return mapping(“part\_number” → (part\_number or part\_name), “part\_name” → (part\_name or part\_number), “description” → description).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part\_number → part\_name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part\_name → part\_number.

**Methods declared on this owner** [get arguments](operations-013.md#op-fbcdf269b452b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L798)

<a id="op-fbcdf269b452b3"></a>
### Step Product Structure.get arguments

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_step_file_stepproductstructure_get_arguments`

**Inputs** self, entity\_id, remaining positional values entity\_types.

**Declared result** list.

**Explicit results** entity at 1.

**Explicit failure paths** validation helper — translated “The STEP file refers to a missing {0} #{1}.”.format(entity\_types at 0, entity\_id).

**Local steps**

- Set entity from self.entities.get(entity\_id).
- If (not entity or entity at 0 does not belong to entity\_types).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not entity → entity at 0 does not belong to entity\_types.
  - Call the validation error handler Platform.throw(translated “The STEP file refers to a missing {0} #{1}.”.format(entity\_types at 0, entity\_id), title = translated “Invalid Design File”).
- Return entity at 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L796)

## Report · Bom explorer

<a id="op-77d69bcf34d9a9"></a>
### Execute

`operation_enterprise_manufacturing_report_bill_of_materials_explorer_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set data from list().
- Set columns from get\_columns().
- Evaluate get\_data(filters, data).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0540.json#L578) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1017)

<a id="op-5b4a3d21451971"></a>
### Get data

`operation_enterprise_manufacturing_report_bill_of_materials_explorer_business_behavior_get_data`

**Inputs** filters, data.

**Local steps**

- Evaluate get\_exploded\_items(filters.bom, data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1019)
