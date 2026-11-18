# Inventory and warehouses · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Packing slip

[Record definition](../../../../data/record-types/packing_slip.json)

<a id="op-c5f95a1604cfe4"></a>
### Packing Slip.validate items

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_validate_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Qty must be greater than 0.”.format(item.idx) · validation helper — translated “Row {0}: Either Delivery Note Item or Packed Item reference is mandatory.”.format(item.idx).

**Local steps**

- Set references from mapping().
- For each item in self.items.
  - <a id="op-c5f95a1604cfe4-guard-4"></a>If item.qty ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Qty must be greater than 0.”.format(item.idx)).
  - If (not item.dn\_detail and not item.pi\_detail).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.dn\_detail → not item.pi\_detail.
    - Call the validation error handler Platform.throw(translated “Row {0}: Either Delivery Note Item or Packed Item reference is mandatory.”.format(item.idx)).
  - Set reference from self.get\_reference\_row(item).
  - Evaluate self.validate\_reference\_row(item, reference).
  - Evaluate self.validate\_remaining\_qty(item, (flt(reference.qty) − flt(reference.packed\_qty))).
  - Set references at (item.dn\_detail or item.pi\_detail) from reference.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.dn\_detail → item.pi\_detail.
- Evaluate self.validate\_total\_qty\_per\_reference(references).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison item.qty ≤ 0, item.qty = 0 selects the branch that calls the validation-error handler with translated “Row {0}: Qty must be greater than 0.”.format(item.idx). With item.qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c5f95a1604cfe4-guard-4)

