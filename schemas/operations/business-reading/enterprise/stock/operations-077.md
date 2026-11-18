# Inventory and warehouses · operations 77

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-fb8688d70f2cc7"></a>
### Stock Entry.validate repack entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_repack_entry`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “When there are multiple finished goods ({0}) in a Repack stock entry, the basic rate for all finished goods  …”.format(“, ”.join(fg\_items)).

**Local steps**

- <a id="op-fb8688d70f2cc7-guard-2"></a>If self.purpose differs from “Repack”.
  - Return no value.
- Set fg\_items from mapping of row.item\_code → row for row drawn from self.items where row.is\_finished\_item.
  - Draw row from self.items, keep a combination only if (row.is\_finished\_item).
- If (len(fg\_items) &gt; 1 and not all(generator of row.set\_basic\_rate\_manually for row drawn from fg\_items.values())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fg\_items) &gt; 1 → not all(generator of row.set\_basic\_rate\_manually for row drawn from fg\_items.values()).
  - Draw row from fg\_items.values().
  - Call the validation error handler Platform.throw(translated “When there are multiple finished goods ({0}) in a Repack stock entry, the basic rate for all finished goods  …”.format(“, ”.join(fg\_items)), title = translated “Set Basic Rate Manually”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose differs from “Repack”, self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Repack”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fb8688d70f2cc7-guard-2)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L770)

<a id="op-b2fbc1043f210d"></a>
### Stock Entry.validate raw materials exists

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_raw_materials_exists`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “At least one raw material item must be present in the stock entry for the type {0}”.format(bold(self.purpose)).

**Local steps**

- <a id="op-b2fbc1043f210d-guard-2"></a>If self.purpose does not belong to list(“Manufacture”, “Repack”, “Disassemble”).
  - Return no value.
- If Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”).
  - Return no value.
- Set raw\_materials from list().
- For each row in self.items.
  - If row.s\_warehouse.
    - Evaluate raw\_materials.append(row.item\_code).
- If not raw\_materials.
  - Call the validation error handler Platform.throw(translated “At least one raw material item must be present in the stock entry for the type {0}”.format(bold(self.purpose)), title = translated “Raw Materials Missing”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to list(“Manufacture”, “Repack”, “Disassemble”), self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b2fbc1043f210d-guard-2)

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L768)

<a id="op-3063fa79ede538"></a>
### Stock Entry.set serial batch for disassembly

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_batch_for_disassembly`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-3063fa79ede538-guard-2"></a>If self.purpose differs from “Disassemble”.
  - Return no value.
- If self.get(“source\_stock\_entry”).
  - Evaluate self.\_set\_serial\_batch\_for\_disassembly\_from\_stock\_entry().
- Otherwise.
  - Evaluate self.\_set\_serial\_batch\_for\_disassembly\_from\_available\_materials().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose differs from “Disassemble”, self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Disassemble”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3063fa79ede538-guard-2)

**Methods declared on this owner** [set serial batch for disassembly from stock entry](operations-077.md#op-ca87d5b6eec2e5), [set serial batch for disassembly from available materials](operations-077.md#op-b06cc3bfedcf26).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L738)

<a id="op-ca87d5b6eec2e5"></a>
### Stock Entry.set serial batch for disassembly from stock entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_batch_for_disassembly_from_stock_entry`

**Inputs** self.

**Local steps**

- Bind dependencies get\_voucher\_wise\_serial\_batch\_from\_bundle.
- Set bundle\_data from get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = list(self.source\_stock\_entry)).
- Set source\_rows\_by\_name from mapping of r.name → r for r drawn from self.get\_items\_from\_manufacture\_stock\_entry().
  - Draw r from self.get\_items\_from\_manufacture\_stock\_entry().
