# Production · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-1589e90fba471f"></a>
### Variant row qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_variant_row_qty`

**Inputs** item\_code, item, stock\_uom.

**Explicit results** mapping(“qty” → flt(item.get(“qty”)), “uom” → uom, “conversion\_factor” → conversion\_factor, “stock\_qty” → stock\_qty, …).

**Local steps**

- Set uom from (item.get(“uom”) or stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“uom”) → stock\_uom.
- Set conversion\_factor from flt(get\_conversion\_factor(item\_code, uom) at “conversion\_factor”).
- Set stock\_qty from flt((flt(item.get(“qty”)) × conversion\_factor), Platform.get\_precision(“Work Order Item”, “required\_qty”)).
- Return mapping(“qty” → flt(item.get(“qty”)), “uom” → uom, “conversion\_factor” → conversion\_factor, “stock\_qty” → stock\_qty, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L32) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1042)

<a id="op-3c9897c6aea9d9"></a>
### Get raw material rate

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_raw_material_rate`

**Inputs** args, wo\_doc, bom\_doc.

**Explicit results** (rate × flt((bom\_doc.conversion\_rate or 1))).

**Local steps**

- Set rate from bom\_doc.get\_rm\_rate(mapping(“company” → wo\_doc.company, “item\_code” → args.get(“item\_code”), “qty” → args.get(“required\_qty”), “uom” → args.get(“stock\_uom”), …), notify = false).
- Return (rate × flt((bom\_doc.conversion\_rate or 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bom\_doc.conversion\_rate → 1.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1009)

<a id="op-1f8935ca6bd9ae"></a>
### Get template rm item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_template_rm_item`

**Inputs** wo\_doc, item\_code.

**Explicit results** row.

**Local steps**

- For each row in wo\_doc.required\_items.
  - If row.item\_code equals item\_code.
    - Return row.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L5) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1015)

<a id="op-d9320fdda84b7c"></a>
### Check if scrap warehouse mandatory

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_check_if_scrap_warehouse_mandatory`

**Inputs** bom\_no.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “BOM” via get\_doc.

**Explicit results** res.

**Local steps**

- Set res from mapping(“set\_scrap\_wh\_mandatory” → false).
- If bom\_no.
  - Set bom from Platform.get\_doc(“BOM”, bom\_no).
  - If bom.has\_scrap\_items().
    - Set res at “set\_scrap\_wh\_mandatory” from true.
- Return res.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L993)

<a id="op-60c08f85327651"></a>
### Set work order ops

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_set_work_order_ops`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** call save on po.

**Local steps**

- Set po from Platform.get\_doc(“Work Order”, name).
- Evaluate po.set\_work\_order\_operations().
- Evaluate po.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0534.json#L5298) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L785)

