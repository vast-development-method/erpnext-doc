# Inventory and warehouses · operations 76

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock closing entry

[Record definition](../../../../data/record-types/stock_closing_entry.json)

<a id="op-c59a1bf9ce692a"></a>
### Stock Closing.get sle entries

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_stock_ledger_entry_entries`

**Inputs** self.

**Explicit results** sl\_entries.

**Local steps**

- Set sl\_entries from list().
- If self.last\_closing\_balance.
  - Set self.from\_date from add\_days(self.last\_closing\_balance.to\_date, 1).
  - Set closing\_balances from self.get\_entries(“Stock Closing Balance”, fields = list(“name”, “item\_code”, “warehouse”, “posting\_date”, …), filters = mapping(“company” → self.company, “stock\_closing\_entry” → self.last\_closing\_balance.name)).
  - For each row in closing\_balances.
    - Set row.from\_closing\_balance from true.
  - Update sl\_entries using + closing\_balances.
- If not self.last\_closing\_balance.
  - Set self.from\_date from “1900-01-01”.
- Update sl\_entries using + self.get\_entries(“Stock Ledger Entry”, fields = list(“name”, “item\_code”, “warehouse”, “posting\_date”, …), filters = mapping(“company” → self.company, “posting\_date” → list(self.from\_date, self.to\_date), “ ….
- Return sl\_entries.

**Methods declared on this owner** [get entries](operations-076.md#op-eb0c5c7a587633).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L748)

<a id="op-eb0c5c7a587633"></a>
### Stock Closing.get entries

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_entries`

**Inputs** self, doctype, fields, filters, remaining named values kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- For each dimension in self.inv\_dimensions.
  - If dimension.fieldname does not belong to fields.
    - Evaluate fields.append(dimension.fieldname).
