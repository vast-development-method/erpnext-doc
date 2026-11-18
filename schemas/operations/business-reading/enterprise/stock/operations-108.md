# Inventory and warehouses · operations 108

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Valuation adjustment

<a id="op-ff4b2ebdbf7c39"></a>
### Adjustment Plan.qty

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentplan_qty`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** sum(generator of row.qty for row drawn from self.rows).

**Local steps**

- Return sum(generator of row.qty for row drawn from self.rows).
  - Draw row from self.rows.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1158)

<a id="op-ee62926e4ccb1a"></a>
### Adjustment Plan.value

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmentplan_value`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** sum(generator of (row.qty × row.valuation\_rate) for row drawn from self.rows).

**Local steps**

- Return sum(generator of (row.qty × row.valuation\_rate) for row drawn from self.rows).
  - Draw row from self.rows.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1159)

<a id="op-a549e98e0212f5"></a>
### Get adjustment plans

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_adjustment_plans`

**Inputs** item\_warehouses, posting\_datetime, exclude\_voucher\_no = no value.

**Declared result** dict at tuple(tuple at tuple(str, str), AdjustmentPlan).

**Explicit results** plans.

**Local steps**

- Set plans from mapping().
- For each tuple(item\_code, warehouse, stock, last\_entry, …) in iterate\_expected\_stock\_at(item\_warehouses, posting\_datetime, exclude\_voucher\_no).
  - Set plan from AdjustmentPlan(item\_code = item\_code, warehouse = warehouse, ledger\_qty = flt(last\_entry.qty\_after\_transaction), ledger\_value = flt(last\_entry.stock\_value)).
  - If (abs((plan.ledger\_qty − stock.qty)) &lt; details.qty\_tolerance and abs((plan.ledger\_value − stock.carried\_value)) &lt; details.value\_tolerance).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in abs((plan.ledger\_qty − stock.qty)) &lt; details.qty\_tolerance → abs((plan.ledger\_value − stock.carried\_value)) &lt; details.value\_tolerance.
    - Set plan.reason from translated “Its stock qty and value are already right on this date.”.
  - Otherwise.
    - Evaluate set\_adjustment\_rows(plan, stock, details, posting\_datetime, …).
  - Set plans at tuple(item\_code, warehouse) from plan.
- Return plans.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1163)

<a id="op-42da1615c19709"></a>
### Set adjustment rows

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_set_adjustment_rows`

