# Inventory and warehouses · operations 105

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock valuation comparison

<a id="op-9318e24f68d007"></a>
### Get rows to show

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_rows_to_show`

**Inputs** item\_code, warehouse, expected\_valuation, filters, tolerance, adjustment = no value.

**Declared result** list at dict.

**Explicit results** rows.

**Local steps**

- Set from\_date from getdate(filters.from\_date) when filters.from\_date, otherwise no value.
  - Value choice on filters.from\_date — true gives getdate(filters.from\_date), false gives no value.
- Set show from (filters.show or SHOW\_FIRST\_DIFFERENCE).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.show → SHOW\_FIRST\_DIFFERENCE.
- Set rows from list().
- For each tuple(entry, expected) in expected\_valuation.
  - If (from\_date and getdate(entry.posting\_date) &lt; from\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → getdate(entry.posting\_date) &lt; from\_date.
    - Continue with the next iteration or loop test.
  - Set row from make\_comparison\_row(item\_code, warehouse, entry, expected, …).
  - If (row.has\_difference and adjustment and get\_datetime(entry.posting\_datetime) &lt; adjustment.posting\_datetime).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.has\_difference → adjustment → get\_datetime(entry.posting\_datetime) &lt; adjustment.posting\_datetime.
    - Set row.adjusted\_by from adjustment.voucher\_no.
    - If not filters.show\_adjusted\_differences.
      - Set row.has\_difference from 0.
      - If show equals SHOW\_ALL\_ENTRIES.
        - Evaluate row.update(dict.fromkeys(DIFFERENCE\_FIELDS, 0.0)).
  - If (show equals SHOW\_ALL\_ENTRIES or row.has\_difference).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in show equals SHOW\_ALL\_ENTRIES → row.has\_difference.
    - Evaluate rows.append(row).
  - If (show equals SHOW\_FIRST\_DIFFERENCE and row.has\_difference).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in show equals SHOW\_FIRST\_DIFFERENCE → row.has\_difference.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return rows.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1066)

<a id="op-c72a1296813f0c"></a>
### Make comparison row

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_make_comparison_row`

**Inputs** item\_code, warehouse, entry, expected, tolerance.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set row from Platform.\_dict(mapping(“stock\_ledger\_entry” → entry.name, “posting\_date” → entry.posting\_date, “posting\_time” → entry.posting\_time, “item\_code” → item\_code, …)).
- Evaluate set\_differences(row, tolerance).
- Return row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1068)

<a id="op-29a2f25ebed702"></a>
### Set differences

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_set_differences`

**Inputs** row, tolerance.

**Declared result** no value.

**Local steps**

- Set row.has\_difference from 0.
- For each tuple(actual\_field, expected\_field, difference\_field) in COMPARED\_VALUES.
  - Set difference from (flt(row at actual\_field) − flt(row at expected\_field)).
  - If (difference\_field equals “valuation\_rate\_difference” and not flt(row.expected\_qty\_after\_transaction)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in difference\_field equals “valuation\_rate\_difference” → not flt(row.expected\_qty\_after\_transaction).
    - Set difference from 0.0.
  - If abs(difference) &lt; max(tolerance, FLOAT\_NOISE).
    - Set difference from 0.0.
  - Set row at difference\_field from difference.
  - If difference.
    - Set row.has\_difference from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1070)

<a id="op-b1590292f0729e"></a>
### Get item warehouses

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_item_warehouses`

**Inputs** filters.

**Declared result** list at dict.