<a id="op-9661628d157c8c"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_stock_entry`

**Inputs** work\_order\_id, purpose, qty = no value, target\_warehouse = no value, is\_additional\_transfer\_entry = false, source\_stock\_entry = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Warehouse” via get\_value · read “BOM” via get\_value.

**State and service calls** request new\_doc for “Stock Entry”.

**Explicit results** stock\_entry.as\_dict().

**Local steps**

- Set work\_order from Platform.get\_doc(“Work Order”, work\_order\_id, check\_permission = “read”).
- If not Platform.db.get\_value(“Warehouse”, work\_order.wip\_warehouse, “is\_group”).
  - Set wip\_warehouse from work\_order.wip\_warehouse.
- Otherwise.
  - Set wip\_warehouse from no value.
- Set stock\_entry from Platform.new\_doc(“Stock Entry”).
- Set stock\_entry.purpose from purpose.
- Set stock\_entry.work\_order from work\_order\_id.
- Set stock\_entry.company from work\_order.company.
- Set stock\_entry.from\_bom from 1.
- Set stock\_entry.bom\_no from work\_order.bom\_no.
- Set stock\_entry.use\_multi\_level\_bom from work\_order.use\_multi\_level\_bom.
- If purpose belongs to list(“Material Transfer for Manufacture”, “Manufacture”).
  - Set stock\_entry.subcontracting\_inward\_order from work\_order.subcontracting\_inward\_order.
- Set stock\_entry.fg\_completed\_qty from qty when qty is distinct from no value, otherwise (flt(work\_order.qty) − flt(work\_order.produced\_qty)).
  - Value choice on qty is distinct from no value — true gives qty, false gives (flt(work\_order.qty) − flt(work\_order.produced\_qty)).
- If purpose equals “Material Transfer for Manufacture”.
  - Set stock\_entry.to\_warehouse from wip\_warehouse.
  - Set stock\_entry.project from work\_order.project.
- Otherwise.
  - Set stock\_entry.from\_warehouse from work\_order.source\_warehouse when (work\_order.skip\_transfer and not work\_order.from\_wip\_warehouse), otherwise wip\_warehouse.
    - Value choice on (work\_order.skip\_transfer and not work\_order.from\_wip\_warehouse) — true gives work\_order.source\_warehouse, false gives wip\_warehouse.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order.skip\_transfer → not work\_order.from\_wip\_warehouse.
  - Set stock\_entry.to\_warehouse from work\_order.fg\_warehouse.
  - Set stock\_entry.project from work\_order.project.
  - If work\_order.bom\_no.
    - Set stock\_entry.inspection\_required from Platform.db.get\_value(“BOM”, work\_order.bom\_no, “inspection\_required”).
- If purpose equals “Disassemble”.
  - Set stock\_entry.from\_warehouse from work\_order.fg\_warehouse.
  - Set stock\_entry.to\_warehouse from (target\_warehouse or work\_order.source\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_warehouse → work\_order.source\_warehouse.
  - If source\_stock\_entry.
    - Set stock\_entry.source\_stock\_entry from source\_stock\_entry.
- Evaluate stock\_entry.set\_stock\_entry\_type().
- Set stock\_entry.is\_additional\_transfer\_entry from is\_additional\_transfer\_entry.
- Evaluate stock\_entry.get\_items().
- Evaluate stock\_entry.set\_secondary\_items\_from\_job\_card().
- If purpose differs from “Disassemble”.
  - Evaluate stock\_entry.set\_serial\_no\_batch\_for\_finished\_good().
- Return stock\_entry.as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L13) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1023)

<a id="op-f39b70c0b46815"></a>
### Get disassembly available qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_get_disassembly_available_quantity`

**Inputs** stock\_entry\_name, current\_se\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Record and data access** read “Stock Entry” via get\_value.

**Explicit results** 0.0 · flt((flt(se.fg\_completed\_qty) − already\_disassembled), Platform.get\_precision(“Stock Entry”, “fg\_completed\_qty”)).

**Local steps**

- Evaluate Platform.has\_permission(“Stock Entry”, “read”, doc = stock\_entry\_name, throw = true).
- Set se from Platform.db.get\_value(“Stock Entry”, stock\_entry\_name, list(“fg\_completed\_qty”), as\_dict = true).
- If not se.
  - Return 0.0.
- Set filters from mapping(“source\_stock\_entry” → stock\_entry\_name, “purpose” → “Disassemble”, “docstatus” → 1).
- If current\_se\_name.
  - Set filters at “name” from tuple(“!=”, current\_se\_name).
- Set already\_disassembled from flt(Platform.db.get\_value(“Stock Entry”, filters, list(mapping(“SUM” → “fg\_completed\_qty”)))).
- Return flt((flt(se.fg\_completed\_qty) − already\_disassembled), Platform.get\_precision(“Stock Entry”, “fg\_completed\_qty”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Entry”, “read”, doc = stock\_entry\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L783)

<a id="op-6cd6acda5354ed"></a>
### Get default warehouse

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_get_default_warehouse`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** mapping(“wip\_warehouse” → wip, “fg\_warehouse” → fg, “scrap\_warehouse” → scrap).

**Local steps**

- Evaluate require\_permission(“Company”, company, “select”).
- Set tuple(wip, fg, scrap) from Platform.get\_cached\_value(“Company”, company, list(“default\_wip\_warehouse”, “default\_fg\_warehouse”, “default\_scrap\_warehouse”)).
- Return mapping(“wip\_warehouse” → wip, “fg\_warehouse” → fg, “scrap\_warehouse” → scrap).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“default\_wip\_warehouse”, “default\_fg\_warehouse”, “default\_scrap\_warehouse”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L782)

<a id="op-e3f31ccb6c3843"></a>
### Distribute transfers over rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_distribute_transfers_over_rows`

**Inputs** rows, qty\_by\_item\_warehouse\_and\_operation.

**Explicit results** qty\_by\_row.

**Local steps**

- Set rows\_by\_item from mapping().
- For each row in rows.
  - Evaluate rows\_by\_item.setdefault(row.item\_code, list()).append(row).
- Set qty\_by\_row from mapping of row.name → 0.0 for row drawn from rows.
  - Draw row from rows.
- For each tuple(key, qty) in qty\_by\_item\_warehouse\_and\_operation.items().
  - Set tuple(item\_code, warehouse, operation\_row\_id, operation) from key.
  - Set item\_rows from rows\_by\_item.get(item\_code).
  - If not item\_rows.
    - Continue with the next iteration or loop test.
  - If operation.
    - Set job\_card\_operation from Platform.\_dict(operation\_row\_id = operation\_row\_id, operation = operation).
    - Set item\_rows from (list of row for row drawn from item\_rows where is\_row\_of\_operation(row, job\_card\_operation) or item\_rows).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of row for row drawn from item\_rows where is\_row\_of\_operation(row, job\_card\_operation) → item\_rows.
      - Draw row from item\_rows, keep a combination only if (is\_row\_of\_operation(row, job\_card\_operation)).
  - Set share\_by\_row from mapping().
  - Set matching\_rows from (list of row for row drawn from item\_rows where row.source\_warehouse equals warehouse or item\_rows).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of row for row drawn from item\_rows where row.source\_warehouse equals warehouse → item\_rows.
    - Draw row from item\_rows, keep a combination only if (row.source\_warehouse equals warehouse).
  - Evaluate split\_item\_qty(matching\_rows, flt(qty), share\_by\_row).
  - For each tuple(name, share) in share\_by\_row.items().
    - Update qty\_by\_row at name using + share.
- Return qty\_by\_row.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L997)

