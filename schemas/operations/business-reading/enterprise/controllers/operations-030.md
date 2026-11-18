# Shared transaction rules · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Subcontracting controller

<a id="op-cac1228714377d"></a>
### Subcontracting Controller.remove serial and batch bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_remove_serial_and_batch_bundle`

**Inputs** self, item.

**State and service calls** request delete\_doc for “Serial and Batch Bundle”.

**Local steps**

- If item.get(“serial\_and\_batch\_bundle”).
  - Evaluate Platform.delete\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L283) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L704)

<a id="op-ef766b7f398426"></a>
### Subcontracting Controller.get materials from bom

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_materials_from_bill_of_materials`

**Inputs** self, item\_code, bom\_no, exploded\_item = 0.

**Record and data access** read “BOM” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set doctype from “BOM Item” when not exploded\_item, otherwise “BOM Explosion Item”.
  - Value choice on not exploded\_item — true gives “BOM Item”, false gives “BOM Explosion Item”.
- Set fields from list(mapping(“DIV” → list(formatted text ′tab{doctype}′.′stock\_qty′, “′tabBOM′.′quantity′”), “as” → “qty\_consumed\_per\_unit”)).
- Set alias\_dict from mapping(“item\_code” → “rm\_item\_code”, “name” → “bom\_detail\_no”, “source\_warehouse” → “reserve\_warehouse”).
- Set fields\_list from list(“item\_code”, “name”, “rate”, “stock\_uom”, …).
- If doctype equals “BOM Item”.
  - Evaluate fields\_list.extend(list(“is\_phantom\_item”, “bom\_no”)).
- For each field in fields\_list.
  - Evaluate fields.append(formatted text ′tab{doctype}′.′{field}′ As {alias\_dict.get(field, field)}).
- Set filters from list(list(doctype, “parent”, “=”, bom\_no), list(doctype, “docstatus”, “=”, 1), list(“BOM”, “item”, “in”, get\_applicable\_bom\_items(item\_code)), list(doctype, “sourced\_by\_supplier”, “=”, 0)).
- Set data from (Platform.get\_all(“BOM”, fields = fields, filters = filters, order\_by = formatted text ′tab{doctype}′.′idx′) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“BOM”, fields = fields, filters = filters, order\_by = formatted text ′tab{doctype}′.′idx′) → list().
- Set to\_remove from list().
- For each item in data.
  - If item.is\_phantom\_item.
    - Set phantom\_materials from self.\_get\_materials\_from\_bom(item.rm\_item\_code, item.bom\_no, exploded\_item = exploded\_item).
    - For each material in phantom\_materials.
      - Update material.qty\_consumed\_per\_unit using × item.qty\_consumed\_per\_unit.
    - Update data using + phantom\_materials.
    - Evaluate to\_remove.append(item).
- For each item in to\_remove.
  - Evaluate data.remove(item).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L688)

<a id="op-822461b281280f"></a>
### Subcontracting Controller.update reserve warehouse

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_reserve_warehouse`

