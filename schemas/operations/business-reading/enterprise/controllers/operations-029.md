# Shared transaction rules · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Subcontracting controller

<a id="op-32abb42cab3375"></a>
### Subcontracting Controller.validate returned raw materials

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_validate_returned_raw_materials`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Returns of {0} would take back more of raw material {1} than it consumed. Use Reset Raw Materials Table to p …”.format(get\_link\_to\_form(self.doctype, self.return\_against), Platform.bold(rm\_item\_code)).

**Local steps**

- Set materials from self.get\_returnable\_raw\_materials().
- Set receipt\_rows from mapping of row.name → row.subcontracting\_receipt\_item for row drawn from self.items.
  - Draw row from self.items.
- Set returned\_qty from defaultdict(float).
- For each row in self.supplied\_items.
  - Update returned\_qty at tuple(receipt\_rows.get(row.reference\_name), row.rm\_item\_code) using + abs(flt(row.consumed\_qty)).
- Set precision from Platform.get\_precision(“Subcontracting Receipt Supplied Item”, “consumed\_qty”).
- For each tuple(tuple(receipt\_row, rm\_item\_code), qty) in returned\_qty.items().
  - Set material from materials.get(receipt\_row, mapping()).get(rm\_item\_code).
  - If (material and flt(((material.returned\_qty + qty) − material.consumed\_qty), precision) &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in material → flt(((material.returned\_qty + qty) − material.consumed\_qty), precision) &gt; 0.
    - Call the validation error handler Platform.throw(translated “Returns of {0} would take back more of raw material {1} than it consumed. Use Reset Raw Materials Table to p …”.format(get\_link\_to\_form(self.doctype, self.return\_against), Platfo ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get returnable raw materials](operations-028.md#op-c5d16d8bcd70f4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L445)

<a id="op-3a06a111a9e1a1"></a>
### Subcontracting Controller.get return consumed qty

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_return_consumed_qty`

**Inputs** self, material.

**Record and data access** read “Item” via get\_cached\_value · read “UOM” via get\_cached\_value.

**Explicit results** negative max(flt((total\_returned\_qty − material.returned\_qty), precision), 0).

**Local steps**

- Set share from min((material.returned\_fg\_qty ÷ material.received\_qty), 1) when material.received\_qty, otherwise 1.
  - Value choice on material.received\_qty — true gives min((material.returned\_fg\_qty ÷ material.received\_qty), 1), false gives 1.
- Set precision from Platform.get\_precision(“Subcontracting Receipt Supplied Item”, “consumed\_qty”).
- Set total\_returned\_qty from flt((material.consumed\_qty × share), precision).
- If (Platform.get\_cached\_value(“Item”, material.item\_details at “rm\_item\_code”, “has\_serial\_no”) or Platform.get\_cached\_value(“UOM”, material.item\_details at “stock\_uom”, “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, material.item\_details at “rm\_item\_code”, “has\_serial\_no”) → Platform.get\_cached\_value(“UOM”, material.item\_details at “stock\_uom”, “must\_be\_whole\_number”).
  - Set total\_returned\_qty from min(ceil(total\_returned\_qty), material.consumed\_qty).
- Return negative max(flt((total\_returned\_qty − material.returned\_qty), precision), 0).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, material.item\_details at “rm\_item\_code”, “has\_serial\_no”), Platform.get\_cached\_value(“UOM”, material.item\_details at “stock\_uom”, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L436)

<a id="op-dd5f644b7b33af"></a>
### Subcontracting Controller.get returnable serial batches

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_returnable_serial_batches`

**Inputs** self.

**Explicit results** mapping of key → list of identity for identity drawn from identities.values() where flt(identity.qty, precision) &gt; 0 for tuple(key, identities) drawn from self.get\_consumed\_serial\_batches().items().

**Local steps**

- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- Return mapping of key → list of identity for identity drawn from identities.values() where flt(identity.qty, precision) &gt; 0 for tuple(key, identities) drawn from self.get\_consumed\_serial\_batches().items().
  - Draw tuple(key, identities) from self.get\_consumed\_serial\_batches().items().
  - Draw identity from identities.values(), keep a combination only if (flt(identity.qty, precision) &gt; 0).

**Methods declared on this owner** [get consumed serial batches](operations-029.md#op-4784b039e0b81d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L438)

<a id="op-4784b039e0b81d"></a>
### Subcontracting Controller.get consumed serial batches

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_consumed_serial_batches`