- Set table from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract.qb.from\_(table).select(expanded fields).orderby(table.posting\_datetime).
- If filters.
  - For each tuple(field, value) in filters.items().
    - If field equals “posting\_date”.
      - Set query from query.where(table at field.between(value at 0, value at 1)).
    - Otherwise.
      - If (isinstance(value, list) or isinstance(value, tuple)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(value, list) → isinstance(value, tuple).
        - Set query from query.where(table at field.isin(value)).
      - Otherwise.
        - Set query from query.where(table at field equals value).
- For each tuple(key, value) in kwargs.items().
  - If value.
    - If (isinstance(value, list) or isinstance(value, tuple)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(value, list) → isinstance(value, tuple).
      - Set query from query.where(table at key.isin(value)).
    - Otherwise.
      - Set query from query.where(table at key equals value).
- If doctype equals “Stock Ledger Entry”.
  - Set sabb\_table from Platform.qb.DocType(“Serial and Batch Entry”).
  - Set query from query.left\_join(sabb\_table).on((sabb\_table.parent equals table.serial\_and\_batch\_bundle bitwise and table.has\_batch\_no equals 1)).
  - Set query from query.select(sabb\_table.batch\_no.as\_(“sabb\_batch\_no”)).
  - Set query from query.select(sabb\_table.qty.as\_(“sabb\_qty”)).
  - Set query from query.select(sabb\_table.stock\_value\_difference.as\_(“sabb\_stock\_value\_difference”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L4138) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L742)

<a id="op-0b6a09b16a72b8"></a>
### Stock Closing.get last stock closing entry

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_last_stock_closing_entry`

**Inputs** self.

**Record and data access** read “Stock Closing Entry” via get\_all.

**Explicit results** entries at 0 when entries, otherwise Platform.\_dict().

**Local steps**

- Set entries from Platform.get\_all(“Stock Closing Entry”, fields = list(“name”, “to\_date”), filters = mapping(“company” → self.company, “to\_date” → list(“&lt;”, self.from\_date), “docstatus” → 1, “status” → “Completed”), order\_ ….
- Return entries at 0 when entries, otherwise Platform.\_dict().
  - Value choice on entries — true gives entries at 0, false gives Platform.\_dict().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L745)

<a id="op-371eaec529bac8"></a>
### Stock Closing.get keys

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_keys`

**Inputs** self, row.

**Explicit results** list(mapping(fields → tuple(generator of row.get(field) for field drawn from fields))) · keys.

**Local steps**

- If row.from\_closing\_balance.
  - If row.inventory\_dimension\_key.
    - Set fields from tuple(json.loads(row.inventory\_dimension\_key)).
  - Otherwise.
    - If row.batch\_no.
      - Set fields from tuple(“item\_code”, “warehouse”, “batch\_no”).
    - Otherwise.
      - Set fields from tuple(“item\_code”, “warehouse”).
  - Return list(mapping(fields → tuple(generator of row.get(field) for field drawn from fields))).
    - Draw field from fields.
- Set keys from list().
- Evaluate keys.append(mapping(tuple(“item\_code”, “warehouse”) → tuple(row.item\_code, row.warehouse))).
- If row.batch\_no.
  - Evaluate keys.append(mapping(tuple(“item\_code”, “warehouse”, “batch\_no”) → tuple(row.item\_code, row.warehouse, row.batch\_no))).
- If row.sabb\_batch\_no.
  - Evaluate keys.append(mapping(tuple(“item\_code”, “warehouse”, “batch\_no”) → tuple(row.item\_code, row.warehouse, row.sabb\_batch\_no))).
- Set dimension\_fields from list().
- Set dimension\_values from list().
- For each dimension in self.inv\_dimensions.
  - If row.get(dimension.fieldname).
    - Evaluate keys.append(mapping(tuple(“item\_code”, “warehouse”, dimension.fieldname) → tuple(row.item\_code, row.warehouse, row.get(dimension.fieldname)))).
    - Evaluate dimension\_fields.append(dimension.fieldname).
    - Evaluate dimension\_values.append(row.get(dimension.fieldname)).
- If (dimension\_fields and len(dimension\_fields) &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension\_fields → len(dimension\_fields) &gt; 1.
  - Evaluate keys.append(mapping(tuple(“item\_code”, “warehouse”, expanded dimension\_fields) → tuple(row.item\_code, row.warehouse, expanded dimension\_values))).
- Return keys.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L744)

<a id="op-17824bfb64f18b"></a>
### Stock Closing.get stock closing balance

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_stock_closing_balance`

**Inputs** self, kwargs, for\_batch = false.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not self.last\_closing\_balance.
  - Return list().
- Set stock\_closing\_entry from self.last\_closing\_balance.name.
- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Set table from Platform.qb.DocType(“Stock Closing Balance”).
- Set query from nested operand in the contract.qb.from\_(table).select(“\*”).where(table.stock\_closing\_entry equals stock\_closing\_entry).
- For each tuple(key, value) in kwargs.items().
  - If key equals “inventory\_dimension\_key”.
    - If (isinstance(value, tuple) and value at 0 equals “is” and value at 1 equals “not set”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, tuple) → value at 0 equals “is” → value at 1 equals “not set”.
      - Set query from query.where((table.inventory\_dimension\_key.isnull() bitwise or table.inventory\_dimension\_key equals empty text)).
  - Otherwise.
    - If (isinstance(value, list) or isinstance(value, tuple)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(value, list) → isinstance(value, tuple).
      - Set query from query.where(table at key.isin(value)).
    - Otherwise.
      - Set query from query.where(table at key equals value).
- If for\_batch.
  - Set query from query.where(table.batch\_no.isnotnull()).
  - Set query from query.where((table.inventory\_dimension\_key.isnull() bitwise or table.inventory\_dimension\_key equals empty text)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L6122) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L746)

<a id="op-589630ffeb9553"></a>
### Get data

`operation_enterprise_stock_record_definitions_stock_closing_entry_stock_closing_entry_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “stock\_closing\_entry”, “transactions” → list(mapping(“label” → translated “Stock Closing Log”, “items” → list(“Stock Closing Balance”)))).

**Local steps**

- Return mapping(“fieldname” → “stock\_closing\_entry”, “transactions” → list(mapping(“label” → translated “Stock Closing Log”, “items” → list(“Stock Closing Balance”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L6897) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L751)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-bd4756c109b965"></a>
### Is costed out of finished item

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_is_costed_out_of_finished_item`

**Inputs** row.

**Declared result** bool.

**Explicit results** bool((row.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”) or (row.secondary\_item\_type and not row.bom\_secondary\_item))).

**Local steps**

- Return bool((row.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”) or (row.secondary\_item\_type and not row.bom\_secondary\_item))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”) → (row.secondary\_item\_type and not row.bom\_secondary\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.secondary\_item\_type → not row.bom\_secondary\_item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0834.json#L5716) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L762)

<a id="op-e4f589a7dd975f"></a>
### Get secondary item key

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_secondary_item_key`

**Inputs** row.

**Explicit results** row.bom\_secondary\_item · tuple(row.item\_code, (row.secondary\_item\_type or “Scrap” when row.get(“valuation\_type”) equals “Valuation Rate”, otherwise empty text)).

**Local steps**

- If row.get(“bom\_secondary\_item”).
  - Return row.bom\_secondary\_item.
- Return tuple(row.item\_code, (row.secondary\_item\_type or “Scrap” when row.get(“valuation\_type”) equals “Valuation Rate”, otherwise empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.secondary\_item\_type → “Scrap” when row.get(“valuation\_type”) equals “Valuation Rate”, otherwise empty text.
  - Value choice on row.get(“valuation\_type”) equals “Valuation Rate” — true gives “Scrap”, false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L649)

<a id="op-054fad93912bc6"></a>
### Qty tolerance

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_qty_tolerance`

**Inputs** precision.

**Declared result** float.

**Explicit results** (1.0 ÷ (10 to the power precision)).

**Local steps**

- Return (1.0 ÷ (10 to the power precision)).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L662)

<a id="op-72f04b0955017f"></a>
### Get whole number units

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_get_whole_number_units`

**Inputs** row.

**Declared result** (tuple at tuple(float, float) bitwise or no value).

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** tuple(flt(row.transfer\_qty), 1.0) · tuple(flt(row.qty), flt(row.conversion\_factor)) · no value.

**Local steps**

- Set uom\_is\_whole from cint(Platform.get\_cached\_value(“UOM”, row.uom, “must\_be\_whole\_number”)).
- Set stock\_uom\_is\_whole from cint(Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”)).
- If (stock\_uom\_is\_whole and (not uom\_is\_whole or flt(row.conversion\_factor) &lt; 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_uom\_is\_whole → (not uom\_is\_whole or flt(row.conversion\_factor) &lt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not uom\_is\_whole → flt(row.conversion\_factor) &lt; 1.
  - Return tuple(flt(row.transfer\_qty), 1.0).
- If uom\_is\_whole.
  - Return tuple(flt(row.qty), flt(row.conversion\_factor)).
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, row.uom, “must\_be\_whole\_number”), Platform.get\_cached\_value(“UOM”, row.stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L656)

<a id="op-da1a58be176984"></a>
### Stock Entry.initialize

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Stock Entry Detail”, “target\_dt” → “Pick List Item”, “join\_field” → “pick\_list\_item”, “target\_field” → “transferred\_qty”, …)).
- If self.purchase\_order.
  - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Purchase Order”, “order\_field” → “purchase\_order”, “rm\_detail\_field” → “po\_detail”, “order\_supplied\_items\_field” → “Purchase Order Item Supplied”)).
- Otherwise.
  - If self.subcontracting\_inward\_order.
    - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Subcontracting Inward Order”, “order\_field” → “subcontracting\_inward\_order”, “rm\_detail\_field” → “scio\_detail”, “order\_received\_items\_field” → “Subcontracting Inwa ….
  - Otherwise.
    - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Subcontracting Order”, “order\_field” → “subcontracting\_order”, “rm\_detail\_field” → “sco\_rm\_detail”, “order\_supplied\_items\_field” → “Subcontracting Order Supplied Item”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L795)

