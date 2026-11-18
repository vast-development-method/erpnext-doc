# Inventory and warehouses · operations 102

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reservation entry

[Record definition](../../../../data/record-types/stock_reservation_entry.json)

<a id="op-d6613b28622897"></a>
### Stock Reservation Entry.get row reserved qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_get_row_reserved_qty`

**Inputs** self.

**Declared result** float.

**Explicit results** flt(reserved\_qty at 0 at 0).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set reserved\_qty from nested operand in the contract(nested operand in the contract).select(Sum((nested operand in the contract − nested operand in the contract))).where(((((nested operand in the contract bitwise and nested ope ….run().
- Return flt(reserved\_qty at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L828)

<a id="op-1bdc347167bc81"></a>
### Stock Reservation Entry.consume serial batch for material transfer

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_consume_serial_batch_for_material_transfer`

**Inputs** self, row\_wise\_serial\_batch.

**State and service calls** call db\_update on entry.

**Local steps**

- For each entry in self.sb\_entries.
  - Set entry.delivered\_qty from 0.
- For each entry in self.sb\_entries.
  - For each row in row\_wise\_serial\_batch.
    - Set data from row\_wise\_serial\_batch at row.
    - If entry.serial\_no belongs to data.serial\_nos.
      - Set entry.delivered\_qty from flt(1).
      - Evaluate data.serial\_nos.remove(entry.serial\_no).
    - Otherwise.
      - If (not entry.serial\_no and entry.batch\_no belongs to data.batch\_nos).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.serial\_no → entry.batch\_no belongs to data.batch\_nos.
        - Set entry.delivered\_qty from min(flt(entry.qty), data.batch\_nos at entry.batch\_no).
        - Update data.batch\_nos at entry.batch\_no using − entry.delivered\_qty.
  - Evaluate entry.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1166)

<a id="op-47baf91d02ef64"></a>
### Stock Reservation Entry.matched serial batch qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_matched_serial_batch_qty`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** sum(generator of min(flt(entry.delivered\_qty), flt(entry.qty)) for entry drawn from self.sb\_entries).

**Local steps**

- Return sum(generator of min(flt(entry.delivered\_qty), flt(entry.qty)) for entry drawn from self.sb\_entries).
  - Draw entry from self.sb\_entries.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L833)

<a id="op-35dcdbe563b9ee"></a>
### Clear reserve stock if disabled

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_clear_reserve_stock_if_disabled`

**Inputs** doc.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Set doc.reserve\_stock from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L813)

<a id="op-9da1c1facc4795"></a>
### Validate stock reservation settings

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_validate_stock_reservation_settings`

**Inputs** voucher.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Set msg from translated “Please enable {0} in the {1}.”.format(Platform.bold(translated “Stock Reservation”), Platform.bold(translated “Stock Settings”)).
  - Call the validation error handler Platform.throw(msg).
- Set allowed\_voucher\_types from list(“Sales Order”).
- If voucher.doctype does not belong to allowed\_voucher\_types.
  - Set msg from translated “Stock Reservation can only be created against {0}.”.format(“, ”.join(allowed\_voucher\_types)).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0869.json#L5669) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1198)

<a id="op-3620ae8bbf491a"></a>
### Get available qty to reserve

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_available_quantity_to_reserve`

**Inputs** item\_code, warehouse, batch\_no = no value, ignore\_sre = no value.

**Declared result** float.

**Explicit results** get\_batch\_qty\_for\_stock(item\_code = item\_code, warehouse = warehouse, batch\_no = batch\_no, ignore\_voucher\_nos = list(ignore\_sre) when ignore\_sre, otherwise no value) · (available\_qty − reserved\_qty) · available\_qty.

**Local steps**

- If batch\_no.
  - Return get\_batch\_qty\_for\_stock(item\_code = item\_code, warehouse = warehouse, batch\_no = batch\_no, ignore\_voucher\_nos = list(ignore\_sre) when ignore\_sre, otherwise no value).
    - Value choice on ignore\_sre — true gives list(ignore\_sre), false gives no value.
- Set available\_qty from \_get\_stock\_balance(item\_code, warehouse).
- If available\_qty.
  - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
  - Set query from nested operand in the contract(nested operand in the contract).select(Sum((nested operand in the contract − nested operand in the contract))).where((((nested operand in the contract equals nested operand i …().
  - If ignore\_sre.
    - Set query from query.where(sre.name differs from ignore\_sre).
  - Set reserved\_qty from (query.run() at 0 at 0 or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.0.
  - If reserved\_qty.
    - Return (available\_qty − reserved\_qty).
- Return available\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1146)

<a id="op-3dd6d651238b13"></a>
### Get available serial nos to reserve

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_available_serial_numbers_to_reserve`

**Inputs** item\_code, warehouse, has\_batch\_no = false, ignore\_sre = no value.

**Declared result** list at tuple.

**Explicit results** list((set(available\_serial\_nos\_list) − set(reserved\_serial\_nos))) · available\_serial\_nos\_list.

**Local steps**

- Bind dependencies get\_available\_serial\_nos.
- Set available\_serial\_nos from get\_available\_serial\_nos(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “has\_batch\_no” → has\_batch\_no, “ignore\_voucher\_nos” → list(ignore\_sre)))).
- Set available\_serial\_nos\_list from list().
- If available\_serial\_nos.
  - Set available\_serial\_nos\_list from list of tuple(d.values()) for d drawn from available\_serial\_nos.
    - Draw d from available\_serial\_nos.
  - Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
  - Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
  - Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(sb\_entry.serial\_no, sre.warehouse).where((((((nest ….
  - If has\_batch\_no.
    - Set query from query.select(sb\_entry.batch\_no).
  - If ignore\_sre.
    - Set query from query.where(sre.name differs from ignore\_sre).
  - Set reserved\_serial\_nos from query.run().
  - If reserved\_serial\_nos.
    - Return list((set(available\_serial\_nos\_list) − set(reserved\_serial\_nos))).
- Return available\_serial\_nos\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1147)

<a id="op-0bccb23f2bd36c"></a>
### Get sre reserved qty for item and warehouse

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_quantity_for_item_and_warehouse`

**Inputs** item\_code, warehouse = no value.

**Declared result** float.

**Explicit results** flt(reserved\_qty at 0 at 0) when reserved\_qty, otherwise 0.0.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“reserved\_qty”)).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operan ….
- If warehouse.
  - Set query from query.where(sre.warehouse equals warehouse).
- Set reserved\_qty from query.run(as\_list = true).
- Return flt(reserved\_qty at 0 at 0) when reserved\_qty, otherwise 0.0.
  - Value choice on reserved\_qty — true gives flt(reserved\_qty at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L1730) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1155)

<a id="op-ae9270352fa1e7"></a>
### Get sre reserved qty for items and warehouses

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_quantity_for_items_and_warehouses`

**Inputs** item\_code\_list, warehouse\_list = no value.

**Declared result** dict.

**Explicit results** mapping() · mapping of tuple(d at “item\_code”, d at “warehouse”) → d at “reserved\_qty” for d drawn from data when data, otherwise mapping().

**Local steps**

- If not item\_code\_list.
  - Return mapping().
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sre.item\_code, sre.warehouse, nested operand in the contract.as\_(“reserved\_qty”)).where((((nested operand in the contract equals nested ….
- If warehouse\_list.
  - Set query from query.where(sre.warehouse.isin(warehouse\_list)).
- Set data from query.run(as\_dict = true).
- Return mapping of tuple(d at “item\_code”, d at “warehouse”) → d at “reserved\_qty” for d drawn from data when data, otherwise mapping().
  - Value choice on data — true gives mapping of tuple(d at “item\_code”, d at “warehouse”) → d at “reserved\_qty” for d drawn from data, false gives mapping().
  - Draw d from data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L2196) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1156)

<a id="op-61c23dc8624a0d"></a>
### Get sre reserved qty details for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_quantity_details_for_voucher`

**Inputs** voucher\_type, voucher\_no.

**Declared result** dict.

**Explicit results** Platform.\_dict(data).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set data from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Return Platform.\_dict(data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L2785) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1154)

<a id="op-02346fbfe8f1af"></a>
### Get sre reserved warehouses for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_warehouses_for_voucher`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no = no value.

**Declared result** list.

**Explicit results** list of d at 0 for d drawn from warehouses when warehouses, otherwise list().

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
- If voucher\_detail\_no.
  - Set query from query.where(sre.voucher\_detail\_no equals voucher\_detail\_no).
- Set warehouses from query.run(as\_list = true).
- Return list of d at 0 for d drawn from warehouses when warehouses, otherwise list().
  - Value choice on warehouses — true gives list of d at 0 for d drawn from warehouses, false gives list().
  - Draw d from warehouses.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1159)

<a id="op-c9937a79876fa2"></a>
### Get sre reserved qty for voucher detail no

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_quantity_for_voucher_detail_number`

**Inputs** item\_code, voucher\_type, voucher\_no, voucher\_detail\_no, ignore\_sre = no value, warehouse = no value, from\_voucher\_detail\_no = no value.

**Declared result** float.

**Explicit results** flt(reserved\_qty at 0 at 0).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract.qb.from\_(sre).select((((nested operand in the contract(nested operand in the contract) − nested operand in the contract(nested operand in the contract)) − Sum(nested operand  ….
- If ignore\_sre.
  - Set query from query.where(sre.name differs from ignore\_sre).
- If warehouse.
  - Set query from query.where(sre.warehouse equals warehouse).
- If from\_voucher\_detail\_no.
  - Set query from query.where(sre.from\_voucher\_detail\_no equals from\_voucher\_detail\_no).
- Set reserved\_qty from query.run(as\_list = true).
- Return flt(reserved\_qty at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L3620) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1157)

<a id="op-0e7ff88562d24d"></a>
### Get sre reserved serial nos details

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_serial_numbers_details`

**Inputs** item\_code, warehouse, serial\_nos = no value.

**Declared result** dict.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sb\_entry.serial\_no, sre.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested o ….
- If serial\_nos.
  - Set query from query.where(sb\_entry.serial\_no.isin(serial\_nos)).
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L4284) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1158)

<a id="op-f5d51fda571c40"></a>
### Get sre reserved serial nos for voucher detail nos

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_sre_reserved_serial_nos_for_voucher_detail_nos`

**Inputs** voucher\_type, voucher\_detail\_nos.

**Declared result** dict.

**Explicit results** reserved\_serial\_nos.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sre.voucher\_detail\_no, sb\_entry.serial\_no).distinct().where(((((nested operand in the contract.docstatus equals 1 bitwise and nested op ….
- Set reserved\_serial\_nos from mapping().
- For each tuple(voucher\_detail\_no, serial\_no) in query.run().
  - Evaluate reserved\_serial\_nos.setdefault(voucher\_detail\_no, set()).add(serial\_no).
- Return reserved\_serial\_nos.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L818)

<a id="op-374fcc596bd447"></a>
### Get sre reserved batch nos details

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_reserved_batch_numbers_details`

**Inputs** item\_code, warehouse, batch\_nos = no value.

**Declared result** dict.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- If batch\_nos.
  - Set query from query.where(sb\_entry.batch\_no.isin(batch\_nos)).
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1153)

<a id="op-b0542f68277910"></a>
### Get sre details for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_stock_reservation_entry_details_for_voucher`

**Inputs** voucher\_type, voucher\_no.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L5374) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1152)

<a id="op-705f775bbf87b8"></a>
### Get serial batch entries for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_serial_batch_entries_for_voucher`

**Inputs** sre\_names.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.qty &gt; nested operand in the contract.delivered\_qty).orderby(sb\_entry.creation).run(as\_dict = true).

