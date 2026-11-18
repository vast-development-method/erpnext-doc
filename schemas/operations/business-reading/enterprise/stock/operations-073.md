# Inventory and warehouses · operations 73

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock balance

<a id="op-b70e0a538134b4"></a>
### Filter items with no transactions

`operation_enterprise_stock_report_stock_balance_business_behavior_filter_items_with_number_transactions`

**Inputs** iwb\_map, float\_precision, inventory\_dimensions = no value.

**Explicit results** iwb\_map.

**Local steps**

- Set pop\_keys from list().
- For each group\_by\_key in iwb\_map.
  - Set qty\_dict from iwb\_map at group\_by\_key.
  - Set no\_transactions from true.
  - For each tuple(key, val) in qty\_dict.items().
    - If (inventory\_dimensions and key belongs to inventory\_dimensions).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in inventory\_dimensions → key belongs to inventory\_dimensions.
      - Continue with the next iteration or loop test.
    - If key belongs to list(“item\_code”, “warehouse”, “item\_name”, “item\_group”, …).
      - Continue with the next iteration or loop test.
    - Set val from flt(val, float\_precision).
    - Set qty\_dict at key from val.
    - If (key differs from “val\_rate” and val).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in key differs from “val\_rate” → val.
      - Set no\_transactions from false.
  - If no\_transactions.
    - Evaluate pop\_keys.append(group\_by\_key).
- For each key in pop\_keys.
  - Evaluate iwb\_map.pop(key).
- Return iwb\_map.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L460)

<a id="op-ac8ef54679e139"></a>
### Get variants attributes

`operation_enterprise_stock_report_stock_balance_business_behavior_get_variants_attributes`

**Inputs** no declared parameters.

**Declared result** list at str.

**Record and data access** read “Item Attribute” via get\_all.

**Explicit results** Platform.get\_all(“Item Attribute”, pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Item Attribute”, pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0914.json#L6502) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L462)

<a id="op-33bfed06ccf5ec"></a>
### Execute

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_execute`

**Inputs** filters.

**Explicit results** StockBalanceSnapshotReport(filters, conn, sync.creation).run().

**Explicit failure paths** validation helper — translated “Stock ageing data is not available from a snapshot. Uncheck {0}, or turn off {1} for this report.”.format(Platform.bold(translated “Show Stock Ageing Data”), Platform.bold(translated “Snapshot Report”)) · validation helper — translated “Stock Balance needs a DuckDB sync of Stock Ledger Entry”.

**Local steps**

- If filters.get(“show\_stock\_ageing\_data”).
  - Call the validation error handler Platform.throw(translated “Stock ageing data is not available from a snapshot. Uncheck {0}, or turn off {1} for this report.”.format(Platform.bold(translated “Show Stock Ageing Data”), Platform.bold(transl ….
- Set sync from get\_latest\_complete\_sync(“Stock Ledger Entry”).
- If not sync.
  - Call the validation error handler Platform.throw(translated “Stock Balance needs a DuckDB sync of Stock Ledger Entry”).
- Set conn from get\_duckdb(true, sync.filename).
- Attempt the following.
  - Return StockBalanceSnapshotReport(filters, conn, sync.creation).run().
- On exit, including pending return or failure.
  - Evaluate conn.close().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1005)

<a id="op-28f73712450659"></a>
### Stock Balance Snapshot Report.initialize

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_init`

**Inputs** self, filters, conn, synced\_at.

**Local steps**

- Evaluate super().\_\_init\_\_(filters).
- Set self.conn from conn.
- Set self.synced\_at from synced\_at.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1016)

<a id="op-2b752aad415633"></a>
### Stock Balance Snapshot Report.get entries from stock closing balance

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_entries_from_stock_closing_balance`

**Inputs** self.

**Record and data access** read “Stock Closing Entry” via get\_value.

**Explicit results** list() · super().get\_entries\_from\_stock\_closing\_balance().

**Local steps**

- Set closing from StockClosing(self.filters.company, self.from\_date, self.from\_date).last\_closing\_balance.
- If (closing and Platform.db.get\_value(“Stock Closing Entry”, closing.name, “modified”) &gt; self.synced\_at).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in closing → Platform.db.get\_value(“Stock Closing Entry”, closing.name, “modified”) &gt; self.synced\_at.
  - Return list().
- Return super().get\_entries\_from\_stock\_closing\_balance().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1009)

<a id="op-8728d965c80556"></a>
### Stock Balance Snapshot Report.get opening vouchers

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_opening_vouchers`

**Inputs** self.

**Record and data access** read voucher\_type via get\_all.

