# Inventory and warehouses · operations 82

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-1a6f3ec0d74523"></a>
### Stock Entry.get items for disassembly

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_items_for_disassembly`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_all.

**Explicit results** self.\_add\_items\_for\_disassembly\_from\_stock\_entry() · self.\_add\_items\_for\_disassembly\_from\_work\_order() · self.\_add\_items\_for\_disassembly\_from\_bom().

**Local steps**

- If (not self.get(“source\_stock\_entry”) and self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“source\_stock\_entry”) → self.work\_order.
  - Set manufacture\_entries from Platform.get\_all(“Stock Entry”, filters = mapping(“work\_order” → self.work\_order, “purpose” → “Manufacture”, “docstatus” → 1), pluck = “name”).
  - For each name in manufacture\_entries.
    - Evaluate Enterprise.require\_permission(“Stock Entry”, name).
  - If len(manufacture\_entries) equals 1.
    - Set self.source\_stock\_entry from manufacture\_entries at 0.
- If self.get(“source\_stock\_entry”).
  - Return self.\_add\_items\_for\_disassembly\_from\_stock\_entry().
- If self.work\_order.
  - Return self.\_add\_items\_for\_disassembly\_from\_work\_order().
- Return self.\_add\_items\_for\_disassembly\_from\_bom().

**Methods declared on this owner** [add items for disassembly from stock entry](operations-082.md#op-3ae0abbe06972f), [add items for disassembly from work order](operations-082.md#op-7fbb17861c3f0c), [add items for disassembly from bom](operations-082.md#op-682c4828aeb4d7).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L699)

<a id="op-3ae0abbe06972f"></a>
### Stock Entry.add items for disassembly from stock entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_items_for_disassembly_from_stock_entry`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Source Stock Entry {0} has no finished goods quantity”.format(self.source\_stock\_entry).

**Local steps**

- Set source\_fg\_qty from self.get\_source\_fg\_qty().
- If not source\_fg\_qty.
  - Call the validation error handler Platform.throw(translated “Source Stock Entry {0} has no finished goods quantity”.format(self.source\_stock\_entry)).
- Evaluate self.\_append\_disassembly\_row\_from\_source(source\_fg\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get source fg qty](operations-078.md#op-d969a5020c4c38), [append disassembly row from source](operations-082.md#op-4e866432a282c8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L670)

<a id="op-7fbb17861c3f0c"></a>
### Stock Entry.add items for disassembly from work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_items_for_disassembly_from_work_order`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Work Order {0} has no produced qty”.format(self.work\_order) · validation helper — translated “Disassemble Qty cannot be less than or equal to 0.”.

**Local steps**

- Set wo\_produced\_qty from self.get\_source\_fg\_qty().
- <a id="op-7fbb17861c3f0c-guard-3"></a>If wo\_produced\_qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Work Order {0} has no produced qty”.format(self.work\_order)).
- If flt(self.fg\_completed\_qty) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Disassemble Qty cannot be less than or equal to 0.”).
- Evaluate self.\_append\_disassembly\_row\_from\_source(wo\_produced\_qty).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison wo\_produced\_qty ≤ 0, wo\_produced\_qty = 0 selects the branch that calls the validation-error handler with translated “Work Order {0} has no produced qty”.format(self.work\_order). With wo\_produced\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7fbb17861c3f0c-guard-3)