- Set used from self.get\_serial\_batches\_used\_by\_earlier\_disassemblies().
- For each row in self.items.
  - If not row.ste\_detail.
    - Continue with the next iteration or loop test.
  - Set source\_row from source\_rows\_by\_name.get(row.ste\_detail).
  - If not source\_row.
    - Continue with the next iteration or loop test.
  - Set source\_warehouse from (source\_row.s\_warehouse or source\_row.t\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_row.s\_warehouse → source\_row.t\_warehouse.
  - Set key from tuple(source\_row.item\_code, source\_warehouse, self.source\_stock\_entry).
  - Set source\_bundle from bundle\_data.get(key, mapping()).
  - Set used\_batch\_qty from used.batch\_qty at source\_warehouse.
  - Set batches from defaultdict(float).
  - Set serial\_nos from list().
  - If source\_bundle.get(“batch\_nos”).
    - Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
    - Set qty\_remaining from row.transfer\_qty.
    - For each tuple(batch\_no, batch\_qty) in source\_bundle at “batch\_nos”.items().
      - <a id="op-ca87d5b6eec2e5-guard-31"></a>If qty\_remaining ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set available\_qty from flt((abs(flt(batch\_qty)) − used\_batch\_qty at batch\_no), precision).
      - <a id="op-ca87d5b6eec2e5-guard-34"></a>If available\_qty ≤ 0.
        - Continue with the next iteration or loop test.
      - Set batches at batch\_no from min(available\_qty, qty\_remaining).
      - Update qty\_remaining using − batches at batch\_no.
  - Otherwise.
    - If source\_row.batch\_no.
      - Set batches at source\_row.batch\_no from row.transfer\_qty.
  - If source\_bundle.get(“serial\_nos”).
    - Set serial\_nos from get\_serial\_nos(source\_bundle at “serial\_nos”).
  - Otherwise.
    - If source\_row.serial\_no.
      - Set serial\_nos from get\_serial\_nos(source\_row.serial\_no).
  - Set serial\_nos from list of serial\_no for serial\_no drawn from serial\_nos where serial\_no does not belong to used.serial\_nos at slice no value to int(row.transfer\_qty).
    - Draw serial\_no from serial\_nos, keep a combination only if (serial\_no does not belong to used.serial\_nos).
  - Evaluate self.\_set\_serial\_batch\_bundle\_for\_disassembly\_row(row, serial\_nos, batches).
  - Evaluate used.serial\_nos.update(serial\_nos).
  - For each tuple(batch\_no, qty) in batches.items().
    - Update used\_batch\_qty at batch\_no using + qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty\_remaining ≤ 0, qty\_remaining = 0 selects the branch that exits the enclosing loop. With qty\_remaining = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ca87d5b6eec2e5-guard-31)
- At the comparison available\_qty ≤ 0, available\_qty = 0 selects the branch that continues with the next loop iteration. With available\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ca87d5b6eec2e5-guard-34)

