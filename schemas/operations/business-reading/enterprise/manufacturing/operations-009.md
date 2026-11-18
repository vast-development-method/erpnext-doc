# Production · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom creator

<a id="op-922cdf0c6ced41"></a>
### BOMCreator.create boms job id

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_create_boms_job_id`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** formatted text bom\_creator\_create\_boms::{self.name}.

**Local steps**

- Return formatted text bom\_creator\_create\_boms::{self.name}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L666)

<a id="op-910e6e5937cdb2"></a>
### BOMCreator.enqueue create boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_enqueue_create_bills_of_materials`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self · enqueue doc with “BOM Creator” · msgprint with translated “The BOMs are being created. The status changes when they are ready.”.

**Local steps**

- Evaluate self.check\_permission(“submit”).
- Evaluate Platform.has\_permission(“BOM”, “submit”, throw = true).
- Evaluate self.validate\_can\_create\_boms().
- Evaluate self.get\_bom\_plan().validate\_can\_make\_boms().
- Evaluate self.db\_set(mapping(“status” → “In Progress”, “error\_log” → no value), notify = true).
- Evaluate Platform.enqueue\_doc(“BOM Creator”, self.name, “create\_boms”, queue = “short”, timeout = 600, enqueue\_after\_commit = true, job\_id = self.create\_boms\_job\_id, …).
- Evaluate Platform.msgprint(translated “The BOMs are being created. The status changes when they are ready.”, alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate can create boms](operations-009.md#op-be8e1091e11590), [get bom plan](operations-008.md#op-e409e50f389a91).

**Values supplied outside this operation** effective access from self.check\_permission(“submit”), Platform.has\_permission(“BOM”, “submit”, throw = true) · service or queued work from Platform.enqueue\_doc(“BOM Creator”, self.name, “create\_boms”, queue = “short”, timeout = 600, enqueue\_after\_commit = true, job\_id = self.create\_boms\_job\_id, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L230)

<a id="op-be8e1091e11590"></a>
### BOMCreator.validate can create boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_validate_can_create_boms`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Submit this design before creating BOMs.” · validation helper — translated “This design has a newer revision. Create BOMs from the latest revision.” · validation helper — translated “BOMs are already created from this design. Cancel them to create them again.” · validation helper — translated “The BOMs of this design are being created. Wait until the status changes.”.

**Local steps**

- <a id="op-be8e1091e11590-guard-2"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Submit this design before creating BOMs.”).
- <a id="op-be8e1091e11590-guard-5"></a>If self.status equals “Superseded”.
  - Call the validation error handler Platform.throw(translated “This design has a newer revision. Create BOMs from the latest revision.”).
- <a id="op-be8e1091e11590-guard-8"></a>If self.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “BOMs are already created from this design. Cancel them to create them again.”).
- If is\_job\_enqueued(self.create\_boms\_job\_id).
  - Call the validation error handler Platform.throw(translated “The BOMs of this design are being created. Wait until the status changes.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Submit this design before creating BOMs.”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-be8e1091e11590-guard-2)
- At the comparison self.status equals “Superseded”, self.status = “Superseded” selects the branch that calls the validation-error handler with translated “This design has a newer revision. Create BOMs from the latest revision.”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-be8e1091e11590-guard-5)
- At the comparison self.status equals “Completed”, self.status = “Completed” selects the branch that calls the validation-error handler with translated “BOMs are already created from this design. Cancel them to create them again.”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-be8e1091e11590-guard-8)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L683)

<a id="op-18bc4752e42708"></a>
### BOMCreator.create boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_create_bills_of_materials`

**Inputs** self.

**State and service calls** call db\_set on self · rollback.

**Explicit results** no value.

**Local steps**

- Evaluate self.db\_set(mapping(“status” → “In Progress”, “error\_log” → no value)).
- Attempt the following.
  - Evaluate self.get\_bom\_plan().make\_boms().
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate self.db\_set(mapping(“status” → “Failed”, “error\_log” → Platform.get\_traceback(with\_context = true)), notify = true).
  - Return no value.
