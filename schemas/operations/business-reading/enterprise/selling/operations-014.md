# Sales · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Sales analytics

<a id="op-ba7a77dc882abc"></a>
### Analytics.get sales transactions based on customers or suppliers

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_customers_or_suppliers`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.filters.doc\_type equals “Payment Entry”.
  - Evaluate self.get\_payment\_entries(“Customer” when self.filters.tree\_type equals “Customer”, otherwise “Supplier”).
    - Value choice on self.filters.tree\_type equals “Customer” — true gives “Customer”, false gives “Supplier”.
  - Return no value.
- Set value\_field from self.value\_field.
- If self.filters.tree\_type equals “Customer”.
  - Set entity\_name from “customer\_name as entity\_name”.
  - If self.filters.doc\_type equals “Quotation”.
    - Set entity from “party\_name as entity”.
  - Otherwise.
    - Set entity from “customer as entity”.
- Otherwise.
  - Set entity from “supplier as entity”.
  - Set entity\_name from “supplier\_name as entity\_name”.
- Set self.entries from Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(entity, entity\_name, value\_field, self.date\_field), filters = self.document\_filters, ignore\_permissions = false).run(as\_dict = true).
- Set self.entity\_names from mapping().
- For each d in self.entries.
  - Evaluate self.entity\_names.setdefault(d.entity, d.entity\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payment entries](operations-014.md#op-bc740b441fc05a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L90)

<a id="op-bc740b441fc05a"></a>
### Analytics.get payment entries

`operation_enterprise_binding_enterprise_selling_report_sales_analytics_sales_analytics_analytics_get_payment_entries`

**Inputs** self, party\_type.

**Local steps**

- Set entries from Platform.qb.get\_query(table = “Payment Entry”, fields = list(“party as entity”, “party\_name as entity\_name”, “payment\_type”, “base\_received\_amount”, …), filters = mapping(expand self.document\_filters, “par ….
- Set inflow from “Receive” when party\_type equals “Customer”, otherwise “Pay”.
  - Value choice on party\_type equals “Customer” — true gives “Receive”, false gives “Pay”.
- For each d in entries.
  - Set amount from d.base\_received\_amount when d.payment\_type equals “Receive”, otherwise d.base\_paid\_amount.
    - Value choice on d.payment\_type equals “Receive” — true gives d.base\_received\_amount, false gives d.base\_paid\_amount.
  - Set d.value\_field from amount when d.payment\_type equals inflow, otherwise negative amount.
    - Value choice on d.payment\_type equals inflow — true gives amount, false gives negative amount.
- Set self.entries from entries.
- Set self.entity\_names from mapping().
- For each d in self.entries.
  - Evaluate self.entity\_names.setdefault(d.entity, d.entity\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L118)

<a id="op-5edd96aaf67eab"></a>
### Analytics.get sales transactions based on items

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.filters at “value\_quantity” equals “Value”.
  - Set value\_field from “base\_net\_amount”.
- Otherwise.
  - Set value\_field from “stock\_qty”.
- Set permitted\_names from self.\_get\_permitted\_parent\_names().
- If not permitted\_names.
  - Set self.entries from list().
  - Set self.entity\_names from mapping().
  - Return no value.
- Set doctype from DocType(self.filters.doc\_type).
- Set doctype\_item from DocType(formatted text {self.filters.doc\_type} Item).
- Set self.entries from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“entity”), nested operand in the contract.as\_(“entity\_name”), doctype\_item.stock\_uom, nested operand ….
- Set self.entity\_names from mapping().
- For each d in self.entries.
  - Evaluate self.entity\_names.setdefault(d.entity, d.entity\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted parent names](operations-013.md#op-073a874f328ec1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L92)

<a id="op-df223b0272f0f9"></a>
### Analytics.get sales transactions based on customer or territory group

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_customer_or_territory_group`

**Inputs** self.

**Local steps**

- If self.filters.tree\_type equals “Customer Group”.
  - Set entity\_field from “customer\_group as entity”.
- Otherwise.
  - If self.filters.tree\_type equals “Supplier Group”.
    - Set entity\_field from “supplier as entity”.
    - Evaluate self.get\_supplier\_parent\_child\_map().
  - Otherwise.
    - Set entity\_field from “territory as entity”.