**Methods declared on this owner** [get source fg qty](operations-078.md#op-d969a5020c4c38), [append disassembly row from source](operations-082.md#op-4e866432a282c8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L671)

<a id="op-4e866432a282c8"></a>
### Stock Entry.append disassembly row from source

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_append_disassembly_row_from_source`

**Inputs** self, source\_fg\_qty.

**Local steps**

- Set progress from self.get\_disassembly\_progress(source\_fg\_qty).
- For each source\_row in self.get\_items\_from\_manufacture\_stock\_entry().
  - If source\_row.is\_finished\_item.
    - Set qty from flt(self.fg\_completed\_qty).
    - Set s\_warehouse from (self.from\_warehouse or source\_row.t\_warehouse).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.from\_warehouse → source\_row.t\_warehouse.
    - Set t\_warehouse from empty text.
  - Otherwise.
    - Set qty from flt((self.get\_component\_stock\_qty(source\_row, progress) ÷ source\_row.conversion\_factor), Platform.get\_precision(“Stock Entry Detail”, “qty”)).
    - If source\_row.s\_warehouse.
      - Set s\_warehouse from empty text.
      - Set t\_warehouse from (self.to\_warehouse or source\_row.s\_warehouse).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.to\_warehouse → source\_row.s\_warehouse.
    - Otherwise.
      - Set s\_warehouse from source\_row.t\_warehouse.
      - Set t\_warehouse from empty text.
  - If not qty.
    - Continue with the next iteration or loop test.
  - Set item from mapping(“item\_code” → source\_row.item\_code, “item\_name” → source\_row.item\_name, “description” → source\_row.description, “stock\_uom” → source\_row.stock\_uom, …).
    - Value choice on (source\_row.batch\_no or source\_row.serial\_no) — true gives 1, false gives 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_row.batch\_no → source\_row.serial\_no.
  - If self.source\_stock\_entry.
    - Evaluate item.update(mapping(“against\_stock\_entry” → self.source\_stock\_entry, “ste\_detail” → source\_row.name)).
  - Evaluate self.append(“items”, item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get disassembly progress](operations-078.md#op-883a013a5f800b), [get items from manufacture stock entry](operations-082.md#op-28a561352164af), [get component stock qty](operations-078.md#op-9eca59f956ffcd).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L675)

<a id="op-682c4828aeb4d7"></a>
### Stock Entry.add items for disassembly from bom

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_items_for_disassembly_from_bom`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value.

**Explicit failure paths** validation helper — translated “BOM and Finished Good Quantity is mandatory for Disassembly”.

**Local steps**

- If (not self.bom\_no or not self.fg\_completed\_qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.bom\_no → not self.fg\_completed\_qty.
  - Call the validation error handler Platform.throw(translated “BOM and Finished Good Quantity is mandatory for Disassembly”).
- Set item\_dict from self.get\_bom\_raw\_materials(self.fg\_completed\_qty).
- For each item\_row in item\_dict.values().
  - Set item\_row at “to\_warehouse” from self.to\_warehouse.
  - Set item\_row at “from\_warehouse” from empty text.
  - Set item\_row at “is\_finished\_item” from 0.
- Evaluate self.add\_to\_stock\_entry\_detail(item\_dict).
- Set secondary\_items from self.get\_secondary\_items(self.fg\_completed\_qty).
- If secondary\_items.
  - Set scrap\_warehouse from self.from\_warehouse.
  - If self.work\_order.
    - Set wo\_values from Platform.db.get\_value(“Work Order”, self.work\_order, list(“scrap\_warehouse”, “fg\_warehouse”), as\_dict = true).
    - Set scrap\_warehouse from (wo\_values.scrap\_warehouse or scrap\_warehouse or wo\_values.fg\_warehouse).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in wo\_values.scrap\_warehouse → scrap\_warehouse → wo\_values.fg\_warehouse.
  - For each item in secondary\_items.values().
    - Set item at “from\_warehouse” from scrap\_warehouse.
    - Set item at “to\_warehouse” from empty text.
    - Set item at “is\_finished\_item” from 0.
    - If item.get(“process\_loss\_per”).
      - Update item at “qty” using − flt((item at “qty” × (item at “process\_loss\_per” ÷ 100)), self.precision(“fg\_completed\_qty”)).
  - Evaluate self.add\_to\_stock\_entry\_detail(secondary\_items, bom\_no = self.bom\_no).
- Evaluate self.load\_items\_from\_bom().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bom raw materials](operations-082.md#op-429d929193c3f8), [add to stock entry detail](operations-083.md#op-e7c2657477c713), [get secondary items](operations-083.md#op-71a15391fcc3c0), [load items from bom](operations-082.md#op-48072fc4cafd54).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L669)

<a id="op-28a561352164af"></a>
### Stock Entry.get items from manufacture stock entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_items_from_manufacture_stock_entry`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.name e … · nested operand in the contract(nested operand in the contract).groupby(SED.item\_code).orderby(SED.idx).run(as\_dict = true).

**Local steps**

- Set SE from Platform.qb.DocType(“Stock Entry”).
- Set SED from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).join(SE).on(SED.parent equals SE.name).where(SE.docstatus equals 1).
- Set common\_fields from list(SED.item\_code, SED.item\_name, SED.description, SED.stock\_uom, …).
- If self.source\_stock\_entry.
  - Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.name e ….
- Return nested operand in the contract(nested operand in the contract).groupby(SED.item\_code).orderby(SED.idx).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L700)

