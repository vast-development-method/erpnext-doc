# Inventory and warehouses · operations 86

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-3fcbba44027db6"></a>
### Get previous operation output sn batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_previous_operation_output_sn_batch`

**Inputs** work\_order, item\_code, warehouse.

**Record and data access** read “Work Order Operation” via exists · read “Item” via get\_cached\_value.

**Explicit results** result.

**Local steps**

- Set result from Platform.\_dict(serial\_nos = list(), batches = defaultdict(float)).
- If not (work\_order and item\_code and warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order → item\_code → warehouse.
  - Return result.
- If not Platform.db.exists(“Work Order Operation”, mapping(“parent” → work\_order, “finished\_good” → item\_code)).
  - Return result.
- Set item\_details from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If (not item\_details or not (item\_details.has\_serial\_no or item\_details.has\_batch\_no)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_details → not (item\_details.has\_serial\_no or item\_details.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_serial\_no → item\_details.has\_batch\_no.
  - Return result.
- Set produced from \_get\_operation\_sn\_batch(work\_order, item\_code, warehouse, produced = true).
- Set consumed from \_get\_operation\_sn\_batch(work\_order, item\_code, warehouse, produced = false).
- For each serial\_no in produced.serial\_nos.
  - If serial\_no does not belong to consumed.serial\_nos.
    - Evaluate result.serial\_nos.append(serial\_no).
- For each tuple(batch\_no, qty) in produced.batches.items().
  - Set available from (flt(qty) − flt(consumed.batches.get(batch\_no))).
  - If available &gt; 0.
    - Set result.batches at batch\_no from available.
- Return result.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L646)

<a id="op-b4d70b5bbb2599"></a>
### Get operation sn batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_operation_sn_batch`

**Inputs** work\_order, item\_code, warehouse, produced = true.

**Explicit results** result.

**Local steps**

- Set bundles from \_get\_operation\_bundles(work\_order, item\_code, warehouse, produced).
- Set result from Platform.\_dict(serial\_nos = list(), batches = defaultdict(float)).
- If not bundles.
  - Return result.
- Set sbe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set entries from nested operand in the contract(nested operand in the contract).orderby(sbe.parent).orderby(sbe.idx).run(as\_dict = true).
- For each row in entries.
  - If row.serial\_no.
    - Evaluate result.serial\_nos.append(row.serial\_no).
  - If row.batch\_no.
    - Update result.batches at row.batch\_no using + abs(flt(row.qty)).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L643)

<a id="op-761101c68567ef"></a>
### Get operation bundles

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_operation_bundles`

**Inputs** work\_order, item\_code, warehouse, produced.

**Explicit results** list of row at 0 for row drawn from query.run().

**Local steps**

- Set se from Platform.qb.DocType(“Stock Entry”).
- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set warehouse\_field from sed.t\_warehouse when produced, otherwise sed.s\_warehouse.
  - Value choice on produced — true gives sed.t\_warehouse, false gives sed.s\_warehouse.
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(sed.serial\_and\_batch\_bundle).where(((((nested oper ….
- If produced.
  - Set query from query.where((se.purpose equals “Manufacture” bitwise and sed.is\_finished\_item equals 1)).
- Return list of row at 0 for row drawn from query.run().
  - Draw row from query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L642)

<a id="op-438416e9013e1e"></a>
### Cap pool to qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_cap_pool_to_qty`

**Inputs** pool, qty.

**Explicit results** tuple(serial\_nos, batches).

**Local steps**

- Set tuple(serial\_nos, batches) from tuple(list(), Platform.\_dict()).
- If pool.serial\_nos.
  - Set serial\_nos from pool.serial\_nos at slice no value to cint(qty).
- Otherwise.
  - If pool.batches.
    - Set remaining from flt(qty).
    - For each tuple(batch\_no, batch\_qty) in pool.batches.items().
      - If remaining ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set use from min(flt(batch\_qty), remaining).
      - Set batches at batch\_no from use.
      - Update remaining using − use.
- Return tuple(serial\_nos, batches).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L622)

