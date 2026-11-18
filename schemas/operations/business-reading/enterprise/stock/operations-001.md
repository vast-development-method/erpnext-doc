# Inventory and warehouses · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Available batch report

<a id="op-095586dd11f463"></a>
### Execute

`operation_enterprise_stock_report_available_batch_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L1235) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L55)

<a id="op-ed2f8fb052840c"></a>
### Get columns

`operation_enterprise_stock_report_available_batch_report_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …)).
- If filters.show\_item\_name.
  - Evaluate columns.append(mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “Link”, “options” → “Item”, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …), mapping(“label” → translated “Batch No”, “fieldname” → “batch\_no” ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L1370) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L58)

<a id="op-9961c69885c5eb"></a>
### Get data

`operation_enterprise_stock_report_available_batch_report_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set batchwise\_data from get\_batchwise\_data\_from\_stock\_ledger(filters).
- Set batchwise\_data from get\_batchwise\_data\_from\_serial\_batch\_bundle(batchwise\_data, filters).
- Set data from parse\_batchwise\_data(batchwise\_data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L2087) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L59)

<a id="op-27695740c33498"></a>
### Parse batchwise data

`operation_enterprise_stock_report_available_batch_report_business_behavior_parse_batchwise_data`

**Inputs** batchwise\_data.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each key in batchwise\_data.
  - Set d from batchwise\_data at key.
  - <a id="op-27695740c33498-guard-5"></a>If d.balance\_qty equals 0.
    - Continue with the next iteration or loop test.
  - Evaluate data.append(d).
- Return data.

**Derived branch illustrations**

- At the comparison d.balance\_qty equals 0, d.balance\_qty = 0 selects the branch that continues with the next loop iteration. With d.balance\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-27695740c33498-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L2223) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L61)

<a id="op-a7da81e1e513af"></a>
### Get batchwise data from stock ledger

`operation_enterprise_stock_report_available_batch_report_business_behavior_get_batchwise_data_from_stock_ledger`

**Inputs** filters.

**Explicit results** batchwise\_data.

**Local steps**

- Set batchwise\_data from Platform.\_dict(mapping()).
- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set batch from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract).select(table.item\_code, table.batch\_no, table.warehouse, batch.expiry\_date, …).where(table.is\_cancelled equals 0).groupby(table.batch\_no, tabl ….
- Set query from get\_query\_based\_on\_filters(query, batch, table, filters).
- For each d in query.run(as\_dict = true).
  - Set key from tuple(d.item\_code, d.warehouse, d.batch\_no).
  - Evaluate batchwise\_data.setdefault(key, d).
- Return batchwise\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L57)

<a id="op-add9ff0e158e19"></a>
### Get batchwise data from serial batch bundle

`operation_enterprise_stock_report_available_batch_report_business_behavior_get_batchwise_data_from_serial_batch_bundle`

**Inputs** batchwise\_data, filters.

**Explicit results** batchwise\_data.

**Local steps**

- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set ch\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set batch from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract).select(table.item\_code, ch\_table.batch\_no, table.warehouse, batch.expiry\_date, …).where((table.is\_cancelled equals 0 bitwise and table.docstat ….
- Set query from get\_query\_based\_on\_filters(query, batch, table, filters).
- For each d in query.run(as\_dict = true).
  - Set key from tuple(d.item\_code, d.warehouse, d.batch\_no).
  - If key belongs to batchwise\_data.
    - Update batchwise\_data at key.balance\_qty using + flt(d.balance\_qty).
  - Otherwise.
    - Evaluate batchwise\_data.setdefault(key, d).
- Return batchwise\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L56)

<a id="op-baaf4413b7a0fe"></a>
### Get query based on filters

`operation_enterprise_stock_report_available_batch_report_business_behavior_get_query_based_on_filters`

**Inputs** query, batch, table, filters.

**Record and data access** read “Warehouse” via get\_value · read “Warehouse” via get\_all.

**Explicit results** query.

**Local steps**

- If filters.company.
  - Set query from query.where(table.company equals filters.company).
- If filters.item\_code.
  - Set query from query.where(table.item\_code equals filters.item\_code).
- If filters.batch\_no.
  - Set query from query.where(batch.name equals filters.batch\_no).
- If not filters.include\_expired\_batches.
  - Set query from query.where((batch.expiry\_date ≥ filters.to\_date bitwise or batch.expiry\_date.isnull())).
- Set to\_date from get\_datetime((str(filters.to\_date) + “ 23:59:59.999999”)).
- Set query from query.where(table.posting\_datetime ≤ to\_date).
- If filters.warehouse.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, filters.warehouse, list(“lft”, “rgt”)).
  - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“lft” → tuple(“&gt;=”, lft), “rgt” → tuple(“&lt;=”, rgt), “is\_group” → 0), pluck = “name”).
  - Set query from query.where(table.warehouse.isin(warehouses)).
- Otherwise.
  - If filters.warehouse\_type.
    - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“warehouse\_type” → filters.warehouse\_type, “is\_group” → 0), pluck = “name”).
    - Set query from query.where(table.warehouse.isin(warehouses)).
- If filters.show\_item\_name.
  - Set query from query.select(batch.item\_name).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L60)

## Report · Available serial no

<a id="op-dedd130cd77951"></a>
### Execute

`operation_enterprise_stock_report_available_serial_number_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** tuple(columns, list()) · tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate is\_reposting\_item\_valuation\_in\_progress().
- Set columns from get\_columns(filters).
- Set items from get\_items(filters).
- Set sl\_entries from get\_stock\_ledger\_entries(filters, items) when items, otherwise list().
  - Value choice on items — true gives get\_stock\_ledger\_entries(filters, items), false gives list().