<a id="op-0084cbc8b530f8"></a>
### Stock Entry.get items

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_items`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Manufacturing Settings” via get\_single\_value · resolve a document from “Work Order” via get\_doc.

**Explicit results** no value · self.get\_items\_for\_disassembly().

**Explicit failure paths** validation helper — translated “Posting date and posting time is mandatory” · validation helper — translated “Manufacturing Quantity is mandatory”.

**Local steps**

- If self.pick\_list.
  - Return no value.
- Evaluate self.check\_source\_documents\_permission().
- Evaluate self.set(“items”, list()).
- Evaluate self.validate\_work\_order().
- If self.purpose equals “Disassemble”.
  - Return self.get\_items\_for\_disassembly().
- If (not self.posting\_date or not self.posting\_time).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.posting\_date → not self.posting\_time.
  - Call the validation error handler Platform.throw(translated “Posting date and posting time is mandatory”).
- Evaluate self.set\_work\_order\_details().
- If self.bom\_no.
  - Evaluate Enterprise.require\_permission(“BOM”, self.bom\_no).
- Set backflush\_based\_on from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”).
- If self.bom\_no.
  - Set backflush\_based\_on from self.get\_backflush\_based\_on().
  - If self.purpose belongs to list(“Material Issue”, “Material Transfer”, “Manufacture”, “Repack”, …).
    - If (self.work\_order and self.purpose equals “Material Transfer for Manufacture”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose equals “Material Transfer for Manufacture”.
      - Set item\_dict from self.get\_pending\_raw\_materials(backflush\_based\_on).
      - If (self.to\_warehouse and self.pro\_doc).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_warehouse → self.pro\_doc.
        - For each item in item\_dict.values().
          - Set item at “to\_warehouse” from self.pro\_doc.wip\_warehouse.
      - Evaluate self.add\_to\_stock\_entry\_detail(item\_dict).
    - Otherwise.
      - If (self.purpose equals “Manufacture” and self.is\_rm\_cost\_from\_consumption\_entries()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Manufacture” → self.is\_rm\_cost\_from\_consumption\_entries().
        - Take no action here.
      - Otherwise.
        - If (self.work\_order and (self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) and not self.pro\_doc.skip\_transfer and backflush\_based\_on equals “Material Transferred ….
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → (self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) → not self.pro\_doc.skip\_transfer → backflush\_based\_on equals “Material Transferred for Manufacture”.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose equals “Manufacture” → self.purpose equals “Material Consumption for Manufacture”.
          - Evaluate self.add\_transfered\_raw\_materials\_in\_items().
        - Otherwise.
          - If (self.work\_order and (self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) and backflush\_based\_on equals “BOM” and Platform.db.get\_single\_value(“Manufacturing Se ….
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → (self.purpose equals “Manufacture” or self.purpose equals “Material Consumption for Manufacture”) → backflush\_based\_on equals “BOM” → Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”) equals 1.
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose equals “Manufacture” → self.purpose equals “Material Consumption for Manufacture”.
            - Evaluate self.get\_unconsumed\_raw\_materials().
          - Otherwise.
            - If not self.fg\_completed\_qty.
              - Call the validation error handler Platform.throw(translated “Manufacturing Quantity is mandatory”).
            - Set item\_dict from self.get\_bom\_raw\_materials(self.fg\_completed\_qty).
            - If (self.get(self.subcontract\_data.order\_field) and self.purpose equals “Send to Subcontractor”).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(self.subcontract\_data.order\_field) → self.purpose equals “Send to Subcontractor”.
              - Set parent from Platform.qb.DocType(self.subcontract\_data.order\_doctype).
              - Set child from Platform.qb.DocType(self.subcontract\_data.order\_supplied\_items\_field).
              - Set item\_wh from nested operand in the contract(nested operand in the contract).select(child.rm\_item\_code, child.reserve\_warehouse).where(parent.name equals self.get(nested operand in the contract.subcontract\_data.order\_fi ….
              - Set item\_wh from Platform.\_dict(item\_wh).
            - For each tuple(original\_item, item) in item\_dict.items().
              - If (self.pro\_doc and cint(self.pro\_doc.from\_wip\_warehouse)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pro\_doc → cint(self.pro\_doc.from\_wip\_warehouse).
                - Set item at “from\_warehouse” from self.pro\_doc.wip\_warehouse.
              - If (self.get(self.subcontract\_data.order\_field) and self.purpose equals “Send to Subcontractor”).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(self.subcontract\_data.order\_field) → self.purpose equals “Send to Subcontractor”.
                - Set item at “from\_warehouse” from item\_wh.get(item.item\_code).
              - Set item at “to\_warehouse” from self.to\_warehouse when self.purpose equals “Send to Subcontractor”, otherwise empty text.
                - Value choice on self.purpose equals “Send to Subcontractor” — true gives self.to\_warehouse, false gives empty text.
              - If (isinstance(original\_item, str) and original\_item differs from item.get(“item\_code”)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(original\_item, str) → original\_item differs from item.get(“item\_code”).
                - Set item at “original\_item” from original\_item.
            - Evaluate self.add\_to\_stock\_entry\_detail(item\_dict).
  - If (self.work\_order and self.purpose equals “Manufacture”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose equals “Manufacture”.
    - Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order).
    - Evaluate add\_additional\_cost(self, work\_order).
  - If self.purpose belongs to tuple(“Manufacture”, “Repack”).
    - Evaluate self.set\_process\_loss\_qty().
    - Evaluate self.load\_items\_from\_bom().
- Evaluate self.set\_serial\_batch\_from\_reserved\_entry().
- Evaluate self.set\_secondary\_items().
- Evaluate self.set\_actual\_qty().
- Evaluate self.validate\_customer\_provided\_item().
- Evaluate self.calculate\_rate\_and\_amount(raise\_error\_if\_no\_rate = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check source documents permission](operations-082.md#op-ebf7496fe05123), [validate work order](operations-078.md#op-5feb3ad798888d), [get items for disassembly](operations-082.md#op-1a6f3ec0d74523), [set work order details](operations-082.md#op-759b32c5cade62), [get backflush based on](operations-082.md#op-10944d97a583f0), [get pending raw materials](operations-083.md#op-6f64d56fedd7d5), [add to stock entry detail](operations-083.md#op-e7c2657477c713), [is rm cost from consumption entries](operations-079.md#op-fccb636dfc2be8), [add transfered raw materials in items](operations-083.md#op-29a61e18a684e5), [get unconsumed raw materials](operations-083.md#op-987595ea7d3553), [get bom raw materials](operations-082.md#op-429d929193c3f8), [set process loss qty](operations-082.md#op-e5cca1a9928da5), [load items from bom](operations-082.md#op-48072fc4cafd54), [set serial batch from reserved entry](operations-082.md#op-84e458d91ceac5), [set secondary items](operations-082.md#op-42a9ace81552df), [set actual qty](operations-079.md#op-eef6d1415cea78), [calculate rate and amount](operations-079.md#op-e089b5c80e72bd).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”), Platform.db.get\_single\_value(“Manufacturing Settings”, “material\_consumption”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L786)

<a id="op-84e458d91ceac5"></a>
### Stock Entry.set serial batch from reserved entry

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_serial_batch_from_reserved_entry`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value.