**Local steps**

- If isinstance(sre\_names, str).
  - Set sre\_names from list(sre\_names).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.qty &gt; nested operand in the contract.delivered\_qty).orderby(sb\_entry.creation).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1148)

<a id="op-5d001b6cddf160"></a>
### Get ssb bundle for voucher

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_get_ssb_bundle_for_voucher`

**Inputs** sre\_list.

**Declared result** object.

**Record and data access** read “Stock Reservation Entry” via get\_cached\_value.

**State and service calls** request new\_doc for “Serial and Batch Bundle” · call save on bundle.

**Explicit results** bundle.

**Local steps**

- Set sb\_entries from get\_serial\_batch\_entries\_for\_voucher(list of sre.name for sre drawn from sre\_list).
  - Draw sre from sre\_list.
- If sb\_entries.
  - Set bundle from Platform.new\_doc(“Serial and Batch Bundle”).
  - Set bundle.type\_of\_transaction from “Outward”.
  - Set bundle.voucher\_type from “Delivery Note”.
  - Set bundle.posting\_date from nowdate().
  - Set bundle.posting\_time from nowtime().
  - For each field in tuple(“item\_code”, “warehouse”, “has\_serial\_no”, “has\_batch\_no”).
    - Evaluate setattr(bundle, field, sre\_list at 0 at field).
  - Set bundle.company from (sre\_list at 0.get(“company”) or Platform.get\_cached\_value(“Stock Reservation Entry”, sre\_list at 0 at “name”, “company”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sre\_list at 0.get(“company”) → Platform.get\_cached\_value(“Stock Reservation Entry”, sre\_list at 0 at “name”, “company”).
  - Evaluate round\_to\_ledger\_qty(sb\_entries).
  - For each sb\_entry in sb\_entries.
    - Evaluate bundle.append(“entries”, sb\_entry).
  - If Platform.flags.in\_test.
    - Set bundle.flags.ignore\_mandatory from true.
  - Evaluate bundle.save().
  - Return bundle.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_value(“Stock Reservation Entry”, sre\_list at 0 at “name”, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1149)

<a id="op-56fa00ea04f062"></a>
### Round to ledger qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_round_to_ledger_qty`