- Set self.status from “Submitted”.
- Evaluate self.set\_status(save = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom plan](operations-008.md#op-e409e50f389a91), [set status](operations-008.md#op-6daa73b51ce54f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L229)

<a id="op-af990f50e329cf"></a>
### Get bom tree

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_bom_tree`

**Inputs** bom\_no, include\_sub\_assemblies = false.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_bom\_rows(bom\_no, sbool(include\_sub\_assemblies), set(bom\_no)).

**Local steps**

- Evaluate Platform.has\_permission(“BOM”, “read”, doc = bom\_no, throw = true).
- Return get\_bom\_rows(bom\_no, sbool(include\_sub\_assemblies), set(bom\_no)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM”, “read”, doc = bom\_no, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L689)

<a id="op-d7549f89fe77c5"></a>
### Get bom rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_bom_rows`

**Inputs** bom\_no, include\_sub\_assemblies, visited.

**Declared result** list at dict.

**Record and data access** resolve a document from “BOM” via get\_doc.

**Explicit results** rows.

**Local steps**

- Set bom from Platform.get\_doc(“BOM”, bom\_no).
- Set rows from list().
- For each item in bom.items.
  - Set expand from (include\_sub\_assemblies and item.bom\_no and item.bom\_no does not belong to visited).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in include\_sub\_assemblies → item.bom\_no → item.bom\_no does not belong to visited.
  - If expand.
    - Evaluate Platform.has\_permission(“BOM”, “read”, doc = item.bom\_no, throw = true).
  - Evaluate rows.append(mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “description” → item.description, “qty” → (flt(item.qty) ÷ (flt(bom.quantity) or 1)), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(bom.quantity) → 1.
    - Value choice on (expand or not item.bom\_no) — true gives 1, false gives item.do\_not\_explode.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in expand → not item.bom\_no.
    - Value choice on expand — true gives empty text, false gives item.bom\_no.
    - Value choice on expand — true gives get\_bom\_rows(item.bom\_no, true, (visited bitwise or set(item.bom\_no))), false gives list().
- Return rows.

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM”, “read”, doc = item.bom\_no, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L688)

<a id="op-2eb57f599f4b59"></a>
### Read design file

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_read_design_file`

**Inputs** file\_url.

**Declared result** dict.

**Explicit results** DESIGN\_FILE\_READERS at extension(content).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You cannot read the design file {0}.”.format(file\_url) · validation helper — translated “Attach a STEP file (.step or .stp) or a CSV file.”.

**Local steps**

- Set file from find\_file\_by\_url(file\_url).
- If not file.
  - Call the validation error handler Platform.throw(translated “You cannot read the design file {0}.”.format(file\_url), Platform.PermissionError).
- Set extension from file.file\_name.rsplit(“.”, 1) at negative 1.lower().
- If extension does not belong to DESIGN\_FILE\_READERS.
  - Call the validation error handler Platform.throw(translated “Attach a STEP file (.step or .stp) or a CSV file.”, title = translated “Invalid Design File”).
- Set content from file.get\_content().
- If isinstance(content, bytes).
  - Set content from content.decode(“utf-8”, errors = “replace”).
- Return DESIGN\_FILE\_READERS at extension(content).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L700)

<a id="op-ed9d6f3b3dc19f"></a>
### Get part paths

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_part_paths`

**Inputs** parts.

**Declared result** dict at tuple(int, tuple).

**Explicit results** paths.

**Explicit failure paths** validation helper — translated “Part {0} is inside its own assembly.”.format(bold(row.part\_number)).

**Local steps**

- Set rows from mapping of row.node\_id → row for row drawn from parts.
  - Draw row from parts.
- Set names from get\_path\_names(parts).
- Set paths from mapping().
- For each row in parts.
  - Set tuple(path, current) from tuple(list(), row).
  - While current.
    - If len(path) &gt; len(rows).
      - Call the validation error handler Platform.throw(translated “Part {0} is inside its own assembly.”.format(bold(row.part\_number))).
    - Evaluate path.append(names at current.node\_id).
    - Set current from rows.get(current.parent\_node\_id).
  - Set paths at row.node\_id from tuple(reversed(path)).
- Return paths.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L694)

<a id="op-46e3ef0f3b0213"></a>
### Get path names

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_path_names`

**Inputs** parts.

**Declared result** dict at tuple(int, str).

**Explicit results** names.

**Local steps**

- Set occurrences from defaultdict(int).
- Set names from mapping().
- For each row in parts.
  - Set sibling from tuple(cint(row.parent\_node\_id), row.part\_number).
  - Update occurrences at sibling using + 1.
  - Set names at row.node\_id from get\_path\_name(row.part\_number, occurrences at sibling).
- Return names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L697)

<a id="op-537aef8d9fea5c"></a>
### Get path name

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_path_name`

**Inputs** part\_number, occurrence.

**Declared result** str.

**Explicit results** part\_number when occurrence equals 1, otherwise formatted text {part\_number} ({occurrence}).

**Local steps**

- Return part\_number when occurrence equals 1, otherwise formatted text {part\_number} ({occurrence}).
  - Value choice on occurrence equals 1 — true gives part\_number, false gives formatted text {part\_number} ({occurrence}).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L696)

