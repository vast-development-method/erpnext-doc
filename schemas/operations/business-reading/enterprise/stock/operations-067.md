# Inventory and warehouses · operations 67

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock

<a id="op-d31436a5ea3bfa"></a>
### Get warehouse account map

`operation_enterprise_stock_initialize_business_behavior_get_warehouse_account_map`

**Inputs** company = no value.

**Record and data access** read “Warehouse” via get\_all · read “Account” via get\_value.

**Explicit results** Platform.flags.warehouse\_account\_map.get(company, Platform.\_dict()) · Platform.flags.warehouse\_account\_map.

**Local steps**

- Set company\_warehouse\_account\_map from (company and Platform.flags.setdefault(“warehouse\_account\_map”, mapping()).get(company)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → Platform.flags.setdefault(“warehouse\_account\_map”, mapping()).get(company).
- Set warehouse\_account\_map from Platform.flags.warehouse\_account\_map.
- If (not warehouse\_account\_map or not company\_warehouse\_account\_map or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not warehouse\_account\_map → not company\_warehouse\_account\_map → Platform.in\_test.
  - Set warehouse\_account from Platform.\_dict().
  - Set filters from mapping().
  - If company.
    - Set filters at “company” from company.
    - Evaluate Platform.flags.setdefault(“warehouse\_account\_map”, mapping()).setdefault(company, mapping()).
  - Set warehouses from Platform.get\_all(“Warehouse”, fields = list(“name”, “account”, “parent\_warehouse”, “company”, …), filters = filters, order\_by = “lft, rgt”).
  - Set stock\_accounts from mapping of company\_name → get\_company\_stock\_accounts(company\_name) for company\_name drawn from set of d.company for d drawn from warehouses where (d.company and not d.account).
    - Draw company\_name from set of d.company for d drawn from warehouses where (d.company and not d.account).
    - Draw d from warehouses, keep a combination only if ((d.company and not d.account)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.company → not d.account.
  - For each d in warehouses.
    - If not d.account.
      - Set d.account from get\_warehouse\_account(d, warehouse\_account, raise\_error = false, stock\_accounts = stock\_accounts.get(d.company, list())).
    - If d.account.
      - Set d.account\_currency from Platform.db.get\_value(“Account”, d.account, “account\_currency”, cache = true).
      - Evaluate warehouse\_account.setdefault(d.name, d).
  - If company.
    - Set Platform.flags.warehouse\_account\_map at company from warehouse\_account.
  - Otherwise.
    - Set Platform.flags.warehouse\_account\_map from warehouse\_account.
- If company.
  - Return Platform.flags.warehouse\_account\_map.get(company, Platform.\_dict()).
- Return Platform.flags.warehouse\_account\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L769)

<a id="op-3c5f0c30ecb2ed"></a>
### Get warehouse account

`operation_enterprise_stock_initialize_business_behavior_get_warehouse_account`

**Inputs** warehouse, warehouse\_account = no value, raise\_error (named only, default true), stock\_accounts (named only, default no value).

**Record and data access** execute query text (SELECT, Warehouse).

**Explicit results** account.

**Explicit failure paths** validation helper — translated “Please set Account in Warehouse {0} or Default Inventory Account in Company {1}”.format(warehouse.name, warehouse.company).

**Local steps**

- Set account from warehouse.account.
- If (not account and warehouse.parent\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → warehouse.parent\_warehouse.
  - If warehouse\_account.
    - If parent bound to warehouse\_account.get(warehouse.parent\_warehouse).
      - Set account from parent.account.
  - Otherwise.
    - Set account from Platform.db.sql(query text (SELECT, Warehouse), tuple(warehouse.lft, warehouse.rgt, warehouse.company), as\_list = 1).
    - Set account from account at 0 at 0 when account, otherwise no value.
      - Value choice on account — true gives account at 0 at 0, false gives no value.
- If (not account and warehouse.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → warehouse.company.
  - Set account from get\_company\_default\_inventory\_account(warehouse.company).
- If (not account and warehouse.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → warehouse.company.
  - If stock\_accounts is identical to no value.
    - Set stock\_accounts from get\_company\_stock\_accounts(warehouse.company).
  - If len(stock\_accounts) equals 1.
    - Set account from stock\_accounts at 0.
- If (raise\_error and not account and warehouse.company and not warehouse.is\_group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in raise\_error → not account → warehouse.company → not warehouse.is\_group.
  - Call the validation error handler Platform.throw(translated “Please set Account in Warehouse {0} or Default Inventory Account in Company {1}”.format(warehouse.name, warehouse.company)).
- Return account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L768)

<a id="op-cf98dacec3a060"></a>
### Get company default inventory account

`operation_enterprise_stock_initialize_business_behavior_get_company_default_inventory_account`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”).

**Local steps**

- Return Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0706.json#L753) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L767)

<a id="op-27bf192bc9674e"></a>
### Get company stock accounts

`operation_enterprise_binding_enterprise_stock_init_get_company_stock_accounts`

**Inputs** company.

**Record and data access** read “Account” via get\_all.

**Explicit results** Platform.get\_all(“Account”, mapping(“account\_type” → “Stock”, “is\_group” → 0, “company” → company), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Account”, mapping(“account\_type” → “Stock”, “is\_group” → 0, “company” → company), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L940)

## Report · Stock ageing

<a id="op-7738d32a481653"></a>
### Execute

`operation_enterprise_stock_report_stock_ageing_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Set to\_date from filters at “to\_date”.
- Set filters.ranges from get\_age\_ranges(filters.range).
- Set columns from get\_columns(filters).
- Set item\_details from FIFOSlots(filters).generate().
- Set data from format\_report\_data(filters, item\_details, to\_date).
- Set chart\_data from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L5580) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L310)

<a id="op-fe302788394c45"></a>
### Get age ranges

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_age_ranges`

**Inputs** age\_range.

**Declared result** list at str.

**Explicit results** sorted(ranges, key = cint).

**Local steps**

- Set ranges from list of num.strip() for num drawn from (age\_range or “30, 60, 90”).split(“,”) where num.strip().isdigit().
  - Draw num from (age\_range or “30, 60, 90”).split(“,”), keep a combination only if (num.strip().isdigit()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in age\_range → “30, 60, 90”.
- Return sorted(ranges, key = cint).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L360)

<a id="op-ea531f8f7bf86f"></a>
### Get float precision

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_decimal_precision`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”, cache = true)).

**Local steps**

- Return cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”, cache = true)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L5960) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L365)

<a id="op-75d0a993e274be"></a>
### Format report data

`operation_enterprise_stock_report_stock_ageing_business_behavior_format_report_data`

**Inputs** filters, item\_details, to\_date.

**Declared result** list at list.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set precision from get\_float\_precision().
- For each tuple(\_item, item\_dict) in item\_details.items().
  - If not flt(item\_dict.get(“total\_qty”), precision).
    - Continue with the next iteration or loop test.
  - Set details from item\_dict at “details”.
  - Set fifo\_queue from get\_report\_fifo\_queue(item\_dict at “fifo\_queue”, details.has\_batch\_no).
  - If not fifo\_queue.
    - Continue with the next iteration or loop test.
  - Evaluate data.append(get\_report\_row(filters, item\_dict, fifo\_queue, to\_date, …)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L6051) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L358)

<a id="op-0922b1fefac513"></a>
### Normalize fifo queue

`operation_enterprise_stock_report_stock_ageing_business_behavior_normalize_first_in_first_out_queue`

**Inputs** fifo\_queue.

**Declared result** list.

**Explicit results** list of get\_batch\_report\_slot(slot) when is\_batch\_slot(slot), otherwise slot for slot drawn from fifo\_queue.

**Local steps**

- Return list of get\_batch\_report\_slot(slot) when is\_batch\_slot(slot), otherwise slot for slot drawn from fifo\_queue.
  - Draw slot from fifo\_queue.
  - Value choice on is\_batch\_slot(slot) — true gives get\_batch\_report\_slot(slot), false gives slot.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L6397) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L372)

<a id="op-49277731afbee7"></a>
### Get report fifo queue

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_report_first_in_first_out_queue`

**Inputs** fifo\_queue, has\_batch\_no.

**Declared result** list.

**Explicit results** normalize\_fifo\_queue(fifo\_queue) · fifo\_queue.

**Local steps**

- Set get\_posting\_date from itemgetter(FIFO\_POSTING\_DATE\_INDEX).
- Set fifo\_queue from sorted(list of slot for slot drawn from fifo\_queue where get\_posting\_date(slot), key = get\_posting\_date).
  - Draw slot from fifo\_queue, keep a combination only if (get\_posting\_date(slot)).
- If has\_batch\_no.
  - Return normalize\_fifo\_queue(fifo\_queue).
- Return fifo\_queue.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L6499) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L367)

<a id="op-6eed6fb2b02546"></a>
### Get batch report slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_batch_report_slot`

**Inputs** slot.

**Declared result** list.

**Explicit results** slot at slice BATCH\_SLOT\_QTY\_INDEX to no value · slot.

**Local steps**

- If is\_batch\_slot(slot).
  - Return slot at slice BATCH\_SLOT\_QTY\_INDEX to no value.
- Return slot.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L6683) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L362)

