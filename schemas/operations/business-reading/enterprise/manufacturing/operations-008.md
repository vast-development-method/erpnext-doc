# Production · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-ed319c79972c1b"></a>
### BOMCreator.on cancel

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_previous\_revision\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update previous revision status](operations-008.md#op-fcdd72a63d85a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L231)

<a id="op-69c3ae8653a350"></a>
### BOMCreator.get status

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_status`

**Inputs** self.

**Declared result** str.

**Record and data access** read “BOM Creator” via exists.

**Explicit results** “Draft” · “Cancelled” · “Superseded” · “Completed” · self.status when self.status belongs to tuple(“In Progress”, “Failed”), otherwise “Submitted”.

**Local steps**

- <a id="op-69c3ae8653a350-guard-2"></a>If self.docstatus equals 0.
  - Return “Draft”.
- <a id="op-69c3ae8653a350-guard-5"></a>If self.docstatus equals 2.
  - Return “Cancelled”.
- If Platform.db.exists(“BOM Creator”, mapping(“previous\_revision” → self.name, “docstatus” → 1)).
  - Return “Superseded”.
- If self.get\_bom\_plan().has\_all\_boms().
  - Return “Completed”.
- Return self.status when self.status belongs to tuple(“In Progress”, “Failed”), otherwise “Submitted”.
  - Value choice on self.status belongs to tuple(“In Progress”, “Failed”) — true gives self.status, false gives “Submitted”.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that returns “Draft”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-69c3ae8653a350-guard-2)
- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that returns “Cancelled”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-69c3ae8653a350-guard-5)

**Methods declared on this owner** [get bom plan](operations-008.md#op-e409e50f389a91).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L671)

<a id="op-6daa73b51ce54f"></a>
### BOMCreator.set status

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_set_status`

**Inputs** self, save = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.status from self.get\_status().
- If save.
  - Evaluate self.db\_set(“status”, self.status, notify = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-008.md#op-69c3ae8653a350).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L233)

<a id="op-fcdd72a63d85a3"></a>
### BOMCreator.update previous revision status

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_update_previous_revision_status`

**Inputs** self.

**Record and data access** resolve a document from “BOM Creator” via get\_doc.

**Local steps**

- If self.previous\_revision.
  - Evaluate Platform.get\_doc(“BOM Creator”, self.previous\_revision).set\_status(save = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L681)

<a id="op-1d77ed71741b48"></a>
### BOMCreator.set design name

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_set_design_name`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Set the Design Name or the Finished Good.”.

**Local steps**

- If (not self.design\_name and self.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.design\_name → self.item\_code.
  - Set self.design\_name from (Platform.get\_cached\_value(“Item”, self.item\_code, “item\_name”) or self.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, self.item\_code, “item\_name”) → self.item\_code.
- If not self.design\_name.
  - Call the validation error handler Platform.throw(translated “Set the Design Name or the Finished Good.”, title = translated “Missing Design Name”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “item\_name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L677)

<a id="op-1e641cbb5a9f8b"></a>
### BOMCreator.validate finished good

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_validate_finished_good`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A phantom BOM cannot use 'Produce Item per Operation'.” · validation helper — translated “Phantom BOM cannot be created for stock item {0}.”.format(self.item\_code) · validation helper — translated “Non-phantom BOM cannot be created for non-stock item {0}.”.format(self.item\_code).

**Local steps**

- If (self.is\_phantom and self.track\_semi\_finished\_goods).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_phantom → self.track\_semi\_finished\_goods.
  - Call the validation error handler Platform.throw(translated “A phantom BOM cannot use 'Produce Item per Operation'.”).
- If not self.item\_code.
  - Return no value.
- Set is\_stock\_item from Platform.get\_cached\_value(“Item”, self.item\_code, “is\_stock\_item”).
- If (is\_stock\_item and self.is\_phantom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_stock\_item → self.is\_phantom.
  - Call the validation error handler Platform.throw(translated “Phantom BOM cannot be created for stock item {0}.”.format(self.item\_code)).
- Otherwise.
  - If (not is\_stock\_item and not self.is\_phantom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_stock\_item → not self.is\_phantom.
    - Call the validation error handler Platform.throw(translated “Non-phantom BOM cannot be created for non-stock item {0}.”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L235)

<a id="op-8810306f448bae"></a>
### BOMCreator.validate operations have routing

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_operations_have_routing`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} has Operation {2}. Set a Routing to create BOMs with operations.”.format(row.idx, bold(row.item\_code), bold(row.operation)).

**Local steps**

- If (self.is\_phantom or self.routing or self.track\_semi\_finished\_goods).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_phantom → self.routing → self.track\_semi\_finished\_goods.
  - Return no value.
- For each row in self.items.
  - If row.operation.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} has Operation {2}. Set a Routing to create BOMs with operations.”.format(row.idx, bold(row.item\_code), bold(row.operation)), title = translated “Routing Required”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L686)