**Record and data access** read “Item Group” via get\_value · read “Item Group” via get\_all · read “Warehouse” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set warehouse from Platform.qb.DocType(“Warehouse”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the  ….
- If filters.item\_code.
  - Set query from query.where(item.name equals filters.item\_code).
- If filters.item\_group.
  - Set item\_group from Platform.db.get\_value(“Item Group”, filters.item\_group, list(“lft”, “rgt”), as\_dict = true).
  - Set item\_groups from Platform.get\_all(“Item Group”, filters = mapping(“lft” → tuple(“&gt;=”, item\_group.lft), “rgt” → tuple(“&lt;=”, item\_group.rgt)), pluck = “name”).
  - Set query from query.where(item.item\_group.isin(item\_groups)).
- If filters.warehouse.
  - Set parent from Platform.db.get\_value(“Warehouse”, filters.warehouse, list(“lft”, “rgt”), as\_dict = true).
  - Set query from query.where((warehouse.lft ≥ parent.lft bitwise and warehouse.rgt ≤ parent.rgt)).
- Set allowed\_values from get\_allowed\_values().
- For each field in tuple(“item\_code”, “warehouse”).
  - If allowed\_values.get(field).
    - Set query from query.where(bin at field.isin(allowed\_values at field)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1063)

<a id="op-b5bf327165dfad"></a>
### Get default tolerance

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_default_tolerance`

**Inputs** no declared parameters.

**Declared result** float.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** (1.0 ÷ (10 to the power currency\_precision)).

**Local steps**

- Set currency\_precision from (cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)) → 2.
- Return (1.0 ÷ (10 to the power currency\_precision)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “currency\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1061)

<a id="op-a342ef2fcef3dd"></a>
### Get columns

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“fieldname” → “posting\_date”, “fieldtype” → “Date”, “label” → translated “Posting Date”, “width” → 100), mapping(“fieldname” → “posting\_time”, “fieldtype” → “Time”, “label” → translated “Posti ….

**Local steps**

- Return list(mapping(“fieldname” → “posting\_date”, “fieldtype” → “Date”, “label” → translated “Posting Date”, “width” → 100), mapping(“fieldname” → “posting\_time”, “fieldtype” → “Time”, “label” → translated “Posti ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1059)

<a id="op-5715a2081e8875"></a>
### Get pending reposts

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_pending_reposts`

**Inputs** item\_warehouses.

**Declared result** dict at tuple(tuple at tuple(str, str), str).

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** mapping() · mapping of key → repost.name for tuple(key, repost) drawn from pending.items().

**Local steps**

- If not item\_warehouses.
  - Return mapping().
- Set pending from mapping().
- For each repost in Platform.get\_all(“Repost Item Valuation”, filters = mapping(“docstatus” → 1, “status” → tuple(“in”, PENDING\_REPOST\_STATUSES), “based\_on” → “Item and Warehouse”, “item\_code” → tuple(“in”, list(set of item\_c ….
  - Draw tuple(item\_code, \_warehouse) from item\_warehouses.
  - Evaluate pending.setdefault(tuple(repost.item\_code, repost.warehouse), repost).
- Return mapping of key → repost.name for tuple(key, repost) drawn from pending.items().
  - Draw tuple(key, repost) from pending.items().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1064)

<a id="op-62aac78c845e7f"></a>
### Get differences to fix

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_differences_to_fix`

**Inputs** company, stock\_ledger\_entries.

**Declared result** dict at tuple(tuple at tuple(str, str), Platform.\_dict).

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** first\_differences.

**Explicit failure paths** validation helper — translated “Select the differences to fix.”.

**Local steps**

- Set stock\_ledger\_entries from (Platform.parse\_json(stock\_ledger\_entries) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(stock\_ledger\_entries) → list().
- If not stock\_ledger\_entries.
  - Call the validation error handler Platform.throw(translated “Select the differences to fix.”).
- Evaluate validate\_company\_permission(company).
- Set filters from mapping(“name” → tuple(“in”, stock\_ledger\_entries), “company” → company, “is\_cancelled” → 0).
- For each tuple(field, values) in get\_allowed\_values().items().
  - If field belongs to tuple(“item\_code”, “warehouse”).
    - Set filters at field from tuple(“in”, values).
- Set first\_differences from mapping().
- For each entry in Platform.get\_all(“Stock Ledger Entry”, filters = filters, fields = list(“name”, “item\_code”, “warehouse”, “posting\_date”, …), order\_by = “posting\_datetime asc, creation asc”).
  - Evaluate first\_differences.setdefault(tuple(entry.item\_code, entry.warehouse), entry).
- Return first\_differences.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1062)

<a id="op-5083dd35a42f41"></a>
### Get repost preview

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_repost_preview`

**Inputs** company, stock\_ledger\_entries.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** preview.

**Local steps**

- Evaluate Platform.has\_permission(“Repost Item Valuation”, “create”, throw = true).
- Set first\_differences from get\_differences\_to\_fix(company, stock\_ledger\_entries).
- Set pending\_reposts from get\_pending\_reposts(list(first\_differences)).
- Set current\_fiscal\_year\_start from get\_fiscal\_year(nowdate(), company = company, boolean = true).
- Set preview from list().
- For each tuple(tuple(item\_code, warehouse), entry) in first\_differences.items().
  - Set fiscal\_year from get\_fiscal\_year(entry.posting\_date, company = company, boolean = true).
  - Evaluate preview.append(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_date” → entry.posting\_date, “posting\_time” → entry.posting\_time, …)).
    - Value choice on fiscal\_year — true gives fiscal\_year at 0, false gives no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_fiscal\_year\_start → getdate(entry.posting\_date) &lt; current\_fiscal\_year\_start at 1.
- Return preview.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Item Valuation”, “create”, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1065)

<a id="op-f5ddb36cc6e2c0"></a>
### Make repost entries

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_make_repost_entries`

**Inputs** company, stock\_ledger\_entries.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Record and data access** resolve a document from mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “company” → company, “item\_code” → row at “item\_code”, …) via get\_doc.

**State and service calls** savepoint “repost\_item\_valuation” · call insert on repost · call submit on repost · rollback.

**Explicit results** mapping(“created” → created, “not\_created” → not\_created).

**Local steps**

- Evaluate Platform.has\_permission(“Repost Item Valuation”, “create”, throw = true).
- Evaluate Platform.has\_permission(“Repost Item Valuation”, “submit”, throw = true).
- Set tuple(created, not\_created) from tuple(list(), list()).
- For each row in get\_repost\_preview(company, stock\_ledger\_entries).
  - If row at “pending\_repost”.
    - Evaluate not\_created.append(mapping(expand row, “reason” → translated “Repost {0} is already pending.”.format(row at “pending\_repost”))).
    - Continue with the next iteration or loop test.
  - Evaluate Platform.db.savepoint(“repost\_item\_valuation”).
  - Attempt the following.
    - Set repost from Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “company” → company, “item\_code” → row at “item\_code”, …)).
    - Evaluate repost.insert().
    - Evaluate repost.submit().
    - Evaluate created.append(mapping(expand row, “repost” → repost.name)).
  - On failure (Platform.ValidationError) bound to e.
    - Evaluate Platform.db.rollback(save\_point = “repost\_item\_valuation”).
    - Evaluate Platform.clear\_messages().
    - Evaluate not\_created.append(mapping(expand row, “reason” → str(e))).
- Return mapping(“created” → created, “not\_created” → not\_created).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Item Valuation”, “create”, throw = true), Platform.has\_permission(“Repost Item Valuation”, “submit”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1069)

<a id="op-12195e14c1f713"></a>
### Make adjustment entry

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_make_adjustment_entry`

**Inputs** company, stock\_ledger\_entries, posting\_date, posting\_time, expense\_account = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** dict.

**Explicit results** mapping(“adjustment\_entry” → doc.name when doc.items, otherwise no value, “not\_adjusted” → not\_adjusted).

**Local steps**

- Evaluate Platform.has\_permission(“Stock Reconciliation”, “create”, throw = true).
- Set adjustment\_datetime from get\_combine\_datetime(posting\_date, posting\_time).
- Set first\_differences from get\_differences\_to\_fix(company, stock\_ledger\_entries).
- Set not\_adjusted from list().
- Set item\_warehouses from list().
- For each tuple(tuple(item\_code, warehouse), entry) in first\_differences.items().
  - If get\_datetime(entry.posting\_datetime) ≥ get\_datetime(adjustment\_datetime).
    - Evaluate not\_adjusted.append(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “reason” → translated “Its difference on {0} is not before the adjustment date.”.format(Platform.format(entry.posting\_date, “Date”)))).
  - Otherwise.
    - Evaluate item\_warehouses.append(tuple(item\_code, warehouse)).
- Set tuple(doc, plans) from make\_draft\_adjustment\_entry(company, item\_warehouses, posting\_date, posting\_time, expense\_account = expense\_account).
- For each tuple(item\_code, warehouse) in item\_warehouses.
  - Set plan from plans.get(tuple(item\_code, warehouse)).
  - If (not plan or plan.reason).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not plan → plan.reason.
    - Evaluate not\_adjusted.append(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “reason” → plan.reason when plan, otherwise translated “It has no stock transactions by then.”)).
      - Value choice on plan — true gives plan.reason, false gives translated “It has no stock transactions by then.”.