**Methods declared on this owner** [get items from manufacture stock entry](operations-082.md#op-28a561352164af), [get serial batches used by earlier disassemblies](operations-077.md#op-f8588a6e49946b), [set serial batch bundle for disassembly row](operations-077.md#op-173cc1e7c1f910).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L740)

<a id="op-f8588a6e49946b"></a>
### Stock Entry.get serial batches used by earlier disassemblies

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_serial_batches_used_by_earlier_disassemblies`

**Inputs** self.

**Declared result** Platform.\_dict.

**Explicit results** used.

**Local steps**

- Set SE from Platform.qb.DocType(“Stock Entry”).
- Set SED from Platform.qb.DocType(“Stock Entry Detail”).
- Set SBE from Platform.qb.DocType(“Serial and Batch Entry”).
- Set source from Platform.qb.DocType(“Stock Entry Detail”).as\_(“source”).
- Set rows from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“warehouse”), SBE.serial\_no, SBE.batch\_no, SBE.qty).where((((nested operand in the contract equals n ….
- Set used from Platform.\_dict(serial\_nos = set(), batch\_qty = defaultdict(deferred anonymous expression)).
- For each row in rows.
  - If row.serial\_no.
    - Evaluate used.serial\_nos.add(row.serial\_no).
  - If row.batch\_no.
    - Update used.batch\_qty at row.warehouse at row.batch\_no using + abs(flt(row.qty)).
- Return used.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L713)

<a id="op-b06cc3bfedcf26"></a>
### Stock Entry.set serial batch for disassembly from available materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_batch_for_disassembly_from_available_materials`

**Inputs** self.

**Local steps**

- Set available\_materials from get\_available\_materials(self.work\_order, self).
- For each row in self.items.
  - If (row.serial\_no or row.batch\_no or row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no → row.serial\_and\_batch\_bundle.
    - Continue with the next iteration or loop test.
  - Set key from tuple(row.item\_code, no value) when row.t\_warehouse, otherwise tuple(row.item\_code, row.s\_warehouse).
    - Value choice on row.t\_warehouse — true gives tuple(row.item\_code, no value), false gives tuple(row.item\_code, row.s\_warehouse).
  - Set materials from available\_materials.get(tuple(expanded key, no value)).
  - If not materials.
    - Continue with the next iteration or loop test.
  - Set batches from defaultdict(float).
  - Set serial\_nos from list().
  - Set qty from row.transfer\_qty.
  - Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
  - For each tuple(batch\_no, batch\_qty) in materials.batch\_details.items().
    - <a id="op-b06cc3bfedcf26-guard-17"></a>If qty ≤ 0.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set batch\_qty from flt(batch\_qty, precision).
    - <a id="op-b06cc3bfedcf26-guard-21"></a>If batch\_qty ≤ 0.
      - Continue with the next iteration or loop test.
    - If batch\_qty ≤ qty.
      - Set batches at batch\_no from batch\_qty.
      - Set qty from flt((qty − batch\_qty), precision).
    - Otherwise.
      - Set batches at batch\_no from qty.
      - Set qty from 0.
  - If materials.serial\_nos.
    - Set serial\_nos from materials.serial\_nos at slice no value to int(row.transfer\_qty).
  - Evaluate self.\_set\_serial\_batch\_bundle\_for\_disassembly\_row(row, serial\_nos, batches).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b06cc3bfedcf26-guard-17)
- At the comparison batch\_qty ≤ 0, batch\_qty = 0 selects the branch that continues with the next loop iteration. With batch\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b06cc3bfedcf26-guard-21)

