# Inventory and warehouses · operations 80

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-50758a10b3e86f"></a>
### Stock Entry.set bomless secondary valuation types

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_bomless_secondary_valuation_types`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: % of Component Cost needs a BOM secondary item. Choose Valuation Rate or Manual for {1}.”.format(d.idx, Platform.bold(d.item\_code)).

**Local steps**

- For each d in self.get(“items”).
  - If d.bom\_secondary\_item.
    - Continue with the next iteration or loop test.
  - If not d.secondary\_item\_type.
    - If d.valuation\_type.
      - Set d.valuation\_type from empty text.
      - Set d.set\_basic\_rate\_manually from 0.
    - Continue with the next iteration or loop test.
  - If d.valuation\_type equals “% of Component Cost”.
    - Call the validation error handler Platform.throw(translated “Row #{0}: % of Component Cost needs a BOM secondary item. Choose Valuation Rate or Manual for {1}.”.format(d.idx, Platform.bold(d.item\_code))).
  - If not d.valuation\_type.
    - Set d.valuation\_type from “Valuation Rate”.
  - Set d.set\_basic\_rate\_manually from cint(d.valuation\_type equals “Manual”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L807)

<a id="op-9075245b5da830"></a>
### Stock Entry.get costed out items cost

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_costed_out_items_cost`

**Inputs** self.

**Declared result** float.

**Explicit results** sum(generator of flt(d.basic\_amount) for d drawn from self.get(“items”) where is\_costed\_out\_of\_finished\_item(d)).

**Local steps**

- Return sum(generator of flt(d.basic\_amount) for d drawn from self.get(“items”) where is\_costed\_out\_of\_finished\_item(d)).
  - Draw d from self.get(“items”), keep a combination only if (is\_costed\_out\_of\_finished\_item(d)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L3571) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L781)

<a id="op-79f62850e78ea4"></a>
### Stock Entry.get secondary items cost basis

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_secondary_items_cost_basis`

**Inputs** self, outgoing\_items\_cost.

**Declared result** float.

**Record and data access** read “Manufacturing Settings” via get\_single.

**Explicit results** outgoing\_items\_cost · self.\_fetch\_consumption\_entry\_cost().

**Local steps**

- If (outgoing\_items\_cost or self.purpose differs from “Manufacture” or not self.work\_order).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in outgoing\_items\_cost → self.purpose differs from “Manufacture” → not self.work\_order.
  - Return outgoing\_items\_cost.
- Set settings from Platform.get\_single(“Manufacturing Settings”).
- If not (settings.material\_consumption and settings.get\_rm\_cost\_from\_consumption\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.material\_consumption → settings.get\_rm\_cost\_from\_consumption\_entry.
  - Return outgoing\_items\_cost.
- If not self.get\_consumption\_entries().
  - Return outgoing\_items\_cost.
- Return self.\_fetch\_consumption\_entry\_cost().

**Methods declared on this owner** [get consumption entries](operations-079.md#op-0e40d62c0f4c78), [fetch consumption entry cost](operations-080.md#op-62e734cd36f637).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L790)

<a id="op-62e734cd36f637"></a>
### Stock Entry.fetch consumption entry cost

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_fetch_consumption_entry_cost`

**Inputs** self.

**Explicit results** (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).

**Local steps**

- Set SE from Platform.qb.DocType(“Stock Entry”).
- Set SE\_ITEM from Platform.qb.DocType(“Stock Entry Detail”).
- Return (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L4838) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L774)

<a id="op-93ae4681686091"></a>
### Stock Entry.get basic rate for manufactured item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_basic_rate_for_manufactured_item`

**Inputs** self, finished\_item\_qty, outgoing\_items\_cost = 0, has\_consumption\_basis = false.

**Declared result** float.

**Record and data access** read “Manufacturing Settings” via get\_single · read “Stock Entry” via exists.

**Explicit results** flt((cost\_left ÷ finished\_item\_qty)) when finished\_item\_qty, otherwise 0.0.

