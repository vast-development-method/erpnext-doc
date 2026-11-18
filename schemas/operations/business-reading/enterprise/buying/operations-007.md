# Purchasing · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Request for quotation

[Record definition](../../../../data/record-types/request_for_quotation.json)

<a id="op-b86a1a3152afba"></a>
### Create rfq items

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_create_rfq_items`

**Inputs** sq\_doc, supplier, rfq\_row, data, dimension\_fields.

**Record and data access** read “Item Supplier” via get\_value.

**Local steps**

- Set args from mapping of field → rfq\_row.get(field) for field drawn from list(“item\_code”, “item\_name”, “description”, “conversion\_factor”, …).
  - Draw field from list(“item\_code”, “item\_name”, “description”, “conversion\_factor”, …).
- Evaluate args.update(mapping of field → rfq\_row.get(field) for field drawn from dimension\_fields).
  - Draw field from dimension\_fields.
- Set rate from flt(data.get(“rate”), sq\_doc.precision(“rate”, “items”)).
- Evaluate args.update(mapping(“qty” → flt(data.get(“qty”)), “rate” → rate, “request\_for\_quotation\_item” → rfq\_row.name, “request\_for\_quotation” → rfq\_row.parent, …)).
- If (data.get(“rate”) does not belong to tuple(no value, empty text) and not rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“rate”) does not belong to tuple(no value, empty text) → not rate.
  - Set args at “discount\_percentage” from 100.
- Evaluate sq\_doc.append(“items”, args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L65)

<a id="op-f17ca735854052"></a>
### Get pdf

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_get_portable_document`

**Inputs** name, supplier, print\_format = no value, language = no value, letterhead = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Request for Quotation” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Request for Quotation”, name).
- If supplier.
  - Evaluate doc.update\_supplier\_part\_no(supplier).
- Evaluate download\_pdf(doc.doctype, doc.name, print\_format, doc = doc, language = language, letterhead = (letterhead or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in letterhead → no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L4930) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L7)

<a id="op-cf35d74b2d6006"></a>
### Get item from material requests based on supplier

`operation_enterprise_binding_enterprise_buying_doctype_request_for_quotation_request_for_quotation_get_item_from_material_requests_based_on_supplier`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Item).

**Explicit results** target\_doc.

**Local steps**

- Set mr\_items\_list from Platform.db.sql(query text (SELECT, Item), mapping(“supplier” → source\_name), as\_dict = 1).
- Set material\_requests from mapping().
- For each d in mr\_items\_list.
  - Evaluate material\_requests.setdefault(d.name, list()).append(d.item\_code).