**Inputs** self.

**Explicit results** mapping() · returnable.

**Local steps**

- If not self.is\_subcontracting\_receipt\_return().
  - Return mapping().
- Set receipt from Platform.qb.DocType(“Subcontracting Receipt”).
- Set item from Platform.qb.DocType(“Subcontracting Receipt Item”).
- Set supplied\_item from Platform.qb.DocType(“Subcontracting Receipt Supplied Item”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set serial from Platform.qb.DocType(“Serial No”).
- Set rows from nested operand in the contract(nested operand in the contract).orderby(supplied\_item.idx).orderby(entry.idx).run(as\_dict = true).
- Set returnable from mapping().
- For each row in sorted(rows, key = deferred anonymous expression).
  - Set key from tuple(row.receipt\_item, row.rm\_item\_code).
  - If row.qty &lt; 0.
    - Set identity from returnable.setdefault(key, mapping()).setdefault(tuple(row.serial\_no, row.batch\_no), Platform.\_dict(serial\_no = row.serial\_no, serial\_number = row.serial\_number, batch\_no = row.batch\_no, qty = 0.0, …)).
  - Otherwise.
    - Set identity from returnable.get(key, mapping()).get(tuple(row.serial\_no, row.batch\_no)).
  - If identity.
    - Update identity.qty using − row.qty.
- Return returnable.

**Methods declared on this owner** [is subcontracting receipt return](operations-028.md#op-a9d0e47e1ced68).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L431)

<a id="op-ae7d1fa5b942ce"></a>
### Subcontracting Controller.set serial batch for return

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_set_serial_batch_for_return`

**Inputs** self, rm\_obj, identities.

**Local steps**

- Set qty from abs(rm\_obj.consumed\_qty).
- Set precision from rm\_obj.precision(“consumed\_qty”).
- Set groups from defaultdict(deferred anonymous expression).
- For each identity in identities.
  - Set allocated from min(qty, identity.qty).
  - If flt(allocated, precision) ≤ 0.
    - Continue with the next iteration or loop test.
  - Update identity.qty using − allocated.
  - Update qty using − allocated.
  - Set group from groups at tuple(identity.batch\_no, identity.rate).
  - Update group.qty using + allocated.
  - If identity.serial\_no.
    - Evaluate group.serial\_nos.append(identity.serial\_number).
- For each tuple(tuple(batch\_no, rate), group) in groups.items().
  - Set row from self.append(self.raw\_material\_table, rm\_obj.as\_dict(no\_default\_fields = true)).
  - Evaluate row.update(mapping(“consumed\_qty” → negative flt(group.qty, precision), “rate” → flt(rate, row.precision(“rate”)), “use\_serial\_batch\_fields” → 1, “batch\_no” → batch\_no, …)).
- Evaluate self.remove(rm\_obj).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L443)

<a id="op-cecb270d3a6450"></a>
### Subcontracting Controller.validate returned serial batches

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_validate_returned_serial_batches`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt Supplied Item” via get\_all · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} of raw material {1} was not consumed by {2} or was already returned. Use Reset Raw Materials Table to pi …”.format(Platform.bold((entry.serial\_no or entry.batch\_no)), Platform.bold(key at 1 ….

**Local steps**

- Set returnable from self.get\_returnable\_serial\_batches().
- Set receipt\_items from mapping of row.name → row.subcontracting\_receipt\_item for row drawn from self.items.
  - Draw row from self.items.
- Set bundle\_keys from mapping of row.serial\_and\_batch\_bundle → tuple(receipt\_items.get(row.reference\_name), row.rm\_item\_code) for row drawn from Platform.get\_all(“Subcontracting Receipt Supplied Item”, filters = mapping(“parent ….
  - Draw row from Platform.get\_all(“Subcontracting Receipt Supplied Item”, filters = mapping(“parent” → self.name, “serial\_and\_batch\_bundle” → tuple(“is”, “set”)), fields = list(“serial\_and\_batch\_bundle”, “reference\_name”,  ….
- If not (returnable and bundle\_keys).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in returnable → bundle\_keys.
  - Return no value.
- Set available from mapping of tuple(key, identity.serial\_no, identity.batch\_no) → identity.qty for tuple(key, identities) drawn from returnable.items(), then identity drawn from identities.
  - Draw tuple(key, identities) from returnable.items().
  - Draw identity from identities.
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each entry in Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, list(bundle\_keys))), fields = list(“parent”, “serial\_no”, “batch\_no”, “qty”)).
  - Set key from bundle\_keys at entry.parent.
  - If key does not belong to returnable.
    - Continue with the next iteration or loop test.
  - Set identity from tuple(key, entry.serial\_no, entry.batch\_no).
  - Set available at identity from (available.get(identity, 0.0) − abs(entry.qty)).
  - If flt(available at identity, precision) &lt; 0.
    - Call the validation error handler Platform.throw(translated “{0} of raw material {1} was not consumed by {2} or was already returned. Use Reset Raw Materials Table to pi …”.format(Platform.bold((entry.serial\_no or entry.batch\_no)), Platfor ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.serial\_no → entry.batch\_no.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get returnable serial batches](operations-029.md#op-dd5f644b7b33af).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L446)

<a id="op-c9c5b5813a25c1"></a>
### Subcontracting Controller.get rejected return rows

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_rejected_return_rows`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt Item” via get\_all.

**Explicit results** set() · set of row.name for row drawn from self.items where is\_rejected\_subcontracting\_return(row, rejected\_warehouses.get(row.subcontracting\_receipt\_item)).

**Local steps**

- If not self.is\_return.
  - Return set().
- Set rejected\_warehouses from dict(Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against), fields = list(“name”, “rejected\_warehouse”), as\_list = true)).
- Return set of row.name for row drawn from self.items where is\_rejected\_subcontracting\_return(row, rejected\_warehouses.get(row.subcontracting\_receipt\_item)).
  - Draw row from self.items, keep a combination only if (is\_rejected\_subcontracting\_return(row, rejected\_warehouses.get(row.subcontracting\_receipt\_item))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L435)

<a id="op-4ddc23cd9f88ea"></a>
### Subcontracting Controller.validate rejected warehouse

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate_rejected_warehouse`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Rejected Warehouse is mandatory for the rejected Item {1}”.format(item.idx, item.item\_code) · validation helper — translated “Row #{0}: Accepted Warehouse and Rejected Warehouse cannot be same”.format(item.idx).

**Local steps**

- For each item in self.get(“items”).
  - If (flt(item.rejected\_qty) and not item.rejected\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.rejected\_qty) → not item.rejected\_warehouse.
    - If self.rejected\_warehouse.
      - Set item.rejected\_warehouse from self.rejected\_warehouse.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Rejected Warehouse is mandatory for the rejected Item {1}”.format(item.idx, item.item\_code)).
  - If (item.get(“rejected\_warehouse”) and item.get(“rejected\_warehouse”) equals item.get(“warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“rejected\_warehouse”) → item.get(“rejected\_warehouse”) equals item.get(“warehouse”).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Accepted Warehouse and Rejected Warehouse cannot be same”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L5816) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L732)

<a id="op-08cdfc9b892346"></a>
### Subcontracting Controller.remove empty rows

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_remove_empty_rows`

**Inputs** self.

**Local steps**

- For each key in list(“service\_items”, “items”, “supplied\_items”, “received\_items”).
  - If self.get(key).
    - Set idx from 1.
    - For each item in self.get(key) at slice no value to no value.
      - If not (item.get(“item\_code”) or item.get(“main\_item\_code”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“item\_code”) → item.get(“main\_item\_code”).
        - Evaluate self.get(key).remove(item).
      - Otherwise.
        - Set item.idx from idx.
        - Update idx using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L6184) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L703)

<a id="op-83e45f2564b86d"></a>
### Subcontracting Controller.set items conversion factor

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_items_conversion_factor`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - If not item.conversion\_factor.
    - Set item.conversion\_factor from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L6486) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1035) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L712)

<a id="op-5dec11ef964883"></a>
### Subcontracting Controller.validate items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate_items`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “BOM” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Item {1} must be a stock item.”.format(item.idx, item.item\_name) · validation helper — translated “Row {0}: Delivery Warehouse cannot be same as Customer Warehouse for Item {1}.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row {0}: Item {1} must be a subcontracted item.”.format(item.idx, item.item\_name) · validation helper — translated “Row {0}: Item {1} must be linked to a {2}.”.format(item.idx, item.item\_name, order\_item\_doctype) · validation helper — translated “Row {0}: Item {1}'s quantity cannot be higher than the available quantity.”.format(item.idx, item.item\_name) · 3 additional forms in the steps below.

**Local steps**

- For each item in self.items.
  - Set tuple(is\_stock\_item, is\_sub\_contracted\_item) from Platform.get\_value(“Item”, item.item\_code, list(“is\_stock\_item”, “is\_sub\_contracted\_item”)).
  - If not is\_stock\_item.
    - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} must be a stock item.”.format(item.idx, item.item\_name)).
  - If (self.doctype equals “Subcontracting Inward Order” and item.delivery\_warehouse equals self.customer\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Subcontracting Inward Order” → item.delivery\_warehouse equals self.customer\_warehouse.
    - Call the validation error handler Platform.throw(translated “Row {0}: Delivery Warehouse cannot be same as Customer Warehouse for Item {1}.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - If (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
    - If not is\_sub\_contracted\_item.
      - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} must be a subcontracted item.”.format(item.idx, item.item\_name)).
    - If self.doctype differs from “Subcontracting Receipt”.
      - Set order\_item\_doctype from “Purchase Order Item” when self.doctype equals “Subcontracting Order”, otherwise “Sales Order Item”.
        - Value choice on self.doctype equals “Subcontracting Order” — true gives “Purchase Order Item”, false gives “Sales Order Item”.
      - Set order\_name from self.purchase\_order when self.doctype equals “Subcontracting Order”, otherwise self.sales\_order.
        - Value choice on self.doctype equals “Subcontracting Order” — true gives self.purchase\_order, false gives self.sales\_order.
      - Set order\_item\_field from Platform.scrub(order\_item\_doctype).
      - If not item.get(order\_item\_field).
        - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} must be linked to a {2}.”.format(item.idx, item.item\_name, order\_item\_doctype)).
      - Set pending\_qty from flt((flt(get\_pending\_subcontracted\_quantity(order\_item\_doctype, order\_name).get(item.get(order\_item\_field))) ÷ item.subcontracting\_conversion\_factor), Platform.get\_precision(order\_item\_doctype, “qty”)).
      - If item.qty &gt; pending\_qty.
        - Call the validation error handler Platform.throw(translated “Row {0}: Item {1}'s quantity cannot be higher than the available quantity.”.format(item.idx, item.item\_name)).
    - If self.doctype does not belong to list(“Subcontracting Inward Order”, “Subcontracting Receipt”).
      - Set item.amount from (item.qty × item.rate).
    - If item.bom.
      - Set tuple(is\_active, bom\_item, docstatus) from Platform.get\_value(“BOM”, item.bom, list(“is\_active”, “item”, “docstatus”)).
      - If (not is\_active or docstatus differs from 1).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_active → docstatus differs from 1.
        - Call the validation error handler Platform.throw(translated “Row {0}: Please select an active and submitted BOM for Item {1}.”.format(item.idx, item.item\_name)).
      - If bom\_item does not belong to get\_applicable\_bom\_items(item.item\_code).
        - Call the validation error handler Platform.throw(translated “Row {0}: Please select an valid BOM for Item {1}.”.format(item.idx, item.item\_name)).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row {0}: Please select a BOM for Item {1}.”.format(item.idx, item.item\_name)).
  - Otherwise.
    - Set item.bom from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L731)

