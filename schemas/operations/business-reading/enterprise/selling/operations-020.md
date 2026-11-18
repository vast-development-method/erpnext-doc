# Sales · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-a4758920bd1a36"></a>
### Get qty billed below amount criterion

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_qty_billed_below_amount_criterion`

**Inputs** sales\_order\_item, billed\_qty.

**Explicit results** (Round((sales\_order\_item.qty − billed\_qty), qty\_precision) ≤ 0 bitwise and Abs(sales\_order\_item.billed\_amt) &lt; Abs(sales\_order\_item.amount)).

**Local steps**

- Set qty\_precision from Platform.get\_precision(“Sales Order Item”, “qty”).
- Return (Round((sales\_order\_item.qty − billed\_qty), qty\_precision) ≤ 0 bitwise and Abs(sales\_order\_item.billed\_amt) &lt; Abs(sales\_order\_item.amount)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L28)

<a id="op-89932b054574c9"></a>
### Get potentially billable item criterion

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_potentially_billable_item_criterion`

**Inputs** sales\_order, sales\_order\_item, item.

**Record and data access** read “Accounts Settings” via get\_cached\_value.

**Explicit results** (is\_unit\_price\_row bitwise or is\_billable\_row).

**Local steps**

- Set global\_allowance from flt(Platform.get\_cached\_value(“Accounts Settings”, no value, “over\_billing\_allowance”)).
- Set allowance from Case().when(item.over\_billing\_allowance differs from 0, item.over\_billing\_allowance).else\_(global\_allowance).
- Set has\_amount\_headroom from (sales\_order\_item.base\_amount equals 0 bitwise or Abs(sales\_order\_item.billed\_amt) &lt; (Abs(sales\_order\_item.amount) × (1 + (allowance ÷ 100)))).
- Set is\_unit\_price\_row from (sales\_order.has\_unit\_price\_items equals 1 bitwise and sales\_order\_item.qty equals 0).
- Set billed\_qty from get\_billed\_qty\_query(sales\_order\_item).
- Set is\_billable\_row from (sales\_order\_item.qty differs from 0 bitwise and ((has\_amount\_headroom bitwise and get\_pending\_qty\_criterion(sales\_order\_item, billed\_qty)) bitwise or get\_qty\_billed\_below\_amount\_criterion(sales\_order\_item ….
- Return (is\_unit\_price\_row bitwise or is\_billable\_row).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Accounts Settings”, no value, “over\_billing\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1332)

<a id="op-411ab3dbbf2eab"></a>
### Has potentially billable items

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_has_potentially_billable_items`

**Inputs** sales\_order.

**Declared result** bool.

**Explicit results** bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Local steps**

- Set so from qb.DocType(“Sales Order”).
- Set so\_item from qb.DocType(“Sales Order Item”).
- Set item from qb.DocType(“Item”).
- Return bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0644.json#L973) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1336)

<a id="op-a9369433a374d4"></a>
### Get potentially billable sales orders

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_potentially_billable_sales_orders`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(cint(page\_len)).offset(cint(start)).run(as\_dict = true).

**Local steps**

- Set so from qb.DocType(“Sales Order”).
- Set so\_item from qb.DocType(“Sales Order Item”).
- Set item from qb.DocType(“Item”).
- Set meta from Platform.get\_meta(“Sales Order”).
- Set search\_fields from list(dict.fromkeys(list(“name”, meta.title\_field, expanded meta.get\_search\_fields()))).
- Set or\_filters from mapping of fieldname → tuple(“like”, formatted text %{txt}%) for fieldname drawn from search\_fields where (fieldname and (fieldname equals “name” or (field bound to nested operand in the contract(nested op ….
  - Value choice on txt — true gives mapping of fieldname → tuple(“like”, formatted text %{txt}%) for fieldname drawn from search\_fields where (fieldname and (fieldname equals “name” or (field bound to nested operand in the contract.get\_field …, false gives no value.
  - Draw fieldname from search\_fields, keep a combination only if ((fieldname and (fieldname equals “name” or (field bound to meta.get\_field(fieldname) and field.fieldtype belongs to LINK\_SEARCH\_FIELDTYPES)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname → (fieldname equals “name” or (field bound to meta.get\_field(fieldname) and field.fieldtype belongs to LINK\_SEARCH\_FIELDTYPES)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname equals “name” → (field bound to meta.get\_field(fieldname) and field.fieldtype belongs to LINK\_SEARCH\_FIELDTYPES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field bound to meta.get\_field(fieldname) → field.fieldtype belongs to LINK\_SEARCH\_FIELDTYPES.
- Set query from Platform.qb.get\_query(so, fields = list(so.name, so.customer, so.transaction\_date, so.creation), filters = filters, or\_filters = or\_filters, ignore\_permissions = false).
- Return nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(cint(page\_len)).offset(cint(start)).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1333)

<a id="op-d82320461f1942"></a>
### Get data

`operation_enterprise_selling_record_definitions_sales_order_sales_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “sales\_order”, “non\_standard\_fieldnames” → mapping(“Delivery Note” → “against\_sales\_order”, “Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → ….

**Local steps**

- Return mapping(“fieldname” → “sales\_order”, “non\_standard\_fieldnames” → mapping(“Delivery Note” → “against\_sales\_order”, “Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0644.json#L2257) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1380)

## Report · Sales order analysis

<a id="op-f3fca54123932f"></a>
### Execute

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list(), no value, list()) · tuple(columns, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Return tuple(list(), list(), no value, list()).
- Set filters from Platform.\_dict(filters).
- Set filters.company from (filters.get(“company”) or Enterprise.get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → Enterprise.get\_default\_company().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Set so\_elapsed\_time from mapping() when filters.get(“group\_by\_item”), otherwise get\_so\_elapsed\_time(data).
  - Value choice on filters.get(“group\_by\_item”) — true gives mapping(), false gives get\_so\_elapsed\_time(data).
- If not data.
  - Return tuple(list(), list(), no value, list()).
- Set tuple(data, chart\_data) from prepare\_data(data, so\_elapsed\_time, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L121)

<a id="op-5fedfe2a96d8ba"></a>
### Validate filters

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “From and To Dates are required.” · validation helper — translated “Group the report by Sales Order or by Item, not both.”.

**Local steps**

- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- Set tuple(from\_date, to\_date) from tuple(filters.get(“from\_date”), filters.get(“to\_date”)).
- Evaluate validate\_date\_range(mapping(“from\_date” → getdate(from\_date), “to\_date” → getdate(to\_date))).
- If (not from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_date → to\_date.
  - Call the validation error handler Platform.throw(translated “From and To Dates are required.”).
- If (filters.get(“group\_by\_so”) and filters.get(“group\_by\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“group\_by\_so”) → filters.get(“group\_by\_item”).
  - Call the validation error handler Platform.throw(translated “Group the report by Sales Order or by Item, not both.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L127)

<a id="op-599f2f10d6c582"></a>
### Get data

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_get_data`

**Inputs** filters.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set permitted\_orders from get\_permitted\_sales\_orders(filters).
- If not permitted\_orders.
  - Return list().
- Set so from qb.DocType(“Sales Order”).
- Set soi from qb.DocType(“Sales Order Item”).
- Set sii from qb.DocType(“Sales Invoice Item”).
- Set si from qb.DocType(“Sales Invoice”).
- Set datediff from CustomFunction(“DATEDIFF”, list(“end\_date”, “start\_date”)).
- Set delay from datediff(nowdate(), soi.delivery\_date).
- Set conversion\_rate from Coalesce(so.conversion\_rate, 1).
- Set is\_closed from so.status equals “Closed”.
- Set no\_delay from so.status.isin(list(“Completed”, “To Bill”, “Closed”)).
- Set counts\_as\_billed from (Coalesce(si.is\_return, 0) equals 0 bitwise or Coalesce(si.update\_billed\_amount\_in\_sales\_order, 0) equals 1).
- Set query from nested operand in the contract(nested operand in the contract).groupby(soi.name, so.name).orderby(so.transaction\_date).orderby(soi.item\_code).
- If filters.get(“warehouse”).
  - Set warehouses from list(expanded get\_descendants\_of(“Warehouse”, filters.get(“warehouse”)), filters.get(“warehouse”)).
  - Set query from query.where(soi.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L123)

<a id="op-df6f5e03f68433"></a>
### Get permitted sales orders

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_permitted_sales_orders`

**Inputs** filters.

**Explicit results** Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Local steps**

- Set so\_filters from list(list(“Sales Order”, “docstatus”, “=”, 1), list(“Sales Order”, “company”, “=”, filters.get(“company”)), list(“Sales Order”, “status”, “not in”, list(“Stopped”, “On Hold”))).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Evaluate so\_filters.append(list(“Sales Order”, “transaction\_date”, “between”, list(filters.get(“from\_date”), filters.get(“to\_date”)))).
- If filters.get(“sales\_order”).
  - Evaluate so\_filters.append(list(“Sales Order”, “name”, “in”, filters.get(“sales\_order”))).
- If filters.get(“status”).
  - Evaluate so\_filters.append(list(“Sales Order”, “status”, “in”, filters.get(“status”))).
- Return Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L127)

<a id="op-8064c52300060f"></a>
### Get so elapsed time

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_get_sales_order_elapsed_time`

**Inputs** data.

**Explicit results** so\_elapsed\_time.

**Local steps**

- Set so\_elapsed\_time from OrderedDict().
- If data.
  - Set sales\_orders from list of x.sales\_order for x drawn from data.
    - Draw x from data.
  - Set so from qb.DocType(“Sales Order”).
  - Set soi from qb.DocType(“Sales Order Item”).
  - Set dn from qb.DocType(“Delivery Note”).
  - Set dni from qb.DocType(“Delivery Note Item”).
  - If Platform.db.db\_type equals “postgres”.
    - Set elapsed\_seconds from ((Max(dn.posting\_date) − so.transaction\_date) × 86400).as\_(“elapsed\_seconds”).
  - Otherwise.
    - Set to\_seconds from CustomFunction(“TO\_SECONDS”, list(“date”)).
    - Set elapsed\_seconds from (to\_seconds(Max(dn.posting\_date)) − to\_seconds(so.transaction\_date)).as\_(“elapsed\_seconds”).
  - Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise  ….
  - Set dn\_elapsed\_time from query.run(as\_dict = true).
  - For each e in dn\_elapsed\_time.
    - Set key from tuple(e.sales\_order, e.so\_item\_code).
    - Set so\_elapsed\_time at key from e.elapsed\_seconds.
- Return so\_elapsed\_time.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0672.json#L2904) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L124)

<a id="op-5c89d17c97a967"></a>
### Prepare data

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_prepare_data`

**Inputs** data, so\_elapsed\_time, filters.

**Explicit results** tuple(data, chart\_data).

**Local steps**

- Set tuple(completed, pending) from tuple(0, 0).
- For each row in data.
  - Update completed using + row at “billed\_amount”.
  - Update pending using + row at “pending\_amount”.
  - Set row at “qty\_to\_bill” from 0 when row at “status” equals “Closed”, otherwise (flt(row at “qty”) − flt(row at “billed\_qty”)).
    - Value choice on row at “status” equals “Closed” — true gives 0, false gives (flt(row at “qty”) − flt(row at “billed\_qty”)).
  - Set row at “delay” from 0 when (row at “delay” and row at “delay” &lt; 0), otherwise row at “delay”.
    - Value choice on (row at “delay” and row at “delay” &lt; 0) — true gives 0, false gives row at “delay”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row at “delay” → row at “delay” &lt; 0.
  - Set row at “time\_taken\_to\_deliver” from so\_elapsed\_time.get(tuple(row.sales\_order, row.item\_code)) when row at “status” belongs to tuple(“To Bill”, “Completed”), otherwise 0.
    - Value choice on row at “status” belongs to tuple(“To Bill”, “Completed”) — true gives so\_elapsed\_time.get(tuple(row.sales\_order, row.item\_code)), false gives 0.
- Set chart\_data from prepare\_chart\_data(pending, completed).
- If filters.get(“group\_by\_so”).
  - Set data from group\_by\_sales\_order(data).
- Otherwise.
  - If filters.get(“group\_by\_item”).
    - Set data from group\_by\_item(data).
- Return tuple(data, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L126)

<a id="op-feb9525dfbe059"></a>
### Group by sales order

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_group_by_sales_order`

**Inputs** data.

**Explicit results** list(sales\_order\_map.values()).

**Local steps**

- Set sales\_order\_map from mapping().
- For each row in data.
  - Set group from sales\_order\_map.get(row at “sales\_order”).
  - If not group.
    - Set sales\_order\_map at row at “sales\_order” from copy.deepcopy(row).
    - Continue with the next iteration or loop test.
  - Set group at “delay” from least\_delay(group at “delay”, row at “delay”).
  - Evaluate add\_aggregated\_fields(group, row).
- Return list(sales\_order\_map.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L133)

<a id="op-66dea03c40246d"></a>
### Least delay

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_least_delay`

**Inputs** remaining positional values delays.

**Explicit results** min(overdue) when overdue, otherwise 0.

**Local steps**

- Set overdue from list of d for d drawn from delays where d.
  - Draw d from delays, keep a combination only if (d).
- Return min(overdue) when overdue, otherwise 0.
  - Value choice on overdue — true gives min(overdue), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L134)

<a id="op-5d9d896d5318f3"></a>
### Group by item

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_group_by_item`

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

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L132)

<a id="op-29f87db550fb48"></a>
### Add aggregated fields

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_add_aggregated_fields`

**Inputs** group, row.

**Local steps**

- For each field in AGGREGATED\_FIELDS.
  - Set group at field from (flt(group at field) + flt(row at field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L120)

<a id="op-14fa5edde7c4cb"></a>
### Prepare chart data

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_prepare_chart_data`

**Inputs** pending, completed.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“values” → list(pending, completed)))), “type” → “donut”, “height” → 300).

**Local steps**

- Set labels from list(translated “Amount to Bill”, translated “Billed Amount”).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“values” → list(pending, completed)))), “type” → “donut”, “height” → 300).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0672.json#L4891) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L125)

<a id="op-395258bb5b89d6"></a>
### Get columns

`operation_enterprise_selling_report_sales_order_analysis_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** get\_grouped\_by\_item\_columns() · columns.

**Local steps**

- If filters.get(“group\_by\_item”).
  - Return get\_grouped\_by\_item\_columns().
- Set columns from get\_sales\_order\_columns().
- If not filters.get(“group\_by\_so”).
  - Update columns using + get\_item\_columns().
- Update columns using + ((get\_quantity\_columns() + get\_amount\_columns()) + get\_delivery\_columns()).
- If not filters.get(“group\_by\_so”).
  - Evaluate columns.append(get\_warehouse\_column()).
- Evaluate columns.append(get\_company\_column()).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L122)

<a id="op-1eed99187d48d6"></a>
### Get grouped by item columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_grouped_by_item_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(get\_item\_code\_column(), get\_uom\_column()).
- Update columns using + (get\_quantity\_columns() + get\_amount\_columns()).
- Evaluate columns.append(get\_company\_column()).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L124)

<a id="op-49560734996f57"></a>
### Get sales order columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_sales_order_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Date”, “width” → 90), mapping(“label” → translated “Sales Order”, “fieldname” → “sales\_order”, “fieldtype” → “Link”, “options” ….

**Local steps**

- Return list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Date”, “width” → 90), mapping(“label” → translated “Sales Order”, “fieldname” → “sales\_order”, “fieldtype” → “Link”, “options” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L129)

<a id="op-9a52fc25733911"></a>
### Get item columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_item_columns`

**Inputs** no declared parameters.

**Explicit results** list(get\_item\_code\_column(), mapping(“label” → translated “Description”, “fieldname” → “description”, “fieldtype” → “Small Text”, “width” → 100)).

**Local steps**

- Return list(get\_item\_code\_column(), mapping(“label” → translated “Description”, “fieldname” → “description”, “fieldtype” → “Small Text”, “width” → 100)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L126)

<a id="op-99ede84531c6d9"></a>
### Get item code column

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_item_code_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …).

**Local steps**

- Return mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L125)

<a id="op-c2d1ba4c955114"></a>
### Get uom column

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_uom_column`

**Inputs** no declared parameters.

**Explicit results** mapping(“label” → translated “UOM”, “fieldname” → “uom”, “fieldtype” → “Link”, “options” → “UOM”, …).

**Local steps**

- Return mapping(“label” → translated “UOM”, “fieldname” → “uom”, “fieldtype” → “Link”, “options” → “UOM”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L130)

<a id="op-a8dba66caa643f"></a>
### Get quantity columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_quantity_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 120, …), mapping(“label” → translated “Delivered Qty”, “fieldname” → “delivered\_qty”, “fieldtype” → “Float”, “ ….

**Local steps**

- Return list(mapping(“label” → translated “Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 120, …), mapping(“label” → translated “Delivered Qty”, “fieldname” → “delivered\_qty”, “fieldtype” → “Float”, “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L128)

<a id="op-1743d60573cdba"></a>
### Get amount columns

`operation_enterprise_binding_enterprise_selling_report_sales_order_analysis_sales_order_analysis_get_amount_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Amount”, “fieldname” → “amount”, “fieldtype” → “Currency”, “width” → 110, …), mapping(“label” → translated “Billed Amount”, “fieldname” → “billed\_amount”, “fieldtype” → “ ….

**Local steps**

- Return list(mapping(“label” → translated “Amount”, “fieldname” → “amount”, “fieldtype” → “Currency”, “width” → 110, …), mapping(“label” → translated “Billed Amount”, “fieldname” → “billed\_amount”, “fieldtype” → “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L121)
