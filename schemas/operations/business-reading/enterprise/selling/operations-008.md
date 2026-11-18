# Sales · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Party specific item

[Record definition](../../../../data/record-types/party_specific_item.json)

<a id="op-295f240d9e440e"></a>
### Get items ranked by orders

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_items_ranked_by_orders`

**Inputs** party\_type, party, filters, or\_filters, fields, start, page\_length.

**Record and data access** read “Item” via get\_list.

**Explicit results** page.

**Local steps**

- Set history from mapping().
- If Platform.has\_permission(ORDER\_DOCTYPES at party\_type, “read”).
  - Set history from mapping of row.item\_code → row for row drawn from get\_order\_history(party\_type, party).
    - Draw row from get\_order\_history(party\_type, party).
- Set rank from mapping of item\_code → idx for tuple(idx, item\_code) drawn from enumerate(history).
  - Draw tuple(idx, item\_code) from enumerate(history).
- Set ordered from Platform.get\_list(“Item”, filters = list(expanded filters, list(“Item”, “name”, “in”, (list(history) or list(empty text)))), or\_filters = or\_filters, fields = fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(history) → list(empty text).
- Evaluate ordered.sort(key = deferred anonymous expression).
- Set page from ordered at slice start to (start + page\_length).
- If len(page) &lt; page\_length.
  - Set not\_ordered from list(expanded filters, list(“Item”, “name”, “not in”, list(history))) when history, otherwise filters.
    - Value choice on history — true gives list(expanded filters, list(“Item”, “name”, “not in”, list(history))), false gives filters.
  - Update page using + Platform.get\_list(“Item”, filters = not\_ordered, or\_filters = or\_filters, fields = fields, order\_by = “′tabItem′.item\_name asc”, …).
- For each item in page.
  - Set row from history.get(item.name).
  - Set item.order\_count from row.order\_count when row, otherwise 0.
    - Value choice on row — true gives row.order\_count, false gives 0.
  - Set item.last\_ordered from row.last\_ordered when row, otherwise no value.
    - Value choice on row — true gives row.last\_ordered, false gives no value.
- Return page.

**Values supplied outside this operation** effective access from Platform.has\_permission(ORDER\_DOCTYPES at party\_type, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1484)

<a id="op-8457a1d7177093"></a>
### Get order history

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_order_history`

**Inputs** party\_type, party, limit = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set order\_doctype from ORDER\_DOCTYPES at party\_type.
- Set party\_field from Platform.scrub(party\_type).
- Set permitted\_orders from Platform.qb.get\_query(order\_doctype, fields = list(“name”), filters = mapping(party\_field → party, “docstatus” → 1), ignore\_permissions = false).
- Set permitted\_items from Platform.qb.get\_query(“Item”, fields = list(“name”), ignore\_permissions = false).
- Set order from Platform.qb.DocType(order\_doctype).
- Set order\_item from Platform.qb.DocType(formatted text {order\_doctype} Item).
- Set order\_count from Count(order.name).distinct().
- Set last\_ordered from Max(order.transaction\_date).
- Set query from nested operand in the contract(nested operand in the contract).orderby(order\_count, order = Order.desc).orderby(last\_ordered, order = Order.desc).orderby(order\_item.item\_code).
- If limit.
  - Set query from query.limit(limit).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1486)

<a id="op-15d6687ee0f50a"></a>
### Get order hint

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_order_hint`

**Inputs** party\_type, item.

**Explicit results** translated “Not bought from this supplier yet” · translated “Bought once, on {0}”.format(formatdate(item.last\_ordered)) · translated “Bought {0} times, last on {1}”.format(item.order\_count, formatdate(item.last\_ordered)) · translated “Not ordered by this customer yet” · translated “Ordered once, on {0}”.format(formatdate(item.last\_ordered)) · 1 additional forms in the steps below.

**Local steps**

- If party\_type equals “Supplier”.
  - If not item.order\_count.
    - Return translated “Not bought from this supplier yet”.
  - If item.order\_count equals 1.
    - Return translated “Bought once, on {0}”.format(formatdate(item.last\_ordered)).
  - Return translated “Bought {0} times, last on {1}”.format(item.order\_count, formatdate(item.last\_ordered)).
- If not item.order\_count.
  - Return translated “Not ordered by this customer yet”.
- If item.order\_count equals 1.
  - Return translated “Ordered once, on {0}”.format(formatdate(item.last\_ordered)).
- Return translated “Ordered {0} times, last on {1}”.format(item.order\_count, formatdate(item.last\_ordered)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1485)

<a id="op-e8ac125a5ac543"></a>
### Count rule items

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_count_rule_items`

