# Inventory and warehouses · operations 81

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-cfe2b722db42e5"></a>
### Stock Entry.get finished item row

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_finished_item_row`

**Inputs** self.

**Explicit results** finished\_item\_row.

**Local steps**

- Set finished\_item\_row from no value.
- If self.purpose belongs to tuple(“Manufacture”, “Repack”).
  - For each d in self.get(“items”).
    - If d.is\_finished\_item.
      - Set finished\_item\_row from d.
- Return finished\_item\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L1883) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L783)

<a id="op-c02cb6d7394438"></a>
### Stock Entry.validate serial batch bundle type

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_serial_batch_bundle_type`

**Inputs** self, serial\_and\_batch\_bundle.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**Explicit failure paths** validation helper — translated “The Serial and Batch Bundle {0} is not valid for this transaction. The 'Type of Transaction' should be 'Outw …”.format(get\_link\_to\_form(“Serial and Batch Bundle”, serial\_and\_batch\_bundle)).

**Local steps**

- If Platform.db.get\_value(“Serial and Batch Bundle”, serial\_and\_batch\_bundle, “type\_of\_transaction”) differs from “Outward”.
  - Call the validation error handler Platform.throw(translated “The Serial and Batch Bundle {0} is not valid for this transaction. The 'Type of Transaction' should be 'Outw …”.format(get\_link\_to\_form(“Serial and Batch Bundle”, serial\_and\_batc ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L2031) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L837)

<a id="op-039036129dbfe4"></a>
### Stock Entry.get sle for source warehouse

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_stock_ledger_entry_for_source_warehouse`

**Inputs** self, sl\_entries, finished\_item\_row.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Local steps**

- For each d in self.get(“items”).
  - If cstr(d.s\_warehouse).
    - If (d.serial\_and\_batch\_bundle and self.docstatus equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.serial\_and\_batch\_bundle → self.docstatus equals 1.
      - Evaluate self.validate\_serial\_batch\_bundle\_type(d.serial\_and\_batch\_bundle).
    - Set sle from self.get\_sl\_entries(d, mapping(“warehouse” → cstr(d.s\_warehouse), “actual\_qty” → negative flt(d.transfer\_qty), “incoming\_rate” → 0)).
    - If cstr(d.t\_warehouse).
      - Set sle.dependant\_sle\_voucher\_detail\_no from d.name.
    - Otherwise.
      - If (finished\_item\_row and (finished\_item\_row.item\_code differs from d.item\_code or finished\_item\_row.t\_warehouse differs from d.s\_warehouse)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in finished\_item\_row → (finished\_item\_row.item\_code differs from d.item\_code or finished\_item\_row.t\_warehouse differs from d.s\_warehouse).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in finished\_item\_row.item\_code differs from d.item\_code → finished\_item\_row.t\_warehouse differs from d.s\_warehouse.
        - Set sle.dependant\_sle\_voucher\_detail\_no from finished\_item\_row.name.
    - If (sle.serial\_and\_batch\_bundle and self.docstatus equals 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_and\_batch\_bundle → self.docstatus equals 2.
      - Set bundle\_id from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_detail\_no” → d.name, “voucher\_no” → self.name, “is\_cancelled” → 0, “type\_of\_transaction” → “Outward”), “name”).
      - If bundle\_id.
        - Set sle.serial\_and\_batch\_bundle from bundle\_id.
    - Evaluate sl\_entries.append(sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate serial batch bundle type](operations-081.md#op-c02cb6d7394438).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_detail\_no” → d.name, “voucher\_no” → self.name, “is\_cancelled” → 0, “type\_of\_transaction” → “Outward”), “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L2232) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L792)

<a id="op-3319d9953413da"></a>
### Stock Entry.make serial and batch bundle for transfer

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_make_serial_and_batch_bundle_for_transfer`

**Inputs** self.

**Record and data access** read “Stock Entry Detail” via get\_all.

**Explicit results** no value.

**Local steps**

- Set ids from Platform.\_dict(Platform.get\_all(“Stock Entry Detail”, fields = list(“name”, “serial\_and\_batch\_bundle”), filters = mapping(“parent” → self.outgoing\_stock\_entry, “serial\_and\_batch\_bundle” → tuple(“is”, “set” ….
- If not ids.
  - Return no value.
- For each d in self.get(“items”).
  - Set serial\_and\_batch\_bundle from ids.get(d.ste\_detail).
  - If not serial\_and\_batch\_bundle.
    - Continue with the next iteration or loop test.
  - Set d.serial\_and\_batch\_bundle from self.make\_package\_for\_transfer(serial\_and\_batch\_bundle, d.s\_warehouse, “Outward”, do\_not\_submit = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L2888) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L797)

<a id="op-d5ff2c9e4e9108"></a>
### Stock Entry.get sle for target warehouse

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_stock_ledger_entry_for_target_warehouse`

**Inputs** self, sl\_entries, finished\_item\_row.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Local steps**

- For each d in self.get(“items”).
  - If cstr(d.t\_warehouse).
    - Set sle from self.get\_sl\_entries(d, mapping(“warehouse” → cstr(d.t\_warehouse), “actual\_qty” → flt(d.transfer\_qty), “incoming\_rate” → flt(d.valuation\_rate))).
    - If (cstr(d.s\_warehouse) or (finished\_item\_row and d.is\_finished\_item)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(d.s\_warehouse) → (finished\_item\_row and d.is\_finished\_item).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in finished\_item\_row → d.is\_finished\_item.
      - Set sle.recalculate\_rate from 1.
    - Set allowed\_types from list(“Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”).
    - If (self.purpose belongs to allowed\_types and d.serial\_and\_batch\_bundle and self.docstatus equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose belongs to allowed\_types → d.serial\_and\_batch\_bundle → self.docstatus equals 1.
      - Set sle.serial\_and\_batch\_bundle from self.make\_package\_for\_transfer(d.serial\_and\_batch\_bundle, d.t\_warehouse).
    - If (sle.serial\_and\_batch\_bundle and self.docstatus equals 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.serial\_and\_batch\_bundle → self.docstatus equals 2.
      - Set bundle\_id from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_detail\_no” → d.name, “voucher\_no” → self.name, “is\_cancelled” → 0, “type\_of\_transaction” → “Inward”), “name”).
      - If sle.serial\_and\_batch\_bundle differs from bundle\_id.
        - Set sle.serial\_and\_batch\_bundle from bundle\_id.
    - Evaluate sl\_entries.append(sle).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_detail\_no” → d.name, “voucher\_no” → self.name, “is\_cancelled” → 0, “type\_of\_transaction” → “Inward”), “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L793)

<a id="op-86e0a2d5b6f671"></a>
### Stock Entry.get gl entries

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map.

**Explicit results** process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Local steps**

- Set gl\_entries from super().get\_gl\_entries(inventory\_account\_map).
- Set tuple(incoming\_items, basis, divide\_based\_on) from self.get\_additional\_cost\_allocation().
- Set item\_account\_wise\_additional\_cost from mapping().
- For each t in self.get(“additional\_costs”).
  - If not divide\_based\_on.
    - Continue with the next iteration or loop test.
  - For each d in incoming\_items.
    - Evaluate item\_account\_wise\_additional\_cost.setdefault(tuple(d.item\_code, d.name), mapping()).
    - Evaluate item\_account\_wise\_additional\_cost at tuple(d.item\_code, d.name).setdefault(t.expense\_account, mapping(“amount” → 0.0, “base\_amount” → 0.0)).
    - Set multiply\_based\_on from flt(d.get(basis)).
    - Update item\_account\_wise\_additional\_cost at tuple(d.item\_code, d.name) at t.expense\_account at “amount” using + (flt((t.amount × multiply\_based\_on)) ÷ divide\_based\_on).
    - Update item\_account\_wise\_additional\_cost at tuple(d.item\_code, d.name) at t.expense\_account at “base\_amount” using + (flt((t.base\_amount × multiply\_based\_on)) ÷ divide\_based\_on).
- If item\_account\_wise\_additional\_cost.
  - Set precision from self.get\_debit\_field\_precision().
  - For each d in self.get(“items”).
    - For each tuple(account, amount) in item\_account\_wise\_additional\_cost.get(tuple(d.item\_code, d.name), mapping()).items().
      - If not amount.
        - Continue with the next iteration or loop test.
      - Set amount at “amount” from flt(amount at “amount”, precision).
      - Set amount at “base\_amount” from flt(amount at “base\_amount”, precision).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → account, “against” → d.expense\_account, “cost\_center” → d.cost\_center, “remarks” → (self.get(“remarks”) or translated “Accounting Entry for Stock”), … ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → d.expense\_account, “against” → account, “cost\_center” → d.cost\_center, “remarks” → (self.get(“remarks”) or translated “Accounting Entry for Stock”), … ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
- Evaluate self.set\_gl\_entries\_for\_landed\_cost\_voucher(gl\_entries, inventory\_account\_map).
- Return process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Methods declared on this owner** [get additional cost allocation](operations-080.md#op-c68d4b11c35a9a), [set gl entries for landed cost voucher](operations-081.md#op-6e8b24c9565b10).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L784)

<a id="op-6e8b24c9565b10"></a>
### Stock Entry.set gl entries for landed cost voucher

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_gl_entries_for_landed_cost_voucher`

**Inputs** self, gl\_entries, inventory\_account\_map.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_custom\_dimension\_overrides.
- Set landed\_cost\_entries from self.get\_item\_account\_wise\_lcv\_entries().
- If not landed\_cost\_entries.
  - Return no value.
- For each item in self.get(“items”).
  - If item.s\_warehouse.
    - Continue with the next iteration or loop test.
  - For each entry in landed\_cost\_entries.get(tuple(item.item\_code, item.name), list()).
    - If not (entry.amount or entry.base\_amount).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → entry.base\_amount.
      - Continue with the next iteration or loop test.
    - Set account\_currency from get\_account\_currency(entry.expense\_account).
    - Set credit\_amount from flt(entry.base\_amount) when (entry.base\_amount or account\_currency differs from self.company\_currency), otherwise flt(entry.amount).
      - Value choice on (entry.base\_amount or account\_currency differs from self.company\_currency) — true gives flt(entry.base\_amount), false gives flt(entry.amount).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.base\_amount → account\_currency differs from self.company\_currency.
    - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map, “t\_warehouse”).
    - Set gl\_dict from self.get\_gl\_dict(mapping(“account” → entry.expense\_account, “against” → \_inv\_dict at “account”, “cost\_center” → (entry.dimensions.cost\_center or item.cost\_center), “debit” → 0.0, …), item = item).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.cost\_center → item.cost\_center.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.project → item.project.
    - Evaluate gl\_dict.update(get\_custom\_dimension\_overrides(entry)).
    - Evaluate gl\_entries.append(gl\_dict).
    - Set account\_currency from get\_account\_currency(item.expense\_account).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → item.expense\_account, “against” → \_inv\_dict at “account”, “cost\_center” → item.cost\_center, “debit” → 0.0, …), item = item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L731)

<a id="op-a303faad3a1e17"></a>
### Stock Entry.is new entry against closed work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_is_new_entry_against_closed_work_order`

**Inputs** self, pro\_doc.

**Explicit results** (pro\_doc.status equals “Closed” and self.docstatus equals 1 and not self.is\_return and self.purpose belongs to tuple(“Material Transfer for Manufacture”, “Manufacture”)).

**Local steps**

- Return (pro\_doc.status equals “Closed” and self.docstatus equals 1 and not self.is\_return and self.purpose belongs to tuple(“Material Transfer for Manufacture”, “Manufacture”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pro\_doc.status equals “Closed” → self.docstatus equals 1 → not self.is\_return → self.purpose belongs to tuple(“Material Transfer for Manufacture”, “Manufacture”).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L722)

<a id="op-b6b50c85eed3ee"></a>
### Stock Entry.update work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc · resolve a document from “Work Order” via get\_doc.

**Local steps**

- Bind local operation \_validate\_work\_order for subsequent calls.
- If self.job\_card.
  - Set job\_doc from Platform.get\_doc(“Job Card”, self.job\_card).
  - If self.purpose differs from “Manufacture”.
    - Evaluate job\_doc.set\_transferred\_qty(update\_status = true).
    - Evaluate job\_doc.set\_transferred\_qty\_in\_job\_card\_item(self).
  - Otherwise.
    - Evaluate job\_doc.set\_consumed\_qty\_in\_job\_card\_item(self).
    - Evaluate job\_doc.set\_manufactured\_qty().
    - Evaluate job\_doc.update\_work\_order().
- If self.work\_order.
  - Set pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
  - Evaluate \_validate\_work\_order(pro\_doc).
  - If pro\_doc.production\_plan.
    - Evaluate ProductionPlanWorkOrderQuantities(pro\_doc.production\_plan).lock\_plan\_row(pro\_doc).
  - If self.fg\_completed\_qty.
    - If self.docstatus equals 1.
      - Evaluate pro\_doc.add\_additional\_items(self).
    - Otherwise.
      - Evaluate pro\_doc.remove\_additional\_items(self).
    - Evaluate pro\_doc.run\_method(“update\_work\_order\_qty”).
  - Evaluate pro\_doc.run\_method(“update\_status”).
  - If (self.fg\_completed\_qty and self.purpose equals “Manufacture”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.fg\_completed\_qty → self.purpose equals “Manufacture”.
    - Evaluate pro\_doc.run\_method(“update\_planned\_qty”).
  - If not pro\_doc.operations.
    - Evaluate pro\_doc.set\_actual\_dates().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from pro\_doc.run\_method(“update\_work\_order\_qty”), pro\_doc.run\_method(“update\_status”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L749)

<a id="op-a8688e782076da"></a>
### Stock Entry.update work order.validate work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_work_order_validate_work_order`

**Inputs** pro\_doc.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set msg from empty text.
- If flt(pro\_doc.docstatus) differs from 1.
  - Set msg from translated “Work Order {0} must be submitted”.format(self.work\_order).
- If pro\_doc.status equals “Stopped”.
  - Set msg from translated “Transaction not allowed against stopped Work Order {0}”.format(self.work\_order).
- If self.is\_new\_entry\_against\_closed\_work\_order(pro\_doc).
  - Set msg from translated “Transaction not allowed against closed Work Order {0}”.format(self.work\_order).
- If msg.
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L750)

<a id="op-b00253f75a4574"></a>
### Stock Entry.update disassembled order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_update_disassembled_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If not self.work\_order.
  - Return no value.
- If (self.purpose equals “Disassemble” and self.fg\_completed\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Disassemble” → self.fg\_completed\_qty.
  - Set pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
  - Evaluate pro\_doc.run\_method(“update\_disassembled\_qty”, self.fg\_completed\_qty, self.\_action equals “cancel”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from pro\_doc.run\_method(“update\_disassembled\_qty”, self.fg\_completed\_qty, self.\_action equals “cancel”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L745)

<a id="op-f62b7b02dbb6d2"></a>
### Stock Entry.make stock reserve for wip and fg

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_make_stock_reserve_for_work_in_progress_and_finished_goods`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If self.is\_stock\_reserve\_for\_work\_order().
  - Set pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
  - If self.skips\_finished\_good\_reservation(pro\_doc).
    - Return no value.
  - Evaluate pro\_doc.set\_reserved\_qty\_for\_wip\_and\_fg(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is stock reserve for work order](operations-081.md#op-4f51c5e5f59f68), [skips finished good reservation](operations-081.md#op-c536cab3ff2597).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L798)

<a id="op-c536cab3ff2597"></a>
### Stock Entry.skips finished good reservation

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_skips_finished_good_reservation`

**Inputs** self, pro\_doc.

**Declared result** bool.

**Explicit results** (self.purpose equals “Manufacture” and not (pro\_doc.sales\_order or self.job\_card or pro\_doc.production\_plan\_sub\_assembly\_item or pro\_doc.subcontracting\_inward\_order)).

**Local steps**

- Return (self.purpose equals “Manufacture” and not (pro\_doc.sales\_order or self.job\_card or pro\_doc.production\_plan\_sub\_assembly\_item or pro\_doc.subcontracting\_inward\_order)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Manufacture” → not (pro\_doc.sales\_order or self.job\_card or pro\_doc.production\_plan\_sub\_assembly\_item or pro\_doc.subcontracting\_inward\_order).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pro\_doc.sales\_order → self.job\_card → pro\_doc.production\_plan\_sub\_assembly\_item → pro\_doc.subcontracting\_inward\_order.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L742)

<a id="op-744bf7594bc4cb"></a>
### Stock Entry.reserve stock for subcontracting

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_reserve_stock_for_subcontracting`

**Inputs** self.

**Record and data access** read “Subcontracting Order” via get\_value · resolve a document from “Subcontracting Order” via get\_doc.

**Local steps**

- If (self.purpose equals “Send to Subcontractor” and Platform.get\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Send to Subcontractor” → Platform.get\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”).
  - Set items from mapping().
  - For each item in self.items.
    - If item.sco\_rm\_detail belongs to items.
      - Update items at item.sco\_rm\_detail.qty\_to\_reserve using + item.transfer\_qty.
      - Evaluate items at item.sco\_rm\_detail.serial\_and\_batch\_bundles.append(item.serial\_and\_batch\_bundle).
    - Otherwise.
      - Set items at item.sco\_rm\_detail from Platform.\_dict(mapping(“name” → item.sco\_rm\_detail, “qty\_to\_reserve” → item.transfer\_qty, “warehouse” → item.t\_warehouse, “reference\_voucher\_detail\_no” → item.name, …)).
  - Evaluate Platform.get\_doc(“Subcontracting Order”, self.subcontracting\_order).make\_raw\_material\_reservations(items = items.values(), stock\_entry = self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L804)

<a id="op-bde470c37ad234"></a>
### Stock Entry.cancel stock reservation entries for subcontracting

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_cancel_stock_reservation_entries_for_subcontracting`

**Inputs** self.

**Local steps**

- Bind dependencies cancel\_stock\_reservation\_entries.
- If self.purpose equals “Send to Subcontractor”.
  - Evaluate cancel\_stock\_reservation\_entries(from\_voucher\_type = “Stock Entry”, from\_voucher\_no = self.name, notify = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L679)

<a id="op-a67eef73f5a242"></a>
### Stock Entry.cancel stock reserve for wip and fg

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_cancel_stock_reserve_for_work_in_progress_and_finished_goods`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If self.is\_stock\_reserve\_for\_work\_order().
  - Set pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
  - If self.skips\_finished\_good\_reservation(pro\_doc).
    - Return no value.
  - Evaluate pro\_doc.cancel\_reserved\_qty\_for\_wip\_and\_fg(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is stock reserve for work order](operations-081.md#op-4f51c5e5f59f68), [skips finished good reservation](operations-081.md#op-c536cab3ff2597).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L770)

<a id="op-4f51c5e5f59f68"></a>
### Stock Entry.is stock reserve for work order

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_is_stock_reserve_for_work_order`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value.

**Explicit results** true · false.

**Local steps**

- If (self.work\_order and self.purpose belongs to list(“Material Transfer for Manufacture”, “Manufacture”) and Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose belongs to list(“Material Transfer for Manufacture”, “Manufacture”) → Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”).
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L5056) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L796)

<a id="op-bf621bc9718386"></a>
### Stock Entry.before sl preview

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_before_sl_preview`

**Inputs** self.

**Local steps**

- Evaluate self.release\_work\_order\_reservation\_for\_preview().

If control reaches the end, it returns no value.

**Methods declared on this owner** [release work order reservation for preview](operations-081.md#op-37efd4dd37dd8a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L678)

<a id="op-083a3093e3c27e"></a>
### Stock Entry.before gl preview

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_before_gl_preview`

**Inputs** self.

**Local steps**

- Evaluate self.release\_work\_order\_reservation\_for\_preview().

If control reaches the end, it returns no value.

**Methods declared on this owner** [release work order reservation for preview](operations-081.md#op-37efd4dd37dd8a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L677)

<a id="op-37efd4dd37dd8a"></a>
### Stock Entry.release work order reservation for preview

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_release_work_order_reservation_for_preview`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If not self.is\_stock\_reserve\_for\_work\_order().
  - Return no value.
- Evaluate self.db\_set(“docstatus”, 1, update\_modified = false).
- Evaluate Platform.get\_doc(“Work Order”, self.work\_order).update\_required\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is stock reserve for work order](operations-081.md#op-4f51c5e5f59f68).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L727)

<a id="op-5a14353401b89f"></a>
### Stock Entry.update wo reservation for subcontracting

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_work_order_reservation_for_subcontracting`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- <a id="op-5a14353401b89f-guard-6"></a>If self.purpose differs from “Send to Subcontractor”.
  - Return no value.
- For each wo\_name in self.get\_reserved\_work\_orders\_for\_subcontracting().
  - Evaluate Platform.get\_doc(“Work Order”, wo\_name).release\_reserved\_qty\_for\_subcontract\_transfer().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose differs from “Send to Subcontractor”, self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Send to Subcontractor”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5a14353401b89f-guard-6)

**Methods declared on this owner** [get reserved work orders for subcontracting](operations-081.md#op-cb263678294959).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L825)

<a id="op-cb263678294959"></a>
### Stock Entry.get reserved work orders for subcontracting

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_reserved_work_orders_for_subcontracting`

**Inputs** self.

**Record and data access** read “Subcontracting Order Item” via get\_all · read “Purchase Order Item” via get\_all · read “Job Card” via get\_all · read “Work Order” via get\_cached\_value.

**Explicit results** list() · reserved\_work\_orders.

**Local steps**

- Set job\_cards from set().
- If self.subcontracting\_order.
  - Evaluate job\_cards.update(Platform.get\_all(“Subcontracting Order Item”, filters = mapping(“parent” → self.subcontracting\_order), pluck = “job\_card”)).
- If self.purchase\_order.
  - Evaluate job\_cards.update(Platform.get\_all(“Purchase Order Item”, filters = mapping(“parent” → self.purchase\_order), pluck = “job\_card”)).
- Set job\_cards from set of jc for jc drawn from job\_cards where jc.
  - Draw jc from job\_cards, keep a combination only if (jc).
- If not job\_cards.
  - Return list().
- Set work\_orders from Platform.get\_all(“Job Card”, filters = mapping(“name” → list(“in”, list(job\_cards))), pluck = “work\_order”).
- Set reserved\_work\_orders from list().
- For each work\_order in set(work\_orders).
  - If not work\_order.
    - Continue with the next iteration or loop test.
  - If Platform.get\_cached\_value(“Work Order”, work\_order, “reserve\_stock”).
    - Evaluate reserved\_work\_orders.append(work\_order).
- Return reserved\_work\_orders.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, work\_order, “reserve\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0837.json#L5362) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L788)

<a id="op-ed2ef52ca500d9"></a>
### Stock Entry.get item details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_item_details`

**Inputs** self, args = no value, for\_update = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Work Order” via get\_value · read “Company” via get\_cached\_value · read self.subcontract\_data.order\_supplied\_items\_field via get\_all.

**Explicit results** ret.

**Explicit failure paths** validation helper — translated “Item {0} is not active or end of life has been reached”.format(args.get(“item\_code”)).

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set item\_default from Platform.qb.DocType(“Item Default”).
- Set query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
- Set item from query.run(as\_dict = true).
- If not item.
  - Call the validation error handler Platform.throw(translated “Item {0} is not active or end of life has been reached”.format(args.get(“item\_code”))).
- Set item from item at 0.
- Set item\_group\_defaults from get\_item\_group\_defaults(item.name, self.company).
- Set brand\_defaults from get\_brand\_defaults(item.name, self.company).
- Set ret from Platform.\_dict(mapping(“uom” → item.stock\_uom, “stock\_uom” → item.stock\_uom, “description” → item.description, “image” → item.image, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → item\_group\_defaults.get(“expense\_account”).
- If self.purpose equals “Send to Subcontractor”.
  - Set ret at “allow\_alternative\_item” from item.allow\_alternative\_item.
- Otherwise.
  - If (self.work\_order and self.purpose belongs to WORK\_ORDER\_ALTERNATIVE\_ITEM\_PURPOSES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose belongs to WORK\_ORDER\_ALTERNATIVE\_ITEM\_PURPOSES.
    - Set ret at “allow\_alternative\_item” from cint((item.allow\_alternative\_item and Platform.db.get\_value(“Work Order”, self.work\_order, “allow\_alternative\_item”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.allow\_alternative\_item → Platform.db.get\_value(“Work Order”, self.work\_order, “allow\_alternative\_item”).
- If (args.get(“uom”) and for\_update).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“uom”) → for\_update.
  - Evaluate ret.update(get\_uom\_details(args.get(“item\_code”), args.get(“uom”), args.get(“qty”))).
- If self.purpose equals “Material Issue”.
  - Set ret at “expense\_account” from (item.get(“expense\_account”) or item\_group\_defaults.get(“expense\_account”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“expense\_account”) → item\_group\_defaults.get(“expense\_account”).
- If not ret.get(“expense\_account”).
  - Set ret at “expense\_account” from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”).
- For each tuple(company\_field, field) in mapping(“stock\_adjustment\_account” → “expense\_account”, “cost\_center” → “cost\_center”).items().
  - If not ret.get(field).
    - Set ret at field from Platform.get\_cached\_value(“Company”, self.company, company\_field).
- Set args at “posting\_date” from self.posting\_date.
- Set args at “posting\_time” from self.posting\_time.
- Set stock\_and\_rate from get\_warehouse\_details(args) when args.get(“warehouse”), otherwise mapping().
  - Value choice on args.get(“warehouse”) — true gives get\_warehouse\_details(args), false gives mapping().
- Evaluate ret.update(stock\_and\_rate).
- If (self.purpose equals “Send to Subcontractor” and self.get(self.subcontract\_data.order\_field) and args.get(“item\_code”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Send to Subcontractor” → self.get(self.subcontract\_data.order\_field) → args.get(“item\_code”).
  - Set subcontract\_items from Platform.get\_all(self.subcontract\_data.order\_supplied\_items\_field, mapping(“parent” → self.get(self.subcontract\_data.order\_field), “rm\_item\_code” → args.get(“item\_code”)), “main\_item\_code”).
  - If (subcontract\_items and len(subcontract\_items) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in subcontract\_items → len(subcontract\_items) equals 1.
    - Set ret at “subcontracted\_item” from subcontract\_items at 0.main\_item\_code.
- Set barcode\_data from get\_barcode\_data(item\_code = item.name).
- If (barcode\_data and len(barcode\_data.get(item.name)) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in barcode\_data → len(barcode\_data.get(item.name)) equals 1.
  - Set ret at “barcode” from barcode\_data.get(item.name) at 0.
- Return ret.

**Values supplied outside this operation** clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”), Platform.get\_cached\_value(“Company”, self.company, company\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L785)

<a id="op-a8eaa838aa7b9f"></a>
### Stock Entry.set items for stock in

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_items_for_stock_in`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Stock Entry” via get\_doc.

**Explicit failure paths** validation helper — translated “Goods are already received against the outward entry {0}”.format(doc.name).

**Local steps**

- Set self.items from list().
- If (self.outgoing\_stock\_entry and self.purpose equals “Material Transfer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.outgoing\_stock\_entry → self.purpose equals “Material Transfer”.
  - Evaluate Enterprise.require\_permission(“Stock Entry”, self.outgoing\_stock\_entry).
  - Set doc from Platform.get\_doc(“Stock Entry”, self.outgoing\_stock\_entry).
  - If doc.per\_transferred equals 100.
    - Call the validation error handler Platform.throw(translated “Goods are already received against the outward entry {0}”.format(doc.name)).
  - For each d in doc.items.
    - Evaluate self.append(“items”, mapping(“s\_warehouse” → d.t\_warehouse, “item\_code” → d.item\_code, “qty” → d.qty, “uom” → d.uom, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L808)