<a id="op-95b9e6d1efe799"></a>
### Subcontracting Controller.get data before save

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_data_before_save`

**Inputs** self.

**Explicit results** item\_dict.

**Local steps**

- Set item\_dict from mapping().
- If (self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”) and self.\_doc\_before\_save).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”) → self.\_doc\_before\_save.
  - For each row in self.\_doc\_before\_save.get(“items”).
    - Set item\_dict at row.name from tuple(row.item\_code, row.received\_qty).
- Return item\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L1439) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L686)

<a id="op-58c96fb1ff5b2b"></a>
### Subcontracting Controller.identify change in item table

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_identify_change_in_item_table`

**Inputs** self.

**Explicit results** no value · true.

**Local steps**

- Set self.\_\_changed\_name from list().
- Set self.\_\_reference\_name from list().
- If (self.doctype belongs to list(“Purchase Order”, “Subcontracting Order”, “Subcontracting Inward Order”) or self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Order”, “Subcontracting Order”, “Subcontracting Inward Order”) → self.is\_new().
  - Evaluate self.set(self.raw\_material\_table, list()).
  - Return no value.
- If not self.get(self.raw\_material\_table).
  - Return no value.
- Set item\_dict from self.\_\_get\_data\_before\_save().
- If not item\_dict.
  - Return true.
