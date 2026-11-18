# Sales relationships · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Prospects engaged but not converted

<a id="op-f2dfeb0f71c902"></a>
### Get lead filters

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_get_lead_filters`

**Inputs** filters.

**Explicit results** lead\_filters.

**Local steps**

- Set lead\_creation\_date from get\_creation\_date\_based\_on\_lead\_age(filters).
- Set lead\_filters from list(list(“status”, “!=”, “Converted”), list(“creation”, “&lt;=”, lead\_creation\_date)).
- If filters.get(“lead”).
  - Evaluate lead\_filters.append(list(“name”, “=”, filters.get(“lead”))).
- Return lead\_filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L28) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1331)

<a id="op-dc4ce87c151258"></a>
### Get creation date based on lead age

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_get_creation_date_based_on_lead_age`

**Inputs** filters.

**Explicit results** add\_days(now(), (filters.get(“lead\_age”) × negative 1)).

**Local steps**

- Return add\_days(now(), (filters.get(“lead\_age”) × negative 1)).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L2755) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1329)

## Report · Sales pipeline analytics

<a id="op-ac531c07303f35"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** SalesPipelineAnalytics(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return SalesPipelineAnalytics(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L31) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1333)

<a id="op-e63ffbd50e8299"></a>
### Sales Pipeline Analytics.initialize

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L3911) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1344)

<a id="op-4e608d9a8b76e6"></a>
### Sales Pipeline Analytics.validate filters

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date is mandatory” · validation helper — translated “To Date is mandatory” · validation helper — translated “Company is mandatory when Based On is Amount”.

**Local steps**

- If not self.filters.from\_date.
  - Call the validation error handler Platform.throw(translated “From Date is mandatory”).
- If not self.filters.to\_date.
  - Call the validation error handler Platform.throw(translated “To Date is mandatory”).
- If (self.filters.based\_on equals “Amount” and not self.filters.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.based\_on equals “Amount” → not self.filters.company.
  - Call the validation error handler Platform.throw(translated “Company is mandatory when Based On is Amount”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1349)

<a id="op-1df9f18e551c62"></a>
### Sales Pipeline Analytics.run

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart).

**Local steps**

- Evaluate self.validate\_filters().
- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.get\_chart\_data().
- Return tuple(self.columns, self.data, no value, self.chart).

**Methods declared on this owner** [validate filters](operations-013.md#op-4e608d9a8b76e6), [get columns](operations-013.md#op-9afaab75840ee2), [get data](operations-013.md#op-7c3aa73dc337e9), [get chart data](operations-013.md#op-78efece838503b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L4146) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1345)

<a id="op-9afaab75840ee2"></a>
### Sales Pipeline Analytics.get columns

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- Evaluate self.set\_range\_columns().
- Evaluate self.set\_pipeline\_based\_on\_column().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set range columns](operations-013.md#op-315748ec02fcd7), [set pipeline based on column](operations-013.md#op-2aee220b0c6112).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L4292) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1339)

<a id="op-315748ec02fcd7"></a>
### Sales Pipeline Analytics.set range columns

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_set_range_columns`

**Inputs** self.

**Local steps**

- Set based\_on from mapping(“Number” → “Int”, “Amount” → “Currency”) at self.filters.get(“based\_on”).
- For each period in self.get\_periods().
  - Evaluate self.columns.append(mapping(expand period, “fieldtype” → based\_on, “width” → 200)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get periods](operations-013.md#op-2a081fbecb6e73).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1348)

<a id="op-2aee220b0c6112"></a>
### Sales Pipeline Analytics.set pipeline based on column

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_set_pipeline_based_on_column`

**Inputs** self.

**State and service calls** call insert on self.columns.

**Local steps**

- If self.filters.get(“pipeline\_by”) equals “Owner”.
  - Evaluate self.columns.insert(0, mapping(“fieldname” → “opportunity\_owner”, “label” → translated “Opportunity Owner”, “width” → 200)).
- Otherwise.
  - If self.filters.get(“pipeline\_by”) equals “Sales Stage”.
    - Evaluate self.columns.insert(0, mapping(“fieldname” → “sales\_stage”, “label” → translated “Sales Stage”, “width” → 200)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L4879) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1347)