- For each tuple(mr, items) in material\_requests.items().
  - Set target\_doc from get\_mapped\_doc(“Material Request”, mr, mapping(“Material Request” → mapping(“doctype” → “Request for Quotation”, “validation” → mapping(“docstatus” → list(“=”, 1), “material\_request\_type” → list(“=”, “Purc ….
- Return target\_doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L67)

<a id="op-4cdcbca6244c94"></a>
### Get supplier tag

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_get_supplier_tag`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Tag Link” via get\_all.

**Explicit results** tags.

**Local steps**

- Set filters from mapping(“document\_type” → “Supplier”).
- Set tags from list(set(generator of tag.tag for tag drawn from Platform.get\_all(“Tag Link”, filters = filters, fields = list(“tag”)) where tag)).
  - Draw tag from Platform.get\_all(“Tag Link”, filters = filters, fields = list(“tag”)), keep a combination only if (tag).
- Return tags.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L5216) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L9)

<a id="op-deb6dfe0fe0290"></a>
### Get rfq containing supplier

`operation_enterprise_buying_record_definitions_request_for_quotation_business_behavior_get_request_for_quotation_containing_supplier`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Request for Quotation Supplier” via get\_all · read “Request for Quotation” via get\_list.

**Explicit results** Platform.get\_list(“Request for Quotation”, filters = rfq\_filters, fields = list(“name”, “transaction\_date”, “company”), group\_by = “name”, order\_by = “transaction\_date asc”, …).

**Local steps**

- Set rfq\_filters from list(list(“docstatus”, “=”, 1), list(“company”, “=”, filters.get(“company”))).
- If Platform.has\_permission(“Request for Quotation”, “read”).
  - Evaluate rfq\_filters.append(list(“Request for Quotation Supplier”, “supplier”, “=”, filters.get(“supplier”))).
- Otherwise.
  - Set parents from Platform.get\_all(“Request for Quotation Supplier”, filters = mapping(“supplier” → filters.get(“supplier”), “parenttype” → “Request for Quotation”), pluck = “parent”, distinct = true).
  - Evaluate rfq\_filters.append(list(“name”, “in”, (parents or list(empty text)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parents → list(empty text).
- If txt.
  - Evaluate rfq\_filters.append(list(“name”, “like”, formatted text %{txt}%)).
- If filters.get(“transaction\_date”).
  - Evaluate rfq\_filters.append(list(“transaction\_date”, “=”, filters.get(“transaction\_date”))).
- Return Platform.get\_list(“Request for Quotation”, filters = rfq\_filters, fields = list(“name”, “transaction\_date”, “company”), group\_by = “name”, order\_by = “transaction\_date asc”, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Request for Quotation”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L8)

<a id="op-22767d1c393fba"></a>
### Get data

`operation_enterprise_buying_record_definitions_request_for_quotation_request_for_quotation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“docstatus” → 1, “fieldname” → “request\_for\_quotation”, “transactions” → list(mapping(“items” → list(“Supplier Quotation”)))).

**Local steps**

- Return mapping(“docstatus” → 1, “fieldname” → “request\_for\_quotation”, “transactions” → list(mapping(“items” → list(“Supplier Quotation”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0346.json#L6174) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L34)

## Report · Requested items to order and receive

<a id="op-becd3033fefcf9"></a>
### Execute

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(columns, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Return tuple(list(), list()).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Set tuple(data, chart\_data) from prepare\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0360.json#L438) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L225)

<a id="op-f91e3bbfd9b765"></a>
### Validate filters

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “From and To Dates are required.” · validation helper — translated “To Date cannot be before From Date.”.

**Local steps**

- Set tuple(from\_date, to\_date) from tuple(filters.get(“from\_date”), filters.get(“to\_date”)).
- Evaluate validate\_date\_range(mapping(“from\_date” → getdate(from\_date), “to\_date” → getdate(to\_date))).
- If (not from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_date → to\_date.
  - Call the validation error handler Platform.throw(translated “From and To Dates are required.”).
- Otherwise.
  - If date\_diff(to\_date, from\_date) &lt; 0.
    - Call the validation error handler Platform.throw(translated “To Date cannot be before From Date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L232)

<a id="op-c517a365305e86"></a>
### Get data

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set mr from Platform.qb.DocType(“Material Request”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(mr.name.as\_(“material\_request”), mr.transaction\_da ….
- Set query from get\_conditions(filters, query, mr, mr\_item).
- Set query from query.groupby(mr.name, mr\_item.item\_code).orderby(mr.transaction\_date, mr.schedule\_date).
- Set data from query.run(as\_dict = true).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L228)

<a id="op-5518c19ef68d32"></a>
### Get conditions

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_get_conditions`

**Inputs** filters, query, mr, mr\_item.

**Explicit results** query.

**Local steps**

- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set query from query.where((mr.transaction\_date ≥ filters.get(“from\_date”) bitwise and mr.transaction\_date ≤ filters.get(“to\_date”))).
- If filters.get(“company”).
  - Set query from query.where(mr.company equals filters.get(“company”)).
- If filters.get(“material\_request”).
  - Set query from query.where(mr.name equals filters.get(“material\_request”)).
- If filters.get(“item\_code”).
  - Set query from query.where(mr\_item.item\_code equals filters.get(“item\_code”)).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0360.json#L2536) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L227)

<a id="op-97d730c47fcfff"></a>
### Update qty columns

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_update_quantity_columns`

**Inputs** row\_to\_update, data\_row.

**Local steps**

- Set fields from list(“qty”, “stock\_qty”, “ordered\_qty”, “received\_qty”, …).
- For each field in fields.
  - Update row\_to\_update at field using + flt(data\_row at field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0360.json#L3049) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L231)

<a id="op-3fa65e0fbaf209"></a>
### Prepare data

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_prepare_data`

**Inputs** data, filters.

**Explicit results** tuple(data, chart\_data).

**Local steps**

- Set tuple(material\_request\_map, item\_qty\_map) from tuple(mapping(), mapping()).
- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- For each row in data.
  - If row at “item\_code” does not belong to item\_qty\_map.
    - Set item\_qty\_map at row at “item\_code” from mapping(“qty” → flt(row at “stock\_qty”, precision), “stock\_qty” → flt(row at “stock\_qty”, precision), “stock\_uom” → row at “stock\_uom”, “uom” → row at “uom”, …).
  - Otherwise.
    - Set item\_entry from item\_qty\_map at row at “item\_code”.
    - Evaluate update\_qty\_columns(item\_entry, row).
  - If filters.get(“group\_by\_mr”).
    - If row at “material\_request” does not belong to material\_request\_map.
      - Set row\_copy from copy.deepcopy(row).
      - Set material\_request\_map at row at “material\_request” from row\_copy.
    - Otherwise.
      - Set mr\_row from material\_request\_map at row at “material\_request”.
      - Set mr\_row at “required\_date” from min(getdate(mr\_row at “required\_date”), getdate(row at “required\_date”)).
      - Evaluate update\_qty\_columns(mr\_row, row).
- Set chart\_data from prepare\_chart\_data(item\_qty\_map).
- If filters.get(“group\_by\_mr”).
  - Set data from list().
  - For each mr in material\_request\_map.
    - Evaluate data.append(material\_request\_map at mr).
  - Return tuple(data, chart\_data).
- Return tuple(data, chart\_data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0360.json#L3198) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L230)

<a id="op-1b943c2caa2f34"></a>
### Prepare chart data

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_prepare_chart_data`

**Inputs** item\_data.

**Explicit results** chart\_data.

**Local steps**

- Set tuple(labels, qty\_to\_order, ordered\_qty, received\_qty, …) from tuple(list(), list(), list(), list(), …).
- If len(item\_data) &gt; 30.
  - Set item\_data from dict(list(item\_data.items()) at slice no value to 30).
- For each row in item\_data.
  - Set mr\_row from item\_data at row.
  - Evaluate labels.append(row).
  - Evaluate qty\_to\_order.append(mr\_row at “qty\_to\_order”).
  - Evaluate ordered\_qty.append(mr\_row at “ordered\_qty”).
  - Evaluate received\_qty.append(mr\_row at “received\_qty”).
  - Evaluate qty\_to\_receive.append(mr\_row at “qty\_to\_receive”).
- Set chart\_data from mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Qty to Order”, “values” → qty\_to\_order), mapping(“name” → translated “Ordered Qty”, “values” → ordered\_qty), mappi ….
- Return chart\_data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0360.json#L4162) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L229)

<a id="op-8a6c03e75c5266"></a>
### Get columns

`operation_enterprise_buying_report_requested_items_to_order_and_receive_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Material Request”, “fieldname” → “material\_request”, “fieldtype” → “Link”, “options” → “Material Request”, …), mapping(“label” → translated “Date”, “fieldname” → “date”,  ….
- If not filters.get(“group\_by\_mr”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “ ….
- Evaluate columns.extend(list(mapping(“label” → translated “Qty in Stock UOM”, “fieldname” → “stock\_qty”, “fieldtype” → “Float”, “width” → 140, …), mapping(“label” → translated “Ordered Qty”, “fieldname” → “ordered\_ ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L226)

## Report · Subcontract order summary

<a id="op-462627f019add9"></a>
### Execute

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L237)

<a id="op-3a157722db4f80"></a>
### Get data

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_data`

**Inputs** report\_filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set orders from get\_subcontracted\_orders(report\_filters).
- If orders.
  - Set supplied\_items from get\_supplied\_items(orders, report\_filters).
  - Set order\_details from prepare\_subcontracted\_data(orders, supplied\_items).
  - Evaluate get\_subcontracted\_data(order\_details, data).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0361.json#L1786) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L239)

<a id="op-f77ce517f848d5"></a>
### Get subcontracted orders

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_subcontracted_orders`

**Inputs** report\_filters.

**Record and data access** read report\_filters.order\_type via get\_list.

**Explicit results** (Platform.get\_list(report\_filters.order\_type, fields = fields, filters = filters) or list()).

**Local steps**

- Set fields from list(formatted text ′tab{report\_filters.order\_type} Item′.′parent′ as order\_id, formatted text ′tab{report\_filters.order\_type} Item′.′item\_code′, formatted text ′tab{report\_filters.order\_type} Item′.′item\_ ….
- Set filters from get\_filters(report\_filters).
- Return (Platform.get\_list(report\_filters.order\_type, fields = fields, filters = filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_list(report\_filters.order\_type, fields = fields, filters = filters) → list().

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L242)

<a id="op-09fadb2702da35"></a>
### Get filters

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_filters`

**Inputs** report\_filters.

**Explicit results** filters.

**Local steps**

- Set filters from list(list(report\_filters.order\_type, “docstatus”, “=”, 1), list(report\_filters.order\_type, “transaction\_date”, “between”, tuple(report\_filters.from\_date, report\_filters.to\_date))).
- If report\_filters.order\_type equals “Purchase Order”.
  - Evaluate filters.append(list(“Purchase Order”, “is\_old\_subcontracting\_flow”, “=”, 1)).
- For each field in list(“name”, “company”).
  - If report\_filters.get(field).
    - Evaluate filters.append(list(report\_filters.order\_type, field, “=”, report\_filters.get(field))).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L240)

<a id="op-ddf7272f15559a"></a>
### Get supplied items

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_supplied_items`

**Inputs** orders, report\_filters.

**Record and data access** read supplied\_items\_table via get\_all.

**Explicit results** list() · supplied\_items.

**Local steps**

- If not orders.
  - Return list().
- Set fields from list(“parent”, “main\_item\_code”, “rm\_item\_code”, “required\_qty”, …).
- Set filters from mapping(“parent” → tuple(“in”, list of d.order\_id for d drawn from orders), “docstatus” → 1).
  - Draw d from orders.
- Set supplied\_items from mapping().
- Set supplied\_items\_table from “Purchase Order Item Supplied” when report\_filters.order\_type equals “Purchase Order”, otherwise “Subcontracting Order Supplied Item”.
  - Value choice on report\_filters.order\_type equals “Purchase Order” — true gives “Purchase Order Item Supplied”, false gives “Subcontracting Order Supplied Item”.
- For each row in Platform.get\_all(supplied\_items\_table, fields = fields, filters = filters).
  - Set new\_key from tuple(row.parent, row.reference\_name, row.main\_item\_code).
  - Evaluate supplied\_items.setdefault(new\_key, list()).append(row).
- Return supplied\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L243)

<a id="op-deb419ec790a49"></a>
### Prepare subcontracted data

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_prepare_subcontracted_data`

**Inputs** orders, supplied\_items.

**Explicit results** order\_details.

**Local steps**

- Set order\_details from mapping().
- For each row in orders.
  - Set key from tuple(row.order\_id, row.name, row.item\_code).
  - If key does not belong to order\_details.
    - Evaluate order\_details.setdefault(key, Platform.\_dict(mapping(“order\_item” → row, “supplied\_items” → list()))).
  - Set details from order\_details at key.
  - If supplied\_items.get(key).
    - For each supplied\_item in supplied\_items at key.
      - Evaluate details at “supplied\_items”.append(supplied\_item).
- Return order\_details.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0361.json#L2763) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L244)

<a id="op-2c7aadc76a1032"></a>
### Get subcontracted data

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_subcontracted_data`

**Inputs** order\_details, data.

**Local steps**

- For each tuple(\_key, details) in order\_details.items().
  - Set res from details.order\_item.
  - For each tuple(index, row) in enumerate(details.supplied\_items).
    - If index differs from 0.
      - Set res from mapping(“order\_id” → details.order\_item.order\_id).
    - Evaluate res.update(row).
    - Evaluate data.append(res).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L241)

<a id="op-205394a159dd8d"></a>
### Get columns

`operation_enterprise_buying_report_subcontract_order_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Subcontract Order”, “fieldname” → “order\_id”, “fieldtype” → “Link”, “options” → filters.order\_type, …), mapping(“label” → translated “Supplier”, “fieldname” → “supplier”, ….

**Local steps**

- Return list(mapping(“label” → translated “Subcontract Order”, “fieldname” → “order\_id”, “fieldtype” → “Link”, “options” → filters.order\_type, …), mapping(“label” → translated “Supplier”, “fieldname” → “supplier”, ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L238)

## Report · Subcontracted item to be received

<a id="op-e860273111ea65"></a>
### Execute

`operation_enterprise_buying_report_subcontracted_item_to_be_received_business_behavior_execute`

**Inputs** filters = no value.

**State and service calls** msgprint with translated “To Date must be greater than From Date”.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If filters.from\_date &gt; filters.to\_date.
  - Evaluate Platform.msgprint(translated “To Date must be greater than From Date”).
- Set data from list().
- Set columns from get\_columns(filters).
- Evaluate get\_data(data, filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L247)

<a id="op-387e6082a8bb60"></a>
### Get columns

`operation_enterprise_buying_report_subcontracted_item_to_be_received_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Subcontract Order”, “fieldtype” → “Link”, “fieldname” → “subcontract\_order”, “options” → filters.order\_type, …), mapping(“label” → translated “Date”, “fieldtype” → “Date” ….

**Local steps**

- Return list(mapping(“label” → translated “Subcontract Order”, “fieldtype” → “Link”, “fieldname” → “subcontract\_order”, “options” → filters.order\_type, …), mapping(“label” → translated “Date”, “fieldtype” → “Date” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L248)