<a id="op-4f05a6311f0082"></a>
### BOMCreator.import design file

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_import_design_file`

**Inputs** self.

**Local steps**

- Set design from read\_design\_file(self.design\_file).
- Set self.design\_name from (self.design\_name or design at “design\_name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.design\_name → design at “design\_name”.
- Set self.part\_number from (self.part\_number or design at “part\_number”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.part\_number → design at “part\_number”.
- Set old\_paths from get\_part\_paths(self.items).
- Set old\_rows from mapping of old\_paths at row.node\_id → row for row drawn from self.items.
  - Draw row from self.items.
- Set manual\_rows from list of row for row drawn from self.items where row.source equals “Manual”.
  - Draw row from self.items, keep a combination only if (row.source equals “Manual”).
- Evaluate self.set(“items”, list()).
- Evaluate self.append\_cad\_parts(design at “parts”, 0, tuple(), old\_rows).
- Evaluate self.append\_manual\_parts(manual\_rows, old\_paths).
- Set new\_node\_ids from mapping of path → node\_id for tuple(node\_id, path) drawn from get\_part\_paths(self.items).items().
  - Draw tuple(node\_id, path) from get\_part\_paths(self.items).items().
- Evaluate OperationPlan(self).remap\_nodes(mapping of node\_id → new\_node\_ids at path for tuple(node\_id, path) drawn from old\_paths.items() where path belongs to new\_node\_ids).
  - Draw tuple(node\_id, path) from old\_paths.items(), keep a combination only if (path belongs to new\_node\_ids).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append cad parts](operations-008.md#op-6180c21710a473), [append manual parts](operations-008.md#op-9d816d52c9ec52).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L674)

<a id="op-6180c21710a473"></a>
### BOMCreator.append cad parts

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_append_cad_parts`

**Inputs** self, nodes, parent\_node\_id, parent\_path, old\_rows.

**Local steps**

- Set occurrences from defaultdict(int).
- For each node in nodes.
  - Update occurrences at node at “part\_number” using + 1.
  - Set path from tuple(expanded parent\_path, get\_path\_name(node at “part\_number”, occurrences at node at “part\_number”)).
  - Set row from self.append(“items”, mapping(“node\_id” → (len(self.items) + 1), “parent\_node\_id” → parent\_node\_id, “part\_number” → node at “part\_number”, “part\_name” → node at “part\_name”, …)).
  - Evaluate self.append\_cad\_parts(node at “children”, row.node\_id, path, old\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L662)

<a id="op-9d816d52c9ec52"></a>
### BOMCreator.append manual parts

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_append_manual_parts`

**Inputs** self, manual\_rows, old\_paths.

**State and service calls** msgprint with translated “Part {0} was removed because its assembly is not in the new design file.”.format(bold(row.part\_number)).

**Local steps**

- Set new\_node\_ids from mapping of path → node\_id for tuple(node\_id, path) drawn from get\_part\_paths(self.items).items().
  - Draw tuple(node\_id, path) from get\_part\_paths(self.items).items().
- Set new\_node\_ids at tuple() from 0.
- For each row in manual\_rows.
  - Set parent\_path from old\_paths.get(row.parent\_node\_id, tuple()).
  - If parent\_path does not belong to new\_node\_ids.
    - Evaluate Platform.msgprint(translated “Part {0} was removed because its assembly is not in the new design file.”.format(bold(row.part\_number))).
    - Continue with the next iteration or loop test.
  - Set new\_row from self.append(“items”, mapping(expand row.as\_dict(no\_default\_fields = true), “node\_id” → (len(self.items) + 1))).
  - Set new\_row.parent\_node\_id from new\_node\_ids at parent\_path.
  - Set new\_node\_ids at old\_paths at row.node\_id from new\_row.node\_id.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L663)

<a id="op-f9f1b06a4a8b62"></a>
### BOMCreator.set part structure

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_set_part_structure`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Parent Node {1} does not exist.”.format(row.idx, row.parent\_node\_id).

**Local steps**