**Explicit failure paths** validation helper — translated “Row {0}: As {1} is enabled, raw materials cannot be added to {2} entry. Use {3} entry to consume raw materials.”.format(item.idx, Platform.bold(label), Platform.bold(translated “Manufacture”),  … · validation helper — translated “Only one {0} entry can be created against the Work Order {1}”.format(Platform.bold(translated “Manufacture”), Platform.bold(self.work\_order)).

**Local steps**

- Set settings from Platform.get\_single(“Manufacturing Settings”).
- Set scrap\_items\_cost from self.get\_costed\_out\_items\_cost().
- Set tuple(manual\_qty, manual\_cost) from self.get\_manually\_rated\_finished\_items().
- If settings.material\_consumption.
  - If (settings.get\_rm\_cost\_from\_consumption\_entry and self.work\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.get\_rm\_cost\_from\_consumption\_entry → self.work\_order.
    - If self.get\_consumption\_entries().
      - For each item in self.items.
        - If (not item.is\_finished\_item and not item.secondary\_item\_type and not item.valuation\_type).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_finished\_item → not item.secondary\_item\_type → not item.valuation\_type.
          - Set label from Platform.get\_meta(settings.doctype).get\_label(“get\_rm\_cost\_from\_consumption\_entry”).
          - Call the validation error handler Platform.throw(translated “Row {0}: As {1} is enabled, raw materials cannot be added to {2} entry. Use {3} entry to consume raw materials.”.format(item.idx, Platform.bold(label), Platform.bold(translated “ ….
      - If Platform.db.exists(“Stock Entry”, mapping(“docstatus” → 1, “work\_order” → self.work\_order, “purpose” → “Manufacture”, “name” → tuple(“!=”, self.name))).
        - Call the validation error handler Platform.throw(translated “Only one {0} entry can be created against the Work Order {1}”.format(Platform.bold(translated “Manufacture”), Platform.bold(self.work\_order))).
      - Set outgoing\_items\_cost from self.\_fetch\_consumption\_entry\_cost().
  - Otherwise.
    - If (not outgoing\_items\_cost and not has\_consumption\_basis).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not outgoing\_items\_cost → not has\_consumption\_basis.
      - Set bom\_items from self.get\_bom\_raw\_materials((finished\_item\_qty + manual\_qty), split\_alternative\_items = false).
      - Set outgoing\_items\_cost from sum(list of (flt(row.qty) × flt(row.rate)) for row drawn from bom\_items.values()).
        - Draw row from bom\_items.values().
- Set cost\_left from ((outgoing\_items\_cost − scrap\_items\_cost) − manual\_cost).
- If self.flags.via\_repost.
  - Set cost\_left from max(cost\_left, 0).
- Return flt((cost\_left ÷ finished\_item\_qty)) when finished\_item\_qty, otherwise 0.0.
  - Value choice on finished\_item\_qty — true gives flt((cost\_left ÷ finished\_item\_qty)), false gives 0.0.

**Methods declared on this owner** [get costed out items cost](operations-080.md#op-9075245b5da830), [get manually rated finished items](operations-079.md#op-d0e6e888b86d29), [get consumption entries](operations-079.md#op-0e40d62c0f4c78), [fetch consumption entry cost](operations-080.md#op-62e734cd36f637), [get bom raw materials](operations-082.md#op-429d929193c3f8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L777)

<a id="op-84acc38a3d574d"></a>
### Stock Entry.distribute additional costs

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_distribute_additional_costs`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not any(generator of d.item\_code for d drawn from self.items where d.t\_warehouse).
  - Draw d from self.items, keep a combination only if (d.t\_warehouse).
  - Set self.additional\_costs from list().
- Set self.total\_additional\_costs from sum(generator of flt(t.base\_amount) for t drawn from self.get(“additional\_costs”)).
  - Draw t from self.get(“additional\_costs”).
- Set tuple(incoming\_items, basis, total\_basis) from self.get\_additional\_cost\_allocation().
- For each d in self.get(“items”).
  - Set d.additional\_cost from 0.
- If not total\_basis.
  - Return no value.
- For each d in incoming\_items.
  - Set d.additional\_cost from ((flt(d.get(basis)) ÷ total\_basis) × self.total\_additional\_costs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get additional cost allocation](operations-080.md#op-c68d4b11c35a9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L5190) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L773)

<a id="op-c68d4b11c35a9a"></a>
### Stock Entry.get additional cost allocation

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_additional_cost_allocation`

**Inputs** self.

**Explicit results** tuple(incoming\_items, “basic\_amount”, total\_basic\_amount) · tuple(incoming\_items, “transfer\_qty”, sum(generator of flt(d.transfer\_qty) for d drawn from incoming\_items)).

**Local steps**

- If self.purpose belongs to tuple(“Repack”, “Manufacture”).
  - Set incoming\_items from list of d for d drawn from self.get(“items”) where d.is\_finished\_item.
    - Draw d from self.get(“items”), keep a combination only if (d.is\_finished\_item).
- Otherwise.
  - Set incoming\_items from list of d for d drawn from self.get(“items”) where d.t\_warehouse.
    - Draw d from self.get(“items”), keep a combination only if (d.t\_warehouse).
- Set total\_basic\_amount from sum(generator of flt(d.basic\_amount) for d drawn from incoming\_items).
  - Draw d from incoming\_items.
- If total\_basic\_amount.
  - Return tuple(incoming\_items, “basic\_amount”, total\_basic\_amount).
- Return tuple(incoming\_items, “transfer\_qty”, sum(generator of flt(d.transfer\_qty) for d drawn from incoming\_items)).
  - Draw d from incoming\_items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L5574) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L775)

<a id="op-542e0c6e5e1320"></a>
### Stock Entry.update valuation rate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_valuation_rate`

**Inputs** self, reset\_outgoing\_rate = true.

**Local steps**

- For each d in self.get(“items”).
  - If (not reset\_outgoing\_rate and d.s\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not reset\_outgoing\_rate → d.s\_warehouse.
    - Continue with the next iteration or loop test.
  - If d.transfer\_qty.
    - Set d.amount from flt(flt(((flt(d.basic\_amount) + flt(d.additional\_cost)) + flt(d.landed\_cost\_voucher\_amount))), d.precision(“amount”)).
    - Set d.valuation\_rate from (flt(d.basic\_rate) + (flt((flt(d.additional\_cost) + flt(d.landed\_cost\_voucher\_amount))) ÷ flt(d.transfer\_qty))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L5925) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L824)

<a id="op-3306fd55966436"></a>
### Stock Entry.set total incoming outgoing value

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_total_incoming_outgoing_value`

**Inputs** self.

**Local steps**

- Set self.total\_incoming\_value, self.total\_outgoing\_value from 0.0.
- For each d in self.get(“items”).
  - If d.t\_warehouse.
    - Update self.total\_incoming\_value using + flt(d.amount).
  - If d.s\_warehouse.
    - Update self.total\_outgoing\_value using + flt(d.amount).
- Set self.value\_difference from (self.total\_incoming\_value − self.total\_outgoing\_value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6286) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L816)

<a id="op-14b64f1a9b0c9b"></a>
### Stock Entry.set total amount

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_total_amount`

**Inputs** self.

**Local steps**

- Set self.total\_amount from no value.
- If self.purpose does not belong to list(“Manufacture”, “Repack”).
  - Set self.total\_amount from sum(list of flt(item.amount) for item drawn from self.get(“items”)).
    - Draw item from self.get(“items”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6502) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L815)

<a id="op-432339854632b9"></a>
### Stock Entry.set stock entry type

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_stock_entry_type`

**Inputs** self.

**Record and data access** read “Stock Entry Type” via get\_cached\_value.

**Local steps**

- If self.purpose.
  - Set self.stock\_entry\_type from Platform.get\_cached\_value(“Stock Entry Type”, mapping(“purpose” → self.purpose, “is\_standard” → 1), “name”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry Type”, mapping(“purpose” → self.purpose, “is\_standard” → 1), “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6668) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L814)

<a id="op-e99ad7ea056d14"></a>
### Stock Entry.set purpose for stock entry

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_purpose_for_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry Type” via get\_cached\_value.

**Local steps**

- If (self.stock\_entry\_type and not self.purpose).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.stock\_entry\_type → not self.purpose.
  - Set self.purpose from Platform.get\_cached\_value(“Stock Entry Type”, self.stock\_entry\_type, “purpose”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry Type”, self.stock\_entry\_type, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6801) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L811)

<a id="op-4bb9bd512a8a5e"></a>
### Stock Entry.make serial and batch bundle for outward

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_make_serial_and_batch_bundle_for_outward`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set serial\_or\_batch\_items from get\_serial\_or\_batch\_items(self.items).
- If not serial\_or\_batch\_items.
  - Return no value.
- Set tuple(serial\_nos, batch\_nos) from self.set\_serial\_batch\_fields\_for\_subcontracting\_inward().
- <a id="op-4bb9bd512a8a5e-guard-8"></a>If self.docstatus equals 0.
  - Return no value.
- Set already\_picked\_serial\_nos from list().
- Set already\_picked\_batches from Platform.\_dict().
- For each row in self.items.
  - If row.use\_serial\_batch\_fields.
    - Continue with the next iteration or loop test.
  - If not row.s\_warehouse.
    - Continue with the next iteration or loop test.
  - If row.item\_code does not belong to serial\_or\_batch\_items.
    - Continue with the next iteration or loop test.
  - Set bundle\_doc from no value.
  - If (row.serial\_and\_batch\_bundle and abs(row.transfer\_qty) differs from abs(Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “total\_qty”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_and\_batch\_bundle → abs(row.transfer\_qty) differs from abs(Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “total\_qty”)).
    - Set bundle\_doc from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.s\_warehouse, “serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle, “type\_of\_transaction” → “Outward”, …)).update\_serial\_and\_bat ….
  - Otherwise.
    - If (not row.serial\_and\_batch\_bundle and Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_and\_batch\_bundle → Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).
      - Set bundle\_doc from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.s\_warehouse, “posting\_datetime” → get\_combine\_datetime(self.posting\_date, self.posting\_time), “voucher\_type” → self.doctype, …)).m ….
  - If not bundle\_doc.
    - Continue with the next iteration or loop test.
  - For each entry in bundle\_doc.entries.
    - If entry.serial\_no.
      - Evaluate already\_picked\_serial\_nos.append(entry.serial\_no).
    - If entry.batch\_no.
      - Set key from tuple(entry.batch\_no, bundle\_doc.warehouse).
      - Set picked from already\_picked\_batches.setdefault(key, Platform.\_dict(batch\_no = entry.batch\_no, warehouse = bundle\_doc.warehouse, qty = 0)).
      - Update picked.qty using + entry.qty.
  - Set row.serial\_and\_batch\_bundle from bundle\_doc.name.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that returns no value. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4bb9bd512a8a5e-guard-8)