- For each row in self.items.
  - Evaluate self.\_\_reference\_name.append(row.name).
  - If (row.name does not belong to item\_dict or tuple(row.item\_code, row.received\_qty) differs from item\_dict at row.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.name does not belong to item\_dict → tuple(row.item\_code, row.received\_qty) differs from item\_dict at row.name.
    - Evaluate self.\_\_changed\_name.append(row.name).
  - If item\_dict.get(row.name).
    - Remove item\_dict at row.name.
- Evaluate self.\_\_changed\_name.extend(item\_dict.keys()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data before save](operations-029.md#op-95b9e6d1efe799).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L1641) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L696)

<a id="op-574f24ae8c37fe"></a>
### Subcontracting Controller.get backflush based on

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_backflush_based_on`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Set self.backflush\_based\_on from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) when self.subcontract\_data.order\_doctype equals “Subcontracting Order”, otherwise “Material Transferred fo ….
  - Value choice on self.subcontract\_data.order\_doctype equals “Subcontracting Order” — true gives Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”), false gives “Material Transferred for Subcontract”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L2163) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1004) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L681)

<a id="op-424667fff2569b"></a>
### Subcontracting Controller.initialized fields

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_initialized_fields`

**Inputs** self.

**Local steps**

- Set self.available\_materials from Platform.\_dict().
- Set self.\_\_transferred\_items from Platform.\_dict().
- Set self.alternative\_item\_details from Platform.\_dict().
- Evaluate self.\_\_get\_backflush\_based\_on().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get backflush based on](operations-029.md#op-574f24ae8c37fe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L2281) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L698)

<a id="op-e3716ec4f97c2d"></a>
### Subcontracting Controller.get subcontract orders

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_subcontract_orders`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.subcontract\_orders from list().
- If self.doctype belongs to list(“Purchase Order”, “Subcontracting Order”, “Subcontracting Inward Order”).
  - Return no value.
- Set self.subcontract\_orders from list of item.get(self.subcontract\_data.order\_field) for item drawn from self.items where item.get(self.subcontract\_data.order\_field).
  - Draw item from self.items, keep a combination only if (item.get(self.subcontract\_data.order\_field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L2415) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L693)

<a id="op-0f369db3134437"></a>
### Subcontracting Controller.get pending qty to receive

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_pending_quantity_to_receive`

**Inputs** self.

**Record and data access** read formatted text {self.subcontract\_data.order\_doctype} Item via get\_all.

**Local steps**

- Set self.qty\_to\_be\_received from defaultdict(float).
- If (self.doctype differs from self.subcontract\_data.order\_doctype and self.backflush\_based\_on differs from “BOM” and self.subcontract\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype differs from self.subcontract\_data.order\_doctype → self.backflush\_based\_on differs from “BOM” → self.subcontract\_orders.
  - For each row in Platform.get\_all(formatted text {self.subcontract\_data.order\_doctype} Item, fields = list(“item\_code”, mapping(“SUB” → list(“qty”, “received\_qty”), “as” → “qty”), “parent”, “bom”), filters = mapping(“docst ….
    - Update self.qty\_to\_be\_received at tuple(row.item\_code, row.parent, row.bom) using + row.qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L2614) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L689)

<a id="op-7f1984cdd575d3"></a>
### Subcontracting Controller.get transferred items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_transferred_items`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set se from Platform.qb.DocType(“Stock Entry”).
- Set se\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(se at self.subcontract\_data.order\_field, se.name.a ….
- If self.backflush\_based\_on equals “BOM”.
  - Set query from query.select(se\_detail.original\_item).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L3009) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L695)

<a id="op-9fec1d9b7c7b00"></a>
### Subcontracting Controller.set alternative item details

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_alternative_item_details`

**Inputs** self, row.

**Local steps**

- If row.get(“original\_item”).
  - Set self.alternative\_item\_details at row.get(“original\_item”) from row.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L3859) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L706)

<a id="op-a43d93f691f206"></a>
### Subcontracting Controller.get received items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_received_items`

**Inputs** self, doctype.

**Record and data access** read formatted text {doctype} via get\_all.

**Explicit results** Platform.get\_all(formatted text {doctype}, fields = fields, filters = filters).

**Local steps**

- Set fields from list().
- For each field in list(“name”, self.subcontract\_data.order\_field, “parent”).
  - Evaluate fields.append(formatted text ′tab{doctype} Item′.′{field}′).
- Set filters from list(list(doctype, “docstatus”, “=”, 1), list(formatted text {doctype} Item, self.subcontract\_data.order\_field, “in”, self.subcontract\_orders)).
- If doctype equals “Purchase Invoice”.
  - Evaluate filters.append(list(“Purchase Invoice”, “update\_stock”, “=”, 1)).
- Return Platform.get\_all(formatted text {doctype}, fields = fields, filters = filters).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L3972) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L691)