- Set self.entries from Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(entity\_field, self.value\_field, self.date\_field), filters = self.document\_filters, ignore\_permissions = false).run(as\_dict = true).
- Evaluate self.get\_groups().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get supplier parent child map](operations-014.md#op-66da76d4b74b0d), [get groups](operations-014.md#op-34d3aaa9587b73).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L89)

<a id="op-32d602f516530f"></a>
### Analytics.get sales transactions based on item group

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_item_group`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.filters at “value\_quantity” equals “Value”.
  - Set value\_field from “base\_net\_amount”.
- Otherwise.
  - Set value\_field from “stock\_qty”.
- Set permitted\_names from self.\_get\_permitted\_parent\_names().
- If not permitted\_names.
  - Set self.entries from list().
  - Evaluate self.get\_groups().
  - Return no value.
- Set doctype from DocType(self.filters.doc\_type).
- Set doctype\_item from DocType(formatted text {self.filters.doc\_type} Item).
- Set self.entries from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“entity”), nested operand in the contract.as\_(“value\_field”), doctype at nested operand in the contr ….
- Evaluate self.get\_groups().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted parent names](operations-013.md#op-073a874f328ec1), [get groups](operations-014.md#op-34d3aaa9587b73).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L91)

<a id="op-c9cd66e595c0c9"></a>
### Analytics.get sales transactions based on project

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_project`

**Inputs** self.

**Local steps**

- Set value\_field from self.value\_field.
- If self.filters.doc\_type equals “Payment Entry”.
  - Set value\_field from “base\_received\_amount as value\_field”.
- Set entity from “project as entity”.
- Set filters from mapping(expand self.document\_filters, “project” → list(“!=”, empty text)).
- Set self.entries from Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(entity, value\_field, self.date\_field), filters = filters, ignore\_permissions = false).run(as\_dict = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L94)

