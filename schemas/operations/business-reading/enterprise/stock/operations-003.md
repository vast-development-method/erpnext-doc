# Inventory and warehouses · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Batch item expiry status

<a id="op-638ac67a50e54b"></a>
### Get batch details

`operation_enterprise_stock_report_batch_item_expiry_status_business_behavior_get_batch_details`

**Inputs** filters.

**Explicit results** list of batch for batch drawn from batches where flt(batch.batch\_qty) &gt; 0.

**Local steps**

- Set batch from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If filters.get(“item”).
  - Set query from query.where(batch.item equals filters at “item”).
- If condition bound to get\_allowed\_masters\_condition(batch.item, “Item”).
  - Set query from query.where(condition).
- Set batches from query.run(as\_dict = true).
- Evaluate set\_permitted\_batch\_qty(batches).
- Return list of batch for batch drawn from batches where flt(batch.batch\_qty) &gt; 0.
  - Draw batch from batches, keep a combination only if (flt(batch.batch\_qty) &gt; 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L71)

<a id="op-b60997af18b7e7"></a>
### Set permitted batch qty

`operation_enterprise_binding_enterprise_stock_report_batch_item_expiry_status_batch_item_expiry_status_set_permitted_batch_qty`

**Inputs** batches.

**Explicit results** no value.

**Local steps**

- Set warehouses from get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Stock Ledger Entry”).
- If (not batches or not warehouses).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not batches → not warehouses.
  - Return no value.
- Set batch\_qty from get\_batch\_qty\_in\_warehouses(list of batch.name for batch drawn from batches, warehouses).
  - Draw batch from batches.
- For each batch in batches.
  - Set batch.batch\_qty from batch\_qty.get(batch.name, 0.0).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L946)

<a id="op-8cbd17e00d01a2"></a>
### Get batch qty in warehouses

`operation_enterprise_binding_enterprise_stock_report_batch_item_expiry_status_batch_item_expiry_status_get_batch_qty_in_warehouses`

**Inputs** batch\_nos, warehouses.

**Explicit results** batch\_qty.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set condition from (sle.is\_cancelled equals 0 bitwise and sle.warehouse.isin(warehouses)).
- Set bundle\_qty from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((condition bitwise and nested operand in the contract(nested operand in the contract))).groupby(entry.ba …().
- Set ledger\_qty from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().
- Set batch\_qty from defaultdict(float).
- For each tuple(batch\_no, qty) in list(expanded bundle\_qty, expanded ledger\_qty).
  - Update batch\_qty at batch\_no using + flt(qty).
- Return batch\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L945)

## Report · Batch wise balance history

