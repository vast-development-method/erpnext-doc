# Inventory and warehouses · operations 96

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock ledger invariant check

<a id="op-dbb662874ae093"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_get_stock_ledger_entries`

**Inputs** filters.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, fields = SLE\_FIELDS, filters = mapping(“item\_code” → filters.item\_code, “warehouse” → filters.warehouse, “is\_cancelled” → 0), order\_by = “posting\_datetime, creation”).

**Local steps**

- Return Platform.get\_all(“Stock Ledger Entry”, fields = SLE\_FIELDS, filters = mapping(“item\_code” → filters.item\_code, “warehouse” → filters.warehouse, “is\_cancelled” → 0), order\_by = “posting\_datetime, creation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0920.json#L1708) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L529)

<a id="op-ef41635ff77ddb"></a>
### Add invariant check fields

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_add_invariant_check_fields`

**Inputs** sles, filters.

**Record and data access** read “Warehouse” via get\_cached\_value · read “System Settings” via get\_single\_value · read “Batch” via get\_value · read “Stock Reconciliation Item” via get\_value.

**Explicit results** list() · sles at slice max((incorrect\_idx − 1), 0) to no value · sles.

**Local steps**

- Set balance\_qty from 0.0.
- Set balance\_stock\_value from 0.0.
- Set company from Platform.get\_cached\_value(“Warehouse”, filters.warehouse, “company”).
- Set valuation\_method from get\_valuation\_method(filters.item\_code, company).
- Set incorrect\_idx from no value.
- Set float\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 3.
- Set currency\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) or float\_precision).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) → float\_precision.
- For each tuple(idx, sle) in enumerate(sles).
  - If sle.batch\_no.
    - Set sle.use\_batchwise\_valuation from Platform.db.get\_value(“Batch”, sle.batch\_no, “use\_batchwise\_valuation”, cache = true).
  - If sle.actual\_qty &lt; 0.
    - Set sle.consumption\_rate from (sle.stock\_value\_difference ÷ sle.actual\_qty).
  - Update balance\_qty using + sle.actual\_qty.
  - Update balance\_stock\_value using + sle.stock\_value\_difference.
  - If (sle.voucher\_type equals “Stock Reconciliation” and not sle.batch\_no and not sle.serial\_and\_batch\_bundle and not sle.is\_adjustment\_entry).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → not sle.batch\_no → not sle.serial\_and\_batch\_bundle → not sle.is\_adjustment\_entry.
    - Set balance\_qty from Platform.db.get\_value(“Stock Reconciliation Item”, sle.voucher\_detail\_no, “qty”).
    - If balance\_qty is identical to no value.
      - Set balance\_qty from sle.qty\_after\_transaction.
  - Set sle.balance\_value\_by\_qty from (sle.stock\_value ÷ sle.qty\_after\_transaction) when sle.qty\_after\_transaction, otherwise no value.
    - Value choice on sle.qty\_after\_transaction — true gives (sle.stock\_value ÷ sle.qty\_after\_transaction), false gives no value.
  - Set sle.expected\_qty\_after\_transaction from balance\_qty.
  - Set sle.stock\_value\_from\_diff from balance\_stock\_value.
  - Set sle.difference\_in\_qty from (sle.qty\_after\_transaction − sle.expected\_qty\_after\_transaction).
  - Set sle.valuation\_diff from (sle.valuation\_rate − sle.balance\_value\_by\_qty) when sle.balance\_value\_by\_qty, otherwise no value.
    - Value choice on sle.balance\_value\_by\_qty — true gives (sle.valuation\_rate − sle.balance\_value\_by\_qty), false gives no value.
  - Set sle.diff\_value\_diff from (sle.stock\_value\_from\_diff − sle.stock\_value).
  - If maintains\_fifo\_queue(sle, valuation\_method).
    - Evaluate add\_fifo\_fields(sle, sles at (idx − 1) when idx, otherwise no value, currency\_precision).
      - Value choice on idx — true gives sles at (idx − 1), false gives no value.
  - If (incorrect\_idx is identical to no value and not is\_sle\_has\_correct\_data(sle, float\_precision, currency\_precision)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in incorrect\_idx is identical to no value → not is\_sle\_has\_correct\_data(sle, float\_precision, currency\_precision).
    - Set incorrect\_idx from idx.
- If filters.get(“show\_incorrect\_entries”).
  - If incorrect\_idx is identical to no value.
    - Return list().
  - Return sles at slice max((incorrect\_idx − 1), 0) to no value.
- Return sles.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, filters.warehouse, “company”), Platform.db.get\_single\_value(“System Settings”, “float\_precision”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L524)

