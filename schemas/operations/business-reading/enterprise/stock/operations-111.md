# Inventory and warehouses · operations 111

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Warehouse wise item balance age and value

<a id="op-d2e18b367dc622"></a>
### Apply permitted warehouses

`operation_enterprise_binding_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_warehouse_wise_item_balance_age_and_value_apply_permitted_warehouses`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** true · bool(permitted).

**Local steps**

- Set permitted from get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Stock Ledger Entry”).
- If not permitted.
  - Return true.
- Set permitted from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, permitted), “is\_group” → 0), pluck = “name”).
- If filters.get(“warehouse”).
  - Set selected from set of warehouse.name for warehouse drawn from get\_warehouse\_list(filters).
    - Draw warehouse from get\_warehouse\_list(filters).
  - Set permitted from list of warehouse for warehouse drawn from permitted where warehouse belongs to selected.
    - Draw warehouse from permitted, keep a combination only if (warehouse belongs to selected).
- Set filters at “warehouse” from permitted.
- Return bool(permitted).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1071)

<a id="op-04e5bbc743f815"></a>
### Get itemwise brand

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_get_itemwise_brand`

**Inputs** items.

**Record and data access** read “Item” via get\_all.

**Explicit results** Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, items)), fields = list(“name”, “brand”), as\_list = 1).

**Local steps**

- Return Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, items)), fields = list(“name”, “brand”), as\_list = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L1464) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L595)

<a id="op-cad33f1718be4a"></a>
### Get columns

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Item” + “:Link/Item:150”), (translated “Item Name” + “:Link/Item:150”), (translated “Item Group” + “::120”), (translated “Brand” + “:Link/Brand:120”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L1598) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L592)

<a id="op-2cbf342bfb4c55"></a>
### Validate filters

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “Please set filter based on Item or Warehouse”.

**Local steps**

- If not (filters.get(“item\_code”) or filters.get(“warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_code”) → filters.get(“warehouse”).
  - Set table from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set sle\_count from flt(nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).run() at 0 at 0).
  - <a id="op-2cbf342bfb4c55-guard-7"></a>If sle\_count &gt; 500000.
    - Call the validation error handler Platform.throw(translated “Please set filter based on Item or Warehouse”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison sle\_count &gt; 500000, sle\_count = 500001 selects the branch that calls the validation-error handler with translated “Please set filter based on Item or Warehouse”. With sle\_count = 500000, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2cbf342bfb4c55-guard-7)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L1816) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L597)

<a id="op-d98be745917bcd"></a>
### Get warehouse list

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_get_warehouse_list`

**Inputs** filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** Platform.get\_all(“Warehouse”, filters = mapping(“company” → filters.get(“company”), “is\_group” → 0), fields = list(“name”), order\_by = “name”) · list() · nested operand in the contract(nested operand in the contract).where((condition bitwise and nested operand in the contract equals nested operand in the contract)).orderby(warehouse.name).run(as\_dict = true).

**Local steps**

- Set warehouses from filters.get(“warehouse”).
- If not warehouses.
  - Return Platform.get\_all(“Warehouse”, filters = mapping(“company” → filters.get(“company”), “is\_group” → 0), fields = list(“name”), order\_by = “name”).
- If isinstance(warehouses, str).
  - Set warehouses from list(warehouses).
- Set subtrees from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, warehouses)), fields = list(“lft”, “rgt”)).
- If not subtrees.
  - Return list().
- Set warehouse from Platform.qb.DocType(“Warehouse”).
- Set condition from Criterion.any(list of (warehouse.lft ≥ row.lft bitwise and warehouse.rgt ≤ row.rgt) for row drawn from subtrees).
  - Draw row from subtrees.
- Return nested operand in the contract(nested operand in the contract).where((condition bitwise and nested operand in the contract equals nested operand in the contract)).orderby(warehouse.name).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L596)

<a id="op-f37181e0f299d9"></a>
### Add warehouse column

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_add_warehouse_column`

**Inputs** columns, warehouse\_list.

**Local steps**

- If len(warehouse\_list) &gt; 1.
  - Update columns using + list((translated “Total Qty” + “:Float:120”)).
- For each wh in warehouse\_list.
  - Update columns using + list((translated wh.name + “:Float:100”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L590)

<a id="op-1295ea4a11b7dc"></a>
### Get item warehouse map

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_get_item_warehouse_map`

