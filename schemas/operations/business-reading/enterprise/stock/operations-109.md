# Inventory and warehouses · operations 109

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Valuation adjustment

<a id="op-76638edecf6507"></a>
### Adjustment Entry.validate result

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_validate_result`

**Inputs** self, item\_code, warehouse, rows.

**Declared result** no value.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit failure paths** validation helper — translated “After the adjustment, Item {0} in Warehouse {1} would hold a qty of {2} worth {3}, instead of {4} worth {5}.”.format(bold(item\_code), bold(warehouse), flt(balance.qty\_after\_transaction), flt(ba ….

**Local steps**

- Set balance from (Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → self.doc.doctype, “voucher\_no” → self.doc.name, “item\_code” → item\_code, “warehouse” → warehouse, …), list(“qty\_after\_transaction”, “st ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → self.doc.doctype, “voucher\_no” → self.doc.name, “item\_code” → item\_code, “warehouse” → warehouse, …), list(“qty\_after\_transaction”, “sto … → Platform.\_dict().
- Set qty from sum(generator of flt(row.qty) for row drawn from rows).
  - Draw row from rows.
- Set value from sum(generator of flt(row.amount) for row drawn from rows).
  - Draw row from rows.
- Set allowance from (0.01 × (len(rows) + 1)).
- If (abs((flt(balance.qty\_after\_transaction) − qty)) &gt; 1e-06 or abs((flt(balance.stock\_value) − value)) &gt; allowance).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs((flt(balance.qty\_after\_transaction) − qty)) &gt; 1e-06 → abs((flt(balance.stock\_value) − value)) &gt; allowance.
  - Call the validation error handler Platform.throw(translated “After the adjustment, Item {0} in Warehouse {1} would hold a qty of {2} worth {3}, instead of {4} worth {5}.”.format(bold(item\_code), bold(warehouse), flt(balance.qty\_after\_trans ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1153)

<a id="op-29751d46c23d13"></a>
### Adjustment Entry.cancel

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_cancel`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Local steps**

