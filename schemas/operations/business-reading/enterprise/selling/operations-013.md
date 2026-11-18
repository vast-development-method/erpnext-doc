# Sales · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quotation

[Record definition](../../../../data/record-types/quotation.json)

<a id="op-c2def927b1d3bf"></a>
### Make sales invoice

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_invoice_4eb67e7f4a6d`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false, args = no value.

**Explicit results** doclist.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set customer from \_make\_customer(source\_name, ignore\_permissions).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Quotation”, source\_name, mapping(“Quotation” → mapping(“doctype” → “Sales Invoice”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Quotation Item” → mapping(“doctype” → “Sales Invoic ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L2)

<a id="op-ca77a1e7df388d"></a>
### Make sales invoice.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_invoice_set_missing_values`

**Inputs** source, target.

**Local steps**

- If customer.
  - Set target.customer from customer.name.
  - Set target.customer\_name from customer.customer\_name.
- Set target.flags.ignore\_permissions from ignore\_permissions.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L4)

<a id="op-18275aedb6a470"></a>
### Make sales invoice.update item

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_invoice_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.cost\_center from no value.
- Set target.stock\_qty from (flt(obj.qty) × flt(obj.conversion\_factor)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L5)

<a id="op-03067924efeb0d"></a>
### Make sales invoice.select item

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_sales_invoice_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L3)

<a id="op-2e59541b29e855"></a>
### Make customer

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_make_customer`

**Inputs** source\_name, ignore\_permissions = false.

**Record and data access** read “Quotation” via get\_value · resolve a document from “Customer” via get\_doc.

**Explicit results** Platform.get\_doc(“Customer”, existing\_customer) · create\_customer\_from\_lead(quotation.party\_name, ignore\_permissions = ignore\_permissions) · create\_customer\_from\_prospect(quotation.party\_name, ignore\_permissions = ignore\_permissions) · no value.

**Local steps**

- Set quotation from Platform.db.get\_value(“Quotation”, source\_name, list(“order\_type”, “quotation\_to”, “party\_name”, “customer\_name”), as\_dict = 1).
- Set existing\_customer from get\_existing\_customer\_name(quotation.quotation\_to, quotation.party\_name).
- If existing\_customer.
  - Return Platform.get\_doc(“Customer”, existing\_customer).
- If quotation.quotation\_to equals “Lead”.
  - Return create\_customer\_from\_lead(quotation.party\_name, ignore\_permissions = ignore\_permissions).
- Otherwise.
  - If quotation.quotation\_to equals “Prospect”.
    - Return create\_customer\_from\_prospect(quotation.party\_name, ignore\_permissions = ignore\_permissions).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1513)

<a id="op-9d59ce1194b070"></a>
### Get existing customer name

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_get_existing_customer_name`

**Inputs** quotation\_to, party\_name.

**Record and data access** read “Customer” via get\_value.

**Explicit results** no value · party\_name · Platform.db.get\_value(“Customer”, mapping(customer\_field → party\_name)).

**Local steps**

- If not party\_name.
  - Return no value.
- If quotation\_to equals “Customer”.
  - Return party\_name.