- Return mapping(“adjustment\_entry” → doc.name when doc.items, otherwise no value, “not\_adjusted” → not\_adjusted).
  - Value choice on doc.items — true gives doc.name, false gives no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Stock Reconciliation”, “create”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1067)

## Service · Stock value by item group

<a id="op-123bf38651ad64"></a>
### Get

`operation_enterprise_stock_dashboard_chart_source_stock_value_by_item_group_business_behavior_get`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Explicit results** mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Stock Value”, “values” → datasets))).

**Local steps**

- If (filters and isinstance(filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → isinstance(filters, str).
  - Set filters from Platform.parse\_json(filters).
- Set company from filters.get(“company”) when filters, otherwise no value.
  - Value choice on filters — true gives filters.get(“company”), false gives no value.
- If not company.
  - Set company from Platform.defaults.get\_defaults().company.
- Set tuple(labels, datasets) from get\_stock\_value\_by\_item\_group(company).
- Return mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Stock Value”, “values” → datasets))).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L688)

<a id="op-3671d6e014c7f2"></a>
### Get stock value by item group

`operation_enterprise_stock_dashboard_chart_source_stock_value_by_item_group_business_behavior_get_stock_value_by_item_group`

**Inputs** company.

**Record and data access** read “Warehouse” via get\_list.

