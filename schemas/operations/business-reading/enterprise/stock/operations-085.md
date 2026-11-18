# Inventory and warehouses · operations 85

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-fb96c4125d6ae8"></a>
### Get valuation rate for finished good entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_valuation_rate_for_finished_good_entry`

**Inputs** work\_order.

**Record and data access** read “Work Order” via get\_cached\_value · read “Stock Entry” via get\_all.

**Explicit results** stock\_data at 0.valuation\_rate.

**Local steps**

- Set work\_order\_qty from flt(Platform.get\_cached\_value(“Work Order”, work\_order, “material\_transferred\_for\_manufacturing”)).
- Set field from (“(SUM(total\_outgoing\_value) / %s) as valuation\_rate” modulo or format work\_order\_qty).
- Set stock\_data from Platform.get\_all(“Stock Entry”, fields = field, filters = mapping(“docstatus” → 1, “purpose” → “Material Transfer for Manufacture”, “work\_order” → work\_order)).
- If stock\_data.
  - Return stock\_data at 0.valuation\_rate.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, work\_order, “material\_transferred\_for\_manufacturing”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L655)

<a id="op-744e7b91fdd98a"></a>
### Get uom details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_unit_of_measure_details`

**Inputs** item\_code, uom, qty.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “UOM conversion factor required for UOM: {0} in Item: {1}”.format(uom, item\_code).

**Explicit results** ret.

**Local steps**

- Set conversion\_factor from get\_conversion\_factor(item\_code, uom).get(“conversion\_factor”).
- If not conversion\_factor.
  - Evaluate Platform.msgprint(translated “UOM conversion factor required for UOM: {0} in Item: {1}”.format(uom, item\_code)).
  - Set ret from mapping(“uom” → empty text).
- Otherwise.
  - Set ret from mapping(“conversion\_factor” → flt(conversion\_factor), “transfer\_qty” → (flt(qty) × flt(conversion\_factor))).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L758)

<a id="op-04e3923b134e31"></a>
### Get expired batch items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_expired_batch_items`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_list.

**Explicit results** list() · list of row for row drawn from expired\_batches\_stock where row.warehouse belongs to permitted\_warehouses.

**Local steps**

- Bind dependencies get\_auto\_batch\_nos.
- Evaluate Platform.has\_permission(“Batch”, “read”, throw = true).
- Set expired\_batches from get\_expired\_batches().
- If not expired\_batches.
  - Return list().
- Set expired\_batches\_stock from get\_auto\_batch\_nos(Platform.\_dict(mapping(“batch\_no” → list(expired\_batches.keys()), “for\_stock\_levels” → true))).
- For each row in expired\_batches\_stock.
  - Evaluate row.update(expired\_batches.get(row.batch\_no)).
- Set permitted\_warehouses from set(Platform.get\_list(“Warehouse”, filters = mapping(“name” → tuple(“in”, list(set of nested operand in the contract.warehouse for row drawn from expired\_batches\_stock))), pluck = “name”)).
  - Draw row from expired\_batches\_stock.
- Return list of row for row drawn from expired\_batches\_stock where row.warehouse belongs to permitted\_warehouses.
  - Draw row from expired\_batches\_stock, keep a combination only if (row.warehouse belongs to permitted\_warehouses).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “read”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L635)

<a id="op-de748641320491"></a>
### Is row of job card operation

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_is_row_of_job_card_operation`

**Inputs** row, operation.

**Explicit results** true · cint(row.operation\_row\_id) equals cint(operation.operation\_row\_id) · (not row.operation or row.operation equals operation.operation).

**Local steps**

- If not operation.
  - Return true.
- If (cint(row.operation\_row\_id) and cint(operation.operation\_row\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(row.operation\_row\_id) → cint(operation.operation\_row\_id).
  - Return cint(row.operation\_row\_id) equals cint(operation.operation\_row\_id).
- Return (not row.operation or row.operation equals operation.operation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.operation → row.operation equals operation.operation.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L657)

<a id="op-1ff3c97428f5a9"></a>
### Get outward rows

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_outward_rows`

