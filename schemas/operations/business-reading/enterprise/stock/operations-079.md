# Inventory and warehouses · operations 79

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry

[Record definition](../../../../data/record-types/stock_entry.json)

<a id="op-d7ae0226a4c4aa"></a>
### Stock Entry.check duplicate entry for work order

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_check_duplicate_entry_for_work_order`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_values · read “Work Order” via get\_value · execute query text (SELECT, Stock Entry Detail).format(“, ”.join(list((“%s” × len(other\_ste)))), “%s”) · read “Manufacturing Settings” via get\_single\_value.

**Explicit failure paths** validation helper with DuplicateEntryForWorkOrderError — translated “Stock Entries already created for Work Order {0}: {1}”.format(self.work\_order, “, ”.join(other\_ste)).

**Local steps**

- Set other\_ste from list of t at 0 for t drawn from Platform.db.get\_values(“Stock Entry”, mapping(“work\_order” → self.work\_order, “purpose” → self.purpose, “docstatus” → list(“!=”, 2), “name” → list(“!=”, self.name)), “name”).
  - Draw t from Platform.db.get\_values(“Stock Entry”, mapping(“work\_order” → self.work\_order, “purpose” → self.purpose, “docstatus” → list(“!=”, 2), “name” → list(“!=”, self.name)), “name”).
- If other\_ste.
  - Set tuple(production\_item, qty) from Platform.db.get\_value(“Work Order”, self.work\_order, list(“production\_item”, “qty”)).
  - Set args from list(expanded other\_ste, production\_item).
  - Set fg\_qty\_already\_entered from Platform.db.sql(query text (SELECT, Stock Entry Detail).format(“, ”.join(list((nested operand in the contract × nested operand in the contract))), “%s”), args) at 0 at 0.
  - Set allowance\_percentage from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”)).
  - Set allowed\_qty from (flt(qty) + ((allowance\_percentage ÷ 100) × flt(qty))).
  - If (fg\_qty\_already\_entered and fg\_qty\_already\_entered ≥ allowed\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fg\_qty\_already\_entered → fg\_qty\_already\_entered ≥ allowed\_qty.
    - Call the validation error handler Platform.throw(translated “Stock Entries already created for Work Order {0}: {1}”.format(self.work\_order, “, ”.join(other\_ste)), DuplicateEntryForWorkOrderError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L680)

<a id="op-394c89809cbd06"></a>
### Stock Entry.validate warehouses company

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_warehouses_company`

**Inputs** self.

**Local steps**