**Methods declared on this owner** [set serial batch bundle for disassembly row](operations-077.md#op-173cc1e7c1f910).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L739)

<a id="op-173cc1e7c1f910"></a>
### Stock Entry.set serial batch bundle for disassembly row

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_batch_bundle_for_disassembly_row`

**Inputs** self, row, serial\_nos, batches.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Local steps**

- If (not serial\_nos and not batches).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → not batches.
  - Return no value.
- Set warehouse from (row.s\_warehouse or row.t\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.s\_warehouse → row.t\_warehouse.
- Set bundle\_doc from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → warehouse, “posting\_datetime” → get\_combine\_datetime(self.posting\_date, self.posting\_time), “voucher\_type” → self.doctype, …)).make\_se ….
  - Value choice on row.t\_warehouse — true gives “Inward”, false gives “Outward”.
- Set row.serial\_and\_batch\_bundle from bundle\_doc.name.
- Set row.use\_serial\_batch\_fields from 0.
- Evaluate row.db\_set(mapping(“serial\_and\_batch\_bundle” → bundle\_doc.name, “use\_serial\_batch\_fields” → 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L736)

<a id="op-a67bd33f66bdff"></a>
### Stock Entry.on submit

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_serial\_batch\_for\_disassembly().
- Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
- Evaluate self.update\_work\_order().
- Evaluate self.update\_disassembled\_order().
- Evaluate self.adjust\_stock\_reservation\_entries\_for\_return().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.update\_wo\_reservation\_for\_subcontracting().
- Evaluate self.update\_stock\_ledger().
- Evaluate set\_fg\_mapping\_on\_submit(self).
- Evaluate self.make\_stock\_reserve\_for\_wip\_and\_fg().
- Evaluate self.reserve\_stock\_for\_subcontracting().
- Evaluate self.update\_subcontract\_order\_supplied\_items().
- Evaluate self.update\_subcontracting\_order\_status().
- Evaluate self.update\_pick\_list\_status().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_project\_consumed\_material\_cost().
- Evaluate self.update\_transferred\_qty().
- Evaluate self.update\_quality\_inspection().
- If (self.purpose equals “Material Transfer” and self.add\_to\_transit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.add\_to\_transit.
  - Evaluate self.set\_material\_request\_transfer\_status(“In Transit”).
- If (self.purpose equals “Material Transfer” and self.outgoing\_stock\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.outgoing\_stock\_entry.
  - Evaluate self.set\_material\_request\_transfer\_status(“Completed”).
- Evaluate super().on\_submit\_subcontracting\_inward().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set serial batch for disassembly](operations-077.md#op-3063fa79ede538), [update work order](operations-081.md#op-b6b50c85eed3ee), [update disassembled order](operations-081.md#op-b00253f75a4574), [update wo reservation for subcontracting](operations-081.md#op-5a14353401b89f), [update stock ledger](operations-080.md#op-cf1f94c4fd8008), [make stock reserve for wip and fg](operations-081.md#op-f62b7b02dbb6d2), [reserve stock for subcontracting](operations-081.md#op-744bf7594bc4cb), [update subcontract order supplied items](operations-083.md#op-8054193fc34b37), [update subcontracting order status](operations-084.md#op-7fefbed445543d), [update pick list status](operations-084.md#op-b625b7c95f64f5), [update transferred qty](operations-084.md#op-2c0345c4548920), [update quality inspection](operations-084.md#op-307ed8cd22fe4a), [set material request transfer status](operations-084.md#op-1ed6300fa18aba).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L801)

<a id="op-a92e4d8328fb2e"></a>
### Stock Entry.on cancel

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_asset\_repair\_is\_cancelled().
- Evaluate self.delink\_asset\_repair\_sabb().
- Evaluate self.validate\_closed\_subcontracting\_order().
- Evaluate self.update\_subcontract\_order\_supplied\_items().
- Evaluate self.update\_subcontracting\_order\_status().
- Evaluate self.update\_pick\_list\_status().
- Evaluate self.cancel\_stock\_reserve\_for\_wip\_and\_fg().
- If (self.work\_order and self.purpose equals “Material Consumption for Manufacture”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose equals “Material Consumption for Manufacture”.
  - Evaluate self.validate\_work\_order\_status().
- Evaluate self.update\_work\_order().
- Evaluate self.update\_disassembled\_order().
- Evaluate self.cancel\_stock\_reservation\_entries\_for\_inward().
- Evaluate self.cancel\_stock\_reservation\_entries\_for\_subcontracting().
- Evaluate self.update\_stock\_ledger().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”, …).
- Evaluate self.make\_gl\_entries\_on\_cancel().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_project\_consumed\_material\_cost().
- Evaluate self.update\_transferred\_qty().
- Evaluate self.update\_quality\_inspection().
- Evaluate self.adjust\_stock\_reservation\_entries\_for\_return().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.update\_wo\_reservation\_for\_subcontracting().
- Evaluate self.delete\_auto\_created\_batches().
- Evaluate self.delete\_linked\_stock\_entry().
- If (self.purpose equals “Material Transfer” and self.add\_to\_transit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.add\_to\_transit.
  - Evaluate self.set\_material\_request\_transfer\_status(“Not Started”).
- If (self.purpose equals “Material Transfer” and self.outgoing\_stock\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer” → self.outgoing\_stock\_entry.
  - Evaluate self.set\_material\_request\_transfer\_status(“In Transit”).
- Evaluate super().on\_cancel\_subcontracting\_inward().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset repair is cancelled](operations-077.md#op-445faff915c13d), [delink asset repair sabb](operations-077.md#op-a2b2e146d9cd93), [validate closed subcontracting order](operations-080.md#op-50b3a238c3596d), [update subcontract order supplied items](operations-083.md#op-8054193fc34b37), [update subcontracting order status](operations-084.md#op-7fefbed445543d), [update pick list status](operations-084.md#op-b625b7c95f64f5), [cancel stock reserve for wip and fg](operations-081.md#op-a67eef73f5a242), [validate work order status](operations-077.md#op-cd4845f3a1543d), [update work order](operations-081.md#op-b6b50c85eed3ee), [update disassembled order](operations-081.md#op-b00253f75a4574), [cancel stock reservation entries for subcontracting](operations-081.md#op-bde470c37ad234), [update stock ledger](operations-080.md#op-cf1f94c4fd8008), [update transferred qty](operations-084.md#op-2c0345c4548920), [update quality inspection](operations-084.md#op-307ed8cd22fe4a), [update wo reservation for subcontracting](operations-081.md#op-5a14353401b89f), [delete linked stock entry](operations-077.md#op-9a69e55e4264c7), [set material request transfer status](operations-084.md#op-1ed6300fa18aba).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L800)

<a id="op-72259e75b308b4"></a>
### Stock Entry.on update

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.set\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0835.json#L2984) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L802)

<a id="op-2abc4e9db09161"></a>
### Stock Entry.set job card data

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_job_card_data`

**Inputs** self.

**Record and data access** read “Job Card” via get\_value.

**Local steps**

- If (self.job\_card and not self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.job\_card → not self.work\_order.
  - Set data from Platform.db.get\_value(“Job Card”, self.job\_card, list(“for\_quantity”, “work\_order”, “bom\_no”, “semi\_fg\_bom”), as\_dict = 1).
  - Set self.fg\_completed\_qty from data.for\_quantity.
  - Set self.work\_order from data.work\_order.
  - Set self.from\_bom from 1.
  - Set self.bom\_no from (data.semi\_fg\_bom or data.bom\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.semi\_fg\_bom → data.bom\_no.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L732)

<a id="op-20d64254e589b9"></a>
### Stock Entry.validate job card fg item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_job_card_finished_goods_item`

**Inputs** self.

**Record and data access** read “Job Card” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Finished Good must be {1}”.format(row.idx, job\_card.fininshed\_good).

**Local steps**

- If not self.job\_card.
  - Return no value.
- Set job\_card from Platform.db.get\_value(“Job Card”, self.job\_card, list(“finished\_good”, “manufactured\_qty”), as\_dict = 1).
- For each row in self.items.
  - If (row.is\_finished\_item and row.item\_code differs from job\_card.finished\_good).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_finished\_item → row.item\_code differs from job\_card.finished\_good.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good must be {1}”.format(row.idx, job\_card.fininshed\_good)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L834)

<a id="op-f0c5bd0d7ef2f3"></a>
### Stock Entry.validate job card item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_job_card_item`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If (not self.job\_card or self.purpose equals “Manufacture”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.job\_card → self.purpose equals “Manufacture”.
  - Return no value.
- If cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”)).
  - Return no value.
