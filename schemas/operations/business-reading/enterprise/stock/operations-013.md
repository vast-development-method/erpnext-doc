# Inventory and warehouses · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Expected valuation

<a id="op-8a3d3da6cc10c1"></a>
### Ledger Data.get valuation method

`operation_enterprise_binding_enterprise_stock_expected_valuation_ledgerdata_get_valuation_method`

**Inputs** self, item\_code, company.

**Declared result** str.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** (self.items at item\_code.valuation\_method or self.company\_valuation\_methods.get(company) or Platform.db.get\_single\_value(“Stock Settings”, “valuation\_method”) or “FIFO”).

**Local steps**

- Return (self.items at item\_code.valuation\_method or self.company\_valuation\_methods.get(company) or Platform.db.get\_single\_value(“Stock Settings”, “valuation\_method”) or “FIFO”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.items at item\_code.valuation\_method → self.company\_valuation\_methods.get(company) → Platform.db.get\_single\_value(“Stock Settings”, “valuation\_method”) → “FIFO”.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “valuation\_method”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L884)

<a id="op-b01fd3ca2f2f31"></a>
### Valuation Details.initialize

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_init`

**Inputs** self, item\_code, company, data.

**Local steps**

- Set self.item\_code from item\_code.
- Set self.company from company.
- Set self.data from data.
- Set self.valuation\_method from data.get\_valuation\_method(item\_code, company).
- Set item from data.items at item\_code.
- Set self.has\_batch\_no from bool(item.has\_batch\_no).
- Set self.values\_everything\_in\_pool from bool((item.has\_serial\_no and not item.use\_serial\_no\_wise\_valuation)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.has\_serial\_no → not item.use\_serial\_no\_wise\_valuation.
- Set self.batch\_wise\_valuation\_is\_off from bool((self.values\_everything\_in\_pool or (self.valuation\_method equals “Moving Average” and data.settings.do\_not\_use\_batchwise\_valuation))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.values\_everything\_in\_pool → (self.valuation\_method equals “Moving Average” and data.settings.do\_not\_use\_batchwise\_valuation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valuation\_method equals “Moving Average” → data.settings.do\_not\_use\_batchwise\_valuation.
- Set self.currency\_precision from data.settings.currency\_precision.
- Set self.qty\_tolerance from data.settings.qty\_tolerance.
- Set self.value\_tolerance from data.settings.value\_tolerance.
- Set self.dimension\_fields from data.settings.dimension\_fields.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L907)

<a id="op-1ef22ec03fdc64"></a>
### Valuation Details.is valued batch wise

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_is_valued_batch_wise`

**Inputs** self, batch\_no.

**Declared result** bool.

**Explicit results** (not self.batch\_wise\_valuation\_is\_off and batch\_no belongs to self.data.batch\_wise\_valued\_batches).

**Local steps**

- Return (not self.batch\_wise\_valuation\_is\_off and batch\_no belongs to self.data.batch\_wise\_valued\_batches).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.batch\_wise\_valuation\_is\_off → batch\_no belongs to self.data.batch\_wise\_valued\_batches.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L911)

<a id="op-f2c4c79be70428"></a>
### Valuation Details.is adjustment voucher

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_is_adjustment_voucher`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** (entry.voucher\_type equals “Stock Reconciliation” and entry.voucher\_no belongs to self.data.adjustment\_vouchers).

**Local steps**

- Return (entry.voucher\_type equals “Stock Reconciliation” and entry.voucher\_no belongs to self.data.adjustment\_vouchers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.voucher\_type equals “Stock Reconciliation” → entry.voucher\_no belongs to self.data.adjustment\_vouchers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L908)

<a id="op-8a322f650ab682"></a>
### Valuation Details.is reconciled balance

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_is_reconciled_balance`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** false · true · (not entry.serial\_and\_batch\_bundle and not entry.serial\_no).

**Local steps**