<a id="op-cda7f92a8a9a4c"></a>
### Get part quantities

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_part_quantities`

**Inputs** parts.

**Declared result** dict at tuple(tuple, float).

**Explicit results** mapping of paths at row.node\_id → get\_design\_quantity(row) for row drawn from parts.

**Local steps**

- Set paths from get\_part\_paths(parts).
- Return mapping of paths at row.node\_id → get\_design\_quantity(row) for row drawn from parts.
  - Draw row from parts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L695)

<a id="op-84f19c4b67f5db"></a>
### Get change

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_change`

**Inputs** row, path, previous.

**Declared result** dict.

**Explicit results** mapping(“part\_number” → current.part\_number, “part\_name” → current.part\_name, “path” → “ &gt; ”.join(path), “previous\_quantity” → get\_design\_quantity(previous) when previous, otherwise no value, …).

**Local steps**

- Set current from (row or previous).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row → previous.
- Return mapping(“part\_number” → current.part\_number, “part\_name” → current.part\_name, “path” → “ &gt; ”.join(path), “previous\_quantity” → get\_design\_quantity(previous) when previous, otherwise no value, …).
  - Value choice on previous — true gives get\_design\_quantity(previous), false gives no value.
  - Value choice on row — true gives get\_design\_quantity(row), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L201) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L690)

<a id="op-3aa3922e01b9bc"></a>
### Get design quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_design_quantity`

**Inputs** row.

**Declared result** float.

**Explicit results** (flt(row.get(“design\_quantity”)) or flt(row.qty)).

**Local steps**

- Return (flt(row.get(“design\_quantity”)) or flt(row.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“design\_quantity”)) → flt(row.qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L691)

<a id="op-851a1ad1e3a84d"></a>
### Get quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_quantity`

**Inputs** old\_row, design\_quantity.

**Declared result** float.

**Explicit results** old\_row.qty · design\_quantity.

**Local steps**

- If (old\_row and flt(old\_row.qty) differs from get\_design\_quantity(old\_row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_row → flt(old\_row.qty) differs from get\_design\_quantity(old\_row).
  - Return old\_row.qty.
- Return design\_quantity.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L698)

<a id="op-b554d0f9611630"></a>
### Get mapping

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_mapping`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping() · mapping of field → row.get(field) for field drawn from MAPPING\_FIELDS.

**Local steps**

- If not row.
  - Return mapping().
- Return mapping of field → row.get(field) for field drawn from MAPPING\_FIELDS.
  - Draw field from MAPPING\_FIELDS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L693)

<a id="op-ed821dcd072b6e"></a>
### Get items by code

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_get_items_by_code`

**Inputs** item\_codes.

**Declared result** dict.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · mapping of item.name → item for item drawn from items.

**Local steps**

- If not item\_codes.
  - Return mapping().
- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, item\_codes)), fields = list(“name”, “stock\_uom”)).
- Return mapping of item.name → item for item drawn from items.
  - Draw item from items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L692)

<a id="op-25b21b1d175293"></a>
### Make item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_make_item`

**Inputs** item\_code, item\_name, description, item\_group, stock\_uom.

**Declared result** str.

**State and service calls** request new\_doc for “Item” · call insert on item.

**Explicit results** item.name.

**Local steps**