**Explicit results** vouchers.

**Local steps**

- Set vouchers from super().get\_opening\_vouchers().
- For each tuple(voucher\_type, opening) in tuple(tuple(“Stock Entry”, mapping(“is\_opening” → “Yes”)), tuple(“Stock Reconciliation”, mapping(“purpose” → “Opening Stock”))).
  - Update vouchers at voucher\_type using + Platform.get\_all(voucher\_type, filters = mapping(“docstatus” → 2, “posting\_date” → tuple(“&lt;=”, self.to\_date), expand opening), pluck = “name”).
- Return vouchers.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1013)

<a id="op-22eb8a591b98ec"></a>
### Stock Balance Snapshot Report.prepare item warehouse map for current period

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_prepare_item_warehouse_map_for_current_period`

**Inputs** self.

**Local steps**

- Set self.opening\_vouchers from self.get\_opening\_vouchers().
- Evaluate self.load\_ledger().
- Evaluate self.prepare\_stock\_reco\_voucher\_wise\_count().
- Set changes from list(expanded self.run\_sql(REPLAY\_ROWS\_SQL), expanded self.run\_sql(self.get\_segments\_sql())).
- Set self.adjustment\_netting from AdjustmentNetting().
- For each change in self.adjustment\_netting.net(sorted(changes, key = itemgetter(“row\_no”))).
  - Evaluate self.apply\_change(change).
- Set self.item\_warehouse\_map from filter\_items\_with\_no\_transactions(self.item\_warehouse\_map, self.float\_precision, self.inventory\_dimensions).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get opening vouchers](operations-073.md#op-8728d965c80556), [load ledger](operations-073.md#op-f59d6b4e602224), [prepare stock reco voucher wise count](operations-073.md#op-4c54b5fbab2a4c), [run sql](operations-073.md#op-75f0df3c0156fc), [get segments sql](operations-073.md#op-aaa45f563029a6), [apply change](operations-073.md#op-c73935cd020bc6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1018)

<a id="op-f59d6b4e602224"></a>
### Stock Balance Snapshot Report.load ledger

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_load_ledger`

**Inputs** self.

**Local steps**

- Set tuple(conditions, params) from self.get\_conditions().
- Evaluate self.register\_items(conditions, params).
- Set grouped from “, ”.join(generator of self.dimension\_columns at field for field drawn from self.get\_grouped\_dimensions()).
  - Draw field from self.get\_grouped\_dimensions().