- If not sl\_entries.
  - Return tuple(columns, list()).
- Set item\_details from get\_item\_details(items, sl\_entries, false).
- Set all\_entries from list(sl\_entries).
- Set opening\_row from get\_opening\_balance(filters, columns, sl\_entries).
- Set kept\_entries from set of id(sle) for sle drawn from sl\_entries.
  - Draw sle from sl\_entries.
- Set opening\_entries from list of Platform.\_dict(sle, is\_opening\_entry = 1) for sle drawn from all\_entries where id(sle) does not belong to kept\_entries.
  - Draw sle from all\_entries, keep a combination only if (id(sle) does not belong to kept\_entries).
- Set precision from cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)).
- Set data from process\_stock\_ledger\_entries(sl\_entries, item\_details, opening\_row, precision, filters = filters, opening\_entries = opening\_entries).
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L62)

<a id="op-61df658fb63014"></a>
### Process stock ledger entries

`operation_enterprise_stock_report_available_serial_number_business_behavior_process_stock_ledger_entries`

**Inputs** sl\_entries, item\_details, opening\_row, precision, filters = no value, opening\_entries = no value.

**Explicit results** data.

**Local steps**

- Set data from list().
- If opening\_row.
  - Evaluate data.append(opening\_row).
- Set bundle\_serial\_nos from mapping().
- If sabb\_list bound to list of sle.serial\_and\_batch\_bundle for sle drawn from sl\_entries where sle.serial\_and\_batch\_bundle.
  - Draw sle from sl\_entries, keep a combination only if (sle.serial\_and\_batch\_bundle).
  - Set bundle\_serial\_nos from get\_serial\_nos\_from\_sle\_list(sabb\_list).
- Set balance\_serial\_nos from mapping().
- If (filters and filters.get(“from\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“from\_date”).
  - Set balance\_serial\_nos from get\_serial\_nos\_in\_stock(filters, (sl\_entries + (opening\_entries or list()))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in opening\_entries → list().
- For each sle in sl\_entries.
  - Evaluate update\_stock\_ledger\_entry(sle, item\_details, precision).
  - Evaluate update\_available\_serial\_nos(balance\_serial\_nos, bundle\_serial\_nos, sle).
  - Evaluate data.append(sle).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L65)

<a id="op-bda91a6af3c21c"></a>
### Get serial nos in stock

`operation_enterprise_binding_enterprise_stock_report_available_serial_no_available_serial_no_get_serial_nos_in_stock`

**Inputs** filters, sl\_entries.

**Explicit results** balance\_serial\_nos.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set opening\_entries from list of row for row drawn from sl\_entries where row.is\_opening\_entry.
  - Draw row from sl\_entries, keep a combination only if (row.is\_opening\_entry).
- Set conditions from ((sle.is\_cancelled equals 0 bitwise and sle.item\_code.isin(set of row.item\_code for row drawn from sl\_entries)) bitwise and sle.warehouse.isin(set of row.warehouse for row drawn from sl\_entries)).
  - Draw row from sl\_entries.
  - Draw row from sl\_entries.
- Set before\_from\_date from sle.posting\_datetime &lt; get\_datetime((filters.from\_date + “ 00:00:00”)).
- If opening\_entries.
  - Update before\_from\_date using bitwise or sle.voucher\_no.isin(set of row.voucher\_no for row drawn from opening\_entries).
    - Draw row from opening\_entries.
- Set serial\_qty from defaultdict(float).
- For each row in get\_bundle\_serial\_qty(sle, (conditions bitwise and before\_from\_date)).
  - Update serial\_qty at tuple(row.item\_code, row.warehouse, row.serial\_no) using + flt(row.qty).
- For each row in get\_legacy\_serial\_entries(sle, (conditions bitwise and before\_from\_date)).
  - For each serial\_no in get\_serial\_nos(row.serial\_no).
    - Update serial\_qty at tuple(row.item\_code, row.warehouse, serial\_no) using + 1 when flt(row.actual\_qty) &gt; 0, otherwise negative 1.
      - Value choice on flt(row.actual\_qty) &gt; 0 — true gives 1, false gives negative 1.
- Set balance\_serial\_nos from mapping().
- For each tuple(tuple(item\_code, warehouse, serial\_no), qty) in sorted(serial\_qty.items()).
  - If qty &gt; 0.
    - Set balance\_serial\_nos.setdefault(tuple(item\_code, warehouse), mapping()) at serial\_no from no value.
- Return balance\_serial\_nos.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L944)

