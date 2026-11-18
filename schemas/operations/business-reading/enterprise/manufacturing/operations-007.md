# Production · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom

<a id="op-e3ac150d1ea71b"></a>
### Get component account

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_component_account`

**Inputs** parent, company.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Workstation Operating Component Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Workstation Operating Component Account”, mapping(“parent” → parent, “company” → company), “expense\_account”).

**Local steps**

- Return Platform.db.get\_value(“Workstation Operating Component Account”, mapping(“parent” → parent, “company” → company), “expense\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L648)

<a id="op-65325f95a94c9e"></a>
### Add additional operating cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_additional_operating_cost`

**Inputs** stock\_entry, work\_order, expense\_account, job\_card = no value.

**Explicit results** no value.

**Local steps**

- If not (work\_order and work\_order.additional\_operating\_cost and work\_order.qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order → work\_order.additional\_operating\_cost → work\_order.qty.
  - Return no value.
- If (job\_card and job\_card.finished\_good and job\_card.finished\_good differs from work\_order.production\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_card → job\_card.finished\_good → job\_card.finished\_good differs from work\_order.production\_item.
  - Return no value.
- Set per\_unit from (flt(work\_order.additional\_operating\_cost) ÷ flt(work\_order.qty)).
- If not per\_unit.
  - Return no value.
- Evaluate stock\_entry.append(“additional\_costs”, mapping(“expense\_account” → expense\_account, “description” → “Additional Operating Cost”, “amount” → (per\_unit × flt(stock\_entry.fg\_completed\_qty)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L618)

<a id="op-6ca0e02aca022e"></a>
### Add operations cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_operations_cost`

**Inputs** stock\_entry, work\_order = no value, expense\_account = no value, job\_card = no value.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Local steps**

- Bind dependencies get\_remaining\_operating\_cost, uses\_sub\_assembly\_operating\_cost.
- Set remaining\_operating\_cost from get\_remaining\_operating\_cost(work\_order, stock\_entry.bom\_no).
- If remaining\_operating\_cost.
  - Set cost\_added from add\_operating\_cost\_component\_wise(stock\_entry, work\_order, expense\_account, job\_card = job\_card).
  - If cost\_added.
    - Evaluate \_add\_fg\_based\_operating\_cost(stock\_entry, work\_order, expense\_account, job\_card).
  - Otherwise.
    - If not job\_card.
      - If (work\_order.operations and not uses\_sub\_assembly\_operating\_cost(work\_order, stock\_entry.bom\_no)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.operations → not uses\_sub\_assembly\_operating\_cost(work\_order, stock\_entry.bom\_no).
        - For each operation in work\_order.operations.
          - Evaluate \_add\_operation\_cost(stock\_entry, work\_order, operation, expense\_account).
        - Evaluate \_add\_fg\_based\_operating\_cost(stock\_entry, work\_order, expense\_account).
      - Otherwise.
        - Evaluate \_append\_operating\_cost(stock\_entry, expense\_account, (remaining\_operating\_cost × flt(stock\_entry.fg\_completed\_qty))).
- Evaluate \_add\_additional\_operating\_cost(stock\_entry, work\_order, expense\_account, job\_card).
- Bind local operation get\_max\_operation\_quantity for subsequent calls.
- Bind local operation get\_utilised\_corrective\_cost for subsequent calls.
- If (work\_order and work\_order.corrective\_operation\_cost and cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order → work\_order.corrective\_operation\_cost → cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”)).
  - Set max\_qty from (get\_max\_operation\_quantity() − work\_order.produced\_qty).
  - Set remaining\_corrective\_cost from (work\_order.corrective\_operation\_cost − get\_utilised\_corrective\_cost()).
  - Evaluate stock\_entry.append(“additional\_costs”, mapping(“expense\_account” → expense\_account, “description” → “Corrective Operation Cost”, “has\_corrective\_cost” → 1, “amount” → ((remaining\_corrective\_cost ÷ max\_qty) ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “add\_corrective\_operation\_cost\_in\_finished\_good\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L623)

<a id="op-7a618b127f3f9b"></a>
### Add operations cost.get max operation quantity

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_operations_cost_get_max_operation_quantity`

**Inputs** no declared parameters.

**Explicit results** min(list of d.qty for d drawn from query.run(as\_dict = true), default = 0).

**Local steps**

- Set table from Platform.qb.DocType(“Job Card”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“qty”)).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the  ….
- Return min(list of d.qty for d drawn from query.run(as\_dict = true), default = 0).
  - Draw d from query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L624)

<a id="op-bf21e9258f1ae9"></a>
### Add operations cost.get utilised corrective cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_operations_cost_get_utilised_corrective_cost`

**Inputs** no declared parameters.

**Explicit results** (query.run(as\_dict = true) at 0.amount or 0).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Entry”).
- Set subquery from nested operand in the contract.qb.from\_(table).select(table.name).where(((table.docstatus equals 1 bitwise and table.work\_order equals work\_order.name) bitwise and table.purpose equals “Manufacture”)).
- Set table from Platform.qb.DocType(“Landed Cost Taxes and Charges”).
- Set query from nested operand in the contract.qb.from\_(table).select(Sum(nested operand in the contract.amount).as\_(“amount”)).where((table.parent.isin(subquery) bitwise and table.has\_corrective\_cost equals 1)).
- Return (query.run(as\_dict = true) at 0.amount or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) at 0.amount → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L625)

<a id="op-ad7177c3230b15"></a>
### Get bom diff

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_bom_diff`

**Inputs** bom1, bom2.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “BOM” via get\_doc.

**Explicit results** out.

**Explicit failure paths** validation helper — translated “BOM 1 {0} and BOM 2 {1} should not be same”.format(Platform.bold(bom1), Platform.bold(bom2)).

**Local steps**

- If bom1 equals bom2.
  - Call the validation error handler Platform.throw(translated “BOM 1 {0} and BOM 2 {1} should not be same”.format(Platform.bold(bom1), Platform.bold(bom2))).
- Set doc1 from Platform.get\_doc(“BOM”, bom1).
- Set doc2 from Platform.get\_doc(“BOM”, bom2).
- Evaluate doc1.check\_permission().
- Evaluate doc2.check\_permission().
- Set out from get\_diff(doc1, doc2).
- Set out.row\_changed from list().
- Set out.added from list().
- Set out.removed from list().
- For each df in doc1.meta.fields.
  - Evaluate diff\_table\_field(df, doc1, doc2, out).
- Return out.

**Values supplied outside this operation** effective access from doc1.check\_permission(), doc2.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L646)

<a id="op-2ac0c8199ccbc8"></a>
### Diff table field

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_diff_table_field`

**Inputs** df, doc1, doc2, out.

**Explicit results** no value.

**Local steps**

- Bind dependencies table\_fields.
- If df.fieldtype does not belong to table\_fields.
  - Return no value.
- Set identifiers from mapping(“operations” → “operation”, “items” → “item\_code”, “secondary\_items” → “item\_code”, “exploded\_items” → “item\_code”).
- Set identifier from identifiers.get(df.fieldname).
- If not identifier.
  - Return no value.
- Set old\_rows from mapping().
- For each row in doc1.get(df.fieldname).
  - Evaluate old\_rows.setdefault(row.get(identifier), list()).append(row).
- Set unmatched\_rows from list().
- For each tuple(index, row) in enumerate(doc2.get(df.fieldname)).
  - If not pop\_unchanged\_row(old\_rows.get(row.get(identifier), list()), row).
    - Evaluate unmatched\_rows.append(tuple(index, row)).
- Evaluate collect\_row\_changes(df, identifier, old\_rows, unmatched\_rows, …).
- For each rows in old\_rows.values().
  - Evaluate out.removed.extend(generator of list(df.fieldname, row.as\_dict()) for row drawn from rows).
    - Draw row from rows.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L645)

<a id="op-7223ccc42db189"></a>
### Pop unchanged row

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_pop_unchanged_row`

**Inputs** candidates, row.

**Explicit results** candidates.pop(index).

**Local steps**

- For each tuple(index, candidate) in enumerate(candidates).
  - If not get\_diff(candidate, row, for\_child = true).
    - Return candidates.pop(index).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L660)

<a id="op-32622e069cccf1"></a>
### Collect row changes

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_collect_row_changes`

**Inputs** df, identifier, old\_rows, unmatched\_rows, out.

**Local steps**

- For each tuple(index, row) in unmatched\_rows.
  - Set candidates from old\_rows.get(row.get(identifier)).
  - If not candidates.
    - Evaluate out.added.append(list(df.fieldname, row.as\_dict())).
    - Continue with the next iteration or loop test.
  - Set diff from get\_diff(candidates.pop(0), row, for\_child = true).
  - If (diff and diff.changed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff → diff.changed.
    - Evaluate out.row\_changed.append(tuple(df.fieldname, index, row.get(identifier), diff.changed)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L644)

<a id="op-270368a392de45"></a>
### Item query

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item Barcode” via get\_all · read “Item” via get\_cached\_value · read “Item” via get\_list.

**Explicit results** Platform.get\_list(“Item”, fields = fields, filters = query\_filters, or\_filters = or\_cond\_filters, order\_by = order\_by, …).

**Local steps**

- Set meta from Platform.get\_meta(“Item”, cached = true).
- Set searchfields from meta.get\_search\_fields().
- Set order\_by from “idx desc, name, item\_name”.
- Set fields from list(“name”, “item\_name”, “item\_group”, “description”).
- Evaluate fields.extend(list of field for field drawn from searchfields where field does not belong to list(“name”, “item\_group”, “description”)).
  - Draw field from searchfields, keep a combination only if (field does not belong to list(“name”, “item\_group”, “description”)).
- If not searchfields.
  - Set searchfields from list(“name”).
- Set query\_filters from list(list(“disabled”, “=”, 0), list(IfNull(Field(“end\_of\_life”), “3099-12-31”), “&gt;”, today())).
- Set or\_cond\_filters from list().
- If txt.
  - For each s\_field in searchfields.
    - Evaluate or\_cond\_filters.append(list(s\_field, “like”, formatted text %{txt}%)).
  - Set barcodes from Platform.get\_all(“Item Barcode”, fields = list(“parent as item\_code”), filters = mapping(“barcode” → tuple(“like”, formatted text %{txt}%)), distinct = true).
  - Set barcodes from list of d.item\_code for d drawn from barcodes.
    - Draw d from barcodes.
  - If barcodes.
    - Evaluate or\_cond\_filters.append(list(“name”, “in”, barcodes)).
- If (filters and filters.get(“item\_code”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“item\_code”).
  - Set has\_variants from Platform.get\_cached\_value(“Item”, filters.get(“item\_code”), “has\_variants”).
  - If not has\_variants.
    - Evaluate query\_filters.append(list(“has\_variants”, “=”, 0)).
- If filters.
  - For each tuple(fieldname, value) in filters.items().
    - Evaluate query\_filters.append(list(fieldname, expanded value) when isinstance(value, (list bitwise or tuple)), otherwise list(fieldname, “=”, value)).
      - Value choice on isinstance(value, (list bitwise or tuple)) — true gives list(fieldname, expanded value), false gives list(fieldname, “=”, value).
- Return Platform.get\_list(“Item”, fields = fields, filters = query\_filters, or\_filters = or\_cond\_filters, order\_by = order\_by, …).

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Item”, filters.get(“item\_code”), “has\_variants”).

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L657)

<a id="op-7e733b60aa1902"></a>
### Make variant bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_make_variant_bom`

**Inputs** source\_name, bom\_no, item, variant\_items, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Bind dependencies add\_variant\_item.
- Bind local operation postprocess for subsequent calls.
- Set doc from get\_mapped\_doc(“BOM”, source\_name, mapping(“BOM” → mapping(“doctype” → “BOM”, “validation” → mapping(“docstatus” → list(“=”, 1))), “BOM Item” → mapping(“doctype” → “BOM Item”, “field\_no\_map” → list(“bom\_no ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L658)

<a id="op-c8d8f4e93786f6"></a>
### Make variant bom.postprocess

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_make_variant_bom_postprocess`

**Inputs** source, doc.

**Local steps**

- Set doc.item from item.
- Set item\_data from \_get\_item\_details(item).
- Evaluate doc.update(mapping(“item\_name” → item\_data.item\_name, “description” → item\_data.description, “uom” → item\_data.stock\_uom, “allow\_alternative\_item” → item\_data.allow\_alternative\_item)).
- Set mapped\_rows from len(doc.items).
- Evaluate add\_variant\_item(variant\_items, doc, source\_name).
- For each row in doc.items at slice mapped\_rows to no value.
  - Set row.qty from (flt(row.qty) × (flt(source.quantity) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(source.quantity) → 1.
  - Set row.stock\_qty from flt((row.qty × row.conversion\_factor), row.precision(“stock\_qty”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L659)

<a id="op-9c86e9b2d24631"></a>
### Get op cost from sub assemblies

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_op_cost_from_sub_assemblies`

**Inputs** bom\_no, op\_cost = 0, skip\_boms\_with\_operations = false.

**Record and data access** read “BOM” via get\_cached\_value.

**Explicit results** (flt(op\_cost) + (unit\_cost × conversion\_rate)).

**Local steps**

- Set conversion\_rate from (flt(Platform.get\_cached\_value(“BOM”, bom\_no, “conversion\_rate”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(Platform.get\_cached\_value(“BOM”, bom\_no, “conversion\_rate”)) → 1.
- Set unit\_cost from \_get\_unit\_operating\_cost(bom\_no, mapping(), skip\_boms\_with\_operations).
- Return (flt(op\_cost) + (unit\_cost × conversion\_rate)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, bom\_no, “conversion\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L651)

<a id="op-35b4e88dd5fa43"></a>
### Get unit operating cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_unit_operating_cost`

**Inputs** bom\_no, unit\_costs, skip\_boms\_with\_operations = false.

**Record and data access** read “BOM” via get\_cached\_value · read “BOM Item” via get\_all.

**Explicit results** unit\_costs at bom\_no · cost.

**Local steps**

- If bom\_no belongs to unit\_costs.
  - Return unit\_costs at bom\_no.
- Set bom from Platform.get\_cached\_value(“BOM”, bom\_no, list(“operating\_cost”, “quantity”, “with\_operations”), as\_dict = true).
- Set quantity from (flt(bom.quantity) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(bom.quantity) → 1.
- Set cost from 0 when (skip\_boms\_with\_operations and bom.with\_operations), otherwise (flt(bom.operating\_cost) ÷ quantity).
  - Value choice on (skip\_boms\_with\_operations and bom.with\_operations) — true gives 0, false gives (flt(bom.operating\_cost) ÷ quantity).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in skip\_boms\_with\_operations → bom.with\_operations.
- For each row in Platform.get\_all(“BOM Item”, filters = mapping(“parent” → bom\_no, “parenttype” → “BOM”, “docstatus” → 1, “bom\_no” → tuple(“is”, “set”)), fields = list(“bom\_no”, “stock\_qty”)).
  - Set child\_cost from \_get\_unit\_operating\_cost(row.bom\_no, unit\_costs, skip\_boms\_with\_operations).
  - Update cost using + ((flt(row.stock\_qty) ÷ quantity) × child\_cost).
- Set unit\_costs at bom\_no from cost.
- Return cost.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, bom\_no, list(“operating\_cost”, “quantity”, “with\_operations”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L655)

<a id="op-ca2ddd55b6b6b5"></a>
### Get good qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_good_qty`

**Inputs** bom.

**Explicit results** good\_qty when good\_qty &gt; 0, otherwise (flt(bom.quantity) or 1).

**Local steps**

- Set good\_qty from (flt(bom.quantity) − flt(bom.process\_loss\_qty)).
- Return good\_qty when good\_qty &gt; 0, otherwise (flt(bom.quantity) or 1).
  - Value choice on good\_qty &gt; 0 — true gives good\_qty, false gives (flt(bom.quantity) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(bom.quantity) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L650)

<a id="op-1c279f78863797"></a>
### Get secondary items from sub assemblies

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_secondary_items_from_sub_assemblies`

**Inputs** bom\_no, company, qty, secondary\_items = no value.

**Record and data access** read “BOM Item” via get\_all.

**Explicit results** secondary\_items.

**Local steps**

- If not secondary\_items.
  - Set secondary\_items from mapping().
- Set bom\_items from Platform.get\_all(“BOM Item”, filters = mapping(“parent” → bom\_no, “docstatus” → 1), fields = list(“bom\_no”, “qty”), order\_by = “idx asc”).
- For each row in bom\_items.
  - If not row.bom\_no.
    - Continue with the next iteration or loop test.
  - Set qty from (flt(row.qty) × flt(qty)).
  - Set items from get\_bom\_items\_as\_dict(row.bom\_no, company, qty = qty, fetch\_exploded = 0, fetch\_secondary\_items = 1).
  - Evaluate secondary\_items.update(items).
  - Evaluate get\_secondary\_items\_from\_sub\_assemblies(row.bom\_no, company, qty, secondary\_items).
- Return secondary\_items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L653)

<a id="op-db1be0b33e88f5"></a>
### Get backflush based on

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_backflush_based_on`

**Inputs** bom\_no.

**Record and data access** read “BOM” via get\_cached\_value · read “Manufacturing Settings” via get\_single\_value.

**Explicit results** backflush\_based\_on.

**Local steps**

- Set backflush\_based\_on from no value.
- If bom\_no.
  - Set backflush\_based\_on from Platform.get\_cached\_value(“BOM”, bom\_no, “backflush\_based\_on”).
- If not backflush\_based\_on.
  - Set backflush\_based\_on from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”).
- Return backflush\_based\_on.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, bom\_no, “backflush\_based\_on”), Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L221)

<a id="op-97c511272e8b12"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_bill_of_materials_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “bom\_no”, “non\_standard\_fieldnames” → mapping(“Item” → “default\_bom”, “Purchase Order” → “bom”, “Purchase Receipt” → “bom”, “Purchase Invoice” → “bom”), “transactions” → list(mapping( ….

**Local steps**

- Return mapping(“fieldname” → “bom\_no”, “non\_standard\_fieldnames” → mapping(“Item” → “default\_bom”, “Purchase Order” → “bom”, “Purchase Receipt” → “bom”, “Purchase Invoice” → “bom”), “transactions” → list(mapping( ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L145)

## Record · Bom creator

<a id="op-707af0b6324548"></a>
### BOMCreator.validate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_validate`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (self.has\_value\_changed(“design\_file”) and self.design\_file).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“design\_file”) → self.design\_file.
  - Evaluate self.import\_design\_file().
- Evaluate self.set\_design\_name().
- Set self.item\_group from (self.item\_group or Platform.db.get\_single\_value(“Stock Settings”, “item\_group”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.item\_group → Platform.db.get\_single\_value(“Stock Settings”, “item\_group”).
- Evaluate self.set\_part\_structure().
- Evaluate self.validate\_part\_models().
- Evaluate self.validate\_existing\_boms().
- Evaluate self.validate\_finished\_good().
- Evaluate OperationPlan(self).validate().
- Evaluate self.set\_revision\_changes().
- Evaluate MaterialCost(self).set\_costs().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [import design file](operations-008.md#op-4f05a6311f0082), [set design name](operations-008.md#op-1d77ed71741b48), [set part structure](operations-008.md#op-f9f1b06a4a8b62), [validate part models](operations-008.md#op-65bfc84efe7b6c), [validate existing boms](operations-008.md#op-128c7f3001014f), [validate finished good](operations-008.md#op-1e641cbb5a9f8b), [set revision changes](operations-008.md#op-664bb86fc6ae09), [set status](operations-008.md#op-6daa73b51ce54f).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “item\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L234)

<a id="op-6417a824847d6b"></a>
### BOMCreator.before submit

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_operations\_have\_routing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate operations have routing](operations-008.md#op-8810306f448bae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L228)

<a id="op-34c4a1586b8968"></a>
### BOMCreator.on submit

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_creator_business_behavior_bill_of_materials_creator_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_previous\_revision\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update previous revision status](operations-008.md#op-fcdd72a63d85a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L232)

<a id="op-ffe278052f2522"></a>
### BOMCreator.before update after submit

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_design\_can\_change().
- Evaluate self.validate\_cad\_parts\_unchanged().
- Evaluate self.validate\_finished\_good().
- Evaluate self.set\_part\_structure().
- Evaluate self.validate\_part\_models().
- Evaluate self.validate\_existing\_boms().
- Evaluate OperationPlan(self).validate().
- Evaluate self.set\_revision\_changes().
- Evaluate MaterialCost(self).set\_costs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate design can change](operations-008.md#op-5a9a877453f40f), [validate cad parts unchanged](operations-008.md#op-2d8281ad978f3f), [validate finished good](operations-008.md#op-1e641cbb5a9f8b), [set part structure](operations-008.md#op-f9f1b06a4a8b62), [validate part models](operations-008.md#op-65bfc84efe7b6c), [validate existing boms](operations-008.md#op-128c7f3001014f), [set revision changes](operations-008.md#op-664bb86fc6ae09).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L665)

<a id="op-bb6125d85cdb69"></a>
### BOMCreator.on update after submit

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(save = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-008.md#op-6daa73b51ce54f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L676)

<a id="op-c2928a28eb22a1"></a>
### BOMCreator.before cancel

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_creator_bom_creator_bomcreator_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-008.md#op-6daa73b51ce54f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L664)