**Inputs** ste\_details.

**Record and data access** read “Stock Entry Detail” via get\_all.

**Explicit results** mapping of row.name → row for row drawn from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“name” → tuple(“in”, ste\_details)), fields = list(“name”, “item\_code”, “t\_warehouse”, “transfer\_qty”)).

**Local steps**

- Return mapping of row.name → row for row drawn from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“name” → tuple(“in”, ste\_details)), fields = list(“name”, “item\_code”, “t\_warehouse”, “transfer\_qty”)).
  - Draw row from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“name” → tuple(“in”, ste\_details)), fields = list(“name”, “item\_code”, “t\_warehouse”, “transfer\_qty”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L644)

<a id="op-7a1c3c5bd88a4a"></a>
### Get transferred qty map

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_transferred_qty_map`

**Inputs** ste\_details.

**Explicit results** dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(sed.ste\_detail).run()).

**Local steps**

- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Return dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(sed.ste\_detail).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L654)

<a id="op-d03e7a60a4fb7d"></a>
### Get expired batches

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_expired_batches`

**Inputs** no declared parameters.

**Record and data access** read “Batch” via get\_list.

**Explicit results** list() · expired\_batches.

**Local steps**

- Set data from Platform.get\_list(“Batch”, filters = list(list(“expiry\_date”, “&lt;”, nowdate()), list(“expiry\_date”, “is”, “set”), list(“disabled”, “=”, 0)), fields = list(“item”, “name as batch\_no”, “stock\_uom”), limit\_pag ….
- If not data.
  - Return list().
- Set expired\_batches from Platform.\_dict().
- For each row in data.
  - Set expired\_batches at row.batch\_no from row.
- Return expired\_batches.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L636)

<a id="op-90e4f209ea2abf"></a>
### Get warehouse details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_get_warehouse_details`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** ret.

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from Platform.\_dict(args).
- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- Evaluate Platform.has\_permission(“Stock Entry”, “read”, throw = true).
- If args.warehouse.
  - Evaluate check\_stock\_entry\_warehouse\_permission(args.warehouse).
- Set ret from mapping().
- If (args.warehouse and args.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.warehouse → args.item\_code.
  - Evaluate args.update(mapping(“posting\_date” → args.posting\_date, “posting\_time” → args.posting\_time)).
  - Set ret from mapping(“actual\_qty” → (get\_previous\_sle(args).get(“qty\_after\_transaction”) or 0), “basic\_rate” → \_get\_incoming\_rate(args)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_previous\_sle(args).get(“qty\_after\_transaction”) → 0.
- Return ret.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true), Platform.has\_permission(“Stock Entry”, “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L760)

<a id="op-afedfaff8f5759"></a>
### Check stock entry warehouse permission

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_check_stock_entry_warehouse_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** warehouse.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L623)