**Inputs** rules.

**Explicit results** counts.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set permitted\_items from Platform.qb.get\_query(“Item”, fields = list(“name”), filters = mapping(“disabled” → 0), ignore\_permissions = false).
- Set brands from list of rule.based\_on\_value for rule drawn from rules where rule.restrict\_based\_on equals “Brand”.
  - Draw rule from rules, keep a combination only if (rule.restrict\_based\_on equals “Brand”).
- Set groups from list of rule.based\_on\_value for rule drawn from rules where rule.restrict\_based\_on equals “Item Group”.
  - Draw rule from rules, keep a combination only if (rule.restrict\_based\_on equals “Item Group”).
- Set counts from mapping().
- If brands.
  - Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contra ….run().
  - Evaluate counts.update(mapping of tuple(“Brand”, brand) → count for tuple(brand, count) drawn from rows).
    - Draw tuple(brand, count) from rows.
- If groups.
  - Set group from Platform.qb.DocType(“Item Group”).
  - Set parent from Platform.qb.DocType(“Item Group”).as\_(“parent\_group”).
  - Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contra ….run().
  - Evaluate counts.update(mapping of tuple(“Item Group”, name) → count for tuple(name, count) drawn from rows).
    - Draw tuple(name, count) from rows.
- Return counts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1479)

## Report · Payment terms status for sales order

<a id="op-7026deebb477f1"></a>
### Get columns

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Sales Order”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Sales Order”), mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Li ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0665.json#L3612) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L48)