<a id="op-2002ba248e0875"></a>
### Stock Entry.onload

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_onload`

**Inputs** self.

**Local steps**

- Evaluate self.update\_items\_from\_bin\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update items from bin details](operations-076.md#op-75a4a96c1e5301).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0834.json#L6856) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L803)

<a id="op-056ad5ea7555f5"></a>
### Stock Entry.before print

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_before_print`

**Inputs** self, settings = no value.

**Local steps**

- Evaluate super().before\_print(settings).
- Evaluate self.update\_items\_from\_bin\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update items from bin details](operations-076.md#op-75a4a96c1e5301).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0834.json#L6907) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L767)

<a id="op-75a4a96c1e5301"></a>
### Stock Entry.update items from bin details

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_update_items_from_bin_details`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - Evaluate item.update(\_get\_bin\_details(item.item\_code, (item.s\_warehouse or item.t\_warehouse))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.s\_warehouse → item.t\_warehouse.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L819)

<a id="op-75abfd76c62ac5"></a>
### Stock Entry.before insert

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_before_insert`

**Inputs** self.

**Record and data access** read “Subcontracting Order” via get\_cached\_value.

**Local steps**

- If (self.subcontracting\_order and Platform.get\_cached\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_order → Platform.get\_cached\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”).
  - Evaluate self.set\_serial\_batch\_from\_reserved\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set serial batch from reserved entry](operations-082.md#op-84e458d91ceac5).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0835.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1164) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L766)

<a id="op-3e862f6bc2305e"></a>
### Stock Entry.before validate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_before_validate`

**Inputs** self.

**Local steps**

- Bind dependencies \_apply\_putaway\_rule.
- Set apply\_rule from (self.apply\_putaway\_rule and self.purpose belongs to list(“Material Transfer”, “Material Receipt”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.apply\_putaway\_rule → self.purpose belongs to list(“Material Transfer”, “Material Receipt”).
- If (self.get(“items”) and apply\_rule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“items”) → apply\_rule.
  - Evaluate \_apply\_putaway\_rule(self.doctype, self.get(“items”), self.company, purpose = self.purpose).
- If self.project.
  - For each item in self.items.
    - If not item.project.
      - Set item.project from self.project.
- Evaluate self.set\_allow\_alternative\_item().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set allow alternative item](operations-076.md#op-9bab6c4a6d9372).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L768)

<a id="op-9bab6c4a6d9372"></a>
### Stock Entry.set allow alternative item

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_set_allow_alternative_item`

**Inputs** self.

**Record and data access** read “Work Order” via get\_value · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (not self.work\_order or self.purpose does not belong to WORK\_ORDER\_ALTERNATIVE\_ITEM\_PURPOSES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.work\_order → self.purpose does not belong to WORK\_ORDER\_ALTERNATIVE\_ITEM\_PURPOSES.
  - Return no value.
- Set wo\_allows\_alternative\_item from Platform.db.get\_value(“Work Order”, self.work\_order, “allow\_alternative\_item”).
- For each row in self.items.
  - If (not row.s\_warehouse or row.is\_finished\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.s\_warehouse → row.is\_finished\_item.
    - Continue with the next iteration or loop test.
  - Set row.allow\_alternative\_item from cint((wo\_allows\_alternative\_item and Platform.get\_cached\_value(“Item”, (row.original\_item or row.item\_code), “allow\_alternative\_item”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in wo\_allows\_alternative\_item → Platform.get\_cached\_value(“Item”, (row.original\_item or row.item\_code), “allow\_alternative\_item”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, (row.original\_item or row.item\_code), “allow\_alternative\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L729)

<a id="op-4c237b7509e3cd"></a>
### Stock Entry.validate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_validate`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- Evaluate self.validate\_reference\_companies().
- Evaluate self.validate\_row\_reference\_parents().
- Set self.pro\_doc from Platform.\_dict().
- If self.work\_order.
  - Set self.pro\_doc from Platform.get\_doc(“Work Order”, self.work\_order).
- Evaluate self.validate\_warehouses\_company().
- Evaluate self.validate\_duplicate\_serial\_and\_batch\_bundle(“items”).
- Evaluate self.validate\_posting\_time().
- Evaluate self.validate\_purpose().
- Evaluate self.validate\_item().
- Evaluate self.validate\_customer\_provided\_item().
- Evaluate self.set\_transfer\_qty().
- Evaluate self.validate\_warehouse\_of\_sabb().
- Evaluate self.validate\_work\_order().
- Evaluate self.validate\_work\_order\_status\_for\_return().
- Evaluate self.validate\_job\_card\_for\_semi\_finished\_goods().
- Evaluate self.validate\_returned\_qty\_within\_work\_order().
- Evaluate self.validate\_alternative\_items().
- Evaluate self.validate\_source\_stock\_entry().
- Evaluate self.validate\_bom().
- Evaluate self.set\_process\_loss\_qty().
- Evaluate self.validate\_purchase\_order().
- Evaluate self.validate\_company\_in\_accounting\_dimension().
- If self.purpose belongs to tuple(“Manufacture”, “Repack”).
  - Evaluate self.mark\_finished\_and\_secondary\_items().
  - Evaluate self.set\_bomless\_secondary\_valuation\_types().
  - If not self.job\_card.
    - Evaluate self.validate\_finished\_goods().
  - Otherwise.
    - Evaluate self.validate\_job\_card\_fg\_item().
  - If self.purpose equals “Manufacture”.
    - Evaluate self.validate\_outputs\_of\_manufacture().
- Evaluate self.validate\_warehouse().
- Evaluate self.validate\_warehouses\_company().
- Evaluate self.validate\_with\_material\_request().
- If self.purpose equals “Disassemble”.
  - Evaluate self.validate\_disassembly\_quantities().
- Evaluate self.validate\_batch().
- Evaluate self.validate\_against\_pick\_list().
- Evaluate self.validate\_inspection().
- Evaluate self.validate\_fg\_completed\_qty().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “transfer\_qty”).
- Evaluate self.validate\_finished\_good\_qty\_against\_fg\_completed\_qty().
- Evaluate self.validate\_job\_card\_pending\_production().
- Evaluate self.validate\_difference\_account().
- Evaluate self.set\_job\_card\_data().
- Evaluate self.validate\_job\_card\_item().
- Evaluate self.set\_purpose\_for\_stock\_entry().
- Evaluate self.clean\_serial\_nos().
- Evaluate self.validate\_repack\_entry().
- If (not self.from\_bom and not self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.from\_bom → not self.work\_order.
  - Set self.fg\_completed\_qty from 0.0.
- Evaluate self.make\_serial\_and\_batch\_bundle\_for\_outward().
- Evaluate self.validate\_serialized\_batch().
- Evaluate self.calculate\_rate\_and\_amount().
- Evaluate self.validate\_putaway\_capacity().
- Evaluate self.validate\_component\_and\_quantities().
- Evaluate self.validate\_finished\_good\_serial\_batch\_for\_work\_order().
- Evaluate self.validate\_inventory\_dimension\_mandatory().
- If self.get(“purpose”) differs from “Manufacture”.
  - Evaluate self.reset\_default\_field\_value(“from\_warehouse”, “items”, “s\_warehouse”).
  - Evaluate self.reset\_default\_field\_value(“to\_warehouse”, “items”, “t\_warehouse”).
- Evaluate self.validate\_same\_source\_target\_warehouse\_during\_material\_transfer().
- Evaluate self.validate\_closed\_subcontracting\_order().
- Evaluate self.validate\_subcontract\_order().
- Evaluate self.validate\_raw\_materials\_exists().
- Evaluate super().validate\_subcontracting\_inward().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reference companies](operations-076.md#op-b2958cc68fb45a), [validate row reference parents](operations-076.md#op-5352e2d944b1a2), [validate warehouses company](operations-079.md#op-394c89809cbd06), [validate purpose](operations-077.md#op-9c7ce87b183519), [validate item](operations-077.md#op-54d84f2ade8ec0), [set transfer qty](operations-077.md#op-90c3ce21ce82a9), [validate work order](operations-078.md#op-5feb3ad798888d), [validate work order status for return](operations-078.md#op-d13281b1716f58), [validate job card for semi finished goods](operations-078.md#op-b120ff66262fb1), [validate returned qty within work order](operations-078.md#op-bd92821f5c6bf8), [validate alternative items](operations-078.md#op-a3ca4e418d3a86), [validate source stock entry](operations-078.md#op-e33c3e985dff60), [validate bom](operations-080.md#op-f7c49ee61cbb73), [set process loss qty](operations-082.md#op-e5cca1a9928da5), [validate purchase order](operations-080.md#op-dd2be8a888a876), [mark finished and secondary items](operations-080.md#op-86b8be23d2cbe4), [set bomless secondary valuation types](operations-080.md#op-50758a10b3e86f), [validate finished goods](operations-080.md#op-280079619d9cd6), [validate job card fg item](operations-077.md#op-20d64254e589b9), [validate outputs of manufacture](operations-080.md#op-4651f6d09274e1), [validate warehouse](operations-078.md#op-b9682769e17d70), [validate with material request](operations-083.md#op-86be136156d55e), [validate disassembly quantities](operations-078.md#op-1e8e13da564b31), [validate batch](operations-083.md#op-31a7b67af0ba2a), [validate against pick list](operations-083.md#op-7defab565a8265), [validate fg completed qty](operations-077.md#op-868760e915c576), [validate finished good qty against fg completed qty](operations-077.md#op-b1e7841d3e5b03), [validate job card pending production](operations-082.md#op-8dc7d6b60f2ad2), [validate difference account](operations-077.md#op-eefce60faea7ad), [set job card data](operations-077.md#op-2abc4e9db09161), [validate job card item](operations-077.md#op-f0c5bd0d7ef2f3), [set purpose for stock entry](operations-080.md#op-e99ad7ea056d14), [validate repack entry](operations-077.md#op-fb8688d70f2cc7), [make serial and batch bundle for outward](operations-080.md#op-4bb9bd512a8a5e), [calculate rate and amount](operations-079.md#op-e089b5c80e72bd), [validate component and quantities](operations-079.md#op-9b1e76ce75dce3), [validate finished good serial batch for work order](operations-076.md#op-53cc533b12300f), [validate same source target warehouse during material transfer](operations-079.md#op-bd756663901f2e), [validate closed subcontracting order](operations-080.md#op-50b3a238c3596d), [validate subcontract order](operations-080.md#op-21a515a00d1446), [validate raw materials exists](operations-077.md#op-b2fbc1043f210d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L826)

<a id="op-b2958cc68fb45a"></a>
### Stock Entry.validate reference companies

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_reference_companies`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**Explicit failure paths** validation helper — translated “{0} {1} does not belong to Company {2}”.format(translated doctype, other\_company\_document at 0, self.company).

**Local steps**

- For each tuple(doctype, names) in self.get\_referenced\_documents().items().
  - If other\_company\_document bound to Platform.get\_all(doctype, filters = mapping(“name” → tuple(“in”, list(names)), “company” → tuple(“!=”, self.company)), pluck = “name”, limit = 1).
    - Call the validation error handler Platform.throw(translated “{0} {1} does not belong to Company {2}”.format(translated doctype, other\_company\_document at 0, self.company)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get referenced documents](operations-076.md#op-47d732b3cb2219).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L769)

<a id="op-5352e2d944b1a2"></a>
### Stock Entry.validate row reference parents

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_row_reference_parents`

**Inputs** self.

**Record and data access** read child\_doctype via get\_all.

**Explicit failure paths** validation helper — translated “{0} {1} does not belong to {2} {3}”.format(translated child\_doctype, other\_parent\_row at 0, translated self.meta.get\_label(parent\_field), parent).

**Local steps**

- For each tuple(row\_field, child\_doctype, parent\_field) in tuple(tuple(“pick\_list\_item”, “Pick List Item”, “pick\_list”), tuple(“job\_card\_item”, “Job Card Item”, “job\_card”)).
  - Set names from set of row.get(row\_field) for row drawn from self.items where row.get(row\_field).
    - Draw row from self.items, keep a combination only if (row.get(row\_field)).
  - Set parent from (self.get(parent\_field) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(parent\_field) → empty text.
  - If (names and other\_parent\_row bound to Platform.get\_all(child\_doctype, filters = mapping(“name” → tuple(“in”, list(names)), “parent” → tuple(“!=”, parent)), pluck = “name”, limit = 1)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in names → other\_parent\_row bound to Platform.get\_all(child\_doctype, filters = mapping(“name” → tuple(“in”, list(names)), “parent” → tuple(“!=”, parent)), pluck = “name”, limit = 1).
    - Call the validation error handler Platform.throw(translated “{0} {1} does not belong to {2} {3}”.format(translated child\_doctype, other\_parent\_row at 0, translated self.meta.get\_label(parent\_field), parent)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L772)

<a id="op-47d732b3cb2219"></a>
### Stock Entry.get referenced documents

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_referenced_documents`

**Inputs** self.

**Explicit results** references.

**Local steps**

- Set references from defaultdict(set).
- For each fieldname in tuple(“work\_order”, “job\_card”, “pick\_list”, “purchase\_order”, …).
  - If name bound to self.get(fieldname).
    - Evaluate references at self.meta.get\_options(fieldname).add(name).
- For each row in self.get(“items”).
  - If row.material\_request.
    - Evaluate references at “Material Request”.add(row.material\_request).
  - If row.against\_stock\_entry.
    - Evaluate references at “Stock Entry”.add(row.against\_stock\_entry).
- Return references.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L707)

<a id="op-53cc533b12300f"></a>
### Stock Entry.validate finished good serial batch for work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_finished_good_serial_batch_for_work_order`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Row {0}: Serial/Batch has been reset to values linked with Work Order {1} because the previously selected se …”.format(row.idx, Platform.bold(self.work\_order)).

**Explicit results** no value.

**Local steps**

- If not (self.work\_order and self.pro\_doc and self.pro\_doc.get(“track\_semi\_finished\_goods”) differs from 1 and cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, ca ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.pro\_doc → self.pro\_doc.get(“track\_semi\_finished\_goods”) differs from 1 → cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, cache = true)) → (self.pro\_doc.has\_serial\_no or self.pro\_doc.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pro\_doc.has\_serial\_no → self.pro\_doc.has\_batch\_no.
  - Return no value.
- For each row in self.items.
  - If not row.is\_finished\_item.
    - Continue with the next iteration or loop test.
  - If self.check\_invalid\_serial\_batch\_nos\_for\_finished\_good\_item(row).
    - Set had\_selection from (row.serial\_no or row.batch\_no or row.serial\_and\_batch\_bundle).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no → row.serial\_and\_batch\_bundle.
    - Evaluate self.reset\_serial\_batch\_on\_fg\_row(row).
    - If had\_selection.
      - Evaluate Platform.msgprint(translated “Row {0}: Serial/Batch has been reset to values linked with Work Order {1} because the previously selected se …”.format(row.idx, Platform.bold(self.work\_order))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check invalid serial batch nos for finished good item](operations-076.md#op-5f4709757c363d), [reset serial batch on fg row](operations-076.md#op-f72826e4a38f32).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L759)

<a id="op-5f4709757c363d"></a>
### Stock Entry.check invalid serial batch nos for finished good item

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_check_invalid_serial_batch_nos_for_finished_good_item`

**Inputs** self, row.

**Declared result** bool.

**Record and data access** read “Serial No” via get\_all · read “Batch” via get\_all.

**Explicit results** bool((set(serial\_nos) − set(valid\_serial\_nos))) · true · bool((set(batch\_nos) − set(valid\_batch\_nos))).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Bind dependencies get\_batches\_from\_bundle, get\_serial\_nos\_from\_bundle.
- If self.pro\_doc.has\_serial\_no.
  - Set serial\_nos from get\_serial\_nos(row.serial\_no) when row.serial\_no, otherwise list().
    - Value choice on row.serial\_no — true gives get\_serial\_nos(row.serial\_no), false gives list().
  - If (not serial\_nos and row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → row.serial\_and\_batch\_bundle.
    - Set serial\_nos from get\_serial\_nos\_from\_bundle(row.serial\_and\_batch\_bundle).
  - If serial\_nos.
    - Set valid\_serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos), “work\_order” → self.work\_order), pluck = “name”).
    - Return bool((set(serial\_nos) − set(valid\_serial\_nos))).
  - Otherwise.
    - Return true.
- If self.pro\_doc.has\_batch\_no.
  - Set batch\_nos from list(row.batch\_no) when row.batch\_no, otherwise list().
    - Value choice on row.batch\_no — true gives list(row.batch\_no), false gives list().
  - If (not batch\_nos and row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not batch\_nos → row.serial\_and\_batch\_bundle.
    - Set batch\_nos from list(get\_batches\_from\_bundle(row.serial\_and\_batch\_bundle).keys()).
  - If batch\_nos.
    - Set valid\_batch\_nos from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, batch\_nos), “reference\_name” → self.work\_order), pluck = “name”).
    - Return bool((set(batch\_nos) − set(valid\_batch\_nos))).
  - Otherwise.
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L682)

<a id="op-f72826e4a38f32"></a>
### Stock Entry.reset serial batch on fg row

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_reset_serial_batch_on_fg_row`

**Inputs** self, row.

**Local steps**

- Set item\_details from Platform.\_dict(mapping(“item\_code” → row.item\_code, “t\_warehouse” → row.t\_warehouse, “qty” → row.qty)).
- Set row.serial\_no from no value.
- Set row.batch\_no from no value.
- Set row.serial\_and\_batch\_bundle from no value.
- If self.pro\_doc.has\_serial\_no.
  - Evaluate self.set\_serial\_no\_batch\_for\_finished\_good().
- Otherwise.
  - If self.pro\_doc.has\_batch\_no.
    - Evaluate self.set\_batchwise\_finished\_goods(item\_details, no value, existing\_row = row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set serial no batch for finished good](operations-084.md#op-9d8ee47d8a638c), [set batchwise finished goods](operations-082.md#op-0b49576a0ae085).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L728)