<a id="op-e5a0c866c08e81"></a>
### Sales Pipeline Analytics.get fields

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_fields`

**Inputs** self.

**Local steps**

- Set self.based\_on from mapping(“Owner” → “\_assign as opportunity\_owner”, “Sales Stage” → “sales\_stage”) at self.filters.get(“pipeline\_by”).
- Set self.data\_based\_on from mapping(“Number” → mapping(“COUNT” → “\*”, “as” → “count”), “Amount” → “opportunity\_amount as amount”) at self.filters.get(“based\_on”).
- Set self.group\_by\_based\_on from mapping(“Owner” → “\_assign”, “Sales Stage” → “sales\_stage”) at self.filters.get(“pipeline\_by”).
- Set opp from Platform.qb.DocType(“Opportunity”).
- Set period\_function from Month when self.filters.get(“range”) equals “Monthly”, otherwise Quarter.
  - Value choice on self.filters.get(“range”) equals “Monthly” — true gives Month, false gives Quarter.
- Set self.period\_expressions from list(Year(opp.expected\_closing), period\_function(opp.expected\_closing)).
- Set self.period\_fields from list(self.period\_expressions at 0.as\_(“year”), self.period\_expressions at 1.as\_(“period”)).
- Set self.pipeline\_by from mapping(“Owner” → “opportunity\_owner”, “Sales Stage” → “sales\_stage”) at self.filters.get(“pipeline\_by”).
- Set self.period\_by from “period”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1342)

<a id="op-7c3aa73dc337e9"></a>
### Sales Pipeline Analytics.get data

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.get\_fields().
- Set opp from Platform.qb.DocType(“Opportunity”).
- Set query from Platform.qb.get\_query(“Opportunity”, filters = self.get\_conditions(), ignore\_permissions = false).
- Set pipeline\_field from opp.\_assign when self.group\_by\_based\_on equals “\_assign”, otherwise opp.sales\_stage.
  - Value choice on self.group\_by\_based\_on equals “\_assign” — true gives opp.\_assign, false gives opp.sales\_stage.
- If self.filters.get(“based\_on”) equals “Number”.
  - Set self.query\_result from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).groupby(pipeline\_field, expanded nested operand in the contract.period\_express ….
  - Evaluate self.set\_row\_periods().
- If self.filters.get(“based\_on”) equals “Amount”.
  - Set self.query\_result from query.select(pipeline\_field.as\_(self.pipeline\_by), opp.opportunity\_amount.as\_(“amount”), expanded self.period\_fields, opp.conversion\_rate, …).run(as\_dict = true).
  - Evaluate self.set\_row\_periods().
  - Evaluate self.convert\_to\_base\_currency().
  - Set self.grouped\_data from list().
  - Set grouping\_key from deferred anonymous expression.
  - For each tuple(tuple(pipeline\_by, period\_by), rows) in groupby(sorted(self.query\_result, key = grouping\_key), grouping\_key).
    - Evaluate self.grouped\_data.append(mapping(self.pipeline\_by → pipeline\_by, self.period\_by → period\_by, “amount” → sum(generator of flt(r at “amount”) for r drawn from rows))).
      - Draw r from rows.
  - Set self.query\_result from self.grouped\_data.
- Evaluate self.get\_periodic\_data().
- Evaluate self.append\_data(self.pipeline\_by, self.period\_by).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get fields](operations-013.md#op-e5a0c866c08e81), [get conditions](operations-013.md#op-9c92b9e632d57b), [set row periods](operations-013.md#op-98eeb1cb6ca325), [convert to base currency](operations-013.md#op-38e7c283929cd1), [get periodic data](operations-013.md#op-cba0999e18fd3a), [append data](operations-013.md#op-4bf24d983f8ae2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1341)

<a id="op-9c92b9e632d57b"></a>
### Sales Pipeline Analytics.get conditions

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_conditions`

