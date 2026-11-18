# Accounting and settlement · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Budget

[Record definition](../../../../data/record-types/budget.json)

<a id="op-eb334470507d23"></a>
### Get accumulated monthly budget

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_accumulated_monthly_budget`

**Inputs** budget\_name, posting\_date.

**Explicit results** flt(result at 0 at “accumulated\_amount”) when result, otherwise 0.0.

**Local steps**

- Set posting\_date from getdate(posting\_date).
- Set bd from Platform.qb.DocType(“Budget Distribution”).
- Set b from Platform.qb.DocType(“Budget”).
- Set result from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals budget\_name).where(bd.start\_date ≤ posting\_date).run(as\_dict = true).
- Return flt(result at 0 at “accumulated\_amount”) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0 at “accumulated\_amount”), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L1459) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L588)

<a id="op-bc0b8f924be760"></a>
### Get item details

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_item_details`

**Inputs** params.

**Record and data access** read “Item Default” via get\_value.

**Explicit results** tuple(cost\_center, expense\_account).

**Local steps**

- Set tuple(cost\_center, expense\_account) from tuple(no value, no value).
- If not params.get(“company”).
  - Return tuple(cost\_center, expense\_account).
- If params.item\_code.
  - Set item\_defaults from Platform.db.get\_value(“Item Default”, mapping(“parent” → params.item\_code, “company” → params.get(“company”)), list(“buying\_cost\_center”, “expense\_account”)).
  - If item\_defaults.
    - Set tuple(cost\_center, expense\_account) from item\_defaults.
- If not (cost\_center and expense\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cost\_center → expense\_account.
  - For each doctype in list(“Item Group”, “Company”).
    - Set data from get\_expense\_cost\_center(doctype, params).
    - If (not cost\_center and data).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → data.
      - Set cost\_center from data at 0.
    - If (not expense\_account and data).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not expense\_account → data.
      - Set expense\_account from data at 1.
    - If (cost\_center and expense\_account).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cost\_center → expense\_account.
      - Return tuple(cost\_center, expense\_account).
- Return tuple(cost\_center, expense\_account).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L1867) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L594)

<a id="op-309cf29d857c12"></a>
### Get expense cost center

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_expense_cost_center`

**Inputs** doctype, params.

**Record and data access** read “Item Default” via get\_value · read doctype via get\_value.

**Explicit results** Platform.db.get\_value(“Item Default”, mapping(“parent” → params.get(Platform.scrub(doctype)), “company” → params.get(“company”)), list(“buying\_cost\_center”, “expense\_account”)) · Platform.db.get\_value(doctype, params.get(Platform.scrub(doctype)), list(“cost\_center”, “default\_expense\_account”)).

**Local steps**

- If doctype equals “Item Group”.
  - Return Platform.db.get\_value(“Item Default”, mapping(“parent” → params.get(Platform.scrub(doctype)), “company” → params.get(“company”)), list(“buying\_cost\_center”, “expense\_account”)).
- Otherwise.
  - Return Platform.db.get\_value(doctype, params.get(Platform.scrub(doctype)), list(“cost\_center”, “default\_expense\_account”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L2376) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L592)

<a id="op-065933afac3673"></a>
### Get fiscal year date range

`operation_enterprise_accounts_record_definitions_budget_business_behavior_get_fiscal_year_date_range`

**Inputs** from\_fiscal\_year, to\_fiscal\_year.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** tuple(from\_year.year\_start\_date, to\_year.year\_end\_date).

**Local steps**

- Set from\_year from Platform.get\_cached\_value(“Fiscal Year”, from\_fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).
- Set to\_year from Platform.get\_cached\_value(“Fiscal Year”, to\_fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).
- Return tuple(from\_year.year\_start\_date, to\_year.year\_end\_date).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, from\_fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true), Platform.get\_cached\_value(“Fiscal Year”, to\_fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L2674) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L593)

<a id="op-bb175f1fe65ad0"></a>
### Revise budget

`operation_enterprise_accounts_record_definitions_budget_business_behavior_revise_budget`

**Inputs** budget\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Budget” via get\_doc.

**State and service calls** call cancel on old\_budget · request copy\_doc for old\_budget · call insert on new\_budget.

**Explicit results** new\_budget.name.

**Local steps**

- Set old\_budget from Platform.get\_doc(“Budget”, budget\_name).
- If old\_budget.docstatus equals 1.
  - Evaluate old\_budget.cancel().
- Set new\_budget from Platform.copy\_doc(old\_budget).
- Set new\_budget.docstatus from 0.
- Set new\_budget.revision\_of from old\_budget.name.
- Evaluate new\_budget.insert().
- Return new\_budget.name.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0034.json#L2877) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L598)

## Report · Budget variance report

<a id="op-fd27148720be21"></a>
### Execute

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, list(), no value, no value) · tuple(columns, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- If filters.get(“budget\_against\_filter”).
  - Set dimensions from filters.get(“budget\_against\_filter”).
  - If filters.get(“budget\_against”) equals “Cost Center”.
    - Set dimensions from get\_cost\_center\_with\_children(dimensions).
- Otherwise.
  - Set dimensions from get\_budget\_dimensions(filters).
- Set dimensions from get\_permitted\_dimensions(filters.get(“budget\_against”), dimensions).
- If not dimensions.
  - Return tuple(columns, list(), no value, no value).
- Set budget\_records from get\_budget\_records(filters, dimensions).
- Set budget\_map from build\_budget\_map(budget\_records, filters).
- Set data from build\_report\_data(budget\_map, filters).
- Set chart\_data from build\_comparison\_chart\_data(filters, columns, data).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L704)

<a id="op-e9fe7b20623b88"></a>
### Validate filters

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_validate_filters`

