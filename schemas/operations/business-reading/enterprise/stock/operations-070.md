# Inventory and warehouses · operations 70

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Stock ageing

<a id="op-842c2eb7c2622d"></a>
### FIFOSlots.prepare stock reco voucher wise count

`operation_enterprise_stock_report_stock_ageing_business_behavior_first_in_first_out_slots_prepare_stock_reco_voucher_wise_count`

**Inputs** self.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** no value.

**Local steps**

- Set self.stock\_reco\_voucher\_wise\_count from Platform.\_dict().
- Set doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.voucher\_detail\_no, nested operand in the contract.as\_(“count”)).where((((nested operand in the contract equals nested operand i ….
- Set data from query.run(as\_dict = true).
- If not data.
  - Return no value.
- For each row in data.
  - <a id="op-842c2eb7c2622d-guard-26"></a>If row.count differs from 1.
    - Continue with the next iteration or loop test.
  - Set sr\_item from Platform.db.get\_value(“Stock Reconciliation Item”, row.voucher\_detail\_no, list(“current\_qty”, “qty”), as\_dict = true).
  - If (sr\_item and sr\_item.qty and sr\_item.current\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sr\_item → sr\_item.qty → sr\_item.current\_qty.
    - Set self.stock\_reco\_voucher\_wise\_count at row.voucher\_detail\_no from sr\_item.current\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison row.count differs from 1, row.count = 2 selects the branch that continues with the next loop iteration. With row.count = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-842c2eb7c2622d-guard-26)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0906.json#L5269) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L347)

## Report · Stock analytics

<a id="op-4ef48794d8efa1"></a>
### Execute

`operation_enterprise_stock_report_stock_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate is\_reposting\_item\_valuation\_in\_progress().
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set period\_columns from get\_period\_columns(filters).
- Set columns from get\_columns(period\_columns).
- Set data from get\_data(filters).
- Set chart from get\_chart\_data(period\_columns).
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L424)

<a id="op-f3585ed0e3e497"></a>
### Get period columns

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_period_columns`

**Inputs** filters.

**Explicit results** period\_columns.

**Local steps**

- Set period\_columns from list().
- Set ranges from get\_period\_date\_ranges(filters).
- For each tuple(\_dummy, end\_date) in ranges.
  - Set period from get\_period(end\_date, filters).
  - Evaluate period\_columns.append(mapping(“label” → translated period, “fieldname” → scrub(period), “fieldtype” → “Float”, “width” → 120)).
- Return period\_columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0910.json#L6065) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L432)

<a id="op-2e42870a0fae58"></a>
### Get columns

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_columns`

**Inputs** period\_columns.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item”, “options” → “Item”, “fieldname” → “name”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Name”, “options” → “Item”, “fieldname” → “item\_name”, “field ….
- Evaluate columns.extend(period\_columns).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0910.json#L6315) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L427)

<a id="op-c5b6d4a63ad7c5"></a>
### Get period date ranges

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_period_date_ranges`

**Inputs** filters.

**Explicit results** periodic\_daterange.

**Local steps**

- Bind dependencies relativedelta.
- Set from\_date from round\_down\_to\_nearest\_frequency(filters.from\_date, filters.range).
- Set to\_date from getdate(filters.to\_date).
- Set increment from mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(filters.range, 1).
- Set periodic\_daterange from list().
- While true.
  - If filters.range equals “Weekly”.
    - Set period\_end\_date from (from\_date + relativedelta(days = 6)).
  - Otherwise.
    - Set period\_end\_date from (from\_date + relativedelta(months = increment, days = negative 1)).
  - If period\_end\_date &gt; to\_date.
    - Set period\_end\_date from to\_date.
  - Evaluate periodic\_daterange.append(list(from\_date, period\_end\_date)).
  - Set from\_date from (period\_end\_date + relativedelta(days = 1)).
  - If period\_end\_date equals to\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return periodic\_daterange.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L433)

<a id="op-1d49b74cc8c086"></a>
### Round down to nearest frequency

`operation_enterprise_stock_report_stock_analytics_business_behavior_round_down_to_nearest_frequency`

**Inputs** date, frequency.

**Declared result** datetime.datetime.

**Explicit results** round\_down\_function(date).

**Local steps**

- Bind local operation \_get\_first\_day\_of\_fiscal\_year for subsequent calls.
- Set round\_down\_function from mapping(“Monthly” → get\_first\_day\_of\_month, “Quarterly” → get\_quarter\_start, “Weekly” → get\_first\_day\_of\_week, “Yearly” → \_get\_first\_day\_of\_fiscal\_year).get(frequency, getdate).
- Return round\_down\_function(date).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0910.json#L7403) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L436)

<a id="op-f0ab55c8edd625"></a>
### Round down to nearest frequency.get first day of fiscal year

`operation_enterprise_stock_report_stock_analytics_business_behavior_round_down_to_nearest_frequency_get_first_day_of_fiscal_year`

**Inputs** date.

**Explicit results** ((fiscal\_year and fiscal\_year at 1) or date).

**Local steps**

- Set fiscal\_year from get\_fiscal\_year(date).
- Return ((fiscal\_year and fiscal\_year at 1) or date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (fiscal\_year and fiscal\_year at 1) → date.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fiscal\_year → fiscal\_year at 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0910.json#L7629) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L437)

<a id="op-3cfc8f30636e41"></a>
### Get period

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_period`

**Inputs** posting\_date, filters.

**Explicit results** period.

**Local steps**

- Set months from list(“Jan”, “Feb”, “Mar”, “Apr”, …).
- If filters.range equals “Weekly”.
  - Set iso\_date from (get\_first\_day\_of\_week(posting\_date) + datetime.timedelta(days = 6)).isocalendar().
  - Set period from translated “Week {0} {1}”.format(str(iso\_date.week), str(iso\_date.year)).
- Otherwise.
  - If filters.range equals “Monthly”.
    - Set period from ((translated str(months at (nested operand in the contract.month − 1)) + one space) + str(posting\_date.year)).
  - Otherwise.
    - If filters.range equals “Quarterly”.
      - Set period from translated “Quarter {0} {1}”.format(str((((posting\_date.month − 1) floor divide 3) + 1)), str(posting\_date.year)).
    - Otherwise.
      - Set year from get\_fiscal\_year(posting\_date, company = filters.company).
      - Set period from str(year at 2).
- Return period.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L431)

<a id="op-b4dffcd996d853"></a>
### Get period of date

`operation_enterprise_binding_enterprise_stock_report_stock_analytics_stock_analytics_get_period_of_date`

**Inputs** posting\_date, ranges, periods, filters.

**Explicit results** periods at index · get\_period(posting\_date, filters).

**Local steps**

- Set posting\_date from getdate(posting\_date).
- Set index from (bisect\_right(ranges, posting\_date, key = deferred anonymous expression) − 1).
- If (index ≥ 0 and posting\_date ≤ getdate(ranges at index at 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in index ≥ 0 → posting\_date ≤ getdate(ranges at index at 1).
  - Return periods at index.
- Return get\_period(posting\_date, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L998)

<a id="op-2e33be02d92342"></a>
### Get periodic data

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_periodic_data`

**Inputs** entry, filters.

**Explicit results** periodic\_data.

**Local steps**

- Set expected\_ranges from get\_period\_date\_ranges(filters).
- Set expected\_periods from list().
- For each tuple(\_start\_date, end\_date) in expected\_ranges.
  - Evaluate expected\_periods.append(get\_period(end\_date, filters)).
- Set range\_start from getdate(expected\_ranges at 0 at 0) when expected\_ranges, otherwise no value.
  - Value choice on expected\_ranges — true gives getdate(expected\_ranges at 0 at 0), false gives no value.
- Set periodic\_data from mapping().
- For each d in entry.
  - Set period from get\_period\_of\_date(d.posting\_date, expected\_ranges, expected\_periods, filters).
  - Set bal\_qty from 0.
  - Evaluate fill\_intermediate\_periods(periodic\_data, d.item\_code, period, expected\_periods).
  - If (periodic\_data.get(d.item\_code) and not periodic\_data.get(d.item\_code).get(period)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in periodic\_data.get(d.item\_code) → not periodic\_data.get(d.item\_code).get(period).
    - Set previous\_balance from periodic\_data at d.item\_code at “balance”.copy().
    - Set periodic\_data at d.item\_code at period from previous\_balance.
  - If (d.voucher\_type equals “Stock Reconciliation” and not d.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.voucher\_type equals “Stock Reconciliation” → not d.batch\_no.
    - If (periodic\_data.get(d.item\_code) and nested operand in the contract.get(nested operand in the contract.item\_code).get(“balance”).get(d.warehouse)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in periodic\_data.get(d.item\_code) → periodic\_data.get(d.item\_code).get(“balance”).get(d.warehouse).
      - Set bal\_qty from periodic\_data at d.item\_code at “balance” at d.warehouse.
    - Set qty\_diff from (d.qty\_after\_transaction − bal\_qty).
  - Otherwise.
    - Set qty\_diff from d.actual\_qty.
  - If filters at “value\_quantity” equals “Quantity”.
    - Set value from qty\_diff.
  - Otherwise.
    - Set value from d.stock\_value\_difference.
  - Evaluate periodic\_data.setdefault(d.item\_code, mapping()).setdefault(“balance”, mapping()).setdefault(d.warehouse, 0.0).
  - Evaluate periodic\_data.setdefault(d.item\_code, mapping()).setdefault(period, mapping()).setdefault(d.warehouse, 0.0).
  - Update periodic\_data at d.item\_code at “balance” at d.warehouse using + value.
  - Set periodic\_data at d.item\_code at period at d.warehouse from periodic\_data at d.item\_code at “balance” at d.warehouse.
  - If (range\_start and getdate(d.posting\_date) &lt; range\_start).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in range\_start → getdate(d.posting\_date) &lt; range\_start.
    - Set periodic\_data at d.item\_code at OPENING\_KEY from periodic\_data at d.item\_code at “balance”.copy().
- Return periodic\_data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L434)

<a id="op-3fce9a6654b3b3"></a>
### Fill intermediate periods

`operation_enterprise_stock_report_stock_analytics_business_behavior_fill_intermediate_periods`

**Inputs** periodic\_data, item\_code, current\_period, all\_periods.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set previous\_period\_data from no value.
- For each period in all\_periods.
  - If period equals current\_period.
    - Return no value.
  - If (periodic\_data.get(item\_code) and not periodic\_data.get(item\_code).get(period) and previous\_period\_data).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in periodic\_data.get(item\_code) → not periodic\_data.get(item\_code).get(period) → previous\_period\_data.
    - Set periodic\_data at item\_code at period from previous\_period\_data.copy().
  - Set previous\_period\_data from periodic\_data.get(item\_code, mapping()).get(period).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0911.json#L1535) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L425)

<a id="op-a3db51c4ae2594"></a>
### Get data

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set items from get\_items(filters).
- Set sle from get\_stock\_ledger\_entries(filters, items).
- Set item\_details from get\_item\_details(items, sle).
- Set periodic\_data from get\_periodic\_data(sle, filters).
- Set ranges from get\_period\_date\_ranges(filters).
- Set today from getdate().
- For each tuple(\_dummy, item\_data) in item\_details.items().
  - Set row from mapping(“name” → item\_data.name, “item\_name” → item\_data.item\_name, “item\_group” → item\_data.item\_group, “uom” → item\_data.stock\_uom, …).
  - Set previous\_period\_value from sum(nested operand in the contract.get(nested operand in the contract.name, mapping()).get(OPENING\_KEY, mapping()).values()).
  - For each tuple(start\_date, end\_date) in ranges.
    - Set period from get\_period(end\_date, filters).
    - Set period\_data from periodic\_data.get(item\_data.name, mapping()).get(period).
    - If period\_data.
      - Set row at scrub(period), previous\_period\_value from sum(period\_data.values()).
    - Otherwise.
      - Set row at scrub(period) from previous\_period\_value when today ≥ start\_date, otherwise no value.
        - Value choice on today ≥ start\_date — true gives previous\_period\_value, false gives no value.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L428)

<a id="op-1aca99ebca6273"></a>
### Get chart data

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_chart_data`

**Inputs** period\_columns.

**Explicit results** chart.

**Local steps**

- Set labels from list of col.get(“label”) for col drawn from period\_columns.
  - Draw col from period\_columns.
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list())).
- Set chart at “type” from “line”.
- Return chart.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0911.json#L2472) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L426)

<a id="op-e48360b032f6fa"></a>
### Get items

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_items`

**Inputs** filters.

**Record and data access** read “Item” via get\_all.

**Explicit results** list(item\_code) when isinstance(item\_code, str), otherwise list(item\_code) · Platform.get\_all(“Item”, filters = item\_filters, pluck = “name”, order\_by = no value).

**Local steps**

- If item\_code bound to filters.get(“item\_code”).
  - Return list(item\_code) when isinstance(item\_code, str), otherwise list(item\_code).
    - Value choice on isinstance(item\_code, str) — true gives list(item\_code), false gives list(item\_code).
- Otherwise.
  - Set item\_filters from mapping(“is\_stock\_item” → 1).
  - If item\_group bound to filters.get(“item\_group”).
    - Set children from get\_descendants\_of(“Item Group”, item\_group, ignore\_permissions = true).
    - Set item\_filters at “item\_group” from tuple(“in”, list(expanded children, item\_group)).
  - If brand bound to filters.get(“brand”).
    - Set item\_filters at “brand” from brand.
  - Return Platform.get\_all(“Item”, filters = item\_filters, pluck = “name”, order\_by = no value).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0911.json#L2640) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L430)

<a id="op-9694689b6b5d54"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_stock_ledger_entries`

**Inputs** filters, items.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract &lt; nes ….
- If items.
  - Set query from query.where(sle.item\_code.isin(items)).
- Set query from apply\_conditions(query, filters).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0911.json#L3046) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L435)

<a id="op-0975896e0502ad"></a>
### Apply conditions

`operation_enterprise_stock_report_stock_analytics_business_behavior_apply_conditions`

**Inputs** query, filters.

**Explicit results** query.

**Explicit failure paths** validation helper — translated “'From Date' is required” · validation helper — translated “'To Date' is required”.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set warehouse\_table from Platform.qb.DocType(“Warehouse”).
- If not filters.get(“from\_date”).
  - Call the validation error handler Platform.throw(translated “'From Date' is required”).
- If to\_date bound to filters.get(“to\_date”).
  - Set to\_date from get\_datetime((str(to\_date) + “ 23:59:59.999999”)).
  - Set query from query.where(sle.posting\_datetime ≤ to\_date).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “'To Date' is required”).
- If company bound to filters.get(“company”).
  - Set query from query.where(sle.company equals company).
- If warehouses bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Warehouse”, list()), “Stock Entry”).
  - Set query from query.where(sle.warehouse.isin(warehouses)).
- If companies bound to get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“Company”, list()), “Stock Ledger Entry”).
  - Set query from query.where(sle.company.isin(companies)).
- If filters.get(“warehouse”).
  - Set query from apply\_warehouse\_filter(query, sle, filters).
- Otherwise.
  - If warehouse\_type bound to filters.get(“warehouse\_type”).
    - Set query from query.join(warehouse\_table).on(warehouse\_table.name equals sle.warehouse).where(warehouse\_table.warehouse\_type equals warehouse\_type).
- Return query.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L423)

<a id="op-bd891951953aba"></a>
### Get item details

`operation_enterprise_stock_report_stock_analytics_business_behavior_get_item_details`

**Inputs** items, sle.

**Explicit results** item\_details.

**Local steps**

- Set item\_details from mapping().
- If not items.
  - Set items from list(set(generator of d.item\_code for d drawn from sle)).
    - Draw d from sle.
- If not items.
  - Return item\_details.
- Set item\_table from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item\_table).select(item\_table.name, item\_table.item\_name, item\_table.description, item\_table.item\_group, …).where(item\_table.name.isin(items)).
- If condition bound to get\_allowed\_masters\_condition(item\_table.name, “Item”).
  - Set query from query.where(condition).
- Set result from query.run(as\_dict = 1).
- For each item\_table in result.
  - Evaluate item\_details.setdefault(item\_table.name, item\_table).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L429)

## Report · Stock and account value comparison

<a id="op-21471b885d7440"></a>
### Execute

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Perpetual inventory required for the company {0} to view this report.”.format(filters.company).

**Local steps**

- If not Enterprise.is\_perpetual\_inventory\_enabled(filters.company).
  - Call the validation error handler Platform.throw(translated “Perpetual inventory required for the company {0} to view this report.”.format(filters.company)).
- Set filters.as\_on\_date from (filters.get(“as\_on\_date”) or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“as\_on\_date”) → today().
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Return tuple(columns, data).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L449)

<a id="op-0dd09e8ce8dd70"></a>
### Get data

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_get_data`

**Inputs** report\_filters.

**Explicit results** data.

**Explicit failure paths** validation helper — translated “From Date cannot be after As On Date”.

**Local steps**

- Set data from list().
- Set filters from mapping(“is\_cancelled” → 0, “company” → report\_filters.company, “posting\_date” → tuple(“&lt;=”, report\_filters.as\_on\_date)).
- If report\_filters.get(“from\_date”).
  - If (report\_filters.as\_on\_date and getdate(report\_filters.from\_date) &gt; getdate(report\_filters.as\_on\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_filters.as\_on\_date → getdate(report\_filters.from\_date) &gt; getdate(report\_filters.as\_on\_date).
    - Call the validation error handler Platform.throw(translated “From Date cannot be after As On Date”).
  - Set filters at “posting\_date” from tuple(“between”, list(report\_filters.from\_date, report\_filters.as\_on\_date)).
- Evaluate (get\_currency\_precision() or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_currency\_precision() → 2.
- Set stock\_ledger\_entries from get\_stock\_ledger\_data(report\_filters, filters).
- Set voucher\_wise\_gl\_data from get\_gl\_data(report\_filters, filters).
- For each d in stock\_ledger\_entries.
  - Set key from tuple(d.voucher\_type, d.voucher\_no).
  - Set gl\_data from (voucher\_wise\_gl\_data.get(key) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in voucher\_wise\_gl\_data.get(key) → mapping().
  - Set d.account\_value from gl\_data.get(“account\_value”, 0).
  - Set d.difference\_value from (d.stock\_value − d.account\_value).
  - Set d.ledger\_type from “Stock Ledger Entry”.
  - If abs(d.difference\_value) &gt; 0.1.
    - Evaluate data.append(d).
  - If key belongs to voucher\_wise\_gl\_data.
    - Remove voucher\_wise\_gl\_data at key.
- If voucher\_wise\_gl\_data.
  - Update data using + get\_gl\_ledgers\_with\_no\_stock\_ledger\_entries(voucher\_wise\_gl\_data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L451)

<a id="op-e0776595a8f3e3"></a>
### Get gl ledgers with no stock ledger entries

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_get_general_ledger_ledgers_with_number_stock_ledger_entries`

**Inputs** voucher\_wise\_gl\_data.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each key in voucher\_wise\_gl\_data.
  - Set gl\_data from (voucher\_wise\_gl\_data.get(key) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in voucher\_wise\_gl\_data.get(key) → mapping().
  - Evaluate data.append(mapping(“name” → gl\_data.get(“name”), “ledger\_type” → “GL Entry”, “voucher\_type” → gl\_data.get(“voucher\_type”), “voucher\_no” → gl\_data.get(“voucher\_no”), …)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0912.json#L618) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L453)

<a id="op-40f738a51cf423"></a>
### Get stock ledger data

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_get_stock_ledger_data`

**Inputs** report\_filters, filters.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, filters = filters, fields = list(“name”, “voucher\_type”, “voucher\_no”, mapping(“SUM” → “stock\_value\_difference”, “as” → “stock\_value”), …), group\_by = “voucher\_type,  ….

**Local steps**

- If report\_filters.account.
  - Set warehouses from get\_warehouses\_based\_on\_account(report\_filters.account, report\_filters.company).
  - Set filters at “warehouse” from tuple(“in”, warehouses).
- Return Platform.get\_all(“Stock Ledger Entry”, filters = filters, fields = list(“name”, “voucher\_type”, “voucher\_no”, mapping(“SUM” → “stock\_value\_difference”, “as” → “stock\_value”), …), group\_by = “voucher\_type,  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L842) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L454)

<a id="op-a78d3c810374a7"></a>
### Get gl data

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_get_general_ledger_data`

**Inputs** report\_filters, filters.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** voucher\_wise\_gl\_data.

**Local steps**

- If report\_filters.account.
  - Set stock\_accounts from list(report\_filters.account).
- Otherwise.
  - Set stock\_accounts from get\_stock\_accounts(report\_filters.company).
- Evaluate filters.update(mapping(“account” → tuple(“in”, stock\_accounts))).
- If filters.get(“warehouse”).
  - Remove filters at “warehouse”.
- Set gl\_entries from Platform.get\_all(“GL Entry”, filters = filters, fields = list(“name”, “voucher\_type”, “voucher\_no”, “posting\_date”, …), group\_by = “voucher\_type, voucher\_no”).
- Set voucher\_wise\_gl\_data from mapping().
- For each d in gl\_entries.
  - Set key from tuple(d.voucher\_type, d.voucher\_no).
  - Set voucher\_wise\_gl\_data at key from d.
- Return voucher\_wise\_gl\_data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L452)

<a id="op-5213cd8be7c752"></a>
### Get columns

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Stock Ledger ID”, “fieldname” → “name”, “fieldtype” → “Dynamic Link”, “options” → “ledger\_type”, …), mapping(“label” → translated “Ledger Type”, “fieldname” → “ledger\_typ ….

**Local steps**

- Return list(mapping(“label” → translated “Stock Ledger ID”, “fieldname” → “name”, “fieldtype” → “Dynamic Link”, “options” → “ledger\_type”, …), mapping(“label” → translated “Ledger Type”, “fieldname” → “ledger\_typ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L450)

<a id="op-aa324f79271b32"></a>
### Create reposting entries

`operation_enterprise_stock_report_stock_and_account_value_comparison_business_behavior_create_reposting_entries`

**Inputs** rows, company.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → item\_code, …) via get\_doc.

**State and service calls** call submit on Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → item\_code, …)) · msgprint with translated “Reposting entries created: {0}”.format(entries).

**Local steps**

- If isinstance(rows, str).
  - Set rows from parse\_json(rows).
- Set entries from list().
- Set item\_wh from Platform.\_dict().
- Set vouchers from list of row.get(“voucher\_no”) for row drawn from rows where row.get(“voucher\_type”) does not belong to list(“Purchase Receipt”, “Purchase Invoice”).
  - Draw row from rows, keep a combination only if (row.get(“voucher\_type”) does not belong to list(“Purchase Receipt”, “Purchase Invoice”)).
- Evaluate repost\_based\_on\_transaction(rows, company, entries).
- Set sles from get\_stock\_ledgers(vouchers).
- For each sle in sles.
  - Set key from tuple(sle.item\_code, sle.warehouse).
  - If key does not belong to item\_wh.
    - Set item\_wh at key from sle.
  - Otherwise.
    - If get\_datetime(item\_wh.get(key).posting\_datetime) &gt; get\_datetime(sle.posting\_datetime).
      - Set item\_wh at key from sle.
- For each tuple(key, sle) in item\_wh.items().
  - Set tuple(item\_code, warehouse) from key.
  - Attempt the following.
    - Set doc from Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “based\_on” → “Item and Warehouse”, “status” → “Queued”, “item\_code” → item\_code, …)).submit().
    - Evaluate entries.append(get\_link\_to\_form(“Repost Item Valuation”, doc.name)).
  - On failure (Platform.DuplicateEntryError).
    - Take no action here.
- If entries.
  - Set entries from “, ”.join(entries).
  - Evaluate Platform.msgprint(translated “Reposting entries created: {0}”.format(entries)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L448)