**Methods declared on this owner** [set serial batch fields for subcontracting inward](operations-080.md#op-97927cdd0fb989).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “total\_qty”), Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L725)

<a id="op-97927cdd0fb989"></a>
### Stock Entry.set serial batch fields for subcontracting inward

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_serial_batch_fields_for_subcontracting_inward`

**Inputs** self.

**Explicit results** tuple(serial\_nos, batch\_nos).

**Local steps**

- Set tuple(serial\_nos, batch\_nos) from tuple(Platform.\_dict(), Platform.\_dict()).
- For each row in self.items.
  - If self.purpose belongs to list(“Return Raw Material to Customer”, “Subcontracting Delivery”, “Subcontracting Return”).
    - If not row.serial\_and\_batch\_bundle.
      - Set tuple(serial\_nos\_list, batch\_nos\_list) from self.get\_serial\_nos\_and\_batches\_from\_sres(row.scio\_detail, only\_pending = self.purpose differs from “Subcontracting Return”).
      - If len(batch\_nos\_list) &gt; 1.
        - Set row.use\_serial\_batch\_fields from 0.
      - If row.use\_serial\_batch\_fields.
        - If (serial\_nos\_list and not row.serial\_no).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_nos\_list → not row.serial\_no.
          - Set row.serial\_no from whitespace '\\n'.join(serial\_nos\_list).
        - If (batch\_nos\_list and not row.batch\_no).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_nos\_list → not row.batch\_no.
          - Set row.batch\_no from next(iter(batch\_nos\_list.keys())).
      - Set tuple(serial\_nos at row.name, batch\_nos at row.name) from tuple(serial\_nos\_list, batch\_nos\_list).
- Return tuple(serial\_nos, batch\_nos).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L737)

<a id="op-21a515a00d1446"></a>
### Stock Entry.validate subcontract order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_subcontract_order`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · resolve a document from self.subcontract\_data.order\_doctype via get\_doc · read formatted text {self.subcontract\_data.order\_doctype} Item via get\_value · read “Item Alternative” via get\_value · read self.subcontract\_data.order\_supplied\_items\_field via get\_value.

**State and service calls** call db\_set on se\_item · call db\_set on row.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item {0} not found in 'Raw Materials Supplied' table in {1} {2}”.format(se\_item.item\_code, self.subcontract\_data.order\_doctype, self.get(self.subcontract\_data.order\_field)) · validation helper — translated “Row #{0}: Item {1} cannot be transferred more than {2} against {3} {4}”.format(se\_item.idx, se\_item.item\_code, total\_allowed, self.subcontract\_data.order\_doctype, …) · validation helper — translated “Row {0}# Item {1} not found in 'Raw Materials Supplied' table in {2} {3}”.format(se\_item.idx, se\_item.item\_code, self.subcontract\_data.order\_doctype, self.get(self.subcontract\_data.order\_field)) · validation helper — translated “Row {0}: Subcontracted Item is mandatory for the raw material {1}”.format(row.idx, Platform.bold(row.item\_code)).

**Local steps**

- Set backflush\_raw\_materials\_based\_on from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”).
- Set qty\_allowance from flt(Platform.db.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”)).
- If not (self.purpose equals “Send to Subcontractor” and self.get(self.subcontract\_data.order\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Send to Subcontractor” → self.get(self.subcontract\_data.order\_field).
  - Return no value.
- If backflush\_raw\_materials\_based\_on equals “BOM”.
  - Set subcontract\_order from Platform.get\_doc(self.subcontract\_data.order\_doctype, self.get(self.subcontract\_data.order\_field)).
  - Set qty\_in\_entry from defaultdict(float).
  - For each se\_item in self.items.
    - Set item\_code from (se\_item.original\_item or se\_item.item\_code).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in se\_item.original\_item → se\_item.item\_code.
    - Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 3).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 3.
    - Set required\_qty from sum(list of flt(d.required\_qty) for d drawn from subcontract\_order.supplied\_items where d.rm\_item\_code equals item\_code).
      - Draw d from subcontract\_order.supplied\_items, keep a combination only if (d.rm\_item\_code equals item\_code).
    - Set total\_allowed from (required\_qty + (required\_qty × (qty\_allowance ÷ 100))).
    - If not required\_qty.
      - Evaluate Platform.db.get\_value(formatted text {self.subcontract\_data.order\_doctype} Item, mapping(“parent” → self.get(self.subcontract\_data.order\_field), “item\_code” → se\_item.subcontracted\_item), “bom”).
      - If se\_item.allow\_alternative\_item.
        - Set original\_item\_code from Platform.get\_value(“Item Alternative”, mapping(“alternative\_item\_code” → item\_code), “item\_code”).
        - Set required\_qty from sum(list of flt(d.required\_qty) for d drawn from subcontract\_order.supplied\_items where d.rm\_item\_code equals original\_item\_code).
          - Draw d from subcontract\_order.supplied\_items, keep a combination only if (d.rm\_item\_code equals original\_item\_code).
        - Set total\_allowed from (required\_qty + (required\_qty × (qty\_allowance ÷ 100))).
    - If not required\_qty.
      - Call the validation error handler Platform.throw(translated “Item {0} not found in 'Raw Materials Supplied' table in {1} {2}”.format(se\_item.item\_code, self.subcontract\_data.order\_doctype, self.get(self.subcontract\_data.order\_field))).
    - Set se from Platform.qb.DocType(“Stock Entry”).
    - Set se\_detail from Platform.qb.DocType(“Stock Entry Detail”).
    - Set total\_supplied from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract when nested oper … at 0 → 0.
      - Value choice on self.subcontract\_data.order\_doctype equals “Purchase Order” — true gives (se.purchase\_order equals self.purchase\_order bitwise and se\_detail.po\_detail equals se\_item.po\_detail), false gives se.subcontracting\_order equals self.subcontracting\_order.
    - Set total\_returned from 0.
    - If self.subcontract\_data.order\_doctype equals “Subcontracting Order”.
      - Set total\_returned from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0 → 0.
    - Set transferred\_qty from (((total\_supplied + qty\_in\_entry at item\_code) + se\_item.transfer\_qty) − total\_returned).
    - Update qty\_in\_entry at item\_code using + se\_item.transfer\_qty.
    - If flt(transferred\_qty, precision) &gt; flt(total\_allowed, precision).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} cannot be transferred more than {2} against {3} {4}”.format(se\_item.idx, se\_item.item\_code, total\_allowed, self.subcontract\_data.order\_doctype, …)).
    - Otherwise.
      - If not se\_item.get(self.subcontract\_data.rm\_detail\_field).
        - Set filters from mapping(“parent” → self.get(self.subcontract\_data.order\_field), “docstatus” → 1, “rm\_item\_code” → (se\_item.original\_item or se\_item.item\_code), “main\_item\_code” → se\_item.subcontracted\_item).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in se\_item.original\_item → se\_item.item\_code.
        - Set order\_rm\_detail from Platform.db.get\_value(self.subcontract\_data.order\_supplied\_items\_field, filters, “name”).
        - If order\_rm\_detail.
          - Evaluate se\_item.db\_set(self.subcontract\_data.rm\_detail\_field, order\_rm\_detail).
        - Otherwise.
          - If not se\_item.allow\_alternative\_item.
            - Call the validation error handler Platform.throw(translated “Row {0}# Item {1} not found in 'Raw Materials Supplied' table in {2} {3}”.format(se\_item.idx, se\_item.item\_code, self.subcontract\_data.order\_doctype, self.get(self.subcontract\_da ….
- Otherwise.
  - If backflush\_raw\_materials\_based\_on equals “Material Transferred for Subcontract”.
    - For each row in self.items.
      - If not row.subcontracted\_item.
        - Call the validation error handler Platform.throw(translated “Row {0}: Subcontracted Item is mandatory for the raw material {1}”.format(row.idx, Platform.bold(row.item\_code))).
      - Otherwise.
        - If not row.get(self.subcontract\_data.rm\_detail\_field).
          - Set filters from mapping(“parent” → self.get(self.subcontract\_data.order\_field), “docstatus” → 1, “rm\_item\_code” → (row.original\_item or row.item\_code), “main\_item\_code” → row.subcontracted\_item).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.
          - Set order\_rm\_detail from Platform.db.get\_value(self.subcontract\_data.order\_supplied\_items\_field, filters, “name”).
          - If order\_rm\_detail.
            - Evaluate row.db\_set(self.subcontract\_data.rm\_detail\_field, order\_rm\_detail).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”), Platform.db.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L775)