- For each row in self.items.
  - If (row.job\_card\_item or not row.s\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.job\_card\_item → not row.s\_warehouse.
    - Continue with the next iteration or loop test.
  - Set msg from formatted text Row #{row.idx}: The job card item reference  is missing. Kindly create the stock entry  from the job card. If you have added the row manually.
  - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L835)

<a id="op-cd4845f3a1543d"></a>
### Stock Entry.validate work order status

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_work_order_status`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit failure paths** validation helper — translated “Cannot cancel transaction for Completed Work Order.”.

**Local steps**

- Set pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
- If pro\_doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “Cannot cancel transaction for Completed Work Order.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0835.json#L3586) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L839)

<a id="op-9c7ce87b183519"></a>
### Stock Entry.validate purpose

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_purpose`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Purpose must be one of {0}”.format(comma\_or(valid\_purposes)).

**Local steps**

- Set valid\_purposes from list(“Material Issue”, “Material Receipt”, “Material Transfer”, “Material Transfer for Manufacture”, …).
- If self.purpose does not belong to valid\_purposes.
  - Call the validation error handler Platform.throw(translated “Purpose must be one of {0}”.format(comma\_or(valid\_purposes))).
- Evaluate super().validate\_purpose().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L767)

<a id="op-9a69e55e4264c7"></a>
### Stock Entry.delete linked stock entry

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_delete_linked_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_all.

**State and service calls** request delete\_doc for “Stock Entry”.

**Local steps**