**Inputs** filters.

**Local steps**

- Evaluate validate\_budget\_dimensions(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0232.json#L3299) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L716)

<a id="op-473ef2b043ffe4"></a>
### Get budget records

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_budget_records`

**Inputs** filters, dimensions.

**Explicit results** nested operand in the contract(nested operand in the contract).select(budget.name, budget.account, nested operand in the contract.as\_(“dimension”), budget.budget\_amount, …).where(((((nested operand in the  ….

**Local steps**

- Set budget\_against\_field from Platform.scrub(filters at “budget\_against”).
- Set budget from Platform.qb.DocType(“Budget”).
- Return nested operand in the contract(nested operand in the contract).select(budget.name, budget.account, nested operand in the contract.as\_(“dimension”), budget.budget\_amount, …).where(((((nested operand in the  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0232.json#L3351) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L708)

<a id="op-5092aea5a9c500"></a>
### Build budget map

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_build_budget_map`

**Inputs** budget\_records, filters.

**Explicit results** budget\_map.

**Local steps**

- Set budget\_map from mapping().
- For each budget in budget\_records.
  - Set actual\_amt from get\_actual\_transactions(budget.dimension, filters).
  - Evaluate budget\_map.setdefault(budget.dimension, mapping()).
  - Evaluate budget\_map at budget.dimension.setdefault(budget.account, mapping()).
  - Set budget\_distributions from get\_budget\_distributions(budget).
  - For each row in budget\_distributions.
    - If (not row.start\_date or not row.end\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.start\_date → not row.end\_date.
      - Continue with the next iteration or loop test.
    - Set months from get\_months\_in\_range(row.start\_date, row.end\_date).
    - If not months.
      - Continue with the next iteration or loop test.
    - Set monthly\_budget from (flt(row.amount) ÷ len(months)).
    - For each month\_date in months.
      - Set fiscal\_year from get\_fiscal\_year(month\_date) at 0.
      - Set month from month\_date.strftime(“%B”).
      - Evaluate budget\_map at budget.dimension at budget.account.setdefault(fiscal\_year, mapping()).
      - Evaluate budget\_map at budget.dimension at budget.account at fiscal\_year.setdefault(month, mapping(“budget” → 0, “actual” → 0)).
      - Update budget\_map at budget.dimension at budget.account at fiscal\_year at month at “budget” using + monthly\_budget.
      - For each ad in actual\_amt.get(budget.account, list()).
        - If (ad.month\_name equals month and ad.fiscal\_year equals fiscal\_year).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in ad.month\_name equals month → ad.fiscal\_year equals fiscal\_year.
          - Update budget\_map at budget.dimension at budget.account at fiscal\_year at month at “actual” using + (flt(ad.debit) − flt(ad.credit)).
- Return budget\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0232.json#L3791) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L701)

<a id="op-9f1ab6538675df"></a>
### Get actual transactions

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_actual_transactions`

**Inputs** dimension\_name, filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** actual\_transactions\_map.

**Local steps**

- Set budget\_against from Platform.scrub(filters.get(“budget\_against”)).
- Set monthname from CustomFunction(“MONTHNAME”, list(“date”)).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set budget from Platform.qb.DocType(“Budget”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set company\_finance\_book from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- Set query from query.where((gle.finance\_book.isin(list(empty text, cstr(company\_finance\_book))) bitwise or gle.finance\_book.isnull())).
- If (filters.get(“budget\_against”) equals “Cost Center” and dimension\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“budget\_against”) equals “Cost Center” → dimension\_name.
  - Set cost\_centers from get\_cost\_center\_with\_children(list(dimension\_name)).
  - Set query from query.where(gle.cost\_center.isin(cost\_centers)).
- Otherwise.
  - Set query from query.where(budget at budget\_against equals gle at budget\_against).
- Set actual\_transactions from query.run(as\_dict = true).
- Set actual\_transactions\_map from mapping().
- For each transaction in actual\_transactions.
  - Evaluate actual\_transactions\_map.setdefault(transaction.account, list()).append(transaction).
- Return actual\_transactions\_map.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L705)

<a id="op-eae9c1590d96d9"></a>
### Get budget distributions

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_budget_distributions`

**Inputs** budget.

**Record and data access** execute query text (SELECT, Budget Distribution).

**Explicit results** Platform.db.sql(query text (SELECT, Budget Distribution), tuple(budget.name), as\_dict = true).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Budget Distribution), tuple(budget.name), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L707)