- Set last\_node\_id from max(generator of (row.node\_id or 0) for row drawn from self.items, default = 0).
  - Draw row from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.node\_id → 0.
- For each row in self.items.
  - Evaluate self.set\_part\_number(row).
  - If not row.node\_id.
    - Update last\_node\_id using + 1.
    - Set row.node\_id from last\_node\_id.
- Set node\_ids from set of row.node\_id for row drawn from self.items.
  - Draw row from self.items.
- For each row in self.items.
  - If (row.parent\_node\_id and row.parent\_node\_id does not belong to node\_ids).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.parent\_node\_id → row.parent\_node\_id does not belong to node\_ids.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Parent Node {1} does not exist.”.format(row.idx, row.parent\_node\_id), title = translated “Invalid Parent Node”).
- Set parent\_node\_ids from set of row.parent\_node\_id for row drawn from self.items.
  - Draw row from self.items.
- For each row in self.items.
  - Set row.is\_expandable from 1 when row.node\_id belongs to parent\_node\_ids, otherwise 0.
    - Value choice on row.node\_id belongs to parent\_node\_ids — true gives 1, false gives 0.
- Evaluate get\_part\_paths(self.items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set part number](operations-008.md#op-f024263dc2e04f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L679)

<a id="op-f024263dc2e04f"></a>
### BOMCreator.set part number

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_set_part_number`

**Inputs** self, row.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: set the Part Number or the Item.”.format(row.idx).

**Local steps**

- Set row.part\_number from (row.part\_number or row.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.part\_number → row.item\_code.
- If not row.part\_number.
  - Call the validation error handler Platform.throw(translated “Row #{0}: set the Part Number or the Item.”.format(row.idx)).
- If (not row.part\_name and row.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.part\_name → row.item\_code.
  - Set row.part\_name from (row.item\_name or Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.item\_name → Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L678)

<a id="op-65bfc84efe7b6c"></a>
### BOMCreator.validate part models

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_part_models`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: attach the 3D model as a STEP, STL or GLB file.”.format(row.idx) · validation helper — translated “Row #{0}: the placements in the model are not valid.”.format(row.idx).

**Local steps**

- For each row in self.items.
  - If (row.model\_file and nested operand in the contract.rsplit(“.”, 1) at negative 1.lower() does not belong to PART\_MODEL\_FORMATS).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.model\_file → nested operand in the contract.model\_file.rsplit(“.”, 1) at negative 1.lower() does not belong to PART\_MODEL\_FORMATS.
    - Call the validation error handler Platform.throw(translated “Row #{0}: attach the 3D model as a STEP, STL or GLB file.”.format(row.idx), title = translated “Invalid 3D Model”).
  - If (row.placements and not isinstance(Platform.parse\_json(row.placements), list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.placements → not isinstance(Platform.parse\_json(row.placements), list).
    - Call the validation error handler Platform.throw(translated “Row #{0}: the placements in the model are not valid.”.format(row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L687)

<a id="op-128c7f3001014f"></a>
### BOMCreator.validate existing boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_existing_boms`

**Inputs** self.

**Record and data access** read “BOM” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: BOM {1} is not an active, submitted BOM of item {2}.”.format(row.idx, bold(row.bom\_no), bold(row.item\_code)).

**Local steps**

- Set rows from list of row for row drawn from self.items where (row.bom\_no and not row.do\_not\_explode and not row.exclude\_from\_bom).
  - Draw row from self.items, keep a combination only if ((row.bom\_no and not row.do\_not\_explode and not row.exclude\_from\_bom)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom\_no → not row.do\_not\_explode → not row.exclude\_from\_bom.
- If not rows.
  - Return no value.
- Set boms from mapping of bom.name → bom for bom drawn from Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, list(set of nested operand in the contract.bom\_no for row drawn from rows))), fields = list(“name ….
  - Draw bom from Platform.get\_all(“BOM”, filters = mapping(“name” → tuple(“in”, list(set of row.bom\_no for row drawn from rows))), fields = list(“name”, “item”, “docstatus”, “is\_active”)).
  - Draw row from rows.
- For each row in rows.
  - Set bom from boms.get(row.bom\_no).
  - If (not bom or bom.item differs from row.item\_code or bom.docstatus differs from 1 or not bom.is\_active).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bom → bom.item differs from row.item\_code → bom.docstatus differs from 1 → not bom.is\_active.
    - Call the validation error handler Platform.throw(translated “Row #{0}: BOM {1} is not an active, submitted BOM of item {2}.”.format(row.idx, bold(row.bom\_no), bold(row.item\_code)), title = translated “Invalid BOM”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L685)

<a id="op-5a9a877453f40f"></a>
### BOMCreator.validate design can change

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_design_can_change`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A design with the status {0} cannot be changed. Make a new revision to change it.”.format(bold(translated status)).

**Local steps**

- Set status from self.get\_doc\_before\_save().get\_status().
- If status does not belong to tuple(“Submitted”, “Failed”).
  - Call the validation error handler Platform.throw(translated “A design with the status {0} cannot be changed. Make a new revision to change it.”.format(bold(translated status)), title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L684)

<a id="op-2d8281ad978f3f"></a>
### BOMCreator.validate cad parts unchanged

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_cad_parts_unchanged`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Parts from the submitted design file cannot be removed: {0}”.format(“, ”.join(removed)).

**Local steps**

- Set before from self.get\_doc\_before\_save().
- If not before.
  - Return no value.
- Set cad\_node\_ids from set of row.node\_id for row drawn from self.items where row.source equals “CAD File”.
  - Draw row from self.items, keep a combination only if (row.source equals “CAD File”).
- Set removed from list of row.part\_number for row drawn from before.items where (row.source equals “CAD File” and row.node\_id does not belong to cad\_node\_ids).
  - Draw row from before.items, keep a combination only if ((row.source equals “CAD File” and row.node\_id does not belong to cad\_node\_ids)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.source equals “CAD File” → row.node\_id does not belong to cad\_node\_ids.
- If removed.
  - Call the validation error handler Platform.throw(translated “Parts from the submitted design file cannot be removed: {0}”.format(“, ”.join(removed)), title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L682)

<a id="op-664bb86fc6ae09"></a>
### BOMCreator.set revision changes

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_set_revision_changes`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.previous\_revision.
  - Return no value.
- Set previous\_quantities from get\_part\_quantities(self.get\_previous\_parts()).
- Set paths from get\_part\_paths(self.items).
- For each row in self.items.
  - Set previous\_quantity from previous\_quantities.get(paths at row.node\_id).
  - If previous\_quantity is identical to no value.
    - Set row.change\_type from “Added”.
  - Otherwise.
    - If flt(previous\_quantity) differs from get\_design\_quantity(row).
      - Set row.change\_type from “Quantity Changed”.
    - Otherwise.
      - Set row.change\_type from empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get previous parts](operations-008.md#op-38379451d7a9c2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L680)

<a id="op-38379451d7a9c2"></a>
### BOMCreator.get previous parts

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_previous_parts`

**Inputs** self.

**Declared result** list.

**Record and data access** read “BOM Creator Item” via get\_all.

**Explicit results** Platform.get\_all(“BOM Creator Item”, filters = mapping(“parent” → self.previous\_revision, “parenttype” → “BOM Creator”), fields = list(“node\_id”, “parent\_node\_id”, “part\_number”, “part\_name”, …), order\_by = “idx”).

**Local steps**

- Return Platform.get\_all(“BOM Creator Item”, filters = mapping(“parent” → self.previous\_revision, “parenttype” → “BOM Creator”), fields = list(“node\_id”, “parent\_node\_id”, “part\_number”, “part\_name”, …), order\_by = “idx”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L669)

<a id="op-71a72b1b53874b"></a>
### BOMCreator.get revision changes

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_revision_changes`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** changes.

**Explicit failure paths** validation helper — translated “This design has no previous revision.”.

**Local steps**

- If not self.previous\_revision.
  - Call the validation error handler Platform.throw(translated “This design has no previous revision.”).
- Evaluate Platform.has\_permission(“BOM Creator”, “read”, doc = self.previous\_revision, throw = true).
- Set previous\_parts from self.get\_previous\_parts().
- Set previous\_paths from get\_part\_paths(previous\_parts).
- Set previous\_rows from mapping of previous\_paths at row.node\_id → row for row drawn from previous\_parts.
  - Draw row from previous\_parts.
- Set current\_paths from get\_part\_paths(self.items).
- Set changes from mapping(“added” → list(), “removed” → list(), “quantity\_changed” → list()).
- For each row in self.items.
  - Set path from current\_paths at row.node\_id.
  - Set previous from previous\_rows.pop(path, no value).
  - If not previous.
    - Evaluate changes at “added”.append(get\_change(row, path, no value)).
  - Otherwise.
    - If get\_design\_quantity(previous) differs from get\_design\_quantity(row).
      - Evaluate changes at “quantity\_changed”.append(get\_change(row, path, previous)).
- Set changes at “removed” from list of get\_change(no value, path, row) for tuple(path, row) drawn from previous\_rows.items().
  - Draw tuple(path, row) from previous\_rows.items().
- Return changes.

**Methods declared on this owner** [get previous parts](operations-008.md#op-38379451d7a9c2).

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM Creator”, “read”, doc = self.previous\_revision, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L670)

<a id="op-a487270008596d"></a>
### BOMCreator.make new revision

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_make_new_revision`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** read “BOM Creator” via exists.

**State and service calls** request copy\_doc for self · call insert on revision.

**Explicit results** revision.name.

**Explicit failure paths** validation helper — translated “Submit this design before making a new revision.” · validation helper — translated “A newer revision of this design already exists.”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- <a id="op-a487270008596d-guard-3"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Submit this design before making a new revision.”).
- If Platform.db.exists(“BOM Creator”, mapping(“previous\_revision” → self.name, “docstatus” → tuple(“&lt;”, 2))).
  - Call the validation error handler Platform.throw(translated “A newer revision of this design already exists.”).
- Set revision from Platform.copy\_doc(self, ignore\_no\_copy = false).
- Set revision.docstatus from 0.
- Set revision.revision from (self.revision + 1).
- Set revision.previous\_revision from self.name.
- Evaluate revision.insert().
- Return revision.name.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Submit this design before making a new revision.”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a487270008596d-guard-3)

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L675)

<a id="op-e409e50f389a91"></a>
### BOMCreator.get bom plan

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_bom_plan`

**Inputs** self.

**Declared result** (OperationPlan bitwise or PartTreePlan).

**Explicit results** OperationPlan(self) when self.track\_semi\_finished\_goods, otherwise PartTreePlan(self).

**Local steps**

- Return OperationPlan(self) when self.track\_semi\_finished\_goods, otherwise PartTreePlan(self).
  - Value choice on self.track\_semi\_finished\_goods — true gives OperationPlan(self), false gives PartTreePlan(self).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L668)

<a id="op-9f9fd56f3b8483"></a>
### BOMCreator.get used parts

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_used_parts`

**Inputs** self.

**Declared result** list.

**Explicit results** list of row for row drawn from self.items where row.node\_id belongs to node\_ids.

**Local steps**

- Set node\_ids from self.get\_bom\_plan().get\_used\_node\_ids().
- Return list of row for row drawn from self.items where row.node\_id belongs to node\_ids.
  - Draw row from self.items, keep a combination only if (row.node\_id belongs to node\_ids).

**Methods declared on this owner** [get bom plan](operations-008.md#op-e409e50f389a91).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L673)

<a id="op-fbeb65a32d24d9"></a>
### BOMCreator.get suggested items

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_get_suggested_items`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** ItemMatcher(parts).get\_matches().

**Local steps**

- Set parts from list of row for row drawn from self.items where (not row.item\_code and not row.exclude\_from\_bom).
  - Draw row from self.items, keep a combination only if ((not row.item\_code and not row.exclude\_from\_bom)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.item\_code → not row.exclude\_from\_bom.
- Return ItemMatcher(parts).get\_matches().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L672)

<a id="op-4e68ee410520eb"></a>
### BOMCreator.create items

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_create_items`

**Inputs** self, item\_group, stock\_uom.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at str.

**State and service calls** call save on self.

**Explicit results** created.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate Platform.has\_permission(“Item”, “create”, throw = true).
- Set created from list().
- Set rows from list of row for row drawn from self.get\_used\_parts() where not row.item\_code.
  - Draw row from self.get\_used\_parts(), keep a combination only if (not row.item\_code).
- Set items from get\_items\_by\_code(list of row.part\_number for row drawn from rows).
  - Draw row from rows.
- For each row in rows.
  - If row.part\_number does not belong to items.
    - Set item\_code from make\_item(row.part\_number, row.part\_name, row.description, item\_group, …).
    - Set items at row.part\_number from Platform.\_dict(name = item\_code, stock\_uom = stock\_uom).
    - Evaluate created.append(item\_code).
  - Set row.item\_code from items at row.part\_number.name.
  - Set row.uom from items at row.part\_number.stock\_uom.
- Evaluate self.save().
- Return created.

**Methods declared on this owner** [get used parts](operations-008.md#op-9f9fd56f3b8483).

**Values supplied outside this operation** effective access from self.check\_permission(“write”), Platform.has\_permission(“Item”, “create”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L667)