- Set customer\_field from mapping(“Lead” → “lead\_name”, “Prospect” → “prospect\_name”, “CRM Deal” → “crm\_deal”).get(quotation\_to).
- If customer\_field.
  - Return Platform.db.get\_value(“Customer”, mapping(customer\_field → party\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1509)

<a id="op-0ea7fa76d8181a"></a>
### Create customer from lead

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_create_customer_from_lead`

**Inputs** lead\_name, ignore\_permissions = false.

**State and service calls** call insert on customer.

**Explicit results** customer.

**Local steps**

- Bind dependencies \_make\_customer.
- Set customer from \_make\_customer(lead\_name, ignore\_permissions = ignore\_permissions).
- Set customer.flags.ignore\_permissions from ignore\_permissions.
- Attempt the following.
  - Evaluate customer.insert().
  - Return customer.
- On failure (Platform.MandatoryError) bound to e.
  - Evaluate handle\_mandatory\_error(e, customer, lead\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1507)

<a id="op-719a36bed451e1"></a>
### Create customer from prospect

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_create_customer_from_prospect`

**Inputs** prospect\_name, ignore\_permissions = false.

**State and service calls** call insert on customer.

**Explicit results** customer.

**Local steps**

- Bind dependencies make\_customer\_from\_prospect.
- Set customer from make\_customer\_from\_prospect(prospect\_name).
- Set customer.flags.ignore\_permissions from ignore\_permissions.
- Attempt the following.
  - Evaluate customer.insert().
  - Return customer.
- On failure (Platform.MandatoryError) bound to e.
  - Evaluate handle\_mandatory\_error(e, customer, prospect\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1508)

<a id="op-4150615f0e5c07"></a>
### Handle mandatory error

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_handle_mandatory_error`

**Inputs** e, customer, lead\_name.

**Explicit failure paths** validation helper — message.

**Local steps**

- Bind dependencies get\_link\_to\_form.
- Set mandatory\_fields from nested operand in the contract.args at 0.split(“:”) at 1.split(“,”).
- Set mandatory\_fields from list of translated customer.meta.get\_label(field.strip()) for field drawn from mandatory\_fields.
  - Draw field from mandatory\_fields.
- Set Platform.local.message\_log from list().
- Set message from (translated “Could not auto create Customer due to the following missing mandatory field(s):” + text in the contract).
- Update message using + ((text in the contract + “&lt;/li&gt;&lt;li&gt;”.join(mandatory\_fields)) + “&lt;/li&gt;&lt;/ul&gt;”).
- Update message using + translated “Please create Customer from Lead {0}.”.format(get\_link\_to\_form(“Lead”, lead\_name)).
- Call the validation error handler Platform.throw(message, title = translated “Mandatory Missing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1512)

<a id="op-1c5f554ef7fa04"></a>
### Get ordered items

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_get_ordered_items`

**Inputs** quotation.

**Record and data access** read “Quotation Item” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Quotation Item”, mapping(“docstatus” → 1, “parent” → quotation, “ordered\_qty” → tuple(“&gt;”, 0)), list(“name”, “ordered\_qty”), as\_list = true)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“Quotation Item”, mapping(“docstatus” → 1, “parent” → quotation, “ordered\_qty” → tuple(“&gt;”, 0)), list(“name”, “ordered\_qty”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1511)

<a id="op-1062453530a3b1"></a>
### Get data

`operation_enterprise_selling_record_definitions_quotation_quotation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “prevdoc\_docname”, “non\_standard\_fieldnames” → mapping(“Auto Repeat” → “reference\_document”), “transactions” → list(mapping(“label” → translated “Sales Order”, “items” → list(“Sales O ….

**Local steps**

- Return mapping(“fieldname” → “prevdoc\_docname”, “non\_standard\_fieldnames” → mapping(“Auto Repeat” → “reference\_document”), “transactions” → list(mapping(“label” → translated “Sales Order”, “items” → list(“Sales O ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L4302) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1279)

## Report · Quotation trends

<a id="op-0bd52ca13d77c2"></a>
### Execute

`operation_enterprise_selling_report_quotation_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Quotation”).
- Set data from get\_data(filters, conditions).
- Set chart\_data from get\_chart\_data(data, conditions, filters).
- Return tuple(conditions at “columns”, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0668.json#L3232) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L67)

<a id="op-2456d782a34956"></a>
### Get chart data

`operation_enterprise_selling_report_quotation_trends_business_behavior_get_chart_data`

**Inputs** data, conditions, filters.

**Explicit results** list() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Quoted Amount”), “values” → datapo ….

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
- Set labels from list of nested operand in the contract.split(“:”) at 0.rsplit(“ (”, 1) at 0 for column drawn from columns.
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
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Quoted Amount”), “values” → datapo ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L68)