<a id="op-973563a2fbb040"></a>
### Is row of operation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_is_row_of_operation`

**Inputs** row, operation.

**Explicit results** cint(row.operation\_row\_id) equals cint(operation.operation\_row\_id) · (not row.operation or row.operation equals operation.operation).

**Local steps**

- If (cint(row.operation\_row\_id) and cint(operation.operation\_row\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(row.operation\_row\_id) → cint(operation.operation\_row\_id).
  - Return cint(row.operation\_row\_id) equals cint(operation.operation\_row\_id).
- Return (not row.operation or row.operation equals operation.operation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.operation → row.operation equals operation.operation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L10) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1020)

<a id="op-97be11c710403e"></a>
### Distribute over rows

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_distribute_over_rows`

**Inputs** rows, qty\_by\_item.

**Explicit results** qty\_by\_row.

**Local steps**

- Set rows\_by\_item from mapping().
- For each row in rows.
  - Evaluate rows\_by\_item.setdefault(row.item\_code, list()).append(row).
- Set qty\_by\_row from mapping().
- For each tuple(item\_code, item\_rows) in rows\_by\_item.items().
  - Evaluate split\_item\_qty(item\_rows, flt(qty\_by\_item.get(item\_code)), qty\_by\_row).
- Return qty\_by\_row.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L996)

<a id="op-da84811c9f201c"></a>
### Get allowed transfer qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_allowed_transfer_qty`

**Inputs** required\_qty.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** (flt(required\_qty) + ((flt(required\_qty) × extra\_pct) ÷ 100)).

**Local steps**

- Set extra\_pct from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”)).
- Return (flt(required\_qty) + ((flt(required\_qty) × extra\_pct) ÷ 100)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “transfer\_extra\_materials\_percentage”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1000)

<a id="op-e4168cdb9367d7"></a>
### Split item qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_split_item_qty`

**Inputs** rows, qty, qty\_by\_row.

**Local steps**

- Set required\_qty from sum(generator of flt(row.required\_qty) for row drawn from rows).
  - Draw row from rows.
- Set remaining\_qty from qty.
- For each row in rows at slice no value to negative 1.
  - Set share from ((qty × flt(row.required\_qty)) ÷ required\_qty) when required\_qty, otherwise 0.0.
    - Value choice on required\_qty — true gives ((qty × flt(row.required\_qty)) ÷ required\_qty), false gives 0.0.
  - Set qty\_by\_row at row.name from share.
  - Update remaining\_qty using − share.
- Set qty\_by\_row at rows at negative 1.name from remaining\_qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1035)

<a id="op-fd9ce9ac2e0e66"></a>
### Is edited item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_is_edited_item`

**Inputs** row, previous\_items, bom\_items.

**Explicit results** previous\_items at row.name differs from row.item\_code · (not row.rate or not find\_bom\_item(bom\_items, row)).

**Local steps**

- If row.name belongs to previous\_items.
  - Return previous\_items at row.name differs from row.item\_code.
- Return (not row.rate or not find\_bom\_item(bom\_items, row)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.rate → not find\_bom\_item(bom\_items, row).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1019)