- If (entry.voucher\_type differs from “Stock Reconciliation” or entry.is\_adjustment\_entry or entry.batch\_no or any(generator of entry.get(fieldname) for fieldname drawn from self.dimension\_fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.voucher\_type differs from “Stock Reconciliation” → entry.is\_adjustment\_entry → entry.batch\_no → any(generator of entry.get(fieldname) for fieldname drawn from self.dimension\_fields).
  - Draw fieldname from self.dimension\_fields.
  - Return false.
- If (self.values\_everything\_in\_pool and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.values\_everything\_in\_pool → not self.has\_batch\_no.
  - Return true.
- Return (not entry.serial\_and\_batch\_bundle and not entry.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.serial\_and\_batch\_bundle → not entry.serial\_no.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L909)

<a id="op-b728574e2b9957"></a>
### Valuation Details.get reconciled balance

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_get_reconciled_balance`

**Inputs** self, entry.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(flt(reconciled.qty), flt(rate, self.currency\_precision)) · tuple(flt(entry.qty\_after\_transaction), flt(entry.valuation\_rate)).

**Local steps**

- Set reconciled from self.data.reconciled\_balances.get(entry.voucher\_detail\_no).
- If reconciled.
  - Set rate from reconciled.valuation\_rate.
  - If (flt(entry.actual\_qty) &lt; 0 and (entry.serial\_and\_batch\_bundle or entry.serial\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(entry.actual\_qty) &lt; 0 → (entry.serial\_and\_batch\_bundle or entry.serial\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.serial\_and\_batch\_bundle → entry.serial\_no.
    - Set rate from reconciled.current\_valuation\_rate.
  - Return tuple(flt(reconciled.qty), flt(rate, self.currency\_precision)).
- Return tuple(flt(entry.qty\_after\_transaction), flt(entry.valuation\_rate)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L906)

<a id="op-d2577ce8df9c26"></a>
### Valuation Details.is valued as a whole

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_is_valued_as_a_whole`

**Inputs** self, entry.

**Declared result** bool.

**Explicit results** false · true · (not entry.serial\_and\_batch\_bundle and not entry.serial\_no and not (entry.batch\_no and self.is\_valued\_batch\_wise(entry.batch\_no))).

**Local steps**

- If self.valuation\_method differs from “Moving Average”.
  - Return false.
- If self.values\_everything\_in\_pool.
  - Return true.
- Return (not entry.serial\_and\_batch\_bundle and not entry.serial\_no and not (entry.batch\_no and self.is\_valued\_batch\_wise(entry.batch\_no))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.serial\_and\_batch\_bundle → not entry.serial\_no → not (entry.batch\_no and self.is\_valued\_batch\_wise(entry.batch\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.batch\_no → self.is\_valued\_batch\_wise(entry.batch\_no).

**Methods declared on this owner** [is valued batch wise](operations-013.md#op-1ef22ec03fdc64).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L910)

<a id="op-734b92eb7f3588"></a>
### Valuation Details.get lot movements

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_get_lot_movements`

**Inputs** self, entry.

**Declared result** list at LotMovement.

**Explicit results** list(LotMovement(qty = qty, rate = flt(entry.incoming\_rate))) · list of LotMovement(qty = abs(flt(row.qty)), rate = flt(row.incoming\_rate), batch\_no = row.batch\_no, serial\_no = row.serial\_no) for row drawn from bundle\_rows · list of LotMovement(qty = 1, rate = rate, serial\_no = serial\_no) for serial\_no drawn from serial\_nos · list(LotMovement(qty = qty, rate = flt(entry.incoming\_rate), batch\_no = entry.batch\_no)).

**Local steps**

- Set qty from abs(flt(entry.actual\_qty)).
- If self.values\_everything\_in\_pool.
  - Return list(LotMovement(qty = qty, rate = flt(entry.incoming\_rate))).
- Set bundle\_rows from self.data.bundle\_rows.get(entry.serial\_and\_batch\_bundle).
- If (entry.serial\_and\_batch\_bundle and bundle\_rows).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_and\_batch\_bundle → bundle\_rows.
  - Return list of LotMovement(qty = abs(flt(row.qty)), rate = flt(row.incoming\_rate), batch\_no = row.batch\_no, serial\_no = row.serial\_no) for row drawn from bundle\_rows.
    - Draw row from bundle\_rows.
- If entry.serial\_no.
  - Set serial\_nos from get\_serial\_nos(entry.serial\_no).
  - Set rate from flt(entry.incoming\_rate).
  - Return list of LotMovement(qty = 1, rate = rate, serial\_no = serial\_no) for serial\_no drawn from serial\_nos.
    - Draw serial\_no from serial\_nos.
- Return list(LotMovement(qty = qty, rate = flt(entry.incoming\_rate), batch\_no = entry.batch\_no)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L904)

<a id="op-fbe1665b031182"></a>
### Valuation Details.get purchase return rate

`operation_enterprise_binding_enterprise_stock_expected_valuation_valuationdetails_get_purchase_return_rate`

**Inputs** self, entry.

**Declared result** (float bitwise or no value).

**Explicit results** no value · self.data.purchase\_return\_rates.get(entry.name).

**Local steps**

- If (self.valuation\_method differs from “FIFO” or self.values\_everything\_in\_pool or entry.voucher\_type does not belong to RETURNABLE\_PURCHASE\_DOCTYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.valuation\_method differs from “FIFO” → self.values\_everything\_in\_pool → entry.voucher\_type does not belong to RETURNABLE\_PURCHASE\_DOCTYPES.
  - Return no value.
- Return self.data.purchase\_return\_rates.get(entry.name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L905)

<a id="op-006c124b9fbfc2"></a>
### Get ledger entries

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_ledger_entries`

**Inputs** item\_warehouses, to\_date, settings.

**Declared result** dict.

**Explicit results** entries\_by\_item\_warehouse.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set fields from list of sle at fieldname for fieldname drawn from tuple(expanded LEDGER\_FIELDS, expanded settings.dimension\_fields).
  - Draw fieldname from tuple(expanded LEDGER\_FIELDS, expanded settings.dimension\_fields).
- Set of\_item\_warehouses from reduce(operator.or\_, generator of (sle.item\_code equals item\_code bitwise and sle.warehouse equals warehouse) for tuple(item\_code, warehouse) drawn from item\_warehouses).
  - Draw tuple(item\_code, warehouse) from item\_warehouses.
- Set query from nested operand in the contract(nested operand in the contract).orderby(sle.warehouse).orderby(sle.posting\_datetime).orderby(sle.creation).
- If to\_date.
  - Set query from query.where(sle.posting\_date ≤ getdate(to\_date)).
- Set entries\_by\_item\_warehouse from mapping().
- For each entry in query.run(as\_dict = true).
  - Evaluate entries\_by\_item\_warehouse.setdefault(tuple(entry.item\_code, entry.warehouse), list()).append(entry).
- Return entries\_by\_item\_warehouse.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L862)

<a id="op-821012658219b7"></a>
### Get bundle rows

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_bundle_rows`

**Inputs** bundles.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** rows\_by\_bundle.

**Local steps**

- Set rows\_by\_bundle from mapping().
- For each bundles\_to\_read in create\_batch(list(bundles), 1000).
  - For each row in Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, bundles\_to\_read)), fields = list(“parent”, “serial\_no”, “batch\_no”, “qty”, …), order\_by = “parent asc, idx asc”).
    - Evaluate rows\_by\_bundle.setdefault(row.parent, list()).append(row).
- Return rows\_by\_bundle.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L857)

<a id="op-b452d5821cb4e5"></a>
### Get batch wise valued batches

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_batch_wise_valued_batches`

**Inputs** batches.

**Declared result** set at str.

**Record and data access** read “Batch” via get\_all.

**Explicit results** valued\_batch\_wise.

**Local steps**

- Set valued\_batch\_wise from set().
- For each batches\_to\_read in create\_batch(list(batches), 1000).
  - Evaluate valued\_batch\_wise.update(Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, batches\_to\_read), “use\_batchwise\_valuation” → 1), pluck = “name”)).
- Return valued\_batch\_wise.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L856)

<a id="op-519fca9093c023"></a>
### Get adjustment vouchers

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_adjustment_vouchers`

**Inputs** ledger\_entries.

**Declared result** set at str.

**Record and data access** read “Stock Reconciliation” via get\_all.

**Explicit results** adjustment\_vouchers.

**Local steps**

- Set reconciliations from set of entry.voucher\_no for entry drawn from ledger\_entries where entry.voucher\_type equals “Stock Reconciliation”.
  - Draw entry from ledger\_entries, keep a combination only if (entry.voucher\_type equals “Stock Reconciliation”).
- Set adjustment\_vouchers from set().
- For each reconciliations\_to\_read in create\_batch(list(reconciliations), 1000).
  - Evaluate adjustment\_vouchers.update(Platform.get\_all(“Stock Reconciliation”, filters = mapping(“name” → tuple(“in”, reconciliations\_to\_read), “purpose” → ADJUSTMENT\_ENTRY), pluck = “name”)).
- Return adjustment\_vouchers.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L855)

<a id="op-57767a9d04483c"></a>
### Get adjustment rows

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_adjustment_rows`

**Inputs** adjustment\_vouchers.

**Declared result** dict at tuple(tuple at tuple(str, str, str), list).

**Record and data access** read “Stock Reconciliation Item” via get\_all.

**Explicit results** rows.

**Local steps**

- Set rows from mapping().
- For each vouchers\_to\_read in create\_batch(list(adjustment\_vouchers), 1000).
  - For each row in Platform.get\_all(“Stock Reconciliation Item”, filters = mapping(“parent” → tuple(“in”, vouchers\_to\_read)), fields = list(“parent”, “item\_code”, “warehouse”, “qty”, …), order\_by = “parent asc, idx asc”).
    - Evaluate rows.setdefault(tuple(row.parent, row.item\_code, row.warehouse), list()).append(row).
- Return rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L854)

<a id="op-ce01ff1c9ad398"></a>
### Get adjustment last entries

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_adjustment_last_entries`

**Inputs** entries\_by\_item\_warehouse, adjustment\_vouchers.

**Declared result** set at str.

**Explicit results** set(last\_entries.values()).

**Local steps**

- Set last\_entries from mapping().
- For each entries in entries\_by\_item\_warehouse.values().
  - For each entry in entries.
    - If (entry.voucher\_type equals “Stock Reconciliation” and entry.voucher\_no belongs to adjustment\_vouchers).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.voucher\_type equals “Stock Reconciliation” → entry.voucher\_no belongs to adjustment\_vouchers.
      - Set last\_entries at tuple(entry.voucher\_no, entry.item\_code, entry.warehouse) from entry.name.
- Return set(last\_entries.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L853)

<a id="op-103821aeac90d5"></a>
### Get reconciled balances

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_reconciled_balances`

**Inputs** ledger\_entries.

**Declared result** dict at tuple(str, Platform.\_dict).

**Record and data access** read “Stock Reconciliation Item” via get\_all.

**Explicit results** reconciled\_balances.

**Local steps**

- Set rows from set of entry.voucher\_detail\_no for entry drawn from ledger\_entries where (entry.voucher\_type equals “Stock Reconciliation” and entry.voucher\_detail\_no).
  - Draw entry from ledger\_entries, keep a combination only if ((entry.voucher\_type equals “Stock Reconciliation” and entry.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.voucher\_type equals “Stock Reconciliation” → entry.voucher\_detail\_no.
- Set reconciled\_balances from mapping().
- For each rows\_to\_read in create\_batch(list(rows), 1000).
  - For each row in Platform.get\_all(“Stock Reconciliation Item”, filters = mapping(“name” → tuple(“in”, rows\_to\_read)), fields = list(“name”, “qty”, “valuation\_rate”, “current\_valuation\_rate”)).
    - Set reconciled\_balances at row.name from row.
- Return reconciled\_balances.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L865)

<a id="op-94cc7ba705ce67"></a>
### Get item settings

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_item_settings`

**Inputs** item\_codes.

**Declared result** dict at tuple(str, Platform.\_dict).

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping() · mapping of item.name → item for item drawn from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(item\_codes))), fields = list(“name”, “valuation\_method”, “has\_serial\_no”, “has\_batch\_no”, …)).

**Local steps**

- If not item\_codes.
  - Return mapping().
- Return mapping of item.name → item for item drawn from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(item\_codes))), fields = list(“name”, “valuation\_method”, “has\_serial\_no”, “has\_batch\_no”, …)).
  - Draw item from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list(item\_codes))), fields = list(“name”, “valuation\_method”, “has\_serial\_no”, “has\_batch\_no”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L861)

<a id="op-3dcb1e615bab24"></a>
### Get company valuation methods

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_company_valuation_methods`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Company” via get\_all.

**Explicit results** dict(Platform.get\_all(“Company”, fields = list(“name”, “valuation\_method”), as\_list = true)).

**Local steps**

- Return dict(Platform.get\_all(“Company”, fields = list(“name”, “valuation\_method”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L858)

<a id="op-c5795eb51935e2"></a>
### Get purchase return rates

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_purchase_return_rates`

**Inputs** ledger\_entries.

**Declared result** dict at tuple(str, (float bitwise or no value)).

**Record and data access** read voucher\_type via get\_all · read formatted text {voucher\_type} Item via get\_all · read “Stock Ledger Entry” via get\_all.

**Explicit results** rates.

**Local steps**

- Set rates from mapping().
- For each voucher\_type in RETURNABLE\_PURCHASE\_DOCTYPES.
  - Set entries from list of entry for entry drawn from ledger\_entries where (entry.voucher\_type equals voucher\_type and flt(entry.actual\_qty) &lt; 0).
    - Draw entry from ledger\_entries, keep a combination only if ((entry.voucher\_type equals voucher\_type and flt(entry.actual\_qty) &lt; 0)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.voucher\_type equals voucher\_type → flt(entry.actual\_qty) &lt; 0.
  - If not entries.
    - Continue with the next iteration or loop test.
  - Set returned\_vouchers from dict(Platform.get\_all(voucher\_type, filters = mapping(“name” → tuple(“in”, list(set of nested operand in the contract.voucher\_no for entry drawn from entries)), “is\_return” → 1), fields = list(“name”, “return\_a …).
    - Draw entry from entries.
  - Set entries from list of entry for entry drawn from entries where returned\_vouchers.get(entry.voucher\_no).
    - Draw entry from entries, keep a combination only if (returned\_vouchers.get(entry.voucher\_no)).
  - If not entries.
    - Continue with the next iteration or loop test.
  - Set returned\_rows from dict(Platform.get\_all(formatted text {voucher\_type} Item, filters = mapping(“name” → tuple(“in”, list(set of nested operand in the contract.voucher\_detail\_no for entry drawn from entries where nested operand in …).
    - Draw entry from entries, keep a combination only if (entry.voucher\_detail\_no).
  - Set tuple(receipt\_rates, receipt\_row\_rates) from tuple(mapping(), mapping()).
  - For each receipt in Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → tuple(“in”, list(set(nested operand in the contract.values()))), “is\_cancelled” → 0, “actual\_qty” → tu ….
    - Set key from tuple(receipt.voucher\_no, receipt.item\_code, receipt.warehouse).
    - Evaluate receipt\_rates.setdefault(key, flt(receipt.incoming\_rate)).
    - Evaluate receipt\_row\_rates.setdefault(tuple(expanded key, receipt.voucher\_detail\_no), flt(receipt.incoming\_rate)).
  - For each entry in entries.
    - Set key from tuple(returned\_vouchers at entry.voucher\_no, entry.item\_code, entry.warehouse).
    - Set returned\_row from returned\_rows.get(entry.voucher\_detail\_no).
    - Set rate from receipt\_row\_rates.get(tuple(expanded key, returned\_row)) when returned\_row, otherwise receipt\_rates.get(key).
      - Value choice on returned\_row — true gives receipt\_row\_rates.get(tuple(expanded key, returned\_row)), false gives receipt\_rates.get(key).
    - If rate is distinct from no value.
      - Set rates at entry.name from rate.
- Return rates.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L864)

<a id="op-77370e391e0a01"></a>
### Get inventory dimension fields

`operation_enterprise_binding_enterprise_stock_expected_valuation_get_inventory_dimension_fields`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list of dimension.get(“fieldname”) for dimension drawn from get\_inventory\_dimensions().

**Local steps**

- Bind dependencies get\_inventory\_dimensions.
- Return list of dimension.get(“fieldname”) for dimension drawn from get\_inventory\_dimensions().
  - Draw dimension from get\_inventory\_dimensions().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L860)

## Report · Fifo queue vs qty after transaction comparison

<a id="op-63bb2942907ada"></a>
### Execute

`operation_enterprise_stock_report_fifo_queue_vs_quantity_after_transaction_comparison_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L135)

<a id="op-d8315bf557b7f1"></a>
### Get data

`operation_enterprise_stock_report_fifo_queue_vs_quantity_after_transaction_comparison_business_behavior_get_data`

**Inputs** filters.

**Explicit results** find\_first\_bad\_queue(sles).

**Explicit failure paths** validation helper — translated “Any one of following filters required: warehouse, Item Code, Item Group”.

**Local steps**

- If not any(list(filters.warehouse, filters.item\_code, filters.item\_group)).
  - Call the validation error handler Platform.throw(translated “Any one of following filters required: warehouse, Item Code, Item Group”).
- Set sles from get\_stock\_ledger\_entries(filters).
- Return find\_first\_bad\_queue(sles).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0890.json#L3422) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L138)

<a id="op-1b7d4c223ba7bd"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_fifo_queue_vs_quantity_after_transaction_comparison_business_behavior_get_stock_ledger_entries`

**Inputs** filters.

**Record and data access** read “Item” via get\_all · read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, fields = SLE\_FIELDS, filters = sle\_filters, order\_by = “posting\_datetime, creation”).

**Local steps**

- Set sle\_filters from mapping(“is\_cancelled” → 0).
- If filters.warehouse.
  - Set children from get\_descendants\_of(“Warehouse”, filters.warehouse).
  - Set sle\_filters at “warehouse” from tuple(“in”, list(expanded children, filters.warehouse)).
- If filters.item\_code.
  - Set sle\_filters at “item\_code” from filters.item\_code.
- Otherwise.
  - If filters.get(“item\_group”).
    - Set item\_group from filters.get(“item\_group”).
    - Set children from get\_descendants\_of(“Item Group”, item\_group).
    - Set item\_group\_filter from mapping(“item\_group” → tuple(“in”, list(expanded children, item\_group))).
    - Set sle\_filters at “item\_code” from tuple(“in”, Platform.get\_all(“Item”, filters = item\_group\_filter, pluck = “name”, order\_by = no value)).
- If (filters.from\_date and filters.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.from\_date → filters.to\_date.
  - Set sle\_filters at “posting\_date” from tuple(“between”, list(filters.from\_date, filters.to\_date)).
- Otherwise.
  - If filters.from\_date.
    - Set sle\_filters at “posting\_date” from tuple(“&gt;=”, filters.from\_date).
  - Otherwise.
    - If filters.to\_date.
      - Set sle\_filters at “posting\_date” from tuple(“&lt;=”, filters.to\_date).
- Return Platform.get\_all(“Stock Ledger Entry”, fields = SLE\_FIELDS, filters = sle\_filters, order\_by = “posting\_datetime, creation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L139)

<a id="op-f404109bb1d0e9"></a>
### Find first bad queue

`operation_enterprise_stock_report_fifo_queue_vs_quantity_after_transaction_comparison_business_behavior_find_first_bad_queue`

**Inputs** sles.

**Record and data access** read “Batch” via get\_value.

**Explicit results** data.

**Local steps**

- Set item\_warehouse\_sles from mapping().
- For each sle in sles.
  - Evaluate item\_warehouse\_sles.setdefault(tuple(sle.item\_code, sle.warehouse), list()).append(sle).
- Set data from list().
- Set valuation\_methods from mapping().
- For each tuple(tuple(item\_code, \_warehouse), sles) in item\_warehouse\_sles.items().
  - For each tuple(idx, sle) in enumerate(sles).
    - Set key from tuple(item\_code, sle.company).
    - If key does not belong to valuation\_methods.
      - Set valuation\_methods at key from get\_valuation\_method(item\_code, sle.company).
    - If sle.batch\_no.
      - Set sle.use\_batchwise\_valuation from Platform.db.get\_value(“Batch”, sle.batch\_no, “use\_batchwise\_valuation”, cache = true).
    - If not keeps\_fifo\_queue(sle, valuation\_methods at key).
      - Continue with the next iteration or loop test.
    - Evaluate set\_queue\_totals(sle).
    - If (abs(sle.fifo\_qty\_diff) &gt; 0.001 or abs(sle.fifo\_value\_diff) &gt; 0.1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs(sle.fifo\_qty\_diff) &gt; 0.001 → abs(sle.fifo\_value\_diff) &gt; 0.1.
      - If idx.
        - Evaluate data.append(sles at (idx − 1)).
      - Evaluate data.append(sle).
      - Evaluate data.append(mapping()).
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L136)