- If self.purpose equals “Send to Warehouse”.
  - For each d in Platform.get\_all(“Stock Entry”, filters = mapping(“docstatus” → 0, “outgoing\_stock\_entry” → self.name, “purpose” → “Receive at Warehouse”)).
    - Evaluate Platform.delete\_doc(“Stock Entry”, d.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0835.json#L3725) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L771)

<a id="op-445faff915c13d"></a>
### Stock Entry.validate asset repair is cancelled

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_asset_repair_is_cancelled`

**Inputs** self.

**Record and data access** read “Asset Repair” via get\_value.

**Explicit failure paths** validation helper — translated “Cancel Asset Repair {0} instead, it cancels this Stock Entry”.format(get\_link\_to\_form(“Asset Repair”, self.asset\_repair)).

**Local steps**

- If (self.asset\_repair and Platform.db.get\_value(“Asset Repair”, self.asset\_repair, “docstatus”) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.asset\_repair → Platform.db.get\_value(“Asset Repair”, self.asset\_repair, “docstatus”) equals 1.
  - Call the validation error handler Platform.throw(translated “Cancel Asset Repair {0} instead, it cancels this Stock Entry”.format(get\_link\_to\_form(“Asset Repair”, self.asset\_repair))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L754)

<a id="op-a2b2e146d9cd93"></a>
### Stock Entry.delink asset repair sabb

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_delink_asset_repair_stock_accounting_balance`

**Inputs** self.

**Record and data access** read “Asset Repair Consumed Item” via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call db\_set on doc.

**Explicit results** no value.

**Local steps**

- If not self.asset\_repair.
  - Return no value.
- For each row in self.items.
  - If row.serial\_and\_batch\_bundle.
    - Set voucher\_detail\_no from Platform.db.get\_value(“Asset Repair Consumed Item”, mapping(“parent” → self.asset\_repair, “serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle), “name”).
    - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).
    - Evaluate doc.db\_set(mapping(“voucher\_type” → “Asset Repair”, “voucher\_no” → self.asset\_repair, “voucher\_detail\_no” → voucher\_detail\_no)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L772)

<a id="op-90c3ce21ce82a9"></a>
### Stock Entry.set transfer qty

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_transfer_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: UOM Conversion Factor is mandatory”.format(item.idx) · validation helper — translated “Row {0}: Qty in Stock UOM can not be zero.”.format(item.idx).

**Local steps**

- Evaluate self.validate\_qty\_is\_not\_zero().
- For each item in self.get(“items”).
  - If not flt(item.conversion\_factor).
    - Call the validation error handler Platform.throw(translated “Row {0}: UOM Conversion Factor is mandatory”.format(item.idx)).
  - Set item.transfer\_qty from flt((flt(item.qty) × flt(item.conversion\_factor)), self.precision(“transfer\_qty”, item)).
  - If not flt(item.transfer\_qty).
    - Call the validation error handler Platform.throw(translated “Row {0}: Qty in Stock UOM can not be zero.”.format(item.idx), title = translated “Zero quantity”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L817)

<a id="op-54d84f2ade8ec0"></a>
### Stock Entry.validate item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_item`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: The item {1}, quantity must be positive number”.format(item.idx, Platform.bold(item.item\_code)) · validation helper — translated “{0} is not a stock Item”.format(item.item\_code).

**Local steps**