<a id="op-84bfc4797493ab"></a>
### Maintains fifo queue

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_maintains_first_in_first_out_queue`

**Inputs** sle, valuation\_method.

**Explicit results** false · not (sle.serial\_and\_batch\_bundle or sle.serial\_no or (sle.batch\_no and sle.use\_batchwise\_valuation)).

**Local steps**

- If valuation\_method equals “Moving Average”.
  - Return false.
- Return not (sle.serial\_and\_batch\_bundle or sle.serial\_no or (sle.batch\_no and sle.use\_batchwise\_valuation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.serial\_and\_batch\_bundle → sle.serial\_no → (sle.batch\_no and sle.use\_batchwise\_valuation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.batch\_no → sle.use\_batchwise\_valuation.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0920.json#L2970) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L531)

<a id="op-3da0c425acea9f"></a>
### Add fifo fields

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_add_first_in_first_out_fields`

**Inputs** sle, prev\_sle, currency\_precision = no value.

**Local steps**

- Set queue from json.loads(sle.stock\_queue) when sle.stock\_queue, otherwise list().
  - Value choice on sle.stock\_queue — true gives json.loads(sle.stock\_queue), false gives list().
- Set fifo\_qty from 0.0.
- Set fifo\_value from 0.0.
- For each tuple(qty, rate) in queue.
  - Update fifo\_qty using + qty.
  - Update fifo\_value using + (qty × flt(rate)).
- Set sle.fifo\_queue\_qty from fifo\_qty.
- Set sle.fifo\_stock\_value from fifo\_value.
- Set sle.fifo\_valuation\_rate from (fifo\_value ÷ fifo\_qty) when fifo\_qty, otherwise no value.
  - Value choice on fifo\_qty — true gives (fifo\_value ÷ fifo\_qty), false gives no value.
- Set sle.fifo\_qty\_diff from (sle.qty\_after\_transaction − fifo\_qty).
- Set sle.fifo\_value\_diff from (sle.stock\_value − fifo\_value).
- Set sle.fifo\_valuation\_diff from (sle.valuation\_rate − sle.fifo\_valuation\_rate) when sle.fifo\_valuation\_rate, otherwise no value.
  - Value choice on sle.fifo\_valuation\_rate — true gives (sle.valuation\_rate − sle.fifo\_valuation\_rate), false gives no value.
- If (prev\_sle and prev\_sle.fifo\_stock\_value is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_sle → prev\_sle.fifo\_stock\_value is distinct from no value.
  - Set sle.fifo\_stock\_diff from (flt(sle.fifo\_stock\_value, currency\_precision) − flt(prev\_sle.fifo\_stock\_value, currency\_precision)).
  - Set sle.fifo\_difference\_diff from (sle.fifo\_stock\_diff − sle.stock\_value\_difference).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L523)

<a id="op-d4fc9a690fbe7e"></a>
### Is sle has correct data

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_is_stock_ledger_entry_has_correct_data`

**Inputs** sle, float\_precision, currency\_precision.

**Explicit results** (flt(sle.difference\_in\_qty, float\_precision) equals 0.0 and flt(sle.diff\_value\_diff, currency\_precision) equals 0.0 and flt(sle.fifo\_qty\_diff, float\_precision) equals 0.0 and flt(sle.fifo\_value\_diff, curre ….

**Local steps**

- Return (flt(sle.difference\_in\_qty, float\_precision) equals 0.0 and flt(sle.diff\_value\_diff, currency\_precision) equals 0.0 and flt(sle.fifo\_qty\_diff, float\_precision) equals 0.0 and flt(sle.fifo\_value\_diff, curre ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(sle.difference\_in\_qty, float\_precision) equals 0.0 → flt(sle.diff\_value\_diff, currency\_precision) equals 0.0 → flt(sle.fifo\_qty\_diff, float\_precision) equals 0.0 → flt(sle.fifo\_value\_diff, currency\_precision) equals 0.0 → flt(sle.fifo\_difference\_diff, currency\_precision) equals 0.0 → abs((flt(sle.valuation\_diff) × flt(sle.qty\_after\_transaction))) &lt; (1 ÷ (10 to the power currency\_precision)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L530)

<a id="op-6b23be712896c9"></a>
### Get columns

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “posting\_date”, “fieldtype” → “Data”, “label” →  ….

**Local steps**

- Return list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “posting\_date”, “fieldtype” → “Data”, “label” →  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0920.json#L3725) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L527)

<a id="op-2e7cdebef1de2a"></a>
### Create reposting entries

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_create_reposting_entries`

