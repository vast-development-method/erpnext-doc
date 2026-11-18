# Sales · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Sales order analysis

<a id="op-8fc41cde889b7d"></a>
### Get delivery columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_delivery_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Delivery Date”, “fieldname” → “delivery\_date”, “fieldtype” → “Date”, “width” → 120), mapping(“label” → translated “Delay (in Days)”, “fieldname” → “delay”, “fieldtype” →  ….

**Local steps**

- Return list(mapping(“label” → translated “Delivery Date”, “fieldname” → “delivery\_date”, “fieldtype” → “Date”, “width” → 120), mapping(“label” → translated “Delay (in Days)”, “fieldname” → “delay”, “fieldtype” →  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L123)

<a id="op-a1965efc9e9c75"></a>
### Get warehouse column

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_warehouse_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …).

**Local steps**

- Return mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L131)

<a id="op-cbcfe93a413995"></a>
### Get company column

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_company_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …).

**Local steps**

- Return mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L122)

## Record · Sales order item

[Record definition](../../../../data/record-types/sales_order_item.json)

<a id="op-e39686a05f8950"></a>
### On doctype update

`operation_enterprise_selling_record_definitions_sales_order_item_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Sales Order Item”.

**Local steps**

- Evaluate Platform.db.add\_index(“Sales Order Item”, list(“item\_code”, “warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0656.json#L3563) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1379)

## Report · Sales order trends

<a id="op-dd0eae3dd7cd08"></a>
### Execute

`operation_enterprise_selling_report_sales_order_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Sales Order”).
- Set data from get\_data(filters, conditions).
- Set chart\_data from get\_chart\_data(data, conditions, filters).
- Return tuple(conditions at “columns”, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L138)

<a id="op-06dbdec263038b"></a>
### Get chart data

`operation_enterprise_selling_report_sales_order_trends_business_behavior_get_chart_data`

**Inputs** data, conditions, filters.

**Explicit results** list() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Sales Value”), “values” → datapoin ….

**Local steps**

- If not (data and conditions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → conditions.
  - Return list().
- Set datapoints from list().
- If filters.get(“based\_on”) belongs to list(“Customer”).
  - Set start from 3.
- Otherwise.
  - If filters.get(“based\_on”) belongs to list(“Item”).
    - Set start from 2.
  - Otherwise.
    - Set start from 1.
- If filters.get(“group\_by”).
  - Update start using + 1.
- Set columns from conditions.get(“columns”) at slice start to negative 2 at slice 2 to no value with step 2.
- Set labels from list of column.split(“:”) at 0.replace(“ (Amt)”, empty text) for column drawn from columns.
  - Draw column from columns.
- Set datapoints from (list(0) × len(labels)).
- Set group\_by\_col\_idx from no value.
- If filters.get(“group\_by”).
  - Set group\_by\_col\_idx from conditions at “columns”.index(conditions at “grbc” at 0).
- For each row in data.
  - If row at 0 equals formatted text '{translated “Total”}'.
    - Continue with the next iteration or loop test.
  - If (group\_by\_col\_idx is distinct from no value and row at group\_by\_col\_idx equals empty text).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in group\_by\_col\_idx is distinct from no value → row at group\_by\_col\_idx equals empty text.
    - Continue with the next iteration or loop test.
  - Set row from list of x when x, otherwise 0 for x drawn from row at slice start to negative 2.
    - Draw x from row at slice start to negative 2.
    - Value choice on x — true gives x, false gives 0.
  - Set row from row at slice 2 to no value with step 2.
  - For each i in range(len(row)).
    - Update datapoints at i using + row at i.
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Sales Value”), “values” → datapoin ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L139)

## Report · Sales partner commission summary

<a id="op-dc6089c05f04a8"></a>
### Execute

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** SalesPartnerCommissionSummaryReport(filters).run().

**Local steps**

- If not filters.
  - Set filters from mapping().
- Return SalesPartnerCommissionSummaryReport(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L5412) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L148)