<a id="op-956eef0d79f201"></a>
### Set previous operation serial batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_set_previous_operation_serial_batch`

**Inputs** parent\_doc, row.

**Explicit results** no value.

**Local steps**

- Set warehouse from (row.get(“s\_warehouse”) or row.get(“from\_warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“s\_warehouse”) → row.get(“from\_warehouse”).
- Set qty from (flt(row.get(“qty”)) × flt((row.get(“conversion\_factor”) or 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“conversion\_factor”) → 1.
- If (not parent\_doc.get(“work\_order”) or not warehouse or qty ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent\_doc.get(“work\_order”) → not warehouse → qty ≤ 0.
  - Return no value.
- If (row.get(“serial\_and\_batch\_bundle”) or row.get(“serial\_no”) or row.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“serial\_and\_batch\_bundle”) → row.get(“serial\_no”) → row.get(“batch\_no”).
  - Return no value.
- Set pool from get\_previous\_operation\_output\_sn\_batch(parent\_doc.work\_order, row.item\_code, warehouse).
- Set tuple(serial\_nos, batches) from \_cap\_pool\_to\_qty(pool, qty).
- If (not serial\_nos and not batches).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → not batches.
  - Return no value.
- Set bundle from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → warehouse, “posting\_datetime” → get\_combine\_datetime(parent\_doc.posting\_date, parent\_doc.posting\_time), “voucher\_type” → “Stock Entry” …().
- If (bundle and bundle.get(“name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundle → bundle.get(“name”).
  - Set row.serial\_and\_batch\_bundle from bundle.name.
  - Set row.use\_serial\_batch\_fields from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L665)

<a id="op-6159ffad7b6f46"></a>
### Get fg mapping

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_fg_mapping`

**Inputs** stock\_entry.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“fg\_values” → get\_fg\_values(doc.name), “raw\_materials” → get\_raw\_material\_entries(doc.name)).

**Local steps**

- Set doc from get\_stock\_entry\_for\_fg\_mapping(stock\_entry, “read”).
- Return mapping(“fg\_values” → get\_fg\_values(doc.name), “raw\_materials” → get\_raw\_material\_entries(doc.name)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L637)

<a id="op-ecf0a8defc29b4"></a>
### Set fg mapping

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_set_fg_mapping`

**Inputs** stock\_entry, mapping.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “Mapping must be a dictionary of raw material entries to finished goods” · validation helper — translated “{0} has no serial / batch tracked finished good”.format(doc.name) · validation helper — translated “Row {0} is not a raw material serial / batch entry of {1}”.format(Platform.bold(escape\_html(cstr(entry\_name))), doc.name) · validation helper — translated “Raw material {0} is already mapped and can't be changed after {1} is submitted”.format(Platform.bold((row.serial\_no or row.batch\_no)), doc.name).

**Local steps**

- Set doc from get\_stock\_entry\_for\_fg\_mapping(stock\_entry, “write”).
- Set mapping from (Platform.parse\_json(mapping) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(mapping) → mapping().
- If not isinstance(mapping, dict).
  - Call the validation error handler Platform.throw(translated “Mapping must be a dictionary of raw material entries to finished goods”).
- Set fg\_targets from set of tuple(row.fg\_field, row.value) for row drawn from get\_fg\_values(doc.name).
  - Draw row from get\_fg\_values(doc.name).
- If not fg\_targets.
  - Call the validation error handler Platform.throw(translated “{0} has no serial / batch tracked finished good”.format(doc.name)).
- Set is\_submitted from doc.docstatus equals 1.
- Set raw\_materials from mapping of row.name → row for row drawn from get\_raw\_material\_entries(doc.name, draft\_only = not is\_submitted, for\_update = is\_submitted).
  - Draw row from get\_raw\_material\_entries(doc.name, draft\_only = not is\_submitted, for\_update = is\_submitted).
- Set entries\_by\_fg\_target from defaultdict(list).
- For each tuple(entry\_name, target) in mapping.items().
  - Set row from raw\_materials.get(entry\_name).
  - If not row.
    - Call the validation error handler Platform.throw(translated “Row {0} is not a raw material serial / batch entry of {1}”.format(Platform.bold(escape\_html(cstr(entry\_name))), doc.name)).
  - Set fg\_target from get\_fg\_target(target, fg\_targets, doc.name).
  - If is\_submitted.
    - If (row.fg\_serial\_no or row.fg\_batch\_no).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.fg\_serial\_no → row.fg\_batch\_no.
      - Call the validation error handler Platform.throw(translated “Raw material {0} is already mapped and can't be changed after {1} is submitted”.format(Platform.bold((row.serial\_no or row.batch\_no)), doc.name)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
    - If not fg\_target at 1.
      - Continue with the next iteration or loop test.
  - Evaluate entries\_by\_fg\_target at fg\_target.append(entry\_name).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- For each tuple(tuple(fg\_field, fg\_value), entry\_names) in entries\_by\_fg\_target.items().
  - Set query from nested operand in the contract(nested operand in the contract).set(sabe.fg\_serial\_no, fg\_value when nested operand in the contract equals nested operand in the contract, otherwise no value).set(sabe.fg\_bat ….
    - Value choice on fg\_field equals “fg\_serial\_no” — true gives fg\_value, false gives no value.
    - Value choice on fg\_field equals “fg\_batch\_no” — true gives fg\_value, false gives no value.
  - If is\_submitted.
    - Set query from query.where((Coalesce(sabe.fg\_serial\_no, empty text) equals empty text bitwise and Coalesce(sabe.fg\_batch\_no, empty text) equals empty text)).
  - Evaluate query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L663)

<a id="op-17b864486ec2f4"></a>
### Set fg mapping on submit

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_set_fg_mapping_on_submit`

**Inputs** doc.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Raw material {0} is mapped to {1}, which is not a finished good of this entry”.format(Platform.bold((row.serial\_no or row.batch\_no)), Platform.bold(target at 1)).

**Local steps**

- If doc.purpose does not belong to tuple(“Manufacture”, “Repack”).
  - Return no value.
- Set fg\_values from get\_fg\_values(doc.name).
- Set fg\_targets from list of tuple(row.fg\_field, row.value) for row drawn from fg\_values.
  - Draw row from fg\_values.
- Set raw\_materials from get\_raw\_material\_entries(doc.name).
- If (not fg\_targets or not raw\_materials).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fg\_targets → not raw\_materials.
  - Return no value.
- Set fg\_qty from mapping of tuple(row.fg\_field, row.value) → (row.qty or 1) for row drawn from fg\_values.
  - Draw row from fg\_values.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.qty → 1.
- Set rows\_by\_item from defaultdict(list).
- For each row in raw\_materials.
  - Set target from tuple(“fg\_serial\_no”, row.fg\_serial\_no) when row.fg\_serial\_no, otherwise tuple(“fg\_batch\_no”, row.fg\_batch\_no).
    - Value choice on row.fg\_serial\_no — true gives tuple(“fg\_serial\_no”, row.fg\_serial\_no), false gives tuple(“fg\_batch\_no”, row.fg\_batch\_no).
  - If (target at 1 and target does not belong to fg\_targets).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in target at 1 → target does not belong to fg\_targets.
    - Call the validation error handler Platform.throw(translated “Raw material {0} is mapped to {1}, which is not a finished good of this entry”.format(Platform.bold((row.serial\_no or row.batch\_no)), Platform.bold(target at 1))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
  - Set row.fg\_target from target when target at 1, otherwise no value.
    - Value choice on target at 1 — true gives target, false gives no value.
  - Evaluate rows\_by\_item at row.item\_code.append(row).
- If not Platform.get\_single\_value(“Stock Settings”, “auto\_map\_raw\_materials\_to\_finished\_goods”).
  - Return no value.
- Set entries\_by\_fg\_target from defaultdict(list).
- For each rows in rows\_by\_item.values().
  - Set per\_fg from get\_fg\_quotas(len(rows), fg\_targets, fg\_qty).
  - Set mapped\_count from defaultdict(int).
  - For each row in rows.
    - If row.fg\_target.
      - Update mapped\_count at row.fg\_target using + 1.
  - For each row in rows.
    - If (row.fg\_target or (len(fg\_targets) &gt; 1 and not row.serial\_no)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.fg\_target → (len(fg\_targets) &gt; 1 and not row.serial\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fg\_targets) &gt; 1 → not row.serial\_no.
      - Continue with the next iteration or loop test.
    - Set target from next(generator of t for t drawn from fg\_targets where mapped\_count at t &lt; per\_fg at t, no value).
      - Draw t from fg\_targets, keep a combination only if (mapped\_count at t &lt; per\_fg at t).
    - If target.
      - Update mapped\_count at target using + 1.
      - Evaluate entries\_by\_fg\_target at target.append(row.name).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- For each tuple(tuple(fg\_field, fg\_value), entry\_names) in entries\_by\_fg\_target.items().
  - Evaluate nested operand in the contract(nested operand in the contract).set(sabe at fg\_field, fg\_value).where(sabe.name.isin(entry\_names)).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_map\_raw\_materials\_to\_finished\_goods”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L664)

<a id="op-834cb1675d7d90"></a>
### Get fg quotas

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_fg_quotas`

**Inputs** count, fg\_targets, fg\_qty.

**Explicit results** quotas.

**Local steps**

- Set total\_qty from sum(generator of fg\_qty at target for target drawn from fg\_targets).
  - Draw target from fg\_targets.
- Set shares from mapping of target → flt(((count × fg\_qty at target) ÷ total\_qty), 6) for target drawn from fg\_targets.
  - Draw target from fg\_targets.
- Set quotas from mapping of target → math.floor(share) for tuple(target, share) drawn from shares.items().
  - Draw tuple(target, share) from shares.items().
- Set by\_remainder from sorted(fg\_targets, key = deferred anonymous expression, reverse = true).
- For each target in by\_remainder at slice no value to (count − sum(quotas.values())).
  - Update quotas at target using + 1.
- Return quotas.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L638)

<a id="op-96bf438482aea4"></a>
### Get fg target

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_fg_target`

**Inputs** target, fg\_targets, stock\_entry.

**Explicit results** tuple(no value, no value) · matches at 0.

**Explicit failure paths** validation helper — translated “{0} is not a finished good serial / batch produced by {1}”.format(Platform.bold(escape\_html(cstr(value))), stock\_entry) · validation helper — translated “{0} is both a finished good serial no and batch no in {1}, please specify which one”.format(Platform.bold(escape\_html(cstr(value))), stock\_entry).

**Local steps**

- If isinstance(target, dict).
  - Set tuple(fg\_field, value) from tuple(target.get(“fg\_field”), target.get(“value”)).
- Otherwise.
  - Set tuple(fg\_field, value) from tuple(no value, target).
- If not value.
  - Return tuple(no value, no value).
- Set matches from list of tuple(field, val) for tuple(field, val) drawn from fg\_targets where (val equals value and fg\_field belongs to tuple(no value, field)).
  - Draw tuple(field, val) from fg\_targets, keep a combination only if ((val equals value and fg\_field belongs to tuple(no value, field))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in val equals value → fg\_field belongs to tuple(no value, field).
- If not matches.
  - Call the validation error handler Platform.throw(translated “{0} is not a finished good serial / batch produced by {1}”.format(Platform.bold(escape\_html(cstr(value))), stock\_entry)).
- <a id="op-96bf438482aea4-guard-19"></a>If len(matches) &gt; 1.
  - Call the validation error handler Platform.throw(translated “{0} is both a finished good serial no and batch no in {1}, please specify which one”.format(Platform.bold(escape\_html(cstr(value))), stock\_entry)).
- Return matches at 0.

**Derived branch illustrations**

- At the comparison len(matches) &gt; 1, length of matches = 2 selects the branch that calls the validation-error handler with translated “{0} is both a finished good serial no and batch no in {1}, please specify which one”.format(Platform.bold(escape\_html(cst …. With length of matches = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-96bf438482aea4-guard-19)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L639)

<a id="op-be50b548a348de"></a>
### Get stock entry for fg mapping

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_stock_entry_for_fg_mapping`

**Inputs** stock\_entry, permission\_type.

**Record and data access** resolve a document from “Stock Entry” via get\_doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Finished good mapping is only allowed for Manufacture and Repack entries” · validation helper — translated “Finished good mapping can't be changed for a cancelled entry”.

**Local steps**

- Set doc from Platform.get\_doc(“Stock Entry”, stock\_entry).
- Evaluate doc.check\_permission(permission\_type).
- If (permission\_type equals “write” and doc.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in permission\_type equals “write” → doc.docstatus equals 1.
  - Evaluate doc.check\_permission(“submit”).
- If doc.purpose does not belong to tuple(“Manufacture”, “Repack”).
  - Call the validation error handler Platform.throw(translated “Finished good mapping is only allowed for Manufacture and Repack entries”).
- <a id="op-be50b548a348de-guard-12"></a>If doc.docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “Finished good mapping can't be changed for a cancelled entry”).
- Return doc.

**Derived branch illustrations**

- At the comparison doc.docstatus equals 2, doc.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Finished good mapping can't be changed for a cancelled entry”. With doc.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-be50b548a348de-guard-12)

**Values supplied outside this operation** effective access from doc.check\_permission(permission\_type), doc.check\_permission(“submit”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L651)

<a id="op-da586e075477d6"></a>
### Get fg values

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_fg_values`

**Inputs** stock\_entry.

**Explicit results** list(fg\_values.values()).

**Local steps**

- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set fg\_entries from nested operand in the contract(nested operand in the contract).orderby(sed.idx).orderby(sabe.idx).run(as\_dict = true).
- Set serialized\_rows from set of row.detail\_name for row drawn from fg\_entries where row.serial\_no.
  - Draw row from fg\_entries, keep a combination only if (row.serial\_no).
- Set fg\_values from mapping().
- For each row in fg\_entries.
  - If row.detail\_name belongs to serialized\_rows.
    - Set tuple(value, fg\_field) from tuple(row.serial\_no, “fg\_serial\_no”).
  - Otherwise.
    - Set tuple(value, fg\_field) from tuple(row.batch\_no, “fg\_batch\_no”).
  - If not value.
    - Continue with the next iteration or loop test.
  - If tuple(fg\_field, value) does not belong to fg\_values.
    - Set fg\_values at tuple(fg\_field, value) from Platform.\_dict(value = value, fg\_field = fg\_field, item\_code = row.item\_code, qty = 0.0).
  - Update fg\_values at tuple(fg\_field, value).qty using + abs(flt(row.qty)).
- Return list(fg\_values.values()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L640)

<a id="op-ecee69e302aa2b"></a>
### Get raw material entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_raw_material_entries`

**Inputs** stock\_entry, draft\_only = false, for\_update = false.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If draft\_only.
  - Set query from query.where((sabb.docstatus equals 0 bitwise and sabe.docstatus equals 0)).
- If for\_update.
  - Set query from query.for\_update().
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L647)

<a id="op-255876ca7f4ea6"></a>
### Get own bundle condition

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_own_bundle_condition`

**Inputs** sabb, stock\_entry.

**Explicit results** (sabb.voucher\_type equals “Stock Entry” bitwise and Coalesce(sabb.voucher\_no, empty text).isin(list(empty text, stock\_entry))).

**Local steps**

- Return (sabb.voucher\_type equals “Stock Entry” bitwise and Coalesce(sabb.voucher\_no, empty text).isin(list(empty text, stock\_entry))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L645)

<a id="op-035e58f082ff56"></a>
### Get data

`operation_enterprise_stock_record_definitions_stock_entry_stock_entry_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “stock\_entry”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “from\_voucher\_no”), “transactions” → list(mapping(“label” → translated “Stock Reservation”, “items” → li ….

**Local steps**

- Return mapping(“fieldname” → “stock\_entry”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “from\_voucher\_no”), “transactions” → list(mapping(“label” → translated “Stock Reservation”, “items” → li ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0839.json#L3616) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L840)

<a id="op-b231511e790451"></a>
### Make stock entry

`operation_enterprise_stock_record_definitions_stock_entry_stock_entry_utils_business_behavior_make_stock_entry`

**Inputs** item\_code (named only), qty (named only), company (named only, default no value), from\_warehouse (named only, default no value), to\_warehouse (named only, default no value), rate (named only, default no value), serial\_no (named only, default no value), batch\_no (named only, default no value), posting\_date (named only, default no value), posting\_time (named only, default no value), purpose (named only, default no value), do\_not\_save (named only, default false), do\_not\_submit (named only, default false), inspection\_required (named only, default false).

**Wrappers, in declaration order** overload.

**Declared result** “StockEntry”.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0839.json#L3774) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L841)

<a id="op-f7215e1d6f08c5"></a>
### Make stock entry

`operation_enterprise_stock_record_definitions_stock_entry_stock_entry_utils_business_behavior_make_stock_entry_2`

**Inputs** remaining named values args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_value · read “Company” via get\_value · read “Item” via get\_value.

**State and service calls** request new\_doc for “Stock Entry” · call insert on s · call submit on s.

**Explicit results** s.

**Local steps**

- Bind dependencies SerialBatchCreation.
- Evaluate Platform.has\_permission(“Stock Entry”, “create”, throw = true).
- Bind local operation process\_serial\_numbers for subsequent calls.
- Set s from Platform.new\_doc(“Stock Entry”).
- Set args from Platform.\_dict(args).
- If (args.posting\_date or args.posting\_time).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.posting\_date → args.posting\_time.
  - Set s.set\_posting\_time from 1.
- If args.posting\_date.
  - Set s.posting\_date from args.posting\_date.
- If args.posting\_time.
  - Set s.posting\_time from args.posting\_time.
- If args.inspection\_required.
  - Set s.inspection\_required from args.inspection\_required.
- If not args.posting\_date.
  - Set s.posting\_date from today().
- If args.from\_warehouse.
  - Set args.source from args.from\_warehouse.
- If args.to\_warehouse.
  - Set args.target from args.to\_warehouse.
- If args.item\_code.
  - Set args.item from args.item\_code.
- If args.apply\_putaway\_rule.
  - Set s.apply\_putaway\_rule from args.apply\_putaway\_rule.
- If isinstance(args.qty, str).
  - If “.” belongs to args.qty.
    - Set args.qty from flt(args.qty).
  - Otherwise.
    - Set args.qty from cint(args.qty).
- If not args.purpose.
  - If (args.source and args.target).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.source → args.target.
    - Set s.purpose from “Material Transfer”.
  - Otherwise.
    - If args.source.
      - Set s.purpose from “Material Issue”.
    - Otherwise.
      - Set s.purpose from “Material Receipt”.
- Otherwise.
  - Set s.purpose from args.purpose.
- If not args.company.
  - If args.source.
    - Set args.company from Platform.db.get\_value(“Warehouse”, args.source, “company”).
  - Otherwise.
    - If args.target.
      - Set args.company from Platform.db.get\_value(“Warehouse”, args.target, “company”).
- If Platform.in\_test.
  - If not args.company.
    - Set args.company from “\_Test Company”.
  - If not args.item.
    - Set args.item from “\_Test Item”.
- Set s.company from (args.company or Enterprise.get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.company → Enterprise.get\_default\_company().
- Set s.add\_to\_transit from (args.add\_to\_transit or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.add\_to\_transit → 0.
- Set s.purchase\_receipt\_no from args.purchase\_receipt\_no.
- Set s.delivery\_note\_no from args.delivery\_note\_no.
- Set s.sales\_invoice\_no from args.sales\_invoice\_no.
- Set s.is\_opening from (args.is\_opening or “No”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.is\_opening → “No”.
- If not args.cost\_center.
  - Set args.cost\_center from Platform.get\_value(“Company”, s.company, “cost\_center”).
- If (not args.expense\_account and s.is\_opening equals “No”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.expense\_account → s.is\_opening equals “No”.
  - Set args.expense\_account from Platform.get\_value(“Company”, s.company, “stock\_adjustment\_account”).
- Set serial\_number from args.serial\_no.
- Set bundle\_id from no value.
- If (not args.use\_serial\_batch\_fields and (args.serial\_no or args.batch\_no or args.batches)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.use\_serial\_batch\_fields → (args.serial\_no or args.batch\_no or args.batches).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.serial\_no → args.batch\_no → args.batches.
  - Set batches from Platform.\_dict(mapping()).
  - If args.batch\_no.
    - Set batches from Platform.\_dict(mapping(args.batch\_no → args.qty)).
  - Otherwise.
    - If args.batches.
      - Set batches from args.batches.
  - Set posting\_datetime from no value.
  - If (s.posting\_date and s.posting\_time).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in s.posting\_date → s.posting\_time.
    - Set posting\_datetime from get\_combine\_datetime(s.posting\_date, s.posting\_time).
  - Set bundle\_id from SerialBatchCreation(mapping(“item\_code” → args.item, “warehouse” → (nested operand in the contract.source or nested operand in the contract.target), “voucher\_type” → “Stock Entry”, “total\_qty” → (nested op …().name.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.source → args.target.
    - Value choice on args.source — true gives negative 1, false gives 1.
    - Value choice on args.source — true gives “Outward”, false gives “Inward”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.rate → args.basic\_rate.
  - Set args at “serial\_no” from empty text.
  - Set args at “batch\_no” from empty text.
- Otherwise.
  - Set args.serial\_no from serial\_number.
- Evaluate s.append(“items”, mapping(“item\_code” → args.item, “s\_warehouse” → args.source, “t\_warehouse” → args.target, “qty” → args.qty, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.rate → args.basic\_rate.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.conversion\_factor → 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(args.conversion\_factor) → 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_value(“Item”, args.item, “sample\_quantity”) → 0.
- Evaluate s.set\_stock\_entry\_type().
- If not args.do\_not\_save.
  - Evaluate s.insert().
  - If not args.do\_not\_submit.
    - Evaluate s.submit().
  - Evaluate s.load\_from\_db().
- Return s.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Entry”, “create”, throw = true) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L842)

<a id="op-a87837344e083b"></a>
### Make stock entry.process serial numbers

`operation_enterprise_stock_record_definitions_stock_entry_stock_entry_utils_business_behavior_make_stock_entry_process_serial_numbers`

**Inputs** serial\_nos\_list.

**Explicit results** whitespace '\\n'.join(uniques).

**Local steps**

- Set serial\_nos\_list from list(whitespace '\\n'.join(generator of serial\_num at “serial\_no” for serial\_num drawn from serial\_nos\_list where serial\_num.serial\_no)).
  - Draw serial\_num from serial\_nos\_list, keep a combination only if (serial\_num.serial\_no).
- Set uniques from list(set(serial\_nos\_list at 0.split(whitespace '\\n'))).
- Return whitespace '\\n'.join(uniques).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0839.json#L6681) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L843)

## Record · Stock entry type

[Record definition](../../../../data/record-types/stock_entry_type.json)

<a id="op-514b87d8244cda"></a>
### Stock Entry Type.validate

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_stock_entry_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_standard\_type().
- Evaluate self.validate\_add\_to\_transit().
- If (self.add\_to\_transit and self.purpose differs from “Material Transfer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.add\_to\_transit → self.purpose differs from “Material Transfer”.
  - Set self.add\_to\_transit from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate standard type](operations-086.md#op-8ea455485f20ae), [validate add to transit](operations-086.md#op-3da0afbc39faaf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L964)

<a id="op-f2e56f59d11cf5"></a>
### Stock Entry Type.on trash

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_type_stock_entry_type_stockentrytype_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Standard Stock Entry Type {0} cannot be deleted”.format(Platform.bold(self.name)).

**Local steps**

- If self.is\_standard.
  - Call the validation error handler Platform.throw(translated “Standard Stock Entry Type {0} cannot be deleted”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L785)

<a id="op-3da0afbc39faaf"></a>
### Stock Entry Type.validate add to transit

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_type_stock_entry_type_stockentrytype_validate_add_to_transit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Add to Transit cannot be enabled on the standard Stock Entry Type {0}. Create a separate Stock Entry Type fo …”.format(Platform.bold(self.name)).

**Local steps**

- If (self.is\_standard and self.add\_to\_transit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.add\_to\_transit.
  - Call the validation error handler Platform.throw(translated “Add to Transit cannot be enabled on the standard Stock Entry Type {0}. Create a separate Stock Entry Type fo …”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L786)

<a id="op-8ea455485f20ae"></a>
### Stock Entry Type.validate standard type

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_stock_entry_type_validate_standard_type`

**Inputs** self.

**Explicit failure paths** validation helper — formatted text Stock Entry Type {self.name} cannot be set as standard.

**Local steps**

- If (self.is\_standard and self.name does not belong to list(“Material Issue”, “Material Receipt”, “Material Transfer”, “Material Transfer for Manufacture”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → self.name does not belong to list(“Material Issue”, “Material Receipt”, “Material Transfer”, “Material Transfer for Manufacture”, …).
  - Call the validation error handler Platform.throw(formatted text Stock Entry Type {self.name} cannot be set as standard).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L965)

<a id="op-34f7a300886402"></a>
### Manufacture Entry.initialize

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_initialize`

**Inputs** self, kwargs.

**Declared result** no value.

**Local steps**

- For each tuple(key, value) in kwargs.items().
  - Evaluate setattr(self, key, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0851.json#L6950) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L28) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L959)

<a id="op-abc400fb6e9959"></a>
### Manufacture Entry.make stock entry

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_make_stock_entry`

**Inputs** self.

**State and service calls** request new\_doc for “Stock Entry”.

**Local steps**

- Set self.stock\_entry from Platform.new\_doc(“Stock Entry”).
- Set self.stock\_entry.purpose from self.purpose.
- Set self.stock\_entry.company from self.company.
- If self.bom\_no.
  - Set self.stock\_entry.from\_bom from 1.
  - Set self.stock\_entry.bom\_no from self.bom\_no.
  - Set self.stock\_entry.use\_multi\_level\_bom from 1.
- Set self.stock\_entry.fg\_completed\_qty from self.for\_quantity.
- Set self.stock\_entry.process\_loss\_qty from self.process\_loss\_qty.
- Set self.stock\_entry.project from self.project.
- Set self.stock\_entry.job\_card from self.job\_card.
- Evaluate self.stock\_entry.set\_stock\_entry\_type().
- Set self.stock\_entry.work\_order from self.work\_order.
- Evaluate self.prepare\_source\_warehouse().
- Evaluate self.add\_raw\_materials().
- Evaluate self.add\_finished\_good().

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare source warehouse](operations-087.md#op-e060c868541907), [add raw materials](operations-087.md#op-7ffb3eb1e42640), [add finished good](operations-087.md#op-25059de1e35abb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L29) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L960)