- Set sql from LEDGER\_SQL.format(dimensions = empty text.join(generator of formatted text , {column} AS "{field}" for tuple(field, column) drawn from self.dimension\_columns.items()), dimension\_key = formatted text list\_f ….
  - Draw tuple(field, column) from self.dimension\_columns.items().
  - Value choice on grouped — true gives formatted text list\_filter(&#91;{grouped}&#93;, value -&gt; coalesce(value, '') &lt;&gt; ''), false gives “NULL”.
- Evaluate self.conn.execute(sql, mapping(expand params, “from\_date” → self.from\_date, “unit” → (10 to the power negative self.float\_precision), “opening\_entries” → self.opening\_vouchers at “Stock Entry”, …)).
- Evaluate self.conn.execute(REPLAY\_SQL).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get conditions](operations-073.md#op-0b3255b7859a6e), [register items](operations-073.md#op-b5319142b53f36), [get grouped dimensions](operations-073.md#op-180705d018c6db).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1017)

<a id="op-b5319142b53f36"></a>
### Stock Balance Snapshot Report.register items

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_register_items`

**Inputs** self, conditions, params.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set query from Platform.qb.from\_(item).select(expanded generator of item at field for field drawn from ITEM\_COLUMNS).
  - Draw field from ITEM\_COLUMNS.
- Set query from self.apply\_items\_filters(query, item).
- Set rows from list().
- For each codes in batched(self.get\_ledger\_item\_codes(conditions, params), BATCH\_SIZE).
  - Update rows using + query.where(item.name.isin(codes)).run(as\_dict = true).
- Evaluate self.conn.register(“snapshot\_items”, pa.Table.from\_pylist(rows, schema = pa.schema(ITEM\_COLUMNS.items()))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ledger item codes](operations-073.md#op-524715f7801466).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1020)

<a id="op-524715f7801466"></a>
### Stock Balance Snapshot Report.get ledger item codes

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_ledger_item_codes`

**Inputs** self, conditions, params.

**Explicit results** list of code for tuple(code) drawn from self.conn.execute(sql, params).fetchall().

**Local steps**

- Set sql from formatted text SELECT DISTINCT sle.item\_code FROM "tabStock Ledger Entry" sle WHERE {conditions}.
- If item\_codes bound to self.filters.get(“item\_code”).
  - Update sql using + “ AND list\_contains($item\_codes::VARCHAR&#91;&#93;, sle.item\_code)”.
  - Set params from mapping(expand params, “item\_codes” → list(item\_codes)).
- Return list of code for tuple(code) drawn from self.conn.execute(sql, params).fetchall().
  - Draw tuple(code) from self.conn.execute(sql, params).fetchall().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1012)

<a id="op-0b3255b7859a6e"></a>
### Stock Balance Snapshot Report.get conditions

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_conditions`

**Inputs** self.

**Explicit results** tuple(“ AND ”.join(conditions), params).

**Local steps**

- Set conditions from list(“sle.docstatus &lt; 2”, “sle.is\_cancelled = 0”, “sle.posting\_date &lt;= $to\_date”).
- Set params from mapping(“to\_date” → self.to\_date).
- If (not self.filters.ignore\_closing\_balance and self.start\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.filters.ignore\_closing\_balance → self.start\_from.
  - Evaluate conditions.append(“sle.posting\_date &gt;= $start\_from”).
  - Set params at “start\_from” from getdate(self.start\_from).
- If company bound to self.filters.get(“company”).
  - Evaluate conditions.append(“sle.company = $company”).
  - Set params at “company” from company.
- If warehouses bound to self.get\_warehouses() is distinct from no value.
  - Evaluate conditions.append(“list\_contains($warehouses::VARCHAR&#91;&#93;, sle.warehouse)”).
  - Set params at “warehouses” from warehouses.
- For each tuple(index, tuple(field, column)) in enumerate(self.dimension\_columns.items()).
  - If values bound to self.filters.get(field).
    - Evaluate conditions.append(formatted text list\_contains($dimension\_{index}::VARCHAR&#91;&#93;, {column})).
    - Set params at formatted text dimension\_{index} from list(values).
- Return tuple(“ AND ”.join(conditions), params).

**Methods declared on this owner** [get warehouses](operations-073.md#op-742bb3094c9a5d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1008)

<a id="op-7c9a2e61014eba"></a>
### Stock Balance Snapshot Report.dimension columns

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_dimension_columns`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** mapping of field → formatted text sle."{field}" when field belongs to synced, otherwise “NULL::VARCHAR” for field drawn from self.inventory\_dimensions.

**Local steps**

- Set synced from set(self.conn.table(“tabStock Ledger Entry”).columns).
- Return mapping of field → formatted text sle."{field}" when field belongs to synced, otherwise “NULL::VARCHAR” for field drawn from self.inventory\_dimensions.
  - Draw field from self.inventory\_dimensions.
  - Value choice on field belongs to synced — true gives formatted text sle."{field}", false gives “NULL::VARCHAR”.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1007)

<a id="op-742bb3094c9a5d"></a>
### Stock Balance Snapshot Report.get warehouses

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_warehouses`

**Inputs** self.

**Explicit results** no value · query.run(pluck = true).

**Local steps**

- If not (self.filters.get(“warehouse”) or self.filters.get(“warehouse\_type”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“warehouse”) → self.filters.get(“warehouse\_type”).
  - Return no value.
- Set warehouse from Platform.qb.DocType(“Warehouse”).
- Set ledger from nested operand in the contract.qb.from\_(warehouse).select(warehouse.name.as\_(“warehouse”)).as\_(“ledger”).
- Set query from self.apply\_warehouse\_filters(Platform.qb.from\_(ledger).select(ledger.warehouse), ledger).
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1015)

<a id="op-180705d018c6db"></a>
### Stock Balance Snapshot Report.get grouped dimensions

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_grouped_dimensions`

**Inputs** self.

**Explicit results** list of field for field drawn from self.inventory\_dimensions where (self.filters.get(field) or self.filters.get(“show\_dimension\_wise\_stock”)).

**Local steps**

- Return list of field for field drawn from self.inventory\_dimensions where (self.filters.get(field) or self.filters.get(“show\_dimension\_wise\_stock”)).
  - Draw field from self.inventory\_dimensions, keep a combination only if ((self.filters.get(field) or self.filters.get(“show\_dimension\_wise\_stock”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(field) → self.filters.get(“show\_dimension\_wise\_stock”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1010)

<a id="op-4c54b5fbab2a4c"></a>
### Stock Balance Snapshot Report.prepare stock reco voucher wise count

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_prepare_stock_reco_voucher_wise_count`

**Inputs** self.

**Record and data access** read “Stock Reconciliation Item” via get\_all.

**Explicit results** no value.

**Local steps**

- Set self.stock\_reco\_voucher\_wise\_count from Platform.\_dict().
- Set details from self.run\_sql(SERIAL\_RECONCILIATIONS\_SQL).
- If not details.
  - Return no value.
- For each item in Platform.get\_all(“Stock Reconciliation Item”, filters = mapping(“name” → tuple(“in”, list of row.voucher\_detail\_no for row drawn from details)), fields = list(“name”, “current\_qty”, “qty”)).
  - Draw row from details.
  - If (item.qty and item.current\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.qty → item.current\_qty.
    - Set self.stock\_reco\_voucher\_wise\_count at item.name from item.current\_qty.

If control reaches the end, it returns no value.

**Methods declared on this owner** [run sql](operations-073.md#op-75f0df3c0156fc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1019)

<a id="op-aaa45f563029a6"></a>
### Stock Balance Snapshot Report.get segments sql

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_segments_sql`

**Inputs** self.

**Explicit results** SEGMENTS\_SQL.format(details = “, ”.join(generator of formatted text arg\_max\_null("{field}", row\_no) AS "{field}" for field drawn from fields)).

**Local steps**

- Set fields from tuple(expanded SEGMENT\_DETAILS, expanded self.inventory\_dimensions).
- Return SEGMENTS\_SQL.format(details = “, ”.join(generator of formatted text arg\_max\_null("{field}", row\_no) AS "{field}" for field drawn from fields)).
  - Draw field from fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1014)

<a id="op-c73935cd020bc6"></a>
### Stock Balance Snapshot Report.apply change

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_apply_change`

**Inputs** self, change.

**Explicit results** no value.

**Local steps**

- Set key from self.get\_group\_by\_key(change).
- If key does not belong to self.item\_warehouse\_map.
  - Evaluate self.initialize\_data(key, change).
- If change.replay.
  - Evaluate self.prepare\_item\_warehouse\_map(change, key).
  - Return no value.
- Set balance from self.item\_warehouse\_map at key.
- Evaluate self.add\_to\_item\_warehouse\_balance(self.get\_item\_warehouse\_balance(change, balance), balance, change.bal\_qty, change.bal\_val).
- For each field in MOVEMENT\_FIELDS.
  - Update balance at field using + change at field.
- Set balance.val\_rate from change.valuation\_rate.
- For each field in self.inventory\_dimensions.
  - Set balance at field from change.get(field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1006)

<a id="op-348e18fb013e8b"></a>
### Stock Balance Snapshot Report.get latest valuation rates

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_get_latest_valuation_rates`

**Inputs** self, rows.

**Declared result** dict.

**Explicit results** mapping() · mapping of tuple(rate.item\_code, rate.warehouse) → rate.valuation\_rate for rate drawn from rates.

**Local steps**

- Set pairs from set of tuple(row.item\_code, row.warehouse) for row drawn from rows.
  - Draw row from rows.
- If not pairs.
  - Return mapping().
- Evaluate self.conn.register(“rate\_pairs”, pa.Table.from\_pylist(list of mapping(“item\_code” → item, “warehouse” → warehouse) for tuple(item, warehouse) drawn from pairs)).
  - Draw tuple(item, warehouse) from pairs.
- Set rates from self.run\_sql(LATEST\_RATES\_SQL, mapping(“to\_date” → self.to\_date)).
- Return mapping of tuple(rate.item\_code, rate.warehouse) → rate.valuation\_rate for rate drawn from rates.
  - Draw rate from rates.

**Methods declared on this owner** [run sql](operations-073.md#op-75f0df3c0156fc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1011)

<a id="op-75f0df3c0156fc"></a>
### Stock Balance Snapshot Report.run sql

`operation_enterprise_binding_enterprise_stock_report_stock_balance_stock_balance_snapshot_stockbalancesnapshotreport_run_sql`

**Inputs** self, sql, params = no value.

**Explicit results** list of Platform.\_dict(zip(columns, row, strict = true)) for row drawn from cursor.fetchall().

**Local steps**

- Set cursor from self.conn.execute(sql, params).
- Set columns from list of column at 0 for column drawn from cursor.description.
  - Draw column from cursor.description.
- Return list of Platform.\_dict(zip(columns, row, strict = true)) for row drawn from cursor.fetchall().
  - Draw row from cursor.fetchall().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1021)

## Service · Stock balance

<a id="op-b623caae3234db"></a>
### Repost

`operation_enterprise_stock_stock_balance_business_behavior_repost`

**Inputs** only\_actual = false, allow\_negative\_stock = false, allow\_zero\_rate = false, only\_bin = false.

**Record and data access** read “Stock Settings” via get\_single\_value · execute query text (SELECT, Bin, Stock Ledger Entry).

**State and service calls** request set\_single\_value on “Stock Settings” · commit · rollback.

**Local steps**

- Set Platform.db.auto\_commit\_on\_many\_writes from 1.
- If allow\_negative\_stock.
  - Set existing\_allow\_negative\_stock from Platform.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).
  - Evaluate Platform.db.set\_single\_value(“Stock Settings”, “allow\_negative\_stock”, 1).
- Set item\_warehouses from Platform.db.sql(query text (SELECT, Bin, Stock Ledger Entry)).
- For each d in item\_warehouses.
  - Attempt the following.
    - Evaluate repost\_stock(d at 0, d at 1, allow\_zero\_rate, only\_actual, …).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
  - On failure (Exception).
    - Evaluate Platform.db.rollback().
- If allow\_negative\_stock.
  - Evaluate Platform.db.set\_single\_value(“Stock Settings”, “allow\_negative\_stock”, existing\_allow\_negative\_stock).
- Set Platform.db.auto\_commit\_on\_many\_writes from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_negative\_stock”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L703)

<a id="op-cf9365ddd8b1ae"></a>
### Repost stock

`operation_enterprise_stock_stock_balance_business_behavior_repost_stock`

**Inputs** item\_code, warehouse, allow\_zero\_rate = false, only\_actual = false, only\_bin = false, allow\_negative\_stock = false.

**Local steps**

- If not only\_bin.
  - Evaluate repost\_actual\_qty(item\_code, warehouse, allow\_zero\_rate, allow\_negative\_stock).
- If (item\_code and warehouse and not only\_actual).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → warehouse → not only\_actual.
  - Set qty\_dict from mapping(“reserved\_qty” → get\_reserved\_qty(item\_code, warehouse), “indented\_qty” → get\_indented\_qty(item\_code, warehouse), “ordered\_qty” → get\_ordered\_qty(item\_code, warehouse), “planned\_qty” → get\_planned\_ ….
  - If only\_bin.
    - Evaluate qty\_dict.update(mapping(“actual\_qty” → get\_balance\_qty\_from\_sle(item\_code, warehouse))).
  - Evaluate update\_bin\_qty(item\_code, warehouse, qty\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0934.json#L4538) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L705)

<a id="op-d32028141640ec"></a>
### Repost actual qty

`operation_enterprise_stock_stock_balance_business_behavior_repost_actual_quantity`

**Inputs** item\_code, warehouse, allow\_zero\_rate = false, allow\_negative\_stock = false.

**Local steps**

- Evaluate create\_repost\_item\_valuation\_entry(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_date” → “1900-01-01”, “posting\_time” → “00:01”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0934.json#L4943) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L704)

<a id="op-a65e94ce74e1e3"></a>
### Get balance qty from sle

`operation_enterprise_stock_stock_balance_business_behavior_get_balance_quantity_from_stock_ledger_entry`

**Inputs** item\_code, warehouse.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit results** flt(balance\_qty at 0 at 0) when balance\_qty, otherwise 0.0.

**Local steps**

- Set balance\_qty from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple(item\_code, warehouse)).
- Return flt(balance\_qty at 0 at 0) when balance\_qty, otherwise 0.0.
  - Value choice on balance\_qty — true gives flt(balance\_qty at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L696)

<a id="op-f3379c237f081d"></a>
### Get reserved qty

`operation_enterprise_stock_stock_balance_business_behavior_get_reserved_quantity`

**Inputs** item\_code, warehouse.

**Record and data access** read “Selling Settings” via get\_cached\_value.

**State and service calls** execute a supplied database query.

**Explicit results** flt(reserved\_qty at 0 at 0) when reserved\_qty, otherwise 0.

**Local steps**

- Set dont\_reserve\_on\_return from Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, “dont\_reserve\_sales\_order\_qty\_on\_sales\_return”).
- Set reserved\_qty from Platform.db.sql(formatted text   select  sum(dnpi\_qty \* ((so\_item\_qty - so\_item\_delivered\_qty - if(dont\_reserve\_qty\_on\_return, so\_item\_returned\_qty, 0)) / so\_item\_qty))  from  , tuple(item\_code, wareh ….
- Return flt(reserved\_qty at 0 at 0) when reserved\_qty, otherwise 0.
  - Value choice on reserved\_qty — true gives flt(reserved\_qty at 0 at 0), false gives 0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, “dont\_reserve\_sales\_order\_qty\_on\_sales\_return”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L701)