<a id="op-6519061250c7a6"></a>
### Execute

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Please select either the Item or Warehouse or Warehouse Type filter to generate the report.”.

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set sle\_count from Platform.db.estimate\_count(“Stock Ledger Entry”).
- If (sle\_count &gt; SLE\_COUNT\_LIMIT and not filters.get(“item\_code”) and not filters.get(“warehouse”) and not filters.get(“warehouse\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle\_count &gt; SLE\_COUNT\_LIMIT → not filters.get(“item\_code”) → not filters.get(“warehouse”) → not filters.get(“warehouse\_type”).
  - Call the validation error handler Platform.throw(translated “Please select either the Item or Warehouse or Warehouse Type filter to generate the report.”).
- Evaluate validate\_mandatory\_date\_range(filters).
- Set float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 3.
- Set columns from get\_columns(filters).
- Set item\_map from get\_item\_details(filters).
- Set iwb\_map from get\_item\_warehouse\_batch\_map(filters, float\_precision).
- Set data from list().
- For each item in sorted(iwb\_map).
  - If (not filters.get(“item”) or filters.get(“item”) equals item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“item”) → filters.get(“item”) equals item.
    - For each wh in sorted(iwb\_map at item).
      - For each batch in sorted(iwb\_map at item at wh).
        - Set qty\_dict from iwb\_map at item at wh at batch.
        - If (qty\_dict.opening\_qty or qty\_dict.in\_qty or qty\_dict.out\_qty or qty\_dict.bal\_qty).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty\_dict.opening\_qty → qty\_dict.in\_qty → qty\_dict.out\_qty → qty\_dict.bal\_qty.
          - Evaluate data.append(list(item, item\_map at item at “item\_name”, item\_map at item at “description”, wh, …)).
            - Value choice on qty\_dict.bal\_qty — true gives (qty\_dict.bal\_value ÷ qty\_dict.bal\_qty), false gives 0.
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0887.json#L994) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L77)

<a id="op-8278af52d8a953"></a>
### Get columns

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Item” + “:Link/Item:100”), (translated “Item Name” + “::120”), (translated “Description” + “::90”), (translated “Warehouse” + “:Link/Warehouse:100”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0887.json#L1968) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L78)

<a id="op-cb1b896556a3f3"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_stock_ledger_entries`

**Inputs** filters.

**Explicit results** entries.

**Local steps**

- Set entries from list().
- Set stk\_cl\_obj from StockClosing(filters.company, filters.from\_date, filters.from\_date).
- If stk\_cl\_obj.last\_closing\_balance.
  - Update entries using + get\_stock\_closing\_balance(stk\_cl\_obj, filters).
  - Set filters.start\_from from stk\_cl\_obj.last\_closing\_balance.to\_date.
- Update entries using + get\_stock\_ledger\_entries\_for\_batch\_no(filters).
- Update entries using + get\_stock\_ledger\_entries\_for\_batch\_bundle(filters).
- Return entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0887.json#L2341) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L82)

<a id="op-e01e93671a74b3"></a>
### Get stock closing balance

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_stock_closing_balance`

**Inputs** stk\_cl\_obj, filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** stk\_cl\_obj.get\_stock\_closing\_balance(query\_filters, for\_batch = true).

**Local steps**

- Set query\_filters from mapping().
- For each field in list(“item\_code”, “warehouse”, “company”, “batch\_no”).
  - If filters.get(field).
    - Set query\_filters at field from filters.get(field).
- If filters.warehouse\_type.
  - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“warehouse\_type” → filters.warehouse\_type, “is\_group” → 0), pluck = “name”).
  - Set query\_filters at “warehouse” from warehouses.