**Inputs** rows, item\_code = no value, warehouse = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → (item\_code or row.item\_code), …) via get\_doc.

**State and service calls** call submit on Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → (item\_code or row.item\_code), …)) · msgprint with translated “Reposting entries created: {0}”.format(entries).

**Local steps**

- If isinstance(rows, str).
  - Set rows from parse\_json(rows).
- Set entries from list().
- For each row in rows.
  - Set row from Platform.\_dict(row).
  - Attempt the following.
    - Set doc from Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → (item\_code or row.item\_code), …)).submit().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_code → row.item\_code.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → row.warehouse.
    - Evaluate entries.append(get\_link\_to\_form(“Repost Item Valuation”, doc.name)).
  - On failure (Platform.DuplicateEntryError).
    - Continue with the next iteration or loop test.
- If entries.
  - Set entries from “, ”.join(entries).
  - Evaluate Platform.msgprint(translated “Reposting entries created: {0}”.format(entries)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L525)

## Report · Stock ledger variance

<a id="op-482cb737201a38"></a>
### Execute

`operation_enterprise_stock_report_stock_ledger_variance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0921.json#L1667) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L551)

<a id="op-c04db1f3cfa8e2"></a>
### Get columns

`operation_enterprise_stock_report_stock_ledger_variance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “posting\_date”, “fieldtype” → “Data”, “label” →  ….

**Local steps**

- Return list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “posting\_date”, “fieldtype” → “Data”, “label” →  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0921.json#L1837) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L552)

<a id="op-3a6bb2041877d7"></a>
### Get data

`operation_enterprise_stock_report_stock_ledger_variance_business_behavior_get_data`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value · read “System Settings” via get\_single\_value.