- Set item from Platform.new\_doc(“Item”).
- Evaluate item.update(mapping(“item\_code” → item\_code, “item\_name” → (item\_name or item\_code), “description” → (description or item\_name or item\_code), “item\_group” → item\_group, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_name → item\_code.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in description → item\_name → item\_code.
- Evaluate item.insert().
- Return item.name.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L699)

<a id="op-d438cb9fa5da92"></a>
### Read bom csv file

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_csv_file_read_bom_csv_file`

**Inputs** content.

**Declared result** dict.

**Explicit results** mapping(“design\_name” → no value, “part\_number” → no value, “parts” → build\_tree(parts)).

**Explicit failure paths** validation helper — translated “The CSV file has no parts.”.

**Local steps**

- Set rows from read\_csv\_content(content).
- <a id="op-d438cb9fa5da92-guard-3"></a>If len(rows) &lt; 2.
  - Call the validation error handler Platform.throw(translated “The CSV file has no parts.”, title = translated “Invalid Design File”).
- Set columns from list of COLUMNS.get(nested operand in the contract(nested operand in the contract).strip().lower()) for header drawn from rows at 0.
  - Draw header from rows at 0.
- Evaluate validate\_columns(columns).
- Set parts from list of get\_part(dict(zip(columns, row, strict = false))) for row drawn from rows at slice 1 to no value where any(row).
  - Draw row from rows at slice 1 to no value, keep a combination only if (any(row)).
- Return mapping(“design\_name” → no value, “part\_number” → no value, “parts” → build\_tree(parts)).

**Derived branch illustrations**

- At the comparison len(rows) &lt; 2, length of rows = 1 selects the branch that calls the validation-error handler with translated “The CSV file has no parts.”. With length of rows = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d438cb9fa5da92-guard-3)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L704)

<a id="op-dc5411eece76f5"></a>
### Validate columns

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_csv_file_validate_columns`

**Inputs** columns.

**Explicit failure paths** validation helper — translated “The CSV file needs a Level or an Item Number column.” · validation helper — translated “The CSV file needs a Part Number or a Part Name column.” · validation helper — translated “The CSV file needs a Quantity column.”.

**Local steps**

- If (“level” does not belong to columns and “item\_number” does not belong to columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “level” does not belong to columns → “item\_number” does not belong to columns.
  - Call the validation error handler Platform.throw(translated “The CSV file needs a Level or an Item Number column.”, title = translated “Invalid Design File”).
- If (“part\_number” does not belong to columns and “part\_name” does not belong to columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “part\_number” does not belong to columns → “part\_name” does not belong to columns.
  - Call the validation error handler Platform.throw(translated “The CSV file needs a Part Number or a Part Name column.”, title = translated “Invalid Design File”).
- If “quantity” does not belong to columns.
  - Call the validation error handler Platform.throw(translated “The CSV file needs a Quantity column.”, title = translated “Invalid Design File”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L705)

<a id="op-6555f5e1859066"></a>
### Get part

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_csv_file_get_part`

**Inputs** values.

**Declared result** dict.

**Explicit results** mapping(“depth” → get\_depth(values), “part\_number” → (part\_number or part\_name), “part\_name” → (part\_name or part\_number), “description” → cstr(values.get(“description”)).strip(), …).

**Local steps**

- Set part\_number from cstr(values.get(“part\_number”)).strip().
- Set part\_name from cstr(values.get(“part\_name”)).strip().
- Return mapping(“depth” → get\_depth(values), “part\_number” → (part\_number or part\_name), “part\_name” → (part\_name or part\_number), “description” → cstr(values.get(“description”)).strip(), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part\_number → part\_name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in part\_name → part\_number.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(values.get(“quantity”)) → 1.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L703)

<a id="op-357fe53d6f7142"></a>
### Get depth

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_csv_file_get_depth`

**Inputs** values.

**Declared result** int.

**Explicit results** cint(values.get(“level”)) · (cstr(nested operand in the contract(nested operand in the contract)).strip().count(“.”) + 1).

**Local steps**

- If values.get(“level”) is distinct from no value.
  - Return cint(values.get(“level”)).
- Return (cstr(nested operand in the contract(nested operand in the contract)).strip().count(“.”) + 1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L702)

<a id="op-c24afab9cd7b0c"></a>
### Build tree

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_csv_file_build_tree`

**Inputs** parts.

**Declared result** list at dict.

**Explicit results** roots.

**Explicit failure paths** validation helper — translated “Row {0}: level {1} does not follow the level of the row above.”.format(row\_no, depth).

**Local steps**

- Set tuple(roots, ancestors) from tuple(list(), list()).
- For each tuple(row\_no, part) in enumerate(parts, start = 2).
  - Set depth from part.pop(“depth”).
  - If (depth &lt; 1 or depth &gt; (len(ancestors) + 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in depth &lt; 1 → depth &gt; (len(ancestors) + 1).
    - Call the validation error handler Platform.throw(translated “Row {0}: level {1} does not follow the level of the row above.”.format(row\_no, depth), title = translated “Invalid Design File”).
  - Remove ancestors at slice (depth − 1) to no value.
  - Set siblings from ancestors at negative 1 at “children” when ancestors, otherwise roots.
    - Value choice on ancestors — true gives ancestors at negative 1 at “children”, false gives roots.
  - Evaluate siblings.append(part).
  - Evaluate ancestors.append(part).
- Return roots.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L701)

<a id="op-4a45f83c5f67a3"></a>
### BOMPlan.initialize

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_init`

**Inputs** self, design.

**Local steps**

- Set self.design from design.
- Set self.parts from mapping of row.node\_id → row for row drawn from design.items.
  - Draw row from design.items.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L225) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L714)

<a id="op-40ce466de7f081"></a>
### BOMPlan.get node item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_plan_bomplan_get_node_item`

**Inputs** self, node\_id.

**Declared result** (str bitwise or no value).

**Explicit results** self.design.item\_code · self.parts at cint(node\_id).item\_code.

**Local steps**

- If not cint(node\_id).
  - Return self.design.item\_code.
- Return self.parts at cint(node\_id).item\_code.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L711)