<a id="op-ad2fb64b68dc76"></a>
### Get descendants of

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_get_descendants_of`

**Inputs** doctype, group\_name.

**Explicit results** child\_nodes.

**Local steps**

- Set group\_doc from qb.DocType(doctype).
- Set tuple(lft, rgt) from nested operand in the contract.select(nested operand in the contract.lft, nested operand in the contract.rgt).where(group\_doc.name equals group\_name).run() at 0.
- Set query from qb.from\_(group\_doc).select(group\_doc.name).where((group\_doc.lft ≥ lft bitwise and group\_doc.rgt ≤ rgt)).
- Set child\_nodes from list().
- For each x in query.run().
  - Evaluate child\_nodes.append(x at 0).
- Return child\_nodes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0665.json#L4660) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L51)

<a id="op-dd2944860b4574"></a>
### Get customers or items

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_get_customers_or_items`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** Platform.desk.reportview.execute(doctype, filters = filter\_list, fields = list(“name”, “customer\_group”) when doctype equals “Customer”, otherwise list(“name”, “item\_group”), limit\_start = start, limit\_pag ….

**Local steps**

- Set filter\_list from list().
- If isinstance(filters, list).
  - For each item in filters.
    - If item at 0 equals doctype.
      - Evaluate filter\_list.append(item).
    - Otherwise.
      - If item at 0 equals “Customer Group”.
        - If item at 3 differs from empty text.
          - Evaluate filter\_list.append(list(doctype, “customer\_group”, “in”, get\_descendants\_of(“Customer Group”, item at 3))).
      - Otherwise.
        - If item at 0 equals “Item Group”.
          - If item at 3 differs from empty text.
            - Evaluate filter\_list.append(list(doctype, “item\_group”, “in”, get\_descendants\_of(“Item Group”, item at 3))).
- If (searchfield and txt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in searchfield → txt.
  - Evaluate filter\_list.append(list(doctype, searchfield, “like”, (“%%%s%%” modulo or format txt))).
- Return Platform.desk.reportview.execute(doctype, filters = filter\_list, fields = list(“name”, “customer\_group”) when doctype equals “Customer”, otherwise list(“name”, “item\_group”), limit\_start = start, limit\_pag ….
  - Value choice on doctype equals “Customer” — true gives list(“name”, “customer\_group”), false gives list(“name”, “item\_group”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L50)

<a id="op-06168b8244c298"></a>
### Get conditions

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set filters from Platform.\_dict(filters) when filters, otherwise Platform.\_dict(mapping()).
  - Value choice on filters — true gives Platform.\_dict(filters), false gives Platform.\_dict(mapping()).
- Set conditions from Platform.\_dict(mapping()).
- Set conditions.company from (filters.company or Platform.defaults.get\_user\_default(“company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.company → Platform.defaults.get\_user\_default(“company”).
- Set conditions.end\_date from (filters.period\_end\_date or Platform.utils.today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.period\_end\_date → Platform.utils.today().
- Set conditions.start\_date from (filters.period\_start\_date or Platform.utils.add\_months(conditions.end\_date, negative 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.period\_start\_date → Platform.utils.add\_months(conditions.end\_date, negative 1).
- Return conditions.

**Values supplied outside this operation** clock or generated value from Platform.utils.today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0665.json#L5757) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L49)

<a id="op-10182e2560d707"></a>
### Build filter criterions

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_build_filter_criterions`

**Inputs** filters.

**Explicit results** qb\_criterions.

**Local steps**

- Set filters from Platform.\_dict(filters) when filters, otherwise Platform.\_dict(mapping()).
  - Value choice on filters — true gives Platform.\_dict(filters), false gives Platform.\_dict(mapping()).
- Set qb\_criterions from list().
- If filters.customer\_group.
  - Evaluate qb\_criterions.append(qb.DocType(“Sales Order”).customer\_group.isin(get\_descendants\_of(“Customer Group”, filters.customer\_group))).
- If filters.customer.
  - Evaluate qb\_criterions.append(qb.DocType(“Sales Order”).customer equals filters.customer).
- If filters.item\_group.
  - Evaluate qb\_criterions.append(qb.DocType(“Sales Order Item”).item\_group.isin(get\_descendants\_of(“Item Group”, filters.item\_group))).
- If filters.item.
  - Evaluate qb\_criterions.append(qb.DocType(“Sales Order Item”).item\_code equals filters.item).
- If filters.from\_due\_date.
  - Evaluate qb\_criterions.append(qb.DocType(“Payment Schedule”).due\_date.gte(filters.from\_due\_date)).
- If filters.to\_due\_date.
  - Evaluate qb\_criterions.append(qb.DocType(“Payment Schedule”).due\_date.lte(filters.to\_due\_date)).
- Return qb\_criterions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0665.json#L6050) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L44)

<a id="op-e187c570f10a9a"></a>
### Get so with invoices

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_get_sales_order_with_invoices`

**Inputs** filters.

**Explicit results** tuple(sorders, invoices).

**Local steps**

- Set sorders from list().
- Set so from qb.DocType(“Sales Order”).
- Set ps from qb.DocType(“Payment Schedule”).
- Set soi from qb.DocType(“Sales Order Item”).
- Set conditions from get\_conditions(filters).
- Set filter\_criterions from build\_filter\_criterions(filters).
- Set datediff from query\_builder.CustomFunction(“DATEDIFF”, list(“cur\_date”, “due\_date”)).
- Set ifelse from query\_builder.CustomFunction(“IF”, list(“condition”, “then”, “else”)).
- Set query\_so from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“Sales Order”).
  - Set query\_so from query\_so.where(Bracket(LiteralValue(match\_conditions))).
- Set sorders from query\_so.run(as\_dict = true).
- Set invoices from list().
- If sorders differs from list().
  - Set soi from qb.DocType(“Sales Order Item”).
  - Set si from qb.DocType(“Sales Invoice”).
  - Set sii from qb.DocType(“Sales Invoice Item”).
  - Set query\_inv from nested operand in the contract(nested operand in the contract).select(sii.sales\_order, nested operand in the contract.as\_(“invoice”), nested operand in the contract.as\_(“invoice\_amount”)).where((nested ope ….
    - Draw x from sorders.
  - Set invoices from query\_inv.run(as\_dict = true).
- Return tuple(sorders, invoices).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L52)

<a id="op-d3934ab25b6268"></a>
### Set payment terms statuses

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_set_payment_terms_statuses`

**Inputs** sales\_orders, invoices, filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(sales\_orders, invoices).

**Local steps**

- For each so in sales\_orders.
  - Set so.currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
  - Set so.invoices from empty text.
  - For each inv in list of x for x drawn from invoices where (x.sales\_order equals so.name and x.invoice\_amount &gt; 0).
    - Draw x from invoices, keep a combination only if ((x.sales\_order equals so.name and x.invoice\_amount &gt; 0)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in x.sales\_order equals so.name → x.invoice\_amount &gt; 0.
    - If (so.base\_payment\_amount − so.paid\_amount) &gt; 0.
      - Set amount from (so.base\_payment\_amount − so.paid\_amount).
      - If inv.invoice\_amount ≥ amount.
        - Update inv.invoice\_amount using − amount.
        - Update so.paid\_amount using + amount.
        - Update so.invoices using + (“,” + inv.invoice).
        - Set so.status from “Completed”.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Otherwise.
        - Update so.paid\_amount using + inv.invoice\_amount.
        - Set inv.invoice\_amount from 0.
        - Update so.invoices using + (“,” + inv.invoice).
        - Set so.status from “Partly Paid”.
- Return tuple(sales\_orders, invoices).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0666.json#L1888) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L54)

<a id="op-4224a9025601de"></a>
### Prepare chart

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_prepare_chart`

**Inputs** s\_orders.

**Explicit results** chart.

**Local steps**

- If len(set(list of x.name for x drawn from s\_orders)) equals 1.
  - Draw x from s\_orders.
  - Set chart from mapping(“data” → mapping(“labels” → list of term.payment\_term for term drawn from s\_orders, “datasets” → list(mapping(“name” → translated “Payment Amount”, “values” → list of x.base\_payment\_amount for x dr ….
    - Draw term from s\_orders.
    - Draw x from s\_orders.
    - Draw x from s\_orders.
  - Return chart.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0666.json#L2395) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L53)

<a id="op-9a9c7c70eb4d04"></a>
### Filter on calculated status

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_filter_on_calculated_status`

**Inputs** filters, sales\_orders.

**Explicit results** list of x for x drawn from sales\_orders where x.status belongs to filters.status · sales\_orders.

**Local steps**

- If (filters.status and sales\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.status → sales\_orders.
  - Return list of x for x drawn from sales\_orders where x.status belongs to filters.status.
    - Draw x from sales\_orders, keep a combination only if (x.status belongs to filters.status).
- Return sales\_orders.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0666.json#L2731) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L47)

<a id="op-90e9979e796055"></a>
### Filter for immediate upcoming term

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_filter_for_immediate_upcoming_term`

**Inputs** filters, sales\_orders.

**Explicit results** filtered\_data · sales\_orders.

**Local steps**

- If (filters.only\_immediate\_upcoming\_term and sales\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.only\_immediate\_upcoming\_term → sales\_orders.
  - Set immediate\_term\_found from set().
  - Set filtered\_data from list().
  - For each order in sales\_orders.
    - If (order.name does not belong to immediate\_term\_found and order.due\_date &gt; getdate()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in order.name does not belong to immediate\_term\_found → order.due\_date &gt; getdate().
      - Evaluate filtered\_data.append(order).
      - Evaluate immediate\_term\_found.add(order.name).
  - Return filtered\_data.
- Return sales\_orders.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0666.json#L2849) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L46)

<a id="op-7361fc75f523e8"></a>
### Execute

`operation_enterprise_selling_report_payment_terms_status_for_sales_order_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, message, chart).

**Local steps**

- Evaluate validate\_date\_range(filters, “period\_start\_date”, “period\_end\_date”).
- Evaluate validate\_date\_range(filters, “from\_due\_date”, “to\_due\_date”).
- Set columns from get\_columns().
- Set tuple(sales\_orders, so\_invoices) from get\_so\_with\_invoices(filters).
- Set tuple(sales\_orders, so\_invoices) from set\_payment\_terms\_statuses(sales\_orders, so\_invoices, filters).
- Set sales\_orders from filter\_on\_calculated\_status(filters, sales\_orders).
- Set sales\_orders from filter\_for\_immediate\_upcoming\_term(filters, sales\_orders).
- Evaluate prepare\_chart(sales\_orders).
- Set data from sales\_orders.
- Set message from list().
- Set chart from prepare\_chart(sales\_orders).
- Return tuple(columns, data, message, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L45)

## Report · Pending so items for purchase request

<a id="op-af0a42602db9a0"></a>
### Execute

`operation_enterprise_selling_report_pending_sales_order_items_for_purchase_request_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L61)

<a id="op-465d5388e8f139"></a>
### Get columns

`operation_enterprise_selling_report_pending_sales_order_items_for_purchase_request_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “options” → “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “options” → “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “fieldtype” → “D ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L62)

<a id="op-fa7c35817d54ad"></a>
### Get data

`operation_enterprise_selling_report_pending_sales_order_items_for_purchase_request_business_behavior_get_data`

**Inputs** filters.

**Explicit results** list() · pending.

**Local steps**

- Set permitted\_orders from get\_permitted\_sales\_orders(filters).
- If not permitted\_orders.
  - Return list().
- Set so from Platform.qb.DocType(“Sales Order”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set so\_items from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.isin(p ….
- Set packed\_item\_map from get\_packed\_items(permitted\_orders).
- Set tuple(requested\_by\_so\_item, requested\_by\_packed\_item, requested\_by\_item) from get\_requested\_qty(permitted\_orders).
- Set groups from mapping().
- For each row in so\_items.
  - Set packed\_rows from packed\_item\_map.get(tuple(row.sales\_order, row.so\_item)).
  - If packed\_rows.
    - For each packed in packed\_rows.
      - Set delivered from (flt(row.delivered\_qty) × (flt(packed.qty) ÷ flt(row.qty))) when row.qty, otherwise 0.
        - Value choice on row.qty — true gives (flt(row.delivered\_qty) × (flt(packed.qty) ÷ flt(row.qty))), false gives 0.
      - Set linked from (requested\_by\_packed\_item.get(packed.name) or mapping()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in requested\_by\_packed\_item.get(packed.name) → mapping().
      - Set line from build\_line(row, packed, flt(packed.qty), delivered, is\_packed = true, …).
      - Evaluate groups.setdefault(tuple(row.sales\_order, packed.item\_code), list()).append(line).
  - Otherwise.
    - Set linked from (requested\_by\_so\_item.get(row.so\_item) or mapping()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in requested\_by\_so\_item.get(row.so\_item) → mapping().
    - Set line from build\_line(row, row, flt(row.qty), flt(row.delivered\_qty), is\_packed = false, …).
    - Evaluate groups.setdefault(tuple(row.sales\_order, row.item\_code), list()).append(line).
- Set pending from list().
- For each tuple(key, lines) in groups.items().
  - Evaluate allocate\_requests(pending, lines, (requested\_by\_item.get(key) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in requested\_by\_item.get(key) → mapping().
- Return pending.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L63)

<a id="op-f117d1d9ee5d8d"></a>
### Build line

`operation_enterprise_binding_enterprise_selling_report_pending_so_items_for_purchase_request_pending_so_items_for_purchase_request_build_line`

**Inputs** so\_row, item\_row, ordered\_qty, delivered\_qty, linked, is\_packed.

**Explicit results** Platform.\_dict(so\_row = so\_row, item\_row = item\_row, ordered\_qty = ordered\_qty, delivered\_qty = delivered\_qty, …).

**Local steps**

- Return Platform.\_dict(so\_row = so\_row, item\_row = item\_row, ordered\_qty = ordered\_qty, delivered\_qty = delivered\_qty, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L114)

<a id="op-24dcbbddd8f885"></a>
### Allocate requests

`operation_enterprise_binding_enterprise_selling_report_pending_so_items_for_purchase_request_pending_so_items_for_purchase_request_allocate_requests`

**Inputs** pending, lines, bucket.

**Local steps**

- Set bucket\_qty from flt(bucket.get(“qty”)).
- Set bucket\_requests from list(bucket.get(“material\_requests”, list())).
- For each line in sorted(lines, key = deferred anonymous expression).
  - Set line\_pending from ((line.ordered\_qty − line.delivered\_qty) − line.requested\_qty).
  - If line\_pending ≤ 0.
    - Continue with the next iteration or loop test.
  - Set allocated from min(line\_pending, bucket\_qty).
  - If allocated &gt; 0.
    - Update bucket\_qty using − allocated.
    - Update line.requested\_qty using + allocated.
    - Update line\_pending using − allocated.
    - Update line.material\_requests using + list of mr for mr drawn from bucket\_requests where mr does not belong to line.material\_requests.
      - Draw mr from bucket\_requests, keep a combination only if (mr does not belong to line.material\_requests).
  - If line\_pending &gt; 0.
    - Evaluate add\_pending\_row(pending, line.so\_row, line.item\_row, line.ordered\_qty, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L113)

<a id="op-6c717313140fc3"></a>
### Add pending row

`operation_enterprise_binding_enterprise_selling_report_pending_so_items_for_purchase_request_pending_so_items_for_purchase_request_add_pending_row`

**Inputs** pending, so\_row, item\_row, ordered\_qty, delivered\_qty, requested.

**Explicit results** no value.

**Local steps**

- Set requested\_qty from flt(requested.get(“qty”)).
- Set pending\_qty from ((ordered\_qty − requested\_qty) − delivered\_qty).
- <a id="op-6c717313140fc3-guard-4"></a>If pending\_qty ≤ 0.
  - Return no value.
- Evaluate pending.append(mapping(“item\_code” → item\_row.item\_code, “item\_name” → item\_row.item\_name, “description” → item\_row.description, “sales\_order\_no” → so\_row.sales\_order, …)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison pending\_qty ≤ 0, pending\_qty = 0 selects the branch that returns no value. With pending\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6c717313140fc3-guard-4)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L112)

<a id="op-b9fb23879a9e0e"></a>
### Get permitted sales orders

`operation_enterprise_binding_enterprise_selling_report_pending_so_items_for_purchase_request_pending_so_items_for_purchase_request_get_permitted_sales_orders`

**Inputs** filters.

**Explicit results** Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Local steps**

- Set so\_filters from mapping(“docstatus” → 1, “status” → list(“not in”, list(“Closed”, “Completed”, “Cancelled”))).
- If filters.get(“company”).
  - Set so\_filters at “company” from filters.company.
- If filters.get(“customer”).
  - Set so\_filters at “customer” from filters.customer.
- If filters.get(“sales\_order”).
  - Set so\_filters at “name” from filters.sales\_order.
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set so\_filters at “transaction\_date” from list(“between”, list(filters.from\_date, filters.to\_date)).
- Otherwise.
  - If filters.get(“from\_date”).
    - Set so\_filters at “transaction\_date” from list(“&gt;=”, filters.from\_date).
  - Otherwise.
    - If filters.get(“to\_date”).
      - Set so\_filters at “transaction\_date” from list(“&lt;=”, filters.to\_date).
- Return Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L115)

<a id="op-29a9b8bb6fbbbe"></a>
### Get requested qty

`operation_enterprise_binding_enterprise_selling_report_pending_so_items_for_purchase_request_pending_so_items_for_purchase_request_get_requested_qty`

**Inputs** sales\_orders.

**Record and data access** read “Material Request Item” via get\_all.

**Explicit results** tuple(by\_so\_item, by\_packed\_item, by\_item).

**Local steps**

- Set by\_so\_item from mapping().
- Set by\_packed\_item from mapping().
- Set by\_item from mapping().
- For each mr in Platform.get\_all(“Material Request Item”, filters = mapping(“sales\_order” → tuple(“in”, sales\_orders), “docstatus” → 1), fields = list(“parent”, “qty”, “item\_code”, “sales\_order”, …)).
  - If mr.packed\_item.
    - Set tuple(target, key) from tuple(by\_packed\_item, mr.packed\_item).
  - Otherwise.
    - If mr.sales\_order\_item.
      - Set tuple(target, key) from tuple(by\_so\_item, mr.sales\_order\_item).
    - Otherwise.
      - Set tuple(target, key) from tuple(by\_item, tuple(mr.sales\_order, mr.item\_code)).
  - Set entry from target.setdefault(key, mapping(“qty” → 0, “material\_requests” → list())).
  - Update entry at “qty” using + flt(mr.qty).
  - If mr.parent does not belong to entry at “material\_requests”.
    - Evaluate entry at “material\_requests”.append(mr.parent).
- Return tuple(by\_so\_item, by\_packed\_item, by\_item).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L116)

<a id="op-ccc0deb9568d92"></a>
### Get packed items

`operation_enterprise_selling_report_pending_sales_order_items_for_purchase_request_business_behavior_get_packed_items`

**Inputs** sales\_orders.

**Record and data access** read “Packed Item” via get\_all.

**Explicit results** packed\_item\_map.

**Local steps**

- Set packed\_item\_map from mapping().
- For each d in Platform.get\_all(“Packed Item”, filters = mapping(“parent” → tuple(“in”, sales\_orders)), fields = list(“name”, “parent”, “parent\_detail\_docname”, “item\_code”, …)).
  - Evaluate packed\_item\_map.setdefault(tuple(d.parent, d.parent\_detail\_docname), list()).append(d).
- Return packed\_item\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L64)