<a id="op-ee0473204c5e63"></a>
### Get bundle serial qty

`operation_enterprise_binding_enterprise_stock_report_available_serial_no_available_serial_no_get_bundle_serial_qty`

**Inputs** sle, conditions.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(conditions).groupby(sle.item\_code, sle.w ….

**Local steps**

- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(conditions).groupby(sle.item\_code, sle.w ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L942)

<a id="op-b069f68e9b3273"></a>
### Get legacy serial entries

`operation_enterprise_binding_enterprise_stock_report_available_serial_no_available_serial_no_get_legacy_serial_entries`

**Inputs** sle, conditions.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(sle.posting\_datetime).orderby(sle.creation).run(as\_dict = true).

**Local steps**

- Return nested operand in the contract(nested operand in the contract).orderby(sle.posting\_datetime).orderby(sle.creation).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L943)

<a id="op-bf542f64de5541"></a>
### Update stock ledger entry

`operation_enterprise_stock_report_available_serial_number_business_behavior_update_stock_ledger_entry`

**Inputs** sle, item\_details, precision.

**Local steps**

- Set item\_detail from item\_details at sle.item\_code.
- Evaluate sle.update(item\_detail).
- Evaluate sle.update(mapping(“in\_qty” → max(sle.actual\_qty, 0), “out\_qty” → min(sle.actual\_qty, 0))).
- If sle.actual\_qty.
  - Set sle at “in\_out\_rate” from flt((sle.stock\_value\_difference ÷ sle.actual\_qty), precision).
- Otherwise.
  - If sle.voucher\_type equals “Stock Reconciliation”.
    - Set sle at “in\_out\_rate” from sle.valuation\_rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L5733) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L67)

<a id="op-a3e50f473e399c"></a>
### Update available serial nos

`operation_enterprise_stock_report_available_serial_number_business_behavior_update_available_serial_numbers`

**Inputs** balance\_serial\_nos, bundle\_serial\_nos, sle.

**Local steps**

- Set serial\_nos from get\_serial\_nos(sle.serial\_no) when sle.serial\_no, otherwise bundle\_serial\_nos.get(sle.serial\_and\_batch\_bundle, list()).
  - Value choice on sle.serial\_no — true gives get\_serial\_nos(sle.serial\_no), false gives bundle\_serial\_nos.get(sle.serial\_and\_batch\_bundle, list()).
- Set sle.serial\_no from whitespace '\\n'.join(serial\_nos).
- Set balance from balance\_serial\_nos.setdefault(tuple(sle.item\_code, sle.warehouse), mapping()).
- For each serial\_no in serial\_nos.
  - If flt(sle.actual\_qty) &gt; 0.
    - Set balance at serial\_no from no value.
  - Otherwise.
    - Evaluate balance.pop(serial\_no, no value).
- Set sle.balance\_serial\_no from whitespace '\\n'.join(balance).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L66)

<a id="op-26ba7bb883d62a"></a>
### Get columns