<a id="op-222266407f2784"></a>
### Get report row

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_report_row`

**Inputs** filters, item\_dict, fifo\_queue, to\_date, precision.

**Declared result** list.

**Explicit results** row.

**Local steps**

- Set details from item\_dict at “details”.
- Set range\_values from get\_range\_age(filters, fifo\_queue, to\_date, item\_dict, …).
- Set row from list(details.name, details.item\_name, details.description, details.item\_group, …).
- If filters.get(“show\_warehouse\_wise\_stock”).
  - Evaluate row.append(details.warehouse).
- Evaluate row.extend(list(flt(item\_dict.get(“total\_qty”), precision), get\_average\_age(fifo\_queue, to\_date), expanded range\_values, date\_diff(to\_date, fifo\_queue at 0 at FIFO\_DATE\_INDEX), …)).
- Return row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L6775) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L368)

<a id="op-b54f5a2b6d92a7"></a>
### Get average age

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_average_age`

**Inputs** fifo\_queue, to\_date.

**Declared result** float.

**Explicit results** flt((age\_qty ÷ total\_qty), 2) when total\_qty, otherwise 0.0.

**Local steps**

- Set age\_qty, total\_qty from 0.0.
- For each slot in normalize\_fifo\_queue(fifo\_queue).
  - Set qty from get\_slot\_qty(slot).
  - Update age\_qty using + (date\_diff(to\_date, slot at FIFO\_DATE\_INDEX) × qty).
  - Update total\_qty using + qty.