**Explicit results** data.

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set item\_warehouse\_map from get\_item\_warehouse\_combinations(filters).
- Set valuation\_method from Platform.get\_cached\_value(“Company”, filters.get(“company”), “valuation\_method”).
- Set data from list().
- If item\_warehouse\_map.
  - Set float\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) or 3).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)) → 3.
  - Set currency\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) or float\_precision).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) → float\_precision.
  - For each item\_warehouse in item\_warehouse\_map.
    - Set report\_data from stock\_ledger\_invariant\_check(item\_warehouse).
    - If not report\_data.
      - Continue with the next iteration or loop test.
    - For each row in report\_data.
      - If has\_difference(row, float\_precision, currency\_precision, filters.difference\_in, …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_warehouse.valuation\_method → valuation\_method.
        - Evaluate row.update(mapping(“item\_code” → item\_warehouse.item\_code, “warehouse” → item\_warehouse.warehouse, “valuation\_method” → (item\_warehouse.valuation\_method or valuation\_method))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_warehouse.valuation\_method → valuation\_method.
        - Evaluate data.append(row).
        - Leave the innermost loop without its normal-exhaustion alternative.
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “valuation\_method”), Platform.db.get\_single\_value(“System Settings”, “float\_precision”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0921.json#L4288) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L553)

<a id="op-f60a56422d4ed2"></a>
### Get item warehouse combinations

`operation_enterprise_stock_report_stock_ledger_variance_business_behavior_get_item_warehouse_combinations`

**Inputs** filters = no value.

**Declared result** dict.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set bin from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set warehouse from Platform.qb.DocType(“Warehouse”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.warehouse equals nested operand in the contract.name).select(bin.item\_code, bin.warehouse, item.valuation\_me ….
- If filters.item\_code.
  - Set query from query.where(item.name equals filters.item\_code).
- If filters.warehouse.
  - Set query from query.where(warehouse.name equals filters.warehouse).
- If not filters.include\_disabled.
  - Set query from query.where((item.disabled equals 0 bitwise and warehouse.disabled equals 0)).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0921.json#L4879) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L554)

<a id="op-df247dc06e5fdf"></a>
### Has difference

`operation_enterprise_stock_report_stock_ledger_variance_business_behavior_has_difference`

**Inputs** row, float\_precision, currency\_precision, difference\_in, valuation\_method.

**Explicit results** true · false.

**Local steps**

- If valuation\_method equals “Moving Average”.
  - Set qty\_diff from flt(row.difference\_in\_qty, float\_precision).
  - Set value\_diff from flt(row.diff\_value\_diff, currency\_precision).
  - Set valuation\_diff from flt(row.valuation\_diff, currency\_precision).
- Otherwise.
  - Set qty\_diff from flt(row.difference\_in\_qty, float\_precision).
  - Set value\_diff from flt(row.diff\_value\_diff, currency\_precision).
  - Set value\_diff from (value\_diff or (flt(row.fifo\_value\_diff, currency\_precision) or flt(row.fifo\_difference\_diff, currency\_precision))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value\_diff → (flt(row.fifo\_value\_diff, currency\_precision) or flt(row.fifo\_difference\_diff, currency\_precision)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.fifo\_value\_diff, currency\_precision) → flt(row.fifo\_difference\_diff, currency\_precision).
  - Set qty\_diff from (qty\_diff or flt(row.fifo\_qty\_diff, float\_precision)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty\_diff → flt(row.fifo\_qty\_diff, float\_precision).
  - Set valuation\_diff from (flt(row.valuation\_diff, currency\_precision) or flt(row.fifo\_valuation\_diff, currency\_precision)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.valuation\_diff, currency\_precision) → flt(row.fifo\_valuation\_diff, currency\_precision).
- If (difference\_in equals “Qty” and qty\_diff).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in difference\_in equals “Qty” → qty\_diff.
  - Return true.
- Otherwise.
  - If (difference\_in equals “Value” and value\_diff).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in difference\_in equals “Value” → value\_diff.
    - Return true.
  - Otherwise.
    - If (difference\_in equals “Valuation” and valuation\_diff).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in difference\_in equals “Valuation” → valuation\_diff.
      - Return true.
    - Otherwise.
      - If (difference\_in does not belong to list(“Qty”, “Value”, “Valuation”) and (qty\_diff or value\_diff or valuation\_diff)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in difference\_in does not belong to list(“Qty”, “Value”, “Valuation”) → (qty\_diff or value\_diff or valuation\_diff).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty\_diff → value\_diff → valuation\_diff.
        - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L555)

## Report · Stock projected qty

<a id="op-1b12508b9b6c47"></a>
### Execute

`operation_enterprise_stock_report_stock_projected_quantity_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate is\_reposting\_item\_valuation\_in\_progress().
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set include\_uom from filters.get(“include\_uom”).
- Set columns from get\_columns().
- Set bin\_list from get\_bin\_list(filters).
- Set item\_map from get\_item\_map(filters.get(“item\_code”), include\_uom).
- Set item\_groups from list().
- If filters.get(“item\_group”).
  - Evaluate item\_groups.append(filters.item\_group).
  - Evaluate item\_groups.extend(get\_descendants\_of(“Item Group”, filters.item\_group)).
- Set data from list().
- Set conversion\_factors from list().
- For each bin in bin\_list.
  - Set item from item\_map.get(bin.item\_code).
  - If not item.
    - Continue with the next iteration or loop test.
  - If (filters.brand and filters.brand differs from item.brand).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.brand → filters.brand differs from item.brand.
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If (item\_groups and item.item\_group does not belong to item\_groups).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_groups → item.item\_group does not belong to item\_groups.
      - Continue with the next iteration or loop test.
  - Set re\_order\_level, re\_order\_qty from 0.
  - For each d in item.get(“reorder\_levels”).
    - If d.warehouse equals bin.warehouse.
      - Set re\_order\_level from d.warehouse\_reorder\_level.
      - Set re\_order\_qty from d.warehouse\_reorder\_qty.
  - Set reserved\_qty\_for\_pos from get\_pos\_reserved\_qty(bin.item\_code, bin.warehouse).
  - If reserved\_qty\_for\_pos.
    - Update bin.projected\_qty using − reserved\_qty\_for\_pos.
  - Set shortage\_qty from 0.
  - If ((re\_order\_level or re\_order\_qty) and re\_order\_level &gt; bin.projected\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (re\_order\_level or re\_order\_qty) → re\_order\_level &gt; bin.projected\_qty.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in re\_order\_level → re\_order\_qty.
    - Set shortage\_qty from (re\_order\_level − flt(bin.projected\_qty)).
  - Evaluate data.append(list(item.name, item.item\_name, item.description, item.item\_group, …)).
  - If include\_uom.
    - Evaluate conversion\_factors.append(item.conversion\_factor).
- Evaluate update\_included\_uom\_in\_report(columns, data, include\_uom, conversion\_factors).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L557)

<a id="op-a0b8a722894617"></a>
### Get columns

`operation_enterprise_stock_report_stock_projected_quantity_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “width” → 100),  ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “width” → 100),  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L559)

<a id="op-b122729ac4af18"></a>
### Get bin list

`operation_enterprise_stock_report_stock_projected_quantity_business_behavior_get_bin_list`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** bin\_list.

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract.qb.from\_(bin).select(bin.item\_code, bin.warehouse, bin.actual\_qty, bin.planned\_qty, …).orderby(bin.item\_code, bin.warehouse).
- If filters.item\_code.
  - Set query from query.where(bin.item\_code equals filters.item\_code).
- If filters.company.
  - Set wh from Platform.qb.DocType(“Warehouse”).
  - Set query from query.where(ExistsCriterion(nested operand in the contract(nested operand in the contract).select(wh.name).where((wh.name equals bin.warehouse bitwise and wh.company equals filters.company)))).
- If filters.warehouse.
  - Set warehouse\_details from Platform.db.get\_value(“Warehouse”, filters.warehouse, list(“lft”, “rgt”), as\_dict = 1).
  - If warehouse\_details.
    - Set wh from Platform.qb.DocType(“Warehouse”).
    - Set query from query.where(ExistsCriterion(nested operand in the contract(nested operand in the contract).select(wh.name).where(((nested operand in the contract.lft ≥ nested operand in the contract.lft bitwise and nested ….
- Set bin\_list from query.run(as\_dict = true).
- Return bin\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0922.json#L3766) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L558)

<a id="op-d98794cbbedac4"></a>
### Get item map

`operation_enterprise_stock_report_stock_projected_quantity_business_behavior_get_item_map`

**Inputs** item\_code, include\_uom.

**Explicit results** item\_map.

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name, item.item\_name, item.description, item.item\_group, …).where((((item.is\_stock\_item equals 1 bitwise and item.disabled equals 0) bitwise and (( ….
- If item\_code.
  - Set query from query.where(item.item\_code equals item\_code).
- If include\_uom.
  - Set ucd from Platform.qb.DocType(“UOM Conversion Detail”).
  - Set query from query.select(ucd.conversion\_factor).
  - Set query from query.left\_join(ucd).on((ucd.parent equals item.name bitwise and ucd.uom equals include\_uom)).
- Set items from query.run(as\_dict = true).
- Set ir from Platform.qb.DocType(“Item Reorder”).
- Set query from Platform.qb.from\_(ir).select(“\*”).
- If item\_code.
  - Set query from query.where(ir.parent equals item\_code).
- Set reorder\_levels from Platform.\_dict().
- For each d in query.run(as\_dict = true).
  - If d.parent does not belong to reorder\_levels.
    - Set reorder\_levels at d.parent from list().
  - Evaluate reorder\_levels at d.parent.append(d).
- Set item\_map from Platform.\_dict().
- For each item in items.
  - Set item at “reorder\_levels” from (reorder\_levels.get(item.name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reorder\_levels.get(item.name) → list().
  - Set item\_map at item.name from item.
- Return item\_map.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L560)

## Report · Stock qty vs batch qty

<a id="op-ab051097adf549"></a>
### Execute

`operation_enterprise_stock_report_stock_quantity_vs_batch_quantity_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L528) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L567)

<a id="op-eff5e01a813e39"></a>
### Get columns

`operation_enterprise_stock_report_stock_quantity_vs_batch_quantity_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L654) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L568)

<a id="op-c9a84611232f69"></a>
### Get data

`operation_enterprise_stock_report_stock_quantity_vs_batch_quantity_business_behavior_get_data`

**Inputs** filters = no value.

**Explicit results** result.

**Local steps**

- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set item from filters.get(“item”).
- Set batch\_no from filters.get(“batch”).
- Set batch\_sle\_data from (get\_batch\_qty\_for\_stock(item\_code = item, batch\_no = batch\_no, for\_stock\_levels = true, consider\_negative\_batches = true, …) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_batch\_qty\_for\_stock(item\_code = item, batch\_no = batch\_no, for\_stock\_levels = true, consider\_negative\_batches = true, …) → list().
- Set stock\_qty\_map from mapping().
- For each row in batch\_sle\_data.
  - Set batch from row.get(“batch\_no”).
  - If not batch.
    - Continue with the next iteration or loop test.
  - Set stock\_qty\_map at batch from (stock\_qty\_map.get(batch, 0) + (row.get(“qty”) or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“qty”) → 0.
- Set batch from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract.qb.from\_(batch).select(batch.name, batch.item, batch.item\_name, batch.batch\_qty).where(batch.disabled equals 0).
- If item.
  - Set query from query.where(batch.item equals item).
- If batch\_no.
  - Set query from query.where(batch.name equals batch\_no).
- If condition bound to get\_allowed\_masters\_condition(batch.item, “Item”).
  - Set query from query.where(condition).
- Set batch\_records from (query.run(as\_dict = true) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) → list().
- Set result from list().
- For each row in batch\_records.
  - Set name from row.get(“name”).
  - Set batch\_qty from (row.get(“batch\_qty”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“batch\_qty”) → 0.
  - Set stock\_qty from stock\_qty\_map.get(name, 0).
  - Set difference from (stock\_qty − batch\_qty).
  - If difference differs from 0.
    - Evaluate result.append(mapping(“item\_code” → row.get(“item”), “item\_name” → row.get(“item\_name”), “batch” → name, “batch\_qty” → batch\_qty, …)).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L569)

<a id="op-b19d6cae17407c"></a>
### Update batch qty

`operation_enterprise_stock_report_stock_quantity_vs_batch_quantity_business_behavior_update_batch_quantity`

**Inputs** selected\_batches = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Batch” · msgprint with translated “Batch Qty updated successfully”.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.has\_permission(“Batch”, “write”, throw = true, ignore\_share\_permissions = true).
- If not selected\_batches.
  - Return no value.
- Set selected\_batches from json.loads(selected\_batches).
- For each row in selected\_batches.
  - Set batch\_name from row.get(“batch”).
  - Set batches from get\_batch\_qty\_for\_stock(batch\_no = batch\_name, item\_code = row.get(“item\_code”), for\_stock\_levels = true, consider\_negative\_batches = true, …).
  - Set batch\_qty from 0.0.
  - If batches.
    - For each batch in batches.
      - Update batch\_qty using + batch.get(“qty”).
  - Evaluate Platform.db.set\_value(“Batch”, batch\_name, “batch\_qty”, batch\_qty).
- Evaluate Platform.msgprint(translated “Batch Qty updated successfully”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “write”, throw = true, ignore\_share\_permissions = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L570)

## Report · Stock qty vs serial no count

<a id="op-ab36bf017253b3"></a>
### Execute

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_warehouse(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters.warehouse, filters.show\_disabled\_items).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L3854) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L571)

<a id="op-b0c689a3758ac4"></a>
### Validate warehouse

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_validate_warehouse`

**Inputs** filters.

**Record and data access** read “Warehouse” via exists.

**Explicit failure paths** validation helper — translated “Warehouse: {0} does not belong to {1}”.format(warehouse, company).

**Local steps**

- Set company from filters.company.
- Set warehouse from filters.warehouse.
- If not Platform.db.exists(“Warehouse”, mapping(“name” → warehouse, “company” → company)).
  - Call the validation error handler Platform.throw(translated “Warehouse: {0} does not belong to {1}”.format(warehouse, company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L3986) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L583)

<a id="op-5ff02e130df1cf"></a>
### Get columns

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L4187) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L572)

<a id="op-9ec4a9291f6bb2"></a>
### Get warehouses

`operation_enterprise_stock_report_stock_quantity_vs_serial_number_count_business_behavior_get_warehouses`

**Inputs** warehouse.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** get\_child\_warehouses(warehouse) · list(warehouse).

**Local steps**

- If Platform.db.get\_value(“Warehouse”, warehouse, “is\_group”).
  - Bind dependencies get\_child\_warehouses.
  - Return get\_child\_warehouses(warehouse).
- Return list(warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0923.json#L4688) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L577)