`operation_enterprise_stock_report_available_serial_number_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Datetime”, “width” → 150), mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “ ….
- Evaluate columns.extend(list(mapping(“label” → translated “In Qty”, “fieldname” → “in\_qty”, “fieldtype” → “Float”, “width” → 80, …), mapping(“label” → translated “Out Qty”, “fieldname” → “out\_qty”, “fieldtype” → “F ….
  - Value choice on filters.valuation\_field\_type equals “Currency” — true gives “Company:company:default\_currency”, false gives no value.
  - Value choice on filters.valuation\_field\_type equals “Currency” — true gives “Company:company:default\_currency”, false gives no value.
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L63)

<a id="op-107d517292fdf4"></a>
### Get items

`operation_enterprise_stock_report_available_serial_number_business_behavior_get_items`

**Inputs** filters.

**Explicit results** query.run(pluck = true).

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name).where(item.has\_serial\_no equals 1).
- If item\_code bound to filters.get(“item\_code”).
  - Set query from query.where(item.name equals item\_code).
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0886.json#L2070) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L64)

## Record · Batch

[Record definition](../../../../data/record-types/batch.json)

<a id="op-785d9d1dc98f5c"></a>
### Get name from hash

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_name_from_hash`

**Inputs** no declared parameters.

**Record and data access** read “Batch” via exists.

**Explicit results** temp.

**Local steps**

- Set temp from no value.
- While not temp.
  - Set temp from Platform.generate\_hash() at slice no value to 7.upper().
  - If Platform.db.exists(“Batch”, temp).
    - Set temp from no value.
- Return temp.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L788)

<a id="op-5a08a48d4a39c2"></a>
### Batch uses naming series

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_uses_naming_series`

**Inputs** no declared parameters.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** bool(use\_naming\_series).

**Local steps**

- Set use\_naming\_series from cint(Platform.get\_single\_value(“Stock Settings”, “use\_naming\_series”)).
- Return bool(use\_naming\_series).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_naming\_series”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L780)

<a id="op-66f603fb9f37b3"></a>
### Get batch prefix

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_batch_prefix`

**Inputs** no declared parameters.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** naming\_series\_prefix.

**Local steps**

- Set naming\_series\_prefix from Platform.get\_single\_value(“Stock Settings”, “naming\_series\_prefix”).
- If not naming\_series\_prefix.
  - Set naming\_series\_prefix from “BATCH-”.
- Return naming\_series\_prefix.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “naming\_series\_prefix”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L267) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L785)

<a id="op-5ff8740711ffcd"></a>
### Make naming series key

`operation_enterprise_stock_record_definitions_batch_business_behavior_make_naming_series_key`

**Inputs** prefix.

**Explicit results** empty text · (“.”.join(parts) + “.#####”).

**Local steps**

- If not str(prefix).
  - Return empty text.
- Otherwise.
  - Set parts from generator of part when part.startswith(“{”), otherwise part.upper() for part drawn from prefix.split(“.”).
    - Draw part from prefix.split(“.”).
    - Value choice on part.startswith(“{”) — true gives part, false gives part.upper().
  - Return (“.”.join(parts) + “.#####”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L792)

<a id="op-8fa71695662936"></a>
### Get batch naming series

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_batch_naming_series`

**Inputs** no declared parameters.

**Explicit results** series.

**Local steps**

- Set series from empty text.
- If batch\_uses\_naming\_series().
  - Set prefix from \_get\_batch\_prefix().
  - Set key from \_make\_naming\_series\_key(prefix).
  - Set series from key.
- Return series.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L458) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L783)

<a id="op-17c463b47f2a65"></a>
### Batch.autoname

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_autoname`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “Batch” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Batch ID is mandatory”.

**Local steps**

- If self.batch\_id.
  - Set self.name from self.batch\_id.
  - Return no value.
- Set tuple(create\_new\_batch, batch\_number\_series) from Platform.db.get\_value(“Item”, self.item, list(“create\_new\_batch”, “batch\_number\_series”)).
- If not create\_new\_batch.
  - Call the validation error handler Platform.throw(translated “Batch ID is mandatory”, Platform.MandatoryError).
- While not self.batch\_id.
  - If batch\_number\_series.
    - Set self.batch\_id from make\_autoname(batch\_number\_series, doc = self).
  - Otherwise.
    - If batch\_uses\_naming\_series().
      - Set self.batch\_id from self.get\_name\_from\_naming\_series().
    - Otherwise.
      - Set self.batch\_id from get\_name\_from\_hash().
  - If Platform.db.exists(“Batch”, self.batch\_id).
    - Set self.batch\_id from no value.
- Set self.name from self.batch\_id.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get name from naming series](operations-002.md#op-d2e6acdfe46be6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L582) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L772)

<a id="op-4c8d456bf5a68e"></a>
### Batch.onload

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_onload`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Local steps**

- Set self.image from Platform.db.get\_value(“Item”, self.item, “image”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L1025) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L776)

<a id="op-2ae971832caf20"></a>
### Batch.after delete

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_after_delete`

**Inputs** self.

**Local steps**

- Evaluate revert\_series\_if\_last(get\_batch\_naming\_series(), self.name, self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L771)