- Set entries from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → self.doc.doctype, “voucher\_no” → self.doc.name, “is\_cancelled” → 0), fields = list(“item\_code”, “warehouse”, “posting\_date”, “posti ….
- Set sl\_entries from list of Platform.\_dict(entry, doctype = “Stock Ledger Entry”, voucher\_type = self.doc.doctype, voucher\_no = self.doc.name, company = self.doc.company, …) for entry drawn from entries.
  - Draw entry from entries.
- Evaluate sl\_entries.reverse().
- If sl\_entries.
  - Evaluate self.doc.make\_sl\_entries(sl\_entries, allow\_negative\_stock = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1139)

<a id="op-70032ed0bf8f05"></a>
### Adjustment Entry.set difference amount from ledger

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_set_difference_amount_from_ledger`

**Inputs** self.

**Declared result** no value.

**State and service calls** call db\_set on self.doc.

**Local steps**

- Set ledger from Platform.qb.DocType(“Stock Ledger Entry”).
- Set difference from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
- Evaluate self.doc.db\_set(“difference\_amount”, flt(difference, self.doc.precision(“difference\_amount”)), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1149)

<a id="op-4e35e843382786"></a>
### Is adjustment voucher

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_is_adjustment_voucher`

**Inputs** voucher\_type, voucher\_no.

**Declared result** bool.

**Record and data access** read “Stock Reconciliation” via get\_cached\_value.

**Explicit results** bool((voucher\_type equals “Stock Reconciliation” and voucher\_no and Platform.get\_cached\_value(“Stock Reconciliation”, voucher\_no, “purpose”) equals ADJUSTMENT\_ENTRY)).

**Local steps**

- Return bool((voucher\_type equals “Stock Reconciliation” and voucher\_no and Platform.get\_cached\_value(“Stock Reconciliation”, voucher\_no, “purpose”) equals ADJUSTMENT\_ENTRY)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type equals “Stock Reconciliation” → voucher\_no → Platform.get\_cached\_value(“Stock Reconciliation”, voucher\_no, “purpose”) equals ADJUSTMENT\_ENTRY.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Reconciliation”, voucher\_no, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1169)

<a id="op-49366ee20e1e17"></a>
### Adjustment Netting.initialize

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentnetting_init`

**Inputs** self, by\_lot = false.

**Record and data access** read “Stock Reconciliation” via get\_all.

**Local steps**

- Set self.vouchers from set(Platform.get\_all(“Stock Reconciliation”, filters = mapping(“purpose” → ADJUSTMENT\_ENTRY, “docstatus” → tuple(“!=”, 0)), pluck = “name”)).
- Set self.lot\_changes from get\_adjustment\_lot\_changes(self.vouchers) when (by\_lot and self.vouchers), otherwise mapping().
  - Value choice on (by\_lot and self.vouchers) — true gives get\_adjustment\_lot\_changes(self.vouchers), false gives mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in by\_lot → self.vouchers.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1154)

<a id="op-8338bc8780a82f"></a>
### Adjustment Netting.is adjustment

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentnetting_is_adjustment`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** bool((entry.get(“is\_adjustment\_entry”) and entry.get(“voucher\_type”) equals “Stock Reconciliation” and entry.get(“voucher\_no”) belongs to self.vouchers)).

**Local steps**

- Return bool((entry.get(“is\_adjustment\_entry”) and entry.get(“voucher\_type”) equals “Stock Reconciliation” and entry.get(“voucher\_no”) belongs to self.vouchers)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.get(“is\_adjustment\_entry”) → entry.get(“voucher\_type”) equals “Stock Reconciliation” → entry.get(“voucher\_no”) belongs to self.vouchers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1155)

<a id="op-0f76c0308c4355"></a>
### Adjustment Netting.net

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentnetting_net`

**Inputs** self, entries, key\_fields = tuple(“item\_code”, “warehouse”).

**Local steps**

- Set merged from no value.
- Set merged\_key from no value.
- For each entry in entries.
  - Set key from no value.
  - If self.is\_adjustment(entry).
    - Set key from tuple(entry.voucher\_no, expanded generator of entry.get(fieldname) for fieldname drawn from key\_fields).
      - Draw fieldname from key\_fields.
  - If (merged is distinct from no value and key equals merged\_key).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in merged is distinct from no value → key equals merged\_key.
    - For each fieldname in tuple(“actual\_qty”, “stock\_value\_difference”).
      - If fieldname belongs to entry.
        - Set merged at fieldname from (flt(merged.get(fieldname)) + flt(entry.get(fieldname))).
    - For each fieldname in tuple(“qty\_after\_transaction”, “stock\_value”, “valuation\_rate”).
      - If fieldname belongs to entry.
        - Set merged at fieldname from entry.get(fieldname).
    - Continue with the next iteration or loop test.
  - If merged is distinct from no value.
    - yield merged.
    - Set merged, merged\_key from no value.
  - If key is identical to no value.
    - yield entry.
  - Otherwise.
    - Set tuple(merged, merged\_key) from tuple(Platform.\_dict(entry), key).
- If merged is distinct from no value.
  - yield merged.

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [is adjustment](operations-109.md#op-8338bc8780a82f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1156)

<a id="op-38b9edae9d8ee4"></a>
### Adjustment Netting.net by lot

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentnetting_net_by_lot`

**Inputs** self, entries, item\_field = “item\_code”.

**Local steps**

- For each entry in self.net(entries, key\_fields = tuple(item\_field, “warehouse”)).
  - Set changes from self.lot\_changes.get(tuple(entry.voucher\_no, entry.get(item\_field), entry.warehouse)) when self.is\_adjustment(entry), otherwise no value.
    - Value choice on self.is\_adjustment(entry) — true gives self.lot\_changes.get(tuple(entry.voucher\_no, entry.get(item\_field), entry.warehouse)), false gives no value.
  - If changes.
    - yield values from split\_by\_lot(entry, changes).
  - Otherwise.
    - yield entry.

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [net](operations-109.md#op-0f76c0308c4355), [is adjustment](operations-109.md#op-8338bc8780a82f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1157)

<a id="op-fe83ae0e878bdf"></a>
### Get adjustment lot changes

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_adjustment_lot_changes`

**Inputs** vouchers.

**Declared result** dict at tuple(tuple at tuple(str, str, str), dict).

**Explicit results** changes.

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set changes from mapping().
- For each vouchers\_to\_read in create\_batch(list(vouchers), 1000).
  - For each row in nested operand in the contract(nested operand in the contract).select(bundle.voucher\_no, bundle.item\_code, bundle.warehouse, entry.serial\_no, …).where((((nested operand in the contract equals nested operan ….
    - Set lots from changes.setdefault(tuple(row.voucher\_no, row.item\_code, row.warehouse), mapping(“serial\_no” → mapping(), “batch\_no” → mapping())).
    - Set fieldname from “serial\_no” when row.serial\_no, otherwise “batch\_no”.
      - Value choice on row.serial\_no — true gives “serial\_no”, false gives “batch\_no”.
    - Set lot from lots at fieldname.setdefault((row.serial\_no or row.batch\_no), list(0.0, 0.0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
    - Update lot at 0 using + flt(row.qty).
    - Update lot at 1 using + flt(row.stock\_value\_difference).
- Return changes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1162)

<a id="op-1991590155ba34"></a>
### Split by lot

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_split_by_lot`

**Inputs** entry, changes.

**Local steps**

- Bind local operation lot\_entry for subsequent calls.
- Set lot\_qty, lot\_value from 0.0.
- For each leaving in tuple(true, false).
  - Set moved from mapping of serial\_no → change for tuple(serial\_no, change) drawn from changes at “serial\_no”.items() where (abs(change at 0) ≥ QTY\_NOISE and change at 0 &lt; 0 equals leaving).
    - Draw tuple(serial\_no, change) from changes at “serial\_no”.items(), keep a combination only if ((abs(change at 0) ≥ QTY\_NOISE and change at 0 &lt; 0 equals leaving)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in abs(change at 0) ≥ QTY\_NOISE → change at 0 &lt; 0 equals leaving.
  - If moved.
    - Set qty from sum(generator of change at 0 for change drawn from moved.values()).
      - Draw change from moved.values().
    - Set value from sum(generator of change at 1 for change drawn from moved.values()).
      - Draw change from moved.values().
    - Update lot\_qty using + qty.
    - Update lot\_value using + value.
    - yield lot\_entry(qty, value, serial\_no = whitespace '\\n'.join(sorted(moved))).
- For each tuple(batch\_no, tuple(qty, value)) in sorted(changes at “batch\_no”.items()).
  - If abs(qty) ≥ QTY\_NOISE.
    - Update lot\_qty using + qty.
    - Update lot\_value using + value.
    - yield lot\_entry(qty, value, batch\_no = batch\_no).
- If abs((flt(entry.actual\_qty) − lot\_qty)) ≥ QTY\_NOISE.
  - yield lot\_entry((flt(entry.actual\_qty) − lot\_qty), (flt(entry.stock\_value\_difference) − lot\_value)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1173)

<a id="op-0bb13ae99a14b8"></a>
### Split by lot.lot entry

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_split_by_lot_lot_entry`

**Inputs** qty, value, remaining named values lot.

**Explicit results** Platform.\_dict(entry, actual\_qty = qty, stock\_value\_difference = value, serial\_and\_batch\_bundle = no value, serial\_no = lot.get(“serial\_no”), …).

**Local steps**

- Return Platform.\_dict(entry, actual\_qty = qty, stock\_value\_difference = value, serial\_and\_batch\_bundle = no value, serial\_no = lot.get(“serial\_no”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1174)

<a id="op-4b1d60698d4a94"></a>
### Validate no later adjustment entry

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_validate_no_later_adjustment_entry`

**Inputs** sle.

**Declared result** no value.

**Record and data access** read “Stock Reconciliation” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with BackdatedEntryBeforeAdjustmentError — translated “Item {0} in Warehouse {1} was adjusted by {2} on {3}, so no stock transaction dated before it can be posted  …”.format(bold(sle.item\_code), bold(sle.warehouse), get\_link\_to\_form(“Stock Reconcil ….

**Local steps**

- If not Platform.db.exists(“Stock Reconciliation”, mapping(“purpose” → ADJUSTMENT\_ENTRY, “docstatus” → 1)).
  - Return no value.
- Set reconciliation from Platform.qb.DocType(“Stock Reconciliation”).
- Set ledger from Platform.qb.DocType(“Stock Ledger Entry”).
- Set of\_item from ledger.warehouse equals sle.warehouse.
- Set tuple(serial\_nos, batch\_nos) from get\_serial\_and\_batch\_nos(sle).
- If (serial\_nos or batch\_nos).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → batch\_nos.
  - Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
  - Set lot from entry.serial\_no.isin(serial\_nos) when serial\_nos, otherwise entry.batch\_no.isin(batch\_nos).
    - Value choice on serial\_nos — true gives entry.serial\_no.isin(serial\_nos), false gives entry.batch\_no.isin(batch\_nos).
  - If (serial\_nos and batch\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_nos → batch\_nos.
    - Set lot from (lot bitwise or entry.batch\_no.isin(batch\_nos)).
  - Set of\_item from (of\_item bitwise or ExistsCriterion(nested operand in the contract(nested operand in the contract).select(entry.name).where((entry.parent equals ledger.serial\_and\_batch\_bundle bitwise and lot)))).
- Set adjustment from nested operand in the contract(nested operand in the contract).orderby(ledger.posting\_datetime, order = nested operand in the contract.qb.desc).limit(1).run(as\_dict = true).
- If adjustment.
  - Call the validation error handler Platform.throw(translated “Item {0} in Warehouse {1} was adjusted by {2} on {3}, so no stock transaction dated before it can be posted  …”.format(bold(sle.item\_code), bold(sle.warehouse), get\_link\_to\_form( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1176)

<a id="op-74305eaa55e8fc"></a>
### Get serial and batch nos

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_serial_and_batch_nos`

**Inputs** sle.

**Declared result** tuple at tuple(list at str, list at str).

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** tuple(sorted(serial\_nos), sorted(batch\_nos)).

**Local steps**

- Set tuple(serial\_nos, batch\_nos) from tuple(set(), set()).
- If sle.serial\_and\_batch\_bundle.
  - For each entry in Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → sle.serial\_and\_batch\_bundle), fields = list(“serial\_no”, “batch\_no”)).
    - If entry.serial\_no.
      - Evaluate serial\_nos.add(entry.serial\_no).
    - If entry.batch\_no.
      - Evaluate batch\_nos.add(entry.batch\_no).
- If sle.serial\_no.
  - Evaluate serial\_nos.update(get\_serial\_nos(sle.serial\_no)).
- If sle.batch\_no.
  - Evaluate batch\_nos.add(sle.batch\_no).
- Return tuple(sorted(serial\_nos), sorted(batch\_nos)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1167)

<a id="op-8e01a991bd3090"></a>
### Get adjusted until

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_adjusted_until`

**Inputs** item\_warehouses, to\_date = no value.

**Declared result** dict at tuple(tuple at tuple(str, str), dict).

**Explicit results** mapping() · adjusted\_until.

**Local steps**

- If not item\_warehouses.
  - Return mapping().
- Set ledger from Platform.qb.DocType(“Stock Ledger Entry”).
- Set reconciliation from Platform.qb.DocType(“Stock Reconciliation”).
- Set query from nested operand in the contract(nested operand in the contract).select(ledger.item\_code, ledger.warehouse, ledger.voucher\_no, ledger.posting\_datetime).where((((nested operand in the contract equals nested o ….
  - Draw tuple(item\_code, \_warehouse) from item\_warehouses.
- If to\_date.
  - Set query from query.where(ledger.posting\_date ≤ to\_date).
- Set adjusted\_until from mapping().
- For each row in query.run(as\_dict = true).
  - Set adjusted\_until at tuple(row.item\_code, row.warehouse) from row.
- Return adjusted\_until.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1161)

## Record · Warehouse

[Record definition](../../../../data/record-types/warehouse.json)

<a id="op-077b89de98e702"></a>
### Warehouse.autoname

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If self.company.
  - Set suffix from (“ - ” + Platform.get\_cached\_value(“Company”, self.company, “abbr”)).
  - If not self.warehouse\_name.endswith(suffix).
    - Set self.name from (self.warehouse\_name + suffix).
    - Return no value.
- Set self.name from self.warehouse\_name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L1863) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L11)

<a id="op-6832f1953ae5e5"></a>
### Warehouse.onload

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_onload`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- If (self.company and cint(Platform.db.get\_value(“Company”, self.company, “enable\_perpetual\_inventory”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → cint(Platform.db.get\_value(“Company”, self.company, “enable\_perpetual\_inventory”)).
  - Set account from (self.account or get\_warehouse\_account(self, raise\_error = false)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.account → get\_warehouse\_account(self, raise\_error = false).
  - If account.
    - Evaluate self.set\_onload(“account”, account).
- Evaluate load\_address\_and\_contact(self).
- Evaluate self.set\_onload(“stock\_exists”, self.check\_if\_sle\_exists(non\_cancelled\_only = true)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if sle exists](operations-110.md#op-9b3e0b6b71a80c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L2061) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L19)

<a id="op-b325895f5fdca8"></a>
### Warehouse.validate

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_warehouse\_account().
- Evaluate self.validate\_inventory\_account().
- Evaluate self.validate\_group\_conversion().
- Evaluate self.validate\_company\_change().
- Evaluate self.validate\_parent\_warehouse().
- Evaluate self.validate\_disable\_with\_stock().
- Evaluate self.validate\_default\_in\_transit\_warehouse().
- Evaluate self.warn\_about\_multiple\_warehouse\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate warehouse account](operations-109.md#op-17e672bafea903), [validate inventory account](operations-109.md#op-18aeb54cc319a8), [validate group conversion](operations-109.md#op-1dac1e6fc74757), [validate company change](operations-109.md#op-47a3efb65964dd), [validate parent warehouse](operations-109.md#op-f6015165057e30), [validate disable with stock](operations-109.md#op-2a6a9ce7ca1ea6), [validate default in transit warehouse](operations-109.md#op-1f631f15840584), [warn about multiple warehouse account](operations-110.md#op-8438ede5d7a30c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L22)

<a id="op-1f631f15840584"></a>
### Warehouse.validate default in transit warehouse

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_default_in_transit_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.default\_in\_transit\_warehouse.
  - Return no value.
- Set transit from Platform.db.get\_value(“Warehouse”, self.default\_in\_transit\_warehouse, list(“warehouse\_type”, “is\_group”, “company”), as\_dict = true).
- If (transit.warehouse\_type differs from “Transit” or transit.is\_group or transit.company differs from self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in transit.warehouse\_type differs from “Transit” → transit.is\_group → transit.company differs from self.company.
  - Evaluate throw(translated “Default In-Transit Warehouse {0} must be a Transit ledger warehouse of Company {1}”.format(Platform.bold(self.default\_in\_transit\_warehouse), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L846)

<a id="op-2a6a9ce7ca1ea6"></a>
### Warehouse.validate disable with stock

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_disable_with_stock`

**Inputs** self.

**Record and data access** read “Bin” via get\_value.

**Explicit results** no value.

**Local steps**

- If (not self.disabled or self.is\_new() or not self.has\_value\_changed(“disabled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.disabled → self.is\_new() → not self.has\_value\_changed(“disabled”).
  - Return no value.
- If item\_code bound to Platform.db.get\_value(“Bin”, mapping(“warehouse” → self.name, “actual\_qty” → tuple(“!=”, 0)), “item\_code”).
  - Evaluate throw(translated “Warehouse {0} cannot be disabled as stock exists for Item {1}”.format(Platform.bold(self.name), Platform.bold(item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L847)

<a id="op-f6015165057e30"></a>
### Warehouse.validate parent warehouse

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_parent_warehouse`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.parent\_warehouse.
  - Return no value.
- Set parent from Platform.db.get\_value(“Warehouse”, self.parent\_warehouse, list(“is\_group”, “company”), as\_dict = true).
- If (not parent.is\_group or (parent.company and parent.company differs from self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent.is\_group → (parent.company and parent.company differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.company → parent.company differs from self.company.
  - Evaluate throw(translated “Parent Warehouse {0} must be a group warehouse of Company {1}”.format(Platform.bold(self.parent\_warehouse), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L849)

<a id="op-47a3efb65964dd"></a>
### Warehouse.validate company change

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_company_change`

**Inputs** self.

**Record and data access** read “Bin” via exists.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“company”).
  - Return no value.
- If (self.check\_if\_sle\_exists() or Platform.db.exists(“Bin”, mapping(“warehouse” → self.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.check\_if\_sle\_exists() → Platform.db.exists(“Bin”, mapping(“warehouse” → self.name)).
  - Evaluate throw(translated “Company cannot be changed for Warehouse {0} as it has stock transactions”.format(Platform.bold(self.name))).
- If self.check\_if\_child\_exists().
  - Evaluate throw(translated “Company cannot be changed for Warehouse {0} as it has child warehouses”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if sle exists](operations-110.md#op-9b3e0b6b71a80c), [check if child exists](operations-110.md#op-ff68794464e502).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L845)

<a id="op-1dac1e6fc74757"></a>
### Warehouse.validate group conversion

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_group_conversion`

**Inputs** self.

**Record and data access** read “Item Default” via exists.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“is\_group”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“is\_group”).
  - Return no value.
- If (self.is\_group and self.check\_if\_sle\_exists()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_group → self.check\_if\_sle\_exists().
  - Evaluate throw(translated “Warehouses with existing transaction can not be converted to group.”).
- If (self.is\_group and bin\_with\_qty bound to self.get\_bin\_with\_quantity()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_group → bin\_with\_qty bound to self.get\_bin\_with\_quantity().
  - Evaluate throw(translated “Warehouse {0} can not be converted to group as quantity exists for Item {1}”.format(self.name, bin\_with\_qty.item\_code)).
- If (self.is\_group and Platform.db.exists(“Item Default”, mapping(“default\_warehouse” → self.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_group → Platform.db.exists(“Item Default”, mapping(“default\_warehouse” → self.name)).
  - Evaluate throw(translated “Warehouse {0} can not be converted to group as it is an Item's default warehouse”.format(self.name)).
- If (not self.is\_group and self.check\_if\_child\_exists()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_group → self.check\_if\_child\_exists().
  - Evaluate throw(translated “Warehouses with child nodes cannot be converted to ledger”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if sle exists](operations-110.md#op-9b3e0b6b71a80c), [get bin with quantity](operations-110.md#op-b549dff773aaad), [check if child exists](operations-110.md#op-ff68794464e502).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L848)

<a id="op-17e672bafea903"></a>
### Warehouse.validate warehouse account

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_validate_warehouse_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Account {0} does not belong to Company {1}”.format(Platform.bold(self.account), Platform.bold(self.company)) · validation helper — translated “Account {0} must be a non-group account of type Stock”.format(Platform.bold(self.account)).

**Local steps**

- If not self.account.
  - Return no value.
- Set account from Platform.get\_cached\_value(“Account”, self.account, list(“company”, “account\_type”, “is\_group”), as\_dict = true).
- If (self.company and account.company and account.company differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → account.company → account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Account {0} does not belong to Company {1}”.format(Platform.bold(self.account), Platform.bold(self.company))).
- If (account.is\_group or account.account\_type differs from “Stock”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.is\_group → account.account\_type differs from “Stock”.
  - Call the validation error handler Platform.throw(translated “Account {0} must be a non-group account of type Stock”.format(Platform.bold(self.account))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, list(“company”, “account\_type”, “is\_group”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L850)

<a id="op-18aeb54cc319a8"></a>
### Warehouse.validate inventory account

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_validate_inventory_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Warehouse” via get\_value.

**Explicit results** no value.

**Local steps**

- If (not self.is\_new() or not self.company or self.flags.ignore\_inventory\_account\_validation or not Platform.get\_cached\_value(“Company”, self.company, “enable\_perpetual\_inventory”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_new() → not self.company → self.flags.ignore\_inventory\_account\_validation → not Platform.get\_cached\_value(“Company”, self.company, “enable\_perpetual\_inventory”).
  - Return no value.
- Set warehouse from Platform.\_dict(self.as\_dict()).
- If (not self.account and self.parent\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.account → self.parent\_warehouse.
  - Set parent\_bounds from Platform.db.get\_value(“Warehouse”, self.parent\_warehouse, list(“lft”, “rgt”), as\_dict = true).
  - If parent\_bounds.
    - Evaluate warehouse.update(parent\_bounds).
- Evaluate get\_warehouse\_account(warehouse).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “enable\_perpetual\_inventory”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L2409) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L23)