**State and service calls** request copy\_doc for d.

**Explicit results** no value.

**Local steps**

- If (self.work\_order and Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”).
  - Set skip\_transfer from Platform.get\_cached\_value(“Work Order”, self.work\_order, “skip\_transfer”).
  - If (self.purpose does not belong to list(“Material Transfer for Manufacture”) and self.get\_backflush\_based\_on() differs from “BOM” and not skip\_transfer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose does not belong to list(“Material Transfer for Manufacture”) → self.get\_backflush\_based\_on() differs from “BOM” → not skip\_transfer.
    - Return no value.
- Set reservation\_entries from self.get\_available\_reserved\_materials().
- If not reservation\_entries.
  - Return no value.
- Set new\_items\_to\_add from list().
- For each d in self.items.
  - If (d.serial\_and\_batch\_bundle or d.serial\_no or d.batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.serial\_and\_batch\_bundle → d.serial\_no → d.batch\_no.
    - Continue with the next iteration or loop test.
  - Set key from tuple(d.item\_code, d.s\_warehouse).
  - If details bound to reservation\_entries.get(key).
    - Set original\_qty from d.qty.
    - If batches bound to details.get(“batch\_no”).
      - For each tuple(batch\_no, qty) in batches.items().
        - <a id="op-84e458d91ceac5-guard-26"></a>If original\_qty ≤ 0.
          - Leave the innermost loop without its normal-exhaustion alternative.
        - <a id="op-84e458d91ceac5-guard-29"></a>If qty ≤ 0.
          - Continue with the next iteration or loop test.
        - Set qty from min(qty, original\_qty).
        - If d.batch\_no.
          - Set new\_row from Platform.copy\_doc(d).
          - Set new\_row.name from no value.
          - Evaluate self.assign\_reserved\_batch(new\_row, batches, details, batch\_no, …).
          - Evaluate new\_items\_to\_add.append(new\_row).
        - Otherwise.
          - Evaluate self.assign\_reserved\_batch(d, batches, details, batch\_no, …).
        - Update original\_qty using − qty.
      - If (original\_qty &gt; 0 and d.batch\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in original\_qty &gt; 0 → d.batch\_no.
        - Set new\_row from Platform.copy\_doc(d).
        - Evaluate new\_row.update(mapping(“name” → no value, “batch\_no” → no value, “serial\_no” → no value, “qty” → original\_qty)).
        - Evaluate new\_items\_to\_add.append(new\_row).
    - If details.get(“serial\_no”).
      - Set d.serial\_no from whitespace '\\n'.join(details.get(“serial\_no”) at slice no value to cint(d.qty)).
    - Set d.use\_serial\_batch\_fields from 1.
- For each new\_row in new\_items\_to\_add.
  - Evaluate self.append(“items”, new\_row).
- Set sorted\_items from sorted(self.items, key = deferred anonymous expression).
- If self.purpose equals “Manufacture”.
  - Set sorted\_items from sorted(sorted\_items, key = deferred anonymous expression).
- Set idx from 0.
- For each row in sorted\_items.
  - Update idx using + 1.
  - Set row.idx from idx.
- Evaluate self.set(“items”, sorted\_items).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison original\_qty ≤ 0, original\_qty = 0 selects the branch that exits the enclosing loop. With original\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-84e458d91ceac5-guard-26)
- At the comparison qty ≤ 0, qty = 0 selects the branch that continues with the next loop iteration. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-84e458d91ceac5-guard-29)

**Methods declared on this owner** [get backflush based on](operations-082.md#op-10944d97a583f0), [get available reserved materials](operations-082.md#op-c1f923155e054e), [assign reserved batch](operations-082.md#op-3ab0ce106a22ae).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “reserve\_stock”), Platform.get\_cached\_value(“Work Order”, self.work\_order, “skip\_transfer”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L813)

<a id="op-3ab0ce106a22ae"></a>
### Stock Entry.assign reserved batch

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_assign_reserved_batch`

**Inputs** row, batches, details, batch\_no, qty.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Set row.batch\_no from batch\_no.
- Set row.qty from qty.
- Update batches at batch\_no using − qty.
- If details.get(“batchwise\_sn”).
  - Set row.serial\_no from whitespace '\\n'.join(details.get(“batchwise\_sn”) at batch\_no at slice no value to cint(qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L676)

<a id="op-10944d97a583f0"></a>
### Stock Entry.get backflush based on

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_backflush_based_on`

**Inputs** self.

**Explicit results** get\_backflush\_based\_on(self.bom\_no).

**Local steps**

- Bind dependencies get\_backflush\_based\_on.
- Return get\_backflush\_based\_on(self.bom\_no).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L688)

<a id="op-c1f923155e054e"></a>
### Stock Entry.get available reserved materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_available_reserved_materials`

**Inputs** self.

**Explicit results** mapping() · itemwise\_serial\_batch\_qty.

**Local steps**

- Set reserved\_entries from self.get\_reserved\_materials().
- If not reserved\_entries.
  - Return mapping().
- Set itemwise\_serial\_batch\_qty from Platform.\_dict().
- For each d in reserved\_entries.
  - Set key from tuple(d.item\_code, d.warehouse).
  - If key does not belong to itemwise\_serial\_batch\_qty.
    - Set itemwise\_serial\_batch\_qty at key from Platform.\_dict(mapping(“serial\_no” → list(), “batch\_no” → defaultdict(float), “batchwise\_sn” → defaultdict(list))).
  - Set details from itemwise\_serial\_batch\_qty at key.
  - If d.batch\_no.
    - Update details.batch\_no at d.batch\_no using + d.qty.
    - If d.serial\_no.
      - Evaluate details.batchwise\_sn at d.batch\_no.extend(d.serial\_no.split(whitespace '\\n')).
  - Otherwise.
    - If d.serial\_no.
      - Evaluate details.serial\_no.append(d.serial\_no).
- Return itemwise\_serial\_batch\_qty.

**Methods declared on this owner** [get reserved materials](operations-082.md#op-1be3eb54792909).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L686)

<a id="op-1be3eb54792909"></a>
### Stock Entry.get reserved materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_reserved_materials`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Stock Reservation Entry”).
- Set serial\_batch\_doc from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(serial\_batch\_doc.serial\_no, serial\_batch\_doc.batch\_no, serial\_batch\_doc.qty, doctype.item\_code, …).where(((nested operand in the contra ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.work\_order → self.subcontracting\_order.
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L708)

<a id="op-42a9ace81552df"></a>
### Stock Entry.set secondary items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_secondary_items`

**Inputs** self.

**Local steps**

- If self.purpose belongs to list(“Manufacture”, “Repack”).
  - Set secondary\_items\_dict from self.get\_secondary\_items(self.fg\_completed\_qty).
  - For each item in secondary\_items\_dict.values().
    - If (self.pro\_doc and item.secondary\_item\_type).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pro\_doc → item.secondary\_item\_type.
      - If (self.pro\_doc.scrap\_warehouse and item.secondary\_item\_type equals “Scrap”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pro\_doc.scrap\_warehouse → item.secondary\_item\_type equals “Scrap”.
        - Set item at “to\_warehouse” from self.pro\_doc.scrap\_warehouse.
    - If item.process\_loss\_per.
      - Update item at “qty” using − flt((item at “qty” × (item.process\_loss\_per ÷ 100)), self.precision(“fg\_completed\_qty”)).
  - Evaluate self.add\_to\_stock\_entry\_detail(secondary\_items\_dict, bom\_no = self.bom\_no).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get secondary items](operations-083.md#op-71a15391fcc3c0), [add to stock entry detail](operations-083.md#op-e7c2657477c713).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L734)

<a id="op-e5cca1a9928da5"></a>
### Stock Entry.set process loss qty

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_process_loss_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “BOM” via get\_cached\_value.

**State and service calls** msgprint with translated “The Process Loss Qty has reset as per job cards Process Loss Qty”.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_upstream\_process\_loss.
- <a id="op-e5cca1a9928da5-guard-4"></a>If self.purpose does not belong to tuple(“Manufacture”, “Repack”).
  - Return no value.
- Set precision from self.precision(“process\_loss\_qty”).
- Set process\_loss\_qty from self.get\_pending\_process\_loss\_qty().
- If (process\_loss\_qty and flt(self.process\_loss\_qty, precision) differs from flt(process\_loss\_qty, precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in process\_loss\_qty → flt(self.process\_loss\_qty, precision) differs from flt(process\_loss\_qty, precision).
  - Set self.process\_loss\_qty from flt(process\_loss\_qty, precision).
  - Evaluate Platform.msgprint(translated “The Process Loss Qty has reset as per job cards Process Loss Qty”, alert = true).
- Set has\_upstream\_loss from (self.work\_order and get\_upstream\_process\_loss(Platform.get\_doc(“Work Order”, self.work\_order))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → get\_upstream\_process\_loss(Platform.get\_doc(“Work Order”, self.work\_order)).
- If (not self.process\_loss\_percentage and not self.process\_loss\_qty and not has\_upstream\_loss).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.process\_loss\_percentage → not self.process\_loss\_qty → not has\_upstream\_loss.
  - Set self.process\_loss\_percentage from Platform.get\_cached\_value(“BOM”, self.bom\_no, “process\_loss\_percentage”).
- If (self.process\_loss\_percentage and not self.process\_loss\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.process\_loss\_percentage → not self.process\_loss\_qty.
  - Set self.process\_loss\_qty from flt(((flt(self.fg\_completed\_qty) × flt(self.process\_loss\_percentage)) ÷ 100)).
- Otherwise.
  - If (self.process\_loss\_qty and self.fg\_completed\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.process\_loss\_qty → self.fg\_completed\_qty.
    - Set self.process\_loss\_percentage from flt(((flt(self.process\_loss\_qty) ÷ flt(self.fg\_completed\_qty)) × 100)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to tuple(“Manufacture”, “Repack”), self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e5cca1a9928da5-guard-4)

**Methods declared on this owner** [get pending process loss qty](operations-082.md#op-8dd3ca9c0fc82a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, self.bom\_no, “process\_loss\_percentage”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L810)

<a id="op-8dc7d6b60f2ad2"></a>
### Stock Entry.validate job card pending production

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate_job_card_pending_production`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The Job Card {0} has only {1} left to produce, but this entry books {2} ({3} finished goods and {4} process  …”.format(Platform.bold(self.job\_card), Platform.bold(formatted text {pending\_qty} { ….

**Local steps**

- If (self.purpose differs from “Manufacture” or not self.job\_card).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purpose differs from “Manufacture” → not self.job\_card.
  - Return no value.
- If self.\_action equals “update\_after\_submit”.
  - Return no value.
- Set job\_card from Platform.get\_doc(“Job Card”, self.job\_card).
- If (job\_card.is\_corrective\_job\_card or job\_card.is\_subcontracted).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_card.is\_corrective\_job\_card → job\_card.is\_subcontracted.
  - Return no value.
- If self.docstatus equals 1.
  - Bind dependencies validate\_job\_card\_submitted\_for\_manufacture.
  - Evaluate validate\_job\_card\_submitted\_for\_manufacture(job\_card).
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- Set pending\_qty from flt((((flt(job\_card.for\_quantity) − flt(job\_card.pending\_qty)) − flt(job\_card.manufactured\_qty)) − flt(job\_card.get\_consumed\_process\_loss())), precision).
- Set finished\_qty from flt(sum(generator of flt(d.transfer\_qty) for d drawn from self.items where d.is\_finished\_item), precision).
  - Draw d from self.items, keep a combination only if (d.is\_finished\_item).
- Set entry\_qty from flt((finished\_qty + flt(self.process\_loss\_qty)), precision).
- If entry\_qty &gt; pending\_qty.
  - Set item\_code from (job\_card.finished\_good or job\_card.production\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_card.finished\_good → job\_card.production\_item.
  - Set uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
  - Call the validation error handler Platform.throw(translated “The Job Card {0} has only {1} left to produce, but this entry books {2} ({3} finished goods and {4} process  …”.format(Platform.bold(self.job\_card), Platform.bold(formatted text  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L836)

<a id="op-8dd3ca9c0fc82a"></a>
### Stock Entry.get pending process loss qty

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_pending_process_loss_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc · resolve a document from “Work Order” via get\_doc.

**Explicit results** max((flt(job\_card.process\_loss\_qty) − flt(job\_card.get\_consumed\_process\_loss())), 0) · max((get\_upstream\_process\_loss(work\_order) − flt(work\_order.process\_loss\_qty)), 0) · 0.

**Local steps**

- Bind dependencies get\_upstream\_process\_loss.
- If self.job\_card.
  - Set job\_card from Platform.get\_doc(“Job Card”, self.job\_card).
  - Return max((flt(job\_card.process\_loss\_qty) − flt(job\_card.get\_consumed\_process\_loss())), 0).
- If self.work\_order.
  - Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order).
  - Return max((get\_upstream\_process\_loss(work\_order) − flt(work\_order.process\_loss\_qty)), 0).
- Return 0.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L787)

<a id="op-ebf7496fe05123"></a>
### Stock Entry.check source documents permission

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_check_source_documents_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L683)

<a id="op-759b32c5cade62"></a>
### Stock Entry.set work order details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_work_order_details`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- If not getattr(self, “pro\_doc”, no value).
  - Set self.pro\_doc from Platform.\_dict().
- If self.work\_order.
  - If not self.pro\_doc.
    - Set self.pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
  - If (self.pro\_doc and not self.pro\_doc.track\_semi\_finished\_goods).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pro\_doc → not self.pro\_doc.track\_semi\_finished\_goods.
    - Set self.bom\_no from self.pro\_doc.bom\_no.
  - Otherwise.
    - Set self.work\_order from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “pro\_doc”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L818)

<a id="op-48072fc4cafd54"></a>
### Stock Entry.load items from bom

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_load_items_from_bom`

**Inputs** self.

**Record and data access** read “BOM” via get\_value · read “Company” via get\_cached\_value · read “Manufacturing Settings” via get\_single\_value.

**Local steps**

- If self.work\_order.
  - Set item\_code from self.pro\_doc.production\_item.
  - Set to\_warehouse from self.pro\_doc.fg\_warehouse.
- Otherwise.
  - Set item\_code from Platform.db.get\_value(“BOM”, self.bom\_no, “item”).
  - Set to\_warehouse from self.to\_warehouse.
- Set item from get\_item\_defaults(item\_code, self.company).
- If (not self.work\_order and not to\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.work\_order → not to\_warehouse.
  - Set to\_warehouse from item.get(“default\_warehouse”).
- Set expense\_account from item.get(“expense\_account”).
- If not expense\_account.
  - Set expense\_account from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”).
- Set args from mapping(“to\_warehouse” → to\_warehouse, “from\_warehouse” → empty text, “qty” → (flt(self.fg\_completed\_qty) − flt(self.process\_loss\_qty)), “item\_name” → item.item\_name, …).
- If self.purpose equals “Disassemble”.
  - Evaluate args.update(mapping(“from\_warehouse” → self.from\_warehouse, “to\_warehouse” → empty text, “qty” → flt(self.fg\_completed\_qty))).
- If (self.work\_order and self.pro\_doc.has\_batch\_no and not self.pro\_doc.has\_serial\_no and cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, cache = true))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.pro\_doc.has\_batch\_no → not self.pro\_doc.has\_serial\_no → cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, cache = true)).
  - Evaluate self.set\_batchwise\_finished\_goods(args, item).
- Otherwise.
  - Evaluate self.add\_finished\_goods(args, item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set batchwise finished goods](operations-082.md#op-0b49576a0ae085), [add finished goods](operations-082.md#op-008197d79002ff).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “stock\_adjustment\_account”), Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L724)

<a id="op-0b49576a0ae085"></a>
### Stock Entry.set batchwise finished goods

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_batchwise_finished_goods`

**Inputs** self, args, item, existing\_row = no value.

**Local steps**

- Set batches from get\_empty\_batches\_based\_work\_order(self.work\_order, self.pro\_doc.production\_item).
- If not batches.
  - If not existing\_row.
    - Evaluate self.add\_finished\_goods(args, item).
- Otherwise.
  - Evaluate self.add\_batchwise\_finished\_good(batches, args, item, existing\_row = existing\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add finished goods](operations-082.md#op-008197d79002ff), [add batchwise finished good](operations-082.md#op-6799b786ad5b77).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L730)

<a id="op-6799b786ad5b77"></a>
### Stock Entry.add batchwise finished good

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_batchwise_finished_good`

**Inputs** self, batches, args, item, existing\_row = no value.

**Explicit results** no value.

**Local steps**

- Set qty from flt(self.fg\_completed\_qty).
- Set row from Platform.\_dict(mapping(“batches\_to\_be\_consume” → defaultdict(float))).
- Evaluate self.update\_batches\_to\_be\_consume(batches, row, qty).
- If not row.batches\_to\_be\_consume.
  - If not existing\_row.
    - Evaluate self.add\_finished\_goods(args, item).
  - Return no value.
- Set \_id from create\_serial\_and\_batch\_bundle(self, row, Platform.\_dict(mapping(“item\_code” → self.pro\_doc.production\_item, “warehouse” → args.get(“to\_warehouse”)))).
- If existing\_row.
  - Set existing\_row.serial\_and\_batch\_bundle from \_id.
  - Set existing\_row.use\_serial\_batch\_fields from 0.
- Otherwise.
  - Set args at “serial\_and\_batch\_bundle” from \_id.
  - Set args at “use\_serial\_batch\_fields” from 0.
  - Evaluate self.add\_finished\_goods(args, item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update batches to be consume](operations-083.md#op-a8b854d36e8071), [add finished goods](operations-082.md#op-008197d79002ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L667)

<a id="op-008197d79002ff"></a>
### Stock Entry.add finished goods

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_add_finished_goods`

**Inputs** self, args, item.

**Local steps**

- Evaluate self.add\_to\_stock\_entry\_detail(mapping(item.name → args), bom\_no = self.bom\_no).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add to stock entry detail](operations-083.md#op-e7c2657477c713).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1171) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L668)

<a id="op-429d929193c3f8"></a>
### Stock Entry.get bom raw materials

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_bill_of_materials_raw_materials`

**Inputs** self, qty, split\_alternative\_items = true.

**Record and data access** read “Work Order” via get\_value · read “Work Order Item” via get\_value.

**Explicit results** item\_dict.

**Local steps**

- Bind dependencies get\_bom\_items\_as\_dict.
- Set item\_dict from get\_bom\_items\_as\_dict(self.bom\_no, self.company, qty = qty, fetch\_exploded = self.use\_multi\_level\_bom, fetch\_qty\_in\_stock\_uom = false).
- For each item in item\_dict.values().
  - If item at “allow\_alternative\_item”.
    - Set item at “allow\_alternative\_item” from Platform.db.get\_value(“Work Order”, self.work\_order, “allow\_alternative\_item”).
  - Set tuple(skip\_transfer, from\_wip\_warehouse) from Platform.get\_value(“Work Order”, self.work\_order, list(“skip\_transfer”, “from\_wip\_warehouse”)) when self.work\_order, otherwise list(no value, no value).
    - Value choice on self.work\_order — true gives Platform.get\_value(“Work Order”, self.work\_order, list(“skip\_transfer”, “from\_wip\_warehouse”)), false gives list(no value, no value).
  - Set item.from\_warehouse from Platform.get\_value(“Work Order Item”, mapping(“parent” → self.work\_order, “item\_code” → item.item\_code), “source\_warehouse”) when (skip\_transfer and not from\_wip\_warehouse), otherwise (self.from\_warehouse  ….
    - Value choice on (skip\_transfer and not from\_wip\_warehouse) — true gives Platform.get\_value(“Work Order Item”, mapping(“parent” → self.work\_order, “item\_code” → item.item\_code), “source\_warehouse”), false gives (self.from\_warehouse or item.source\_warehouse or item.default\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in skip\_transfer → not from\_wip\_warehouse.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.from\_warehouse → item.source\_warehouse → item.default\_warehouse.
- If (self.work\_order and split\_alternative\_items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → split\_alternative\_items.
  - Evaluate self.split\_alternative\_items(item\_dict).
- Return item\_dict.

**Methods declared on this owner** [split alternative items](operations-082.md#op-e470aa4b26d48b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L779)

<a id="op-e470aa4b26d48b"></a>
### Stock Entry.split alternative items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_split_alternative_items`

**Inputs** self, item\_dict.

**Explicit results** no value.

**Local steps**

- Set alternative\_items from get\_alternative\_items\_for\_work\_order(self.work\_order, list of item.item\_code for item drawn from item\_dict.values(), exclude\_stock\_entry = no value when self.is\_new(), otherwise self.name).
  - Draw item from item\_dict.values().
  - Value choice on self.is\_new() — true gives no value, false gives self.name.
- If not alternative\_items.
  - Return no value.
- Set items from list(item\_dict.items()).
- Evaluate item\_dict.clear().
- For each tuple(key, item) in items.
  - Set original\_item from (item.get(“item\_code”) or key).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“item\_code”) → key.
  - Set materials from alternative\_items.get(original\_item).
  - Set split from split\_qty\_by\_alternative\_items(item.qty, materials) when materials, otherwise list().
    - Value choice on materials — true gives split\_qty\_by\_alternative\_items(item.qty, materials), false gives list().
  - If not split.
    - Set item\_dict at key from item.
    - Continue with the next iteration or loop test.
  - Set conversion\_factor from (flt(item.get(“conversion\_factor”)) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.get(“conversion\_factor”)) → 1.
  - For each tuple(material, qty) in split.
    - If not material.original\_item.
      - Set item\_dict at key from Platform.\_dict(item, qty = qty).
      - Continue with the next iteration or loop test.
    - Set item\_dict at tuple(material.item\_code, expanded key when isinstance(key, tuple), otherwise tuple(key)) from Platform.\_dict(item, item\_code = material.item\_code, item\_name = material.item\_name, description = material.description, stock\_uom = material.stock\_uom, …).
      - Value choice on isinstance(key, tuple) — true gives key, false gives tuple(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L743)