- Return stk\_cl\_obj.get\_stock\_closing\_balance(query\_filters, for\_batch = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0887.json#L2559) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L81)

<a id="op-757ec9601cb2fe"></a>
### Get stock ledger entries for batch no

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_stock_ledger_entries_for_batch_number`

**Inputs** filters.

**Wrappers, in declaration order** record a compatibility advisory for the invoked interface.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** (query.run(as\_dict = true) or list()).

**Explicit failure paths** validation helper — translated “'From Date' is required” · validation helper — translated “'To Date' is required”.

**Local steps**

- If not filters.get(“from\_date”).
  - Call the validation error handler Platform.throw(translated “'From Date' is required”).
- If not filters.get(“to\_date”).
  - Call the validation error handler Platform.throw(translated “'To Date' is required”).
- Set posting\_datetime from get\_datetime(add\_to\_date(filters at “to\_date”, days = 1)).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, sle.batch\_no, sle.posting\_date, …).where((((nested operand in the contract &lt; nested operand in the contra ….
- Set query from apply\_warehouse\_filter(query, sle, filters).
- If (filters.warehouse\_type and not filters.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.warehouse\_type → not filters.warehouse.
  - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“warehouse\_type” → filters.warehouse\_type, “is\_group” → 0), pluck = “name”).
  - If warehouses.
    - Set query from query.where(sle.warehouse.isin(warehouses)).
- For each field in list(“item\_code”, “batch\_no”, “company”).
  - If filters.get(field).
    - Set query from query.where(sle at field equals filters.get(field)).
- If filters.start\_from.
  - Set query from query.where(sle.posting\_datetime &gt; get\_datetime(filters.start\_from)).
- If filters.to\_datetime.
  - Set query from query.where(sle.posting\_datetime ≤ get\_datetime(filters.to\_datetime)).
- Return (query.run(as\_dict = true) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L84)

<a id="op-dd314ad9232e89"></a>
### Get stock ledger entries for batch bundle

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_stock_ledger_entries_for_batch_bundle`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** (query.run(as\_dict = true) or list()).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch\_package from Platform.qb.DocType(“Serial and Batch Entry”).
- Set to\_date from get\_datetime((str(filters.to\_date) + “ 23:59:59.999999”)).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, batch\_package.batch\_no, sle.posting\_date, …).where((((nested operand in the contract &lt; nested operand in  ….
- Set query from apply\_warehouse\_filter(query, sle, filters).
- If (filters.warehouse\_type and not filters.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.warehouse\_type → not filters.warehouse.
  - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“warehouse\_type” → filters.warehouse\_type, “is\_group” → 0), pluck = “name”).
  - If warehouses.
    - Set query from query.where(sle.warehouse.isin(warehouses)).
- For each field in list(“item\_code”, “batch\_no”, “company”).
  - If filters.get(field).
    - If field equals “batch\_no”.
      - Set query from query.where(batch\_package at field equals filters.get(field)).
    - Otherwise.
      - Set query from query.where(sle at field equals filters.get(field)).
- If filters.start\_from.
  - Set query from query.where(sle.posting\_date &gt; getdate(filters.start\_from)).
- If filters.to\_datetime.
  - Set query from query.where(sle.posting\_datetime ≤ get\_datetime(filters.to\_datetime)).
- Return (query.run(as\_dict = true) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L83)

<a id="op-94773549802d55"></a>
### Get item warehouse batch map

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_item_warehouse_batch_map`

**Inputs** filters, float\_precision.

**Explicit results** iwb\_map.

**Local steps**

- Set sle from get\_stock\_ledger\_entries(filters).
- Set iwb\_map from mapping().
- Set from\_date from getdate(filters at “from\_date”).
- Set to\_date from getdate(filters at “to\_date”).
- For each d in sle.
  - Evaluate iwb\_map.setdefault(d.item\_code, mapping()).setdefault(d.warehouse, mapping()).setdefault(d.batch\_no, Platform.\_dict(mapping(“opening\_qty” → 0.0, “in\_qty” → 0.0, “out\_qty” → 0.0, “bal\_qty” → 0.0, …))).
  - Set qty\_dict from iwb\_map at d.item\_code at d.warehouse at d.batch\_no.
  - If d.posting\_date &lt; from\_date.
    - Set qty\_dict.opening\_qty from (flt(qty\_dict.opening\_qty, float\_precision) + flt(d.actual\_qty, float\_precision)).
  - Otherwise.
    - If (d.posting\_date ≥ from\_date and d.posting\_date ≤ to\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.posting\_date ≥ from\_date → d.posting\_date ≤ to\_date.
      - If flt(d.actual\_qty) &gt; 0.
        - Set qty\_dict.in\_qty from (flt(qty\_dict.in\_qty, float\_precision) + flt(d.actual\_qty, float\_precision)).
      - Otherwise.
        - Set qty\_dict.out\_qty from (flt(qty\_dict.out\_qty, float\_precision) + abs(flt(d.actual\_qty, float\_precision))).
  - Set qty\_dict.bal\_qty from (flt(qty\_dict.bal\_qty, float\_precision) + flt(d.actual\_qty, float\_precision)).
  - Update qty\_dict.bal\_value using + flt(d.stock\_value\_difference).
- Evaluate set\_pooled\_batch\_values(filters, iwb\_map).
- Return iwb\_map.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L80)

<a id="op-36d41eaa984cbe"></a>
### Set pooled batch values

`operation_enterprise_binding_enterprise_stock_report_batch_wise_balance_history_batch_wise_balance_history_set_pooled_batch_values`

**Inputs** filters, iwb\_map.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set moving\_average\_is\_pooled from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).
- Set pooled\_items from list of item for item drawn from iwb\_map where is\_pooled(item, filters.company, moving\_average\_is\_pooled).
  - Draw item from iwb\_map, keep a combination only if (is\_pooled(item, filters.company, moving\_average\_is\_pooled)).
- If not pooled\_items.
  - Return no value.
- Set warehouses from set of warehouse for item drawn from pooled\_items, then warehouse drawn from iwb\_map at item.
  - Draw item from pooled\_items.
  - Draw warehouse from iwb\_map at item.
- Set cutoff from get\_datetime((filters.to\_datetime or formatted text {filters.to\_date} 23:59:59.999999)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.to\_datetime → formatted text {filters.to\_date} 23:59:59.999999.
- Set rates from get\_last\_valuation\_rates(pooled\_items, warehouses, cutoff).
- For each item in pooled\_items.
  - For each tuple(warehouse, batches) in iwb\_map at item.items().
    - Set rate from flt(rates.get(tuple(item, warehouse))).
    - For each balance in batches.values().
      - Set balance.bal\_value from (balance.bal\_qty × rate).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L949)

<a id="op-f229c2df836d5e"></a>
### Get last valuation rates

`operation_enterprise_binding_enterprise_stock_report_batch_wise_balance_history_batch_wise_balance_history_get_last_valuation_rates`

**Inputs** items, warehouses, cutoff.

**Explicit results** mapping of tuple(row.item\_code, row.warehouse) → row.valuation\_rate for row drawn from rows.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set ranked from nested operand in the contract.qb.from\_(sle).select(sle.item\_code, sle.warehouse, sle.valuation\_rate, nested operand in the contract.orderby(nested operand in the contract.posting\_datetime, nested operand  ….
- Set rows from nested operand in the contract(nested operand in the contract).select(ranked.item\_code, ranked.warehouse, ranked.valuation\_rate).where(ranked.row\_no equals 1).run(as\_dict = true).
- Return mapping of tuple(row.item\_code, row.warehouse) → row.valuation\_rate for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L947)

<a id="op-c5b5f0a832f96b"></a>
### Is pooled

`operation_enterprise_binding_enterprise_stock_report_batch_wise_balance_history_batch_wise_balance_history_is_pooled`

**Inputs** item, company, moving\_average\_is\_pooled.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** not serial\_no\_wise · (moving\_average\_is\_pooled and get\_valuation\_method(item, company) equals “Moving Average”).

**Local steps**

- Set tuple(has\_serial\_no, serial\_no\_wise) from Platform.get\_cached\_value(“Item”, item, list(“has\_serial\_no”, “use\_serial\_no\_wise\_valuation”)).
- If has\_serial\_no.
  - Return not serial\_no\_wise.
- Return (moving\_average\_is\_pooled and get\_valuation\_method(item, company) equals “Moving Average”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in moving\_average\_is\_pooled → get\_valuation\_method(item, company) equals “Moving Average”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item, list(“has\_serial\_no”, “use\_serial\_no\_wise\_valuation”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L948)

<a id="op-de4411440c76f7"></a>
### Get item details

`operation_enterprise_stock_report_batch_wise_balance_history_business_behavior_get_item_details`

**Inputs** filters.

**Explicit results** item\_map.

**Local steps**

- Set item\_map from mapping().
- For each d in nested operand in the contract.qb.from\_(“Item”).select(“name”, “item\_name”, “description”, “stock\_uom”).run(as\_dict = 1).
  - Evaluate item\_map.setdefault(d.name, d).
- Return item\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0887.json#L6005) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L79)

## Record · Bin

[Record definition](../../../../data/record-types/bin.json)

<a id="op-725b04392b1840"></a>
### Bin.recalculate values

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_recalculate_values`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- Evaluate Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true).
- Evaluate self.reload().
- Evaluate self.set\_stock\_values\_from\_ledger().
- Evaluate self.set\_pending\_and\_reserved\_qty().
- Evaluate self.set\_projected\_qty().
- Evaluate update\_bin\_columns(self.name, mapping of fieldname → flt(self.get(fieldname)) for fieldname drawn from RECALCULATED\_FIELDS).
  - Draw fieldname from RECALCULATED\_FIELDS.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set stock values from ledger](operations-003.md#op-78c16d28a76e91), [set pending and reserved qty](operations-003.md#op-2c10738727e352), [set projected qty](operations-003.md#op-5ccf68e09d9a15).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L821)

<a id="op-78c16d28a76e91"></a>
### Bin.set stock values from ledger

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_bin_set_stock_values_from_ledger`

**Inputs** self.

**Local steps**

- Set last\_sle from get\_last\_sle\_values(self.item\_code, self.warehouse).
- Set self.actual\_qty from last\_sle.qty\_after\_transaction.
- Set self.valuation\_rate from last\_sle.valuation\_rate.
- Set self.stock\_value from last\_sle.stock\_value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L201)

<a id="op-2c10738727e352"></a>
### Bin.set pending and reserved qty

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_bin_set_pending_and_reserved_qty`

**Inputs** self.

**Local steps**

- Bind dependencies get\_reserved\_qty\_for\_production.
- Bind dependencies get\_indented\_qty, get\_ordered\_qty, get\_planned\_qty, get\_reserved\_qty.
- Set self.planned\_qty from get\_planned\_qty(self.item\_code, self.warehouse).
- Set self.indented\_qty from get\_indented\_qty(self.item\_code, self.warehouse).
- Set self.ordered\_qty from get\_ordered\_qty(self.item\_code, self.warehouse).
- Set self.reserved\_qty from get\_reserved\_qty(self.item\_code, self.warehouse).
- Set self.reserved\_qty\_for\_production from get\_reserved\_qty\_for\_production(self.item\_code, self.warehouse).
- Evaluate self.update\_reserved\_qty\_for\_sub\_contracting(update\_qty = false).
- Evaluate self.update\_reserved\_qty\_for\_production\_plan(skip\_project\_qty\_update = true, update\_qty = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty for sub contracting](operations-003.md#op-e097dd50393349), [update reserved qty for production plan](operations-003.md#op-31c903ad9f9752).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L200)

<a id="op-be15eecedb3f34"></a>
### Bin.before save

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_before_save`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If (self.get(“\_\_islocal”) or not self.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → not self.stock\_uom.
  - Set self.stock\_uom from Platform.get\_cached\_value(“Item”, self.item\_code, “stock\_uom”).
- Evaluate self.set\_projected\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set projected qty](operations-003.md#op-5ccf68e09d9a15).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L4687) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L820)

<a id="op-5ccf68e09d9a15"></a>
### Bin.set projected qty

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_set_projected_quantity`

**Inputs** self.

**Local steps**

- Set self.projected\_qty from (((((((nested operand in the contract + nested operand in the contract) + nested operand in the contract(nested operand in the contract)) + flt(nested operand in the contract.planned\_qty)) − flt(self.reser ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L4838) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L822)

<a id="op-31c903ad9f9752"></a>
### Bin.update reserved qty for production plan

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_update_reserved_quantity_for_production_plan`

**Inputs** self, skip\_project\_qty\_update = false, update\_qty = true.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_reserved\_qty\_for\_production\_plan.
- Set reserved\_qty\_for\_production\_plan from get\_reserved\_qty\_for\_production\_plan(self.item\_code, self.warehouse).
- If (reserved\_qty\_for\_production\_plan is identical to no value and not self.reserved\_qty\_for\_production\_plan).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reserved\_qty\_for\_production\_plan is identical to no value → not self.reserved\_qty\_for\_production\_plan.
  - Return no value.
- Set self.reserved\_qty\_for\_production\_plan from flt(reserved\_qty\_for\_production\_plan).
- If update\_qty.
  - Evaluate self.db\_set(“reserved\_qty\_for\_production\_plan”, flt(self.reserved\_qty\_for\_production\_plan), update\_modified = true).
- If not skip\_project\_qty\_update.
  - Evaluate self.set\_projected\_qty().
  - Evaluate self.db\_set(“projected\_qty”, self.projected\_qty, update\_modified = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set projected qty](operations-003.md#op-5ccf68e09d9a15).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L5065) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L825)

<a id="op-e7e827276fa106"></a>
### Bin.update reserved qty for for sub assembly

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_update_reserved_quantity_for_for_subordinate_assembly`

**Inputs** self.

**Wrappers, in declaration order** record a compatibility advisory for the invoked interface.

**Local steps**

- Evaluate self.update\_reserved\_qty\_for\_production\_plan().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty for production plan](operations-003.md#op-31c903ad9f9752).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L823)

<a id="op-6e9691d14a8baf"></a>
### Bin.update reserved qty for production

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_update_reserved_quantity_for_production`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies get\_reserved\_qty\_for\_production.
- Set self.reserved\_qty\_for\_production from get\_reserved\_qty\_for\_production(self.item\_code, self.warehouse).
- Evaluate self.db\_set(“reserved\_qty\_for\_production”, flt(self.reserved\_qty\_for\_production), update\_modified = true).
- Evaluate self.update\_reserved\_qty\_for\_production\_plan(skip\_project\_qty\_update = true).
- Evaluate self.set\_projected\_qty().
- Evaluate self.db\_set(“projected\_qty”, self.projected\_qty, update\_modified = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty for production plan](operations-003.md#op-31c903ad9f9752), [set projected qty](operations-003.md#op-5ccf68e09d9a15).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L5644) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L824)

<a id="op-e097dd50393349"></a>
### Bin.update reserved qty for sub contracting

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_update_reserved_quantity_for_subordinate_contracting`

**Inputs** self, subcontract\_doctype = “Subcontracting Order”, update\_qty = true.

**State and service calls** call db\_set on self.

**Local steps**

- Set subcontract\_order from Platform.qb.DocType(subcontract\_doctype).
- Set supplied\_item from Platform.qb.DocType(“Purchase Order Item Supplied” when subcontract\_doctype equals “Purchase Order”, otherwise “Subcontracting Order Supplied Item”).
  - Value choice on subcontract\_doctype equals “Purchase Order” — true gives “Purchase Order Item Supplied”, false gives “Subcontracting Order Supplied Item”.
- Set pending\_qty\_per\_order from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract when nested oper ….
  - Value choice on subcontract\_doctype equals “Purchase Order” — true gives ((subcontract\_order.is\_old\_subcontracting\_flow equals 1 bitwise and subcontract\_order.status differs from “Closed”) bitwise and subcontract\_order.docstatus equals 1), false gives (subcontract\_order.status differs from “Closed” bitwise and subcontract\_order.docstatus equals 1).
- Set reserved\_qty\_for\_sub\_contract from sum(generator of max(flt(qty), 0) for qty drawn from pending\_qty\_per\_order).
  - Draw qty from pending\_qty\_per\_order.
- Set self.reserved\_qty\_for\_sub\_contract from reserved\_qty\_for\_sub\_contract.
- If update\_qty.
  - Evaluate self.db\_set(“reserved\_qty\_for\_sub\_contract”, reserved\_qty\_for\_sub\_contract, update\_modified = true).
  - Evaluate self.set\_projected\_qty().
  - Evaluate self.db\_set(“projected\_qty”, self.projected\_qty, update\_modified = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set projected qty](operations-003.md#op-5ccf68e09d9a15).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L826)

<a id="op-115363e7a47d38"></a>
### Bin.update reserved stock

`operation_enterprise_stock_record_definitions_bin_business_behavior_bin_update_reserved_stock`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies get\_sre\_reserved\_qty\_for\_item\_and\_warehouse.
- Set reserved\_stock from get\_sre\_reserved\_qty\_for\_item\_and\_warehouse(self.item\_code, self.warehouse).
- Evaluate self.db\_set(“reserved\_stock”, flt(reserved\_stock), update\_modified = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L7282) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L827)