- Set warehouses from (set of d.s\_warehouse for d drawn from self.get(“items”) bitwise or set of d.t\_warehouse for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
  - Draw d from self.get(“items”).
- For each warehouse in (warehouses − set(no value, empty text)).
  - Evaluate validate\_warehouse\_company(warehouse, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L778)

<a id="op-eef6d1415cea78"></a>
### Stock Entry.set actual qty

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_actual_quantity`

**Inputs** self.

**Explicit failure paths** validation helper with NegativeStockError — ((translated “Row {0}: Quantity not available for {4} in warehouse {1} at posting time of the entry ({2} {3})”.format(d.idx, Platform.bold(d.s\_warehouse), formatdate(self.posting\_date), format\_time(self.po ….

**Local steps**

- Bind dependencies is\_negative\_stock\_allowed.
- Evaluate self.validate\_warehouses\_company().
- For each d in self.get(“items”).
  - Set allow\_negative\_stock from is\_negative\_stock\_allowed(item\_code = d.item\_code).
  - Set previous\_sle from get\_previous\_sle(mapping(“item\_code” → d.item\_code, “warehouse” → (d.s\_warehouse or d.t\_warehouse), “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.s\_warehouse → d.t\_warehouse.
  - Set d.actual\_qty from (previous\_sle.get(“qty\_after\_transaction”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_sle.get(“qty\_after\_transaction”) → 0.
  - If (d.docstatus equals 1 and d.s\_warehouse and not allow\_negative\_stock and flt(d.actual\_qty, d.precision(“actual\_qty”)) &lt; flt(d.transfer\_qty, d.precision(“actual\_qty”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.docstatus equals 1 → d.s\_warehouse → not allow\_negative\_stock → flt(d.actual\_qty, d.precision(“actual\_qty”)) &lt; flt(d.transfer\_qty, d.precision(“actual\_qty”)).
    - Call the validation error handler Platform.throw(((translated “Row {0}: Quantity not available for {4} in warehouse {1} at posting time of the entry ({2} {3})”.format(d.idx, Platform.bold(d.s\_warehouse), formatdate(self.posting\_date), form ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate warehouses company](operations-079.md#op-394c89809cbd06).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L805)

<a id="op-9b1e76ce75dce3"></a>
### Stock Entry.validate component and quantities

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_component_and_quantities`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “According to the BOM {0}, the Item '{1}' is missing in the stock entry.”.format(get\_link\_to\_form(“BOM”, self.bom\_no), Platform.bold(item\_code)) · validation helper — translated “For the item {0}, the consumed quantity should be {1} according to the BOM {2}.”.format(Platform.bold(item\_code), flt(bom\_qty, precision), get\_link\_to\_form(“BOM”, self.bom\_no)).

**Local steps**

- <a id="op-9b1e76ce75dce3-guard-2"></a>If self.purpose does not belong to list(“Manufacture”, “Material Transfer for Manufacture”).
  - Return no value.
- If not self.fg\_completed\_qty.
  - If (self.work\_order and self.purpose equals “Material Transfer for Manufacture”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.work\_order → self.purpose equals “Material Transfer for Manufacture”.
    - Evaluate self.\_validate\_no\_excess\_transfer().
  - Return no value.
- If not Platform.db.get\_single\_value(“Manufacturing Settings”, “validate\_components\_quantities\_per\_bom”).
  - Return no value.
- If self.consumes\_transferred\_materials().
  - Return no value.
- Set raw\_materials from self.get\_bom\_raw\_materials(self.fg\_completed\_qty, split\_alternative\_items = false).
- Set precision from Platform.get\_precision(“Stock Entry Detail”, “qty”).
- For each tuple(item\_code, bom\_qty) in get\_bom\_stock\_qty\_by\_item(raw\_materials).items().
  - Set matched\_items from self.get\_matched\_items(item\_code).
  - If not matched\_items.
    - Call the validation error handler Platform.throw(translated “According to the BOM {0}, the Item '{1}' is missing in the stock entry.”.format(get\_link\_to\_form(“BOM”, self.bom\_no), Platform.bold(item\_code)), title = translated “Missing Item”).
  - If flt(bom\_qty, precision) differs from flt(sum(generator of flt(d.transfer\_qty) for d drawn from matched\_items), precision).
    - Draw d from matched\_items.
    - Call the validation error handler Platform.throw(translated “For the item {0}, the consumed quantity should be {1} according to the BOM {2}.”.format(Platform.bold(item\_code), flt(bom\_qty, precision), get\_link\_to\_form(“BOM”, self.bom\_no)),  ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose does not belong to list(“Manufacture”, “Material Transfer for Manufacture”), self.purpose = “Material Issue” selects the branch that returns no value. With self.purpose = “Material Transfer for Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9b1e76ce75dce3-guard-2)

**Methods declared on this owner** [validate no excess transfer](operations-079.md#op-9a7e5623bf80fa), [consumes transferred materials](operations-079.md#op-19cf8f67da62a1), [get bom raw materials](operations-082.md#op-429d929193c3f8), [get matched items](operations-079.md#op-0f1af63002b908).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “validate\_components\_quantities\_per\_bom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L755)

<a id="op-19cf8f67da62a1"></a>
### Stock Entry.consumes transferred materials

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_consumes_transferred_materials`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · not (self.pro\_doc and self.pro\_doc.skip\_transfer) · true.

**Local steps**

- If self.get\_backflush\_based\_on() differs from “Material Transferred for Manufacture”.
  - Return false.
- If self.purpose equals “Manufacture”.
  - Return not (self.pro\_doc and self.pro\_doc.skip\_transfer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pro\_doc → self.pro\_doc.skip\_transfer.
- Return true.

**Methods declared on this owner** [get backflush based on](operations-082.md#op-10944d97a583f0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L684)

<a id="op-9a7e5623bf80fa"></a>
### Stock Entry.validate no excess transfer

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_no_excess_transfer`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot transfer {1} {2} of Item {3}. Maximum transferable quantity is {4} {2}.”.format(item.idx, transfer\_qty, item.stock\_uom, Platform.bold(item.item\_code), …).

**Local steps**

- If self.is\_return.
  - Return no value.
- If Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”) equals “Material Transferred for Manufacture”.
  - Return no value.
- Set wo from self.pro\_doc.
- If not wo.
  - Return no value.
- Bind dependencies get\_allowed\_transfer\_qty.
- Set pending\_by\_item from mapping().
- For each r in wo.required\_items.
  - Set pending\_by\_item at r.item\_code from ((pending\_by\_item.get(r.item\_code, 0.0) + get\_allowed\_transfer\_qty(r.required\_qty)) − flt(r.transferred\_qty)).
- Set transfer\_by\_item from mapping().
- Set first\_row\_by\_item from mapping().
- For each item in self.items.
  - If not item.s\_warehouse.
    - Continue with the next iteration or loop test.
  - Set key from (item.original\_item or item.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.original\_item → item.item\_code.
  - If key does not belong to pending\_by\_item.
    - Continue with the next iteration or loop test.
  - Set transfer\_by\_item at key from (transfer\_by\_item.get(key, 0.0) + (flt(item.qty) × flt((item.conversion\_factor or 1)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
  - Evaluate first\_row\_by\_item.setdefault(key, item).
- For each tuple(key, transfer\_qty) in transfer\_by\_item.items().
  - Set item from first\_row\_by\_item at key.
  - Set precision from item.precision(“transfer\_qty”).
  - Set transfer\_qty from flt(transfer\_qty, precision).
  - Set pending\_qty from max(0.0, flt(pending\_by\_item at key, precision)).
  - If transfer\_qty &gt; pending\_qty.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot transfer {1} {2} of Item {3}. Maximum transferable quantity is {4} {2}.”.format(item.idx, transfer\_qty, item.stock\_uom, Platform.bold(item.item\_code), …), title  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L763)

<a id="op-bd756663901f2e"></a>
### Stock Entry.validate same source target warehouse during material transfer

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_validate_same_source_target_warehouse_during_material_transfer`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Source and Target Warehouse cannot be the same for Material Transfer”.format(item.idx) · validation helper — translated “Row #{0}: Source, Target Warehouse and Inventory Dimensions cannot be the exact same for Material Transfer”.format(item.idx).

**Local steps**

- If Platform.get\_single\_value(“Stock Settings”, “validate\_material\_transfer\_warehouses”).
  - Bind dependencies get\_inventory\_dimensions.
  - Set inventory\_dimensions from get\_inventory\_dimensions().
  - If self.purpose equals “Material Transfer”.
    - For each item in self.items.
      - If cstr(item.s\_warehouse) equals cstr(item.t\_warehouse).
        - If not inventory\_dimensions.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Source and Target Warehouse cannot be the same for Material Transfer”.format(item.idx), title = translated “Invalid Source and Target Warehouse”).
        - Otherwise.
          - Set difference\_found from false.
          - For each dimension in inventory\_dimensions.
            - Set fieldname from dimension.source\_fieldname when dimension.source\_fieldname.startswith(“to\_”), otherwise formatted text to\_{dimension.source\_fieldname}.
              - Value choice on dimension.source\_fieldname.startswith(“to\_”) — true gives dimension.source\_fieldname, false gives formatted text to\_{dimension.source\_fieldname}.
            - If (item.get(dimension.source\_fieldname) and item.get(fieldname) and item.get(dimension.source\_fieldname) differs from item.get(fieldname)).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(dimension.source\_fieldname) → item.get(fieldname) → item.get(dimension.source\_fieldname) differs from item.get(fieldname).
              - Set difference\_found from true.
              - Leave the innermost loop without its normal-exhaustion alternative.
          - If not difference\_found.
            - Call the validation error handler Platform.throw(translated “Row #{0}: Source, Target Warehouse and Inventory Dimensions cannot be the exact same for Material Transfer”.format(item.idx), title = translated “Invalid Source and Target Warehouse”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “validate\_material\_transfer\_warehouses”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L773)

<a id="op-0f1af63002b908"></a>
### Stock Entry.get matched items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_matched_items`

**Inputs** self, item\_code.

**Explicit results** list of row for row drawn from (items or self.get\_consumed\_items()) where (row.original\_item or row.item\_code) equals item\_code.

**Local steps**

- Set items from list of item for item drawn from self.items where item.s\_warehouse.
  - Draw item from self.items, keep a combination only if (item.s\_warehouse).
- Return list of row for row drawn from (items or self.get\_consumed\_items()) where (row.original\_item or row.item\_code) equals item\_code.
  - Draw row from (items or self.get\_consumed\_items()), keep a combination only if ((row.original\_item or row.item\_code) equals item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items → self.get\_consumed\_items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.original\_item → row.item\_code.

**Methods declared on this owner** [get consumed items](operations-079.md#op-c1bcef5e683c3a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L703)

<a id="op-c1bcef5e683c3a"></a>
### Stock Entry.get consumed items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_consumed_items`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent from Platform.qb.DocType(“Stock Entry”).
- Set child from Platform.qb.DocType(“Stock Entry Detail”).
- Set query from nested operand in the contract(nested operand in the contract).select(child.item\_code, nested operand in the contract.as\_(“qty”), nested operand in the contract.as\_(“transfer\_qty”), child.original\_item).wh ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L695)

<a id="op-f7b32eea3e3f8a"></a>
### Stock Entry.get stock and rate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_stock_and_rate`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_source\_documents\_permission().
- Evaluate self.set\_work\_order\_details().
- If self.bom\_no.
  - Evaluate Enterprise.require\_permission(“BOM”, self.bom\_no).
- Evaluate self.set\_transfer\_qty().
- Evaluate self.set\_actual\_qty().
- Evaluate self.calculate\_rate\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check source documents permission](operations-082.md#op-ebf7496fe05123), [set work order details](operations-082.md#op-759b32c5cade62), [set transfer qty](operations-077.md#op-90c3ce21ce82a9), [set actual qty](operations-079.md#op-eef6d1415cea78), [calculate rate and amount](operations-079.md#op-e089b5c80e72bd).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L791)

<a id="op-e089b5c80e72bd"></a>
### Stock Entry.calculate rate and amount

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_calculate_rate_and_amount`

**Inputs** self, reset\_outgoing\_rate = true, raise\_error\_if\_no\_rate = true.

**Local steps**

- Evaluate self.set\_basic\_rate(reset\_outgoing\_rate, raise\_error\_if\_no\_rate).
- Evaluate init\_landed\_taxes\_and\_totals(self).
- Evaluate self.distribute\_additional\_costs().
- Evaluate self.update\_valuation\_rate().
- Evaluate self.set\_total\_incoming\_outgoing\_value().
- Evaluate self.set\_total\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set basic rate](operations-079.md#op-c7faca0e1a48eb), [distribute additional costs](operations-080.md#op-84acc38a3d574d), [update valuation rate](operations-080.md#op-542e0c6e5e1320), [set total incoming outgoing value](operations-080.md#op-3306fd55966436), [set total amount](operations-080.md#op-14b64f1a9b0c9b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0835.json#L6221) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L769)

<a id="op-c7faca0e1a48eb"></a>
### Stock Entry.set basic rate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_basic_rate`

**Inputs** self, reset\_outgoing\_rate = true, raise\_error\_if\_no\_rate = true.

**Record and data access** read “BOM Secondary Item” via get\_value.

**State and service calls** msgprint with message.

**Local steps**

- Set outgoing\_items\_cost from self.set\_rate\_for\_outgoing\_items(reset\_outgoing\_rate, raise\_error\_if\_no\_rate).
- Set has\_consumption\_basis from self.has\_consumption\_basis().
- Set bom\_cost\_allocation\_per from self.get\_finished\_good\_cost\_allocation\_per() when self.bom\_no, otherwise no value.
  - Value choice on self.bom\_no — true gives self.get\_finished\_good\_cost\_allocation\_per(), false gives no value.
- Set secondary\_items\_cost\_basis from self.get\_secondary\_items\_cost\_basis(outgoing\_items\_cost).
- Set items from list().
- Set finished\_items\_last from sorted(self.get(“items”), key = deferred anonymous expression).
- For each d in finished\_items\_last.
  - If (d.s\_warehouse or d.set\_basic\_rate\_manually).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.s\_warehouse → d.set\_basic\_rate\_manually.
    - If d.set\_basic\_rate\_manually.
      - Set d.basic\_amount from flt((flt(d.transfer\_qty) × flt(d.basic\_rate)), d.precision(“basic\_amount”)).
    - Continue with the next iteration or loop test.
  - If (d.secondary\_item\_type and flt(d.transfer\_qty) equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.secondary\_item\_type → flt(d.transfer\_qty) equals 0.
    - Set d.basic\_rate from 0.0.
    - Set d.basic\_amount from 0.0.
    - Continue with the next iteration or loop test.
  - Set has\_derived\_rate from false.
  - If (d.allow\_zero\_valuation\_rate and (d.basic\_rate or d.is\_finished\_item) and self.purpose differs from “Receive from Customer”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allow\_zero\_valuation\_rate → (d.basic\_rate or d.is\_finished\_item) → self.purpose differs from “Receive from Customer”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.basic\_rate → d.is\_finished\_item.
    - If d.basic\_rate.
      - Evaluate items.append(d.item\_code).
    - Set d.basic\_rate from 0.0.
  - Otherwise.
    - If d.is\_finished\_item.
      - If self.purpose equals “Manufacture”.
        - Set d.basic\_rate from self.get\_basic\_rate\_for\_manufactured\_item(self.get\_finished\_items\_qty(), outgoing\_items\_cost, has\_consumption\_basis).
        - Set has\_derived\_rate from (has\_consumption\_basis or self.has\_manually\_rated\_finished\_items()).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_consumption\_basis → self.has\_manually\_rated\_finished\_items().
      - Otherwise.
        - If self.purpose equals “Repack”.
          - Set d.basic\_rate from self.get\_basic\_rate\_for\_repacked\_items(self.get\_finished\_items\_qty(), outgoing\_items\_cost).
          - Set has\_derived\_rate from any(generator of item.s\_warehouse for item drawn from self.get(“items”)).
            - Draw item from self.get(“items”).
      - If self.bom\_no.
        - Update d.basic\_rate using × (bom\_cost\_allocation\_per ÷ 100).
    - Otherwise.
      - If is\_costed\_out\_of\_finished\_item(d).
        - Set d.basic\_rate from self.get\_row\_valuation\_rate(d, raise\_error\_if\_no\_rate).
        - Set has\_derived\_rate from true.
      - Otherwise.
        - If (d.secondary\_item\_type and d.bom\_secondary\_item).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.secondary\_item\_type → d.bom\_secondary\_item.
          - Set cost\_allocation\_per from flt(Platform.get\_value(“BOM Secondary Item”, d.bom\_secondary\_item, “cost\_allocation\_per”)).
          - If flt(d.transfer\_qty).
            - Set secondary\_items\_qty from sum(generator of flt(item.transfer\_qty) for item drawn from self.items where (item.bom\_secondary\_item equals d.bom\_secondary\_item and not item.s\_warehouse and not item.set\_basic\_rate\_manually and not is\_costed …).
              - Draw item from self.items, keep a combination only if ((item.bom\_secondary\_item equals d.bom\_secondary\_item and not item.s\_warehouse and not item.set\_basic\_rate\_manually and not is\_costed\_out\_of\_finished\_item(item))).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.bom\_secondary\_item equals d.bom\_secondary\_item → not item.s\_warehouse → not item.set\_basic\_rate\_manually → not is\_costed\_out\_of\_finished\_item(item).
            - Set allocation\_basis from (secondary\_items\_cost\_basis − self.get\_costed\_out\_items\_cost()).
            - Set d.basic\_rate from ((allocation\_basis × (cost\_allocation\_per ÷ 100)) ÷ secondary\_items\_qty).
            - Set has\_derived\_rate from true.
  - If (not d.basic\_rate and not d.allow\_zero\_valuation\_rate and not has\_derived\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.basic\_rate → not d.allow\_zero\_valuation\_rate → not has\_derived\_rate.
    - If self.is\_new().
      - Set raise\_error\_if\_no\_rate from false.
    - Set d.basic\_rate from self.get\_row\_valuation\_rate(d, raise\_error\_if\_no\_rate).
  - Set d.basic\_rate from flt(d.basic\_rate).
  - Set d.basic\_amount from flt((flt(d.transfer\_qty) × flt(d.basic\_rate)), d.precision(“basic\_amount”)).
- If items.
  - Set message from empty text.
  - If len(items) &gt; 1.
    - Set message from translated “Items rate has been updated to zero as Allow Zero Valuation Rate is checked for the following items: {0}”.format(“, ”.join(generator of Platform.bold(item) for item drawn from items)).
      - Draw item from items.
  - Otherwise.
    - Set message from translated “Item rate has been updated to zero as Allow Zero Valuation Rate is checked for item {0}”.format(Platform.bold(items at 0)).
  - Evaluate Platform.msgprint(message, alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set rate for outgoing items](operations-079.md#op-a0c702d12aac68), [has consumption basis](operations-079.md#op-2d8ba921a7d94f), [get finished good cost allocation per](operations-079.md#op-82ec70df5eeedf), [get secondary items cost basis](operations-080.md#op-79f62850e78ea4), [get basic rate for manufactured item](operations-080.md#op-93ae4681686091), [get finished items qty](operations-079.md#op-3cb390ac4bafc8), [has manually rated finished items](operations-079.md#op-75d61bbf643dac), [get basic rate for repacked items](operations-079.md#op-980a4bedfa6b73), [get row valuation rate](operations-079.md#op-137be9d4d4a590), [get costed out items cost](operations-080.md#op-9075245b5da830).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L806)

<a id="op-137be9d4d4a590"></a>
### Stock Entry.get row valuation rate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_row_valuation_rate`

**Inputs** self, d, raise\_error\_if\_no\_rate.

**Explicit results** get\_valuation\_rate(d.item\_code, d.t\_warehouse, self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company, raise\_error\_if\_no\_rate = raise\_error\_if\_no\_rate, ba ….

**Local steps**

- Return get\_valuation\_rate(d.item\_code, d.t\_warehouse, self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company, raise\_error\_if\_no\_rate = raise\_error\_if\_no\_rate, ba ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L789)

<a id="op-5a431860498fef"></a>
### Stock Entry.first sle creation

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_first_sle_creation`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_no” → self.name, “voucher\_type” → self.doctype, “is\_cancelled” → 0), “creation”, order\_by = “creation asc”).

**Local steps**

- Return Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_no” → self.name, “voucher\_type” → self.doctype, “is\_cancelled” → 0), “creation”, order\_by = “creation asc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L685)

<a id="op-2d8ba921a7d94f"></a>
### Stock Entry.has consumption basis

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_has_consumption_basis`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · self.is\_rm\_cost\_from\_consumption\_entries().

**Local steps**

- If any(generator of d.s\_warehouse for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
  - Return true.
- Return self.is\_rm\_cost\_from\_consumption\_entries().

**Methods declared on this owner** [is rm cost from consumption entries](operations-079.md#op-fccb636dfc2be8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L794)

<a id="op-fccb636dfc2be8"></a>
### Stock Entry.is rm cost from consumption entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_is_rm_cost_from_consumption_entries`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Manufacturing Settings” via get\_single.

**Explicit results** bool(self.get\_consumption\_entries()) · false.

**Local steps**

- Set settings from Platform.get\_single(“Manufacturing Settings”).
- If (settings.material\_consumption and settings.get\_rm\_cost\_from\_consumption\_entry and self.work\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.material\_consumption → settings.get\_rm\_cost\_from\_consumption\_entry → self.work\_order.
  - Return bool(self.get\_consumption\_entries()).
- Return false.

**Methods declared on this owner** [get consumption entries](operations-079.md#op-0e40d62c0f4c78).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L723)

<a id="op-0e40d62c0f4c78"></a>
### Stock Entry.get consumption entries

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_consumption_entries`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Stock Entry” via get\_all.

**Explicit results** self.\_consumption\_entries.

**Local steps**

- If getattr(self, “\_consumption\_entries”, no value) is identical to no value.
  - Set self.\_consumption\_entries from Platform.get\_all(“Stock Entry”, filters = mapping(“docstatus” → 1, “work\_order” → self.work\_order, “purpose” → “Material Consumption for Manufacture”), pluck = “name”).
- Return self.\_consumption\_entries.

**Values supplied outside this operation** selected callable from getattr(self, “\_consumption\_entries”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L448) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L780)

<a id="op-a0c702d12aac68"></a>
### Stock Entry.set rate for outgoing items

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_set_rate_for_outgoing_items`

**Inputs** self, reset\_outgoing\_rate = true, raise\_error\_if\_no\_rate = true.

**Explicit results** outgoing\_items\_cost.

**Local steps**

- Set outgoing\_items\_cost from 0.0.
- For each d in self.get(“items”).
  - If d.s\_warehouse.
    - If reset\_outgoing\_rate.
      - Set args from self.get\_args\_for\_incoming\_rate(d).
      - Set rate from \_get\_incoming\_rate(args, raise\_error\_if\_no\_rate).
      - If rate ≥ 0.
        - Set d.basic\_rate from rate.
    - Set d.basic\_amount from flt((flt(d.transfer\_qty) × flt(d.basic\_rate)), d.precision(“basic\_amount”)).
    - If not d.t\_warehouse.
      - Update outgoing\_items\_cost using + flt(d.basic\_amount).
- Return outgoing\_items\_cost.

**Methods declared on this owner** [get args for incoming rate](operations-079.md#op-40e0c9b3b9dd04).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L812)

<a id="op-40e0c9b3b9dd04"></a>
### Stock Entry.get args for incoming rate

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_arguments_for_incoming_rate`

**Inputs** self, item.

**Explicit results** Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → (item.s\_warehouse or item.t\_warehouse), “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).

**Local steps**

- Return Platform.\_dict(mapping(“item\_code” → item.item\_code, “warehouse” → (item.s\_warehouse or item.t\_warehouse), “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.s\_warehouse → item.t\_warehouse.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item.s\_warehouse and (negative 1 × flt(item.transfer\_qty))) → flt(item.transfer\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.s\_warehouse → (negative 1 × flt(item.transfer\_qty)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0836.json#L2458) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L776)

<a id="op-3cb390ac4bafc8"></a>
### Stock Entry.get finished items qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_finished_items_qty`

**Inputs** self.

**Declared result** float.

**Explicit results** sum(generator of flt(d.transfer\_qty) for d drawn from self.get(“items”) where (d.is\_finished\_item and d.t\_warehouse and not d.s\_warehouse and not d.set\_basic\_rate\_manually and not d.allow\_zero\_valuation\_rate)).

**Local steps**

- Return sum(generator of flt(d.transfer\_qty) for d drawn from self.get(“items”) where (d.is\_finished\_item and d.t\_warehouse and not d.s\_warehouse and not d.set\_basic\_rate\_manually and not d.allow\_zero\_valuation\_rate)).
  - Draw d from self.get(“items”), keep a combination only if ((d.is\_finished\_item and d.t\_warehouse and not d.s\_warehouse and not d.set\_basic\_rate\_manually and not d.allow\_zero\_valuation\_rate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_finished\_item → d.t\_warehouse → not d.s\_warehouse → not d.set\_basic\_rate\_manually → not d.allow\_zero\_valuation\_rate.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L698)

<a id="op-75d61bbf643dac"></a>
### Stock Entry.has manually rated finished items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_has_manually_rated_finished_items`

**Inputs** self.

**Declared result** bool.

**Explicit results** self.get\_manually\_rated\_finished\_items() at 1 &gt; 0.

**Local steps**

- Return self.get\_manually\_rated\_finished\_items() at 1 &gt; 0.

**Methods declared on this owner** [get manually rated finished items](operations-079.md#op-d0e6e888b86d29).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L721)

<a id="op-d0e6e888b86d29"></a>
### Stock Entry.get manually rated finished items

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_manually_rated_finished_items`

**Inputs** self.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(sum(generator of flt(d.transfer\_qty) for d drawn from rows), sum(generator of (flt(d.transfer\_qty) × flt(d.basic\_rate)) for d drawn from rows)).

**Local steps**

- Set rows from list of d for d drawn from self.get(“items”) where (d.is\_finished\_item and d.t\_warehouse and not d.s\_warehouse and d.set\_basic\_rate\_manually).
  - Draw d from self.get(“items”), keep a combination only if ((d.is\_finished\_item and d.t\_warehouse and not d.s\_warehouse and d.set\_basic\_rate\_manually)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_finished\_item → d.t\_warehouse → not d.s\_warehouse → d.set\_basic\_rate\_manually.
- Return tuple(sum(generator of flt(d.transfer\_qty) for d drawn from rows), sum(generator of (flt(d.transfer\_qty) × flt(d.basic\_rate)) for d drawn from rows)).
  - Draw d from rows.
  - Draw d from rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L702)

<a id="op-82ec70df5eeedf"></a>
### Stock Entry.get finished good cost allocation per

`operation_enterprise_binding_enterprise_stock_doctype_stock_entry_stock_entry_stockentry_get_finished_good_cost_allocation_per`

**Inputs** self.

**Declared result** float.

**Record and data access** read “BOM Secondary Item” via get\_all.

**Explicit results** 100.0 · flt((100 − sum(generator of flt(per) for per drawn from allocated\_per))).

**Local steps**

- Set secondary\_rows from set of d.bom\_secondary\_item for d drawn from self.get(“items”) where (d.bom\_secondary\_item and flt(d.transfer\_qty)).
  - Draw d from self.get(“items”), keep a combination only if ((d.bom\_secondary\_item and flt(d.transfer\_qty))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.bom\_secondary\_item → flt(d.transfer\_qty).
- If not secondary\_rows.
  - Return 100.0.
- Set allocated\_per from Platform.get\_all(“BOM Secondary Item”, filters = mapping(“name” → tuple(“in”, list(secondary\_rows)), “parent” → self.bom\_no), pluck = “cost\_allocation\_per”).
- Return flt((100 − sum(generator of flt(per) for per drawn from allocated\_per))).
  - Draw per from allocated\_per.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0023.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L697)

<a id="op-980a4bedfa6b73"></a>
### Stock Entry.get basic rate for repacked items

`operation_enterprise_stock_record_definitions_stock_entry_business_behavior_stock_entry_get_basic_rate_for_repacked_items`

**Inputs** self, finished\_item\_qty, outgoing\_items\_cost.

**Explicit results** flt((cost\_left ÷ finished\_item\_qty)) when finished\_item\_qty, otherwise 0.0.

**Local steps**

- Set manual\_cost from self.get\_manually\_rated\_finished\_items() at 1.
- Set cost\_left from ((outgoing\_items\_cost − self.get\_costed\_out\_items\_cost()) − manual\_cost).
- If self.flags.via\_repost.
  - Set cost\_left from max(cost\_left, 0).
- Return flt((cost\_left ÷ finished\_item\_qty)) when finished\_item\_qty, otherwise 0.0.
  - Value choice on finished\_item\_qty — true gives flt((cost\_left ÷ finished\_item\_qty)), false gives 0.0.

**Methods declared on this owner** [get manually rated finished items](operations-079.md#op-d0e6e888b86d29), [get costed out items cost](operations-080.md#op-9075245b5da830).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L778)