<a id="op-664c6a3cfffe6d"></a>
### Find bom item

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_find_bom_item`

**Inputs** item\_dict, row.

**Explicit results** item\_dict at key.

**Local steps**

- For each key in tuple(tuple(row.item\_code, row.operation), tuple(row.item\_code, row.operation\_row\_id), row.item\_code).
  - If key belongs to item\_dict.
    - Return item\_dict at key.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L999)

<a id="op-42f4d06d135d00"></a>
### Get batch size flags

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_batch_size_flags`

**Inputs** operation\_names.

**Record and data access** read “Operation” via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(“Operation”, filters = mapping(“name” → list(“in”, list(names))), fields = list(“name”, “create\_job\_card\_based\_on\_batch\_size”), as\_list = true, limit\_page\_length = 0)).

**Local steps**

- Set names from set of name for name drawn from operation\_names where name.
  - Draw name from operation\_names, keep a combination only if (name).
- If not names.
  - Return mapping().
- Return dict(Platform.get\_all(“Operation”, filters = mapping(“name” → list(“in”, list(names))), fields = list(“name”, “create\_job\_card\_based\_on\_batch\_size”), as\_list = true, limit\_page\_length = 0)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1001)

<a id="op-d83825658ecc4b"></a>
### Get operation time per unit

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_operation_time_per_unit`

**Inputs** d, qty, units, exploded, batch\_size\_flags.

**Explicit results** ((d.time\_in\_mins × flt(units)) ÷ flt(d.batch\_size)) · (d.time\_in\_mins × flt(qty)) when exploded, otherwise (d.time\_in\_mins ÷ flt(qty)).

**Local steps**

- If (batch\_size\_flags.get(d.operation) and flt(d.batch\_size)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_size\_flags.get(d.operation) → flt(d.batch\_size).
  - Return ((d.time\_in\_mins × flt(units)) ÷ flt(d.batch\_size)).
- Return (d.time\_in\_mins × flt(qty)) when exploded, otherwise (d.time\_in\_mins ÷ flt(qty)).
  - Value choice on exploded — true gives (d.time\_in\_mins × flt(qty)), false gives (d.time\_in\_mins ÷ flt(qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1008)

<a id="op-1bb65b3bfac37c"></a>
### Qty against sales order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_qty_against_sales_order`

**Inputs** wo, plan\_item.

**Explicit results** Case().when(wo.status equals “Closed”, wo.produced\_qty).else\_(output\_qty).

**Local steps**

- Set loss\_percentage from IfNull(plan\_item.process\_loss\_percentage, 0).
- Set planned\_loss\_qty from ((wo.qty × loss\_percentage) ÷ 100).
- Set loss\_qty from Case().when(wo.process\_loss\_qty &gt; planned\_loss\_qty, wo.process\_loss\_qty).else\_(planned\_loss\_qty).
- Set output\_qty from Case().when(wo.produced\_qty &gt; (wo.qty − loss\_qty), wo.produced\_qty).else\_((wo.qty − loss\_qty)).
- Return Case().when(wo.status equals “Closed”, wo.produced\_qty).else\_(output\_qty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L20) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1030)

<a id="op-fc628a296e6707"></a>
### Validate status change

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_validate_status_change`

**Inputs** work\_order, status, allowed\_statuses.

**Explicit failure paths** validation helper — translated “Work Order status cannot be set to {0}”.format(Platform.bold(status)) · validation helper — translated “Only a submitted Work Order can be closed, stopped or resumed”.

**Local steps**

- If status does not belong to allowed\_statuses.
  - Call the validation error handler Platform.throw(translated “Work Order status cannot be set to {0}”.format(Platform.bold(status))).
- <a id="op-fc628a296e6707-guard-5"></a>If work\_order.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Work Order can be closed, stopped or resumed”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison work\_order.docstatus differs from 1, work\_order.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Work Order can be closed, stopped or resumed”. With work\_order.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fc628a296e6707-guard-5)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L30) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1040)

<a id="op-9ffe0320c08a1c"></a>
### Stop unstop

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_stop_unstop`

**Inputs** work\_order, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** msgprint with translated “Work Order has been {0}”.format(status).

**Explicit results** pro\_order.status.

**Explicit failure paths** validation helper — translated “Closed Work Order can not be stopped or Re-opened”.

**Local steps**