<a id="op-f7c49ee61cbb73"></a>
### Stock Entry.validate bom

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_bill_of_materials`

**Inputs** self.

**Local steps**

- For each d in self.get(“items”).
  - If (d.bom\_no and d.is\_finished\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.bom\_no → d.is\_finished\_item.
    - Set item\_code from (d.original\_item or d.item\_code).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.original\_item → d.item\_code.
    - Evaluate validate\_bom\_no(item\_code, d.bom\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L6919) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L828)

<a id="op-dd2be8a888a876"></a>
### Stock Entry.validate purchase order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_purchase_order`

**Inputs** self.

**Record and data access** read “Purchase Order” via get\_value.

**Explicit failure paths** validation helper — translated “Please select Subcontracting Order instead of Purchase Order {0}”.format(self.purchase\_order).

**Local steps**

- If (self.purpose equals “Send to Subcontractor” and self.get(“purchase\_order”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Send to Subcontractor” → self.get(“purchase\_order”).
  - Set is\_old\_subcontracting\_flow from Platform.db.get\_value(“Purchase Order”, self.purchase\_order, “is\_old\_subcontracting\_flow”).
  - If not is\_old\_subcontracting\_flow.
    - Call the validation error handler Platform.throw(translated “Please select Subcontracting Order instead of Purchase Order {0}”.format(self.purchase\_order)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L766)

<a id="op-50b3a238c3596d"></a>
### Stock Entry.validate closed subcontracting order

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_closed_subcontracting_order`

**Inputs** self.

**Local steps**

- Set order from (self.get(“subcontracting\_order”) or self.get(“subcontracting\_inward\_order”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“subcontracting\_order”) → self.get(“subcontracting\_inward\_order”).
- If order.
  - Evaluate check\_on\_hold\_or\_closed\_status(“Subcontracting Order” when self.get(“subcontracting\_order”), otherwise “Subcontracting Inward Order”, order).
    - Value choice on self.get(“subcontracting\_order”) — true gives “Subcontracting Order”, false gives “Subcontracting Inward Order”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L829)

<a id="op-4651f6d09274e1"></a>
### Stock Entry.validate outputs of manufacture

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_outputs_of_manufacture`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} is received but is neither the finished good nor a secondary item. Set its Secondary Item Type …”.format(d.idx, Platform.bold(d.item\_code)).

**Local steps**

- For each d in self.get(“items”).
  - If (d.t\_warehouse and not d.s\_warehouse and not d.is\_finished\_item and not d.secondary\_item\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.t\_warehouse → not d.s\_warehouse → not d.is\_finished\_item → not d.secondary\_item\_type.
    - Call the validation error handler Platform.throw(translated “Row #{0}: {1} is received but is neither the finished good nor a secondary item. Set its Secondary Item Type …”.format(d.idx, Platform.bold(d.item\_code)), title = translated “Unv ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L765)

<a id="op-86b8be23d2cbe4"></a>
### Stock Entry.mark finished and secondary items

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_mark_finished_and_secondary_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.purpose differs from “Repack” and any(list of d.item\_code for d drawn from self.items where (d.is\_finished\_item and d.t\_warehouse))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose differs from “Repack” → any(list of d.item\_code for d drawn from self.items where (d.is\_finished\_item and d.t\_warehouse)).
  - Draw d from self.items, keep a combination only if ((d.is\_finished\_item and d.t\_warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_finished\_item → d.t\_warehouse.
  - Return no value.
- Set finished\_item from self.get\_finished\_item().
- If (not finished\_item and self.purpose equals “Manufacture”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not finished\_item → self.purpose equals “Manufacture”.
  - Return no value.
- For each d in self.items.
  - If (d.t\_warehouse and not d.s\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.t\_warehouse → not d.s\_warehouse.
    - If (d.secondary\_item\_type or d.valuation\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.secondary\_item\_type → d.valuation\_type.
      - Set d.is\_finished\_item from 0.
    - Otherwise.
      - If (self.purpose equals “Repack” or d.item\_code equals finished\_item).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose equals “Repack” → d.item\_code equals finished\_item.
        - Set d.is\_finished\_item from 1.
  - Otherwise.
    - Set d.is\_finished\_item from 0.
    - Set d.secondary\_item\_type from empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get finished item](operations-080.md#op-64ecc9ce2c478d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L799)

<a id="op-64ecc9ce2c478d"></a>
### Stock Entry.get finished item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_finished_item`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value · read “BOM” via get\_value.

**Explicit results** finished\_item.

**Local steps**

- Set finished\_item from no value.
- If self.work\_order.
  - Set finished\_item from Platform.db.get\_value(“Work Order”, self.work\_order, “production\_item”).
- Otherwise.
  - If self.bom\_no.
    - Set finished\_item from Platform.db.get\_value(“BOM”, self.bom\_no, “item”).
- Return finished\_item.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L586) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L782)

<a id="op-280079619d9cd6"></a>
### Stock Entry.validate finished goods

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_finished_goods`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value · read “Manufacturing Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Finished Item {0} does not match with Work Order {1}”.format(d.item\_code, self.work\_order) · validation helper with FinishedGoodError · validation helper — translated “For quantity {0} should not be greater than allowed quantity {1}”.format(flt(self.fg\_completed\_qty), allowed\_qty).

**Local steps**

- Set tuple(production\_item, wo\_qty, finished\_items) from tuple(no value, 0, list()).
- If self.work\_order.
  - Set wo\_details from Platform.db.get\_value(“Work Order”, self.work\_order, list(“production\_item”, “qty”)).
  - If wo\_details.
    - Set tuple(production\_item, wo\_qty) from wo\_details.
- For each d in self.get(“items”).
  - If d.is\_finished\_item.
    - If not self.work\_order.
      - Evaluate finished\_items.append(d.item\_code).
      - Continue with the next iteration or loop test.
    - If d.item\_code differs from production\_item.
      - Call the validation error handler Platform.throw(translated “Finished Item {0} does not match with Work Order {1}”.format(d.item\_code, self.work\_order)).
    - Evaluate finished\_items.append(d.item\_code).
- If not finished\_items.
  - Call the validation error handler Platform.throw(msg = translated “There must be atleast 1 Finished Good in this Stock Entry”.format(self.name), title = translated “Missing Finished Good”, exc = FinishedGoodError).
- If self.purpose equals “Manufacture”.
  - If len(set(finished\_items)) &gt; 1.
    - Call the validation error handler Platform.throw(msg = translated “Multiple items cannot be marked as finished item”, title = translated “Note”, exc = FinishedGoodError).
  - Set allowance\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
  - Set allowed\_qty from (wo\_qty + ((allowance\_percentage ÷ 100) × wo\_qty)).
  - If (self.work\_order and self.fg\_completed\_qty &gt; allowed\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.fg\_completed\_qty &gt; allowed\_qty.
    - Call the validation error handler Platform.throw(translated “For quantity {0} should not be greater than allowed quantity {1}”.format(flt(self.fg\_completed\_qty), allowed\_qty)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L831)

<a id="op-cf1f94c4fd8008"></a>
### Stock Entry.update stock ledger

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_stock_ledger`

**Inputs** self, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false.

**Explicit results** no value.

**Local steps**

- Set tuple(source\_entries, target\_entries) from tuple(list(), list()).
- Set finished\_item\_row from self.get\_finished\_item\_row().
- Evaluate self.get\_sle\_for\_source\_warehouse(source\_entries, finished\_item\_row).
- Evaluate self.get\_sle\_for\_target\_warehouse(target\_entries, finished\_item\_row).
- If self.docstatus equals 2.
  - Evaluate self.make\_sl\_entries((source\_entries + target\_entries) at slice no value to no value with step negative 1, allow\_negative\_stock = allow\_negative\_stock, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).
  - Return no value.
- Evaluate make\_sl\_entries(source\_entries, allow\_negative\_stock, via\_landed\_cost\_voucher, defer\_dimension\_checks = true).
- If self.recalculate\_for\_bundles\_picked\_while\_posting().
  - Set valuation\_rates from mapping of d.name → flt(d.valuation\_rate) for d drawn from self.items.
    - Draw d from self.items.
  - For each sle in target\_entries.
    - Set sle.incoming\_rate from valuation\_rates at sle.voucher\_detail\_no.
- Evaluate self.make\_sl\_entries(target\_entries, allow\_negative\_stock = allow\_negative\_stock, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).
- Evaluate run\_pending\_dimension\_checks(self.doctype, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get finished item row](operations-081.md#op-cfe2b722db42e5), [get sle for source warehouse](operations-081.md#op-039036129dbfe4), [get sle for target warehouse](operations-081.md#op-d5ff2c9e4e9108), [recalculate for bundles picked while posting](operations-080.md#op-749a94f6bf70a3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L822)

<a id="op-749a94f6bf70a3"></a>
### Stock Entry.recalculate for bundles picked while posting

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_recalculate_for_bundles_picked_while_posting`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Stock Ledger Entry” via exists.

**Explicit results** false · true.

**Local steps**

- If not Platform.db.exists(“Stock Ledger Entry”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “actual\_qty” → tuple(“&lt;”, 0), “auto\_created\_serial\_and\_batch\_bundle” → 1, …)).
  - Return false.
- Evaluate self.reload().
- Evaluate self.calculate\_rate\_and\_amount(reset\_outgoing\_rate = false, raise\_error\_if\_no\_rate = false).
- Evaluate self.db\_update\_all().
- Return true.

**Methods declared on this owner** [calculate rate and amount](operations-079.md#op-e089b5c80e72bd).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L726)