**Inputs** plan, stock, details, posting\_datetime, exclude\_voucher\_no.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (stock.serials\_issued\_before\_receipt or any(generator of lot.qty &lt; negative details.qty\_tolerance for lot drawn from stock.batch\_lots.values())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock.serials\_issued\_before\_receipt → any(generator of lot.qty &lt; negative details.qty\_tolerance for lot drawn from stock.batch\_lots.values()).
  - Draw lot from stock.batch\_lots.values().
  - Set plan.reason from translated “Some of its serial nos or batches should be short of stock on this date.”.
  - Return no value.
- Set layers from get\_pool\_layers(stock, details, posting\_datetime).
- If any(generator of qty &lt; 0 for tuple(qty, \_rate) drawn from layers).
  - Draw tuple(qty, \_rate) from layers.
  - Set plan.reason from translated “Its stock should be negative on this date, which cannot be counted in.”.
  - Return no value.
- Set precision from details.currency\_precision.
- Set serial\_nos\_by\_rate from defaultdict(list).
- For each tuple(serial\_no, rate) in stock.serial\_rates.items().
  - Evaluate serial\_nos\_by\_rate at flt(rate, precision).append(serial\_no).
- For each tuple(rate, serial\_nos) in sorted(serial\_nos\_by\_rate.items()).
  - Evaluate plan.rows.append(AdjustmentRow(qty = len(serial\_nos), valuation\_rate = rate, serial\_nos = sorted(serial\_nos))).
- For each tuple(batch\_no, lot) in sorted(stock.batch\_lots.items()).
  - If lot.qty ≥ details.qty\_tolerance.
    - Evaluate plan.rows.append(AdjustmentRow(qty = lot.qty, valuation\_rate = flt((lot.value ÷ lot.qty), precision), batch\_no = batch\_no)).
- Set pooled\_lots from get\_pooled\_lots(plan, details, posting\_datetime, exclude\_voucher\_no).
- Set is\_serial from values\_serial\_nos\_in\_pool(details.data.items at plan.item\_code, details).
- Evaluate plan.rows.extend(spread\_over\_layers(layers, pooled\_lots, details, is\_serial)).
- If not plan.rows.
  - Evaluate plan.rows.append(AdjustmentRow(qty = 0, valuation\_rate = 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1172)

<a id="op-1c9d00d3953682"></a>
### Get pool layers

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_pool_layers`

**Inputs** stock, details, posting\_datetime.

**Declared result** list at tuple at tuple(float, float).

**Explicit results** list of tuple(qty, rate) for tuple(qty, rate) drawn from layers where abs(qty) ≥ details.qty\_tolerance.

**Local steps**

- Set precision from details.currency\_precision.
- Set pool from stock.pool.
- If isinstance(pool, QueuePool).
  - Set layers from list of tuple(qty, flt(rate, precision)) for tuple(qty, rate) drawn from pool.layers.
    - Draw tuple(qty, rate) from pool.layers.
- Otherwise.
  - Set layers from list(tuple(pool.qty, flt(pool.rate, precision))).
- Return list of tuple(qty, rate) for tuple(qty, rate) drawn from layers where abs(qty) ≥ details.qty\_tolerance.
  - Draw tuple(qty, rate) from layers, keep a combination only if (abs(qty) ≥ details.qty\_tolerance).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1165)

<a id="op-b54f87db5b1e7a"></a>
### Get pooled lots

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_pooled_lots`

**Inputs** plan, details, posting\_datetime, exclude\_voucher\_no.

**Declared result** list at list.

**Explicit results** list() · list of list(serial\_no, 1.0) for tuple(serial\_no, qty) drawn from lots.serial\_qty.items() where qty &gt; 0 · list of list(batch\_no, qty) for tuple(batch\_no, qty) drawn from lots.batch\_qty.items() where (qty ≥ details.qty\_tolerance and not details.is\_valued\_batch\_wise(batch\_no)).

**Local steps**

- Set item from details.data.items at plan.item\_code.
- If (not item.has\_serial\_no and not item.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.has\_serial\_no → not item.has\_batch\_no.
  - Return list().
- Set lots from get\_ledger\_lots(plan.item\_code, plan.warehouse, posting\_datetime, exclude\_voucher\_no).
- If values\_serial\_nos\_in\_pool(item, details).
  - Return list of list(serial\_no, 1.0) for tuple(serial\_no, qty) drawn from lots.serial\_qty.items() where qty &gt; 0.
    - Draw tuple(serial\_no, qty) from lots.serial\_qty.items(), keep a combination only if (qty &gt; 0).
- If item.has\_serial\_no.
  - Return list().
- Return list of list(batch\_no, qty) for tuple(batch\_no, qty) drawn from lots.batch\_qty.items() where (qty ≥ details.qty\_tolerance and not details.is\_valued\_batch\_wise(batch\_no)).
  - Draw tuple(batch\_no, qty) from lots.batch\_qty.items(), keep a combination only if ((qty ≥ details.qty\_tolerance and not details.is\_valued\_batch\_wise(batch\_no))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty ≥ details.qty\_tolerance → not details.is\_valued\_batch\_wise(batch\_no).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1166)

<a id="op-7f9a028290be26"></a>
### Values serial nos in pool

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_values_serial_nos_in_pool`

**Inputs** item, details.

**Declared result** bool.

**Explicit results** bool((item.has\_serial\_no and details.values\_everything\_in\_pool)).

**Local steps**

- Return bool((item.has\_serial\_no and details.values\_everything\_in\_pool)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.has\_serial\_no → details.values\_everything\_in\_pool.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1177)

<a id="op-68c0188809a796"></a>
### Spread over layers

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_spread_over_layers`

**Inputs** layers, pooled\_lots, details, is\_serial.

**Declared result** list at AdjustmentRow.

**Explicit results** rows.

**Local steps**

- Set rows from list().
- For each tuple(layer\_qty, rate) in layers.
  - Set serial\_nos from list().
  - While (layer\_qty ≥ details.qty\_tolerance and pooled\_lots).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in layer\_qty ≥ details.qty\_tolerance → pooled\_lots.
    - Set lot from pooled\_lots at 0.
    - Set qty from min(layer\_qty, lot at 1).
    - If is\_serial.
      - Evaluate serial\_nos.append(lot at 0).
    - Otherwise.
      - Evaluate rows.append(AdjustmentRow(qty = qty, valuation\_rate = rate, batch\_no = lot at 0)).
    - Update layer\_qty using − qty.
    - Update lot at 1 using − qty.
    - If lot at 1 &lt; details.qty\_tolerance.
      - Evaluate pooled\_lots.pop(0).
  - If serial\_nos.
    - Evaluate rows.append(AdjustmentRow(qty = len(serial\_nos), valuation\_rate = rate, serial\_nos = serial\_nos)).
  - If layer\_qty ≥ details.qty\_tolerance.
    - Evaluate rows.append(AdjustmentRow(qty = layer\_qty, valuation\_rate = rate)).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1175)

<a id="op-40a932d9fa0d30"></a>
### Get ledger lots

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_ledger_lots`

**Inputs** item\_code, warehouse, posting\_datetime, exclude\_voucher\_no = no value.

**Declared result** LedgerLots.

**Explicit results** lots.

**Local steps**

- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set ledger from Platform.qb.DocType(“Stock Ledger Entry”).
- Set cutoff from get\_datetime(posting\_datetime).
- Set bundle\_entries from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
- Set legacy\_entries from nested operand in the contract.qb.from\_(ledger).select(ledger.serial\_no, ledger.batch\_no, ledger.actual\_qty, ledger.stock\_value\_difference).where((((((nested operand in the contract equals nested operand i ….
- If exclude\_voucher\_no.
  - Set bundle\_entries from bundle\_entries.where(entry.voucher\_no differs from exclude\_voucher\_no).
  - Set legacy\_entries from legacy\_entries.where(ledger.voucher\_no differs from exclude\_voucher\_no).
- Set lots from LedgerLots().
- For each row in bundle\_entries.run(as\_dict = true).
  - If row.serial\_no.
    - Update lots.serial\_qty at row.serial\_no using + flt(row.qty).
  - If row.batch\_no.
    - Update lots.batch\_qty at row.batch\_no using + flt(row.qty).
    - Update lots.batch\_value at row.batch\_no using + flt(row.stock\_value\_difference).
- For each row in legacy\_entries.run(as\_dict = true).
  - For each serial\_no in get\_serial\_nos((row.serial\_no or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → empty text.
    - Update lots.serial\_qty at serial\_no using + 1 when flt(row.actual\_qty) &gt; 0, otherwise negative 1.
      - Value choice on flt(row.actual\_qty) &gt; 0 — true gives 1, false gives negative 1.
  - If row.batch\_no.
    - Update lots.batch\_qty at row.batch\_no using + flt(row.actual\_qty).
    - Update lots.batch\_value at row.batch\_no using + flt(row.stock\_value\_difference).
- Return lots.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1164)

<a id="op-ecf1a2fbdd6013"></a>
### Make adjustment entry

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_make_adjustment_entry`

**Inputs** company, item\_warehouses, posting\_date, posting\_time, expense\_account = no value, cost\_center = no value.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Stock Reconciliation” · call insert on doc.

**Explicit results** tuple(doc, plans).

**Local steps**

- Set plans from get\_adjustment\_plans(item\_warehouses, get\_combine\_datetime(posting\_date, posting\_time)).
- Set doc from Platform.new\_doc(“Stock Reconciliation”).
- Evaluate doc.update(mapping(“purpose” → ADJUSTMENT\_ENTRY, “is\_made\_from\_valuation\_comparison” → 1, “company” → company, “posting\_date” → posting\_date, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expense\_account → get\_stock\_adjustment\_account(company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cost\_center → Platform.get\_cached\_value(“Company”, company, “cost\_center”).
- For each plan in plans.values().
  - If not plan.reason.
    - For each row in plan.rows.
      - Evaluate doc.append(“items”, make\_item\_row(plan, row)).
- If doc.items.
  - Evaluate doc.insert().
- Return tuple(doc, plans).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1170)

<a id="op-e08d0e04847553"></a>
### Get stock adjustment account

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_get_stock_adjustment_account`

**Inputs** company.

**Declared result** (str bitwise or no value).

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_value.

**Explicit results** (Platform.get\_cached\_value(“Company”, company, “stock\_adjustment\_account”) or Platform.db.get\_value(“Account”, mapping(“account\_type” → “Stock Adjustment”, “company” → company, “is\_group” → 0), “name”)).

**Local steps**

- Return (Platform.get\_cached\_value(“Company”, company, “stock\_adjustment\_account”) or Platform.db.get\_value(“Account”, mapping(“account\_type” → “Stock Adjustment”, “company” → company, “is\_group” → 0), “name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, company, “stock\_adjustment\_account”) → Platform.db.get\_value(“Account”, mapping(“account\_type” → “Stock Adjustment”, “company” → company, “is\_group” → 0), “name”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “stock\_adjustment\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1168)

<a id="op-0008303b89bfda"></a>
### Make item row

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_make_item_row`

**Inputs** plan, row.

**Declared result** dict.

**Explicit results** mapping(“item\_code” → plan.item\_code, “warehouse” → plan.warehouse, “qty” → row.qty, “valuation\_rate” → row.valuation\_rate, …).

**Local steps**

- Return mapping(“item\_code” → plan.item\_code, “warehouse” → plan.warehouse, “qty” → row.qty, “valuation\_rate” → row.valuation\_rate, …).
  - Value choice on row.valuation\_rate — true gives 0, false gives 1.
  - Value choice on (row.batch\_no or row.serial\_nos) — true gives 1, false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_no → row.serial\_nos.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1171)

<a id="op-3fdf3f251364d8"></a>
### Adjustment Entry.initialize

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_init`

**Inputs** self, doc.

**Local steps**

- Set self.doc from doc.
- Set self.posting\_datetime from get\_combine\_datetime(doc.posting\_date, doc.posting\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1144)

<a id="op-4d3dd8bf819a2b"></a>
### Adjustment Entry.get rows by item warehouse

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_get_rows_by_item_warehouse`

**Inputs** self.

**Declared result** dict at tuple(tuple at tuple(str, str), list).

**Explicit results** rows.

**Local steps**

- Set rows from defaultdict(list).
- For each row in self.doc.items.
  - Evaluate rows at tuple(row.item\_code, row.warehouse).append(row).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1143)

<a id="op-8dee28d901bf6f"></a>
### Adjustment Entry.get plans

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_get_plans`

**Inputs** self.

**Declared result** dict at tuple(tuple at tuple(str, str), AdjustmentPlan).

**Explicit results** self.doc.flags.adjustment\_plans.

**Local steps**

- If self.doc.flags.adjustment\_plans is identical to no value.
  - Set self.doc.flags.adjustment\_plans from get\_adjustment\_plans(list(self.get\_rows\_by\_item\_warehouse()), self.posting\_datetime, exclude\_voucher\_no = self.doc.name).
- Return self.doc.flags.adjustment\_plans.

**Methods declared on this owner** [get rows by item warehouse](operations-108.md#op-4d3dd8bf819a2b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1142)

<a id="op-23601a1f20e879"></a>
### Adjustment Entry.validate

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_validate`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Item {0} in Warehouse {1} cannot be adjusted on {2}: {3}”.format(bold(item\_code), bold(warehouse), format\_datetime(self.posting\_datetime), plan.reason when plan, otherwise translated “It has no … · validation helper — translated “The rows of Item {0} in Warehouse {1} are not the stock it should hold on this date. Make the Adjustment Ent …”.format(bold(item\_code), bold(warehouse)).

**Local steps**

- For each tuple(tuple(item\_code, warehouse), rows) in self.get\_rows\_by\_item\_warehouse().items().
  - Set plan from self.get\_plans().get(tuple(item\_code, warehouse)).
  - If (not plan or plan.reason).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not plan → plan.reason.
    - Call the validation error handler Platform.throw(translated “Item {0} in Warehouse {1} cannot be adjusted on {2}: {3}”.format(bold(item\_code), bold(warehouse), format\_datetime(self.posting\_datetime), plan.reason when plan, otherwise transl ….
      - Value choice on plan — true gives plan.reason, false gives translated “It has no stock transactions by then.”.
  - Set given from sorted(generator of AdjustmentRow(qty = flt(row.qty), valuation\_rate = flt(row.valuation\_rate), batch\_no = row.batch\_no, serial\_nos = get\_serial\_nos((row.serial\_no or empty text))) for row drawn from rows, ….
    - Draw row from rows.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → empty text.
  - Set needed from sorted(plan.rows, key = deferred anonymous expression).
  - Set rate\_precision from rows at 0.precision(“valuation\_rate”).
  - If (len(given) differs from len(needed) or any(generator of (a.key differs from b.key or flt(nested operand in the contract.valuation\_rate, rate\_precision) differs from flt(nested operand in the contract.valu ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(given) differs from len(needed) → any(generator of (a.key differs from b.key or flt(a.valuation\_rate, rate\_precision) differs from flt(b.valuation\_rate, rate\_precision)) for tuple(a, b) drawn from zip(given, needed, strict = true)).
    - Draw tuple(a, b) from zip(given, needed, strict = true).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in a.key differs from b.key → flt(a.valuation\_rate, rate\_precision) differs from flt(b.valuation\_rate, rate\_precision).
    - Call the validation error handler Platform.throw(translated “The rows of Item {0} in Warehouse {1} are not the stock it should hold on this date. Make the Adjustment Ent …”.format(bold(item\_code), bold(warehouse)), title = translated “Adju ….
  - Evaluate self.set\_row\_amounts(plan, rows).
- Set self.doc.difference\_amount from flt(sum(generator of flt(row.amount\_difference) for row drawn from self.doc.items), self.doc.precision(“difference\_amount”)).
  - Draw row from self.doc.items.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows by item warehouse](operations-108.md#op-4d3dd8bf819a2b), [get plans](operations-108.md#op-8dee28d901bf6f), [set row amounts](operations-108.md#op-031742c0364839).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1151)

<a id="op-f569d2184a4303"></a>
### Adjustment Entry.validate made from report

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_validate_made_from_report`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with ManualAdjustmentEntryError — translated “Adjustment Entry can only be used by the system from the Stock Valuation Comparison report. Users can only s …”.

**Local steps**

- If self.doc.is\_made\_from\_valuation\_comparison.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Adjustment Entry can only be used by the system from the Stock Valuation Comparison report. Users can only s …”, title = translated “Not Allowed Purpose”, exc = ManualAdjustmentEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1152)

<a id="op-031742c0364839"></a>
### Adjustment Entry.set row amounts

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_set_row_amounts`

**Inputs** self, plan, rows.

**Declared result** no value.

**Local steps**

- For each tuple(index, row) in enumerate(rows).
  - Set row.amount from flt((flt(row.qty) × flt(row.valuation\_rate)), row.precision(“amount”)).
  - Set row.current\_qty from plan.ledger\_qty when index equals 0, otherwise 0.
    - Value choice on index equals 0 — true gives plan.ledger\_qty, false gives 0.
  - Set row.current\_amount from flt(plan.ledger\_value, row.precision(“current\_amount”)) when index equals 0, otherwise 0.
    - Value choice on index equals 0 — true gives flt(plan.ledger\_value, row.precision(“current\_amount”)), false gives 0.
  - Set row.current\_valuation\_rate from flt((plan.ledger\_value ÷ plan.ledger\_qty), row.precision(“current\_valuation\_rate”)) when (index equals 0 and plan.ledger\_qty), otherwise 0.
    - Value choice on (index equals 0 and plan.ledger\_qty) — true gives flt((plan.ledger\_value ÷ plan.ledger\_qty), row.precision(“current\_valuation\_rate”)), false gives 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in index equals 0 → plan.ledger\_qty.
  - Set row.quantity\_difference from (flt(row.qty) − flt(row.current\_qty)).
  - Set row.amount\_difference from (flt(row.amount) − flt(row.current\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1150)

<a id="op-3278d4e12b79e7"></a>
### Adjustment Entry.post

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_post`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies update\_batch\_qty.
- For each tuple(tuple(item\_code, warehouse), rows) in self.get\_rows\_by\_item\_warehouse().items().
  - Evaluate self.reset(item\_code, warehouse, rows).
  - Evaluate self.validate\_result(item\_code, warehouse, rows).
- Evaluate update\_batch\_qty(self.doc.doctype, self.doc.name, self.doc.docstatus).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows by item warehouse](operations-108.md#op-4d3dd8bf819a2b), [reset](operations-108.md#op-df73d0bd9ef6eb), [validate result](operations-109.md#op-76638edecf6507).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1146)

<a id="op-df73d0bd9ef6eb"></a>
### Adjustment Entry.reset

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_reset`

**Inputs** self, item\_code, warehouse, rows.

**Declared result** no value.

**Record and data access** read “Item” via get\_cached\_value · read “Stock Ledger Entry” via get\_value.

**Local steps**

- Set lots from get\_ledger\_lots(item\_code, warehouse, self.posting\_datetime, self.doc.name).
- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true).
- Set ledger\_qty from flt(Platform.db.get\_value(“Stock Ledger Entry”, mapping(“item\_code” → item\_code, “warehouse” → warehouse, “is\_cancelled” → 0, “posting\_datetime” → tuple(“&lt;=”, self.posting\_datetime), …), “qty\_after\_transaction …).
- Set first\_row from rows at 0.
- Set primed from self.get\_lots\_to\_prime(item\_code, lots).
- If primed.
  - Evaluate self.post\_entry(first\_row, sum(primed.values()), lots = primed, rate = 0, row\_suffix = “-primed”).
- Set on\_hand from mapping of lot → (qty + primed.get(lot, 0)) for tuple(lot, qty) drawn from self.get\_lots\_on\_hand(item, lots).items().
  - Draw tuple(lot, qty) from self.get\_lots\_on\_hand(item, lots).items().
- Set on\_hand from mapping of lot → qty for tuple(lot, qty) drawn from on\_hand.items() where qty ≥ QTY\_NOISE.
  - Draw tuple(lot, qty) from on\_hand.items(), keep a combination only if (qty ≥ QTY\_NOISE).
- Set without\_lot from ((ledger\_qty + sum(primed.values())) − sum(on\_hand.values())).
- If without\_lot ≤ negative QTY\_NOISE.
  - Evaluate self.post\_entry(first\_row, negative without\_lot, rate = 0).
- If on\_hand.
  - Evaluate self.post\_entry(first\_row, negative sum(on\_hand.values()), lots = on\_hand).
- If without\_lot ≥ QTY\_NOISE.
  - Evaluate self.post\_entry(first\_row, negative without\_lot).
- For each row in rows.
  - If flt(row.qty).
    - Set lots\_of\_row from mapping of serial\_no → 1.0 for serial\_no drawn from get\_serial\_nos(row.serial\_no) when row.serial\_no, otherwise mapping(row.batch\_no → flt(row.qty)) when row.batch\_no, otherwise no value.
      - Value choice on row.serial\_no — true gives mapping of serial\_no → 1.0 for serial\_no drawn from get\_serial\_nos(row.serial\_no), false gives mapping(row.batch\_no → flt(row.qty)) when row.batch\_no, otherwise no value.
      - Draw serial\_no from get\_serial\_nos(row.serial\_no).
      - Value choice on row.batch\_no — true gives mapping(row.batch\_no → flt(row.qty)), false gives no value.
    - Evaluate self.post\_entry(row, flt(row.qty), lots = lots\_of\_row, rate = flt(row.valuation\_rate), counts\_in\_row = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get lots to prime](operations-108.md#op-94777b23ccb73d), [post entry](operations-108.md#op-c42770d10311fe), [get lots on hand](operations-108.md#op-d93ce323f8b2b8).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1148)

<a id="op-d93ce323f8b2b8"></a>
### Adjustment Entry.get lots on hand

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_get_lots_on_hand`

**Inputs** self, item, lots.

**Declared result** dict.

**Explicit results** dict(lots.serial\_qty) · dict(lots.batch\_qty) · mapping().

**Local steps**

- If item.has\_serial\_no.
  - Return dict(lots.serial\_qty).
- If item.has\_batch\_no.
  - Return dict(lots.batch\_qty).
- Return mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1140)

<a id="op-94777b23ccb73d"></a>
### Adjustment Entry.get lots to prime

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_get_lots_to_prime`

**Inputs** self, item\_code, lots.

**Declared result** dict.

**Record and data access** read “Batch” via get\_all · read “Stock Settings” via get\_single\_value · read “Item” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** primed.

**Local steps**

- Set primed from mapping().
- For each tuple(serial\_no, qty) in lots.serial\_qty.items().
  - If qty ≤ negative QTY\_NOISE.
    - Set primed at serial\_no from negative qty.
- Set batch\_wise from set(Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, (list(nested operand in the contract.batch\_qty) or list(empty text))), “use\_batchwise\_valuation” → 1), pluck = “name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(lots.batch\_qty) → list(empty text).
- If (Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”) and (Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”) or Platform.get\_cached\_value(“Company”, self.doc.company ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”) → (Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”) or Platform.get\_cached\_value(“Company”, self.doc.company, “valuation\_method”)) equals “Moving Average”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”) → Platform.get\_cached\_value(“Company”, self.doc.company, “valuation\_method”).
  - Set batch\_wise from set().
- For each tuple(batch\_no, qty) in lots.batch\_qty.items().
  - Set holds\_value from abs(flt(lots.batch\_value at batch\_no, 2)) &gt; 0.
  - If (batch\_no belongs to batch\_wise and qty &lt; QTY\_NOISE and (holds\_value or qty ≤ negative QTY\_NOISE)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no belongs to batch\_wise → qty &lt; QTY\_NOISE → (holds\_value or qty ≤ negative QTY\_NOISE).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in holds\_value → qty ≤ negative QTY\_NOISE.
    - Set primed at batch\_no from (1 − qty).
  - Otherwise.
    - If qty ≤ negative QTY\_NOISE.
      - Set primed at batch\_no from negative qty.
- Return primed.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”), Platform.get\_cached\_value(“Item”, item\_code, “valuation\_method”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1141)

<a id="op-c42770d10311fe"></a>
### Adjustment Entry.post entry

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_post_entry`

**Inputs** self, row, qty, lots = no value, rate = no value, counts\_in\_row = false, row\_suffix = empty text.

**Declared result** no value.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** call db\_set on row.

**Local steps**

- Set sle from Platform.\_dict(mapping(“doctype” → “Stock Ledger Entry”, “item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.doc.posting\_date, …)).
- If qty &gt; 0.
  - Set sle.incoming\_rate from flt(rate).
- If lots.
  - Set sle.serial\_and\_batch\_bundle from self.make\_bundle(row, qty, lots, rate, …).
  - If counts\_in\_row.
    - Evaluate row.db\_set(“serial\_and\_batch\_bundle”, sle.serial\_and\_batch\_bundle, update\_modified = false).
- Evaluate make\_sl\_entries(list(sle), allow\_negative\_stock = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make bundle](operations-108.md#op-20cba2b16f923d).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1147)

<a id="op-20cba2b16f923d"></a>
### Adjustment Entry.make bundle

`operation_enterprise_binding_enterprise_stock_valuation_adjustment_adjustmententry_make_bundle`

**Inputs** self, row, qty, lots, rate, voucher\_detail\_no.

**Declared result** str.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** bundle.name.

**Local steps**

- Bind dependencies SerialBatchCreation.
- Set has\_serial\_no from Platform.get\_cached\_value(“Item”, row.item\_code, “has\_serial\_no”).
- Set bundle from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “company” → self.doc.company, “posting\_datetime” → self.posting\_datetime, …)).make\_serial\_and\_batch\_bundle().
  - Value choice on qty &gt; 0 — true gives “Inward”, false gives “Outward”.
  - Value choice on has\_serial\_no — true gives list(lots), false gives no value.
  - Value choice on has\_serial\_no — true gives no value, false gives Platform.\_dict(lots).
- Return bundle.name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “has\_serial\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1145)