**Inputs** self, row, item, job\_card\_warehouses.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If (self.doctype equals self.subcontract\_data.order\_doctype and self.doctype differs from “Subcontracting Inward Order”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals self.subcontract\_data.order\_doctype → self.doctype differs from “Subcontracting Inward Order”.
  - Set row.reserve\_warehouse from (self.set\_reserve\_warehouse or job\_card\_warehouses.get(tuple(item.get(“job\_card”), row.rm\_item\_code)) or item.warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.set\_reserve\_warehouse → job\_card\_warehouses.get(tuple(item.get(“job\_card”), row.rm\_item\_code)) → item.warehouse.
- Otherwise.
  - If (Platform.get\_cached\_value(“Item”, row.rm\_item\_code, “is\_customer\_provided\_item”) and self.get(“customer\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, row.rm\_item\_code, “is\_customer\_provided\_item”) → self.get(“customer\_warehouse”).
    - Set row.warehouse from self.customer\_warehouse.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.rm\_item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L727)

<a id="op-29453778f939dc"></a>
### Subcontracting Controller.set alternative item

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_alternative_item`

**Inputs** self, bom\_item.

**Local steps**

- If self.alternative\_item\_details.get(bom\_item.rm\_item\_code).
  - Evaluate bom\_item.update(self.alternative\_item\_details at bom\_item.rm\_item\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L1551) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L705)

<a id="op-87e35a684a8fbf"></a>
### Subcontracting Controller.set serial and batch bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_serial_and_batch_bundle`

**Inputs** self, item\_row, rm\_obj, qty.

**Explicit results** no value · bundle.name.

**Local steps**

- Set key from tuple(rm\_obj.rm\_item\_code, item\_row.item\_code, item\_row.get(self.subcontract\_data.order\_field)).
- If not self.available\_materials.get(key).
  - Return no value.
- If (not self.available\_materials at key at “serial\_no” and not self.available\_materials at key at “batch\_no”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.available\_materials at key at “serial\_no” → not self.available\_materials at key at “batch\_no”.
  - Return no value.
- Set serial\_nos from list().
- Set batches from Platform.\_dict(mapping()).
- If (self.available\_materials.get(key) and self.available\_materials at key at “serial\_no”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “serial\_no”.
  - Set serial\_nos from self.\_\_get\_serial\_nos\_for\_bundle(qty, key).
- Otherwise.
  - If (self.available\_materials.get(key) and self.available\_materials at key at “batch\_no”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “batch\_no”.
    - Set batches from self.\_\_get\_batch\_nos\_for\_bundle(qty, key).
- Set bundle from SerialBatchCreation(Platform.\_dict(mapping(“company” → self.company, “item\_code” → rm\_obj.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “qty” → qty, …))).make\_serial\_and\_batch\_bundle().
  - Value choice on qty &gt; 0 — true gives “Outward”, false gives “Inward”.
- Return bundle.name.

**Methods declared on this owner** [get serial nos for bundle](operations-030.md#op-68eadee10ffe02), [get batch nos for bundle](operations-030.md#op-7087c1e65fa3e9).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L1665) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1039) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L716)

<a id="op-7087c1e65fa3e9"></a>
### Subcontracting Controller.get batch nos for bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_batch_numbers_for_bundle`

**Inputs** self, qty, key.

**Explicit results** available\_batches.

**Local steps**

- Set available\_batches from defaultdict(float).
- Set precision from Platform.get\_precision(“Subcontracting Receipt Supplied Item”, “consumed\_qty”).
- For each tuple(batch\_no, batch\_qty) in self.available\_materials at key at “batch\_no”.items().
  - If flt(batch\_qty, precision) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set qty\_to\_consumed from 0.
  - If qty &gt; 0.
    - If batch\_qty ≥ qty.
      - Set qty\_to\_consumed from qty.
    - Otherwise.
      - Set qty\_to\_consumed from batch\_qty.
    - Update qty using − qty\_to\_consumed.
    - If qty\_to\_consumed &gt; 0.
      - Update available\_batches at batch\_no using + qty\_to\_consumed.
      - Update self.available\_materials at key at “batch\_no” at batch\_no using − qty\_to\_consumed.
- Return available\_batches.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L2413) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L682)

<a id="op-68eadee10ffe02"></a>
### Subcontracting Controller.get serial nos for bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_serial_numbers_for_bundle`

**Inputs** self, qty, key.

**Explicit results** serial\_nos.

**Local steps**

- Set available\_sns from sorted(self.available\_materials at key at “serial\_no”) at slice 0 to cint(qty).
- Set serial\_nos from list().
- For each serial\_no in available\_sns.
  - Evaluate serial\_nos.append(serial\_no).
  - Evaluate self.available\_materials at key at “serial\_no”.remove(serial\_no).
- Return serial\_nos.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L2814) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L692)

<a id="op-bb036061907bfd"></a>
### Subcontracting Controller.add supplied or received item

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_add_supplied_or_received_item`

**Inputs** self, item\_row, bom\_item, qty.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set bom\_item.conversion\_factor from item\_row.conversion\_factor.
- If self.subcontract\_data.order\_doctype equals “Subcontracting Inward Order”.
  - Evaluate bom\_item.pop(“rate”).
- Set rm\_obj from self.append(self.raw\_material\_table, bom\_item).
- If rm\_obj.get(“qty”).
  - Set rm\_obj.qty from 0.0.
- Set rm\_obj.reference\_name from item\_row.name.
- Set use\_serial\_batch\_fields from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
- If self.doctype equals self.subcontract\_data.order\_doctype.
  - Set rm\_obj.required\_qty from flt(qty, rm\_obj.precision(“required\_qty”)).
  - If self.doctype differs from “Subcontracting Inward Order”.
    - Set rm\_obj.amount from flt((rm\_obj.required\_qty × rm\_obj.rate), rm\_obj.precision(“amount”)).
- Otherwise.
  - Set rm\_obj.consumed\_qty from flt(qty, rm\_obj.precision(“consumed\_qty”)).
  - Set rm\_obj.required\_qty from flt((bom\_item.required\_qty or qty), rm\_obj.precision(“required\_qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bom\_item.required\_qty → qty.
  - Set rm\_obj.serial\_and\_batch\_bundle from no value.
  - Evaluate setattr(rm\_obj, self.subcontract\_data.order\_field, item\_row.get(self.subcontract\_data.order\_field)).
  - Set return\_key from tuple(item\_row.get(“subcontracting\_receipt\_item”), rm\_obj.rm\_item\_code).
  - If return\_key belongs to self.returnable\_serial\_batches.
    - Evaluate self.set\_serial\_batch\_for\_return(rm\_obj, self.returnable\_serial\_batches at return\_key).
    - Return no value.
  - If use\_serial\_batch\_fields.
    - Set rm\_obj.use\_serial\_batch\_fields from 1.
    - If not self.flags.get(“reset\_raw\_materials”).
      - Evaluate self.\_\_set\_batch\_nos(bom\_item, item\_row, rm\_obj, qty).
- If self.doctype equals “Subcontracting Receipt”.
  - If not use\_serial\_batch\_fields.
    - Set rm\_obj.serial\_and\_batch\_bundle from self.\_\_set\_serial\_and\_batch\_bundle(item\_row, rm\_obj, rm\_obj.consumed\_qty).
    - Evaluate self.set\_rate\_for\_supplied\_items(rm\_obj, item\_row).
  - Otherwise.
    - If self.backflush\_based\_on equals “BOM”.
      - Evaluate self.update\_rate\_for\_supplied\_items().
      - Evaluate self.set\_batch\_for\_supplied\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set serial batch for return](operations-029.md#op-ae7d1fa5b942ce), [set batch nos](operations-030.md#op-7f8da589ba4553), [set serial and batch bundle](operations-030.md#op-87e35a684a8fbf), [set rate for supplied items](operations-030.md#op-8624f79d9d07d8), [update rate for supplied items](operations-030.md#op-860162f0d3c4be), [set batch for supplied items](operations-030.md#op-f32f43c42df9df).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L675)

<a id="op-f32f43c42df9df"></a>
### Subcontracting Controller.set batch for supplied items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_batch_for_supplied_items`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** request copy\_doc for row.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_serial\_nos\_for\_outward.
- Bind dependencies get\_used\_serial\_nos.
- If self.is\_return.
  - Return no value.
- For each row in self.supplied\_items.
  - Set item\_details from Platform.get\_cached\_value(“Item”, row.rm\_item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = 1).
  - If (not item\_details.has\_batch\_no and not item\_details.has\_serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_details.has\_batch\_no → not item\_details.has\_serial\_no.
    - Continue with the next iteration or loop test.
  - If not row.use\_serial\_batch\_fields.
    - Continue with the next iteration or loop test.
  - Set kwargs from Platform.\_dict(mapping(“item\_code” → row.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).
  - If (item\_details.has\_serial\_no and not row.serial\_and\_batch\_bundle and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details.has\_serial\_no → not row.serial\_and\_batch\_bundle → not row.serial\_no.
    - Set kwargs at “ignore\_serial\_nos” from list(get\_used\_serial\_nos(self, “supplied\_items”)).
    - Set serial\_nos from get\_available\_serial\_nos(kwargs).
    - If serial\_nos.
      - Set serial\_nos from list of sn.get(“serial\_no”) for sn drawn from serial\_nos.
        - Draw sn from serial\_nos.
      - Set row.serial\_no from whitespace '\\n'.join(serial\_nos).
  - Otherwise.
    - If (item\_details.has\_batch\_no and not row.serial\_and\_batch\_bundle and (not row.batch\_no or self.batch\_has\_not\_available(row.batch\_no, row.consumed\_qty))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details.has\_batch\_no → not row.serial\_and\_batch\_bundle → (not row.batch\_no or self.batch\_has\_not\_available(row.batch\_no, row.consumed\_qty)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.batch\_no → self.batch\_has\_not\_available(row.batch\_no, row.consumed\_qty).
      - Set batches from get\_auto\_batch\_nos(kwargs).
      - If batches.
        - Set consumed\_qty from row.consumed\_qty.
        - For each tuple(index, d) in enumerate(batches).
          - <a id="op-f32f43c42df9df-guard-45"></a>If consumed\_qty ≤ 0.
            - Leave the innermost loop without its normal-exhaustion alternative.
          - If index equals 0.
            - Set row.batch\_no from d.get(“batch\_no”).
            - Set row.consumed\_qty from d.get(“qty”).
            - Update consumed\_qty using − d.get(“qty”).
          - Otherwise.
            - Set new\_row from self.append(“supplied\_items”, mapping()).
            - Evaluate new\_row.update(Platform.copy\_doc(row).as\_dict()).
            - Evaluate new\_row.update(mapping(“consumed\_qty” → d.get(“qty”), “batch\_no” → d.get(“batch\_no”), “rate” → row.rate, “amount” → (flt(d.get(“qty”)) × flt(row.rate)))).
            - Update consumed\_qty using − d.get(“qty”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison consumed\_qty ≤ 0, consumed\_qty = 0 selects the branch that exits the enclosing loop. With consumed\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f32f43c42df9df-guard-45)

**Methods declared on this owner** [batch has not available](operations-030.md#op-1b63a4f6deb07d).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.rm\_item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L707)

<a id="op-1b63a4f6deb07d"></a>
### Subcontracting Controller.batch has not available

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_batch_has_not_available`

**Inputs** self, batch\_no, qty\_required.

**Explicit results** batch\_qty &lt; qty\_required.

**Local steps**

- Set batch\_qty from get\_batch\_qty\_for\_stock(batch\_no, self.supplier\_warehouse, consider\_negative\_batches = true).
- Return batch\_qty &lt; qty\_required.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L676)

<a id="op-860162f0d3c4be"></a>
### Subcontracting Controller.update rate for supplied items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_rate_for_supplied_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.doctype differs from “Subcontracting Receipt”.
  - Return no value.
- For each row in self.supplied\_items.
  - Set item\_row from no value.
  - If row.reference\_name.
    - Set item\_row from self.get\_item\_row(row.reference\_name).
  - If not item\_row.
    - Continue with the next iteration or loop test.
  - Evaluate self.set\_rate\_for\_supplied\_items(row, item\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item row](operations-030.md#op-483b55dd373a85), [set rate for supplied items](operations-030.md#op-8624f79d9d07d8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L5320) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L725)

<a id="op-483b55dd373a85"></a>
### Subcontracting Controller.get item row

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_item_row`

**Inputs** self, reference\_name.

**Explicit results** item.

**Local steps**

- For each item in self.items.
  - If item.name equals reference\_name.
    - Return item.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L5514) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L687)

<a id="op-8624f79d9d07d8"></a>
### Subcontracting Controller.set rate for supplied items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_rate_for_supplied_items`

**Inputs** self, rm\_obj, item\_row.

**Explicit results** no value.

**Local steps**

- If self.is\_return.
  - Return no value.
- Set args from Platform.\_dict(mapping(“item\_code” → rm\_obj.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).
- If rm\_obj.serial\_and\_batch\_bundle.
  - Set args at “serial\_and\_batch\_bundle” from rm\_obj.serial\_and\_batch\_bundle.
- If rm\_obj.use\_serial\_batch\_fields.
  - Set args at “batch\_no” from rm\_obj.batch\_no.
  - Set args at “serial\_no” from rm\_obj.serial\_no.
- Set rm\_obj.rate from \_get\_incoming\_rate(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1038) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L715)

<a id="op-7f8da589ba4553"></a>
### Subcontracting Controller.set batch nos

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_batch_numbers`

**Inputs** self, bom\_item, item\_row, rm\_obj, qty.

**Explicit results** no value.

**Local steps**

- Set key from tuple(rm\_obj.rm\_item\_code, item\_row.item\_code, item\_row.get(self.subcontract\_data.order\_field)).
- If (self.available\_materials.get(key) and self.available\_materials at key at “batch\_no”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “batch\_no”.
  - Set new\_rm\_obj from no value.
  - For each tuple(batch\_no, batch\_qty) in self.available\_materials at key at “batch\_no”.items().
    - If (batch\_qty ≥ qty or (rm\_obj.consumed\_qty equals 0 and self.backflush\_based\_on equals “BOM” and len(nested operand in the contract.available\_materials at key at “batch\_no”) equals 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in batch\_qty ≥ qty → (rm\_obj.consumed\_qty equals 0 and self.backflush\_based\_on equals “BOM” and len(self.available\_materials at key at “batch\_no”) equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in rm\_obj.consumed\_qty equals 0 → self.backflush\_based\_on equals “BOM” → len(self.available\_materials at key at “batch\_no”) equals 1.
      - If rm\_obj.consumed\_qty equals 0.
        - Evaluate self.\_\_set\_consumed\_qty(rm\_obj, qty).
      - Evaluate self.\_\_set\_batch\_no\_as\_per\_qty(item\_row, rm\_obj, batch\_no, qty).
      - Update self.available\_materials at key at “batch\_no” at batch\_no using − qty.
      - Return no value.
    - Otherwise.
      - If (qty &gt; 0 and batch\_qty &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty &gt; 0 → batch\_qty &gt; 0.
        - Update qty using − batch\_qty.
        - Set new\_rm\_obj from self.append(self.raw\_material\_table, bom\_item).
        - Set new\_rm\_obj.serial\_and\_batch\_bundle from no value.
        - Set new\_rm\_obj.use\_serial\_batch\_fields from 1.
        - Set new\_rm\_obj.reference\_name from item\_row.name.
        - Evaluate self.\_\_set\_batch\_no\_as\_per\_qty(item\_row, new\_rm\_obj, batch\_no, batch\_qty).
        - Set self.available\_materials at key at “batch\_no” at batch\_no from 0.
  - If new\_rm\_obj.
    - Evaluate self.remove(rm\_obj).
  - Otherwise.
    - If abs(qty) &gt; 0.
      - Evaluate self.\_\_set\_consumed\_qty(rm\_obj, qty).
- Otherwise.
  - Evaluate self.\_\_set\_consumed\_qty(rm\_obj, qty, (bom\_item.required\_qty or qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bom\_item.required\_qty → qty.
  - Evaluate self.\_\_set\_serial\_nos(item\_row, rm\_obj).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set consumed qty](operations-030.md#op-b97dbf1cc496a5), [set batch no as per qty](operations-030.md#op-94ab8f45f9d2e1), [set serial nos](operations-030.md#op-6125f765f574b8).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L6091) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L709)

<a id="op-b97dbf1cc496a5"></a>
### Subcontracting Controller.set consumed qty

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_consumed_quantity`

**Inputs** self, rm\_obj, consumed\_qty, required\_qty = 0.

**Local steps**

- Set rm\_obj.required\_qty from flt(required\_qty, rm\_obj.precision(“required\_qty”)).
- Set rm\_obj.consumed\_qty from flt(consumed\_qty, rm\_obj.precision(“consumed\_qty”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L7015) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L710)

<a id="op-6125f765f574b8"></a>
### Subcontracting Controller.set serial nos

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_serial_numbers`

**Inputs** self, item\_row, rm\_obj.

**Local steps**

- Set key from tuple(rm\_obj.rm\_item\_code, item\_row.item\_code, item\_row.get(self.subcontract\_data.order\_field)).
- If (self.available\_materials.get(key) and self.available\_materials at key at “serial\_no”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “serial\_no”.
  - Set used\_serial\_nos from self.available\_materials at key at “serial\_no” at slice 0 to cint(rm\_obj.consumed\_qty).
  - Set rm\_obj.serial\_no from whitespace '\\n'.join(used\_serial\_nos).
  - For each sn in used\_serial\_nos.
    - Evaluate self.available\_materials at key at “serial\_no”.remove(sn).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1040) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L717)

<a id="op-94ab8f45f9d2e1"></a>
### Subcontracting Controller.set batch no as per qty

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_batch_number_as_per_quantity`

**Inputs** self, item\_row, rm\_obj, batch\_no, qty.

**Local steps**

- Evaluate rm\_obj.update(mapping(“consumed\_qty” → qty, “batch\_no” → batch\_no, “required\_qty” → qty, self.subcontract\_data.order\_field → item\_row.get(self.subcontract\_data.order\_field))).
- Evaluate self.\_\_set\_serial\_nos(item\_row, rm\_obj).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set serial nos](operations-030.md#op-6125f765f574b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L340) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L708)

<a id="op-fd701a11e626a3"></a>
### Subcontracting Controller.get qty based on material transfer

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_quantity_based_on_material_transfer`

**Inputs** self, item\_row, transfer\_item.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** transfer\_item.qty · Platform.utils.ceil(qty) · qty.

**Local steps**

- Set key from tuple(item\_row.item\_code, item\_row.get(self.subcontract\_data.order\_field), item\_row.get(“bom”)).
- If self.qty\_to\_be\_received equals item\_row.qty.
  - Return transfer\_item.qty.
- If self.qty\_to\_be\_received.get(key).
  - Set qty from ((self.get\_qty\_for\_costing(item\_row) × flt(transfer\_item.qty)) ÷ flt(self.qty\_to\_be\_received.get(key))).
  - Set transfer\_item.item\_details.required\_qty from transfer\_item.qty.
  - If (transfer\_item.serial\_no or Platform.get\_cached\_value(“UOM”, transfer\_item.item\_details.stock\_uom, “must\_be\_whole\_number”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transfer\_item.serial\_no → Platform.get\_cached\_value(“UOM”, transfer\_item.item\_details.stock\_uom, “must\_be\_whole\_number”).
    - Return Platform.utils.ceil(qty).
  - Return qty.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty for costing](operations-031.md#op-17e3a48aaee02f).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, transfer\_item.item\_details.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L690)

<a id="op-11effd03c89e0e"></a>
### Subcontracting Controller.get job card source warehouses

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_job_card_source_warehouses`

**Inputs** self.

**Record and data access** read “Job Card Item” via get\_all.

**Explicit results** mapping() · mapping of tuple(d.parent, d.item\_code) → d.source\_warehouse for d drawn from rows.

**Local steps**

- Set job\_cards from set of row.job\_card for row drawn from self.items where row.get(“job\_card”).
  - Draw row from self.items, keep a combination only if (row.get(“job\_card”)).
- If (self.doctype differs from self.subcontract\_data.order\_doctype or not job\_cards).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype differs from self.subcontract\_data.order\_doctype → not job\_cards.
  - Return mapping().
- Set rows from Platform.get\_all(“Job Card Item”, filters = mapping(“parent” → tuple(“in”, list(job\_cards))), fields = list(“parent”, “item\_code”, “source\_warehouse”)).
- Return mapping of tuple(d.parent, d.item\_code) → d.source\_warehouse for d drawn from rows.
  - Draw d from rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L432)

<a id="op-99fffc6f1ec1b3"></a>
### Subcontracting Controller.set supplied or received items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_supplied_or_received_items`

**Inputs** self.

**Local steps**

- Set self.bom\_items from mapping().
- Set job\_card\_warehouses from self.get\_job\_card\_source\_warehouses().
- Set has\_items from true when self.get(self.raw\_material\_table), otherwise false.
  - Value choice on self.get(self.raw\_material\_table) — true gives true, false gives false.
- Set kept\_rows from list of row for row drawn from self.items where (self.doctype differs from self.subcontract\_data.order\_doctype and ((self.\_\_changed\_name and row.name does not belong to self.\_\_changed\_name) or (has\_items a ….
  - Draw row from self.items, keep a combination only if ((self.doctype differs from self.subcontract\_data.order\_doctype and ((self.\_\_changed\_name and row.name does not belong to self.\_\_changed\_name) or (has\_items and not self.\_\_changed\_name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype differs from self.subcontract\_data.order\_doctype → ((self.\_\_changed\_name and row.name does not belong to self.\_\_changed\_name) or (has\_items and not self.\_\_changed\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.\_\_changed\_name and row.name does not belong to self.\_\_changed\_name) → (has\_items and not self.\_\_changed\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_\_changed\_name → row.name does not belong to self.\_\_changed\_name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_items → not self.\_\_changed\_name.
- Evaluate self.count\_kept\_return\_rows(kept\_rows).
- For each row in self.items.
  - If row belongs to kept\_rows.
    - Continue with the next iteration or loop test.
  - If self.is\_subcontracting\_receipt\_return().
    - Evaluate self.add\_returned\_raw\_materials(row).
  - Otherwise.
    - If (self.doctype equals self.subcontract\_data.order\_doctype or (self.backflush\_based\_on equals “BOM” or self.is\_return)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals self.subcontract\_data.order\_doctype → (self.backflush\_based\_on equals “BOM” or self.is\_return).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.backflush\_based\_on equals “BOM” → self.is\_return.
      - For each bom\_item in self.\_get\_materials\_from\_bom(row.item\_code, row.bom, row.get(“include\_exploded\_items”)).
        - Set qty from ((flt(bom\_item.qty\_consumed\_per\_unit) × flt((row.get(“received\_qty”) or (row.qty + (nested operand in the contract(nested operand in the contract) or 0))))) × row.conversion\_factor).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“received\_qty”) → (row.qty + (row.get(“rejected\_qty”) or 0)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“rejected\_qty”) → 0.
        - Set bom\_item.main\_item\_code from row.item\_code.
        - Evaluate self.\_\_update\_reserve\_warehouse(bom\_item, row, job\_card\_warehouses).
        - Evaluate self.\_\_set\_alternative\_item(bom\_item).
        - Evaluate self.\_\_add\_supplied\_or\_received\_item(row, bom\_item, qty).
    - Otherwise.
      - If self.backflush\_based\_on differs from “BOM”.
        - For each tuple(key, transfer\_item) in self.available\_materials.items().
          - If (tuple(key at 1, key at 2) equals tuple(row.item\_code, row.get(self.subcontract\_data.order\_field)) and transfer\_item.qty &gt; 0).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in tuple(key at 1, key at 2) equals tuple(row.item\_code, row.get(self.subcontract\_data.order\_field)) → transfer\_item.qty &gt; 0.
            - Set qty from flt(self.\_\_get\_qty\_based\_on\_material\_transfer(row, transfer\_item)).
            - Update transfer\_item.qty using − qty.
            - Evaluate self.\_\_add\_supplied\_or\_received\_item(row, transfer\_item.get(“item\_details”), qty).
        - If self.qty\_to\_be\_received.
          - Update self.qty\_to\_be\_received at tuple(row.item\_code, row.get(self.subcontract\_data.order\_field), row.get(“bom”)) using − self.get\_qty\_for\_costing(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get job card source warehouses](operations-030.md#op-11effd03c89e0e), [count kept return rows](operations-028.md#op-3b3a961c21f91c), [is subcontracting receipt return](operations-028.md#op-a9d0e47e1ced68), [add returned raw materials](operations-028.md#op-1218478997d6c0), [get materials from bom](operations-030.md#op-ef766b7f398426), [update reserve warehouse](operations-030.md#op-822461b281280f), [set alternative item](operations-030.md#op-29453778f939dc), [add supplied or received item](operations-030.md#op-bb036061907bfd), [get qty based on material transfer](operations-030.md#op-fd701a11e626a3), [get qty for costing](operations-031.md#op-17e3a48aaee02f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L719)

<a id="op-3dee0b7f319a11"></a>
### Subcontracting Controller.set rate for serial and batch bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_rate_for_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If self.doctype differs from “Subcontracting Receipt”.
  - Return no value.
- For each row in self.get(self.raw\_material\_table).
  - If not row.get(“serial\_and\_batch\_bundle”).
    - Continue with the next iteration or loop test.
  - Set row.rate from Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “avg\_rate”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “avg\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L2012) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1037) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L714)

<a id="op-e3efcb82aee2f0"></a>
### Subcontracting Controller.modify serial and batch bundle

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_modify_serial_and_batch_bundle`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or self.get(“is\_return”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.get(“is\_return”).
  - Return no value.
- If self.doctype differs from “Subcontracting Receipt”.
  - Return no value.
- For each item\_row in self.items.
  - If (self.\_\_changed\_name and item\_row.name belongs to self.\_\_changed\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_\_changed\_name → item\_row.name belongs to self.\_\_changed\_name.
    - Continue with the next iteration or loop test.
  - Set modified\_data from self.\_\_get\_bundle\_to\_modify(item\_row.name).
  - If modified\_data.
    - Set serial\_nos from list().
    - Set batches from Platform.\_dict(mapping()).
    - Set key from tuple(modified\_data.rm\_item\_code, item\_row.item\_code, item\_row.get(self.subcontract\_data.order\_field)).
    - If (self.available\_materials.get(key) and self.available\_materials at key at “serial\_no”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “serial\_no”.
      - Set serial\_nos from self.\_\_get\_serial\_nos\_for\_bundle(modified\_data.consumed\_qty, key).
    - Otherwise.
      - If (self.available\_materials.get(key) and self.available\_materials at key at “batch\_no”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_materials.get(key) → self.available\_materials at key at “batch\_no”.
        - Set batches from self.\_\_get\_batch\_nos\_for\_bundle(modified\_data.consumed\_qty, key).
    - Evaluate SerialBatchCreation(mapping(“item\_code” → modified\_data.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “serial\_and\_batch\_bundle” → modified\_data.serial\_and\_batch\_bundle, “type\_of\_transaction” → “Outw …().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bundle to modify](operations-030.md#op-cbbe9bb3233c96), [get serial nos for bundle](operations-030.md#op-68eadee10ffe02), [get batch nos for bundle](operations-030.md#op-7087c1e65fa3e9).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L700)

<a id="op-cbbe9bb3233c96"></a>
### Subcontracting Controller.get bundle to modify

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_bundle_to_modify`

**Inputs** self, name.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Explicit results** row.

**Local steps**

- For each row in self.get(“supplied\_items”).
  - If (row.reference\_name equals name and row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_name equals name → row.serial\_and\_batch\_bundle.
    - If row.consumed\_qty differs from abs(Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “total\_qty”)).
      - Return row.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “total\_qty”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L2888) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L683)

<a id="op-80cb4a7991f343"></a>
### Subcontracting Controller.prepare supplied or received items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_prepare_supplied_or_received_items`

**Inputs** self.

**Local steps**

- Evaluate self.initialized\_fields().
- Evaluate self.\_\_get\_subcontract\_orders().
- Evaluate self.\_\_get\_pending\_qty\_to\_receive().
- Evaluate self.get\_available\_materials().
- Set self.returnable\_serial\_batches from self.get\_returnable\_serial\_batches().
- Set self.returnable\_raw\_materials from self.get\_returnable\_raw\_materials().
- Evaluate self.\_\_remove\_changed\_rows().
- Evaluate self.\_\_set\_supplied\_or\_received\_items().
- Evaluate self.\_\_modify\_serial\_and\_batch\_bundle().
- Evaluate self.\_\_set\_rate\_for\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialized fields](operations-029.md#op-424667fff2569b), [get subcontract orders](operations-029.md#op-e3716ec4f97c2d), [get pending qty to receive](operations-029.md#op-0f369db3134437), [get available materials](operations-029.md#op-511b4c38bd0d44), [get returnable serial batches](operations-029.md#op-dd5f644b7b33af), [get returnable raw materials](operations-028.md#op-c5d16d8bcd70f4), [remove changed rows](operations-029.md#op-ee1fcf5a551bac), [set supplied or received items](operations-030.md#op-99fffc6f1ec1b3), [modify serial and batch bundle](operations-030.md#op-e3efcb82aee2f0), [set rate for serial and batch bundle](operations-030.md#op-3dee0b7f319a11).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L701)
