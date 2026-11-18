# Purchasing · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Purchase order analysis

<a id="op-e43767ccb42467"></a>
### Group by item

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_group_by_item`

**Inputs** data.

**Explicit results** sorted(item\_map.values(), key = deferred anonymous expression).

**Local steps**

- Set item\_map from mapping().
- For each row in data.
  - Set key from tuple(row at “company”, row at “item\_code”, row at “uom”).
  - Set group from item\_map.get(key).
  - If not group.
    - Set item\_map at key from copy.deepcopy(row).
    - Continue with the next iteration or loop test.
  - Evaluate add\_aggregated\_fields(group, row).
- Return sorted(item\_map.values(), key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L230) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L132)

<a id="op-6a5dcdcb12e2b2"></a>
### Add aggregated fields

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_add_aggregated_fields`

**Inputs** group, row.

**Local steps**

- For each field in AGGREGATED\_FIELDS.
  - Set group at field from (flt(group at field) + flt(row at field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L220) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L122)

<a id="op-cb58c8a1f7146c"></a>
### Prepare chart data

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_prepare_chart_data`

**Inputs** pending, completed.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“values” → list(pending, completed)))), “type” → “donut”, “height” → 300).

**Local steps**

- Set labels from list(translated “Amount to Bill”, translated “Billed Amount”).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“values” → list(pending, completed)))), “type” → “donut”, “height” → 300).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0359.json#L798) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L219)

<a id="op-a685d9f0ae45cb"></a>
### Get columns

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** get\_grouped\_by\_item\_columns() · columns.

**Local steps**

- If filters.get(“group\_by\_item”).
  - Return get\_grouped\_by\_item\_columns().
- Set columns from get\_purchase\_order\_columns().
- If not filters.get(“group\_by\_po”).
  - Evaluate columns.append(get\_item\_code\_column()).
- Update columns using + (get\_quantity\_columns() + get\_amount\_columns()).
- Update columns using + list(get\_warehouse\_column(), get\_company\_column()).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L216)

<a id="op-c9d002354e2eac"></a>
### Get grouped by item columns

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_grouped_by_item_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(get\_item\_code\_column(), get\_uom\_column()).
- Update columns using + (get\_quantity\_columns() + get\_amount\_columns()).
- Evaluate columns.append(get\_company\_column()).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L224) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L126)

<a id="op-2bc331be2a4593"></a>
### Get purchase order columns

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_purchase_order_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Date”, “width” → 90), mapping(“label” → translated “Required By”, “fieldname” → “required\_date”, “fieldtype” → “Date”, “width” ….

**Local steps**

- Return list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Date”, “width” → 90), mapping(“label” → translated “Required By”, “fieldname” → “required\_date”, “fieldtype” → “Date”, “width” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L128)

<a id="op-c02d217ee9dd72"></a>
### Get item code column

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_item_code_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …).

**Local steps**

- Return mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L225) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L127)

<a id="op-3ec5efd3fe0b00"></a>
### Get uom column

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_uom_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “UOM”, “fieldname” → “uom”, “fieldtype” → “Link”, “options” → “UOM”, …).

**Local steps**

- Return mapping(“label” → translated “UOM”, “fieldname” → “uom”, “fieldtype” → “Link”, “options” → “UOM”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L228) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L130)

<a id="op-68ada9f8bb2861"></a>
### Get quantity columns

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_quantity_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 120, …), mapping(“label” → translated “Received Qty”, “fieldname” → “received\_qty”, “fieldtype” → “Float”, “wi ….

**Local steps**

- Return list(mapping(“label” → translated “Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 120, …), mapping(“label” → translated “Received Qty”, “fieldname” → “received\_qty”, “fieldtype” → “Float”, “wi ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L227) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L129)

<a id="op-829376caf5f476"></a>
### Get amount columns

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_amount_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Amount”, “fieldname” → “amount”, “fieldtype” → “Currency”, “width” → 110, …), mapping(“label” → translated “Billed Amount”, “fieldname” → “billed\_amount”, “fieldtype” → “ ….

**Local steps**

- Return list(mapping(“label” → translated “Amount”, “fieldname” → “amount”, “fieldtype” → “Currency”, “width” → 110, …), mapping(“label” → translated “Billed Amount”, “fieldname” → “billed\_amount”, “fieldtype” → “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L221) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L123)

<a id="op-86a1f8be28b15b"></a>
### Get warehouse column

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_warehouse_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …).

**Local steps**

- Return mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L229) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L131)

<a id="op-cfb1b79184ea42"></a>
### Get company column

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_company_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …).

**Local steps**

- Return mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L223) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L125)

## Record · Purchase order item

[Record definition](../../../../data/record-types/purchase_order_item.json)

<a id="op-d61f42dcffc0f0"></a>
### On doctype update

`operation_enterprise_buying_record_definitions_purchase_order_item_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Purchase Order Item”.