**Inputs** sb\_entries.

**Declared result** no value.

**Local steps**

- Set qty\_before\_last from sum(generator of flt(entry.qty) for entry drawn from sb\_entries at slice no value to negative 1).
  - Draw entry from sb\_entries at slice no value to negative 1.
- Set total from flt((qty\_before\_last + flt(sb\_entries at negative 1.qty)), Platform.get\_precision(“Serial and Batch Entry”, “qty”)).
- Set sb\_entries at negative 1.qty from (total − qty\_before\_last).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L822)

<a id="op-2eae1bdd08512b"></a>
### Get qty up to rounding

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_qty_up_to_rounding`

**Inputs** qty, full\_qty.

**Declared result** float.

**Explicit results** full\_qty when flt((full\_qty − qty), precision) equals 0, otherwise qty.

**Local steps**

- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- Return full\_qty when flt((full\_qty − qty), precision) equals 0, otherwise qty.
  - Value choice on flt((full\_qty − qty), precision) equals 0 — true gives full\_qty, false gives qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L816)

<a id="op-a41301e9384579"></a>
### Get qty to undeliver

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_qty_to_undeliver`

**Inputs** delivered\_qty, qty.

**Declared result** float.

**Explicit results** (delivered\_qty − flt((delivered\_qty − min(delivered\_qty, qty)), precision)).