## Report · Sales analytics

<a id="op-44e819cf307203"></a>
### Execute

`operation_enterprise_selling_report_sales_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** output · Analytics(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If filters.doc\_type equals “All”.
  - Set filters.tree\_type from “Customer”.
  - Set filters.value\_quantity from “Value”.
  - Set filters.curves from “total”.
  - Set output from no value.
  - For each dt in list(“Quotation”, “Sales Order”, “Delivery Note”, “Sales Invoice”, …).
    - Set filters.doc\_type from dt.
    - Set output from append\_report(dt, output, Analytics(filters).run()).
  - Return output.
- Otherwise.
  - Return Analytics(filters).run().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L101)

<a id="op-dd2743d31ef932"></a>
### Append report

`operation_enterprise_selling_report_sales_analytics_business_behavior_append_report`

**Inputs** dt, org, new.

**State and service calls** call insert on new at 1.

**Explicit results** org · new.

**Local steps**

- Evaluate new at 1.insert(0, mapping(“entity” → translated dt)).
- Evaluate new at 1.append(mapping()).
- If not new at 3 at “data” at “datasets”.
  - Evaluate new at 3 at “data” at “datasets”.append(mapping(“name” → no value, “values” → list())).
- Set new at 3 at “data” at “datasets” at 0 at “name” from translated dt.
- If org.
  - Evaluate org at 1.extend(new at 1).
  - Evaluate org at 3 at “data” at “datasets”.extend(new at 3 at “data” at “datasets”).
  - Return org.
- Otherwise.
  - Return new.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L100)

<a id="op-7adb439c3fa0ad"></a>
### Analytics.initialize

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_initialize`

**Inputs** self, filters = no value.