- Set stock\_items from self.get\_stock\_items().
- For each item in self.get(“items”).
  - If (flt(item.qty) and flt(item.qty) &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.qty) → flt(item.qty) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: The item {1}, quantity must be positive number”.format(item.idx, Platform.bold(item.item\_code))).
  - If item.item\_code does not belong to stock\_items.
    - Call the validation error handler Platform.throw(translated “{0} is not a stock Item”.format(item.item\_code)).
  - Set item\_details from self.get\_item\_details(Platform.\_dict(mapping(“item\_code” → item.item\_code, “company” → self.company, “project” → self.project, “uom” → item.uom, …)), for\_update = true).
  - Set reset\_fields from tuple(“stock\_uom”, “item\_name”).
  - For each field in reset\_fields.
    - Evaluate item.set(field, item\_details.get(field)).
  - Set update\_fields from tuple(“uom”, “description”, “expense\_account”, “cost\_center”, …).
  - For each field in update\_fields.
    - If not item.get(field).
      - Evaluate item.set(field, item\_details.get(field)).
    - If (field equals “conversion\_factor” and item.uom equals item\_details.get(“stock\_uom”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in field equals “conversion\_factor” → item.uom equals item\_details.get(“stock\_uom”).
      - Evaluate item.set(field, item\_details.get(field)).
  - If (not item.transfer\_qty and item.qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.transfer\_qty → item.qty.
    - Set item.transfer\_qty from flt((flt(item.qty) × flt(item.conversion\_factor)), self.precision(“transfer\_qty”, item)).
  - If self.purpose belongs to list(“Subcontracting Delivery”, “Subcontracting Return”).
    - Set item.expense\_account from Platform.get\_value(“Company”, self.company, “default\_expense\_account”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item details](operations-081.md#op-ed2ef52ca500d9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L833)

<a id="op-868760e915c576"></a>
### Stock Entry.validate fg completed qty

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_finished_goods_completed_quantity`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Since there is a process loss of {0} units for the finished good {1}, you should reduce the quantity by {0}  …”.format(Platform.bold(self.process\_loss\_qty), Platform.bold(d.item\_code)).

**Local steps**

- If (self.purpose differs from “Manufacture” or not self.from\_bom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose differs from “Manufacture” → not self.from\_bom.
  - Return no value.
- Set fg\_qty from defaultdict(float).
- For each d in self.items.
  - If d.is\_finished\_item.
    - Update fg\_qty at d.item\_code using + flt(d.transfer\_qty).
- If not fg\_qty.
  - Return no value.
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Set fg\_item from next(iter(fg\_qty.keys())).
- Set fg\_item\_qty from flt(fg\_qty at fg\_item, precision).
- Set fg\_completed\_qty from flt(self.fg\_completed\_qty, precision).
- For each d in self.items.
  - If not fg\_qty.get(d.item\_code).
    - Continue with the next iteration or loop test.
  - If (fg\_completed\_qty − fg\_item\_qty) &gt; 0.
    - Set self.process\_loss\_qty from (fg\_completed\_qty − fg\_item\_qty).
  - If not self.process\_loss\_qty.
    - Continue with the next iteration or loop test.
  - If fg\_completed\_qty differs from (flt(fg\_item\_qty, precision) + flt(self.process\_loss\_qty, precision)).
    - Call the validation error handler Platform.throw(translated “Since there is a process loss of {0} units for the finished good {1}, you should reduce the quantity by {0}  …”.format(Platform.bold(self.process\_loss\_qty), Platform.bold(d.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L832)

<a id="op-b1e7841d3e5b03"></a>
### Stock Entry.validate finished good qty against fg completed qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_finished_good_qty_against_fg_completed_qty`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with FinishedGoodError — translated “The finished good rows receive {0}, which is more than the Finished Good Quantity {1}. Set Finished Good Qua …”.format(Platform.bold(finished\_qty), Platform.bold(fg\_completed\_qty)).

**Local steps**

- <a id="op-b1e7841d3e5b03-guard-2"></a>If self.purpose does not belong to tuple(“Manufacture”, “Repack”).
  - Return no value.
- If not (self.from\_bom and self.bom\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_bom → self.bom\_no.
  - Return no value.
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “transfer\_qty”).
- Set finished\_qty from flt(self.get\_bom\_item\_finished\_qty(), precision).
- Set fg\_completed\_qty from flt(self.fg\_completed\_qty, precision).
- If finished\_qty &gt; fg\_completed\_qty.
  - Call the validation error handler Platform.throw(translated “The finished good rows receive {0}, which is more than the Finished Good Quantity {1}. Set Finished Good Qua …”.format(Platform.bold(finished\_qty), Platform.bold(fg\_completed\_qty ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to tuple(“Manufacture”, “Repack”), self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b1e7841d3e5b03-guard-2)

**Methods declared on this owner** [get bom item finished qty](operations-077.md#op-9e02cde2492a4e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L758)

<a id="op-9e02cde2492a4e"></a>
### Stock Entry.get bom item finished qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_bom_item_finished_qty`

**Inputs** self.

**Record and data access** read “BOM” via get\_cached\_value · read “Item” via get\_cached\_value.

**Explicit results** sum(generator of flt(row.transfer\_qty) for row drawn from self.items where (row.is\_finished\_item and row.t\_warehouse and not row.s\_warehouse and bom\_item belongs to tuple(row.item\_code, nested operand in the c …).

**Local steps**

- Set bom\_item from Platform.get\_cached\_value(“BOM”, self.bom\_no, “item”).
- Return sum(generator of flt(row.transfer\_qty) for row drawn from self.items where (row.is\_finished\_item and row.t\_warehouse and not row.s\_warehouse and bom\_item belongs to tuple(row.item\_code, nested operand in the c …).
  - Draw row from self.items, keep a combination only if ((row.is\_finished\_item and row.t\_warehouse and not row.s\_warehouse and bom\_item belongs to tuple(row.item\_code, Platform.get\_cached\_value(“Item”, row.item\_code, “variant\_of”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_finished\_item → row.t\_warehouse → not row.s\_warehouse → bom\_item belongs to tuple(row.item\_code, Platform.get\_cached\_value(“Item”, row.item\_code, “variant\_of”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, self.bom\_no, “item”), Platform.get\_cached\_value(“Item”, row.item\_code, “variant\_of”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L691)

<a id="op-eefce60faea7ad"></a>
### Stock Entry.validate difference account

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_difference_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**State and service calls** msgprint with translated “At row #{0}: you have selected the Difference Account {1}, which is a Cost of Goods Sold type account. Pleas …”.format(d.idx, bold(get\_link\_to\_form(“Account”, d.expense\_account))).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please enter &lt;b&gt;Difference Account&lt;/b&gt; or set default &lt;b&gt;Stock Adjustment Account&lt;/b&gt; for company {0}”.format(Platform.bold(self.company)) · validation helper with OpeningEntryAccountError — translated “Difference Account must be a Asset/Liability type account (Temporary Opening), since this Stock Entry is an  …” · validation helper — translated “At row #{0}: the Difference Account must not be a Stock type account, please change the Account Type for the …”.format(d.idx, get\_link\_to\_form(“Account”, d.expense\_account)).

**Local steps**

- If not cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Return no value.
- For each d in self.get(“items”).
  - If not d.expense\_account.
    - Call the validation error handler Platform.throw(translated “Please enter &lt;b&gt;Difference Account&lt;/b&gt; or set default &lt;b&gt;Stock Adjustment Account&lt;/b&gt; for company {0}”.format(Platform.bold(self.company))).
  - Set acc\_details from Platform.get\_cached\_value(“Account”, d.expense\_account, list(“account\_type”, “report\_type”), as\_dict = true).
  - If (self.is\_opening equals “Yes” and acc\_details.report\_type equals “Profit and Loss”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “Yes” → acc\_details.report\_type equals “Profit and Loss”.
    - Call the validation error handler Platform.throw(translated “Difference Account must be a Asset/Liability type account (Temporary Opening), since this Stock Entry is an  …”, OpeningEntryAccountError).
  - If acc\_details.account\_type equals “Stock”.
    - Call the validation error handler Platform.throw(translated “At row #{0}: the Difference Account must not be a Stock type account, please change the Account Type for the …”.format(d.idx, get\_link\_to\_form(“Account”, d.expense\_account)), tit ….
  - If (self.purpose does not belong to list(“Material Issue”, “Subcontracting Delivery”, “Subcontracting Return”) and acc\_details.account\_type equals “Cost of Goods Sold”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose does not belong to list(“Material Issue”, “Subcontracting Delivery”, “Subcontracting Return”) → acc\_details.account\_type equals “Cost of Goods Sold”.
    - Evaluate Platform.msgprint(translated “At row #{0}: you have selected the Difference Account {1}, which is a Cost of Goods Sold type account. Pleas …”.format(d.idx, bold(get\_link\_to\_form(“Account”, d.expense\_accoun ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.expense\_account, list(“account\_type”, “report\_type”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L830)