<a id="op-077bbf7bab8ece"></a>
### Subcontracting Controller.get consumed items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_consumed_items`

**Inputs** self, doctype, receipt\_items.

**Record and data access** read self.subcontract\_data.receipt\_supplied\_items\_field via get\_all.

**Explicit results** Platform.get\_all(self.subcontract\_data.receipt\_supplied\_items\_field, fields = fields, filters = mapping(“docstatus” → 1, “reference\_name” → tuple(“in”, list(receipt\_items)), “parenttype” → doctype)).

**Local steps**

- Set fields from list(“serial\_no”, “rm\_item\_code”, “reference\_name”, “batch\_no”, …).
- If self.subcontract\_data.receipt\_supplied\_items\_field differs from “Purchase Receipt Item Supplied”.
  - Evaluate fields.append(“serial\_and\_batch\_bundle”).
- Return Platform.get\_all(self.subcontract\_data.receipt\_supplied\_items\_field, fields = fields, filters = mapping(“docstatus” → 1, “reference\_name” → tuple(“in”, list(receipt\_items)), “parenttype” → doctype)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L4350) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L684)

<a id="op-54bf6518aa48ac"></a>
### Subcontracting Controller.update consumed materials

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_consumed_materials`

**Inputs** self, doctype, return\_consumed\_items = false.

**Explicit results** tuple(list(), mapping()) when return\_consumed\_items, otherwise no value · tuple(consumed\_materials, receipt\_items) · no value.

**Local steps**

- Set receipt\_items from self.\_\_get\_received\_items(doctype).
- If not receipt\_items.
  - Return tuple(list(), mapping()) when return\_consumed\_items, otherwise no value.
    - Value choice on return\_consumed\_items — true gives tuple(list(), mapping()), false gives no value.
- Set receipt\_items from mapping of item.name → item.get(self.subcontract\_data.order\_field) for item drawn from receipt\_items.
  - Draw item from receipt\_items.
- Set consumed\_materials from self.\_\_get\_consumed\_items(doctype, receipt\_items.keys()).
- If return\_consumed\_items.
  - Return tuple(consumed\_materials, receipt\_items).
- If not consumed\_materials.
  - Return no value.
- Set voucher\_nos from list of d.voucher\_no for d drawn from consumed\_materials where d.voucher\_no.
  - Draw d from consumed\_materials, keep a combination only if (d.voucher\_no).
- Set voucher\_bundle\_data from get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = voucher\_nos, is\_outward = 1, get\_subcontracted\_item = tuple(“Subcontracting Receipt Supplied Item”, “main\_item\_code”)) when voucher\_nos, otherwise mapping().
  - Value choice on voucher\_nos — true gives get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = voucher\_nos, is\_outward = 1, get\_subcontracted\_item = tuple(“Subcontracting Receipt Supplied Item”, “main\_item\_code”)), false gives mapping().
- For each row in consumed\_materials.
  - Set key from tuple(row.rm\_item\_code, row.main\_item\_code, receipt\_items.get(row.reference\_name)).
  - If not self.available\_materials.get(key).
    - Continue with the next iteration or loop test.
  - Update self.available\_materials at key at “qty” using − row.consumed\_qty.
  - Set bundle\_key from tuple(row.rm\_item\_code, row.main\_item\_code, self.supplier\_warehouse, row.voucher\_no).
  - Set consumed\_bundles from voucher\_bundle\_data.get(bundle\_key, Platform.\_dict()).
  - If consumed\_bundles.serial\_nos.
    - Set self.available\_materials at key at “serial\_no” from list((set(self.available\_materials at key at “serial\_no”) − set(consumed\_bundles.serial\_nos))).
  - If consumed\_bundles.batch\_nos.
    - For each tuple(batch\_no, qty) in consumed\_bundles.batch\_nos.items().
      - If qty.
        - Update self.available\_materials at key at “batch\_no” at batch\_no using + qty.
        - Update consumed\_bundles.batch\_nos at batch\_no using + abs(qty).
  - If (row.serial\_no and not consumed\_bundles.serial\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → not consumed\_bundles.serial\_nos.
    - Bind dependencies deprecation\_warning.
    - Evaluate record a compatibility advisory for the invoked interface.
    - Set self.available\_materials at key at “serial\_no” from list((set(self.available\_materials at key at “serial\_no”) − set(get\_serial\_nos(row.serial\_no)))).
  - If (row.batch\_no and not consumed\_bundles.batch\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → not consumed\_bundles.batch\_nos.
    - Bind dependencies deprecation\_warning.
    - Evaluate record a compatibility advisory for the invoked interface.
    - Update self.available\_materials at key at “batch\_no” at row.batch\_no using − row.consumed\_qty.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get received items](operations-029.md#op-a43d93f691f206), [get consumed items](operations-029.md#op-077bbf7bab8ece).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0393.json#L4653) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L722)

<a id="op-511b4c38bd0d44"></a>
### Subcontracting Controller.get available materials

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_available_materials`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.subcontract\_orders.
  - Return no value.