**Explicit results** tuple(list(), list()) · tuple(labels, datapoints).

**Local steps**

- Set doctype from Platform.qb.DocType(“Bin”).
- Set item\_doctype from Platform.qb.DocType(“Item”).
- Set warehouse\_filters from list(list(“is\_group”, “=”, 0)).
- If company.
  - Evaluate warehouse\_filters.append(list(“company”, “=”, company)).
- Set warehouses from Platform.get\_list(“Warehouse”, pluck = “name”, filters = warehouse\_filters).
- If not warehouses.
  - Return tuple(list(), list()).
- Set permitted\_items from Platform.qb.get\_query(“Item”, fields = list(“name”), ignore\_permissions = false).
- Set stock\_value from Sum(doctype.stock\_value).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).groupby(item\_doctype.item\_group).orderby(stock\_value, order = Platform.qb.desc).limit(10).
- Set query from query.where(doctype.warehouse.isin(warehouses)).
- Set query from query.where(doctype.item\_code.isin(permitted\_items)).
- Set results from query.run(as\_dict = true).
- Set labels from list().
- Set datapoints from list().
- For each row in results.
  - If not row.stock\_value.
    - Continue with the next iteration or loop test.
  - Evaluate labels.append(translated row.item\_group).
  - Evaluate datapoints.append(row.stock\_value).
- Return tuple(labels, datapoints).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L689)

## Report · Total stock summary

<a id="op-8c3128553d5998"></a>
### Execute