<a id="op-434aaea79c990b"></a>
### Get months in range

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_months_in_range`

**Inputs** start\_date, end\_date.

**Explicit results** months.

**Local steps**

- Set months from list().
- Set current from start\_date.
- While current ≤ end\_date.
  - Evaluate months.append(current).
  - Set current from add\_months(current, 1).
- Return months.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0232.json#L5606) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L713)

<a id="op-83d86e85d9bb9d"></a>
### Build report data

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_build_report_data`

**Inputs** budget\_map, filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set show\_cumulative from (filters.get(“show\_cumulative”) and filters.get(“period”) differs from “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“show\_cumulative”) → filters.get(“period”) differs from “Yearly”.
- Set periods from get\_periods(filters).
- For each tuple(dimension, accounts) in budget\_map.items().
  - For each tuple(account, fiscal\_year\_map) in accounts.items().
    - Set row from mapping(“budget\_against” → dimension, “account” → account).
    - Set running\_budget from 0.
    - Set running\_actual from 0.
    - Set total\_budget from 0.
    - Set total\_actual from 0.
    - For each period in periods.
      - Set fiscal\_year from period at “fiscal\_year”.
      - Set months from get\_months\_between(period at “from\_date”, period at “to\_date”).
      - Set period\_budget from 0.
      - Set period\_actual from 0.
      - Set month\_map from fiscal\_year\_map.get(fiscal\_year, mapping()).
      - For each month in months.
        - Set values from month\_map.get(month).
        - If values.
          - Update period\_budget using + values.get(“budget”, 0).
          - Update period\_actual using + values.get(“actual”, 0).
      - If show\_cumulative.
        - Update running\_budget using + period\_budget.
        - Update running\_actual using + period\_actual.
        - Set display\_budget from running\_budget.
        - Set display\_actual from running\_actual.
      - Otherwise.
        - Set display\_budget from period\_budget.
        - Set display\_actual from period\_actual.
      - Update total\_budget using + period\_budget.
      - Update total\_actual using + period\_actual.
      - If filters at “period” equals “Yearly”.
        - Set budget\_label from ((translated “Budget” + one space) + fiscal\_year).
        - Set actual\_label from ((translated “Actual” + one space) + fiscal\_year).
        - Set variance\_label from ((translated “Variance” + one space) + fiscal\_year).
      - Otherwise.
        - Set budget\_label from (translated “Budget” + formatted text  ({period at “label\_suffix”}) {fiscal\_year}).
        - Set actual\_label from (translated “Actual” + formatted text  ({period at “label\_suffix”}) {fiscal\_year}).
        - Set variance\_label from (translated “Variance” + formatted text  ({period at “label\_suffix”}) {fiscal\_year}).
      - Set row at Platform.scrub(budget\_label) from display\_budget.
      - Set row at Platform.scrub(actual\_label) from display\_actual.
      - Set row at Platform.scrub(variance\_label) from (display\_budget − display\_actual).
    - If filters at “period” differs from “Yearly”.
      - Set row at “total\_budget” from total\_budget.
      - Set row at “total\_actual” from total\_actual.
      - Set row at “total\_variance” from (total\_budget − total\_actual).
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L703)