<a id="op-5430cc3e252aca"></a>
### Sales Partner Summary Report.initialize

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_initialize`

**Inputs** self, filters.

**Local steps**

- Set self.filters from filters.
- Set self.columns from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L5503) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L157)

<a id="op-c549b4db45a74e"></a>
### Sales Partner Summary Report.run

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.validate\_filters().
- Evaluate self.prepare\_columns().
- Evaluate self.get\_data().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [validate filters](operations-021.md#op-a995b36141a74e), [prepare columns](operations-021.md#op-985be5dfd72e1f), [get data](operations-021.md#op-3a2814e5c502be).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L5579) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L160)

<a id="op-a995b36141a74e"></a>
### Sales Partner Summary Report.validate filters

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select the document type first.” · validation helper — translated “DocType can be one of them {0}”.format(comma\_or(SALES\_TRANSACTION\_DOCTYPES)) · validation helper — translated “Please select a company.” · validation helper — translated “From Date cannot be greater than To Date.”.

**Local steps**

- Evaluate validate\_date\_range(self.filters).
- If not self.filters.get(“doctype”).
  - Call the validation error handler Platform.throw(translated “Please select the document type first.”).
- If self.filters.get(“doctype”) does not belong to SALES\_TRANSACTION\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “DocType can be one of them {0}”.format(comma\_or(SALES\_TRANSACTION\_DOCTYPES))).
- If not self.filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “Please select a company.”).
- If (self.filters.get(“from\_date”) and self.filters.get(“to\_date”) and self.filters.get(“from\_date”) &gt; self.filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“from\_date”) → self.filters.get(“to\_date”) → self.filters.get(“from\_date”) &gt; self.filters.get(“to\_date”).
  - Call the validation error handler Platform.throw(translated “From Date cannot be greater than To Date.”).
- Evaluate self.\_set\_date\_field\_and\_label().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set date field and label](operations-021.md#op-bf61ea9e63b683).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L162)

<a id="op-bf61ea9e63b683"></a>
### Sales Partner Summary Report.set date field and label

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_set_date_field_and_label`

**Inputs** self.

**Local steps**

- Set self.date\_field from “transaction\_date” when self.filters.get(“doctype”) equals “Sales Order”, otherwise “posting\_date”.
  - Value choice on self.filters.get(“doctype”) equals “Sales Order” — true gives “transaction\_date”, false gives “posting\_date”.
- Set self.date\_label from translated “Order Date” when self.date\_field equals “transaction\_date”, otherwise translated “Posting Date”.
  - Value choice on self.date\_field equals “transaction\_date” — true gives translated “Order Date”, false gives translated “Posting Date”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6181) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L161)

<a id="op-985be5dfd72e1f"></a>
### Sales Partner Summary Report.prepare columns

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_prepare_columns`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6369) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L159)

<a id="op-3a2814e5c502be"></a>
### Sales Partner Summary Report.get data

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.build\_report\_query().
- Set self.data from self.query.run(as\_dict = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build report query](operations-021.md#op-0e8440d49f8a0d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6411) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L156)

<a id="op-0e8440d49f8a0d"></a>
### Sales Partner Summary Report.build report query

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_build_report_query`

**Inputs** self.

**Local steps**

- Evaluate self.\_build\_report\_base\_query().
- Evaluate self.extend\_report\_query().
- Evaluate self.\_apply\_common\_filters().
- Evaluate self.apply\_filters().

If control reaches the end, it returns no value.

**Methods declared on this owner** [build report base query](operations-021.md#op-d88626c31dfe5d), [extend report query](operations-021.md#op-19d5abb9c87bc3), [apply common filters](operations-021.md#op-4707583101bb6b), [apply filters](operations-021.md#op-bf1932b36f5d86).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6505) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L154)

<a id="op-d88626c31dfe5d"></a>
### Sales Partner Summary Report.build report base query

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_build_report_base_query`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set self.dt from DocType(self.filters.get(“doctype”)).
- Set company\_currency from Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).
- Set self.query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L6616) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L153)

<a id="op-19d5abb9c87bc3"></a>
### Sales Partner Summary Report.extend report query

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_extend_report_query`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L7124) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L155)

<a id="op-4707583101bb6b"></a>
### Sales Partner Summary Report.apply common filters

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_apply_common_filters`

**Inputs** self.

**Local steps**

- For each field in list(“company”, “customer”, “territory”, “sales\_partner”).
  - If self.filters.get(field).
    - Set self.query from self.query.where(Field(field, table = self.dt) equals self.filters.get(field)).
- If condition bound to self.\_get\_allowed\_companies\_condition().
  - Set self.query from self.query.where(condition).
- If self.filters.get(“from\_date”).
  - Set self.query from self.query.where(Field(self.date\_field, table = self.dt) ≥ self.filters.get(“from\_date”)).
- If self.filters.get(“to\_date”).
  - Set self.query from self.query.where(Field(self.date\_field, table = self.dt) ≤ self.filters.get(“to\_date”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allowed companies condition](operations-021.md#op-6a528f244b83a1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L151)

<a id="op-6a528f244b83a1"></a>
### Sales Partner Summary Report.get allowed companies condition

`operation_enterprise_binding_enterprise_selling_report_sales_partner_commission_summary_sales_partner_commission_summary_salespartnersummaryreport_get_allowed_companies_condition`

**Inputs** self.

**Explicit results** no value · self.dt.company.isin(allowed).

**Local steps**

- Bind dependencies get\_allowed\_docs\_for\_doctype, get\_user\_permissions.
- Set user\_permissions from get\_user\_permissions(Platform.session.user).
- If “Company” does not belong to user\_permissions.
  - Return no value.
- If allowed bound to get\_allowed\_docs\_for\_doctype(user\_permissions at “Company”, self.filters.get(“doctype”)).
  - Return self.dt.company.isin(allowed).
- Return no value.

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L135)

<a id="op-bf1932b36f5d86"></a>
### Sales Partner Summary Report.apply filters

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_apply_filters`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0674.json#L7634) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L152)