**Inputs** self.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- If self.filters.get(“opportunity\_source”).
  - Evaluate conditions.append(mapping(“utm\_source” → self.filters.get(“opportunity\_source”))).
- If self.filters.get(“opportunity\_type”).
  - Evaluate conditions.append(mapping(“opportunity\_type” → self.filters.get(“opportunity\_type”))).
- If self.filters.get(“status”).
  - Evaluate conditions.append(mapping(“status” → self.filters.get(“status”))).
- Otherwise.
  - Evaluate conditions.append(list(“status”, “not in”, list(“Lost”, “Closed”))).
- If self.filters.get(“company”).
  - Evaluate conditions.append(mapping(“company” → self.filters.get(“company”))).
- If self.filters.get(“assigned\_to”).
  - Set assigned\_to from nested operand in the contract.filters.get(“assigned\_to”).replace(“%”, “\\%”).replace(“\_”, “\\\_”).
  - Evaluate conditions.append(list(“\_assign”, “like”, formatted text %"{assigned\_to}"%)).
- If (self.filters.get(“from\_date”) and self.filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“from\_date”) → self.filters.get(“to\_date”).
  - Evaluate conditions.append(list(“expected\_closing”, “between”, list(self.filters.get(“from\_date”), self.filters.get(“to\_date”)))).
- Return conditions.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1340)

<a id="op-78efece838503b"></a>
### Sales Pipeline Analytics.get chart data

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_chart_data`

**Inputs** self.

**Explicit results** self.chart.

**Local steps**

- Set labels from list().
- Set datasets from list().
- Evaluate self.append\_to\_dataset(datasets).
- For each column in self.columns.
  - If (column at “fieldname” differs from “opportunity\_owner” and column at “fieldname” differs from “sales\_stage”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in column at “fieldname” differs from “opportunity\_owner” → column at “fieldname” differs from “sales\_stage”.
    - Evaluate labels.append(column at “label”).
- Set self.chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “line”).
- Return self.chart.

**Methods declared on this owner** [append to dataset](operations-013.md#op-28f638b1c798ea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L36) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1338)

<a id="op-cba0999e18fd3a"></a>
### Sales Pipeline Analytics.get periodic data

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_get_periodic_data`

**Inputs** self.

**Local steps**