<a id="op-a1089136b46670"></a>
### Analytics.filter data by entities

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_filter_data_by_entities`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.entities.
  - Return no value.
- Set entities from set(self.entities).
- Set selected\_data from list().
- For each row in self.data.
  - If row at “entity” does not belong to entities.
    - Continue with the next iteration or loop test.
  - Set row from row.copy().
  - If “indent” belongs to row.
    - Set row at “indent” from 0.
  - Evaluate selected\_data.append(row).
- Set self.data from selected\_data.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L2257) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L78)

<a id="op-c546c7b1202588"></a>
### Analytics.get rows

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_rows`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Evaluate self.get\_periodic\_data().
- For each tuple(entity, period\_data) in self.entity\_periodic\_data.items().
  - Set row from mapping(“entity” → entity, “entity\_name” → self.entity\_names.get(entity) when hasattr(self, “entity\_names”), otherwise no value).
    - Value choice on hasattr(self, “entity\_names”) — true gives self.entity\_names.get(entity), false gives no value.
  - Set total from 0.
  - For each end\_date in self.periodic\_daterange.
    - Set period from self.get\_period(end\_date).
    - Set amount from flt(period\_data.get(period, 0.0)).
    - Set row at scrub(period) from amount.
    - Update total using + amount.
  - Set row at “total” from total.
  - If self.filters.tree\_type equals “Item”.
    - Set row at “stock\_uom” from period\_data.get(“stock\_uom”).
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get periodic data](operations-014.md#op-bbd90c359c102d), [get period](operations-014.md#op-afd9f102fb44fb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L2526) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L87)

<a id="op-a648e02b363576"></a>
### Analytics.get rows by group

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_rows_by_group`

**Inputs** self.

**Local steps**

- Evaluate self.get\_periodic\_data().
- Set out from list().
- For each d in reversed(self.group\_entries).
  - Set row from mapping(“entity” → d.name, “indent” → self.depth\_map.get(d.name)).
  - Set total from 0.
  - For each end\_date in self.periodic\_daterange.
    - Set period from self.get\_period(end\_date).
    - Set amount from flt(self.entity\_periodic\_data.get(d.name, mapping()).get(period, 0.0)).
    - Set row at scrub(period) from amount.
    - If (d.parent and (self.filters.tree\_type differs from “Order Type” or d.parent equals “Order Types”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.parent → (self.filters.tree\_type differs from “Order Type” or d.parent equals “Order Types”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.tree\_type differs from “Order Type” → d.parent equals “Order Types”.
      - Evaluate self.entity\_periodic\_data.setdefault(d.parent, Platform.\_dict()).setdefault(period, 0.0).
      - Update self.entity\_periodic\_data at d.parent at period using + amount.
    - Update total using + amount.
  - Set row at “total” from total.
  - Set out from list(row, expanded out).
- Set self.data from out.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get periodic data](operations-014.md#op-bbd90c359c102d), [get period](operations-014.md#op-afd9f102fb44fb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L3007) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L88)

<a id="op-bbd90c359c102d"></a>
### Analytics.get periodic data

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_periodic_data`

**Inputs** self.

**Local steps**

- Set self.entity\_periodic\_data from Platform.\_dict().
- For each d in self.entries.
  - If self.filters.tree\_type equals “Supplier Group”.
    - Set d.entity from self.parent\_child\_map.get(d.entity).
  - Set period from self.get\_period(d.get(self.date\_field)).
  - Evaluate self.entity\_periodic\_data.setdefault(d.entity, Platform.\_dict()).setdefault(period, 0.0).
  - Update self.entity\_periodic\_data at d.entity at period using + flt(d.value\_field).
  - If self.filters.tree\_type equals “Item”.
    - Set self.entity\_periodic\_data at d.entity at “stock\_uom” from d.stock\_uom.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period](operations-014.md#op-afd9f102fb44fb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L3610) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L85)

<a id="op-afd9f102fb44fb"></a>
### Analytics.get period

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_period`

**Inputs** self, posting\_date.

**Explicit results** period.

**Local steps**

- If self.filters.range equals “Weekly”.
  - Set iso\_date from posting\_date.isocalendar().
  - Set period from translated “Week {0} {1}”.format(str(iso\_date.week), str(iso\_date.year)).
- Otherwise.
  - If self.filters.range equals “Monthly”.
    - Set period from ((translated str(self.months at (nested operand in the contract.month − 1)) + one space) + str(posting\_date.year)).
  - Otherwise.
    - If self.filters.range equals “Quarterly”.
      - Set period from translated “Quarter {0} {1}”.format(str((((posting\_date.month − 1) floor divide 3) + 1)), str(posting\_date.year)).
    - Otherwise.
      - Set year from get\_fiscal\_year(posting\_date, company = self.filters.company at 0).
      - Set period from str(year at 0).
- Return period.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L83)

<a id="op-996618f7bca5d3"></a>
### Analytics.get period date ranges

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_period_date_ranges`

**Inputs** self.

**Local steps**

- Bind dependencies MO, relativedelta.
- Set tuple(from\_date, to\_date) from tuple(getdate(self.filters.from\_date), getdate(self.filters.to\_date)).
- Set increment from mapping(“Monthly” → 1, “Quarterly” → 3, “Half-Yearly” → 6, “Yearly” → 12).get(self.filters.range, 1).
- If self.filters.range belongs to list(“Monthly”, “Quarterly”).
  - Set from\_date from from\_date.replace(day = 1).
- Otherwise.
  - If self.filters.range equals “Yearly”.
    - Set from\_date from get\_fiscal\_year(from\_date) at 1.
  - Otherwise.
    - Set from\_date from (from\_date + relativedelta(from\_date, weekday = MO(negative 1))).
- Set self.periodic\_daterange from list().
- For each \_dummy in range(1, 53).
  - If self.filters.range equals “Weekly”.
    - Set period\_end\_date from add\_days(from\_date, 6).
  - Otherwise.
    - Set period\_end\_date from add\_to\_date(from\_date, months = increment, days = negative 1).
  - If period\_end\_date &gt; to\_date.
    - Set period\_end\_date from to\_date.
  - Evaluate self.periodic\_daterange.append(period\_end\_date).
  - Set from\_date from add\_days(period\_end\_date, 1).
  - If period\_end\_date equals to\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0670.json#L4515) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L84)

<a id="op-34d3aaa9587b73"></a>
### Analytics.get groups

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_groups`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “Invalid Tree Type {0}”.format(self.filters.tree\_type).

**Local steps**

- Set parent\_field\_map from mapping(“Territory” → “parent\_territory”, “Customer Group” → “parent\_customer\_group”, “Item Group” → “parent\_item\_group”, “Supplier Group” → “parent\_supplier\_group”).
- If self.filters.tree\_type does not belong to parent\_field\_map.
  - Call the validation error handler Platform.throw(translated “Invalid Tree Type {0}”.format(self.filters.tree\_type)).
- Set parent from parent\_field\_map at self.filters.tree\_type.
- Set self.depth\_map from Platform.\_dict().
- Set self.group\_entries from Platform.db.sql(formatted text select name, lft, rgt , {parent} as parent  from ′tab{self.filters.tree\_type}′ order by lft, as\_dict = 1).
- For each d in self.group\_entries.
  - If d.parent.
    - Evaluate self.depth\_map.setdefault(d.name, (self.depth\_map.get(d.parent) + 1)).
  - Otherwise.
    - Evaluate self.depth\_map.setdefault(d.name, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L82)

<a id="op-2bc001d855c186"></a>
### Analytics.get teams

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_teams`

**Inputs** self.

**Record and data access** read “DocType” via exists.

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “Invalid Document Type {0}”.format(self.filters.doc\_type).

**Local steps**

- Set self.depth\_map from Platform.\_dict().
- If not Platform.db.exists(“DocType”, self.filters.doc\_type).
  - Call the validation error handler Platform.throw(translated “Invalid Document Type {0}”.format(self.filters.doc\_type)).
- Set self.group\_entries from Platform.db.sql(formatted text  select \* from (select "Order Types" as name, 0 as lft,  2 as rgt, '' as parent union select distinct order\_type as name, 1 as lft, 1 as rgt, "Order, as\_dict = 1).
- For each d in self.group\_entries.
  - If d.parent.
    - Evaluate self.depth\_map.setdefault(d.name, (self.depth\_map.get(d.parent) + 1)).
  - Otherwise.
    - Evaluate self.depth\_map.setdefault(d.name, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L96)

<a id="op-66da76d4b74b0d"></a>
### Analytics.get supplier parent child map

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_supplier_parent_child_map`

**Inputs** self.

**Record and data access** execute query text (SELECT, Supplier).

**Local steps**

- Set self.parent\_child\_map from Platform.\_dict(Platform.db.sql(query text (SELECT, Supplier))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L95)

<a id="op-6dcce73c9b43d6"></a>
### Analytics.get chart data

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_chart_data`

**Inputs** self.

**Local steps**

- Set length from len(self.columns).
- If self.filters.tree\_type belongs to list(“Customer”, “Supplier”).
  - Set labels from list of d.get(“label”) for d drawn from self.columns at slice 2 to (length − 1).
    - Draw d from self.columns at slice 2 to (length − 1).
- Otherwise.
  - If self.filters.tree\_type equals “Item”.
    - Set labels from list of d.get(“label”) for d drawn from self.columns at slice 3 to (length − 1).
      - Draw d from self.columns at slice 3 to (length − 1).
  - Otherwise.
    - Set labels from list of d.get(“label”) for d drawn from self.columns at slice 1 to (length − 1).
      - Draw d from self.columns at slice 1 to (length − 1).
- Set datasets from list().
- If self.filters.curves differs from “select”.
  - For each curve in self.data.
    - Set data from mapping(“name” → curve.get(“entity\_name”, curve at “entity”), “values” → list of curve at scrub(label) for label drawn from labels).
      - Draw label from labels.
    - If (self.filters.curves equals “non-zeros” and not sum(data at “values”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.curves equals “non-zeros” → not sum(data at “values”).
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If (self.filters.curves equals “total” and “indent” belongs to curve).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.curves equals “total” → “indent” belongs to curve.
        - If curve at “indent” equals 0.
          - Evaluate datasets.append(data).
      - Otherwise.
        - If self.filters.curves equals “total”.
          - If datasets.
            - Set a from list of (data at “values” at idx + datasets at 0 at “values” at idx) for idx drawn from range(len(data at “values”)).
              - Draw idx from range(len(data at “values”)).
            - Set datasets at 0 at “values” from a.
          - Otherwise.
            - Evaluate datasets.append(data).
            - Set datasets at 0 at “name” from translated “Total”.
        - Otherwise.
          - Evaluate datasets.append(data).
- Set self.chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “line”).
- If self.filters at “value\_quantity” equals “Value”.
  - Set self.chart at “fieldtype” from “Currency”.
- Otherwise.
  - Set self.chart at “fieldtype” from “Float”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0671.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L79)

## Workspace · Sales funnel

<a id="op-0df2d4fb24e99d"></a>
### Validate filters

`operation_enterprise_selling_page_sales_funnel_business_behavior_validate_filters`

**Inputs** from\_date, to\_date, company.

**Explicit failure paths** validation helper — translated “To Date must be greater than From Date” · validation helper — translated “Please Select a Company”.

**Local steps**

- If (from\_date and to\_date and from\_date &gt; to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date → from\_date &gt; to\_date.
  - Call the validation error handler Platform.throw(translated “To Date must be greater than From Date”).
- If not company.
  - Call the validation error handler Platform.throw(translated “Please Select a Company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1120)

<a id="op-07b3e3a1726a30"></a>
### Base amount

`operation_enterprise_binding_enterprise_selling_page_sales_funnel_sales_funnel_base_amount`

**Inputs** opportunity.

**Explicit results** ((flt(opportunity at “opportunity\_amount”) × flt(opportunity at “conversion\_rate”)) or flt(opportunity at “base\_opportunity\_amount”)).

**Local steps**

- Return ((flt(opportunity at “opportunity\_amount”) × flt(opportunity at “conversion\_rate”)) or flt(opportunity at “base\_opportunity\_amount”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (flt(opportunity at “opportunity\_amount”) × flt(opportunity at “conversion\_rate”)) → flt(opportunity at “base\_opportunity\_amount”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L93)

<a id="op-d826fa88a9fec5"></a>
### Get funnel data

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_funnel_data`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list(mapping(“title” → translated “Active Leads”, “value” → active\_leads, “color” → “#B03B46”), mapping(“title” → translated “Opportunities”, “value” → opportunities, “color” → “#F09C00”), mapping(“title”  ….

**Local steps**

- Evaluate Platform.has\_permission(“Company”, doc = company, throw = true).
- Evaluate validate\_filters(from\_date, to\_date, company).
- Set date\_range from tuple(“between”, list(from\_date, to\_date)).
- Set active\_leads from len(Platform.qb.get\_query(“Lead”, fields = list(“name”), filters = mapping(“creation” → date\_range, “company” → company), ignore\_permissions = false).run(pluck = “name”)).
- Set opportunities from len(Platform.qb.get\_query(“Opportunity”, fields = list(“name”), filters = mapping(“creation” → date\_range, “opportunity\_from” → “Lead”, “company” → company), ignore\_permissions = false).run(pluck = “name”)).
- Set quotations from 0.
- Set quotation\_names from Platform.qb.get\_query(“Quotation”, fields = list(“name”), filters = mapping(“docstatus” → 1, “creation” → date\_range, “company” → company), ignore\_permissions = false).run(pluck = “name”).
- If quotation\_names.
  - Set lead\_opportunities from Platform.qb.get\_query(“Opportunity”, fields = list(“name”), filters = mapping(“opportunity\_from” → “Lead”), ignore\_permissions = false).run(pluck = “name”).
  - Set quotation from Platform.qb.DocType(“Quotation”).
  - Set condition from quotation.quotation\_to equals “Lead”.
  - If lead\_opportunities.
    - Set condition from (condition bitwise or quotation.opportunity.isin(lead\_opportunities)).
  - Set quotations from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and condition)).run() at 0 at 0.
- Set converted from 0.
- Set customer\_names from Platform.qb.get\_query(“Customer”, fields = list(“name”), filters = mapping(“creation” → date\_range), ignore\_permissions = false).run(pluck = “name”).
- If customer\_names.
  - Set customer from Platform.qb.DocType(“Customer”).
  - Set lead from Platform.qb.DocType(“Lead”).
  - Set converted from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract equals nested operand in the  ….
- Return list(mapping(“title” → translated “Active Leads”, “value” → active\_leads, “color” → “#B03B46”), mapping(“title” → translated “Opportunities”, “value” → opportunities, “color” → “#F09C00”), mapping(“title”  ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1114)

<a id="op-765cf211967f5d"></a>
### Get opp by utm source

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_opportunity_by_campaign_tracking_source`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_opp\_by(“utm\_source”, from\_date, to\_date, company, ignore\_permissions = false).

**Local steps**

- Return get\_opp\_by(“utm\_source”, from\_date, to\_date, company, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0660.json#L1382) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1118)

<a id="op-f58ab4f28e061b"></a>
### Get opp by utm campaign

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_opportunity_by_campaign_tracking_campaign`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_opp\_by(“utm\_campaign”, from\_date, to\_date, company, ignore\_permissions = false).

**Local steps**

- Return get\_opp\_by(“utm\_campaign”, from\_date, to\_date, company, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0660.json#L1509) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1116)

<a id="op-6a6540a8683c2b"></a>
### Get opp by utm medium

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_opportunity_by_campaign_tracking_medium`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_opp\_by(“utm\_medium”, from\_date, to\_date, company, ignore\_permissions = false).

**Local steps**

- Return get\_opp\_by(“utm\_medium”, from\_date, to\_date, company, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0660.json#L1636) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1117)

<a id="op-26de310ea0b5fb"></a>
### Get opp by

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_opportunity_by`

**Inputs** by\_field, from\_date, to\_date, company, ignore\_permissions = false.

**Explicit results** result · “empty”.

**Local steps**

- Evaluate validate\_filters(from\_date, to\_date, company).
- Set get\_opportunities from Platform.get\_all when ignore\_permissions, otherwise Platform.get\_list.
  - Value choice on ignore\_permissions — true gives Platform.get\_all, false gives Platform.get\_list.
- Set opportunities from get\_opportunities(“Opportunity”, filters = list(list(“status”, “in”, list(“Open”, “Quotation”, “Replied”)), list(“company”, “=”, company), list(“transaction\_date”, “Between”, list(from\_date, to\_date))), fi ….
- If opportunities.
  - Set cp\_opportunities from list of dict(x, expanded names mapping(“compound\_amount” → ((base\_amount(x) × x at “probability”) ÷ 100))) for x drawn from opportunities where x.get(by\_field).
    - Draw x from opportunities, keep a combination only if (x.get(by\_field)).
  - Set summary from mapping().
  - Set sales\_stages from set().
  - Set group\_key from deferred anonymous expression.
  - For each tuple(tuple(by\_field\_group, sales\_stage), rows) in groupby(sorted(cp\_opportunities, key = group\_key), group\_key).
    - Set summary.setdefault(by\_field\_group, mapping()) at sales\_stage from sum(generator of r at “compound\_amount” for r drawn from rows).
      - Draw r from rows.
    - Evaluate sales\_stages.add(sales\_stage).
  - Set pivot\_table from list().
  - For each sales\_stage in sales\_stages.
    - Set row from list().
    - For each sales\_stage\_values in summary.values().
      - Evaluate row.append(flt(sales\_stage\_values.get(sales\_stage))).
    - Evaluate pivot\_table.append(mapping(“chartType” → “bar”, “name” → sales\_stage, “values” → row)).
  - Set result from mapping(“datasets” → pivot\_table, “labels” → list(summary.keys())).
  - Return result.
- Otherwise.
  - Return “empty”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1115)

<a id="op-d94ce31d3d11d0"></a>
### Get pipeline data

`operation_enterprise_selling_page_sales_funnel_business_behavior_get_pipeline_data`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Opportunity” via get\_list.

**Explicit results** result · “empty”.

**Local steps**

- Evaluate validate\_filters(from\_date, to\_date, company).
- Set opportunities from Platform.get\_list(“Opportunity”, filters = list(list(“status”, “in”, list(“Open”, “Quotation”, “Replied”)), list(“company”, “=”, company), list(“transaction\_date”, “Between”, list(from\_date, to\_date))), fi ….
- If opportunities.
  - Set cp\_opportunities from list of dict(x, expanded names mapping(“compound\_amount” → ((base\_amount(x) × x at “probability”) ÷ 100))) for x drawn from opportunities.
    - Draw x from opportunities.
  - Set summary from mapping().
  - For each opportunity in cp\_opportunities.
    - Set sales\_stage from opportunity at “sales\_stage”.
    - Set summary at sales\_stage from (summary.get(sales\_stage, 0) + flt(opportunity at “compound\_amount”)).
  - Set result from mapping(“labels” → list(summary.keys()), “datasets” → list(mapping(“name” → translated “Total Amount”, “values” → list(summary.values()), “chartType” → “bar”))).
  - Return result.
- Otherwise.
  - Return “empty”.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1119)