<a id="op-aafff6e7fa432c"></a>
### Validate sample quantity

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_validate_sample_quantity`

**Inputs** item\_code, sample\_quantity, qty, company, batch\_no = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value.

**State and service calls** msgprint with translated “Maximum Samples - {0} have already been retained for Batch {1} and Item {2} in Batch {3}.”.format(retainted\_qty, batch\_no, item\_code, batch\_no) · msgprint with message.

**Explicit results** sample\_quantity.

**Explicit failure paths** validation helper — translated “Sample quantity {0} cannot be more than received quantity {1}”.format(sample\_quantity, qty).

**Local steps**

- If cint(qty) &lt; cint(sample\_quantity).
  - Call the validation error handler Platform.throw(translated “Sample quantity {0} cannot be more than received quantity {1}”.format(sample\_quantity, qty)).
- Set retention\_warehouse from get\_sample\_retention\_warehouse(company).
- Set retainted\_qty from 0.
- If batch\_no.
  - Set retainted\_qty from get\_batch\_qty(batch\_no, retention\_warehouse, item\_code).
- Set max\_retain\_qty from Platform.get\_value(“Item”, item\_code, “sample\_quantity”).
- If retainted\_qty ≥ max\_retain\_qty.
  - Evaluate Platform.msgprint(translated “Maximum Samples - {0} have already been retained for Batch {1} and Item {2} in Batch {3}.”.format(retainted\_qty, batch\_no, item\_code, batch\_no), alert = true).
  - Set sample\_quantity from 0.
- Set qty\_diff from (max\_retain\_qty − retainted\_qty).
- If cint(sample\_quantity) &gt; cint(qty\_diff).
  - If batch\_no.
    - Set message from translated “Maximum Samples - {0} can be retained for Batch {1} and Item {2}.”.format(max\_retain\_qty, batch\_no, item\_code).
  - Otherwise.
    - Set message from translated “Maximum Samples - {0} can be retained for Item {1}.”.format(max\_retain\_qty, item\_code).
  - Evaluate Platform.msgprint(message, alert = true).
  - Set sample\_quantity from qty\_diff.
- Return sample\_quantity.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L784)

<a id="op-3f194e3cb96d21"></a>
### Get sample retention warehouse

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_sample_retention_warehouse`

**Inputs** company.

**Declared result** str.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** warehouse.

**Explicit failure paths** validation helper — translated “Please set {0} in Company {1} to retain samples.”.format(bold(translated “Sample Retention Warehouse”), bold(company)).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
- Set warehouse from Platform.get\_cached\_value(“Company”, company, “sample\_retention\_warehouse”).
- If not warehouse.
  - Call the validation error handler Platform.throw(translated “Please set {0} in Company {1} to retain samples.”.format(bold(translated “Sample Retention Warehouse”), bold(company)), title = translated “Sample Retention Warehouse Missing”).
- Return warehouse.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “sample\_retention\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L648)

<a id="op-dbb57cba5da00b"></a>
### Get supplied items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_supplied_items`

**Inputs** subcontract\_order, rm\_detail\_field = “sco\_rm\_detail”, subcontract\_order\_field = “subcontracting\_order”.

**Record and data access** read “Stock Entry” via get\_all.

**Explicit results** supplied\_item\_details.

**Local steps**

- Set fields from list(“′tabStock Entry Detail′.′transfer\_qty′”, “′tabStock Entry′.′is\_return′”, formatted text ′tabStock Entry Detail′.′{rm\_detail\_field}′, “′tabStock Entry Detail′.′item\_code′”).
- Set filters from list(list(“Stock Entry”, “docstatus”, “=”, 1), list(“Stock Entry”, subcontract\_order\_field, “=”, subcontract\_order)).
- Set supplied\_item\_details from mapping().
- For each row in Platform.get\_all(“Stock Entry”, fields = fields, filters = filters).
  - If not row.get(rm\_detail\_field).
    - Continue with the next iteration or loop test.
  - Set key from row.get(rm\_detail\_field).
  - If key does not belong to supplied\_item\_details.
    - Evaluate supplied\_item\_details.setdefault(key, Platform.\_dict(mapping(“supplied\_qty” → 0, “returned\_qty” → 0, “total\_supplied\_qty” → 0))).
  - Set supplied\_item from supplied\_item\_details at key.
  - If row.is\_return.
    - Update supplied\_item.returned\_qty using + row.transfer\_qty.
  - Otherwise.
    - Update supplied\_item.supplied\_qty using + row.transfer\_qty.
  - Set supplied\_item.total\_supplied\_qty from (flt(supplied\_item.supplied\_qty) − flt(supplied\_item.returned\_qty)).
- Return supplied\_item\_details.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L652)

<a id="op-9a9cafa2e69488"></a>
### Get items from subcontract order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_items_from_subcontract_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from json.loads(target\_doc) via get\_doc.