- Return flt((age\_qty ÷ total\_qty), 2) when total\_qty, otherwise 0.0.
  - Value choice on total\_qty — true gives flt((age\_qty ÷ total\_qty), 2), false gives 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L7223) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L361)

<a id="op-dbeee5ef5a7665"></a>
### Get slot qty

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_slot_quantity`

**Inputs** slot.

**Declared result** float.

**Explicit results** slot at FIFO\_QTY\_INDEX · 1.0.

**Local steps**

- If is\_qty\_slot(slot).
  - Return slot at FIFO\_QTY\_INDEX.
- Return 1.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L369)

<a id="op-4ac4bf233e5d09"></a>
### Get range age

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_range_age`

**Inputs** filters, fifo\_queue, to\_date, item\_dict, precision = no value.

**Declared result** list.

**Explicit results** range\_values.

**Local steps**

- Set precision from precision when precision is distinct from no value, otherwise get\_float\_precision().
  - Value choice on precision is distinct from no value — true gives precision, false gives get\_float\_precision().
- Set range\_values from (list(0.0) × ((len(filters.ranges) × 2) + 2)).
- For each slot in fifo\_queue.
  - Set bucket\_index from get\_age\_bucket\_index(filters.ranges, slot, to\_date).
  - Set qty from 1.0 when item\_dict at “has\_serial\_no”, otherwise flt(slot at FIFO\_QTY\_INDEX).
    - Value choice on item\_dict at “has\_serial\_no” — true gives 1.0, false gives flt(slot at FIFO\_QTY\_INDEX).
  - Set stock\_value from flt(slot at FIFO\_VALUE\_INDEX).
  - Evaluate add\_to\_range\_bucket(range\_values, bucket\_index, qty, stock\_value, …).
- Return range\_values.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L366)

<a id="op-be1aed7cfc452f"></a>
### Get age bucket index

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_age_bucket_index`

**Inputs** age\_ranges, slot, to\_date.

**Declared result** int.

**Explicit results** (index × 2) · (len(age\_ranges) × 2).

**Local steps**

- Set age from flt(date\_diff(to\_date, slot at FIFO\_DATE\_INDEX)).
- For each tuple(index, age\_limit) in enumerate(age\_ranges).
  - If age ≤ flt(age\_limit).
    - Return (index × 2).
- Return (len(age\_ranges) × 2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L473) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L359)

<a id="op-3a55fa8be720c0"></a>
### Add to range bucket

`operation_enterprise_stock_report_stock_ageing_business_behavior_add_to_range_bucket`

**Inputs** range\_values, bucket\_index, qty, stock\_value, precision.

**Declared result** no value.

**Local steps**

- Set range\_values at bucket\_index from flt((range\_values at bucket\_index + qty), precision).
- Set range\_values at (bucket\_index + 1) from flt((range\_values at (bucket\_index + 1) + stock\_value), precision).
- If (range\_values at bucket\_index equals 0.0 and round\_off\_if\_near\_zero(range\_values at (bucket\_index + 1), 2) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in range\_values at bucket\_index equals 0.0 → round\_off\_if\_near\_zero(range\_values at (bucket\_index + 1), 2) equals 0.
  - Set range\_values at (bucket\_index + 1) from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L697) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L309)

<a id="op-84bf2f78a74c12"></a>
### Get columns

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_columns`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set range\_columns from list().
- Evaluate setup\_ageing\_columns(filters, range\_columns).
- Set columns from list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….
- If filters.get(“show\_warehouse\_wise\_stock”).
  - Update columns using + list(mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “Available Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 100), mapping(“label” → translated “Average Age”, “fieldname” → “average\_age”, “field ….
- Evaluate columns.extend(range\_columns).
- Evaluate columns.extend(list(mapping(“label” → translated “Earliest”, “fieldname” → “earliest”, “fieldtype” → “Int”, “width” → 80), mapping(“label” → translated “Latest”, “fieldname” → “latest”, “fieldtype” → “Int” ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L364)

<a id="op-282a63ef24c3f5"></a>
### Get chart data

`operation_enterprise_stock_report_stock_ageing_business_behavior_get_chart_data`

**Inputs** data, filters.

**Declared result** dict.

**Explicit results** list() · mapping() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Average Age”, “values” → datapoints))), “type” → “bar”).