<a id="op-b8eb7452893239"></a>
### Get periods

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_periods`

**Inputs** filters.

**Explicit results** periods.

**Local steps**

- Set periods from list().
- Set group\_months from filters at “period” differs from “Monthly”.
- For each tuple(fiscal\_year) in get\_fiscal\_years(filters).
  - For each tuple(from\_date, to\_date) in get\_period\_date\_ranges(filters at “period”, fiscal\_year).
    - If filters at “period” equals “Yearly”.
      - Set label\_suffix from fiscal\_year.
    - Otherwise.
      - If group\_months.
        - Set label\_suffix from ((formatdate(from\_date, “MMM”) + “-”) + formatdate(to\_date, “MMM”)).
      - Otherwise.
        - Set label\_suffix from formatdate(from\_date, “MMM”).
    - Evaluate periods.append(mapping(“fiscal\_year” → fiscal\_year, “from\_date” → from\_date, “to\_date” → to\_date, “label\_suffix” → label\_suffix)).
- Return periods.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L1346) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L714)

<a id="op-65b4df43852784"></a>
### Get months between

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_months_between`

**Inputs** from\_date, to\_date.

**Explicit results** months.

**Local steps**

- Set months from list().
- Set current from from\_date.
- While current ≤ to\_date.
  - Evaluate months.append(formatdate(current, “MMMM”)).
  - Set current from add\_months(current, 1).
- Return months.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L1753) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L712)