`operation_enterprise_stock_report_total_stock_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, stock).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns(filters).
- Set stock from get\_total\_stock(filters).
- Return tuple(columns, stock).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0924.json#L3329) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L586)

<a id="op-b45507823a9f97"></a>
### Get columns

`operation_enterprise_stock_report_total_stock_summary_business_behavior_get_columns`

**Inputs** filters.

**State and service calls** call insert on columns.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Item” + “:Link/Item:150”), (translated “Description” + “::300”), (translated “Current Qty” + “:Float:100”)).
- If filters.get(“group\_by”) equals “Warehouse”.
  - Evaluate columns.insert(0, (translated “Warehouse” + “:Link/Warehouse:150”)).
- Otherwise.
  - Evaluate columns.insert(0, (translated “Company” + “:Link/Company:250”)).
- Return columns.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0924.json#L3460) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L587)

<a id="op-759a8622315d07"></a>
### Get total stock

`operation_enterprise_stock_report_total_stock_summary_business_behavior_get_total_stock`

**Inputs** filters.

**Explicit results** query.run().

**Local steps**

- Set bin from Platform.qb.DocType(“Bin”).
- Set item from Platform.qb.DocType(“Item”).
- Set wh from Platform.qb.DocType(“Warehouse”).
- Set query from nested operand in the contract(nested operand in the contract).inner\_join(wh).on(wh.name equals bin.warehouse).where(bin.actual\_qty differs from 0).
- If warehouses bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Stock Entry”).
  - Set query from query.where(bin.warehouse.isin(warehouses)).
- If filters.get(“group\_by”) equals “Warehouse”.
  - If filters.get(“company”).
    - Set query from query.where(wh.company equals filters.get(“company”)).
  - Set query from query.select(bin.warehouse).groupby(bin.warehouse).
- Otherwise.
  - Set query from query.select(wh.company).groupby(wh.company).
- Set query from query.select(item.item\_code, item.description, Sum(nested operand in the contract.actual\_qty).as\_(“actual\_qty”)).groupby(item.item\_code).
- Return query.run().

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L588)

## Service · Utils

<a id="op-2b8df0a9f2920f"></a>
### Get stock value from bin

`operation_enterprise_stock_utils_business_behavior_get_stock_value_from_bin`

**Inputs** warehouse = no value, item\_code = no value.

**State and service calls** execute a supplied database query.

**Explicit results** stock\_value.

**Local steps**

- Set values from mapping().
- Set conditions from empty text.
- If warehouse.
  - Update conditions using + query text (SELECT, Warehouse).
  - Set values at “warehouse” from warehouse.
- If item\_code.
  - Update conditions using + “ and ′tabBin′.item\_code = %(item\_code)s”.
  - Set values at “item\_code” from item\_code.
- Set query from (query text (SELECT, Bin) modulo or format conditions).
- Set stock\_value from Platform.db.sql(query, values).
- Return stock\_value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L890)

<a id="op-e9ba180c2ceca3"></a>
### Get stock value on

`operation_enterprise_stock_utils_business_behavior_get_stock_value_on`

**Inputs** warehouses = no value, posting\_date = no value, item\_code = no value, company = no value.

**Declared result** float.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.run(as\_list = true) at 0 at 0.

**Local steps**

- If not posting\_date.
  - Set posting\_date from nowdate().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract.qb.from\_(sle).select(IfNull(Sum(sle.stock\_value\_difference), 0)).where((sle.posting\_date ≤ posting\_date bitwise and sle.is\_cancelled equals 0)).
- If warehouses.
  - If isinstance(warehouses, str).
    - Set warehouses from list(warehouses).
  - Set warehouses from set(warehouses).
  - For each wh in list(warehouses).
    - If Platform.db.get\_value(“Warehouse”, wh, “is\_group”).
      - Evaluate warehouses.update(get\_child\_warehouses(wh)).
  - Set query from query.where(sle.warehouse.isin(warehouses)).
- If item\_code.
  - Set query from query.where(sle.item\_code equals item\_code).
- If company.
  - Set query from query.where(sle.company equals company).
- Return query.run(as\_list = true) at 0 at 0.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0946.json#L6797) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L891)

<a id="op-7a210c7fb0e215"></a>
### Get stock balance

`operation_enterprise_stock_utils_business_behavior_get_stock_balance`

**Inputs** item\_code, warehouse, posting\_date = no value, posting\_time = no value, with\_valuation\_rate = false, with\_serial\_no = false, inventory\_dimensions\_dict = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_stock\_balance(item\_code, warehouse, posting\_date, posting\_time, …).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- Evaluate require\_user\_permission(“Item”, item\_code).
- Evaluate require\_user\_permission(“Warehouse”, warehouse).
- Return \_get\_stock\_balance(item\_code, warehouse, posting\_date, posting\_time, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L889)

<a id="op-f7361813b2f294"></a>
### Get stock balance

`operation_enterprise_binding_enterprise_stock_utils_get_stock_balance`

**Inputs** item\_code, warehouse, posting\_date = no value, posting\_time = no value, with\_valuation\_rate = false, with\_serial\_no = false, inventory\_dimensions\_dict = no value.

**Explicit results** tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate, serial\_nos) when last\_entry, otherwise tuple(0.0, 0.0, no value) · tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate) when last\_entry, otherwise tuple(0.0, 0.0) · last\_entry.qty\_after\_transaction when last\_entry, otherwise 0.0.

**Explicit failure paths** validation helper — translated “{0} is not a valid {1} fieldname.”.format(Platform.bold(field), Platform.bold(“Inventory Dimension”)).

**Local steps**

- Bind dependencies get\_previous\_sle.
- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- If posting\_date is identical to no value.
  - Set posting\_date from nowdate().
- If posting\_time is identical to no value.
  - Set posting\_time from nowtime().
- Set args from mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_date” → posting\_date, “posting\_time” → posting\_time).
- Set extra\_cond from empty text.
- If inventory\_dimensions\_dict.
  - Set inventory\_dimensions\_fieldname from list of d.get(“fieldname”) for d drawn from get\_inventory\_dimensions().
    - Draw d from get\_inventory\_dimensions().
  - For each tuple(field, value) in inventory\_dimensions\_dict.items().
    - If field does not belong to inventory\_dimensions\_fieldname.
      - Call the validation error handler Platform.throw(translated “{0} is not a valid {1} fieldname.”.format(Platform.bold(field), Platform.bold(“Inventory Dimension”))).
    - Set args at field from value.
    - Update extra\_cond using + formatted text  and {field} = %({field})s.
- Set last\_entry from get\_previous\_sle(args, extra\_cond = extra\_cond).
- If with\_valuation\_rate.
  - If with\_serial\_no.
    - Set serial\_no\_details from get\_available\_serial\_nos(Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_datetime” → get\_combine\_datetime(posting\_date, posting\_time), “ignore\_warehouse” → 1, …))).
    - Set serial\_nos from empty text.
    - If serial\_no\_details.
      - Set serial\_nos from whitespace '\\n'.join(generator of d.serial\_no for d drawn from serial\_no\_details).
        - Draw d from serial\_no\_details.
    - Return tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate, serial\_nos) when last\_entry, otherwise tuple(0.0, 0.0, no value).
      - Value choice on last\_entry — true gives tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate, serial\_nos), false gives tuple(0.0, 0.0, no value).
  - Otherwise.
    - Return tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate) when last\_entry, otherwise tuple(0.0, 0.0).
      - Value choice on last\_entry — true gives tuple(last\_entry.qty\_after\_transaction, last\_entry.valuation\_rate), false gives tuple(0.0, 0.0).
- Otherwise.
  - Return last\_entry.qty\_after\_transaction when last\_entry, otherwise 0.0.
    - Value choice on last\_entry — true gives last\_entry.qty\_after\_transaction, false gives 0.0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1135)

<a id="op-258cb9846a9ba0"></a>
### Get serial nos data

`operation_enterprise_stock_utils_business_behavior_get_serial_numbers_data`

**Inputs** serial\_nos.

**Explicit results** get\_serial\_nos(serial\_nos).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Return get\_serial\_nos(serial\_nos).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0947.json#L1092) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L888)

<a id="op-a915157f9e4e90"></a>
### Get latest stock qty

`operation_enterprise_stock_utils_business_behavior_get_latest_stock_quantity`

**Inputs** item\_code, warehouse = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_value.

**State and service calls** execute a supplied database query.

**Explicit results** actual\_qty.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- If warehouse.
  - Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Set tuple(values, condition) from tuple(list(item\_code), empty text).
- If warehouse.
  - Set tuple(lft, rgt, is\_group) from Platform.db.get\_value(“Warehouse”, warehouse, list(“lft”, “rgt”, “is\_group”)).
  - If is\_group.
    - Evaluate values.extend(list(lft, rgt)).
    - Update condition using + query text (SELECT, Warehouse).
  - Otherwise.
    - Evaluate values.append(warehouse).
    - Update condition using + “ AND warehouse = %s”.
- Set actual\_qty from Platform.db.sql(formatted text select sum(actual\_qty) from tabBin  where item\_code=%s {condition}, values) at 0 at 0.
- Return actual\_qty.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L886)

<a id="op-1ad6ac69130611"></a>
### Get latest stock qty for items

`operation_enterprise_binding_enterprise_stock_utils_get_latest_stock_qty_for_items`

**Inputs** items\_by\_warehouse.

**Declared result** dict at tuple(tuple at tuple(str, str), float).

**Explicit results** mapping() · quantities.

**Local steps**

- If not items\_by\_warehouse.
  - Return mapping().
- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- Set bin\_dt from Platform.qb.DocType(“Bin”).
- Set quantities from mapping().
- For each tuple(warehouse, item\_codes) in items\_by\_warehouse.items().
  - Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(item\_codes)).where(get\_bin\_warehouse\_condition(warehouse)).groupby(b ….
  - For each tuple(item\_code, qty) in query.run().
    - Set quantities at tuple(item\_code, warehouse) from qty.
- Return quantities.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1134)

<a id="op-5cfb73c1dac7a6"></a>
### Get bin warehouse condition

`operation_enterprise_binding_enterprise_stock_utils_get_bin_warehouse_condition`

**Inputs** warehouse.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** bin\_dt.warehouse equals warehouse · bin\_dt.warehouse.isin(nested operand in the contract.from\_(wh).select(wh.name).where((wh.lft ≥ lft bitwise and wh.rgt ≤ rgt))).

**Local steps**

- Set bin\_dt from Platform.qb.DocType(“Bin”).
- Set tuple(lft, rgt, is\_group) from Platform.db.get\_value(“Warehouse”, warehouse, list(“lft”, “rgt”, “is\_group”)).
- If not is\_group.
  - Return bin\_dt.warehouse equals warehouse.
- Set wh from Platform.qb.DocType(“Warehouse”).
- Return bin\_dt.warehouse.isin(nested operand in the contract.from\_(wh).select(wh.name).where((wh.lft ≥ lft bitwise and wh.rgt ≤ rgt))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1132)