- Evaluate Platform.has\_permission(“Work Order”, “write”, throw = true).
- Set pro\_order from Platform.get\_doc(“Work Order”, work\_order, check\_permission = “write”).
- Evaluate validate\_status\_change(pro\_order, status, tuple(“Stopped”, “Resumed”)).
- If pro\_order.status equals “Closed”.
  - Call the validation error handler Platform.throw(translated “Closed Work Order can not be stopped or Re-opened”).
- Evaluate pro\_order.update\_status(status).
- Evaluate pro\_order.update\_planned\_qty().
- Evaluate Platform.msgprint(translated “Work Order has been {0}”.format(status)).
- Evaluate pro\_order.notify\_update().
- Return pro\_order.status.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L786)

<a id="op-60c135ed7ba806"></a>
### Query sales order

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_query_sales_order`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list at str.

**Record and data access** read “Sales Order” via get\_list.

**Explicit results** Platform.get\_list(“Sales Order”, fields = list(“name”), filters = list(list(“Sales Order”, “docstatus”, “=”, 1)), or\_filters = list(list(“Sales Order Item”, “item\_code”, “=”, filters.get(“production\_item”) ….

**Local steps**

- Return Platform.get\_list(“Sales Order”, fields = list(“name”), filters = list(list(“Sales Order”, “docstatus”, “=”, 1)), or\_filters = list(list(“Sales Order Item”, “item\_code”, “=”, filters.get(“production\_item”) ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L784)

<a id="op-a8a8f6d0110634"></a>
### Make job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_make_job_card`

**Inputs** work\_order, operations, parent\_bom = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- If isinstance(operations, str).
  - Set operations from json.loads(operations).
- Set work\_order from Platform.get\_doc(“Work Order”, work\_order).
- For each row in operations.
  - Set row from Platform.\_dict(row).
  - Evaluate row.update(get\_operation\_details(row.name, work\_order, parent\_bom)).
  - Evaluate validate\_operation\_data(row).
  - Set qty from row.get(“qty”).
  - While qty &gt; 0.
    - Set qty from split\_qty\_based\_on\_batch\_size(work\_order, row, qty).
    - If row.job\_card\_qty &gt; 0.
      - Evaluate create\_job\_card(work\_order, row, auto\_create = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L11) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1021)

<a id="op-972f622d1c2470"></a>
### Get operation details

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_operation_details`

**Inputs** name, work\_order, parent\_bom.

**Explicit results** mapping(“idx” → row.idx, “workstation” → row.workstation, “workstation\_type” → row.workstation\_type, “source\_warehouse” → row.source\_warehouse, …).

**Local steps**

- For each row in work\_order.operations.
  - If row.name equals name.
    - Return mapping(“idx” → row.idx, “workstation” → row.workstation, “workstation\_type” → row.workstation\_type, “source\_warehouse” → row.source\_warehouse, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“bom\_no”) → parent\_bom.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1005)

<a id="op-c9028b2517653b"></a>
### Close work order

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_close_work_order`

**Inputs** work\_order, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Job Card” via get\_list.

**State and service calls** msgprint with translated “Work Order has been {0}”.format(status).

**Explicit results** work\_order.status.

**Explicit failure paths** validation helper — translated “Work Order {0} is already Closed”.format(work\_order.name) · validation helper — translated “Can not close Work Order. Since {0} Job Cards are in Work In Progress state.”.format(job\_cards).

**Local steps**

- Evaluate Platform.has\_permission(“Work Order”, “write”, throw = true).
- Set work\_order from Platform.get\_doc(“Work Order”, work\_order, check\_permission = “write”).
- Evaluate validate\_status\_change(work\_order, status, tuple(“Closed”)).
- If work\_order.status equals “Closed”.
  - Call the validation error handler Platform.throw(translated “Work Order {0} is already Closed”.format(work\_order.name)).
- If work\_order.get(“operations”).
  - Set job\_cards from Platform.get\_list(“Job Card”, filters = mapping(“work\_order” → work\_order.name, “status” → “Work In Progress”, “docstatus” → 1), pluck = “name”).
  - If job\_cards.
    - Set job\_cards from “, ”.join(job\_cards).
    - Call the validation error handler Platform.throw(translated “Can not close Work Order. Since {0} Job Cards are in Work In Progress state.”.format(job\_cards)).
- Evaluate work\_order.update\_status(status).
- Evaluate work\_order.on\_close\_or\_cancel().
- Evaluate Platform.msgprint(translated “Work Order has been {0}”.format(status)).
- Evaluate work\_order.notify\_update().
- Return work\_order.status.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Work Order”, “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L780)