- Set self.periodic\_data from Platform.\_dict().
- Set based\_on from mapping(“Number” → “count”, “Amount” → “amount”) at self.filters.get(“based\_on”).
- Set pipeline\_by from mapping(“Owner” → “opportunity\_owner”, “Sales Stage” → “sales\_stage”) at self.filters.get(“pipeline\_by”).
- For each info in self.query\_result.
  - Set period from info.get(self.period\_by).
  - Set value from info.get(pipeline\_by).
  - Set count\_or\_amount from info.get(based\_on).
  - If self.filters.get(“pipeline\_by”) equals “Owner”.
    - If (value equals “Not Assigned” or value equals “&#91;&#93;” or value is identical to no value or not value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value equals “Not Assigned” → value equals “&#91;&#93;” → value is identical to no value → not value.
      - Set assigned\_to from list(“Not Assigned”).
    - Otherwise.
      - Set assigned\_to from json.loads(value).
    - Evaluate self.check\_for\_assigned\_to(period, value, count\_or\_amount, assigned\_to, …).
  - Otherwise.
    - Evaluate self.set\_formatted\_data(period, value, count\_or\_amount, no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check for assigned to](operations-013.md#op-2a1a610cc5a6ab), [set formatted data](operations-013.md#op-532b961bff9582).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L44) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1343)

<a id="op-532b961bff9582"></a>
### Sales Pipeline Analytics.set formatted data

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_set_formatted_data`

**Inputs** self, period, value, count\_or\_amount, assigned\_to.

**Local steps**

- If assigned\_to.
  - If len(assigned\_to) &gt; 1.
    - If self.filters.get(“assigned\_to”).
      - For each user in assigned\_to.
        - If self.filters.get(“assigned\_to”) equals user.
          - Set value from user.
          - Evaluate self.periodic\_data.setdefault(value, Platform.\_dict()).setdefault(period, 0).
          - Update self.periodic\_data at value at period using + count\_or\_amount.
    - Otherwise.
      - For each user in assigned\_to.
        - Set value from user.
        - Evaluate self.periodic\_data.setdefault(value, Platform.\_dict()).setdefault(period, 0).
        - Update self.periodic\_data at value at period using + count\_or\_amount.
  - Otherwise.
    - Set value from assigned\_to at 0.
    - Evaluate self.periodic\_data.setdefault(value, Platform.\_dict()).setdefault(period, 0).
    - Update self.periodic\_data at value at period using + count\_or\_amount.
- Otherwise.
  - Evaluate self.periodic\_data.setdefault(value, Platform.\_dict()).setdefault(period, 0).
  - Update self.periodic\_data at value at period using + count\_or\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0440.json#L1690) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1346)

<a id="op-2a1a610cc5a6ab"></a>
### Sales Pipeline Analytics.check for assigned to

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_check_for_assigned_to`

**Inputs** self, period, value, count\_or\_amount, assigned\_to, info.

**Local steps**

- If self.filters.get(“assigned\_to”).
  - For each data in json.loads((info.get(“opportunity\_owner”) or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in info.get(“opportunity\_owner”) → “&#91;&#93;”.
    - If data equals self.filters.get(“assigned\_to”).
      - Evaluate self.set\_formatted\_data(period, data, count\_or\_amount, assigned\_to).
- Otherwise.
  - Evaluate self.set\_formatted\_data(period, value, count\_or\_amount, assigned\_to).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set formatted data](operations-013.md#op-532b961bff9582).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0440.json#L2312) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1336)

<a id="op-2a081fbecb6e73"></a>
### Sales Pipeline Analytics.get periods

`operation_enterprise_binding_enterprise_crm_report_sales_pipeline_analytics_sales_pipeline_analytics_salespipelineanalytics_get_periods`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** periods.

**Local steps**

- Set periods from list().
- Set months\_per\_period from 1 when self.filters.get(“range”) equals “Monthly”, otherwise 3.
  - Value choice on self.filters.get(“range”) equals “Monthly” — true gives 1, false gives 3.
- Set current\_date from self.get\_period\_start(getdate(self.filters.get(“from\_date”)), months\_per\_period).
- While current\_date ≤ getdate(self.filters.get(“to\_date”)).
  - Evaluate periods.append(self.get\_period(current\_date)).
  - Set current\_date from (current\_date + relativedelta(months = months\_per\_period)).
- Return periods.

**Methods declared on this owner** [get period start](operations-013.md#op-203bc719b4524d), [get period](operations-013.md#op-80f38a18a728fd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L574)

<a id="op-203bc719b4524d"></a>
### Sales Pipeline Analytics.get period start

`operation_enterprise_binding_enterprise_crm_report_sales_pipeline_analytics_sales_pipeline_analytics_salespipelineanalytics_get_period_start`

**Inputs** self, day, months\_per\_period.

**Declared result** date.

**Explicit results** date(day.year, ((((day.month − 1) floor divide months\_per\_period) × months\_per\_period) + 1), 1).

**Local steps**

- Return date(day.year, ((((day.month − 1) floor divide months\_per\_period) × months\_per\_period) + 1), 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L573)

<a id="op-80f38a18a728fd"></a>
### Sales Pipeline Analytics.get period

`operation_enterprise_binding_enterprise_crm_report_sales_pipeline_analytics_sales_pipeline_analytics_salespipelineanalytics_get_period`

**Inputs** self, period\_start.

**Declared result** dict.

**Explicit results** mapping(“fieldname” → period\_start.strftime(“%B\_%Y”).lower(), “label” → label) · mapping(“fieldname” → formatted text q{quarter}\_{period\_start.year}, “label” → formatted text Q{quarter} {period\_start.year}).

**Local steps**

- If self.filters.get(“range”) equals “Monthly”.
  - Set label from formatted text {translated period\_start.strftime(“%B”)} {period\_start.year}.
  - Return mapping(“fieldname” → period\_start.strftime(“%B\_%Y”).lower(), “label” → label).
- Set quarter from (((period\_start.month − 1) floor divide 3) + 1).
- Return mapping(“fieldname” → formatted text q{quarter}\_{period\_start.year}, “label” → formatted text Q{quarter} {period\_start.year}).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L572)

<a id="op-98eeb1cb6ca325"></a>
### Sales Pipeline Analytics.set row periods

`operation_enterprise_binding_enterprise_crm_report_sales_pipeline_analytics_sales_pipeline_analytics_salespipelineanalytics_set_row_periods`

**Inputs** self.

**Local steps**

- For each row in self.query\_result.
  - Set month from cint(row.period) when self.filters.get(“range”) equals “Monthly”, otherwise ((cint(row.period) × 3) − 2).
    - Value choice on self.filters.get(“range”) equals “Monthly” — true gives cint(row.period), false gives ((cint(row.period) × 3) − 2).
  - Set row.period from self.get\_period(date(cint(row.year), month, 1)) at “fieldname”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period](operations-013.md#op-80f38a18a728fd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L575)

<a id="op-28f638b1c798ea"></a>
### Sales Pipeline Analytics.append to dataset

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_append_to_dataset`

**Inputs** self, datasets.

**Local steps**

- Set based\_on from mapping(“Amount” → “amount”, “Number” → “count”) at self.filters.get(“based\_on”).
- Set frequency\_list from list of period at “fieldname” for period drawn from self.get\_periods().
  - Draw period from self.get\_periods().
- Set count from (list(0) × len(frequency\_list)).
- For each info in self.query\_result.
  - For each i in range(len(frequency\_list)).
    - If info at self.period\_by equals frequency\_list at i.
      - Set count at i from (count at i + info at based\_on).
- Evaluate datasets.append(mapping(“name” → based\_on, “values” → count)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get periods](operations-013.md#op-2a081fbecb6e73).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1335)

<a id="op-4bf24d983f8ae2"></a>
### Sales Pipeline Analytics.append data

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_append_data`

**Inputs** self, pipeline\_by, period\_by.

**Local steps**

- Set self.data from list().
- For each tuple(pipeline, period\_data) in self.periodic\_data.items().
  - Set row from mapping(pipeline\_by → pipeline).
  - For each info in self.query\_result.
    - Set period from info.get(period\_by).
    - Set count from period\_data.get(period, 0.0).
    - Set row at period from count.
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L32) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1334)

<a id="op-38e7c283929cd1"></a>
### Sales Pipeline Analytics.convert to base currency

`operation_enterprise_customer_relationship_management_report_sales_pipeline_analytics_business_behavior_sales_pipeline_analytics_convert_to_base_currency`

**Inputs** self.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.filters.company).
- For each row in self.query\_result.
  - Set row at “amount” from (flt(row at “amount”) × self.get\_conversion\_rate(row, company\_currency)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get conversion rate](operations-013.md#op-40cb98d98ff803).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L35) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1337)

<a id="op-40cb98d98ff803"></a>
### Sales Pipeline Analytics.get conversion rate

`operation_enterprise_binding_enterprise_crm_report_sales_pipeline_analytics_sales_pipeline_analytics_salespipelineanalytics_get_conversion_rate`

**Inputs** self, row, company\_currency.

**Declared result** float.

**Explicit results** flt(row.conversion\_rate) · 1.0 · flt(get\_exchange\_rate(row.currency, company\_currency, row.transaction\_date)).

**Local steps**

- If flt(row.conversion\_rate).
  - Return flt(row.conversion\_rate).
- If (not row.currency or row.currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.currency → row.currency equals company\_currency.
  - Return 1.0.
- Return flt(get\_exchange\_rate(row.currency, company\_currency, row.transaction\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L571)