**Local steps**

- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- Return (delivered\_qty − flt((delivered\_qty − min(delivered\_qty, qty)), precision)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L815)

<a id="op-fde0b7aaf9ef0d"></a>
### Get whole sales unit qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_whole_sales_unit_qty`

**Inputs** item, stock\_qty, max\_qty = no value.

**Declared result** float.

**Record and data access** read “UOM” via get\_cached\_value.

**Explicit results** stock\_qty · (floor(flt((flt(stock\_qty) ÷ conversion\_factor), 6)) × conversion\_factor).

**Local steps**

- Set conversion\_factor from (flt(item.get(“conversion\_factor”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.get(“conversion\_factor”)) → 1.
- If (conversion\_factor equals 1 or not Platform.get\_cached\_value(“UOM”, item.get(“uom”), “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conversion\_factor equals 1 → not Platform.get\_cached\_value(“UOM”, item.get(“uom”), “must\_be\_whole\_number”).
  - Return stock\_qty.
- If max\_qty is distinct from no value.
  - Set stock\_qty from min((ceil(flt((flt(stock\_qty) ÷ conversion\_factor), 6)) × conversion\_factor), max\_qty).
- Return (floor(flt((flt(stock\_qty) ÷ conversion\_factor), 6)) × conversion\_factor).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, item.get(“uom”), “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L820)

<a id="op-47179a096dd872"></a>
### Has reserved stock

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_has_reserved_stock`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no = no value.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If \_get\_stock\_reservation\_entries\_for\_voucher(voucher\_type, voucher\_no, voucher\_detail\_no, fields = list(“name”), ignore\_status = true).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L6666) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1160)

<a id="op-85db0f8df7198f"></a>
### Stock Reservation.initialize

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_initialize`

**Inputs** self, doc, items = no value, kwargs = no value.

**Record and data access** resolve a document from “Work Order” via get\_doc.

**Local steps**

- If isinstance(doc, str).
  - Set doc from parse\_json(doc).
  - Set doc from Platform.get\_doc(“Work Order”, doc.get(“name”)).
- Set self.doc from doc.
- Set self.items from items.
- Set self.kwargs from kwargs.
- Evaluate self.initialize\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize fields](operations-103.md#op-3ec41c7818bf49).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0870.json#L6816) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1190)