**Inputs** filters, sle.

**Explicit results** iwb\_map.

**Local steps**

- Set iwb\_map from mapping().
- Set from\_date from getdate(filters.get(“from\_date”)).
- Set to\_date from getdate(filters.get(“to\_date”)).
- Set float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 3.
- For each d in sle.
  - Set group\_by\_key from get\_group\_by\_key(d).
  - If group\_by\_key does not belong to iwb\_map.
    - Set iwb\_map at group\_by\_key from Platform.\_dict(mapping(“opening\_qty” → 0.0, “opening\_val” → 0.0, “in\_qty” → 0.0, “in\_val” → 0.0, …)).
  - Set qty\_dict from iwb\_map at group\_by\_key.
  - If (d.voucher\_type equals “Stock Reconciliation” and not d.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.voucher\_type equals “Stock Reconciliation” → not d.batch\_no.
    - Set qty\_diff from (flt(d.qty\_after\_transaction) − flt(qty\_dict.bal\_qty)).
  - Otherwise.
    - Set qty\_diff from flt(d.actual\_qty).
  - Set value\_diff from flt(d.stock\_value\_difference).
  - If d.posting\_date &lt; from\_date.
    - Update qty\_dict.opening\_qty using + qty\_diff.
    - Update qty\_dict.opening\_val using + value\_diff.
  - Otherwise.
    - If (d.posting\_date ≥ from\_date and d.posting\_date ≤ to\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.posting\_date ≥ from\_date → d.posting\_date ≤ to\_date.
      - If flt(qty\_diff, float\_precision) ≥ 0.
        - Update qty\_dict.in\_qty using + qty\_diff.
        - Update qty\_dict.in\_val using + value\_diff.
      - Otherwise.
        - Update qty\_dict.out\_qty using + abs(qty\_diff).
        - Update qty\_dict.out\_val using + abs(value\_diff).
  - Set qty\_dict.val\_rate from d.valuation\_rate.
  - Update qty\_dict.bal\_qty using + qty\_diff.
  - Update qty\_dict.bal\_val using + value\_diff.
- Set iwb\_map from filter\_items\_with\_no\_transactions(iwb\_map, float\_precision).
- Return iwb\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L2938) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L594)

<a id="op-35190221fceb88"></a>
### Get group by key

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_get_group_by_key`

**Inputs** row.

**Declared result** tuple.

**Explicit results** tuple(row.company, row.item\_code, row.warehouse).

**Local steps**

- Return tuple(row.company, row.item\_code, row.warehouse).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L3851) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L593)

## Report · Warehouse wise stock balance

<a id="op-c0288f8f0df8a1"></a>
### Execute

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L4485) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L604)

<a id="op-22d608bee47ec5"></a>
### Get warehouse wise balance

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_get_warehouse_wise_balance`

**Inputs** filters.

**Declared result** list at SLEntry.

**Explicit results** Platform.\_dict(data) when data, otherwise Platform.\_dict().

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.warehouse, nested operand in the contract.as\_(“stock\_balance”)).where((sle.docstatus &lt; 2 bitwise and sle.is\_cancelled equals 0)).gr ….
- If filters.get(“company”).
  - Set query from query.where(sle.company equals filters.get(“company”)).
- Set data from query.run(as\_list = true).
- Return Platform.\_dict(data) when data, otherwise Platform.\_dict().
  - Value choice on data — true gives Platform.\_dict(data), false gives Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L4620) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L607)

<a id="op-125e86025074d5"></a>
### Get warehouses

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_get_warehouses`

**Inputs** report\_filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** Platform.get\_all(“Warehouse”, fields = list(“name”, “parent\_warehouse”, “is\_group”, “disabled”), filters = filters, order\_by = “lft”).

**Local steps**

- Set filters from list(list(“company”, “=”, report\_filters.company)).
- If companies bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Company”, list()), “Warehouse”).
  - Evaluate filters.append(list(“company”, “in”, companies)).
- Return Platform.get\_all(“Warehouse”, fields = list(“name”, “parent\_warehouse”, “is\_group”, “disabled”), filters = filters, order\_by = “lft”).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L608)

<a id="op-cb2a24eb2df379"></a>
### Get data

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_get_data`