- Set transferred\_items from self.\_\_get\_transferred\_items().
- Set voucher\_nos from list of row.voucher\_no for row drawn from transferred\_items.
  - Draw row from transferred\_items.
- Set voucher\_bundle\_data from get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = voucher\_nos, is\_outward = 0, get\_subcontracted\_item = tuple(“Stock Entry Detail”, “subcontracted\_item”)) when voucher\_nos, otherwise mapping().
  - Value choice on voucher\_nos — true gives get\_voucher\_wise\_serial\_batch\_from\_bundle(voucher\_no = voucher\_nos, is\_outward = 0, get\_subcontracted\_item = tuple(“Stock Entry Detail”, “subcontracted\_item”)), false gives mapping().
- For each row in transferred\_items.
  - Set key from tuple(row.rm\_item\_code, row.main\_item\_code, row.get(self.subcontract\_data.order\_field)).
  - If key does not belong to self.available\_materials.
    - Evaluate self.available\_materials.setdefault(key, Platform.\_dict(mapping(“qty” → 0, “serial\_no” → list(), “batch\_no” → defaultdict(float), “item\_details” → row, …))).
  - Set details from self.available\_materials at key.
  - Update details.qty using + row.qty.
  - Evaluate details at formatted text {self.subcontract\_data.rm\_detail\_field}s.append(row.get(self.subcontract\_data.rm\_detail\_field)).
  - If row.serial\_no.
    - Evaluate details.serial\_no.extend(get\_serial\_nos(row.serial\_no)).
  - If row.batch\_no.
    - Update details.batch\_no at row.batch\_no using + row.qty.
  - If (not row.serial\_no and not row.batch\_no and voucher\_bundle\_data).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_no → not row.batch\_no → voucher\_bundle\_data.
    - Set bundle\_key from tuple(row.rm\_item\_code, row.main\_item\_code, row.t\_warehouse, row.voucher\_no).
    - Set bundle\_data from voucher\_bundle\_data.get(bundle\_key, Platform.\_dict()).
    - If bundle\_data.serial\_nos.
      - Evaluate details.serial\_no.extend(bundle\_data.serial\_nos).
      - Set bundle\_data.serial\_nos from list().
    - If bundle\_data.batch\_nos.
      - For each tuple(batch\_no, qty) in bundle\_data.batch\_nos.items().
        - If qty &lt; 0.
          - Set qty from abs(qty).
        - If qty &gt; 0.
          - Update details.batch\_no at batch\_no using + qty.
          - Update bundle\_data.batch\_nos at batch\_no using − qty.
  - Evaluate self.\_\_set\_alternative\_item\_details(row).