**Methods declared on this owner** [get reference row](operations-037.md#op-a2ced6a0e3f583), [validate reference row](operations-037.md#op-9f63df20d3ea68), [validate remaining qty](operations-037.md#op-6cd5363b212579), [validate total qty per reference](operations-037.md#op-252e1ff3b5466b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L47)

<a id="op-252e1ff3b5466b"></a>
### Packing Slip.validate total qty per reference

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_validate_total_qty_per_reference`

**Inputs** self, references.

**Explicit failure paths** validation helper — translated “Row {0}: Total packed qty cannot be greater than {1} for the Item {2}.”.format(item.idx, Platform.bold(remaining\_qty), Platform.bold(item.item\_code)).

**Local steps**

- Set qty\_by\_reference from mapping().
- For each item in self.items.
  - Set key from (item.dn\_detail or item.pi\_detail).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.dn\_detail → item.pi\_detail.
  - Set qty\_by\_reference at key from (qty\_by\_reference.get(key, 0) + flt(item.qty)).
  - Set reference from references at key.
  - Set remaining\_qty from (flt(reference.qty) − flt(reference.packed\_qty)).
  - If qty\_by\_reference at key &gt; remaining\_qty.
    - Call the validation error handler Platform.throw(translated “Row {0}: Total packed qty cannot be greater than {1} for the Item {2}.”.format(item.idx, Platform.bold(remaining\_qty), Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L409)

<a id="op-a2ced6a0e3f583"></a>
### Packing Slip.get reference row

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_get_reference_row`

**Inputs** self, item.

**Record and data access** read “Delivery Note Item” when item.dn\_detail, otherwise “Packed Item” via get\_value.

**Explicit results** Platform.db.get\_value(“Delivery Note Item” when item.dn\_detail, otherwise “Packed Item”, mapping(“name” → (item.dn\_detail or item.pi\_detail), “docstatus” → 0), list(“parent”, “item\_code”, “qty”, “packed\_qt ….

**Local steps**

- Return Platform.db.get\_value(“Delivery Note Item” when item.dn\_detail, otherwise “Packed Item”, mapping(“name” → (item.dn\_detail or item.pi\_detail), “docstatus” → 0), list(“parent”, “item\_code”, “qty”, “packed\_qt ….
  - Value choice on item.dn\_detail — true gives “Delivery Note Item”, false gives “Packed Item”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.dn\_detail → item.pi\_detail.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L406)

<a id="op-9f63df20d3ea68"></a>
### Packing Slip.validate reference row

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_validate_reference_row`

**Inputs** self, item, reference.

**Explicit failure paths** validation helper — translated “Row {0}: Please provide a valid Delivery Note Item or Packed Item reference.”.format(item.idx).

**Local steps**

- If (not reference or reference.parent differs from self.delivery\_note or reference.item\_code differs from item.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reference → reference.parent differs from self.delivery\_note → reference.item\_code differs from item.item\_code.
  - Call the validation error handler Platform.throw(translated “Row {0}: Please provide a valid Delivery Note Item or Packed Item reference.”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L407)

<a id="op-6cd5363b212579"></a>
### Packing Slip.validate remaining qty

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_validate_remaining_qty`

**Inputs** self, item, remaining\_qty.

**Explicit failure paths** validation helper — translated “Row {0}: Packing Slip is already created for Item {1}.”.format(item.idx, Platform.bold(item.item\_code)) · validation helper — translated “Row {0}: Qty cannot be greater than {1} for the Item {2}.”.format(item.idx, Platform.bold(remaining\_qty), Platform.bold(item.item\_code)).

**Local steps**

- If remaining\_qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row {0}: Packing Slip is already created for Item {1}.”.format(item.idx, Platform.bold(item.item\_code))).
- Otherwise.
  - If item.qty &gt; remaining\_qty.
    - Call the validation error handler Platform.throw(translated “Row {0}: Qty cannot be greater than {1} for the Item {2}.”.format(item.idx, Platform.bold(remaining\_qty), Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L408)

<a id="op-8d180f984191c2"></a>
### Packing Slip.set missing values

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_set_missing_values`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Local steps**

- If not self.from\_case\_no.
  - Set self.from\_case\_no from self.get\_recommended\_case\_no().
- For each item in self.items.
  - Set tuple(weight\_per\_unit, weight\_uom) from Platform.db.get\_value(“Item”, item.item\_code, list(“weight\_per\_unit”, “weight\_uom”)).
  - If (weight\_per\_unit and not item.net\_weight).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in weight\_per\_unit → not item.net\_weight.
    - Set item.net\_weight from (flt(weight\_per\_unit) × self.get\_conversion\_factor(item)).
  - If (weight\_uom and not item.weight\_uom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in weight\_uom → not item.weight\_uom.
    - Set item.weight\_uom from weight\_uom.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get recommended case no](operations-037.md#op-5833794f9a6a1b), [get conversion factor](operations-037.md#op-7eb10c29a6f2fc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L43)

<a id="op-7eb10c29a6f2fc"></a>
### Packing Slip.get conversion factor

`operation_enterprise_binding_enterprise_stock_doctype_packing_slip_packing_slip_packingslip_get_conversion_factor`

**Inputs** self, item.

**Record and data access** read “Delivery Note Item” via get\_value.

**Explicit results** 1.0 · (flt(Platform.db.get\_value(“Delivery Note Item”, item.dn\_detail, “conversion\_factor”)) or 1.0).

**Local steps**

- If not item.dn\_detail.
  - Return 1.0.
- Return (flt(Platform.db.get\_value(“Delivery Note Item”, item.dn\_detail, “conversion\_factor”)) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(Platform.db.get\_value(“Delivery Note Item”, item.dn\_detail, “conversion\_factor”)) → 1.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L405)

<a id="op-5833794f9a6a1b"></a>
### Packing Slip.get recommended case no

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_get_recommended_case_number`

**Inputs** self.

**Record and data access** read “Packing Slip” via get\_value.

**Explicit results** (cint(Platform.db.get\_value(“Packing Slip”, mapping(“delivery\_note” → self.delivery\_note, “docstatus” → 1), list(mapping(“MAX” → “to\_case\_no”)))) + 1).

**Local steps**

- Return (cint(Platform.db.get\_value(“Packing Slip”, mapping(“delivery\_note” → self.delivery\_note, “docstatus” → 1), list(mapping(“MAX” → “to\_case\_no”)))) + 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L3424) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L39)

<a id="op-bdefd236935ba4"></a>
### Packing Slip.calculate net total pkg

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_packing_slip_calculate_net_total_pkg`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Different UOM for items will lead to incorrect (Total) Net Weight value. Make sure that Net Weight of each i …”.

**Local steps**

- Set self.net\_weight\_uom from self.items at 0.weight\_uom when self.items, otherwise no value.
  - Value choice on self.items — true gives self.items at 0.weight\_uom, false gives no value.
- Set self.gross\_weight\_uom from self.net\_weight\_uom.
- Set net\_weight\_pkg from 0.
- For each item in self.items.
  - If item.weight\_uom differs from self.net\_weight\_uom.
    - Call the validation error handler Platform.throw(translated “Different UOM for items will lead to incorrect (Total) Net Weight value. Make sure that Net Weight of each i …”).
  - Update net\_weight\_pkg using + (flt(item.net\_weight) × flt(item.qty)).
- Set self.net\_weight\_pkg from round(net\_weight\_pkg, 2).
- If not flt(self.gross\_weight\_pkg).
  - Set self.gross\_weight\_pkg from self.net\_weight\_pkg.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0760.json#L3577) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L38)

<a id="op-b5d4ac347609bf"></a>
### Item details

`operation_enterprise_stock_record_definitions_packing_slip_business_behavior_item_details`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, Item, Delivery Note Item).format(“%s”, searchfield, “%s”, get\_match\_cond(doctype), …).

**Explicit results** Platform.db.sql(query text (SELECT, Item, Delivery Note Item).format(“%s”, searchfield, “%s”, get\_match\_cond(doctype), …), tuple((filters or mapping()).get(“delivery\_note”), (“%%%s%%” modulo or format txt) ….

**Local steps**

- Bind dependencies get\_match\_cond.
- Return Platform.db.sql(query text (SELECT, Item, Delivery Note Item).format(“%s”, searchfield, “%s”, get\_match\_cond(doctype), …), tuple((filters or mapping()).get(“delivery\_note”), (“%%%s%%” modulo or format txt) ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L37)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-dcddde727b9b32"></a>
### Pick List.initialize

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Pick List Item”, “target\_dt” → “Material Request Item”, “target\_field” → “picked\_qty”, “target\_parent\_dt” → “Material Request”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L88)

<a id="op-7b4c27163bb212"></a>
### Pick List.onload

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_onload`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_cached\_value.

**Local steps**

- If Platform.get\_cached\_value(“Stock Settings”, no value, “enable\_stock\_reservation”).
  - If self.has\_unreserved\_stock().
    - Evaluate self.set\_onload(“has\_unreserved\_stock”, true).
- If self.has\_reserved\_stock().
  - Evaluate self.set\_onload(“has\_reserved\_stock”, true).
- If (self.docstatus.is\_draft() and not hasattr(self, “\_action”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus.is\_draft() → not hasattr(self, “\_action”).
  - Set company from self.company.
  - For each item in self.get(“locations”).
    - Set details from get\_item\_details(item.item\_code, item.uom, item.warehouse, company).
    - Evaluate details.pop(“conversion\_factor”, no value).
    - Evaluate item.update(details).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has unreserved stock](operations-039.md#op-52cdb43f348185), [has reserved stock](operations-039.md#op-3729827498d09e).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Settings”, no value, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L98)

<a id="op-ca338bc9edc87c"></a>
### Pick List.validate

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_stock\_qty().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”, “Pick List Item”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, list(“stock\_qty”, “picked\_qty”), “Pick List Item”).
- Evaluate self.validate\_expired\_batches().
- Evaluate self.validate\_for\_qty().
- Evaluate self.validate\_stock\_qty().
- Evaluate self.check\_serial\_no\_status().
- Evaluate self.validate\_with\_previous\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set stock qty](operations-037.md#op-0ec474fbfd53af), [validate expired batches](operations-038.md#op-af104d224e13ed), [validate for qty](operations-039.md#op-89d49a05d53215), [validate stock qty](operations-037.md#op-9b8aae34057855), [check serial no status](operations-037.md#op-a4fb61b1244b44), [validate with previous doc](operations-037.md#op-ff03b3107a1aab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L112)

<a id="op-0ec474fbfd53af"></a>
### Pick List.set stock qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_set_stock_qty`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If (not self.docstatus.is\_draft() and getattr(self, “\_action”, no value) differs from “submit”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.docstatus.is\_draft() → getattr(self, “\_action”, no value) differs from “submit”.
  - Return no value.
- Set conversion\_factors from get\_uom\_conversion\_factors(set of row.item\_code for row drawn from self.locations where row.item\_code).
  - Draw row from self.locations, keep a combination only if (row.item\_code).
- Set ordered\_conversion\_factors from self.get\_ordered\_conversion\_factors().
- For each row in self.locations.
  - If not row.item\_code.
    - Continue with the next iteration or loop test.
  - Set stock\_uom from Platform.get\_cached\_value(“Item”, row.item\_code, “stock\_uom”).
  - Set row.stock\_uom from stock\_uom.
  - Set row.uom from (row.uom or stock\_uom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.uom → stock\_uom.
  - Set ordered\_row from (not row.product\_bundle\_item and (row.sales\_order\_item or row.material\_request\_item)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.product\_bundle\_item → (row.sales\_order\_item or row.material\_request\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.sales\_order\_item → row.material\_request\_item.
  - If row.uom equals stock\_uom.
    - Set row.conversion\_factor from 1.
  - Otherwise.
    - If tuple(ordered\_row, row.item\_code, row.uom) belongs to ordered\_conversion\_factors.
      - Set row.conversion\_factor from ordered\_conversion\_factors at tuple(ordered\_row, row.item\_code, row.uom).
    - Otherwise.
      - If tuple(row.item\_code, row.uom) belongs to conversion\_factors.
        - Set row.conversion\_factor from conversion\_factors at tuple(row.item\_code, row.uom).
  - Set row.stock\_qty from flt((flt(row.qty) × flt(row.conversion\_factor)), row.precision(“stock\_qty”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ordered conversion factors](operations-037.md#op-35ab4959b38ae3).

**Values supplied outside this operation** selected callable from getattr(self, “\_action”, no value) · configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L448)

<a id="op-35ab4959b38ae3"></a>
### Pick List.get ordered conversion factors

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_ordered_conversion_factors`

**Inputs** self.

**Declared result** dict.

**Record and data access** read doctype via get\_all.

**Explicit results** conversion\_factors.

**Local steps**

- Set conversion\_factors from mapping().
- For each tuple(doctype, field) in tuple(tuple(“Sales Order Item”, “sales\_order\_item”), tuple(“Material Request Item”, “material\_request\_item”)).
  - Set names from set of row.get(field) for row drawn from self.locations where row.get(field).
    - Draw row from self.locations, keep a combination only if (row.get(field)).
  - If not names.
    - Continue with the next iteration or loop test.
  - For each row in Platform.get\_all(doctype, filters = mapping(“name” → tuple(“in”, list(names))), fields = list(“name”, “item\_code”, “uom”, “conversion\_factor”)).
    - Set conversion\_factors at tuple(row.name, row.item\_code, row.uom) from flt(row.conversion\_factor).
- Return conversion\_factors.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L200) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L445)

<a id="op-30c5c845f999eb"></a>
### Pick List.before save

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- If not self.pick\_manually.
  - Evaluate self.set\_item\_locations().
- If self.get(“locations”).
  - Evaluate self.validate\_sales\_order\_percentage().
  - Evaluate self.validate\_warehouses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-038.md#op-644d0ad34fadce), [set item locations](operations-039.md#op-3b00d61c3d44ac), [validate sales order percentage](operations-037.md#op-0bbbd890dd25cb), [validate warehouses](operations-037.md#op-f705e081d99005).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0762.json#L1661) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L73)

<a id="op-9b8aae34057855"></a>
### Pick List.validate stock qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_stock_quantity`

**Inputs** self.

**Record and data access** read “Bin” via get\_value.

**Explicit failure paths** validation helper — translated “At Row #{0}: The picked quantity {1} for the item {2} is greater than available stock {3} for the batch {4}  …”.format(row.idx, row\_qty, row.item\_code, batch\_qty, …) · validation helper — translated “At Row #{0}: The picked quantity {1} for the item {2} is greater than available stock {3} in the warehouse {4}.”.format(row.idx, row\_qty, bold(row.item\_code), bin\_qty, …).

**Local steps**

- For each row in self.get(“locations”).
  - Set row\_qty from self.get\_qty\_to\_pick(row).
  - If not row\_qty.
    - Continue with the next iteration or loop test.
  - If row.batch\_no.
    - Set batch\_qty from get\_batch\_qty\_for\_stock(row.batch\_no, row.warehouse, item\_code = row.item\_code).
    - If row\_qty &gt; batch\_qty.
      - Call the validation error handler Platform.throw(translated “At Row #{0}: The picked quantity {1} for the item {2} is greater than available stock {3} for the batch {4}  …”.format(row.idx, row\_qty, row.item\_code, batch\_qty, …), title = tra ….
    - Continue with the next iteration or loop test.
  - Set bin\_qty from flt(Platform.db.get\_value(“Bin”, mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse), “actual\_qty”)).
  - If row\_qty &gt; bin\_qty.
    - Call the validation error handler Platform.throw(translated “At Row #{0}: The picked quantity {1} for the item {2} is greater than available stock {3} in the warehouse {4}.”.format(row.idx, row\_qty, bold(row.item\_code), bin\_qty, …), title  ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty to pick](operations-037.md#op-7065db3f95f646).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L121)

<a id="op-7065db3f95f646"></a>
### Pick List.get qty to pick

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_qty_to_pick`

**Inputs** self, row.

**Explicit results** flt(row.picked\_qty) · flt(row.stock\_qty).

**Local steps**

- If (row.picked\_qty or self.scan\_mode or not self.docstatus.is\_submitted()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.picked\_qty → self.scan\_mode → not self.docstatus.is\_submitted().
  - Return flt(row.picked\_qty).
- Return flt(row.stock\_qty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L447)

<a id="op-f705e081d99005"></a>
### Pick List.validate warehouses

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_warehouses`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit failure paths** validation helper with MissingWarehouseValidationError — translated “Row {0}: Warehouse is required”.format(location.idx) · validation helper with IncorrectWarehouseValidationError — translated “Row {0}: Warehouse {1} is linked to company {2}. Please select a warehouse belonging to company {3}.”.format(location.idx, Platform.bold(location.warehouse), Platform.bold(company), Platform.bo ….

**Local steps**

- For each location in self.locations.
  - If not location.warehouse.
    - Call the validation error handler Platform.throw(translated “Row {0}: Warehouse is required”.format(location.idx), title = translated “Missing Warehouse”, exc = MissingWarehouseValidationError).
  - Set company from Platform.get\_cached\_value(“Warehouse”, location.warehouse, “company”).
  - If company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Row {0}: Warehouse {1} is linked to company {2}. Please select a warehouse belonging to company {3}.”.format(location.idx, Platform.bold(location.warehouse), Platform.bold(compan ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, location.warehouse, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0762.json#L2424) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L122)

<a id="op-a4fb61b1244b44"></a>
### Pick List.check serial no status

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_check_serial_number_status`

**Inputs** self.

**Record and data access** read “Serial No” via get\_all.

**Explicit failure paths** validation helper — translated “The Serial No at Row #{0}: {1} is not available in warehouse {2}.”.format(row.idx, “, ”.join(incorrect\_serial\_nos), row.warehouse).

**Local steps**

- Bind dependencies get\_serial\_nos.
- For each row in self.get(“locations”).
  - If not row.serial\_no.
    - Continue with the next iteration or loop test.
  - Set picked\_serial\_nos from get\_serial\_nos(row.serial\_no).
  - Set validated\_serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, picked\_serial\_nos), “warehouse” → row.warehouse), pluck = “name”).
  - Set incorrect\_serial\_nos from (set(picked\_serial\_nos) − set(validated\_serial\_nos)).
  - If incorrect\_serial\_nos.
    - Call the validation error handler Platform.throw(translated “The Serial No at Row #{0}: {1} is not available in warehouse {2}.”.format(row.idx, “, ”.join(incorrect\_serial\_nos), row.warehouse), title = translated “Incorrect Warehouse”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0762.json#L2829) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L76)

<a id="op-ff03b3107a1aab"></a>
### Pick List.validate with previous doc

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_with_previous_record`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Sales Order” → mapping(“ref\_dn\_field” → “sales\_order”, “compare\_fields” → list(list(“company”, “=”))))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0762.json#L3230) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L123)

<a id="op-0bbbd890dd25cb"></a>
### Pick List.validate sales order percentage

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_sales_order_percentage`

**Inputs** self.

**Record and data access** read “Sales Order” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{}: item {} has been picked already.”.format(location.idx, location.item\_code).

**Local steps**

- For each location in self.get(“locations”).
  - If (location.sales\_order and Platform.db.get\_value(“Sales Order”, location.sales\_order, “per\_picked”, cache = true) equals 100).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in location.sales\_order → Platform.db.get\_value(“Sales Order”, location.sales\_order, “per\_picked”, cache = true) equals 100.
    - Call the validation error handler Platform.throw(translated “Row #{}: item {} has been picked already.”.format(location.idx, location.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L119)

<a id="op-c5fb289678ad26"></a>
### Pick List.before submit

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_sales\_order().
- Evaluate self.validate\_picked\_items().
- Evaluate self.validate\_picked\_serial\_and\_batch().
- Evaluate self.validate\_pending\_qty\_in\_work\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales order](operations-038.md#op-35c2ba3ae2a68f), [validate picked items](operations-038.md#op-bd63f64c96ecac), [validate picked serial and batch](operations-038.md#op-c2b12b6d4a6ece), [validate pending qty in work order](operations-037.md#op-6a59620aab45f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L74)

<a id="op-6a59620aab45f2"></a>
### Pick List.validate pending qty in work order

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_pending_quantity_in_work_order`

**Inputs** self.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “Material Request Item” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: picked qty {1} {2} exceeds the pending qty in Material Request {3}.”.format(row.idx, row.picked\_qty, row.stock\_uom, row.material\_request).

**Local steps**

- If not self.work\_order.
  - Return no value.
- Set work\_order from Platform.get\_doc(“Work Order”, self.work\_order, for\_update = true).
- Set live\_requests from mapping().
- Set request\_pending from mapping().
- Set incoming from mapping().
- For each row in self.locations.
  - If row.material\_request does not belong to live\_requests.
    - Set live\_requests at row.material\_request from is\_live\_material\_request(row.material\_request).
  - If not (row.material\_request\_item and live\_requests at row.material\_request).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.material\_request\_item → live\_requests at row.material\_request.
    - Set incoming at row.item\_code from (incoming.get(row.item\_code, 0.0) + flt(row.picked\_qty)).
    - Continue with the next iteration or loop test.
  - If row.material\_request\_item does not belong to request\_pending.
    - Set tuple(stock\_qty, ordered\_qty) from Platform.db.get\_value(“Material Request Item”, row.material\_request\_item, list(“stock\_qty”, “ordered\_qty”)).
    - Set request\_pending at row.material\_request\_item from (flt(stock\_qty) − flt(ordered\_qty)).
  - If flt((row.picked\_qty − request\_pending at row.material\_request\_item), 6) &gt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: picked qty {1} {2} exceeds the pending qty in Material Request {3}.”.format(row.idx, row.picked\_qty, row.stock\_uom, row.material\_request), title = translated “Exceeds R ….
  - Update request\_pending at row.material\_request\_item using − flt(row.picked\_qty).
- Evaluate work\_order.validate\_incoming\_material\_demand(incoming).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L115)