**Inputs** filters.

**Explicit results** warehouses · list of warehouse for warehouse drawn from warehouses where (not warehouse.disabled or warehouse.stock\_balance).

**Local steps**

- Set warehouse\_balance from get\_warehouse\_wise\_balance(filters).
- Set warehouses from get\_warehouses(filters).
- For each warehouse in warehouses.
  - Set warehouse.stock\_balance from (warehouse\_balance.get(warehouse.name, 0) or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse\_balance.get(warehouse.name, 0) → 0.0.
- Evaluate update\_indent(warehouses).
- Evaluate set\_balance\_in\_parent(warehouses).
- If filters.get(“show\_disabled\_warehouses”).
  - Return warehouses.
- Return list of warehouse for warehouse drawn from warehouses where (not warehouse.disabled or warehouse.stock\_balance).
  - Draw warehouse from warehouses, keep a combination only if ((not warehouse.disabled or warehouse.stock\_balance)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not warehouse.disabled → warehouse.stock\_balance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L606)

<a id="op-c0572982f3a71c"></a>
### Update indent

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_update_indent`

**Inputs** warehouses.

**Local steps**

- Set indent\_by\_name from mapping().
- For each warehouse in warehouses.
  - Set warehouse.indent from (indent\_by\_name.get(warehouse.parent\_warehouse, negative 1) + 1).
  - Set indent\_by\_name at warehouse.name from warehouse.indent.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L610)

<a id="op-13bff6154daa94"></a>
### Set balance in parent

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_set_balance_in_parent`

**Inputs** warehouses.

**Local steps**

- Set warehouse\_by\_name from mapping of warehouse.name → warehouse for warehouse drawn from warehouses.
  - Draw warehouse from warehouses.
- For each warehouse in reversed(warehouses).
  - If parent bound to warehouse\_by\_name.get(warehouse.parent\_warehouse).
    - Update parent.stock\_balance using + warehouse.stock\_balance.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L609)

<a id="op-e04e94bd5b8c4d"></a>
### Get columns

`operation_enterprise_stock_report_warehouse_wise_stock_balance_business_behavior_get_columns`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Warehouse”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Warehouse”, …), mapping(“label” → translated “Stock Balance”, “fieldname” → “stock\_balance”, “fieldty ….
- If filters.get(“show\_disabled\_warehouses”).
  - Evaluate columns.append(mapping(“label” → translated “Warehouse Disabled?”, “fieldname” → “disabled”, “fieldtype” → “Check”, “width” → 200)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L5981) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L605)

## Service · Warehouse wise stock value

<a id="op-fd6b9e4bbad9a8"></a>
### Get

`operation_enterprise_stock_dashboard_chart_source_warehouse_wise_stock_value_business_behavior_get`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Record and data access** read “Warehouse” via get\_list · read “Bin” via get\_list.

**Explicit results** list() · mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Stock Value”, “values” → datapoints)), “type” → “bar”).

**Local steps**

- Set tuple(labels, datapoints) from tuple(list(), list()).
- Set filters from Platform.parse\_json(filters).
- Set warehouse\_filters from list(list(“is\_group”, “=”, 0)).
- If (filters and filters.get(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“company”).
  - Evaluate warehouse\_filters.append(list(“company”, “=”, filters.get(“company”))).
- Set warehouses from Platform.get\_list(“Warehouse”, pluck = “name”, filters = warehouse\_filters, order\_by = “name”).
- Set warehouses from Platform.get\_list(“Bin”, fields = list(“warehouse”, mapping(“SUM” → “stock\_value”, “as” → “stock\_value”)), filters = mapping(“warehouse” → list(“IN”, warehouses), “stock\_value” → list(“&gt;”, 0)), group\_by =  ….
- If not warehouses.
  - Return list().
- For each warehouse in warehouses.
  - Evaluate labels.append(translated warehouse.get(“warehouse”)).
  - Evaluate datapoints.append(warehouse.get(“stock\_value”)).
- Return mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Stock Value”, “values” → datapoints)), “type” → “bar”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L690)