- Set self.\_\_transferred\_items from copy.deepcopy(self.available\_materials).
- If self.get(“is\_old\_subcontracting\_flow”).
  - For each doctype in list(“Purchase Receipt”, “Purchase Invoice”).
    - Evaluate self.\_\_update\_consumed\_materials(doctype).
- Otherwise.
  - Evaluate self.\_\_update\_consumed\_materials(“Subcontracting Receipt”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transferred items](operations-029.md#op-7f1984cdd575d3), [set alternative item details](operations-029.md#op-9fec1d9b7c7b00), [update consumed materials](operations-029.md#op-54bf6518aa48ac).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L680)

<a id="op-ee1fcf5a551bac"></a>
### Subcontracting Controller.remove changed rows

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_remove_changed_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.\_\_changed\_name.
  - Return no value.
- Set i from 1.
- Evaluate self.set(self.raw\_material\_table, list()).
- For each item in self.\_doc\_before\_save.supplied\_items.
  - If item.reference\_name belongs to self.\_\_changed\_name.
    - Evaluate self.\_\_remove\_serial\_and\_batch\_bundle(item).
    - Continue with the next iteration or loop test.
  - If item.reference\_name does not belong to self.\_\_reference\_name.
    - Continue with the next iteration or loop test.
  - Set item.idx from i.
  - Evaluate self.append(“supplied\_items”, item).
  - Update i using + 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove serial and batch bundle](operations-030.md#op-cac1228714377d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0394.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L702)