**Explicit results** target\_doc.

**Local steps**

- Bind dependencies make\_rm\_stock\_entry.
- If isinstance(target\_doc, str).
  - Set target\_doc from Platform.get\_doc(json.loads(target\_doc)).
- Set order\_doctype from “Purchase Order” when target\_doc.purchase\_order, otherwise “Subcontracting Order”.
  - Value choice on target\_doc.purchase\_order — true gives “Purchase Order”, false gives “Subcontracting Order”.
- Set target\_doc from make\_rm\_stock\_entry(subcontract\_order = source\_name, order\_doctype = order\_doctype, target\_doc = target\_doc).
- Return target\_doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L641)

<a id="op-e847562a613d08"></a>
### Get available materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_available_materials`

**Inputs** work\_order, stock\_entry\_doc = no value.

**Declared result** dict.

**Explicit results** available\_materials.

**Local steps**

- Set data from get\_stock\_entry\_data(work\_order, stock\_entry\_doc = stock\_entry\_doc).
- Set is\_disassemble from (stock\_entry\_doc and stock\_entry\_doc.purpose equals “Disassemble”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry\_doc → stock\_entry\_doc.purpose equals “Disassemble”.
- Set available\_materials from mapping().
- For each row in data.
  - Set key from tuple(row.item\_code, row.warehouse).
  - If (row.purpose differs from “Material Transfer for Manufacture” or row.is\_return).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.purpose differs from “Material Transfer for Manufacture” → row.is\_return.
    - Set key from tuple(row.item\_code, row.s\_warehouse).
  - If is\_disassemble.
    - Set key from \_get\_disassembly\_material\_key(row).
  - Set key from tuple(expanded key, no value when is\_disassemble, otherwise (row.original\_item or no value)).
    - Value choice on is\_disassemble — true gives no value, false gives (row.original\_item or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → no value.
  - If ((row.purpose equals “Material Transfer for Manufacture” and not row.is\_return) or (is\_disassemble and row.purpose equals “Manufacture”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (row.purpose equals “Material Transfer for Manufacture” and not row.is\_return) → (is\_disassemble and row.purpose equals “Manufacture”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.purpose equals “Material Transfer for Manufacture” → not row.is\_return.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_disassemble → row.purpose equals “Manufacture”.
    - Set item\_data from \_get\_available\_material(available\_materials, key, row).
    - Update item\_data.qty using + row.qty.
    - If row.batch\_no.
      - Update item\_data.batch\_details at row.batch\_no using + row.qty.
    - Otherwise.
      - If row.batch\_nos.
        - For each tuple(batch\_no, qty) in row.batch\_nos.items().
          - Update item\_data.batch\_details at batch\_no using + abs(qty).
    - If row.serial\_no.
      - Evaluate item\_data.serial\_nos.extend(get\_serial\_nos(row.serial\_no)).
      - Evaluate item\_data.serial\_nos.sort().
    - Otherwise.
      - If row.serial\_nos.
        - Evaluate item\_data.serial\_nos.extend(get\_serial\_nos(row.serial\_nos)).
        - Evaluate item\_data.serial\_nos.sort().
  - Otherwise.
    - Set buckets from (\_get\_consumption\_buckets(available\_materials, key) or list(\_get\_available\_material(available\_materials, key, row))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_consumption\_buckets(available\_materials, key) → list(\_get\_available\_material(available\_materials, key, row)).
    - Set available\_qty from list of bucket.qty for bucket drawn from buckets.
      - Draw bucket from buckets.
    - Evaluate \_deduct\_consumed\_material(buckets, row).
    - If row.purpose differs from “Material Transfer for Manufacture”.
      - For each tuple(bucket, qty) in zip(buckets, available\_qty, strict = true).
        - If bucket.qty differs from qty.
          - Set bucket.consumed\_for at row.name from flt(row.fg\_completed\_qty).
- Return available\_materials.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L630)

<a id="op-5ba6eccca00584"></a>
### Get disassembly material key

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_disassembly_material_key`

**Inputs** row.

**Explicit results** tuple(row.item\_code, no value) · tuple(row.item\_code, (row.s\_warehouse or row.warehouse)).

**Local steps**

- If row.purpose equals “Manufacture”.
  - Set is\_component from bool(row.s\_warehouse).
- Otherwise.
  - Set is\_component from not row.s\_warehouse.
- If is\_component.
  - Return tuple(row.item\_code, no value).
- Return tuple(row.item\_code, (row.s\_warehouse or row.warehouse)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.s\_warehouse → row.warehouse.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L634)

<a id="op-7b90b68ce32b9a"></a>
### Get available material

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_available_material`

**Inputs** available\_materials, key, row.

**Explicit results** available\_materials at key.

**Local steps**

- If key does not belong to available\_materials.
  - Set available\_materials at key from Platform.\_dict(mapping(“item\_details” → row, “batch\_details” → defaultdict(float), “qty” → 0, “serial\_nos” → list(), …)).
- Return available\_materials at key.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L629)

<a id="op-84e3775133d87f"></a>
### Get consumption buckets

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_consumption_buckets`

**Inputs** available\_materials, key.

**Explicit results** list(available\_materials at key) · buckets.

**Local steps**

- If (key at 2 and key belongs to available\_materials).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key at 2 → key belongs to available\_materials.
  - Return list(available\_materials at key).
- Set buckets from list(available\_materials at key) when key belongs to available\_materials, otherwise list().
  - Value choice on key belongs to available\_materials — true gives list(available\_materials at key), false gives list().
- Evaluate buckets.extend(generator of bucket for tuple(material\_key, bucket) drawn from available\_materials.items() where (material\_key at slice no value to 2 equals key at slice no value to 2 and material\_key diffe ….
  - Draw tuple(material\_key, bucket) from available\_materials.items(), keep a combination only if ((material\_key at slice no value to 2 equals key at slice no value to 2 and material\_key differs from key)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in material\_key at slice no value to 2 equals key at slice no value to 2 → material\_key differs from key.
- Return buckets.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L633)

<a id="op-bc8c314baeea6a"></a>
### Deduct consumed material

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_deduct_consumed_material`

**Inputs** buckets, row.

**Local steps**

- Set consumed\_qty from flt(row.qty).
- Set batches from mapping(row.batch\_no → flt(row.qty)) when row.batch\_no, otherwise mapping of batch\_no → abs(flt(qty)) for tuple(batch\_no, qty) drawn from (row.batch\_nos or mapping()).items().
  - Value choice on row.batch\_no — true gives mapping(row.batch\_no → flt(row.qty)), false gives mapping of batch\_no → abs(flt(qty)) for tuple(batch\_no, qty) drawn from (row.batch\_nos or mapping()).items().
  - Draw tuple(batch\_no, qty) from (row.batch\_nos or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_nos → mapping().
- For each tuple(batch\_no, batch\_qty) in batches.items().
  - Evaluate \_deduct\_consumed\_batch\_qty(buckets, batch\_no, batch\_qty).
  - Update consumed\_qty using − batch\_qty.
- For each serial\_no in get\_serial\_nos((row.serial\_no or row.serial\_nos)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.serial\_nos.
  - Set bucket from next(generator of bucket for bucket drawn from buckets where serial\_no belongs to bucket.serial\_nos, no value).
    - Draw bucket from buckets, keep a combination only if (serial\_no belongs to bucket.serial\_nos).
  - If not bucket.
    - Continue with the next iteration or loop test.
  - Evaluate bucket.serial\_nos.remove(serial\_no).
  - If not batches.
    - Update bucket.qty using − 1.
    - Update consumed\_qty using − 1.
- Evaluate \_deduct\_consumed\_qty(buckets, consumed\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L626)

<a id="op-8c0064bda821dd"></a>
### Deduct consumed qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_deduct_consumed_qty`

**Inputs** buckets, consumed\_qty.

**Local steps**

- For each bucket in buckets at slice no value to negative 1.
  - Set deducted from min(max(flt(bucket.qty), 0.0), consumed\_qty).
  - Update bucket.qty using − deducted.
  - Update consumed\_qty using − deducted.
- Update buckets at negative 1.qty using − consumed\_qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L627)

<a id="op-9f99284f056c6c"></a>
### Deduct consumed batch qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_deduct_consumed_batch_qty`

**Inputs** buckets, batch\_no, consumed\_qty.

**Local steps**

- Set holders from (list of bucket for bucket drawn from buckets where batch\_no belongs to bucket.batch\_details or buckets at slice negative 1 to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of bucket for bucket drawn from buckets where batch\_no belongs to bucket.batch\_details → buckets at slice negative 1 to no value.
  - Draw bucket from buckets, keep a combination only if (batch\_no belongs to bucket.batch\_details).
- For each bucket in holders at slice no value to negative 1.
  - Set deducted from min(max(flt(bucket.batch\_details at batch\_no), 0.0), consumed\_qty).
  - Update bucket.batch\_details at batch\_no using − deducted.
  - Update bucket.qty using − deducted.
  - Update consumed\_qty using − deducted.
- Update holders at negative 1.batch\_details at batch\_no using − consumed\_qty.
- Update holders at negative 1.qty using − consumed\_qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L625)

<a id="op-051c896425cd14"></a>
### Get stock entry data

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_stock_entry_data`

**Inputs** work\_order, stock\_entry\_doc = no value.

**Explicit results** list() · data.

**Local steps**

- Bind dependencies get\_voucher\_wise\_serial\_batch\_from\_bundle.
- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set stock\_entry\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set data from nested operand in the contract(nested operand in the contract).select(stock\_entry\_detail.item\_name, stock\_entry\_detail.original\_item, stock\_entry\_detail.item\_code, nested operand in the contract.as\_(“qty”) ….
- If (stock\_entry\_doc and stock\_entry\_doc.purpose equals “Disassemble”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry\_doc → stock\_entry\_doc.purpose equals “Disassemble”.
  - Set data from data.where(stock\_entry.purpose.isin(list(“Disassemble”, “Manufacture”))).
  - Set data from data.where(stock\_entry.name differs from stock\_entry\_doc.name).
- Otherwise.
  - Set data from data.where(stock\_entry.purpose.isin(list(“Manufacture”, “Material Consumption for Manufacture”, “Material Transfer for Manufacture”))).
  - Set data from data.where(stock\_entry\_detail.s\_warehouse.isnotnull()).
- Set data from data.run(as\_dict = 1).
- If not data.
  - Return list().
- Set voucher\_nos from list of row.get(“name”) for row drawn from data where row.get(“name”).
  - Draw row from data, keep a combination only if (row.get(“name”)).
- If voucher\_nos.
  - Set bundle\_data from get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = voucher\_nos).
  - For each row in data.
    - Set key from tuple(row.item\_code, row.warehouse, row.name).
    - If (row.purpose differs from “Material Transfer for Manufacture” or row.is\_return).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.purpose differs from “Material Transfer for Manufacture” → row.is\_return.
      - Set key from tuple(row.item\_code, row.s\_warehouse, row.name).
    - If (stock\_entry\_doc and stock\_entry\_doc.purpose equals “Disassemble”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_entry\_doc → stock\_entry\_doc.purpose equals “Disassemble”.
      - Set key from tuple(row.item\_code, (row.s\_warehouse or row.warehouse), row.name).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.s\_warehouse → row.warehouse.
    - If bundle\_data.get(key).
      - Evaluate row.update(bundle\_data.get(key)).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L650)

<a id="op-c2fb2bd6666906"></a>
### Create serial and batch bundle

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_create_serial_and_batch_bundle`

**Inputs** parent\_doc, row, child, type\_of\_transaction = no value.

**Record and data access** read “Item” via get\_cached\_value · resolve a document from mapping(“doctype” → “Serial and Batch Bundle”, “voucher\_type” → “Stock Entry”, “company” → parent\_doc.company, “item\_code” → child.item\_code, …) via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value · doc.insert(ignore\_permissions = true).name.

**Local steps**

- Set item\_details from Platform.get\_cached\_value(“Item”, child.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If not (item\_details.has\_serial\_no or item\_details.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_serial\_no → item\_details.has\_batch\_no.
  - Return no value.
- If not type\_of\_transaction.
  - Set type\_of\_transaction from “Inward”.
- Set doc from Platform.get\_doc(mapping(“doctype” → “Serial and Batch Bundle”, “voucher\_type” → “Stock Entry”, “company” → parent\_doc.company, “item\_code” → child.item\_code, …)).
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- If (row.serial\_nos and row.batches\_to\_be\_consume).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_nos → row.batches\_to\_be\_consume.
  - Set doc.has\_serial\_no from 1.
  - Set doc.has\_batch\_no from 1.
  - Set batchwise\_serial\_nos from get\_batchwise\_serial\_nos(child.item\_code, row).
  - For each tuple(batch\_no, qty) in row.batches\_to\_be\_consume.items().
    - While flt(qty, precision) &gt; 0.
      - Update qty using − 1.
      - Evaluate doc.append(“entries”, mapping(“batch\_no” → batch\_no, “serial\_no” → batchwise\_serial\_nos.get(batch\_no).pop(0), “warehouse” → row.warehouse, “qty” → negative 1)).
- Otherwise.
  - If row.serial\_nos.
    - Set doc.has\_serial\_no from 1.
    - For each serial\_no in row.serial\_nos.
      - Evaluate doc.append(“entries”, mapping(“serial\_no” → serial\_no, “warehouse” → row.warehouse, “qty” → negative 1)).
  - Otherwise.
    - If row.batches\_to\_be\_consume.
      - Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
      - Set doc.has\_batch\_no from 1.
      - For each tuple(batch\_no, qty) in row.batches\_to\_be\_consume.items().
        - If flt(qty, precision) &gt; 0.
          - Set qty from flt(qty, precision).
          - Evaluate doc.append(“entries”, mapping(“batch\_no” → batch\_no, “warehouse” → row.warehouse, “qty” → (qty × negative 1))).
- If not doc.entries.
  - Return no value.
- Return doc.insert(ignore\_permissions = true).name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, child.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L624)

<a id="op-8991c4a67e87b7"></a>
### Get batchwise serial nos

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_batchwise_serial_nos`

**Inputs** item\_code, row.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** batchwise\_serial\_nos.

**Local steps**

- Set batchwise\_serial\_nos from mapping().
- For each batch\_no in row.batches\_to\_be\_consume.
  - Set serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“item\_code” → item\_code, “batch\_no” → batch\_no, “name” → tuple(“in”, row.serial\_nos))).
  - If serial\_nos.
    - Set batchwise\_serial\_nos at batch\_no from sorted(list of serial\_no.name for serial\_no drawn from serial\_nos).
      - Draw serial\_no from serial\_nos.
- Return batchwise\_serial\_nos.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L631)

<a id="op-cd94d3b31c66f1"></a>
### Get transferred qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_transferred_qty`

**Inputs** material\_request.

**Explicit results** query at 0.

**Local steps**

- Bind dependencies Case.
- Set se from DocType(“Stock Entry”).
- Set sed from DocType(“Stock Entry Detail”).
- Set completed\_qty from Case().when(se.add\_to\_transit equals 1, sed.transferred\_qty).else\_(sed.transfer\_qty).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“transfer\_qty”), nested operand in the contract.as\_(“transferred\_qty”)).where((sed.material\_request  ….
- Return query at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L653)