**Local steps**

- If not data.
  - Return list().
- Set tuple(labels, datapoints) from tuple(list(), list()).
- If filters.get(“show\_warehouse\_wise\_stock”).
  - Return mapping().
- Evaluate data.sort(key = deferred anonymous expression, reverse = true).
- If len(data) &gt; MAX\_CHART\_ITEMS.
  - Set data from data at slice no value to MAX\_CHART\_ITEMS.
- For each row in data.
  - Evaluate labels.append(row at 0).
  - Evaluate datapoints.append(row at AVERAGE\_AGE\_COLUMN).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Average Age”, “values” → datapoints))), “type” → “bar”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L2327) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L363)

<a id="op-ac21a8ad778bc8"></a>
### Setup ageing columns

`operation_enterprise_stock_report_stock_ageing_business_behavior_setup_ageing_columns`

**Inputs** filters, range\_columns.

**Local steps**

- Set prev\_range\_value from 0.
- Set ranges from list().
- For each age\_range in filters.ranges.
  - Evaluate ranges.append(formatted text {prev\_range\_value} - {age\_range}).
  - Set prev\_range\_value from (cint(age\_range) + 1).
- Evaluate ranges.append(formatted text {prev\_range\_value} - Above).
- For each tuple(i, label) in enumerate(ranges).
  - Set fieldname from (“range” + str((i + 1))).
  - Evaluate add\_column(range\_columns, label = translated “Age ({0})”.format(label), fieldname = fieldname).
  - Evaluate add\_column(range\_columns, label = translated “Value ({0})”.format(label), fieldname = (fieldname + “value”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L2767) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L373)

<a id="op-72f17089b3194e"></a>
### Add column

`operation_enterprise_stock_report_stock_ageing_business_behavior_add_column`

**Inputs** range\_columns, label, fieldname, fieldtype = “Float”, width = 140.

**Local steps**

- Evaluate range\_columns.append(dict(label = label, fieldname = fieldname, fieldtype = fieldtype, width = width)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L3220) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L308)

<a id="op-8f74859468335d"></a>
### Is batch slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_is_batch_slot`

**Inputs** slot.

**Declared result** bool.

**Explicit results** len(slot) equals BATCH\_SLOT\_SIZE.

**Local steps**

- Return len(slot) equals BATCH\_SLOT\_SIZE.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L3379) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L370)

<a id="op-8eb5beab779673"></a>
### Is qty slot

`operation_enterprise_stock_report_stock_ageing_business_behavior_is_quantity_slot`

**Inputs** slot.

**Declared result** bool.

**Explicit results** isinstance(slot at FIFO\_QTY\_INDEX, (int bitwise or float)).

**Local steps**

- Return isinstance(slot at FIFO\_QTY\_INDEX, (int bitwise or float)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0904.json#L3448) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L371)

<a id="op-c0eabbb99dcf35"></a>
### FIFOSlots.initialize

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_initialize`

**Inputs** self, filters = no value, sle = no value.

**Local steps**

- Set self.item\_details from mapping().
- Set self.transferred\_item\_details from mapping().
- Set self.serial\_no\_details from mapping().
- Set self.batch\_no\_details from mapping().
- Set self.batches\_with\_negative\_slots from set().
- Set self.batchwise\_valuation\_by\_batch from mapping().
- Set self.valuation\_method\_by\_item from mapping().
- Set self.filters from filters.
- Set self.sle from sle.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L340)