<a id="op-dd824aaf8e383f"></a>
### Sales Partner Summary Report.make column

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_summary_report_make_column`

**Inputs** self, label, fieldname, fieldtype, width = 140, options = empty text, hidden = 0.

**Local steps**

- Evaluate self.columns.append(dict(label = label, fieldname = fieldname, fieldtype = fieldtype, options = options, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0675.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L158)

<a id="op-13fdd7e1ed7f7f"></a>
### Sales Partner Commission Summary Report.prepare columns

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_commission_summary_report_prepare_columns`

**Inputs** self.

**Local steps**

- Evaluate self.make\_column(translated self.filters.get(“doctype”), “name”, “Link”, options = self.filters.get(“doctype”)).
- Evaluate self.make\_column(translated “Customer”, “customer”, “Link”, options = “Customer”).
- Evaluate self.make\_column(translated “Currency”, “currency”, “Data”, 80, hidden = 1).
- Evaluate self.make\_column(translated “Territory”, “territory”, “Link”, 100, …).
- Evaluate self.make\_column(self.date\_label, “posting\_date”, “Date”).
- Evaluate self.make\_column(translated “Amount”, “amount”, “Currency”, 120, …).
- Evaluate self.make\_column(translated “Sales Partner”, “sales\_partner”, “Link”, options = “Sales Partner”).
- Evaluate self.make\_column(translated “Commission Rate %”, “commission\_rate”, “Data”, 100).
- Evaluate self.make\_column(translated “Total Commission”, “total\_commission”, “Currency”, 120, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0675.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L150)

<a id="op-e1d44badd9924f"></a>
### Sales Partner Commission Summary Report.extend report query

`operation_enterprise_selling_report_sales_partner_commission_summary_business_behavior_sales_partner_commission_summary_report_extend_report_query`

**Inputs** self.

**Local steps**

- Set self.query from self.query.select(self.dt.base\_net\_total.as\_(“amount”), self.dt.total\_commission).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0675.json#L843) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L149)

## Report · Sales partner target variance based on item group

<a id="op-87ecd1b255183b"></a>
### Get data column

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_data_column`

**Inputs** filters, partner\_doctype.

**Explicit results** tuple(columns, data).

**Local steps**

- Set data from list().
- Set period\_list from get\_period\_list(filters.fiscal\_year, filters.fiscal\_year, empty text, empty text, company = filters.company, …).
- Set rows from get\_data(filters, period\_list, partner\_doctype).
- Set columns from get\_columns(filters, period\_list, partner\_doctype).
- If not rows.
  - Return tuple(columns, data).
- For each tuple(key, value) in rows.items().
  - Evaluate value.update(mapping(Platform.scrub(partner\_doctype) → key at 0, “item\_group” → key at 1)).
  - Evaluate data.append(value).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L1207) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L178)

<a id="op-50b283c234aa5d"></a>
### Get data

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_data`

**Inputs** filters, period\_list, partner\_doctype.

**Explicit results** no value · prepare\_data(filters, sales\_users\_data, sales\_user\_wise\_item\_groups, actual\_data, …).

**Local steps**

- Set sales\_field from Platform.scrub(partner\_doctype).
- Set sales\_users\_data from get\_parents\_data(filters, partner\_doctype).
- If not sales\_users\_data.
  - Return no value.
- Set sales\_users from list().
- Set sales\_user\_wise\_item\_groups from mapping().
- For each d in sales\_users\_data.
  - If d.parent does not belong to sales\_users.
    - Evaluate sales\_users.append(d.parent).
  - Evaluate sales\_user\_wise\_item\_groups.setdefault(d.parent, list()).
  - If d.item\_group.
    - Evaluate sales\_user\_wise\_item\_groups at d.parent.append(d.item\_group).
- Set date\_field from “transaction\_date” when filters.get(“doctype”) equals “Sales Order”, otherwise “posting\_date”.
  - Value choice on filters.get(“doctype”) equals “Sales Order” — true gives “transaction\_date”, false gives “posting\_date”.
- Set sales\_user\_map from get\_sales\_user\_map(partner\_doctype, sales\_users).
- Set actual\_users from set of name for names drawn from sales\_user\_map.values(), then name drawn from names.
  - Draw names from sales\_user\_map.values().
  - Draw name from names.
- Set actual\_data from get\_actual\_data(filters, list(actual\_users), date\_field, sales\_field).
- Return prepare\_data(filters, sales\_users\_data, sales\_user\_wise\_item\_groups, actual\_data, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L177)