**Local steps**

- Evaluate Platform.db.add\_index(“Purchase Order Item”, list(“item\_code”, “warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1395)

## Report · Purchase order trends

<a id="op-c163244e67514f"></a>
### Execute

`operation_enterprise_buying_report_purchase_order_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Purchase Order”).
- Set data from get\_data(filters, conditions).
- Set chart\_data from get\_chart\_data(data, conditions, filters).
- Return tuple(conditions at “columns”, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0359.json#L3407) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L223)

<a id="op-347e891193e78e"></a>
### Get chart data

`operation_enterprise_buying_report_purchase_order_trends_business_behavior_get_chart_data`

**Inputs** data, conditions, filters.

**Explicit results** list() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Purchase Value”), “values” → datap ….

**Local steps**

- If not (data and conditions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → conditions.
  - Return list().
- Set datapoints from list().
- If filters.get(“based\_on”) belongs to list(“Supplier”).
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
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → ((nested operand in the contract(nested operand in the contract) + one space) + translated “Purchase Value”), “values” → datap ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0359.json#L3618) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L224)

## Record · Request for quotation

[Record definition](../../../../data/record-types/request_for_quotation.json)

<a id="op-47e3d218218897"></a>
### Requestfor Quotation.before validate

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_unit\_price\_items().
- Set self.flags.allow\_zero\_qty from self.has\_unit\_price\_items.
- Evaluate self.set\_data\_for\_supplier().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has unit price items](operations-005.md#op-4b9ed794d10a15), [set data for supplier](operations-005.md#op-906154f178cb29).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L4282) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L11)

<a id="op-628e18d7d0cd88"></a>
### Requestfor Quotation.validate

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_validate`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_duplicate\_supplier().
- Evaluate self.ensure\_supplier\_is\_not\_blocked().
- Evaluate self.validate\_supplier\_list().
- Evaluate super().validate\_qty\_is\_not\_zero().
- Evaluate validate\_for\_items(self).
- Evaluate self.set\_missing\_item\_names().
- Evaluate super().set\_qty\_as\_per\_stock\_uom().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.update\_email\_id().
- If self.docstatus &lt; 1.
  - Evaluate self.db\_set(“status”, “Draft”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate supplier](operations-005.md#op-26453d187369fd), [validate supplier list](operations-005.md#op-3039323be82c97), [set missing item names](operations-005.md#op-e50091d57774b8), [update email id](operations-005.md#op-fdfb7e32e28ea3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L29)

<a id="op-e50091d57774b8"></a>
### Requestfor Quotation.set missing item names

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_requestforquotation_set_missing_item_names`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- For each row in self.items.
  - If (row.item\_code and not row.item\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.item\_name.
    - Set row.item\_name from Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L831) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L71)

<a id="op-4b9ed794d10a15"></a>
### Requestfor Quotation.set has unit price items

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_set_has_unit_price_items`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_request\_for\_quotation”).
  - Set self.has\_unit\_price\_items from 0.
  - Return no value.
- Set self.has\_unit\_price\_items from any(generator of not row.qty for row drawn from self.get(“items”) where (row.item\_code and not row.qty)).
  - Draw row from self.get(“items”), keep a combination only if ((row.item\_code and not row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.qty.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_request\_for\_quotation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L22)

<a id="op-906154f178cb29"></a>
### Requestfor Quotation.set data for supplier

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_set_data_for_supplier`

**Inputs** self.

**Record and data access** read “Email Template” via get\_value.

**Local steps**

- If self.email\_template.
  - Set data from Platform.get\_value(“Email Template”, self.email\_template, list(“use\_html”, “response”, “response\_html”, “subject”), as\_dict = true).
  - Set self.use\_html from data.use\_html.
  - If data.use\_html.
    - If not self.mfs\_html.
      - Set self.mfs\_html from data.response\_html.
  - Otherwise.
    - If not self.message\_for\_supplier.
      - Set self.message\_for\_supplier from data.response.
  - If not self.subject.
    - Set self.subject from data.subject.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L4798) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L21)

<a id="op-26453d187369fd"></a>
### Requestfor Quotation.validate duplicate supplier

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_validate_duplicate_supplier`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Same supplier has been entered multiple times”.

**Local steps**

- Set supplier\_list from list of d.supplier for d drawn from self.suppliers.
  - Draw d from self.suppliers.
- If len(supplier\_list) differs from len(set(supplier\_list)).
  - Call the validation error handler Platform.throw(translated “Same supplier has been entered multiple times”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L5103) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L30)

<a id="op-3039323be82c97"></a>
### Requestfor Quotation.validate supplier list

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_validate_supplier_list`

**Inputs** self.

**Record and data access** read “Supplier” via get\_value · read “Supplier Scorecard” via get\_value.

**State and service calls** msgprint with translated “{0} currently has a {1} Supplier Scorecard standing, and RFQs to this supplier should be issued with caution.”.format(d.supplier, standing).

**Explicit failure paths** validation helper — translated “RFQs are not allowed for {0} due to a scorecard standing of {1}”.format(d.supplier, standing).

**Local steps**

- For each d in self.suppliers.
  - Evaluate validate\_party\_frozen\_disabled(self.company, “Supplier”, d.supplier).
  - Set prevent\_rfqs from Platform.db.get\_value(“Supplier”, d.supplier, “prevent\_rfqs”).
  - If prevent\_rfqs.
    - Set standing from Platform.db.get\_value(“Supplier Scorecard”, mapping(“supplier” → d.supplier), “status”).
    - Call the validation error handler Platform.throw(translated “RFQs are not allowed for {0} due to a scorecard standing of {1}”.format(d.supplier, standing)).
  - Set warn\_rfqs from Platform.db.get\_value(“Supplier”, d.supplier, “warn\_rfqs”).
  - If warn\_rfqs.
    - Set standing from Platform.db.get\_value(“Supplier Scorecard”, mapping(“supplier” → d.supplier), “status”).
    - Evaluate Platform.msgprint(translated “{0} currently has a {1} Supplier Scorecard standing, and RFQs to this supplier should be issued with caution.”.format(d.supplier, standing), title = translated “Caution”, indi ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L199) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L32)

<a id="op-fdfb7e32e28ea3"></a>
### Requestfor Quotation.update email id

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_update_email_identifier`

**Inputs** self.

**Record and data access** read “Contact” via get\_value.

**Local steps**

- For each rfq\_supplier in self.suppliers.
  - If not rfq\_supplier.email\_id.
    - Set rfq\_supplier.email\_id from Platform.db.get\_value(“Contact”, rfq\_supplier.contact, “email\_id”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L5758) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L24)

<a id="op-01094a51eead55"></a>
### Requestfor Quotation.validate email id

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_requestfor_quotation_validate_email_identifier`

**Inputs** self, args.

**Explicit failure paths** validation helper — translated “Row {0}: For Supplier {1}, Email Address is Required to send an email”.format(args.idx, Platform.bold(args.supplier)).

**Local steps**

- If not args.email\_id.
  - Call the validation error handler Platform.throw(translated “Row {0}: For Supplier {1}, Email Address is Required to send an email”.format(args.idx, Platform.bold(args.supplier))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0345.json#L5885) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L31)
