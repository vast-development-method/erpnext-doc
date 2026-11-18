# Production · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Dashboard fixtures

<a id="op-0a30b7f4e6f3ff"></a>
### Get dashboards

`operation_enterprise_manufacturing_dashboard_fixtures_business_behavior_get_dashboards`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“name” → “Manufacturing”, “dashboard\_name” → “Manufacturing”, “charts” → list(mapping(“chart” → “Produced Quantity”, “width” → “Half”), mapping(“chart” → “Completed Operation”, “width” → “Half”), m …).

**Local steps**

- Return list(mapping(“name” → “Manufacturing”, “dashboard\_name” → “Manufacturing”, “charts” → list(mapping(“chart” → “Produced Quantity”, “width” → “Half”), mapping(“chart” → “Completed Operation”, “width” → “Half”), m …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L412) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L141)

<a id="op-0d089008b408b9"></a>
### Get charts

`operation_enterprise_manufacturing_dashboard_fixtures_business_behavior_get_charts`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_value.

**Explicit results** list(mapping(“doctype” → “Dashboard Chart”, “based\_on” → “modified”, “chart\_type” → “Sum”, “chart\_name” → translated “Produced Quantity”, …), mapping(“doctype” → “Dashboard Chart”, “based\_on” → “creation”, ….

**Local steps**

- Set company from Enterprise.get\_default\_company().
- If not company.
  - Set company from Platform.db.get\_value(“Company”, mapping(“is\_group” → 0), “name”).
- Return list(mapping(“doctype” → “Dashboard Chart”, “based\_on” → “modified”, “chart\_type” → “Sum”, “chart\_name” → translated “Produced Quantity”, …), mapping(“doctype” → “Dashboard Chart”, “based\_on” → “creation”, ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L893) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L140)

<a id="op-2ffec8479c2fd1"></a>
### Get number cards

`operation_enterprise_manufacturing_dashboard_fixtures_business_behavior_get_number_cards`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“doctype” → “Number Card”, “document\_type” → “Work Order”, “name” → “Monthly Total Work Order”, “filters\_json” → json.dumps(list(list(“Work Order”, “docstatus”, “=”, 1), list(“Work Order”, “cr ….

**Local steps**

- Set start\_date from add\_months(nowdate(), negative 1).
- Set end\_date from nowdate().
- Return list(mapping(“doctype” → “Number Card”, “document\_type” → “Work Order”, “name” → “Monthly Total Work Order”, “filters\_json” → json.dumps(list(list(“Work Order”, “docstatus”, “=”, 1), list(“Work Order”, “cr ….

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0451.json#L3559) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L143)

## Report · Downtime analysis

<a id="op-6c1a3dc81541c6"></a>
### Execute

`operation_enterprise_manufacturing_report_downtime_analysis_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Set chart\_data from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0544.json#L5800) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1069)

<a id="op-2ed0d001428d6d"></a>
### Get data

`operation_enterprise_manufacturing_report_downtime_analysis_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Downtime Entry” via get\_list.

**Explicit results** data.

**Local steps**

- Set query\_filters from mapping().
- Set fields from list(“name”, “workstation”, “operator”, “from\_time”, …).
- Set from\_date from get\_datetime(filters.get(“from\_date”)).
- Set to\_date from get\_datetime(filters.get(“to\_date”)).
- Evaluate validate\_date\_range(filters).
- Set query\_filters at “from\_time” from tuple(“&lt;”, to\_date).
- Set query\_filters at “to\_time” from tuple(“&gt;”, from\_date).
- If filters.get(“workstation”).
  - Set query\_filters at “workstation” from filters.get(“workstation”).
- Set data from (Platform.get\_list(“Downtime Entry”, fields = fields, filters = query\_filters, limit\_page\_length = 0) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_list(“Downtime Entry”, fields = fields, filters = query\_filters, limit\_page\_length = 0) → list().
- For each d in data.
  - Set d.downtime from time\_diff\_in\_hours(min(get\_datetime(d.to\_time), to\_date), max(get\_datetime(d.from\_time), from\_date)).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1072)

<a id="op-8f743155e98e2b"></a>
### Get chart data

`operation_enterprise_manufacturing_report_downtime_analysis_business_behavior_get_chart_data`

**Inputs** data, columns.

**Explicit results** chart.

**Local steps**

- Set labels from sorted(list(set(list of d.workstation for d drawn from data))).
  - Draw d from data.
- Set workstation\_wise\_data from mapping().
- For each d in data.
  - If d.workstation does not belong to workstation\_wise\_data.
    - Set workstation\_wise\_data at d.workstation from 0.
  - Update workstation\_wise\_data at d.workstation using + flt(d.downtime, 2).
- Set datasets from list().
- For each label in labels.
  - Evaluate datasets.append(workstation\_wise\_data.get(label, 0)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → “Machine Downtime”, “values” → datasets))), “type” → “bar”).
- Return chart.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0544.json#L6418) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1070)

<a id="op-ce0fe934de0445"></a>
### Get columns

`operation_enterprise_manufacturing_report_downtime_analysis_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “ID”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Downtime Entry”, …), mapping(“label” → translated “Machine”, “fieldname” → “workstation”, “fieldtype” → “Lin ….

**Local steps**

- Return list(mapping(“label” → translated “ID”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Downtime Entry”, …), mapping(“label” → translated “Machine”, “fieldname” → “workstation”, “fieldtype” → “Lin ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1071)

## Record · Downtime entry

[Record definition](../../../../data/record-types/downtime_entry.json)

<a id="op-c13be202f17aef"></a>
### Downtime Entry.validate

`operation_enterprise_manufacturing_record_definitions_downtime_entry_business_behavior_downtime_entry_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To Time must be after From Time”.

**Local steps**

- If (self.from\_time and self.to\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_time → self.to\_time.
  - If get\_datetime(self.to\_time) ≤ get\_datetime(self.from\_time).
    - Call the validation error handler Platform.throw(translated “To Time must be after From Time”).
  - Set self.downtime from (time\_diff\_in\_hours(self.to\_time, self.from\_time) × 60).
  - Evaluate self.validate\_overlap().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlap](operations-017.md#op-99bc94103148e1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L378)

<a id="op-99bc94103148e1"></a>
### Downtime Entry.validate overlap

`operation_enterprise_binding_enterprise_manufacturing_doctype_downtime_entry_downtime_entry_downtimeentry_validate_overlap`

**Inputs** self.

**Record and data access** read “Workstation” via get\_value.

**Explicit failure paths** validation helper — translated “Downtime overlaps with {0} for workstation {1}”.format(get\_link\_to\_form(“Downtime Entry”, overlap at 0), Platform.bold(self.workstation)).

**Local steps**

- Evaluate Platform.db.get\_value(“Workstation”, self.workstation, “name”, for\_update = true).
- Set entry from Platform.qb.DocType(“Downtime Entry”).
- Set overlap from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract &gt; nested operand ….
- If overlap.
  - Call the validation error handler Platform.throw(translated “Downtime overlaps with {0} for workstation {1}”.format(get\_link\_to\_form(“Downtime Entry”, overlap at 0), Platform.bold(self.workstation))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L805)

## Report · Exponential smoothing forecasting

<a id="op-9daf15c31ad82e"></a>
### Execute

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** ForecastingReport(filters).execute\_report().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return ForecastingReport(filters).execute\_report().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1081)

<a id="op-b4cd0dbafd3898"></a>
### Exponential Smoothing Forecast.forecast future data

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_exponential_smoothing_forecast_forecast_future_data`

**Inputs** self.

**Local steps**

- Set from\_date from getdate(self.filters.from\_date).
- For each tuple(\_key, value) in self.period\_wise\_data.items().
  - Set forecast\_data from list().
  - For each period in self.period\_list.
    - Set forecast\_key from (“forecast\_” + period.key).
    - Set is\_future from getdate(period.from\_date) ≥ from\_date.
    - If (value.get(period.key) and not forecast\_data).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value.get(period.key) → not forecast\_data.
      - Set value at forecast\_key from (flt(value.get(“avg”, 0)) or flt(value.get(period.key))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(value.get(“avg”, 0)) → flt(value.get(period.key)).
    - Otherwise.
      - If forecast\_data.
        - Set previous\_period\_data from forecast\_data at negative 1.
        - Set value at forecast\_key from (previous\_period\_data at 1 + (flt(self.filters.smoothing\_constant) × (flt(previous\_period\_data at 0) − flt(previous\_period\_data at 1)))).
    - If value.get(forecast\_key).
      - Set actual from value.get(forecast\_key) when is\_future, otherwise value.get(period.key).
        - Value choice on is\_future — true gives value.get(forecast\_key), false gives value.get(period.key).
      - Evaluate forecast\_data.append(list(actual, value.get(forecast\_key))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1082)

<a id="op-cc90cfae8c0bd1"></a>
### Forecasting Report.initialize

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.data from list().
- Set self.doctype from self.filters.based\_on\_document.
- Set self.child\_doctype from (self.doctype + “ Item”).
- Set self.based\_on\_field from “qty” when self.filters.based\_on\_field equals “Qty”, otherwise “amount”.
  - Value choice on self.filters.based\_on\_field equals “Qty” — true gives “qty”, false gives “amount”.
- Set self.fieldtype from “Float” when self.based\_on\_field equals “qty”, otherwise “Currency”.
  - Value choice on self.based\_on\_field equals “qty” — true gives “Float”, false gives “Currency”.
- Set self.company\_currency from Enterprise.get\_company\_currency(self.filters.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L3468) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1089)

<a id="op-cc63f43e83f25f"></a>
### Forecasting Report.execute report

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_execute_report`

**Inputs** self.

**Explicit results** tuple(columns, self.data, no value, charts, …).

**Local steps**

- Evaluate self.prepare\_periodical\_data().
- Evaluate self.forecast\_future\_data().
- Evaluate self.prepare\_final\_data().
- Evaluate self.add\_total().
- Set columns from self.get\_columns().
- Set charts from self.get\_chart\_data().
- Set summary\_data from self.get\_summary\_data().
- Return tuple(columns, self.data, no value, charts, …).

**Methods declared on this owner** [prepare periodical data](operations-017.md#op-f560fac8b540ce), [prepare final data](operations-017.md#op-16e9c8b8906262), [add total](operations-017.md#op-06e8efd86fec94), [get columns](operations-017.md#op-a9222779a38a0a), [get chart data](operations-017.md#op-1f11203ab80903), [get summary data](operations-017.md#op-6f6f3bf9a1db63).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L3779) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1084)

<a id="op-f560fac8b540ce"></a>
### Forecasting Report.prepare periodical data

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_prepare_periodical_data`

**Inputs** self.

**Local steps**

- Set self.period\_wise\_data from mapping().
- Set from\_date from add\_years(self.filters.from\_date, (cint(self.filters.no\_of\_years) × negative 1)).
- Set self.period\_list from get\_period\_list(from\_date, self.filters.to\_date, from\_date, self.filters.to\_date, ignore\_fiscal\_year = true, …).
- Set order\_data from (self.get\_data\_for\_forecast() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_data\_for\_forecast() → list().
- For each entry in order\_data.
  - Set key from tuple(entry.item\_code, entry.warehouse).
  - If key does not belong to self.period\_wise\_data.
    - Set self.period\_wise\_data at key from entry.
  - Set period\_data from self.period\_wise\_data at key.
  - For each period in self.period\_list.
    - If (entry.posting\_date ≥ period.from\_date and entry.posting\_date ≤ period.to\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.posting\_date ≥ period.from\_date → entry.posting\_date ≤ period.to\_date.
      - Set period\_data at period.key from (period\_data.get(period.key, 0.0) + flt(entry.get(self.based\_on\_field))).
- For each value in self.period\_wise\_data.values().
  - Set list\_of\_period\_value from list of value.get(p.key, 0) for p drawn from self.period\_list.
    - Draw p from self.period\_list.
  - If list\_of\_period\_value.
    - Set total\_qty from list of 1 for d drawn from list\_of\_period\_value where d.
      - Draw d from list\_of\_period\_value, keep a combination only if (d).
    - If total\_qty.
      - Set value at “avg” from (flt(sum(list\_of\_period\_value)) ÷ flt(sum(total\_qty))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data for forecast](operations-017.md#op-89f8f371c591d3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L3998) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1091)

<a id="op-89f8f371c591d3"></a>
### Forecasting Report.get data for forecast

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_get_data_for_forecast`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(self.doctype, “read”, throw = true).
- Set parent from Platform.qb.DocType(self.doctype).
- Set child from Platform.qb.DocType(self.child\_doctype).
- Set date\_field from “posting\_date” when self.doctype belongs to tuple(“Delivery Note”, “Sales Invoice”), otherwise “transaction\_date”.
  - Value choice on self.doctype belongs to tuple(“Delivery Note”, “Sales Invoice”) — true gives “posting\_date”, false gives “transaction\_date”.
- Set query from nested operand in the contract(nested operand in the contract).from\_(child).select(parent at date\_field.as\_(“posting\_date”), child.item\_code, child.warehouse, child.item\_name, …).where((((parent.docstatus  ….
- Set permitted from Platform.qb.get\_query(self.doctype, fields = list(“name”), filters = mapping(“docstatus” → 1, “company” → self.filters.company), ignore\_permissions = false).
- Set query from query.where(parent.name.isin(permitted)).
- If self.filters.item\_code.
  - Set query from query.where(child.item\_code equals self.filters.item\_code).
- If self.filters.warehouse.
  - Set warehouses from (get\_child\_warehouses(self.filters.warehouse) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_child\_warehouses(self.filters.warehouse) → list().
  - Set query from query.where(child.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1087)

<a id="op-16e9c8b8906262"></a>
### Forecasting Report.prepare final data

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_prepare_final_data`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.data from list().
- If not self.period\_wise\_data.
  - Return no value.
- For each key in self.period\_wise\_data.
  - Evaluate self.data.append(self.period\_wise\_data.get(key)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L5436) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1090)

<a id="op-06e8efd86fec94"></a>
### Forecasting Report.add total

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_add_total`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.data.
  - Return no value.
- Set total\_row from mapping(“item\_code” → translated “Total Quantity”).
- For each value in self.data.
  - For each period in self.period\_list.
    - Set forecast\_key from (“forecast\_” + period.key).
    - If forecast\_key does not belong to total\_row.
      - Evaluate total\_row.setdefault(forecast\_key, 0.0).
    - If period.key does not belong to total\_row.
      - Evaluate total\_row.setdefault(period.key, 0.0).
    - Update total\_row at forecast\_key using + value.get(forecast\_key, 0.0).
    - Update total\_row at period.key using + value.get(period.key, 0.0).
- Evaluate self.data.append(total\_row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L5574) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1083)

<a id="op-a9222779a38a0a"></a>
### Forecasting Report.get columns

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_get_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Item Code”, “options” → “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, …), mapping(“label” → translated “Warehouse”, “options” → “Warehouse”, “fieldname” → “war ….
- Set width from 180 when self.filters.periodicity belongs to list(“Yearly”, “Half-Yearly”, “Quarterly”), otherwise 100.
  - Value choice on self.filters.periodicity belongs to list(“Yearly”, “Half-Yearly”, “Quarterly”) — true gives 180, false gives 100.
- For each period in self.period\_list.
  - If (self.filters.periodicity belongs to list(“Yearly”, “Half-Yearly”, “Quarterly”) or period.from\_date ≥ getdate(self.filters.from\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.periodicity belongs to list(“Yearly”, “Half-Yearly”, “Quarterly”) → period.from\_date ≥ getdate(self.filters.from\_date).
    - Set forecast\_key from period.key.
    - Set label from translated period.label.
    - If period.from\_date ≥ getdate(self.filters.from\_date).
      - Set forecast\_key from (“forecast\_” + period.key).
      - Set label from ((translated period.label + one space) + translated “(Forecast)”).
    - Evaluate columns.append(mapping(“label” → label, “fieldname” → forecast\_key, “fieldtype” → self.fieldtype, “width” → width, …)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0545.json#L5954) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1086)

<a id="op-1f11203ab80903"></a>
### Forecasting Report.get chart data

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_get_chart_data`

**Inputs** self.

**Explicit results** no value · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Demand”, “values” → self.total\_demand), mapping(“name” → translated “Forecast”, “values” → self.total\_forecast))), ….

**Local steps**

- If not self.data.
  - Return no value.
- Set labels from list().
- Set self.total\_demand from list().
- Set self.total\_forecast from list().
- Set self.total\_history\_forecast from list().
- Set self.total\_future\_forecast from list().
- For each period in self.period\_list.
  - Set forecast\_key from (“forecast\_” + period.key).
  - Evaluate labels.append(translated period.label).
  - If period.from\_date &lt; getdate(self.filters.from\_date).
    - Evaluate self.total\_demand.append(self.data at negative 1.get(period.key, 0)).
    - Evaluate self.total\_history\_forecast.append(self.data at negative 1.get(forecast\_key, 0)).
  - Otherwise.
    - Evaluate self.total\_future\_forecast.append(self.data at negative 1.get(forecast\_key, 0)).
  - Evaluate self.total\_forecast.append(self.data at negative 1.get(forecast\_key, 0)).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Demand”, “values” → self.total\_demand), mapping(“name” → translated “Forecast”, “values” → self.total\_forecast))), ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0546.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1085)

<a id="op-6f6f3bf9a1db63"></a>
### Forecasting Report.get summary data

`operation_enterprise_manufacturing_report_exponential_smoothing_forecasting_business_behavior_forecasting_report_get_summary_data`

**Inputs** self.

**Explicit results** no value · list(mapping(“value” → sum(self.total\_demand), “label” → translated “Total Demand (Past Data)”, “currency” → self.company\_currency, “datatype” → self.fieldtype), mapping(“value” → sum(self.total\_history\_fo ….

**Local steps**

- If not self.data.
  - Return no value.
- Return list(mapping(“value” → sum(self.total\_demand), “label” → translated “Total Demand (Past Data)”, “currency” → self.company\_currency, “datatype” → self.fieldtype), mapping(“value” → sum(self.total\_history\_fo ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0546.json#L688) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1088)

## Record · Job card

[Record definition](../../../../data/record-types/job_card.json)

<a id="op-675ab5c2f115e9"></a>
### Job Card.onload

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_onload`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Local steps**

- Set excess\_transfer from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”).
- Evaluate self.set\_onload(“job\_card\_excess\_transfer”, excess\_transfer).
- Evaluate self.set\_onload(“enforce\_time\_logs”, Platform.db.get\_single\_value(“Manufacturing Settings”, “enforce\_time\_logs”)).
- Evaluate self.set\_onload(“work\_order\_closed”, self.is\_work\_order\_closed()).
- Evaluate self.set\_onload(“has\_stock\_entry”, self.has\_stock\_entry()).
- If self.docstatus equals 0.
  - Evaluate self.set\_onload(“max\_completable\_qty”, self.get\_max\_completable\_qty()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is work order closed](operations-022.md#op-082c74472582c6), [has stock entry](operations-017.md#op-5e4dbf556ec671), [get max completable qty](operations-021.md#op-a414a68aa53731).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “job\_card\_excess\_transfer”), Platform.db.get\_single\_value(“Manufacturing Settings”, “enforce\_time\_logs”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L418)

<a id="op-88c65eb7549316"></a>
### Job Card.on discard

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L1855) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L415)

<a id="op-5e4dbf556ec671"></a>
### Job Card.has stock entry

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_has_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry” via exists.

**Explicit results** Platform.db.exists(“Stock Entry”, mapping(“job\_card” → self.name, “docstatus” → list(“!=”, 2))).

**Local steps**

- Return Platform.db.exists(“Stock Entry”, mapping(“job\_card” → self.name, “docstatus” → list(“!=”, 2))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L1918) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L411)

<a id="op-e054fee068f7fb"></a>
### Job Card.before validate

`operation_enterprise_manufacturing_record_definitions_job_card_business_behavior_job_card_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_wip\_warehouse().
- Evaluate self.set\_stock\_uom().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set wip warehouse](operations-021.md#op-1c834bc3b1e488), [set stock uom](operations-021.md#op-de69b5d2862a89).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0470.json#L2033) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L391)