<a id="op-fe65f05aa0b923"></a>
### Get columns

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated filters.get(“budget\_against”), “fieldtype” → “Link”, “fieldname” → “budget\_against”, “options” → filters.get(“budget\_against”), …), mapping(“label” → translated “Account”, ….
- Set group\_months from false when filters at “period” equals “Monthly”, otherwise true.
  - Value choice on filters at “period” equals “Monthly” — true gives false, false gives true.
- Set fiscal\_year from get\_fiscal\_years(filters).
- For each year in fiscal\_year.
  - For each tuple(from\_date, to\_date) in get\_period\_date\_ranges(filters at “period”, year at 0).
    - If filters at “period” equals “Yearly”.
      - Set labels from list(((translated “Budget” + one space) + str(year at 0)), ((translated “Actual” + one space) + str(year at 0)), ((translated “Variance” + one space) + str(year at 0))).
      - For each label in labels.
        - Evaluate columns.append(mapping(“label” → label, “fieldtype” → “Float”, “fieldname” → Platform.scrub(label), “width” → 150)).
    - Otherwise.
      - For each label in list((((translated “Budget” + “ (%s)”) + one space) + str(year at 0)), (((translated “Actual” + “ (%s)”) + one space) + str(year at 0)), (((translated “Variance” + “ (%s)”) + one space) + str(year at 0))).
        - If group\_months.
          - Set label from (label modulo or format ((formatdate(from\_date, format\_string = “MMM”) + “-”) + formatdate(to\_date, format\_string = “MMM”))).
        - Otherwise.
          - Set label from (label modulo or format formatdate(from\_date, format\_string = “MMM”)).
        - Evaluate columns.append(mapping(“label” → label, “fieldtype” → “Float”, “fieldname” → Platform.scrub(label), “width” → 150)).
- If filters at “period” differs from “Yearly”.
  - For each label in list(translated “Total Budget”, translated “Total Actual”, translated “Total Variance”).
    - Evaluate columns.append(mapping(“label” → label, “fieldtype” → “Float”, “fieldname” → Platform.scrub(label), “width” → 150)).
  - Return columns.
- Otherwise.
  - Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L1917) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L709)

<a id="op-d16b98cc07430b"></a>
### Get fiscal years

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_fiscal_years`

**Inputs** filters.

**Record and data access** execute query text (SELECT, Fiscal Year).

**Explicit results** fiscal\_year.

**Local steps**

- Set fiscal\_year from Platform.db.sql(query text (SELECT, Fiscal Year), mapping(“from\_fiscal\_year” → filters at “from\_fiscal\_year”, “to\_fiscal\_year” → filters at “to\_fiscal\_year”)).
- Return fiscal\_year.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L711)

<a id="op-d2102d22caf5e7"></a>
### Get cost center with children

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_cost_center_with_children`

**Inputs** cost\_centers.

**Record and data access** read “Cost Center” via get\_value.

**Explicit results** list(all\_cost\_centers).

**Local steps**

- Set cc from Platform.qb.DocType(“Cost Center”).
- Set all\_cost\_centers from set().
- For each cost\_center in cost\_centers.
  - Set result from Platform.db.get\_value(“Cost Center”, cost\_center, list(“lft”, “rgt”)).
  - If not result.
    - Continue with the next iteration or loop test.
  - Set tuple(lft, rgt) from result.
  - Set children from nested operand in the contract(nested operand in the contract).select(cc.name).where((cc.lft ≥ lft bitwise and cc.rgt ≤ rgt)).run(pluck = “name”).
  - Evaluate all\_cost\_centers.update(children).
- Return list(all\_cost\_centers).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L3523) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L710)

<a id="op-9f1ed2083bfcaf"></a>
### Get budget dimensions

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_get_budget_dimensions`

**Inputs** filters.

**Explicit results** query.run(pluck = “name”) · nested operand in the contract.qb.from\_(dimension).select(dimension.name).run(pluck = “name”).

**Local steps**

- Set budget\_against from filters.get(“budget\_against”).
- Set dimension from Platform.qb.DocType(budget\_against).
- If budget\_against belongs to list(“Cost Center”, “Project”).
  - Set query from nested operand in the contract.qb.from\_(dimension).select(dimension.name).where(dimension.company equals filters.get(“company”)).
  - If budget\_against equals “Cost Center”.
    - Set query from query.orderby(dimension.lft).
  - Return query.run(pluck = “name”).
- Otherwise.
  - Return nested operand in the contract.qb.from\_(dimension).select(dimension.name).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L3914) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L706)

<a id="op-e61530282039d5"></a>
### Get permitted dimensions

`operation_enterprise_binding_enterprise_accounts_report_budget_variance_report_budget_variance_report_get_permitted_dimensions`

**Inputs** budget\_against, dimensions.

**Declared result** list.

**Record and data access** read budget\_against via get\_list.

**Explicit results** list() · list of dimension for dimension drawn from dimensions where dimension belongs to permitted.

**Local steps**

- If not dimensions.
  - Return list().
- Set permitted from set(Platform.get\_list(budget\_against, filters = mapping(“name” → list(“in”, dimensions)), pluck = “name”)).
- Return list of dimension for dimension drawn from dimensions where dimension belongs to permitted.
  - Draw dimension from dimensions, keep a combination only if (dimension belongs to permitted).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1137)

<a id="op-c8d3ed99e034be"></a>
### Validate budget dimensions

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_validate_budget_dimensions`