**Explicit failure paths** validation helper — translated “Only Value available for Payment Entry”.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.entities from (self.filters.get(“entity”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“entity”) → list().
- If (self.filters.doc\_type equals “Payment Entry” and self.filters.value\_quantity equals “Quantity”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.doc\_type equals “Payment Entry” → self.filters.value\_quantity equals “Quantity”.
  - Call the validation error handler Platform.throw(translated “Only Value available for Payment Entry”).
- Set self.date\_field from “transaction\_date” when self.filters.doc\_type belongs to list(“Quotation”, “Sales Order”, “Purchase Order”), otherwise “due\_date” when self.filters.doc\_type equals “Sales Invoice (due)”, otherwise “posting\_date”.
  - Value choice on self.filters.doc\_type belongs to list(“Quotation”, “Sales Order”, “Purchase Order”) — true gives “transaction\_date”, false gives “due\_date” when self.filters.doc\_type equals “Sales Invoice (due)”, otherwise “posting\_date”.
  - Value choice on self.filters.doc\_type equals “Sales Invoice (due)” — true gives “due\_date”, false gives “posting\_date”.
- If self.filters.doc\_type.startswith(“Sales Invoice”).
  - Set self.filters.doc\_type from “Sales Invoice”.
- Set self.months from list(“Jan”, “Feb”, “Mar”, “Apr”, …).
- Evaluate self.get\_period\_date\_ranges().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period date ranges](operations-014.md#op-996618f7bca5d3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0669.json#L3159) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L97)

<a id="op-2cf6e308cf28b6"></a>
### Analytics.update company list for parent company

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_update_company_list_for_parent_company`

**Inputs** self.

**Record and data access** read “Company” via get\_value · read “Company” via get\_list.

**Local steps**

- Set company\_list from list(self.filters.get(“company”)).
- Set selected\_company from self.filters.get(“company”).
- If (selected\_company and self.filters.get(“show\_aggregate\_value\_from\_subsidiary\_companies”) and Platform.db.get\_value(“Company”, selected\_company, “is\_group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_company → self.filters.get(“show\_aggregate\_value\_from\_subsidiary\_companies”) → Platform.db.get\_value(“Company”, selected\_company, “is\_group”).
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Company”, selected\_company, list(“lft”, “rgt”)).
  - Set child\_companies from Platform.db.get\_list(“Company”, filters = mapping(“lft” → list(“&gt;”, lft), “rgt” → list(“&lt;”, rgt)), pluck = “name”).
  - Evaluate company\_list.extend(child\_companies).
- Set self.filters at “company” from company\_list.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0669.json#L3673) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L99)

<a id="op-b19b3cbd4bce34"></a>
### Analytics.run

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart, …).

**Local steps**

- Evaluate self.update\_company\_list\_for\_parent\_company().
- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.filter\_data\_by\_entities().
- Evaluate self.get\_chart\_data().
- Set skip\_total\_row from 0.
- If self.filters.tree\_type belongs to list(“Supplier Group”, “Item Group”, “Customer Group”, “Territory”, …).
  - Set skip\_total\_row from 1.
- Return tuple(self.columns, self.data, no value, self.chart, …).

**Methods declared on this owner** [update company list for parent company](operations-013.md#op-2cf6e308cf28b6), [get columns](operations-013.md#op-58128500fa0103), [get data](operations-013.md#op-8d0e787a069fa3), [filter data by entities](operations-014.md#op-a1089136b46670), [get chart data](operations-014.md#op-6dcce73c9b43d6).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L98)

<a id="op-58128500fa0103"></a>
### Analytics.get columns

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list(mapping(“label” → translated self.filters.tree\_type, “options” → self.filters.tree\_type when self.filters.tree\_type differs from “Order Type”, otherwise empty text, “fieldname” → “entity”, “fieldtype” → “L …).
  - Value choice on self.filters.tree\_type differs from “Order Type” — true gives self.filters.tree\_type, false gives empty text.
  - Value choice on self.filters.tree\_type differs from “Order Type” — true gives “Link”, false gives “Data”.
  - Value choice on self.filters.tree\_type differs from “Order Type” — true gives 140, false gives 200.
- If self.filters.tree\_type belongs to list(“Customer”, “Supplier”, “Item”).
  - Evaluate self.columns.append(mapping(“label” → translated (self.filters.tree\_type + “ Name”), “fieldname” → “entity\_name”, “fieldtype” → “Data”, “width” → 140)).
- If self.filters.tree\_type equals “Item”.
  - Evaluate self.columns.append(mapping(“label” → translated “UOM”, “fieldname” → “stock\_uom”, “fieldtype” → “Link”, “options” → “UOM”, …)).
- For each end\_date in self.periodic\_daterange.
  - Set period from self.get\_period(end\_date).
  - Evaluate self.columns.append(mapping(“label” → translated period, “fieldname” → scrub(period), “fieldtype” → “Float”, “width” → 120)).
- Evaluate self.columns.append(mapping(“label” → translated “Total”, “fieldname” → “total”, “fieldtype” → “Float”, “width” → 120)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get period](operations-014.md#op-afd9f102fb44fb).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0669.json#L4369) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L80)

<a id="op-8d0e787a069fa3"></a>
### Analytics.get data

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_data`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.filters.tree\_type belongs to list(“Customer”, “Supplier”).
  - Evaluate self.get\_sales\_transactions\_based\_on\_customers\_or\_suppliers().
  - Evaluate self.get\_rows().
- Otherwise.
  - If self.filters.tree\_type equals “Item”.
    - If self.filters.doc\_type equals “Payment Entry”.
      - Set self.data from list().
      - Return no value.
    - Evaluate self.get\_sales\_transactions\_based\_on\_items().
    - Evaluate self.get\_rows().
  - Otherwise.
    - If self.filters.tree\_type belongs to list(“Customer Group”, “Supplier Group”, “Territory”).
      - If self.filters.doc\_type equals “Payment Entry”.
        - Set self.data from list().
        - Return no value.
      - Evaluate self.get\_sales\_transactions\_based\_on\_customer\_or\_territory\_group().
      - Evaluate self.get\_rows\_by\_group().
    - Otherwise.
      - If self.filters.tree\_type equals “Item Group”.
        - If self.filters.doc\_type equals “Payment Entry”.
          - Set self.data from list().
          - Return no value.
        - Evaluate self.get\_sales\_transactions\_based\_on\_item\_group().
        - Evaluate self.get\_rows\_by\_group().
      - Otherwise.
        - If self.filters.tree\_type equals “Order Type”.
          - If self.filters.doc\_type does not belong to list(“Quotation”, “Sales Order”).
            - Set self.data from list().
            - Return no value.
          - Evaluate self.get\_sales\_transactions\_based\_on\_order\_type().
          - Evaluate self.get\_rows\_by\_group().
        - Otherwise.
          - If self.filters.tree\_type equals “Project”.
            - If self.filters.doc\_type equals “Quotation”.
              - Set self.data from list().
              - Return no value.
            - Evaluate self.get\_sales\_transactions\_based\_on\_project().
            - Evaluate self.get\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales transactions based on customers or suppliers](operations-014.md#op-ba7a77dc882abc), [get rows](operations-014.md#op-c546c7b1202588), [get sales transactions based on items](operations-014.md#op-5edd96aaf67eab), [get sales transactions based on customer or territory group](operations-014.md#op-df223b0272f0f9), [get rows by group](operations-014.md#op-a648e02b363576), [get sales transactions based on item group](operations-014.md#op-32d602f516530f), [get sales transactions based on order type](operations-013.md#op-512cbe4fd65039), [get sales transactions based on project](operations-014.md#op-c9cd66e595c0c9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0669.json#L5258) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L81)

<a id="op-267c9dac4fc14b"></a>
### Analytics.document filters

`operation_enterprise_binding_enterprise_selling_report_sales_analytics_sales_analytics_analytics_document_filters`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** filters.

**Local steps**

- Set filters from mapping(“docstatus” → 1, “company” → list(“in”, self.filters.company), self.date\_field → tuple(“between”, list(self.filters.from\_date, self.filters.to\_date))).
- If self.filters.doc\_type belongs to list(“Sales Invoice”, “Purchase Invoice”, “Payment Entry”).
  - Set filters at “is\_opening” from “No”.
- Return filters.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L117)

<a id="op-858462fd3c811a"></a>
### Analytics.value field

`operation_enterprise_binding_enterprise_selling_report_sales_analytics_sales_analytics_analytics_value_field`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** “base\_net\_total as value\_field” · “items.stock\_qty as value\_field”.

**Local steps**

- If self.filters at “value\_quantity” equals “Value”.
  - Return “base\_net\_total as value\_field”.
- Return “items.stock\_qty as value\_field”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L119)

<a id="op-073a874f328ec1"></a>
### Analytics.get permitted parent names

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_permitted_parent_names`

**Inputs** self.

**Explicit results** Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(“name”), filters = self.document\_filters, ignore\_permissions = false).run(pluck = “name”).

**Local steps**

- Return Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(“name”), filters = self.document\_filters, ignore\_permissions = false).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L86)

<a id="op-512cbe4fd65039"></a>
### Analytics.get sales transactions based on order type

`operation_enterprise_selling_report_sales_analytics_business_behavior_analytics_get_sales_transactions_based_on_order_type`

**Inputs** self.

**Local steps**

- Set self.entries from Platform.qb.get\_query(table = self.filters.doc\_type, fields = list(“order\_type as entity”, self.value\_field, self.date\_field), filters = mapping(expand self.document\_filters, “order\_type” → list(“is”, “set ….
- Evaluate self.get\_teams().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get teams](operations-014.md#op-2bc001d855c186).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L93)