**Inputs** filters.

**Explicit failure paths** validation helper.

**Local steps**

- Set dimensions from list of d.get(“document\_type”) for d drawn from get\_dimensions(with\_cost\_center\_and\_project = true) at 0.
  - Draw d from get\_dimensions(with\_cost\_center\_and\_project = true) at 0.
- If (filters.get(“budget\_against”) and filters.get(“budget\_against”) does not belong to dimensions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“budget\_against”) → filters.get(“budget\_against”) does not belong to dimensions.
  - Call the validation error handler Platform.throw(title = translated “Invalid Accounting Dimension”, msg = translated “{0} is not a valid Accounting Dimension.”.format(Platform.bold(filters.get(“budget\_against”)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L4329) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L715)

<a id="op-2f28f29d878374"></a>
### Build comparison chart data

`operation_enterprise_accounts_report_budget_variance_report_business_behavior_build_comparison_chart_data`

**Inputs** filters, columns, data.

**Explicit results** no value · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Budget”, “chartType” → “bar”, “values” → budget\_values), mapping(“name” → translated “Actual Expense”, “chartType” ….

**Local steps**

- If not data.
  - Return no value.
- Set budget\_fields from list().
- Set actual\_fields from list().
- For each col in columns.
  - Set fieldname from col.get(“fieldname”).
  - If not fieldname.
    - Continue with the next iteration or loop test.
  - If fieldname equals “budget\_against”.
    - Continue with the next iteration or loop test.
  - If fieldname.startswith(“budget\_”).
    - Evaluate budget\_fields.append(fieldname).
  - Otherwise.
    - If fieldname.startswith(“actual\_”).
      - Evaluate actual\_fields.append(fieldname).
- If (not budget\_fields or not actual\_fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not budget\_fields → not actual\_fields.
  - Return no value.
- Set labels from list of col at “label”.replace(“Budget”, empty text).strip() for col drawn from columns where (col.get(“fieldname”, empty text).startswith(“budget\_”) and col.get(“fieldname”) differs from “budget\_against”).
  - Draw col from columns, keep a combination only if ((col.get(“fieldname”, empty text).startswith(“budget\_”) and col.get(“fieldname”) differs from “budget\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“fieldname”, empty text).startswith(“budget\_”) → col.get(“fieldname”) differs from “budget\_against”.
- Set budget\_values from (list(0) × len(budget\_fields)).
- Set actual\_values from (list(0) × len(actual\_fields)).
- For each row in data.
  - For each tuple(i, field) in enumerate(budget\_fields).
    - Update budget\_values at i using + flt(row.get(field)).
  - For each tuple(i, field) in enumerate(actual\_fields).
    - Update actual\_values at i using + flt(row.get(field)).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Budget”, “chartType” → “bar”, “values” → budget\_values), mapping(“name” → translated “Actual Expense”, “chartType” ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0233.json#L4635) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L702)

## Report · Calculated discount mismatch

<a id="op-e5f2976882aab7"></a>
### Execute

`operation_enterprise_accounts_report_calculated_discount_mismatch_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0234.json#L1035) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L727)

<a id="op-a4af5d731dadf7"></a>
### Get columns

`operation_enterprise_accounts_report_calculated_discount_mismatch_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “doctype”, “label” → translated “Transaction Type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“fieldname” → “docname”, “label” → translated “Transaction Name”, “fi ….

**Local steps**

- Return list(mapping(“fieldname” → “doctype”, “label” → translated “Transaction Type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“fieldname” → “docname”, “label” → translated “Transaction Name”, “fi ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L728)
